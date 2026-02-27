// @ts-check

import eslint from '@eslint/js';
import tseslint from 'typescript-eslint';
import eslintPluginVitest from 'eslint-plugin-vitest';
import eslintPluginPrettier from 'eslint-plugin-prettier/recommended';
import json from 'eslint-plugin-json';
import globals from 'globals';

export default [
  {
    name: 'base',
    ignores: ['**/node_modules/**', '**/dist/**', '**/built/**', '**/coverage/**'],
  },
  // JavaScript 配置
  {
    name: 'js/recommended',
    files: ['**/*.js'],
    languageOptions: {
      globals: {
        ...globals.node,
      },
    },
    rules: {
      ...eslint.configs.recommended.rules,
      'no-unused-vars': ['warn', { argsIgnorePattern: '^_' }],
      'no-undef': 'warn',
      'no-console': ['warn', { allow: ['error', 'warn', 'info'] }],
      'prefer-const': 'error',
      'no-var': 'error',
    },
  },
  // TypeScript 配置
  ...tseslint.configs.recommended.map((config) => ({
    ...config,
    files: ['**/*.ts', '**/*.tsx'],
  })),
  {
    name: 'ts/strict',
    files: ['**/*.ts', '**/*.tsx'],
    languageOptions: {
      parser: tseslint.parser,
      parserOptions: {
        project: './scripts/tsconfig.json',
      },
    },
    rules: {
      '@typescript-eslint/explicit-function-return-type': 'warn',
      '@typescript-eslint/no-explicit-any': 'error',
      '@typescript-eslint/no-unused-vars': ['warn', { argsIgnorePattern: '^_' }],
      '@typescript-eslint/prefer-nullish-coalescing': 'error',
      '@typescript-eslint/prefer-optional-chain': 'error',
      '@typescript-eslint/strict-boolean-expressions': 'warn',
    },
  },
  // 测试文件配置
  {
    name: 'vitest/recommended',
    files: ['**/*.test.{js,ts}', '**/*.spec.{js,ts}'],
    ...eslintPluginVitest.configs['flat/recommended'],
    languageOptions: {
      globals: {
        ...eslintPluginVitest.environments.env.globals,
      },
    },
    rules: {
      '@typescript-eslint/no-explicit-any': 'off', // 测试中允许 any
    },
  },
  // JSON 配置
  {
    name: 'json/recommended',
    files: ['**/*.json'],
    ...json.configs['recommended'],
    rules: {
      'json/*': ['warn', { allowComments: false }],
    },
  },
  // Prettier 配置（放在最后）
  eslintPluginPrettier,
];
