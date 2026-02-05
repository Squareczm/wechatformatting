#!/usr/bin/env python3
"""
微信公众号简洁排版工具
将 Markdown 转换为微信公众号优化的 HTML 格式

设计理念：
- 保留原文：不添加任何标签
- 简洁排版：清晰的层级，干净的段落
- 克制强调：只对真正重要的内容加粗
"""

import re
import sys
import os
from pathlib import Path
from typing import Tuple

# 强制设置 UTF-8 编码输出
if sys.platform == 'win32':
    os.environ['PYTHONIOENCODING'] = 'utf-8'

# ============================================================================
# 配色方案
# ============================================================================

THEME_COLOR = "#2563eb"  # 主题色
TEXT_COLOR = "#374151"   # 正文色
TEXT_LIGHT = "#6b7280"   # 辅助色
BORDER_COLOR = "#e5e7eb" # 分割线/边框
BG_QUOTE = "#f9fafb"     # 引用背景

# ============================================================================
# 工具函数
# ============================================================================

def escape_html(text: str) -> str:
    """转义 HTML 特殊字符（仅转义 & < >，保留引号以兼容微信编辑器）"""
    replacements = [
        ("&", "&amp;"),
        ("<", "&lt;"),
        (">", "&gt;"),
        # 注意：微信编辑器对 HTML 属性值的引号处理较好
        # 只转义会导致内容中的引号被错误显示为 &quot;
        # 所以这里不转义引号
    ]
    for old, new in replacements:
        text = text.replace(old, new)
    return text


def parse_frontmatter(lines: list) -> Tuple[list, str]:
    """解析 Markdown 文档，分离 frontmatter 和正文内容"""
    if len(lines) < 3 or lines[0] != "---":
        return [], "\n".join(lines)
    
    for i in range(1, len(lines)):
        if lines[i] == "---":
            frontmatter = lines[1:i]
            content = "\n".join(lines[i+1:])
            return frontmatter, content
    
    return [], "\n".join(lines)


def is_special_title(line: str) -> bool:
    """检测是否是特殊格式的标题"""
    stripped = line.strip()
    
    if ' - ' not in stripped and ' – ' not in stripped and ' — ' not in stripped:
        return False
    
    if '●' in stripped:
        return False
    
    patterns = [
        r'^[\d\.]+\s*[-–—]',
        r'^[\d\.]+[亿万千百万亿]\s*[-–—]',
        r'^[\d\.]+[亿万千百万亿][^\s]*\s*[-–—]',
    ]
    
    for pattern in patterns:
        if re.match(pattern, stripped):
            return True
    
    return False


# ============================================================================
# HTML 生成函数
# ============================================================================

def generate_h1(title: str) -> str:
    """一级标题：居中，黑体，底部细线"""
    return f'''<h1 style="margin: 24px 0 16px; font-size: 24px; font-weight: bold; color: #111827; text-align: center; padding-bottom: 12px; border-bottom: 1px solid {BORDER_COLOR};">{escape_html(title)}</h1>'''


def generate_h2(title: str) -> str:
    """二级标题：居中，加粗"""
    return f'''<h2 style="margin: 28px 0 16px; font-size: 20px; font-weight: 600; color: #111827; text-align: center;">{escape_html(title)}</h2>'''


def generate_h3(title: str) -> str:
    """三级标题：左对齐，左侧竖线"""
    return f'''<h3 style="margin: 24px 0 12px; font-size: 17px; font-weight: 600; color: #374151; padding-left: 12px; border-left: 3px solid {THEME_COLOR};">{escape_html(title)}</h3>'''


def generate_special_title(title: str) -> str:
    """特殊格式标题"""
    return f'''<h2 style="margin: 28px 0 16px; font-size: 20px; font-weight: 600; color: #111827; text-align: center;">{escape_html(title)}</h2>'''


def generate_blockquote(content: str) -> str:
    """引用块 - 支持多个段落"""
    # 如果内容包含段落分隔符，分割成多个段落
    if "__PARAGRAPH_BREAK__" in content:
        paragraphs = content.split("__PARAGRAPH_BREAK__")
        paragraph_html = []
        for para in paragraphs:
            if para.strip():
                paragraph_html.append(f'<p style="margin: 8px 0; font-size: 15px; line-height: 1.8; color: {TEXT_LIGHT};">{para.strip()}</p>')
        paragraphs_content = "".join(paragraph_html)
        return f'''<blockquote style="margin: 16px 0; padding: 12px 16px; background: {BG_QUOTE}; border-left: 3px solid {THEME_COLOR};">
    {paragraphs_content}
</blockquote>'''
    else:
        return f'''<blockquote style="margin: 16px 0; padding: 12px 16px; background: {BG_QUOTE}; border-left: 3px solid {THEME_COLOR};">
    <p style="margin: 0; font-size: 15px; line-height: 1.8; color: {TEXT_LIGHT};">{content}</p>
</blockquote>'''


