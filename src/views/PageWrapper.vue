<template>
  <section id="vw_pageWrapper">
    <NavBar />
    <router-view id="vw_pageWrapper-content" />
  </section>
</template>
<script setup lang="ts">
import NavBar from "@views/NavBar.vue";
</script>
<style scoped>
#vw_pageWrapper {
  height: 100%;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
}

#vw_pageWrapper-content {
  flex: 1;
}
</style>
