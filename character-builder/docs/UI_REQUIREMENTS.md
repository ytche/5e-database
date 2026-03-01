# D&D 5e 车卡小程序 - 页面功能需求文档

> 📝 本文档用于记录和整理车卡小程序的页面功能需求
> - 创建时间：2026-02-27
> - 最后更新：2026-02-27
> - 状态：步骤1-8设计完成

---

## 📱 页面概览

### 主流程页面

| 页面 | 路径 | 状态 | 描述 |
|------|------|------|------|
| 首页/入口 | `/index` | ✅ 已定义 | 小程序入口页面 |
| 角色创建 | `/builder` | ✅ 已定义 | 创建/编辑角色流程（8步骤） |

### 角色创建流程（8步骤）

| 步骤 | 页面 | 路径 | 状态 | 描述 |
|------|------|------|------|------|
| 1 | 战役设置 | `/builder/campaign` | ✅ 已定义 | 选择规则和扩展书 |
| 2 | 选择种族 | `/builder/race` | ✅ 已定义 | 选择种族和亚种 |
| 3 | 选择职业 | `/builder/class` | ✅ 已定义 | 选择职业、装备和抉择项 |
| 4 | 分配属性 | `/builder/abilities` | ✅ 已定义 | 购点法分配属性 |
| 5 | 选择背景 | `/builder/background` | ✅ 已定义 | 选择背景、阵营 |
| 6 | 选择法术 | `/builder/spells` | ✅ 已定义 | 施法者选择法术 |
| 7 | 起始装备 | `/builder/equipment` | ✅ 已定义 | 确认装备，完成选择 |
| 8 | 确认角色 | `/builder/review` | ✅ 已定义 | 预览并确认完成 |

### 其他页面（待定义）

| 页面 | 路径 | 状态 | 描述 |
|------|------|------|------|
| 角色列表 | `/characters` | 📝 待定义 | 管理已创建的角色 |
| 角色详情 | `/character/:id` | 📝 待定义 | 查看已完成的角色卡 |
| 我的 | `/profile` | 📝 待定义 | 个人中心 |
| 设置 | `/settings` | 📝 待定义 | 小程序设置 |
| 规则查询 | `/rules` | 📝 待定义 | 规则信息查询（暂不实现） |

---

## 📋 全局规范

### 视觉风格：卡片式

整个小程序采用**卡片式（Card-based）**设计风格，所有内容区块以卡片形式呈现。

**卡片规范**：

| 属性 | 规范 |
|------|------|
| 背景 | 白色或浅灰色卡片，页面背景为浅灰/米白 #f5f5f5 |
| 圆角 | 12px - 16px |
| 阴影 | 轻微阴影或无边框线分割 |
| 间距 | 卡片之间 12px - 16px 间距 |
| 内边距 | 卡片内部 16px 内边距 |

**卡片层级**：

```
┌─────────────────────────┐  ← 页面（浅灰背景）
│  ┌─────────────────┐    │
│  │                 │    │  ← 卡片1（白底圆角）
│  │                 │    │
│  └─────────────────┘    │
│                         │
│  ┌─────────────────┐    │
│  │                 │    │  ← 卡片2（白底圆角）
│  │                 │    │
│  └─────────────────┘    │
│                         │
│  ┌─────────────────┐    │
│  │  🏠 首页 👤 我的 │    │  ← Tab导航卡片
│  └─────────────────┘    │
└─────────────────────────┘
```

### 底部 Tab 导航

所有页面底部固定显示 Tab 导航栏，以卡片形式呈现：

| Tab | 图标 | 页面 | 说明 |
|-----|------|------|------|
| 首页 | 🏠 | `/index` | 小程序主页 |
| 我的 | 👤 | `/profile` | 个人中心 |

**规则**：
- 所有页面底部都必须包含 Tab 导航卡片
- 当前所在 Tab 高亮显示
- 点击切换时保留页面状态（不刷新）

### 步骤导航样式

角色创建流程顶部固定显示步骤指示器：

- 当前步骤高亮，已完成步骤可点击返回
- 未开始步骤置灰不可点击
- 格式：`步骤 1/8  战役设置`