def generate_divider() -> str:
    """分割线"""
    return f'<hr style="border: none; border-top: 1px solid {BORDER_COLOR}; margin: 24px 0;">'


def generate_paragraph(content: str) -> str:
    """普通段落"""
    return f'<p style="margin: 16px 0; font-size: 16px; line-height: 1.8; color: {TEXT_COLOR};">{content}</p>'


def generate_list_item(content: str) -> str:
    """列表项"""
    return f'<p style="margin: 8px 0; padding-left: 24px; text-indent: -24px; font-size: 16px; line-height: 1.8; color: {TEXT_COLOR};">{content}</p>'


def generate_code_block(content: str) -> str:
    """代码块"""
    # 微信编辑器里深色代码块不太利于阅读，这里用浅底+细边框
    return (
        f'<pre style="margin: 16px 0; padding: 14px 16px; background: {BG_QUOTE}; '
        f'border: 1px solid {BORDER_COLOR}; border-radius: 6px; overflow-x: auto; '
        f'white-space: pre-wrap; word-break: break-word; '
        f'font-family: \\"SF Mono\\", \\"Fira Code\\", monospace; font-size: 13px; '
        f'line-height: 1.7; color: #111827;">{content}</pre>'
    )


def generate_image(alt_text: str, img_url: str) -> str:
    """图片 - 使用单引号避免与内容中的双引号冲突"""
    return f"<figure style='margin: 20px 0; text-align: center;'><img src='{escape_html(img_url)}' alt='{escape_html(alt_text)}' style='max-width: 100%; height: auto; border-radius: 6px;'></figure>"


def generate_link(text: str, url: str) -> str:
    """链接"""
    # text 允许包含格式化后的 HTML（strong/code），因此这里不再 escape text，只 escape url
    return (
        f"<p style='margin: 8px 0; font-size: 16px; line-height: 1.8; color: {TEXT_COLOR};'>"
        f"<a href='{escape_html(url)}' style='color: {THEME_COLOR}; text-decoration: none;'>"
        f"{text}"
        f"</a></p>"
    )


def format_strong_escaped(text: str) -> str:
    """处理加粗文本（输入必须已经 escape_html）"""
    result = text
    result = re.sub(
        r'\*\*([^*]+)\*\*',
        r'<strong style="color: {0}; font-weight: 600;">\1</strong>'.format(THEME_COLOR),
        result,
    )
    result = re.sub(
        r'__([^_]+)__',
        r'<strong style="color: {0}; font-weight: 600;">\1</strong>'.format(THEME_COLOR),
        result,
    )
    return result


def format_inline_code_escaped(text: str) -> str:
    """处理行内代码（输入必须已经 escape_html）"""
    # 关键点：不要在这里再 escape，否则会把 <code> 再次转义成 &lt;code&gt;
    return re.sub(
        r'`([^`]+)`',
        r'<code style="background: {0}; padding: 2px 6px; border-radius: 4px; '
        r'font-family: "SF Mono", "Fira Code", monospace; font-size: 13px; '
        r'color: #1f293b;">\1</code>'.format(BG_QUOTE),
        text,
    )


def format_text(text: str) -> str:
    """统一的行内格式化：先转义，再处理 code，再处理加粗"""
    escaped = escape_html(text)
    escaped = format_inline_code_escaped(escaped)
    escaped = format_strong_escaped(escaped)
    return escaped


# ============================================================================
# 主处理函数
# ============================================================================

