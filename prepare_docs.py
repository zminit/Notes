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
FILES_TO_COPY = ["index.md", "notestyle.css"]


def fix_image_refs_in_file(filepath: Path, images_dir: Path) -> int:
    """修复单个文件中的 URL 编码图片引用，返回修复数量。"""
    content = filepath.read_text(encoding="utf-8")

    pattern = re.compile(
        r'(?<=src=["\'])(\.\./images/|images/)([^"\')\s]*%[0-9A-F]{2}[^"\')\s]*)'
    )

    def replace_match(match):
        prefix = match.group(1)
        encoded_path = match.group(2)
        decoded_path = urllib.parse.unquote(encoded_path, encoding="utf-8")
        full_path = images_dir / decoded_path
        if full_path.exists():
            return prefix + decoded_path
        return match.group(0)

    new_content, count = pattern.subn(replace_match, content)

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