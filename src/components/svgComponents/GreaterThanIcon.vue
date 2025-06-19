<template>
  <svg
    class="greater-than-icon"
    xmlns="http://www.w3.org/2000/svg"
    viewBox="0 0 512 512"
  >
    <path
      :fill="state.fill"
      fill-opacity="1"
      :stroke="state.outline"
      :stroke-width="stroke"
      d="M224.3 273l-136 136c-9.4 9.4-24.6 9.4-33.9 0l-22.6-22.6c-9.4-9.4-9.4-24.6 0-33.9l96.4-96.4-96.4-96.4c-9.4-9.4-9.4-24.6 0-33.9L54.3 103c9.4-9.4 24.6-9.4 33.9 0l136 136c9.5 9.4 9.5 24.6.1 34z"
    />
  </svg>
</template>

<script setup lang="ts">
import { computed, PropType, reactive } from "vue";
import { BaseColorVariant } from "bootstrap-vue-next";
import { getThemeColor } from "@/controllers";

const props = defineProps({
  variant: {
    type: String as PropType<keyof BaseColorVariant>,
    default: "primary",
  },
  outline: {
    type: String as PropType<keyof BaseColorVariant>,
    default: "dark",
  },
  background: {
    type: String as PropType<keyof BaseColorVariant | null | undefined>,
    default: undefined,
  },
  stroke: {
    type: Number,
    default: 1,
  },
});

const state = reactive({
  fill: computed(() => getThemeColor(props.variant)),
  outline: computed(() => getThemeColor(props.outline)),
  background: computed(() => getThemeColor(props.background!)),
});
</script>

<style scoped>
.greater-than-icon {
  aspect-ratio: 1/1;
  background: no-repeat center;
  background-size: cover;
  height: 100%;
}
</style>
