# 微信公众号简洁排版样式参考

本文档定义了微信公众号文章的简洁排版样式。

## 设计理念

- **纯净**：纯白背景，无彩色渐变
- **简洁**：去阴影、去复杂装饰
- **克制**：只对真正的重点加粗

## 配色方案

| 用途 | 颜色值 |
|------|--------|
| 主题色 | `#2563eb`（蓝） |
| 正文色 | `#374151`（深灰） |
| 辅助色 | `#6b7280` |
| 分割线 | `#e5e7eb` |

## 字体设置

```css
body {
  font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", "PingFang SC",
               "Hiragino Sans GB", "Microsoft YaHei", sans-serif;
}
```

## 标题样式

### 一级标题

```css
h1 {
  font-size: 24px;
  font-weight: bold;
  color: #111827;
  text-align: center;
  margin: 24px 0 16px;
  padding-bottom: 12px;
  border-bottom: 1px solid #e5e7eb;
}
```

### 二级标题

```css
h2 {
  font-size: 20px;
  font-weight: 600;
  color: #111827;
  text-align: center;
  margin: 28px 0 16px;
}
```

### 三级标题

```css
h3 {
  font-size: 17px;
  font-weight: 600;
  color: #374151;
  margin: 24px 0 12px;
  padding-left: 12px;
  border-left: 3px solid #2563eb;
}
```

## 正文样式

```css
p {
  font-size: 16px;
  line-height: 1.8;
  color: #374151;
  margin: 16px 0;
}
```

## 重点内容

### 加粗文本

```css
strong {
  color: #2563eb;
  font-weight: 600;
}
```

### 引用块

```css
blockquote {
  margin: 16px 0;
  padding: 12px 16px;
  background: #f9fafb;
  border-left: 3px solid #2563eb;
}

blockquote p {
  margin: 0;
  font-size: 15px;
  color: #6b7280;
}
```

## 分割线

```css
hr {
  border: none;
  border-top: 1px solid #e5e7eb;
  margin: 24px 0;
}
```

## 列表样式

```css
ul, ol {
  padding-left: 24px;
}

li {
  margin: 8px 0;
  font-size: 16px;
  line-height: 1.8;
  color: #374151;
}
```

## 链接样式

```css
a {
  color: #2563eb;
  text-decoration: none;
}
```

## 容器设置

```css
body {
  margin: 0;
  padding: 16px;
  background-color: #ffffff;
}
```

## 移动端适配

```css
@media screen and (max-width: 768px) {
  body {
    padding: 12px;
  }
  h1 {
    font-size: 22px;
  }
  h2 {
    font-size: 18px;
  }
  h3 {
    font-size: 16px;
  }
  p {
    font-size: 15px;
  }
}
```

## 注意事项

1. 微信公众号编辑器对 CSS 支持有限，全部使用内联样式
2. 图片使用图床链接，避免本地路径
3. 克制使用加粗，不要过度强调
4. 保持整体视觉的干净和统一
