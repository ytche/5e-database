# D&D 5e 中文版数据查询应用 - 技术架构设计

> 版本: v1.0  
> 日期: 2026-02-25  
> 作者: 技术架构师

---

## 目录

1. [整体架构图](#1-整体架构图)
2. [前端技术选型](#2-前端技术选型)
3. [后端技术选型](#3-后端技术选型)
4. [部署架构](#4-部署架构)
5. [数据流设计](#5-数据流设计)
6. [代码目录结构](#6-代码目录结构)
7. [实施路线图](#7-实施路线图)

---

## 1. 整体架构图

### 1.1 分层架构设计

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                              客户端层 (Client Layer)                         │
│  ┌───────────────────────────────────────────────────────────────────────┐  │
│  │  Web 浏览器 / 移动端 / 桌面端                                           │  │
│  │  - React SPA / PWA                                                     │  │
│  │  - 响应式设计 (Desktop + Mobile)                                        │  │
│  └───────────────────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────────────────┘
                                      │
                                      ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                          CDN / 边缘缓存层 (Edge Layer)                       │
│  ┌───────────────────────────────────────────────────────────────────────┐  │
│  │  CloudFlare / Vercel Edge / 阿里云 CDN                                │  │
│  │  - 静态资源缓存                                                        │  │
│  │  - API 响应缓存 (TTL: 1h)                                              │  │
│  │  - DDoS 防护                                                          │  │
│  └───────────────────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────────────────┘
                                      │
                                      ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                         前端应用层 (Frontend Layer)                          │
│  ┌───────────────────────────────────────────────────────────────────────┐  │
│  │  React 18 + TypeScript SPA                                             │  │
│  │  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐  │  │
│  │  │   路由层    │  │  状态管理   │  │  UI 组件库  │  │  数据获取   │  │  │
│  │  │  React Router│  │   Zustand   │  │  Ant Design │  │ TanStack    │  │  │
│  │  │    v6      │  │             │  │    v5       │  │   Query     │  │  │
│  │  └─────────────┘  └─────────────┘  └─────────────┘  └─────────────┘  │  │
│  └───────────────────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────────────────┘
                                      │
                                      ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                     API 网关层 (API Gateway Layer) - 可选                   │
│  ┌───────────────────────────────────────────────────────────────────────┐  │
│  │  Kong / Nginx / AWS API Gateway                                       │  │
│  │  - 限流 (Rate Limiting): 100 req/min                                  │  │
│  │  - 认证 (JWT/OAuth2)                                                  │  │
│  │  - 日志与监控                                                          │  │
│  └───────────────────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────────────────┘
                                      │
                                      ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                     BFF 层 (Backend for Frontend) - 可选                   │
│  ┌───────────────────────────────────────────────────────────────────────┐  │
│  │  是否需要 BFF？                                                        │  │
│  │                                                                        │  │
│  │  ✅ 推荐场景:                                                          │  │
│  │     - 需要聚合多个微服务的数据                                          │  │
│  │     - 需要为不同客户端定制 API (Web/Mobile)                             │  │
│  │     - 需要复杂的业务逻辑处理                                            │  │
│  │                                                                        │  │
│  │  ❌ 当前建议: 初期不需要 BFF                                            │  │
│  │     - 数据来源单一 (MongoDB)                                            │  │
│  │     - API 相对简单，直接调用即可                                         │  │
│  │     - 可直接扩展现有 5e-srd-api                                         │  │
│  │                                                                        │  │
│  │  💡 未来演进: 当需要以下功能时考虑添加 BFF                              │  │
│  │     - 用户系统 (收藏、历史记录)                                         │  │
│  │     - 多数据源整合 (规则 + 用户数据)                                     │  │
│  │     - 移动端专用 API 优化                                               │  │
│  └───────────────────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────────────────┘
                                      │
                                      ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                       后端服务层 (Backend Layer)                             │
│  ┌───────────────────────────────────────────────────────────────────────┐  │
│  │  5e-srd-api (Node.js + Express + TypeScript)                          │  │
│  │                                                                        │  │
│  │  ┌─────────────────────────────────────────────────────────────────┐  │  │
│  │  │  RESTful API Endpoints                                           │  │  │
│  │  │  - /api/2014/*    - 2014 版规则 (中文)                           │  │  │
│  │  │  - /api/2024/*    - 2024 版规则                                 │  │  │
│  │  │  - /api/search    - 全文搜索                                     │  │  │
│  │  │  - /api/graphql   - GraphQL 端点 (可选)                          │  │  │
│  │  └─────────────────────────────────────────────────────────────────┘  │  │
│  │                                                                        │  │
│  │  ┌─────────────────────────────────────────────────────────────────┐  │  │
│  │  │  中间件栈                                                        │  │  │
│  │  │  - CORS / Helmet (安全)                                          │  │  │
│  │  │  - Compression (gzip/brotli)                                     │  │  │
│  │  │  - Rate Limiter                                                  │  │  │
│  │  │  - Request Logger                                                │  │  │
│  │  │  - Error Handler                                                 │  │  │
│  │  └─────────────────────────────────────────────────────────────────┘  │  │
│  └───────────────────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────────────────┘
                                      │
                                      ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                        缓存层 (Cache Layer)                                  │
│  ┌─────────────────────┐    ┌─────────────────────┐    ┌─────────────────┐  │
│  │     Redis           │    │  In-Memory Cache    │    │   MongoDB       │  │
│  │  - 查询结果缓存      │    │  (Node.js)          │    │   Query Cache   │  │
│  │  - 热点数据缓存      │    │  - LRU Cache        │    │  - 聚合管道缓存  │  │
│  │  - Session 存储      │    │  - TTL: 5min        │    │  - 索引优化      │  │
│  │  - TTL: 1h          │    │                     │    │                 │  │
│  └─────────────────────┘    └─────────────────────┘    └─────────────────┘  │
└─────────────────────────────────────────────────────────────────────────────┘
                                      │
                                      ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                        数据层 (Data Layer)                                   │
│  ┌───────────────────────────────────────────────────────────────────────┐  │
│  │  MongoDB (本地/容器化/云托管)                                          │  │
│  │                                                                        │  │
│  │  Collections:                                                          │  │
│  │  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────────┐   │  │
│  │  │  2014-spells    │  │  2014-classes   │  │  2014-monsters      │   │  │
│  │  │  2014-equipment │  │  2014-features  │  │  2014-ability-scores│   │  │
│  │  │  2014-races     │  │  2014-skills    │  │  ...                │   │  │
│  │  └─────────────────┘  └─────────────────┘  └─────────────────────┘   │  │
│  │                                                                        │  │
│  │  Indexes:                                                              │  │
│  │  - index (唯一)                                                        │  │
│  │  - name (文本搜索)                                                     │  │
│  │  - level (法术等级)                                                    │  │
│  │  - classes.index (职业关联)                                            │  │
│  └───────────────────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────────────────┘
```

### 1.2 架构决策说明

| 决策项 | 选择 | 理由 |
|--------|------|------|
| BFF 层 | ❌ 初期不需要 | 数据来源单一，API 简单，可直接使用现有 5e-srd-api |
| CDN | ✅ 推荐 | 加速静态资源，缓存 API 响应，提高全球访问速度 |
| API Gateway | ⚠️ 可选 | 初期可直接使用 Nginx，业务增长后考虑 Kong |
| GraphQL | ⚠️ 可选 | RESTful API 已满足需求，GraphQL 可作为未来扩展 |

---

## 2. 前端技术选型

### 2.1 技术栈概览

```
┌─────────────────────────────────────────────────────────────────┐
│                      前端技术栈选择                               │
├─────────────────────────────────────────────────────────────────┤
│  框架: React 18 + TypeScript 5.x                                │
│  构建: Vite 5.x                                                 │
│  路由: React Router v6                                          │
│  状态: Zustand + TanStack Query (React Query)                   │
│  UI库: Ant Design 5.x + Tailwind CSS                            │
│  图标: Lucide React                                             │
│  测试: Vitest + React Testing Library                           │
│  代码: ESLint + Prettier + Husky                                │
└─────────────────────────────────────────────────────────────────┘
```

### 2.2 详细选型对比

#### 2.2.1 框架选择: React vs Vue vs 其他

| 框架 | 优点 | 缺点 | 推荐度 |
|------|------|------|--------|
| **React** | 生态丰富、TypeScript 支持好、社区活跃、灵活 | 学习曲线较陡 | ⭐⭐⭐⭐⭐ |
| Vue 3 | 上手快、模板语法直观、性能好 | 大型项目生态不如 React | ⭐⭐⭐⭐ |
| Svelte | 编译时优化、包体积小 | 生态较小、招聘难 | ⭐⭐⭐ |
| Next.js | SSR/SSG 支持、SEO 友好 | 对于纯数据查询应用可能过度 | ⭐⭐⭐⭐ |

**决策: React 18 + Vite (SPA)**
- 理由: D&D 查询应用主要是数据展示，不需要 SSR
- Vite 构建速度远超 CRA，开发体验好
- 未来如需 SEO 可迁移到 Next.js

#### 2.2.2 状态管理: Zustand vs Redux vs Context

| 方案 | 优点 | 缺点 | 适用场景 |
|------|------|------|----------|
| **Zustand** | 极简 API、无样板代码、TypeScript 友好、体积小(1KB) | 生态不如 Redux | ⭐⭐⭐⭐⭐ 推荐 |
| Redux Toolkit | 成熟、生态丰富、调试工具强 | 样板代码多、学习成本高 | 超大型应用 |
| Jotai/Recoil | 原子化状态、细粒度更新 | 较新、生态待完善 | 复杂状态依赖 |
| Context | 内置、无需额外库 | 性能问题、不适合高频更新 | 主题/语言等低频状态 |

**决策: Zustand + TanStack Query**
- Zustand: 管理客户端状态 (UI 状态、用户偏好)
- TanStack Query: 管理服务端状态 (API 数据、缓存、去重)

```typescript
// store/uiStore.ts - Zustand 示例
import { create } from 'zustand';
import { persist } from 'zustand/middleware';

interface UIState {
  sidebarCollapsed: boolean;
  theme: 'light' | 'dark';
  recentSearches: string[];
  setSidebarCollapsed: (collapsed: boolean) => void;
  setTheme: (theme: 'light' | 'dark') => void;
  addRecentSearch: (query: string) => void;
}

export const useUIStore = create<UIState>()(
  persist(
    (set) => ({
      sidebarCollapsed: false,
      theme: 'light',
      recentSearches: [],
      setSidebarCollapsed: (collapsed) => set({ sidebarCollapsed: collapsed }),
      setTheme: (theme) => set({ theme }),
      addRecentSearch: (query) =>
        set((state) => ({
          recentSearches: [query, ...state.recentSearches.slice(0, 9)],
        })),
    }),
    { name: 'dnd-ui-storage' }
  )
);
```

#### 2.2.3 数据获取: TanStack Query vs SWR vs Axios

| 方案 | 优点 | 缺点 | 推荐度 |
|------|------|------|--------|
| **TanStack Query** | 强大的缓存、自动重试、乐观更新、TypeScript 支持 | 包体积稍大 | ⭐⭐⭐⭐⭐ |
| SWR | 轻量、Vercel 出品、功能足够 | 功能不如 TanStack Query 丰富 | ⭐⭐⭐⭐ |
| Axios + Context | 灵活、可定制 | 需要手动处理缓存、加载、错误 | ⭐⭐⭐ |

**决策: TanStack Query (React Query) v5**

```typescript
// hooks/useSpells.ts - TanStack Query 示例
import { useQuery, useInfiniteQuery } from '@tanstack/react-query';
import { api } from '@/lib/api';

const STALE_TIME = 1000 * 60 * 60; // 1 hour - D&D 数据很少变化

export function useSpells(filters?: SpellFilters) {
  return useQuery({
    queryKey: ['spells', filters],
    queryFn: () => api.spells.list(filters),
    staleTime: STALE_TIME,
  });
}

export function useSpell(index: string) {
  return useQuery({
    queryKey: ['spell', index],
    queryFn: () => api.spells.get(index),
    staleTime: STALE_TIME,
  });
}

export function useSearchSpells(query: string) {
  return useQuery({
    queryKey: ['spells', 'search', query],
    queryFn: () => api.spells.search(query),
    enabled: query.length >= 2, // 至少 2 个字符才搜索
    staleTime: STALE_TIME,
  });
}
```

#### 2.2.4 UI 组件库: Ant Design vs Material-UI vs Tailwind

| 方案 | 优点 | 缺点 | 推荐度 |
|------|------|------|--------|
| **Ant Design 5** | 组件丰富、企业级设计、中文文档好、主题定制灵活 | 包体积较大 | ⭐⭐⭐⭐⭐ |
| Material-UI | 设计规范、生态丰富 | 默认风格不适合 D&D 主题 | ⭐⭐⭐⭐ |
| Tailwind + Headless | 完全定制、体积小 | 需要自行组装组件 | ⭐⭐⭐⭐ |
| Chakra UI | 简洁、易定制 | 组件数量不如 AntD | ⭐⭐⭐⭐ |

**决策: Ant Design 5 + Tailwind CSS**
- Ant Design: 提供完整的基础组件 (Table、Form、Modal 等)
- Tailwind CSS: 用于自定义样式、D&D 主题定制
- 使用 Ant Design 的 ConfigProvider 进行主题定制

```typescript
// theme/index.ts
import { ThemeConfig } from 'antd';

export const dndTheme: ThemeConfig = {
  token: {
    colorPrimary: '#8B0000', // D&D 深红色
    colorInfo: '#1e3a5f',    // 深蓝
    borderRadius: 6,
    fontFamily: '"Noto Sans SC", -apple-system, sans-serif',
  },
  components: {
    Card: {
      headerBg: '#f5f5f5',
    },
    Table: {
      headerBg: '#fafafa',
      rowHoverBg: '#f0f0f0',
    },
  },
};
```

### 2.3 前端项目结构

```
frontend/
├── public/                      # 静态资源
│   ├── favicon.ico
│   └── manifest.json
├── src/
│   ├── api/                     # API 客户端
│   │   ├── client.ts            # axios/fetch 配置
│   │   ├── spells.ts            # 法术相关 API
│   │   ├── classes.ts           # 职业相关 API
│   │   ├── equipment.ts         # 装备相关 API
│   │   └── types.ts             # API 类型定义
│   │
│   ├── components/              # 组件
│   │   ├── common/              # 通用组件
│   │   │   ├── AppHeader.tsx
│   │   │   ├── AppSidebar.tsx
│   │   │   ├── SearchBox.tsx
│   │   │   └── Loading.tsx
│   │   ├── spells/              # 法术相关组件
│   │   │   ├── SpellList.tsx
│   │   │   ├── SpellCard.tsx
│   │   │   └── SpellDetail.tsx
│   │   ├── classes/             # 职业相关组件
│   │   └── equipment/           # 装备相关组件
│   │
│   ├── hooks/                   # 自定义 Hooks
│   │   ├── useSpells.ts         # TanStack Query hooks
│   │   ├── useClasses.ts
│   │   ├── useSearch.ts
│   │   └── useDebounce.ts
│   │
│   ├── pages/                   # 页面组件
│   │   ├── HomePage.tsx
│   │   ├── SpellsPage.tsx
│   │   ├── SpellDetailPage.tsx
│   │   ├── ClassesPage.tsx
│   │   ├── EquipmentPage.tsx
│   │   └── SearchPage.tsx
│   │
│   ├── stores/                  # Zustand 状态
│   │   ├── uiStore.ts
│   │   ├── searchStore.ts
│   │   └── userStore.ts
│   │
│   ├── utils/                   # 工具函数
│   │   ├── formatters.ts
│   │   ├── constants.ts
│   │   └── helpers.ts
│   │
│   ├── styles/                  # 样式
│   │   ├── globals.css
│   │   └── variables.less
│   │
│   ├── types/                   # 全局类型
│   │   └── index.ts
│   │
│   ├── App.tsx
│   ├── main.tsx
│   └── router.tsx               # React Router 配置
│
├── tests/                       # 测试文件
├── index.html
├── vite.config.ts
├── tsconfig.json
├── tailwind.config.js
└── package.json
```

---

## 3. 后端技术选型

### 3.1 技术栈概览

```
┌─────────────────────────────────────────────────────────────────┐
│                      后端技术栈选择                               │
├─────────────────────────────────────────────────────────────────┤
│  运行时: Node.js 22 LTS                                         │
│  框架: Express.js 4.x / Fastify (可选)                          │
│  语言: TypeScript 5.x                                           │
│  数据库: MongoDB 7.x                                            │
│  缓存: Redis 7.x                                                │
│  ODM: Mongoose 8.x                                              │
│  验证: Zod / Joi                                                │
│  测试: Vitest + Supertest                                       │
│  文档: Swagger/OpenAPI 3.0                                      │
└─────────────────────────────────────────────────────────────────┘
```

### 3.2 是否继续使用现有 5e-srd-api？

**决策: 基于现有 5e-srd-api 扩展 ✅**

理由：
1. 现有 API 已经成熟稳定，提供了完整的 D&D 数据接口
2. 本项目数据结构与 5e-srd-api 兼容
3. 只需添加中文支持和新功能，无需重写

**需要做的修改：**

```typescript
// 扩展现有 API 以支持中文数据

// 1. 修改路由以支持版本和语言
// GET /api/2014/spells - 中文法术 (默认)
// GET /api/2014/spells?lang=en - 英文法术
// GET /api/2024/spells - 2024 版规则

// 2. 添加搜索端点
// GET /api/search?q=火球术&types=spells,classes

// 3. 添加聚合端点
// GET /api/2014/spells/by-level
// GET /api/2014/spells/by-school
```

### 3.3 是否需要 GraphQL？

**决策: 初期不需要，但预留扩展接口 ⚠️**

理由：
- RESTful API 已满足当前需求
- 数据关系相对简单，不需要复杂的查询嵌套
- 团队熟悉 REST，开发和维护成本低

**未来考虑 GraphQL 的场景：**
- 需要高度灵活的数据查询
- 移动端需要精确控制返回字段
- 需要聚合多个数据源

```typescript
// 预留 GraphQL 扩展 (可选)
// 使用 Apollo Server + TypeGraphQL

import { buildSchema } from 'type-graphql';
import { SpellResolver } from './resolvers/SpellResolver';

const schema = await buildSchema({
  resolvers: [SpellResolver],
  emitSchemaFile: true,
});
```

### 3.4 缓存策略 (Redis)

#### 3.4.1 多层缓存架构

```
┌─────────────────────────────────────────────────────────────┐
│                     缓存策略设计                              │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  L1: 客户端缓存 (TanStack Query)                             │
│  ├── staleTime: 1 hour (D&D 数据很少变化)                    │
│  ├── cacheTime: 24 hours                                     │
│  └── 离线支持: 可选                                           │
│                                                              │
│  L2: CDN 缓存 (CloudFlare/Vercel)                            │
│  ├── 静态资源: 1 year (immutable)                            │
│  ├── API 响应: 1 hour                                        │
│  └── Cache-Control: public, max-age=3600                     │
│                                                              │
│  L3: Redis 缓存                                              │
│  ├── 查询结果缓存: TTL 1 hour                                │
│  ├── 热点数据: TTL 24 hours                                  │
│  ├── 搜索建议: TTL 15 minutes                                │
│  └── Session 数据: TTL 7 days                                │
│                                                              │
│  L4: 应用内存缓存 (Node.js)                                  │
│  ├── 配置数据: LRU Cache, max 100 items                      │
│  └── 元数据: TTL 5 minutes                                   │
│                                                              │
│  L5: MongoDB 缓存                                            │
│  ├── 查询计划缓存: 自动                                      │
│  └── WiredTiger 缓存: 内存的 50%                             │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

#### 3.4.2 Redis 缓存实现

```typescript
// utils/cache.ts
import Redis from 'ioredis';

const redis = new Redis({
  host: process.env.REDIS_HOST || 'localhost',
  port: parseInt(process.env.REDIS_PORT || '6379'),
  password: process.env.REDIS_PASSWORD,
  db: 0,
});

export class Cache {
  private static readonly DEFAULT_TTL = 3600; // 1 hour

  static async get<T>(key: string): Promise<T | null> {
    const data = await redis.get(key);
    return data ? JSON.parse(data) : null;
  }

  static async set(key: string, value: any, ttl: number = this.DEFAULT_TTL): Promise<void> {
    await redis.setex(key, ttl, JSON.stringify(value));
  }

  static async del(key: string): Promise<void> {
    await redis.del(key);
  }

  static async delPattern(pattern: string): Promise<void> {
    const keys = await redis.keys(pattern);
    if (keys.length > 0) {
      await redis.del(...keys);
    }
  }

  // 生成缓存 key
  static generateKey(prefix: string, params: Record<string, any>): string {
    const sortedParams = Object.keys(params)
      .sort()
      .map((k) => `${k}:${params[k]}`)
      .join('|');
    return `${prefix}:${sortedParams}`;
  }
}

// 缓存装饰器
export function Cacheable(prefix: string, ttl: number = 3600) {
  return function (target: any, propertyKey: string, descriptor: PropertyDescriptor) {
    const originalMethod = descriptor.value;
    descriptor.value = async function (...args: any[]) {
      const cacheKey = Cache.generateKey(prefix, args[0] || {});
      const cached = await Cache.get(cacheKey);
      if (cached) return cached;
      const result = await originalMethod.apply(this, args);
      await Cache.set(cacheKey, result, ttl);
      return result;
    };
  };
}
```

### 3.5 API 设计规范

```typescript
// 统一的 API 响应格式
interface ApiResponse<T> {
  success: boolean;
  data: T;
  meta?: {
    total: number;
    page: number;
    perPage: number;
    totalPages: number;
  };
  error?: {
    code: string;
    message: string;
    details?: any;
  };
}

// 错误码定义
enum ErrorCode {
  NOT_FOUND = 'NOT_FOUND',
  VALIDATION_ERROR = 'VALIDATION_ERROR',
  RATE_LIMITED = 'RATE_LIMITED',
  INTERNAL_ERROR = 'INTERNAL_ERROR',
}

// RESTful 端点设计
/*
GET    /api/2014/spells              # 法术列表 (支持分页、筛选)
GET    /api/2014/spells/:index       # 法术详情
GET    /api/2014/spells/by-level/:level  # 按等级查询
GET    /api/2014/spells/by-school/:school  # 按学派查询

GET    /api/2014/classes             # 职业列表
GET    /api/2014/classes/:index      # 职业详情
GET    /api/2014/classes/:index/levels   # 职业等级信息
GET    /api/2014/classes/:index/spells   # 职业法术列表

GET    /api/2014/equipment           # 装备列表
GET    /api/2014/equipment/:index    # 装备详情

GET    /api/search?q=:query&types=:types  # 全局搜索

GET    /api/2014/metadata            # 元数据 (用于筛选器)
*/
```

### 3.6 后端项目结构

```
backend/
├── src/
│   ├── config/                  # 配置
│   │   ├── database.ts          # MongoDB 连接
│   │   ├── redis.ts             # Redis 连接
│   │   └── env.ts               # 环境变量验证
│   │
│   ├── models/                  # Mongoose 模型
│   │   ├── Spell.ts
│   │   ├── Class.ts
│   │   ├── Equipment.ts
│   │   └── index.ts
│   │
│   ├── controllers/             # 控制器
│   │   ├── spellController.ts
│   │   ├── classController.ts
│   │   ├── equipmentController.ts
│   │   └── searchController.ts
│   │
│   ├── routes/                  # 路由
│   │   ├── spells.ts
│   │   ├── classes.ts
│   │   ├── equipment.ts
│   │   ├── search.ts
│   │   └── index.ts
│   │
│   ├── middlewares/             # 中间件
│   │   ├── errorHandler.ts
│   │   ├── rateLimiter.ts
│   │   ├── cacheMiddleware.ts
│   │   └── validator.ts
│   │
│   ├── services/                # 业务逻辑
│   │   ├── spellService.ts
│   │   ├── cacheService.ts
│   │   └── searchService.ts
│   │
│   ├── utils/                   # 工具函数
│   │   ├── logger.ts
│   │   ├── cache.ts
│   │   └── helpers.ts
│   │
│   ├── types/                   # 类型定义
│   │   └── index.ts
│   │
│   ├── app.ts                   # Express 应用配置
│   └── server.ts                # 入口文件
│
├── tests/                       # 测试
├── docker-compose.yml
├── Dockerfile
├── package.json
└── tsconfig.json
```

---

## 4. 部署架构

### 4.1 开发环境

```yaml
# docker-compose.dev.yml
version: '3.8'

services:
  # MongoDB 数据库
  mongodb:
    image: mongo:7
    container_name: dnd-mongodb-dev
    ports:
      - '27017:27017'
    volumes:
      - mongodb_data:/data/db
      - ./scripts/init-mongo.js:/docker-entrypoint-initdb.d/init-mongo.js
    environment:
      MONGO_INITDB_DATABASE: dnd_5e_zh

  # Redis 缓存
  redis:
    image: redis:7-alpine
    container_name: dnd-redis-dev
    ports:
      - '6379:6379'
    volumes:
      - redis_data:/data

  # 后端 API
  backend:
    build:
      context: ./backend
      dockerfile: Dockerfile.dev
    container_name: dnd-backend-dev
    ports:
      - '3001:3001'
    environment:
      NODE_ENV: development
      MONGODB_URI: mongodb://mongodb:27017/dnd_5e_zh
      REDIS_URL: redis://redis:6379
    volumes:
      - ./backend:/app
      - /app/node_modules
    depends_on:
      - mongodb
      - redis
    command: npm run dev

  # 前端开发服务器
  frontend:
    build:
      context: ./frontend
      dockerfile: Dockerfile.dev
    container_name: dnd-frontend-dev
    ports:
      - '5173:5173'
    environment:
      VITE_API_URL: http://localhost:3001
    volumes:
      - ./frontend:/app
      - /app/node_modules
    depends_on:
      - backend
    command: npm run dev

volumes:
  mongodb_data:
  redis_data:
```

### 4.2 生产环境架构

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                         生产环境部署架构                                     │
└─────────────────────────────────────────────────────────────────────────────┘

                              用户请求
                                 │
                                 ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│  CDN (CloudFlare / 阿里云 CDN)                                              │
│  ├── 静态资源缓存 (dnd-zh.com)                                              │
│  ├── API 缓存 (api.dnd-zh.com)                                              │
│  └── DDoS 防护 + WAF                                                        │
└─────────────────────────────────────────────────────────────────────────────┘
                                 │
                                 ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│  负载均衡器 (Nginx / AWS ALB / 阿里云 SLB)                                   │
│  ├── SSL 终端                                                                │
│  ├── 请求分发                                                                │
│  └── 健康检查                                                                │
└─────────────────────────────────────────────────────────────────────────────┘
                                 │
            ┌────────────────────┴────────────────────┐
            ▼                                         ▼
┌─────────────────────────────┐       ┌─────────────────────────────┐
│   前端服务器 (Vercel/        │       │   后端服务器集群             │
│    Netlify/阿里云 OSS)       │       │   (Docker Swarm / K8s)       │
│                             │       │                             │
│  ┌───────────────────────┐  │       │  ┌─────────┐  ┌─────────┐  │
│  │  静态网站 (React SPA)  │  │       │  │ API-1   │  │ API-2   │  │
│  │  - 预渲染              │  │       │  │ Node.js │  │ Node.js │  │
│  │  - Service Worker      │  │       │  └─────────┘  └─────────┘  │
│  └───────────────────────┘  │       │                             │
│                             │       │  ┌─────────┐  ┌─────────┐  │
└─────────────────────────────┘       │  │ API-3   │  │ API-N   │  │
                                      │  │ Node.js │  │ Node.js │  │
                                      │  └─────────┘  └─────────┘  │
                                      │                             │
                                      └──────────┬──────────────────┘
                                                 │
                    ┌────────────────────────────┼────────────────────────────┐
                    ▼                            ▼                            ▼
          ┌─────────────────┐         ┌─────────────────┐         ┌──────────────┐
          │   MongoDB       │         │     Redis       │         │  监控/日志    │
          │   Replica Set   │         │   Cluster       │         │              │
          │                 │         │                 │         │  Prometheus  │
          │  Primary        │         │  - 主缓存        │         │  Grafana     │
          │  Secondary x2   │         │  - Session      │         │  ELK Stack   │
          │  Arbiter        │         │  - 热点数据      │         │              │
          └─────────────────┘         └─────────────────┘         └──────────────┘
```

### 4.3 Docker Compose 生产配置

```yaml
# docker-compose.prod.yml
version: '3.8'

services:
  nginx:
    image: nginx:alpine
    container_name: dnd-nginx
    ports:
      - '80:80'
      - '443:443'
    volumes:
      - ./nginx/nginx.conf:/etc/nginx/nginx.conf
      - ./nginx/ssl:/etc/nginx/ssl
      - frontend_dist:/usr/share/nginx/html
    depends_on:
      - backend
    restart: unless-stopped

  backend:
    build:
      context: ./backend
      dockerfile: Dockerfile
    environment:
      NODE_ENV: production
      MONGODB_URI: ${MONGODB_URI}
      REDIS_URL: ${REDIS_URL}
      PORT: 3001
    deploy:
      replicas: 3
      resources:
        limits:
          cpus: '0.5'
          memory: 512M
    depends_on:
      - mongodb
      - redis
    restart: unless-stopped

  mongodb:
    image: mongo:7
    container_name: dnd-mongodb
    command: ['--replSet', 'rs0', '--bind_ip_all']
    volumes:
      - mongodb_data:/data/db
    environment:
      MONGO_INITDB_ROOT_USERNAME: ${MONGO_ROOT_USER}
      MONGO_INITDB_ROOT_PASSWORD: ${MONGO_ROOT_PASS}
    restart: unless-stopped

  redis:
    image: redis:7-alpine
    container_name: dnd-redis
    command: redis-server --appendonly yes
    volumes:
      - redis_data:/data
    restart: unless-stopped

  # 可选: 监控
  prometheus:
    image: prom/prometheus
    volumes:
      - ./monitoring/prometheus.yml:/etc/prometheus/prometheus.yml
    ports:
      - '9090:9090'

  grafana:
    image: grafana/grafana
    ports:
      - '3000:3000'
    volumes:
      - grafana_data:/var/lib/grafana

volumes:
  mongodb_data:
  redis_data:
  grafana_data:
  frontend_dist:
```

### 4.4 部署平台推荐

| 环境 | 推荐方案 | 成本估算 | 备注 |
|------|----------|----------|------|
| **开发** | Docker Compose (本地) | 免费 | 完整本地开发环境 |
| **测试** | Vercel (前端) + Railway/Render (后端) | $0-20/月 | 快速部署，自动 CI/CD |
| **生产** | 阿里云/腾讯云 ECS + MongoDB Atlas | $50-200/月 | 国内访问速度快 |
| **生产** | AWS/GCP + MongoDB Atlas | $100-300/月 | 国际访问，生态丰富 |

---

## 5. 数据流设计

### 5.1 前端数据消费流程

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                        前端数据消费架构                                      │
└─────────────────────────────────────────────────────────────────────────────┘

用户操作 (点击/搜索/筛选)
    │
    ▼
┌─────────────────────────────────────────────────────────────────────────┐
│ 1. 组件层 (Component)                                                    │
│    - 收集用户输入                                                        │
│    - 调用 Hooks                                                          │
│    - 展示加载/错误状态                                                    │
└─────────────────────────────────────────────────────────────────────────┘
    │
    ▼
┌─────────────────────────────────────────────────────────────────────────┐
│ 2. Hooks 层 (TanStack Query)                                             │
│    - 检查缓存 (staleTime)                                                │
│    ├── 命中缓存 ──▶ 直接返回数据                                          │
│    └── 缓存过期 ──▶ 发起 API 请求                                         │
│         - isLoading: true                                                │
│         - 去重相同请求                                                    │
│         - 自动重试 (失败时)                                               │
└─────────────────────────────────────────────────────────────────────────┘
    │
    ▼
┌─────────────────────────────────────────────────────────────────────────┐
│ 3. API 客户端层                                                          │
│    - Axios/Fetch 配置                                                    │
│    - 请求拦截: 添加 Token、日志                                          │
│    - 响应拦截: 错误处理、数据转换                                         │
└─────────────────────────────────────────────────────────────────────────┘
    │
    ▼
┌─────────────────────────────────────────────────────────────────────────┐
│ 4. 状态更新                                                              │
│    - TanStack Query 自动更新缓存                                         │
│    - 触发组件重新渲染                                                     │
│    - 乐观更新 (可选)                                                      │
└─────────────────────────────────────────────────────────────────────────┘
    │
    ▼
┌─────────────────────────────────────────────────────────────────────────┐
│ 5. UI 渲染                                                               │
│    - 展示数据                                                             │
│    - 错误边界处理                                                         │
│    - 加载骨架屏                                                          │
└─────────────────────────────────────────────────────────────────────────┘
```

### 5.2 错误处理策略

```typescript
// hooks/useApi.ts - 统一的错误处理
import { useQuery, useMutation, QueryClient } from '@tanstack/react-query';
import { message } from 'antd';

const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      retry: (failureCount, error: any) => {
        // 不重试 4xx 错误
        if (error?.response?.status >= 400 && error?.response?.status < 500) {
          return false;
        }
        return failureCount < 3;
      },
      retryDelay: (attemptIndex) => Math.min(1000 * 2 ** attemptIndex, 30000),
      onError: (error: any) => {
        // 全局错误提示
        const errorMessage = error?.response?.data?.error?.message || '请求失败';
        message.error(errorMessage);
      },
    },
    mutations: {
      onError: (error: any) => {
        message.error(error?.response?.data?.error?.message || '操作失败');
      },
    },
  },
});

// 组件中使用
function SpellList() {
  const { data, isLoading, error, refetch } = useSpells();

  if (isLoading) return <Skeleton active />;
  
  if (error) {
    return (
      <ErrorFallback 
        error={error} 
        retry={refetch}
        message="加载法术列表失败，请检查网络连接"
      />
    );
  }

  return <SpellTable data={data} />;
}
```

### 5.3 搜索/筛选实现方案

#### 方案 1: 前端筛选 (适合数据量小)

```typescript
// 适用于少于 1000 条数据的列表
function useFilteredSpells(spells: Spell[], filters: SpellFilters) {
  return useMemo(() => {
    return spells.filter((spell) => {
      // 等级筛选
      if (filters.level !== undefined && spell.level !== filters.level) {
        return false;
      }
      // 学派筛选
      if (filters.school && spell.school.index !== filters.school) {
        return false;
      }
      // 职业筛选
      if (filters.class && !spell.classes.some(c => c.index === filters.class)) {
        return false;
      }
      // 搜索文本
      if (filters.query) {
        const query = filters.query.toLowerCase();
        const matchName = spell.name.toLowerCase().includes(query);
        const matchDesc = spell.desc.some(d => d.toLowerCase().includes(query));
        if (!matchName && !matchDesc) return false;
      }
      return true;
    });
  }, [spells, filters]);
}
```

#### 方案 2: 后端筛选 (推荐 ✅)

```typescript
// 适用于大数据量，支持分页
// GET /api/2014/spells?level=3&school=evocation&class=wizard&page=1

// backend/controllers/spellController.ts
export const getSpells = async (req: Request, res: Response) => {
  const { level, school, class: className, query, page = 1, limit = 20 } = req.query;
  
  const filter: any = {};
  
  if (level !== undefined) filter.level = parseInt(level as string);
  if (school) filter['school.index'] = school;
  if (className) filter['classes.index'] = className;
  if (query) {
    filter.$or = [
      { name: { $regex: query, $options: 'i' } },
      { desc: { $regex: query, $options: 'i' } },
    ];
  }

  const skip = (parseInt(page as string) - 1) * parseInt(limit as string);
  
  const [spells, total] = await Promise.all([
    Spell.find(filter)
      .skip(skip)
      .limit(parseInt(limit as string))
      .lean(),
    Spell.countDocuments(filter),
  ]);

  res.json({
    success: true,
    data: spells,
    meta: {
      total,
      page: parseInt(page as string),
      perPage: parseInt(limit as string),
      totalPages: Math.ceil(total / parseInt(limit as string)),
    },
  });
};
```

#### 方案 3: 全文搜索 (Elasticsearch / MongoDB Text Search)

```typescript
// MongoDB Text Search 方案
// 需要先创建索引: db.spells.createIndex({ name: "text", desc: "text" })

export const searchSpells = async (req: Request, res: Response) => {
  const { q } = req.query;
  
  if (!q || (q as string).length < 2) {
    return res.json({ success: true, data: [] });
  }

  const spells = await Spell.find(
    { $text: { $search: q as string } },
    { score: { $meta: 'textScore' } }
  )
    .sort({ score: { $meta: 'textScore' } })
    .limit(20)
    .lean();

  res.json({ success: true, data: spells });
};
```

### 5.4 数据流时序图

```
用户搜索"火球术"
    │
    ▼
┌─────────────────────────────────────────────────────────────────────┐
│ SearchBox 组件                                                      │
│ - 输入: "火球术"                                                   │
│ - 使用 useDebounce(300ms)                                          │
└─────────────────────────────────────────────────────────────────────┘
    │
    ▼ (debounced query: "火球术")
┌─────────────────────────────────────────────────────────────────────┐
│ useSearchSpells("火球术")                                          │
│ - 检查缓存: cache.get(['search', '火球术'])                        │
│ - 缓存未命中                                                         │
└─────────────────────────────────────────────────────────────────────┘
    │
    ▼
┌─────────────────────────────────────────────────────────────────────┐
│ api.spells.search("火球术")                                        │
│ GET /api/search?q=火球术&types=spells                              │
└─────────────────────────────────────────────────────────────────────┘
    │
    ▼
┌─────────────────────────────────────────────────────────────────────┐
│ Nginx (CDN 检查缓存)                                                │
│ - Cache Miss                                                        │
└─────────────────────────────────────────────────────────────────────┘
    │
    ▼
┌─────────────────────────────────────────────────────────────────────┐
│ Backend API                                                         │
│ 1. 检查 Redis Cache                                                │
│    - Key: search:火球术:spells                                     │
│    - Cache Miss                                                     │
│ 2. 查询 MongoDB                                                    │
│    - db.spells.find({ $text: { $search: "火球术" } })              │
│ 3. 写入 Redis (TTL: 1h)                                            │
│ 4. 返回结果                                                         │
└─────────────────────────────────────────────────────────────────────┘
    │
    ▼
┌─────────────────────────────────────────────────────────────────────┐
│ 前端处理                                                            │
│ 1. TanStack Query 缓存结果                                          │
│ 2. 更新 UI                                                          │
│ 3. 展示搜索结果列表                                                  │
└─────────────────────────────────────────────────────────────────────┘
```

---

## 6. 代码目录结构

### 6.1 完整项目结构

```
dnd-5e-zh-app/                          # 项目根目录
├── README.md
├── ARCHITECTURE.md                     # 本架构文档
├── docker-compose.yml                  # 开发环境编排
├── docker-compose.prod.yml             # 生产环境编排
├── Makefile                            # 常用命令
│
├── frontend/                           # 前端应用
│   ├── README.md
│   ├── package.json
│   ├── vite.config.ts
│   ├── tsconfig.json
│   ├── tailwind.config.js
│   ├── index.html
│   │
│   ├── public/
│   │   ├── favicon.ico
│   │   └── manifest.json
│   │
│   └── src/
│       ├── api/
│       │   ├── client.ts
│       │   ├── spells.ts
│       │   ├── classes.ts
│       │   ├── equipment.ts
│       │   └── types.ts
│       │
│       ├── components/
│       │   ├── common/
│       │   │   ├── AppHeader.tsx
│       │   │   ├── AppSidebar.tsx
│       │   │   ├── AppFooter.tsx
│       │   │   ├── SearchBox.tsx
│       │   │   ├── FilterPanel.tsx
│       │   │   ├── Loading.tsx
│       │   │   ├── ErrorBoundary.tsx
│       │   │   └── Pagination.tsx
│       │   │
│       │   ├── spells/
│       │   │   ├── SpellCard.tsx
│       │   │   ├── SpellList.tsx
│       │   │   ├── SpellDetail.tsx
│       │   │   ├── SpellFilters.tsx
│       │   │   └── SpellTable.tsx
│       │   │
│       │   ├── classes/
│       │   │   ├── ClassCard.tsx
│       │   │   ├── ClassDetail.tsx
│       │   │   └── ClassFeatures.tsx
│       │   │
│       │   └── equipment/
│       │       ├── EquipmentCard.tsx
│       │       └── EquipmentDetail.tsx
│       │
│       ├── hooks/
│       │   ├── useSpells.ts
│       │   ├── useClasses.ts
│       │   ├── useEquipment.ts
│       │   ├── useSearch.ts
│       │   └── useDebounce.ts
│       │
│       ├── pages/
│       │   ├── HomePage.tsx
│       │   ├── SpellsPage.tsx
│       │   ├── SpellDetailPage.tsx
│       │   ├── ClassesPage.tsx
│       │   ├── ClassDetailPage.tsx
│       │   ├── EquipmentPage.tsx
│       │   ├── SearchPage.tsx
│       │   └── NotFoundPage.tsx
│       │
│       ├── stores/
│       │   ├── uiStore.ts
│       │   ├── searchStore.ts
│       │   └── userStore.ts
│       │
│       ├── utils/
│       │   ├── constants.ts
│       │   ├── formatters.ts
│       │   └── helpers.ts
│       │
│       ├── styles/
│       │   ├── globals.css
│       │   └── variables.less
│       │
│       ├── types/
│       │   └── index.ts
│       │
│       ├── App.tsx
│       ├── main.tsx
│       └── router.tsx
│
├── backend/                            # 后端 API
│   ├── README.md
│   ├── package.json
│   ├── tsconfig.json
│   ├── Dockerfile
│   ├── Dockerfile.dev
│   │
│   └── src/
│       ├── config/
│       │   ├── database.ts
│       │   ├── redis.ts
│       │   └── env.ts
│       │
│       ├── models/
│       │   ├── Spell.ts
│       │   ├── Class.ts
│       │   ├── Equipment.ts
│       │   ├── Feature.ts
│       │   └── index.ts
│       │
│       ├── controllers/
│       │   ├── spellController.ts
│       │   ├── classController.ts
│       │   ├── equipmentController.ts
│       │   └── searchController.ts
│       │
│       ├── routes/
│       │   ├── index.ts
│       │   ├── spells.ts
│       │   ├── classes.ts
│       │   ├── equipment.ts
│       │   └── search.ts
│       │
│       ├── middlewares/
│       │   ├── errorHandler.ts
│       │   ├── rateLimiter.ts
│       │   ├── cacheMiddleware.ts
│       │   ├── validator.ts
│       │   └── logger.ts
│       │
│       ├── services/
│       │   ├── spellService.ts
│       │   ├── cacheService.ts
│       │   └── searchService.ts
│       │
│       ├── utils/
│       │   ├── logger.ts
│       │   ├── cache.ts
│       │   └── helpers.ts
│       │
│       ├── types/
│       │   └── index.ts
│       │
│       ├── app.ts
│       └── server.ts
│
├── database/                           # 数据库 (当前项目)
│   ├── src/
│   │   ├── 2014-zh/                    # 2014 版中文数据
│   │   ├── 2014-final/                 # 最终合并数据
│   │   └── 2024/                       # 2024 版规则
│   ├── scripts/
│   │   ├── dbRefresh.ts
│   │   └── dbUtils.ts
│   └── package.json
│
├── nginx/                              # Nginx 配置
│   ├── nginx.conf
│   ├── nginx.dev.conf
│   └── ssl/
│       ├── dnd-zh.com.crt
│       └── dnd-zh.com.key
│
├── monitoring/                         # 监控配置
│   ├── prometheus.yml
│   ├── grafana-dashboard.json
│   └── alert-rules.yml
│
└── docs/                               # 文档
    ├── api/
    │   └── openapi.yaml
    ├── deployment/
    │   ├── setup.md
    │   └── troubleshooting.md
    └── development/
        ├── frontend-guide.md
        └── backend-guide.md
```

---

## 7. 实施路线图

### 7.1 阶段划分

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                         项目实施路线图                                       │
└─────────────────────────────────────────────────────────────────────────────┘

Phase 1: MVP (4-6 周)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
✅ 基础架构搭建
   - Docker Compose 开发环境
   - 前端项目初始化 (React + Vite + AntD)
   - 后端 API  fork/扩展 5e-srd-api
   
✅ 核心功能
   - 法术列表展示 (分页、基础筛选)
   - 法术详情页
   - 全文搜索 (基础)
   
✅ 数据
   - 导入中文法术数据到 MongoDB
   - 创建必要索引

Phase 2: 功能完善 (4 周)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📋 扩展功能
   - 职业、装备数据展示
   - 高级筛选 (多维度)
   - 搜索联想/自动完成
   
📋 用户体验
   - 响应式设计优化
   - 加载状态优化
   - 错误处理完善
   
📋 性能优化
   - Redis 缓存实现
   - CDN 配置
   - 图片/资源优化

Phase 3: 生产就绪 (3-4 周)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📋 部署
   - 生产环境配置
   - CI/CD 流水线
   - 监控告警
   
📋 安全
   - HTTPS 配置
   - 限流/防刷
   - 安全头部
   
📋 文档
   - API 文档 (Swagger)
   - 用户手册
   - 运维手册

Phase 4: 扩展功能 (可选)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
💡 进阶功能
   - 用户系统 (收藏、历史)
   - 角色构建器
   - 法术卡生成器
   - 数据导出 (PDF)
   
💡 多平台
   - PWA 支持
   - 小程序
   - 移动端 App
```

### 7.2 技术债务管理

| 优先级 | 项目 | 说明 |
|--------|------|------|
| P0 | 单元测试覆盖 | 核心功能至少 70% 覆盖率 |
| P0 | 错误监控 | 接入 Sentry 或类似服务 |
| P1 | 性能监控 | 接入 APM 工具 |
| P1 | 自动化测试 | E2E 测试 (Playwright) |
| P2 | GraphQL | 当 API 复杂度增长时考虑 |
| P2 | 微服务拆分 | 当用户量增长时考虑 |

---

## 附录

### A. 推荐学习资源

- [React 18 官方文档](https://react.dev/)
- [TanStack Query 文档](https://tanstack.com/query/latest)
- [Zustand 文档](https://docs.pmnd.rs/zustand)
- [Ant Design 5.0](https://ant.design/)
- [MongoDB 索引最佳实践](https://docs.mongodb.com/manual/indexes/)
- [Redis 缓存模式](https://redis.io/docs/manual/patterns/)

### B. 性能基准

| 指标 | 目标值 | 说明 |
|------|--------|------|
| 首屏加载 | < 2s | Lighthouse Performance > 90 |
| API 响应 | < 200ms | P95 响应时间 |
| 搜索响应 | < 500ms | 包含网络延迟 |
| 缓存命中率 | > 80% | Redis + CDN |

---

**文档结束**

如有任何问题或需要调整，请随时提出。
