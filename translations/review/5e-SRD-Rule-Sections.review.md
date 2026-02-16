# 5e-SRD-Rule-Sections 翻译审查报告

## 审查统计
- 审查时间：2026-02-16 20:53:22
- 审查规则分段总数：33
- 问题数量：8

## 问题列表

### 1. [术语不一致] 使用各属性 (using-each-ability)
- 位置：index: using-each-ability
- 问题描述：技能译名与 GLOSSARY.md 标准译名不一致
  - 使用了"杂技"，标准应为"体操" (Acrobatics)
  - 使用了"手上功夫"，标准应为"巧手" (Sleight of Hand)
- 建议修正：
  ```json
  {
    "old": "***杂技。*** 你的敏捷（杂技）检定涵盖你在保持平衡时遇到的困难情况",
    "new": "***体操。*** 你的敏捷（体操）检定涵盖你在保持平衡时遇到的困难情况"
  }
  {
    "old": "***手上功夫。*** 你的敏捷（手上功夫）检定涵盖你试图灵活操纵某物时遇到的困难情况",
    "new": "***巧手。*** 你的敏捷（巧手）检定涵盖你试图灵活操纵某物时遇到的困难情况"
  }
  ```

### 2. [翻译不完整] 时间 (time)
- 位置：index: time
- 问题描述：英文句子未翻译
  - "hurry across those fifteen miles in just under four hours' time" 仍为英文
- 建议修正：
  ```json
  {
    "old": "急于到达森林中心孤独塔的冒险者 hurry across those fifteen miles in just under four hours' time。",
    "new": "急于到达森林中心孤独塔的冒险者在不到四小时的时间内赶完这十五英里。"
  }
  ```

### 3. [翻译不完整] 水下战斗 (underwater-combat)
- 位置：index: underwater-combat
- 问题描述：英文词组未翻译
  - "flooded dungeon room" 未翻译
- 建议修正：
  ```json
  {
    "old": "或发现自己在 flooded dungeon room 中时",
    "new": "或发现自己身处被水淹没的地下城房间时"
  }
  ```

### 4. [术语不一致] 伤害与治疗 (damage-and-healing)
- 位置：index: damage-and-healing
- 问题描述："濒死"状态术语未在 GLOSSARY 中定义
  - 原文使用 "dying"，翻译为"濒死"
  - 虽然翻译合理，但建议与 GLOSSARY 统一
- 建议修正：
  - 在 GLOSSARY.md 中增加：
    | Dying | 濒死 | 0生命值且未稳定的状态 |

### 5. [格式问题] 什么是法术 (what-is-a-spell)
- 位置：index: what-is-a-spell
- 问题描述：Markdown 标题格式不一致
  - "法术等级"小节使用了 #### 四级标题，而其他同级小节使用 ### 三级标题
- 建议修正：
  ```json
  {
    "old": "#### 法术等级",
    "new": "### 法术等级"
  }
  ```

### 6. [术语不一致] 存在位面 (the-planes-of-existence)
- 位置：index: the-planes-of-existence
- 问题描述：位面名称翻译与常用译名有差异
  - "Carceri" 翻译为"卡瑟利"（可接受）
  - "Pandemonium" 在 madness 中提及，翻译为"喧癫空隧"（但本文档未出现）
  - 某些外层位面名称未使用标准中文译名
- 建议修正：保持当前翻译，但建议统一位面名称术语表

### 7. [翻译准确性] 疯狂 (madness)
- 位置：index: madness
- 问题描述：状态效果翻译
  - "retreats into his or her own mind" 翻译为"退入自己的意识中"，可以更通顺
- 建议修正：
  ```json
  {
    "old": "角色退入自己的意识中，**失能**",
    "new": "角色退缩到自己的意识深处，陷入**失能**状态"
  }
  ```

### 8. [完整性检查] 标准兑换率 (standard-exchange-rates)
- 位置：index: standard-exchange-rates
- 问题描述：内容完整但格式可优化
  - 表格格式正确，但缺少表头与内容之间的分隔线说明
- 建议修正：无需修正，格式正确

## 修正建议汇总（JSON Patch 格式）

