<template>
  <BCard class="card-home-favorite outline-black box-shadow-dark">
    <BCardBody class="card-home-favorite-body">
      <BCardImg
        class="card-home-favorite-img"
        :src="data.image ?? defaultImg"
      />
      <BCardTitle class="card-home-favorite-title" :text="data?.title" />
      <BCardSubtitle
        class="card-home-favorite-code"
        :text="data.code ?? charInvisible"
      />
      <BCardText
        class="card-home-favorite-description"
        :text="data.description"
      />
      <Button
        class="card-home-favorite-button" label="Open Topic >>" />
    </BCardBody>
  </BCard>
</template>

<script setup lang="ts">
import { ITopicProperties } from "@/models";
import { PropType } from "vue";
import { charInvisible } from "@/controllers";
import { Button } from "..";
defineProps({
  data: {
    type: Object as PropType<ITopicProperties>,
    required: true,
  },
});
const defaultImg =
  "https://framerusercontent.com/images/6rpk2kywXgQTGE0L8A1f2IeKjXc.jpg?scale-down-to=512";
</script>

<style scoped>
.card-home-favorite {
  border-radius: 15px;
  min-width: 300px;
  max-width: 300px;
  align-self: stretch;
}

.card-home-favorite-body {
  padding: 16px;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: top;
}

.card-home-favorite-img {
  max-width: 100%;
  margin-bottom: 10px;
  border-radius: 15px 15px 2px 2px;
}

.card-home-favorite-title {
  align-self: flex-start;
  font-weight: bolder;
}

.card-home-favorite-code {
  align-self: flex-start;
  margin-bottom: 10px;
}

.card-home-favorite-button {
  margin-top: 10px;
  align-self: flex-end;
  border-radius: 30px;
}
</style>
