"""构建前准备脚本。

源文件保持原位置不动，docs/ 仅用于 MkDocs 构建，已加入 .gitignore。
除了复制文件，这里还会对构建副本做两项兼容处理：

* 修正原生 ``<img>`` 标签相对于 MkDocs 输出页面的图片路径；
* 修正列表中使用两个空格缩进的 ``$$...$$`` 块公式。

这样可以继续用现有的笔记习惯写 Markdown，不需要每次手工改源文件。
"""
import os
import re
import shutil
import urllib.parse
from pathlib import Path
from typing import List, Optional, Tuple


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


IMG_TAG_PATTERN = re.compile(r"<img\b[^>]*>", re.IGNORECASE)
SRC_ATTR_PATTERN = re.compile(
    r"(?P<prefix>\bsrc\s*=\s*)"
    r"(?:(?P<quote>['\"])(?P<quoted>[^'\"]*)(?P=quote)|(?P<bare>[^\s>]+))",
    re.IGNORECASE,
)


def output_page_dir(filepath: Path, docs_dir: Path) -> Path:
    """返回 MkDocs ``use_directory_urls: true`` 时页面所在的目录。

    例如 ``docs/人工智能学习笔记/深度学习基础.md`` 会生成到
    ``人工智能学习笔记/深度学习基础/index.html``，因此页面目录比源
    Markdown 文件多一层。
    """
    relative = filepath.relative_to(docs_dir)
    if relative.parent == Path(".") and relative.name.lower() == "index.md":
        return docs_dir
    return docs_dir / relative.parent / relative.stem


def normalize_image_url(
    url: str, filepath: Path, docs_dir: Path, images_dir: Path
) -> Optional[str]:
    """把源文件中的 images URL 转成最终 HTML 可用的相对 URL。"""
    parsed = urllib.parse.urlsplit(url)
    path = parsed.path

    if path.startswith("../images/"):
        filename = path[len("../images/") :]
    elif path.startswith("images/"):
        filename = path[len("images/") :]
    else:
        return None

    # 先还原 URL 编码，再按磁盘上的真实中文文件名检查。
    filename = urllib.parse.unquote(filename, encoding="utf-8")
    filename_path = Path(filename)
    if ".." in filename_path.parts:
        return None

    source_image = images_dir / filename_path
    if not source_image.exists():
        return None

    page_dir = output_page_dir(filepath, docs_dir)
    output_url = os.path.relpath(source_image, page_dir).replace(os.sep, "/")
    if parsed.query:
        output_url += f"?{parsed.query}"
    if parsed.fragment:
        output_url += f"#{parsed.fragment}"
    return output_url


def fix_image_refs_in_file(
    filepath: Path, docs_dir: Path, images_dir: Path
) -> Tuple[int, List[str]]:
    """修正单个文件的原生图片引用，返回修改数和未找到的引用。"""
    content = filepath.read_text(encoding="utf-8")
    count = 0
    missing: List[str] = []

    def replace_src(match: re.Match) -> str:
        nonlocal count
        url = match.group("quoted") or match.group("bare")
        normalized = normalize_image_url(url, filepath, docs_dir, images_dir)
        if normalized is None:
            if url.startswith(("../images/", "images/")):
                missing.append(url)
            return match.group(0)

        count += 1
        # 统一加引号，避免中文、空格或 query 让 HTML 属性被错误拆分。
        return f'{match.group("prefix")}"{normalized}"'

    def replace_img_tag(match: re.Match) -> str:
        return SRC_ATTR_PATTERN.sub(replace_src, match.group(0))

    new_content = IMG_TAG_PATTERN.sub(replace_img_tag, content)

    if count > 0:
        filepath.write_text(new_content, encoding="utf-8")
        print(f"  [FIXED] {filepath.relative_to(docs_dir)}: 图片引用 {count} 处")

    return count, missing


def fix_image_refs(docs_dir: Path):
    """扫描 docs/ 下所有 Markdown 文件并修正图片引用。"""
    images_dir = docs_dir / "images"
    print("\n正在修正图片引用...")
    total_fixed = 0
    missing: List[Tuple[Path, str]] = []

    for md_file in docs_dir.rglob("*.md"):
        fixed, unresolved = fix_image_refs_in_file(md_file, docs_dir, images_dir)
        total_fixed += fixed
        missing.extend((md_file, url) for url in unresolved)

    print(f"图片引用处理完成，共修改 {total_fixed} 处。")
    if missing:
        print(f"警告：有 {len(missing)} 个图片引用未找到对应文件：")
        for filepath, url in missing[:20]:
            print(f"  - {filepath.relative_to(docs_dir)}: {url}")
        if len(missing) > 20:
            print(f"  ... 其余 {len(missing) - 20} 个未显示")


