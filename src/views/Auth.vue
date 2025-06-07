<template>
  <section id="vw_auth">
    <section class="vw_auth-container">
      <section class="vw_auth-buttons">
        <Button
          v-for="button in buttons"
          :label="button.label"
          :icon="button.icon"
          @click="button.func"
          @mouseenter="onMouseEnter(button.desc)"
          @mouseleave="onMouseLeave"
        />
      </section>
    </section>
    <section class="vw_auth-container">
      <section class="vw_auth-sidebar">
        <span class="desc-title">{{ states.description.title }}</span>
        <div class="desc-details">
          <span
            class="desc-detail"
            v-for="detail in states.description.details"
            >{{ detail }}</span
          >
        </div>
      </section>
    </section>
  </section>
</template>

<script setup lang="ts">
import { Button } from "@/components";
import { reactive } from "vue";
import EventChannel from "@/controllers/EventChannel";
const char_invisible = "\u200B";

interface IDescriptionData {
  title: string;
  details: string[];
}
interface IDescriptionsContainer {
  default: IDescriptionData;
  anonymous: IDescriptionData;
  guest: IDescriptionData;
  google: IDescriptionData;
}
const descriptions: IDescriptionsContainer = {
  default: {
    title: "REVIEWER",
    details: [
      "Welcome to the reviewer!",
      char_invisible,
      "Choose your type of authentication",
    ],
  },
  anonymous: {
    title: "Login as Anonymous",
    details: [],
  },
  guest: {
    title: "Login as Guest",
    details: [],
  },
  google: {
    title: "Login with Google",
    details: [],
  },
};

interface IButtonData {
  id: string,
  label: string;
  func: () => any;
  icon: string;
  desc: IDescriptionData;
}
const buttons: IButtonData[] = [
  {
    id: "Anonymous",
    label: "Login as Anonymous",
    func: () => EventChannel.emit("auth", { authType: "Anonymous" }),
    icon: "",
    desc: descriptions.anonymous,
  },
  {
    id: "Guest",
    label: "Login as Guest",
    func: () => EventChannel.emit("auth", { authType: "Guest" }),
    icon: "",
    desc: descriptions.guest,
  },
  {
    id: "Google",
    label: "Login with Google",
    func: () => EventChannel.emit("auth", { authType: "Google" }),
    icon: "",
    desc: descriptions.google,
  },
];

const states = reactive({
  description: descriptions.default,
});
const onMouseEnter = (desc: IDescriptionData) => {
  states.description = desc;
};
const onMouseLeave = () => {
  states.description = descriptions.default;
};
</script>

<style scoped>
#vw_auth {
  display: flex;
  align-items: center;
  justify-content: space-between;
  --padding: 30px;
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
