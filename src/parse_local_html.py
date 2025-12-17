from bs4 import BeautifulSoup
import json
from pathlib import Path
import re

class LocalHTMLParser:
    def __init__(self):
        pass
    
    def parse_article_from_file(self, html_file_path):
        """Parse article content from local HTML file"""
        try:
            with open(html_file_path, 'r', encoding='utf-8') as f:
                html_content = f.read()
            return self.parse_article(html_content, str(html_file_path))
        except Exception as e:
            print(f"Error reading file {html_file_path}: {e}")
            return None
    
    def parse_article(self, html_content, source_name="unknown"):
        """Parse article content from HTML"""
        soup = BeautifulSoup(html_content, 'html.parser')
        
        # Extract title - try multiple selectors
        title = None
        title_selectors = [
            ('h1', {'class': 'Post-Title'}),
            ('h1', {'class': 'ArticleItem-title'}),
            ('title', {}),
            ('h1', {}),
        ]
        
        for tag, attrs in title_selectors:
            title_elem = soup.find(tag, attrs)
            if title_elem:
                title = title_elem.get_text(strip=True)
                # Clean up title
                title = re.sub(r'\s*[-–—]\s*知乎.*$', '', title)
                title = re.sub(r'\(\d+\+.*?\)', '', title)
                if title and len(title) > 5:
                    break
        
        if not title:
            title = "未知标题"
        
        print(f"Parsing: {title}")
        
        # Extract main content - try multiple selectors
        content_elem = None
        content_selectors = [
            ('div', {'class': 'Post-RichTextContainer'}),
            ('div', {'class': 'RichText'}),
            ('div', {'class': 'Post-RichText'}),
            ('article', {}),
            ('div', {'class': 'content'}),
        ]
        
        for tag, attrs in content_selectors:
            content_elem = soup.find(tag, attrs)
            if content_elem:
                break
        
        if not content_elem:
            print(f"Warning: Could not find main content container in {source_name}")
            # Try to find any substantial text content
            content_elem = soup.find('body')
        
        if not content_elem:
            return None
        
        # Extract text content while preserving structure
        content_parts = []
        
        # Process all relevant elements
        for elem in content_elem.find_all(['p', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'ul', 'ol', 'pre', 'blockquote', 'div']):
            # Skip if this element is inside another element we'll process
            if elem.find_parent(['pre', 'code']):
                continue
                
            if elem.name.startswith('h'):
                level = int(elem.name[1])
                text = elem.get_text(strip=True)
                if text and len(text) > 2:
                    content_parts.append({
                        'type': 'heading',
                        'level': level,
                        'text': text
                    })
            elif elem.name == 'p':
                text = elem.get_text(strip=True)
                if text and len(text) > 5:
                    content_parts.append({
                        'type': 'paragraph',
                        'text': text
                    })
            elif elem.name in ['ul', 'ol']:
                items = []
                for li in elem.find_all('li', recursive=False):
                    item_text = li.get_text(strip=True)
                    if item_text:
                        items.append(item_text)
                if items:
                    content_parts.append({
                        'type': 'list',
                        'ordered': elem.name == 'ol',
                        'items': items
                    })
            elif elem.name == 'pre':
                code = elem.get_text()
                if code.strip():
                    content_parts.append({
                        'type': 'code',
                        'text': code
                    })
            elif elem.name == 'blockquote':
                text = elem.get_text(strip=True)
                if text:
                    content_parts.append({
                        'type': 'quote',
                        'text': text
                    })
            elif elem.name == 'div' and 'highlight' in elem.get('class', []):
                code = elem.get_text()
                if code.strip():
                    content_parts.append({
                        'type': 'code',
                        'text': code
                    })
        
        # Find links to other parts
        links = []
        for link in soup.find_all('a', href=True):
            href = link['href']
            if 'zhuanlan.zhihu.com/p/' in href or '/p/' in href:
                link_text = link.get_text(strip=True)
                if any(keyword in link_text for keyword in ['第', '部分', 'Part', '章', '篇']):
                    full_url = href if href.startswith('http') else f"https:{href}" if href.startswith('//') else f"https://zhuanlan.zhihu.com{href}"
                    links.append({
                        'text': link_text,
                        'url': full_url
                    })
        
        return {
            'title': title,
            'content': content_parts,
            'related_links': links
        }
    
    def parse_directory(self, directory_path):
        """Parse all HTML files in a directory"""
        directory = Path(directory_path)
        html_files = list(directory.glob('*.html')) + list(directory.glob('*.htm'))
        
        if not html_files:
            print(f"No HTML files found in {directory_path}")
            return []
        
        articles = []
        for html_file in html_files:
            print(f"\nProcessing: {html_file.name}")
            article = self.parse_article_from_file(html_file)
            if article and article['content']:
                articles.append({
                    'source_file': html_file.name,
                    'data': article
                })
            else:
                print(f"  Skipped (no content found)")
        
        return articles
    
    def save_to_json(self, articles, output_path):
        """Save articles to JSON file"""
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(articles, f, ensure_ascii=False, indent=2)
        print(f"\nSaved {len(articles)} articles to {output_path}")

def main():
    parser = LocalHTMLParser()
    
    # Check for HTML files in html_sources directory
    base_dir = Path(__file__).parent.parent
    html_dir = base_dir / "html_sources"
    output_dir = base_dir / "output"
    
    # Fallback to current directory if html_sources doesn't exist
    if not html_dir.exists():
        html_dir = Path(__file__).parent
    
    articles = parser.parse_directory(html_dir)
    
    if articles:
        # Ensure output directory exists
        output_dir.mkdir(exist_ok=True)
        output_path = output_dir / "articles_data.json"
        parser.save_to_json(articles, output_path)
        print(f"\nSuccessfully parsed {len(articles)} article(s):")
        for i, article in enumerate(articles, 1):
            print(f"  {i}. {article['data']['title']} (from {article['source_file']})")
        print(f"\nNext step: Run 'python src/generate_ebook.py' to create the e-book")
    else:
        print("\n" + "="*60)
        print("No HTML files found!")
        print("="*60)
        print("\nPlease save the Zhihu articles as HTML files:")
        print("1. Open https://zhuanlan.zhihu.com/p/1960475996017923529 in your browser")
        print("2. Press Ctrl+S (or Cmd+S on Mac) to save the page")
        print("3. Save as 'Complete HTML' or 'Web Page, Complete'")
        print("4. Save all related article parts the same way")
        print(f"5. Place all HTML files in: {html_dir}")
        print("6. Run this script again")

if __name__ == "__main__":
    main()
