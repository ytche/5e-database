#!/usr/bin/env python3
"""
法术描述翻译脚本 - 最终版
使用逐句翻译策略，保留英文原文在desc_en
"""

import json
import re
import sys

# 核心术语映射 - 按优先级排序
CORE_TERMS = {
    # 1. 句子开头模式 (最高优先级)
    "You create": "你创造",
    "You hurl": "你投掷",
    "You touch": "你触摸",
    "You choose": "你选择",
    "You can": "你可以",
    "You must": "你必须",
    "You do": "你进行",
    "You make": "你进行",
    "You set": "你设置",
    "You target": "你指定目标",
    "You mentally": "你以精神",
    "You decide": "你决定",
    "You gain": "你获得",
    "You have": "你拥有",
    "You are": "你处于",
    "You become": "你变为",
    "You take": "你受到",
    "You cast": "你施放",
    "You summon": "你召唤",
    "You transform": "你变形",
    "Your spell": "你的法术",
    "You assume": "你变为",
    "You specify": "你指定",
    "You speak": "你说出",
    "When you cast": "当你施放",
    "When the": "当",
    "If you": "如果你",
    "If the": "如果",
    "If a": "如果",
    "If an": "如果",
    
    # 2. 第三人称主语
    "The target": "目标",
    "The creature": "该生物",
    "The spell": "该法术",
    "The barrier": "该屏障",
    "The hand": "该手掌",
    "The object": "该物体",
    "The area": "该区域",
    "Each target": "每个目标",
    "Each creature": "每个生物",
    "All creatures": "所有生物",
    "All targets": "所有目标",
    "A target": "一个目标",
    "A creature": "一个生物",
    "An object": "一个物体",
    
    # 3. 常见动词
    "becomes a": "变为一个",
    "becomes": "变为",
    "become": "变为",
    "deals": "造成",
    "deal": "造成",
    "takes": "受到",
    "take": "受到",
    "make a": "进行一次",
    "makes a": "进行一次",
    "succeed on a": "成功通过",
    "succeeds on a": "成功通过",
    "must succeed on a": "必须成功通过",
    "or take": "否则受到",
    "or be": "否则被",
    "or become": "否则变为",
    "can make": "可以进行",
    "can use": "可以使用",
    "can see": "可以看见",
    "can move": "可以移动",
    "can choose": "可以选择",
    "can end": "可以结束",
    "can open": "可以打开",
    "can designate": "可以指定",
    "can appear": "可以出现",
    "can breathe": "可以呼吸",
    "can look": "可以看",
    "can pass": "可以通过",
    "can attack": "可以攻击",
    "can cast": "可以施放",
    "can't speak": "无法说话",
    "can't": "无法",
    "cannot": "无法",
    "may": "可以",
    
    # 4. 条件结果
    "On a hit": "命中时",
    "On a miss": "未命中时",
    "On a success": "成功时",
    "On a successful save": "豁免成功时",
    "on a successful save": "豁免成功时",
    "On a failed save": "豁免失败时",
    "on a failed save": "豁免失败时",
    "for the duration": "在持续时间内",
    "until the spell ends": "直到法术结束",
    "until dispelled": "直到被解除",
    "for the spell's duration": "在法术持续时间内",
    "while the spell lasts": "在法术持续期间",
    "Once given": "一旦给予",
    "As long as": "只要",
    "as long as": "只要",
    "Once": "一旦",
    "Whenever": "每当",
    "whenever": "每当",
    "Every time": "每次",
    "each time": "每次",
    
    # 5. 位置和距离
    "within range": "在射程内",
    "within": "在...范围内",
    "of it": "范围内",
    "of you": "范围内",
    "of the": "的",
    "within 5 feet of": "在5尺内的",
    "within 10 feet of": "在10尺内的",
    "within 30 feet of": "在30尺内的",
    "within 60 feet of": "在60尺内的",
    "within 120 feet of": "在120尺内的",
    "within 500 feet of": "在500尺内的",
    "within 1 mile of": "在1英里内的",
    "centered on you": "以你为中心",
    "centered on": "以...为中心",
    "in a": "在一个",
    "in an": "在一个",
    "in the": "在该",
    "in its": "在其",
    "in your": "在你的",
    "on a": "在一个",
    "on an": "在一个",
    "on the": "在该",
    "on its": "在其",
    "on your": "在你的",
    "at the": "在该",
    "at a": "在一个",
    "at an": "在一个",
    "at its": "在其",
    "at your": "在你的",
    
    # 6. 时间和持续
    "at the end of": "在...结束时",
    "at the start of": "在...开始时",
    "at the beginning of": "在...开始时",
    "the end of its next turn": "其下个回合结束时",
    "the end of your next turn": "你下个回合结束时",
    "its next turn": "其下个回合",
    "your next turn": "你下个回合",
    "for 1 minute": "持续1分钟",
    "for 1 hour": "持续1小时",
    "for 24 hours": "持续24小时",
    "for 8 hours": "持续8小时",
    "during its next turn": "在其下个回合期间",
    "on each of your turns": "在你每个回合",
    "as an action": "作为一个动作",
    "as a bonus action": "作为一个附赠动作",
    "as a reaction": "作为一个反应",
    "on subsequent turns": "在随后的回合",
    "at any time": "在任何时候",
    "at all times": "始终",
    "immediately": "立即",
    
    # 7. 数值和判定
    "equal to": "等于",
    "equals": "等于",
    "increases by": "增加",
    "decreases by": "减少",
    "gains": "获得",
    "gain": "获得",
    "has": "拥有",
    "had": "拥有",
    "adds": "添加",
    "add": "添加",
    "plus": "加",
    "minus": "减",
    "divided by": "除以",
    "multiplied by": "乘以",
    
    # 8. 效果描述
    "is reduced to 0": "降至0",
    "reduced to 0": "降至0",
    "drops to 0": "降至0",
    "reverts to": "恢复为",
    "returns to": "恢复为",
    "is suppressed": "被压制",
    "are suppressed": "被压制",
    "is charmed": "被魅惑",
    "is frightened": "陷入恐慌",
    "is poisoned": "中毒",
    "is blinded": "目盲",
    "is deafened": "耳聋",
    "is paralyzed": "被麻痹",
    "is stunned": "被震慑",
    "is prone": "倒地",
    "is grappled": "被擒抱",
    "is restrained": "被束缚",
    "is invisible": "处于隐形状态",
    "is immune to": "免疫于",
    "is resistant to": "具有抗性",
    "is vulnerable to": "具有易伤",
    "is affected by": "被影响",
    "are affected by": "被影响",
    "is targeted by": "被指定为目标",
    "are targeted by": "被指定为目标",
    
    # 9. 移动相关
    "moves": "移动",
    "move": "移动",
    "travels": "移动",
    "travel": "移动",
    "approaches": "接近",
    "approach": "接近",
    "retreats": "后退",
    "retreat": "后退",
    "enters": "进入",
    "enter": "进入",
    "exits": "离开",
    "exit": "离开",
    "leaves": "离开",
    "leave": "离开",
    "arrives": "到达",
    "arrive": "到达",
    "appears": "出现",
    "appear": "出现",
    "disappears": "消失",
    "disappear": "消失",
    "vanishes": "消失",
    "vanish": "消失",
    "remains": "保持",
    "remain": "保持",
    "lasts": "持续",
    "last": "持续",
    "end": "结束",
    "ends": "结束",
    "begins": "开始",
    "begin": "开始",
    "starts": "开始",
    "start": "开始",
    
    # 10. 动作类型
    "action": "动作",
    "actions": "动作",
    "bonus action": "附赠动作",
    "bonus actions": "附赠动作",
    "reaction": "反应",
    "reactions": "反应",
    "attack of opportunity": "借机攻击",
    
    # 11. 判定类型
    "saving throw": "豁免",
    "saving throws": "豁免",
    "ability check": "属性检定",
    "skill check": "技能检定",
    "spell attack": "法术攻击",
    "spell attacks": "法术攻击",
    "melee spell attack": "近战法术攻击",
    "ranged spell attack": "远程法术攻击",
    "attack roll": "攻击检定",
    "damage roll": "伤害检定",
    "concentration check": "专注检定",
    "contested check": "对抗检定",
    
    # 12. 资源类型
    "spell slot": "法术位",
    "spell slots": "法术位",
    "spell level": "法术环阶",
    "slot level": "法术位环阶",
    "character level": "角色等级",
    "hit point": "生命值",
    "hit points": "生命值",
    "temporary hit points": "临时生命值",
    "hit point maximum": "生命值上限",
    "current hit points": "当前生命值",
    "HP": "生命值",
    
    # 13. 属性
    "Strength": "力量",
    "Dexterity": "敏捷",
    "Constitution": "体质",
    "Intelligence": "智力",
    "Wisdom": "感知",
    "Charisma": "魅力",
    "strength": "力量",
    "dexterity": "敏捷",
    "constitution": "体质",
    "intelligence": "智力",
    "wisdom": "感知",
    "charisma": "魅力",
    "STR": "力量",
    "DEX": "敏捷",
    "CON": "体质",
    "INT": "智力",
    "WIS": "感知",
    "CHA": "魅力",
    
    # 14. 距离
    "melee": "近战",
    "ranged": "远程",
    "reach": "触及",
    "touch": "接触",
    "self": "自身",
    "sight": "视野",
    "unlimited": "无限",
    "feet": "尺",
    "foot": "尺",
    "range": "射程",
    "long range": "远距射程",
    
    # 15. 时间单位
    "instantaneous": "立即",
    "round": "回合",
    "rounds": "回合",
    "turn": "轮",
    "turns": "轮",
    "minute": "分钟",
    "minutes": "分钟",
    "hour": "小时",
    "hours": "小时",
    "day": "日",
    "days": "日",
    "duration": "持续时间",
    "casting time": "施法时间",
    
    # 16. 伤害类型
    "bludgeoning damage": "钝击伤害",
    "piercing damage": "穿刺伤害",
    "slashing damage": "挥砍伤害",
    "acid damage": "强酸伤害",
    "cold damage": "冷冻伤害",
    "fire damage": "火焰伤害",
    "force damage": "力场伤害",
    "lightning damage": "闪电伤害",
    "necrotic damage": "黯蚀伤害",
    "poison damage": "毒素伤害",
    "psychic damage": "心灵伤害",
    "radiant damage": "光耀伤害",
    "thunder damage": "雷鸣伤害",
    "damage type": "伤害类型",
    "half damage": "一半伤害",
    "half as much": "一半",
    "no damage": "无伤害",
    "extra damage": "额外伤害",
    "additional damage": "额外伤害",
    "initial damage": "初始伤害",
    
    # 17. 生物类型
    "creature": "生物",
    "creatures": "生物",
    "willing creature": "自愿生物",
    "willing creatures": "自愿生物",
    "hostile creature": "敌对生物",
    "hostile creatures": "敌对生物",
    "humanoid": "类人生物",
    "beast": "野兽",
    "undead": "不死生物",
    "construct": "构装生物",
    "fiend": "邪魔",
    "celestial": "天界生物",
    "fey": "精类",
    "elemental": "元素生物",
    "dragon": "龙",
    "aberration": "异怪",
    "ooze": "泥怪",
    "plant": "植物",
    "monstrosity": "怪兽",
    "giant": "巨人",
    "swarm": "集群",
    
    # 18. 体型
    "Tiny": "微型",
    "Small": "小型",
    "Medium": "中型",
    "Large": "大型",
    "Huge": "巨型",
    "Gargantuan": "超巨型",
    "or smaller": "或更小",
    "or larger": "或更大",
    
    # 19. 法术相关
    "spell": "法术",
    "spells": "法术",
    "cantrip": "戏法",
    "cantrips": "戏法",
    "ritual": "仪式",
    "magic": "魔法",
    "magical": "魔法的",
    "nonmagical": "非魔法的",
    "arcane": "奥术",
    "divine": "神圣",
    "spellcasting ability": "施法属性",
    "spellcasting ability modifier": "施法属性调整值",
    "spell save DC": "法术豁免DC",
    "school of magic": "魔法学派",
    "magic school": "魔法学派",
    
    # 20. 组件
    "component": "成分",
    "components": "成分",
    "verbal component": "言语成分",
    "somatic component": "姿势成分",
    "material component": "材料成分",
    
    # 21. 专注
    "concentration": "专注",
    "concentrating": "专注",
    "breaks concentration": "打断专注",
    "lose concentration": "失去专注",
    "maintain concentration": "维持专注",
    
    # 22. 效果区域
    "target": "目标",
    "targets": "目标",
    "effect": "效果",
    "effects": "效果",
    "area": "区域",
    "radius": "半径",
    "cube": "立方体",
    "sphere": "球体",
    "cone": "锥形",
    "line": "线形",
    "cylinder": "圆柱",
    "wall": "墙",
    "circle": "圆形",
    "hemisphere": "半球",
    "area of effect": "影响区域",
    
    # 23. 状态
    "charmed": "魅惑",
    "frightened": "恐慌",
    "paralyzed": "麻痹",
    "poisoned": "中毒",
    "blinded": "目盲",
    "deafened": "耳聋",
    "prone": "倒地",
    "grappled": "被擒抱",
    "restrained": "被束缚",
    "stunned": "被震慑",
    "unconscious": "昏迷",
    "incapacitated": "失能",
    "invisible": "隐形",
    "petrified": "石化",
    "exhaustion": "力竭",
    
    # 24. 阵营
    "lawful good": "守序善良",
    "neutral good": "中立善良",
    "chaotic good": "混乱善良",
    "lawful neutral": "守序中立",
    "true neutral": "绝对中立",
    "chaotic neutral": "混乱中立",
    "lawful evil": "守序邪恶",
    "neutral evil": "中立邪恶",
    "chaotic evil": "混乱邪恶",
    "alignment": "阵营",
    
    # 25. 其他
    "ally": "盟友",
    "allies": "盟友",
    "enemy": "敌人",
    "enemies": "敌人",
    "object": "物体",
    "objects": "物体",
    "weapon": "武器",
    "weapons": "武器",
    "armor": "护甲",
    "shield": "盾牌",
    "equipment": "装备",
    "gear": "装备",
    "item": "物品",
    "items": "物品",
    "tool": "工具",
    "tools": "工具",
    
    # 26. 视觉
    "vision": "视觉",
    "darkvision": "黑暗视觉",
    "blindsight": "盲视",
    "truesight": "真实视觉",
    "see": "看见",
    "sees": "看见",
    "saw": "看见",
    "seen": "看见",
    "look": "看",
    "looks": "看",
    "looking": "看",
    "appears": "出现",
    "appear": "出现",
    "visible": "可见的",
    "invisible": "隐形的",
    "line of sight": "视野线",
    
    # 27. 感知
    "hear": "听见",
    "hears": "听见",
    "heard": "听见",
    "listen": "聆听",
    "listens": "聆听",
    "smell": "闻到",
    "smells": "闻到",
    "sense": "感知",
    "senses": "感知",
    "feel": "感觉",
    "feels": "感觉",
    
    # 28. 移动速度
    "speed": "速度",
    "walking speed": "步行速度",
    "flying speed": "飞行速度",
    "swimming speed": "游泳速度",
    "climbing speed": "攀爬速度",
    "burrowing speed": "掘穴速度",
    "hover": "悬浮",
    "difficult terrain": "困难地形",
    
    # 29. 优势劣势
    "advantage": "优势",
    "disadvantage": "劣势",
    "proficiency": "熟练",
    "expertise": "专精",
    "proficient": "熟练的",
    
    # 30. 其他游戏术语
    "attack": "攻击",
    "attacks": "攻击",
    "damage": "伤害",
    "healing": "治疗",
    "heal": "治疗",
    "restores": "恢复",
    "restore": "恢复",
    "regains": "恢复",
    "regain": "恢复",
    "cover": "掩护",
    "half cover": "半身掩护",
    "three-quarters cover": "四分之三掩护",
    "total cover": "完全掩护",
    "DC": "DC",
    "AC": "AC",
    "challenge rating": "挑战等级",
    "CR": "CR",
    "XP": "XP",
    "inspiration": "激励",
    
    # 31. 常见形容词
    "magical": "魔法的",
    "nonmagical": "非魔法的",
    "willing": "自愿的",
    "unwilling": "非自愿的",
    "hostile": "敌对的",
    "friendly": "友善的",
    "neutral": "中立的",
    "aware": "察觉的",
    "unaware": "未察觉的",
    "conscious": "清醒的",
    "adjacent": "相邻的",
    "nearby": "附近的",
    "distant": "遥远的",
    "close": "近的",
    "far": "远的",
    "short": "短的",
    "long": "长的",
    "large": "大的",
    "small": "小的",
    "huge": "巨大的",
    "tiny": "微小的",
    "different": "不同的",
    "same": "相同的",
    "similar": "相似的",
    "various": "各种的",
    "specific": "特定的",
    "particular": "特定的",
    "general": "一般的",
    "certain": "特定的",
    "additional": "额外的",
    "extra": "额外的",
    "special": "特殊的",
    "normal": "正常的",
    "abnormal": "异常的",
    "natural": "自然的",
    "unnatural": "不自然的",
    "physical": "物理的",
    "mental": "精神的",
    "spiritual": "精神的",
    "ethereal": "以太的",
    "incorporeal": "无形的",
    "corporeal": "有形的",
    
    # 32. 常见名词
    "size": "体型",
    "height": "高度",
    "weight": "重量",
    "length": "长度",
    "width": "宽度",
    "depth": "深度",
    "distance": "距离",
    "maximum": "最大",
    "minimum": "最小",
    "total": "总计",
    "partial": "部分",
    "complete": "完整",
    "full": "满的",
    "empty": "空的",
    "quantity": "数量",
    "quality": "品质",
    "property": "特性",
    "properties": "特性",
    "feature": "特征",
    "features": "特征",
    "trait": "特质",
    "traits": "特质",
    "ability": "能力",
    "abilities": "能力",
    "power": "力量",
    "powers": "力量",
    "bonus": "加值",
    "penalty": "惩罚",
    
    # 33. 成功失败
    "success": "成功",
    "succeed": "成功",
    "succeeds": "成功",
    "successful": "成功的",
    "successfully": "成功地",
    "failure": "失败",
    "fail": "失败",
    "fails": "失败",
    "failed": "失败的",
    
    # 34. 材质相关
    "object": "物体",
    "objects": "物体",
    "substance": "物质",
    "material": "材料",
    "surface": "表面",
    "solid": "固体的",
    "liquid": "液体的",
    "gas": "气体的",
    "metal": "金属",
    "wood": "木材",
    "stone": "石头",
    "glass": "玻璃",
    "cloth": "布料",
    "paper": "纸张",
    "gem": "宝石",
    "crystal": "水晶",
    
    # 35. 其他动词
    "choose": "选择",
    "chooses": "选择",
    "chosen": "选择的",
    "select": "选择",
    "selects": "选择",
    "designate": "指定",
    "designates": "指定",
    "affect": "影响",
    "affects": "影响",
    "affected": "受影响的",
    "increase": "增加",
    "increases": "增加",
    "increased": "增加的",
    "decrease": "减少",
    "decreases": "减少",
    "decreased": "减少的",
    "reduce": "减少",
    "reduces": "减少",
    "reduced": "减少的",
    "extend": "延伸",
    "extends": "延伸",
    "expand": "扩展",
    "expands": "扩展",
    "prevent": "阻止",
    "prevents": "阻止",
    "block": "阻挡",
    "blocks": "阻挡",
    "protect": "保护",
    "protects": "保护",
    "resist": "抵抗",
    "resists": "抵抗",
    "immune": "免疫",
    "absorb": "吸收",
    "absorbs": "吸收",
    "heal": "治疗",
    "heals": "治疗",
    "expend": "消耗",
    "expends": "消耗",
    "consume": "消耗",
    "consumes": "消耗",
    "use": "使用",
    "uses": "使用",
    "using": "使用",
    "cast": "施放",
    "casting": "施放",
    "summon": "召唤",
    "summons": "召唤",
    "create": "创造",
    "creates": "创造",
    "created": "创造的",
    "transform": "变形",
    "transforms": "变形",
    "change": "改变",
    "changes": "改变",
    "replace": "替代",
    "replaces": "替代",
    "ignore": "无视",
    "ignores": "无视",
    "avoid": "避免",
    "avoids": "避免",
    "suppress": "压制",
    "suppresses": "压制",
    "dispel": "解除",
    "dispels": "解除",
    "counter": "反制",
    "counters": "反制",
    
    # 36. 冠词限定词
    "a": "一个",
    "an": "一个",
    "the": "该",
    "this": "这个",
    "that": "那个",
    "these": "这些",
    "those": "那些",
    "all": "所有",
    "any": "任何",
    "some": "某些",
    "many": "许多",
    "few": "少量",
    "several": "数个",
    "each": "每个",
    "every": "每个",
    "both": "两者都",
    "either": "任一",
    "neither": "两者都不",
    "none": "无",
    "other": "其他",
    "another": "另一个",
    "such": "这样的",
    "what": "什么",
    "which": "哪个",
    "whose": "谁的",
    
    # 37. 代词
    "it": "它",
    "its": "它的",
    "they": "它们",
    "them": "它们",
    "their": "它们的",
    "theirs": "它们的",
    "he": "他",
    "him": "他",
    "his": "他的",
    "she": "她",
    "her": "她的",
    "hers": "她的",
    "you": "你",
    "your": "你的",
    "yours": "你的",
    "we": "我们",
    "us": "我们",
    "our": "我们的",
    "ours": "我们的",
    "I": "我",
    "me": "我",
    "my": "我的",
    "mine": "我的",
    "who": "谁",
    "whom": "谁",
    "whoever": "无论谁",
    "whomever": "无论谁",
    "whatever": "无论什么",
    "whichever": "无论哪个",
    
    # 38. 介词
    "in": "在",
    "on": "在",
    "at": "在",
    "by": "通过",
    "with": "带有",
    "without": "没有",
    "from": "从",
    "to": "至",
    "into": "进入",
    "onto": "到...上",
    "out": "出去",
    "off": "离开",
    "up": "向上",
    "down": "向下",
    "over": "在...上方",
    "under": "在...下方",
    "above": "在...上方",
    "below": "在...下方",
    "before": "在...之前",
    "after": "在...之后",
    "behind": "在...后面",
    "beside": "在...旁边",
    "near": "靠近",
    "between": "在...之间",
    "among": "在...之中",
    "through": "穿过",
    "across": "横跨",
    "along": "沿着",
    "around": "围绕",
    "against": "对抗",
    "toward": "朝向",
    "towards": "朝向",
    "within": "在...之内",
    "inside": "在...内部",
    "outside": "在...外部",
    "beyond": "超出",
    "past": "经过",
    "per": "每",
    "during": "在...期间",
    "until": "直到",
    "of": "的",
    "for": "为了",
    "about": "关于",
    "against": "对抗",
    "like": "像",
    "unlike": "不像",
    "except": "除了",
    "besides": "除了",
    "including": "包括",
    "excluding": "不包括",
    
    # 39. 连词
    "and": "且",
    "or": "或",
    "but": "但",
    "yet": "然而",
    "so": "所以",
    "because": "因为",
    "since": "因为",
    "as": "由于",
    "while": "当",
    "when": "当",
    "whenever": "每当",
    "if": "如果",
    "unless": "除非",
    "although": "虽然",
    "though": "虽然",
    "even": "即使",
    "whether": "是否",
    "than": "比",
    "then": "那么",
    
    # 40. 副词
    "not": "不",
    "no": "无",
    "never": "从不",
    "always": "总是",
    "often": "经常",
    "sometimes": "有时",
    "usually": "通常",
    "also": "也",
    "too": "也",
    "either": "也",
    "only": "仅",
    "just": "刚刚",
    "even": "甚至",
    "still": "仍然",
    "already": "已经",
    "yet": "还",
    "soon": "很快",
    "now": "现在",
    "then": "那时",
    "here": "这里",
    "there": "那里",
    "everywhere": "到处",
    "somewhere": "某处",
    "anywhere": "任何地方",
    "elsewhere": "其他地方",
    "together": "一起",
    "apart": "分开",
    "instead": "代替",
    "otherwise": "否则",
    "therefore": "因此",
    "thus": "因此",
    "however": "然而",
    "moreover": "此外",
    "furthermore": "此外",
    "besides": "此外",
    "indeed": "确实",
    "actually": "实际上",
    "really": "真的",
    "truly": "真正地",
    "certainly": "当然",
    "probably": "可能",
    "perhaps": "也许",
    "maybe": "也许",
    "likely": "可能",
    "possibly": "可能",
    "almost": "几乎",
    "nearly": "几乎",
    "quite": "相当",
    "very": "非常",
    "much": "很",
    "more": "更多",
    "most": "最多",
    "less": "更少",
    "least": "最少",
    "enough": "足够",
    "rather": "相当",
    "quite": "相当",
    "fairly": "相当",
    "pretty": "相当",
    "completely": "完全地",
    "totally": "完全地",
    "entirely": "完全地",
    "fully": "完全地",
    "partly": "部分地",
    "partially": "部分地",
    "hardly": "几乎不",
    "barely": " barely",
    "scarcely": " scarcely",
    "well": " well",
    "badly": " badly",
    "better": "更好",
    "best": "最好",
    "worse": "更糟",
    "worst": "最糟",
}

