import { fileURLToPath, URL } from 'node:url';
import { defineConfig } from 'vite';
import vue from '@vitejs/plugin-vue';
import viteCompression from 'vite-plugin-compression';
import AutoImport from 'unplugin-auto-import/vite'
import Components from 'unplugin-vue-components/vite';
import { ElementPlusResolver } from 'unplugin-vue-components/resolvers';
import vuetify from 'vite-plugin-vuetify';

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [
    vue(),
    vuetify({ autoImport: true }),
    AutoImport({
      resolvers: [ElementPlusResolver()],
    }),
    Components({
      resolvers: [ElementPlusResolver()],
    }),
    // Gzip compression
    viteCompression({
      algorithm: 'gzip',
      ext: '.gz',
      deleteOriginFile: false, // Keep original uncompressed files
    }),
    viteCompression({
      algorithm: 'brotliCompress',
      ext: '.br',
      deleteOriginFile: false, 
    }),
  ],
  resolve: {
    alias: {
      '@': fileURLToPath(new URL('./src', import.meta.url)),
      '@tests': fileURLToPath(new URL('./tests', import.meta.url)),
    },
  },
  test: { // Configuración para Vitest
    globals: true,
    environment: 'jsdom',
  },
  build: {
    manifest: true,
    chunkSizeWarningLimit: 2000,
    modulePreload: {
      polyfill: true,
      resolveDependencies: (filename, deps, { hostId, hostType }) => {
        // Filter out pdf-export chunk from being preloaded
        return deps.filter(dep => 
          !dep.includes('pdf-export') && 
          !dep.includes('element-plus')
        );
      }
    },
    rollupOptions: {
      output: {
        manualChunks(id) {
          if (
            id.includes('vite/modulepreload-polyfill.js') ||
            id.includes('vite/preload-helper.js') ||
            id.endsWith('plugin-vue:export-helper') || // Vue SFC compiler helper
            id.includes('vite/dist/client/client.mjs') || // Vite client (might contain DIH)
            id.includes('vite/dist/client/env.mjs') ||
            id.startsWith('\0vite/dynamic-import-helper') // Vite internal namespace for helpers
          ) {
            // console.log('>>> Forcing Vite internal to vendor:', id);
            return 'vendor';
          }

          if (id.includes('node_modules')) {
            if (id.includes('echarts') || id.includes('zrender')) return 'echarts';
            if (id.includes('xlsx')) return 'xlsx';
            if (id.includes('html2canvas') || id.includes('jspdf')) return 'pdf-export';
            if (id.includes('@fortawesome')) return 'fontawesome';
            if (id.includes('element-plus')) return 'element-plus';
            if (id.includes('vuetify')) return 'vuetify';
            if (id.includes('lodash-es')) return 'lodash';
            if (id.includes('core-js')) return 'corejs';
            return 'vendor';
          }
        },
        entryFileNames: 'assets/[name].js',
        chunkFileNames: 'assets/[name].js',
        assetFileNames: 'assets/[name].[ext]' // Removes content hash
      },
    },
    minify: 'terser',
    // Tree shaking optimization
    sourcemap: false
  },
});
