<template>
  <section id="vw_home">
    <!-- <h1>Home</h1>
    <button @click="routeTo('/Sample')">Go to Sample</button> -->
    <!-- Favorites -->
    <section id="vw_home-favorites" class="main-container">
      <h1 id="vw_home-favorites-title">Favorites</h1>
      <section class="container-scrollable scrollable">
        <ButtonAddHomeFavorite v-if="state.favorites.length == 0" />
        <CardHomeFavorite
          v-else
          v-for="topic in state.favorites"
          :data="topic"
        />
      </section>
    </section>
    <!-- Recently reviewed topics -->
    <section id="vw_home-recents" class="main-container" v-show="state.recents.length != 0">
      <h3 id="vw_home-recents-title">Recently reviewed topics</h3>
      <section id="vw_home-recents-contents">
        <TagHomeRecent v-for="topic in state.recents" :data="topic" />
      </section>
    </section>
    <WaveDivider background="secondary" />
    <!-- Topics -->
    <section id="vw_home-footer"></section>
  </section>
</template>
<script setup lang="ts">
import {
  WaveDivider,
  CardHomeFavorite,
  ButtonAddHomeFavorite,
  TagHomeRecent,
} from "@/components";
import { reactive } from "vue";
import { ITopicProperties } from "@/models";

const defaultState = {
  favorites: [
    // {
    //   title: "Title 1",
    //   description: "this is a blank",
    //   version: "0.1.1",
    //   token: "123456",
    //   code: "12345",
    // },
    // {
    //   title: "Title 2",
    //   description: "this is a blank",
    //   version: "0.1.2",
    //   token: "123456",
    //   code: "289465",
    // },
    // {
    //   title: "Title 3",
    //   description: "this is a blank",
    //   version: "0.1.2",
    //   token: "123456",
    // },
  ] as ITopicProperties[],
  recents: [
    // {
    //   title: "Title 1",
    // },
    // {
    //   title: "Title 1dwaaaaaaaaaa",
    // },
    // {
    //   title: "Title 1dwaaaaaaaaaa",
    // },
    // {
    //   title: "Title 1",
    // },
    // {
    //   title: "Title 1waddddddddddddddddd",
    // },
    // {
    //   title: "Title 1waddddddddddddddddd",
    // },
  ] as ITopicProperties[],
};
const state = reactive(defaultState);
</script>
<style scoped>
#vw_home-favorites,
#vw_home-recents {
  width: 100%;
  background-color: var(--bs-primary);
}

#vw_home-recents {
  > #vw_home-recents-title {
    text-align: left;
  }

  > #vw_home-recents-contents {
    display: flex;
    flex-flow: row wrap;
    justify-content: space-between;
    gap: 10px;
  }
}

#vw_home-footer {
  width: 100%;
  height: 600px;
  background-color: var(--bs-secondary);
}
</style>
