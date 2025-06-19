<template>
  <section id="fr_fragmentFavoriteTopics" class="main-container">
    <h1 id="fr_fragmentFavoriteTopics-title">Favorites</h1>
    <section class="container-scrollable scrollable">
      <ButtonAddHomeFavorite v-if="state.favorites.length == 0" />
      <CardHomeFavorite v-else v-for="topic in state.favorites" :data="topic" />
    </section>
  </section>
</template>

<script setup lang="ts">
import { CardHomeFavorite, ButtonAddHomeFavorite } from "@/components";
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
};
const state = reactive(defaultState);
</script>

<style scoped>
#fr_fragmentFavoriteTopics {
  width: 100%;
  background-color: var(--bs-primary);
}
</style>