# 需要保持原样的模式
PROTECTED_PATTERNS = [
    r'\bDC\s*\d+',  # DC 15
    r'\d+d\d+(?:\s*\+\s*\d+)?',  # 2d6, 4d4+2
    r'\+\d+\s+to\s+hit',  # +8 to hit
    r'\d+\s*(?:ft\.?|feet|foot)',  # 30 feet
    r'\d+\s*(?:minute|hour|day|round|turn)s?',  # 10 minutes
    r'\d+\s*(?:gp|sp|cp)',  # 25gp
    r'\d+\s*mile',  # 1 mile
    r'\bAC\s*\d+',  # AC 20
    r'\d+\s*级',  # 5级
    r'\d+\s*环',  # 3环
    r'\d+\s*hp',  # 25 hp
    r'\d+\s*HP',  # 25 HP
    r'\d+%',  # 50%
    r'\+\d+',  # +1
    r'-\d+',  # -1
    r'\d+\.\d+',  # 1.5
    r'\d+',  # 保护数字
]

def translate_text(text):
    """翻译文本"""
    if not text or not isinstance(text, str):
        return text
    
    # 保护 Markdown 格式和特殊内容
    placeholders = []
    protected_text = text
    
    # 保护 Markdown 格式
    md_patterns = [
        (r'\*\*\*[^*]+\*\*\*', '***'),  # bold italic headers
        (r'\*\*[^*]+\*\*', '**'),       # bold
        (r'\*[^*]+\*', '*'),            # italic
        (r'`[^`]+`', '`'),              # code
        (r'\[[^\]]+\]\([^)]+\)', '[]()'), # links
        (r'\|[^|]+\|', '|'),            # table cells
        (r'[-]+', '---'),               # table separators
        (r'#+\s+', '# '),               # headers
    ]
    
    for pattern, prefix in md_patterns:
        matches = re.finditer(pattern, protected_text)
        for match in matches:
            placeholder = f"__P{len(placeholders)}__"
            placeholders.append((placeholder, match.group()))
            protected_text = protected_text.replace(match.group(), placeholder, 1)
    
    # 保护特定游戏数值模式
    for pattern in PROTECTED_PATTERNS:
        matches = re.finditer(pattern, protected_text, re.IGNORECASE)
        for match in matches:
            placeholder = f"__P{len(placeholders)}__"
            placeholders.append((placeholder, match.group()))
            protected_text = protected_text.replace(match.group(), placeholder, 1)
    
    # 翻译 - 按长度降序以避免部分匹配
    translated = protected_text
    for en, zh in sorted(CORE_TERMS.items(), key=lambda x: -len(x[0])):
        pattern = r'\b' + re.escape(en) + r'\b'
        translated = re.sub(pattern, zh, translated, flags=re.IGNORECASE)
    
    # 恢复保护的内容
    for placeholder, original in placeholders:
        translated = translated.replace(placeholder, original, 1)
    
    # 后处理：清理多余空格
    translated = re.sub(r'\s+', ' ', translated).strip()
    
    return translated


