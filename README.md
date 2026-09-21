# Qoder Skill Box

可复用的 Qoder CLI Skills 集合：克隆后一条命令安装到本机 `~/.qoder/skills/`，即可在任意项目里通过 `/skill-name` 触发。

## Skills

| Skill | 用途 | 触发示例 |
|---|---|---|
| [paper-scout](skills/paper-scout) | 按研究方向检索 arXiv 论文 + GitHub 项目，输出链接与结构化拆解 | `/paper-scout agent memory`、"最近多模态有什么新工作" |
| [offer-board](skills/offer-board) | 记录投递/面试/offer 状态，渲染 HTML 看板并部署到 GitHub Pages | "字节二面过了"、"更新求职进度"、"部署进度看板" |
| [interview-prep](skills/interview-prep) | 简历+JD 生成分层面试准备文档，投喂面经自动按频次升降优先级 | "帮我准备 X 公司面试"、"收到一份面经"、"今天被问了…" |
| [skill-share](skills/skill-share) | 校验新 skill 规范并收录进本仓库、同步 GitHub | "把这个 skill 收录进仓库"、"检查 skill 规范" |

## 安装

```bash
git clone https://github.com/Lesereingrape/skillbox.git && cd skillbox

# macOS / Linux / Git Bash
bash install.sh

# PowerShell
.\install.ps1
```

安装即把 `skills/` 下所有 skill 复制到 `~/.qoder/skills/`（Windows：`C:\Users\<user>\.qoder\skills\`）。重开会话或 `/skills reload` 生效。

只想装单个：`bash install.sh paper-scout`。

## 新增 skill

1. 在 `skills/<name>/` 写 `SKILL.md`（frontmatter 含 name + 单行 description）。
2. 校验：`python skills/skill-share/scripts/validate_skill.py skills/<name>`。
3. 对 Qoder 说 `/skill-share skills/<name>` 自动完成收录 + 更新本表 + 提交。

## 依赖

- Python 3.9+（脚本仅用标准库；paper-scout 在有 certifi 时可免配置过 TLS 校验）。
- offer-board 部署需要 `gh` CLI 已登录 + 已启用 Pages 的仓库。
