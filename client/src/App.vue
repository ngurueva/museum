<script setup>
import { isAuthenticated } from '@/composables/auth'
</script>

<template>
  <div class="app-container">
    <div class="container">
      <nav class="navbar navbar-expand-lg navbar-light navbar-transparent" style="border-radius: 8px;">
        <div class="container-fluid">
          <router-link class="nav-link" to="/"><img src="../../media/free-icon-museum-1085260.png" style="max-height: 25px;" alt="Музей"></router-link>
          <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNavDropdown" aria-controls="navbarNavDropdown" aria-expanded="false" aria-label="Toggle navigation">
            <span class="navbar-toggler-icon"></span>
          </button>
          <div class="collapse navbar-collapse" id="navbarNavDropdown">
            <ul class="navbar-nav me-auto">
              <li class="nav-item">
                <router-link class="nav-link" to="/">Мероприятия</router-link>
              </li>
              
              <li class="nav-item" v-if="isAuthenticated">
                <router-link class="nav-link" to="/users">Посетители</router-link>
              </li>
              <li class="nav-item" v-if="isAuthenticated">
                <router-link class="nav-link" to="/reservations">Бронирования</router-link>
              </li>
              <li class="nav-item" v-if="isAuthenticated">
                <router-link class="nav-link" to="/reviews">Отзывы</router-link>
              </li>
              <li class="nav-item">
                <router-link class="nav-link" to="/about">О музее</router-link>
              </li>
            </ul>
            <ul class="navbar-nav ms-auto">
              <li class="nav-item" v-if="isAuthenticated">
                <a class="nav-link" href="http://localhost:8000/admin" target="_blank">Админка</a>
              </li>
              <li class="nav-item" v-else>
                <a class="nav-link" href="http://localhost:8000/admin" target="_blank">Войти</a>
              </li>
            </ul>
          </div>
        </div>
      </nav>
      <div class="container content-container">
        <router-view/>
      </div>
    </div>
  </div>
</template>

<style scoped>
.app-container {
  background-color: rgba(230, 211, 211, 0.929);
  background-size: cover;
  background-repeat: no-repeat;
  background-position: center;
  display: flex;
  flex-direction: column;
  min-height: 100vh;
  background-attachment: fixed;
  font-family: 'Segoe UI', sans-serif;
}

.navbar-transparent {
  background-color: rgba(255, 255, 255, 0.95);
  border-radius: 12px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.06);
  padding: 10px 20px;
  transition: background-color 0.3s ease;
  margin-top: 20px;
}

.navbar-light .navbar-nav .nav-link {
  color: #333;
  font-weight: 500;
  padding: 8px 16px;
  border-radius: 8px;
  transition: background-color 0.3s ease, color 0.3s ease;
}

.navbar-light .navbar-nav .router-link-exact-active {
  background-color: #333;
  color: #fff !important;
}

img[alt="Музей"] {
  max-height: 36px;
  margin-right: 10px;
}

.content-container {
  flex-grow: 1;
  margin-top: 30px;
}
</style>
