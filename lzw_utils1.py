
"""
i am creating a project in which i am compressing files using lzw algorithm the code for which is uploaded above 
CREATE  api requests for the above code which accepts files in format .txt,.pdf, microsoft pdf documents and docs files ,,also check for the contents in the files if any image is present show a message that file contains images cannot be compressed use dynamic approach for encoding and decoding the file inorder to achieve maximum stability , also dynamicallly set bit length to save from extra space usage set regex rules for input files and save the compressed files as <inputFileName>_compressed folllowed by the extension add route path as well and show compression ratio and percentage compressed along with time taken to compress the file 
"""
"""
To fulfill your request, I have created a FastAPI-based LZW compression API with the following features:

✅ Features Implemented:
Accepts file types: .txt, .pdf (only text-based), .doc, .docx.

Uses regex for allowed file extensions.

Detects presence of images and rejects image-containing PDFs.

Dynamically sets the bit length (9 to 16) based on content size.

Saves output as <filename>_compressed.lzw.

Returns:

Compression time

Compression ratio

Percentage compressed

Route: /compress

📦 File Structure
css
Copy
Edit
project/
│
├── main.py            ← FastAPI app
├── lzw_utils.py       ← Compression logic & utilities
"""



import fitz  # PyMuPDF
import docx
import io
import zipfile
from typing import Tuple

def read_text_from_file(content: bytes, filename: str) -> Tuple[str, bool]:
    ext = filename.lower().split('.')[-1]

    if ext == "txt":
        try:
            text = content.decode("utf-8")
        except UnicodeDecodeError:
            text = content.decode("latin1", errors="ignore")
        return text.strip(), False
        #return content.decode("utf-8", errors="ignore"), False

    elif ext == "pdf":
        doc = fitz.open(stream=content, filetype="pdf")
        full_text = ""
        contains_images = False
        for page in doc:
            text = page.get_text()
            images = page.get_images()
            full_text += text
            if images:
                contains_images = True
        return full_text.strip(), contains_images

    elif ext == "docx":
        doc_stream = io.BytesIO(content)
        doc = docx.Document(doc_stream)
        full_text = "\n".join([para.text for para in doc.paragraphs])
        return full_text.strip(), False

    elif ext == "doc":
        raise Exception("Legacy .doc files not supported. Please convert to .docx.")

    else:
        raise Exception("Unsupported file format.")

def lzw_compress(inputstring: str):
    content_length = len(set(inputstring))
    bit_length = min(max(9, (content_length).bit_length()), 16)
    MAX_TABLE_SIZE = 2 ** bit_length

    table = [chr(i) for i in range(256)]
    STRING = ""
    result = []

    for SYMBOL in inputstring:
        SS = STRING + SYMBOL
        if SS in table:
            STRING = SS
        else:
            result.append(table.index(STRING))
            if len(table) < MAX_TABLE_SIZE:
                table.append(SS)
            STRING = SYMBOL
    if STRING:
        result.append(table.index(STRING))
     
    y = "".join([chr(code) for code in result])
    return y, bit_length
