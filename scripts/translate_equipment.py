#!/usr/bin/env python3
"""
翻译 5e-SRD-Equipment.json 文件
"""

import json
import re

# ========== 术语翻译表 ==========

# 装备名称翻译 (来自 GLOSSARY.md 第16节)
EQUIPMENT_NAMES = {
    # 简易武器 - 近战
    "Club": "短棒",
    "Dagger": "匕首",
    "Greatclub": "巨棒",
    "Handaxe": "手斧",
    "Javelin": "标枪",
    "Light hammer": "轻锤",
    "Mace": "硬头锤",
    "Quarterstaff": "长棍",
    "Sickle": "镰刀",
    "Spear": "矛",
    # 简易武器 - 远程
    "Crossbow, light": "轻弩",
    "Dart": "飞镖",
    "Shortbow": "短弓",
    "Sling": "投石索",
    # 军用武器 - 近战
    "Battleaxe": "战斧",
    "Flail": "链枷",
    "Glaive": "长柄刀",
    "Greataxe": "巨斧",
    "Greatsword": "巨剑",
    "Halberd": "戟",
    "Lance": "骑枪",
    "Longsword": "长剑",
    "Maul": "巨锤",
    "Morningstar": "钉头锤",
    "Pike": "长矛",
    "Rapier": "刺剑",
    "Scimitar": "弯刀",
    "Shortsword": "短剑",
    "Trident": "三叉戟",
    "War pick": "战镐",
    "Warhammer": "战锤",
    "Whip": "鞭",
    # 军用武器 - 远程
    "Blowgun": "吹箭筒",
    "Crossbow, hand": "手弩",
    "Crossbow, heavy": "重弩",
    "Longbow": "长弓",
    "Net": "捕网",
    # 护甲
    "Padded Armor": "布甲",
    "Leather Armor": "皮甲",
    "Studded Leather Armor": "镶钉皮甲",
    "Hide Armor": "兽皮甲",
    "Chain Shirt": "链甲衫",
    "Scale Mail": "鳞甲",
    "Breastplate": "胸甲",
    "Half Plate Armor": "半身板甲",
    "Ring Mail": "环甲",
    "Chain Mail": "锁子甲",
    "Splint Armor": "板条甲",
    "Plate Armor": "板甲",
    "Shield": "盾牌",
}

# 装备分类翻译
CATEGORY_NAMES = {
    "Weapon": "武器",
    "Armor": "护甲",
    "Adventuring Gear": "冒险装备",
    "Ammunition": "弹药",
    "Tools": "工具",
    "Mounts and Vehicles": "坐骑与载具",
    "Standard Gear": "标准装备",
    "Kits": "工具包",
    "Equipment Packs": "装备包",
}

# 武器分类
WEAPON_CATEGORIES = {
    "Simple": "简易",
    "Martial": "军用",
}

WEAPON_RANGES = {
    "Melee": "近战",
    "Ranged": "远程",
}

# category_range 组合翻译
CATEGORY_RANGES = {
    "Simple Melee": "简易近战",
    "Simple Ranged": "简易远程",
    "Martial Melee": "军用近战",
    "Martial Ranged": "军用远程",
}

# 伤害类型
DAMAGE_TYPES = {
    "Bludgeoning": "钝击",
    "Piercing": "穿刺",
    "Slashing": "挥砍",
}

# 武器属性 (来自 GLOSSARY.md 第8节)
WEAPON_PROPERTIES = {
    "Ammunition": "弹药",
    "Finesse": "灵巧",
    "Heavy": "重型",
    "Light": "轻型",
    "Loading": "装填",
    "Reach": "触及",
    "Special": "特殊",
    "Thrown": "投掷",
    "Two-Handed": "双手",
    "Versatile": "两用",
    "Monk": "武僧",
}

# 护甲分类
ARMOR_CATEGORIES = {
    "Light": "轻甲",
    "Medium": "中甲",
    "Heavy": "重甲",
    "Shield": "盾牌",
}

