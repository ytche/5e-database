# D&D 5e 中文数据查询项目 - 代码规范与审查标准

> 版本：1.0.0  
> 最后更新：2026-02-25

---

## 目录

1. [代码风格规范](#1-代码风格规范)
2. [Git 工作流规范](#2-git-工作流规范)
3. [代码质量要求](#3-代码质量要求)
4. [Review Checklist](#4-review-checklist)
5. [项目特定规范](#5-项目特定规范)
6. [附录：配置文件](#6-附录配置文件)

---

## 1. 代码风格规范

### 1.1 JavaScript/TypeScript 规范

#### 基础规则

- **缩进**：2 个空格（禁止 Tab）
- **换行符**：LF (`\n`)
- **编码**：UTF-8（必须包含 BOM 以正确处理中文）
- **最大行宽**：100 字符
- **引号**：单引号（`'`）
- **分号**：必须添加
- **尾随逗号**：ES5 兼容模式（对象/数组最后一项不加逗号）

#### TypeScript 严格规则

```typescript
// tsconfig.json 推荐配置
{
  "compilerOptions": {
    "target": "ES2022",
    "module": "NodeNext",
    "moduleResolution": "NodeNext",
    "lib": ["ES2022"],
    "strict": true,
    "noImplicitAny": true,
    "strictNullChecks": true,
    "strictFunctionTypes": true,
    "strictBindCallApply": true,
    "strictPropertyInitialization": true,
    "noImplicitThis": true,
    "alwaysStrict": true,
    "noUnusedLocals": true,
    "noUnusedParameters": true,
    "noImplicitReturns": true,
    "noFallthroughCasesInSwitch": true,
    "esModuleInterop": true,
    "skipLibCheck": true,
    "forceConsistentCasingInFileNames": true,
    "resolveJsonModule": true,
    "declaration": true,
    "outDir": "./built"
  }
}
```

#### 命名规范

| 类型 | 命名风格 | 示例 | 说明 |
|------|---------|------|------|
| 变量 | camelCase | `userName`, `spellList` | 语义清晰，避免缩写 |
| 常量 | UPPER_SNAKE_CASE | `MAX_LEVEL`, `API_BASE_URL` | 全大写下划线分隔 |
| 函数 | camelCase | `getSpellById()`, `formatDescription()` | 动词开头 |
| 类/接口 | PascalCase | `SpellService`, `CharacterData` | 名词或名词短语 |
| 类型别名 | PascalCase | `SpellType`, `AbilityScore` | 使用 `type` 定义 |
| 枚举 | PascalCase | `DamageType`, `SchoolOfMagic` | 枚举值用 UPPER_SNAKE |
| 文件名 | kebab-case | `spell-service.ts`, `db-utils.ts` | 小写短横线分隔 |
| React 组件 | PascalCase | `SpellCard.tsx`, `CharacterSheet.tsx` | 组件文件用 .tsx |
| 测试文件 | `*.test.ts` | `spell-service.test.ts` | 与被测文件同名 |

#### 变量命名最佳实践

```typescript
// ✅ 推荐：语义清晰
const spellName = '火球术';
const characterLevel = 5;
const isConcentrationRequired = true;

// ❌ 避免：缩写或无意义名称
const sn = '火球术';  // 不清晰
const x = 5;          // 无意义
const flag = true;    // 太泛化
```

### 1.2 React 组件编写规范

#### 组件结构

```tsx
// SpellCard.tsx
import React, { useState, useCallback } from 'react';
import { Spell } from '@/types/spell';
import { formatRange } from '@/utils/formatters';

// 类型定义
interface SpellCardProps {
  spell: Spell;
  onCast?: (spell: Spell) => void;
  showDetails?: boolean;
}

// 组件定义
export const SpellCard: React.FC<SpellCardProps> = ({
  spell,
  onCast,
  showDetails = false,
}) => {
  // State 声明
  const [isExpanded, setIsExpanded] = useState(false);

  // Callback 函数
  const handleCast = useCallback(() => {
    onCast?.(spell);
  }, [onCast, spell]);

  // 渲染
  return (
    <div className="spell-card">
      <h3>{spell.name}</h3>
      {/* ... */}
    </div>
  );
};

// 默认导出（可选）
export default SpellCard;
```

#### React 规范要点

1. **函数组件**：使用箭头函数或普通函数，优先使用 `React.FC` 显式声明
2. **Hooks 规则**：
   - 只在最顶层调用 Hooks
   - 只在 React 函数中调用 Hooks
   - 自定义 Hooks 以 `use` 开头
3. **Props 解构**：在参数中直接解构
4. **事件处理**：使用 `handle` 前缀，如 `handleClick`, `handleSubmit`
5. **条件渲染**：避免在 JSX 中写复杂逻辑

```tsx
// ✅ 推荐
const renderSpellLevel = () => {
  if (spell.level === 0) return '戏法';
  return `${spell.level} 环法术`;
};

// ❌ 避免：JSX 中嵌套复杂逻辑
<div>
  {spell.level === 0 ? '戏法' : `${spell.level} 环法术`}
</div>
```

### 1.3 注释规范

#### JSDoc 规范

```typescript
/**
 * 根据索引获取法术详情
 * 
 * @param index - 法术的唯一索引标识
 * @param language - 语言代码，可选 'zh' 或 'en'，默认为 'zh'
 * @returns 法术对象，如未找到则返回 null
 * @throws {NotFoundError} 当法术索引不存在时抛出
 * 
 * @example
 * ```typescript
 * const spell = await getSpellByIndex('fireball', 'zh');
 * console.log(spell.name); // '火球术'
 * ```
 */
async function getSpellByIndex(
  index: string,
  language: 'zh' | 'en' = 'zh'
): Promise<Spell | null> {
  // 实现...
}
```

#### 注释规则

1. **必须注释**：
   - 所有公共 API 函数
   - 复杂的业务逻辑
   - 非直观的代码实现
   - 中文数据处理的特殊处理

2. **禁止注释**：
   - 显而易见的代码
   - 过时或错误的注释
   - 大段注释掉的代码

3. **中文注释**：允许并鼓励使用中文注释，特别是涉及 D&D 规则说明时

---

## 2. Git 工作流规范

### 2.1 分支命名规范

| 分支类型 | 命名格式 | 示例 |
|---------|---------|------|
| 主分支 | `main` | `main` |
| 功能分支 | `feature/<功能描述>` | `feature/spell-search`, `feature/monster-filter` |
| 修复分支 | `fix/<问题描述>` | `fix/typo-in-fireball`, `fix/api-timeout` |
| 热修复 | `hotfix/<紧急描述>` | `hotfix/critical-data-error` |
| 发布分支 | `release/<版本号>` | `release/4.2.0` |
| 文档分支 | `docs/<文档描述>` | `docs/update-api-guide` |
| 翻译分支 | `translate/<内容类型>` | `translate/spells-2014`, `translate/monsters-core` |

#### 命名规则

- 使用小写字母
- 使用短横线 `-` 分隔单词
- 使用英文描述（便于国际化协作）
- 描述简洁明了，避免过长

### 2.2 Commit Message 规范

遵循 [Conventional Commits](https://www.conventionalcommits.org/) 规范：

```
<type>(<scope>): <subject>

<body>

<footer>
```

#### 类型 (Type)

| 类型 | 说明 | 版本影响 |
|-----|------|---------|
| `feat` | 新功能 | Minor |
| `fix` | Bug 修复 | Patch |
| `docs` | 文档更新 | - |
| `style` | 代码格式调整（不影响功能） | - |
| `refactor` | 代码重构 | - |
| `perf` | 性能优化 | - |
| `test` | 测试相关 | - |
| `chore` | 构建/工具/依赖更新 | - |
| `data` | 数据更新/修正 | Patch |
| `i18n` | 国际化/翻译更新 | - |

#### 作用域 (Scope)

可选，用于说明影响范围：

- `api` - API 相关
- `data` - 数据文件
- `ui` - 用户界面
- `db` - 数据库脚本
- `search` - 搜索功能
- `spell` - 法术相关
- `monster` - 怪物相关
- `i18n` - 国际化
- `config` - 配置文件

#### 示例

```
feat(spell): 添加法术等级过滤功能

- 实现按等级筛选法术列表
- 支持多选和范围选择
- 添加相应的单元测试

Closes #123
```

```
fix(data): 修正火球术伤害骰数值

将火球术伤害从 8d6 修正为 8d6（原为错误的 6d6）

Fixes #456
```

```
data(i18n): 更新 2014 版法术中文翻译

- 补充缺失的法术描述
- 修正部分术语翻译
- 统一格式风格
```

### 2.3 PR（Pull Request）规范

#### PR 标题格式

```
[<type>]: <描述>
```

例如：
- `[feat]: 添加怪物图鉴搜索功能`
- `[fix]: 修复法术索引重复问题`
- `[data]: 补充 2024 版装备中文翻译`

#### PR 描述模板

```markdown
## 变更描述
<!-- 简要描述本次变更的内容 -->

## 相关 Issue
<!-- 关联的 Issue 编号，如 Fixes #123 -->

## 变更类型
- [ ] 新功能 (feat)
- [ ] Bug 修复 (fix)
- [ ] 数据更新 (data)
- [ ] 翻译更新 (i18n)
- [ ] 代码重构 (refactor)
- [ ] 文档更新 (docs)

## 检查清单
- [ ] 代码通过 ESLint 检查
- [ ] 单元测试全部通过
- [ ] 新增/修改的功能有相应测试
- [ ] 中文内容编码正确（UTF-8）
- [ ] API 文档已更新（如有变更）

## 测试说明
<!-- 如何验证本次变更 -->

## 截图（如适用）
<!-- UI 变更请提供截图 -->
```

#### PR 审查要求

1. 至少需要 **1 名**审查者批准
2. 必须通过 CI 检查（Lint + Test）
3. PR 描述必须完整填写
4. 冲突必须解决后才能合并
5. 使用 `Squash and Merge` 合并方式

---

## 3. 代码质量要求

### 3.1 单元测试覆盖率要求

| 指标 | 最低要求 | 推荐目标 |
|-----|---------|---------|
| 行覆盖率 (Lines) | 70% | 85% |
| 分支覆盖率 (Branches) | 60% | 75% |
| 函数覆盖率 (Functions) | 80% | 90% |
| 语句覆盖率 (Statements) | 70% | 85% |

#### 测试文件规范

```typescript
// spell-service.test.ts
import { describe, it, expect, beforeEach, vi } from 'vitest';
import { SpellService } from './spell-service';
import { mockSpells } from '@/tests/fixtures/spells';

describe('SpellService', () => {
  let service: SpellService;

  beforeEach(() => {
    service = new SpellService();
  });

  describe('getSpellByIndex', () => {
    it('应该根据索引返回正确的法术', async () => {
      const spell = await service.getSpellByIndex('fireball');
      expect(spell).toBeDefined();
      expect(spell?.name).toBe('火球术');
    });

    it('当法术不存在时应返回 null', async () => {
      const spell = await service.getSpellByIndex('non-existent');
      expect(spell).toBeNull();
    });

    it('应该正确处理中文法术名称查询', async () => {
      const spell = await service.getSpellByIndex('火球术');
      expect(spell?.index).toBe('fireball');
    });
  });
});
```

#### 测试命名规范

- 测试套件：`describe('<被测对象>', () => {})`
- 测试用例：`it('应该...当...', () => {})` 或 `it('should...when...', () => {})`
- 使用中文描述测试意图（推荐）

### 3.2 代码复杂度限制

| 指标 | 警告阈值 | 错误阈值 |
|-----|---------|---------|
| 圈复杂度 (Cyclomatic) | 10 | 15 |
| 认知复杂度 (Cognitive) | 8 | 12 |
| 函数行数 | 50 | 100 |
| 文件行数 | 300 | 500 |
| 类成员数 | 15 | 20 |
| 参数个数 | 4 | 6 |

#### 复杂度优化示例

```typescript
// ❌ 高复杂度 - 需要优化
function processSpellData(data: any, mode: string, lang: string) {
  if (mode === 'create') {
    if (lang === 'zh') {
      // ... 大量逻辑
    } else if (lang === 'en') {
      // ... 大量逻辑
    }
  } else if (mode === 'update') {
    // ... 更多逻辑
  }
  // ... 更多分支
}

// ✅ 优化后 - 拆分函数，降低复杂度
function createSpell(data: SpellInput, lang: Language): Spell {
  return lang === 'zh' ? createZhSpell(data) : createEnSpell(data);
}

function updateSpell(data: SpellInput, lang: Language): Spell {
  // 更新逻辑
}
```

### 3.3 TypeScript 类型严格程度

#### 强制规则

```typescript
// ✅ 必须显式声明函数返回值
function calculateDamage(dice: number, sides: number): number {
  return dice * (sides + 1) / 2;
}

// ❌ 禁止隐式 any
function badFunction(x) {  // Error!
  return x + 1;
}

// ✅ 必须处理 null/undefined
function getSpellName(spell: Spell | null): string {
  return spell?.name ?? '未知法术';
}

// ✅ 枚举必须使用 const 或完整定义
const enum DamageType {
  Fire = 'fire',
  Cold = 'cold',
  Lightning = 'lightning',
}

// ✅ 接口必须使用明确类型
interface Spell {
  index: string;
  name: string;
  nameEn: string;
  level: number;
  school: MagicSchool;
  castingTime: string;
  range: string;
  components: Component[];
  duration: string;
  description: string;
  higherLevels?: string;
}
```

---

## 4. Review Checklist

### 4.1 每次审查必须检查的项目

#### 基础检查

- [ ] 代码是否遵循命名规范
- [ ] 是否包含适当的注释和文档
- [ ] 是否处理了所有错误情况
- [ ] 是否有未使用的变量或导入
- [ ] 是否有调试代码或 console.log 遗留

#### TypeScript 检查

- [ ] 是否使用了适当的类型（无隐式 any）
- [ ] 接口定义是否完整
- [ ] 可选属性是否正确标记
- [ ] 是否处理了 null/undefined

#### 测试检查

- [ ] 是否包含单元测试
- [ ] 测试是否覆盖了主要分支
- [ ] 测试断言是否明确
- [ ] 是否使用了适当的 mock

#### 性能检查

- [ ] 是否有明显的性能问题（如循环中的重复计算）
- [ ] 是否有内存泄漏风险
- [ ] 是否有不必要的重新渲染（React）
- [ ] 数据库查询是否优化

#### 安全与数据检查

- [ ] 输入数据是否经过验证
- [ ] 中文内容编码是否正确（UTF-8）
- [ ] JSON 数据格式是否正确
- [ ] 索引是否唯一

### 4.2 常见代码坏味道及避免方法

| 坏味道 | 示例 | 解决方案 |
|-------|------|---------|
| **魔法数字** | `if (level > 20)` | 使用常量 `MAX_CHARACTER_LEVEL` |
| **过长函数** | 函数超过 100 行 | 拆分为多个小函数 |
| **重复代码** | 相同逻辑多处出现 | 提取为公共函数 |
| **深层嵌套** | `if` 嵌套超过 3 层 | 提前返回，使用卫语句 |
| ** God Object ** | 一个类处理所有事情 | 拆分职责，使用组合 |
| **字符串硬编码** | `type === 'fire'` | 使用枚举或常量 |
| **空值判断缺失** | `data.name.length` | 使用可选链 `data?.name?.length` |
| **类型断言滥用** | `data as Spell` | 使用类型守卫或正确类型定义 |
| **回调地狱** | 多层嵌套回调 | 使用 async/await |
| **可变状态** | 直接修改对象属性 | 使用不可变更新 |

#### 代码坏味道示例与修复

```typescript
// ❌ 坏味道：魔法数字 + 深层嵌套
function canCastSpell(spell: Spell, character: Character) {
  if (character) {
    if (character.level) {
      if (character.level >= 5) {
        return true;
      }
    }
  }
  return false;
}

// ✅ 修复后
const MIN_SPELL_LEVEL = 5;

function canCastSpell(spell: Spell, character?: Character): boolean {
  return (character?.level ?? 0) >= MIN_SPELL_LEVEL;
}
```

```typescript
// ❌ 坏味道：重复代码
function processFireSpell(spell: Spell) {
  const damage = spell.damage;
  const range = spell.range;
  console.log(`火球术: 伤害 ${damage}, 范围 ${range}`);
}

function processIceSpell(spell: Spell) {
  const damage = spell.damage;
  const range = spell.range;
  console.log(`冰风暴: 伤害 ${damage}, 范围 ${range}`);
}

// ✅ 修复后
function processSpell(spell: Spell): void {
  const { damage, range, name } = spell;
  console.log(`${name}: 伤害 ${damage}, 范围 ${range}`);
}
```

---

## 5. 项目特定规范

### 5.1 API 数据处理规范

#### 数据文件结构

```
src/
├── 2014/           # 英文源数据（2014版规则）
├── 2014-zh/        # 中文翻译数据
├── 2014-final/     # 合并后的最终数据
└── 2024/           # 2024版规则数据
```

#### JSON 数据规范

```json
{
  "index": "fireball",           // 唯一索引，小写，短横线分隔
  "name": "火球术",               // 中文名称
  "name_en": "Fireball",         // 英文原名
  "level": 3,                    // 法术等级
  "school": {                     // 嵌套对象引用
    "index": "evocation",
    "name": "塑能",
    "name_en": "Evocation",
    "url": "/api/2014/magic-schools/evocation"
  },
  "url": "/api/2014/spells/fireball"  // API 路径
}
```

#### 数据处理规则

1. **索引规范**：
   - 全部小写
   - 空格替换为短横线 `-`
   - 无特殊字符
   - 示例：`'magic missile'` → `'magic-missile'`

2. **URL 规范**：
   - 格式：`/api/{version}/{resource}/{index}`
   - 版本：`2014` 或 `2024`
   - 资源：复数形式，如 `spells`, `monsters`

3. **名称规范**：
   - `name`: 中文名称
   - `name_en`: 英文原名
   - 保持官方术语翻译一致性

4. **数据验证**：
   - 所有 JSON 必须通过 schema 验证
   - 索引必须唯一
   - URL 引用必须有效

### 5.2 中文内容显示处理

#### 编码规范

1. **文件编码**：UTF-8 with BOM
2. **HTTP 响应头**：`Content-Type: application/json; charset=utf-8`
3. **HTML meta**：`<meta charset="UTF-8">`

#### 字体规范

```css
/* 推荐字体栈 */
font-family: 
  "Noto Sans SC",    /* 思源黑体（首选） */
  "PingFang SC",     /* 苹方（macOS） */
  "Microsoft YaHei", /* 微软雅黑（Windows） */
  "WenQuanYi Micro Hei", /* 文泉驿（Linux） */
  sans-serif;
```

#### 中文排版规范

1. **标点符号**：使用全角中文标点
2. **数字与字母**：与中文之间保留空格
3. **术语统一**：使用统一的 D&D 术语翻译表

```typescript
// ✅ 正确的中文内容处理
const spellDescription = '造成 8d6 点火焰伤害，范围 20 尺半径。';

// ❌ 错误：数字紧贴中文
const badDescription = '造成8d6点火焰伤害，范围20尺半径。';
```

#### 术语翻译表（部分）

| 英文 | 中文 | 说明 |
|-----|------|------|
| Ability Score | 属性值 | 力量、敏捷等 |
| Advantage | 优势 | 掷骰机制 |
| Saving Throw | 豁免 | 避免效果的掷骰 |
| Spell Slot | 法术位 | 施法资源 |
| Concentration | 专注 | 维持法术的机制 |
| Cantrip | 戏法 | 0 级法术 |
| Proficiency | 熟练 | 技能/装备熟练 |

### 5.3 性能优化最佳实践

#### 数据加载优化

```typescript
// ✅ 推荐：延迟加载 + 缓存
class DataService {
  private cache = new Map<string, any>();
  
  async getData<T>(key: string, loader: () => Promise<T>): Promise<T> {
    if (this.cache.has(key)) {
      return this.cache.get(key);
    }
    const data = await loader();
    this.cache.set(key, data);
    return data;
  }
}
```

#### 搜索优化

```typescript
// ✅ 推荐：使用索引 + 防抖
import { debounce } from 'lodash-es';

class SearchService {
  private searchIndex: Map<string, string[]> = new Map();
  
  // 预构建搜索索引
  buildIndex(items: SearchableItem[]) {
    items.forEach(item => {
      const keywords = this.extractKeywords(item);
      keywords.forEach(keyword => {
        if (!this.searchIndex.has(keyword)) {
          this.searchIndex.set(keyword, []);
        }
        this.searchIndex.get(keyword)!.push(item.index);
      });
    });
  }
  
  // 防抖搜索
  search = debounce((query: string) => {
    return this.performSearch(query);
  }, 300);
}
```

#### React 性能优化

```tsx
// ✅ 推荐：使用 memo + useMemo + useCallback
import { memo, useMemo, useCallback } from 'react';

interface SpellListProps {
  spells: Spell[];
  onSelect: (spell: Spell) => void;
}

export const SpellList = memo(({ spells, onSelect }: SpellListProps) => {
  // 缓存排序结果
  const sortedSpells = useMemo(() => {
    return [...spells].sort((a, b) => a.level - b.level);
  }, [spells]);
  
  // 缓存回调
  const handleSelect = useCallback((spell: Spell) => {
    onSelect(spell);
  }, [onSelect]);
  
  return (
    <ul>
      {sortedSpells.map(spell => (
        <SpellItem 
          key={spell.index} 
          spell={spell} 
          onSelect={handleSelect}
        />
      ))}
    </ul>
  );
});
```

#### MongoDB 优化

```typescript
// ✅ 推荐：创建适当的索引
// 在 dbRefresh.ts 或迁移脚本中
async function createIndexes(db: Db) {
  // 单字段索引
  await db.collection('spells').createIndex({ index: 1 }, { unique: true });
  await db.collection('spells').createIndex({ level: 1 });
  await db.collection('spells').createIndex({ school: 1 });
  
  // 复合索引（用于筛选查询）
  await db.collection('spells').createIndex({ level: 1, school: 1 });
  
  // 文本索引（用于全文搜索）
  await db.collection('spells').createIndex(
    { name: 'text', name_en: 'text', description: 'text' },
    { default_language: 'chinese' }
  );
}
```

---

## 6. 附录：配置文件

### 6.1 ESLint 配置（eslint.config.mjs）

```javascript
// @ts-check

import eslint from '@eslint/js';
import tseslint from 'typescript-eslint';
import eslintPluginVitest from 'eslint-plugin-vitest';
import eslintPluginPrettier from 'eslint-plugin-prettier/recommended';
import json from 'eslint-plugin-json';
import globals from 'globals';

export default [
  {
    name: 'base',
    ignores: ['**/node_modules/**', '**/dist/**', '**/built/**', '**/coverage/**'],
  },
  // JavaScript 配置
  {
    name: 'js/recommended',
    files: ['**/*.js'],
    languageOptions: {
      globals: {
        ...globals.node,
      },
    },
    rules: {
      ...eslint.configs.recommended.rules,
      'no-unused-vars': ['warn', { argsIgnorePattern: '^_' }],
      'no-undef': 'warn',
      'no-console': ['warn', { allow: ['error', 'warn', 'info'] }],
      'prefer-const': 'error',
      'no-var': 'error',
    },
  },
  // TypeScript 配置
  ...tseslint.configs.recommended.map(config => ({
    ...config,
    files: ['**/*.ts', '**/*.tsx'],
  })),
  {
    name: 'ts/strict',
    files: ['**/*.ts', '**/*.tsx'],
    languageOptions: {
      parser: tseslint.parser,
      parserOptions: {
        project: './scripts/tsconfig.json',
      },
    },
    rules: {
      '@typescript-eslint/explicit-function-return-type': 'warn',
      '@typescript-eslint/no-explicit-any': 'error',
      '@typescript-eslint/no-unused-vars': ['warn', { argsIgnorePattern: '^_' }],
      '@typescript-eslint/prefer-nullish-coalescing': 'error',
      '@typescript-eslint/prefer-optional-chain': 'error',
      '@typescript-eslint/strict-boolean-expressions': 'warn',
    },
  },
  // 测试文件配置
  {
    name: 'vitest/recommended',
    files: ['**/*.test.{js,ts}', '**/*.spec.{js,ts}'],
    ...eslintPluginVitest.configs['flat/recommended'],
    languageOptions: {
      globals: {
        ...eslintPluginVitest.environments.env.globals,
      },
    },
    rules: {
      '@typescript-eslint/no-explicit-any': 'off', // 测试中允许 any
    },
  },
  // JSON 配置
  {
    name: 'json/recommended',
    files: ['**/*.json'],
    ...json.configs['recommended'],
    rules: {
      'json/*': ['warn', { allowComments: false }],
    },
  },
  // Prettier 配置（放在最后）
  eslintPluginPrettier,
];
```

### 6.2 Prettier 配置（.prettierrc）

```json
{
  "printWidth": 100,
  "tabWidth": 2,
  "useTabs": false,
  "semi": true,
  "singleQuote": true,
  "quoteProps": "as-needed",
  "trailingComma": "es5",
  "bracketSpacing": true,
  "bracketSameLine": false,
  "arrowParens": "always",
  "endOfLine": "lf",
  "embeddedLanguageFormatting": "auto"
}
```

### 6.3 TypeScript 配置（tsconfig.json）

```json
{
  "compilerOptions": {
    "target": "ES2022",
    "module": "NodeNext",
    "moduleResolution": "NodeNext",
    "lib": ["ES2022"],
    "outDir": "./built",
    "rootDir": ".",
    "strict": true,
    "noImplicitAny": true,
    "strictNullChecks": true,
    "strictFunctionTypes": true,
    "strictBindCallApply": true,
    "strictPropertyInitialization": true,
    "noImplicitThis": true,
    "alwaysStrict": true,
    "noUnusedLocals": true,
    "noUnusedParameters": true,
    "noImplicitReturns": true,
    "noFallthroughCasesInSwitch": true,
    "esModuleInterop": true,
    "skipLibCheck": true,
    "forceConsistentCasingInFileNames": true,
    "resolveJsonModule": true,
    "declaration": true,
    "declarationMap": true,
    "sourceMap": true,
    "removeComments": false
  },
  "include": ["**/*.ts"],
  "exclude": ["node_modules", "built", "dist"]
}
```

### 6.4 Vitest 配置（vitest.config.ts）

```typescript
import { defineConfig } from 'vitest/config';

export default defineConfig({
  test: {
    include: ['**/*.test.{js,ts}'],
    exclude: ['node_modules/**', 'built/**', 'dist/**'],
    environment: 'node',
    globals: true,
    coverage: {
      provider: 'v8',
      reporter: ['text', 'json', 'html'],
      exclude: [
        'node_modules/**',
        'coverage/**',
        'dist/**',
        'built/**',
        '*.config.{js,ts}',
        'scripts/dbUtils.ts',
      ],
      thresholds: {
        lines: 70,
        functions: 80,
        branches: 60,
        statements: 70,
      },
    },
  },
});
```

### 6.5 Husky + lint-staged 配置

package.json 中添加：

```json
{
  "husky": {
    "hooks": {
      "pre-commit": "lint-staged",
      "commit-msg": "commitlint -E HUSKY_GIT_PARAMS"
    }
  },
  "lint-staged": {
    "*.{js,ts,tsx}": [
      "eslint --fix",
      "prettier --write",
      "vitest related --run"
    ],
    "*.json": [
      "prettier --write",
      "eslint --fix"
    ],
    "*.{md,mdx}": [
      "prettier --write"
    ]
  }
}
```

### 6.6 Commitlint 配置（commitlint.config.js）

```javascript
module.exports = {
  extends: ['@commitlint/config-conventional'],
  rules: {
    'type-enum': [
      2,
      'always',
      [
        'feat',
        'fix',
        'docs',
        'style',
        'refactor',
        'perf',
        'test',
        'chore',
        'data',
        'i18n',
      ],
    ],
    'scope-enum': [
      0,
      'always',
      [
        'api',
        'data',
        'ui',
        'db',
        'search',
        'spell',
        'monster',
        'i18n',
        'config',
        'deps',
      ],
    ],
    'subject-full-stop': [0, 'never'],
    'subject-case': [0, 'never'],
  },
};
```

---

## 总结

本规范旨在确保 D&D 5e 中文数据查询项目的代码质量、可维护性和团队协作效率。所有团队成员都应熟悉并遵循这些规范。

### 快速检查清单

提交代码前，请确认：

- [ ] `npm run lint` 无错误
- [ ] `npm test` 全部通过
- [ ] 代码覆盖率符合要求
- [ ] Commit message 符合规范
- [ ] 中文内容编码正确

### 相关链接

- [Conventional Commits](https://www.conventionalcommits.org/)
- [TypeScript 官方文档](https://www.typescriptlang.org/docs/)
- [ESLint 规则](https://eslint.org/docs/rules/)
- [Prettier 选项](https://prettier.io/docs/en/options.html)

---

*本规范由代码审查团队制定，如有疑问请在团队讨论区提出。*
