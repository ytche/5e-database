# 翻译审查报告：5e-SRD-Traits.json

## 审查摘要
- **审查结果**：✅ 通过
- **总特性数**：38
- **发现问题**：0 个严重错误，0 个建议修改

---

## 详细审查结果

### 一、完整性检查 ✅

| 检查项 | 结果 |
|-------|------|
| 英文源文件特性总数 | 38 |
| 中文翻译文件特性总数 | 38 |
| 缺失条目 | 无 |
| 多余条目 | 无 |

### 二、格式规范性 ✅

所有特性均遵循标准格式：
- `name` + `name_en`：特性名称双语对照
- `desc` + `desc_en`：特性描述双语对照
- `races` 和 `subraces` 中的种族名称包含 `name` + `name_en`
- `proficiencies` 中的熟练项包含 `name` + `name_en`
- 嵌套引用（如法术、语言选项）均正确翻译并保留英文

### 三、术语一致性 ✅

#### 3.1 关键术语确认（用户已确认）

| 英文 | 确认译文 | 状态 |
|-----|---------|------|
| Draconic Ancestry | 龙族血统 | ✅ 正确 |
| Breath Weapon | 吐息武器 | ✅ 正确 |
| Fey Ancestry | 妖精血统 | ✅ 正确 |
| Trance | 出神 | ✅ 正确 |
| Gnome Cunning | 侏儒狡黠 | ✅ 正确 |
| Relentless Endurance | 坚韧不屈 | ✅ 正确 |
| Savage Attacks | 凶蛮攻击 | ✅ 正确 |
| Hellish Resistance | 炎狱抗性 | ✅ 正确 |
| Infernal Legacy | 地狱遗赠 | ✅ 正确 |
| Naturally Stealthy | 天生善匿 | ✅ 正确 |

#### 3.2 其他特性名称翻译

| 原文 | 译文 | 所属种族 | 状态 |
|-----|------|---------|------|
| Darkvision | 黑暗视觉 | 多个种族 | ✅ 正确 |
| Dwarven Resilience | 矮人韧性 | 矮人 | ✅ 正确 |
| Dwarven Combat Training | 矮人战斗训练 | 矮人 | ✅ 正确 |
| Tool Proficiency | 工具熟练 | 矮人 | ✅ 正确 |
| Stonecunning | 石中精妙 | 矮人 | ✅ 正确 |
| Dwarven Toughness | 矮人坚韧 | 丘陵矮人 | ✅ 正确 |
| Keen Senses | 敏锐感官 | 精灵 | ✅ 正确 |
| Elf Weapon Training | 精灵武器训练 | 高等精灵 | ✅ 正确 |
| High Elf Cantrip | 高等精灵戏法 | 高等精灵 | ✅ 正确 |
| Extra Language | 额外语言 | 高等精灵 | ✅ 正确 |
| Lucky | 幸运 | 半身人 | ✅ 正确 |
| Brave | 勇敢 | 半身人 | ✅ 正确 |
| Halfling Nimbleness | 半身人敏捷 | 半身人 | ✅ 正确 |
| Damage Resistance | 伤害抗性 | 龙裔 | ✅ 正确 |
| Artificer's Lore | 工匠学识 | 岩侏儒 | ✅ 正确 |
| Tinker | 修补匠 | 岩侏儒 | ✅ 正确 |
| Skill Versatility | 技能多样性 | 半精灵 | ✅ 正确 |
| Menacing | 威吓 | 半兽人 | ✅ 正确 |

### 四、翻译准确性 ✅

#### 4.1 ✅ 正确翻译示例

| 原文 | 译文 | 备注 |
|-----|------|------|
| You have superior vision in dark and dim conditions... | 你在黑暗和昏暗条件下拥有卓越的视力... | 黑暗视觉描述，准确 |
| You have advantage on saving throws against being charmed... | 你在对抗魅惑的豁免检定上具有优势... | 妖精血统描述，准确 |
| Elves do not need to sleep. Instead, they meditate deeply... | 精灵不需要睡眠。相反，他们会深度冥想... | 出神描述，准确 |
| When you roll a 1 on the d20... | 当你在攻击检定、能力检定或豁免检定的d20骰出1时... | 幸运描述，准确 |
| When you are reduced to 0 hit points but not killed outright... | 当你的生命值降至0但没有被直接杀死时... | 坚韧不屈描述，准确 |

#### 4.2 嵌套对象翻译检查

所有嵌套对象均正确翻译：
- `trait_specific.breath_weapon`：包含 `name`/`name_en` 和 `desc`/`desc_en`
- `trait_specific.damage_type`：伤害类型名称双语对照
- `proficiency_choices`：选项中的名称均双语对照
- `language_options`：语言选项名称双语对照
- `parent`：父特性引用双语对照

### 五、种族名称翻译一致性 ✅

