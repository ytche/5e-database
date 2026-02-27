import { defineConfig } from 'vitest/config';

export default defineConfig({
  test: {
    // Glob pattern to find test files
    include: ['**/*.test.{js,ts}'],
    // Test environment (node, jsdom, happy-dom, edge-runtime)
    environment: 'node',
    // Enable globals like describe, it, expect for Jest compatibility
    globals: true,
    coverage: {
      // Coverage provider
      provider: 'v8',
      // Files to ignore in coverage reports
      exclude: [
        'node_modules/**',
        'coverage/**',
        'dist/**',
        'built/**',
        '*.config.{js,ts}',
        'scripts/dbUtils.ts',
      ],
      // Coverage reporters
      reporter: ['text', 'json', 'html'],
      // Coverage thresholds
      thresholds: {
        lines: 70,
        functions: 80,
        branches: 60,
        statements: 70,
      },
    },
  },
});
