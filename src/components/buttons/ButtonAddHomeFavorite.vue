<template>
  <BButton
    class="button button-add-home-favorite outline-black box-shadow-dark"
  >
    <svg
      class="button-add-home-favorite-icon"
      fill="#000000"
      viewBox="0 0 500 500"
      xmlns="http://www.w3.org/2000/svg"
    >
      <path
        d="M306,192h-48v-48c0-4.4-3.6-8-8-8s-8,3.6-8,8v48h-48c-4.4,0-8,3.6-8,8s3.6,8,8,8h48v48c0,4.4,3.6,8,8,8s8-3.6,8-8v-48h48
	c4.4,0,8-3.6,8-8S310.4,192,306,192z"
      />
    </svg>
    <h4>{{ text }}</h4>
  </BButton>
</template>

<script setup lang="ts">
defineProps({
  text: {
    type: String,
    default: "Add Favorites",
  },
});
</script>

<style scoped>
.button-add-home-favorite {
  border-radius: 15px;
  min-width: 300px;
  max-width: 300px;
  align-self: stretch;
}

.button-add-home-favorite-icon {
  width: min-content;
}
</style>
