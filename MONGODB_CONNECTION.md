# MongoDB 连接信息与 API 访问指南

> ⚠️ **注意**: 此文件包含本地数据库连接信息，不要提交到 Git！

---

## 🚀 API 服务已启动

**API 地址**: http://localhost:3000

### 基础端点

| 端点 | 描述 |
|------|------|
| `GET /api/2014` | 查看所有可用资源列表 |
| `GET /api/2014/classes` | 获取所有职业 |
| `GET /api/2014/spells` | 获取所有法术 |
| `GET /api/2014/monsters` | 获取所有怪物 |

---

## 📊 数据语言状态

| 数据类型 | 语言 | 示例 |
|---------|------|------|
| **职业 (Classes)** | ✅ 中文 | 野蛮人、法师、牧师... |
| **法术 (Spells)** | ✅ 中文 | 火球术、祈愿术、法术反制... |
| **特性 (Features)** | ✅ 中文 | 狂暴、法术位... |
| **魔法物品 (Magic Items)** | ✅ 中文 | 各种魔法装备... |
| **装备 (Equipment)** | ✅ 中文 | 武器、护甲、物品... |
| **种族 (Races)** | ✅ 中文 | 人类、精灵、矮人... |
| **怪物 (Monsters)** | 🇬🇧 英文 | Adult Red Dragon... |

---

## 🧪 API 测试示例

```bash
# 1. 查看 API 根目录
curl http://localhost:3000/api/2014

# 2. 获取中文职业数据
curl http://localhost:3000/api/2014/classes/barbarian

# 3. 获取中文法术数据
curl http://localhost:3000/api/2014/spells/fireball

# 4. 获取英文怪物数据
curl http://localhost:3000/api/2014/monsters/adult-red-dragon

# 5. 获取所有法术列表
curl http://localhost:3000/api/2014/spells

# 6. 获取特定等级法术
curl "http://localhost:3000/api/2014/spells?level=3"
```

---

## 🗄️ MongoDB 连接信息

### 连接地址
```
mongodb://localhost:27017/5e-database
```

### 常用命令

#### 连接数据库
```bash
mongosh mongodb://localhost/5e-database
```

#### 查看集合列表
```bash
mongosh mongodb://localhost/5e-database --eval "db.getCollectionNames()"
```

#### 查看特定集合数据量
```bash
mongosh mongodb://localhost/5e-database --eval "db['2014-spells'].countDocuments()"
```

---

## 📁 数据库集合

| 集合名 | 内容 | 语言 | 数量 |
|--------|------|------|------|
| `2014-classes` | 12个职业 | 中文 | 12 |
| `2014-spells` | 法术 | 中文 | 319 |
| `2014-features` | 特性 | 中文 | 407 |
| `2014-magic-items` | 魔法物品 | 中文 | 362 |
| `2014-monsters` | 怪物 | **英文** | 334 |
| `2014-races` | 种族 | 中文 | 9 |
| `2014-equipment` | 装备 | 中文 | 237 |
| `2014-*` | 其他数据 | 中文 | ... |
| `2024-*` | 2024版数据 | 英文 | ... |

---

## 🛠️ 服务控制

### MongoDB
```bash
# 启动
brew services start mongodb/brew/mongodb-community

# 停止
brew services stop mongodb/brew/mongodb-community

# 重启
brew services restart mongodb/brew/mongodb-community

# 查看状态
brew services list | grep mongodb
```

### Redis
```bash
# 启动
brew services start redis

# 停止
brew services stop redis

# 查看状态
brew services list | grep redis
```

### API 服务
```bash
# 重新加载数据库（如有更新）
cd /Users/chezi/code/java/5e-database
MONGODB_URI=mongodb://localhost/5e-database npm run db:refresh

# 重启 API 服务
cd /Users/chezi/code/java/5e-srd-api
npm run start
```

---

## 📂 项目文件结构

```
/Users/chezi/code/java/
├── 5e-database/          # 数据库项目
│   ├── src/2014/         # 英文源数据
│   ├── src/2014-zh/      # 中文翻译数据
│   ├── src/2014-final/   # 合并数据（中文+英文怪物）
│   └── MONGODB_CONNECTION.md  # 本文档
│
└── 5e-srd-api/           # API 服务项目
    ├── src/              # 源代码
    └── dist/             # 编译输出
```

---

## ⚠️ 注意事项

1. **不要提交本文档到 Git** - 已添加到 `.gitignore`
2. **确保 MongoDB 和 Redis 运行** - API 依赖这两个服务
3. **怪物数据保持英文** - 未翻译，其他数据已汉化
4. **API 默认端口 3000** - 如需修改请检查环境变量

---

*生成时间: 2026-02-25*
*版本: 5e-database + 5e-srd-api 中文适配*
