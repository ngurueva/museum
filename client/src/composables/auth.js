// src/composables/auth.js
import { ref } from 'vue'
import axios from 'axios'

export const isAuthenticated = ref(false)

export const checkAuth = async () => {
  try {
    const response = await axios.get('http://localhost:8000/api/is_authenticated/', {
      withCredentials: true, // обязательно для отправки cookies (сессия)
    })
    isAuthenticated.value = response.data.authenticated
  } catch (e) {
    isAuthenticated.value = false
  }
}
