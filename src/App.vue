<template>
  <main>
    <section v-if="authLoggedIn">
      <header>
        <nav></nav>
      </header>
      <router-view />
      <footer></footer>
    </section>
    <section v-else>
      <Auth />
    </section>
  </main>
</template>

<script setup lang="ts">
import { onBeforeMount, onMounted, ref } from "vue";
import Auth from "@views/Auth.vue";
import { currentUser } from "@controllers/firebase/auth";
import EventChannel from "@/controllers/EventChannel";

const authLoggedIn = ref(false);
onBeforeMount(() => {
  authLoggedIn.value = !!currentUser();
});

onMounted(async () => {
  EventChannel.on("auth", (data) => {
    authLoggedIn.value = true;
    console.log("Got data:", data);
  });
});
</script>

<style scoped>
header {
  width: 100%;
  height: 20px;

  position: relative;
  top: 0;
  left: 0;
}
</style>
