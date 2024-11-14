# Options for ResumeCLT
# --source_dir: Directory where the resume files are stored
# --output_dir: Directory where the output files will be stored
# (optional)
# --target_list: File containing the list of target schools

import argparse

import os
import pytesseract

# 获取当前脚本所在的目录
base_path = os.path.dirname(os.path.abspath(__file__))

# 定义 input 和 output 文件夹的路径
input_dir = os.path.join(base_path, 'input')
output_dir = os.path.join(base_path, 'output')
target_school_list_path = os.path.join(base_path, 'target_school_list.txt')
env_path = os.path.join(base_path, '.env')

# 配置 Tesseract OCR 的路径（可选）
tesseract_path = os.path.join(base_path, 'resources', 'tesseract', 'tesseract.exe')
pytesseract.pytesseract.tesseract_cmd = tesseract_path

# 创建 input 和 output 文件夹（如果不存在）
os.makedirs(input_dir, exist_ok=True)
os.makedirs(output_dir, exist_ok=True)


def parse_args():
    parser = argparse.ArgumentParser(description='Options for ResumeCLT')

    parser.add_argument('--source_dir', type=str, required=True,
                        help='Directory where the resume files are stored')
    parser.add_argument('--output_dir', type=str, required=True,
                        help='Directory where the output files will be stored')
    parser.add_argument('--target_list', type=str, required=False,
                        help='File containing the list of target schools')

    return parser.parse_args()

if __name__ == "__main__":
    args = parse_args()
    print(args)