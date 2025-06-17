import { app, BrowserWindow, ipcMain } from "electron";
import { fileURLToPath } from "url";
import { join } from "path";
import http from "http";

const __dirname = fileURLToPath(new URL('.', import.meta.url))

function waitForViteServer(url: string) {
  return new Promise<void>((resolve) => {
    const timer = setInterval(() => {
      http
        .get(url, () => {
          clearInterval(timer);
          resolve();
        })
        .on("error", () => {});
    }, 300);
  });
}

app.whenReady().then(async () => {
  const mainWindow = new BrowserWindow({
    width: 800,
    height: 600,
    webPreferences: {
      nodeIntegration: true,
      contextIsolation: false,
    },
  });

  const dev = !app.isPackaged;
  const url = "http://localhost:5173";

  if (dev) {
    await waitForViteServer(url);
    mainWindow.loadURL(url);
  } else {
    mainWindow.loadFile(join(__dirname, "../dist/index.html"));
  }
});

app.on("window-all-closed", () => {
  if (process.platform !== "darwin") app.quit();
});
