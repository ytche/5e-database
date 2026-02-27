# D&D 5e 车卡系统

一个可扩展、跨平台的 D&D 5e 角色构建工具。

## 特性

- 🎲 **完整SRD支持**：基于D&D 5e SRD 2014中文版
- 🔌 **可扩展架构**：支持官方扩展包和自定义Homebrew内容
- 📱 **跨平台**：Web端 + 微信小程序（未来支持更多平台）
- ⚡ **性能优化**：懒加载、数据缓存、增量更新
- 🛡️ **类型安全**：完整的TypeScript支持

## 快速开始

### 安装

```bash
npm install @dnd5e/character-builder
```

### 基础使用

```typescript
import { CharacterBuilder } from '@dnd5e/character-builder';
import { WebPlatformAdapter } from '@dnd5e/character-builder/web';

// 初始化车卡器
const builder = new CharacterBuilder({
  platform: new WebPlatformAdapter(),
  dataSources: ['srd-2014-zh'],
});

await builder.initialize();

// 开始车卡
const currentStep = builder.getCurrentStep();
console.log(currentStep.name); // "选择种族"

// 获取选项
const options = currentStep.getOptions(builder.getContext());

// 做出选择
builder.dispatch({
  type: 'SELECT_RACE',
  payload: { raceId: 'elf', subraceId: 'high-elf' }
});

// 继续下一步
builder.nextStep();

// 导出角色
const character = builder.exportCharacter();
console.log(character);
```

### 加载扩展包

```typescript
// 从URL加载扩展
await builder.loadExtension({
  id: 'xge',
  url: 'https://extensions.dnd5e.com/xge-v1.0.json'
});

// 从本地文件加载（桌面端）
await builder.loadExtensionFromFile(homebrewFile);
```

## 架构设计

```
┌─────────────────────────────────────────────────────────────┐
│                         平台适配层                            │
│    Web    │    微信小程序    │    Mobile    │    Desktop    │
└─────────────────────────────┬───────────────────────────────┘
                              │
┌─────────────────────────────▼───────────────────────────────┐
│                        核心引擎层                            │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────────────┐  │
│  │ State Machine│  │ Validation  │  │ Character Calculator│  │
│  └─────────────┘  └─────────────┘  └─────────────────────┘  │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────────────┐  │
│  │ Step Registry│  │ Plugin System│  │ Export Manager     │  │
│  └─────────────┘  └─────────────┘  └─────────────────────┘  │
└─────────────────────────────────────────────────────────────┘
```

详细架构说明请查看 [ARCHITECTURE.md](./docs/ARCHITECTURE.md)。

## 项目结构

```
character-builder/
├── src/
│   ├── core/              # 核心引擎（平台无关）
│   │   ├── data-registry.ts
│   │   └── utils/
│   ├── builder/           # 车卡系统
│   │   ├── state-machine.ts
│   │   └── steps/         # 各步骤实现
│   ├── validation/        # 验证系统
│   ├── plugin/            # 插件系统
│   ├── export/            # 导出系统
│   ├── platform/          # 平台适配
│   │   ├── web/
│   │   └── weixin/
│   └── types/             # 类型定义
├── data/                  # 静态数据
├── docs/                  # 文档
└── tests/                 # 测试
```

## 开发

### 安装依赖

```bash
npm install
```

### 运行测试

```bash
npm test
```

### 构建

```bash
npm run build
```

### 创建扩展包

查看 [EXTENSION_GUIDE.md](./docs/EXTENSION_GUIDE.md) 了解如何创建自定义扩展包。

## 支持的步骤

| 步骤 | ID | 描述 |
|------|-----|------|
| 选择种族 | select-race | 选择种族和亚种族 |
| 选择职业 | select-class | 选择职业和子职业 |
| 分配属性 | allocate-abilities | 使用购点法或标准数组分配属性 |
| 选择背景 | select-background | 选择角色背景 |
| 选择法术 | select-spells | 施法者选择法术 |
| 选择专长 | select-feats | 选择专长或属性提升 |
| 购买装备 | buy-equipment | 购买起始装备 |

## 导出格式

- **JSON**: 完整角色数据
- **Compact JSON**: 精简格式，适合分享
- **PDF**: 标准角色卡（计划中）
- **Foundry VTT**: Foundry VTT兼容格式（计划中）

## 路线图

### MVP (已完成)
- [x] 基础架构设计
- [x] 数据注册表
- [x] 车卡状态机
- [x] 种族选择步骤
- [x] 职业选择步骤
- [x] 属性分配步骤

### 第一阶段
- [ ] 背景选择步骤
- [ ] 法术选择步骤
- [ ] 角色卡导出
- [ ] Web UI 实现

### 第二阶段
- [ ] 微信小程序适配
- [ ] 扩展包加载器
- [ ] 用户自定义内容

### 第三阶段
- [ ] 升级系统
- [ ] 多职业支持
- [ ] PDF导出

## 贡献

欢迎提交Issue和PR！

## 许可

MIT License - 详见 [LICENSE](./LICENSE)

数据基于 D&D 5e SRD (System Reference Document)，遵循 Open Gaming License v1.0a。
