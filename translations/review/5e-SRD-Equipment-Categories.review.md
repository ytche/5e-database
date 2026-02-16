# 5e-SRD-Equipment-Categories 翻译审查报告

## 审查统计
- 审查时间：2026-02-16T19:06:29+08:00
- 审查条目总数：983
- 问题数量：12

## 问题列表

### 1. [严重-翻译缺失] Ioun Stone of Sustenance
- 位置：wondrous-items / 艾恩石
- 问题描述：`sustenance` 未翻译，且中文值前有多余空格
- 当前值：" sustenance艾恩石"
- 建议修正：" sustenance艾恩石" → "辟谷艾恩石" 或 "维系艾恩石"

### 2. [术语不一致] Padded Armor
- 位置：armor / light-armor
- 问题描述：Padded Armor 当前译为"软甲"，与术语表中的"布甲"不一致
- 当前值："软甲"
- 建议修正："软甲" → "布甲"

### 3. [术语不一致] Tinderbox
- 位置：adventuring-gear / standard-gear
- 问题描述：Tinderbox 当前译为"火绒盒"，与术语表中的"打火盒"不一致
- 当前值："火绒盒"
- 建议修正："火绒盒" → "打火盒"

### 4. [术语不一致] Bedroll
- 位置：adventuring-gear / standard-gear
- 问题描述：Bedroll 当前译为"铺盖卷"，与术语表中的"睡袋"不一致
- 当前值："铺盖卷"
- 建议修正："铺盖卷" → "睡袋"

### 5. [术语不一致] Rations
- 位置：adventuring-gear / standard-gear
- 问题描述：Rations 当前译为"口粮"，与术语表中的"干粮"不一致
- 当前值："口粮（1天）"
- 建议修正："口粮" → "干粮"

### 6. [术语不一致] Pike
- 位置：weapon / martial-weapons
- 问题描述：Pike 当前译为"长矛"，但 Spear 也译为"矛"，两者容易混淆。按照D&D惯例，Pike应译为"长枪"
- 当前值："长矛"
- 建议修正："长矛" → "长枪"

### 7. [数据问题] 重复条目 - Hourglass
- 位置：standard-gear
- 问题描述：Hourglass（沙漏）条目在 standard-gear 中重复出现两次（第3110行和第3134行）
- 建议修正：删除重复条目

### 8. [数据问题] 重复条目 - Hunting Trap
- 位置：standard-gear
- 问题描述：Hunting Trap（狩猎陷阱）条目在 standard-gear 中重复出现两次（第3115行和第3140行）
- 建议修正：删除重复条目

### 9. [数据问题] 重复条目 - Ink
- 位置：standard-gear
- 问题描述：Ink（墨水）和 Ink Pen（钢笔）条目在 standard-gear 中重复出现两次（第3121行和第3146行）
- 建议修正：删除重复条目

### 10. [数据问题] 重复条目 - mounts-and-vehicles
- 位置：mounts-and-vehicles
- 问题描述：马铠（barding）和载具条目在该分类中完全重复了一遍（第1680-1828行与第1830-1978行）
- 建议修正：删除第1830-1978行的重复条目

### 11. [翻译建议] Giant Slayer
- 位置：weapon（魔法武器）
- 问题描述：当前译为"巨人杀"，略显生硬
- 当前值："巨人杀"
- 建议修正："巨人杀" → "巨人杀手" 或 "巨人斩杀者"

### 12. [翻译建议] Shield of Missile Attraction
- 位置：armor（魔法护甲）
- 问题描述：当前译为"导弹吸引盾"，"导弹"一词在现代语境中有特定含义
- 当前值："导弹吸引盾"
- 建议修正："导弹吸引盾" → "飞弹吸引盾"

## 修正建议汇总（JSON Patch 格式）

```json
[
  {
    "path": "$[4].equipment[?(@.index=='ioun-stone-of-sustenance')].name",
    "current": " sustenance艾恩石",
    "suggested": "辟谷艾恩石"
  },
  {
    "path": "$[1].equipment[?(@.index=='padded-armor')].name",
    "current": "软甲",
    "suggested": "布甲"
  },
  {
    "path": "$[14].equipment[?(@.index=='padded-armor')].name",
    "current": "软甲",
    "suggested": "布甲"
  },
  {
    "path": "$[2].equipment[?(@.index=='tinderbox')].name",
    "current": "火绒盒",
    "suggested": "打火盒"
  },
  {
    "path": "$[13].equipment[?(@.index=='tinderbox')].name",
    "current": "火绒盒",
    "suggested": "打火盒"
  },
  {
    "path": "$[2].equipment[?(@.index=='bedroll')].name",
    "current": "铺盖卷",
    "suggested": "睡袋"
  },
  {
    "path": "$[13].equipment[?(@.index=='bedroll')].name",
    "current": "铺盖卷",
    "suggested": "睡袋"
  },
  {
    "path": "$[2].equipment[?(@.index=='rations-1-day')].name",
    "current": "口粮（1天）",
    "suggested": "干粮（1天）"
  },
  {
    "path": "$[13].equipment[?(@.index=='rations-1-day')].name",
    "current": "口粮（1天）",
    "suggested": "干粮（1天）"
  },
  {
    "path": "$[0].equipment[?(@.index=='pike')].name",
    "current": "长矛",
    "suggested": "长枪"
  },
  {
    "path": "$[3].equipment[?(@.index=='pike')].name",
    "current": "长矛",
    "suggested": "长枪"
  },
  {
    "path": "$[6].equipment[?(@.index=='pike')].name",
    "current": "长矛",
    "suggested": "长枪"
  },
  {
    "path": "$[8].equipment[?(@.index=='pike')].name",
    "current": "长矛",
    "suggested": "长枪"
  },
  {
    "path": "$[0].equipment[?(@.index=='giant-slayer')].name",
    "current": "巨人杀",
    "suggested": "巨人杀手"
  },
  {
    "path": "$[1].equipment[?(@.index=='shield-of-missile-attraction')].name",
    "current": "导弹吸引盾",
    "suggested": "飞弹吸引盾"
  }
]
```

