import sys
import difflib
import re
import string
import argparse
import logging
import time
import cProfile
import os  # 添加了os模块用于检查文件是否存在

# 从文件读取文本内容
def read_file(file_path):
    if not os.path.exists(file_path):
        print(f"File not found: {file_path}")
        sys.exit(1)

    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            text = file.read()
        return text
    except Exception as e:
        print(f"Error reading file: {str(e)}")
        sys.exit(1)

# 清理文本，去除标点符号和将文本转换为小写
def clean_text(text):
    text = re.sub(f"[{string.punctuation}]", '', text)
    text = text.lower()
    return text

# 计算文本相似度
def calculate_similarity(original_text, plagiarized_text):
    original_text = clean_text(original_text)
    plagiarized_text = clean_text(plagiarized_text)

    # 使用difflib库的SequenceMatcher来计算相似性
    similarity = difflib.SequenceMatcher(None, original_text, plagiarized_text).ratio()
    return round(similarity, 4)

# 主函数
def main():
    # 创建命令行参数解析器
    parser = argparse.ArgumentParser(description="Check plagiarism between two text files")
    parser.add_argument("original_file_path", type=str, help="Path to the original text file")
    parser.add_argument("plagiarized_file_path", type=str, help="Path to the plagiarized text file")
    parser.add_argument("output_file_path", type=str, help="Path to the output file")
    args = parser.parse_args()
    # 启用性能分析
    profiler = cProfile.Profile()
    profiler.enable()

    #开始计时
    start_time = time.time()

    # 从文件读取原始文本和抄袭文本
    original_text = read_file(args.original_file_path)
    plagiarized_text = read_file(args.plagiarized_file_path)

    # 计算文本相似度
    similarity = calculate_similarity(original_text, plagiarized_text)

    end_time = time.time()

    # 将相似度写入输出文件
    with open(args.output_file_path, 'w', encoding='utf-8') as output_file:
        output_file.write(f"{similarity:.2f}\n")

        # 显示运行时间和结果
    print(f"Similarity: {similarity:.2f}")
    print(f"Execution time: {end_time - start_time:.4f} seconds")

    # 停止性能分析
    profiler.disable()
    profiler.print_stats(sort='cumulative')

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)  # 设置日志级别为INFO
    main()