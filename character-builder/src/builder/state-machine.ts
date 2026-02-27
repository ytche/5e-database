/**
 * 车卡状态机 - 管理整个车卡流程的状态
 */

import {
  BuildContext,
  BuildAction,
  Character,
  BuilderStep,
  ValidationResult,
  StepRegistry,
  DataSource,
} from '../types';
import { StepRegistry as StepRegistryImpl } from './steps/step-registry';
import { DataRegistry } from '../core/data-registry';
import { CharacterCalculator } from './character-calculator';
import { produce } from '../core/utils/immutable';

export interface CharacterBuilderConfig {
  dataRegistry: DataRegistry;
  stepRegistry?: StepRegistry;
  dataSources?: string[];
  initialContext?: Partial<BuildContext>;
}

export class CharacterBuilderStateMachine {
  private context: BuildContext;
  private dataRegistry: DataRegistry;
  private stepRegistry: StepRegistry;
  private calculator: CharacterCalculator;
  private listeners: Set<(context: BuildContext) => void> = new Set();
  private maxHistorySize = 50;

  constructor(config: CharacterBuilderConfig) {
    this.dataRegistry = config.dataRegistry;
    this.stepRegistry = config.stepRegistry || new StepRegistryImpl();
    this.calculator = new CharacterCalculator(config.dataRegistry);
    this.context = this.createInitialContext(config);
    
    // 加载指定的数据源
    if (config.dataSources) {
      for (const sourceId of config.dataSources) {
        const source = this.dataRegistry.getSource(sourceId);
        if (source) {
          source.enabled = true;
        }
      }
    }
  }

  /**
   * 初始化构建上下文
   */
  private createInitialContext(config: CharacterBuilderConfig): BuildContext {
    const now = new Date();
    return {
      version: '1.0.0',
      character: {
        abilityScores: { str: 8, dex: 8, con: 8, int: 8, wis: 8, cha: 8 } as Record<string, number>,
        abilityBonuses: {},
        proficiencies: {
          skills: {} as Record<string, 'none' | 'proficient' | 'expertise'>,
          savingThrows: {} as Record<string, boolean>,
          armor: [],
          weapons: [],
          tools: [],
        },
        languages: [],
        traits: [],
        features: [],
        equipment: [],
        classes: [],
      },
      completedSteps: [],
      currentStepId: null,
      history: [],
      historyIndex: -1,
      metadata: {
        createdAt: now,
        modifiedAt: now,
        dataSources: config.dataSources || [],
        ...config.initialContext?.metadata,
      },
      ...config.initialContext,
    };
  }

  /**
   * 执行动作
   */
  dispatch(action: BuildAction): void {
    const newContext = this.reducer(this.context, action);
    
    // 如果上下文变化，添加到历史
    if (newContext !== this.context) {
      // 添加当前状态到历史
      if (this.context.historyIndex < this.context.history.length - 1) {
        // 如果在历史中间，截断后面的历史
        this.context.history = this.context.history.slice(0, this.context.historyIndex + 1);
      }
      
      this.context.history.push(action);
      
      // 限制历史大小
      if (this.context.history.length > this.maxHistorySize) {
        this.context.history.shift();
      }
      
      this.context.historyIndex = this.context.history.length - 1;
      this.context.metadata.modifiedAt = new Date();
    }
    
    this.context = newContext;
    this.notifyListeners();
  }

  /**
   * Reducer - 处理所有动作
   */
  private reducer(context: BuildContext, action: BuildAction): BuildContext {
    switch (action.type) {
      case 'SELECT_RACE':
        return this.handleSelectRace(context, action.payload);
      
      case 'SELECT_CLASS':
        return this.handleSelectClass(context, action.payload);
      
      case 'ALLOCATE_ABILITIES':
        return this.handleAllocateAbilities(context, action.payload);
      
      case 'SELECT_BACKGROUND':
        return this.handleSelectBackground(context, action.payload);
      
      case 'SELECT_SPELLS':
        return this.handleSelectSpells(context, action.payload);
      
      case 'SELECT_FEATS':
        return this.handleSelectFeats(context, action.payload);
      
      case 'BUY_EQUIPMENT':
        return this.handleBuyEquipment(context, action.payload);
      
      case 'SET_DETAILS':
        return this.handleSetDetails(context, action.payload);
      
      case 'UNDO':
        return this.handleUndo(context);
      
      case 'REDO':
        return this.handleRedo(context);
      
      case 'RESET':
        return this.handleReset(context);
      
      default:
        return context;
    }
  }

