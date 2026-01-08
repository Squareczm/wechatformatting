# 微信公众号简洁排版工具 (wechat-public-account-formatter)

将 Markdown 文章转换为微信公众号可直接粘贴的简洁 HTML 格式。保留原文内容，仅优化排版层次。

![Python Version](https://img.shields.io/badge/python-3.6+-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)

## ✨ 特性

- **保留原文**：不添加任何额外标签，不修改文字内容
- **简洁排版**：清晰的层级，适度的留白
- **重点突出**：仅对真正重要的内容加粗
- **纯净设计**：纯白背景，无彩色渐变，无复杂装饰
- **微信优化**：专为微信公众号编辑器优化的内联 CSS 样式

## 🎨 设计理念

本工具遵循"克制"的设计原则：

1. **纯净背景**：纯白背景，营造清爽的阅读体验
2. **清晰层级**：标题有明确的视觉区分，便于导航
3. **克制强调**：加粗仅用于真正的核心观点，避免过度标记
4. **移动适配**：响应式设计，完美适配手机端阅读

## 📦 安装

将整个文件夹放入 Claude 的 skills 目录：

```bash
.claude/skills/wechatformatting
```



## 📝 Markdown 格式规范

### 支持的语法

| Markdown 语法 | HTML 输出 |
|--------------|-----------|
| `# 一级标题` | 一级标题（居中+底部细线） |
| `## 二级标题` | 二级标题（居中+加粗） |
| `### 三级标题` | 三级标题（左侧竖线） |
| `**粗体**` | 主题色加粗 |
| `> 引用内容` | 引用块（灰色背景+蓝色左边框） |
| `---` | 分割线 |
| `` `code` `` | 行内代码 |
| ```` ```code``` ```` | 代码块 |
| `![alt](url)` | 图片 |
| `[链接文本](url)` | 超链接 |

### 推荐的文章结构

```markdown
# 文章主标题

> 作者简介或引用

---

## 引言

介绍性段落...

---

## 主要章节

### 小节标题 1

内容...

### 小节标题 2

内容...

---

## 总结

总结性段落...

---

> 公众号/作者信息
```

## 🎯 样式规范

### 配色方案

| 用途 | 颜色值 | 说明 |
|------|--------|------|
| 主题色 | `#2563eb` | 蓝色，用于链接、加粗、强调 |
| 正文色 | `#374151` | 深灰色，主体内容颜色 |
| 辅助色 | `#6b7280` | 灰色，用于引用、辅助说明 |
| 分割线 | `#e5e7eb` | 极浅灰色，用于分隔线 |
| 背景色 | `#f9fafb` | 浅灰背景，用于引用块 |
| 标题色 | `#111827` | 近黑色，用于各级标题 |

### 字体设置

- **正文字号**：16px
- **行高**：1.8
- **段间距**：16px
- **默认字体**：-apple-system, BlinkMacSystemFont, "Segoe UI", "PingFang SC", "Hiragino Sans GB", "Microsoft YaHei", sans-serif

### 标题样式

| 层级 | 字号 | 样式 |
|------|------|------|
| 一级 `#` | 24px | 居中，黑体，底部细线 |
| 二级 `##` | 20px | 居中，加粗 |
| 三级 `###` | 17px | 左对齐，左侧蓝色竖线 |

### 重点强调

- **加粗**：`color: #2563eb`（主题蓝色）
- **引用**：左侧细边框 + 浅灰背景

## 📁 项目结构

```
wechatformatting/
├── README.md                    # 项目说明文档
├── SKILL.md                     # Claude Skill 配置
├── scripts/
│   ├── __pycache__/            # Python 缓存文件
│   └── formatter.py            # 主转换脚本
└── references/
    ├── css_styles.md           # CSS 样式规范
    └── optimization_prompt.md  # Markdown 优化指南
```

## 🔧 核心函数

### `format_markdown(markdown_text: str) -> str`
将完整的 Markdown 文本转换为 HTML 文档（包含 `<!DOCTYPE>`）。

### `format_markdown_simple(markdown_text: str) -> str`
仅转换正文部分，返回 HTML 片段。

### `save_html_file(html_content: str, output_path: str) -> None`
将 HTML 内容保存到文件。

## 📊 版本历史

### v3.0 (当前版本)
- ✅ 重新设计：去掉所有类型标记（[DATA]、[INSIGHT] 等）
- ✅ 简化排版：纯净白底，无彩色渐变
- ✅ 克制样式：去阴影、去复杂装饰
- ✅ 保留原文：只优化格式，不添加任何标签

### v2.0
- 卡片式设计
- 渐变背景效果
- 丰富的视觉样式

### v1.0
- 基础 Markdown 转 HTML
- 支持基本标题和段落

## 🤝 贡献

欢迎提交 Issue 和 Pull Request！

## 📄 许可证

MIT License

## 🙏 致谢

- 感谢所有为开源社区贡献的开发者
- 微信公众号编辑器团队的优秀工作
