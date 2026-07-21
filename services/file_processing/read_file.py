"""
take in 1 path 
    return its text content or None    
"""

from pathlib import Path

def get_text_content(file_path : Path) -> str | None: 
    
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            text_content = f.read()
            
            if not text_content.strip():
                return None 
            return text_content
        
    except (UnicodeDecodeError, OSError): #OSError = file system problems (path is a dir, other read failures)
        return None