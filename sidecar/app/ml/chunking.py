import ast
import re
from langchain_text_splitters import RecursiveCharacterTextSplitter

def chunk_prose(text: str, chunk_size: int = 1500) -> list[str]:
    """
    Slices prose text into optimal chunks using LangChain's RecursiveCharacterTextSplitter.
    Includes a 15% overlap buffer.
    """
    overlap_size = int(chunk_size * 0.15)
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=overlap_size,
        length_function=len,
        separators=["\n\n", "\n", " ", ""]
    )
    return text_splitter.split_text(text)

def split_python_code_by_ast(code: str) -> list[str]:
    """
    Parses Python code using the AST module to split along class and function definitions.
    Falls back to raw split if syntax is invalid.
    """
    try:
        root = ast.parse(code)
    except SyntaxError:
        return [code]
        
    lines = code.splitlines()
    top_level_nodes = []
    
    for node in root.body:
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
            start_line = node.lineno - 1
            end_line = getattr(node, "end_lineno", len(lines))
            top_level_nodes.append((start_line, end_line))
            
    chunks = []
    current_chunk = []
    line_idx = 0
    
    while line_idx < len(lines):
        in_node = False
        for start, end in top_level_nodes:
            if start <= line_idx < end:
                in_node = True
                if current_chunk:
                    chunks.append("\n".join(current_chunk))
                    current_chunk = []
                chunks.append("\n".join(lines[start:end]))
                line_idx = end
                break
        if not in_node:
            current_chunk.append(lines[line_idx])
            line_idx += 1
            
    if current_chunk:
        chunks.append("\n".join(current_chunk))
        
    return chunks

def split_braced_code(code: str, language: str) -> list[str]:
    """
    Splits braced programming languages (JS, TS, Go, Rust, C++) by identifying top-level block boundaries.
    """
    lines = code.splitlines()
    chunks = []
    current_chunk = []
    
    brace_count = 0
    in_block = False
    block_lines = []
    
    # Identify common class, function, struct, interface boundaries
    block_start_regex = re.compile(
        r'^\s*(export\s+|async\s+)*(class|function|func|fn|struct|interface|const\s+\w+\s*=\s*(\(.*?\)|async\s*\(.*?\))\s*=>)\b'
    )
    
    for line in lines:
        if not in_block:
            if block_start_regex.search(line) and "{" in line:
                in_block = True
                brace_count = line.count("{") - line.count("}")
                block_lines = [line]
                if brace_count == 0:
                    in_block = False
                    current_chunk.extend(block_lines)
            else:
                current_chunk.append(line)
        else:
            block_lines.append(line)
            brace_count += line.count("{") - line.count("}")
            if brace_count <= 0:
                in_block = False
                if current_chunk:
                    chunks.append("\n".join(current_chunk))
                    current_chunk = []
                chunks.append("\n".join(block_lines))
                block_lines = []
                
    if current_chunk:
        chunks.append("\n".join(current_chunk))
    if block_lines:
        chunks.append("\n".join(block_lines))
        
    return chunks

def chunk_document(text: str, language: str = None, chunk_size: int = 1500) -> list[str]:
    """
    Slices any text document into optimal chunks. 
    Routes code structures to AST/brace splitters, and prose to recursive character splitters.
    """
    if language and language != "text":
        if language == "python":
            raw_chunks = split_python_code_by_ast(text)
        else:
            raw_chunks = split_braced_code(text, language)
            
        final_chunks = []
        current_block = []
        current_len = 0
        
        for rc in raw_chunks:
            rc_len = len(rc)
            if rc_len > chunk_size:
                if current_block:
                    final_chunks.append("\n\n".join(current_block))
                    current_block = []
                    current_len = 0
                final_chunks.extend(chunk_prose(rc, chunk_size))
            else:
                if current_len + rc_len > chunk_size:
                    final_chunks.append("\n\n".join(current_block))
                    current_block = [rc]
                    current_len = rc_len
                else:
                    current_block.append(rc)
                    current_len += rc_len + 2
                    
        if current_block:
            final_chunks.append("\n\n".join(current_block))
            
        return final_chunks
    else:
        return chunk_prose(text, chunk_size)