# 工具分类
TOOL_CATEGORIES = {
    "Artisan's Tools": "工匠工具",
    "Gaming Sets": "游戏套具",
    "Musical Instruments": "乐器",
    "Other Tools": "其他工具",
}

# 载具分类
VEHICLE_CATEGORIES = {
    "Mounts and Other Animals": "坐骑和其他动物",
    "Tack, Harness, and Drawn Vehicles": "挽具和载具",
    "Waterborne Vehicles": "水上载具",
}

# 成本单位
COST_UNITS = {
    "cp": "铜币",
    "sp": "银币",
    "gp": "金币",
    "pp": "铂金币",
}

# 冒险装备名称 (需要翻译的常用装备)
ADVENTURING_GEAR_NAMES = {
    # 基础装备
    "Abacus": "算盘",
    "Acid (vial)": "强酸（小瓶）",
    "Alchemist's fire (flask)": "炼金术士之火（烧瓶）",
    "Alms box": "布施盒",
    "Arrow": "箭矢",
    "Backpack": "背包",
    "Ball bearings (bag of 1,000)": "滚珠（1000颗袋装）",
    "Barrel": "桶",
    "Basket": "篮子",
    "Bedroll": "铺盖",
    "Bell": "铃铛",
    "Blanket": "毯子",
    "Block and tackle": "滑轮组",
    "Block of incense": "香块",
    "Blowgun needles (50)": "吹箭（50支）",
    "Book": "书籍",
    "Bottle, glass": "玻璃瓶",
    "Bucket": "水桶",
    "Caltrops": "铁蒺藜",
    "Candle": "蜡烛",
    "Case, crossbow bolt": "弩矢盒",
    "Case, map or scroll": "地图或卷轴筒",
    "Chain (10 feet)": "锁链（10尺）",
    "Chalk (1 piece)": "粉笔（1支）",
    "Chest": "箱子",
    "Climber's kit": "攀爬工具",
    "Clothes, common": "普通衣物",
    "Clothes, costume": "戏服",
    "Clothes, fine": "精致衣物",
    "Clothes, traveler's": "旅行者衣物",
    "Component pouch": "材料包",
    "Crowbar": "撬棍",
    "Fishing tackle": "钓具",
    "Flask or tankard": "烧瓶或酒杯",
    "Grappling hook": "抓钩",
    "Hammer": "锤子",
    "Hammer, sledge": "大锤",
    "Healer's kit": "医疗工具包",
    "Holy water (flask)": "圣水（烧瓶）",
    "Hourglass": "沙漏",
    "Hunting trap": "狩猎陷阱",
    "Ink (1 ounce bottle)": "墨水（1盎司瓶）",
    "Ink pen": "钢笔",
    "Jug or pitcher": "壶或 pitcher",
    "Ladder (10-foot)": "梯子（10尺）",
    "Lamp": "油灯",
    "Lantern, bullseye": "提灯，聚光式",
    "Lantern, hooded": "提灯，罩式",
    "Lock": "锁",
    "Magnifying glass": "放大镜",
    "Manacles": "镣铐",
    "Mess kit": "餐具包",
    "Mirror, steel": "钢镜",
    "Oil (flask)": "燃油（烧瓶）",
    "Paper (one sheet)": "纸张（一张）",
    "Parchment (one sheet)": "羊皮纸（一张）",
    "Perfume (vial)": "香水（小瓶）",
    "Pick, miner's": "矿工镐",
    "Piton": "岩钉",
    "Poison, basic (vial)": "基础毒药（小瓶）",
    "Pole (10-foot)": "长杆（10尺）",
    "Pot, iron": "铁锅",
    "Potion of healing": "治疗药水",
    "Pouch": "小包",
    "Quiver": "箭袋",
    "Ram, portable": "破门锤，便携式",
    "Rations (1 day)": "口粮（1天）",
    "Robes": "长袍",
    "Rope, hempen (50 feet)": "麻绳（50尺）",
    "Rope, silk (50 feet)": "丝绳（50尺）",
    "Sack": "麻袋",
    "Scale, merchant's": "天平，商人用",
    "Sealing wax": "封蜡",
    "Shovel": "铲子",
    "Signal whistle": "信号哨",
    "Signet ring": "印章戒指",
    "Soap": "肥皂",
    "Spellbook": "法术书",
    "Spike, iron": "铁钉",
    "Spyglass": "望远镜",
    "String (10 feet)": "细绳（10尺）",
    "Tent, two-person": "帐篷，双人",
    "Tinderbox": "火绒盒",
    "Torch": "火把",
    "Vestments": "祭服",
    "Vial": "小瓶",
    "Waterskin": "水袋",
    "Whetstone": "磨刀石",
    # 法术法器 - 奥术
    "Crystal": "水晶",
    "Orb": "法球",
    "Rod": "权杖",
    "Staff": "法杖",
    "Wand": "魔杖",
    # 法术法器 - 德鲁伊
    "Sprig of mistletoe": "槲寄生枝条",
    "Totem": "图腾",
    "Wooden staff": "木制法杖",
    "Yew wand": "紫杉魔杖",
    # 法术法器 - 圣徽
    "Amulet": "护符",
    "Emblem": "徽章",
    "Reliquary": "圣物匣",
    # 小物品（装备包中的）
    "Small knife": "小刀",
    "Little bag of sand": "小袋沙子",
    # 其他工具
    "Disguise Kit": "易容工具包",
    "Disguise kit": "易容工具包",
    "Forgery Kit": "伪造工具包",
    "Forgery kit": "伪造工具包",
    "Herbalism Kit": "草药工具包",
    "Herbalism kit": "草药工具包",
    "Poisoner's Kit": "制毒工具包",
    "Poisoner's kit": "制毒工具包",
    "Navigator's Tools": "领航工具",
    "Navigator's tools": "领航工具",
    "Thieves' Tools": "盗贼工具",
    "Thieves' tools": "盗贼工具",
    # 其他缺失的工具和装备
    "Antitoxin (vial)": "解毒剂（小瓶）",
    "Blowgun needle": "吹箭",
    "Censer": "香炉",
    "Climber's Kit": "攀爬工具",
    "Climber's kit": "攀爬工具",
    "Crossbow bolt": "弩矢",
    "Dice Set": "骰子套组",
    "Dice set": "骰子套组",
    "Healer's Kit": "医疗工具包",
    "Healer's kit": "医疗工具包",
    "Mess Kit": "餐具包",
    "Mess kit": "餐具包",
    "Playing Card Set": "扑克牌套组",
    "Playing card set": "扑克牌套组",
    "Sling bullet": "投石索弹丸",
    # 弹药
    "Crossbow bolts (20)": "弩矢（20支）",
    "Sling bullets (20)": "投石索弹丸（20颗）",
    # 游戏套具
    "Dice set": "骰子套组",
    "Playing card set": "扑克牌套组",
    # 乐器
    "Bagpipes": "风笛",
    "Drum": "鼓",
    "Dulcimer": "扬琴",
    "Flute": "长笛",
    "Lute": "鲁特琴",
    "Lyre": "里拉琴",
    "Horn": "角号",
    "Pan flute": "排箫",
    "Shawm": "芦笛",
    "Viol": "提琴",
    # 工匠工具
    "Alchemist's Supplies": "炼金工具",
    "Alchemist's supplies": "炼金工具",
    "Brewer's Supplies": "酿酒工具",
    "Brewer's supplies": "酿酒工具",
    "Calligrapher's Supplies": "书法工具",
    "Calligrapher's supplies": "书法工具",
    "Carpenter's Tools": "木匠工具",
    "Carpenter's tools": "木匠工具",
    "Cartographer's Tools": "制图工具",
    "Cartographer's tools": "制图工具",
    "Cobbler's Tools": "鞋匠工具",
    "Cobbler's tools": "鞋匠工具",
    "Cook's Utensils": "厨师工具",
    "Cook's utensils": "厨师工具",
    "Glassblower's Tools": "玻璃匠工具",
    "Glassblower's tools": "玻璃匠工具",
    "Jeweler's Tools": "珠宝工匠具",
    "Jeweler's tools": "珠宝工匠具",
    "Leatherworker's Tools": "皮匠工具",
    "Leatherworker's tools": "皮匠工具",
    "Mason's Tools": "石匠工具",
    "Mason's tools": "石匠工具",
    "Painter's Supplies": "画家工具",
    "Painter's supplies": "画家工具",
    "Potter's Tools": "陶匠工具",
    "Potter's tools": "陶匠工具",
    "Smith's Tools": "铁匠工具",
    "Smith's tools": "铁匠工具",
    "Tinker's Tools": "修补工具",
    "Tinker's tools": "修补工具",
    "Weaver's Tools": "织布工具",
    "Weaver's tools": "织布工具",
    "Woodcarver's Tools": "木雕工具",
    "Woodcarver's tools": "木雕工具",
    # 装备包
    "Burglar's Pack": "窃贼套装",
    "Diplomat's Pack": "外交家套装",
    "Dungeoneer's Pack": "地城探险套装",
    "Entertainer's Pack": "艺人套装",
    "Explorer's Pack": "探险家套装",
    "Priest's Pack": "牧师套装",
    "Scholar's Pack": "学者套装",
    # 坐骑
    "Camel": "骆驼",
    "Donkey": "驴",
    "Mule": "骡子",
    "Elephant": "大象",
    "Horse, draft": "马，役用",
    "Horse, riding": "马，骑乘",
    "Mastiff": "獒犬",
    "Pony": "矮马",
    "Warhorse": "战马",
    # 载具装备
    "Barding: Padded": "马铠：布甲",
    "Barding: Leather": "马铠：皮甲",
    "Barding: Studded Leather": "马铠：镶钉皮甲",
    "Barding: Hide": "马铠：兽皮甲",
    "Barding: Chain shirt": "马铠：链甲衫",
    "Barding: Scale mail": "马铠：鳞甲",
    "Barding: Breastplate": "马铠：胸甲",
    "Barding: Half plate": "马铠：半身板甲",
    "Barding: Ring mail": "马铠：环甲",
    "Barding: Chain mail": "马铠：锁子甲",
    "Barding: Splint": "马铠：板条甲",
    "Barding: Plate": "马铠：板甲",
    "Bit and bridle": "马嚼和缰绳",
    "Carriage": "马车",
    "Cart": "手推车",
    "Chariot": "战车",
    "Animal Feed (1 day)": "动物饲料（1天）",
    "Saddle, Exotic": "鞍具，异种",
    "Saddle, Military": "鞍具，军用",
    "Saddle, Pack": "鞍具，驮鞍",
    "Saddle, Riding": "鞍具，骑鞍",
    "Saddlebags": "鞍囊",
    "Sled": "雪橇",
    "Stabling (1 day)": "寄养（1天）",
    "Wagon": "货车",
    "Galley": "桨帆船",
    "Keelboat": "龙骨船",
    "Longship": "长船",
    "Rowboat": "划艇",
    "Sailing ship": "帆船",
    "Warship": "战舰",
}

