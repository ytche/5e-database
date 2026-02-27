#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
翻译 5e-SRD-Classes.json 文件
"""

import json
import re

# 职业名称翻译映射
CLASS_NAMES = {
    "Barbarian": "野蛮人",
    "Bard": "吟游诗人",
    "Cleric": "牧师",
    "Druid": "德鲁伊",
    "Fighter": "斗士",
    "Monk": "武僧",
    "Paladin": "圣武士",
    "Ranger": "游侠",
    "Rogue": "游荡者",
    "Sorcerer": "术士",
    "Warlock": "邪术师",
    "Wizard": "法师",
}

# 子职业名称翻译映射
SUBCLASS_NAMES = {
    "Berserker": "狂战士",
    "Lore": "知识",
    "Life": "生命",
    "Land": "大地",
    "Champion": "勇士",
    "Open Hand": "开掌",
    "Devotion": "奉献",
    "Hunter": "猎手",
    "Thief": "盗贼",
    "Draconic": "龙族",
    "Fiend": "邪魔",
    "Evocation": "塑能",
}

# 技能名称翻译映射
SKILL_NAMES = {
    "Acrobatics": "杂技",
    "Animal Handling": "驯兽",
    "Arcana": "奥秘",
    "Athletics": "运动",
    "Deception": "欺瞒",
    "History": "历史",
    "Insight": "洞察",
    "Intimidation": "威吓",
    "Investigation": "调查",
    "Medicine": "医药",
    "Nature": "自然",
    "Perception": "察觉",
    "Performance": "表演",
    "Persuasion": "说服",
    "Religion": "宗教",
    "Sleight of Hand": "巧手",
    "Stealth": "隐匿",
    "Survival": "生存",
}

# 装备/熟练项名称翻译映射
EQUIPMENT_NAMES = {
    # 护甲
    "Light Armor": "轻甲",
    "Medium Armor": "中甲",
    "Heavy Armor": "重甲",
    "All armor": "所有护甲",
    "Shields": "盾牌",
    "Shield": "盾牌",
    # 武器类别
    "Simple Weapons": "简易武器",
    "Martial Weapons": "军用武器",
    "Martial Melee Weapons": "军用近战武器",
    "Simple Melee Weapons": "简易近战武器",
    "Crossbows, light": "轻弩",
    "Hand crossbows": "手弩",
    # 具体武器
    "Daggers": "匕首",
    "Dagger": "匕首",
    "Darts": "飞镖",
    "Dart": "飞镖",
    "Slings": "投石索",
    "Quarterstaffs": "长棍",
    "Quarterstaff": "长棍",
    "Crossbows, light": "轻弩",
    "Clubs": "棍棒",
    "Javelins": "标枪",
    "Javelin": "标枪",
    "Maces": "硬头锤",
    "Mace": "硬头锤",
    "Spears": "矛",
    "Spear": "矛",
    "Sickles": "镰刀",
    "Scimitars": "弯刀",
    "Scimitar": "弯刀",
    "Longswords": "长剑",
    "Longsword": "长剑",
    "Rapiers": "刺剑",
    "Rapier": "刺剑",
    "Shortswords": "短剑",
    "Shortsword": "短剑",
    "Shortbow": "短弓",
    "Longbow": "长弓",
    "Greataxe": "巨斧",
    "Handaxe": "手斧",
    "Warhammer": "战锤",
    "Warhammers": "战锤",
    "Crossbow, light": "轻弩",
    "Lute": "鲁特琴",
    "Leather Armor": "皮甲",
    "Scale Mail": "鳞甲",
    "Chain Mail": "锁子甲",
    "Explorer's Pack": "探险家套组",
    "Dungeoneer's Pack": "地下城套组",
    "Priest's Pack": "牧师套组",
    "Scholar's Pack": "学者套组",
    "Burglar's Pack": "窃贼套组",
    "Diplomat's Pack": "外交官套组",
    "Entertainer's Pack": "艺人套组",
    "Component pouch": "材料包",
    "Spellbook": "法术书",
    "Arrow": "箭",
    "Crossbow bolt": "弩矢",
    "Thieves' Tools": "盗贼工具",
    "Herbalism Kit": "草药工具包",
    # 豁免
    "Saving Throw: STR": "豁免：力量",
    "Saving Throw: DEX": "豁免：敏捷",
    "Saving Throw: CON": "豁免：体质",
    "Saving Throw: INT": "豁免：智力",
    "Saving Throw: WIS": "豁免：感知",
    "Saving Throw: CHA": "豁免：魅力",
    "Saving Throw": "豁免",
    # 属性
    "STR": "力量",
    "DEX": "敏捷",
    "CON": "体质",
    "INT": "智力",
    "WIS": "感知",
    "CHA": "魅力",
    # 装备类别
    "Holy Symbols": "圣徽",
    "Arcane Foci": "奥术法器",
    "Druidic Foci": "德鲁伊法器",
    "Musical Instruments": "乐器",
    # 乐器
    "Bagpipes": "风笛",
    "Drum": "鼓",
    "Dulcimer": "洋琴",
    "Flute": "长笛",
    "Lyre": "里拉琴",
    "Horn": "号角",
    "Pan flute": "排箫",
    "Shawm": "双簧管",
    "Viol": "维奥尔琴",
    # 工匠工具
    "Alchemist's Supplies": "炼金术士工具",
    "Brewer's Supplies": "酿酒师工具",
    "Calligrapher's Supplies": "书法家工具",
    "Carpenter's Tools": "木匠工具",
    "Cartographer's Tools": "制图师工具",
    "Cobbler's Tools": "鞋匠工具",
    "Cook's utensils": "厨师工具",
    "Glassblower's Tools": "玻璃匠工具",
    "Jeweler's Tools": "珠宝匠工具",
    "Leatherworker's Tools": "皮匠工具",
    "Mason's Tools": "石匠工具",
    "Painter's Supplies": "画家工具",
    "Potter's Tools": "陶匠工具",
    "Smith's Tools": "铁匠工具",
    "Tinker's Tools": "修补匠工具",
    "Weaver's Tools": "织匠工具",
    "Woodcarver's Tools": "木雕匠工具",
    "Disguise Kit": "易容工具",
    "Forgery Kit": "伪造工具",
}

# 法术施法信息中的名称翻译
SPELLCASTING_NAMES = {
    "Cantrips": "戏法",
    "Spell Slots": "法术位",
    "Spells Known of 1st Level and Higher": "已知1级及以上法术",
    "Preparing and Casting Spells": "准备和施放法术",
    "Spellcasting Ability": "施法能力",
    "Ritual Casting": "仪式施法",
    "Spellcasting Focus": "施法焦点",
    "Spellbook": "法术书",
}

# desc 内容翻译函数
def translate_desc(desc):
    """翻译描述文本"""
    if not desc:
        return desc
    
    # 如果desc是列表，翻译每个元素
    if isinstance(desc, list):
        return [translate_desc(d) for d in desc]
    
    if not isinstance(desc, str):
        return desc
    
    desc_en = desc
    
    # 技能选择描述翻译映射
    desc_mapping = {
        # 技能选择
        "Choose two from": "从以下技能中选择两项：",
        "Choose three from": "从以下技能中选择三项：",
        "Choose four from": "从以下技能中选择四项：",
        "Choose any three": "任选三项",
        "Choose two skills from": "从以下技能中选择两项：",
        
        # 完整技能列表
        "Acrobatics, Animal Handling, Athletics, History, Insight, Intimidation, Perception, and Survival":
            "杂技、驯兽、运动、历史、洞察、威吓、察觉和生存",
        "Acrobatics, Athletics, Deception, Insight, Intimidation, Investigation, Perception, Performance, Persuasion, Sleight of Hand, and Stealth":
            "杂技、运动、欺瞒、洞察、威吓、调查、察觉、表演、说服、巧手和隐匿",
        "Acrobatics, Athletics, History, Insight, Religion, and Stealth":
            "杂技、运动、历史、洞察、宗教和隐匿",
        "Animal Handling, Athletics, Insight, Investigation, Nature, Perception, Stealth, and Survival":
            "驯兽、运动、洞察、调查、自然、察觉、隐匿和生存",
        "Animal Handling, Athletics, Intimidation, Nature, Perception, and Survival":
            "驯兽、运动、威吓、自然、察觉和生存",
        "Arcana, Animal Handling, Insight, Medicine, Nature, Perception, Religion, and Survival":
            "奥秘、驯兽、洞察、医药、自然、察觉、宗教和生存",
        "Arcana, Deception, History, Intimidation, Investigation, Nature, and Religion":
            "奥秘、欺瞒、历史、威吓、调查、自然和宗教",
        "Arcana, Deception, Insight, Intimidation, Persuasion, and Religion":
            "奥秘、欺瞒、洞察、威吓、说服和宗教",
        "Arcana, History, Insight, Investigation, Medicine, and Religion":
            "奥秘、历史、洞察、调查、医药和宗教",
        "Athletics, Insight, Intimidation, Medicine, Persuasion, and Religion":
            "运动、洞察、威吓、医药、说服和宗教",
        "History, Insight, Medicine, Persuasion, and Religion":
            "历史、洞察、医药、说服和宗教",
        
        # 装备选择
        "Three musical instruments of your choice": "任选三种乐器",
        "any martial melee weapon": "任意军用近战武器",
        "any simple weapon": "任意简易武器",
        "any martial weapon": "任意军用武器",
        "any simple melee weapon": "任意简易近战武器",
        "two martial weapons": "两把军用武器",
        "two simple melee weapons": "两把简易近战武器",
        "a martial weapon": "一把军用武器",
        "artisan's tools": "工匠工具",
        "musical instrument": "乐器",
        "any other musical instrument": "任意其他乐器",
        "arcane focus": "奥术法器",
        "holy symbol": "圣徽",
        "druidic focus": "德鲁伊法器",
        "if proficient": "若熟练",
        "skill": "技能",
        # 装备选项前缀
        "(a) a greataxe or (b)": "(a) 巨斧或 (b)",
        "(a) two handaxes or (b)": "(a) 两把手斧或 (b)",
        "(a) a wooden shield or (b)": "(a) 木盾或 (b)",
        "(a) a scimitar or (b)": "(a) 弯刀或 (b)",
        "(a) chain mail or (b) leather armor, longbow, and 20 arrows": "(a) 锁子甲或 (b) 皮甲、长弓和20支箭",
        "(a) a martial weapon and a shield or (b)": "(a) 一把军用武器和盾牌或 (b)",
        "(a) a light crossbow and 20 bolts or (b)": "(a) 轻弩和20支弩矢或 (b)",
        "(a) a dungeoneer's pack or (b)": "(a) 地下城套组或 (b)",
        "(a) a rapier, (b) a longsword, or (c)": "(a) 刺剑、(b) 长剑或 (c)",
        "(a) a diplomat's pack or (b)": "(a) 外交官套组或 (b)",
        "(a) a lute or (b)": "(a) 鲁特琴或 (b)",
        "(a) a mace or (b) a warhammer": "(a) 硬头锤或 (b) 战锤",
        "(a) scale mail, (b) leather armor, or (c) chain mail": "(a) 鳞甲、(b) 皮甲或 (c) 锁子甲",
        "(a) a light crossbow and 20 bolts or (b)": "(a) 轻弩和20支弩矢或 (b)",
        "(a) a priest's pack or (b)": "(a) 牧师套组或 (b)",
        "(a) scale mail or (b)": "(a) 鳞甲或 (b)",
        "(a) two shortswords or (b)": "(a) 两把短剑或 (b)",
        "(a) a rapier or (b)": "(a) 刺剑或 (b)",
        "(a) a shortbow and quiver of 20 arrows or (b)": "(a) 短弓和20支箭的箭袋或 (b)",
        "(a) a burglar's pack, (b) a dungeoneer's pack, or (c)": "(a) 窃贼套组、(b) 地下城套组或 (c)",
        "(a) a quarterstaff or (b)": "(a) 长棍或 (b)",
        "(a) a component pouch or (b)": "(a) 材料包或 (b)",
        "(a) a scholar's pack or (b)": "(a) 学者套组或 (b)",
        "(a) five javelins or (b)": "(a) 五支标枪或 (b)",
    }
    
    # 应用描述映射
    for en, cn in desc_mapping.items():
        desc = desc.replace(en, cn)
    
    # 职业名称在描述中
    for en, cn in CLASS_NAMES.items():
        desc = desc.replace(en, cn)
    
    # 单独替换技能名称（用于未在完整列表中匹配的情况）
    skill_replacements = {
        "Acrobatics": "杂技",
        "Animal Handling": "驯兽",
        "Arcana": "奥秘",
        "Athletics": "运动",
        "Deception": "欺瞒",
        "History": "历史",
        "Insight": "洞察",
        "Intimidation": "威吓",
        "Investigation": "调查",
        "Medicine": "医药",
        "Nature": "自然",
        "Perception": "察觉",
        "Performance": "表演",
        "Persuasion": "说服",
        "Religion": "宗教",
        "Sleight of Hand": "巧手",
        "Stealth": "隐匿",
        "Survival": "生存",
    }
    
    for en, cn in skill_replacements.items():
        desc = desc.replace(en, cn)
    
    return desc

# 处理name字段的翻译
def translate_name(name):
    """翻译名称字段"""
    if not name:
        return name, None
    
    # 首先检查是否是技能名称
    if name.startswith("Skill: "):
        skill_name = name.replace("Skill: ", "")
        if skill_name in SKILL_NAMES:
            return f"技能：{SKILL_NAMES[skill_name]}", name
    
    # 检查是否在直接映射中
    if name in CLASS_NAMES:
        return CLASS_NAMES[name], name
    
    if name in SUBCLASS_NAMES:
        return SUBCLASS_NAMES[name], name
    
    if name in EQUIPMENT_NAMES:
        return EQUIPMENT_NAMES[name], name
    
    if name in SPELLCASTING_NAMES:
        return SPELLCASTING_NAMES[name], name
    
    # 检查是否是复数形式
    if name.endswith("s") and name[:-1] in EQUIPMENT_NAMES:
        base_name = name[:-1]
        if base_name in EQUIPMENT_NAMES:
            return EQUIPMENT_NAMES[base_name] + "（复数）", name
    
    # 如果没有匹配，返回原值
    return name, None

def process_object(obj):
    """递归处理JSON对象，翻译name和desc字段"""
    if isinstance(obj, dict):
        result = {}
        
        # 先处理name字段
        if "name" in obj:
            original_name = obj["name"]
            translated_name, name_en = translate_name(original_name)
            result["name"] = translated_name
            if name_en:
                result["name_en"] = name_en
        
        # 处理desc字段
        if "desc" in obj:
            original_desc = obj["desc"]
            if isinstance(original_desc, str):
                translated_desc = translate_desc(original_desc)
                if translated_desc != original_desc:
                    result["desc"] = translated_desc
                    result["desc_en"] = original_desc
                else:
                    result["desc"] = original_desc
            elif isinstance(original_desc, list):
                translated_list = []
                has_translation = False
                for item in original_desc:
                    translated_item = translate_desc(item)
                    if translated_item != item:
                        has_translation = True
                    translated_list.append(translated_item)
                result["desc"] = translated_list
                if has_translation:
                    result["desc_en"] = original_desc
            else:
                result["desc"] = original_desc
        
        # 处理其他字段
        for key, value in obj.items():
            if key not in ["name", "desc"]:
                if key in ["index", "url"]:
                    # 永不翻译
                    result[key] = value
                else:
                    result[key] = process_object(value)
        
        return result
    
    elif isinstance(obj, list):
        return [process_object(item) for item in obj]
    
    else:
        return obj

def main():
    # 读取源文件
    with open("/Users/chezi/code/java/5e-database/src/2014/5e-SRD-Classes.json", "r", encoding="utf-8") as f:
        data = json.load(f)
    
    # 处理翻译
    translated_data = process_object(data)
    
    # 保存输出文件
    with open("/Users/chezi/code/java/5e-database/src/2014-zh/5e-SRD-Classes.json", "w", encoding="utf-8") as f:
        json.dump(translated_data, f, ensure_ascii=False, indent=2)
    
    # 输出统计信息
    class_count = len(data)
    print(f"翻译完成！")
    print(f"- 职业数量: {class_count}")
    print(f"- 输出文件: /Users/chezi/code/java/5e-database/src/2014-zh/5e-SRD-Classes.json")

if __name__ == "__main__":
    main()
