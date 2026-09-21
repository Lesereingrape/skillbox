---
name: skill-share
description: 把本地写好的 skill 收录进团队的 skill 集合仓库并同步到 GitHub：校验 SKILL.md 规范、复制到 skills/ 目录、更新仓库 README 清单、提交并推送。当用户说"把这个 skill 收录进仓库"、"同步 skill 到 GitHub"、"检查 skill 规范"、"新增一个 skill 到集合"时使用。
when_to_use: 用户要把新建的 skill 加入本地 skill 集合仓库、校验 skill 格式或推送到 GitHub
argument-hint: <skill 目录路径，如 C:\...\skills\my-skill>
---

# Skill Share — 校验并收录 skill 到集合仓库

## Overview

以一个"集合仓库"（根下有 `skills/` 目录和 README 清单的 git 仓库）为中心：校验 → 收录 → 更新清单 → 提交推送。

## 步骤

### 1. 定位两端

- 来源：参数给出的 skill 目录；未给则询问要收录哪个 skill。
- 集合仓库：在工作目录内找含 `skills/` 且带 README 清单的仓库；找不到就问用户路径，或提议新建（`mkdir -p <name>/skills` + 建 README 表 + `git init`）。

### 2. 校验

```
python <skill-dir>/scripts/validate_skill.py <待收录目录> <仓库内全部现存 skill>
```

FAIL 时逐条修复（改 frontmatter、删 TODO、删多余 README/空目录），修复原则见仓库里任意现存 skill 的写法；不确定的命名问题问用户。

### 3. 收录

- 复制整个 skill 文件夹到 `<repo>/skills/<name>/`（保持文件夹名 = frontmatter name）。
- 若同名 skill 已存在：diff 后询问用户是覆盖还是跳过，不要静默覆盖。
- 更新仓库 README 的 skill 清单表：加一行"skill 名 | 一句话用途 | 触发词示例"。

### 4. 安装到本机（可选，用户要求时做）

复制 `<repo>/skills/<name>/` 到用户级目录 `~/.qoder/skills/<name>/`（Windows 为 `C:\Users\<user>\.qoder\skills\`），提醒 `/skills reload` 或重开会话生效。

### 5. 提交与推送

- `git status` 确认只包含预期文件后 commit，消息格式：`add(<skill-name>): <一句话用途>`。
- **push 是对外可见操作：先向用户确认远程仓库与推送，再执行**；GitHub 网络受限时 `export HTTPS_PROXY=http://127.0.0.1:7897`。

## Resources

- `scripts/validate_skill.py` — 规范检查：frontmatter、name 与文件夹一致性、description 单行 ≤1024、正文 ≤500 行、无 TODO、无多余文档、无空资源目录；多目录批量输出 PASS/FAIL。
