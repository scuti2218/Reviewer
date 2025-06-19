<template>
  <BAlert
    class="alert-dismissable"
    v-model="state.timer"
    dismissible
    fade
    @close-countdown="state.value = $event"
    :noHoverPause="!!noHoverPause"
    :variant="state.variant"
  >
    {{ state.message }}
    <BProgress
      class="alert-progress outline-black"
      striped
      :max="state.timer"
      :value="state.value"
      height="6px"
    />
  </BAlert>
</template>

<script setup lang="ts">
import { useAlertChannel } from "@/controllers";
import { onMounted, reactive, PropType } from "vue";
import { BaseColorVariant } from "bootstrap-vue-next";

const props = defineProps({
  keyID: {
    type: String,
    required: true,
  },
  message: String,
  timer: {
    type: Number,
    default: 3000,
  },
  noHoverPause: Boolean,
  variant: {
    type: String as PropType<keyof BaseColorVariant | null | undefined>,
    default: "info",
  },
});

const defaultState = {
  message: "" as string,
  timer: 0 as number,
  value: 0 as number,
  variant: "info" as keyof BaseColorVariant | null | undefined,
};
const state = reactive(defaultState);

onMounted(() => {
  useAlertChannel(props.keyID).listen((data) => {
    state.message = props.message ?? data.message;
    state.timer = data.timer ?? props.timer;
    state.variant = data.variant ?? props.variant;
  });
});
</script>

<style scoped>
.alert-dismissable {
  position: absolute;
  bottom: 0;
  width: calc(100% - 2 * var(--padding-main-top));
  margin: var(--padding-main);
}
</style>
