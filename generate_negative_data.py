import os
import dspy
import dotenv
import random
import pandas as pd
from concurrent.futures import ThreadPoolExecutor, as_completed
from tqdm import tqdm
dotenv.load_dotenv()

def lm_config(model:str):
    return dspy.LM(model=model, 
                api_key=os.getenv('API_KEY'),
                api_base=os.getenv('API_BASE'), 
                temperature=1.0,
                cache=False)
    
lm_01 = lm_config('openai/Qwen/Qwen2.5-Coder-32B-Instruct')
lm_02 = lm_config('openai/deepseek-ai/DeepSeek-V2.5')
lm_03 = lm_config('openai/meta-llama/Llama-3.3-70B-Instruct')
lm_04 = lm_config('openai/01-ai/Yi-1.5-34B-Chat-16K',)

#dspy.configure(lm=lm)

class Rewrite(dspy.Signature):
    """将用给定的文本进行改写，使其文本风格更加学术，逻辑更加严谨，用词更加专业，结构更加清晰。"""
    origin_text: str = dspy.InputField()
    language: str = dspy.OutputField()
    rewrited_text: str = dspy.OutputField()

def process_row(row, rewrite):
    """处理单行数据的线程函数"""
    if row['is_human'] == 1:  # 只处理人工编写的文本
        result = rewrite(origin_text=row['text'])
        return {
            'input': result.rewrited_text.replace('\n', ' '),
            'output': row['text'],
            'field': row['field'],
            'paper_name': row['paper_name']
        }
    return None

def process_csv(input_path, output_path, max_workers=4):
    # 读取原始csv文件
    original_df = pd.read_csv(input_path)
    
    # 初始化rewrite模型
    def init_rewrite(models):
        lm = random.choice(models)
        with dspy.context(lm=dspy.configure(lm=lm)):
            rewrite = dspy.Predict(Rewrite)
        return rewrite
    models = [lm_01, lm_02, lm_03, lm_04]
    
    # 创建线程池处理数据
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = [
            executor.submit(process_row, row, init_rewrite(models))
            for _, row in original_df.iterrows()
        ]
        
        # 收集处理结果并显示进度
        new_rows = []
        with tqdm(total=len(futures), desc="Processing rows") as pbar:
            for future in as_completed(futures):
                result = future.result()
                if result:
                    new_rows.append(result)
                pbar.update(1)
    
    # 将新数据转换为DataFrame
    new_df = pd.DataFrame(new_rows)

    # 保存结果
    new_df.to_csv(output_path, index=False)

if __name__ == '__main__':
    input_csv = 'output/datasets_工程.csv'
    output_csv = 'output/datasets_工程_processed.csv'
    process_csv(input_csv, output_csv, max_workers=4)