```json
[
  {
    "index": "using-each-ability",
    "changes": [
      {
        "path": "$.desc",
        "op": "replace",
        "old": "***杂技。*** 你的敏捷（杂技）检定",
        "new": "***体操。*** 你的敏捷（体操）检定"
      },
      {
        "path": "$.desc",
        "op": "replace",
        "old": "***手上功夫。*** 你的敏捷（手上功夫）检定",
        "new": "***巧手。*** 你的敏捷（巧手）检定"
      }
    ]
  },
  {
    "index": "time",
    "changes": [
      {
        "path": "$.desc",
        "op": "replace",
        "old": "急于到达森林中心孤独塔的冒险者 hurry across those fifteen miles in just under four hours' time。",
        "new": "急于到达森林中心孤独塔的冒险者在不到四小时的时间内赶完这十五英里。"
      }
    ]
  },
  {
    "index": "underwater-combat",
    "changes": [
      {
        "path": "$.desc",
        "op": "replace",
        "old": "或发现自己在 flooded dungeon room 中时",
        "new": "或发现自己身处被水淹没的地下城房间时"
      }
    ]
  },
  {
    "index": "what-is-a-spell",
    "changes": [
      {
        "path": "$.desc",
        "op": "replace",
        "old": "#### 法术等级",
        "new": "### 法术等级"
      }
    ]
  }
]
```

## 术语一致性检查摘要

### 核心游戏术语（检查通过）
| 英文 | 标准中文 | 使用情况 |
|-----|---------|---------|
| Ability Score | 属性值 | ✓ 正确使用 |
| Modifier | 调整值 | ✓ 正确使用 |
| Saving Throw | 豁免 | ✓ 正确使用 |
| Proficiency Bonus | 熟练加值 | ✓ 正确使用 |
| Advantage | 优势 | ✓ 正确使用 |
| Disadvantage | 劣势 | ✓ 正确使用 |
| Armor Class (AC) | AC | ✓ 正确使用 |
| Difficulty Class (DC) | DC | ✓ 正确使用 |
| Hit Points | 生命值 | ✓ 正确使用 |
| Hit Dice | 生命骰 | ✓ 正确使用 |
| Short Rest | 短休 | ✓ 正确使用 |
| Long Rest | 长休 | ✓ 正确使用 |
| Action | 动作 | ✓ 正确使用 |
| Bonus Action | 附赠动作 | ✓ 正确使用 |
| Reaction | 反应 | ✓ 正确使用 |
| Spell Slot | 法术位 | ✓ 正确使用 |
| Concentration | 专注 | ✓ 正确使用 |
| Cover | 掩护 | ✓ 正确使用 |

### 战斗术语（检查通过）
| 英文 | 中文 | 使用情况 |
|-----|------|---------|
| Attack | 攻击 | ✓ 正确使用 |
| Damage | 伤害 | ✓ 正确使用 |
| Critical Hit | 重击 | ✓ 正确使用（致命一击/重击）|
| Opportunity Attack | 借机攻击 | ✓ 正确使用 |

### 状态条件（检查通过）
| 英文 | 标准中文 | 使用情况 |
|-----|---------|---------|
| Blinded | 目盲 | ✓ 正确使用 |
| Charmed | 魅惑 | ✓ 正确使用 |
| Deafened | 耳聋 | ✓ 正确使用 |
| Exhaustion | 力竭/疲惫 | ✓ 正确使用 |
| Frightened | 恐慌 | ✓ 正确使用 |
| Grappled | 擒抱 | ✓ 正确使用 |
| Incapacitated | 失能 | ✓ 正确使用 |
| Invisible | 隐形 | ✓ 正确使用 |
| Paralyzed | 麻痹 | ✓ 正确使用 |
| Poisoned | 中毒 | ✓ 正确使用 |
| Prone | 倒地 | ✓ 正确使用 |
| Restrained | 束缚 | ✓ 正确使用 |
| Stunned | 震慑 | ✓ 正确使用 |
| Unconscious | 昏迷 | ✓ 正确使用 |

### 规则分段名称（检查通过）
| 英文 | 中文 | 使用情况 |
|-----|------|---------|
| The Order of Combat | 战斗流程 | ✓ 正确使用 |
| Fantasy-Historical Pantheons | 现实史传奇幻神系 | ✓ 正确使用 |

## 总体评价

### 翻译质量：良好

**优点：**
1. 术语一致性整体良好，核心游戏术语使用规范
2. Markdown 格式规范，标题层级清晰
3. 表格格式正确，对齐良好
4. 翻译准确，规则描述清晰易懂
5. 所有33个规则分段均已翻译，无遗漏

**需要改进：**
1. 技能译名需要与 GLOSSARY.md 保持一致
2. 存在少量英文未翻译的残留内容
3. 建议统一位面名称术语

### 严重程度分类
- **轻微**：问题5（格式）、问题7（措辞优化）
- **中等**：问题1（术语一致性）、问题2/3（翻译遗漏）
- **建议**：问题4（术语表补充）、问题6（位面名称统一）

---
*审查完成时间：2026-02-16 20:53:22*
*审查人：Kimi Code CLI*
