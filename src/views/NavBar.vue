<template>
  <BNavbar id="vw_navBar" toggleable="lg" variant="dark" class="sticky-top">
    <BNavbarBrand id="vw_navBar-brand">Reviewer</BNavbarBrand>
    <BNavbarToggle target="nav-collapse" />
    <BCollapse id="nav-collapse" is-nav>
      <BNavbarNav class="vw_navBar-avatar ms-auto mb-2 mb-lg-0">
        <em class="blend-text-to-bg">{{ state.auth.name }}</em>
        <BNavItemDropdown right>
          <template #button-content>
            <BAvatar variant="secondary" :text="state.auth.name[0]"
          /></template>
          <BDropdownItem href="#">Profile</BDropdownItem>
          <BDropdownItem @click="cmdLogout">Sign Out</BDropdownItem>
        </BNavItemDropdown>
      </BNavbarNav>
    </BCollapse>
  </BNavbar>
</template>

<script setup lang="ts">
import { onBeforeMount, onMounted, reactive } from "vue";
import {
  AuthChannel,
  IAuthData,
  defaultAuthData,
  logout,
} from "@/controllers/auth";
import { overlayCoverChannel, useAlertChannel } from "@/controllers";
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
const cmdLogout = () => {
  overlayCoverChannel.transmit(true);
  logout().finally(() => {
    useAlertChannel("app").transmit({
      message: "Logged Out Succesfully",
      variant: "success",
    });
    overlayCoverChannel.transmit(false);
    AuthChannel.transmit(state.auth, "logout");
  });
};
</script>

<style scoped>
#vw_navBar-brand {
  font-weight: bold;
  color: white;
  mix-blend-mode: normal;
}

.vw_navBar-avatar {
  display: flex;
  flex-direction: row;
  align-items: center;
  gap: 10px;
}
</style>
