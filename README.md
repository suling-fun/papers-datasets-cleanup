# Papers Datasets Cleanup

该项目用于整理和管理研究论文数据集，主要功能包括：

- PDF/CAJ文件解析
- 文本提取和转换
- 元数据管理
- 多线程并行处理（支持4线程并发）

## 文件结构

- `Papers/`: 存储原始论文文件
- `output/`: 存储处理后的数据集
- `Changelog/`: 记录项目变更

## 项目依赖

- torch==2.5.1
- torchvision==0.20.1
- markitdown==0.0.1a3
- marker-pdf==1.2.4

## .gitignore

项目包含.gitignore文件，用于忽略以下文件类型：

- 系统文件 (.DS_Store)
- Python编译文件 (*.pyc, __pycache__/)
- 日志文件 (*.log)
- 环境变量文件 (.env)
- 输出目录 (/output/)