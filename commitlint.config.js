module.exports = {
  extends: ['@commitlint/config-conventional'],
  rules: {
    'type-enum': [
      2,
      'always',
      [
        'feat', // 新功能
        'fix', // Bug 修复
        'docs', // 文档更新
        'style', // 代码格式调整
        'refactor', // 代码重构
        'perf', // 性能优化
        'test', // 测试相关
        'chore', // 构建/工具/依赖更新
        'data', // 数据更新/修正
        'i18n', // 国际化/翻译更新
      ],
    ],
    'scope-enum': [
      0, // 0 = disabled, 改为 1 或 2 启用
      'always',
      [
        'api', // API 相关
        'data', // 数据文件
        'ui', // 用户界面
        'db', // 数据库脚本
        'search', // 搜索功能
        'spell', // 法术相关
        'monster', // 怪物相关
        'i18n', // 国际化
        'config', // 配置文件
        'deps', // 依赖更新
      ],
    ],
    'subject-full-stop': [0, 'never'],
    'subject-case': [0, 'never'],
  },
};