# 速度单位
SPEED_UNITS = {
    "ft/round": "尺/轮",
    "mph": "英里/小时",
}


def translate_name(name):
    """翻译装备名称"""
    if not name:
        return name
    
    # 直接匹配
    if name in EQUIPMENT_NAMES:
        return EQUIPMENT_NAMES[name]
    if name in ADVENTURING_GEAR_NAMES:
        return ADVENTURING_GEAR_NAMES[name]
    
    # 尝试匹配括号内的内容
    # 例如 "Rations (1 day)" -> "口粮（1天）"
    
    return name


def translate_cost_unit(unit):
    """翻译成本单位"""
    return COST_UNITS.get(unit, unit)


def translate_equipment_category(cat):
    """翻译装备分类对象"""
    if not cat or not isinstance(cat, dict):
        return cat
    
    new_cat = dict(cat)
    if "name" in cat:
        orig_name = cat["name"]
        new_cat["name"] = CATEGORY_NAMES.get(orig_name, orig_name)
        new_cat["name_en"] = orig_name
    return new_cat


def translate_damage_type(dt):
    """翻译伤害类型对象"""
    if not dt or not isinstance(dt, dict):
        return dt
    
    new_dt = dict(dt)
    if "name" in dt:
        orig_name = dt["name"]
        new_dt["name"] = DAMAGE_TYPES.get(orig_name, orig_name)
        new_dt["name_en"] = orig_name
    return new_dt


