import os
import shutil
import re
from PIL import Image

# 1️⃣ 设置路径
posts_dir = "_xjtuse-algorithm"  # 原始 Markdown 文件夹
attachment_dir = os.path.join(posts_dir, "attachment")  # 旧图片目录
assets_dir = "assets/xjtuse-algorithm"  # 目标图片目录

# 2️⃣ 确保目标 `assets` 目录存在
os.makedirs(assets_dir, exist_ok=True)

# 3️⃣ 处理图片
image_extensions = (".png", ".jpg", ".jpeg", ".webp")
max_width = 800  # 设置最大宽度

for filename in os.listdir(attachment_dir):
    if filename.endswith(image_extensions):  # 只处理图片文件
        src_path = os.path.join(attachment_dir, filename)
        dest_path = os.path.join(assets_dir, filename)

        try:
            with Image.open(src_path) as img:
                width, height = img.size
                if width > max_width:
                    # 计算新的高度，保持纵横比
                    new_height = int((max_width / width) * height)
                    img = img.resize((max_width, new_height), Image.ANTIALIAS)
                    img.save(dest_path)  # 保存缩放后的图片
                    print(f"📏 缩小图片: {filename} ({width}x{height} → {max_width}x{new_height}) → {dest_path}")
                else:
                    shutil.move(src_path, dest_path)  # 直接移动不缩放
                    print(f"✅ 移动图片: {filename} → {dest_path}")

        except Exception as e:
            print(f"❌ 处理图片失败: {filename}, 错误: {e}")

# 4️⃣ 批量修改 Markdown 文件中的图片路径
md_files = [f for f in os.listdir(posts_dir) if f.endswith(".md")]

for md_file in md_files:
    md_path = os.path.join(posts_dir, md_file)

    with open(md_path, "r", encoding="utf-8") as f:
        content = f.read()

    # 使用正则替换 `![](attachment/xxx.webp)` → `![](/assets/xjtuse-algorithm/xxx.webp)`
    new_content = re.sub(r"!\[\]\(attachment/([\w\.-]+)\)", r"![](/assets/xjtuse-algorithm/\1)", content)

    with open(md_path, "w", encoding="utf-8") as f:
        f.write(new_content)

    print(f"✅ 更新 Markdown: {md_file}")

print("\n🎉 所有图片已移动，并且超大图片已缩小！")
