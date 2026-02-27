/**
 * D&D 5e 车卡系统 - 类型定义
 */

// ============================================================================
// 基础类型
// ============================================================================

export type AbilityScore = 'str' | 'dex' | 'con' | 'int' | 'wis' | 'cha';

export type Size = 'Tiny' | 'Small' | 'Medium' | 'Large' | 'Huge' | 'Gargantuan';

export type Alignment = 
  | 'lawful-good' | 'lawful-neutral' | 'lawful-evil'
  | 'neutral-good' | 'neutral' | 'neutral-evil'
  | 'chaotic-good' | 'chaotic-neutral' | 'chaotic-evil';

export type Skill = 
  | 'acrobatics' | 'animal-handling' | 'arcana' | 'athletics'
  | 'deception' | 'history' | 'insight' | 'intimidation'
  | 'investigation' | 'medicine' | 'nature' | 'perception'
  | 'performance' | 'persuasion' | 'religion' | 'sleight-of-hand'
  | 'stealth' | 'survival';

// ============================================================================
// 数据来源
// ============================================================================

export enum DataSourceType {
  CORE = 'core',
  EXTENSION = 'extension',
  HOMEBREW = 'homebrew',
}

export interface DataSource {
  id: string;
  type: DataSourceType;
  name: string;
  version: string;
  dependencies?: string[];
  priority: number;
  enabled: boolean;
  metadata: {
    author?: string;
    description?: string;
    coverImage?: string;
    releaseDate?: string;
    license?: string;
  };
}

export interface SourcedData<T> {
  source: DataSource;
  data: T;
  overrides?: string[];
}

// ============================================================================
// 数据类型枚举
// ============================================================================

export enum DataType {
  RACE = 'races',
  SUBRACE = 'subraces',
  CLASS = 'classes',
  SUBCLASS = 'subclasses',
  BACKGROUND = 'backgrounds',
  SPELL = 'spells',
  FEAT = 'feats',
  EQUIPMENT = 'equipment',
  TRAIT = 'traits',
  PROFICIENCY = 'proficiencies',
  SKILL = 'skills',
  ABILITY_SCORE = 'ability-scores',
  LANGUAGE = 'languages',
  LEVEL = 'levels',
  FEATURE = 'features',
}

// ============================================================================
// 游戏数据接口（基于现有JSON结构）
// ============================================================================

export interface APIReference {
  index: string;
  name: string;
  name_en?: string;
  url?: string;
}

export interface AbilityBonus {
  ability_score: APIReference;
  bonus: number;
}

export interface Race {
  index: string;
  name: string;
  name_en: string;
  speed: number;
  ability_bonuses: AbilityBonus[];
  ability_bonus_options?: ChoiceOption;
  alignment: string;
  alignment_en: string;
  age: string;
  age_en: string;
  size: string;
  size_en: string;
  size_description: string;
  size_description_en: string;
  languages: APIReference[];
  language_desc: string;
  language_desc_en: string;
  language_options?: ChoiceOption;
  traits: APIReference[];
  subraces: APIReference[];
  starting_proficiencies?: APIReference[];
  starting_proficiency_options?: ChoiceOption;
  url?: string;
}

export interface Subrace {
  index: string;
  name: string;
  name_en: string;
  race: APIReference;
  desc: string;
  desc_en: string;
  ability_bonuses: AbilityBonus[];
  ability_bonus_options?: ChoiceOption;
  starting_proficiencies?: APIReference[];
  starting_proficiency_options?: ChoiceOption;
  languages?: APIReference[];
  language_options?: ChoiceOption;
  traits: APIReference[];
  url?: string;
}

export interface Class {
  index: string;
  name: string;
  name_en: string;
  hit_die: number;
  proficiency_choices: ChoiceOption[];
  proficiencies: APIReference[];
  saving_throws: APIReference[];
  starting_equipment: StartingEquipment[];
  starting_equipment_options: ChoiceOption[];
  class_levels: string;
  multi_classing?: Multiclassing;
  spellcasting?: Spellcasting;
  subclasses: APIReference[];
  url?: string;
}

export interface Subclass {
  index: string;
  class: APIReference;
  name: string;
  name_en: string;
  subclass_flavor: string;
  desc: string[];
  desc_en: string[];
  spells?: SubclassSpell[];
  subclass_levels: string;
  url?: string;
}

export interface SubclassSpell {
  prerequisites: APIReference[];
  spell: APIReference;
}

