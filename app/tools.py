"""Agent 可用的工具。目前只有一个：读取本地 CSV 并合计某一列。"""

import csv
from pathlib import Path

from langchain_core.tools import tool


@tool
def sum_csv_column(path: str, column: str) -> str:
    """读取本地 CSV，计算某一数值列的合计。

    path: CSV 文件路径。
    column: 要合计的列名。
    """
    file_path = Path(path)
    if not file_path.is_file():
        return f"文件不存在: {path}"
    if file_path.suffix.lower() != ".csv":
        return f"不是 CSV 文件: {path}"

    total = 0.0
    count = 0
    with file_path.open(newline="", encoding="utf-8-sig") as handle:
        reader = csv.DictReader(handle)
        fields = reader.fieldnames or []
        if column not in fields:
            return f"找不到列 {column!r}。现有列: {', '.join(fields)}"
        for line_no, row in enumerate(reader, start=2):
            raw = (row.get(column) or "").strip()
            if not raw:
                continue
            try:
                total += float(raw)
            except ValueError:
                return f"第 {line_no} 行的 {column!r} 不是数字: {raw!r}"
            count += 1
    return f"{column} 合计 {total:g}，共 {count} 行"