---

## 📋 功能需求清单

### 1. 首页/入口页面 (`/index`)

**第一版（MVP）**
| 功能项 | 描述 | 优先级 | 状态 |
|--------|------|--------|------|
| 创建新角色 | 主按钮：开始创建新角色 | P0 | ✅ 已定义 |

**页面布局**：

```
┌─────────────────────────┐  ← 浅灰背景 #f5f5f5
│                         │
│   ┌─────────────────┐   │
│   │  [Logo/标题]     │   │  ← Logo区域
│   │ D&D 5e角色构建器 │   │
│   └─────────────────┘   │
│                         │
│   ┌─────────────────┐   │
│   │ [ + 创建新角色 ] │   │  ← 主按钮
│   └─────────────────┘   │
│                         │
│   ┌─────────────────┐   │
│   │ © Wizards of    │   │  ← 版权声明
│   │   the Coast     │   │
│   │ Open Game       │   │
│   │   License v1.0  │   │
│   └─────────────────┘   │
│                         │
│   ┌─────────────────┐   │
│   │  🏠 首页 👤 我的 │   │  ← Tab导航
│   └─────────────────┘   │
└─────────────────────────┘
```

---

### 2. 角色创建流程 (`/builder`)

#### 步骤 1：战役设置 (`/builder/campaign`)

**页面说明**：开始创建角色前，配置当前战役的规则版本和启用的扩展规则书。

**API 数据格式**：

```typescript
interface CampaignData {
  version: string;              // 规则版本，如 "5e-2014"
  extensions: string[];         // 启用的扩展书，如 ["phb", "xge"]
}

interface VersionInfo {
  index: string;
  name: string;                 // 如 "5E (2014)"
  description: string;
  available: boolean;           // 是否可用
}

interface ExtensionInfo {
  index: string;
  code: string;                 // 如 "PHB"
  name: string;                 // 如 "玩家手册"
  description: string;
  defaultEnabled: boolean;      // 是否默认启用
  required?: boolean;           // 是否必选
}
```

**页面布局**：

```
┌─────────────────────────┐
│  ←  步骤 1/8  战役设置   │
├─────────────────────────┤
│ ⚠️ 与 DM 确认           │
│ 请与地下城主确认规则    │
│ 和扩展书                │
├─────────────────────────┤
│ 📋 规则版本              │
│  ● 5E (2014)            │
│  ⚪ 5R (2024) [暂未开放] │
├─────────────────────────┤
│ 📚 扩展规则书            │
│  ☑ 玩家手册 [必选]      │
│  ─────────────────      │
│  ☐ DM指南               │
│  ☐ 珊娜萨指南           │
│  ☐ 塔莎坩埚             │
├─────────────────────────┤
│    [  下一步  ]         │
└─────────────────────────┘
```

---

#### 步骤 2：选择种族 (`/builder/race`)

**API 数据格式**：

```typescript
interface RaceData {
  index: string;
  name: string;                 // 中文名
  nameEn: string;               // 英文名
  icon: string;
  abilityBonuses: AbilityBonus[];
  speed: number;                // 速度（英尺）
  size: string;                 // 体型代码
  sizeLabel: string;            // 体型显示文本
  age: string;                  // 年龄描述
  languages: {
    fixed: Language[];          // 固定语言
    optional: Language[];       // 可选语言
    optionalCount: number;      // 可选数量
  };
  subraces: Subrace[];          // 亚种列表
  traits: Trait[];              // 种族特性
}

interface Subrace {
  index: string;
  name: string;
  description: string;
  abilityBonuses: AbilityBonus[];
}

interface Trait {
  index: string;
  name: string;
  description: string;
  optional: boolean;
  options?: TraitOption[];
}
```

**页面布局**：

