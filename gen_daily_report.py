# -*- coding: utf-8 -*-
"""
每日信息日报 PDF 生成器
用法: python gen_daily_report.py --title "标题" --content "正文内容" --images img1.jpg,img2.png --output output.pdf

功能：
- 将每日推送的考公/AI资讯整理为精美PDF
- 支持内嵌图片（招聘截图、新闻配图等）
- 彩色分类表格、手机友好的排版
"""
import argparse
import os
import sys
from datetime import datetime

from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import mm, cm
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.lib.colors import HexColor, white, black
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    HRFlowable, Image as RLImage, KeepTogether
)
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

# ===== Font =====
_font_candidates = [
    ("C:/Windows/Fonts/msyh.ttc", "msyh"),
    ("C:/Windows/Fonts/msyhbd.ttc", "msyhbd"),
    ("C:/Windows/Fonts/simhei.ttf", "simhei"),
    ("C:/Windows/Fonts/simsun.ttc", "simsun"),
]
FONT = "Helvetica"
FONT_BOLD = "Helvetica-Bold"
for fp, name in _font_candidates:
    if os.path.exists(fp):
        try:
            pdfmetrics.registerFont(TTFont(name, fp))
            if FONT == "Helvetica":
                FONT = name
                FONT_BOLD = name
            if "bd" in name.lower() or "bold" in name.lower():
                FONT_BOLD = name
        except Exception:
            continue

# ===== Colors =====
C_PRIMARY = HexColor("#1a5276")
C_SECONDARY = HexColor("#2980b9")
C_ACCENT = HexColor("#e74c3c")
C_HEADER_BG = HexColor("#2c3e50")
C_ROW_EVEN = HexColor("#f8f9fa")
C_ROW_ODD = HexColor("#ffffff")
C_URGENT = HexColor("#c0392b")
C_WARN = HexColor("#e67e22")
C_OK = HexColor("#27ae60")
C_INFO = HexColor("#2980b9")
C_LIGHT_BG = HexColor("#eaf2f8")
C_GRAY = HexColor("#7f8c8d")
C_LIGHT_GRAY = HexColor("#bdc3c7")

# ===== Styles =====
STYLES = {}

def get_style(name, **kwargs):
    if name not in STYLES:
        STYLES[name] = ParagraphStyle(name, fontName=FONT, **kwargs)
    return STYLES[name]

def init_styles():
    STYLES["title"] = get_style("title", fontSize=20, textColor=C_PRIMARY,
                                 spaceAfter=4*mm, alignment=TA_CENTER, leading=28)
    STYLES["subtitle"] = get_style("subtitle", fontSize=11, textColor=C_GRAY,
                                    spaceAfter=6*mm, alignment=TA_CENTER, leading=16)
    STYLES["h1"] = get_style("h1", fontSize=14, textColor=C_PRIMARY,
                              spaceBefore=6*mm, spaceAfter=3*mm, leading=20)
    STYLES["h2"] = get_style("h2", fontSize=12, textColor=C_SECONDARY,
                              spaceBefore=4*mm, spaceAfter=2*mm, leading=18)
    STYLES["h3"] = get_style("h3", fontSize=10.5, textColor=HexColor("#34495e"),
                              spaceBefore=3*mm, spaceAfter=2*mm, leading=16)
    STYLES["body"] = get_style("body", fontSize=9.5, textColor=HexColor("#2c3e50"),
                                spaceAfter=2*mm, leading=15)
    STYLES["body_small"] = get_style("body_small", fontSize=8.5, textColor=HexColor("#2c3e50"),
                                      spaceAfter=1.5*mm, leading=13)
    STYLES["urgent"] = get_style("urgent", fontSize=10, textColor=C_URGENT,
                                  spaceAfter=2*mm, leading=15)
    STYLES["warn"] = get_style("warn", fontSize=10, textColor=C_WARN,
                                spaceAfter=2*mm, leading=15)
    STYLES["ok"] = get_style("ok", fontSize=10, textColor=C_OK,
                              spaceAfter=2*mm, leading=15)
    STYLES["note"] = get_style("note", fontSize=8, textColor=C_GRAY,
                                spaceAfter=1*mm, leading=12)
    STYLES["footer"] = get_style("footer", fontSize=7.5, textColor=C_LIGHT_GRAY,
                                  alignment=TA_CENTER, leading=11)
    STYLES["th"] = get_style("th", fontSize=9, textColor=white,
                              alignment=TA_CENTER, leading=13)
    STYLES["td"] = get_style("td", fontSize=8.5, textColor=HexColor("#2c3e50"),
                              leading=13)
    STYLES["td_c"] = get_style("td_c", fontSize=8.5, textColor=HexColor("#2c3e50"),
                                alignment=TA_CENTER, leading=13)
    STYLES["img_caption"] = get_style("img_caption", fontSize=8, textColor=C_GRAY,
                                       alignment=TA_CENTER, spaceAfter=3*mm, leading=11)

