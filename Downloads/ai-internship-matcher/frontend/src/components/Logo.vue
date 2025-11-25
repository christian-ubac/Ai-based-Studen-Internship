<template>
  <svg
    :class="sizeClass"
    viewBox="0 0 24 24"
    fill="none"
    xmlns="http://www.w3.org/2000/svg"
    role="img"
    :aria-hidden="!label"
  >
    <title v-if="label">{{ label }}</title>
    <rect x="3" y="7" width="18" height="10" rx="2" :stroke="color" stroke-width="1.5" :fill="fillColor" opacity="0.15" />
    <path d="M8 7V6a4 4 0 0 1 8 0v1" :stroke="color" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" />
    <path d="M3 11h18" :stroke="color" stroke-width="1.5" stroke-linecap="round" />
  </svg>
</template>

<script setup>
import { computed } from 'vue'

const props = defineProps({
  size: { type: String, default: 'w-8 h-8' },
  color: { type: String, default: '#16a34a' },
  fillColor: { type: String, default: '#22c55e' },
  label: { type: String, default: 'AI Internship Matcher logo' }
})

const sizeClass = computed(() => props.size)
</script>

<style scoped>
svg { display: inline-block; vertical-align: middle; }
</style>
