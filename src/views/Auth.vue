<template>
  <section id="vw_auth">
    <section
      class="vw_auth-container vw_auth-auth_message"
      v-show="state.authenticating"
    >
      <span>Please wait while we try to log you in</span>
    </section>
    <section class="vw_auth-container" v-show="!state.authenticating">
      <section class="vw_auth-buttons" @mouseleave="cmdMouseLeave">
        <ButtonAuth
          v-for="description in Object.values(descriptions)"
          v-show="description.isButton"
          :label="description.info.title"
          :icon="description.info.icon"
          @click="cmdClick(description.info.callback)"
          @mouseenter="cmdMouseEnter(description)"
          :disabled="description.info.params?.disableOnOffline(state.isOnline)"
        />
      </section>
    </section>
    <section class="vw_auth-container" v-show="!state.authenticating">
      <section class="vw_auth-sidebar">
        <span class="desc-title">{{ state.description.info.title }}</span>
        <div class="desc-details">
          <span
            class="desc-detail"
            v-for="detail in state.description.info.details"
            >{{ detail }}</span
          >
        </div>
      </section>
    </section>
  </section>
</template>

<script setup lang="ts">
import { ButtonAuth } from "@/components";
import { onBeforeMount, onMounted, reactive } from "vue";
import { AuthTypeContainerInfo, AuthTypeInfo } from "@/controllers/auth";
import { FirebaseConnectivityChannel } from "@/controllers/useFirebaseConnection";

// DESCRIPTION PREPARATION
const char_invisible = "\u200B";
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
      char_invisible,
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
  state.authenticating = true;
  callback().catch(() => {
    state.authenticating = false;
  });
};

// STATES
const state = reactive({
  description: descriptions.default as TDescriptions,
  authenticating: false as boolean,
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
  display: flex;
  align-items: center;
  justify-content: space-between;
  --padding: var(--padding-main);
  padding: var(--padding);
  height: calc(100vh - (2 * var(--padding)));
}

.vw_auth-container {
  width: calc(50% - var(--padding));
  height: 100%;

  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;

  > section {
    border-radius: 10px;
    background-color: var(--color-quaternary);
    outline: 6px solid var(--color-secondary);
  }
}

.vw_auth-auth_message {
  flex: 1;
}

.vw_auth-buttons {
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  gap: 40px;
  padding: 30px;

  > .button {
    height: 50px;
    width: 250px;
  }
}

.vw_auth-sidebar {
  --padding-sidebar-block: 10px;
  --padding-sidebar-inline: 20px;
  padding: var(--padding-sidebar-block) var(--padding-sidebar-inline);
  width: calc(100% - (2 * var(--padding-sidebar-inline)));
  height: 100%;
  font-family: inherit;
  font-weight: 500;

  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 20px;

  > .desc-title {
    font-size: 1.5em;
    font-weight: bold;
  }

  > .desc-details {
    align-self: flex-start;
    display: flex;
    flex-direction: column;
    align-items: flex-start;
  }
}
</style>
