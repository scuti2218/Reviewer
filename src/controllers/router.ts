import { useRouter } from 'vue-router'

export function useRouteTo() {
    const router = useRouter()
    return (target: string) => router.push(target)
}