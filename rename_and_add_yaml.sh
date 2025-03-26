#!/bin/bash

# 目标目录
TARGET_DIR="_xjtuse-algorithm"
DATE="2024-12-26"  # 统一时间戳，可以改成当前日期

# 确保目录存在
if [ ! -d "$TARGET_DIR" ]; then
    echo "❌ 目录 $TARGET_DIR 不存在，请检查路径！"
    exit 1
fi

# 遍历 Markdown 文件
for file in "$TARGET_DIR"/*.md; do
    # 获取原文件名（去掉路径）
    filename=$(basename "$file")

    # 提取序号和标题，例如 `1、绪论.md`
    if [[ "$filename" =~ ([0-9]+)、(.+)\.md ]]; then
        num="${BASH_REMATCH[1]}"      # 1
        title="${BASH_REMATCH[2]}"    # 绪论

        # 生成新文件名
        new_filename="${DATE}-${title}.md"

        # 检查文件是否已处理过，防止重复添加 YAML 头
        if ! grep -q "^---" "$file"; then
            # 添加 YAML 头部
            yaml_header="---
layout: post
title: \"$title\"
date: $DATE
collection: xjtuse-project-management
---"

            # 先加 YAML 头，再重命名
            echo "$yaml_header" | cat - "$file" > "${TARGET_DIR}/temp.md" && mv "${TARGET_DIR}/temp.md" "$file"
        fi

        # 重命名文件
        mv "$file" "${TARGET_DIR}/${new_filename}"
        echo "✅ 处理完成：$filename -> $new_filename"
    else
        echo "⚠️ 无法解析文件名格式：$filename，跳过"
    fi
done

echo "🎉 所有 Markdown 文件处理完成！"
