/**
 * 步骤注册表 - 管理所有车卡步骤
 */

import { BuilderStep, BuildContext } from '../../types';

export class StepRegistry {
  private steps: Map<string, BuilderStep> = new Map();
  private orderedCache: BuilderStep[] | null = null;

  /**
   * 注册步骤
   */
  register(step: BuilderStep): void {
    if (this.steps.has(step.id)) {
      console.warn(`Step '${step.id}' is already registered, overwriting`);
    }
    this.steps.set(step.id, step);
    this.orderedCache = null; // 清除缓存
  }

  /**
   * 注销步骤
   */
  unregister(stepId: string): void {
    this.steps.delete(stepId);
    this.orderedCache = null;
  }

  /**
   * 获取步骤
   */
  getStep(id: string): BuilderStep | undefined {
    return this.steps.get(id);
  }

  /**
   * 获取所有步骤（按order排序）
   */
  getAllSteps(): BuilderStep[] {
    if (!this.orderedCache) {
      this.orderedCache = Array.from(this.steps.values())
        .sort((a, b) => a.order - b.order);
    }
    return this.orderedCache;
  }

  /**
   * 获取在指定步骤之前的步骤
   */
  getStepsBefore(stepId: string, context: BuildContext): BuilderStep[] {
    const targetStep = this.steps.get(stepId);
    if (!targetStep) return [];

    return this.getAllSteps().filter(step => 
      step.order < targetStep.order && step.shouldShow(context)
    );
  }

  /**
   * 获取在指定步骤之后的步骤
   */
  getStepsAfter(stepId: string, context: BuildContext): BuilderStep[] {
    const targetStep = this.steps.get(stepId);
    if (!targetStep) return [];

    return this.getAllSteps().filter(step => 
      step.order > targetStep.order && step.shouldShow(context)
    );
  }

  /**
   * 检查步骤是否存在
   */
  hasStep(id: string): boolean {
    return this.steps.has(id);
  }

  /**
   * 获取步骤数量
   */
  getStepCount(): number {
    return this.steps.size;
  }

  /**
   * 清除所有步骤
   */
  clear(): void {
    this.steps.clear();
    this.orderedCache = null;
  }
}

// 单例实例
let globalRegistry: StepRegistry | null = null;

export function getGlobalStepRegistry(): StepRegistry {
  if (!globalRegistry) {
    globalRegistry = new StepRegistry();
  }
  return globalRegistry;
}

export function setGlobalStepRegistry(registry: StepRegistry): void {
  globalRegistry = registry;
}