def translate_property(prop):
    """翻译武器属性对象"""
    if not prop or not isinstance(prop, dict):
        return prop
    
    new_prop = dict(prop)
    if "name" in prop:
        orig_name = prop["name"]
        new_prop["name"] = WEAPON_PROPERTIES.get(orig_name, orig_name)
        new_prop["name_en"] = orig_name
    return new_prop


def translate_item(item):
    """翻译内容物中的项目引用"""
    if not item or not isinstance(item, dict):
        return item
    
    new_item = dict(item)
    if "name" in item:
        orig_name = item["name"]
        new_item["name"] = translate_name(orig_name)
        new_item["name_en"] = orig_name
    return new_item


def translate_capacity(cap):
    """翻译载重能力，将 lb. 转换为 磅"""
    if not cap or not isinstance(cap, str):
        return cap
    # 替换 lb. 为 磅
    return cap.replace(" lb.", "磅").replace("lb.", "磅")


def translate_desc(desc_list):
    """
    翻译描述数组
    注意：由于描述内容较长且复杂，这里保留英文原样，只添加 desc_en 字段
    实际翻译需要人工完成或使用更高级的翻译方法
    """
    if not desc_list or not isinstance(desc_list, list):
        return desc_list, None
    
    # 暂时保留英文描述，添加 desc_en
    # 对于复杂的描述文本，建议后续人工翻译
    return desc_list, desc_list.copy()


