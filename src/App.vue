<template>
  <main>
    <Splashart v-if="!state.initDone" @done="onSplashartDone" />
    <Auth v-else-if="!persistentData.auth.loggedIn" />
    <PageWrapper v-else />
  </main>
</template>

<script setup lang="ts">
import { onBeforeMount, onMounted, reactive, watch } from "vue";
import { Auth, Splashart, PageWrapper } from "@/views";
import { User } from "firebase/auth";
import {
  onFirebaseInitialize,
  IAuthData,
  AuthChannel,
  defaultAuthData,
  EAuthType,
  loginAnonymous,
  loginWithGoogle,
  deleteUserIfAnonymous,
  logout,
} from "@/controllers/auth";
import {
  FirebaseConnectivityChannel,
  useFirebaseConnection,
} from "@controllers/useFirebaseConnection";
import { usePersistentData } from "@controllers/usePersistentData";

// DATA: STATE
const defaultState = {
  initSplashart: false as boolean,
  initFirebase: false as boolean,
  initAuth: false as boolean,
  initDone: false as boolean,
  isOnline: false as boolean,
};
const state = reactive(defaultState);

// STATE: PERSISTENT DATA
const defaultPersistentData = {
  auth: defaultAuthData as IAuthData,
};
const persistentData = usePersistentData(
  "app-persistentData",
  defaultPersistentData
);

// WATCHER: INITIALIZATION
watch(
  () =>
    [state.initSplashart, state.initFirebase, state.initAuth].every(Boolean),
  () => {
    state.initDone = [
      state.initFirebase,
      state.initAuth,
      state.initSplashart,
    ].every(Boolean);
  }
);

// METHOD: CHECK IF A USER IS CURRENTLY LOGGED IN
const initAuth = async (user: User | null) => {
  if (!!persistentData.auth.loggedIn === !!user) return;

  if (!!user) {
    await deleteUserIfAnonymous();
    return;
  }

  const relogin = () =>
    persistentData.auth.type == EAuthType.Google
      ? loginWithGoogle(false)
      : loginAnonymous();
  return relogin().then(() =>
    AuthChannel.transmit(persistentData.auth, "login")
  );
};

// EVENT: ON SPLASHART FINISH
const onSplashartDone = () => {
  state.initSplashart = true;
};

// EVENT: ON BEFORE MOUNT
onBeforeMount(() => {
  FirebaseConnectivityChannel.listen((data: boolean) => {
    state.isOnline = data;
  }, "transmit").listen(
    () =>
      FirebaseConnectivityChannel.transmit(state.isOnline, "request-feedback"),
    "request"
  );

  AuthChannel.listen(() => {
    AuthChannel.transmit(persistentData.auth, "request-feedback");
  }, "request")
    .listen((data: IAuthData) => {
      persistentData.auth = data;
    }, "login")
    .listen(() => {
      logout().finally(() => {
        persistentData.auth = defaultAuthData;
      });
    }, "logout");
});

// EVENT: ON MOUNTED
onMounted(async () => {
  useFirebaseConnection();
  onFirebaseInitialize()
    .then((user: User | null) => {
      state.initFirebase = true;
      return initAuth(user);
    })
    .then(() => {
      state.initAuth = true;
    });
});
</script>

<style scoped>
</style>
