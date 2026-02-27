#!/usr/bin/env python3
"""
翻译所有 Features 描述文本
"""

import json
from pathlib import Path

# 翻译目录
trans_dir = Path("/Users/chezi/code/java/5e-database/translations/features")
src_path = Path("/Users/chezi/code/java/5e-database/src/2014/5e-SRD-Features.json")
dst_path = Path("/Users/chezi/code/java/5e-database/src/2014-zh/5e-SRD-Features.json")

# 术语映射表 - 用于保持翻译一致性
TERM_MAPPING = {
    # 动作相关
    "action": "动作",
    "bonus action": "附赠动作",
    "reaction": "反应",
    "free action": "自由动作",
    "movement": "移动",
    "speed": "速度",
    "feet": "尺",
    "range": "射程",
    "reach": "触及",
    
    # 检定和豁免
    "ability check": "属性检定",
    "saving throw": "豁免检定",
    "attack roll": "攻击检定",
    "damage roll": "伤害检定",
    "advantage": "优势",
    "disadvantage": "劣势",
    
    # 属性
    "Strength": "力量",
    "Dexterity": "敏捷",
    "Constitution": "体质",
    "Intelligence": "智力",
    "Wisdom": "感知",
    "Charisma": "魅力",
    "ability score": "属性值",
    "ability modifier": "属性调整值",
    "proficiency bonus": "熟练加值",
    
    # 生命和伤害
    "hit point": "生命值",
    "hit dice": "生命骰",
    "hit die": "生命骰",
    "temporary hit point": "临时生命值",
    "damage": "伤害",
    "resistance": "抗性",
    "immunity": "免疫",
    "vulnerability": "易伤",
    
    # 法术相关
    "spell": "法术",
    "spell slot": "法术位",
    "spell level": "法术等级",
    "cantrip": "戏法",
    "spellcasting": "施法",
    "spell save DC": "法术豁免DC",
    "spell attack": "法术攻击",
    "concentration": "专注",
    "ritual": "仪式",
    "component": "成分",
    "verbal": "言语",
    "somatic": "姿势",
    "material": "材料",
    
    # 状态
    "condition": "状态",
    "blinded": "目盲",
    "charmed": "魅惑",
    "deafened": "耳聋",
    "frightened": "恐惧",
    "grappled": "擒抱",
    "incapacitated": "失能",
    "invisible": "隐形",
    "paralyzed": "麻痹",
    "petrified": "石化",
    "poisoned": "中毒",
    "prone": "倒地",
    "restrained": "束缚",
    "stunned": "震慑",
    "unconscious": "昏迷",
    "exhaustion": "力竭",
    
    # 感官
    "darkvision": "黑暗视觉",
    "truesight": "真实视觉",
    "blindsight": "盲视",
    "tremorsense": "颤动感知",
    
    # 其他
    "long rest": "长休",
    "short rest": "短休",
    "proficiency": "熟练",
    "language": "语言",
    "tool": "工具",
    "weapon": "武器",
    "armor": "护甲",
    "shield": "盾牌",
    "gold piece": "金币",
    "silver piece": "银币",
    "copper piece": "铜币",
    "level": "等级",
    "experience point": "经验值",
    "challenge rating": "挑战等级",
    "alignment": "阵营",
    "size": "体型",
    
    # 特殊
    "turn undead": "驱散亡灵",
    "divine intervention": "神圣干预",
    "wild shape": "荒野形态",
    "rage": "狂暴",
    "sneak attack": "偷袭",
    "bardic inspiration": "吟游诗人激励",
    "ki": "气",
    "sorcery point": "术法点",
    "eldritch invocation": "魔能祈唤",
    "pact magic": "契约魔法",
    "metamagic": "超魔法",
    "fighting style": "战斗风格",
    "second wind": "回气",
    "action surge": "动作如潮",
    "lay on hands": "圣疗",
    "divine smite": "神圣打击",
    "channel divinity": "引导神力",
    "wild magic surge": "狂野魔法浪涌",
    
    # 伤害类型
    "acid": "酸蚀",
    "bludgeoning": "钝击",
    "cold": "寒冷",
    "fire": "火焰",
    "force": "力场",
    "lightning": "闪电",
    "necrotic": "死灵",
    "piercing": "穿刺",
    "poison": "毒素",
    "psychic": "心灵",
    "radiant": "光耀",
    "slashing": "挥砍",
    "thunder": "雷鸣",
}

def translate_text(text):
    """
    翻译单段文本
    这是一个占位符函数，实际翻译将由AI完成
    """
    return text

def process_class_file(class_name):
    """处理单个职业的翻译文件"""
    input_file = trans_dir / f"{class_name.lower()}_to_translate.json"
    output_file = trans_dir / f"{class_name.lower()}_translated.json"
    
    if not input_file.exists():
        print(f"File not found: {input_file}")
        return None
    
    with open(input_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # 计算字符数
    total_chars = sum(sum(len(d) for d in item["desc"] if d) for item in data)
    
    return {
        "class": class_name,
        "file": input_file,
        "output": output_file,
        "count": len(data),
        "chars": total_chars,
        "data": data
    }

def main():
    # 列出所有职业
    classes = ["barbarian", "bard", "cleric", "druid", "fighter", 
               "monk", "paladin", "ranger", "rogue", "sorcerer", 
               "warlock", "wizard"]
    
    print("Features translation summary:")
    print("-" * 60)
    
    total_features = 0
    total_chars = 0
    
    for class_name in classes:
        info = process_class_file(class_name)
        if info:
            print(f"{class_name.capitalize():12} | {info['count']:3} features | {info['chars']:6} chars")
            total_features += info['count']
            total_chars += info['chars']
    
    print("-" * 60)
    print(f"{'Total':12} | {total_features:3} features | {total_chars:6} chars")

if __name__ == "__main__":
    main()
