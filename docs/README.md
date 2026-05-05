# 智能旅行助手 API 文档

基于 MkDocs Material 主题构建的 API 文档系统。

## 快速开始

### 1. 安装依赖

```bash
pip install mkdocs mkdocs-material mkdocstrings mkdocstrings-python
```

### 2. 预览文档

```bash
cd docs
mkdocs serve
```

访问 http://localhost:8000 查看文档。

### 3. 构建文档

```bash
mkdocs build
```

生成的静态文件位于 `site/` 目录。

### 4. 部署到 GitHub Pages

```bash
mkdocs gh-deploy
```

## 自动化脚本

### Windows (PowerShell)

```powershell
.\build_docs.ps1
```

### Linux/Mac

```bash
chmod +x build_docs.sh
./build_docs.sh
```

## 文档结构

```
docs/
├── mkdocs.yml              # MkDocs 配置
├── docs/                   # 文档源文件
│   ├── index.md           # 首页
│   ├── getting-started/   # 快速开始
│   ├── api/               # API 接口文档
│   ├── models/            # 数据模型
│   └── architecture/      # 架构设计
└── site/                  # 生成的静态文件
```

## 自定义主题

编辑 `mkdocs.yml` 修改主题配置：

```yaml
theme:
  name: material
  palette:
    primary: teal
    accent: teal
```

## 添加新页面

1. 在 `docs/` 目录下创建 `.md` 文件
2. 在 `mkdocs.yml` 的 `nav` 部分添加导航
3. 运行 `mkdocs serve` 预览
