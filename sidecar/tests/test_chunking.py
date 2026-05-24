import os
import tempfile
import pytest
from app.ml.parsers import parse_markdown, parse_code
from app.ml.chunking import chunk_document

def test_parse_markdown_frontmatter():
    markdown_content = """---
tags: [test, science]
title: "Physics Notes"
---
# Classical Mechanics
Newtonian mechanics describes the motion of macroscopic objects.
"""
    with tempfile.NamedTemporaryFile(suffix=".md", delete=False, mode="w", encoding="utf-8") as f:
        f.write(markdown_content)
        temp_path = f.name
        
    try:
        body, metadata = parse_markdown(temp_path)
        assert "Classical Mechanics" in body
        assert "Newtonian mechanics" in body
        assert "science" in metadata["tags"]
        assert "test" in metadata["tags"]
        assert metadata["type"] == "markdown"
    finally:
        os.remove(temp_path)

def test_parse_code_structure():
    code_content = """
def calculate_sum(a, b):
    \"\"\"Calculates sum of two numbers.\"\"\"
    return a + b

class VectorCalculator:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        
    def magnitude(self):
        return (self.x**2 + self.y**2)**0.5
"""
    with tempfile.NamedTemporaryFile(suffix=".py", delete=False, mode="w", encoding="utf-8") as f:
        f.write(code_content)
        temp_path = f.name
        
    try:
        body, metadata = parse_code(temp_path)
        assert "VectorCalculator" in body
        assert "calculate_sum" in body
        assert metadata["language"] == "python"
        assert metadata["type"] == "code"
    finally:
        os.remove(temp_path)

def test_chunk_document_markdown():
    text = """# Header 1
Content of first header.
## Subheader 1.1
Content of subheader.
# Header 2
Content of second header.
"""
    chunks = chunk_document(text, "markdown")
    assert len(chunks) > 0
    assert any("Header 1" in c for c in chunks)
    assert any("Header 2" in c for c in chunks)

def test_chunk_document_code():
    code = """
class DataPipeline:
    def __init__(self, source):
        self.source = source
        
    def run(self):
        print("Running pipeline from", self.source)
        
def root_helper():
    return "Helper"
"""
    chunks = chunk_document(code, "python")
    assert len(chunks) > 0
    assert any("DataPipeline" in c for c in chunks)
    assert any("root_helper" in c for c in chunks)
