#!/bin/bash
# MkDocs 文档自动化生成脚本

set -e

echo "🚀 开始生成 MkDocs 文档..."

# 检查依赖
echo "📦 检查依赖..."
if ! command -v mkdocs &> /dev/null; then
    echo "❌ MkDocs 未安装，正在安装..."
    pip install mkdocs mkdocs-material mkdocstrings mkdocstrings-python
fi

# 进入文档目录
cd docs

# 构建文档
echo "📝 构建文档..."
mkdocs build --clean

echo "✅ 文档构建完成！"
echo "📂 输出目录: docs/site/"
echo ""
echo "🌐 预览文档:"
echo "   mkdocs serve"
echo ""
echo "📦 部署到 GitHub Pages:"
echo "   mkdocs gh-deploy"
