# D&D 5e 车卡系统架构设计

## 1. 架构概览

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                              平台适配层 (Platform)                             │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐        │
│  │   Web App   │  │   微信小程序 │  │   Mobile    │  │   Desktop   │        │
│  └──────┬──────┘  └──────┬──────┘  └──────┬──────┘  └──────┬──────┘        │
└─────────┼────────────────┼────────────────┼────────────────┼───────────────┘
          │                │                │                │
          └────────────────┴───────┬────────┴────────────────┘
                                   │
┌──────────────────────────────────▼──────────────────────────────────────────┐
│                           核心引擎层 (Core Engine)                           │
│  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────────────────┐ │
│  │   Builder State │  │  Validation     │  │   Character Calculator      │ │
│  │   Machine       │  │  Engine         │  │   (属性/HP/AC计算)            │ │
│  └─────────────────┘  └─────────────────┘  └─────────────────────────────┘ │
│  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────────────────┐ │
│  │   Step Registry │  │   Plugin System │  │   Export Manager            │ │
│  │                 │  │                 │  │                             │ │
│  └─────────────────┘  └─────────────────┘  └─────────────────────────────┘ │
└──────────────────────────────────┬──────────────────────────────────────────┘
                                   │
┌──────────────────────────────────▼──────────────────────────────────────────┐
│                            数据管理层 (Data Layer)                           │
│  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────────────────┐ │
│  │   Data Registry │  │  Version        │  │   Lazy Loader               │ │
│  │                 │  │  Manager        │  │   (按需加载)                  │ │
│  └─────────────────┘  └─────────────────┘  └─────────────────────────────┘ │
│  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────────────────┐ │
│  │   SRD Core      │  │  Extensions     │  │   Homebrew                  │ │
│  │   (2014/2024)   │  │  (XGE/TCE等)    │  │   (用户自定义)                │ │
│  └─────────────────┘  └─────────────────┘  └─────────────────────────────┘ │
└─────────────────────────────────────────────────────────────────────────────┘
```

## 2. 核心设计原则

### 2.1 单一职责原则 (SRP)
- 每个模块只做一件事，且做好
- 数据、逻辑、UI 严格分离

### 2.2 开闭原则 (OCP)
- 对扩展开放：通过插件机制添加新内容
- 对修改关闭：核心引擎不随内容扩展而修改

### 2.3 依赖倒置原则 (DIP)
- 高层模块依赖抽象接口，不依赖具体实现
- 具体实现通过依赖注入配置

### 2.4 组合优于继承
- 使用组合构建角色能力
- 避免深度继承层次

## 3. 数据层架构

### 3.1 数据版本管理

```typescript
// types/data-source.ts

/**
 * 数据源类型
 */
export enum DataSourceType {
  CORE = 'core',           // 核心SRD
  EXTENSION = 'extension', // 官方扩展
  HOMEBREW = 'homebrew',   // 用户自定义
}

/**
 * 数据来源标识
 */
export interface DataSource {
  id: string;              // 唯一标识: "srd-2014", "xge", "tce", "my-homebrew"
  type: DataSourceType;
  name: string;            // 显示名称
  version: string;         // 版本号
  dependencies?: string[]; // 依赖的其他数据源
  priority: number;        // 优先级（冲突解决）
  enabled: boolean;        // 是否启用
  metadata: {
    author?: string;
    description?: string;
    coverImage?: string;
    releaseDate?: string;
    license?: string;
  };
}

/**
 * 带来源标识的数据项
 */
export interface SourcedData<T> {
  source: DataSource;
  data: T;
  overrides?: string[];    // 此数据覆盖的其他数据ID
}
```

### 3.2 数据注册表

```typescript
// core/data-registry.ts

export class DataRegistry {
  private sources: Map<string, DataSource> = new Map();
  private dataStores: Map<string, DataStore<unknown>> = new Map();
  
  // 注册数据源
  registerSource(source: DataSource): void;
  
  // 启用/禁用数据源
  enableSource(sourceId: string): void;
  disableSource(sourceId: string): void;
  
