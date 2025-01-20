import os
import csv
from docx import Document

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
                
                # 根据结尾标点决定抛弃条件
                if para[-1] in '。？！:：——》….?!':
                    # 根据语言决定抛弃条件
                    if is_mostly_chinese(para):
                        return len(para) < 100
                    else:
                        return len(para.split()) < 50
                else:
                    return True

            if should_discard_paragraph(para):
                continue
            # 删除两个中文字符之间的空格
            para = ''.join([char for i, char in enumerate(para) if not (char == ' ' and '\u4e00' <= para[i-1] <= '\u9fff' and '\u4e00' <= para[i+1] <= '\u9fff')])
            # 将两个中文字符之间的半角逗号“,”替换为全角逗号“，”
            para = ''.join([char if not (char == ',' and '\u4e00' <= para[i-1] <= '\u9fff' and '\u4e00' <= para[i+1] <= '\u9fff') else '，' for i, char in enumerate(para)])
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