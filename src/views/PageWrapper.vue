<template>
  <section id="vw_pageWrapper">
    <header>
      <section id="vw_pageWrapper-header-left"></section>
      <section id="vw_pageWrapper-header-middle"></section>
      <section id="vw_pageWrapper-header-right">
        <span>{{ state.auth.name }}</span>
        <button @click="cmdLogout">logout</button>
      </section>
    </header>
    <router-view />
    <footer></footer>
  </section>
</template>
<script setup lang="ts">
import { onBeforeMount, onMounted, reactive } from "vue";
import { AuthChannel, IAuthData, defaultAuthData } from "@/controllers/auth";
const defaultState = {
  auth: defaultAuthData as IAuthData,
};
const state = reactive(defaultState);

onBeforeMount(() => {
  AuthChannel.listen(
    (auth) => {
      state.auth = auth;
    },
    "request-feedback",
    "login"
  );
});
onMounted(async () => {
  AuthChannel.transmit(defaultAuthData, "request");
});

const cmdLogout = () => AuthChannel.transmit(state.auth, "logout");
</script>
<style scoped>
header {
  height: 50px;
  background-color: yellow;

  display: flex;
  flex-direction: row;
  gap: 20px;
  align-items: center;
  justify-content: space-between;
  padding-inline: var(--padding-main-inline);

  > #vw_pageWrapper-header-right {
    display: flex;
    flex-direction: row;
    gap: 10px;
    align-items: center;
    justify-content: space-between;
  }
}
</style>
