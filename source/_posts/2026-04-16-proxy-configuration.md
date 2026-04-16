---
title: 代理配置指南
date: 2026-04-16 12:00:00
categories: 技术笔记
tags:
  - 代理配置
  - yum
  - docker
  - pip
---

# 代理配置指南

## 1. yum配置代理

```bash
# vim /etc/yum.conf
# 加入下面一行代理配置
proxy= http://10.33.49.191:10809
```

## 2. docker 配置代理

```bash
sudo mkdir -p /etc/systemd/system/docker.service.d
vim /etc/systemd/system/docker.service.d/http-proxy.conf    
#添加代理配置
[Service]
Environment="HTTP_PROXY=http://your-proxy-server:port/"
Environment="HTTPS_PROXY=https://your-proxy-server:port/"
Environment="NO_PROXY=localhost,127.0.0.1,.example.com"
```

## 3. pip配置代理和源

```bash
pip config set global.proxy http://10.100.28.114:3180
pip config set global.index-url https://mirrors.ustc.edu.cn/pypi/simple
pip config set global.trusted-host mirrors.ustc.edu.cn
```