  // 获取有效数据（按优先级合并）
  getActiveData<T>(type: DataType): SourcedData<T>[];
  
  // 获取特定来源的数据
  getDataBySource<T>(type: DataType, sourceId: string): T[];
  
  // 检查数据冲突
  detectConflicts(type: DataType): DataConflict[];
  
  // 解决冲突（按优先级或手动选择）
  resolveConflicts(conflicts: DataConflict[]): void;
}

// 数据类型枚举
export enum DataType {
  RACE = 'races',
  SUBRACE = 'subraces',
  CLASS = 'classes',
  SUBCLASS = 'subclasses',
  BACKGROUND = 'backgrounds',
  SPELL = 'spells',
  FEAT = 'feats',
  EQUIPMENT = 'equipment',
  // ... 更多
}
```

### 3.3 懒加载策略

```typescript
// core/lazy-loader.ts

export interface LoadStrategy {
  // 预加载策略
  preload(): Promise<void>;
  // 按需加载
  load<T>(type: DataType, id: string): Promise<T>;
  // 批量加载
  loadBatch<T>(type: DataType, ids: string[]): Promise<T[]>;
  // 搜索加载
  loadByQuery<T>(type: DataType, query: DataQuery): Promise<T[]>;
}

/**
 * 分层加载策略
 */
export class TieredLoadStrategy implements LoadStrategy {
  // Tier 1: 核心元数据（立即加载）- 种族/职业列表、名称、图标
  // Tier 2: 详细数据（按需加载）- 具体种族/职业的完整数据
  // Tier 3: 关联数据（懒加载）- 法术、装备等
  
  async preload(): Promise<void> {
    // 只加载Tier 1数据
    await this.loadTier1Data();
  }
  
  async load<T>(type: DataType, id: string): Promise<T> {
    // 检查缓存 -> 加载 -> 缓存 -> 返回
  }
}

/**
 * 缓存策略
 */
export interface CacheStrategy {
  get<T>(key: string): T | undefined;
  set<T>(key: string, value: T, ttl?: number): void;
  invalidate(key: string): void;
  invalidateByPattern(pattern: RegExp): void;
}
```

## 4. 车卡流程架构

### 4.1 步骤系统

```typescript
// builder/steps/step-system.ts

/**
 * 车卡步骤接口
 */
export interface BuilderStep {
  id: string;
  name: string;
  order: number;
  
  // 条件显示：是否在当前角色状态下显示此步骤
  shouldShow(context: BuildContext): boolean;
  
  // 依赖检查：前置步骤是否完成
  checkDependencies(context: BuildContext): DependencyResult;
  
  // 验证当前步骤是否完成
  validate(context: BuildContext): ValidationResult;
  
  // 获取此步骤的可用选项
  getOptions(context: BuildContext): StepOption[];
  
  // 执行步骤（应用选择）
  execute(context: BuildContext, selection: unknown): BuildContext;
  
  // 撤销步骤
  rollback(context: BuildContext): BuildContext;
}

/**
 * 步骤注册表
 */
export class StepRegistry {
  private steps: Map<string, BuilderStep> = new Map();
  
  register(step: BuilderStep): void;
  unregister(stepId: string): void;
  
  // 获取所有活跃步骤（按order排序）
  getActiveSteps(context: BuildContext): BuilderStep[];
  
  // 获取特定步骤
  getStep(id: string): BuilderStep | undefined;
}
```

### 4.2 内置步骤实现

```typescript
// builder/steps/select-race-step.ts

export class SelectRaceStep implements BuilderStep {
  id = 'select-race';
  name = '选择种族';
  order = 10;
  
  shouldShow(context: BuildContext): boolean {
    return true; // 始终显示
  }
  
  checkDependencies(): DependencyResult {
    return { satisfied: true }; // 无依赖
  }
  
  validate(context: BuildContext): ValidationResult {
    return context.character.race 
      ? { valid: true }
      : { valid: false, errors: ['请选择种族'] };
  }
  
