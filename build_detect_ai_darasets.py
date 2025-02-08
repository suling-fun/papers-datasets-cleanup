"""
构建微调数据集,数据集的格式参考:
{"messages": [{"role": "system", "content": "判断用户给定的文本是否为AI生成的内容。"}, {"role": "user", "content": ""}, {"role": "assistant", "content": ""}]}
{"messages": [{"role": "system", "content": "判断用户给定的文本是否为AI生成的内容。"}, {"role": "user", "content": ""}, {"role": "assistant", "content": ""}]}
"""

import json
import os
import random
import pandas as pd

def process_csv(input_path, test_output_path, train_output_path):
    """处理单个csv文件,生成测试集和训练集"""
    # 使用pandas读取CSV文件
    df = pd.read_csv(input_path, encoding='utf-8')
    
    test_data = []
    train_data = []
    
    # 将DataFrame转换为字典列表进行处理
    for i, row in df.iterrows():
        data_item = {
            "messages": [
                {"role": "system", "content": "判断用户给定的文本是否为AI生成的内容。"},
                {"role": "user", "content": row["input"]},
                {"role": "assistant", "content": "是"}
            ]
        }
        
        data_item_negative = {
            "messages": [
                {"role": "system", "content": "判断用户给定的文本是否为AI生成的内容。"},
                {"role": "user", "content": row["output"]},
                {"role": "assistant", "content": "否"}
            ]
        }
        
        if i < 500:
            test_data.extend([data_item, data_item_negative])
        else:
            train_data.extend([data_item, data_item_negative])

    # 打乱顺序
    random.shuffle(train_data)
    random.shuffle(test_data)
    
    # 写入测试集,每行一个json对象
    with open(test_output_path, "w", encoding="utf-8") as f:
        for item in test_data:
            f.write(json.dumps(item, ensure_ascii=False) + "\n")
        
    # 写入训练集,每行一个json对象
    with open(train_output_path, "w", encoding="utf-8") as f:
        for item in train_data:
            f.write(json.dumps(item, ensure_ascii=False) + "\n")
    
    print(f"处理完成: {input_path}")
    print(f"- 测试集数量: {len(test_data)}")
    print(f"- 训练集数量: {len(train_data)}")

def main():
    """主程序入口"""
    raw_dir = "datasets/raw"
    test_dir = "datasets/test"
    train_dir = "datasets/training"
    
    # 创建输出目录
    os.makedirs(test_dir, exist_ok=True)
    os.makedirs(train_dir, exist_ok=True)
    
    # 处理每个csv文件
    for filename in os.listdir(raw_dir):
        if filename.endswith('.csv'):
            input_path = os.path.join(raw_dir, filename)
            base_name = os.path.splitext(filename)[0]
            
            test_output_path = os.path.join(test_dir, f"{base_name}_test.jsonl")
            train_output_path = os.path.join(train_dir, f"{base_name}_train.jsonl")
            
            try:
                process_csv(input_path, test_output_path, train_output_path)
            except Exception as e:
                print(f"处理文件 {filename} 时出错: {str(e)}")

if __name__ == "__main__":
    main()
