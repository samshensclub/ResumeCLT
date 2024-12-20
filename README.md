# ResumeCLT

This is a command line tool to help HR interns rename all the resumes they have received with the power of OpenAI and OCR.

## Requirements

You need to have `python`, `pip`, `poppler-utils` and `tesseract` installed.

```
pip install -r requirements.txt
```

You might need additonal tesseract language packs per your use cases. For example,

```
sudo dnf install tesseract-langpack-chi_sim
```

You need to provide your own OpenAI API with `.env`.

## Usage

```
ResumeCLT.py [-h] --source_dir test_resume --output_dir output [--target_list TARGET_LIST]

Options for ResumeCLT

options:
  -h, --help            show this help message and exit
  --source_dir  
                        Directory where the resume files are stored
  --output_dir output
                        Directory where the output files will be stored
  --target_list target_school_list.txt
                        File containing the list of target schools
```

Run provided test case with:

```
ResumeCLT.py  --source_dir test_resume --output_dir output --target_list target_school_list.txt
```

Enjoy being our HR intern.

Copy this to cmd:
 cd C:\Users\s84387544\Desktop\ResumeCLT-main
then:
ResumeCLT.py  --source_dir test_resume --output_dir output --target_list target_school_list.txt