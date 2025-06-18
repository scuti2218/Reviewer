import { onMounted, onUnmounted, watch, Ref, reactive } from "vue";

export interface ComponentPosition {
  top: number;
  bottom: number;
  topPercent: number;
  bottomPercent: number;
}

export function useComponentPosition(elRef: Ref<HTMLElement | null>) {
  const componentPosition = reactive<ComponentPosition>({
    top: 0,
    bottom: 0,
    topPercent: 0,
    bottomPercent: 0,
  });

  const update = () => {
    if (!elRef.value) return;
    const rect = elRef.value.getBoundingClientRect();
    const height = window.innerHeight;

    componentPosition.topPercent = (rect.top / height) * 100;
    componentPosition.bottomPercent = ((height - rect.bottom) / height) * 100;
  };

  onMounted(() => {
    update();
    window.addEventListener("scroll", update);
    window.addEventListener("resize", update);
  });

  onUnmounted(() => {
    window.removeEventListener("scroll", update);
    window.removeEventListener("resize", update);
  });

  watch(elRef, update);

  return componentPosition;
}