def fix_indented_display_math_in_file(filepath: Path) -> int:
    """规范独占一行的 ``$$...$$`` 块公式，返回修正的公式块数量。

    Python-Markdown 对列表续行的解析比很多本地编辑器严格。把公式规范成
    分隔符独占一行后，pymdownx.arithmatex 才能稳定识别。列表中的公式使用
    四空格缩进，顶层公式保持顶层。不会触碰代码围栏或普通行内公式。
    """
    content = filepath.read_text(encoding="utf-8")
    had_final_newline = content.endswith("\n")
    lines = content.splitlines()
    output: List[str] = []
    in_fence = False
    fixed = 0
    i = 0

    while i < len(lines):
        line = lines[i]
        stripped = line.lstrip()
        if stripped.startswith(("```", "~~~")):
            in_fence = not in_fence
            output.append(line)
            i += 1
            continue

        opening = re.match(r"^(?P<indent> *)\$\$(?P<body>.*)$", line)
        if in_fence or opening is None:
            output.append(line)
            i += 1
            continue

        indent = opening.group("indent")
        # 只有顶层公式或列表续行公式需要处理；四空格以上已经是合法的
        # 列表块缩进，仍然规范其分隔符，但保留原有层级。
        if indent and len(indent) == 1:
            output.append(line)
            i += 1
            continue
        block_indent = "" if not indent else ("    " if len(indent) < 4 else indent)

        # 找到当前公式的结束分隔符；支持 $$ 既出现在单行，也出现在末行。
        body_first = opening.group("body")
        close_pos = body_first.find("$$")
        close_line_index = i if close_pos >= 0 else None
        if close_line_index is None:
            j = i + 1
            while j < len(lines):
                if "$$" in lines[j]:
                    close_line_index = j
                    break
                j += 1
            if close_line_index is None:
                output.append(line)
                i += 1
                continue

        # 空的 $$...$$ 没有可渲染内容，删除构建副本中的空块，避免它们
        # 被 Markdown 当成普通文本输出为原始 $$。
        empty_block = (
            not body_first.strip()
            and (
                close_line_index == i
                or (
                    all(
                        not lines[k].strip()
                        for k in range(i + 1, close_line_index)
                    )
                    and lines[close_line_index].strip() == "$$"
                )
            )
        )
        if empty_block:
            if output and output[-1].strip():
                output.append("")
            fixed += 1
            i = close_line_index + 1
            continue

        # 与列表项分离，保证公式是一个独立块；空行不会改变原始笔记内容。
        if output and output[-1].strip():
            output.append("")
        output.append(f"{block_indent}$$")

        if close_line_index == i:
            body = body_first[:close_pos].strip()
            if body:
                output.append(f"{block_indent}{body}")
        else:
            if body_first.strip():
                output.append(f"{block_indent}{body_first.strip()}")
            for body_line in lines[i + 1 : close_line_index]:
                # LaTeX 块内的空行会让 Python-Markdown 提前结束公式块，
                # 因此删除纯空白行；这不改变公式的数学含义。
                if body_line.strip():
                    output.append(f"{block_indent}{body_line.strip()}")

            close_line = lines[close_line_index]
            close_at = close_line.find("$$")
            before_close = close_line[:close_at].strip()
            if before_close:
                output.append(f"{block_indent}{before_close}")

        output.append(f"{block_indent}$$")
        if close_line_index + 1 < len(lines) and lines[close_line_index + 1].strip():
            output.append("")
        fixed += 1
        i = close_line_index + 1

    new_content = "\n".join(output)
    if had_final_newline:
        new_content += "\n"
    if fixed:
        filepath.write_text(new_content, encoding="utf-8")
        print(f"  [FIXED] {filepath.relative_to(ROOT_DIR)}: 块公式 {fixed} 个")
    return fixed


def fix_indented_display_math(docs_dir: Path):
    """扫描 docs/ 下所有 Markdown 并规范块公式。"""
    print("\n正在规范块公式...")
    total_fixed = sum(
        fix_indented_display_math_in_file(md_file)
        for md_file in docs_dir.rglob("*.md")
    )
    print(f"块公式处理完成，共修改 {total_fixed} 个。\n")


def main():
    # 清理并重建 docs 目录
    if DOCS_DIR.exists():
        shutil.rmtree(DOCS_DIR)
    DOCS_DIR.mkdir()

    # 复制笔记目录
    for directory in NOTE_DIRS:
        src = ROOT_DIR / directory
        if src.exists():
            shutil.copytree(src, DOCS_DIR / directory)
            print(f"[COPY] {directory}/")

    # 复制单独文件
    for filename in FILES_TO_COPY:
        src = ROOT_DIR / filename
        if src.exists():
            shutil.copy2(src, DOCS_DIR / filename)
            print(f"[COPY] {filename}")

    # 复制 images 目录
    images_src = ROOT_DIR / "images"
    if images_src.exists():
        shutil.copytree(images_src, DOCS_DIR / "images")
        print(f"[COPY] images/ ({len(list(images_src.iterdir()))} 个文件)")

    # 修正构建副本中的图片路径和列表内块公式
    fix_image_refs(DOCS_DIR)
    fix_indented_display_math(DOCS_DIR)

    print("docs/ 目录准备完成！")


if __name__ == "__main__":
    main()
