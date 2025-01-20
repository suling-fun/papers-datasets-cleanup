"""
构建微调数据集，数据集的格式参考：
{"messages": [{"role": "system", "content": "将用户输入的内容改写，使其更符合人类写作的习惯。"}, {"role": "user", "content": ""}, {"role": "assistant", "content": ""}]}
{"messages": [{"role": "system", "content": "将用户输入的内容改写，使其更符合人类写作的习惯。"}, {"role": "user", "content": ""}, {"role": "assistant", "content": ""}]}
"""

import csv
import json
import os
from datetime import datetime

def process_csv(input_path, test_output_path, train_output_path):
    """处理单个csv文件，生成测试集和训练集"""
    with open(input_path, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        test_data = []
        train_data = []
        
        for i, row in enumerate(reader):
            if i < 400:
                test_data.append({
                    "messages": [
                        {"role": "system", "content": "将用户输入的内容改写，使其更符合人类写作的习惯。"},
                        {"role": "user", "content": row["input"]},
                        {"role": "assistant", "content": row["output"]}
                    ]
                })
            else:
                train_data.append({
                    "messages": [
                        {"role": "system", "content": "将用户输入的内容改写，使其更符合人类写作的习惯。"},
                        {"role": "user", "content": row["input"]},
                        {"role": "assistant", "content": row["output"]}
                    ]
                })
    
    # 写入测试集，每行一个json对象
    with open(test_output_path, "w", encoding="utf-8") as f:
        for item in test_data:
            f.write(json.dumps(item, ensure_ascii=False) + "\n")
        
    # 写入训练集，每行一个json对象
    with open(train_output_path, "w", encoding="utf-8") as f:
        for item in train_data:
            f.write(json.dumps(item, ensure_ascii=False) + "\n")

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
        input_path = os.path.join(raw_dir, filename)
        base_name = os.path.splitext(filename)[0]
        
        test_output_path = os.path.join(test_dir, f"{base_name}_test.jsonl")
        train_output_path = os.path.join(train_dir, f"{base_name}_train.jsonl")
        
        process_csv(input_path, test_output_path, train_output_path)
    
    # 更新Changelog
    changelog_path = f"Changelog/{datetime.now().strftime('%Y-%m-%d')}.md"
    entry = f"## [{datetime.now().strftime('%Y-%m-%d %H:%M')}]\n- 处理了{len(os.listdir(raw_dir))}个csv文件\n- 生成测试集和训练集\n- 输出格式改为jsonl\n"
    
    if os.path.exists(changelog_path):
        with open(changelog_path, "a", encoding="utf-8") as f:
            f.write("\n" + entry)
    else:
        with open(changelog_path, "w", encoding="utf-8") as f:
            f.write(entry)

if __name__ == "__main__":
    main()
