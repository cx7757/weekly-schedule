# -*- coding: utf-8 -*-
"""
知识库更新周报生成器 - 第1期 (2026-04-26)
自动生成PDF并保存到output目录
"""
import sys
import os

sys.path.insert(0, "c:/Users/chenx/WorkBuddy/Claw")
os.makedirs("c:/Users/chenx/WorkBuddy/Claw/output", exist_ok=True)

from gen_daily_report import build_notes_report

notes_data = {
    "date_str": "2026年4月26日（第1期）",
    "period": "4月20日 ~ 4月26日",
    "categories": [
        {
            "name": "政治",
            "total": 68,
            "stale_days": -1,
            "custom_added": 0,
            "suggestions": [
                "习近平同莫桑比克总统查波会谈（4月21日），提升双边关系",
                "中老建交65周年互致贺电（4月25日），中老命运共同体建设",
                "各地传达学习习近平近期重要讲话精神"
            ]
        },
        {
            "name": "经济",
            "total": 54,
            "stale_days": -1,
            "custom_added": 0,
            "suggestions": [
                "2026年一季度GDP同比增长5.0%，总量334193亿元（4月16日）",
                "LPR连续11个月不变：1年期3.0%，5年期以上3.5%（4月20日）",
                "一季度农村居民收入增速5.4%高于城镇，城乡收入差距持续收窄"
            ]
        },
        {
            "name": "法律",
            "total": 47,
            "stale_days": -1,
            "custom_added": 0,
            "suggestions": [
                "两高发布《贪污贿赂刑事案件司法解释（二）》，5月1日施行，加大隐性腐败惩治",
                "最高法发布《侵害知识产权民事纠纷惩罚性赔偿解释》（4月20日）",
                "完善介绍贿赂罪相关规定，聚焦新型腐败形式"
            ]
        },
        {
            "name": "历史",
            "total": 42,
            "stale_days": -1,
            "custom_added": 0,
            "suggestions": [
                "4月24日：中国航天日，2026年是航天事业创建70周年（1956-2026）",
                "4月24日：东方红一号发射纪念日（1970年，第11个航天日）",
                "中老建交65周年：中老友好合作历史背景值得整理"
            ]
        },
        {
            "name": "人文",
            "total": 38,
            "stale_days": -1,
            "custom_added": 0,
            "suggestions": [
                "中国航天文化：载人航天精神、航天强国战略",
                "中非友好合作：中莫关系提升，非洲外交新动态"
            ]
        },
        {
            "name": "科技",
            "total": 52,
            "stale_days": -1,
            "custom_added": 0,
            "suggestions": [
                "中国首批外籍航天员：2名巴基斯坦航天员入选，4月24日赴京参训",
                "第11个中国航天日：十五五规划多项航天重大成果发布，国际合作加速",
                "嫦娥五号月球样品新研究成果即将发布"
            ]
        },
        {
            "name": "地理",
            "total": 44,
            "stale_days": -1,
            "custom_added": 0,
            "suggestions": [
                "中老铁路沿线区域发展：中老建交65周年，互联互通成果",
                "莫桑比克地理区位：东南非洲，印度洋沿岸国家"
            ]
        },
        {
            "name": "申论",
            "total": 72,
            "stale_days": -1,
            "custom_added": 0,
            "suggestions": [
                "一季度GDP增5%：可作为经济高质量发展、新质生产力论据",
                "航天强国：科技自立自强、创新驱动发展战略申论素材",
                "城乡收入差距收窄：共同富裕、乡村振兴政策成效素材"
            ]
        }
    ],
    "stats": {
        "total_notes": 417,
        "total_custom": 0,
        "weekly_added": 0
    },
    "action_items": [
        "【政治】将习近平本周外事活动（中莫会谈、中老65周年）录入政治分类",
        "【经济】将一季度GDP 5.0%、LPR不变等核心数据更新到经济分类",
        "【法律】两高贪污贿赂司法解释（二）重点整理，5月1日考点",
        "【科技/历史】4月24日中国航天日双重打卡：70周年成就+首批外籍航天员",
        "【申论】整理本周政治经济要点为申论万能素材库，对应国考考点"
    ]
}

output_path = "c:/Users/chenx/WorkBuddy/Claw/output/notes_weekly_2026-04-26.pdf"
result = build_notes_report(notes_data, images=None, output_path=output_path)
print(f"SUCCESS: {result}")