export interface Background {
  index: string;
  name: string;
  name_en: string;
  starting_proficiencies: APIReference[];
  language_options?: ChoiceOption;
  starting_equipment: StartingEquipment[];
  starting_equipment_options: ChoiceOption[];
  feature: BackgroundFeature;
  personality_traits: ChoiceOption;
  ideals: ChoiceOption;
  bonds: ChoiceOption;
  flaws: ChoiceOption;
  url?: string;
}

export interface BackgroundFeature {
  name: string;
  name_en: string;
  desc: string[];
  desc_en: string[];
}

export interface Spell {
  index: string;
  name: string;
  name_en?: string;
  desc: string[];
  higher_level?: string[];
  range: string;
  components: ('V' | 'S' | 'M')[];
  material?: string;
  ritual: boolean;
  duration: string;
  concentration: boolean;
  casting_time: string;
  level: number;
  attack_type?: string;
  damage?: Damage;
  school: APIReference;
  classes: APIReference[];
  subclasses: APIReference[];
  url?: string;
}

export interface Feat {
  index: string;
  name: string;
  name_en: string;
  prerequisites?: FeatPrerequisite[];
  desc: string[];
  desc_en: string[];
  url?: string;
}

// ============================================================================
// 通用结构
// ============================================================================

export interface ChoiceOption {
  desc: string;
  desc_en?: string;
  choose: number;
  type: string;
  from: OptionSet;
}

export type OptionSet = 
  | { option_set_type: 'options_array'; options: Option[] }
  | { option_set_type: 'equipment_category'; equipment_category: APIReference }
  | { option_set_type: 'resource_list'; resource_list_url: string };

export type Option =
  | { option_type: 'reference'; item: APIReference }
  | { option_type: 'choice'; choice: ChoiceOption }
  | { option_type: 'string'; string: string };

export interface StartingEquipment {
  equipment: APIReference;
  quantity: number;
}

export interface Multiclassing {
  prerequisites?: MulticlassPrerequisite[];
  prerequisite_options?: ChoiceOption;
  proficiencies: APIReference[];
  proficiency_choices?: ChoiceOption[];
}

export interface MulticlassPrerequisite {
  ability_score: APIReference;
  minimum_score: number;
}

export interface Spellcasting {
  level: number;
  spellcasting_ability: APIReference;
  info: SpellcastingInfo[];
}

export interface SpellcastingInfo {
  name: string;
  desc: string[];
}

export interface Damage {
  damage_type: APIReference;
  damage_at_slot_level?: Record<string, string>;
  damage_at_character_level?: Record<string, string>;
}

// ============================================================================
// 角色数据
// ============================================================================

export interface Character {
  // 基本信息
  id: string;
  name: string;
  playerName?: string;
  
  // 核心属性
  race: CharacterRace;
  classes: CharacterClass[];
  background: string;
  
  // 属性值
  abilityScores: Record<AbilityScore, number>;
  abilityBonuses: Partial<Record<AbilityScore, number>>;
  
  // 派生属性
  proficiencyBonus: number;
  hitPoints: HitPoints;
  armorClass: number;
  speed: number;
  initiative: number;
  
  // 技能和熟练项
  proficiencies: {
    skills: Record<Skill, 'none' | 'proficient' | 'expertise'>;
    savingThrows: Record<AbilityScore, boolean>;
    armor: string[];
    weapons: string[];
    tools: string[];
  };
  
  // 其他
  languages: string[];
  traits: string[];
  features: string[];
  spells?: SpellcastingState;
  equipment: EquipmentItem[];
  
  // 外观和背景
  appearance?: CharacterAppearance;
  personality?: CharacterPersonality;
  
  // 元数据
  createdAt: Date;
  modifiedAt: Date;
  dataSources: string[];
}

export interface CharacterRace {
  index: string;
  name: string;
  subrace?: string;
}

export interface CharacterClass {
  index: string;
  name: string;
  level: number;
  subclass?: string;
  isPrimary?: boolean;
}

export interface HitPoints {
  max: number;
  current: number;
  temp: number;
  hitDice: Record<string, { total: number; remaining: number }>;
}

export interface SpellcastingState {
  ability: AbilityScore;
  saveDC: number;
  attackBonus: number;
  spellsKnown: Record<number, string[]>; // level -> spell indices
  spellSlots: Record<number, { total: number; remaining: number }>;
  cantripsKnown: string[];
}

export interface EquipmentItem {
  index: string;
  name: string;
  quantity: number;
  equipped?: boolean;
  attuned?: boolean;
  notes?: string;
}