init_styles()

# ===== PDF Builder =====
class DailyReportPDF:
    def __init__(self, title, subtitle="", output_path="daily_report.pdf"):
        self.title = title
        self.subtitle = subtitle
        self.output_path = output_path
        self.story = []
        self.doc = SimpleDocTemplate(
            output_path,
            pagesize=A4,
            rightMargin=1.5*cm,
            leftMargin=1.5*cm,
            topMargin=1.5*cm,
            bottomMargin=1.5*cm,
        )

    def add_title_page(self):
        """添加标题区域"""
        self.story.append(Paragraph(self.title, STYLES["title"]))
        if self.subtitle:
            self.story.append(Paragraph(self.subtitle, STYLES["subtitle"]))
        self.story.append(HRFlowable(width="100%", thickness=1.5, color=C_SECONDARY,
                                      spaceAfter=4*mm))
        today = datetime.now().strftime("%Y年%m月%d日")
        self.story.append(Paragraph(f"生成日期：{today}", STYLES["note"]))
        self.story.append(Spacer(1, 3*mm))

    def add_section(self, title, level=1):
        """添加章节标题"""
        key = f"h{level}" if level <= 2 else "h3"
        color_map = {1: C_PRIMARY, 2: C_SECONDARY}
        c = color_map.get(level, HexColor("#34495e"))
        style = get_style(f"sec_{title}_{level}", fontSize=[0, 14, 12, 10.5][level],
                          textColor=c, spaceBefore=[0, 6, 4, 3][level]*mm,
                          spaceAfter=[0, 3, 2, 2][level]*mm,
                          leading=[0, 20, 18, 16][level])
        self.story.append(Paragraph(f"<b>{title}</b>", style))

    def add_body(self, text, style_key="body"):
        """添加正文段落"""
        self.story.append(Paragraph(text, STYLES.get(style_key, STYLES["body"])))

    def add_colored_body(self, text, color, style_key="body"):
        """添加彩色正文"""
        s = get_style(f"cb_{style_key}_{id(text)}", fontSize=9.5, textColor=color,
                      spaceAfter=2*mm, leading=15)
        self.story.append(Paragraph(text, s))

    def add_bullet(self, text, indent=8):
        """添加要点列表"""
        s = get_style(f"bullet_{id(text)}", fontSize=9.5, textColor=HexColor("#2c3e50"),
                      leftIndent=indent, spaceAfter=1.5*mm, leading=15,
                      bulletIndent=2, bulletFontSize=8)
        self.story.append(Paragraph(f"• {text}", s))

    def add_spacer(self, height=3):
        self.story.append(Spacer(1, height*mm))

    def add_table(self, headers, rows, col_widths=None, urgent_first_rows=0):
        """添加彩色表格
        urgent_first_rows: 前N行用红色高亮
        """
        # Header row
        data = [[Paragraph(f"<b>{h}</b>", STYLES["th"]) for h in headers]]
        for row in rows:
            data.append([Paragraph(str(c), STYLES["td_c"]) if len(str(c)) < 15
                         else Paragraph(str(c), STYLES["td"]) for c in row])

        n_cols = len(headers)
        if not col_widths:
            available = A4[0] - 3*cm
            col_widths = [available / n_cols] * n_cols

        style_cmds = [
            ('BACKGROUND', (0, 0), (-1, 0), C_HEADER_BG),
            ('TEXTCOLOR', (0, 0), (-1, 0), white),
            ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, -1), FONT),
            ('FONTSIZE', (0, 0), (-1, -1), 8.5),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
            ('TOPPADDING', (0, 0), (-1, -1), 5),
            ('LEFTPADDING', (0, 0), (-1, -1), 4),
            ('RIGHTPADDING', (0, 0), (-1, -1), 4),
            ('GRID', (0, 0), (-1, -1), 0.5, C_LIGHT_GRAY),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ]

        # Row backgrounds
        for i in range(1, len(data)):
            if i <= urgent_first_rows:
                style_cmds.append(('BACKGROUND', (0, i), (-1, i), HexColor("#fdedec")))
            elif i % 2 == 0:
                style_cmds.append(('BACKGROUND', (0, i), (-1, i), C_ROW_EVEN))
            else:
                style_cmds.append(('BACKGROUND', (0, i), (-1, i), C_ROW_ODD))

        t = Table(data, colWidths=col_widths)
        t.setStyle(TableStyle(style_cmds))
        self.story.append(t)
        self.story.append(Spacer(1, 3*mm))

    def add_image(self, img_path, caption="", max_width=16*cm, max_height=10*cm):
        """添加图片，自动缩放"""
        if not os.path.exists(img_path):
            self.add_colored_body(f"[图片未找到: {img_path}]", C_ACCENT, "body_small")
            return

        try:
            from PIL import Image
            pil_img = Image.open(img_path)
            w, h = pil_img.size
            ratio = min(max_width / w, max_height / h, 1.0)
            display_w = w * ratio
            display_h = h * ratio
        except ImportError:
            # PIL not available, use reportlab's default sizing
            display_w = max_width
            display_h = max_height

        img = RLImage(img_path, width=display_w, height=display_h)
        if caption:
            self.story.append(KeepTogether([
                img,
                Spacer(1, 1*mm),
                Paragraph(caption, STYLES["img_caption"]),
            ]))
        else:
            self.story.append(img)
        self.story.append(Spacer(1, 3*mm))

    def add_divider(self):
        self.story.append(HRFlowable(width="100%", thickness=0.5, color=C_LIGHT_GRAY,
                                      spaceAfter=3*mm))

    def add_page_break(self):
        self.story.append(__import__("reportlab.platypus", fromlist=["PageBreak"]).PageBreak())

    def add_footer(self):
        self.story.append(Spacer(1, 5*mm))
        self.story.append(HRFlowable(width="100%", thickness=0.5, color=C_LIGHT_GRAY,
                                      spaceAfter=2*mm))
        today = datetime.now().strftime("%Y-%m-%d %H:%M")
        self.story.append(Paragraph(
            f"小轩同学 每日信息日报 | {today} 自动生成",
            STYLES["footer"]
        ))

    def build(self):
        self.doc.build(self.story)
        print(f"PDF generated: {self.output_path}")
        return self.output_path


