"""构建前准备脚本：将笔记文件复制到 docs/ 目录，并修复 URL 编码的图片引用。

源文件保持原位置不动，docs/ 仅用于 MkDocs 构建，已加入 .gitignore。
"""
import os
import re
import shutil
import urllib.parse
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent
DOCS_DIR = ROOT_DIR / "docs"

# 需要复制到 docs/ 的笔记目录
NOTE_DIRS = [
    "Effective C++",
    "Games101课程笔记",
    "Games104课程笔记",
    "Games202课程笔记",
    "OpenGL学习笔记",
    "《Unity Shader入门精要》笔记",
    "人工智能学习笔记",
    "神经渲染",
    "论文阅读笔记",
]

# 需要复制到 docs/ 的单独文件
FILES_TO_COPY = ["index.md", "notestyle.css", "mathjax-config.js"]


def fix_image_refs_in_file(filepath: Path, images_dir: Path) -> int:
    """修复单个文件中的 URL 编码图片引用，返回修复数量。"""
    content = filepath.read_text(encoding="utf-8")
    count = 0

    def replace_match(m):
        nonlocal count
        if m.group(1) is not None:
            # 带引号：src="..." 或 src='...'
            quote = m.group(1)
            url = m.group(2)
        else:
            # 不带引号：src=...（以空格或 > 结束）
            quote = ""
            url = m.group(3)

        if "%" not in url:
            return m.group(0)

        if url.startswith("../images/"):
            prefix = "../images/"
            filename = urllib.parse.unquote(url, encoding="utf-8")[len("../images/"):]
        elif url.startswith("images/"):
            prefix = "images/"
            filename = urllib.parse.unquote(url, encoding="utf-8")[len("images/"):]
        else:
            return m.group(0)

        if (images_dir / filename).exists():
            count += 1
            return f"src={quote}{prefix}{filename}{quote}"
        return m.group(0)

    # 一个正则同时匹配带引号和不带引号的 src 值
    # group(1)+group(2): 带引号  |  group(3): 不带引号
    pattern = re.compile(
        r'src=(?:(["\'])((?:\.\./images/|images/)[^"\']*?)\1'
        r'|'
        r'((?:\.\./images/|images/)[^\s>]+))'
    )

    new_content = pattern.sub(replace_match, content)

    if count > 0:
        filepath.write_text(new_content, encoding="utf-8")
        print(f"  [FIXED] {filepath.relative_to(DOCS_DIR)}: {count} 处引用")

    return count


def fix_image_refs(docs_dir: Path):
    """扫描 docs/ 下所有 Markdown 文件并修复 URL 编码的图片引用。"""
    images_dir = docs_dir / "images"
    print("\n正在修复 URL 编码的图片引用...")
    total_fixed = 0

    for md_file in docs_dir.rglob("*.md"):
        total_fixed += fix_image_refs_in_file(md_file, images_dir)

    print(f"修复完成，共修改 {total_fixed} 处引用。\n")


def main():
    # 清理并重建 docs 目录
    if DOCS_DIR.exists():
        shutil.rmtree(DOCS_DIR)
    DOCS_DIR.mkdir()

    # 复制笔记目录
    for d in NOTE_DIRS:
        src = ROOT_DIR / d
        if src.exists():
            shutil.copytree(src, DOCS_DIR / d)
            print(f"[COPY] {d}/")

    # 复制单独文件
    for f in FILES_TO_COPY:
        src = ROOT_DIR / f
        if src.exists():
            shutil.copy2(src, DOCS_DIR / f)
            print(f"[COPY] {f}")

    # 复制 images 目录
    images_src = ROOT_DIR / "images"
    if images_src.exists():
        shutil.copytree(images_src, DOCS_DIR / "images")
        print(f"[COPY] images/ ({len(list(images_src.iterdir()))} 个文件)")

    # 修复 URL 编码的图片引用
    fix_image_refs(DOCS_DIR)

    print("docs/ 目录准备完成！")


if __name__ == "__main__":
    main()