#!/usr/bin/env python3
"""
翻译 5e-SRD-Features.json 文件
"""

import json
import re
from pathlib import Path

# 职业名称翻译映射
CLASS_NAMES = {
    "Barbarian": "野蛮人",
    "Bard": "吟游诗人",
    "Cleric": "牧师",
    "Druid": "德鲁伊",
    "Fighter": "战士",
    "Monk": "武僧",
    "Paladin": "圣武士",
    "Ranger": "游侠",
    "Rogue": "游荡者",
    "Sorcerer": "术士",
    "Warlock": "邪术师",
    "Wizard": "法师",
}

# 常见子职业名称映射（部分）
SUBCLASS_NAMES = {
    "Berserker": "狂战士",
    "Totem Warrior": "图腾战士",
    "Lore": "知识",
    "Valor": "勇气",
    "Life": "生命",
    "Light": "光明",
    "Nature": "自然",
    "Tempest": "风暴",
    "Trickery": "诡术",
    "War": "战争",
    "Land": "大地",
    "Moon": "月亮",
    "Champion": "勇士",
    "Battle Master": "战斗大师",
    "Eldritch Knight": "奥法骑士",
    "Open Hand": "敞掌",
    "Shadow": "暗影",
    "Four Elements": "四象",
    "Devotion": "奉献",
    "Ancients": "远古",
    "Vengeance": "复仇",
    "Hunter": "猎人",
    "Beast Master": "野兽大师",
    "Thief": "盗贼",
    "Assassin": "刺客",
    "Arcane Trickster": "奥术诡术师",
    "Draconic Bloodline": "龙族血脉",
    "Wild Magic": "狂野魔法",
    "The Fiend": "邪魔",
    "The Great Old One": "旧日支配者",
    "The Archfey": "至高妖精",
    "Abjuration": "防护",
    "Conjuration": "召唤",
    "Divination": "预言",
    "Enchantment": "惑控",
    "Evocation": "塑能",
    "Illusion": "幻术",
    "Necromancy": "死灵",
    "Transmutation": "变化",
    "Death": "死亡",
    "Grave": "坟墓",
    "Knowledge": "知识",
}

