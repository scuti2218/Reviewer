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
import { onBeforeMount, ref } from "vue";
import Auth from "@views/Auth.vue";
import { currentUser } from "@controllers/firebase/auth";

const authLoggedIn = ref(false);
onBeforeMount(() => {
  authLoggedIn.value = !!currentUser();
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
