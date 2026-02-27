/**
 * 基础使用示例
 * 
 * 这个示例展示了如何使用车卡系统创建一个精灵法师角色
 */

import { 
  CharacterBuilder, 
  DataRegistry,
  BuildContext,
} from '../src';

// 模拟数据加载
async function loadSRDData(registry: DataRegistry) {
  // 注册核心数据源
  registry.registerSource({
    id: 'srd-2014-zh',
    type: 'core' as const,
    name: 'D&D 5e SRD 2014 中文版',
    version: '1.0.0',
    priority: 100,
    enabled: true,
    metadata: {
      author: 'Wizards of the Coast',
      license: 'OGL',
    },
  });

  // 加载种族数据（示例）
  registry.loadData('races', 'srd-2014-zh', [
    {
      index: 'elf',
      name: '精灵',
      name_en: 'Elf',
      speed: 30,
      ability_bonuses: [
        { ability_score: { index: 'dex', name: 'DEX', url: '' }, bonus: 2 }
      ],
      alignment: '精灵热爱自由、多样性...',
      alignment_en: 'Elves love freedom...',
      age: '虽然精灵大约在与人类相同的年龄达到生理成熟...',
      age_en: 'Although elves reach physical maturity...',
      size: '中型',
      size_en: 'Medium',
      size_description: '精灵身高从5英尺到6英尺不等...',
      size_description_en: 'Elves range from under 5 to over 6 feet tall...',
      languages: [
        { index: 'common', name: '通用语', name_en: 'Common', url: '' },
        { index: 'elvish', name: '精灵语', name_en: 'Elvish', url: '' }
      ],
      language_desc: '你能说、读、写通用语和精灵语...',
      language_desc_en: 'You can speak, read, and write Common and Elvish...',
      traits: [
        { index: 'darkvision', name: '黑暗视觉', name_en: 'Darkvision', url: '' },
        { index: 'fey-ancestry', name: '妖精血统', name_en: 'Fey Ancestry', url: '' },
        { index: 'trance', name: '出神', name_en: 'Trance', url: '' },
        { index: 'keen-senses', name: '敏锐感官', name_en: 'Keen Senses', url: '' }
      ],
      subraces: [
        { index: 'high-elf', name: '高等精灵', name_en: 'High Elf', url: '' }
      ]
    },
    {
      index: 'human',
      name: '人类',
      name_en: 'Human',
      speed: 30,
      ability_bonuses: [
        { ability_score: { index: 'str', name: 'STR', url: '' }, bonus: 1 },
        { ability_score: { index: 'dex', name: 'DEX', url: '' }, bonus: 1 },
        { ability_score: { index: 'con', name: 'CON', url: '' }, bonus: 1 },
        { ability_score: { index: 'int', name: 'INT', url: '' }, bonus: 1 },
        { ability_score: { index: 'wis', name: 'WIS', url: '' }, bonus: 1 },
        { ability_score: { index: 'cha', name: 'CHA', url: '' }, bonus: 1 }
      ],
      alignment: '人类没有特定的阵营倾向...',
      age: '人类在十几岁时成年...',
      size: '中型',
      size_description: '人类身高差异很大...',
      languages: [
        { index: 'common', name: '通用语', name_en: 'Common', url: '' }
      ],
      language_options: {
        choose: 1,
        type: 'languages',
        from: {
          option_set_type: 'resource_list',
          resource_list_url: '/api/languages'
        }
      },
      language_desc: '你能说、读、写通用语和一种自选语言...',
      traits: []
    }
  ]);

  // 加载亚种族数据
  registry.loadData('subraces', 'srd-2014-zh', [
    {
      index: 'high-elf',
      name: '高等精灵',
      name_en: 'High Elf',
      race: { index: 'elf', name: '精灵', url: '' },
      desc: '作为高等精灵，你有敏锐的头脑和基本的魔法能力...',
      desc_en: 'As a high elf, you have a keen mind and a mastery of at least the basics of magic...',
      ability_bonuses: [
        { ability_score: { index: 'int', name: 'INT', url: '' }, bonus: 1 }
      ],
      traits: [
        { index: 'elf-weapon-training', name: '精灵武器训练', name_en: 'Elf Weapon Training', url: '' },
        { index: 'cantrip', name: '戏法', name_en: 'Cantrip', url: '' },
        { index: 'extra-language', name: '额外语言', name_en: 'Extra Language', url: '' }
      ]
    }
  ]);

  // 加载职业数据
  registry.loadData('classes', 'srd-2014-zh', [
    {
      index: 'wizard',
      name: '法师',
      name_en: 'Wizard',
      hit_die: 6,
      proficiency_choices: [
        {
          desc: '从奥秘、历史、洞悉、调查、医药、宗教中选择两项',
          desc_en: 'Choose two from Arcana, History, Insight, Investigation, Medicine, and Religion',
          choose: 2,
          type: 'proficiencies',
          from: {
            option_set_type: 'options_array',
            options: [
              { option_type: 'reference', item: { index: 'skill-arcana', name: '技能：奥秘', name_en: 'Skill: Arcana', url: '' } },
              { option_type: 'reference', item: { index: 'skill-history', name: '技能：历史', name_en: 'Skill: History', url: '' } },
              { option_type: 'reference', item: { index: 'skill-insight', name: '技能：洞悉', name_en: 'Skill: Insight', url: '' } },
              { option_type: 'reference', item: { index: 'skill-investigation', name: '技能：调查', name_en: 'Skill: Investigation', url: '' } }
            ]
          }
        }
      ],
      proficiencies: [
        { index: 'daggers', name: '匕首', name_en: 'Daggers', url: '' },
        { index: 'darts', name: '飞镖', name_en: 'Darts', url: '' },
        { index: 'slings', name: '投石索', name_en: 'Slings', url: '' },
        { index: 'quarterstaffs', name: '长棍', name_en: 'Quarterstaffs', url: '' },
        { index: 'light-crossbows', name: '轻弩', name_en: 'Light Crossbows', url: '' }
      ],
      saving_throws: [
        { index: 'int', name: 'INT', url: '' },
        { index: 'wis', name: 'WIS', url: '' }
      ],
      starting_equipment: [],
      starting_equipment_options: [],
      class_levels: '/api/classes/wizard/levels',
      spellcasting: {
        level: 1,
        spellcasting_ability: { index: 'int', name: 'INT', url: '' },
        info: [
          { name: '法术位', desc: ['1级时，你拥有两个1级法术位'] }
        ]
      },
      subclasses: [
        { index: 'abjuration', name: '防护', name_en: 'Abjuration', url: '' }
      ]
    },
    {
      index: 'fighter',
      name: '战士',
      name_en: 'Fighter',
      hit_die: 10,
      proficiency_choices: [
        {
          desc: '从杂技、驯兽、运动、历史、洞悉、威吓、察觉、生存中选择两项',
          choose: 2,
          type: 'proficiencies',
          from: {
            option_set_type: 'options_array',
            options: []
          }
        }
      ],
      proficiencies: [
        { index: 'light-armor', name: '轻甲', name_en: 'Light Armor', url: '' },
        { index: 'medium-armor', name: '中甲', name_en: 'Medium Armor', url: '' },
        { index: 'heavy-armor', name: '重甲', name_en: 'Heavy Armor', url: '' },
        { index: 'shields', name: '盾牌', name_en: 'Shields', url: '' },
        { index: 'simple-weapons', name: '简易武器', name_en: 'Simple Weapons', url: '' },
        { index: 'martial-weapons', name: '军用武器', name_en: 'Martial Weapons', url: '' }
      ],
      saving_throws: [
        { index: 'str', name: 'STR', url: '' },
        { index: 'con', name: 'CON', url: '' }
      ],
      starting_equipment: [],
      starting_equipment_options: [],
      class_levels: '/api/classes/fighter/levels',
      subclasses: [
        { index: 'champion', name: '勇士', name_en: 'Champion', url: '' }
      ]
    }
  ]);

  console.log('✓ SRD数据加载完成');
}

