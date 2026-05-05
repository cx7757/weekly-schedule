"""
finance_manager.py - 轩哥财务数据管理工具

用法：
  python finance_manager.py add        交互式添加记录
  python finance_manager.py add --date 2026-05-01 --type expense --cat food --name 午饭 --amount 15 --account wechat
  python finance_manager.py summary     查看本月汇总
  python finance_manager.js summary --month 2026-04  查看指定月汇总
  python finance_manager.py export      导出为浏览器可导入的JSON
  python finance_manager.py list        列出所有记录

数据文件：finance_data.json（与脚本同目录）
"""

import json
import sys
import os
from datetime import datetime, date

DATA_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'finance_data.json')

CATEGORIES = {
    'food': '饭钱', 'shop': '购物', 'daily': '日用品',
    'transport': '交通', 'ent': '娱乐', 'health': '医疗', 'other': '其他'
}
INCOME_SOURCES = ['生活费', '奖学金', '兼职收入', '红包', '其他']
ACCOUNTS = {'alipay': '支付宝', 'wechat': '微信', 'cash': '现金'}


def load_data():
    if not os.path.exists(DATA_FILE):
        return {"meta": {"version": "1.0", "created": str(date.today()),
                         "last_updated": str(date.today()),
                         "description": "轩哥财务数据持久化存储"},
                "settings": {"monthly_budget": 2500, "daily_food_budget": 35,
                             "travel_goal": 5000, "travel_deadline": "2027-06",
                             "fixed_costs": {"饭钱": 1050, "话费": 100, "唇膏": 70, "药费": 53},
                             "fixed_cost_total": 1223},
                "records": [], "monthly_summary": {}}
    with open(DATA_FILE, 'r', encoding='utf-8') as f:
        return json.load(f)