## 术语表贡献

列出本次翻译中出现的新术语建议添加到 GLOSSARY.md：

| 英文 | 中文 | 类别 | 备注 |
|------|------|------|------|
| Berserker Axe | 狂战士战斧 | 魔法武器 | - |
| Dancing Sword | 舞剑 | 魔法武器 | - |
| Defender | 守卫者 | 魔法武器 | - |
| Dragon Slayer | 屠龙剑 | 魔法武器 | - |
| Dwarven Thrower | 矮人飞锤 | 魔法武器 | - |
| Flame Tongue | 焰舌 | 魔法武器 | - |
| Frost Brand | 霜铭 | 魔法武器 | - |
| Giant Slayer | 巨人杀手 | 魔法武器 | 建议统一译名 |
| Hammer of Thunderbolts | 雷霆之锤 | 魔法武器 | - |
| Holy Avenger | 神圣复仇者 | 魔法武器 | - |
| Javelin of Lightning | 闪电标枪 | 魔法武器 | - |
| Luck Blade | 幸运剑 | 魔法武器 | - |
| Mace of Disruption | 破敌硬头锤 | 魔法武器 | - |
| Mace of Smiting | 重击硬头锤 | 魔法武器 | - |
| Mace of Terror | 恐惧硬头锤 | 魔法武器 | - |
| Nine Lives Stealer | 九命夺魂剑 | 魔法武器 | - |
| Oathbow | 誓约弓 | 魔法武器 | - |
| Scimitar of Speed | 疾速弯刀 | 魔法武器 | - |
| Sun Blade | 日刃 | 魔法武器 | - |
| Sword of Life Stealing | 生命偷取剑 | 魔法武器 | - |
| Sword of Sharpness | 锐利之剑 | 魔法武器 | - |
| Sword of Wounding | 创伤剑 | 魔法武器 | - |
| Trident of Fish Command | 控鱼三叉戟 | 魔法武器 | - |
| Vicious Weapon | 凶恶武器 | 魔法武器 | - |
| Vorpal Sword | 斩首剑 | 魔法武器 | - |
| Adamantine Armor | 精金护甲 | 魔法护甲 | - |
| Animated Shield | 活化盾 | 魔法护甲 | - |
| Armor of Invulnerability | 无敌护甲 | 魔法护甲 | - |
| Armor of Resistance | 抗性护甲 | 魔法护甲 | - |
| Armor of Vulnerability | 弱点护甲 | 魔法护甲 | - |
| Arrow-Catching Shield | 捕箭盾 | 魔法护甲 | - |
| Demon Armor | 恶魔护甲 | 魔法护甲 | - |
| Dragon Scale Mail | 龙鳞甲 | 魔法护甲 | - |
| Dwarven Plate | 矮人板甲 | 魔法护甲 | - |
| Elven Chain | 精灵链甲 | 魔法护甲 | - |
| Glamoured Studded Leather | 魅惑镶钉皮甲 | 魔法护甲 | - |
| Mithral Armor | 秘银护甲 | 魔法护甲 | - |
| Plate Armor of Etherealness | 空灵板甲 | 魔法护甲 | - |
| Shield of Missile Attraction | 飞弹吸引盾 | 魔法护甲 | 建议修正 |
| Spellguard Shield | 法术守护盾 | 魔法护甲 | - |
| Ioun Stone | 艾恩石 | 奇物 | - |
| Bag of Holding | 次元袋 | 奇物 | - |
| Deck of Many Things | 万法牌组 | 奇物 | - |
| Figurine of Wondrous Power | 奇力塑像 | 奇物 | - |
| Portable Hole | 便携洞 | 奇物 | - |
| Sovereign Glue | 万能胶 | 奇物 | - |
| Universal Solvent | 万能溶剂 | 奇物 | - |
| Well of Many Worlds | 万界之井 | 奇物 | - |

---

## 审查总结

### 总体评价
本次翻译整体质量较高，绝大多数装备名称翻译准确，格式规范，遵循了 `name` + `name_en` 的双语格式。

### 主要问题分类
1. **翻译缺失**：1处（Ioun Stone of Sustenance）
2. **术语不一致**：5处（与提供的术语表对照）
3. **数据重复**：4处（标准装备和坐骑载具分类中的重复条目）
4. **翻译建议**：2处（ Giant Slayer、Shield of Missile Attraction）

### 建议优先级
- **高优先级**：修复翻译缺失问题（#1）
- **中优先级**：统一术语一致性（#2-#6）
- **低优先级**：清理重复数据（#7-#10）、优化翻译（#11-#12）

### 数据完整性检查
- 所有 `name` 字段都已翻译：✓
- 所有条目都包含 `name_en` 字段：✓
- JSON 格式正确：✓