def process_markdown(content: str) -> str:
    """处理 Markdown 内容"""
    lines = content.strip().split("\n")
    html_lines = []
    
    i = 0
    while i < len(lines):
        line = lines[i].rstrip()
        
        if not line:
            i += 1
            continue
        
        # 检测标题层级
        if line.startswith("### "):
            html_lines.append(generate_h3(line[4:]))
        elif line.startswith("## "):
            html_lines.append(generate_h2(line[3:]))
        elif line.startswith("# "):
            html_lines.append(generate_h1(line[2:]))
        
        # 检测特殊格式标题
        elif is_special_title(line):
            html_lines.append(generate_special_title(line.strip()))
        
        # 检测引用块
        elif line.startswith(">"):
            blockquote_lines = []
            # 收集所有引用块行（包括空行）
            while i < len(lines):
                current_line = lines[i].rstrip()
                if current_line.startswith(">"):
                    # 提取内容（去掉 > 或 > 后的空格）
                    if current_line.startswith("> "):
                        blockquote_lines.append(current_line[2:])
                    elif current_line == ">":
                        blockquote_lines.append("")  # 空行，保留用于段落分隔
                    else:
                        # 以 > 开头但后面没有空格的情况
                        blockquote_lines.append(current_line[1:])
                    i += 1
                elif not current_line:
                    # 遇到空行，结束引用块
                    break
                else:
                    # 遇到非引用块内容，结束引用块
                    break
            
            # 合并内容：过滤掉连续的空行，保留单个空行作为段落分隔
            content_parts = []
            prev_empty = False
            for part in blockquote_lines:
                if part.strip():
                    content_parts.append(part)
                    prev_empty = False
                elif not prev_empty:
                    # 只保留第一个空行作为段落分隔
                    content_parts.append("")
                    prev_empty = True
            
            # 过滤掉末尾的空行
            while content_parts and not content_parts[-1].strip():
                content_parts.pop()
            
            if content_parts:
                # 处理每个段落：先格式化加粗和代码，然后用特殊标记分隔
                formatted_parts = []
                for part in content_parts:
                    if part.strip():
                        formatted_parts.append(format_text(part))
                    else:
                        formatted_parts.append("__PARAGRAPH_BREAK__")
                
                # 用段落分隔符连接
                content = "__PARAGRAPH_BREAK__".join(formatted_parts)
                html_lines.append(generate_blockquote(content))
            continue
        
        # 检测分割线
        elif line.strip() in ["---", "***", "___"]:
            html_lines.append(generate_divider())
        
        # 检测列表
        elif line.startswith("- ") or line.startswith("* "):
            html_lines.append(generate_list_item(format_text(line)))
        elif re.match(r"^\d+\.\s", line):
            html_lines.append(generate_list_item(format_text(line)))
        
        # 检测代码块
        elif line.startswith("```"):
            code_lines = []
            i += 1
            while i < len(lines) and not lines[i].startswith("```"):
                code_lines.append(escape_html(lines[i]))
                i += 1
            code_content = "<br>".join(code_lines)
            html_lines.append(generate_code_block(code_content))
            # 跳过结束的 ``` 行，避免把结束标记当作下一个代码块开头
            if i < len(lines) and lines[i].startswith("```"):
                i += 1
            continue
        
        # 检测图片
        elif line.startswith("!["):
            img_match = re.match(r'!\[([^\]]*)\]\(([^)]+)\)', line)
            if img_match:
                alt_text = img_match.group(1)
                img_url = img_match.group(2)
                html_lines.append(generate_image(alt_text, img_url))
            else:
                html_lines.append(generate_paragraph(format_text(line)))
        
        # 检测链接
        elif line.startswith("[") and "](" in line:
            link_match = re.match(r'\[([^\]]+)\]\(([^)]+)\)', line)
            if link_match:
                link_text = link_match.group(1)
                link_url = link_match.group(2)
                html_lines.append(generate_link(format_text(link_text), link_url))
            else:
                html_lines.append(generate_paragraph(format_text(line)))
        
        # 普通段落
        else:
            formatted_content = format_text(line)
            html_lines.append(generate_paragraph(formatted_content))
        
        i += 1
    
    return "\n".join(html_lines)


def generate_html(body: str, title: str = "") -> str:
    """生成完整的 HTML 文档"""
    html = f'''<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    <title>{escape_html(title) if title else '微信公众号文章'}</title>
</head>
<body style="margin: 0; padding: 16px; background-color: #ffffff;">
    <div style="max-width: 100%; margin: 0 auto;">
        {body}
    </div>
</body>
</html>'''
    return html


def format_markdown(markdown_text: str) -> str:
    """主函数：将 Markdown 转换为微信公众号优化的 HTML"""
    lines = markdown_text.split("\n")
    frontmatter, content = parse_frontmatter(lines)
    
    title = ""
    if frontmatter:
        for line in frontmatter:
            if line.startswith("title:"):
                title = line[6:].strip().strip('"').strip("'")
    
    body_html = process_markdown(content)
    full_html = generate_html(body_html, title)
    
    return full_html


def format_markdown_simple(markdown_text: str) -> str:
    """简化版：只返回正文部分"""
    lines = markdown_text.split("\n")
    _, content = parse_frontmatter(lines)
    return process_markdown(content)


def save_html_file(html_content: str, output_path: str) -> None:
    """保存 HTML 文件"""
    dir_path = os.path.dirname(output_path)
    if dir_path:
        os.makedirs(dir_path, exist_ok=True)
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(html_content)


def get_html_output_path(input_path: str) -> str:
    """生成 HTML 输出文件路径"""
    path = Path(input_path)
    return str(path.parent / f"{path.stem}.html")


if __name__ == "__main__":
    save_html = False
    input_path = None

    for arg in sys.argv[1:]:
        if arg == "--save-html":
            save_html = True
        elif arg.startswith("-"):
            continue
        else:
            input_path = arg

    if not input_path:
        markdown_input = sys.stdin.read()
        output_html_path = None
    else:
        output_html_path = get_html_output_path(input_path)
        if not os.path.exists(input_path):
            print(f"错误：文件不存在 - {input_path}", file=sys.stderr)
            sys.exit(1)
        with open(input_path, "r", encoding="utf-8") as f:
            markdown_input = f.read()

    result = format_markdown(markdown_input)

    if save_html and output_html_path:
        save_html_file(result, output_html_path)
        print(f"已保存 HTML 文件: {output_html_path}", file=sys.stderr)

    if sys.platform == 'win32':
        import io
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

    print(result)