# 扩展特性名称映射
FEATURE_NAMES = {
    # 通用
    "Ability Score Improvement": "属性值提升",
    "Extra Attack": "额外攻击",
    "Extra Attack (2)": "额外攻击 (2)",
    "Extra Attack (3)": "额外攻击 (3)",
    "Unarmored Defense": "无甲防御",
    "Fast Movement": "快速移动",
    "Feral Instinct": "野兽本能",
    "Brutal Critical": "凶蛮重击",
    "Brutal Critical (1 die)": "凶蛮重击 (1枚骰)",
    "Brutal Critical (2 dice)": "凶蛮重击 (2枚骰)",
    "Brutal Critical (3 dice)": "凶蛮重击 (3枚骰)",
    "Relentless Rage": " relentless 狂暴",
    "Indomitable Might": "不屈强韧",
    "Primal Champion": "原初冠军",
    "Path feature": "道路特性",
    "Persistent Rage": "持续狂暴",
    "Elusive": "难以捉摸",
    "Stroke of Luck": "幸运一击",
    
    # 狂暴系列
    "Rage": "狂暴",
    "Reckless Attack": "鲁莽攻击",
    "Danger Sense": "危险感知",
    "Primal Path": "原初道路",
    "Frenzy": "狂暴",
    "Mindless Rage": "无心狂暴",
    "Intimidating Presence": "威吓存在",
    "Retaliation": "反击",
    "Spirit Seeker": "灵魂追寻者",
    "Totem Spirit": "图腾灵魂",
    "Aspect of the Beast": "野兽形态",
    "Spirit Walker": "灵魂行者",
    "Totemic Attunement": "图腾调谐",
    
    # 吟游诗人
    "Spellcasting": "施法",
    "Bardic Inspiration": "吟游诗人激励",
    "Bardic Inspiration (d6)": "吟游诗人激励 (d6)",
    "Bardic Inspiration (d8)": "吟游诗人激励 (d8)",
    "Bardic Inspiration (d10)": "吟游诗人激励 (d10)",
    "Bardic Inspiration (d12)": "吟游诗人激励 (d12)",
    "Jack of All Trades": "万事通",
    "Song of Rest": "休憩曲",
    "Song of Rest (d8)": "休憩曲 (d8)",
    "Song of Rest (d10)": "休憩曲 (d10)",
    "Song of Rest (d12)": "休憩曲 (d12)",
    "Bard College": "吟游诗人学院",
    "Bard College feature": "吟游诗人学院特性",
    "Expertise": "专长",
    "Font of Inspiration": "激励之源",
    "Countercharm": "反魅惑",
    "Superior Inspiration": "卓越激励",
    "Cutting Words": "刻薄言语",
    "Additional Magical Secrets": "额外魔法秘密",
    "Peerless Skill": "无双技艺",
    "Combat Inspiration": "战斗激励",
    "College feature": "学院特性",
    
    # 牧师
    "Divine Domain": "神圣领域",
    "Divine Domain feature": "神圣领域特性",
    "Channel Divinity": "引导神力",
    "Channel Divinity (1/rest)": "引导神力 (1/短休)",
    "Channel Divinity (2/rest)": "引导神力 (2/短休)",
    "Channel Divinity (3/rest)": "引导神力 (3/短休)",
    "Channel Divinity: Turn Undead": "引导神力：驱散亡灵",
    "Destroy Undead": "摧毁亡灵",
    "Destroy Undead (CR 1/2 or below)": "摧毁亡灵 (挑战等级1/2或更低)",
    "Destroy Undead (CR 1 or below)": "摧毁亡灵 (挑战等级1或更低)",
    "Destroy Undead (CR 2 or below)": "摧毁亡灵 (挑战等级2或更低)",
    "Destroy Undead (CR 3 or below)": "摧毁亡灵 (挑战等级3或更低)",
    "Destroy Undead (CR 4 or below)": "摧毁亡灵 (挑战等级4或更低)",
    "Divine Intervention": "神圣干预",
    "Divine Intervention Improvement": "神圣干预改进",
    "Domain Spells": "领域法术",
    "Bonus Proficiency": "额外熟练",
    "Disciple of Life": "生命门徒",
    "Channel Divinity: Preserve Life": "引导神力：保存生命",
    "Blessed Healer": "祝福医者",
    "Supreme Healing": "至高治疗",
    "Domain feature": "领域特性",
    "Warding Flare": "防护闪光",
    "Channel Divinity: Radiance of the Dawn": "引导神力：黎明光辉",
    "Improved Flare": "强化闪光",
    "Potent Spellcasting": "强效施法",
    "Corona of Light": "光之冠冕",
    "Acolyte of Nature": "自然侍僧",
    "Channel Divinity: Charm Animals and Plants": "引导神力：魅惑动植物",
    "Dampen Elements": "抑制元素",
    "Divine Strike": "神圣打击",
    "Master of Nature": "自然主宰",
    "Wrath of the Storm": "风暴之怒",
    "Channel Divinity: Destructive Wrath": "引导神力：毁灭之怒",
    "Thunderbolt Strike": "雷霆打击",
    "Stormborn": "风暴之子",
    "Blessing of the Trickster": "诡术祝福",
    "Channel Divinity: Invoke Duplicity": "引导神力：召唤幻象",
    "Channel Divinity: Cloak of Shadows": "引导神力：暗影斗篷",
    "Improved Duplicity": "强化幻象",
    "War Priest": "战争祭司",
    "Channel Divinity: Guided Strike": "引导神力：引导打击",
    "Channel Divinity: War God's Blessing": "引导神力：战神祝福",
    "Avatar of Battle": "战斗化身",
    "Bonus Cantrip": "额外戏法",
    "Bonus Proficiencies": "额外熟练",
    
    # 德鲁伊
    "Druidic": "德鲁伊语",
    "Wild Shape": "荒野形态",
    "Druid Circle": "德鲁伊结社",
    "Druid Circle feature": "德鲁伊结社特性",
    "Timeless Body": "永恒身躯",
    "Beast Spells": "野兽法术",
    "Archdruid": "大德鲁伊",
    "Circle Spells": "结社法术",
    "Land's Stride": "大地行者",
    "Nature's Ward": "自然守护",
    "Nature's Sanctuary": "自然圣所",
    "Combat Wild Shape": "战斗荒野形态",
    "Circle Forms": "结社形态",
    "Primal Strike": "原初打击",
    "Elemental Wild Shape": "元素荒野形态",
    "Thousand Forms": "千形万象",
    "Circle feature": "结社特性",
    "Natural Recovery": "自然恢复",
    "Land Feature": "大地特性",
    "Circle of the Land": "大地结社",
    "Circle of the Land: Arctic": "大地结社：极地",
    "Circle of the Land: Coast": "大地结社：海岸",
    "Circle of the Land: Desert": "大地结社：沙漠",
    "Circle of the Land: Forest": "大地结社：森林",
    "Circle of the Land: Grassland": "大地结社：草原",
    "Circle of the Land: Mountain": "大地结社：山地",
    "Circle of the Land: Swamp": "大地结社：沼泽",
    
    # 战士
    "Second Wind": "回气",
    "Action Surge": "动作如潮",
    "Action Surge (1 use)": "动作如潮 (1次)",
    "Action Surge (2 uses)": "动作如潮 (2次)",
    "Martial Archetype": "武术范型",
    "Improved Critical": "改进重击",
    "Remarkable Athlete": "非凡运动员",
    "Additional Fighting Style": "额外战斗风格",
    "Superior Critical": "卓越重击",
    "Survivor": "生存者",
    "Improved Second Wind": "改进回气",
    "Archetype feature": "范型特性",
    "Combat Superiority": "战斗优势",
    "Student of War": "战争学徒",
    "Know Your Enemy": "知己知彼",
    "Improved Combat Superiority": "改进战斗优势",
    "Relentless": "无情",
    "Weapon Bond": "武器契约",
    "War Magic": "战争魔法",
    "Eldritch Strike": "奥法打击",
    "Arcane Charge": "奥法冲锋",
    "Improved War Magic": "改进战争魔法",
    "Maneuvers": "战技",
    "Maneuver: Disarming Attack": "战技：缴械攻击",
    "Maneuver: Precision Attack": "战技：精准攻击",
    "Maneuver: Trip Attack": "战技：绊摔攻击",
    "Maneuver: Riposte": "战技：反击",
    "Maneuver: Feinting Attack": "战技：佯攻",
    "Maneuver: Menacing Attack": "战技：威吓攻击",
    "Maneuver: Pushing Attack": "战技：推撞攻击",
    "Maneuver: Sweeping Attack": "战技：横扫攻击",
    "Maneuver: Evasive Footwork": "战技：闪避步法",
    "Maneuver: Distracting Strike": "战技：分心打击",
    "Maneuver: Rally": "战技：鼓舞",
    "Maneuver: Goading Attack": "战技：激怒攻击",
    "Maneuver: Lunging Attack": "战技：突刺攻击",
    "Maneuver: Commander's Strike": "战技：指挥官打击",
    "Maneuver: Maneuvering Attack": "战技：机动攻击",
    
    # 武僧
    "Martial Arts": "武术",
    "Ki": "气",
    "Unarmored Movement": "无甲移动",
    "Monastic Tradition": "修道传统",
    "Deflect Missiles": "拨挡飞弹",
    "Slow Fall": "缓降",
    "Stunning Strike": "震惧掌",
    "Ki-Empowered Strikes": "气能打击",
    "Evasion": "闪避",
    "Stillness of Mind": "心灵宁静",
    "Purity of Body": "身净",
    "Tongue of the Sun and Moon": "日月之舌",
    "Diamond Soul": "钻石灵魂",
    "Empty Body": "空身",
    "Perfect Self": "完美自我",
    "Unarmored Movement Improvement": "无甲移动改进",
    "Tradition feature": "传统特性",
    "Flurry of Blows": "疾风连击",
    "Patient Defense": " Patient 防御",
    "Step of the Wind": "疾风步",
    "Open Hand Technique": "敞掌技艺",
    "Wholeness of Body": "身全",
    "Tranquility": " Tranquility ",
    "Quivering Palm": "震颤掌",
    "Shadow Arts": "暗影技艺",
    "Shadow Step": "暗影步",
    "Improved Shadow Step": "改进暗影步",
    "Cloak of Shadows": "暗影斗篷",
    "Elemental Attunement": "元素调谐",
    "Discipline": " discipline ",
    
    # 圣武士
    "Divine Sense": "神圣感知",
    "Lay on Hands": "圣疗",
    "Fighting Style": "战斗风格",
    "Divine Smite": "神圣打击",
    "Divine Health": "神圣健康",
    "Sacred Oath": "神圣誓言",
    "Aura of Protection": "防护光环",
    "Aura of Courage": "勇气光环",
    "Improved Divine Smite": "改进神圣打击",
    "Cleansing Touch": "净化触碰",
    "Aura improvements": "光环改进",
    "Oath Spells": "誓言法术",
    "Channel Divinity: Sacred Weapon": "引导神力：神圣武器",
    "Channel Divinity: Turn the Unholy": "引导神力：驱散邪魔",
    "Aura of Devotion": "奉献光环",
    "Purity of Spirit": "精神纯净",
    "Holy Nimbus": "圣洁光轮",
    "Channel Divinity: Nature's Wrath": "引导神力：自然之怒",
    "Channel Divinity: Turn the Faithless": "引导神力：驱散背信者",
    "Aura of Warding": "守护光环",
    "Undying Sentinel": "不死哨兵",
    "Elder Champion": "远古冠军",
    "Channel Divinity: Abjure Enemy": "引导神力：驱逐敌人",
    "Channel Divinity: Vow of Enmity": "引导神力：仇敌誓言",
    "Relentless Avenger": "无情复仇者",
    "Soul of Vengeance": "复仇之魂",
    "Avenging Angel": "复仇天使",
    "Oath feature": "誓言特性",
    
    # 游侠
    "Favored Enemy": "宿敌",
    "Favored Enemy (1 type)": "宿敌 (1种类型)",
    "Favored Enemy (2 types)": "宿敌 (2种类型)",
    "Favored Enemy (3 enemies)": "宿敌 (3种敌人)",
    "Natural Explorer": "自然探索者",
    "Primeval Awareness": "原初感知",
    "Lands Stride": "大地行者",
    "Hide in Plain Sight": " plain sight 隐藏",
    "Vanish": "消失",
    "Feral Senses": "野兽感官",
    "Foe Slayer": "敌手屠戮者",
    "Ranger Archetype": "游侠范型",
    "Archetype feature": "范型特性",
    "Colossus Slayer": "巨人屠戮者",
    "Giant Killer": "巨人杀手",
    "Horde Breaker": " Horde Breaker ",
    "Defensive Tactics": "防御战术",
    "Defensive Tactics: Escape the Horde": "防御战术： Escape the Horde ",
    "Defensive Tactics: Multiattack Defense": "防御战术： Multiattack Defense ",
    "Defensive Tactics: Steel Will": "防御战术： Steel Will ",
    "Escape the Horde": " Escape the Horde ",
    "Multiattack Defense": " Multiattack Defense ",
    "Steel Will": " Steel Will ",
    "Volley": "齐射",
    "Whirlwind Attack": "旋风攻击",
    "Superior Hunter's Defense": "卓越猎手防御",
    "Stand Against the Tide": " Stand Against the Tide ",
    "Ranger's Companion": "游侠伙伴",
    "Exceptional Training": "卓越训练",
    "Bestial Fury": "野兽狂怒",
    "Share Spells": "法术共享",
    
    # 游荡者
    "Thieves' Cant": "盗贼黑话",
    "Cunning Action": "狡诈行动",
    "Roguish Archetype": "游荡者范型",
    "Uncanny Dodge": "非凡闪避",
    "Reliable Talent": "可靠才能",
    "Blindsense": "盲感",
    "Slippery Mind": "滑溜心智",
    "Fast Hands": "快手",
    "Second-Story Work": " Second-Story Work ",
    "Supreme Sneak": " Supreme Sneak ",
    "Use Magic Device": "使用魔法装置",
    "Thief's Reflexes": "盗贼反射",
    "Assassinate": "暗杀",
    "Infiltration Expertise": "渗透专长",
    "Impostor": " Impostor ",
    "Death Strike": " Death Strike ",
    "Spell Thief": "法术窃贼",
    "Mage Hand Legerdemain": " Mage Hand Legerdemain ",
    "Magical Ambush": " Magical Ambush ",
    "Versatile Trickster": " Versatile Trickster ",
    
    # 术士
    "Sorcerous Origin": "术法起源",
    "Origin feature": "起源特性",
    "Font of Magic": "魔法源泉",
    "Metamagic": "超魔法",
    "Sorcerous Restoration": "术法恢复",
    "Sorcery Points": "术法点",
    "Flexible Casting": "灵活施法",
    "Flexible Casting: Converting Spell Slot": "灵活施法：转换法术位",
    "Flexible Casting: Creating Spell Slots": "灵活施法：创造法术位",
    "Hunter's Prey": "猎手猎物",
    "Hunter's Prey: Colossus Slayer": "猎手猎物：巨人屠戮者",
    "Hunter's Prey: Giant Killer": "猎手猎物：巨人杀手",
    "Hunter's Prey: Horde Breaker": "猎手猎物：Horde Breaker",
    "Indomitable (1 use)": "Indomitable (1次)",
    "Indomitable (2 uses)": "Indomitable (2次)",
    "Indomitable (3 uses)": "Indomitable (3次)",
    "Ki Empowered Strikes": "气能打击",
    "Magical Secrets": "魔法秘密",
    "Martial Archetype feature": "武术范型特性",
    "Monastic Tradition feature": "修道传统特性",
    "Multiattack": "多重攻击",
    "Multiattack: Volley": "多重攻击：齐射",
    "Multiattack: Whirlwind Attack": "多重攻击：旋风攻击",
    "Mystic Arcanum (6th level)": "秘法奥义 (6环)",
    "Mystic Arcanum (7th level)": "秘法奥义 (7环)",
    "Mystic Arcanum (8th level)": "秘法奥义 (8环)",
    "Mystic Arcanum (9th level)": "秘法奥义 (9环)",
    "Natural Explorer (1 terrain type)": "自然探索者 (1种地形)",
    "Natural Explorer (2 terrain types)": "自然探索者 (2种地形)",
    "Natural Explorer (3 terrain types)": "自然探索者 (3种地形)",
    "Otherworldly Patron feature": "异界宗主特性",
    "Ranger Archetype feature": "游侠范型特性",
    "Roguish Archetype feature": "游荡者范型特性",
    "Sacred Oath feature": "神圣誓言特性",
    "Signature Spell": " signature 法术",
    "Sneak Attack": "偷袭",
    "Song of Rest (d6)": "休憩曲 (d6)",
    "Sorcerous Origin feature": "术法起源特性",
    "Spellcasting: Bard": "施法：吟游诗人",
    "Spellcasting: Cleric": "施法：牧师",
    "Spellcasting: Druid": "施法：德鲁伊",
    "Spellcasting: Paladin": "施法：圣武士",
    "Spellcasting: Ranger": "施法：游侠",
    "Spellcasting: Sorcerer": "施法：术士",
    "Spellcasting: Wizard": "施法：法师",
    "Superior Hunter's Defense: Evasion": "卓越猎手防御：闪避",
    "Superior Hunter's Defense: Stand Against the Tide": "卓越猎手防御：Stand Against the Tide",
    "Superior Hunter's Defense: Uncanny Dodge": "卓越猎手防御：非凡闪避",
    "Wild Shape (CR 1 or below)": "荒野形态 (挑战等级1或更低)",
    "Wild Shape (CR 1/2 or below, no flying speed)": "荒野形态 (挑战等级1/2或更低，无飞行速度)",
    "Wild Shape (CR 1/4 or below, no flying or swim speed)": "荒野形态 (挑战等级1/4或更低，无飞行或游泳速度)",
    
    # 武僧四象法术
    "Breath of Winter": " Breath of Winter ",
    "Clench of the North Wind": " Clench of the North Wind ",
    "Eternal Mountain Defense": " Eternal Mountain Defense ",
    "Fangs of the Fire Snake": " Fangs of the Fire Snake ",
    "Fist of Four Thunders": " Fist of Four Thunders ",
    "Fist of Unbroken Air": " Fist of Unbroken Air ",
    "Flames of the Phoenix": " Flames of the Phoenix ",
    "Gong of the Summit": " Gong of the Summit ",
    "Mist Stance": " Mist Stance ",
    "Ride the Wind": " Ride the Wind ",
    "River of Hungry Flame": " River of Hungry Flame ",
    "Rush of the Gale Spirits": " Rush of the Gale Spirits ",
    "Shape the Flowing River": " Shape the Flowing River ",
    "Sweeping Cinder Strike": " Sweeping Cinder Strike ",
    "Water Whip": " Water Whip ",
    "Wave of Rolling Earth": " Wave of Rolling Earth ",
    "Creating Spell Slots": "创造法术位",
    "Converting a Spell Slot to Sorcery Points": "法术位转换为术法点",
    "Draconic Ancestry": "龙族血统",
    "Dragon Ancestor": "龙族先祖",
    "Dragon Ancestor: Black - Acid Damage": "龙族先祖：黑龙 - 酸蚀伤害",
    "Dragon Ancestor: Blue - Lightning Damage": "龙族先祖：蓝龙 - 闪电伤害",
    "Dragon Ancestor: Brass - Fire Damage": "龙族先祖：黄铜龙 - 火焰伤害",
    "Dragon Ancestor: Bronze - Lightning Damage": "龙族先祖：青铜龙 - 闪电伤害",
    "Dragon Ancestor: Copper - Acid Damage": "龙族先祖：赤铜龙 - 酸蚀伤害",
    "Dragon Ancestor: Gold - Fire Damage": "龙族先祖：金龙 - 火焰伤害",
    "Dragon Ancestor: Green - Poison Damage": "龙族先祖：绿龙 - 毒素伤害",
    "Dragon Ancestor: Red - Fire Damage": "龙族先祖：红龙 - 火焰伤害",
    "Dragon Ancestor: Silver - Cold Damage": "龙族先祖：银龙 - 寒冷伤害",
    "Dragon Ancestor: White - Cold Damage": "龙族先祖：白龙 - 寒冷伤害",
    "Draconic Resilience": "龙族韧性",
    "Elemental Affinity": "元素亲和",
    "Dragon Wings": "龙翼",
    "Draconic Presence": "龙族威势",
    "Wild Magic Surge": "狂野魔法浪涌",
    "Tides of Chaos": "混沌潮汐",
    "Bend Luck": "扭转命运",
    "Controlled Chaos": "可控混沌",
    "Spell Bombardment": "法术轰击",
    
    # 邪术师
    "Otherworldly Patron": "异界宗主",
    "Patron feature": "宗主特性",
    "Pact Magic": "契约魔法",
    "Eldritch Invocations": "魔能祈唤",
    "Pact Boon": "契约恩惠",
    "Mystic Arcanum": "秘法奥义",
    "Eldritch Master": "魔能大师",
    "Dark One's Blessing": " Dark One's Blessing ",
    "Dark One's Own Luck": " Dark One's Own Luck ",
    "Fiendish Resilience": "邪魔韧性",
    "Hurl Through Hell": " Hurl Through Hell ",
    "Awakened Mind": " Awakened Mind ",
    "Entropic Ward": " Entropic Ward ",
    "Thought Shield": " Thought Shield ",
    "Create Thrall": " Create Thrall ",
    "Fey Presence": " Fey Presence ",
    "Misty Escape": " Misty Escape ",
    "Beguiling Defenses": " Beguiling Defenses ",
    "Dark Delirium": " Dark Delirium ",
    "Pact of the Chain": "锁链契约",
    "Pact of the Blade": "刃之契约",
    "Pact of the Tome": "书卷契约",
    
    # 法师
    "Arcane Recovery": "奥术恢复",
    "Arcane Tradition": "奥术传承",
    "Arcane Tradition feature": "奥术传承特性",
    "Spell Mastery": "法术精通",
    "Signature Spells": " signature 法术",
    "Abjuration Savant": "防护学者",
    "Arcane Ward": "奥术结界",
    "Projected Ward": " Projected Ward ",
    "Improved Abjuration": "改进防护",
    "Spell Resistance": "法术抗性",
    "Conjuration Savant": "召唤学者",
    "Minor Conjuration": " Minor Conjuration ",
    "Benign Transposition": " Benign Transposition ",
    "Focused Conjuration": " Focused Conjuration ",
    "Durable Summons": " Durable Summons ",
    "Divination Savant": "预言学者",
    "Portent": " Portent ",
    "Expert Divination": " Expert Divination ",
    "Third Eye": " Third Eye ",
    "Superior Portent": " Superior Portent ",
    "Enchantment Savant": "惑控学者",
    "Hypnotic Gaze": " Hypnotic Gaze ",
    "Instinctive Charm": " Instinctive Charm ",
    "Split Enchantment": " Split Enchantment ",
    "Alter Memories": " Alter Memories ",
    "Evocation Savant": "塑能学者",
    "Sculpt Spells": " Sculpt Spells ",
    "Potent Cantrip": " Potent Cantrip ",
    "Empowered Evocation": " Empowered Evocation ",
    "Overchannel": " Overchannel ",
    "Illusion Savant": "幻术学者",
    "Improved Minor Illusion": "改进次级幻影",
    "Malleable Illusions": " Malleable Illusions ",
    "Illusory Self": " Illusory Self ",
    "Illusory Reality": " Illusory Reality ",
    "Necromancy Savant": "死灵学者",
    "Grim Harvest": " Grim Harvest ",
    "Undead Thralls": " Undead Thralls ",
    "Inured to Undeath": " Inured to Undeath ",
    "Command Undead": " Command Undead ",
    "Transmutation Savant": "变化学者",
    "Transmuter's Stone": " Transmuter's Stone ",
    "Shapechanger": "变形者",
    "Transmutation Master": "变化大师",
    
    # 战斗风格
    "Fighting Style: Archery": "战斗风格：箭术",
    "Fighting Style: Defense": "战斗风格：防御",
    "Fighting Style: Dueling": "战斗风格：对决",
    "Fighting Style: Great Weapon Fighting": "战斗风格：巨武器战斗",
    "Fighting Style: Protection": "战斗风格：守护",
    "Fighting Style: Two-Weapon Fighting": "战斗风格：双武器战斗",
    
    # 魔能祈唤
    "Eldritch Invocation: Agonizing Blast": "魔能祈唤：苦痛爆燃",
    "Eldritch Invocation: Armor of Shadows": "魔能祈唤：影之铠甲",
    "Eldritch Invocation: Ascendant Step": "魔能祈唤：超凡步法",
    "Eldritch Invocation: Beast Speech": "魔能祈唤：野兽之语",
    "Eldritch Invocation: Beguiling Influence": "魔能祈唤：魅惑影响",
    "Eldritch Invocation: Bewitching Whispers": "魔能祈唤：魅惑耳语",
    "Eldritch Invocation: Book of Ancient Secrets": "魔能祈唤：远古秘密之书",
    "Eldritch Invocation: Chains of Carceri": "魔能祈唤：卡瑟利之链",
    "Eldritch Invocation: Devil's Sight": "魔能祈唤：魔鬼视界",
    "Eldritch Invocation: Dreadful Word": "魔能祈唤：恐怖之言",
    "Eldritch Invocation: Eldritch Sight": "魔能祈唤：魔能视界",
    "Eldritch Invocation: Eldritch Spear": "魔能祈唤：魔能长枪",
    "Eldritch Invocation: Eyes of the Rune Keeper": "魔能祈唤：符文守护者之眼",
    "Eldritch Invocation: Fiendish Vigor": "魔能祈唤：邪魔活力",
    "Eldritch Invocation: Gaze of Two Minds": "魔能祈唤：双心凝视",
    "Eldritch Invocation: Lifedrinker": "魔能祈唤：饮命者",
    "Eldritch Invocation: Mask of Many Faces": "魔能祈唤：千面之假",
    "Eldritch Invocation: Master of Myriad Forms": "魔能祈唤：万象之主",
    "Eldritch Invocation: Minions of Chaos": "魔能祈唤：混沌仆从",
    "Eldritch Invocation: Mire the Mind": "魔能祈唤：心智泥沼",
    "Eldritch Invocation: Misty Visions": "魔能祈唤：迷雾幻视",
    "Eldritch Invocation: One with Shadows": "魔能祈唤：影遁",
    "Eldritch Invocation: Otherworldly Leap": "魔能祈唤：异界之跃",
    "Eldritch Invocation: Repelling Blast": "魔能祈唤：斥力爆",
    "Eldritch Invocation: Sculptor of Flesh": "魔能祈唤：血肉雕刻者",
    "Eldritch Invocation: Sign of Ill Omen": "魔能祈唤：凶兆之印",
    "Eldritch Invocation: Thief of Five Fates": "魔能祈唤：五命之盗",
    "Eldritch Invocation: Thirsting Blade": "魔能祈唤：饥渴之刃",
    "Eldritch Invocation: Visions of Distant Realms": "魔能祈唤：远域幻视",
    "Eldritch Invocation: Voice of the Chain Master": "魔能祈唤：锁链主宰之声",
    "Eldritch Invocation: Whispers of the Grave": "魔能祈唤：坟墓低语",
    "Eldritch Invocation: Witch Sight": "魔能祈唤：女巫视界",
    
    # 超魔法
    "Metamagic: Careful Spell": "超魔法：谨慎法术",
    "Metamagic: Distant Spell": "超魔法：远距法术",
    "Metamagic: Empowered Spell": "超魔法：强效法术",
    "Metamagic: Extended Spell": "超魔法：延时法术",
    "Metamagic: Heightened Spell": "超魔法：升阶法术",
    "Metamagic: Quickened Spell": "超魔法：迅捷法术",
    "Metamagic: Subtle Spell": "超魔法：精妙法术",
    "Metamagic: Twinned Spell": "超魔法：双生法术",
}