def translate_equipment(item):
    """翻译单个装备条目"""
    if not item or not isinstance(item, dict):
        return item
    
    new_item = dict(item)
    
    # 1. 翻译 name
    if "name" in item:
        orig_name = item["name"]
        new_item["name"] = translate_name(orig_name)
        new_item["name_en"] = orig_name
    
    # 2. 翻译 equipment_category
    if "equipment_category" in item:
        new_item["equipment_category"] = translate_equipment_category(item["equipment_category"])
    
    # 3. 翻译 gear_category (用于冒险装备)
    if "gear_category" in item:
        new_item["gear_category"] = translate_equipment_category(item["gear_category"])
    
    # 4. 翻译武器特有字段
    if "weapon_category" in item:
        new_item["weapon_category"] = WEAPON_CATEGORIES.get(item["weapon_category"], item["weapon_category"])
    
    if "weapon_range" in item:
        new_item["weapon_range"] = WEAPON_RANGES.get(item["weapon_range"], item["weapon_range"])
    
    if "category_range" in item:
        cr = item["category_range"]
        new_item["category_range"] = CATEGORY_RANGES.get(cr, cr)
    
    # 5. 翻译护甲特有字段
    if "armor_category" in item:
        new_item["armor_category"] = ARMOR_CATEGORIES.get(item["armor_category"], item["armor_category"])
    
    # 6. 翻译工具特有字段
    if "tool_category" in item:
        new_item["tool_category"] = TOOL_CATEGORIES.get(item["tool_category"], item["tool_category"])
    
    # 7. 翻译载具特有字段
    if "vehicle_category" in item:
        new_item["vehicle_category"] = VEHICLE_CATEGORIES.get(item["vehicle_category"], item["vehicle_category"])
    
    # 8. 翻译 cost.unit
    if "cost" in item and isinstance(item["cost"], dict):
        cost = dict(item["cost"])
        if "unit" in cost:
            cost["unit"] = translate_cost_unit(cost["unit"])
        new_item["cost"] = cost
    
    # 9. 翻译 speed.unit
    if "speed" in item and isinstance(item["speed"], dict):
        speed = dict(item["speed"])
        if "unit" in speed:
            orig_unit = speed["unit"]
            speed["unit"] = SPEED_UNITS.get(orig_unit, orig_unit)
        new_item["speed"] = speed
    
    # 10. 翻译 capacity
    if "capacity" in item:
        new_item["capacity"] = translate_capacity(item["capacity"])
    
    # 11. 翻译 damage.damage_type
    if "damage" in item and isinstance(item["damage"], dict):
        damage = dict(item["damage"])
        if "damage_type" in damage:
            damage["damage_type"] = translate_damage_type(damage["damage_type"])
        new_item["damage"] = damage
    
    # 12. 翻译 two_handed_damage.damage_type
    if "two_handed_damage" in item and isinstance(item["two_handed_damage"], dict):
        thd = dict(item["two_handed_damage"])
        if "damage_type" in thd:
            thd["damage_type"] = translate_damage_type(thd["damage_type"])
        new_item["two_handed_damage"] = thd
    
    # 13. 翻译 properties 数组
    if "properties" in item and isinstance(item["properties"], list):
        new_item["properties"] = [translate_property(p) for p in item["properties"]]
    
    # 14. 翻译 contents 数组（装备包内容物）
    if "contents" in item and isinstance(item["contents"], list):
        new_contents = []
        for content in item["contents"]:
            new_content = dict(content)
            if "item" in content:
                new_content["item"] = translate_item(content["item"])
            new_contents.append(new_content)
        new_item["contents"] = new_contents
    
    # 15. 翻译 desc 数组
    if "desc" in item and isinstance(item["desc"], list):
        desc_en = item["desc"].copy()
        # 描述暂时保留英文，添加 desc_en 备份
        # 实际翻译工作量大，需要人工处理或使用翻译API
        new_item["desc_en"] = desc_en
    
    # 16. 翻译 special 数组（武器特殊描述，如 Net 和 Lance）
    if "special" in item and isinstance(item["special"], list):
        # 暂时保留英文
        new_item["special_en"] = item["special"].copy()
    
    return new_item


