---
name: offer-board
description: 秋招/实习求职进度的记录与看板部署技能：用 JSON 记录投递、测评、各轮面试、Offer、拒信状态，一句话更新状态，自动渲染单文件 HTML 看板并可部署到 GitHub Pages 持续在线。当用户说"记录我投了X"、"X面试挂了/过了/约了二面"、"更新求职进度"、"我的投递看板"、"部署进度网页"时使用。
when_to_use: 用户要记录/更新求职投递与面试状态，或查看、部署、刷新求职进度网页
argument-hint: <可选：要记录的事件，如 "字节一面通过，三面约在周五">
---

# Offer Board — 求职进度记录 + Pages 看板

## Overview

单一数据源 `data/applications.json` 记录所有投递；`scripts/render_board.py` 把它注入 HTML 模板生成自包含看板；push 到 GitHub 后 Actions 自动发布 Pages。

## 数据文件位置

按顺序找：`data/applications.json`、`applications.json`（当前目录及其子目录一层）。找不到则视为未初始化，走"初始化"。

## 更新状态（核心流程）

1. 读当前 JSON，依据 `references/schema.md` 修改：
   - 新公司 → 追加条目；已有事件 → 更新 `status`/`round`/`next_action`/`deadline`，并在 `history` 追加一行；刷新顶层 `updated` 为今天。
   - 用户一句话可能涉及多条（"腾讯挂了你帮我把网易进度也记上"），逐条确认后一次改完。
   - 状态语义拿不准时问用户，不要猜；不删除 history。
2. 渲染：`python <skill-dir>/scripts/render_board.py data/applications.json --out public/index.html`（未部署模式用默认 out 即可）。
3. 已配置 git 仓库时：commit 并 push（先向用户展示改了哪些条目）；Pages 会自动重新发布。
4. 对话里回复一行变更摘要（哪条状态从 A → B），不要把整个 JSON 贴出来。

## 初始化（本地看板，不联网）

1. `mkdir -p data public`，按 schema 写一个含 1–2 条真实记录的 `data/applications.json`（请用户口述现有投递，别造假数据）。
2. 渲染并在浏览器打开 `index.html` 验证。

## 部署到 GitHub Pages

前置确认（一次问清）：仓库名（默认 `offer-board`）、公开还是私有。**必须告知用户：Pages 站点内容公网可抓取，看板会暴露求职去向；手机号/邮箱等绝不写入 JSON。**

1. 目录：`data/applications.json`、`public/index.html`、`.github/workflows/deploy-pages.yml`（复制 `<skill-dir>/assets/deploy-pages.yml`）。
2. `.gitignore` 不需要特殊处理（index.html 属于产物但入库，Pages 直接吃静态文件）。
3. 创建并推送（GitHub 网络受限时先 `export HTTPS_PROXY=http://127.0.0.1:7897`）：
   ```
   git init -b main && git add . && git commit -m "init offer board"
   gh repo create <name> --public --push --source .
   gh api repos/<owner>/<name>/pages -X POST -f 'source[branch]=main' -f 'source[path]=public'
   ```
   若 Pages 已存在则跳过最后一步。
4. 等 30–60 秒，用 `gh api repos/<owner>/<name>/pages --jq .html_url` 拿地址，浏览器打开核对渲染结果后把链接给用户。

## 日常同步

用户说"同步/上线一下" → 渲染到 `public/index.html` → `git add -A && git commit -m "update: <摘要>" && git push` → 回报 Pages 链接。

## Resources

- `scripts/render_board.py` — JSON → 单文件 HTML（stdlib，无依赖）。
- `references/schema.md` — 数据契约：字段、status 枚举、修改规则、隐私红线。
- `assets/dashboard-template.html` — 看板模板（暗色卡片 + 状态分组 + 搜索过滤），占位符 `__BOARD_DATA__`。
- `assets/deploy-pages.yml` — GitHub Actions 静态发布工作流（发布 `public/`）。
