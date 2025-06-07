<template>
  <button class="button">
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
  </button>
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
});

const slots = useSlots();
</script>

<style scoped>
.button {
  outline: 5px solid var(--color-secondary);
  color: var(--color-secondary);
  border: none;
  border-radius: 3px;
  font-size: 1em;
  font-weight: 500;
  font-family: inherit;
  cursor: pointer;
  transition: all 0.10s;
  
  --hover-opacity: 0.8;
  --active-opacity: 0.5;
}

.label {
  font-weight: bold;
}

.button:hover {
  outline: 5px solid var(--color-tertiary);
  color: var(--color-tertiary);
}

.button:active {
  outline: 5px solid var(--color-secondary);
  color: var(--color-secondary);
}
</style>