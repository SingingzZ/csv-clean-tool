# CSV文件清洗与统计分析工具

## 项目简介
使用Python开发的CSV文件清洗与统计分析工具，支持读取CSV文件、清洗数据（去重、去空、数据校验）、异常处理等功能。

## 功能特性
- 自动识别文件编码（UTF-8 / GBK / Latin-1）
- 删除空行（所有字段均为空白）
- 删除完全重复的行
- 自动保留表头行，跳过表头数据校验
- 数据校验：
  - 自动检测表头中是否存在 `age` 列，若存在则校验该列值是否为整数，无效行跳过并打印警告
  - 自动检测表头中是否存在 `city` 列，若存在则校验该列是否为空字符串，为空则跳过并打印警告
- 异常处理：文件不存在、编码错误、列数不一致等
- 输出清洗统计明细，依据实际列名动态展示删除原因

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
### 包含 age/city 列的 CSV
```
File: data.csv
Total rows: 11
Total columns: 3
清洗前: 11行
清洗后: 5行
删除了 6行（其中 2行因为空行，2行因重复，1行因年龄无效，1行因城市为空）
输出文件: cleaned.csv
```

### 不包含 age/city 列的 CSV
```
File: scores.csv
Total rows: 601
Total columns: 14
清洗前: 601行
清洗后: 599行
删除了 2行（其中 1行因为空行，1行因重复）
输出文件: cleaned.csv
```

**说明：** 删除原因仅统计实际发生的类型；若 CSV 表头中不存在 `age` 或 `city` 列，则不会输出对应原因。