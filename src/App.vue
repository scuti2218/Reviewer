<template>
  <main v-show="state.initDone">
    <span>isOnline = {{ state.isOnline }}</span>
    <section v-if="persistentData.auth.loggedIn">
      <header>
        <nav>
          <span>{{ persistentData.auth.name }}</span>
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
import { onBeforeMount, onMounted, reactive } from "vue";
import Auth from "@views/Auth.vue";
import {
  onFirebaseInitialize,
  IAuthData,
  AuthChannel,
  defaultAuthData,
  EAuthType,
  loginAnonymous,
  loginWithGoogle,
} from "@/controllers/auth";
import { logout } from "@/controllers/auth";
import {
  usePersistentData,
  resetPersistentData,
} from "./controllers/usePersistentData";
import { User } from "firebase/auth";
import {
  FirebaseConnectivityChannel,
  useFirebaseConnection,
} from "./controllers/useFirebaseConnection";

const defaultState = {
  initFirebase: false as boolean,
  initAuth: false as boolean,
  initDone: false as boolean,
  isOnline: false as boolean,
};
const state = reactive(defaultState);
const persistentData = usePersistentData("app-persistentData", {
  auth: defaultAuthData as IAuthData,
});

const onInitAuth = async (user: User | null) => {
  if (!!persistentData.auth.loggedIn === !!user) return true;

  if (!!user) {
    resetPersistentData(persistentData, defaultAuthData);
    return true;
  }

  const login = () =>
    persistentData.auth.type == EAuthType.Google
      ? loginWithGoogle(false)
      : loginAnonymous();
  return login().then(() => true);
};

onBeforeMount(() => {
  useFirebaseConnection();
  FirebaseConnectivityChannel.listen((data: boolean) => {
    state.isOnline = data;
  }, "transmit");
  FirebaseConnectivityChannel.listen(
    () =>
      FirebaseConnectivityChannel.transmit(state.isOnline, "request-feedback"),
    "request"
  );

  onFirebaseInitialize()
    .then((user: User | null) => {
      state.initFirebase = true;
      return onInitAuth(user);
    })
    .then(() => {
      state.initAuth = true;
      state.initDone = [state.initFirebase, state.initAuth].every(Boolean);
    });
});

onMounted(async () => {
  AuthChannel.listen((data: IAuthData) => {
    persistentData.auth = data;
  });
});

const cmdLogout = () =>
  logout().finally(() => {
    resetPersistentData(persistentData.auth, defaultAuthData);
    Object.assign(state, defaultState);
    FirebaseConnectivityChannel.transmit(state.isOnline, "request-feedback");
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