  /**
   * 处理选择种族
   */
  private handleSelectRace(context: BuildContext, payload: import('../types').RaceSelection): BuildContext {
    const { Race, Subrace } = import('../types');
    
    return produce(context, draft => {
      // 清除之前的种族相关数据
      draft.character.race = undefined;
      draft.character.abilityBonuses = {};
      draft.character.traits = [];
      draft.character.languages = [];
      
      // 设置种族
      draft.character.race = {
        index: payload.raceId,
        name: this.dataRegistry.getById('races', payload.raceId)?.name || payload.raceId,
        subrace: payload.subraceId,
      };

      // 应用种族属性加成
      const race = this.dataRegistry.getById<import('../types').Race>('races', payload.raceId);
      if (race?.ability_bonuses) {
        for (const bonus of race.ability_bonuses) {
          const ability = bonus.ability_score.index as string;
          draft.character.abilityBonuses[ability] = 
            (draft.character.abilityBonuses[ability] || 0) + bonus.bonus;
        }
      }

      // 应用亚种族属性加成
      if (payload.subraceId) {
        const subrace = this.dataRegistry.getById<import('../types').Subrace>('subraces', payload.subraceId);
        if (subrace?.ability_bonuses) {
          for (const bonus of subrace.ability_bonuses) {
            const ability = bonus.ability_score.index as string;
            draft.character.abilityBonuses[ability] = 
              (draft.character.abilityBonuses[ability] || 0) + bonus.bonus;
          }
        }
        
        // 应用亚种族特性
        if (subrace?.traits) {
          draft.character.traits.push(...subrace.traits.map(t => t.index));
        }
      }

      // 应用种族特性
      if (race?.traits) {
        draft.character.traits.push(...race.traits.map(t => t.index));
      }

      // 应用种族语言
      if (race?.languages) {
        draft.character.languages.push(...race.languages.map(l => l.index));
      }

      // 标记步骤完成
      this.markStepComplete(draft, 'select-race');
    });
  }

  /**
   * 处理选择职业
   */
  private handleSelectClass(context: BuildContext, payload: import('../types').ClassSelection): BuildContext {
    return produce(context, draft => {
      const cls = this.dataRegistry.getById<import('../types').Class>('classes', payload.classId);
      if (!cls) return;

      const classData = {
        index: payload.classId,
        name: cls.name,
        level: payload.level || 1,
        subclass: payload.subclassId,
        isPrimary: !payload.isMulticlass || draft.character.classes?.length === 0,
      };

      if (payload.isMulticlass && draft.character.classes?.length > 0) {
        // 添加多职业
        draft.character.classes.push(classData);
      } else {
        // 替换主职业
        draft.character.classes = [classData];
      }

      // 应用职业熟练项
      if (cls.proficiencies) {
        for (const prof of cls.proficiencies) {
          this.addProficiency(draft, prof.index);
        }
      }

      // 应用职业豁免
      if (cls.saving_throws) {
        for (const save of cls.saving_throws) {
          draft.character.proficiencies.savingThrows[save.index] = true;
        }
      }

      this.markStepComplete(draft, 'select-class');
    });
  }

  /**
   * 处理属性分配
   */
  private handleAllocateAbilities(context: BuildContext, payload: import('../types').AbilityAllocation): BuildContext {
    return produce(context, draft => {
      draft.character.abilityScores = payload.scores as Record<string, number>;
      this.markStepComplete(draft, 'allocate-abilities');
    });
  }