```
┌─────────────────────────┐
│  ←  步骤 2/8  选择种族   │
├─────────────────────────┤
│ 🧝 精灵 Elf ▼           │  ← 下拉选择
├─────────────────────────┤
│ 📋 选择亚种             │
│  ○ 高等精灵 智力+1      │
│  ● 木精灵    感知+1     │
│  ○ 卓尔      魅力+1     │
├─────────────────────────┤
│ 📋 基础信息             │
│  年龄: ┌─────┐          │
│        │  25  │          │
│        └─────┘          │
│  精灵的成熟速度...      │
│  体型: 中型             │
│  速度: 30尺             │
│  语言: ☑通用语 ☑精灵语  │
│  额外语言(选1): ○矮人语 │
│                ●兽人语  │
├─────────────────────────┤
│ ✨ 种族特性             │
│ ┌─────────────────┐     │
│ │ 黑暗视觉        │     │
│ │ 在微光黑暗中视物│     │
│ └─────────────────┘     │
│ ┌─────────────────┐     │
│ │ 精灵武器训练    │     │
│ │ ○长剑 ○短剑 ●长弓│     │
│ └─────────────────┘     │
├─────────────────────────┤
│    [  下一步  ]         │
└─────────────────────────┘
```

---

#### 步骤 3：选择职业 (`/builder/class`)

**API 数据格式**：

```typescript
interface ClassData {
  index: string;
  name: string;
  nameEn: string;
  icon: string;
  hitDice: number;              // 生命骰（如 8 代表 d8）
  hpAtFirstLevel: string;       // "8 + 体质调整值"
  hpAtHigherLevels: string;     // "5 (1d8) + 体质调整值"
  proficiencies: {
    savingThrows: {
      options: SavingThrowOption[];
      choose: number;
    };
    skills: {
      options: SkillOption[];
      choose: number;
    };
    armor?: string[];
    weapons?: string[];
    tools?: {
      options: ToolOption[];
      choose: number;
    };
  };
  startingEquipment: EquipmentOption[];
  choices: ClassChoice[];       // 1级抉择项
  spellcasting?: SpellcastingInfo;
}

interface ClassChoice {
  index: string;
  name: string;
  cardTitle: string;            // 卡片标题
  description?: string;
  options: ChoiceOption[];
}

interface SpellcastingInfo {
  ability: string;              // int/wis/cha
  cantripsKnown: number;
  spellSlots: number;
  spellSelection: {
    type: 'known' | 'prepared' | 'spellbook';
    spellbookSize?: number;
    maxPrepared?: number;
  };
}
```

**页面布局**：

```
┌─────────────────────────┐
│  ←  步骤 3/8  选择职业   │
├─────────────────────────┤
│ 🧙 法师 Mage ▼          │  ← 下拉选择
├─────────────────────────┤
│ ❤️ 生命值               │
│  生命骰: 1d6            │
│  第一级: 6+体质调整值   │
│  后续升级: 4(1d6)+体质调整值│
├─────────────────────────┤
│ 🛡️ 熟练项目             │
│  护甲: 无               │
│  武器: 匕首 飞镖 轻十字弩│
│  工具: 多选标签         │
│  豁免: ☑智力 ☑感知      │
│  技能(选2): 多选标签    │
├─────────────────────────┤
│ 🎒 起始装备             │
│  ① 轻十字弩和20发弩箭   │
│  ② 选择1个: ●短棍 ○匕首 │
│  ③ 选择1个: ●学者套组   │
│             ○探险家套组 │
├─────────────────────────┤
│ 📋 领域选择             │  ← 抉择卡片（动态）
│  ● 生命领域             │
│  ○ 光明领域             │
├─────────────────────────┤
│    [  下一步  ]         │
└─────────────────────────┘
```

---

#### 步骤 4：分配属性 (`/builder/abilities`)

**API 数据格式**：

```typescript
interface AbilitiesData {
  method: 'point-buy' | 'dice-roll';  // 分配方式
  points: number;                     // 剩余点数（购点法）
  scores: {                           // 当前属性值
    str: number;
    dex: number;
    con: number;
    int: number;
    wis: number;
    cha: number;
  };
  racialBonuses: {                    // 种族加值
    [ability: string]: number;
  };
  classPrimary: string;               // 主属性
  classSecondary?: string;            // 次属性
}

// 购点法成本表
const POINT_BUY_COST: { [score: number]: number } = {
  8: 0, 9: 1, 10: 2, 11: 3, 12: 4,
  13: 5, 14: 7, 15: 9
};
```

