"""在 MkDocs 构建前修复 Markdown 中的 URL 编码图片引用。

部分 Markdown 文件中图片引用使用了 URL 编码（如 %E6%B7%B1%E5%BA%A6），
但磁盘上的实际文件名是中文。此脚本将 URL 编码的引用还原为实际文件名。
"""
import os
import re
import urllib.parse
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent


def fix_image_refs_in_file(filepath: Path) -> bool:
    """修复单个文件中的 URL 编码图片引用，返回是否有修改。"""
    content = filepath.read_text(encoding="utf-8")

    # 匹配 ../images/ 或 images/ 开头且包含 URL 编码字符的图片路径
    pattern = re.compile(
        r'(?<=src=["\'])(\.\./images/|images/)([^"\')\s]*%[0-9A-F]{2}[^"\')\s]*)'
    )

    def replace_match(match):
        prefix = match.group(1)
        encoded_path = match.group(2)
        # 尝试 URL 解码
        decoded_path = urllib.parse.unquote(encoded_path, encoding="utf-8")
        # 只在实际文件存在时才替换
        full_path = ROOT_DIR / "images" / decoded_path
        if full_path.exists():
            return prefix + decoded_path
        return match.group(0)  # 文件不存在则保持原样

    new_content, count = pattern.subn(replace_match, content)

    if count > 0:
        filepath.write_text(new_content, encoding="utf-8")
        print(f"  [FIXED] {filepath.relative_to(ROOT_DIR)}: {count} 处引用")
        return True
    return False


def main():
    """扫描所有 Markdown 文件并修复 URL 编码的图片引用。"""
    print("正在扫描 Markdown 文件中的 URL 编码图片引用...\n")
    total_fixed = 0

    for md_file in ROOT_DIR.rglob("*.md"):
        if fix_image_refs_in_file(md_file):
            total_fixed += 1

    print(f"\n修复完成，共修改 {total_fixed} 个文件。")


if __name__ == "__main__":
    main()