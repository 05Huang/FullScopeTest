import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';
import path from 'path';

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [react()],
  resolve: {
    alias: {
      '@': path.resolve(__dirname, './src'),
    },
  },
  server: {
    port: 3001,
    proxy: {
      '/api/': {
        target: 'http://localhost:5211',
        changeOrigin: true,
      },
    },
  },
  build: {
    outDir: 'dist',
    sourcemap: false,
    rollupOptions: {
      output: {
        manualChunks: {
          // React 核心
          'vendor-react': ['react', 'react-dom', 'react-router-dom'],
          // UI 框架
          'vendor-antd': ['antd', '@ant-design/icons'],
          // 代码编辑器
          'vendor-monaco': ['@monaco-editor/react'],
          // 图表库
          'vendor-charts': ['echarts', 'echarts-for-react'],
          // 状态管理
          'vendor-zustand': ['zustand'],
          // 工具库
          'vendor-utils': ['axios', 'dayjs'],
        },
      },
    },
    // 分包阈值
    chunkSizeWarningLimit: 1000,
  },
});
