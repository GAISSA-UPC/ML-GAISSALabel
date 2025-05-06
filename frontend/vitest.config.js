import { fileURLToPath } from 'node:url'
import { mergeConfig } from 'vite'
import { configDefaults, defineConfig } from 'vitest/config'
import viteConfig from './vite.config'

export default mergeConfig(
  viteConfig,
  defineConfig({
    test: {
      environment: 'jsdom',
      exclude: [...configDefaults.exclude, 'e2e/*'],
      root: fileURLToPath(new URL('./', import.meta.url)),
      transformMode: {
        web: [/\.[jt]sx$/]
      },
      setupFiles: ['./vitest.setup.js'],
      // Mock css imports during tests
      css: {
        modules: {
          classNameStrategy: 'non-scoped'
        }
      },
      deps: {
        inline: ['element-plus']
      }
    }
  })
)