  getOptions(context: BuildContext): StepOption[] {
    const races = dataRegistry.getActiveData<Race>(DataType.RACE);
    return races.map(r => ({
      id: r.data.index,
      name: r.data.name,
      description: r.data.desc,
      icon: r.data.icon,
      source: r.source,
      // 扩展信息
      details: {
        abilityBonuses: r.data.ability_bonuses,
        speed: r.data.speed,
        size: r.data.size,
      }
    }));
  }
  
  execute(context: BuildContext, selection: RaceSelection): BuildContext {
    const race = dataRegistry.getById(DataType.RACE, selection.raceId);
    
    return produce(context, draft => {
      draft.character.race = {
        index: race.index,
        name: race.name,
        subrace: selection.subraceId,
      };
      
      // 应用种族属性加成
      race.ability_bonuses?.forEach(bonus => {
        draft.character.abilityBonuses[bonus.ability_score.index] = 
          (draft.character.abilityBonuses[bonus.ability_score.index] || 0) + bonus.bonus;
      });
      
      // 应用种族特性
      draft.character.traits.push(...race.traits.map(t => t.index));
      
      // 应用语言
      draft.character.languages.push(...race.languages.map(l => l.index));
    });
  }
}

// builder/steps/select-spells-step.ts

export class SelectSpellsStep implements BuilderStep {
  id = 'select-spells';
  name = '选择法术';
  order = 50;
  
  shouldShow(context: BuildContext): boolean {
    // 只有施法者才显示此步骤
    const cls = dataRegistry.getById(DataType.CLASS, context.character.class?.index);
    return cls?.spellcasting !== undefined;
  }
  
  checkDependencies(context: BuildContext): DependencyResult {
    if (!context.character.class) {
      return { satisfied: false, blockingSteps: ['select-class'] };
    }
    return { satisfied: true };
  }
  
  getOptions(context: BuildContext): SpellOption[] {
    const cls = dataRegistry.getById(DataType.CLASS, context.character.class.index);
    const spellcasting = cls.spellcasting;
    
    // 根据施法者类型获取可用法术
    const availableSpells = this.getSpellsForClass(cls.index);
    
    // 根据等级筛选
    const maxSpellLevel = this.getMaxSpellLevel(context.character.level, spellcasting);
    
    return availableSpells
      .filter(s => s.level <= maxSpellLevel)
      .map(s => ({
        id: s.index,
        name: s.name,
        level: s.level,
        school: s.school,
        description: s.desc[0],
      }));
  }
}
```

### 4.3 车卡状态机

```typescript
// builder/state-machine.ts

export interface BuildContext {
  version: string;                    // 构建版本
  character: Partial<Character>;      // 当前角色状态
  completedSteps: string[];           // 已完成步骤
  currentStepId: string | null;       // 当前步骤
  history: BuildAction[];             // 操作历史（用于撤销）
  metadata: {
    createdAt: Date;
    modifiedAt: Date;
    dataSources: string[];            // 使用的数据源
  };
}

export type BuildAction = 
  | { type: 'SELECT_RACE'; payload: RaceSelection }
  | { type: 'SELECT_CLASS'; payload: ClassSelection }
  | { type: 'ALLOCATE_ABILITIES'; payload: AbilityAllocation }
  | { type: 'SELECT_BACKGROUND'; payload: BackgroundSelection }
  | { type: 'SELECT_SPELLS'; payload: SpellSelection }
  | { type: 'SELECT_FEATS'; payload: FeatSelection }
  | { type: 'BUY_EQUIPMENT'; payload: EquipmentPurchase }
  | { type: 'UNDO' }
  | { type: 'REDO' };

export class CharacterBuilderStateMachine {
  private context: BuildContext;
  private stepRegistry: StepRegistry;
  private listeners: Set<(context: BuildContext) => void> = new Set();
  
  constructor(stepRegistry: StepRegistry) {
    this.stepRegistry = stepRegistry;
    this.context = this.createInitialContext();
  }
  
  // 执行动作
  dispatch(action: BuildAction): void {
    const newContext = this.reducer(this.context, action);
    this.context = newContext;
    this.notifyListeners();
  }
  
