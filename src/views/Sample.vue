<template>
   <h1>Sample</h1>
  <button @click="routeTo('/home')">Go to Home</button>
</template>
<script setup lang="ts">
import { useRouteTo } from "@/utils/router";
const routeTo = useRouteTo()
</script>
<style scoped>
</style>