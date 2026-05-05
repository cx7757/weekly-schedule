#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
gen_daily_notes.py - 每日生成考公笔记并注入到 index.html
用法：
  python gen_daily_notes.py --date 2026-05-03
  python gen_daily_notes.py  # 默认今天
"""

import json
import argparse
import sys
import os
import subprocess
import re
from datetime import datetime, timedelta

# 分类与搜索关键词映射
TOPIC_KEYWORDS = {
    "政治": ["2026年5月 时政热点 考公", "最新政治理论 方针政策 2026"],
    "经济": ["2026年 经济数据 CPI GDP 最新", "最新经济政策 产业政策 2026"],
    "法律": ["2026年 新出台法律法规 修订", "最新司法解释 考公法律常识"],
    "历史": ["本周历史纪念日 历史事件", "中国近代史 世界历史 常识"],
    "人文": ["文学常识 文化常识 考公", "人文知识 2026"],
    "科技": ["2026年 科技成就 航天 AI 突破", "最新科技创新 国家科技奖"],
    "地理": ["中国地理 世界地理 常识 考公", "最新地理发现 资源环境"],
    "申论": ["申论素材 政策解读 2026", "申论写作技巧 范文"]
}

# 分类 -> 子分类映射
CAT_SUBCAT = {
    "政治": "时政热点",
    "经济": "经济数据",
    "法律": "法律法规",
    "历史": "中国近代史",
    "人文": "文学常识",
    "科技": "科技成就",
    "地理": "中国地理",
    "申论": "申论素材"
}

def get_today_str():
    return datetime.now().strftime("%Y-%m-%d")

def get_week_range(date_str):
    """获取本周起止日期"""
    d = datetime.strptime(date_str, "%Y-%m-%d")
    start = d - timedelta(days=d.weekday())  # 周一
    end = start + timedelta(days=6)  # 周日
    return start.strftime("%Y-%m-%d"), end.strftime("%Y-%m-%d")

def search_with_web(topic, keywords, max_results=3):
    """
    使用 web_search 获取考公相关内容
    注意：此函数需要在 WorkBuddy 环境中由 AI 直接调用 web_search，
    这里只定义数据结构，实际搜索由自动化任务中的 AI 完成。
    返回格式：[{"title": "...", "snippet": "..."}, ...]
    """
    # 此函数仅供文档参考，实际搜索在自动化 prompt 中完成
    return []

def build_notes_from_search(topic, search_results):
    """将搜索结果转换为笔记格式"""
    notes = []
    subcat = CAT_SUBCAT.get(topic, topic)
    
    for i, result in enumerate(search_results[:5]):
        title = result.get("title", "")
        snippet = result.get("snippet", "")
        text = f"{title}：{snippet}".strip()
        # 清理多余空白
        text = re.sub(r'\s+', ' ', text).strip()
        if len(text) > 150:
            text = text[:150] + "..."
        if text:
            notes.append({
                "category": topic,
                "subcategory": subcat,
                "text": text
            })
    
    return notes

def save_notes_json(notes, output_path):
    """保存笔记为JSON文件"""
    os.makedirs(os.path.dirname(output_path) or ".", exist_ok=True)
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(notes, f, ensure_ascii=False, indent=2)
    return output_path

def run_inject(html_path, json_path):
    """调用 inject_notes.py 注入笔记"""
    result = subprocess.run(
        ["python", "inject_notes.py", "--input", json_path, "--html", html_path],
        capture_output=True, text=True, encoding="utf-8"
    )
    return result.stdout + result.stderr

def git_commit_push(date_str, note_count):
    """提交并推送到GitHub"""
    cmds = [
        f'git add index.html',
        f'git commit -m "docs: 考公知识库每日更新 {date_str}（+{note_count}条）"',
        f'git push origin main'
    ]
    results = []
    for cmd in cmds:
        result = subprocess.run(
            cmd, shell=True, capture_output=True, text=True, encoding="utf-8"
        )
        results.append(result.stdout + result.stderr)
    return results

def main():
    parser = argparse.ArgumentParser(description='每日生成考公笔记并注入到 index.html')
    parser.add_argument('--date', '-d', help='日期（YYYY-MM-DD格式，默认今天）')
    parser.add_argument('--html', '-H', default='index.html', help='目标HTML文件')
    parser.add_argument('--topics', '-t', nargs='+', 
                        choices=list(TOPIC_KEYWORDS.keys()),
                        help='指定分类（默认全部）')
    parser.add_argument('--dry-run', action='store_true', help='试运行，不实际修改')
    args = parser.parse_args()

    date_str = args.date or get_today_str()
    html_path = args.html
    topics = args.topics or list(TOPIC_KEYWORDS.keys())

    print(f"[{date_str}] 开始生成考公笔记...")
    print(f"目标分类: {', '.join(topics)}")

    all_notes = []
    for topic in topics:
        # 这里实际需要由 AI 调用 web_search 获取内容
        # 脚本只负责接收搜索结果并注入
        print(f"  处理分类: {topic}")
        # 搜索结果由调用方提供，这里仅作占位
        # 实际使用时，AI 会先搜索，再把结果传入

    if args.dry_run:
        print(f"[DRY RUN] 将生成笔记并注入，但不会实际修改文件")
        return

    # 实际执行时，搜索结果通过 stdin 或文件传入
    # 格式：JSON数组，每个元素包含 title 和 snippet
    if not sys.stdin.isatty():
        try:
            search_results = json.load(sys.stdin)
            all_notes = build_notes_from_search(topics[0], search_results)
        except:
            pass

    print(f"生成了 {len(all_notes)} 条笔记")
    
    if not all_notes:
        print("没有新笔记需要注入，退出。")
        return

    # 保存为JSON
    json_path = f"notes_daily_{date_str.replace('-', '')}.json"
    save_notes_json(all_notes, json_path)
    print(f"笔记已保存到 {json_path}")

    # 注入到HTML
    inject_result = run_inject(html_path, json_path)
    print(f"注入结果: {inject_result}")

    # Git提交推送
    git_result = git_commit_push(date_str, len(all_notes))
    print(f"Git结果: {git_result}")

if __name__ == '__main__':
    main()
