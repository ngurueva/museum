import { createApp } from 'vue'
import { createPinia } from 'pinia'
import 'bootstrap/dist/css/bootstrap.min.css'
import 'bootstrap'
import App from './App.vue'
import router from './router'
import axios from 'axios' // ← ВАЖНО!

axios.defaults.withCredentials = true // ← Теперь сработает!

const app = createApp(App)

app.use(createPinia())
app.use(router)

app.mount('#app')