**页面布局**：

```
┌─────────────────────────┐
│  ←  步骤 4/8  分配属性   │
├─────────────────────────┤
│  [ 27点购点 | 骰子掷骰 ] │  ← Tab切换
├─────────────────────────┤
│ 💡 购点法说明           │
│ 基础8，上限15           │
│ 总点数: 27              │
├─────────────────────────┤
│ 力量(STR)               │
│  8  9  10  11  12  13   │
│     14  15              │
│  种族+2  最终: 14       │
│                         │
│ 敏捷(DEX)  ☆           │  ← 次属性标记
│  8  9  10  11  12  13   │
│     ●14  15             │
│  最终: 14               │
│                         │
│ 智力(INT)  ★           │  ← 主属性标记
│  8  9  10  11  12  13   │
│     14  ●15             │
│  种族+1  最终: 16       │
│  调整值: +3             │
├─────────────────────────┤
│ 剩余点数: 5             │
├─────────────────────────┤
│    [  下一步  ]         │
└─────────────────────────┘
```

---

#### 步骤 5：选择背景 (`/builder/background`)

**API 数据格式**：

```typescript
interface BackgroundData {
  index: string;
  name: string;
  description: string;
  skillProficiencies: string[];     // 固定技能
  languages?: {
    choose: number;                 // 可选语言数量
  };
  toolProficiencies?: {
    options: string[];
    choose: number;
  };
  equipment: string[];              // 起始装备
  feature: {
    name: string;
    description: string;
  };
  characteristics: {                // 个性特征选项
    personalityTraits: string[];
    ideals: string[];
    bonds: string[];
    flaws: string[];
  };
}

// 阵营九宫格
interface Alignment {
  ethical: 'lawful' | 'neutral' | 'chaotic';   // 守序/中立/混乱
  moral: 'good' | 'neutral' | 'evil';          // 善良/中立/邪恶
  name: string;                                // 如"守序善良"
}
```

**页面布局**：

```
┌─────────────────────────┐
│  ←  步骤 5/8  选择背景   │
├─────────────────────────┤
│ 🏛️ 士兵 Soldier ▼       │  ← 下拉选择
├─────────────────────────┤
│ 📋 阵营选择             │
│     善良  中立  邪恶    │
│ 守序 ●      ○      ○    │
│ 中立 ○      ○      ○    │
│ 混乱 ○      ○      ○    │
├─────────────────────────┤
│ 📋 背景信息             │
│  技能: 运动 威吓        │
│  语言(选1): ○矮人语     │
│             ●精灵语     │
│  装备: 军阶徽章等       │
├─────────────────────────┤
│ ✨ 背景特性             │
│  军阶                   │
│  士兵同伴尊敬你...      │
├─────────────────────────┤
│    [  下一步  ]         │
└─────────────────────────┘
```

---

#### 步骤 6：选择法术 (`/builder/spells`)

**API 数据格式**：

```typescript
interface SpellData {
  index: string;
  name: string;                 // 法术名称
  level: number;                // 法术等级
  school: string;               // 学派
  ritual: boolean;              // 是否为仪式
  castingTime: string;          // 施法时间
  range: string;                // 射程
  components: string[];         // 成分 V/S/M
  duration: string;             // 持续时间
  description: string;          // 描述
  higherLevels?: string;        // 升环效果
}

// 三种施法机制
interface SpellSelection {
  // 已知法术（术士/吟游诗人）
  type: 'known';
  cantripsKnown: number;
  spellsKnown: number;
  
  // 或准备法术（牧师/德鲁伊）
  type: 'prepared';
  cantripsKnown: number;
  maxPrepared: number;          // 调整值+等级
  
  // 或法术书+准备（法师）
  type: 'spellbook';
  spellbookSize: number;        // 抄写数量（6个）
  maxPrepared: number;          // 准备数量（3个）
}
```

**页面布局 - 术士（已知法术）**：

