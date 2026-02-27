/**
 * 角色计算器 - 计算角色的派生属性
 */

import {
  Character,
  DataType,
  Class,
  Race,
  AbilityScore,
} from '../types';
import { DataRegistry } from '../core/data-registry';

export class CharacterCalculator {
  constructor(private dataRegistry: DataRegistry) {}

  /**
   * 计算最终角色属性
   */
  calculateFinal(character: Partial<Character>): Character {
    const base = { ...character } as Character;

    // 计算派生属性
    base.proficiencyBonus = this.calculateProficiencyBonus(base);
    base.armorClass = this.calculateArmorClass(base);
    base.initiative = this.calculateInitiative(base);
    base.speed = this.calculateSpeed(base);
    base.hitPoints = this.calculateHitPoints(base);

    // 计算施法属性（如果是施法者）
    if (base.spells) {
      base.spells.saveDC = this.calculateSpellSaveDC(base);
      base.spells.attackBonus = this.calculateSpellAttackBonus(base);
    }

    return base;
  }

  /**
   * 计算熟练加值
   */
  calculateProficiencyBonus(character: Character): number {
    const totalLevel = character.classes?.reduce((sum, c) => sum + c.level, 0) || 1;
    return Math.floor((totalLevel - 1) / 4) + 2;
  }

  /**
   * 计算护甲等级
   */
  calculateArmorClass(character: Character): number {
    // 基础AC计算
    const dexMod = this.getAbilityModifier(character, 'dex');
    
    // 默认无甲防御
    let baseAC = 10 + dexMod;

    // 检查是否有野蛮人无甲防御
    const hasBarbarianUnarmored = character.classes?.some(
      c => c.index === 'barbarian' && !this.isWearingArmor(character)
    );
    if (hasBarbarianUnarmored) {
      const conMod = this.getAbilityModifier(character, 'con');
      baseAC = Math.max(baseAC, 10 + dexMod + conMod);
    }

    // 检查是否有武僧无甲防御
    const hasMonkUnarmored = character.classes?.some(
      c => c.index === 'monk' && !this.isWearingArmor(character) && !this.isWieldingShield(character)
    );
    if (hasMonkUnarmored) {
      const wisMod = this.getAbilityModifier(character, 'wis');
      baseAC = Math.max(baseAC, 10 + dexMod + wisMod);
    }

    // TODO: 考虑装备提供的AC

    return baseAC;
  }

  /**
   * 计算先攻
   */
  calculateInitiative(character: Character): number {
    return this.getAbilityModifier(character, 'dex');
  }

  /**
   * 计算速度
   */
  calculateSpeed(character: Character): number {
    if (!character.race) return 30;

    const race = this.dataRegistry.getById<Race>(DataType.RACE, character.race.index);
    return race?.speed || 30;
  }

  /**
   * 计算生命值
   */
  calculateHitPoints(character: Character): Character['hitPoints'] {
    const conMod = this.getAbilityModifier(character, 'con');
    const classes = character.classes || [];

    let maxHP = 0;
    const hitDice: Character['hitPoints']['hitDice'] = {};

    for (const cls of classes) {
      const classData = this.dataRegistry.getById<Class>(DataType.CLASS, cls.index);
      if (!classData) continue;

      const hitDie = classData.hit_die;
      const level = cls.level;

      // 计算此职业的生命值
      // 第一级取最大值，后续取平均值（向上取整）
      const firstLevelHP = hitDie + conMod;
      const subsequentLevelsHP = (level - 1) * (Math.floor(hitDie / 2) + 1 + conMod);
      
      maxHP += firstLevelHP + subsequentLevelsHP;

      // 记录生命骰
      const dieType = `d${hitDie}`;
      if (!hitDice[dieType]) {
        hitDice[dieType] = { total: 0, remaining: 0 };
      }
      hitDice[dieType].total += level;
      hitDice[dieType].remaining += level;
    }

    // 如果还没有职业，使用默认值
    if (classes.length === 0) {
      maxHP = 8 + conMod;
    }

    return {
      max: Math.max(maxHP, 1),
      current: character.hitPoints?.current || maxHP,
      temp: character.hitPoints?.temp || 0,
      hitDice,
    };
  }

