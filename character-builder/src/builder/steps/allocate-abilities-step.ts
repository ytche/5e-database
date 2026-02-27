/**
 * 分配属性点步骤
 */

import {
  BuilderStep,
  BuildContext,
  StepOption,
  ValidationResult,
  DependencyResult,
  AbilityAllocation,
  AbilityScore,
  DataType,
} from '../../types';
import { produce } from '../../core/utils/immutable';

// 标准数组
const STANDARD_ARRAY = [15, 14, 13, 12, 10, 8];

// 购点法成本表
const POINT_BUY_COSTS: Record<number, number> = {
  8: 0, 9: 1, 10: 2, 11: 3, 12: 4, 13: 5, 14: 7, 15: 9,
};

// 最大购点数
const MAX_POINTS = 27;

// 属性范围
const MIN_SCORE = 8;
const MAX_SCORE = 15; // 购点法上限（不含种族加成）

export interface AbilityAllocationDetails {
  method: 'point-buy' | 'standard-array' | 'roll';
  scores: Record<AbilityScore, number>;
  racialBonuses: Partial<Record<AbilityScore, number>>;
  totalBonuses: Record<AbilityScore, number>;
  modifiers: Record<AbilityScore, number>;
  pointBuyCost?: number;
  pointBuyRemaining?: number;
  isValid: boolean;
  errors: string[];
}

export class AllocateAbilitiesStep implements BuilderStep {
  id = 'allocate-abilities';
  name = '分配属性';
  order = 30;

  shouldShow(): boolean {
    return true;
  }

  checkDependencies(context: BuildContext): DependencyResult {
    if (!context.character.race) {
      return {
        satisfied: false,
        blockingSteps: ['select-race'],
        message: '请先选择种族',
      };
    }
    return { satisfied: true };
  }

  validate(context: BuildContext): ValidationResult {
    const scores = context.character.abilityScores;
    
    if (!scores) {
      return {
        valid: false,
        errors: [{ code: 'ABILITIES_REQUIRED', message: '请分配属性点', field: 'abilityScores' }],
      };
    }

    const details = this.getAllocationDetails(context);
    
    if (!details.isValid) {
      return {
        valid: false,
        errors: details.errors.map(msg => ({ 
          code: 'INVALID_ABILITY_SCORES', 
          message: msg,
          field: 'abilityScores',
        })),
      };
    }

    return { valid: true };
  }

  getOptions(context: BuildContext): StepOption[] {
    // 返回可用的分配方法
    return [
      {
        id: 'point-buy',
        name: '购点法',
        description: '使用27点购买属性，范围8-15',
        details: {
          maxPoints: MAX_POINTS,
          costTable: POINT_BUY_COSTS,
        },
      },
      {
        id: 'standard-array',
        name: '标准数组',
        description: '使用预设值：15, 14, 13, 12, 10, 8',
        details: {
          values: STANDARD_ARRAY,
        },
      },
      {
        id: 'roll',
        name: '掷骰决定',
        description: '掷4d6，取最高3个（暂不实现）',
        disabled: true,
        disabledReason: '暂不支持',
      },
    ];
  }

  /**
   * 获取详细的分配信息（用于UI显示）
   */
  getAllocationDetails(context: BuildContext): AbilityAllocationDetails {
    const scores = context.character.abilityScores || {
      str: 8, dex: 8, con: 8, int: 8, wis: 8, cha: 8,
    };
    
    const racialBonuses = context.character.abilityBonuses || {};
    const abilities: AbilityScore[] = ['str', 'dex', 'con', 'int', 'wis', 'cha'];
    
    // 计算总属性值和修正值
    const totalBonuses: Record<AbilityScore, number> = {} as Record<AbilityScore, number>;
    const modifiers: Record<AbilityScore, number> = {} as Record<AbilityScore, number>;
    
    for (const ability of abilities) {
      const base = scores[ability] || 8;
      const bonus = racialBonuses[ability] || 0;
      totalBonuses[ability] = base + bonus;
      modifiers[ability] = Math.floor((totalBonuses[ability] - 10) / 2);
    }

    // 计算购点成本
    let pointBuyCost = 0;
    const errors: string[] = [];

    for (const ability of abilities) {
      const score = scores[ability] || 8;
      
      // 验证范围
      if (score < MIN_SCORE || score > MAX_SCORE) {
        errors.push(`${ability.toUpperCase()} 的 ${score} 超出范围 (${MIN_SCORE}-${MAX_SCORE})`);
      }
      
      // 计算成本
      const cost = POINT_BUY_COSTS[score];
      if (cost === undefined) {
        errors.push(`${ability.toUpperCase()} 的 ${score} 不是有效的购点值`);
      } else {
        pointBuyCost += cost;
      }
    }

    // 验证总成本
    if (pointBuyCost > MAX_POINTS) {
      errors.push(`购点总和 ${pointBuyCost} 超过上限 ${MAX_POINTS}`);
    }

    return {
      method: 'point-buy',
      scores: scores as Record<AbilityScore, number>,
      racialBonuses: racialBonuses as Partial<Record<AbilityScore, number>>,
      totalBonuses,
      modifiers,
      pointBuyCost,
      pointBuyRemaining: MAX_POINTS - pointBuyCost,
      isValid: errors.length === 0,
      errors,
    };
  }

