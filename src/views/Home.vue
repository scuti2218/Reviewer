<template>
  <section id="vw_home">
    <!-- <h1>Home</h1>
    <button @click="routeTo('/Sample')">Go to Sample</button> -->
    <!-- Favorites -->
    <!-- Topics -->
    <section id="vw_home-header"></section>
    <WaveDivider background="secondary" />
    <section id="vw_home-footer"></section>
  </section>
</template>
<script setup lang="ts">
import { useRouteTo } from "@/controllers/router";
import { WaveDivider } from "@/components";
const routeTo = useRouteTo();
</script>
<style scoped>
#vw_home-header {
  width: 100%;
  height: 600px;
  background-color: var(--bs-primary);
}
#vw_home-footer {
  width: 100%;
  height: 600px;
  background-color: var(--bs-secondary);
}
</style>
