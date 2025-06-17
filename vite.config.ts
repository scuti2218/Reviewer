import { defineConfig } from "vite";
import vue from "@vitejs/plugin-vue";
import path from "path";
import Components from "unplugin-vue-components/vite";
import { BootstrapVueNextResolver } from "bootstrap-vue-next";

const folders = [
  "",
  "assets",
  "components",
  "controllers",
  "models",
  "router",
  "views",
  "services",
  "types"
];

const alias = Object.fromEntries(
  folders.map((name) => {
    const key = "@" + (name ? name : "");
    const val = path.resolve(__dirname, "src", name);
    return [key, val];
  })
);

// https://vite.dev/config/
export default defineConfig({
  plugins: [
    vue(),
    Components({
      resolvers: [BootstrapVueNextResolver()],
    }),
  ],
  build: {
    outDir: "dist",
  },
  resolve: {
    alias,
  },
  css: {
    preprocessorOptions: {
      scss: {
        additionalData: `@use "bootstrap/scss/functions";`,
      },
    },
  },
});
