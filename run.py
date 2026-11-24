"""命令行入口。在项目根目录执行：python run.py"""

import sys

from langchain_core.messages import HumanMessage

from app.graph import build_agent
from app.settings import csv_path, load_config, resolve_api_key


def main() -> None:
    config = load_config()
    if not resolve_api_key(config):
        raise SystemExit("请在 config/config.toml 的 model.api_key 填入阿里云百炼 API Key。")
    question = " ".join(sys.argv[1:]).strip()
    if not question:
        column = config["data"]["column"]
        question = f"读取 {csv_path(config)}，计算 {column} 列的合计。"

    result = build_agent(config).invoke(
        {
            "messages": [
                HumanMessage(content=config["agent"]["system_prompt"]),
                HumanMessage(content=question),
            ]
        }
    )
    print(result["messages"][-1].content)


if __name__ == "__main__":
    main()
