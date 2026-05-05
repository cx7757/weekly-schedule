# -*- coding: utf-8 -*-
import sys
sys.path.insert(0, '.')
from gen_daily_report import build_ai_report
import os

ai_data = {
    'date_str': '2026年4月23日（第4期）',
    'news': [
        ['国务院首次表态支持采购大模型和智能体', '4月21日国务院印发《关于推进服务业扩能提质的意见》，明确提出深入实施人工智能+行动，支持采购大模型、智能体，这是国家层面对AI应用的重大政策利好', '中国政府网/科技圈'],
        ['福布斯发布2026年AI 50榜单：OpenAI与Anthropic融资占比近八成', '福布斯第八届AI 50榜单总融资约3056亿美元，OpenAI与Anthropic合计融资2426亿美元约合1.66万亿元人民币，占榜单总融资约80%', '福布斯/PANews'],
        ['Anthropic年化收入300亿美元反超OpenAI', 'Anthropic凭借Claude在企业级市场的强劲表现，ARR突破300亿美元，商业闭环跑通，但其闭源策略和冲击上下游的做法也引发争议', '21世纪经济报道/Pedaily'],
        ['GPT-6正式发布：200万Token上下文+原生多模态', 'OpenAI完成GPT-6预训练，具备200万Token超长上下文窗口和原生多模态能力，AI大模型竞争进入新阶段', 'CSDN/AI圈'],
        ['国产大模型集体爆发：阿里千问登顶全球调用榜', '4月阿里、字节、腾讯密集发布，DeepSeek、Qwen3.6-Plus、GLM-5.1等国产模型凭借高性价比抢占市场，千问登顶全球调用量榜首', '51CTO/知乎'],
        ['腾讯阿里同日发布世界模型：空间智能成新战场', '4月11日至17日，腾讯和阿里巴巴同天发布世界模型新品，将AI竞争焦点从语言对话推向空间智能领域', '腾讯新闻/163'],
        ['斯坦福发布《2026年人工智能指数报告》', '斯坦福HAI发布年度报告，指出2025年AI模型性能在多项基准测试中逼近人类基线，全球企业AI投资飙升至5817亿美元，但负责任AI治理严重滞后', '斯坦福HAI/腾讯新闻'],
        ['OpenAI Images 2.0发布：图像生成能力大幅提升', 'OpenAI发布Images 2.0模型，在详细指令遵循、物体精准放置及密集文本渲染方面取得巨大进步，支持多种宽高比生成，视觉审美更接近人工设计', '澎湃新闻'],
    ],
    'summary': '4月AI圈密集爆发：政策层面国务院首表态支持大模型采购，资本层面Anthropic年收300亿反超OpenAI，技术层面GPT-6和国产模型集体亮相，竞争焦点转向空间智能。'
}

output_path = 'output/ai_daily_2026-04-23.pdf'
os.makedirs('output', exist_ok=True)
result = build_ai_report(ai_data, images=None, output_path=output_path)
print(f'PDF生成成功: {result}')