| 英文 | 译文 | 状态 |
|-----|------|------|
| Dwarf | 矮人 | ✅ 正确 |
| Elf | 精灵 | ✅ 正确 |
| Gnome | 侏儒 | ✅ 正确 |
| Half-Elf | 半精灵 | ✅ 正确 |
| Half-Orc | 半兽人 | ✅ 正确 |
| Tiefling | 提夫林 | ✅ 正确 |
| Halfling | 半身人 | ✅ 正确 |
| Dragonborn | 龙裔 | ✅ 正确 |
| Hill Dwarf | 丘陵矮人 | ✅ 正确 |
| High Elf | 高等精灵 | ✅ 正确 |
| Lightfoot Halfling | 轻足半身人 | ✅ 正确 |
| Rock Gnome | 岩侏儒 | ✅ 正确 |

### 六、子特性（龙族血统变体）翻译 ✅

所有10种龙族血统变体均已正确翻译：

| 英文 | 译文 |
|-----|------|
| Draconic Ancestry (Black) | 龙族血统（黑龙）|
| Draconic Ancestry (Blue) | 龙族血统（蓝龙）|
| Draconic Ancestry (Brass) | 龙族血统（黄铜龙）|
| Draconic Ancestry (Bronze) | 龙族血统（青铜龙）|
| Draconic Ancestry (Copper) | 龙族血统（赤铜龙）|
| Draconic Ancestry (Gold) | 龙族血统（金龙）|
| Draconic Ancestry (Green) | 龙族血统（绿龙）|
| Draconic Ancestry (Red) | 龙族血统（红龙）|
| Draconic Ancestry (Silver) | 龙族血统（银龙）|
| Draconic Ancestry (White) | 龙族血统（白龙）|

### 七、伤害类型翻译一致性 ✅

| 英文 | 译文 |
|-----|------|
| Acid | 强酸 |
| Lightning | 闪电 |
| Fire | 火焰 |
| Poison | 毒素 |
| Cold | 冷冻 |

---

## 审查结论

### ✅ 正确翻译

全部38个特性翻译均正确，具体包括：

| 序号 | 特性索引 | 特性名称（中文） | 所属种族 |
|-----|---------|----------------|---------|
| 1 | darkvision | 黑暗视觉 | 通用 |
| 2 | dwarven-resilience | 矮人韧性 | 矮人 |
| 3 | dwarven-combat-training | 矮人战斗训练 | 矮人 |
| 4 | tool-proficiency | 工具熟练 | 矮人 |
| 5 | stonecunning | 石中精妙 | 矮人 |
| 6 | dwarven-toughness | 矮人坚韧 | 丘陵矮人 |
| 7 | keen-senses | 敏锐感官 | 精灵 |
| 8 | fey-ancestry | 妖精血统 | 精灵、半精灵 |
| 9 | trance | 出神 | 精灵 |
| 10 | elf-weapon-training | 精灵武器训练 | 高等精灵 |
| 11 | high-elf-cantrip | 高等精灵戏法 | 高等精灵 |
| 12 | extra-language | 额外语言 | 高等精灵 |
| 13 | lucky | 幸运 | 半身人 |
| 14 | brave | 勇敢 | 半身人 |
| 15 | halfling-nimbleness | 半身人敏捷 | 半身人 |
| 16 | naturally-stealthy | 天生善匿 | 轻足半身人 |
| 17 | draconic-ancestry | 龙族血统 | 龙裔 |
| 18-27 | draconic-ancestry-* | 龙族血统（各色龙） | 龙裔 |
| 28 | breath-weapon | 吐息武器 | 龙裔 |
| 29 | damage-resistance | 伤害抗性 | 龙裔 |
| 30 | gnome-cunning | 侏儒狡黠 | 侏儒 |
| 31 | artificers-lore | 工匠学识 | 岩侏儒 |
| 32 | tinker | 修补匠 | 岩侏儒 |
| 33 | skill-versatility | 技能多样性 | 半精灵 |
| 34 | menacing | 威吓 | 半兽人 |
| 35 | relentless-endurance | 坚韧不屈 | 半兽人 |
| 36 | savage-attacks | 凶蛮攻击 | 半兽人 |
| 37 | hellish-resistance | 炎狱抗性 | 提夫林 |
| 38 | infernal-legacy | 地狱遗赠 | 提夫林 |

### ⚠️ 建议修改

无。

### ❌ 错误/遗漏

无。

---

## 总结

本次审查覆盖了《5e-SRD-Traits.json》全部38个种族特性翻译。经详细比对：

1. **完整性**：✅ 所有特性均已翻译，无遗漏
2. **格式规范**：✅ 严格遵循 `name`/`name_en`、`desc`/`desc_en` 双语格式
3. **术语一致**：✅ 关键术语翻译与用户确认的标准一致
4. **翻译准确**：✅ 描述内容翻译准确，无错译漏译

**审查结果：通过** ✅

---

*审查时间：2026-02-16*  
*审查员：AI Translation Reviewer*