```
┌─────────────────────────┐
│  ←  步骤 6/8  选择法术   │
├─────────────────────────┤
│ 🔮 施法能力             │
│  施法属性: 魅力(CHA)    │
│  法术豁免DC: 13         │
│  法术攻击调整值: +5     │
├─────────────────────────┤
│ 🌟 选择0环法术 (2/4)    │
│  ☑ 法师之手  戏法       │
│  ☑ 光照术    戏法       │
│  ☐ 魔法飞弹  戏法       │
│  ☑ 冷冻射线  戏法       │
├─────────────────────────┤
│ 📜 选择1环法术 (1/2)    │
│  已知法术               │
│  ☑ 燃烧之手  1环 塑能  │
│    [仪式] 施法时间:1动作│
│    射程:15尺 成分:V/S   │
│    持续时间:瞬间        │
│    火焰从你伸出的手掌.. │
│  ☐ 魔法飞弹  1环 塑能  │
│    ▶ 点击展开详情      │
├─────────────────────────┤
│    [  下一步  ]         │
└─────────────────────────┘
```

**页面布局 - 法师（法术书+准备）**：

```
┌─────────────────────────┐
│  ←  步骤 6/8  选择法术   │
├─────────────────────────┤
│ 🔮 施法能力             │
│  施法属性: 智力(INT)    │
├─────────────────────────┤
│ 📚 步骤1: 抄写法术书    │
│  选择6个法术加入法术书  │
│  (4/6)                  │
│  ☑ 魔法飞弹  ☑ 护盾术  │
│  ☑ 燃烧之手  ☑ 睡眠术  │
│  ☐ 隐雾术  ☑ 魅惑人类  │
├─────────────────────────┤
│ 🔖 步骤2: 准备今日法术  │
│  从法术书中准备3个      │
│  (2/3)                  │
│  ☑ 魔法飞弹  ☐ 护盾术  │
│  ☑ 燃烧之手  ☐ 睡眠术  │
├─────────────────────────┤
│    [  下一步  ]         │
└─────────────────────────┘
```

---

#### 步骤 7：起始装备 (`/builder/equipment`)

**API 数据格式**：

```typescript
interface EquipmentData {
  // 职业和背景已提供的装备
  startingEquipment: {
    class: EquipmentItem[];
    background: EquipmentItem[];
  };
  
  // 待完成的装备选择（如有）
  pendingChoices?: EquipmentChoice[];
  
  // 起始金币
  startingGold: number;
}

interface EquipmentItem {
  index: string;
  name: string;
  quantity: number;
  description?: string;
}

interface EquipmentChoice {
  index: string;
  description: string;
  options: EquipmentOption[];
  choose: number;
}
```

**页面布局**：

```
┌─────────────────────────┐
│  ←  步骤 7/8  起始装备   │
├─────────────────────────┤
│ 🎒 已获装备             │
│ 【职业装备】            │
│  链甲 长剑 盾           │
│  轻十字弩 弩箭x20       │
│  探险家套组             │
│ 【背景装备】            │
│  军阶徽章 骨制骰子      │
├─────────────────────────┤
│ ⚔️ 装备选择             │  ← 如有则显示
│ 选择近战武器:           │
│ ● 长剑 ○ 战斧 ○ 长矛   │
│ 选择远程武器:           │
│ ● 轻十字弩 ○ 短弓      │
├─────────────────────────┤
│ 💡 提示                 │
│ 装备已完整提供          │
│ 起始金币: 0 gp          │
├─────────────────────────┤
│    [  下一步  ]         │
└─────────────────────────┘
```

---

#### 步骤 8：确认角色 (`/builder/review`)

**API 数据格式**：

```typescript
interface CharacterReview {
  // 基础信息
  name: string;
  race: { name: string; subrace?: string };
  class: { name: string; level: number };
  background: string;
  alignment: string;
  
  // 属性
  abilities: {
    [key: string]: { score: number; modifier: number };
  };
  
  // 战斗数值
  hp: number;
  ac: number;
  proficiencyBonus: number;
  
  // 熟练项
  proficiencies: {
    savingThrows: string[];
    skills: string[];
    armor?: string[];
    weapons?: string[];
    tools?: string[];
  };
  
  // 法术（如有）
  spellcasting?: {
    ability: string;
    saveDc: number;
    attackBonus: number;
    cantrips: string[];
    spells: string[];
    spellSlots: number;
  };
  
  // 装备
  equipment: string[];
  
  // 特性
  features: string[];
}
```

