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

file1 = r"C:\Users\kevin\Desktop\Taospace\output\細胞活化開啟青春密碼_陳文彬醫師講座筆記.docx"
file2 = r"C:\Users\kevin\Desktop\Taospace\output\細胞活化開啟青春密碼筆記.docx"

text1 = get_docx_text(file1)
text2 = get_docx_text(file2)

with open(r"C:\Users\kevin\Desktop\Taospace\output\compare_log.txt", 'w', encoding='utf-8') as f:
    f.write(f"--- FILE 1 ({file1.split(chr(92))[-1]}) LENGTH ---\n")
    f.write(f"{len(text1)}\n")
    f.write(f"--- FILE 2 ({file2.split(chr(92))[-1]}) LENGTH ---\n")
    f.write(f"{len(text2)}\n\n")
    
    if text1 == text2:
        f.write("--- CONCLUSION ---\nThe text content is identical.\n")
    else:
        f.write("--- CONCLUSION ---\nThe text content is different.\n")
        f.write("\nFile 1 excerpt:\n" + text1[:500] + "\n...\n")
        f.write("\nFile 2 excerpt:\n" + text2[:500] + "\n...\n")
