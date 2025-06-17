<template>
  <section id="vw_splashart">Splashart</section>
</template>
<script setup lang="ts">
import { onMounted } from "vue";

const emits = defineEmits(["done"]);

onMounted(async () => {
  setTimeout(() => emits("done"), 2000);
});
</script>
<style scoped></style>
