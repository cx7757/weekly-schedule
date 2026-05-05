#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
inject_notes.py - 将结构化笔记注入到 index.html 的 NOTES_DB 中
用法：
  python inject_notes.py --input new_notes.json --html index.html
  python inject_notes.py --category "政治" --subcategory "时政热点" --text "新知识点内容"
"""

import json
import re
import argparse
import sys
import os

def load_new_notes(input_file):
    """加载新笔记数据，支持两种格式：
    格式1: [{"category": "政治", "subcategory": "时政热点", "text": "内容"}, ...]
    格式2: {"政治": {"时政热点": [{"t": "内容"}], ...}, ...}
    """
    with open(input_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    return data

def inject_into_html(html_path, new_notes, dry_run=False):
    """
    将新笔记注入到 index.html 的 NOTES_DB 中
    new_notes 格式：
      [{"category": "政治", "subcategory": "时政热点", "text": "知识点内容"}, ...]
      或
      {"政治": {"时政热点": [{"t": "知识点内容"}], ...}}
    """
    with open(html_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # 找到 NOTES_DB 常量
    # 格式: const NOTES_DB = { ... };
    match = re.search(r'(const NOTES_DB\s*=\s*)(\{[\s\S]*?\})\s*;', content)
    if not match:
        print("ERROR: 无法在 index.html 中找到 NOTES_DB 常量", file=sys.stderr)
        sys.exit(1)

    prefix = match.group(1)
    notes_db_str = match.group(2)

    try:
        notes_db = json.loads(notes_db_str)
    except json.JSONDecodeError as e:
        print(f"ERROR: 解析 NOTES_DB 失败: {e}", file=sys.stderr)
        sys.exit(1)

    # 标准化新笔记格式为列表
    if isinstance(new_notes, dict):
        note_list = []
        for cat, subcats in new_notes.items():
            for subcat, items in subcats.items():
                for item in items:
                    if isinstance(item, str):
                        note_list.append({"category": cat, "subcategory": subcat, "text": item})
                    elif isinstance(item, dict) and 't' in item:
                        note_list.append({"category": cat, "subcategory": subcat, "text": item['t']})
    else:
        note_list = new_notes

    added_count = 0
    skipped_count = 0

    for note in note_list:
        cat = note.get('category', '')
        subcat = note.get('subcategory', '')
        text = note.get('text', '').strip()
        if not cat or not subcat or not text:
            continue

        # 确保分类存在
        if cat not in notes_db:
            notes_db[cat] = {}
        if subcat not in notes_db[cat]:
            notes_db[cat][subcat] = []

        # 检查是否已存在（避免重复）
        existing_texts = {item.get('t', '') for item in notes_db[cat][subcat]}
        if text in existing_texts:
            skipped_count += 1
            continue

        notes_db[cat][subcat].append({"t": text})
        added_count += 1

    # 写回
    new_notes_db_str = json.dumps(notes_db, ensure_ascii=False, indent=2)
    new_content = content[:match.start(2)] + new_notes_db_str + content[match.end(2):]

    if dry_run:
        print(f"[DRY RUN] 将新增 {added_count} 条笔记，跳过 {skipped_count} 条重复笔记")
        return added_count

    with open(html_path, 'w', encoding='utf-8') as f:
        f.write(new_content)

    print(f"成功注入 {added_count} 条新笔记到 {html_path}，跳过 {skipped_count} 条重复笔记")
    return added_count

def generate_notes_from_search(topic, search_results):
    """
    根据搜索结果生成结构化笔记
    topic: 分类名称（政治/经济/法律/历史/人文/科技/地理/申论）
    search_results: 搜索结果列表，每个包含 title 和 snippet
    返回: [{"category": "...", "subcategory": "...", "text": "..."}, ...]
    """
    # 子分类映射
    subcat_map = {
        "政治": ["时政热点", "中共党史"],
        "经济": ["经济数据", "经济政策"],
        "法律": ["法律法规", "法律常识"],
        "历史": ["中国近代史", "世界历史"],
        "人文": ["文学常识", "文化常识"],
        "科技": ["科技成就", "科技常识"],
        "地理": ["中国地理", "世界地理"],
        "申论": ["申论素材", "政策解读"]
    }

    notes = []
    subs = subcat_map.get(topic, [topic])

    for result in search_results:
        text = result.get('title', '') + '：' + result.get('snippet', '')
        text = text.strip()[:200]  # 限制长度
        if text:
            notes.append({
                "category": topic,
                "subcategory": subs[0],
                "text": text
            })

    return notes

def main():
    parser = argparse.ArgumentParser(description='将笔记注入到 index.html 的 NOTES_DB 中')
    parser.add_argument('--input', '-i', help='输入JSON文件（包含新笔记数据）')
    parser.add_argument('--html', '-H', default='index.html', help='目标HTML文件（默认: index.html）')
    parser.add_argument('--category', '-c', help='分类名称（直接添加单条时使用）')
    parser.add_argument('--subcategory', '-s', help='子分类名称（直接添加单条时使用）')
    parser.add_argument('--text', '-t', help='知识点内容（直接添加单条时使用）')
    parser.add_argument('--dry-run', action='store_true', help='试运行，不实际修改文件')
    args = parser.parse_args()

    if args.input:
        new_notes = load_new_notes(args.input)
        if isinstance(new_notes, list):
            note_list = new_notes
        else:
            # 转换为列表格式
            note_list = []
            for cat, subcats in new_notes.items():
                for subcat, items in subcats.items():
                    for item in items:
                        if isinstance(item, str):
                            note_list.append({"category": cat, "subcategory": subcat, "text": item})
                        elif isinstance(item, dict) and 't' in item:
                            note_list.append({"category": cat, "subcategory": subcat, "text": item['t']})
            new_notes = note_list
    elif args.category and args.subcategory and args.text:
        new_notes = [{
            "category": args.category,
            "subcategory": args.subcategory,
            "text": args.text
        }]
    else:
        print("ERROR: 必须提供 --input 或直接指定 --category --subcategory --text", file=sys.stderr)
        parser.print_help()
        sys.exit(1)

    inject_into_html(args.html, new_notes, dry_run=args.dry_run)

if __name__ == '__main__':
    main()