# ===== Quick helpers for automation =====
def build_exam_report(exam_data, images=None, output_path="exam_daily.pdf"):
    """快速生成考公信息日报PDF
    exam_data: dict with keys:
        - urgent: list of [title, detail, deadline]
        - important: list of [title, detail, deadline]
        - excluded: list of [name, reason]
        - actions: list of action strings
        - date_str: e.g. "2026年4月22日（第6期）"
    """
    pdf = DailyReportPDF(
        title="温州考公信息日报",
        subtitle=exam_data.get("date_str", ""),
        output_path=output_path
    )
    pdf.add_title_page()

    # Urgent section
    urgent = exam_data.get("urgent", [])
    if urgent:
        pdf.add_section("今日紧急提醒")
        rows = []
        for item in urgent:
            rows.append([item[0], item[1] if len(item) > 1 else "", item[2] if len(item) > 2 else ""])
        pdf.add_table(["招聘单位", "详情", "截止时间"], rows,
                      col_widths=[4.5*cm, 8*cm, 3.5*cm], urgent_first_rows=len(rows))

    # Important section
    important = exam_data.get("important", [])
    if important:
        pdf.add_section("重点关注")
        rows = []
        for item in important:
            rows.append([item[0], item[1] if len(item) > 1 else "", item[2] if len(item) > 2 else ""])
        pdf.add_table(["招聘单位", "详情", "截止时间"], rows,
                      col_widths=[4.5*cm, 8*cm, 3.5*cm])

    # Images
    if images:
        pdf.add_section("资料截图")
        for img_info in images:
            if isinstance(img_info, str):
                pdf.add_image(img_info)
            elif isinstance(img_info, (list, tuple)):
                pdf.add_image(img_info[0], caption=img_info[1] if len(img_info) > 1 else "")

    # Excluded
    excluded = exam_data.get("excluded", [])
    if excluded:
        pdf.add_section("排除项（不符合条件）")
        rows = [[item[0], item[1] if len(item) > 1 else ""] for item in excluded]
        pdf.add_table(["招聘单位", "排除原因"], rows, col_widths=[6*cm, 10*cm])

    # Actions
    actions = exam_data.get("actions", [])
    if actions:
        pdf.add_section("行动清单")
        for i, action in enumerate(actions, 1):
            pdf.add_bullet(action)

    pdf.add_footer()
    return pdf.build()