  /**
   * 处理选择背景
   */
  private handleSelectBackground(context: BuildContext, payload: import('../types').BackgroundSelection): BuildContext {
    return produce(context, draft => {
      const bg = this.dataRegistry.getById<import('../types').Background>('backgrounds', payload.backgroundId);
      if (!bg) return;

      draft.character.background = payload.backgroundId;

      // 应用背景熟练项
      if (bg.starting_proficiencies) {
        for (const prof of bg.starting_proficiencies) {
          this.addProficiency(draft, prof.index);
        }
      }

      // 应用背景装备
      if (bg.starting_equipment) {
        for (const item of bg.starting_equipment) {
          draft.character.equipment.push({
            index: item.equipment.index,
            name: item.equipment.name,
            quantity: item.quantity,
          });
        }
      }

      // 应用背景特性
      if (bg.feature) {
        draft.character.features.push(bg.feature.name);
      }

      this.markStepComplete(draft, 'select-background');
    });
  }

  /**
   * 处理选择法术
   */
  private handleSelectSpells(context: BuildContext, payload: import('../types').SpellSelection): BuildContext {
    return produce(context, draft => {
      draft.character.spells = {
        ability: 'int' as import('../types').AbilityScore,
        saveDC: 10,
        attackBonus: 0,
        spellsKnown: {},
        spellSlots: {},
        cantripsKnown: payload.cantrips,
      };

      for (const spell of payload.spells) {
        const spellData = this.dataRegistry.getById<import('../types').Spell>('spells', spell);
        if (spellData) {
          const level = spellData.level;
          if (!draft.character.spells.spellsKnown[level]) {
            draft.character.spells.spellsKnown[level] = [];
          }
          draft.character.spells.spellsKnown[level].push(spell);
        }
      }

      this.markStepComplete(draft, 'select-spells');
    });
  }

  /**
   * 处理选择专长
   */
  private handleSelectFeats(context: BuildContext, payload: import('../types').FeatSelection): BuildContext {
    return produce(context, draft => {
      const feat = this.dataRegistry.getById<import('../types').Feat>('feats', payload.featId);
      if (feat) {
        draft.character.features.push(feat.name);
      }

      // 应用属性提升
      if (payload.abilityScoreImprovement) {
        for (const [ability, bonus] of Object.entries(payload.abilityScoreImprovement)) {
          draft.character.abilityBonuses[ability] = 
            (draft.character.abilityBonuses[ability] || 0) + (bonus || 0);
        }
      }

      this.markStepComplete(draft, 'select-feats');
    });
  }

  /**
   * 处理购买装备
   */
  private handleBuyEquipment(context: BuildContext, payload: import('../types').EquipmentPurchase): BuildContext {
    return produce(context, draft => {
      for (const item of payload.items) {
        const existing = draft.character.equipment.find(e => e.index === item.index);
        if (existing) {
          existing.quantity += item.quantity;
        } else {
          draft.character.equipment.push({
            index: item.index,
            name: item.index, // Will be resolved
            quantity: item.quantity,
          });
        }
      }

      this.markStepComplete(draft, 'buy-equipment');
    });
  }

  /**
   * 处理设置详情
   */
  private handleSetDetails(context: BuildContext, payload: import('../types').CharacterDetails): BuildContext {
    return produce(context, draft => {
      if (payload.name) draft.character.name = payload.name;
      if (payload.alignment) (draft.character as Record<string, unknown>).alignment = payload.alignment;
      if (payload.appearance) (draft.character as Record<string, unknown>).appearance = payload.appearance;
      if (payload.personality) (draft.character as Record<string, unknown>).personality = payload.personality;
    });
  }

  /**
   * 撤销操作
   */
  private handleUndo(context: BuildContext): BuildContext {
    // 简化实现：实际应该恢复到上一个状态
    // 这里只是示例
    return context;
  }

  /**
   * 重做操作
   */
  private handleRedo(context: BuildContext): BuildContext {
    // 简化实现
    return context;
  }

  /**
   * 重置构建
   */
  private handleReset(context: BuildContext): BuildContext {
    return this.createInitialContext({
      dataRegistry: this.dataRegistry,
      dataSources: context.metadata.dataSources,
    });
  }

