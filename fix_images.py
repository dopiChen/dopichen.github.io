import os
import shutil
import re

# 1️⃣ 设置路径
posts_dir = "_xjtuse-algorithm"  # 原始 Markdown 文件夹
attachment_dir = os.path.join(posts_dir, "attachment")  # 旧图片目录
assets_dir = "assets/xjtuse-algorithm"  # 目标图片目录

# 2️⃣ 确保目标 `assets` 目录存在
os.makedirs(assets_dir, exist_ok=True)

# 3️⃣ 移动图片到 `assets/`
image_extensions = (".png", ".jpg", ".jpeg", ".webp")

for filename in os.listdir(attachment_dir):
    if filename.endswith(image_extensions):  # 只处理图片文件
        src_path = os.path.join(attachment_dir, filename)
        dest_path = os.path.join(assets_dir, filename)

        shutil.move(src_path, dest_path)  # 移动文件
        print(f"✅ 移动图片: {filename} → {dest_path}")

# 4️⃣ 批量修改 Markdown 文件中的图片路径
md_files = [f for f in os.listdir(posts_dir) if f.endswith(".md")]

for md_file in md_files:
    md_path = os.path.join(posts_dir, md_file)

    with open(md_path, "r", encoding="utf-8") as f:
        content = f.read()

    # 使用正则替换 `![](attachment/xxx.webp)` → `![](/assets/xjtuse-project-management/xxx.webp)`
    new_content = re.sub(r"!\[\]\(attachment/([\w\.-]+)\)", r"![](/assets/xjtuse-algorithm/\1)", content)

    with open(md_path, "w", encoding="utf-8") as f:
        f.write(new_content)

    print(f"✅ 更新 Markdown: {md_file}")

print("\n🎉 所有图片已移动，Markdown 也已更新！")
