# MkDocs 文档自动化生成脚本 (PowerShell)

Write-Host "🚀 开始生成 MkDocs 文档..." -ForegroundColor Green

# 检查依赖
Write-Host "📦 检查依赖..." -ForegroundColor Yellow
if (-not (Get-Command mkdocs -ErrorAction SilentlyContinue)) {
    Write-Host "❌ MkDocs 未安装，正在安装..." -ForegroundColor Red
    pip install mkdocs mkdocs-material mkdocstrings mkdocstrings-python
}

# 进入文档目录
Set-Location -Path "docs"

# 构建文档
Write-Host "📝 构建文档..." -ForegroundColor Yellow
mkdocs build --clean

Write-Host "✅ 文档构建完成！" -ForegroundColor Green
Write-Host "📂 输出目录: docs/site/" -ForegroundColor Cyan
Write-Host ""
Write-Host "🌐 预览文档:" -ForegroundColor Cyan
Write-Host "   mkdocs serve" -ForegroundColor White
Write-Host ""
Write-Host "📦 部署到 GitHub Pages:" -ForegroundColor Cyan
Write-Host "   mkdocs gh-deploy" -ForegroundColor White
