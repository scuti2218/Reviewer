<template>
  <section id="vw_saample">
    <h1>Sample</h1>
    <button @click="routeTo('/home')">Go to Home</button>
  </section>
</template>
<script setup lang="ts">
import { useRouteTo } from "@composables/router";
const routeTo = useRouteTo();
</script>
<style scoped></style>
