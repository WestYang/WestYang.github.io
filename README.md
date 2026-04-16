# 杨森的学习笔记

这是一个使用Hexo静态站点生成器构建的个人博客，通过GitHub Actions实现自动构建和部署。

## 功能特点

- 使用Markdown编写文章
- GitHub Actions自动构建和部署
- 支持分类和标签
- 响应式设计

## 如何使用

### 1. 添加新文章

1. 在 `source/_posts` 目录中创建Markdown文件
2. 文件名格式：`YYYY-MM-DD-title.md`
3. 文件头部需要包含Front Matter，例如：

```markdown
---
title: 文章标题
date: 2026-04-16 12:00:00
categories: 分类
 tags:
  - 标签1
  - 标签2
---

文章内容...
```

4. 提交更改并推送到GitHub
5. GitHub Actions会自动构建并部署到GitHub Pages

### 2. 本地测试

如果需要在本地测试，可以按照以下步骤操作：

1. 安装Node.js和npm
2. 安装依赖：`npm install`
3. 本地预览：`npx hexo server`
4. 构建静态文件：`npm run build`

### 3. 部署

部署完全由GitHub Actions自动处理，无需手动操作。当你将更改推送到GitHub仓库时，GitHub Actions会自动：

1. 安装依赖
2. 构建静态文件
3. 部署到GitHub Pages

## 项目结构

```
.
├── .github/            # GitHub Actions工作流
├── source/             # 源文件
│   └── _posts/         # Markdown格式的文章
├── public/             # 生成的静态文件（自动生成）
├── _config.yml         # Hexo配置文件
├── package.json        # 项目配置和依赖
└── README.md           # 项目说明
```

## 技术栈

- Hexo 6.3.0
- GitHub Actions
- GitHub Pages
- Markdown

## 访问地址

博客地址：https://westyang.github.io