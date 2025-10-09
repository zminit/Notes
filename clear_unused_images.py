import os
import re
import sys
import urllib.parse
import shutil # <-- 确保导入

def find_markdown_files(note_folder):
    """
    递归查找指定文件夹下所有的 Markdown 文件 (.md, .markdown)。
    """
    markdown_files = []
    for root, _, files in os.walk(note_folder):
        for file in files:
            if file.endswith(('.md', '.markdown')):
                markdown_files.append(os.path.join(root, file))
    return markdown_files

def extract_referenced_images(markdown_files):
    """
    从 Markdown 文件中提取所有引用的图片文件名，并处理 URL 编码和额外属性。
    """
    referenced_images = set()
    image_pattern = re.compile(
        r'../images/(.*?\.(?:png|jpg|jpeg|gif|svg|webp|bmp|tiff))', 
        re.IGNORECASE
    )

    for file_path in markdown_files:
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
                matches = image_pattern.findall(content)
                for image_name in matches:
                    decoded_image_name = urllib.parse.unquote(image_name.strip())
                    referenced_images.add(decoded_image_name)
        except Exception as e:
            print(f"Error reading file {file_path}: {e}")
            
    return referenced_images

def find_all_images(images_folder):
    """
    获取 images 文件夹中所有的文件名。
    """
    if not os.path.isdir(images_folder):
        return []
    return [f for f in os.listdir(images_folder) if os.path.isfile(os.path.join(images_folder, f)) and not f.startswith('.')]

def main():
    """
    主执行函数。
    """
    if getattr(sys, 'frozen', False):
        base_dir = os.path.dirname(sys.executable)
    else:
        base_dir = os.path.dirname(os.path.abspath(__file__))
        
    note_folder = os.path.join(base_dir)
    images_folder = os.path.join(base_dir, 'images')
    trash_bin_folder = os.path.join(base_dir, 'trash bin')

    print(f"📓 笔记文件夹: {note_folder}")
    print(f"🖼️ 图片文件夹: {images_folder}")
    print(f"🗑️ 垃圾箱文件夹: {trash_bin_folder}\n")

    if not os.path.isdir(note_folder):
        print(f"❌ 错误: 找不到笔记文件夹 '{note_folder}'。请确保脚本位置正确。")
        sys.exit(1)
    if not os.path.isdir(images_folder):
        print(f"❌ 错误: 找不到图片文件夹 '{images_folder}'。请确保脚本位置正确。")
        sys.exit(1)

    # 1. 查找所有 Markdown 文件
    markdown_files = find_markdown_files(note_folder)
    if not markdown_files:
        print("🟡 警告: 在 'Note' 文件夹中没有找到任何 Markdown 文件。")
        return
    print(f"✅ 找到 {len(markdown_files)} 个 Markdown 文件。")

    # 2. 提取所有被引用的图片
    referenced_images = extract_referenced_images(markdown_files)
    print(f"✅ 提取到 {len(referenced_images)} 个被引用的图片链接。")

    # 3. 查找 images 文件夹中的所有图片
    all_images_in_folder = find_all_images(images_folder)
    print(f"✅ 在 'images' 文件夹中找到 {len(all_images_in_folder)} 个图片文件。")

    # 4. 找出未被引用的图片
    unreferenced_images = set(all_images_in_folder) - referenced_images
    
    if not unreferenced_images:
        print("\n🎉 恭喜！ 'images' 文件夹中没有未被引用的图片。")
        return

    print("\n--- 发现未引用的图片 ---")
    for i, image_name in enumerate(unreferenced_images, 1):
        print(f"{i}. {image_name}")
    print("--------------------------\n")

    # 5. 请求用户确认移动
    try:
        confirm = input(f"❓ 是否要将这 {len(unreferenced_images)} 个未引用的图片移动到 'trash bin' 文件夹？ (输入 'yes' 确认): ")
    except KeyboardInterrupt:
        print("\n操作已取消。")
        return

    if confirm.lower() == 'yes':
        os.makedirs(trash_bin_folder, exist_ok=True)
        
        moved_count = 0
        for image_name in unreferenced_images:
            source_path = os.path.join(images_folder, image_name)
            destination_path = os.path.join(trash_bin_folder, image_name)
            try:
                shutil.move(source_path, destination_path)
                print(f"📁 已移动到 trash bin: {image_name}")
                moved_count += 1
            except Exception as e:
                print(f"❌ 移动失败: {image_name} - {e}")
        print(f"\n✅ 操作完成！共移动了 {moved_count} 个图片文件到 'trash bin'。")
    else:
        print("操作已取消，没有文件被移动。")

if __name__ == '__main__':
    main()