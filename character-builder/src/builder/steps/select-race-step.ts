/**
 * 选择种族步骤
 */

import {
  BuilderStep,
  BuildContext,
  StepOption,
  ValidationResult,
  DependencyResult,
  Race,
  Subrace,
  RaceSelection,
  DataType,
} from '../../types';
import { getGlobalRegistry } from '../../core/data-registry';
import { produce } from '../../core/utils/immutable';

export class SelectRaceStep implements BuilderStep {
  id = 'select-race';
  name = '选择种族';
  order = 10;

  shouldShow(): boolean {
    return true; // 始终显示
  }

  checkDependencies(): DependencyResult {
    return { satisfied: true }; // 无依赖
  }

  validate(context: BuildContext): ValidationResult {
    if (!context.character.race) {
      return {
        valid: false,
        errors: [{ code: 'RACE_REQUIRED', message: '请选择一个种族', field: 'race' }],
      };
    }

    // 验证亚种族（如果有）
    const race = getGlobalRegistry().getById<Race>(DataType.RACE, context.character.race.index);
    if (race?.subraces?.length > 0 && !context.character.race.subrace) {
      // 亚种族是可选的，但如果选择了，要验证有效性
    }

    return { valid: true };
  }

  getOptions(): StepOption[] {
    const registry = getGlobalRegistry();
    const races = registry.getActiveData<Race>(DataType.RACE);

    return races.map(r => ({
      id: r.data.index,
      name: r.data.name,
      nameEn: r.data.name_en,
      description: this.truncateDesc(r.data.alignment, 100),
      icon: `/icons/races/${r.data.index}.png`,
      source: r.source,
      details: {
        speed: r.data.speed,
        size: r.data.size,
        abilityBonuses: r.data.ability_bonuses.map(ab => ({
          ability: ab.ability_score.index,
          bonus: ab.bonus,
        })),
        traits: r.data.traits.map(t => ({
          index: t.index,
          name: t.name,
        })),
        languages: r.data.languages.map(l => ({
          index: l.index,
          name: l.name,
        })),
        hasSubraces: r.data.subraces?.length > 0,
        subraces: r.data.subraces?.map(s => s.index) || [],
      },
    }));
  }

  /**
   * 获取亚种族选项
   */
  getSubraceOptions(raceId: string): StepOption[] {
    const registry = getGlobalRegistry();
    const race = registry.getById<Race>(DataType.RACE, raceId);
    
    if (!race?.subraces?.length) {
      return [];
    }

    return race.subraces.map(sr => {
      const subraceData = registry.getById<Subrace>(DataType.SUBRACE, sr.index);
      return {
        id: sr.index,
        name: subraceData?.name || sr.name,
        nameEn: subraceData?.name_en,
        description: subraceData?.desc,
        details: subraceData ? {
          abilityBonuses: subraceData.ability_bonuses?.map(ab => ({
            ability: ab.ability_score.index,
            bonus: ab.bonus,
          })),
          traits: subraceData.traits?.map(t => ({
            index: t.index,
            name: t.name,
          })),
        } : undefined,
      };
    });
  }

