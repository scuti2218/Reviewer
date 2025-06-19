<template>
  <section id="vw_home">
    <FragmentFavoriteTopics />
    <FragmentRecentTopics />
    <WaveDivider background="secondary" />
  </section>
</template>
<script setup lang="ts">
import { WaveDivider } from "@/components";
import { FragmentFavoriteTopics, FragmentRecentTopics } from "@/fragments";
</script>
<style scoped></style>
