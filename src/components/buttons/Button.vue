<template>
  <BButton
    class="button box-shadow outline-black"
    :disabled="!!disabled"
    variant="tertiary"
  >
    <span class="icon" v-if="(!!slots.icon || !!icon) && !hideIcon">
      <slot name="icon" />
      {{ !slots.icon ? icon : "" }}
    </span>
    <span class="label" v-if="(!!slots.label || !!label) && !hideLabel">
      <slot name="label" />
      {{ !slots.label ? label : "" }}
    </span>
    <span class="default" v-if="!!slots.default && !hideDefault">
      <slot />
    </span>
  </BButton>
</template>

<script setup lang="ts">
import { useSlots } from "vue";

defineProps({
  icon: String,
  label: String,
  selected: Boolean,
  hideIcon: Boolean,
  hideLabel: Boolean,
  hideDefault: Boolean,
  disabled: Boolean,
});

const slots = useSlots();
</script>

<style scoped>
.button {
  font-size: 1em;
  font-weight: 500;
  font-family: inherit;
  height: 50px;
}

.label {
  font-weight: bold;
}
</style>
