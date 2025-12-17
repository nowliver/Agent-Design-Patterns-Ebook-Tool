# 智能体设计模式 - 电子书生成工具

将知乎专栏《智能体设计模式：构建智能系统的实践指南》系列文章整合成精美的 Typst 电子书。

## ✨ 功能特点

- 📖 解析本地保存的 HTML 文件，提取结构化内容
- 🎨 生成专业排版的 Typst 电子书，包含：
  - 精美渐变封面
  - 自动生成目录
  - 分级标题样式
  - 代码块语法高亮
  - 引用块美化
  - 页眉页脚
  - 版权页
- 🇨🇳 优化的中文排版（首行缩进、两端对齐）

## 📁 项目结构

```
智能体设计模式/
├── build.py              # 一键构建脚本
├── README.md             # 项目说明
├── src/                  # 源代码
│   ├── parse_local_html.py   # HTML 解析器
│   ├── generate_ebook.py     # Typst 生成器
│   └── requirements.txt      # Python 依赖
├── html_sources/         # HTML 源文件（已保存）
│   └── *.html
└── output/               # 输出文件
    ├── articles_data.json    # 解析后的数据
    └── 智能体设计模式.typ    # 生成的电子书
```

## 🚀 快速开始

### 方法一：一键构建（推荐）

```bash
python build.py
```

### 方法二：分步执行

#### 1. 安装依赖

```bash
pip install beautifulsoup4 lxml
```

#### 2. 解析 HTML 文件

```bash
python src/parse_local_html.py
```

#### 3. 生成电子书

```bash
python src/generate_ebook.py
```

#### 4. 编译为 PDF（可选）

```bash
typst compile output/智能体设计模式.typ
```

## 📥 如何获取 HTML 源文件

如果 `html_sources/` 目录为空，需要手动保存网页：

1. 在浏览器中打开：https://zhuanlan.zhihu.com/p/1960475996017923529
2. 按 `Ctrl+S` 保存网页
3. 选择"网页，全部"格式
4. 保存到 `html_sources/` 目录
5. 对文章中提到的其他部分重复以上步骤

## 🛠️ 依赖说明

### Python 依赖
- `beautifulsoup4` - HTML 解析
- `lxml` - XML/HTML 解析器

### 可选工具
- **Typst** - 编译 .typ 文件为 PDF
  - Windows: `winget install Typst.Typst`
  - Mac: `brew install typst`
  - 或从 https://github.com/typst/typst/releases 下载

## 📝 生成的电子书特性

| 特性 | 说明 |
|------|------|
| 封面 | 渐变背景 + 装饰线 |
| 目录 | 自动生成，支持 3 级标题 |
| 标题 | 分级样式，自动编号 |
| 代码块 | 灰色背景，圆角边框 |
| 引用 | 蓝色左边框，斜体文字 |
| 页眉 | 显示书名 |
| 页脚 | 居中页码 |
| 版权页 | 来源说明 |

## ❓ 常见问题

**Q: 编译 PDF 时字体报错？**  
A: 确保系统安装了中文字体（如思源宋体、微软雅黑）

**Q: 生成的内容格式有问题？**  
A: 可以直接编辑 `output/智能体设计模式.typ` 文件进行调整

## 📚 源文章

- [全文](https://zhuanlan.zhihu.com/p/1960475996017923529)
- 第一部分、第二三部分、第四部分（见文章内链接）
