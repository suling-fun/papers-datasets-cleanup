import os
import dspy
import dotenv
import pandas as pd
dotenv.load_dotenv()

lm = dspy.LM('deepseek-chat',
             api_key=os.getenv('API_KEY'),
             api_base=os.getenv('API_BASE'))
dspy.configure(lm=lm)

class Rewrite(dspy.Signature):
    """将用给定的文本进行改写，使其文本风格更加学术，逻辑更加严谨，用词更加专业，结构更加清晰。"""
    origin_text: str = dspy.InputField()
    rewrited_text: str = dspy.OutputField()

def process_csv(input_path, output_path):
    # 读取原始csv文件
    original_df = pd.read_csv(input_path)
    
    # 初始化rewrite模型
    rewrite = dspy.Predict(Rewrite)
    
    # 创建新DataFrame存储改写结果
    new_rows = []
    
    # 遍历每一行进行改写
    for index, row in original_df.iterrows():
        if row['is_human'] == 1:  # 只处理人工编写的文本
            result = rewrite(origin_text=row['text'])
            # 创建新行数据
            new_row = {
                'text': result.rewrited_text.replace('\n', ' '),
                'is_human': 0,
                'field': row['field'],
                'paper_name': row['paper_name']
            }
            new_rows.append(new_row)
    
    # 将新数据转换为DataFrame
    new_df = pd.DataFrame(new_rows)
    
    # 合并原始数据和新数据
    combined_df = pd.concat([original_df, new_df], ignore_index=True)
    
    # 保存结果
    combined_df.to_csv(output_path, index=False)

if __name__ == '__main__':
    input_csv = 'output/datasets.csv'
    output_csv = 'output/datasets.csv'
    process_csv(input_csv, output_csv)