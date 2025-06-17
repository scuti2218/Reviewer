import { reactive, watch } from 'vue'

export function usePersistentData<T extends object>(key: string, defaults: T) {
  const saved = localStorage.getItem(key)
  const state = reactive(saved ? JSON.parse(saved) : defaults) as T

  watch(state, () => {
    localStorage.setItem(key, JSON.stringify(state))
  }, { deep: true })

  return state
}

export function resetPersistentData<T extends object>(state: T, defaultState: T) {
  Object.assign(state, JSON.parse(JSON.stringify(defaultState)))
}