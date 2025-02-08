import os
import csv
from docx import Document

def cn_punctuation(text):
    """将与中文字符相邻的英文标点转换为中文标点"""
    # 标点映射字典
    punctuation_map = {
        ',': '，',
        '.': '。',
        '?': '？', 
        '!': '！',
        ':': '：',
        ';': '；',
        '(': '（',
        ')': '）',
        '"': '“',
        '\'':'‘'
    }
    
    result = list(text)
    for i in range(len(result)):
        # 检查当前字符是否是需要转换的英文标点
        if result[i] in punctuation_map:
            # 检查前后字符是否是中文
            prev_is_cn = (i > 0 and '\u4e00' <= result[i-1] <= '\u9fff')
            next_is_cn = (i < len(result)-1 and '\u4e00' <= result[i+1] <= '\u9fff')
            
            if prev_is_cn or next_is_cn:
                result[i] = punctuation_map[result[i]]
                
    return ''.join(result)

def extract_paragraphs(file_path)->list[str]:
    def merge_paragraphs(text):
        # 抛弃较短段落
        paragraphs = [p.strip() for p in text.split('\n') if p.strip()]
        merged = []
        
        for para in paragraphs:
            
            # 判断段落是否应该被抛弃
            def should_discard_paragraph(para):
                def is_mostly_chinese(text):
                    chinese_chars = sum(1 for char in text if '\u4e00' <= char <= '\u9fff')
                    return chinese_chars / len(text) > 0.5
                # 排除首字符不是中文和英文字母的段落
                if para[0].isalpha():
                    # 根据结尾标点决定抛弃条件
                    if para[-1] in '。？！:：——》….?!':
                        # 根据语言决定抛弃条件
                        if is_mostly_chinese(para):
                            return len(para) < 40
                        else:
                            return len(para.split()) < 20
                    else:
                        return True
                else:
                    return True

            if should_discard_paragraph(para):
                continue
            # 删除两个中文字符之间的空格
            para = ''.join([char for i, char in enumerate(para) if not (char == ' ' and '\u4e00' <= para[i-1] <= '\u9fff' and '\u4e00' <= para[i+1] <= '\u9fff')])
            # 将中文字符相邻的标点符号改为中文标点符号。
            para = cn_punctuation(para)
            merged.append(para)
            
        return merged

    if file_path.endswith('.txt') or file_path.endswith('.md'):
        with open(file_path, 'r', encoding='utf-8') as f:
            return merge_paragraphs(f.read())
    elif file_path.endswith('.doc') or file_path.endswith('.docx'):
        doc = Document(file_path)
        return merge_paragraphs('\n'.join([para.text for para in doc.paragraphs]))
    else:
        return ''

def process_files(directory):
    log_file = 'text_extraction.log'
    with open(log_file, 'w', encoding='utf-8') as log:
        # Convert to absolute path and ensure it's a directory
        abs_directory = os.path.abspath(directory)
        if not os.path.isdir(abs_directory):
            log.write(f'Error: {abs_directory} is not a valid directory\n')
            return
            
        # Create output directory if not exists
        output_dir = os.path.join(os.path.dirname(__file__), 'output')
        os.makedirs(output_dir, exist_ok=True)
        
        # Dictionary to store CSV writers for each field
        field_writers = {}
        
        for root, dirs, files in os.walk(abs_directory):
            for file in files:
                if file.endswith(('.txt', '.doc', '.docx', '.md')):
                    file_path = os.path.join(root, file)
                    try:
                        paragraphs = extract_paragraphs(file_path)
                        if not paragraphs:
                            log.write(f'Warning: No paragraphs found in {file_path}\n')
                            continue
                        # 提取 field 和 paper_name
                        field = os.path.basename(os.path.dirname(file_path))
                        paper_name = os.path.splitext(file)[0]
                        
                        # Create CSV writer for this field if not exists
                        if field not in field_writers:
                            csv_path = os.path.join(output_dir, f'datasets_{field}.csv')
                            csvfile = open(csv_path, 'w', newline='', encoding='utf-8')
                            writer = csv.writer(csvfile)
                            writer.writerow(['text', 'is_human', 'field', 'paper_name'])
                            field_writers[field] = (csvfile, writer)
                        
                        # Write data to corresponding CSV
                        for para in paragraphs:
                            field_writers[field][1].writerow([para, 1, field, paper_name])
                    except Exception as e:
                        log.write(f'Error processing {file_path}: {str(e)}\n')
        
        # Close all CSV files
        for csvfile, _ in field_writers.values():
            csvfile.close()

if __name__ == '__main__':
    # Ensure input_dir points to the correct Papers directory
    input_dir = os.path.join(os.path.dirname(__file__), 'Papers')
    process_files(input_dir)