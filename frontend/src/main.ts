
import './assets/main.css'

import { createApp } from 'vue'
import App from './App.vue'
import router from './router'

import ParticlesPlugin from '@tsparticles/vue3'
import { loadSlim } from '@tsparticles/slim'
import type { Engine } from '@tsparticles/engine'

const app = createApp(App)

app.use(router)

app.use(ParticlesPlugin, {
  init: async (engine: Engine) => {
    await loadSlim(engine)
  }
})

app.mount('#app')
