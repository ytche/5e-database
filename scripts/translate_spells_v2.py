#!/usr/bin/env python3
"""
法术描述翻译脚本 V2 - 智能规则翻译
分批翻译 5e-SRD-Spells.json 中的法术描述
"""

import json
import re
import sys

# 扩展的术语翻译映射表 - 包含短语和常用表达
TRANSLATIONS = {
    # 完整短语和表达
    "You create": "你创造",
    "You choose": "你选择",
    "You can": "你可以",
    "You must": "你必须",
    "You do": "你进行",
    "You make": "你进行",
    "You touch": "你触摸",
    "You hurl": "你投掷",
    "You assume": "你变为",
    "You set": "你设置",
    "You target": "你指定目标",
    "You mentally": "你以精神",
    "You and": "你和",
    "You decide": "你决定",
    "You gain": "你获得",
    "You have": "你拥有",
    "You are": "你处于",
    "You become": "你变为",
    "You take": "你受到",
    "You cast": "你施放",
    "Your spell": "你的法术",
    "your spell": "你的法术",
    
    # 句子开头常用语
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
    
    # 动作描述
    "becomes a": "变为一个",
    "becomes": "变为",
    "become": "变为",
    "deals": "造成",
    "deal": "造成",
    "takes": "受到",
    "take": "受到",
    "make a": "进行一次",
    "makes a": "进行一次",
    "succeed on a": "成功通过一次",
    "succeeds on a": "成功通过一次",
    "must succeed on a": "必须成功通过一次",
    "or take": "否则受到",
    "or be": "否则被",
    "or become": "否则变为",
    
    # 条件描述
    "On a hit": "命中时",
    "On a miss": "未命中时",
    "On a success": "成功时",
    "On a successful save": "豁免成功时",
    "on a successful save": "豁免成功时",
    "On a failed save": "豁免失败时",
    "on a failed save": "豁免失败时",
    "for the duration": "在持续时间内",
    "until the spell ends": "直到法术结束",
    "for the spell's duration": "在法术持续时间内",
    "while the spell lasts": "在法术持续期间",
    "If you": "如果你",
    "If the": "如果该",
    "If a": "如果一个",
    "If an": "如果一个",
    "When you": "当你",
    "When the": "当该",
    "When a": "当一个",
    "When an": "当一个",
    "Once given": "一旦给予",
    "As long as": "只要",
    "as long as": "只要",
    
    # 位置和距离
    "within range": "在射程内",
    "within": "在",
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
    "centered on": "以",
    
    # 时间和持续
    "at the end of": "在结束时",
    "at the start of": "在开始时",
    "at the beginning of": "在开始时",
    "the end of its next turn": "其下个回合结束时",
    "its next turn": "其下个回合",
    "your next turn": "你下个回合",
    "for 1 minute": "持续1分钟",
    "for 1 hour": "持续1小时",
    "for 24 hours": "持续24小时",
    "until dispelled": "直到被解除",
    "for the duration": "在持续时间内",
    "during its next turn": "在其下个回合期间",
    "on each of your turns": "在你每个回合",
    "as an action": "作为一个动作",
    "as a bonus action": "作为一个附赠动作",
    "as a reaction": "作为一个反应",
    "on subsequent turns": "在随后的回合",
    
    # 数值和判定
    "equal to": "等于",
    "increases by": "增加",
    "decreases by": "减少",
    "gains": "获得",
    "gain": "获得",
    "has": "拥有",
    "have": "拥有",
    "can see": "可以看见",
    "can hear": "可以听见",
    "can speak": "可以说话",
    "can't speak": "无法说话",
    "can't": "无法",
    "cannot": "无法",
    
    # 效果描述
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
    
    # 魔法术语
    "saving throw": "豁免",
    "saving throws": "豁免",
    "spell attack": "法术攻击",
    "spell slot": "法术位",
    "spell slots": "法术位",
    "spell level": "法术环阶",
    "spellcasting ability": "施法属性",
    "spellcasting ability modifier": "施法属性调整值",
    "spell save DC": "法术豁免DC",
    
    # 动作类型
    "bonus action": "附赠动作",
    "bonus actions": "附赠动作",
    "reaction": "反应",
    "reactions": "反应",
    "free action": "免费动作",
    "action": "动作",
    "actions": "动作",
    "movement": "移动力",
    
    # 资源
    "hit point": "生命值",
    "hit points": "生命值",
    "temporary hit points": "临时生命值",
    "hit point maximum": "生命值上限",
    "current hit points": "当前生命值",
    
    # 战斗术语
    "attack roll": "攻击检定",
    "damage roll": "伤害检定",
    "ability check": "属性检定",
    "skill check": "技能检定",
    "concentration check": "专注检定",
    "concentration": "专注",
    "concentrating": "专注",
    
    # 距离
    "melee": "近战",
    "ranged": "远程",
    "reach": "触及",
    "touch": "接触",
    "self": "自身",
    "sight": "视野",
    "feet": "尺",
    "foot": "尺",
    
    # 时间单位
    "instantaneous": "立即",
    "round": "回合",
    "rounds": "回合",
    "minute": "分钟",
    "minutes": "分钟",
    "hour": "小时",
    "hours": "小时",
    "day": "日",
    "days": "日",
    "turn": "轮",
    "turns": "轮",
    
    # 伤害类型
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
    
    # 效果
    "half damage": "一半伤害",
    "half as much": "一半",
    "no damage": "无伤害",
    "extra damage": "额外伤害",
    "additional damage": "额外伤害",
    
    # 生物类型
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
    
    # 体型
    "Tiny": "微型",
    "Small": "小型",
    "Medium": "中型",
    "Large": "大型",
    "Huge": "巨型",
    "Gargantuan": "超巨型",
    "or smaller": "或更小",
    "or larger": "或更大",
    
    # 属性
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
    
    # 常见动词
    "choose": "选择",
    "chooses": "选择",
    "select": "选择",
    "target": "指定目标",
    "targets": "指定目标",
    "affect": "影响",
    "affects": "影响",
    "affected": "受影响的",
    "increase": "增加",
    "increases": "增加",
    "increased": "增加",
    "decrease": "减少",
    "decreases": "减少",
    "decreased": "减少",
    "reduce": "减少",
    "reduces": "减少",
    "reduced": "减少",
    "extend": "延伸",
    "extends": "延伸",
    "expand": "扩展",
    "expands": "扩展",
    "move": "移动",
    "moves": "移动",
    "travel": "移动",
    "travels": "移动",
    "appear": "出现",
    "appears": "出现",
    "disappear": "消失",
    "disappears": "消失",
    "vanish": "消失",
    "vanishes": "消失",
    "emerge": "显现",
    "emerges": "显现",
    "remain": "保持",
    "remains": "保持",
    "lasts": "持续",
    "last": "持续",
    "end": "结束",
    "ends": "结束",
    "begin": "开始",
    "begins": "开始",
    "start": "开始",
    "starts": "开始",
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
    "restore": "恢复",
    "restores": "恢复",
    "regain": "恢复",
    "regains": "恢复",
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
    "resist": "抵抗",
    "resists": "抵抗",
    "suppress": "压制",
    "suppresses": "压制",
    "dispel": "解除",
    "dispels": "解除",
    "counter": "反制",
    "counters": "反制",
    
    # 形容词
    "magical": "魔法的",
    "nonmagical": "非魔法的",
    "invisible": "隐形的",
    "visible": "可见的",
    "ethereal": "以太的",
    "incorporeal": "无形的",
    "corporeal": "有形的",
    "willing": "自愿的",
    "unwilling": "非自愿的",
    "hostile": "敌对的",
    "friendly": "友善的",
    "neutral": "中立的",
    "aware": "察觉的",
    "unaware": "未察觉的",
    "conscious": "清醒的",
    "unconscious": "昏迷的",
    "alive": "活着的",
    "dead": "死亡的",
    "undead": "不死的",
    
    # 方位和位置
    "centered": "以...为中心",
    "adjacent": "相邻的",
    "nearby": "附近的",
    "distant": "遥远的",
    "far": "远的",
    "close": "近的",
    "near": "靠近",
    "above": "上方",
    "below": "下方",
    "under": "下方",
    "over": "上方",
    "between": "之间",
    "among": "之中",
    "through": "穿过",
    "into": "进入",
    "out of": "离开",
    "away from": "远离",
    "toward": "朝向",
    "towards": "朝向",
    "against": "对抗",
    "beside": "旁边",
    "inside": "内部",
    "outside": "外部",
    "within": "在...之内",
    "beyond": "超出",
    "across": "横跨",
    "along": "沿着",
    "around": "围绕",
    "behind": "后面",
    "in front of": "前面",
    "next to": "旁边",
    "on top of": "顶部",
    "at the bottom of": "底部",
    
    # 常用介词短语
    "in addition": "此外",
    "in addition to": "此外",
    "instead of": "代替",
    "rather than": "而非",
    "as well as": "以及",
    "as if": "如同",
    "as though": "如同",
    "even if": "即使",
    "even though": "即使",
    "so that": "以便",
    "such as": "例如",
    "for example": "例如",
    "that is": "即",
    "in other words": "换句话说",
    "at least": "至少",
    "at most": "至多",
    "up to": "最多",
    "more than": "多于",
    "less than": "少于",
    "a number of": "若干",
    "the number of": "...的数量",
    "a piece of": "一块",
    "a bit of": "一点",
    "a drop of": "一滴",
    "a pinch of": "一撮",
    
    # 条件和结果
    "if": "如果",
    "then": "那么",
    "else": "否则",
    "otherwise": "否则",
    "unless": "除非",
    "whether": "是否",
    "although": "虽然",
    "though": "虽然",
    "while": "当",
    "during": "在...期间",
    "before": "在...之前",
    "after": "在...之后",
    "until": "直到",
    "till": "直到",
    "since": "自从",
    "once": "一旦",
    "whenever": "每当",
    "every time": "每次",
    "each time": "每次",
    
    # 逻辑连接
    "and": "且",
    "or": "或",
    "but": "但",
    "however": "然而",
    "therefore": "因此",
    "thus": "因此",
    "hence": "因此",
    "so": "所以",
    "because": "因为",
    "since": "因为",
    "as": "由于",
    "for": "因为",
    "also": "也",
    "too": "也",
    "either": "也",
    "neither": "也不",
    "both": "两者都",
    "all": "所有",
    "none": "无",
    "neither": "两者都不",
    "either": "任一",
    "whether": "无论",
    
    # 量词
    "any": "任何",
    "some": "某些",
    "many": "许多",
    "few": "少量",
    "several": "数个",
    "various": "各种",
    "multiple": "多个",
    "single": "单个",
    "one": "一个",
    "two": "两个",
    "three": "三个",
    "four": "四个",
    "five": "五个",
    "six": "六个",
    "seven": "七个",
    "eight": "八个",
    "nine": "九个",
    "ten": "十个",
    
    # 代词
    "it": "它",
    "its": "它的",
    "they": "它们",
    "them": "它们",
    "their": "它们的",
    "he": "他",
    "him": "他",
    "his": "他的",
    "she": "她",
    "her": "她",
    "hers": "她的",
    "you": "你",
    "your": "你的",
    "yours": "你的",
    "I": "我",
    "me": "我",
    "my": "我的",
    "mine": "我的",
    "we": "我们",
    "us": "我们",
    "our": "我们的",
    "ours": "我们的",
    "this": "这个",
    "that": "那个",
    "these": "这些",
    "those": "那些",
    "which": "哪个",
    "who": "谁",
    "whom": "谁",
    "whose": "谁的",
    "what": "什么",
    "whatever": "无论什么",
    "whoever": "无论谁",
    "whichever": "无论哪个",
    
    # 法术学派
    "abjuration": "防护",
    "conjuration": "咒法",
    "divination": "预言",
    "enchantment": "惑控",
    "evocation": "塑能",
    "illusion": "幻术",
    "necromancy": "死灵",
    "transmutation": "变化",
    
    # 其他游戏术语
    "level": "环阶",
    "cantrip": "戏法",
    "ritual": "仪式",
    "concentration": "专注",
    "verbal component": "言语成分",
    "somatic component": "姿势成分",
    "material component": "材料成分",
    "duration": "持续时间",
    "range": "射程",
    "area of effect": "影响区域",
    "saving throw": "豁免",
    "spell resistance": "法术抗力",
    "damage resistance": "伤害抗性",
    "damage immunity": "伤害免疫",
    "damage vulnerability": "伤害易伤",
    "condition immunity": "状态免疫",
    "magic resistance": "魔法抗性",
    "advantage": "优势",
    "disadvantage": "劣势",
    "proficiency": "熟练",
    "expertise": "专精",
    
    # 移动相关
    "speed": "速度",
    "walking speed": "步行速度",
    "flying speed": "飞行速度",
    "swimming speed": "游泳速度",
    "climbing speed": "攀爬速度",
    "burrowing speed": "掘穴速度",
    "hover": "悬浮",
    "difficult terrain": "困难地形",
    
    # 视觉相关
    "vision": "视觉",
    "darkvision": "黑暗视觉",
    "blindsight": "盲视",
    "truesight": "真实视觉",
    "see": "看见",
    "saw": "看见",
    "seen": "看见",
    "look": "看",
    "looks": "看",
    "appear": "出现",
    "appears": "出现",
    "visible": "可见的",
    "invisible": "隐形的",
    
    # 感知相关
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
    
    # 交流和思维
    "speak": "说话",
    "speaks": "说话",
    "spoke": "说话",
    "spoken": "说话",
    "say": "说",
    "says": "说",
    "said": "说",
    "tell": "告诉",
    "tells": "告诉",
    "told": "告诉",
    "communicate": "交流",
    "communicates": "交流",
    "understand": "理解",
    "understands": "理解",
    "know": "知道",
    "knows": "知道",
    "knew": "知道",
    "known": "知道",
    "think": "思考",
    "thinks": "思考",
    "thought": "思考",
    "believe": "相信",
    "believes": "相信",
    "remember": "记得",
    "remembers": "记得",
    "forget": "忘记",
    "forgets": "忘记",
    
    # 情感和意愿
    "want": "想要",
    "wants": "想要",
    "willing": "自愿的",
    "unwilling": "非自愿的",
    "choose": "选择",
    "chooses": "选择",
    "decide": "决定",
    "decides": "决定",
    "prefer": "偏好",
    "prefers": "偏好",
    "wish": "希望",
    "wishes": "希望",
    "hope": "希望",
    "hopes": "希望",
    "fear": "恐惧",
    "fears": "恐惧",
    "afraid": "害怕的",
    "frightened": "恐慌的",
    "terrified": "恐惧的",
    "calm": "平静",
    "angry": "愤怒的",
    "happy": "快乐的",
    "sad": "悲伤的",
    
    # 状态和条件
    "normal": "正常的",
    "abnormal": "异常的",
    "active": "激活的",
    "inactive": "未激活的",
    "available": "可用的",
    "unavailable": "不可用的",
    "possible": "可能的",
    "impossible": "不可能的",
    "able": "能够",
    "unable": "无法",
    "ready": "准备好的",
    "prepared": "准备好的",
    "unprepared": "未准备的",
    
    # 大小和数量
    "size": "体型",
    "height": "高度",
    "weight": "重量",
    "length": "长度",
    "width": "宽度",
    "depth": "深度",
    "area": "区域",
    "volume": "体积",
    "space": "空间",
    "distance": "距离",
    "range": "射程",
    "maximum": "最大",
    "minimum": "最小",
    "total": "总计",
    "partial": "部分",
    "complete": "完整",
    "incomplete": "不完整",
    "full": "满的",
    "empty": "空的",
    
    # 品质和特性
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
    "effect": "效果",
    "effects": "效果",
    "benefit": "益处",
    "benefits": "益处",
    "penalty": "惩罚",
    "penalties": "惩罚",
    "bonus": "加值",
    "bonuses": "加值",
    
    # 动作结果
    "success": "成功",
    "succeed": "成功",
    "succeeds": "成功",
    "successful": "成功的",
    "successfully": "成功地",
    "failure": "失败",
    "fail": "失败",
    "fails": "失败",
    "failed": "失败的",
    "win": "获胜",
    "wins": "获胜",
    "won": "获胜",
    "lose": "失去",
    "loses": "失去",
    "lost": "失去",
    "defeat": "击败",
    "defeats": "击败",
    "defeated": "被击败的",
    "victory": "胜利",
    "defeat": "失败",
    
    # 特殊表达
    "to hit": "命中",
    "to hit,": "命中，",
    "to damage": "伤害",
    "to the attack": "攻击检定",
    "to the damage": "伤害",
    "to all": "所有",
    "to any": "任何",
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
]

