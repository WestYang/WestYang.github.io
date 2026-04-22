# 杨森的学习笔记

这是一个基于静态网站生成器的个人博客项目，用于分享技术学习笔记和博客文章。

## 项目结构

```
WestYang.github.io/
├── blog/                 # 生成的HTML文章
├── css/                  # 样式文件
├── js/                   # JavaScript文件
├── posts/                # Markdown格式的文章源文件
├── scripts/              # 构建脚本
│   ├── build_site.py     # 主构建脚本
│   └── sync_dist_to_root.py  # 同步构建结果到根目录
├── .github/workflows/    # GitHub Actions工作流
│   └── deploy-pages.yml  # 自动构建和部署工作流
├── .gitignore            # Git忽略配置
├── about.html            # 关于页面
├── archives.html         # 归档页面
├── index.html            # 首页
└── requirements.txt      # Python依赖管理
```

## 技术栈

- **前端**：HTML5, CSS3, JavaScript
- **后端**：Python 3
- **构建工具**：自定义Python脚本
- **部署**：GitHub Actions, GitHub Pages

## 功能特点

- 支持Markdown格式的文章
- 自动生成HTML页面
- 响应式设计，支持移动端
- 文章归档功能
- 标签功能
- 自动部署到GitHub Pages

## 如何使用

### 本地开发

1. **克隆仓库**：
   ```bash
   git clone https://github.com/WestYang/WestYang.github.io.git
   cd WestYang.github.io
   ```

2. **安装依赖**：
   ```bash
   pip install -r requirements.txt
   ```

3. **添加文章**：
   在 `posts` 目录中创建Markdown格式的文章文件，例如 `2026-04-22-my-post.md`。

4. **构建网站**：
   ```bash
   python scripts/build_site.py
   ```

5. **查看构建结果**：
   构建结果会生成在 `dist` 目录中，可以使用本地服务器查看。

### 部署到GitHub Pages

1. **推送更改**：
   将Markdown文章和其他更改推送到GitHub仓库。

2. **自动构建**：
   GitHub Actions会自动检测到更改，并执行构建和部署流程。

3. **访问网站**：
   部署完成后，访问 `https://westyang.github.io` 查看网站。

## 文章格式

Markdown文章可以包含Front Matter，用于指定文章的元数据：

```markdown
---
title: 文章标题
date: 2026-04-22
category: 技术笔记
tags: [标签1, 标签2]
summary: 文章摘要
---

文章内容...
```

## 配置

### 站点配置

在 `scripts/build_site.py` 文件中，可以修改以下配置：

- `SITE_NAME`：网站名称
- `SITE_SUBTITLE`：网站副标题
- `SITE_YEAR`：版权年份

### GitHub Actions配置

在 `.github/workflows/deploy-pages.yml` 文件中，可以修改构建和部署的配置。

## 常见问题

1. **构建失败**：
   检查Markdown文件的格式是否正确，确保Front Matter格式正确。

2. **部署失败**：
   检查GitHub Actions的执行日志，查看具体的错误信息。

3. **文章不显示**：
   确保文章文件放在 `posts` 目录中，并且文件名以 `.md` 结尾。

## 贡献

欢迎提交Issue和Pull Request，帮助改进这个项目。

## 许可证

本项目采用MIT许可证。

## 联系方式

如果有任何问题或建议，请联系杨森。
