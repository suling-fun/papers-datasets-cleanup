# merge csv files from /output

import os
import pandas as pd

# 设置输入目录和输出文件路径
input_dir = 'output'
output_file = 'output/merged_output.csv'

# 获取输入目录中的所有CSV文件
csv_files = [f for f in os.listdir(input_dir) if f.endswith('.csv')]

# 初始化一个空的DataFrame来存储合并后的数据
merged_df = pd.DataFrame()

# 遍历每个CSV文件并将其内容追加到merged_df中
for csv_file in csv_files:
    file_path = os.path.join(input_dir, csv_file)
    df = pd.read_csv(file_path)
    merged_df = pd.concat([merged_df, df], ignore_index=True)

# random every row in df
merged_df = merged_df.sample(frac=1).reset_index(drop=True)

# 将合并后的数据保存到输出文件中
merged_df.to_csv(output_file, index=False)