def smart_translate(text):
    """智能翻译文本"""
    if not text or not isinstance(text, str):
        return text
    
    # 保护需要保持原样的内容
    placeholders = []
    protected_text = text
    
    # 保护 Markdown 格式和特殊内容
    patterns_to_protect = [
        (r'\*\*\*[^*]+\*\*\*', '***'),  # bold italic headers
        (r'\*\*[^*]+\*\*', '**'),       # bold
        (r'\*[^*]+\*', '*'),            # italic
        (r'`[^`]+`', '`'),              # code
        (r'\[[^\]]+\]\([^)]+\)', '[]()'), # links
        (r'\|[^|]+\|', '|'),            # table cells
        (r'[-]+', '---'),               # table separators
        (r'#+\s+', '# '),               # headers
    ]
    
    for pattern, prefix in patterns_to_protect:
        matches = re.finditer(pattern, protected_text)
        for match in matches:
            placeholder = f"__P{len(placeholders)}__"
            placeholders.append((placeholder, match.group()))
            protected_text = protected_text.replace(match.group(), placeholder, 1)
    
    # 保护特定模式
    for pattern in PROTECTED_PATTERNS:
        matches = re.finditer(pattern, protected_text, re.IGNORECASE)
        for match in matches:
            placeholder = f"__P{len(placeholders)}__"
            placeholders.append((placeholder, match.group()))
            protected_text = protected_text.replace(match.group(), placeholder, 1)
    
    # 翻译 - 按长度降序以避免部分匹配
    translated = protected_text
    for en, zh in sorted(TRANSLATIONS.items(), key=lambda x: -len(x[0])):
        # 使用词边界进行精确匹配
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
        # 确保长度一致
        while len(spell['desc']) < len(spell['desc_en']):
            spell['desc'].append('')
        for i, text in enumerate(spell['desc_en']):
            if i < len(spell['desc']):
                spell['desc'][i] = smart_translate(text)
    
    # 翻译 higher_level
    if 'higher_level_en' in spell and spell['higher_level_en']:
        if 'higher_level' not in spell:
            spell['higher_level'] = []
        while len(spell['higher_level']) < len(spell['higher_level_en']):
            spell['higher_level'].append('')
        for i, text in enumerate(spell['higher_level_en']):
            if i < len(spell['higher_level']):
                spell['higher_level'][i] = smart_translate(text)
    
    # 翻译 material
    if 'material_en' in spell and spell['material_en']:
        spell['material'] = smart_translate(spell['material_en'])
    
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
        # 在原数组中找到并更新
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
        print("Usage: python translate_spells_v2.py <batch_number>")
        print("  batch 1: cantrips + level 1-2 (127 spells)")
        print("  batch 2: level 3-5 (110 spells)")
        print("  batch 3: level 6-9 (82 spells)")
        print("  batch all: all spells (319 spells)")
        sys.exit(1)
    
    batch = sys.argv[1]
    input_file = 'src/2014-zh/5e-SRD-Spells.json'
    output_file = 'src/2014-zh/5e-SRD-Spells.json'
    
    if batch == "1":
        # 第一批：戏法(0) + 1-2环 = 24 + 49 + 54 = 127
        count = 0
        count += process_spells(input_file, output_file, 0, 0)
        count += process_spells(input_file, output_file, 1, 2)
        print(f"\n=== Batch 1 complete: {count} spells ===")
    elif batch == "2":
        # 第二批：3-5环 = 42 + 31 + 37 = 110
        count = process_spells(input_file, output_file, 3, 5)
        print(f"\n=== Batch 2 complete: {count} spells ===")
    elif batch == "3":
        # 第三批：6-9环 = 31 + 20 + 16 + 15 = 82
        count = process_spells(input_file, output_file, 6, 9)
        print(f"\n=== Batch 3 complete: {count} spells ===")
    elif batch == "all":
        count = process_spells(input_file, output_file, 0, 9)
        print(f"\n=== All batches complete: {count} spells ===")
    else:
        print(f"Unknown batch: {batch}")
        sys.exit(1)
