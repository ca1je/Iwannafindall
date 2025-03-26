import os
import re
import chardet
from datetime import datetime

def read_regex_patterns(file_path):
    """从文件中读取正则表达式规则，格式为 '规则名:正则语句'"""
    patterns = {}
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            for line in file:
                line = line.strip()
                if line and ':' in line:  # 确保行有效且包含冒号分隔符
                    rule_name, pattern = line.split(':', 1)
                    patterns[rule_name.strip()] = pattern.strip()
        print(f"加载的正则表达式规则：")
        flog.write(f"加载的正则表达式规则：\n")
        for rule_name, pattern in patterns.items():
            print(f"  {rule_name}: {pattern}")
            flog.write(f"  {rule_name}: {pattern}\n")
        print(f"开始检查：")
        flog.write(f"开始检查：\n")
    except FileNotFoundError:
        print(f"错误：文件 {file_path} 未找到。")
        flog.writ(f"错误：文件 {file_path} 未找到。\n")
    except Exception as e:
        print(f"读取正则表达式文件时出错：{e}")
        flog.write(f"读取正则表达式文件时出错：{e}\n")
    return patterns

def detect_file_encoding(file_path):
    """检测文件编码"""
    try:
        with open(file_path, 'rb') as f:
            raw_data = f.read(1000)  # 读取前1000字节用于检测编码
        return chardet.detect(raw_data)['encoding']
    except Exception as e:
        flog.write(f"检测文件编码时出错：{e}\n")
        return None

def read_file_content(file_path):
    """读取文件内容，自动检测编码"""
    encoding = detect_file_encoding(file_path)
    if not encoding:
        flog.write(f"无法检测文件 {file_path} 的编码，跳过该文件。\n")
        return None

    try:
        with open(file_path, 'r', encoding=encoding, errors='ignore') as f:
            return f.read()
    except Exception as e:
        flog.write(f"无法读取文件 {file_path}，原因：{e}\n")
        return None

def find_matches_in_file(file_path, patterns):
    """在单个文件中使用所有正则表达式规则进行匹配"""
    content = read_file_content(file_path)
    if content is None:
        return

    flog.write(f"正在检查文件：{file_path}\n")
    for rule_name, pattern in patterns.items():
        matches = re.findall(pattern, content)
        if matches:
            print(f"  规则 '{rule_name}' 在{file_path}匹配到以下内容：")
            fr.write(f"  规则 '{rule_name}' 在{file_path}匹配到以下内容：\n")
            flog.write(f"  规则 '{rule_name}' 在{file_path}匹配到以下内容：\n")
            for match in matches:
                print(f"    - {match}\n")
                fr.write(f"    - {match}\n")
                flog.write(f"    - {match}\n")
        else:
            flog.write(f"  规则 '{rule_name}' 未匹配到任何内容。\n")

def find_matches_in_directory(directory, patterns):
    """遍历指定目录及其子目录中的所有文件，并匹配正则表达式"""
    if not patterns:
        print("未加载有效的正则表达式，无法进行匹配。")
        flog.write("未加载有效的正则表达式，无法进行匹配。\n")
        return

    # 遍历当前文件夹及其子文件夹
    for root, dirs, files in os.walk(directory):
        for file in files:
            file_path = os.path.join(root, file)
            if 'rule.txt' in str(file_path) or 'rest.txt' in str(file_path) or 'log.log' in str(file_path):
                pass
            else:
                find_matches_in_file(file_path, patterns)

def main():
    # 当前工作目录
    current_directory = os.getcwd()
    print(f"正在检查当前目录：{current_directory}")

    # 读取正则表达式规则文件
    regex_file = "rule.txt"
    patterns = read_regex_patterns(regex_file)

    # 如果正则表达式有效，则开始匹配
    if patterns:
        find_matches_in_directory(current_directory, patterns)
    else:
        print("未加载任何规则，无法进行匹配。")

if __name__ == "__main__":
    fr = open('result.txt','w+',encoding='utf-8')
    flog = open('log.log','a+',encoding = 'utf-8')
    flog.write("---------------------------检查开始于"+str(datetime.now())+"---------------------------\n")
    main()
    flog.write("---------------------------检查结束于"+str(datetime.now())+"---------------------------\n")
    fr.close()
    flog.close()
