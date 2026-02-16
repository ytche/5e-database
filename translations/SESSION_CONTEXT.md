# 对话上下文记忆文件

> 创建时间：2026-02-16
> 
> 用途：每次新对话开始时，由用户或 AI 加载此文件以恢复上下文

---

## 🎯 项目目标

将 D&D 5e SRD (2014版) 完整翻译成中文，保持 API 兼容性（index/url 不翻译）。

---

## ✅ 必须遵守的要求

### 1. Git 提交规范
- **必须使用中文提交信息**（已在 COMMIT_GUIDELINE.md 中定义）
- 类型：(zh)、(glossary)、(workflow)、(review)

### 2. 翻译格式规范
- `index` - 永不翻译
- `url` - 永不翻译  
- `name` - 翻译为中文，添加 `name_en` 保留英文
- `desc` - 翻译为中文，添加 `desc_en` 保留英文

### 3. 工作流程
- 遵循 translations/WORKFLOW.md 定义的 6 阶段流程
- 每文件翻译后更新 GLOSSARY.md
- 生成审查报告到 translations/review/

### 4. 术语一致性
- 优先使用 GLOSSARY.md 中定义的术语
- 新术语必须先确认再使用
- 参考 5E 不全书 (https://5echm.kagangtuya.top/)

---

## 📁 重要文件位置

| 文件 | 用途 |
|-----|------|
| `translations/WORKFLOW.md` | 翻译工作流程 V2.1 |
| `translations/GLOSSARY.md` | 完整术语表（快速参考+详细章节）|
| `translations/COMMIT_GUIDELINE.md` | Git 提交规范 |
| `translations/PROGRESS.md` | 翻译进度追踪（本文档下方）|
| `translations/review/*.review.md` | 各文件审查报告 |

---

## 📊 当前项目状态

见 `translations/PROGRESS.md`

---

## 💡 下次对话启动建议

用户可以说：
- "加载上下文，继续翻译" → 读取 PROGRESS.md 找到下一个待翻译文件
- "翻译 [文件名]" → 直接开始指定文件的翻译流程
- "更新术语表" → 检查 GLOSSARY.md 是否需要补充

---

*本文件由 AI 在每次对话结束后更新*
