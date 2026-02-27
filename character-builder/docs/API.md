# D&D 5e 角色构建器 - API 文档

> 📝 本文档用于记录车卡小程序的接口定义
> - 创建时间：2026-02-27
> - 状态：收集中

---

## 📑 目录

- [接口概览](#接口概览)
- [数据接口](#数据接口)
- [角色接口](#角色接口)
- [扩展包接口](#扩展包接口)
- [错误码](#错误码)

---

## 接口概览

### Base URL

```
本地开发：http://localhost:3000/api
生产环境：https://api.dnd5e-builder.com/api
```

### 通用响应格式

```typescript
interface ApiResponse<T> {
  code: number;       // 业务状态码
  message: string;    // 提示信息
  data: T;           // 响应数据
}

interface ApiError {
  code: number;       // 错误码
  message: string;    // 错误信息
  details?: string;   // 详细错误（开发环境）
}
```

---

## 数据接口

### 获取规则版本列表

获取支持的 D&D 规则版本列表。

```http
GET /data/versions
```

**请求参数**：无

**响应示例**：

```json
{
  "code": 0,
  "message": "success",
  "data": {
    "versions": [
      {
        "id": "5e-2014",
        "name": "5E (2014)",
        "description": "D&D 第五版 2014 规则",
        "available": true
      },
      {
        "id": "5r-2024",
        "name": "5R (2024)",
        "description": "D&D 第五版 2024 规则",
        "available": false
      }
    ]
  }
}
```

---

### 获取扩展规则书列表

获取指定规则版本支持的扩展规则书列表。

```http
GET /data/extensions
```

**请求参数**：

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| version | string | 是 | 规则版本 ID，如 `5e-2014` |

**响应示例**：

```json
{
  "code": 0,
  "message": "success",
  "data": {
    "extensions": [
      {
        "id": "phb",
        "name": "玩家手册",
        "nameEn": "Player's Handbook",
        "code": "PHB",
        "required": true,
        "description": "核心规则书，包含基础种族、职业、法术等"
      },
      {
        "id": "xge",
        "name": "珊娜萨的万事指南",
        "nameEn": "Xanathar's Guide to Everything",
        "code": "XGE",
        "required": false,
        "description": "扩展职业选项、法术、子职业等"
      }
    ]
  }
}
```

---

### 获取种族列表

获取指定规则配置下的可用种族列表，包含完整的种族信息、亚种和特性数据。

```http
GET /data/races
```

**请求参数**：

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| version | string | 是 | 规则版本 ID，如 `5e-2014` |
| extensions | string[] | 否 | 启用的扩展规则书 ID 列表 |

**响应数据结构**：

```typescript
interface RaceData {
  index: string;           // 种族唯一标识
  name: string;            // 中文名称
  nameEn: string;          // 英文名称
  icon: string;            // 图标URL或emoji
  speed: number;           // 基础移速（英尺）
  size: string;            // 体型代码：Small/Medium/Large
  sizeLabel: string;       // 体型显示文本：小型/中型/大型
  age: string;             // 年龄描述文本
  abilityBonuses: AbilityBonus[];  // 种族属性加成
  languages: LanguageInfo; // 语言信息
  subraces: Subrace[];     // 亚种列表
  traits: Trait[];         // 种族特性列表
  source: Source;          // 来源规则书
}

interface LanguageInfo {
  fixed: Language[];       // 固定语言列表（必选，不可更改）
  optional: Language[];    // 可选语言列表
  optionalCount: number;   // 需要从可选语言中选择的数量（通常为1）
}

interface Language {
  index: string;           // 语言代码：common/elvish/dwarvish 等
  name: string;            // 语言中文名
  nameEn: string;          // 语言英文名
}

interface AbilityBonus {
  ability: string;         // 属性代码：str/dex/con/int/wis/cha
  abilityName: string;     // 属性中文名
  bonus: number;           // 加成数值
}

interface Subrace {
  index: string;           // 亚种唯一标识
  name: string;            // 亚种中文名称
  description: string;     // 亚种描述文本
  abilityBonuses: AbilityBonus[];  // 亚种额外属性加成
}

interface Trait {
  index: string;           // 特性唯一标识
  name: string;            // 特性名称
  description: string;     // 特性描述
  optional: boolean;       // 是否为可选特性
  options?: TraitOption[]; // 可选特性的选项列表
}

interface TraitOption {
  index: string;           // 选项标识
  name: string;            // 选项名称
  description: string;     // 选项描述
}
```

**响应示例**：

```json
{
  "code": 0,
  "message": "success",
  "data": {
    "races": [
      {
        "index": "elf",
        "name": "精灵",
        "nameEn": "Elf",
        "icon": "🧝",
        "speed": 30,
        "size": "Medium",
        "sizeLabel": "中型",
        "age": "精灵的成熟速度与人类相同，但在100岁之前都被认为是年轻人。平均而言，他们能活大约750年。",
        "abilityBonuses": [
          { "ability": "dex", "abilityName": "敏捷", "bonus": 2 }
        ],
        "languages": {
          "fixed": [
            { "index": "common", "name": "通用语", "nameEn": "Common" },
            { "index": "elvish", "name": "精灵语", "nameEn": "Elvish" }
          ],
          "optional": [
            { "index": "dwarvish", "name": "矮人语", "nameEn": "Dwarvish" },
            { "index": "orc", "name": "兽人语", "nameEn": "Orc" },
            { "index": "giant", "name": "巨人语", "nameEn": "Giant" },
            { "index": "draconic", "name": "龙语", "nameEn": "Draconic" }
          ],
          "optionalCount": 1
        },
        "subraces": [
          {
            "index": "high-elf",
            "name": "高等精灵",
            "description": "高等精灵是学识渊博的精灵，他们研究奥术魔法，精通剑术与魔法。",
            "abilityBonuses": [
              { "ability": "int", "abilityName": "智力", "bonus": 1 }
            ]
          },
          {
            "index": "wood-elf",
            "name": "木精灵",
            "description": "木精灵是林地的守护者，他们与自然界紧密相连，是出色的猎人和追踪者。",
            "abilityBonuses": [
              { "ability": "wis", "abilityName": "感知", "bonus": 1 }
            ]
          },
          {
            "index": "drow",
            "name": "卓尔",
            "description": "卓尔是居住在幽暗地域的黑暗精灵，他们适应了地底的黑暗环境。",
            "abilityBonuses": [
              { "ability": "cha", "abilityName": "魅力", "bonus": 1 }
            ]
          }
        ],
        "traits": [
          {
            "index": "darkvision",
            "name": "黑暗视觉",
            "description": "在微光光照下，身边60尺内可以视为等同于明亮光照。在黑暗中，该范围内可以视为等同于微光光照。",
            "optional": false
          },
          {
            "index": "fey-ancestry",
            "name": "精类血统",
            "description": "你进行对抗魅惑的豁免时具有优势，并且不会因魔法效应而陷入睡眠。",
            "optional": false
          },
          {
            "index": "trance",
            "name": "出神",
            "description": "精灵不需要睡眠，而是会以半清醒冥想的方式度过4小时。",
            "optional": false
          },
          {
            "index": "elf-weapon-training",
            "name": "精灵武器训练",
            "description": "你熟练使用长剑、短剑、短弓和长弓中的一种。",
            "optional": true,
            "options": [
              { "index": "longsword", "name": "长剑", "description": "熟练使用长剑" },
              { "index": "shortsword", "name": "短剑", "description": "熟练使用短剑" },
              { "index": "shortbow", "name": "短弓", "description": "熟练使用短弓" },
              { "index": "longbow", "name": "长弓", "description": "熟练使用长弓" }
            ]
          }
        ],
        "source": {
          "id": "phb",
          "name": "玩家手册"
        }
      }
    ]
  }
}
```

---

### 获取职业列表

获取指定规则配置下的可用职业列表，包含完整的职业信息、子职业、熟练项和特性数据。

```http
GET /data/classes
```

**请求参数**：

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| version | string | 是 | 规则版本 ID，如 `5e-2014` |
| extensions | string[] | 否 | 启用的扩展规则书 ID 列表 |

**响应数据结构**：

```typescript
interface ClassData {
  index: string;           // 职业唯一标识
  name: string;            // 中文名称
  nameEn: string;          // 英文名称
  icon: string;            // 图标URL或emoji
  hitDice: number;         // 生命骰面数（如 8 代表 d8）
  hpAtFirstLevel: string;  // 第一级生命值，如 "8 + 体质调整值"
  hpAtHigherLevels: string; // 后续升级生命值，如 "5 (1d8) + 体质调整值"
  proficiencies: {         // 熟练项信息
    savingThrows: SavingThrowProficiency[];  // 熟练豁免（通常是2个固定）
    skills: SkillProficiency;                // 技能熟练
    armor?: string[];      // 熟练护甲列表
    weapons?: string[];    // 熟练武器列表
    tools?: ToolProficiency; // 熟练工具（可选）
  };
  startingEquipment: EquipmentOption[]; // 起始装备选项列表
  choices: ClassChoice[];  // 1级抉择项列表（0个或多个）
  spellcasting?: SpellcastingInfo;  // 施法信息（施法职业）
  source: Source;          // 来源规则书
}

interface ToolProficiency {
  options: ToolOption[];   // 可选工具列表
  choose: number;          // 需要选择的工具数量
}

interface ToolOption {
  index: string;           // 工具代码
  name: string;            // 工具中文名
}

interface EquipmentOption {
  index: string;           // 装备选项ID
  description?: string;    // 直接描述（如"一把轻十字弩和20发弩箭"）
  options?: EquipmentChoice[]; // 或提供选择列表
  choose?: number;         // 需要选择的数量（默认为1）
}

interface EquipmentChoice {
  index: string;
  name: string;            // 选项名称
  description: string;     // 选项描述
}

interface ClassChoice {
  index: string;           // 抉择项唯一标识
  name: string;            // 抉择项名称：如"领域"、"战斗风格"、"魔契恩泽"
  cardTitle: string;       // 卡片标题："XX选择"，如"领域选择"、"战斗风格选择"
  description?: string;    // 抉择项描述说明
  options: ChoiceOption[]; // 选项列表
}

interface ChoiceOption {
  index: string;           // 选项唯一标识
  name: string;            // 选项名称
  description: string;     // 选项描述
}

interface SavingThrowProficiency {
  ability: string;         // 属性代码：str/dex/con/int/wis/cha
  abilityName: string;     // 属性中文名
}

interface SkillProficiency {
  options: SkillOption[];  // 可选技能列表
  choose: number;          // 需要选择的技能数量
}

interface SkillOption {
  index: string;           // 技能代码
  name: string;            // 技能中文名
  ability: string;         // 关联属性
}

interface SpellcastingInfo {
  ability: string;         // 施法关键属性：int/wis/cha
  abilityName: string;     // 属性中文名
  cantripsKnown: number;   // 已知戏法数量（1级）
  spellsKnown?: number;    // 已知法术数量（1级，法师等为null）
  spellSlotsLevel1: number; // 1级法术位数量
}
```

**响应示例**：

```json
{
  "code": 0,
  "message": "success",
  "data": {
    "classes": [
      {
        "index": "wizard",
        "name": "法师",
        "nameEn": "Wizard",
        "icon": "🧙",
        "hitDice": 6,
        "hpAtFirstLevel": "6 + 体质调整值",
        "hpAtHigherLevels": "4 (1d6) + 体质调整值",
        "proficiencies": {
          "savingThrows": [
            { "ability": "int", "abilityName": "智力" },
            { "ability": "wis", "abilityName": "感知" }
          ],
          "skills": {
            "options": [
              { "index": "arcana", "name": "奥秘", "ability": "int" },
              { "index": "history", "name": "历史", "ability": "int" },
              { "index": "insight", "name": "洞悉", "ability": "wis" },
              { "index": "investigation", "name": "调查", "ability": "int" },
              { "index": "nature", "name": "自然", "ability": "int" },
              { "index": "religion", "name": "宗教", "ability": "int" }
            ],
            "choose": 2
          },
          "armor": [],
          "weapons": ["匕首", "飞镖", "轻十字弩", "长棍"]
        },
        "startingEquipment": [
          {
            "index": "weapon",
            "description": "一把轻十字弩和20发弩箭"
          },
          {
            "index": "simple-weapon",
            "options": [
              { "index": "quarterstaff", "name": "长棍", "description": "一把长棍" },
              { "index": "dagger", "name": "匕首", "description": "一把匕首" }
            ],
            "choose": 1
          },
          {
            "index": "explorer-pack",
            "options": [
              { "index": "scholar-pack", "name": "学者套组", "description": "包含书籍、墨水、墨水笔和小刀" },
              { "index": "explorer-pack", "name": "探险家套组", "description": "包含背包、睡袋、野炊用具和口粮" }
            ],
            "choose": 1
          }
        ],
        "spellcasting": {
          "ability": "int",
          "abilityName": "智力",
          "cantripsKnown": 3,
          "spellsKnown": null,
          "spellSlotsLevel1": 2
        },
        "choices": [],
        "source": {
          "id": "phb",
          "name": "玩家手册"
        }
      },
      {
        "index": "cleric",
        "name": "牧师",
        "nameEn": "Cleric",
        "icon": "✝️",
        "hitDice": 8,
        "proficiencies": {
          "savingThrows": [
            { "ability": "wis", "abilityName": "感知" },
            { "ability": "cha", "abilityName": "魅力" }
          ],
          "skills": {
            "options": [
              { "index": "history", "name": "历史", "ability": "int" },
              { "index": "insight", "name": "洞悉", "ability": "wis" },
              { "index": "medicine", "name": "医药", "ability": "wis" },
              { "index": "persuasion", "name": "游说", "ability": "cha" },
              { "index": "religion", "name": "宗教", "ability": "int" }
            ],
            "choose": 2
          },
          "armor": ["轻甲", "中甲", "盾牌"],
          "weapons": ["简易武器"]
        },
        "choices": [
          {
            "index": "divine-domain",
            "name": "领域",
            "cardTitle": "领域选择",
            "description": "1级时选择你的神圣领域，获得领域特性和领域法术。",
            "options": [
              { "index": "knowledge", "name": "知识领域", "description": "追求真理与知识，掌握更多技能与法术。" },
              { "index": "life", "name": "生命领域", "description": "专注于治疗与保护，是队伍中的坚实后盾。" },
              { "index": "light", "name": "光明领域", "description": "掌控光明与火焰之力，驱散黑暗与邪恶。" },
              { "index": "nature", "name": "自然领域", "description": "亲近自然，获得德鲁伊般的自然之力。" },
              { "index": "tempest", "name": "风暴领域", "description": "驾驭风暴与雷电之力，威力强大。" },
              { "index": "trickery", "name": "诡术领域", "description": "掌握幻术与欺骗，善于诡诈与隐匿。" },
              { "index": "war", "name": "战争领域", "description": "精通战斗，在前线挥舞武器与信仰。" }
            ]
          }
        ],
        "startingEquipment": [
          {
            "index": "weapon",
            "options": [
              { "index": "mace", "name": "钉头锤", "description": "一把钉头锤" },
              { "index": "warhammer", "name": "战锤", "description": "一把战锤（如熟练）" }
            ],
            "choose": 1
          },
          {
            "index": "armor",
            "options": [
              { "index": "scale-mail", "name": "鳞甲", "description": "一套鳞甲" },
              { "index": "leather", "name": "皮甲", "description": "一套皮甲" },
              { "index": "chain-mail", "name": "链甲", "description": "一套链甲（如熟练）" }
            ],
            "choose": 1
          },
          {
            "index": "pack",
            "options": [
              { "index": "priest-pack", "name": "牧师套组", "description": "包含背包、毛毯、蜡烛和口粮" },
              { "index": "explorer-pack", "name": "探险家套组", "description": "包含背包、睡袋、野炊用具和口粮" }
            ],
            "choose": 1
          }
        ],
        "spellcasting": {
          "ability": "wis",
          "abilityName": "感知",
          "cantripsKnown": 3,
          "spellsKnown": null,
          "spellSlotsLevel1": 2
        },
        "source": {
          "id": "phb",
          "name": "玩家手册"
        }
      }
    ]
  }
}
```

**说明**：
- **法师**：`choices` 为空数组（1级无抉择），3级时才选择学派
- **牧师**：`choices` 包含1个抉择项（领域选择），1级时必须选择
- **战士**：`choices` 包含1个抉择项（战斗风格选择），1级时必须选择

**战士示例（有战斗风格选择）**：

```json
{
  "index": "fighter",
  "name": "战士",
  "nameEn": "Fighter",
  "icon": "⚔️",
  "hitDice": 10,
  "proficiencies": {
    "savingThrows": [
      { "ability": "str", "abilityName": "力量" },
      { "ability": "con", "abilityName": "体质" }
    ],
    "skills": {
      "options": [
        { "index": "acrobatics", "name": "杂技", "ability": "dex" },
        { "index": "animal-handling", "name": "驯兽", "ability": "wis" },
        { "index": "athletics", "name": "运动", "ability": "str" },
        { "index": "history", "name": "历史", "ability": "int" },
        { "index": "insight", "name": "洞悉", "ability": "wis" },
        { "index": "intimidation", "name": "威吓", "ability": "cha" },
        { "index": "perception", "name": "察觉", "ability": "wis" },
        { "index": "survival", "name": "生存", "ability": "wis" }
      ],
      "choose": 2
    },
    "armor": ["轻甲", "中甲", "重甲", "盾牌"],
    "weapons": ["简易武器", "军用武器"]
  },
  "choices": [
    {
      "index": "fighting-style",
      "name": "战斗风格",
      "cardTitle": "战斗风格选择",
      "description": "1级时你选择一种战斗风格作为专精。",
      "options": [
        { "index": "archery", "name": "箭术", "description": "使用远程武器进行攻击时，攻击检定+2。" },
        { "index": "defense", "name": "防御", "description": "身着护甲时，AC+1。" },
        { "index": "dueling", "name": "对决", "description": "单手持用近战武器且未持用其他武器时，该武器伤害+2。" },
        { "index": "great-weapon-fighting", "name": "双武器战斗", "description": "双手持用近战武器进行攻击时，若伤害骰掷出1或2，可以重掷。" },
        { "index": "protection", "name": "守护", "description": "持用盾牌时，可以阻碍攻击你5尺内目标的攻击者，使其攻击检定具有劣势。" },
        { "index": "two-weapon-fighting", "name": "双持武器战斗", "description": "进行双持武器战斗时，可以将能力调整值加到第二次攻击的伤害上。" }
      ]
    }
  ],
  "features": [
    {
      "index": "fighting-style",
      "name": "战斗风格",
      "description": "你 adopting 一种特定的战斗风格作为你的专长。",
      "level": 1,
      "optional": false
    },
    {
      "index": "second-wind",
      "name": "回气",
      "description": "你可以用一个 bonus action 恢复1d10+战士等级的生命值。短休或长休后恢复使用次数。",
      "level": 1,
      "optional": false
    }
  ],
  "source": {
    "id": "phb",
    "name": "玩家手册"
  }
}
```

---

## 角色接口

### 创建角色

创建新角色，进入角色创建流程。

```http
POST /characters
```

**请求参数**：

```json
{
  "version": "5e-2014",
  "extensions": ["phb"]
}
```

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| version | string | 是 | 规则版本 ID |
| extensions | string[] | 是 | 启用的扩展规则书 ID 列表 |

**响应示例**：待补充

---

### 保存角色进度

保存角色创建过程中的进度。

```http
PUT /characters/:id/progress
```

**请求参数**：待补充

---

### 获取角色详情

获取角色的完整信息。

```http
GET /characters/:id
```

**请求参数**：无

**响应示例**：待补充

---

### 获取角色列表

获取用户的角色列表。

```http
GET /characters
```

**请求参数**：

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| status | string | 否 | 筛选状态：draft/completed/all |
| page | number | 否 | 页码，默认 1 |
| pageSize | number | 否 | 每页数量，默认 20 |

**响应示例**：待补充

---

### 删除角色

删除指定角色。

```http
DELETE /characters/:id
```

**请求参数**：无

---

## 扩展包接口

### 获取扩展包列表

获取可用的扩展包列表及下载状态。

```http
GET /packages
```

**请求参数**：无

**响应示例**：待补充

---

### 下载扩展包

下载指定的扩展包数据。

```http
POST /packages/:id/download
```

**请求参数**：无

---

## 错误码

| 错误码 | 说明 |
|--------|------|
| 0 | 成功 |
| 400 | 请求参数错误 |
| 401 | 未授权 |
| 404 | 资源不存在 |
| 500 | 服务器内部错误 |

---

## 📝 变更日志

| 日期 | 变更内容 | 记录人 |
|------|----------|--------|
| 2026-02-27 | 创建文档框架，定义数据接口基础结构 | Kimi |

---

> 💡 **如何使用本文档**
> 1. 讨论中提到的接口会整理到这里
> 2. 每个接口包含：URL、请求参数、响应格式
> 3. 最终会形成完整的 API 文档供开发使用
