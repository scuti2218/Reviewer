<template>
  <section id="vw_topics">
    <FragmentTableTopics />
    <WaveDivider />
  </section>
</template>

<script setup lang="ts">
import { WaveDivider } from "@/components";
import { FragmentTableTopics } from "@/fragments";
</script>

<style scoped>
#fr_fragmentTableTopics {
  background-color: var(--bs-primary);
}
</style>
