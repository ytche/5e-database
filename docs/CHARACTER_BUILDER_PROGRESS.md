# D&D 5e 车卡小程序 - 工作进度记录

> 📅 创建时间：2026-02-27
> 📝 最后更新：2026-02-27

---

## 📊 整体进度概览

| 模块 | 状态 | 完成度 |
|------|------|--------|
| 需求分析 | ✅ 已完成 | 100% |
| UI 设计文档 | ✅ 已完成 | 100% |
| API 接口设计 | ✅ 已完成 | 100% |
| 核心架构代码 | ✅ 已完成 | 100% |
| 后续步骤 | 📝 待实现 | 0% |

---

## ✅ 已完成工作

### 1. 项目初始化

**提交记录**：
- `86cad85` feat: add D&D 5e character builder module
- `9a47190` chore: update project configuration and add translation scripts

**文件结构**：
```
character-builder/
├── README.md                    # 项目说明
├── docs/
│   ├── API.md                   # API 接口文档
│   ├── ARCHITECTURE.md          # 架构设计文档
│   ├── EXTENSION_GUIDE.md       # 扩展包开发指南
│   └── UI_REQUIREMENTS.md       # UI 需求文档
├── examples/
│   └── basic-usage.ts           # 使用示例
└── src/
    ├── builder/                 # 车卡核心
    │   ├── character-calculator.ts
    │   ├── state-machine.ts
    │   └── steps/
    │       ├── allocate-abilities-step.ts
    │       ├── select-class-step.ts
    │       ├── select-race-step.ts
    │       └── step-registry.ts
    ├── core/                    # 核心引擎
    │   ├── data-registry.ts
    │   └── utils/
    │       └── immutable.ts
    ├── platform/                # 平台适配
    │   ├── platform-adapter.ts
    │   └── web/
    ├── types/                   # 类型定义
    └── index.ts                 # 入口文件
```

---

### 2. 页面设计（UI_REQUIREMENTS.md）

#### 2.1 首页 (`/index`)

**状态**：✅ MVP 版本设计完成

| 功能 | 状态 | 说明 |
|------|------|------|
| 创建新角色按钮 | ✅ | 唯一主按钮，突出显示 |
| 规则查询按钮 | 🚫 | 隐藏，后续版本实现 |
| 版权声明 | ✅ | OGL 声明，底部显示 |
| Tab 导航 | ✅ | 首页 + 我的 |

**布局**：
- Logo/标题区域
- 创建新角色按钮
- 版权声明卡片
- Tab 导航

---

#### 2.2 战役设置 (`/builder/campaign`)

**状态**：✅ 设计完成

| 功能 | 状态 | 说明 |
|------|------|------|
| DM 提示卡片 | ✅ | 提醒与 DM 确认规则 |
| 规则版本选择 | ✅ | 5E(可用)/5R(禁用) |
| 扩展规则选择 | ✅ | 列表形式，PHB 必选 |
| 下一步按钮 | ✅ | 进入下一步 |

**数据接口**：
```http
GET /data/versions
GET /data/extensions
```

---

#### 2.3 选择种族 (`/builder/race`)

**状态**：✅ 设计完成

| 功能 | 状态 | 说明 |
|------|------|------|
| 下拉选择框 | ✅ | 带搜索，默认选第一个 |
| 亚种选择 | ✅ | 单选，无亚种隐藏 |
| 基础信息卡片 | ✅ | 年龄/体型/速度/语言 |
| 种族特性卡片 | ✅ | 固定+可选特性 |

**关键设计**：
- 年龄：数字输入，下方显示种族年龄描述
- 语言：固定标签 + 可选单选
- 特性：小卡片形式展示

**数据结构**：
```typescript
interface RaceData {
  index, name, nameEn, icon
  speed, size, sizeLabel
  age: string                    // 年龄描述
  abilityBonuses[]
  languages: {
    fixed: Language[]            // 固定语言
    optional: Language[]         // 可选语言
    optionalCount: number
  }
  subraces: Subrace[]
  traits: Trait[]
}
```

---

#### 2.4 选择职业 (`/builder/class`)

**状态**：✅ 设计完成（最新调整）

**卡片顺序**：
1. 下拉选择框
2. **生命值卡片** ❤️
3. **熟练项目卡片** 🛡️
4. **起始装备卡片** 🎒
5. **抉择卡片** 📋 (0-n个)

**详细设计**：

**生命值卡片**：
- 生命骰（如 1d6）
- 第一级生命值（如 6+体质调整值）
- 后续升级生命值（如 4(1d6)+体质调整值）

**熟练项目卡片**：
- 护甲：只读标签
- 武器：只读标签
- 工具：多选标签（如有）
- 豁免：多选标签（通常2个）
- 技能：多选标签（需选够数量）

**起始装备卡片**：
- 可能有多条（①②③...）
- 每条：直接描述 或 多选

