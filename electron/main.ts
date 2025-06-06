import { app, BrowserWindow } from 'electron'
import { join } from 'path'
import { fileURLToPath } from 'url'
import { spawn } from 'child_process'
import http from 'http'

const __dirname = fileURLToPath(new URL('.', import.meta.url))

function waitForViteServer(url: string) {
  return new Promise<void>((resolve) => {
    const timer = setInterval(() => {
      http.get(url, () => {
        clearInterval(timer)
        resolve()
      }).on('error', () => {})
    }, 300)
  })
}

app.whenReady().then(async () => {
  const win = new BrowserWindow({
    width: 800,
    height: 600,
    webPreferences: { nodeIntegration: true, contextIsolation: false },
  })

  const dev = !app.isPackaged
  const url = 'http://localhost:5173'

  if (dev) {
    await waitForViteServer(url)
    win.loadURL(url)
  } else {
    win.loadFile(join(__dirname, '../dist/index.html'))
  }
})

app.on('window-all-closed', () => { if (process.platform !== 'darwin') app.quit() })