def save_data(data):
    data['meta']['last_updated'] = str(date.today())
    with open(DATA_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def add_record_interactive():
    """交互式添加记录"""
    data = load_data()
    print("=== 添加财务记录 ===")
    print("类型: 1=支出 2=收入")
    rtype = input("选择(1/2): ").strip()
    is_income = rtype == '2'

    today = str(date.today())
    dt = input(f"日期(回车={today}): ").strip() or today

    if is_income:
        print(f"收入来源: {', '.join(INCOME_SOURCES)}")
        source = input("来源: ").strip() or '其他'
        amount = float(input("金额: ").strip() or '0')
        note = input("备注(选填): ").strip()
        acct = input(f"账户({', '.join(ACCOUNTS.values())}, 默认支付宝): ").strip()
        acct_key = [k for k, v in ACCOUNTS.items() if v == acct]
        account = acct_key[0] if acct_key else 'alipay'
        record = {
            "id": len(data['records']) + 1,
            "date": dt, "type": "income",
            "category": "income", "name": source,
            "amount": amount, "note": note, "account": account
        }
    else:
        cats = '\n'.join([f"  {k}={v}" for k, v in CATEGORIES.items()])
        print(f"支出分类:\n{cats}")
        cat = input("分类: ").strip() or 'food'
        if cat not in CATEGORIES:
            print(f"未知分类'{cat}'，已归为其他")
            cat = 'other'
        name = input("名称(如'午饭'，回车=分类名): ").strip() or CATEGORIES[cat]
        amount = float(input("金额: ").strip() or '0')
        note = input("备注(选填): ").strip()
        acct = input(f"账户({', '.join(ACCOUNTS.values())}, 默认微信): ").strip()
        acct_key = [k for k, v in ACCOUNTS.items() if v == acct]
        account = acct_key[0] if acct_key else 'wechat'
        record = {
            "id": len(data['records']) + 1,
            "date": dt, "type": "expense",
            "category": cat, "name": name,
            "amount": amount, "note": note, "account": account
        }

    data['records'].append(record)
    save_data(data)
    print(f"✅ 已记录: {dt} {'[收入]' if is_income else '[支出]'} {record['name']} ¥{amount:.0f}")


def show_summary(month=None):
    """查看月度汇总"""
    data = load_data()
    if not month:
        month = str(date.today())[:7]  # YYYY-MM

    records = [r for r in data['records'] if r['date'].startswith(month)]
    expenses = [r for r in records if r.get('type') != 'income']
    incomes = [r for r in records if r.get('type') == 'income']

    total_exp = sum(r['amount'] for r in expenses)
    total_inc = sum(r['amount'] for r in incomes)

    print(f"\n=== {month} 财务汇总 ===")
    print(f"收入: ¥{total_inc:.0f} ({len(incomes)}笔)")
    print(f"支出: ¥{total_exp:.0f} ({len(expenses)}笔)")
    print(f"结余: ¥{total_inc - total_exp:.0f}")

    if expenses:
        print("\n--- 支出分类 ---")
        cat_sum = {}
        for r in expenses:
            cat = r.get('category', 'other')
            cat_sum[cat] = cat_sum.get(cat, 0) + r['amount']
        for cat, amt in sorted(cat_sum.items(), key=lambda x: -x[1]):
            name = CATEGORIES.get(cat, cat)
            pct = amt / total_exp * 100 if total_exp > 0 else 0
            print(f"  {name}: ¥{amt:.0f} ({pct:.1f}%)")

    if records:
        print("\n--- 明细 ---")
        for r in sorted(records, key=lambda x: x['date'], reverse=True):
            sign = '+' if r.get('type') == 'income' else '-'
            acct = ACCOUNTS.get(r.get('account', ''), '')
            print(f"  {r['date']} {sign}¥{r['amount']:.0f}  {r['name']}  {acct}")

    # 旅游基金进度
    all_months = sorted(set(r['date'][:7] for r in data['records'] if r.get('type') != 'income'))
    total_saved = 0
    s = data['settings']
    for m in all_months:
        m_exp = sum(r['amount'] for r in data['records'] if r['date'].startswith(m) and r.get('type') != 'income')
        m_inc = sum(r['amount'] for r in data['records'] if r['date'].startswith(m) and r.get('type') == 'income')
        budget = m_inc if m_inc > 0 else s['monthly_budget']
        sv = budget - m_exp
        if sv > 0:
            total_saved += sv
    goal = s['travel_goal']
    pct = min(100, total_saved / goal * 100) if goal > 0 else 0
    print(f"\n--- 旅游基金 ---")
    print(f"已攒: ¥{total_saved:.0f} / ¥{goal}  ({pct:.1f}%)")


def list_records():
    """列出所有记录"""
    data = load_data()
    if not data['records']:
        print("暂无记录")
        return
    print(f"共 {len(data['records'])} 条记录\n")
    for r in sorted(data['records'], key=lambda x: (x['date'], x['id'])):
        sign = '+' if r.get('type') == 'income' else '-'
        acct = ACCOUNTS.get(r.get('account', ''), '')
        print(f"  {r['date']} {sign}¥{r['amount']:.0f}  {r['name']}  {acct}  {r.get('note', '')}")


def export_for_browser():
    """导出为财务管家可导入的JSON格式"""
    data = load_data()
    # 转换为浏览器端格式
    browser_records = []
    for r in data['records']:
        browser_records.append({
            "id": r['id'],
            "date": r['date'],
            "type": r.get('type', 'expense'),
            "category": r.get('category', 'food'),
            "name": r['name'],
            "amount": r['amount'],
            "note": r.get('note', ''),
            "account": r.get('account', 'wechat')
        })

    export = {
        "version": "2.3",
        "exported": str(date.today()),
        "records": browser_records,
        "settings": data['settings']
    }

    export_file = DATA_FILE.replace('.json', '_export.json')
    with open(export_file, 'w', encoding='utf-8') as f:
        json.dump(export, f, ensure_ascii=False, indent=2)
    print(f"✅ 已导出到: {export_file}")
    print(f"   共 {len(browser_records)} 条记录")
    print("   可在财务管家 → 设置 → 导入数据 中导入")


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(0)

    cmd = sys.argv[1]
    if cmd == 'add':
        add_record_interactive()
    elif cmd == 'summary':
        month = sys.argv[3] if len(sys.argv) > 2 and sys.argv[2] == '--month' else None
        show_summary(month)
    elif cmd == 'list':
        list_records()
    elif cmd == 'export':
        export_for_browser()
    else:
        print(f"未知命令: {cmd}")
        print(__doc__)
