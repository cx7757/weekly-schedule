# -*- coding: utf-8 -*-
import sys
import os
sys.path.insert(0, "c:/Users/chenx/WorkBuddy/Claw")
os.makedirs("c:/Users/chenx/WorkBuddy/Claw/output", exist_ok=True)

from gen_daily_report import build_ai_report

n1_title = "DeepSeek V4正式发布并全开源，1.6万亿参数MoE刷新开源纪录"
n1_summary = "4月24日，DeepSeek发布V4-Pro（1.6T参数/49B激活）和V4-Flash（284B参数）双版本，支持百万Token上下文，深度适配华为昇腾910C，KV缓存比V3减少90%，全线开源MIT协议。"
n1_source = "DeepSeek官方/观察者网"

n2_title = "OpenAI同日发布GPT-5.5：最强智能体编码模型，夺回综合榜第一"
n2_summary = "4月24日，OpenAI正式推出GPT-5.5，号称迄今最智能旗舰模型，主打多步骤复杂任务Agent能力。Terminal-Bench 2.0达82.7%准确率，SWE-Bench Pro达58.6%，综合榜重夺第一。"
n2_source = "21经济报道/新浪财经"

n3_title = "腾讯开源混元Hy3 Preview：295B参数MoE，快慢融合思考"
n3_summary = "4月23日，腾讯发布并开源混元Hy3 preview，总参数295B、激活参数21B，支持256K上下文，融合快慢思考，代码智能体和搜索智能体能力突出，API最低1.2元/百万tokens。"
n3_source = "腾讯新闻"

n4_title = "具身智能融资狂飙：它石智航4.55亿美元刷新中国单轮纪录"
n4_summary = "4月16日，具身智能公司它石智航完成4.55亿美元Pre-A轮融资（约31亿元），高瓴、红杉联合领投，美团战投参与。资本评判标准已从看硬件关节根本转向看机器人大脑，2026年具身智能赛道融资狂飙。"
n4_source = "腾讯新闻/36氪"

n5_title = "Meta宣布裁员约10%（约8000人），重押AI大规模投资"
n5_summary = "Meta宣布计划裁减约10%员工（约8000个岗位），将资金用于AI领域巨额投资，裁员行动5月20日启动，是近年硅谷巨头裁员转型AI最典型案例。"
n5_source = "CSDN博客/极客公园"

n6_title = "英伟达黄仁勋强制全员使用OpenAI Codex：AI吃AI时代来临"
n6_summary = "黄仁勋向全体1万名员工发内部邮件，强制所有部门使用OpenAI Codex智能体编程工具，称其为队友和超能力，标志硅谷芯片巨头向AI原生工作模式全面转型。"
n6_source = "CSDN博客/极客公园"

n7_title = "工信部部署AI+质量与普惠算力双线推进"
n7_summary = "工信部副部长表示将在十五五时期推进AI+质量行动，同步宣布开展人工智能中小企业创业支持计划，通过算力银行、算力超市降低中小企业获取算力的门槛。"
n7_source = "CSDN博客"

n8_title = "广东省AI应用对接大会4月27日在深圳举办"
n8_summary = "2026广东省人工智能应用对接大会将于4月27日在深圳福田会展中心举行，主题为智联千行赋能百业，采用1+5模式，聚焦AI全域全行业高水平应用落地。"
n8_source = "深圳特区报"

n9_title = "英特尔Q1超预期，CEO宣告CPU重回AI基础，股价盘后涨20%"
n9_summary = "英特尔发布超预期Q1财报，营收136亿美元（同比+7.2%），盘后股价大涨近20%。CEO表示CPU重新成为人工智能的基础，传统芯片巨头重获AI时代话语权。"
n9_source = "CSDN博客/21经济报道"

n10_title = "ChatGPT遭佛罗里达州刑事调查，AI伦理进入现实法律博弈"
n10_summary = "佛罗里达州总检察长宣布对OpenAI展开刑事调查，指控ChatGPT涉嫌为枪击案嫌疑人提供策划协助。OpenAI回应称GPT仅基于事实回答。AI治理从理论研究进入现实法律博弈。"
n10_source = "CSDN博客"

summary_text = "4月25日前后，DeepSeek V4与GPT-5.5同日巅峰对决，开源大模型首次全面比肩顶级闭源；具身智能融资爆发，机器人大脑成资本新焦点；AI时代全面加速，治理与商业落地同步进入新拐点。"

ai_data = {
    "date_str": "2026年4月25日（第2期）",
    "news": [
        [n1_title, n1_summary, n1_source],
        [n2_title, n2_summary, n2_source],
        [n3_title, n3_summary, n3_source],
        [n4_title, n4_summary, n4_source],
        [n5_title, n5_summary, n5_source],
        [n6_title, n6_summary, n6_source],
        [n7_title, n7_summary, n7_source],
        [n8_title, n8_summary, n8_source],
        [n9_title, n9_summary, n9_source],
        [n10_title, n10_summary, n10_source],
    ],
    "summary": summary_text
}

output_path = "c:/Users/chenx/WorkBuddy/Claw/output/ai_daily_2026-04-25.pdf"
result = build_ai_report(ai_data, images=None, output_path=output_path)
print("SUCCESS:", result)
