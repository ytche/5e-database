# D&D 5e 车卡系统 - 扩展包开发指南

## 目录

1. [扩展包概述](#扩展包概述)
2. [扩展包结构](#扩展包结构)
3. [数据扩展](#数据扩展)
4. [自定义步骤](#自定义步骤)
5. [规则覆盖](#规则覆盖)
6. [示例扩展包](#示例扩展包)
7. [发布与分发](#发布与分发)

---

## 扩展包概述

扩展包（Extension）是车卡系统的插件机制，允许开发者：

- 添加新的种族、职业、法术、装备等数据
- 创建自定义车卡步骤
- 修改现有游戏规则
- 添加自定义验证器

### 扩展包类型

| 类型 | 用途 | 示例 |
|------|------|------|
| 官方扩展 | WotC 官方资料书 | Xanathar's Guide, Tasha's Cauldron |
| 第三方扩展 | 社区创作内容 | Critical Role 内容 |
| Homebrew | 用户自定义内容 | 个人战役设定 |

---

## 扩展包结构

```
my-extension/
├── manifest.json          # 扩展包清单（必需）
├── data/                  # 数据文件
│   ├── races.json
│   ├── classes.json
│   ├── subclasses.json
│   └── spells.json
├── scripts/               # 自定义脚本
│   ├── steps.js
│   └── validators.js
├── assets/                # 资源文件
│   └── icons/
└── README.md              # 说明文档
```

### 清单文件 (manifest.json)

```json
{
  "id": "xanathars-guide",
  "name": "Xanathar's Guide to Everything",
  "nameZh": "珊娜萨的万事指南",
  "version": "1.0.0",
  "description": "添加珊娜萨的万事指南中的新种族、子职业和法术",
  "author": "Wizards of the Coast",
  "license": "OGL",
  
  "dependencies": {
    "core": "srd-2014-zh@>=1.0.0",
    "extensions": []
  },
  
  "compatibility": {
    "engine": ">=1.0.0",
    "platforms": ["web", "weixin"]
  },
  
  "dataFiles": {
    "races": "data/races.json",
    "subraces": "data/subraces.json",
    "classes": "data/classes.json",
    "subclasses": "data/subclasses.json",
    "spells": "data/spells.json",
    "feats": "data/feats.json",
    "backgrounds": "data/backgrounds.json"
  },
  
  "customSteps": [
    {
      "id": "select-invocation",
      "name": "选择魔能祈唤",
      "nameZh": "选择魔能祈唤",
      "order": 35,
      "condition": {
        "requiresClass": ["warlock"],
        "requiresLevel": { "min": 2 }
      },
      "optionsProvider": "getInvocationOptions",
      "executor": "applyInvocationSelection"
    }
  ],
  
  "ruleOverrides": [
    {
      "target": "ability-score-improvement",
      "property": "allowFeatAtLevel1",
      "value": true,
      "condition": "variant-human"
    }
  ],
  
  "scripts": [
    "scripts/steps.js",
    "scripts/validators.js"
  ]
}
```

---

## 数据扩展

### 数据格式

扩展包中的数据格式与核心SRD数据格式完全一致：

#### 添加新种族 (races.json)

```json
[
  {
    "index": "aasimar",
    "name": "阿斯莫",
    "name_en": "Aasimar",
    "speed": 30,
    "ability_bonuses": [
      {
        "ability_score": {
          "index": "cha",
          "name": "CHA",
          "url": "/api/ability-scores/cha"
        },
        "bonus": 2
      }
    ],
    "alignment": "阿斯莫通常倾向于善良...",
    "age": "阿斯莫在20岁左右成年...",
    "size": "中型",
    "size_description": "阿斯莫身高与体型与常人相似...",
    "languages": [
      { "index": "common", "name": "通用语", "url": "/api/languages/common" },
      { "index": "celestial", "name": "天界语", "url": "/api/languages/celestial" }
    ],
    "traits": [
      { "index": "darkvision", "name": "黑暗视觉", "url": "/api/traits/darkvision" },
      { "index": "celestial-resistance", "name": "天界抗性", "url": "/api/traits/celestial-resistance" },
      { "index": "healing-hands", "name": "治疗之手", "url": "/api/traits/healing-hands" },
      { "index": "light-bearer", "name": "光明使者", "url": "/api/traits/light-bearer" }
    ],
    "subraces": [
      { "index": "protector-aasimar", "name": "守护者阿斯莫", "url": "/api/subraces/protector-aasimar" },
      { "index": "scourge-aasimar", "name": "惩罚者阿斯莫", "url": "/api/subraces/scourge-aasimar" },
      { "index": "fallen-aasimar", "name": "堕落者阿斯莫", "url": "/api/subraces/fallen-aasimar" }
    ]
  }
]
```

#### 添加新子职业 (subclasses.json)

```json
[
  {
    "index": "hexblade",
    "class": {
      "index": "warlock",
      "name": "邪术师",
      "url": "/api/classes/warlock"
    },
    "name": "咒剑",
    "name_en": "Hexblade",
    "subclass_flavor": "异界宗主",
    "desc": [
      "咒剑宗主存在于阴影位面..."
    ],
    "spells": [
      {
        "prerequisites": [
          { "index": "warlock-1", "type": "level", "name": "Warlock 1" }
        ],
        "spell": { "index": "shield", "name": "Shield", "url": "/api/spells/shield" }
      },
      {
        "prerequisites": [
          { "index": "warlock-1", "type": "level", "name": "Warlock 1" }
        ],
        "spell": { "index": "wrathful-smite", "name": "Wrathful Smite", "url": "/api/spells/wrathful-smite" }
      }
    ]
  }
]
```

### 数据冲突处理

当多个扩展包提供相同ID的数据时，系统按以下规则处理：

1. **优先级**：priority 值高的覆盖低的
2. **手动选择**：用户可以选择使用哪个版本
3. **合并**：某些数据类型支持合并（如法术列表）

```javascript
// 扩展包中声明数据覆盖
{
  "id": "my-homebrew",
  "overrides": {
    "races": ["elf"],  // 此扩展包的elf数据覆盖其他来源
    "spells": {
      "fireball": "merge"  // 合并而非覆盖
    }
  }
}
```

---

## 自定义步骤

### 步骤定义

```javascript
// scripts/steps.js

/**
 * 获取步骤选项
 * @param {BuildContext} context - 当前构建上下文
 * @returns {StepOption[]}
 */
function getInvocationOptions(context) {
  const level = context.character.classes
    .find(c => c.index === 'warlock')?.level || 0;
  
  // 获取所有魔能祈唤
  const allInvocations = api.getData('features')
    .filter(f => f.feature_type === 'invocation');
  
  // 根据等级和前置条件筛选
  return allInvocations
    .filter(inv => {
      if (inv.level_required && inv.level_required > level) return false;
      if (inv.prerequisites) {
        return checkPrerequisites(context, inv.prerequisites);
      }
      return true;
    })
    .map(inv => ({
      id: inv.index,
      name: inv.name,
      description: inv.desc[0],
      prerequisites: inv.prerequisites,
    }));
}

/**
 * 应用选择
 * @param {BuildContext} context
 * @param {string[]} selection - 选择的祈唤ID列表
 * @returns {BuildContext}
 */
function applyInvocationSelection(context, selection) {
  // 验证选择数量
  const level = context.character.classes
    .find(c => c.index === 'warlock')?.level || 0;
  const maxInvocations = Math.min(2 + Math.floor((level - 2) / 3), 8);
  
  if (selection.length > maxInvocations) {
    throw new Error(`最多只能选择 ${maxInvocations} 个魔能祈唤`);
  }
  
  // 应用选择
  context.character.features.push(...selection.map(id => ({
    type: 'invocation',
    index: id,
  })));
  
  return context;
}

/**
 * 检查前置条件
 */
function checkPrerequisites(context, prerequisites) {
  for (const prereq of prerequisites) {
    switch (prereq.type) {
      case 'feature':
        if (!context.character.features.includes(prereq.index)) {
          return false;
        }
        break;
      case 'spell':
        // 检查是否知道特定法术
        break;
      case 'pact':
        // 检查契约类型
        break;
    }
  }
  return true;
}
```

### 条件步骤

```javascript
{
  "customSteps": [
    {
      "id": "select-fighting-style",
      "condition": {
        // 只有特定职业显示
        "requiresClass": ["fighter", "paladin", "ranger"],
        
        // 等级要求
        "requiresLevel": { "min": 1, "max": 20 },
        
        // 自定义条件脚本
        "customScript": "context.character.classes.some(c => ['fighter', 'paladin', 'ranger'].includes(c.index))"
      }
    }
  ]
}
```

---

## 规则覆盖

### 覆盖类型

```javascript
{
  "ruleOverrides": [
    // 修改属性点购买上限
    {
      "target": "ability-score-generation",
      "property": "pointBuyMaxPoints",
      "value": 32,  // 默认27点
    },
    
    // 允许初始专长
    {
      "target": "feat",
      "property": "allowAtLevel1",
      "value": true,
    },
    
    // 修改多职业前置条件
    {
      "target": "multiclass",
      "property": "prerequisites",
      "value": "relaxed",  // 使用宽松的前置条件
    },
    
    // 特定条件下的规则覆盖
    {
      "target": "variant-human",
      "property": "startingFeat",
      "value": true,
      "condition": "race.index === 'human' && subrace === 'variant'"
    }
  ]
}
```

---

## 示例扩展包

### 完整示例：添加一个自定义种族

```
custom-dragonborn/
├── manifest.json
├── data/
│   └── races.json
└── README.md
```

**manifest.json**

```json
{
  "id": "custom-dragonborn",
  "name": "改进的龙裔种族",
  "version": "1.0.0",
  "description": "基于Fizban's Treasury of Dragons的改进龙裔",
  "author": "Your Name",
  "dependencies": {
    "core": "srd-2014-zh@>=1.0.0"
  },
  "dataFiles": {
    "races": "data/races.json"
  }
}
```

**data/races.json**

```json
[
  {
    "index": "gem-dragonborn",
    "name": "宝石龙裔",
    "name_en": "Gem Dragonborn",
    "speed": 30,
    "ability_bonuses": [
      {
        "ability_score": { "index": "cha", "name": "CHA", "url": "/api/ability-scores/cha" },
        "bonus": 1
      }
    ],
    "ability_bonus_options": {
      "desc": "选择一项属性+2",
      "choose": 1,
      "type": "ability_bonuses",
      "from": {
        "option_set_type": "options_array",
        "options": [
          { "option_type": "reference", "item": { "index": "str", "name": "STR" } },
          { "option_type": "reference", "item": { "index": "dex", "name": "DEX" } },
          { "option_type": "reference", "item": { "index": "con", "name": "CON" } },
          { "option_type": "reference", "item": { "index": "int", "name": "INT" } },
          { "option_type": "reference", "item": { "index": "wis", "name": "WIS" } }
        ]
      }
    },
    "alignment": "宝石龙裔具有独特的气质...",
    "age": "年轻的宝石龙裔快速成长...",
    "size": "中型",
    "size_description": "宝石龙裔身高5到6英尺...",
    "languages": [
      { "index": "common", "name": "通用语" },
      { "index": "draconic", "name": "龙语" }
    ],
    "traits": [
      { "index": "draconic-ancestry-gem", "name": "龙族血统（宝石）" },
      { "index": "breath-weapon-gem", "name": "宝石吐息武器" },
      { "index": "damage-resistance-gem", "name": "伤害抗性（宝石）" },
      { "index": "psionic-mind", "name": "灵能心灵" }
    ]
  }
]
```

---

## 发布与分发

### 本地测试

```javascript
// 在应用中加载本地扩展
const extensionData = await fetch('/extensions/custom-dragonborn/manifest.json')
  .then(r => r.json());

await builder.loadExtension({
  id: extensionData.id,
  url: '/extensions/custom-dragonborn/'
});
```

### CDN 分发

```javascript
// 从CDN加载
await builder.loadExtension({
  id: 'xanathars-guide',
  url: 'https://cdn.example.com/extensions/xge-v1.0.json'
});
```

### 扩展包市场

未来可以建立扩展包市场：

```javascript
// 浏览可用扩展
const availableExtensions = await builder.browseExtensions();

// 安装扩展
await builder.installExtension('xanathars-guide');

// 管理已安装扩展
builder.enableExtension('xanathars-guide');
builder.disableExtension('tashas-cauldron');
builder.uninstallExtension('unwanted-extension');
```

---

## 最佳实践

### 1. 数据验证

在发布前验证扩展包数据：

```bash
npm run validate-extension ./my-extension/
```

### 2. 版本管理

- 使用语义化版本（SemVer）
- 维护更新日志
- 测试向后兼容性

### 3. 性能考虑

- 数据文件不宜过大（建议 < 500KB）
- 图片资源使用压缩格式
- 延迟加载非必要数据

### 4. 文档

- 提供清晰的README
- 说明依赖关系
- 记录已知问题

---

## 故障排除

### 常见问题

**Q: 扩展包数据未显示**
- 检查 manifest.json 格式
- 确认数据源已启用
- 查看控制台错误信息

**Q: 与其他扩展冲突**
- 检查 overrides 配置
- 调整 priority 值
- 使用依赖管理

**Q: 自定义步骤不生效**
- 验证 condition 条件
- 检查 order 值是否合适
- 确认脚本语法正确
