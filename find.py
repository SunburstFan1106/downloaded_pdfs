import os
import fitz  # PyMuPDF

# 设置PDF文件夹路径
pdf_dir = "C:/Users/cyez-oi/Downloads/downloaded_pdfs"

names_input = input("请输入要查找的人名（多个用逗号或空格分隔）：")
# 支持逗号、空格、换行分隔
names = [n.strip() for n in names_input.replace('\n', ',').replace(' ', ',').split(',') if n.strip()]

results = {}

for name in names:
    found_files = []
    for filename in os.listdir(pdf_dir):
        if filename.lower().endswith(".pdf"):
            pdf_path = os.path.join(pdf_dir, filename)
            doc = fitz.open(pdf_path)
            for page in doc:
                text = page.get_text()
                if name in text:
                    found_files.append(filename)
                    break
            doc.close()
    results[name] = found_files

for name in names:
    found_files = results[name]
    if found_files:
        print(f"在以下文件中找到“{name}”：")
        for f in found_files:
            print(f)
    else:
        print(f"未在任何文件中找到“{name}”。")