<template>
  <section id="vw_auth">
    <BCard
      title="LOGIN"
      variant="primary"
      class="vw_auth-card box-shadow-light outline-black"
      @mouseleave="cmdMouseLeave"
    >
      <section class="vw_auth-container">
        <Button
          v-for="description in Object.values(descriptions)"
          v-show="description.isButton"
          :label="description.info.title"
          :icon="description.info.icon"
          @click="cmdClick(description.info.callback)"
          @mouseenter="cmdMouseEnter(description)"
          :disabled="description.info.params?.disableOnOffline(state.isOnline)"
        />
      </section>
    </BCard>
    <BCard
      :title="state.description.info.title"
      variant="primary"
      class="vw_auth-card box-shadow-light outline-black"
    >
      <section id="vw_auth-desc-details" class="vw_auth-container">
        <span
          class="desc-detail"
          v-for="detail in state.description.info.details"
          >{{ detail }}</span
        >
      </section>
    </BCard>
  </section>
</template>

<script setup lang="ts">
import { Button } from "@/components";
import { onBeforeMount, onMounted, reactive } from "vue";
import { AuthTypeContainerInfo, AuthTypeInfo } from "@/controllers/auth";
import { FirebaseConnectivityChannel } from "@/controllers/useFirebaseConnection";
import {
  useAlertChannel,
  overlayCoverChannel,
  charInvisible,
} from "@/controllers";

// DESCRIPTION PREPARATION
type TDescriptions = {
  isButton: boolean;
  info: AuthTypeInfo;
};
const descriptions = Object.entries(AuthTypeContainerInfo).reduce(
  (acc, [key, info]) => {
    acc[key] = { isButton: true, info };
    return acc;
  },
  {} as Record<string, TDescriptions>
);
descriptions["default"] = {
  isButton: false,
  info: {
    title: "REVIEWER",
    details: [
      "Welcome to Reviewer App",
      charInvisible,
      "Please choose your authentication type.",
    ],
    callback: async () => {},
  },
};
const cmdMouseEnter = (desc: TDescriptions) => {
  state.description = desc;
};
const cmdMouseLeave = () => {
  state.description = descriptions.default;
};
const cmdClick = (callback: () => Promise<any>) => {
  overlayCoverChannel.transmit(true);
  callback()
    .then(() => {
      useAlertChannel("app").transmit({
        message: "Login Successful",
        variant: "success",
      });
    })
    .catch(() => {
      useAlertChannel("app").transmit({
        message: "Login Failed",
        variant: "danger",
      });
    })
    .finally(() => {
      overlayCoverChannel.transmit(false);
    });
};

// STATES
const state = reactive({
  description: descriptions.default as TDescriptions,
  isOnline: false as boolean,
  initNetwork: false as boolean,
});

onBeforeMount(() => {
  FirebaseConnectivityChannel.listen(
    (data: boolean) => {
      state.isOnline = data;
      state.initNetwork = true;
    },
    "transmit",
    "request-feedback"
  );
});

onMounted(() => {
  FirebaseConnectivityChannel.transmit(true, "request");
});
</script>

<style scoped>
#vw_auth {
  height: 100%;
  display: flex;
  align-items: center;
  justify-content: space-evenly;
  padding: var(--padding-main);
  gap: var(--padding-main-top);
  flex-wrap: wrap;
  background-color: var(--bs-secondary);
}

.vw_auth-card {
  min-width: 320px;
  max-width: 450px;
  width: 100%;
  display: flex;
}

.vw_auth-container {
  display: flex;
  flex-direction: column;
  align-items: stretch;
  justify-content: center;
  gap: 30px;
  padding: var(--padding-main);
}
</style>
