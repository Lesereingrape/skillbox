# applications.json 数据契约

## 顶层

```json
{
  "owner": "显示在看板标题的昵称",
  "season": "2027届秋招",
  "updated": "YYYY-MM-DD（每次改动都要刷新）",
  "applications": [ ... ]
}
```

## application 条目

```json
{
  "id": "字节-大模型算法",
  "company": "字节跳动",
  "position": "大模型算法工程师",
  "batch": "提前批",
  "channel": "官网",
  "status": "interviewing",
  "round": "三面",
  "url": "",
  "applied_at": "2026-08-12",
  "next_action": "等待三面反馈",
  "deadline": "2026-09-30",
  "history": [
    {"date": "2026-08-12", "event": "官网投递"},
    {"date": "2026-09-05", "event": "三面"}
  ],
  "notes": "面试官关注 agent 框架落地经验"
}
```

## status 枚举（看板按此分组）

| 值 | 含义 |
|---|---|
| to_apply | 待投递（准备好的目标） |
| applied | 已投递无反馈 |
| assessment | 待做测评/笔试 |
| interviewing | 面试流程中（配合 round 字段写第几面） |
| offer | 已有 offer 待比较/待答复 |
| accepted | 已接 offer 签约 |
| rejected | 被拒 |
| dropped | 主动放弃/关闭 |

## 修改规则

- id 唯一且稳定，重命名公司时不改 id，只改 company。
- 状态只能前进不回退；流程倒退（如三面挂后重开）用新条目 + notes 关联说明。
- 每次事件在 history 追加一条，不删除旧条目。
- deadline 只填 offer 答复、流程关闭等真实截止日，可留空。
- 页面公网可见：不写入手机号、邮箱、身份证等敏感信息。
