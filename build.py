#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
智能体设计模式电子书 - 一键构建脚本
运行此脚本自动解析HTML文件并生成Typst电子书
"""

import subprocess
import sys
from pathlib import Path

def main():
    base_dir = Path(__file__).parent
    src_dir = base_dir / "src"
    output_dir = base_dir / "output"
    html_dir = base_dir / "html_sources"
    
    # Ensure output directory exists
    output_dir.mkdir(exist_ok=True)
    
    print("=" * 60)
    print("智能体设计模式 - 电子书构建工具")
    print("=" * 60)
    
    # Step 1: Parse HTML files
    print("\n[1/2] 解析 HTML 文件...")
    parse_script = src_dir / "parse_local_html.py"
    
    # Temporarily change the script to use correct paths
    result = subprocess.run(
        [sys.executable, str(parse_script)],
        cwd=str(html_dir),
        capture_output=True,
        text=True,
        encoding='mbcs',
        errors='replace'
    )
    
    if result.returncode != 0:
        print(f"解析失败: {result.stderr}")
        # Try running from base directory
        result = subprocess.run(
            [sys.executable, str(parse_script)],
            cwd=str(base_dir),
            capture_output=True,
            text=True,
            encoding='mbcs',
            errors='replace'
        )
    
    print(result.stdout)
    
    # Move articles_data.json to output if it was created in html_sources
    json_in_html = html_dir / "articles_data.json"
    json_in_output = output_dir / "articles_data.json"
    if json_in_html.exists():
        import shutil
        shutil.move(str(json_in_html), str(json_in_output))
    
    # Step 2: Generate e-book
    print("\n[2/2] 生成 Typst 电子书...")
    generate_script = src_dir / "generate_ebook.py"
    
    result = subprocess.run(
        [sys.executable, str(generate_script)],
        cwd=str(base_dir),
        capture_output=True,
        text=True,
        encoding='mbcs',
        errors='replace'
    )
    print(result.stdout)
    if result.stderr:
        print(result.stderr)
    
    # Move generated typ file to output
    typ_file = base_dir / "智能体设计模式.typ"
    if typ_file.exists():
        import shutil
        shutil.move(str(typ_file), str(output_dir / "智能体设计模式.typ"))
    
    print("\n" + "=" * 60)
    print("✓ 构建完成！")
    print("=" * 60)
    print(f"\n输出文件位于: {output_dir}")
    print("\n要编译为 PDF，请运行:")
    print(f'  typst compile "{output_dir / "智能体设计模式.typ"}"')

if __name__ == "__main__":
    main()