  private reducer(context: BuildContext, action: BuildAction): BuildContext {
    switch (action.type) {
      case 'SELECT_RACE':
        return this.handleSelectRace(context, action.payload);
      case 'SELECT_CLASS':
        return this.handleSelectClass(context, action.payload);
      // ... 其他动作
      case 'UNDO':
        return this.handleUndo(context);
      default:
        return context;
    }
  }
  
  // 获取当前可用步骤
  getAvailableSteps(): BuilderStep[] {
    const allSteps = this.stepRegistry.getAllSteps();
    return allSteps
      .filter(step => step.shouldShow(this.context))
      .filter(step => step.checkDependencies(this.context).satisfied)
      .sort((a, b) => a.order - b.order);
  }
  
  // 验证整个构建
  validateBuild(): ValidationResult {
    const steps = this.getAvailableSteps();
    const results = steps.map(step => step.validate(this.context));
    
    return {
      valid: results.every(r => r.valid),
      stepResults: results,
    };
  }
  
  // 导出最终角色卡
  exportCharacter(): Character {
    const validation = this.validateBuild();
    if (!validation.valid) {
      throw new Error('Character build is incomplete');
    }
    
    return characterCalculator.calculateFinal(this.context.character);
  }
}
```

## 5. 插件/扩展机制

### 5.1 扩展包规范

```typescript
// plugin/extension-manifest.ts

/**
 * 扩展包清单
 */
export interface ExtensionManifest {
  id: string;                    // 唯一标识
  name: string;                  // 显示名称
  version: string;               // 语义化版本
  description?: string;
  author?: string;
  
  // 依赖声明
  dependencies: {
    core?: string;              // 需要的数据核心版本
    extensions?: string[];      // 依赖的其他扩展
  };
  
  // 数据文件
  dataFiles: {
    [key in DataType]?: string; // 数据类型 -> 文件路径
  };
  
  // 自定义步骤
  customSteps?: CustomStepDefinition[];
  
  // 规则覆盖
  ruleOverrides?: RuleOverride[];
  
  // 自定义验证器
  validators?: string[];
  
  // 自定义计算器
  calculators?: string[];
}

/**
 * 自定义步骤定义
 */
export interface CustomStepDefinition {
  id: string;
  name: string;
  order: number;
  condition?: {              // 显示条件
    requiresClass?: string[];
    requiresRace?: string[];
    requiresLevel?: { min?: number; max?: number };
    customScript?: string;   // 自定义条件脚本
  };
  optionsProvider: string;   // 选项提供函数
  executor: string;          // 执行函数
}
```

### 5.2 扩展包加载器

```typescript
// plugin/extension-loader.ts

export class ExtensionLoader {
  private registry: DataRegistry;
  private stepRegistry: StepRegistry;
  
  async loadExtension(manifest: ExtensionManifest, data: ExtensionData): Promise<void> {
    // 1. 验证依赖
    await this.validateDependencies(manifest);
    
    // 2. 注册数据源
    const source: DataSource = {
      id: manifest.id,
      type: DataSourceType.EXTENSION,
      name: manifest.name,
      version: manifest.version,
      dependencies: manifest.dependencies.extensions,
      priority: 100,
      enabled: true,
      metadata: {
        author: manifest.author,
        description: manifest.description,
      },
    };
    this.registry.registerSource(source);
    
    // 3. 加载数据文件
    for (const [dataType, filePath] of Object.entries(manifest.dataFiles)) {
      const data = await this.loadDataFile(filePath);
      this.registry.loadData(dataType as DataType, source.id, data);
    }
    
    // 4. 注册自定义步骤
    for (const stepDef of manifest.customSteps || []) {
      const step = this.createCustomStep(stepDef, data.scripts);
      this.stepRegistry.register(step);
    }
    
    // 5. 注册规则覆盖
    for (const override of manifest.ruleOverrides || []) {
      ruleEngine.registerOverride(override);
    }
    
    // 6. 注册自定义验证器
    for (const validatorPath of manifest.validators || []) {
      const validator = await this.loadScript(validatorPath);
      validationEngine.registerValidator(validator);
    }
  }
  