**页面布局**：

```
┌─────────────────────────┐
│  ←  步骤 8/8  确认角色   │
├─────────────────────────┤
│ ┌─────────────────┐     │
│ │   [头像占位]    │     │  ← 角色卡片
│ │   阿拉斯塔      │     │
│ │   木精灵 牧师1  │     │
│ │   士兵 守序善良 │     │
│ └─────────────────┘     │
├─────────────────────────┤
│ ⚔️ 战斗数值             │
│  HP: 10  AC: 16         │
│  先攻: +2  速度: 30尺   │
├─────────────────────────┤
│ 📊 属性值               │
│  力14(+2) 敏14(+2) 体14(+2)│
│  智10(+0) 感16(+3) 魅10(+0)│
├─────────────────────────┤
│ 🛡️ 熟练项目             │
│  豁免: 感知 魅力        │
│  技能: 运动 威吓 医药.. │
├─────────────────────────┤
│ ✨ 种族特性             │
│  黑暗视觉 精灵血统      │
├─────────────────────────┤
│ ✨ 职业特性             │
│  生命领域 虔诚护盾..    │
├─────────────────────────┤
│ 🔮 法术（生命领域牧师） │
│  戏法: 光亮术 神导术    │
│  1环(2/2): 祝福 治愈真言 │
│  领域法术: 祝福 治愈伤痛 │
├─────────────────────────┤
│ 🎒 装备                 │
│  链甲 钉头锤 盾...      │
├─────────────────────────┤
│    [  完成创建  ]       │
└─────────────────────────┘
```

---

### 3. 角色列表页面 (`/characters`)

| 功能项 | 描述 | 优先级 | 状态 |
|--------|------|--------|------|
| 角色卡片 | 展示角色基本信息 | P0 | 📝 待补充 |
| 搜索筛选 | 按种族/职业/等级筛选 | P1 | 📝 待补充 |
| 排序功能 | 按创建时间/名称/等级排序 | P1 | 📝 待补充 |

---

### 4. 角色详情页面 (`/character/:id`)

| 功能项 | 描述 | 优先级 | 状态 |
|--------|------|--------|------|
| 角色卡展示 | 完整角色信息 | P0 | 📝 待补充 |
| 导出功能 | 导出为PDF/图片 | P2 | 📝 待补充 |
| 分享功能 | 生成分享码 | P2 | 📝 待补充 |

---

### 5. 我的页面 (`/profile`)

| 功能项 | 描述 | 优先级 | 状态 |
|--------|------|--------|------|
| 用户信息 | 微信授权信息 | P1 | 📝 待补充 |
| 角色统计 | 总角色数等 | P1 | 📝 待补充 |
| 规则版本 | 切换 SRD 版本 | P1 | 📝 待补充 |
| 扩展包管理 | 扩展包下载 | P2 | 📝 待补充 |
| 数据备份 | 云端同步 | P2 | 📝 待补充 |
| 设置 | 进入设置 | P0 | 📝 待补充 |

---

### 6. 设置页面 (`/settings`)

| 功能项 | 描述 | 优先级 | 状态 |
|--------|------|--------|------|
| 语言设置 | 简中/繁中/英文 | P2 | 📝 待补充 |
| 主题设置 | 浅色/深色模式 | P2 | 📝 待补充 |
| 清除缓存 | 清理本地缓存 | P1 | 📝 待补充 |

---

## 🎯 优先级说明

| 优先级 | 说明 |
|--------|------|
| P0 | 核心功能，必须有 |
| P1 | 重要功能，应该有 |
| P2 | 增强功能，可以有 |
| P3 | 未来版本考虑 |

---

## 📝 变更日志

| 日期 | 变更内容 | 记录人 |
|------|----------|--------|
| 2026-02-27 | 创建文档框架 | Kimi |
| 2026-02-27 | 完成步骤1-8设计 | Kimi |

---

> 💡 **参考文档**
> - 详细API定义: `API.md`
> - 各步骤详细设计: `*_page.md`