  /**
   * 设置单个属性值
   */
  setAbilityScore(context: BuildContext, ability: AbilityScore, value: number): BuildContext {
    return produce(context, draft => {
      if (!draft.character.abilityScores) {
        draft.character.abilityScores = { str: 8, dex: 8, con: 8, int: 8, wis: 8, cha: 8 };
      }
      (draft.character.abilityScores as Record<AbilityScore, number>)[ability] = value;
    });
  }

  /**
   * 应用标准数组
   */
  applyStandardArray(context: BuildContext, assignments: Record<AbilityScore, number>): BuildContext {
    // 验证使用的值是否匹配标准数组
    const values = Object.values(assignments).sort((a, b) => b - a);
    const expected = [...STANDARD_ARRAY].sort((a, b) => b - a);
    
    if (JSON.stringify(values) !== JSON.stringify(expected)) {
      throw new Error('Invalid standard array assignment');
    }

    return this.execute(context, {
      method: 'standard-array',
      scores: assignments,
    });
  }

  /**
   * 获取推荐分配
   */
  getRecommendedAllocation(context: BuildContext): Partial<Record<AbilityScore, number>> {
    const classes = context.character.classes;
    if (!classes || classes.length === 0) {
      return {};
    }

    const registry = (await import('../../core/data-registry')).getGlobalRegistry();
    const primaryClass = classes.find(c => c.isPrimary) || classes[0];
    const cls = registry.getById<{ saving_throws: { index: string }[]; spellcasting?: { spellcasting_ability: { index: string } } }>(DataType.CLASS, primaryClass.index);
    
    if (!cls) return {};

    // 基于职业推断主要属性
    const primaryAbilities = new Set<string>();
    
    // 豁免熟练通常是主要属性
    cls.saving_throws?.forEach(st => primaryAbilities.add(st.index));
    
    // 施法能力是主要属性
    if (cls.spellcasting?.spellcasting_ability) {
      primaryAbilities.add(cls.spellcasting.spellcasting_ability.index);
    }

    // 特定职业调整
    const classSpecific: Record<string, string[]> = {
      barbarian: ['str', 'con'],
      bard: ['cha', 'dex'],
      cleric: ['wis', 'con'],
      druid: ['wis', 'con'],
      fighter: ['str', 'con', 'dex'],
      monk: ['dex', 'wis'],
      paladin: ['str', 'cha', 'con'],
      ranger: ['dex', 'wis'],
      rogue: ['dex'],
      sorcerer: ['cha', 'con'],
      warlock: ['cha', 'con'],
      wizard: ['int', 'con'],
    };

    const specific = classSpecific[primaryClass.index];
    if (specific) {
      specific.forEach(a => primaryAbilities.add(a));
    }

    // 构建推荐分配（优先职业属性）
    const sortedAbilities = ['str', 'dex', 'con', 'int', 'wis', 'cha'] as AbilityScore[];
    const sortedValues = [...STANDARD_ARRAY].sort((a, b) => b - a);
    
    const recommendation: Partial<Record<AbilityScore, number>> = {};
    let valueIndex = 0;

    // 首先分配主要属性
    for (const ability of sortedAbilities) {
      if (primaryAbilities.has(ability)) {
        recommendation[ability] = sortedValues[valueIndex++];
      }
    }

    // 然后分配其他属性
    for (const ability of sortedAbilities) {
      if (!(ability in recommendation)) {
        recommendation[ability] = sortedValues[valueIndex++];
      }
    }

    return recommendation;
  }

  execute(context: BuildContext, selection: AbilityAllocation): BuildContext {
    return produce(context, draft => {
      draft.character.abilityScores = selection.scores as Record<string, number>;
      this.markStepComplete(draft);
    });
  }

  rollback(context: BuildContext): BuildContext {
    return produce(context, draft => {
      draft.character.abilityScores = { str: 8, dex: 8, con: 8, int: 8, wis: 8, cha: 8 };
      this.unmarkStepComplete(draft);
    });
  }

  private markStepComplete(draft: BuildContext): void {
    if (!draft.completedSteps.includes(this.id)) {
      draft.completedSteps.push(this.id);
    }
  }

  private unmarkStepComplete(draft: BuildContext): void {
    const index = draft.completedSteps.indexOf(this.id);
    if (index > -1) {
      draft.completedSteps.splice(index, 1);
    }
  }
}