def translate_spell(spell):
    """翻译单个法术"""
    # 翻译 desc
    if 'desc_en' in spell and spell['desc_en']:
        if 'desc' not in spell:
            spell['desc'] = []
        while len(spell['desc']) < len(spell['desc_en']):
            spell['desc'].append('')
        for i, text in enumerate(spell['desc_en']):
            if i < len(spell['desc']):
                spell['desc'][i] = translate_text(text)
    
    # 翻译 higher_level
    if 'higher_level_en' in spell and spell['higher_level_en']:
        if 'higher_level' not in spell:
            spell['higher_level'] = []
        while len(spell['higher_level']) < len(spell['higher_level_en']):
            spell['higher_level'].append('')
        for i, text in enumerate(spell['higher_level_en']):
            if i < len(spell['higher_level']):
                spell['higher_level'][i] = translate_text(text)
    
    # 翻译 material
    if 'material_en' in spell and spell['material_en']:
        spell['material'] = translate_text(spell['material_en'])
    
    return spell


def process_spells(input_file, output_file, level_min=None, level_max=None):
    """处理法术文件"""
    with open(input_file, 'r', encoding='utf-8') as f:
        spells = json.load(f)
    
    # 筛选指定等级的法术
    if level_min is not None and level_max is not None:
        target_spells = [s for s in spells if level_min <= s.get('level', 0) <= level_max]
    else:
        target_spells = spells
    
    print(f"Translating {len(target_spells)} spells (level {level_min}-{level_max})...")
    
    # 翻译每个法术
    for i, spell in enumerate(target_spells):
        for j, s in enumerate(spells):
            if s.get('index') == spell.get('index'):
                spells[j] = translate_spell(s)
                break
        
        if (i + 1) % 10 == 0 or (i + 1) == len(target_spells):
            print(f"  Progress: {i + 1}/{len(target_spells)}")
    
    # 保存结果
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(spells, f, ensure_ascii=False, indent=2)
    
    return len(target_spells)


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: python translate_final.py <batch_number>")
        print("  batch 1: cantrips + level 1-2 (127 spells)")
        print("  batch 2: level 3-5 (110 spells)")
        print("  batch 3: level 6-9 (82 spells)")
        print("  batch all: all spells (319 spells)")
        sys.exit(1)
    
    batch = sys.argv[1]
    input_file = 'src/2014-zh/5e-SRD-Spells.json'
    output_file = 'src/2014-zh/5e-SRD-Spells.json'
    
    if batch == "1":
        count = 0
        count += process_spells(input_file, output_file, 0, 0)
        count += process_spells(input_file, output_file, 1, 2)
        print(f"\n=== Batch 1 complete: {count} spells ===")
    elif batch == "2":
        count = process_spells(input_file, output_file, 3, 5)
        print(f"\n=== Batch 2 complete: {count} spells ===")
    elif batch == "3":
        count = process_spells(input_file, output_file, 6, 9)
        print(f"\n=== Batch 3 complete: {count} spells ===")
    elif batch == "all":
        count = process_spells(input_file, output_file, 0, 9)
        print(f"\n=== All batches complete: {count} spells ===")
    else:
        print(f"Unknown batch: {batch}")
        sys.exit(1)
