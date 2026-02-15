# D&D 5e SRD 翻译术语表

本项目用于记录 2014 版 SRD 的中英文对照翻译。

## 📁 文件说明

| 文件 | 说明 | 状态 |
|-----|------|-----|
| `core-abilities.json` | 核心属性术语（六大属性）| ✅ 已完成 |
| `core-skills.json` | 技能术语 | ✅ 已完成 |
| `core-alignments.json` | 阵营术语（九大阵营）| ✅ 已完成 |
| `core-conditions.json` | 状态/条件术语（15种）| ✅ 已完成 |
| `core-damage-types.json` | 伤害类型术语（13种）| ✅ 已完成 |
| `core-magic-schools.json` | 魔法学派术语（8种）| ✅ 已完成 |
| `core-languages.json` | 语言术语（16种）| ✅ 已完成 |
| `core-weapon-properties.json` | 武器属性术语（11种）| ✅ 已完成 |
| `core-subraces.json` | 亚种术语（4种）| ✅ 已完成 |
| `races-map.json` | 种族术语（9种族）| ✅ 已完成 |
| `classes-map.json` | 职业术语 | 📝 待翻译 |
| `races-map.json` | 种族术语 | 📝 待翻译 |
| `spells-map.json` | 法术术语 | 📝 待翻译 |
| `equipment-map.json` | 装备术语 | 📝 待翻译 |
| `monsters-map.json` | 怪物术语 | 📝 待翻译 |

## 📝 翻译原则

1. **index 和 url 字段**：永不翻译，保持原样（API 兼容性）
2. **name 字段**：`中文 (英文缩写)` 格式，如 `力量 (STR)`
3. **full_name 和 desc**：完整翻译为中文，同时保留 `full_name_en` 和 `desc_en`
4. **专业术语**：优先使用 D&D 官方/社区通用译名

## 📊 已翻译文件

| 源文件 | 中文文件 | 状态 |
|-------|---------|-----|
| `5e-SRD-Ability-Scores.json` | `5e-SRD-Ability-Scores.json` | ✅ 已完成 |
| `5e-SRD-Alignments.json` | `5e-SRD-Alignments.json` | ✅ 已完成 |
| `5e-SRD-Conditions.json` | `5e-SRD-Conditions.json` | ✅ 已完成 |
| `5e-SRD-Backgrounds.json` | `5e-SRD-Backgrounds.json` | ✅ 已完成 |
| `5e-SRD-Skills.json` | `5e-SRD-Skills.json` | ✅ 已完成 |
| `5e-SRD-Damage-Types.json` | `5e-SRD-Damage-Types.json` | ✅ 已完成 |
| `5e-SRD-Magic-Schools.json` | `5e-SRD-Magic-Schools.json` | ✅ 已完成 |
| `5e-SRD-Languages.json` | `5e-SRD-Languages.json` | ✅ 已完成 |
| `5e-SRD-Weapon-Properties.json` | `5e-SRD-Weapon-Properties.json` | ✅ 已完成 |
| `5e-SRD-Feats.json` | `5e-SRD-Feats.json` | ✅ 已完成 |
| `5e-SRD-Subraces.json` | `5e-SRD-Subraces.json` | ✅ 已完成 |
| `5e-SRD-Races.json` | `5e-SRD-Races.json` | ✅ 已完成 |

## 🔍 术语参考来源

- 主要参考：5E 不全书 (https://5echm.kagangtuya.top/)
- 社区通用译名
- D&D 5e 官方中文（如有）

## ✅ 技能译名对照表（来自 core-abilities.json）

| 英文 | 中文译名 | 所属属性 |
|-----|---------|---------|
| Athletics | 运动 | 力量 (STR) |
| Acrobatics | 体操 | 敏捷 (DEX) |
| Sleight of Hand | 巧手 | 敏捷 (DEX) |
| Stealth | 隐匿 | 敏捷 (DEX) |
| Arcana | 奥秘 | 智力 (INT) |
| History | 历史 | 智力 (INT) |
| Investigation | 调查 | 智力 (INT) |
| Nature | 自然 | 智力 (INT) |
| Religion | 宗教 | 智力 (INT) |
| Animal Handling | 驯兽 | 感知 (WIS) |
| Insight | 洞悉 | 感知 (WIS) |
| Medicine | 医药 | 感知 (WIS) |
| Perception | 察觉 | 感知 (WIS) |
| Survival | 生存 | 感知 (WIS) |
| Deception | 欺瞒 | 魅力 (CHA) |
| Intimidation | 威吓 | 魅力 (CHA) |
| Performance | 表演 | 魅力 (CHA) |
| Persuasion | 说服 | 魅力 (CHA) |

## ✅ 状态/条件术语表（来自 core-conditions.json）

| 英文 | 中文译名 | 效果简述 |
|-----|---------|---------|
| Blinded | 目盲 | 无法看见，攻击劣势 |
| Charmed | 魅惑 | 无法攻击魅惑者 |
| Deafened | 耳聋 | 无法听见 |
| Exhaustion | 力竭 | 分6级，逐渐削弱 |
| Frightened | 恐慌 | 无法靠近恐惧源 |
| Grappled | 擒抱 | 速度为0 |
| Incapacitated | 失能 | 无法执行动作 |
| Invisible | 隐形 | 攻击优势，被攻击劣势 |
| Paralyzed | 麻痹 | 无法行动，豁免自动失败 |
| Petrified | 石化 | 变为石头，伤害减半 |
| Poisoned | 中毒 | 攻击和检定劣势 |
| Prone | 倒地 | 只能爬行，攻击劣势 |
| Restrained | 束缚 | 速度为0，敏捷豁免劣势 |
| Stunned | 震慑 | 失能，豁免自动失败 |
| Unconscious | 昏迷 | 失能，倒地，5尺内命中即重击 |