**抉择卡片**（0个或多个）：
- 卡片标题来自 `cardTitle`（如"领域选择"）
- 单选形式，默认选第一个
- 示例：领域选择、战斗风格选择、魔契恩泽选择

**数据结构**：
```typescript
interface ClassData {
  index, name, nameEn, icon
  hitDice: number
  hpAtFirstLevel: string        // 新增
  hpAtHigherLevels: string      // 新增
  proficiencies: {
    savingThrows: { options[], choose }
    skills: { options[], choose }
    armor?, weapons?
    tools?: { options[], choose }  // 改为对象
  }
  startingEquipment: EquipmentOption[]  // 新增
  choices: ClassChoice[]         // 抉择项
}

interface EquipmentOption {
  index
  description?: string           // 直接描述
  options?: EquipmentChoice[]    // 或提供选择
  choose?: number
}

interface ClassChoice {
  index, name
  cardTitle: string              // 卡片标题
  description?
  options: ChoiceOption[]
}
```

---

### 3. API 文档（API.md）

**状态**：✅ 已同步更新

**已定义接口**：

| 接口 | 方法 | 说明 |
|------|------|------|
| `/data/versions` | GET | 获取规则版本列表 |
| `/data/extensions` | GET | 获取扩展规则书列表 |
| `/data/races` | GET | 获取种族列表（含完整数据） |
| `/data/classes` | GET | 获取职业列表（含完整数据） |
| `/characters` | POST | 创建新角色 |
| `/characters/:id/progress` | PUT | 保存角色进度 |
| `/characters/:id` | GET | 获取角色详情 |
| `/characters` | GET | 获取角色列表 |
| `/characters/:id` | DELETE | 删除角色 |

---

### 4. 核心架构代码

**状态**：✅ 已完成

**主要模块**：
- `state-machine.ts` - 车卡状态机
- `character-calculator.ts` - 角色计算器
- `data-registry.ts` - 数据注册表
- `step-registry.ts` - 步骤注册表
- `platform-adapter.ts` - 平台适配器

---

## 📝 待完成工作

### 后续步骤设计

| 步骤 | 页面 | 优先级 | 状态 |
|------|------|--------|------|
| 4 | `/builder/abilities` | P0 | 📝 待设计 |
| 5 | `/builder/background` | P0 | 📝 待设计 |
| 6 | `/builder/spells` | P1 | 📝 待设计 |
| 7 | `/builder/equipment` | P1 | 📝 待设计 |
| 8 | `/builder/review` | P0 | 📝 待设计 |

### 其他页面

| 页面 | 优先级 | 状态 |
|------|--------|------|
| 角色列表 (`/characters`) | P0 | 📝 待设计 |
| 角色详情 (`/character/:id`) | P0 | 📝 待设计 |
| 我的页面 (`/profile`) | P1 | 📝 待设计 |
| 设置页面 (`/settings`) | P2 | 📝 待设计 |

### 技术实现

| 任务 | 优先级 | 状态 |
|------|--------|------|
| 后端 API 实现 | P0 | 📝 待开发 |
| 前端页面实现 | P0 | 📝 待开发 |
| 数据导入（SRD） | P0 | 📝 待处理 |
| 微信小程序适配 | P1 | 📝 待开发 |
| 扩展包系统 | P2 | 📝 待开发 |

---

## 💬 关键设计决策记录

### 1. 卡片式设计风格
- 所有内容区块以卡片形式呈现
- 白色卡片，浅灰背景
- 圆角 12-16px

### 2. 底部 Tab 导航
- 所有页面固定显示
- 两个入口：首页、我的
- 当前 Tab 高亮

### 3. 下拉选择 + 详情展示
- 种族/职业选择使用下拉框
- 选择后下方展示详细配置
- 带搜索功能

### 4. 抉择卡片机制
- 通用组件，支持多种选择类型
- 卡片标题动态（领域选择/战斗风格选择等）
- 数量灵活（0-n个）

### 5. 数据结构分层
- 数据源版本管理（5e-2014/2024）
- 扩展包支持（XGE/TCE等）
- 可选内容标记

---

## 📁 相关文档链接

| 文档 | 路径 |
|------|------|
| UI 需求文档 | `character-builder/docs/UI_REQUIREMENTS.md` |
| API 文档 | `character-builder/docs/API.md` |
| 架构设计 | `character-builder/docs/ARCHITECTURE.md` |
| 扩展指南 | `character-builder/docs/EXTENSION_GUIDE.md` |
| 项目 README | `character-builder/README.md` |

---

## 🎯 下一步建议

1. **继续完善页面设计**
   - 步骤4：分配属性（购点法）
   - 步骤5：选择背景
   - 步骤8：角色确认页面

2. **开始技术实现**
   - 后端 API 开发
   - SRD 数据导入
   - 前端页面实现

3. **测试验证**
   - 车卡流程端到端测试
   - 数据正确性验证

---

*此文档记录了 D&D 5e 车卡小程序的设计和开发进度，供团队成员参考。*
