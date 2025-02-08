"""
构建微调数据集,数据集的格式参考:
{"messages": [{"role": "system", "content": "将用户输入的内容改写,使其更符合人类写作的习惯。"}, {"role": "user", "content": ""}, {"role": "assistant", "content": ""}]}
{"messages": [{"role": "system", "content": "将用户输入的内容改写,使其更符合人类写作的习惯。"}, {"role": "user", "content": ""}, {"role": "assistant", "content": ""}]}
"""

import json
import os
from datetime import datetime
import pandas as pd

def process_csv(input_path, test_output_path, train_output_path):
    """处理单个csv文件,生成测试集和训练集"""
    try:
        # 使用pandas读取CSV文件,自动处理编码
        df = pd.read_csv(input_path)
        print(f"成功读取文件 {input_path}, 共 {len(df)} 行数据")
        
        # 分割数据集
        test_df = df.head(500)
        train_df = df.iloc[500:]
        
        # 转换为目标格式
        def convert_to_format(row):
            return {
                "messages": [
                    {"role": "system", "content": "将用户输入的内容改写,使其更符合人类写作的习惯。"},
                    {"role": "user", "content": row["input"]},
                    {"role": "assistant", "content": row["output"]}
                ]
            }
        
        # 生成数据集
        test_data = test_df.apply(convert_to_format, axis=1).tolist()
        train_data = train_df.apply(convert_to_format, axis=1).tolist()
        
        # 写入测试集
        with open(test_output_path, "w", encoding="utf-8") as f:
            for item in test_data:
                f.write(json.dumps(item, ensure_ascii=False) + "\n")
        
        # 写入训练集
        with open(train_output_path, "w", encoding="utf-8") as f:
            for item in train_data:
                f.write(json.dumps(item, ensure_ascii=False) + "\n")
                
        print(f"已生成测试集 {test_output_path} ({len(test_data)} 条数据)")
        print(f"已生成训练集 {train_output_path} ({len(train_data)} 条数据)")
                
    except Exception as e:
        print(f"处理文件 {input_path} 时出错: {str(e)}")
        raise

def main():
    """主程序入口"""
    raw_dir = "datasets/raw"
    test_dir = "datasets/test"
    train_dir = "datasets/training"
    
    # 创建输出目录
    os.makedirs(test_dir, exist_ok=True)
    os.makedirs(train_dir, exist_ok=True)
    
    # 处理每个csv文件
    processed_count = 0
    for filename in os.listdir(raw_dir):
        if not filename.endswith('.csv'):
            continue
            
        input_path = os.path.join(raw_dir, filename)
        base_name = os.path.splitext(filename)[0]
        
        test_output_path = os.path.join(test_dir, f"{base_name}_test.jsonl")
        train_output_path = os.path.join(train_dir, f"{base_name}_train.jsonl")
        
        process_csv(input_path, test_output_path, train_output_path)
        processed_count += 1
    
    print(f"处理完成,共处理了 {processed_count} 个CSV文件")
    
    # 更新Changelog
    changelog_path = f"Changelog/{datetime.now().strftime('%Y-%m-%d')}.md"
    entry = f"## [{datetime.now().strftime('%Y-%m-%d %H:%M')}]\n- 改用pandas处理CSV文件,提升了编码兼容性\n- 优化了数据处理流程,添加了处理进度输出\n- 改进了错误处理机制\n"
    
    if os.path.exists(changelog_path):
        with open(changelog_path, "a", encoding="utf-8") as f:
            f.write("\n" + entry)
    else:
        with open(changelog_path, "w", encoding="utf-8") as f:
            f.write(entry)

if __name__ == "__main__":
    main()