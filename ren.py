import os
import re

# 设置文件夹路径
txt_dir = "C:/Users/cyez-oi/Downloads/downloaded_pdfs"

def extract_from_structured_format():
    """从结构化格式的txt文件中提取信息"""
    all_students = []
    
    for filename in os.listdir(txt_dir):
        if filename.lower().endswith(".txt"):
            txt_path = os.path.join(txt_dir, filename)
            print(f"正在处理: {filename}")
            
            try:
                with open(txt_path, 'r', encoding='utf-8') as file:
                    lines = file.readlines()
                
                i = 0
                while i < len(lines):
                    line = lines[i].strip()
                    
                    # 检查是否是姓名（中文姓名）
                    if re.match(r'^[\u4e00-\u9fa5]{2,4}$', line) and i + 1 < len(lines):
                        name = line
                        school = lines[i + 1].strip()
                        
                        # 检查下一行是否是学校（不是年级）
                        if not re.match(r'^(初|高|小学|预初)', school) and school != '':
                            # 获取年级和等第信息（如果存在）
                            grade = ""
                            award = ""
                            
                            if i + 2 < len(lines):
                                potential_grade = lines[i + 2].strip()
                                if re.match(r'^(初|高|小学|预初)', potential_grade):
                                    grade = potential_grade
                                    if i + 3 < len(lines):
                                        potential_award = lines[i + 3].strip()
                                        if "等奖" in potential_award:
                                            award = potential_award
                            
                            student_info = {
                                'name': name,
                                'school': school,
                                'grade': grade,
                                'award': award
                            }
                            all_students.append(student_info)
                            
                    i += 1
                    
            except Exception as e:
                print(f"处理文件 {filename} 时出错: {e}")
    
    return all_students

def extract_from_search_format():
    """从搜索格式的txt文件中提取信息"""
    name_school_pairs = []
    
    for filename in os.listdir(txt_dir):
        if filename.lower().endswith(".txt"):
            txt_path = os.path.join(txt_dir, filename)
            
            try:
                with open(txt_path, 'r', encoding='utf-8') as file:
                    content = file.read()
                    
                    # 提取"在以下文件中找到"格式
                    pattern = r'在以下文件中找到"([^"]+)"：\s*\n([^\n]+)'
                    matches = re.findall(pattern, content)
                    
                    for name, file_info in matches:
                        # 从文件名提取学校信息
                        school_match = re.search(r'2025年(.+?)(?:_\d+)?\.pdf', file_info)
                        if school_match:
                            school = school_match.group(1)
                            name_school_pairs.append((name, school))
                    
                    # 提取"人名 学校"格式
                    lines = content.split('\n')
                    for line in lines:
                        line = line.strip()
                        if re.match(r'^[\u4e00-\u9fa5]{2,4}\s+', line):
                            parts = line.split(' ', 1)
                            if len(parts) == 2:
                                name, school = parts[0].strip(), parts[1].strip()
                                name_school_pairs.append((name, school))
                                
            except Exception as e:
                print(f"处理文件 {filename} 时出错: {e}")
    
    return name_school_pairs

def main():
    print("=== 整合所有TXT文件信息 ===\n")
    
    # 提取结构化格式的学生信息
    print("1. 提取详细学生信息...")
    students = extract_from_structured_format()
    
    # 提取搜索格式的人名-学校对应
    print("2. 提取人名-学校对应关系...")
    name_school_pairs = extract_from_search_format()
    
    # 整合所有信息
    all_info = {}
    
    # 添加详细信息
    for student in students:
        name = student['name']
        all_info[name] = {
            'school': student['school'],
            'grade': student['grade'],
            'award': student['award']
        }
    
    # 添加简单的人名-学校对应
    for name, school in name_school_pairs:
        if name not in all_info:
            all_info[name] = {
                'school': school,
                'grade': '',
                'award': ''
            }
    
    # 输出整合结果
    print(f"\n=== 整合结果 ===")
    print(f"共找到 {len(all_info)} 个学生信息\n")
    
    # 按姓名排序
    sorted_names = sorted(all_info.keys())
    
    # 输出格式1：详细信息
    print("详细信息格式：")
    print("-" * 80)
    detailed_output = []
    for name in sorted_names:
        info = all_info[name]
        if info['grade'] and info['award']:
            line = f"{name} {info['school']} {info['grade']} {info['award']}"
        else:
            line = f"{name} {info['school']}"
        detailed_output.append(line)
        print(line)
    
    # 输出格式2：仅人名学校
    print(f"\n仅人名学校格式：")
    print("-" * 80)
    simple_output = []
    for name in sorted_names:
        line = f"{name} {all_info[name]['school']}"
        simple_output.append(line)
        print(line)
    
    # 输出格式3：仅人名列表
    print(f"\n仅人名列表：")
    print("-" * 80)
    names_only = " ".join(sorted_names)
    print(names_only)
    
    # 保存结果到文件
    base_path = txt_dir
    
    # 保存详细信息
    with open(os.path.join(base_path, "integrated_detailed.txt"), 'w', encoding='utf-8') as f:
        f.write("\n".join(detailed_output))
    
    # 保存简单格式
    with open(os.path.join(base_path, "integrated_simple.txt"), 'w', encoding='utf-8') as f:
        f.write("\n".join(simple_output))
    
    # 保存仅人名
    with open(os.path.join(base_path, "names_only.txt"), 'w', encoding='utf-8') as f:
        f.write(names_only)
    
    print(f"\n结果已保存到:")
    print(f"- 详细信息: integrated_detailed.txt")
    print(f"- 简单格式: integrated_simple.txt") 
    print(f"- 仅人名: names_only.txt")
    
    print(f"\n=== 整合完成 ===")

if __name__ == "__main__":
    main()