def build_ai_report(ai_data, images=None, output_path="ai_daily.pdf"):
    """快速生成AI资讯日报PDF
    ai_data: dict with keys:
        - date_str: e.g. "2026年4月22日"
        - news: list of [title, summary, source]
        - summary: one-line daily summary
    """
    pdf = DailyReportPDF(
        title="AI资讯日报",
        subtitle=ai_data.get("date_str", ""),
        output_path=output_path
    )
    pdf.add_title_page()

    news = ai_data.get("news", [])
    if news:
        pdf.add_section("今日AI圈重要动态")
        rows = []
        for i, item in enumerate(news, 1):
            title = f"{i}. {item[0]}"
            summary = item[1] if len(item) > 1 else ""
            source = item[2] if len(item) > 2 else ""
            rows.append([title, summary, source])
        pdf.add_table(["标题", "摘要", "来源"], rows,
                      col_widths=[4*cm, 9*cm, 3*cm])

    # Images
    if images:
        pdf.add_section("相关图片")
        for img_info in images:
            if isinstance(img_info, str):
                pdf.add_image(img_info)
            elif isinstance(img_info, (list, tuple)):
                pdf.add_image(img_info[0], caption=img_info[1] if len(img_info) > 1 else "")

    # Daily summary
    summary = ai_data.get("summary", "")
    if summary:
        pdf.add_divider()
        pdf.add_section("一句话总结")
        pdf.add_colored_body(summary, C_SECONDARY)

    pdf.add_footer()
    return pdf.build()