export interface CharacterAppearance {
  age?: number;
  height?: string;
  weight?: string;
  eyes?: string;
  skin?: string;
  hair?: string;
  description?: string;
}

export interface CharacterPersonality {
  traits?: string[];
  ideals?: string;
  bonds?: string;
  flaws?: string;
}

// ============================================================================
// 车卡系统
// ============================================================================

export interface BuildContext {
  version: string;
  character: Partial<Character>;
  completedSteps: string[];
  currentStepId: string | null;
  history: BuildAction[];
  historyIndex: number;
  metadata: {
    createdAt: Date;
    modifiedAt: Date;
    dataSources: string[];
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
  | { type: 'SET_DETAILS'; payload: CharacterDetails }
  | { type: 'UNDO' }
  | { type: 'REDO' }
  | { type: 'RESET' };

export interface RaceSelection {
  raceId: string;
  subraceId?: string;
  abilityBonusChoice?: Record<string, string>;
  proficiencyChoices?: string[];
  languageChoices?: string[];
}

export interface ClassSelection {
  classId: string;
  subclassId?: string;
  level?: number;
  isMulticlass?: boolean;
  skillChoices?: string[];
  equipmentChoices?: EquipmentChoice[];
}

export interface AbilityAllocation {
  method: 'point-buy' | 'standard-array' | 'roll';
  scores: Record<AbilityScore, number>;
  racialBonusesApplied?: boolean;
}

export interface BackgroundSelection {
  backgroundId: string;
  proficiencyChoices?: string[];
  languageChoices?: string[];
  equipmentChoices?: EquipmentChoice[];
  personalityTraits?: string[];
  ideal?: string;
  bond?: string;
  flaw?: string;
}

export interface SpellSelection {
  cantrips: string[];
  spells: string[];
  prepared?: string[];
}

export interface FeatSelection {
  featId: string;
  abilityScoreImprovement?: Partial<Record<AbilityScore, number>>;
  choices?: Record<string, unknown>;
}

export interface EquipmentPurchase {
  items: { index: string; quantity: number }[];
  startingGold?: number;
  remainingGold: number;
}

export interface EquipmentChoice {
  optionIndex: number;
  selected: string;
  quantity?: number;
}

export interface CharacterDetails {
  name?: string;
  playerName?: string;
  alignment?: Alignment;
  appearance?: CharacterAppearance;
  personality?: CharacterPersonality;
}

// ============================================================================
// 步骤系统
// ============================================================================

export interface BuilderStep {
  id: string;
  name: string;
  order: number;
  shouldShow(context: BuildContext): boolean;
  checkDependencies(context: BuildContext): DependencyResult;
  validate(context: BuildContext): ValidationResult;
  getOptions(context: BuildContext): StepOption[];
  execute(context: BuildContext, selection: unknown): BuildContext;
  rollback?(context: BuildContext): BuildContext;
}

export interface DependencyResult {
  satisfied: boolean;
  blockingSteps?: string[];
  message?: string;
}

export interface ValidationResult {
  valid: boolean;
  errors?: ValidationError[];
  warnings?: ValidationError[];
}

export interface ValidationError {
  code: string;
  message: string;
  field?: string;
  severity?: 'error' | 'warning' | 'info';
}

export interface StepOption {
  id: string;
  name: string;
  description?: string;
  icon?: string;
  source?: DataSource;
  disabled?: boolean;
  disabledReason?: string;
  details?: Record<string, unknown>;
}

// ============================================================================
// 导出系统
// ============================================================================

export interface ExportFormat {
  id: string;
  name: string;
  extension: string;
  mimeType: string;
  serialize(character: Character): string | Blob;
}

export interface ExportResult {
  filename: string;
  mimeType: string;
  data: string | Blob;
}

// ============================================================================
// 插件系统
// ============================================================================

export interface ExtensionManifest {
  id: string;
  name: string;
  version: string;
  description?: string;
  author?: string;
  dependencies: {
    core?: string;
    extensions?: string[];
  };
  dataFiles: Partial<Record<DataType, string>>;
  customSteps?: CustomStepDefinition[];
  ruleOverrides?: RuleOverride[];
  validators?: string[];
  calculators?: string[];
}

export interface CustomStepDefinition {
  id: string;
  name: string;
  order: number;
  condition?: {
    requiresClass?: string[];
    requiresRace?: string[];
    requiresLevel?: { min?: number; max?: number };
    customScript?: string;
  };
  optionsProvider: string;
  executor: string;
}

export interface RuleOverride {
  target: string;
  property: string;
  value: unknown;
  condition?: string;
}
