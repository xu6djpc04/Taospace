import zipfile
import xml.etree.ElementTree as ET

def get_docx_text(path):
    try:
        document = zipfile.ZipFile(path)
        xml_content = document.read('word/document.xml')
        document.close()
        tree = ET.XML(xml_content)
        
        NAMESPACE = '{http://schemas.openxmlformats.org/wordprocessingml/2006/main}'
        PARA = NAMESPACE + 'p'
        TEXT = NAMESPACE + 't'
        
        paragraphs = []
        for paragraph in tree.iter(PARA):
            texts = [node.text for node in paragraph.iter(TEXT) if node.text]
            if texts:
                paragraphs.append(''.join(texts))
        return '\n'.join(paragraphs)
    except Exception as e:
        return f"Error reading {path}: {e}"

files = [
    r"C:\Users\kevin\Desktop\Taospace\output\細胞活化開啟青春密碼_整合版.docx",
    r"C:\Users\kevin\Desktop\Taospace\output\細胞活化開啟青春密碼_終極完美排版版.docx"
]

with open(r"C:\Users\kevin\Desktop\Taospace\output\compare_2_log.txt", 'w', encoding='utf-8') as f:
    for path in files:
        text = get_docx_text(path)
        filename = path.split('\\')[-1]
        f.write(f"=== {filename} ({len(text)} chars) ===\n")
        f.write(text + "\n\n")
