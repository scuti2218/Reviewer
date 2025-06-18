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
import { useAlertChannel, overlayCoverChannel } from "@/controllers";

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
  overlayCoverChannel.transmit(true);
  callback()
    .then(() => {
      useAlertChannel("app").transmit({
        message: "Login Successful",
        variant: "success"
      });
    })
    .catch(() => {
      useAlertChannel("app").transmit({
        message: "Login Failed",
        variant: "danger"
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

/* #vw_auth-login-buttons {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 30px;
  padding: var(--padding-main);

  min-width: 320px;
  max-width: 450px;
} */

/* #vw_auth-sidebar {
  width: auto;

  min-height: 20px;
  max-height: 600px;
  height: auto;
  transition: all 1000ms;
}

#vw_auth-desc-details {
  display: flex;
  flex-direction: column;
} */

/* .vw_auth-container {
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
} */
</style>
