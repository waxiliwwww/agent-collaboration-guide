# 协作规约（Agent Collaboration Guide）

一个 Agent Skill，用来约束人和智能体共同完成一项工作时的几个关键动作：开始前确认目标、范围和完成条件；执行中沿现有入口把真实交接走通；交付时说明做了什么、验证到哪里、还剩什么。

适合需求讨论、长任务接续、技术文档、开发验证和结果复核。清楚的小修可以直接做，不要求先建计划、台账或逐项确认。

方法入口是 [SKILL.md](skills/agent-collaboration-guide/SKILL.md)。那里写了适用边界、主干方法和按场景读取的参考；这份 README 说明使用结构、安装、目录和更新。

## 怎样使用

宿主先提供技能名称与描述，用户点名或 Agent 判断匹配后读取 `SKILL.md`；已指定的宿主默认入口可先要求读取本机配置；本规约沿该入口，按当前任务读取项目规则和必要场景扩展。常见协作场景可以适用，简单请求保持轻量，不靠“任何事都必读全部材料”触发。

场景中发现已有专用技能可承担任务时，实际复用其模板、脚本与方法，本规约只补目标、授权、交接和验收缺口；没有时说明能力边界、按需建议具体安装，不假装已有。描述匹配、阅读和执行由宿主及 Agent 完成，不是本仓库的自动调度服务，也不保证每次都触发或遵守。SKILL.md 是执行入口，README 不替代它。

[技能与资料收藏](docs/resource-collection.md)仅供用户浏览，不在默认执行阅读链中；场景使用的选用方法另在技能包内维护，不要求先读整份收藏。

## 安装

把仓库里的 `skills/agent-collaboration-guide` 目录安装到宿主的技能目录。支持 Agent Skill 的宿主可以按各自的发现方式加载，Codex、DSH 等环境均可使用；具体触发和权限行为以宿主为准。

Codex 可以用 `skill-installer` 从本仓库安装。手工安装时，把整个技能目录复制到目标位置，已有同名技能先备份再替换。

安装后直接用技能名调用即可。

## 更新

从仓库运行更新器，只替换公共文件，保留安装目录里的 `local/`：

```bash
python3 skills/agent-collaboration-guide/scripts/update_install.py \
  skills/agent-collaboration-guide /path/to/skills/agent-collaboration-guide --init-local
```

先加 `--dry-run` 可以只看将写入哪些文件。首次运行时，`--init-local` 会在缺少 `local/preferences.md` 时创建一个入口；已有的私有配置不会被读取或覆盖。更新器不会删除目标目录里的其他内容。

## 目录

```text
skills/agent-collaboration-guide/
├── SKILL.md                  使用入口与通用方法
├── references/               按场景读取的扩展
├── scripts/update_install.py 保留私有目录的更新器
├── agents/openai.yaml        宿主界面元数据
└── local/                    安装后的私有配置；公开源不包含
```

`local/` 里放个人选择、项目约定和必要的场景记录。配置也可以放在宿主或项目指定的位置；迁移时先备份，再让旧入口指向新位置，避免同一项内容维护两份。[配置与更新细则](skills/agent-collaboration-guide/references/local-profile.md)

## 版本与维护

当前版本 **0.8.12**。本仓库是维护源，安装目录是发行副本；日常使用不需要每次联网更新。`local/` 不进公开仓库，导出时从公开源复制，不要直接打包整个安装目录。

结构、更新保留和引用检查能说明包可以使用、私有文件没有被替换；它们不能证明每个模型在每项任务上都会按这套方法执行，实际效果仍要看具体任务。

- [修订记录](CHANGELOG.md)
- [验证与已知限制](docs/evidence.md)
- [来源与设计取舍](docs/design-and-sources.md)
- [使用示例](docs/examples.md)
- [MIT 许可](LICENSE) 与[第三方说明](THIRD_PARTY_NOTICES.md)

更早的协作母本已退役；[原始理念](skills/agent-collaboration-guide/references/principles-original.md)保留作背景，不作为另一套入口。