  // 从URL加载扩展（支持本地文件、CDN、用户上传）
  async loadFromURL(url: string): Promise<void>;
  
  // 从本地文件加载（桌面端）
  async loadFromFile(file: File): Promise<void>;
  
  // 从微信小程序存储加载
  async loadFromWXStorage(key: string): Promise<void>;
}
```

### 5.3 运行时脚本安全

```typescript
// plugin/sandbox.ts

/**
 * 沙箱执行环境
 * 用于执行扩展包中的自定义脚本
 */
export class ScriptSandbox {
  private allowedGlobals: Set<string> = new Set([
    'Math', 'JSON', 'Array', 'Object', 'String', 'Number', 'Date'
  ]);
  
  execute<T>(code: string, context: SandboxContext): T {
    // 使用 Web Worker 或 vm2 (Node) 隔离执行
    // 限制访问：只能访问上下文提供的数据和API
    
    const sandbox = {
      ...this.createSafeGlobals(),
      context: context,
      api: this.createSafeAPI(),
    };
    
    return this.runInSandbox(code, sandbox);
  }
  
  private createSafeAPI() {
    return {
      // 只暴露必要的API
      getData: (type: DataType, id: string) => {
        return dataRegistry.getById(type, id);
      },
      log: (...args: unknown[]) => {
        console.log('[Extension]', ...args);
      },
      // ... 其他安全API
    };
  }
}
```

## 6. 验证规则系统

### 6.1 可扩展验证器

```typescript
// validation/validation-engine.ts

export interface ValidationRule {
  id: string;
  name: string;
  
  // 适用条件
  appliesTo: (context: BuildContext) => boolean;
  
  // 验证逻辑
  validate: (context: BuildContext) => ValidationError[];
  
  // 自动修复（可选）
  autoFix?: (context: BuildContext) => BuildContext;
  
  // 严重程度
  severity: 'error' | 'warning' | 'info';
}

export class ValidationEngine {
  private rules: ValidationRule[] = [];
  
  registerRule(rule: ValidationRule): void {
    this.rules.push(rule);
  }
  
  unregisterRule(ruleId: string): void {
    this.rules = this.rules.filter(r => r.id !== ruleId);
  }
  
  validate(context: BuildContext): ValidationResult {
    const allErrors: ValidationError[] = [];
    
    for (const rule of this.rules) {
      if (rule.appliesTo(context)) {
        const errors = rule.validate(context);
        allErrors.push(...errors.map(e => ({ ...e, severity: rule.severity })));
      }
    }
    
    return {
      valid: !allErrors.some(e => e.severity === 'error'),
      errors: allErrors,
    };
  }
}

// 内置验证规则示例

/**
 * 属性点分配验证
 */
export const AbilityAllocationRule: ValidationRule = {
  id: 'ability-allocation',
  name: '属性点分配验证',
  severity: 'error',
  
  appliesTo: (ctx) => ctx.character.abilityScores !== undefined,
  
  validate: (ctx) => {
    const errors: ValidationError[] = [];
    const scores = ctx.character.abilityScores!;
    
    // 检查总分是否超过27点购买限制
    const totalCost = Object.values(scores).reduce((sum, score) => {
      return sum + abilityScoreCost(score);
    }, 0);
    
    if (totalCost > 27) {
      errors.push({
        code: 'ABILITY_BUDGET_EXCEEDED',
        message: `属性点购买超出限制：使用了 ${totalCost} 点，上限为 27 点`,
        field: 'abilityScores',
      });
    }
    
    // 检查是否在8-15范围内
    for (const [ability, score] of Object.entries(scores)) {
      if (score < 8 || score > 15) {
        errors.push({
          code: 'ABILITY_SCORE_OUT_OF_RANGE',
          message: `${ability} 属性值 ${score} 超出范围（8-15）`,
          field: `abilityScores.${ability}`,
        });
      }
    }
    
    return errors;
  },
};

