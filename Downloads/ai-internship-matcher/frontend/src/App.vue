<template>
  <div class="flex flex-col items-center py-10">
    <div class="w-full max-w-5xl bg-white/70 backdrop-blur-md rounded-2xl shadow-lg p-6 sm:p-10 border border-green-200">
      <header class="flex flex-col md:flex-row justify-between items-center mb-6 md:mb-8" role="banner">
        <h1 class="text-2xl sm:text-4xl font-bold text-green-700 flex items-center gap-3">
          <Logo size="w-8 h-8" :label="'AI Internship Matcher logo'" />
          <span>AI Internship Matcher</span>
        </h1>
        <p class="text-gray-500 italic mt-3 md:mt-0">Empowered by Deep Learning &amp; LLM</p>
      </header>

      <hr class="mb-6 md:mb-8 border-green-300" />

      <main class="min-h-[60vh]">
        <router-view />
      </main>

      <footer class="mt-8 text-center text-sm text-gray-500" role="contentinfo">
        © {{ new Date().getFullYear() }} CCIS Internship Matcher | Developed by Christian Ubac
      </footer>
    </div>
  </div>
</template>

<script setup>
import Logo from './components/Logo.vue'
</script>
