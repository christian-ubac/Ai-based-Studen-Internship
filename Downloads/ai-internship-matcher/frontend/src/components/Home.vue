<template>
  <section class="home-grid grid md:grid-cols-2 gap-8">
    <UploadResume class="shadow-md" />
    <Recommendations class="shadow-md" />
  </section>
</template>

<script setup>
import UploadResume from './UploadResume.vue'
import Recommendations from './Recommendations.vue'
</script>

<style scoped>
.home-grid { min-height: 60vh; }
</style>