  /**
   * 计算法术豁免DC
   */
  calculateSpellSaveDC(character: Character): number {
    if (!character.spells?.ability) return 10;

    const mod = this.getAbilityModifier(character, character.spells.ability);
    const profBonus = this.calculateProficiencyBonus(character);

    return 8 + mod + profBonus;
  }

  /**
   * 计算法术攻击加值
   */
  calculateSpellAttackBonus(character: Character): number {
    if (!character.spells?.ability) return 0;

    const mod = this.getAbilityModifier(character, character.spells.ability);
    const profBonus = this.calculateProficiencyBonus(character);

    return mod + profBonus;
  }

  /**
   * 获取属性修正值
   */
  getAbilityModifier(character: Character, ability: AbilityScore): number {
    const baseScore = character.abilityScores?.[ability] || 10;
    const bonus = character.abilityBonuses?.[ability] || 0;
    const totalScore = baseScore + bonus;

    return Math.floor((totalScore - 10) / 2);
  }

  /**
   * 获取技能加值
   */
  getSkillBonus(character: Character, skill: string): number {
    // 技能对应的属性
    const skillToAbility: Record<string, AbilityScore> = {
      'acrobatics': 'dex',
      'animal-handling': 'wis',
      'arcana': 'int',
      'athletics': 'str',
      'deception': 'cha',
      'history': 'int',
      'insight': 'wis',
      'intimidation': 'cha',
      'investigation': 'int',
      'medicine': 'wis',
      'nature': 'int',
      'perception': 'wis',
      'performance': 'cha',
      'persuasion': 'cha',
      'religion': 'int',
      'sleight-of-hand': 'dex',
      'stealth': 'dex',
      'survival': 'wis',
    };

    const ability = skillToAbility[skill];
    if (!ability) return 0;

    const abilityMod = this.getAbilityModifier(character, ability);
    const proficiency = character.proficiencies?.skills?.[skill];

    if (proficiency === 'expertise') {
      return abilityMod + (this.calculateProficiencyBonus(character) * 2);
    } else if (proficiency === 'proficient') {
      return abilityMod + this.calculateProficiencyBonus(character);
    }

    return abilityMod;
  }

  /**
   * 获取豁免加值
   */
  getSaveBonus(character: Character, ability: AbilityScore): number {
    const abilityMod = this.getAbilityModifier(character, ability);
    const isProficient = character.proficiencies?.savingThrows?.[ability];

    if (isProficient) {
      return abilityMod + this.calculateProficiencyBonus(character);
    }

    return abilityMod;
  }

  /**
   * 检查是否穿戴护甲
   */
  private isWearingArmor(character: Character): boolean {
    // TODO: 检查装备
    return false;
  }

  /**
   * 检查是否持盾
   */
  private isWieldingShield(character: Character): boolean {
    // TODO: 检查装备
    return false;
  }

  /**
   * 计算被动察觉
   */
  calculatePassivePerception(character: Character): number {
    const base = 10;
    const wisdomMod = this.getAbilityModifier(character, 'wis');
    const perceptionProficiency = character.proficiencies?.skills?.['perception'];
    
    let bonus = wisdomMod;
    if (perceptionProficiency === 'expertise') {
      bonus += this.calculateProficiencyBonus(character) * 2;
    } else if (perceptionProficiency === 'proficient') {
      bonus += this.calculateProficiencyBonus(character);
    }

    // 观察专长可能会提供加值
    if (character.features?.includes('Observant')) {
      bonus += 5;
    }

    return base + bonus;
  }

  /**
   * 计算负重能力
   */
  calculateCarryingCapacity(character: Character): { 
    light: number; 
    medium: number; 
    heavy: number; 
    pushDragLift: number;
  } {
    const strScore = (character.abilityScores?.str || 10) + 
                     (character.abilityBonuses?.str || 0);
    
    // 大小调整（小体型减半）
    const sizeMultiplier = this.getSize(character) === 'Small' ? 0.5 : 1;
    
    const heavy = Math.floor(strScore * 15 * sizeMultiplier);
    
    return {
      light: Math.floor(heavy * 1/3),
      medium: Math.floor(heavy * 2/3),
      heavy: heavy,
      pushDragLift: heavy * 2,
    };
  }

  /**
   * 获取体型
   */
  private getSize(character: Character): string {
    if (!character.race) return 'Medium';
    
    const race = this.dataRegistry.getById<Race>(DataType.RACE, character.race.index);
    return race?.size || 'Medium';
  }
}
