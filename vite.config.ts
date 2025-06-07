import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import path from 'path'

const folders = [
  '',
  'assets',
  'components',
  'composables',
  'controllers',
  'models',
  'router',
  'views',
  'services'
]

const alias = Object.fromEntries(
  folders.map(name => {
    const key = '@' + (name ? name : '')
    const val = path.resolve(__dirname, 'src', name)
    return [key, val]
  })
)

// https://vite.dev/config/
export default defineConfig({
  plugins: [vue()],
  build: {
    outDir: 'dist',
  },
  resolve: {
    alias
  },
})