/**
 * 多职业前置条件验证
 */
export const MulticlassPrerequisiteRule: ValidationRule = {
  id: 'multiclass-prereq',
  name: '多职业前置条件',
  severity: 'error',
  
  appliesTo: (ctx) => (ctx.character.classes?.length || 0) > 1,
  
  validate: (ctx) => {
    const errors: ValidationError[] = [];
    const classes = ctx.character.classes!;
    
    // 检查每个副职业的前置条件
    for (let i = 1; i < classes.length; i++) {
      const cls = dataRegistry.getById(DataType.CLASS, classes[i].index);
      const prereq = cls.multi_classing?.prerequisites;
      
      if (prereq) {
        const meetsPrereq = checkPrerequisites(ctx.character, prereq);
        if (!meetsPrereq) {
          errors.push({
            code: 'MULTICLASS_PREREQ_NOT_MET',
            message: `不满足 ${cls.name} 的多职业前置条件`,
            field: `classes[${i}]`,
          });
        }
      }
    }
    
    return errors;
  },
};
```

## 7. 角色卡导出系统

### 7.1 导出格式

```typescript
// export/export-manager.ts

export interface ExportFormat {
  id: string;
  name: string;
  extension: string;
  mimeType: string;
  serialize(character: Character): string | Blob;
}

export class ExportManager {
  private formats: Map<string, ExportFormat> = new Map();
  
  registerFormat(format: ExportFormat): void {
    this.formats.set(format.id, format);
  }
  
  export(character: Character, formatId: string): ExportResult {
    const format = this.formats.get(formatId);
    if (!format) {
      throw new Error(`Unknown export format: ${formatId}`);
    }
    
    const data = format.serialize(character);
    
    return {
      filename: `${character.name || 'character'}.${format.extension}`,
      mimeType: format.mimeType,
      data,
    };
  }
}

// JSON 格式（完整数据）
export const JSONExportFormat: ExportFormat = {
  id: 'json',
  name: 'JSON',
  extension: 'json',
  mimeType: 'application/json',
  serialize: (character) => JSON.stringify(character, null, 2),
};

// 简化 JSON（用于分享）
export const CompactJSONFormat: ExportFormat = {
  id: 'compact-json',
  name: 'Compact JSON',
  extension: 'json',
  mimeType: 'application/json',
  serialize: (character) => {
    const compact = {
      v: 1, // 版本
      n: character.name,
      r: character.race?.index,
      sr: character.race?.subrace,
      c: character.classes?.map(c => ({
        i: c.index,
        l: c.level,
        sc: c.subclass,
      })),
      a: character.abilityScores,
      // ... 其他必要字段
    };
    return JSON.stringify(compact);
  },
};

// 标准角色卡 PDF（未来实现）
export const PDFExportFormat: ExportFormat = {
  id: 'pdf',
  name: 'PDF 角色卡',
  extension: 'pdf',
  mimeType: 'application/pdf',
  serialize: (character) => {
    // 使用 pdf-lib 生成标准角色卡
    return generateCharacterSheetPDF(character);
  },
};

// Foundry VTT 格式
export const FoundryVTTExportFormat: ExportFormat = {
  id: 'foundry',
  name: 'Foundry VTT',
  extension: 'json',
  mimeType: 'application/json',
  serialize: (character) => {
    // 转换为 Foundry VTT 角色数据格式
    return JSON.stringify(convertToFoundryFormat(character), null, 2);
  },
};
```

## 8. 平台适配层

### 8.1 跨平台抽象

```typescript
// platform/platform-adapter.ts

export interface PlatformAdapter {
  // 存储
  storage: StorageAdapter;
  
  // 文件系统
  fileSystem: FileSystemAdapter;
  
  // 网络
  network: NetworkAdapter;
  
  // UI 能力
  ui: UIAdapter;
  
  // 分享
  share: ShareAdapter;
}

// Web 平台适配
export class WebPlatformAdapter implements PlatformAdapter {
  storage = new LocalStorageAdapter();
  fileSystem = new WebFileSystemAdapter();
  network = new FetchNetworkAdapter();
  ui = new WebUIAdapter();
  share = new WebShareAdapter();
}