def count_by_category(equipment):
    """按分类统计装备数量（使用 name_en 字段）"""
    stats = {
        "武器": 0,
        "护甲": 0,
        "冒险装备": 0,
        "工具": 0,
        "坐骑与载具": 0,
        "其他": 0,
    }
    
    for item in equipment:
        # 优先使用 name_en 字段进行分类统计
        cat_obj = item.get("equipment_category", {})
        cat = cat_obj.get("name_en", cat_obj.get("name", ""))
        
        if cat == "Weapon":
            stats["武器"] += 1
        elif cat == "Armor":
            stats["护甲"] += 1
        elif cat == "Adventuring Gear":
            stats["冒险装备"] += 1
        elif cat == "Tools":
            stats["工具"] += 1
        elif cat == "Mounts and Vehicles":
            stats["坐骑与载具"] += 1
        else:
            stats["其他"] += 1
    
    return stats


def main():
    # 读取源文件
    with open("src/2014/5e-SRD-Equipment.json", "r", encoding="utf-8") as f:
        equipment = json.load(f)
    
    print(f"读取到 {len(equipment)} 件装备")
    
    # 统计原始数据
    original_stats = count_by_category(equipment)
    print("\n原始分类统计：")
    for cat, count in original_stats.items():
        if count > 0:
            print(f"  {cat}: {count} 件")
    
    # 翻译所有装备
    translated = [translate_equipment(item) for item in equipment]
    
    # 统计翻译后数据
    translated_stats = count_by_category(translated)
    print("\n翻译后分类统计：")
    for cat, count in translated_stats.items():
        if count > 0:
            print(f"  {cat}: {count} 件")
    
    # 写入输出文件
    output_path = "src/2014-zh/5e-SRD-Equipment.json"
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(translated, f, ensure_ascii=False, indent=2)
    
    print(f"\n翻译完成！输出文件：{output_path}")
    
    # 计算文件大小
    import os
    file_size = os.path.getsize(output_path)
    print(f"文件大小：{file_size / 1024:.1f} KB")


if __name__ == "__main__":
    main()
