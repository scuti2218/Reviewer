import { createRouter, createWebHashHistory } from 'vue-router'
import type { RouteRecordRaw } from "vue-router";

const views = import.meta.glob('../views/**/*.vue')

const routes: RouteRecordRaw[] = Object.keys(views).map((path) => {
  const name = path.match(/..\/views\/(.*)\.vue$/)?.[1] || ''
  const urlPath = '/' + name.toLowerCase()
  return { path: urlPath, component: views[path] }
})

routes.push({ path: '/', redirect: '/home' })

export default createRouter({
  history: createWebHashHistory(),
  routes,
})