// 微信小程序适配
export class WXPlatformAdapter implements PlatformAdapter {
  storage = new WXStorageAdapter();
  fileSystem = new WXFileSystemAdapter();
  network = new WXNetworkAdapter();
  ui = new WXUIAdapter();
  share = new WXShareAdapter();
}

// 存储适配器接口
export interface StorageAdapter {
  get<T>(key: string): Promise<T | null>;
  set<T>(key: string, value: T): Promise<void>;
  remove(key: string): Promise<void>;
  clear(): Promise<void>;
}

// 微信小程序存储实现
export class WXStorageAdapter implements StorageAdapter {
  async get<T>(key: string): Promise<T | null> {
    try {
      const result = await wx.getStorage({ key });
      return result.data as T;
    } catch {
      return null;
    }
  }
  
  async set<T>(key: string, value: T): Promise<void> {
    await wx.setStorage({ key, data: value });
  }
  
  // ... 其他方法
}
```

## 9. 完整文件结构

```
character-builder/
├── src/
│   ├── core/                          # 核心引擎（平台无关）
│   │   ├── data-registry.ts
│   │   ├── lazy-loader.ts
│   │   ├── event-bus.ts
│   │   └── utils/
│   │       ├── immutable.ts
│   │       ├── id-generator.ts
│   │       └── validators.ts
│   │
│   ├── builder/                       # 车卡系统
│   │   ├── state-machine.ts
│   │   ├── character-calculator.ts
│   │   ├── steps/
│   │   │   ├── step-system.ts
│   │   │   ├── select-race-step.ts
│   │   │   ├── select-class-step.ts
│   │   │   ├── allocate-abilities-step.ts
│   │   │   ├── select-background-step.ts
│   │   │   ├── select-spells-step.ts
│   │   │   ├── select-feats-step.ts
│   │   │   ├── buy-equipment-step.ts
│   │   │   └── index.ts
│   │   └── context/
│   │       ├── build-context.ts
│   │       └── context-helpers.ts
│   │
│   ├── validation/                    # 验证系统
│   │   ├── validation-engine.ts
│   │   ├── rules/
│   │   │   ├── ability-rules.ts
│   │   │   ├── class-rules.ts
│   │   │   ├── multiclass-rules.ts
│   │   │   └── index.ts
│   │   └── error-messages.ts
│   │
│   ├── plugin/                        # 插件系统
│   │   ├── extension-loader.ts
│   │   ├── extension-manager.ts
│   │   ├── sandbox.ts
│   │   └── types/
│   │       └── extension-manifest.ts
│   │
│   ├── export/                        # 导出系统
│   │   ├── export-manager.ts
│   │   └── formats/
│   │       ├── json-format.ts
│   │       ├── compact-format.ts
│   │       ├── pdf-format.ts
│   │       └── foundry-format.ts
│   │
│   ├── data/                          # 数据处理
│   │   ├── transformers/
│   │   ├── mergers/
│   │   └── migrations/
│   │
│   ├── platform/                      # 平台适配
│   │   ├── platform-adapter.ts
│   │   ├── web/
│   │   │   ├── storage.ts
│   │   │   ├── filesystem.ts
│   │   │   └── index.ts
│   │   └── weixin/
│   │       ├── storage.ts
│   │       ├── filesystem.ts
│   │       └── index.ts
│   │
│   ├── types/                         # 类型定义
│   │   ├── character.ts
│   │   ├── data-source.ts
│   │   ├── builder.ts
│   │   ├── validation.ts
│   │   └── index.ts
│   │
│   └── index.ts                       # 主入口
│
├── data/                              # 静态数据
│   ├── core/                          # 核心SRD数据
│   │   ├── 2014/
│   │   └── 2024/
│   ├── extensions/                    # 官方扩展
│   │   ├── xge/                       # Xanathar's Guide
│   │   ├── tce/                       # Tasha's Cauldron
│   │   └── vgm/                       # Volo's Guide
│   └── homebrew/                      # 用户自定义（gitignore）
│
├── packages/                          # 平台特定包
│   ├── web/                           # Web 应用
│   │   ├── src/
│   │   ├── public/
│   │   └── package.json
│   │
│   └── weixin/                        # 微信小程序
│       ├── pages/
│       ├── components/
│       └── app.json
│
├── docs/                              # 文档
│   ├── ARCHITECTURE.md
│   ├── EXTENSION_GUIDE.md
│   └── API_REFERENCE.md
│
├── tests/
│   ├── unit/
│   ├── integration/
│   └── fixtures/
│
├── scripts/
│   ├── build-data.ts
│   ├── validate-extensions.ts
│   └── generate-types.ts
│
├── package.json
├── tsconfig.json
└── README.md
```

## 10. 使用示例

### 10.1 基础使用

```typescript
import { CharacterBuilder } from '@dnd5e/character-builder';
import { WebPlatformAdapter } from '@dnd5e/character-builder/web';

