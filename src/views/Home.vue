<template>
  <h1>Home</h1>
  <button @click="routeTo('/Sample')">Go to Sample</button>
</template>
<script setup lang="ts">
import { useRouteTo } from "@composables/router";
const routeTo = useRouteTo()
</script>
<style scoped>
</style>