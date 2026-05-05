#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
考公信息爬虫 - exam_tracker/crawler.py
抓取目标：
  1. 浙江省公务员考试录用网 (gwy.zjks.com)
  2. 浙江省事业单位招聘网 (qssy.zjks.com)
  3. 温州市人力资源和社会保障局 (rlzybzj.wenzhou.gov.cn)
  4. 国家公务员局 (www.gov.cn/ldhd/guojia gwy)

运行方式：
  python crawler.py           # 立即抓一次
  python crawler.py --daemon  # 后台定时运行（每天8:00和20:00各抓一次）

依赖安装：
  pip install requests beautifulsoup4 schedule lxml
"""

import os
import json
import time
import hashlib
import logging
import argparse
import datetime
import requests
import schedule
from bs4 import BeautifulSoup
from pathlib import Path

# ── 配置 ────────────────────────────────────────────────────────────────────

DATA_DIR = Path(__file__).parent / "data"
DATA_DIR.mkdir(exist_ok=True)

NOTICES_FILE = DATA_DIR / "notices.json"   # 公告数据库
LOG_FILE     = DATA_DIR / "crawler.log"

# 可选：企业微信/Server酱推送Token（留空则只写文件，不推送）
SERVERCHAN_KEY = ""   # Server酱SendKey，填入后有新公告会推送到微信
WXPUSHER_TOKEN = ""   # WxPusher token（备选）

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/124.0.0.0 Safari/537.36"
    ),
    "Accept-Language": "zh-CN,zh;q=0.9",
}

# 抓取目标配置
TARGETS = [
    {
        "name": "浙江省考-公务员",
        "url": "https://gwy.zjks.com/col/col210/index.html",
        "list_selector": ".listContent li",
        "title_selector": "a",
        "date_selector": "span",
        "base_url": "https://gwy.zjks.com",
        "keywords": ["温州", "公告", "招考", "职位表", "报名"],
    },
    {
        "name": "浙江事业编",
        "url": "https://qssy.zjks.com/col/col12/index.html",
        "list_selector": ".listContent li",
        "title_selector": "a",
        "date_selector": "span",
        "base_url": "https://qssy.zjks.com",
        "keywords": ["温州", "公告", "招聘", "事业单位"],
    },
    {
        "name": "温州人社局",
        "url": "https://rlzybzj.wenzhou.gov.cn/col/col1229075/index.html",
        "list_selector": "ul.list-news li",
        "title_selector": "a",
        "date_selector": ".date",
        "base_url": "https://rlzybzj.wenzhou.gov.cn",
        "keywords": ["招聘", "考试", "公告", "编制", "事业", "国企"],
    },
    {
        "name": "国家公务员局",
        "url": "https://www.neea.edu.cn/",   # 占位，实际用国考官网
        "list_selector": ".news-list li",
        "title_selector": "a",
        "date_selector": "span.date",
        "base_url": "https://www.neea.edu.cn",
        "keywords": ["招录", "公告", "职位表", "报名"],
    },
]

# ── 日志配置 ─────────────────────────────────────────────────────────────────

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler(LOG_FILE, encoding="utf-8"),
        logging.StreamHandler(),
    ],
)
log = logging.getLogger("exam_tracker")


# ── 数据读写 ─────────────────────────────────────────────────────────────────

def load_notices() -> dict:
    if NOTICES_FILE.exists():
        with open(NOTICES_FILE, encoding="utf-8") as f:
            return json.load(f)
    return {}


def save_notices(data: dict):
    with open(NOTICES_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def notice_id(title: str, url: str) -> str:
    """根据标题+URL生成唯一ID，用于去重"""
    return hashlib.md5(f"{title}|{url}".encode()).hexdigest()[:12]


# ── 推送通知 ─────────────────────────────────────────────────────────────────

def push_notification(title: str, content: str):
    """有新公告时推送到微信（需配置 SERVERCHAN_KEY）"""
    if not SERVERCHAN_KEY:
        return
    try:
        url = f"https://sctapi.ftqq.com/{SERVERCHAN_KEY}.send"
        requests.post(url, data={"title": title, "desp": content}, timeout=10)
        log.info(f"推送成功: {title}")
    except Exception as e:
        log.warning(f"推送失败: {e}")


# ── 核心爬取逻辑 ──────────────────────────────────────────────────────────────

def fetch_page(url: str, timeout: int = 15) -> str | None:
    try:
        resp = requests.get(url, headers=HEADERS, timeout=timeout)
        resp.encoding = resp.apparent_encoding or "utf-8"
        return resp.text
    except requests.RequestException as e:
        log.warning(f"请求失败 {url}: {e}")
        return None


def parse_notices(html: str, target: dict) -> list[dict]:
    """解析公告列表，返回 [{title, url, date, source}]"""
    soup = BeautifulSoup(html, "lxml")
    items = soup.select(target["list_selector"])
    results = []
    for item in items[:30]:  # 只取最新30条
        a_tag = item.select_one(target["title_selector"])
        date_tag = item.select_one(target["date_selector"])
        if not a_tag:
            continue
        title = a_tag.get_text(strip=True)
        href  = a_tag.get("href", "")
        date  = date_tag.get_text(strip=True) if date_tag else ""

        # 过滤关键词（只保留相关公告）
        kws = target.get("keywords", [])
        if kws and not any(k in title for k in kws):
            continue

        # 补全URL
        if href.startswith("http"):
            full_url = href
        elif href.startswith("/"):
            full_url = target["base_url"] + href
        else:
            full_url = target["base_url"] + "/" + href

        results.append({
            "id":     notice_id(title, full_url),
            "title":  title,
            "url":    full_url,
            "date":   date,
            "source": target["name"],
            "fetched_at": datetime.datetime.now().strftime("%Y-%m-%d %H:%M"),
        })
    return results


def crawl_once() -> list[dict]:
    """抓取所有目标，返回新增公告列表"""
    existing = load_notices()
    new_notices = []

    for target in TARGETS:
        log.info(f"抓取: {target['name']} -> {target['url']}")
        html = fetch_page(target["url"])
        if not html:
            continue

        items = parse_notices(html, target)
        log.info(f"  解析到 {len(items)} 条相关公告")

        for item in items:
            nid = item["id"]
            if nid not in existing:
                existing[nid] = item
                new_notices.append(item)
                log.info(f"  [新] {item['date']} {item['title']}")

        time.sleep(2)  # 礼貌性延迟，避免被封IP

    save_notices(existing)

    if new_notices:
        summary = "\n".join([f"- [{n['source']}] {n['title']}" for n in new_notices[:5]])
        push_notification(
            f"考公新公告 {len(new_notices)} 条",
            f"以下公告已更新：\n\n{summary}\n\n查看详情请打开 dashboard.html"
        )
        log.info(f"本次新增 {len(new_notices)} 条公告")
    else:
        log.info("本次无新增公告")

    # 每次抓完都重新生成仪表盘
    generate_dashboard(existing)

    return new_notices


# ── 生成仪表盘 ────────────────────────────────────────────────────────────────

def generate_dashboard(notices: dict):
    """根据最新数据重新生成 dashboard.html"""
    dashboard_path = Path(__file__).parent / "dashboard.html"

    # 按来源分组
    by_source: dict[str, list] = {}
    for n in notices.values():
        src = n.get("source", "其他")
        by_source.setdefault(src, []).append(n)

    # 按日期降序
    for src in by_source:
        by_source[src].sort(key=lambda x: x.get("date", ""), reverse=True)

    total = len(notices)
    updated = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")

    # 生成各来源的HTML卡片
    cards_html = ""
    source_colors = {
        "浙江省考-公务员": "#2C5F8A",
        "浙江事业编":      "#27AE60",
        "温州人社局":      "#E05C2A",
        "国家公务员局":    "#8E44AD",
    }

    for source, items in by_source.items():
        color = source_colors.get(source, "#555")
        rows = ""
        for item in items[:20]:
            rows += f"""
            <tr>
              <td><a href="{item['url']}" target="_blank">{item['title']}</a></td>
              <td style="white-space:nowrap;color:#888">{item['date']}</td>
              <td style="white-space:nowrap;color:#aaa;font-size:12px">{item['fetched_at']}</td>
            </tr>"""

        cards_html += f"""
        <div class="card">
          <div class="card-header" style="border-left:4px solid {color}">
            <span class="source-tag" style="background:{color}">{source}</span>
            <span class="count">{len(items)} 条</span>
          </div>
          <table>
            <thead><tr><th>标题</th><th>发布日期</th><th>抓取时间</th></tr></thead>
            <tbody>{rows}</tbody>
          </table>
        </div>"""

    html_content = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>考公信息追踪仪表盘</title>
<style>
  * {{ box-sizing: border-box; margin: 0; padding: 0; }}
  body {{ font-family: "Microsoft YaHei", "PingFang SC", sans-serif;
          background: #f0f2f5; color: #333; }}
  header {{ background: linear-gradient(135deg,#2C5F8A,#1a3d5c);
            color:#fff; padding:24px 32px; }}
  header h1 {{ font-size:22px; margin-bottom:6px; }}
  header p  {{ font-size:13px; opacity:.8; }}
  .stats {{ display:flex; gap:16px; padding:20px 32px; flex-wrap:wrap; }}
  .stat-box {{ background:#fff; border-radius:10px; padding:16px 24px;
               box-shadow:0 2px 8px rgba(0,0,0,.08); min-width:140px; }}
  .stat-box .num {{ font-size:28px; font-weight:700; color:#2C5F8A; }}
  .stat-box .label {{ font-size:13px; color:#888; margin-top:4px; }}
  .main {{ padding:0 32px 32px; }}
  .card {{ background:#fff; border-radius:10px; margin-bottom:20px;
           box-shadow:0 2px 8px rgba(0,0,0,.08); overflow:hidden; }}
  .card-header {{ padding:14px 20px; display:flex; align-items:center;
                  gap:12px; border-bottom:1px solid #f0f0f0; }}
  .source-tag {{ color:#fff; padding:3px 10px; border-radius:20px;
                 font-size:13px; font-weight:600; }}
  .count {{ color:#888; font-size:13px; }}
  table {{ width:100%; border-collapse:collapse; font-size:14px; }}
  th {{ background:#fafafa; padding:10px 16px; text-align:left;
        color:#666; font-weight:500; border-bottom:1px solid #f0f0f0; }}
  td {{ padding:10px 16px; border-bottom:1px solid #f8f8f8; }}
  tr:last-child td {{ border-bottom:none; }}
  tr:hover td {{ background:#f9fbff; }}
  a {{ color:#2C5F8A; text-decoration:none; }}
  a:hover {{ text-decoration:underline; }}
  .refresh-btn {{ position:fixed; bottom:24px; right:24px;
                  background:#2C5F8A; color:#fff; border:none;
                  border-radius:50px; padding:12px 24px; font-size:14px;
                  cursor:pointer; box-shadow:0 4px 12px rgba(0,0,0,.2);
                  display:flex; align-items:center; gap:8px; }}
  .refresh-btn:hover {{ background:#1a3d5c; }}
  .empty {{ padding:32px; text-align:center; color:#aaa; font-size:14px; }}
  @media(max-width:600px) {{
    .stats,.main {{ padding-left:16px; padding-right:16px; }}
    header {{ padding:16px; }}
  }}
</style>
</head>
<body>

<header>
  <h1>📋 考公信息追踪仪表盘</h1>
  <p>数据最后更新：{updated} · 运行 crawler.py 刷新数据</p>
</header>

<div class="stats">
  <div class="stat-box">
    <div class="num">{total}</div>
    <div class="label">累计公告</div>
  </div>
  <div class="stat-box">
    <div class="num">{len(by_source)}</div>
    <div class="label">监控来源</div>
  </div>
  <div class="stat-box">
    <div class="num" id="countdown">--</div>
    <div class="label">距2026浙江省考</div>
  </div>
  <div class="stat-box">
    <div class="num" style="color:#27AE60">{updated.split()[0]}</div>
    <div class="label">上次抓取日期</div>
  </div>
</div>

<div class="main">
  {"".join(cards_html) if cards_html else '<div class="empty">暂无数据，请先运行 crawler.py 抓取</div>'}
</div>

<button class="refresh-btn" onclick="window.location.reload()">
  🔄 刷新页面
</button>

<script>
// 倒计时到2026浙江省考（预计5月份，暂定5月1日）
const examDate = new Date("2026-05-01");
function updateCountdown() {{
  const now = new Date();
  const diff = Math.floor((examDate - now) / 86400000);
  document.getElementById("countdown").textContent =
    diff > 0 ? diff + "天" : "已开始";
}}
updateCountdown();
setInterval(updateCountdown, 60000);
</script>

</body>
</html>"""

    dashboard_path.write_text(html_content, encoding="utf-8")
    log.info(f"仪表盘已更新: {dashboard_path}")


# ── 定时任务 ──────────────────────────────────────────────────────────────────

def run_daemon():
    log.info("守护模式启动，每天 08:00 和 20:00 自动抓取")
    schedule.every().day.at("08:00").do(crawl_once)
    schedule.every().day.at("20:00").do(crawl_once)
    # 启动时先抓一次
    crawl_once()
    while True:
        schedule.run_pending()
        time.sleep(60)


# ── 入口 ─────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="考公信息爬虫")
    parser.add_argument("--daemon", action="store_true", help="守护模式（持续定时运行）")
    args = parser.parse_args()

    if args.daemon:
        run_daemon()
    else:
        crawl_once()