// 初始化
const builder = new CharacterBuilder({
  platform: new WebPlatformAdapter(),
  dataSources: ['srd-2014-zh'],
});

// 开始车卡
await builder.initialize();

// 获取当前步骤
const currentStep = builder.getCurrentStep();
console.log(currentStep.name); // "选择种族"

// 获取可用选项
const options = currentStep.getOptions(builder.getContext());
// [{ id: 'elf', name: '精灵', ... }, { id: 'dwarf', name: '矮人', ... }]

// 做出选择
builder.dispatch({
  type: 'SELECT_RACE',
  payload: { raceId: 'elf', subraceId: 'high-elf' }
});

// 继续下一步
builder.nextStep();

// 导出角色
const character = builder.exportCharacter();
const json = builder.export('json');
```

### 10.2 加载扩展

```typescript
// 从 CDN 加载扩展
await builder.loadExtension({
  id: 'xge',
  url: 'https://extensions.dnd5e.com/xge-v1.0.json'
});

// 从本地文件加载（桌面端）
await builder.loadExtensionFromFile(homebrewFile);

// 启用/禁用扩展
builder.enableExtension('xge');
builder.disableExtension('tce');
```

### 10.3 自定义步骤

```typescript
// 扩展包中定义自定义步骤
const myExtension = {
  id: 'custom-subclass-step',
  customSteps: [
    {
      id: 'select-patron',
      name: '选择宗主',
      order: 25,
      condition: {
        requiresClass: ['warlock'],
      },
      optionsProvider: 'getPatronOptions',
      executor: 'applyPatronSelection',
    }
  ]
};

// 在沙箱中执行
const sandbox = new ScriptSandbox();
sandbox.execute(`
  function getPatronOptions(context) {
    return api.getData('subclasses', 'warlock')
      .filter(sc => sc.subclass_flavor === ' Otherworldly Patron');
  }
  
  function applyPatronSelection(context, selection) {
    context.character.patron = selection;
    return context;
  }
`, { context: builder.getContext() });
```

## 11. 性能优化策略

### 11.1 数据加载
- **分层加载**: 元数据立即加载，详情按需加载
- **预加载**: 预测用户下一步，提前加载
- **索引**: 建立快速查找索引
- **压缩**: 大数据使用 MessagePack 压缩

### 11.2 状态管理
- **不可变更新**: 使用 Immer 确保状态不可变
- **选择器缓存**: 使用 Reselect 缓存计算结果
- **增量计算**: 只重新计算变化的部分

### 11.3 微信小程序优化
- **分包加载**: 按步骤分包
- **本地存储**: 缓存已加载的数据
- **骨架屏**: 提升感知性能

## 12. 安全考虑

### 12.1 数据安全
- 用户数据本地存储，不上传服务器
- 扩展包签名验证
- 沙箱执行限制

### 12.2 内容安全
- 用户生成内容审核
- XSS 防护
- 敏感词过滤

---

*本文档描述了 D&D 5e 车卡系统的整体架构设计。具体实现时可根据实际需求调整。*
