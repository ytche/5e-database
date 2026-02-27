/**
 * 选择职业步骤
 */

import {
  BuilderStep,
  BuildContext,
  StepOption,
  ValidationResult,
  DependencyResult,
  Class,
  Subclass,
  ClassSelection,
  DataType,
} from '../../types';
import { getGlobalRegistry } from '../../core/data-registry';
import { produce } from '../../core/utils/immutable';

export class SelectClassStep implements BuilderStep {
  id = 'select-class';
  name = '选择职业';
  order = 20;

  shouldShow(): boolean {
    return true;
  }

  checkDependencies(context: BuildContext): DependencyResult {
    // 可以选择依赖种族步骤完成
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
    const classes = context.character.classes;
    
    if (!classes || classes.length === 0) {
      return {
        valid: false,
        errors: [{ code: 'CLASS_REQUIRED', message: '请至少选择一个职业', field: 'class' }],
      };
    }

    // 验证主职业
    const primaryClass = classes.find(c => c.isPrimary);
    if (!primaryClass) {
      return {
        valid: false,
        errors: [{ code: 'PRIMARY_CLASS_REQUIRED', message: '需要一个主职业', field: 'class' }],
      };
    }

    // 验证职业等级总和
    const totalLevel = classes.reduce((sum, c) => sum + c.level, 0);
    if (totalLevel > 20) {
      return {
        valid: false,
        errors: [{ 
          code: 'LEVEL_EXCEEDED', 
          message: `总等级 ${totalLevel} 超过最大等级 20`, 
          field: 'level' 
        }],
      };
    }

    // 验证多职业前置条件
    if (classes.length > 1) {
      const errors = this.validateMulticlassPrerequisites(context);
      if (errors.length > 0) {
        return { valid: false, errors };
      }
    }

    return { valid: true };
  }

  getOptions(context: BuildContext): StepOption[] {
    const registry = getGlobalRegistry();
    const classes = registry.getActiveData<Class>(DataType.CLASS);
    const isMulticlass = (context.character.classes?.length || 0) > 0;

    return classes.map(c => {
      const classData = c.data;
      const prerequisites = classData.multi_classing?.prerequisites;
      
      return {
        id: classData.index,
        name: classData.name,
        nameEn: classData.name_en,
        description: `生命骰: d${classData.hit_die}`,
        icon: `/icons/classes/${classData.index}.png`,
        source: c.source,
        disabled: isMulticlass ? !this.meetsPrerequisites(context, classData) : false,
        disabledReason: isMulticlass && !this.meetsPrerequisites(context, classData) 
          ? '不满足多职业前置条件' 
          : undefined,
        details: {
          hitDie: classData.hit_die,
          isSpellcaster: !!classData.spellcasting,
          spellcastingAbility: classData.spellcasting?.spellcasting_ability?.index,
          primaryAbilities: this.getPrimaryAbilities(classData),
          savingThrows: classData.saving_throws?.map(s => s.index) || [],
          skillChoices: {
            count: classData.proficiency_choices?.[0]?.choose || 0,
            options: classData.proficiency_choices?.[0]?.from?.options
              ?.filter(o => o.option_type === 'reference')
              .map(o => (o as { item: { index: string; name: string } }).item.index.replace('skill-', '')) || [],
          },
          armorProficiencies: classData.proficiencies
            ?.filter(p => ['light-armor', 'medium-armor', 'heavy-armor', 'shields'].includes(p.index))
            .map(p => p.index) || [],
          weaponProficiencies: classData.proficiencies
            ?.filter(p => ['simple-weapons', 'martial-weapons'].includes(p.index))
            .map(p => p.index) || [],
          subclasses: classData.subclasses?.map(s => s.index) || [],
          prerequisites: prerequisites?.map(p => ({
            ability: p.ability_score.index,
            minimumScore: p.minimum_score,
          })),
        },
      };
    });
  }

  /**
   * 获取子职业选项
   */
  getSubclassOptions(classId: string, level: number = 3): StepOption[] {
    const registry = getGlobalRegistry();
    const cls = registry.getById<Class>(DataType.CLASS, classId);
    
    if (!cls?.subclasses?.length) {
      return [];
    }

    // 检查等级要求（通常3级选择子职业）
    const subclasses = registry.getActiveData<Subclass>(DataType.SUBCLASS)
      .filter(s => s.data.class.index === classId);

    return subclasses.map(s => ({
      id: s.data.index,
      name: s.data.name,
      nameEn: s.data.name_en,
      description: s.data.subclass_flavor,
      source: s.source,
      details: {
        flavor: s.data.subclass_flavor,
        description: s.data.desc?.[0],
        spells: s.data.spells?.map(sp => ({
          level: this.parseLevelFromPrerequisite(sp.prerequisites[0]),
          spell: sp.spell.index,
        })),
      },
    }));
  }