def translate_text(text, is_name=False):
    """翻译文本"""
    if not text or not isinstance(text, str):
        return text
    
    # 如果是名称，先查找映射
    if is_name:
        # 直接匹配
        if text in FEATURE_NAMES:
            return FEATURE_NAMES[text]
        if text in CLASS_NAMES:
            return CLASS_NAMES[text]
        if text in SUBCLASS_NAMES:
            return SUBCLASS_NAMES[text]
    
    return text

def translate_feature(feature):
    """翻译单个特性"""
    # 翻译 name
    if "name" in feature:
        original_name = feature["name"]
        translated_name = translate_text(original_name, is_name=True)
        if translated_name != original_name:
            feature["name"] = translated_name
            feature["name_en"] = original_name
        else:
            # 如果没有找到映射，保留原名（后续可能需要手动处理）
            pass
    
    # 翻译 class.name
    if "class" in feature and "name" in feature["class"]:
        class_name = feature["class"]["name"]
        if class_name in CLASS_NAMES:
            feature["class"]["name"] = CLASS_NAMES[class_name]
            feature["class"]["name_en"] = class_name
    
    # 翻译 subclass.name
    if "subclass" in feature and "name" in feature["subclass"]:
        subclass_name = feature["subclass"]["name"]
        translated = translate_text(subclass_name, is_name=True)
        if translated != subclass_name:
            feature["subclass"]["name"] = translated
            feature["subclass"]["name_en"] = subclass_name
        elif subclass_name in SUBCLASS_NAMES:
            feature["subclass"]["name"] = SUBCLASS_NAMES[subclass_name]
            feature["subclass"]["name_en"] = subclass_name
    
    return feature

