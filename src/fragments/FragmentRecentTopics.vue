<template>
  <section
    id="fr_fragmentRecentTopics"
    class="main-container"
    v-show="state.recents.length != 0"
  >
    <h3 id="fr_fragmentRecentTopics-title">Recently reviewed topics</h3>
    <section id="fr_fragmentRecentTopics-contents">
      <TagHomeRecent v-for="topic in state.recents" :data="topic" />
    </section>
  </section>
</template>

<script setup lang="ts">
import { TagHomeRecent } from "@/components";
import { reactive } from "vue";
import { ITopicProperties } from "@/models";

const defaultState = {
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
#fr_fragmentRecentTopics {
  width: 100%;
  background-color: var(--bs-primary);
  > #fr_fragmentRecentTopics-title {
    text-align: left;
  }

  > #fr_fragmentRecentTopics-contents {
    display: flex;
    flex-flow: row wrap;
    justify-content: space-between;
    gap: 10px;
  }
}
</style>
