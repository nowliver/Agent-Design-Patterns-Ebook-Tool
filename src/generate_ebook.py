import json
from pathlib import Path
import re
from datetime import datetime

class EnhancedTypstEbookGenerator:
    """Enhanced Typst e-book generator with professional formatting based on Typst best practices."""
    
    def __init__(self, articles_data):
        self.articles = articles_data
        self.book_title = "智能体设计模式"
        self.book_subtitle = "构建智能系统的实践指南"
        self.author = "知乎专栏"
        self.date = datetime.now().strftime("%Y年%m月")
        
    def escape_typst(self, text):
        """Escape special characters for Typst"""
        if not text:
            return ""
        # Escape backslashes first
        text = text.replace('\\', '\\\\')
        # Escape other special characters
        replacements = {
            '#': '\\#',
            '$': '\\$',
            '_': '\\_',
            '*': '\\*',
            '[': '\\[',
            ']': '\\]',
            '<': '\\<',
            '>': '\\>',
            '@': '\\@',
        }
        for old, new in replacements.items():
            text = text.replace(old, new)
        return text
    
    def format_heading(self, level, text):
        """Format heading for Typst"""
        prefix = '=' * min(level, 6)
        return f"{prefix} {self.escape_typst(text)}\n\n"
    
    def format_paragraph(self, text):
        """Format paragraph for Typst"""
        escaped = self.escape_typst(text)
        return f"{escaped}\n\n"
    
    def format_list(self, items, ordered=False):
        """Format list for Typst with proper indentation"""
        result = []
        for i, item in enumerate(items, 1):
            escaped_item = self.escape_typst(item)
            if ordered:
                result.append(f"+ {escaped_item}")
            else:
                result.append(f"- {escaped_item}")
        return '\n'.join(result) + '\n\n'
    
    def format_code(self, code, lang="python"):
        """Format code block for Typst with syntax highlighting hint"""
        # Clean up the code
        code = code.strip()
        return f"#block(\n  fill: luma(245),\n  inset: 10pt,\n  radius: 4pt,\n  width: 100%,\n)[\n```{lang}\n{code}\n```\n]\n\n"
    
    def format_quote(self, text):
        """Format quote block for Typst with styled box"""
        escaped = self.escape_typst(text)
        return f"""#block(
  fill: rgb("#f0f7ff"),
  inset: (left: 12pt, right: 12pt, top: 10pt, bottom: 10pt),
  radius: 2pt,
  stroke: (left: 3pt + rgb("#3b82f6")),
)[
  #text(style: "italic")[{escaped}]
]

"""
    
    def generate_document_setup(self):
        """Generate document setup and styling rules"""
        return f'''// ============================================================
// 智能体设计模式：构建智能系统的实践指南
// 自动生成的 Typst 电子书
// 生成日期：{self.date}
// ============================================================

// 文档元数据
#set document(
  title: "{self.book_title}：{self.book_subtitle}",
  author: "{self.author}",
  date: auto,
)

// 页面设置
#set page(
  paper: "a4",
  margin: (
    top: 2.5cm,
    bottom: 2.5cm,
    left: 2.5cm,
    right: 2cm,
  ),
  header: context {{
    if counter(page).get().first() > 1 [
      #set text(size: 9pt, fill: luma(100))
      #h(1fr)
      #emph[{self.book_title}]
      #h(1fr)
    ]
  }},
  footer: context {{
    let page-num = counter(page).get().first()
    if page-num > 1 [
      #set text(size: 9pt)
      #h(1fr)
      #page-num
      #h(1fr)
    ]
  }},
)

// 文本设置 - 优先使用系统中文字体
#set text(
  font: ("Source Han Serif SC", "Noto Serif CJK SC", "SimSun", "Microsoft YaHei"),
  size: 11pt,
  lang: "zh",
  region: "cn",
)

// 段落设置
#set par(
  justify: true,
  leading: 0.8em,
  first-line-indent: 2em,
  spacing: 1.2em,
)

// 标题设置
#set heading(numbering: "1.1.1")

// 一级标题样式
#show heading.where(level: 1): it => {{
  set text(size: 20pt, weight: "bold")
  set block(above: 2em, below: 1.5em)
  it
}}

// 二级标题样式
#show heading.where(level: 2): it => {{
  set text(size: 16pt, weight: "bold")
  set block(above: 1.8em, below: 1em)
  it
}}

// 三级标题样式
#show heading.where(level: 3): it => {{
  set text(size: 13pt, weight: "bold")
  set block(above: 1.5em, below: 0.8em)
  it
}}

// 四级及以下标题样式
#show heading.where(level: 4): it => {{
  set text(size: 11pt, weight: "bold")
  set block(above: 1.2em, below: 0.6em)
  it
}}

// 代码块样式
#show raw.where(block: true): it => {{
  set text(font: ("Consolas", "Source Code Pro", "Courier New"), size: 9pt)
  it
}}

// 行内代码样式
#show raw.where(block: false): box.with(
  fill: luma(240),
  inset: (x: 3pt, y: 0pt),
  outset: (y: 3pt),
  radius: 2pt,
)

// 链接样式
#show link: it => {{
  set text(fill: rgb("#2563eb"))
  underline(it)
}}

// 列表样式
#set list(indent: 1.5em, body-indent: 0.5em)
#set enum(indent: 1.5em, body-indent: 0.5em)

'''
    
    def generate_title_page(self):
        """Generate beautiful title page"""
        return f'''
// ============================================================
// 封面页
// ============================================================

#page(
  margin: (top: 0cm, bottom: 0cm, left: 0cm, right: 0cm),
  header: none,
  footer: none,
)[
  #box(
    width: 100%,
    height: 100%,
    fill: gradient.linear(
      rgb("#1e3a5f"),
      rgb("#2d5a87"),
      angle: 135deg,
    ),
  )[
    #align(center + horizon)[
      #block(width: 80%)[
        // 装饰线
        #line(length: 60%, stroke: 2pt + white.transparentize(50%))
        
        #v(2em)
        
        // 主标题
        #text(
          size: 36pt,
          weight: "bold",
          fill: white,
          tracking: 0.1em,
        )[{self.book_title}]
        
        #v(1em)
        
        // 副标题
        #text(
          size: 18pt,
          fill: white.transparentize(20%),
        )[{self.book_subtitle}]
        
        #v(3em)
        
        // 装饰线
        #line(length: 40%, stroke: 1pt + white.transparentize(50%))
        
        #v(4em)
        
        // 来源信息
        #text(
          size: 12pt,
          fill: white.transparentize(40%),
        )[来源：{self.author}]
        
        #v(1em)
        
        // 日期
        #text(
          size: 11pt,
          fill: white.transparentize(50%),
        )[{self.date}]
      ]
    ]
  ]
]

'''
    
    def generate_toc(self):
        """Generate table of contents page"""
        return '''
// ============================================================
// 目录页
// ============================================================

#page(header: none, footer: none)[
  #v(2em)
  
  #align(center)[
    #text(size: 24pt, weight: "bold")[目 录]
  ]
  
  #v(2em)
  
  #outline(
    title: none,
    indent: 2em,
    depth: 3,
  )
]

#pagebreak()

'''
    
    def generate_chapter_header(self, title, chapter_num):
        """Generate a styled chapter header"""
        escaped_title = self.escape_typst(title)
        return f'''
// ============================================================
// 第 {chapter_num} 章
// ============================================================

#pagebreak(weak: true)

= {escaped_title}

'''
    
    def generate_typst(self):
        """Generate complete Typst document with enhanced formatting"""
        parts = []
        
        # Document setup
        parts.append(self.generate_document_setup())
        
        # Title page
        parts.append(self.generate_title_page())
        
        # Table of contents
        parts.append(self.generate_toc())
        
        # Process each article as a chapter
        for idx, article_data in enumerate(self.articles, 1):
            article = article_data['data']
            
            # Chapter header
            parts.append(self.generate_chapter_header(article['title'], idx))
            
            # Process content
            for item in article['content']:
                if item['type'] == 'heading':
                    level = min(item['level'] + 1, 6)
                    parts.append(self.format_heading(level, item['text']))
                elif item['type'] == 'paragraph':
                    parts.append(self.format_paragraph(item['text']))
                elif item['type'] == 'list':
                    parts.append(self.format_list(item['items'], item.get('ordered', False)))
                elif item['type'] == 'code':
                    parts.append(self.format_code(item['text']))
                elif item['type'] == 'quote':
                    parts.append(self.format_quote(item['text']))
        
        # Colophon / end page
        parts.append(self.generate_colophon())
        
        return ''.join(parts)
    
    def generate_colophon(self):
        """Generate colophon (end page with book info)"""
        return f'''
// ============================================================
// 版权页
// ============================================================

#pagebreak()

#align(center + horizon)[
  #block(width: 70%)[
    #line(length: 100%, stroke: 0.5pt + luma(200))
    
    #v(2em)
    
    #text(size: 14pt, weight: "bold")[{self.book_title}]
    
    #text(size: 11pt)[{self.book_subtitle}]
    
    #v(1.5em)
    
    #text(size: 10pt, fill: luma(100))[
      本电子书内容来源于知乎专栏文章，\\
      仅供个人学习参考使用。\\
      \\
      生成日期：{self.date}
    ]
    
    #v(2em)
    
    #line(length: 100%, stroke: 0.5pt + luma(200))
  ]
]
'''
    
    def save_typst(self, output_path):
        """Save Typst document to file"""
        content = self.generate_typst()
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"Typst document saved to {output_path}")


# Keep the old class for backward compatibility
class TypstEbookGenerator(EnhancedTypstEbookGenerator):
    """Alias for backward compatibility"""
    pass

def main():
    # Set up paths for new directory structure
    base_dir = Path(__file__).parent.parent
    output_dir = base_dir / "output"
    
    # Look for articles_data.json in output directory first, then current directory
    data_path = output_dir / "articles_data.json"
    if not data_path.exists():
        data_path = Path(__file__).parent / "articles_data.json"
    
    if not data_path.exists():
        print(f"Error: articles_data.json not found.")
        print(f"Please run 'python src/parse_local_html.py' first.")
        return
    
    with open(data_path, 'r', encoding='utf-8') as f:
        articles = json.load(f)
    
    if not articles:
        print("No articles found in data file")
        return
    
    # Ensure output directory exists
    output_dir.mkdir(exist_ok=True)
    
    # Generate Typst e-book
    generator = EnhancedTypstEbookGenerator(articles)
    output_path = output_dir / "智能体设计模式.typ"
    generator.save_typst(output_path)
    
    print(f"\nE-book generated successfully!")
    print(f"To compile to PDF, run:")
    print(f'  typst compile "{output_path}"')

if __name__ == "__main__":
    main()