def main():
    # 读取源文件
    src_path = Path("/Users/chezi/code/java/5e-database/src/2014/5e-SRD-Features.json")
    dst_path = Path("/Users/chezi/code/java/5e-database/src/2014-zh/5e-SRD-Features.json")
    
    with open(src_path, 'r', encoding='utf-8') as f:
        features = json.load(f)
    
    print(f"Total features: {len(features)}")
    
    # 统计职业分布
    class_count = {}
    for feature in features:
        class_name = feature.get("class", {}).get("name", "Unknown")
        class_count[class_name] = class_count.get(class_name, 0) + 1
    
    print("\nClass distribution:")
    for cls, count in sorted(class_count.items()):
        print(f"  {cls}: {count}")
    
    # 翻译所有特性
    translated_features = []
    for feature in features:
        translated = translate_feature(feature)
        translated_features.append(translated)
    
    # 保存结果
    dst_path.parent.mkdir(parents=True, exist_ok=True)
    with open(dst_path, 'w', encoding='utf-8') as f:
        json.dump(translated_features, f, ensure_ascii=False, indent=2)
    
    print(f"\nTranslation saved to: {dst_path}")
    
    # 统计未翻译的名称（用于后续处理）
    untranslated_names = set()
    for feature in translated_features:
        if "name_en" not in feature and "name" in feature:
            name = feature["name"]
            if name and isinstance(name, str) and not name.startswith("Maneuver:") and "Savant" not in name:
                untranslated_names.add(name)
    
    if untranslated_names:
        print(f"\nUntranslated names ({len(untranslated_names)}):")
        for name in sorted(untranslated_names)[:50]:
            print(f"  - {name}")

if __name__ == "__main__":
    main()
