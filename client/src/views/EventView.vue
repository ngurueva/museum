<template>
  <div>
    <header style="border-radius: 10px;">
      <h1>{{ event.name }}</h1>
      <button class="book-button" @click="openModal">Забронировать место</button>
    </header>

    <main>
      <img
        v-if="event.image"
        :src="event.image"
        alt="Картинка мероприятия"
        class="event-image"
      />
      <p><strong>Тип мероприятия:</strong> {{ event.event_type }}</p>
      <p><strong>Описание:</strong></p>
      <p>{{ event.description }}</p>
      <p><strong>Максимальное количество участников:</strong> {{ event.capacity }}</p>

      <div v-if="event.schedules && event.schedules.length" class="schedule-block">
        <h3>Расписание:</h3>
        <ul>
          <li v-for="(schedule, index) in event.schedules" :key="index">
            {{ formatDate(schedule.date) }} с {{ schedule.time_start }} до {{ schedule.time_end }}
          </li>
        </ul>
      </div>
      <p v-else style="color: gray;">Нет запланированных дат для этого мероприятия.</p>
    </main>

    <div :class="['modal', { 'modal--visible': showModal }]">
      <div class="modal-content">
        <button class="close-btn" @click="closeModal">×</button>
        <h2>Забронировать место</h2>
        <form @submit.prevent="submitBooking">
          <div class="form-field">
            <label>Имя</label>
            <input v-model="form.name" type="text" required />
          </div>
          <div class="form-field">
            <label>Телефон</label>
            <div style="display: flex; align-items: center;">
              <span class="prefix">+7</span>
              <input
                v-model="form.phone"
                type="text"
                maxlength="10"
                pattern="\d{10}"
                required
                placeholder="9241234567"
                inputmode="numeric"
              />
            </div>
          </div>
          <div class="form-field">
            <label>Email</label>
            <input v-model="form.email" type="email" required />
          </div>
          <button type="submit" class="book-button" style="width: 100%; margin-top: 10px;">
            Забронировать
          </button>
        </form>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import axios from 'axios'

const route = useRoute()
const showModal = ref(false)
const event = ref({
  name: '',
  event_type: '',
  description: '',
  capacity: 0,
  image: '',
  schedules: []
})
const form = ref({
  name: '',
  phone: '',
  email: '',
  telegram_username: ''  // Новое поле для Telegram username
})

const fetchEvent = async () => {
  const eventId = route.params.id
  try {
    const response = await axios.get(`http://localhost:8000/api/events/${eventId}/`)
    console.log('Полученные данные события:', response.data)
    event.value = response.data
  } catch (error) {
    console.error('Ошибка при загрузке события:', error)
  }
}

const formatDate = (dateStr) => {
  const date = new Date(dateStr)
  return date.toLocaleDateString('ru-RU', { day: 'numeric', month: 'long', year: 'numeric' })
}

const openModal = () => {
  console.log('Открытие модального окна')
  showModal.value = true
}

const closeModal = () => {
  showModal.value = false
}

const getCsrfToken = () => {
  const cookieValue = document.cookie
    .split('; ')
    .find(row => row.startsWith('csrftoken='))
    ?.split('=')[1];
  return cookieValue || '';
};

const submitBooking = async () => {
  try {
    // Форматируем телефон перед отправкой
    const formattedPhone = form.value.phone.startsWith('+7') 
      ? form.value.phone 
      : `+7${form.value.phone}`;

    const response = await axios.post('http://localhost:8000/api/book/', {
      name: form.value.name,
      phone: formattedPhone,
      email: form.value.email,
      telegram_username: form.value.telegram_username,
      event_id: route.params.id  // Добавляем ID события
    }, {
      headers: {
        'X-CSRFToken': getCsrfToken(),
        'Content-Type': 'application/json'
      },
      withCredentials: true
    });

    console.log('✅ Сервер ответил:', response.data);
    alert('Заявка отправлена! Письмо отправлено на почту.');
    closeModal();
    
    // Очищаем форму после успешной отправки
    form.value = {
      name: '',
      phone: '',
      email: '',
      telegram_username: ''
    };
  } catch (error) {
    console.error('❌ Полная информация об ошибке:', {
      message: error.message,
      status: error.response?.status,
      data: error.response?.data,
      config: error.config
    });
    
    if (error.response?.status === 403) {
      if (error.response.data?.detail === 'CSRF Failed: CSRF token missing or incorrect.') {
        alert('Ошибка безопасности. Пожалуйста, обновите страницу и попробуйте снова.');
      } else {
        alert('Доступ запрещен. У вас нет прав для этого действия.');
      }
    } else {
      alert('Произошла ошибка. Попробуйте позже.');
    }
  }
};

onMounted(fetchEvent)
</script>
  
  <style scoped>
  body {
    font-family: sans-serif;
    background: #f8f8f8;
    margin: 0;
    padding: 0;
  }
  header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    background: #fff;
    padding: 20px 40px;
    box-shadow: 0 2px 10px rgba(0, 0, 0, 0.05);
  }
  .book-button {
    background-color: #007bff;
    color: white;
    padding: 14px 24px;
    font-size: 16px;
    border: none;
    border-radius: 10px;
    cursor: pointer;
    transition: 0.3s;
  }
  .book-button:hover {
    background-color: #0056b3;
  }
  main {
    max-width: 960px;
    margin: 40px auto;
    background: #fff;
    padding: 30px;
    border-radius: 12px;
    box-shadow: 0 4px 10px rgba(0, 0, 0, 0.05);
  }
  .event-image {
    width: 100%;
    max-height: 400px;
    object-fit: cover;
    border-radius: 10px;
    margin-bottom: 20px;
  }
  .schedule-block {
    background: #f0f0f0;
    padding: 15px;
    border-radius: 8px;
    margin-top: 20px;
  }
  
  /* Modal */
  .modal {
    display: flex;
    position: fixed;
    z-index: 1000;
    left: 0;
    top: 0;
    width: 100%;
    height: 100%;
    background: rgba(0, 0, 0, 0.5);
    align-items: center;
    justify-content: center;
  }
  .modal-content {
    background: #fff;
    padding: 30px;
    border-radius: 12px;
    width: 400px;
    box-shadow: 0 4px 20px rgba(0, 0, 0, 0.2);
  }
  .modal h2 {
    margin-top: 0;
  }
  .form-field {
    margin-bottom: 15px;
  }
  .form-field input {
    width: 100%;
    padding: 10px;
    border: 1px solid #ddd;
    border-radius: 8px;
  }
  .close-btn {
    background: none;
    border: none;
    font-size: 18px;
    float: right;
    cursor: pointer;
  }
  .prefix {
    padding: 8px;
    background: #eee;
    border: 1px solid #ccc;
    border-right: none;
    border-radius: 6px 0 0 6px;
  }
  .modal {
  display: none;
  position: fixed;
  z-index: 1000;
  left: 0; top: 0;
  width: 100%; height: 100%;
  background: rgba(0, 0, 0, 0.5);
  align-items: center;
  justify-content: center;
}

.modal.modal--visible {
  display: flex;
}


  </style>
  