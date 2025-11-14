import { createApp } from 'vue'
import App from './App.vue'
import './style.css'
import * as lucide from 'lucide-vue-next'
import router from './router'

const app = createApp(App)
for (const [name, component] of Object.entries(lucide)) {
  app.component(`i-lucide-${name.toLowerCase()}`, component)
}

app.use(router)
app.mount('#app')
