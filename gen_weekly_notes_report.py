#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
知识库更新周报生成脚本 - 第2期
用法: python gen_weekly_notes_report.py
"""

import sys
import os

# 添加Claw目录到路径
sys.path.insert(0, r"c:/Users/chenx/WorkBuddy/Claw")

from gen_daily_report import build_notes_report

# 第2期 - 2026年5月3日
notes_data = {
    "date_str": "2026年5月3日（第2期）",
    "period": "4月27日 ~ 5月3日",
    "categories": [
        {
            "name": "政治",
            "total": 52,
            "stale_days": -1,
            "custom_added": 0,
            "suggestions": [
                "习近平出席加强基础研究座谈会重要讲话（4月30日）",
                "十四届全国人大常委会第二十二次会议（4月27-30日）",
                "2026年是'十五五'开局之年相关论述"
            ]
        },
        {
            "name": "经济",
            "total": 48,
            "stale_days": -1,
            "custom_added": 0,
            "suggestions": [
                "2026年一季度GDP同比增长5.0%",
                "1-3月全国规模以上工业企业利润增长15.5%",
                "国务院研究稳就业稳经济推动高质量发展举措（4月24日）"
            ]
        },
        {
            "name": "法律",
            "total": 45,
            "stale_days": -1,
            "custom_added": 0,
            "suggestions": [
                "两高贪污贿赂司法解释（二）5月1日起施行",
                "最高法关于适用《海商法》时间效力若干规定5月1日起施行",
                "5月起施行的反腐、金融、食品安全等新规"
            ]
        },
        {
            "name": "历史",
            "total": 38,
            "stale_days": -1,
            "custom_added": 0,
            "suggestions": [
                "5月1日：国际劳动节",
                "5月4日：五四运动纪念日（临近）",
                "4月24日：第11个中国航天日（可补充航天发展史）"
            ]
        },
        {
            "name": "人文",
            "total": 42,
            "stale_days": -1,
            "custom_added": 0,
            "suggestions": [
                "2026年全国知识产权宣传周（4月20日启动）",
                "第三届全民阅读大会在昆明举办（4月20日）"
            ]
        },
        {
            "name": "科技",
            "total": 50,
            "stale_days": -1,
            "custom_added": 0,
            "suggestions": [
                "第11个中国航天日（4月24日），2026年嫦娥七号发射计划",
                "国家超算互联网核心节点上线（3万张国产AI加速芯片）",
                "中国空间站'千眼'天基雷达发射（4月23日）"
            ]
        },
        {
            "name": "地理",
            "total": 35,
            "stale_days": -1,
            "custom_added": 0,
            "suggestions": [
                "粤港澳大湾区首个'华龙一号'核电项目投产（4月20日）",
                "南京至安徽和县高速公路通车（4月22日）"
            ]
        },
        {
            "name": "申论",
            "total": 67,
            "stale_days": -1,
            "custom_added": 0,
            "suggestions": [
                "热点：统筹发展和安全，加快建设新型能源体系",
                "热点：'十五五'开局之年推动高质量发展",
                "热点：基础研究是科技自立自强的源头"
            ]
        }
    ],
    "stats": {
        "total_notes": 417,
        "total_custom": 0,
        "weekly_added": 0
    },
    "action_items": [
        "【政治】本周习近平出席加强基础研究座谈会重要讲话值得加入政治分类",
        "【经济】一季度GDP 5.0%数据和工业企业利润增长15.5%应补充到经济分类",
        "【法律】两高贪污贿赂司法解释（二）和海商法新规5月1日起施行，需加入法律分类",
        "【科技】中国航天日、嫦娥七号计划、超算互联网节点等科技热点值得更新",
        "【申论】'统筹发展和安全'、'基础研究重要性'可作为申论写作素材积累"
    ]
}

# 输出路径
output_path = r"c:/Users/chenx/WorkBuddy/Claw/output/notes_weekly_2026-05-03.pdf"

# 生成PDF
print("正在生成知识库更新周报PDF...")
result = build_notes_report(notes_data, images=None, output_path=output_path)
print(f"✅ PDF已生成: {result}")
