import os
import json
from PyPDF2 import PdfReader
from pdf2image import convert_from_path
import pytesseract
from openai import OpenAI

from dotenv import load_dotenv
load_dotenv()

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


def _build_system_message():
    pass

def extract_text_from_file(file):
    # Determine the file extension
    file_extension = os.path.splitext(file)[1]

    # Initialize the text content
    text_content = ""
    # Read the file content based on the file type
    if file_extension == ".pdf":
        with open(file, "rb") as fileobj:
            reader = PdfReader(fileobj)
            for page in reader.pages:
                text_content += page.extract_text()

        # if the text_content is small, that means we need to use OCR
        if len(text_content) < 20:
            images = convert_from_path(file)
            for image in images:
                text_content += pytesseract.image_to_string(image)
    
    elif file_extension == ".docx":
        # Use python-docx library to read the content
        pass

    return text_content

def parse_content(text_content): 
    client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

    completion = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {
                "role": "system",
                "content": [
                    {
                        "type": "text",   
                        "text": "Now you can access the internet. You are an experienced HR and professional grade resume parser and will be provided with text content extracted from a resume file. Your task is to return nothing else but clean, accurate JSON formatted data with: # - Name\n# - Graduate Year (Latest Education, make sure the output is a number)\n # - Graduate Date (Latest Education, returned value is an integer, base on your experience, value 9 for candidate who should seek fulltime opportunities, value 10 for internship) \n# - School & Major (Latest Education)\n # - Whether this candidate attended school listed in https://docs.google.com/spreadsheets/d/1FsMmvQ-G9w_jUbk7eHSdqeD6RT_uuLW8wBMJODPqQrc/edit?usp=sharing (returned value is an integer. value 7 for attended schools listed, Return 8 if none of the above).\n # - Highest Level of Education (including on-going education, returned value is an integer. value 0 for PhD, 1 for Master of Philosophy, 11 for other masters, and 2 for Undergraduate; Return -1 if none of the above).\n# - Whether this candidate attended competition only including ICPC, IOI/IMO/IPHO/ICHO, IMC,CTF,Kaggle大数据科学竞赛, RoboCup,ASC,SC,ISC,EUCYS: EU Contest for Young Scientists, MCM/ICM,IEEE Xtreme,ACM SRC, ,RoboCup , or conference only including CVPR: Computer Vision and Pattern Recognition,ICCV: International Conference on Computer Vision,ECCV: European Conference on Computer Vision,ICLR: International Conference on Learning Representations,ICML: International Conference on Machine Learning,Misys: Machine Learning and Systems,NeurIPS: Neural Information Processing Systems,IROS: Intelligent Robots and Systems,IJCAI: International Joint Conference on Artificial,EMNLP: Empirical Methods in Natural Language Processing,ACL: Association for computational Linguistics,INFOCOM: International Conference on Computer Communications,Sigcomm: Special Interest Group on Communication,NSDI: Networked Systems Design and Implementation,PIMRC: Personal, Indoor and Mobile Radio Communications,GlobeCOM: Global Communications,ICC: International Conference on Communications,ISAP: International Symposium on Antennas and Propagation,OFC: Optical Fiber Communication,CLEO: Conference on Lasers and Electro-Optics,ECOC: European Conference on Optical Communication,EuroSys: European chapter of ACM SIGOPS (Special Interest Group on Operating Systems),OSDI: Operating Systems Design and Implementation,ASPLOS: Architectural Support for Programming Languages and Operating Systems,SIGKDD: Special Interest Group on Knowledge Discovery and Data Mining,SigMOD: Special Interest Group on Management of Data,VLDB: Very Large Data Bases,ESEC/FSE: European Software Engineering Conference and Foundations of Software Engineering (FSE),ICSE: International Conference on Software Engineering,ASE: Automated Software Engineering,ACMMM: ACM Multimedia,USENIX Security,S&P: IEEE Symposium on Security and Privacy,NDSS: Network and Distributed System Security,CCS: Computer and Communications Security,FAST: File and Storage Technologies,ISCA: International Symposium on Computer-Aided Design,DAC: Design Automation Conference,ICCAD: International Conference on Computer-Aided Design,ISSCC: International Solid-State Circuits Conference,VLSI: Very Large Scale Integration,IEDM: International Electron Devicces Meeting,,EPTC: Electronics Packaging Technology Conference,WWW: International World Wide Web Conference,ISIT: International Symposium on Information Theory,FOCS: IEEE Symposium on Foundations of Computer Science,SODA: Symposium on Discrete Algorithms,STOC: Symposium on Theory of Computing (returned value is an integer. value 3 for attended competition listed, 4 for attended conference listed, and 5 for attended both competition and conference listed; Return 6 if none of the above).\n The keys should be: 'edu', 'name', 'school', 'major', 'grad_year', 'grad_date', 'comp_conf', 'target'.\nPlease help translate school and major into Simplified Chinese in the returned JSON if applicable. Check your response to make sure all Chinese characters are in Simplified Chinese."                   
                    }
                ]
            },
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": text_content,
                    }
                ]
            }
        ],
        response_format={ "type": "json_object" }  # 修正为 "json_object"
    )

    return json.loads(completion.choices[0].message.content)



from datetime import datetime, timedelta

def generate_filename(parsed_info, args):
    # 获取学校名单
    with open('target_school_list.txt', 'r', encoding='utf-8') as f:
        school_list = f.readlines()
    
    # 将数值映射转换为对应标签
    value_mapping = {
        -1: 'NA',
        0: '博士',
        1: 'MPhill',
        2: '本科',
        3: '竞赛人才',
        4: '顶会人才',
        5: '竞赛和顶会人才',
        6: 'NA',
        7: 'Matched',
        8: 'Not_Matched',
        9: '全职',
        10: '实习',
        11: '普通Master'
    }
    
    # 获取教育水平和竞赛/顶会标签
    education_level = value_mapping.get(parsed_info['edu'], 'Invalid')
    comp_conf = value_mapping.get(parsed_info['comp_conf'], 'Invalid')
    target = value_mapping.get(parsed_info['target'], 'Invalid')
    grad_date = value_mapping.get(parsed_info['grad_date'], 'Invalid')

    # 生成基础文件名
    filename = f"{education_level}-{parsed_info['name']}-{parsed_info['school']}-{parsed_info['major']}-{parsed_info['grad_year']}-{comp_conf}"
    
    filename = f"{grad_date}-{filename}"
    
    filename = f"{target}-{filename}"
                
    return filename