  execute(context: BuildContext, selection: RaceSelection): BuildContext {
    const registry = getGlobalRegistry();
    const race = registry.getById<Race>(DataType.RACE, selection.raceId);

    if (!race) {
      throw new Error(`Race '${selection.raceId}' not found`);
    }

    return produce(context, draft => {
      // 清除之前的种族数据
      draft.character.race = undefined;
      draft.character.abilityBonuses = {};
      draft.character.traits = [];
      draft.character.languages = [];
      draft.character.proficiencies = {
        skills: {},
        savingThrows: {},
        armor: [],
        weapons: [],
        tools: [],
      };

      // 设置种族
      draft.character.race = {
        index: selection.raceId,
        name: race.name,
        subrace: selection.subraceId,
      };

      // 应用种族属性加成
      if (race.ability_bonuses) {
        for (const bonus of race.ability_bonuses) {
          const ability = bonus.ability_score.index;
          draft.character.abilityBonuses[ability] = 
            (draft.character.abilityBonuses[ability] || 0) + bonus.bonus;
        }
      }

      // 处理属性加成选择（例如：半精灵）
      if (selection.abilityBonusChoice && race.ability_bonus_options) {
        for (const [ability, value] of Object.entries(selection.abilityBonusChoice)) {
          draft.character.abilityBonuses[ability] = 
            (draft.character.abilityBonuses[ability] || 0) + parseInt(value, 10);
        }
      }

      // 应用亚种族
      if (selection.subraceId) {
        const subrace = registry.getById<Subrace>(DataType.SUBRACE, selection.subraceId);
        if (subrace) {
          // 应用亚种族属性加成
          if (subrace.ability_bonuses) {
            for (const bonus of subrace.ability_bonuses) {
              const ability = bonus.ability_score.index;
              draft.character.abilityBonuses[ability] = 
                (draft.character.abilityBonuses[ability] || 0) + bonus.bonus;
            }
          }

          // 应用亚种族特性
          if (subrace.traits) {
            draft.character.traits.push(...subrace.traits.map(t => t.index));
          }

          // 应用亚种族语言
          if (subrace.languages) {
            draft.character.languages.push(...subrace.languages.map(l => l.index));
          }

          // 处理亚种族语言选择
          if (selection.languageChoices && subrace.language_options) {
            for (const lang of selection.languageChoices) {
              if (!draft.character.languages.includes(lang)) {
                draft.character.languages.push(lang);
              }
            }
          }
        }
      }

      // 应用种族特性
      if (race.traits) {
        draft.character.traits.push(...race.traits.map(t => t.index));
      }

      // 应用种族语言
      if (race.languages) {
        draft.character.languages.push(...race.languages.map(l => l.index));
      }

      // 处理种族语言选择
      if (selection.languageChoices && race.language_options) {
        for (const lang of selection.languageChoices) {
          if (!draft.character.languages.includes(lang)) {
            draft.character.languages.push(lang);
          }
        }
      }

      // 应用种族起始熟练项
      if (race.starting_proficiencies) {
        for (const prof of race.starting_proficiencies) {
          this.addProficiency(draft, prof.index);
        }
      }

      // 处理种族熟练项选择
      if (selection.proficiencyChoices && race.starting_proficiency_options) {
        for (const prof of selection.proficiencyChoices) {
          this.addProficiency(draft, prof);
        }
      }

      // 标记步骤完成
      this.markStepComplete(draft);
    });
  }

  rollback(context: BuildContext): BuildContext {
    return produce(context, draft => {
      draft.character.race = undefined;
      draft.character.abilityBonuses = {};
      draft.character.traits = [];
      draft.character.languages = [];
      draft.character.proficiencies = {
        skills: {},
        savingThrows: {},
        armor: [],
        weapons: [],
        tools: [],
      };
      this.unmarkStepComplete(draft);
    });
  }

  /**
   * 获取种族的详细预览信息
   */
  getRacePreview(raceId: string): {
    baseAttributes: Record<string, unknown>;
    traits: { name: string; description: string }[];
    abilityBonuses: { ability: string; bonus: number }[];
  } {
    const registry = getGlobalRegistry();
    const race = registry.getById<Race>(DataType.RACE, raceId);
    
    if (!race) {
      throw new Error(`Race '${raceId}' not found`);
    }

    return {
      baseAttributes: {
        speed: race.speed,
        size: race.size,
      },
      traits: race.traits?.map(t => ({
        name: t.name,
        description: '', // 需要从traits数据加载
      })) || [],
      abilityBonuses: race.ability_bonuses?.map(ab => ({
        ability: ab.ability_score.index,
        bonus: ab.bonus,
      })) || [],
    };
  }

  private truncateDesc(text: string, maxLength: number): string {
    if (!text || text.length <= maxLength) return text || '';
    return text.substring(0, maxLength) + '...';
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
      draft.character.proficiencies.skills[skill] = 'proficient';
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