// 示例：创建一个精灵法师
async function createElfWizard() {
  console.log('\n=== 创建精灵法师角色 ===\n');

  // 创建数据注册表
  const dataRegistry = new DataRegistry();
  await loadSRDData(dataRegistry);

  // 创建车卡器
  const builder = new CharacterBuilder({
    dataRegistry,
    dataSources: ['srd-2014-zh'],
  });

  await builder.initialize();

  // 订阅状态变化
  const unsubscribe = builder.subscribe((context: BuildContext) => {
    console.log(`\n[状态更新] 已完成步骤: ${context.completedSteps.join(', ') || '无'}`);
  });

  // ===== 第1步：选择种族 =====
  console.log('\n--- 第1步：选择种族 ---');
  
  const raceStep = builder.getCurrentStep();
  console.log(`当前步骤: ${raceStep?.name}`);
  
  const raceOptions = raceStep?.getOptions(builder.getContext());
  console.log('可用种族:', raceOptions?.map(r => r.name).join(', '));

  // 选择高等精灵
  builder.dispatch({
    type: 'SELECT_RACE',
    payload: {
      raceId: 'elf',
      subraceId: 'high-elf',
    }
  });

  console.log('✓ 已选择：高等精灵');
  console.log('种族属性加成:', builder.getContext().character.abilityBonuses);

  // ===== 第2步：选择职业 =====
  builder.nextStep();
  console.log('\n--- 第2步：选择职业 ---');
  
  const classStep = builder.getCurrentStep();
  console.log(`当前步骤: ${classStep?.name}`);
  
  const classOptions = classStep?.getOptions(builder.getContext());
  console.log('可用职业:', classOptions?.map(c => c.name).join(', '));

  // 选择法师
  builder.dispatch({
    type: 'SELECT_CLASS',
    payload: {
      classId: 'wizard',
      level: 1,
      skillChoices: ['arcana', 'investigation'], // 选择奥秘和调查技能
    }
  });

  console.log('✓ 已选择：法师');
  console.log('豁免熟练:', Object.keys(builder.getContext().character.proficiencies?.savingThrows || {}));

  // ===== 第3步：分配属性 =====
  builder.nextStep();
  console.log('\n--- 第3步：分配属性 ---');
  
  const abilityStep = builder.getCurrentStep();
  console.log(`当前步骤: ${abilityStep?.name}`);

  // 使用购点法分配属性
  // 法师主要需要智力，其次是体质和敏捷
  builder.dispatch({
    type: 'ALLOCATE_ABILITIES',
    payload: {
      method: 'point-buy',
      scores: {
        str: 8,
        dex: 14,
        con: 14,
        int: 15,
        wis: 12,
        cha: 8,
      }
    }
  });

  console.log('✓ 属性已分配');
  const abilityScores = builder.getContext().character.abilityScores;
  const abilityBonuses = builder.getContext().character.abilityBonuses;
  
  console.log('基础属性:', abilityScores);
  console.log('种族加成:', abilityBonuses);
  console.log('最终属性:', {
    str: (abilityScores?.str || 0) + (abilityBonuses?.str || 0),
    dex: (abilityScores?.dex || 0) + (abilityBonuses?.dex || 0),
    con: (abilityScores?.con || 0) + (abilityBonuses?.con || 0),
    int: (abilityScores?.int || 0) + (abilityBonuses?.int || 0),
    wis: (abilityScores?.wis || 0) + (abilityBonuses?.wis || 0),
    cha: (abilityScores?.cha || 0) + (abilityBonuses?.cha || 0),
  });

  // ===== 验证并导出 =====
  console.log('\n--- 验证构建 ---');
  
  const validation = builder.validate();
  console.log('验证结果:', validation.valid ? '✓ 通过' : '✗ 失败');
  if (validation.errors) {
    console.log('错误:', validation.errors);
  }

  // 导出角色
  try {
    const character = builder.exportCharacter();
    console.log('\n=== 角色创建成功！ ===');
    console.log('角色名称:', character.name || '未命名');
    console.log('种族:', character.race?.name);
    console.log('职业:', character.classes?.map(c => `${c.name} ${c.level}级`).join(' / '));
    console.log('熟练加值:', character.proficiencyBonus);
    console.log('AC:', character.armorClass);
    console.log('HP:', character.hitPoints?.max);
    console.log('速度:', character.speed);
    console.log('语言:', character.languages?.join(', '));
    console.log('特性:', character.traits?.join(', '));
  } catch (err) {
    console.error('导出失败:', err);
  }

  // 取消订阅
  unsubscribe();

  // 序列化保存
  const serialized = builder.serialize();
  console.log('\n角色数据已序列化，长度:', serialized.length, '字节');

  return builder;
}

