<template>
  <div class="flex flex-col items-center py-10">
    <div class="w-full max-w-5xl bg-white/70 backdrop-blur-md rounded-2xl shadow-lg p-10 border border-green-200">
      <div class="flex flex-col md:flex-row justify-between items-center mb-8">
        <h1 class="text-4xl font-bold text-green-700 flex items-center gap-2">
          <i-lucide-briefcase class="w-8 h-8" />
          AI Internship Matcher
        </h1>
        <p class="text-gray-500 italic">Empowered by Deep Learning & LLM</p>
      </div>

      <hr class="mb-8 border-green-300" />

      <div class="grid md:grid-cols-2 gap-8">
        <UploadResume class="shadow-md" />
        <Recommendations class="shadow-md" />
      </div>

      <footer class="mt-10 text-center text-sm text-gray-500">
        © {{ new Date().getFullYear() }} CCIS Internship Matcher | Developed by Christian Ubac
      </footer>
    </div>
  </div>
</template>

<script setup>
import { Briefcase } from "lucide-vue-next"
import UploadResume from './components/UploadResume.vue'
import Recommendations from './components/Recommendations.vue'
</script>
