# Agent Collaboration Guide · 协作规约

一个指导性 Agent Skill，帮助人和智能体固定目标与范围、解释复杂机制、沿真实交接完成工作，并从明确反馈中改进下一次处理。适合默认协作、长任务接续、技术文档、开发验证和重要结果复核；清楚的小请求保持轻量。

**唯一使用入口：[SKILL.md](skills/agent-collaboration-guide/SKILL.md)。** 入口直接给出能力、适用边界、主干方法和场景直达表；不用先读项目说明、历史或全部参考才能决定是否有用。README 只负责安装与维护定位。

## 安装与更新

从本仓库取得 `skills/agent-collaboration-guide`，安装到宿主的技能目录。支持 Codex、DSH 等能读取 Agent Skill 的环境，具体发现与权限行为以宿主为准，不承诺自动加载效果。

使用包内更新器，避免删除整个旧安装而丢失本地配置：

```bash
python3 skills/agent-collaboration-guide/scripts/update_install.py \
  skills/agent-collaboration-guide /你的技能目录/agent-collaboration-guide --init-local
```

首次创建缺失的 `local/preferences.md`；更新时同样执行，已有私有内容保留。先预览可加 `--dry-run`。脚本只复制公共文件、跳过源 `local/`，不删除目标整树，也不读取或替换其中的私有数据。更新失败如实报告，需重新检查完成状态。

公共方法与私有偏好分工如下：

```text
agent-collaboration-guide/
├── SKILL.md                 唯一使用入口与通用主干
├── references/              按场景读取的扩展
├── scripts/update_install.py 保留私有目录的公开文件更新器
├── agents/openai.yaml       宿主界面元数据
└── local/                   安装后私有；公开源不包含
    ├── preferences.md       当前个人选择与按需索引
    └── …                    项目、场景和历史，确有需要才建立
```

外置配置仍可显式指定。迁移已有配置先备份、对照有效项，旧入口改指针，不保留两份独立真源。常驻入口只加载当前有效选择；历史、案例和项目细节按需读取。[配置与更新细则](skills/agent-collaboration-guide/references/local-profile.md)

## 如何越用越合适

初次采用 → 读取当前有效偏好 → 按任务执行 → 明确纠正及时写回 → 相关任务回用 → 复核实际效果 → 提炼可复用方法、清理重复。

本次决定、项目约束、个人偏好与推断分开保存；同类反复偏差先查规则、触发、执行和检查哪一处失效。通用候选脱敏并说明边界和成本后再进入公共技能，个人路径、固定格式及授权不随之公开。详见入口和[反馈闭环](skills/agent-collaboration-guide/references/decisions-and-review.md)。

场景扩展是按需读取的文件，不新增插件运行服务；可选制作／写作技能是独立依赖，只有任务适用时才采用。[推荐资源](skills/agent-collaboration-guide/references/recommended-skills.md)

## 维护与证据

当前版本 **0.7.1**。唯一维护源为本仓库，安装目录是发行副本；日常任务不要求每次联网更新。`local/` 不提交，导出时从公开源复制，勿直接打包整个安装目录。其他更新器是否保留本地数据需要核对，不能只依赖忽略规则。

结构、更新保留与引用检查证明的是包可用与私有数据保护；场景演练只能说明相应样例的表现，不能证明以后所有模型和任务都会更快收敛。发布与外部变更仍需相应授权。

- [验证与已知限制](docs/evidence.md)
- [来源与设计取舍](docs/design-and-sources.md)
- [使用示例](docs/examples.md)
- [修订记录](CHANGELOG.md)
- [MIT 许可](LICENSE)与[第三方说明](THIRD_PARTY_NOTICES.md)

历史母本已退役。[原始理念](skills/agent-collaboration-guide/references/principles-original.md)保留为背景，不作为另一套使用入口。
