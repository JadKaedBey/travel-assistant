import path from 'node:path';
import { fileURLToPath } from 'node:url';
import { fixupConfigRules, fixupPluginRules } from '@eslint/compat';
import typescriptEslint from '@typescript-eslint/eslint-plugin';
import react from 'eslint-plugin-react';
import _import from 'eslint-plugin-import';
import globals from 'globals';
import tsParser from '@typescript-eslint/parser';
import js from '@eslint/js';
import { FlatCompat } from '@eslint/eslintrc';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);
const compat = new FlatCompat({
  baseDirectory: __dirname,
  recommendedConfig: js.configs.recommended,
  allConfig: js.configs.all
});

export default [{
  ignores: ['**/dist/**/*.js', 'vite.config.js', 'eslint.config.mjs', 'api.d.ts'],
}, ...fixupConfigRules(compat.extends(
  'eslint:all',
  'plugin:@typescript-eslint/all',
  'plugin:react/recommended',
  'plugin:import/recommended',
  'plugin:import/typescript',
)), {
  plugins: {
    '@typescript-eslint': fixupPluginRules(typescriptEslint),
    react: fixupPluginRules(react),
    import: fixupPluginRules(_import),
  },

  languageOptions: {
    globals: {
      ...globals.browser,
    },

    parser: tsParser,
    ecmaVersion: 'latest',
    sourceType: 'module',

    parserOptions: {
      project: ['./tsconfig.json'],
    },
  },

  settings: {
    react: {
      version: 'detect',
    },

    'import/resolver': {
      typescript: true,
    },
  },

  rules: {
    'import/order': 'error',
    'react/react-in-jsx-scope': 'off',
    'react/prop-types': 'off',
    '@typescript-eslint/no-non-null-assertion': 'off',
    '@typescript-eslint/no-magic-numbers': 'off',
    '@typescript-eslint/strict-boolean-expressions': 'off',
    '@typescript-eslint/no-floating-promises': 'off',
    '@typescript-eslint/explicit-module-boundary-types': 'off',
    '@typescript-eslint/no-misused-promises': 'off',
    '@typescript-eslint/prefer-readonly-parameter-types': 'off',
    '@typescript-eslint/explicit-function-return-type': 'off',

    '@typescript-eslint/naming-convention': ['error', {
      selector: 'function',
      format: ['camelCase', 'PascalCase'],
    }],

    'no-duplicate-imports': 'off', // breaks `import type` and `import` from same source
    'new-cap': 'off',
    'no-ternary': 'off',
    'no-undefined': 'off',
    camelcase: 'off',
    'id-length': 'off',
    'sort-imports': 'off',
    'sort-keys': 'off',
    'one-var': 'off',
    'max-lines-per-function': 'off',
    'no-inline-comments': 'off',
    'max-statements': 'off',
    indent: ['error', 2],
    'linebreak-style': ['error', 'unix'],
    quotes: ['error', 'single'],
    semi: ['error', 'always'],
  },
}];