// 示例：加载扩展包
async function loadExtensionExample(builder: CharacterBuilder) {
  console.log('\n=== 加载扩展包示例 ===\n');

  // 模拟扩展包数据
  const extensionManifest = {
    id: 'custom-subclass',
    name: '自定义子职业扩展',
    version: '1.0.0',
    dependencies: {
      core: 'srd-2014-zh@>=1.0.0',
    },
  };

  // 添加新的子职业数据
  builder.loadDataSource('custom-subclass', {
    subclasses: [
      {
        index: 'blade-singer',
        class: { index: 'wizard', name: '法师', url: '' },
        name: '剑歌者',
        name_en: 'Blade Singer',
        subclass_flavor: '奥术传承',
        desc: ['剑歌者将武术与奥术魔法结合在一起...'],
        spells: [],
        subclass_levels: '/api/subclasses/blade-singer/levels',
      }
    ]
  });

  console.log('✓ 扩展包加载完成');
  console.log('新增子职业: 剑歌者');
}

// 运行示例
async function main() {
  try {
    const builder = await createElfWizard();
    await loadExtensionExample(builder);
    
    console.log('\n=== 示例完成 ===');
  } catch (err) {
    console.error('运行失败:', err);
  }
}

// 如果在Node环境运行
if (typeof window === 'undefined') {
  main();
}

export { createElfWizard, loadSRDData };