  execute(context: BuildContext, selection: ClassSelection): BuildContext {
    const registry = getGlobalRegistry();
    const cls = registry.getById<Class>(DataType.CLASS, selection.classId);

    if (!cls) {
      throw new Error(`Class '${selection.classId}' not found`);
    }

    return produce(context, draft => {
      const level = selection.level || 1;
      const isMulticlass = selection.isMulticlass && draft.character.classes?.length > 0;

      const classData = {
        index: selection.classId,
        name: cls.name,
        level,
        subclass: selection.subclassId,
        isPrimary: !isMulticlass,
      };

      if (isMulticlass) {
        // 添加为多职业
        draft.character.classes.push(classData);
        
        // 应用多职业熟练项（不是全部，只有 multiclassing.proficiencies）
        if (cls.multi_classing?.proficiencies) {
          for (const prof of cls.multi_classing.proficiencies) {
            this.addProficiency(draft, prof.index);
          }
        }
      } else {
        // 设置为主职业（替换或初始化）
        draft.character.classes = [classData];
        
        // 清除之前的职业熟练项
        draft.character.proficiencies.savingThrows = {};
        
        // 应用完整职业熟练项
        if (cls.proficiencies) {
          for (const prof of cls.proficiencies) {
            this.addProficiency(draft, prof.index);
          }
        }

        // 应用豁免熟练
        if (cls.saving_throws) {
          for (const save of cls.saving_throws) {
            draft.character.proficiencies.savingThrows[save.index] = true;
          }
        }
      }

      // 处理技能选择
      if (selection.skillChoices && cls.proficiency_choices?.[0]) {
        for (const skill of selection.skillChoices) {
          draft.character.proficiencies.skills[skill] = 'proficient';
        }
      }

      // 计算并设置生命值
      this.calculateHitPoints(draft);

      this.markStepComplete(draft);
    });
  }

  rollback(context: BuildContext): BuildContext {
    return produce(context, draft => {
      // 如果是多职业，移除最后一个职业
      if (draft.character.classes?.length > 1) {
        draft.character.classes.pop();
      } else {
        draft.character.classes = [];
      }
      this.unmarkStepComplete(draft);
    });
  }

  /**
   * 验证多职业前置条件
   */
  private validateMulticlassPrerequisites(context: BuildContext): import('../../types').ValidationError[] {
    const errors: import('../../types').ValidationError[] = [];
    const registry = getGlobalRegistry();
    const classes = context.character.classes;

    // 从第二个职业开始检查
    for (let i = 1; i < classes.length; i++) {
      const cls = registry.getById<Class>(DataType.CLASS, classes[i].index);
      if (!cls?.multi_classing?.prerequisites) continue;

      for (const prereq of cls.multi_classing.prerequisites) {
        const ability = prereq.ability_score.index;
        const baseScore = context.character.abilityScores?.[ability] || 8;
        const bonus = context.character.abilityBonuses?.[ability] || 0;
        const totalScore = baseScore + bonus;

        if (totalScore < prereq.minimum_score) {
          errors.push({
            code: 'MULTICLASS_PREREQ_NOT_MET',
            message: `${cls.name} 需要 ${ability.toUpperCase()} 至少 ${prereq.minimum_score}（当前 ${totalScore}）`,
            field: `classes[${i}]`,
          });
        }
      }
    }

    return errors;
  }

  /**
   * 检查是否满足多职业前置条件
   */
  private meetsPrerequisites(context: BuildContext, cls: Class): boolean {
    if (!cls.multi_classing?.prerequisites) {
      return true;
    }

    return cls.multi_classing.prerequisites.every(prereq => {
      const ability = prereq.ability_score.index;
      const baseScore = context.character.abilityScores?.[ability] || 8;
      const bonus = context.character.abilityBonuses?.[ability] || 0;
      return (baseScore + bonus) >= prereq.minimum_score;
    });
  }

  /**
   * 获取主要属性（基于豁免和熟练项推断）
   */
  private getPrimaryAbilities(cls: Class): string[] {
    const abilities = new Set<string>();
    
    // 从豁免推断
    cls.saving_throws?.forEach(st => abilities.add(st.index));
    
    // 从施法能力推断
    if (cls.spellcasting?.spellcasting_ability) {
      abilities.add(cls.spellcasting.spellcasting_ability.index);
    }
    
    return Array.from(abilities);
  }

  /**
   * 计算生命值
   */
  private calculateHitPoints(draft: BuildContext): void {
    // 简化计算，实际应该基于等级、体质等计算
    // 这里只是示例
  }

  private addProficiency(draft: BuildContext, proficiencyId: string): void {
    if (!draft.character.proficiencies) {
      draft.character.proficiencies = {
        skills: {},
        savingThrows: {},
        armor: [],
        weapons: [],
        tools: [],
      };
    }

    if (proficiencyId.startsWith('skill-')) {
      const skill = proficiencyId.replace('skill-', '');
      if (!draft.character.proficiencies.skills[skill]) {
        draft.character.proficiencies.skills[skill] = 'proficient';
      }
    } else if (['light-armor', 'medium-armor', 'heavy-armor', 'shields'].includes(proficiencyId)) {
      if (!draft.character.proficiencies.armor.includes(proficiencyId)) {
        draft.character.proficiencies.armor.push(proficiencyId);
      }
    } else if (['simple-weapons', 'martial-weapons'].includes(proficiencyId)) {
      if (!draft.character.proficiencies.weapons.includes(proficiencyId)) {
        draft.character.proficiencies.weapons.push(proficiencyId);
      }
    } else {
      if (!draft.character.proficiencies.tools.includes(proficiencyId)) {
        draft.character.proficiencies.tools.push(proficiencyId);
      }
    }
  }

  private parseLevelFromPrerequisite(prereq: { index: string; type: string }): number {
    // 解析 "cleric-3" -> 3
    const match = prereq.index.match(/-(\d+)$/);
    return match ? parseInt(match[1], 10) : 1;
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
