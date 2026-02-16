# 翻译审查报告：5e-SRD-Subclasses.json

## 审查摘要
- **审查结果**：需修改
- **总子职业数**：12
- **发现问题数**：1处轻微翻译不完整

---

### ✅ 正确翻译

| 原文 | 译文 | 所属职业 |
|------|------|----------|
| Berserker | 狂战士 | 野蛮人 (Barbarian) |
| Lore | 逸闻 | 吟游诗人 (Bard) |
| Life | 生命 | 牧师 (Cleric) |
| Land | 大地 | 德鲁伊 (Druid) |
| Champion | 勇士 | 战士 (Fighter) |
| Open Hand | 散打 | 武僧 (Monk) |
| Devotion | 奉献 | 圣武士 (Paladin) |
| Hunter | 猎手 | 游侠 (Ranger) |
| Thief | 盗贼 | 游荡者 (Rogue) |
| Draconic | 龙族 | 术士 (Sorcerer) |
| Fiend | 邪魔 | 邪术师 (Warlock) |
| Evocation | 塑能 | 法师 (Wizard) |

### 子职业类型翻译对照

| 原文 | 译文 |
|------|------|
| Primal Path | 原始道途 |
| Bard College | 吟游诗人学院 |
| Divine Domain | 神圣领域 |
| Druid Circle | 德鲁伊结社 |
| Martial Archetype | 武术范型 |
| Monastic Tradition | 修道传统 |
| Sacred Oath | 神圣誓约 |
| Ranger Archetype | 游侠范型 |
| Roguish Archetype | 游荡者范型 |
| Sorcerous Origin | 术士起源 |
| Otherworldly Patron | 异界宗主 |
| Arcane Tradition | 奥术传承 |

---

### ⚠️ 建议修改

| 原文 | 当前译文 | 建议译文 | 理由 |
|------|----------|----------|------|
| aspiring tyrants | aspiring 暴君 | 有抱负的暴君 / 觊觎者 | 塑能学派(Evocation)描述最后一句中"aspiring"为英文未翻译，需补充完整中文翻译 |

**具体位置**：`index: evocation` → `desc` 字段最后一句

**当前文本**：
> 一些塑能师在军队中任职，作为炮兵从远处轰击敌军。其他人则使用他们壮观的力量来保护弱者，而有些人则寻求自己的利益，成为强盗、冒险者或 aspiring 暴君。

**建议修改为**：
> 一些塑能师在军队中任职，作为炮兵从远处轰击敌军。其他人则使用他们壮观的力量来保护弱者，而有些人则寻求自己的利益，成为强盗、冒险者或**渴望权力的**暴君。

---

### ❌ 错误/遗漏

| 位置 | 问题描述 | 建议修复 |
|------|----------|----------|
| 无 | - | - |

---

### 📋 格式规范性检查

| 检查项 | 状态 |
|--------|------|
| `name` + `name_en` 格式 | ✅ 通过（所有12个子职业均符合） |
| `desc` + `desc_en` 格式 | ✅ 通过（所有12个子职业均符合） |
| `class.name` + `class.name_en` 格式 | ✅ 通过 |
| `subclass_flavor` 翻译 | ✅ 已翻译 |
| 数据结构完整性 | ✅ 通过 |

---

### 📝 详细审查说明

#### 1. 术语一致性
- 所有12个子职业名称与用户确认的译名完全一致
- 职业名称翻译统一：野蛮人、吟游诗人、牧师、德鲁伊、战士、武僧、圣武士、游侠、游荡者、术士、邪术师、法师

#### 2. 翻译准确性
- **整体评价**：翻译质量高，语义准确，表达流畅
- **亮点翻译**：
  - "Way of the Open Hand" → "散打之道"（简洁有力）
  - "College of Lore" 描述中的 "loyalty lies in the pursuit of beauty and truth" → "忠诚在于追求美与真理"
  - "Old Faith" → "古旧信仰"（符合D&D世界观传统译法）
  - 邪魔契约描述中的恶魔领主名称音译准确

#### 3. 完整性
- 源文件12个子职业，翻译文件12个子职业，无一遗漏
- 所有子职业的 `desc` 描述均已翻译
- 所有法术列表结构保持完整

---

### 🎯 审查结论

本次翻译整体质量优秀，仅需修复一处未翻译的英文单词"aspiring"。建议修正后通过审查。

**问题统计**：
- 严重错误：0
- 建议修改：1
- 格式问题：0
