<template>
  <main v-show="state.initDone">
    <section v-if="state.authLoggedIn">
      <header>
        <nav>
          {{ state.authData.authUsername }}
          <button @click="cmdLogout">logout</button>
        </nav>
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
import { onBeforeMount, onMounted } from "vue";
import Auth from "@views/Auth.vue";
import {
  onFirebaseInitialize,
  EAuthType,
  IAuthData,
  AuthChannel,
  defaultAuthData,
} from "@/controllers/auth";
import { User } from "firebase/auth";
import { logout } from "@/controllers/auth";
import {
  usePersistentState,
  resetState,
} from "./controllers/usePersistentState";

const defaultState = {
  initFirebase: false as boolean,
  initDone: false as boolean,

  initAuth: false as boolean,
  authData: defaultAuthData as IAuthData,

  authLoggedIn: false as boolean,
};
const state = usePersistentState("app-state", defaultState);

const onInitAuth = (user: User | null) => {
  state.authData.authUser = user;
  if (!!user) {
    state.authData.authType = EAuthType.Google;
    state.authData.authUsername = user.displayName ?? "";
    state.authLoggedIn = true;
  }
};

onBeforeMount(() => {
  onFirebaseInitialize().then((user: User | null) => {
    state.initFirebase = true;
    onInitAuth(user);
    state.initAuth = true;
    state.initDone = true;
  });
});

onMounted(async () => {
  AuthChannel.listen((data: IAuthData) => {
    state.authData = data;
    state.authLoggedIn = true;
  });
});

const cmdLogout = () => {
  resetState(state, defaultState);
  logout().then(() => window.location.reload());
};
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
