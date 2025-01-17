import os
from marker.converters.pdf import PdfConverter
from marker.models import create_model_dict
from marker.config.parser import ConfigParser
from marker.output import save_output

def extract_title_n_field(file_path):
    field = os.path.basename(os.path.dirname(file_path))
    paper_name = os.path.splitext(os.path.basename(file_path))[0]
    return field, paper_name

config = {
    "output_format": "markdown",
    "ADDITIONAL_KEY": "VALUE",
    "pdftext_workers":"3",
    "use_fast": True,
    "disable_image_extraction": True,
    "languages": "zh",
    "page_range":"2-30",
    "strip_existing_ocr": True
}
config_parser = ConfigParser(config)

converter = PdfConverter(
    config=config_parser.generate_config_dict(),
    artifact_dict=create_model_dict(),
    processor_list=config_parser.get_processors(),
    renderer=config_parser.get_renderer()
)

def process_pdf_file(file_path):
    try:
        field, paper_name = extract_title_n_field(file_path)
        print(f"Processing: {paper_name} ({field})")
        rendered = converter(file_path)
        print(f"Rendered: {paper_name} ({field})")
        os.makedirs(f'Papers/{field}/', exist_ok=True)
        save_output(rendered=rendered,
                   output_dir=f'Papers/{field}/',
                   fname_base=paper_name)
        return True
    except Exception as e:
        print(f"Error processing {file_path}: {str(e)}")
        return False

if __name__ == "__main__":
    papers_dir = 'Papers'
    total_files = 0
    processed_files = 0
    
    # 遍历Papers目录下的所有PDF文件和MD文件，若同时存在同名文件，则从列表中排除
    for root, dirs, files in os.walk(papers_dir):
        # 使用集合来存储文件名，方便快速查找
        file_set = set(f.lower() for f in files)
        
        for file in files:
            file_lower = file.lower()
            if file_lower.endswith('.pdf'):
                md_file = file_lower.replace('.pdf', '.md')
                if md_file in file_set:
                    continue
            elif file_lower.endswith('.md'):
                pdf_file = file_lower.replace('.md', '.pdf')
                if pdf_file in file_set:
                    continue
            else:
                continue  # 如果不是PDF或MD文件，跳过
            
            total_files += 1
            file_path = os.path.join(root, file)
            if process_pdf_file(file_path):
                processed_files += 1
    
    print(f"\nProcessing complete. Successfully processed {processed_files}/{total_files} files.")