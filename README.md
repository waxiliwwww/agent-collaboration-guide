# 协作规约

和 Agent 协作时，这些问题最常出现：确认过的做法下次被忘了；你指出一个问题，同类的问题没人查；改了很久，结果还是取不回来；你不知道到底做完了没有。

这个技能处理这些问题。它不管你在做什么任务，只管协作过程的质量。

## 规约要求 Agent 怎样做

- **沿用已有决定**：读取已确认的背景与取舍，条件未变不重复问。
- **检查同类问题**：用户指出一处错误时，同时检查共享原因和相关使用路径。
- **检查实际结果**：确认成果可以取回和使用，不以运行了命令代替结果可用。
- **说清完成情况**：分别说明验证过、没验证和没完成的内容。

这些是执行要求，不是安装后必然达到的效果；实际执行、用户理解与业务验收仍需分别核实。[已有证据及其范围](docs/evidence.md)

## 怎么用

安装后，在任务里说：

> 请按 agent-collaboration-guide 协作规约，帮我完成……

也可以在宿主配置里设为默认，之后不用每次点名。

给出目标、已有材料和已知限制就够了。尚未授权的新功能或重要取舍才需要你判断，其他的 Agent 自己处理。

## 有现成技能就先用

这个技能管协作质量，制作和检查方法优先用专门的技能：

| 要做的事 | 先用什么 |
| --- | --- |
| 制作网页 PPT | [guizang-ppt-skill](https://github.com/op7418/guizang-ppt-skill) |
| 去套话、改进文风 | [human-writing-skills](https://github.com/whh110112/human-writing-skills) |
| 写测试、检查测试是否有效 | [prove-it](https://github.com/nagi-studio/skills/tree/main/skills/rookie/prove-it) |

具体选用、缺失和授权处理见[技能复用](skills/agent-collaboration-guide/references/recommended-skills.md)。[技能与资料收藏](docs/resource-collection.md)仅供用户浏览，不在默认执行阅读链中。

## 安装和更新

将仓库中的 `skills/agent-collaboration-guide` 安装到宿主的技能目录。已有安装时运行更新器：

```bash
python3 skills/agent-collaboration-guide/scripts/update_install.py \
  skills/agent-collaboration-guide /path/to/skills/agent-collaboration-guide
```

首次安装加 `--init-local` 创建私有配置入口；`--dry-run` 可先预览。更新器只复制公共文件，保留 `local/`。

---

<details>
<summary>Agent 读哪些内容</summary>

宿主先把技能名称和 description 提供给 Agent。用户点名、默认采用或任务匹配后，Agent 按宿主约定读指定配置、SKILL.md 和项目规则，按需读取场景扩展；通用规则始终适用，继续同一任务时未变内容沿用。

```mermaid
flowchart TD
    A[任务开始] --> B[读指定配置、SKILL.md 和项目规则]
    B --> C{需要专门方法？}
    C -- 是 --> D[按路由表读对应扩展材料]
    C -- 否 --> E[用通用三步主干完成工作]
    D --> E
    E --> F[对照原始目标核对，说清完成情况]
```

</details>

<details>
<summary>文件分工</summary>

| 位置 | 内容 |
| --- | --- |
| README | 给使用者和维护者：用途、怎么运行、安装和文件分工 |
| [SKILL.md](skills/agent-collaboration-guide/SKILL.md) | 给 Agent：通用底线三步 + 路由表 |
| `references/` | 写作、测试、代码、演示等专门方法，按需读取 |
| 安装后的 `local/` | 个人选择和私有记录，不进公共仓库 |
| `docs/` | 收藏、例子、设计来源和验证记录 |

</details>

---

当前版本 **0.8.20**，以 SKILL.md 元数据为准。

[修订记录](CHANGELOG.md) · [设计与来源](docs/design-and-sources.md) · [使用示例](docs/examples.md) · [MIT 许可](LICENSE)
