<script setup>
import { RouterView } from 'vue-router'
</script>

<template>
  <RouterView />
</template>

<style scoped>
/* Hide Vite Inspector overlay button */
.vue-inspector-toggle {
  display: none !important;
}

html, body {
  margin: 0;
  padding: 0;
  font-family: 'Inter', sans-serif;
  background-color: #fff;
}

* {
  box-sizing: border-box;
}
</style>
