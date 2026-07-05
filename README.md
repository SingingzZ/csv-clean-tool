# CSV文件清洗与统计分析工具

## 项目简介
使用Python开发的CSV文件清洗与统计分析工具，支持读取CSV文件、清洗数据（去重、去空、数据校验）、异常处理等功能。

## 功能特性
- 自动识别文件编码（UTF-8 / GBK / Latin-1）
- 删除空行（所有字段均为空白）
- 删除完全重复的行
- 自动保留表头行，跳过表头数据校验
- 数据校验：
  - 自动检测第 2 列（age）是否为整数，无效行跳过并打印警告
  - 自动检测第 3 列（city）是否为空字符串，为空则跳过并打印警告
- 异常处理：文件不存在、编码错误、列数不一致等
- 输出清洗统计明细

## 开发工具
- 编程语言：Python
- AI编程智能体：Kilo Code
- 版本控制：Git + GitHub

## 使用方法

### 基本用法
```bash
python cleaner.py --input data.csv --output cleaned.csv
```

### 默认参数
```bash
python cleaner.py
```
- 默认读取 `test.csv`
- 默认输出到 `cleaned.csv`

### 参数说明
- `--input`：输入CSV文件路径（默认：test.csv）
- `--output`：输出CSV文件路径（默认：cleaned.csv）

## 输出示例
```
File: scores.csv
Total rows: 601
Total columns: 14
清洗前: 601行
清洗后: 599行
删除了 2行（其中 0行因年龄无效，0行因城市为空）
输出文件: cleaned.csv
```