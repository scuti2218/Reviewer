<template>
  <BFormTag class="tag-home-recent outline-black" variant="light">
    <h5 class="tag-home-recent-text">{{ data.title }}</h5>
  </BFormTag>
</template>

<script setup lang="ts">
import { ITopicProperties } from "@/models";
import { PropType } from "vue";
defineProps({
  data: {
    type: Object as PropType<ITopicProperties>,
    required: true,
  },
});
</script>

<style scoped>
.tag-home-recent {
  display: flex;
  flex-direction: row;
  gap: 10px;
  justify-content: center;
  align-items: center;
}
</style>
