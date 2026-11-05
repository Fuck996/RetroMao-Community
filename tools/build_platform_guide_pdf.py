"""Render the trilingual platform guide. Optional dependency: reportlab==4.4.9.

Pass --font and --bold-font pointing to redistributable CJK TrueType fonts locally.
Font binaries are embedded in the PDF, never copied to the source repository.
"""

import argparse
import html
from pathlib import Path
import re
from urllib.parse import urljoin

from reportlab.lib import colors
from reportlab.lib.enums import TA_LEFT
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.utils import simpleSplit
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import SimpleDocTemplate, Paragraph, Preformatted, Spacer, PageBreak, KeepTogether, CondPageBreak

ROOT = Path(__file__).resolve().parents[1]
INK, TEAL, MUTED = '#203446', '#087F81', '#607486'


def inline(text):
    text = html.escape(text)
    text = re.sub(r'\[([^\]]+)\]\(([^)]+)\)', lambda match:
        '<link color="'+TEAL+'" href="'+html.escape(urljoin('https://github.com/Fuck996/RetroMao-Community/blob/main/docs/', html.unescape(match[2])), quote=True)+'">'+match[1]+'</link>', text)
    return re.sub(r'`([^`]+)`', r'<font color="'+TEAL+r'">\1</font>', text)


def build(output, font, bold_font):
    pdfmetrics.registerFont(TTFont('Guide', font))
    pdfmetrics.registerFont(TTFont('GuideBold', bold_font))
    normal = ParagraphStyle('body', fontName='Guide', fontSize=10, leading=17, textColor=colors.HexColor(INK), spaceAfter=10, wordWrap='CJK')
    h1 = ParagraphStyle('h1', parent=normal, fontName='GuideBold', fontSize=24, leading=34, textColor=colors.HexColor(TEAL), spaceAfter=18)
    h2 = ParagraphStyle('h2', parent=normal, fontName='GuideBold', fontSize=17, leading=25, spaceBefore=12, spaceAfter=12, keepWithNext=True)
    h3 = ParagraphStyle('h3', parent=normal, fontName='GuideBold', fontSize=12, leading=20, textColor=colors.HexColor(TEAL), spaceBefore=14, spaceAfter=8, keepWithNext=True)
    code_style = ParagraphStyle('code', parent=normal, fontSize=8.5, leading=13, leftIndent=10, rightIndent=8,
        borderPadding=9, backColor=colors.HexColor('#F1F5F7'), spaceAfter=13)
    quote_style = ParagraphStyle('prompt', parent=normal, fontSize=9.3, leading=15.5, leftIndent=12,
        borderColor=colors.HexColor(TEAL), borderWidth=.6, borderPadding=9, backColor=colors.HexColor('#F0F8F7'))
    small = ParagraphStyle('small', parent=normal, fontSize=9, leading=15, textColor=colors.HexColor(MUTED))
    output = Path(output); output.parent.mkdir(parents=True, exist_ok=True)
    document = SimpleDocTemplate(str(output), pagesize=(595.276,841.89), leftMargin=48, rightMargin=48,
        topMargin=54, bottomMargin=50, title='复古猫：通过公共仓库添加完整平台', author='RetroMao',
        subject='Platform format 3: Fork, author, validate, publish and download; AI task templates')
    story = [Spacer(1,55), Paragraph('RetroMao / 复古猫',small), Spacer(1,18),
        Paragraph('通过公共仓库<br/>添加完整平台',h1),
        Paragraph('从 Fork、图标与模型制作，到发布和应用内下载',normal), Spacer(1,22),
        Paragraph('Platform format 3 · Host 1.0.32<br/>2026-11-05',small), Spacer(1,28),
        Paragraph('中文完整教程 / English guide / 日本語ガイド',normal),
        Paragraph('含可直接复制给 AI 的制作任务模板',normal), Spacer(1,24),
        Paragraph(inline('[公共仓库](https://github.com/Fuck996/RetroMao-Community)'), normal),
        Paragraph('适用于包含格式 3 实现的主程序构建。正式发行与真机验收状态请核对公共能力契约。',small), PageBreak()]
    text = (ROOT/'docs/PLATFORM_GUIDE.md').read_text(encoding='utf-8')
    lines, i, started = text.splitlines(), 0, False
    while i < len(lines):
        line = lines[i]
        if line.startswith('## '):
            if started: story.append(PageBreak())
            started=True; story.append(Paragraph(inline(line[3:]),h2)); i+=1; continue
        if not started: i+=1; continue
        if line.startswith('### '):
            if line.startswith('### 11.'): story.append(CondPageBreak(390))
            story.append(Paragraph(inline(line[4:]),h3)); i+=1; continue
        if line.startswith('```'):
            i+=1; code=[]
            while i<len(lines) and not lines[i].startswith('```'):
                value=lines[i]
                # Long PowerShell commands use valid continuation lines, preserving copy/paste.
                if len(value)>105 and ' -' in value:
                    value=' `\n  '.join(re.split(r' (?=-)',value))
                for part in value.splitlines() or ['']:
                    if pdfmetrics.stringWidth(part,'Guide',8.5)>document.width-38:
                        raise ValueError('Code line is too wide; reformat source: '+part)
                    code.append(part)
                i+=1
            story.append(KeepTogether([Preformatted('\n'.join(code),code_style)])); i+=1; continue
        if line.startswith('> '):
            quote=[]
            while i<len(lines) and (lines[i].startswith('> ') or not lines[i].strip()):
                if lines[i].startswith('> '): quote.append(inline(lines[i][2:]))
                i+=1
            story.append(KeepTogether([Paragraph('<br/>'.join(quote),quote_style)])); continue
        if line.strip(): story.append(Paragraph(inline(line),normal))
        i+=1
    def page(canvas, doc):
        canvas.saveState(); canvas.setStrokeColor(colors.HexColor('#DCE6EB')); canvas.line(48,806,547,806)
        canvas.setFont('Guide',8); canvas.setFillColor(colors.HexColor(MUTED))
        canvas.drawString(48,817,'RETROMAO / PLATFORM EXTENSIONS')
        canvas.drawString(48,28,'FORMAT 3  |  2026-11-05'); canvas.drawRightString(547,28,str(doc.page))
        canvas.restoreState()
    document.build(story,onFirstPage=page,onLaterPages=page)
    print(output)


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--font',required=True); parser.add_argument('--bold-font',required=True)
    parser.add_argument('--output',default=ROOT/'docs/PLATFORM_GUIDE.pdf',type=Path)
    args=parser.parse_args(); build(args.output,args.font,args.bold_font)
