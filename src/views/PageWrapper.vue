<template>
  <section id="vw_pageWrapper">
    <NavBar />
    <router-view id="vw_pageWrapper-content" />
    <footer></footer>
  </section>
</template>
<script setup lang="ts">
import { NavBar } from "@/views";
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

footer {
  height: 50px;
  background-color: red;
}
</style>