def build_notes_report(notes_data, images=None, output_path="notes_weekly.pdf"):
    """生成知识库更新提醒周报PDF
    notes_data: dict with keys:
        - date_str: e.g. "2026年4月26日（第1期）"
        - period: e.g. "4月20日 ~ 4月26日"
        - categories: list of dicts:
            - name: 分类名 (e.g. "政治")
            - total: 该分类总知识点数
            - custom_added: 本周自定义新增数量
            - stale_days: 距上次更新的天数（-1表示从未自定义更新过）
            - suggestions: list of 建议更新的内容
        - stats: dict with keys:
            - total_notes: 总知识点数
            - total_custom: 总自定义数
            - weekly_added: 本周新增自定义数
        - action_items: list of 行动建议
    """
    pdf = DailyReportPDF(
        title="📚 知识库更新周报",
        subtitle=notes_data.get("date_str", ""),
        output_path=output_path
    )
    pdf.add_title_page()

    # 本周概览
    stats = notes_data.get("stats", {})
    pdf.add_section("📊 本周概览")
    overview_rows = [
        ["总知识点数", str(stats.get("total_notes", "-"))],
        ["自定义知识点", str(stats.get("total_custom", "-"))],
        ["本周新增", str(stats.get("weekly_added", "-")) + " 条"],
    ]
    pdf.add_table(["指标", "数值"], overview_rows, col_widths=[6*cm, 6*cm])

    # 各分类状态
    categories = notes_data.get("categories", [])
    if categories:
        pdf.add_section("📁 分类状态")
        cat_rows = []
        for cat in categories:
            name = cat.get("name", "")
            total = cat.get("total", "-")
            stale = cat.get("stale_days", -1)
            added = cat.get("custom_added", 0)
            if stale == -1:
                status = "从未更新"
            elif stale > 7:
                status = f"⚠️ {stale}天前"
            elif stale > 0:
                status = f"📌 {stale}天前"
            else:
                status = "✅ 本周"
            cat_rows.append([name, str(total), status, f"+{added}" if added > 0 else "-"])
        pdf.add_table(["分类", "知识点", "上次更新", "本周新增"], cat_rows,
                      col_widths=[3*cm, 3*cm, 4*cm, 3*cm])

    # 更新建议
    suggestions = notes_data.get("action_items", [])
    if suggestions:
        pdf.add_section("💡 行动建议")
        for i, item in enumerate(suggestions, 1):
            pdf.add_body(f"{i}. {item}")

    # Images
    if images:
        pdf.add_section("相关资料")
        for img_info in images:
            if isinstance(img_info, str):
                pdf.add_image(img_info)
            elif isinstance(img_info, (list, tuple)):
                pdf.add_image(img_info[0], caption=img_info[1] if len(img_info) > 1 else "")

    pdf.add_divider()
    pdf.add_colored_body("💡 每周日晚提醒：拍照→打开知识库→📷按钮→粘贴文字→保存", C_SECONDARY)
    pdf.add_footer()
    return pdf.build()


# ===== CLI =====
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="每日信息日报 PDF 生成器")
    parser.add_argument("--title", default="每日信息日报", help="PDF标题")
    parser.add_argument("--subtitle", default="", help="副标题")
    parser.add_argument("--content", default="", help="正文内容（支持\\n换行）")
    parser.add_argument("--images", default="", help="图片路径，逗号分隔")
    parser.add_argument("--output", default="daily_report.pdf", help="输出路径")
    parser.add_argument("--type", choices=["exam", "ai", "custom"], default="custom",
                        help="报告类型")
    args = parser.parse_args()

    if args.type == "custom":
        pdf = DailyReportPDF(title=args.title, subtitle=args.subtitle,
                             output_path=args.output)
        pdf.add_title_page()
        if args.content:
            for line in args.content.split("\\n"):
                if line.strip():
                    pdf.add_body(line)
        if args.images:
            for img_path in args.images.split(","):
                img_path = img_path.strip()
                if img_path:
                    pdf.add_image(img_path)
        pdf.add_footer()
        pdf.build()
    else:
        # For exam/ai types, use the helper with JSON or defaults
        print(f"Tip: For {args.type} type, use the build_exam_report/build_ai_report API.")
        print("Example: from gen_daily_report import build_exam_report; build_exam_report({...}, images=['a.jpg'])")
