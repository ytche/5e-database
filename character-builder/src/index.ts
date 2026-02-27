/**
 * D&D 5e 车卡系统 - 主入口
 */

// 类型导出
export * from './types';

// 核心导出
export { DataRegistry, getGlobalRegistry, setGlobalRegistry } from './core/data-registry';
export { produce, deepClone, deepEqual } from './core/utils/immutable';

// 车卡系统导出
export { 
  CharacterBuilderStateMachine, 
  CharacterBuilderConfig 
} from './builder/state-machine';
export { CharacterCalculator } from './builder/character-calculator';
export { StepRegistry, getGlobalStepRegistry } from './builder/steps/step-registry';

// 步骤导出
export { SelectRaceStep } from './builder/steps/select-race-step';
export { SelectClassStep } from './builder/steps/select-class-step';
export { AllocateAbilitiesStep } from './builder/steps/allocate-abilities-step';

// 验证系统导出（待实现）
// export { ValidationEngine } from './validation/validation-engine';

// 插件系统导出（待实现）
// export { ExtensionLoader, ExtensionManager } from './plugin/extension-loader';

// 导出系统导出（待实现）
// export { ExportManager } from './export/export-manager';

import { DataRegistry, getGlobalRegistry } from './core/data-registry';
import { StepRegistry, getGlobalStepRegistry } from './builder/steps/step-registry';
import { CharacterBuilderStateMachine, CharacterBuilderConfig } from './builder/state-machine';
import { SelectRaceStep } from './builder/steps/select-race-step';
import { SelectClassStep } from './builder/steps/select-class-step';
import { AllocateAbilitiesStep } from './builder/steps/allocate-abilities-step';

/**
 * 车卡器主类
 * 简化API入口
 */
export class CharacterBuilder {
  private stateMachine: CharacterBuilderStateMachine;
  private dataRegistry: DataRegistry;
  private stepRegistry: StepRegistry;

  constructor(config: {
    dataRegistry?: DataRegistry;
    stepRegistry?: StepRegistry;
    dataSources?: string[];
  } = {}) {
    this.dataRegistry = config.dataRegistry || getGlobalRegistry();
    this.stepRegistry = config.stepRegistry || getGlobalStepRegistry();

    // 注册默认步骤
    this.registerDefaultSteps();

    this.stateMachine = new CharacterBuilderStateMachine({
      dataRegistry: this.dataRegistry,
      stepRegistry: this.stepRegistry,
      dataSources: config.dataSources,
    });
  }

  /**
   * 注册默认步骤
   */
  private registerDefaultSteps(): void {
    // 只注册未存在的步骤
    if (!this.stepRegistry.getStep('select-race')) {
      this.stepRegistry.register(new SelectRaceStep());
    }
    if (!this.stepRegistry.getStep('select-class')) {
      this.stepRegistry.register(new SelectClassStep());
    }
    if (!this.stepRegistry.getStep('allocate-abilities')) {
      this.stepRegistry.register(new AllocateAbilitiesStep());
    }
  }

  /**
   * 初始化
   */
  async initialize(): Promise<void> {
    // 预加载必要数据
    // await this.dataRegistry.preload();
  }

  /**
   * 执行动作
   */
  dispatch(action: import('./types').BuildAction): void {
    this.stateMachine.dispatch(action);
  }

  /**
   * 获取当前上下文
   */
  getContext(): import('./types').BuildContext {
    return this.stateMachine.getContext();
  }

  /**
   * 获取当前步骤
   */
  getCurrentStep(): import('./types').BuilderStep | null {
    return this.stateMachine.getCurrentStep();
  }

  /**
   * 获取所有可用步骤
   */
  getAvailableSteps(): import('./types').BuilderStep[] {
    return this.stateMachine.getAvailableSteps();
  }

  /**
   * 前进到下一步
   */
  nextStep(): import('./types').BuilderStep | null {
    return this.stateMachine.nextStep();
  }

  /**
   * 验证构建
   */
  validate(): import('./types').ValidationResult {
    return this.stateMachine.validateBuild();
  }

  /**
   * 导出角色
   */
  exportCharacter(): import('./types').Character {
    return this.stateMachine.exportCharacter();
  }

  /**
   * 订阅状态变化
   */
  subscribe(listener: (context: import('./types').BuildContext) => void): () => void {
    return this.stateMachine.subscribe(listener);
  }

  /**
   * 序列化状态
   */
  serialize(): string {
    return this.stateMachine.serialize();
  }

  /**
   * 反序列化状态
   */
  static deserialize(json: string, config?: { dataRegistry?: DataRegistry }): CharacterBuilder {
    const dataRegistry = config?.dataRegistry || getGlobalRegistry();
    const builder = new CharacterBuilder({ dataRegistry });
    // 恢复状态逻辑...
    return builder;
  }

  /**
   * 加载数据源
   */
  loadDataSource(sourceId: string, data: Record<string, unknown[]>): void {
    // 启用数据源
    const source = this.dataRegistry.getSource(sourceId);
    if (source) {
      source.enabled = true;
    }

    // 加载数据
    for (const [type, items] of Object.entries(data)) {
      this.dataRegistry.loadData(type as import('./types').DataType, sourceId, items);
    }
  }

  /**
   * 注册自定义步骤
   */
  registerStep(step: import('./types').BuilderStep): void {
    this.stepRegistry.register(step);
  }

  /**
   * 获取数据注册表
   */
  getDataRegistry(): DataRegistry {
    return this.dataRegistry;
  }

  /**
   * 获取步骤注册表
   */
  getStepRegistry(): StepRegistry {
    return this.stepRegistry;
  }
}

// 默认导出
export default CharacterBuilder;
