# 开发快速指南

> 新成员必读：如何快速开始参与本项目

## 快速开始

```bash
# 1. 克隆仓库
git clone https://github.com/5e-bits/5e-database.git
cd 5e-database

# 2. 安装依赖（Node.js 22.x 必需）
npm install

# 3. 验证环境
npm run validate
```

## 常用命令

### 代码质量

```bash
# 代码检查
npm run lint              # 运行 ESLint
npm run lint:fix          # 自动修复 ESLint 问题
npm run format            # 运行 Prettier 格式化
npm run format:check      # 检查代码格式

# 类型检查
npm run typecheck         # TypeScript 类型检查
```

### 测试

```bash
# 运行测试
npm test                  # 运行所有测试
npm run test:watch        # 监视模式运行测试
npm run test:ui           # 打开 Vitest UI
npm run coverage          # 生成覆盖率报告
```

### 数据库操作

```bash
# 构建 TypeScript 脚本
npm run build:ts

# 刷新数据库（完整重建）
npm run db:refresh

# 更新数据库（增量更新）
npm run db:update
```

### 完整验证

```bash
npm run validate          # 运行 lint + typecheck + test
```

## Git 工作流

### 1. 创建功能分支

```bash
# 从 main 分支创建
 git checkout main
 git pull origin main
 
 # 创建功能分支（示例）
 git checkout -b feature/spell-search
 # 或
 git checkout -b fix/typo-in-fireball
 # 或
 git checkout -b translate/monsters-core
```

### 2. 提交代码

```bash
# 添加更改
git add .

# 提交（遵循 Conventional Commits）
git commit -m "feat(spell): add spell level filter"
# 或
git commit -m "fix(data): correct fireball damage dice"
# 或
git commit -m "i18n(monster): translate core monsters to Chinese"
```

### 3. 推送并创建 PR

```bash
# 推送到远程
git push -u origin feature/spell-search

# 然后到 GitHub 创建 Pull Request
```

## 项目结构

```
5e-database/
├── src/                      # 数据文件
│   ├── 2014/                 # 英文源数据（2014版规则）
│   ├── 2014-zh/              # 中文翻译数据
│   ├── 2014-final/           # 合并后的最终数据
│   ├── 2024/                 # 2024版规则数据
│   └── */tests/              # 数据测试
├── scripts/                  # TypeScript 脚本
│   ├── *.ts                  # 脚本源文件
│   ├── built/                # 编译后的脚本
│   └── tsconfig.json         # TypeScript 配置
├── translations/             # 翻译相关文件
├── docker/                   # Docker 配置
├── .github/                  # GitHub 配置
│   ├── workflows/            # CI/CD 工作流
│   ├── ISSUE_TEMPLATE/       # Issue 模板
│   ├── pull_request_template.md
│   ├── CODE_REVIEW_CHECKLIST.md
│   └── TERMINOLOGY.md        # 术语翻译表
├── CODE_STANDARDS.md         # 代码规范（完整版）
├── DEVELOPMENT_GUIDE.md      # 本文件
├── eslint.config.mjs         # ESLint 配置
├── .prettierrc               # Prettier 配置
├── vitest.config.ts          # Vitest 配置
└── package.json
```

## 代码规范速查

### 命名规范

| 类型 | 格式 | 示例 |
|-----|------|------|
| 变量/函数 | camelCase | `getSpellById`, `userName` |
| 类/接口 | PascalCase | `SpellService`, `CharacterData` |
| 常量 | UPPER_SNAKE_CASE | `MAX_LEVEL`, `API_BASE_URL` |
| 文件 | kebab-case | `spell-service.ts` |
| 分支 | 类型/描述 | `feature/spell-search` |

### Commit 类型

| 类型 | 用途 |
|-----|------|
| `feat` | 新功能 |
| `fix` | Bug 修复 |
| `data` | 数据更新 |
| `i18n` | 翻译更新 |
| `docs` | 文档更新 |
| `refactor` | 代码重构 |
| `test` | 测试相关 |
| `chore` | 构建/工具 |

## 数据文件规范

### JSON 结构示例

```json
{
  "index": "fireball",
  "name": "火球术",
  "name_en": "Fireball",
  "level": 3,
  "school": {
    "index": "evocation",
    "name": "塑能",
    "name_en": "Evocation",
    "url": "/api/2014/magic-schools/evocation"
  },
  "url": "/api/2014/spells/fireball"
}
```

### 关键规则

1. **index**: 唯一标识，小写，短横线分隔
2. **name**: 中文名称
3. **name_en**: 英文原名
4. **url**: 格式 `/api/{version}/{resource}/{index}`

## 常见问题

### Q: 如何添加新的法术翻译？

A:
1. 在 `src/2014-zh/` 找到对应文件
2. 参考 `src/2014/` 中的英文源数据
3. 保持相同的 JSON 结构
4. 添加 `name`（中文）和保留 `name_en`（英文）
5. 运行 `npm test` 验证数据完整性

### Q: 测试失败了怎么办？

A:
1. 查看错误信息：`npm test -- --reporter=verbose`
2. 检查 JSON 格式是否合法
3. 确认索引是否唯一
4. 验证 URL 引用是否正确

### Q: 如何更新数据库？

A:
```bash
# 确保 MongoDB 已运行
export MONGODB_URI=mongodb://localhost/5e-database

# 刷新数据库
npm run db:refresh
```

### Q: 提交信息被拒绝了怎么办？

A:
确保遵循 Conventional Commits 格式：
```
<type>(<scope>): <subject>

示例：
feat(spell): add spell search by level
fix(data): correct monster HP calculation
docs: update API documentation
```

## 资源链接

- [完整代码规范](./CODE_STANDARDS.md)
- [代码审查清单](./.github/CODE_REVIEW_CHECKLIST.md)
- [术语翻译表](./.github/TERMINOLOGY.md)
- [Conventional Commits](https://www.conventionalcommits.org/)
- [D&D 5e SRD](https://dnd.wizards.com/resources/systems-reference-document)

## 获取帮助

- 查看 [Issues](https://github.com/5e-bits/5e-database/issues)
- 加入 [Discord](https://discord.gg/TQuYTv7) 讨论
- 阅读 [完整规范](./CODE_STANDARDS.md)

---

**欢迎贡献！** 🎉