  /**
   * 辅助方法：标记步骤完成
   */
  private markStepComplete(draft: BuildContext, stepId: string): void {
    if (!draft.completedSteps.includes(stepId)) {
      draft.completedSteps.push(stepId);
    }
  }

  /**
   * 辅助方法：添加熟练项
   */
  private addProficiency(draft: BuildContext, proficiencyId: string): void {
    // 解析熟练项类型
    if (proficiencyId.startsWith('skill-')) {
      const skill = proficiencyId.replace('skill-', '');
      draft.character.proficiencies.skills[skill] = 'proficient';
    } else if (['light-armor', 'medium-armor', 'heavy-armor', 'shields'].includes(proficiencyId)) {
      draft.character.proficiencies.armor.push(proficiencyId);
    } else if (['simple-weapons', 'martial-weapons'].includes(proficiencyId)) {
      draft.character.proficiencies.weapons.push(proficiencyId);
    } else {
      draft.character.proficiencies.tools.push(proficiencyId);
    }
  }

  /**
   * 获取当前上下文
   */
  getContext(): BuildContext {
    return this.context;
  }

  /**
   * 获取当前步骤
   */
  getCurrentStep(): BuilderStep | null {
    const availableSteps = this.getAvailableSteps();
    
    // 找到第一个未完成的步骤
    for (const step of availableSteps) {
      const validation = step.validate(this.context);
      if (!validation.valid) {
        return step;
      }
    }
    
    return null; // 所有步骤都已完成
  }

  /**
   * 获取所有可用步骤
   */
  getAvailableSteps(): BuilderStep[] {
    const allSteps = this.stepRegistry.getAllSteps();
    return allSteps
      .filter(step => step.shouldShow(this.context))
      .filter(step => step.checkDependencies(this.context).satisfied)
      .sort((a, b) => a.order - b.order);
  }

  /**
   * 前进到下一步
   */
  nextStep(): BuilderStep | null {
    const availableSteps = this.getAvailableSteps();
    const currentIndex = availableSteps.findIndex(s => s.id === this.context.currentStepId);
    
    const nextStep = availableSteps[currentIndex + 1] || availableSteps[0];
    if (nextStep) {
      this.context = produce(this.context, draft => {
        draft.currentStepId = nextStep.id;
      });
      this.notifyListeners();
    }
    
    return nextStep;
  }

  /**
   * 验证整个构建
   */
  validateBuild(): ValidationResult {
    const availableSteps = this.getAvailableSteps();
    const errors: import('../types').ValidationError[] = [];
    const warnings: import('../types').ValidationError[] = [];

    for (const step of availableSteps) {
      const result = step.validate(this.context);
      if (result.errors) {
        errors.push(...result.errors);
      }
      if (result.warnings) {
        warnings.push(...result.warnings);
      }
    }

    return {
      valid: errors.length === 0,
      errors: errors.length > 0 ? errors : undefined,
      warnings: warnings.length > 0 ? warnings : undefined,
    };
  }

  /**
   * 导出最终角色
   */
  exportCharacter(): Character {
    const validation = this.validateBuild();
    if (!validation.valid) {
      throw new Error('Cannot export incomplete character: ' + 
        validation.errors?.map(e => e.message).join(', '));
    }

    return this.calculator.calculateFinal(this.context.character as Partial<Character>);
  }

  /**
   * 订阅状态变化
   */
  subscribe(listener: (context: BuildContext) => void): () => void {
    this.listeners.add(listener);
    return () => this.listeners.delete(listener);
  }

  /**
   * 通知所有监听器
   */
  private notifyListeners(): void {
    for (const listener of this.listeners) {
      listener(this.context);
    }
  }

  /**
   * 序列化状态（用于保存）
   */
  serialize(): string {
    return JSON.stringify({
      context: this.context,
      version: '1.0.0',
    });
  }

  /**
   * 反序列化状态（用于恢复）
   */
  static deserialize(json: string, config: CharacterBuilderConfig): CharacterBuilderStateMachine {
    const { context } = JSON.parse(json);
    const builder = new CharacterBuilderStateMachine({
      ...config,
      initialContext: context,
    });
    return builder;
  }
}
