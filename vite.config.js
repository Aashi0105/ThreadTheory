import { defineConfig } from 'vite';
import fs from 'fs';
import path from 'path';



export default defineConfig({
  server: {
    proxy: {
      '/api': {
        target: 'http://localhost:3000',
        changeOrigin: true
      }
    },
    fs: {
      allow: [
        '.',
        'C:/Users/Aashi/.gemini/antigravity-ide/brain/8a51b963-f609-405d-8d52-56f1cf1e0f30',
        'C:/Users/Aashi/.gemini/antigravity-ide/brain'
      ]
    }
  }
});
