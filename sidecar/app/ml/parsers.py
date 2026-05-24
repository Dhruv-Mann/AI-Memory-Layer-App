import os
import re
from typing import Dict, Any, Tuple
from pypdf import PdfReader

def parse_markdown(file_path: str) -> Tuple[str, Dict[str, Any]]:
    """
    Parses Markdown documents, extracting YAML frontmatter configuration metadata 
    and clean content body.
    """
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()

    metadata = {"source": os.path.basename(file_path), "type": "markdown"}
    
    # Detect frontmatter bounded by ---
    frontmatter_match = re.match(r"^---\s*\n(.*?)\n---\s*\n", content, re.DOTALL)
    
    if frontmatter_match:
        frontmatter_text = frontmatter_match.group(1)
        for line in frontmatter_text.split("\n"):
            if ":" in line:
                key, val = line.split(":", 1)
                key = key.strip()
                val = val.strip().strip('"').strip("'")
                if key == "tags":
                    if val.startswith("[") and val.endswith("]"):
                        metadata[key] = [t.strip() for t in val[1:-1].split(",") if t.strip()]
                    else:
                        metadata[key] = [t.strip() for t in val.split(",") if t.strip()]
                else:
                    metadata[key] = val
                    
        content = content[frontmatter_match.end():]
        
    return content.strip(), metadata

def parse_pdf(file_path: str) -> Tuple[str, Dict[str, Any]]:
    """
    Parses PDF documents page-by-page, returning combined text and document metadata properties.
    """
    reader = PdfReader(file_path)
    metadata = {
        "source": os.path.basename(file_path),
        "type": "pdf",
        "total_pages": len(reader.pages)
    }
    
    if reader.metadata:
        for key, val in reader.metadata.items():
            clean_key = key.replace("/", "").lower()
            metadata[clean_key] = str(val)
            
    extracted_text = []
    for page in reader.pages:
        page_text = page.extract_text()
        if page_text:
            extracted_text.append(page_text)
            
    full_text = "\n\n".join(extracted_text)
    return full_text.strip(), metadata

def parse_code(file_path: str) -> Tuple[str, Dict[str, Any]]:
    """
    Parses code source files, extracting raw content and identifying programming language.
    """
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()
        
    ext = os.path.splitext(file_path)[1].lower()
    lang_map = {
        ".py": "python",
        ".js": "javascript",
        ".ts": "typescript",
        ".go": "go",
        ".java": "java",
        ".cpp": "cpp",
        ".c": "c",
        ".rs": "rust"
    }
    lang = lang_map.get(ext, "text")
    
    metadata = {
        "source": os.path.basename(file_path),
        "type": "code",
        "language": lang
    }
    
    return content.strip(), metadata

def parse_file(file_path: str) -> Tuple[str, Dict[str, Any]]:
    """
    Generic dispatcher API routing processing to the appropriate parser by file extension.
    """
    ext = os.path.splitext(file_path)[1].lower()
    if ext == ".md":
        return parse_markdown(file_path)
    elif ext == ".pdf":
        return parse_pdf(file_path)
    elif ext in [".py", ".js", ".ts", ".go", ".java", ".cpp", ".c", ".rs"]:
        return parse_code(file_path)
    else:
        with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
            content = f.read()
        metadata = {"source": os.path.basename(file_path), "type": "text"}
        return content.strip(), metadata
