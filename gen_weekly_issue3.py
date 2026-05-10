# -*- coding: utf-8 -*-
"""生成第3期知识库更新周报PDF"""
import sys
import os
sys.path.insert(0, os.path.dirname(__file__))
from gen_daily_report import build_notes_report

output_path = os.path.join(os.path.dirname(__file__), 'output', 'notes_weekly_2026-05-10.pdf')

notes_data = {
    'date_str': '2026年5月10日（第3期）',
    'period': '5月4日 ~ 5月10日',
    'categories': [
        {
            'name': '政治',
            'total': 72,
            'stale_days': -1,
            'custom_added': 0,
            'suggestions': [
                '4月28日中央政治局会议分析经济形势，强调"四稳"（稳就业、稳企业、稳市场、稳预期），需掌握会议要点',
                '新华社5月4日发布《大国之大利天下——2026年春季中国元首外交纪事》，回顾莫桑比克总统访华等外交大事',
                '5月1日起中国对全部非洲建交国实施零关税，成为全球首个实现全覆盖零关税的主要经济体'
            ]
        },
        {
            'name': '经济',
            'total': 65,
            'stale_days': -1,
            'custom_added': 0,
            'suggestions': [
                '一季度GDP同比增长5.0%，主要指标好于预期，政治局会议要求"以更大力度抓好经济工作"',
                '政治局会议提出挖掘内需潜力，推动消费升级，加强"六网"建设（水网、电网、算力网、通信网、管网、物流网）',
                '2026年预算赤字率或继续突破4%，新增专项债限额或为4.5万亿'
            ]
        },
        {
            'name': '法律',
            'total': 58,
            'stale_days': -1,
            'custom_added': 0,
            'suggestions': [
                '最高法行政诉讼起诉期限司法解释（法释[2026]3号）5月1日起施行，涉及诉权保障',
                '5月新规：商业短信治理、外卖安全监管、殡葬明码标价、海商法调整等多项法规施行',
                '全国人大常委会2026年度立法工作计划公布，继续审议法律案15件'
            ]
        },
        {
            'name': '历史',
            'total': 45,
            'stale_days': -1,
            'custom_added': 0,
            'suggestions': [
                '5月4日五四运动纪念日（1919年），反帝反封建爱国运动爆发',
                '5月5日马克思诞辰纪念日（1818年），马克思主义创始人',
                '5月10日《实践是检验真理的唯一标准》发表（1978年），引发全国真理标准大讨论'
            ]
        },
        {
            'name': '人文',
            'total': 40,
            'stale_days': -1,
            'custom_added': 0,
            'suggestions': [
                '五四青年节相关人文知识，五四精神与当代价值',
                '立夏节气（5月5日），二十四节气相关知识可补充'
            ]
        },
        {
            'name': '科技',
            'total': 52,
            'stale_days': -1,
            'custom_added': 0,
            'suggestions': [
                '人工智能终端系列国家标准5月8日发布，覆盖手机、眼镜、汽车等7个品类智能化分级',
                '2026世界数字教育大会5月11-13日杭州举办，主题"人工智能+教育"，将发布八项成果',
                '腾讯发布混元2.0模型（可生成3D世界），Meta开源Llama4大模型'
            ]
        },
        {
            'name': '地理',
            'total': 42,
            'stale_days': -1,
            'custom_added': 0,
            'suggestions': [
                '莫桑比克国家概况，中莫建交50周年（1975年建交）',
                '浙江杭州承办世界数字教育大会，可补充杭州城市地理知识'
            ]
        },
        {
            'name': '申论',
            'total': 43,
            'stale_days': -1,
            'custom_added': 0,
            'suggestions': [
                '"以更大力度和更实举措抓好经济工作"可作为申论经济类话题素材',
                '"人工智能+教育"主题适合教育类申论写作，关注AI与教育公平'
            ]
        }
    ],
    'stats': {
        'total_notes': 417,
        'total_custom': 0,
        'weekly_added': 0
    },
    'action_items': [
        '【政治】4月28日政治局会议是本周最重要考点，"四稳"、"六网建设"、"十五五良好开局"等表述务必掌握',
        '【经济】一季度GDP+5.0%的数据和政治局对经济形势的判断（起步有力、基础需稳固）要重点记忆',
        '【法律】5月新规集中施行，特别是行政诉讼起诉期限司法解释和商业短信治理新规值得补充',
        '【历史】本周三大历史纪念日（五四运动5.4、马克思诞辰5.5、真理标准讨论5.10），是常识题高频考点',
        '【科技】AI终端国家标准和世界数字教育大会是"人工智能+"主题的重要时事素材，适合申论和常识',
        '【备考提醒】距2026年11月国考约6个月，建议本周开始系统复习时政和常识模块'
    ]
}

os.makedirs(os.path.dirname(output_path), exist_ok=True)
result = build_notes_report(notes_data, output_path=output_path)
print(f'PDF generated: {result}')
print(f'File exists: {os.path.exists(result)}')
print(f'File size: {os.path.getsize(result)} bytes')
