 <template>
<div>
  <!-- Кнопка "Добавить" -->
  <div v-if="isAuthenticated" class="mb-3">
    <button @click="openModal()" class="btn btn-success btn-sm">
      ➕ Добавить мероприятие
    </button>
  </div>


    <div v-if="loading">Загрузка...</div>
    <div v-else>
      <ul class="event-list">
        <li
          v-for="item in events"
          :key="item.id"
          :class="['event-card', isAuthenticated && !item.is_visible ? 'hidden' : '']"
        >
        
          <div class="event-link" @click="goToEvent(item.id)">
            <img v-if="item.image" :src="item.image" alt="Картинка" class="event-image" />
            <div class="event-details">
              <h2>{{ item.name }}</h2>
              <p><strong>Тип:</strong> {{ item.event_type }}</p>
              <p><strong>Места:</strong> {{ item.capacity }}</p>
              <p v-if="isAuthenticated"><strong>Статус:</strong> {{ item.is_visible ? "Видимо" : "Скрыто" }}</p>

              <div v-if="item.schedules && item.schedules.length > 0" class="schedule-box">
                <p><strong>📅 Ближайшее мероприятие:</strong></p>
                
                <!-- Find the nearest schedule -->
                <p v-if="item.nearest_schedule">
                  {{ formatDate(item.nearest_schedule.date) }}
                  с {{ item.nearest_schedule.time_start.slice(0, 5) }}
                  до {{ item.nearest_schedule.time_end.slice(0, 5) }}
                </p>
                <p v-else style="color: gray;">Нет предстоящих дат.</p>

              </div>

              <!-- Внутри карточки мероприятия -->
              <div v-if="isAuthenticated" class="mt-3 d-flex gap-2 flex-wrap">
                <button @click.stop="openModal(item)" class="btn btn-outline-primary btn-sm">
                  ✏️ Редактировать
                </button>
                <button @click.stop="toggleVisibility(item)" class="btn btn-outline-warning btn-sm">
                  {{ item.is_visible ? '🙈 Скрыть' : '👁 Показать' }}
                </button>
                <button @click.stop="onRemoveClick(item)" class="btn btn-outline-danger btn-sm">
                  🗑 Удалить
                </button>
              </div>


            </div>
          </div>
        </li>
      </ul>
    </div>

    <!-- Модальное окно -->
    <div class="modal fade" id="eventModal" tabindex="-1">
      <div class="modal-dialog modal-lg">
        <div class="modal-content">
          <form @submit.prevent="submitEvent">
            <div class="modal-header">
              <h5 class="modal-title">{{ modalEvent.id ? 'Редактировать' : 'Добавить' }} мероприятие</h5>
              <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
            </div>
            <div class="modal-body">
              <div class="mb-3">
                <label>Название</label>
                <input v-model="modalEvent.name" class="form-control" required />
              </div>
              <div class="mb-3">
                <label>Описание</label>
                <textarea v-model="modalEvent.description" class="form-control" required></textarea>
              </div>
              <div class="mb-3">
                <label>Тип</label>
                <input v-model="modalEvent.event_type" class="form-control" required />
              </div>
              <div class="mb-3">
                <label>Количество мест</label>
                <input v-model="modalEvent.capacity" type="number" class="form-control" required />
              </div>
              <div class="mb-3">
                <label>Изображение</label>
                <input type="file" class="form-control" @change="e => imageFile = e.target.files[0]" />
              </div>
              <div class="mt-4">
  <h5>Расписание</h5>
  <div v-for="(s, idx) in modalEvent.schedules" :key="idx" class="d-flex align-items-end gap-2 mb-2">
    <div>
      <label>Дата</label>
      <input type="date" v-model="s.date" class="form-control" required />
    </div>
    <div>
      <label>Начало</label>
      <input type="time" v-model="s.time_start" class="form-control" required />
    </div>
    <div>
      <label>Конец</label>
      <input type="time" v-model="s.time_end" class="form-control" required />
    </div>
    <button type="button" class="btn btn-outline-danger" @click="removeSchedule(idx)">🗑</button>
  </div>

  <button type="button" class="btn btn-outline-secondary btn-sm" @click="addSchedule">
    ➕ Добавить расписание
  </button>
</div>

            </div>
            <div class="modal-footer">
              <button type="submit" class="btn btn-primary">Сохранить</button>
              <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Отмена</button>
            </div>
          </form>
        </div>
      </div>
    </div>
  </div>
</template>


<script setup>
import { ref, onMounted } from 'vue'
import axios from 'axios'
import Cookies from 'js-cookie'
import { Modal } from 'bootstrap'
import { useRouter } from 'vue-router'
import { checkAuth, isAuthenticated } from '@/composables/auth'

const events = ref([])  // Хранение списка мероприятий
const loading = ref(false)  // Статус загрузки
const modalEvent = ref({})  // Событие для модального окна
const imageFile = ref(null)  // Изображение для модального окна
let modalInstance = null  // Инстанс модального окна
const router = useRouter()

const goToEvent = (id) => {
  router.push(`/events/${id}`)
}

const fetchEvents = async () => {
  loading.value = true
  try {
    const { data } = await axios.get('/api/events/', {
      withCredentials: true,
    })

    // фильтруем только для НЕавторизованных
    events.value = isAuthenticated.value
      ? data
      : data.filter(item => item.is_visible)

  } catch (e) {
    console.error('Ошибка загрузки:', e)
  } finally {
    loading.value = false
  }
}


// Форматируем дату
const formatDate = (dateStr) => {
  const date = new Date(dateStr)
  return date.toLocaleDateString('ru-RU', { day: 'numeric', month: 'long', year: 'numeric' })
}

// Открытие модального окна для добавления/редактирования
const openModal = (event = null) => {
  modalEvent.value = event
    ? { ...event, schedules: event.schedules ? [...event.schedules] : [] }
    : {
        name: '',
        description: '',
        event_type: '',
        capacity: null,
        is_visible: true,
        schedules: []
      }

  imageFile.value = null
  if (!modalInstance) {
    modalInstance = new Modal(document.getElementById('eventModal'))
  }
  modalInstance.show()
}

// Добавление нового расписания
const addSchedule = () => {
  modalEvent.value.schedules.push({ date: '', time_start: '', time_end: '' })
}

// Удаление расписания
const removeSchedule = (idx) => {
  modalEvent.value.schedules.splice(idx, 1)
}

const toggleVisibility = async (event) => {
  const originalVisibility = event.is_visible;
  try {
    const response = await axios.patch(`/api/events/${event.id}/`, {
      is_visible: !originalVisibility
    }, {
      headers: {
        'X-CSRFToken': Cookies.get('csrftoken'),
      },
    });

    // Найти индекс события
    const index = events.value.findIndex(e => e.id === event.id);
    if (index !== -1) {
      // Обновляем локально
      events.value[index] = response.data;
    }
  } catch (e) {
    console.error('Ошибка изменения видимости:', e);
    alert('Не удалось изменить видимость. Попробуйте позже.');
  }
};






const onRemoveClick = async (event) => {
  if (!confirm('Удалить мероприятие?')) return;

  try {
    const response = await axios.delete(`/api/events/${event.id}/`, {
      headers: {
        'X-CSRFToken': Cookies.get('csrftoken'),
      },
      withCredentials: true,
    });

    console.log('Удаление успешно:', response.data);  // отладка

    // Обновляем список мероприятий
    await fetchEvents();
  } catch (e) {
    console.error('Ошибка при удалении:', e);
  }
};

const submitEvent = async () => {
  // Проверка на обязательные поля
  if (!modalEvent.value || !modalEvent.value.name || !modalEvent.value.capacity) {
    console.error("Данные для события неполные!");
    return; // Останавливаем выполнение
  }

  try {
    const response = await axios.post("/api/events/", modalEvent.value, {
      headers: {
        'X-CSRFToken': Cookies.get('csrftoken'), // Проверка CSRF токена
      },
      withCredentials: true, // Убедитесь, что куки отправляются с запросом
    });

    console.log(response.data); // Ответ от сервера
  } catch (error) {
    console.error("Ошибка при отправке запроса: ", error);
    if (error.response) {
      console.error("Ответ сервера с ошибкой: ", error.response.data);
    } else {
      console.error("Ошибка запроса: ", error.message);
    }
  }
};

onMounted(async () => {
  await checkAuth();   
  await fetchEvents();   
});

</script>


<style scoped>
@import 'bootstrap/dist/css/bootstrap.min.css';

body {
  font-family: 'Segoe UI', sans-serif;
  background: #f5f7fa;
  padding: 20px;
}

h1 {
  text-align: center;
  margin-bottom: 30px;
  font-weight: 700;
}

.btn-success {
  font-weight: 500;
  padding: 8px 16px;
}

.event-list {
  list-style: none;
  max-width: 1000px;
  margin: 0 auto;
  padding: 0;
}

.event-card {
  background: #ffffff;
  border-radius: 16px;
  padding: 20px;
  margin-bottom: 24px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.06);
  transition: transform 0.2s ease, box-shadow 0.2s ease;
}

.event-card:hover {
  transform: translateY(-3px);
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.08);
}

.event-link {
  display: flex;
  gap: 20px;
  align-items: flex-start;
}

.event-image {
  width: 260px;
  height: 160px;
  object-fit: cover;
  border-radius: 12px;
}

.event-details {
  flex: 1;
}

.event-details h2 {
  margin-top: 0;
  font-size: 1.5rem;
  margin-bottom: 10px;
}

.event-details p {
  margin-bottom: 8px;
  color: #333;
}

.schedule-box {
  background: #f0f4f8;
  padding: 10px 14px;
  border-radius: 10px;
  margin-top: 12px;
  font-size: 0.95rem;
  color: #444;
}

.mt-2 button {
  margin-right: 8px;
}

.modal-content {
  border-radius: 16px;
}

.modal-title {
  font-weight: bold;
}

.modal-body label {
  font-weight: 500;
  margin-bottom: 4px;
}

.modal-body input,
.modal-body textarea {
  border-radius: 10px;
}

.modal-body textarea {
  resize: vertical;
  min-height: 80px;
}

.schedule-box strong {
  display: block;
  margin-bottom: 4px;
}

.schedule-section {
  margin-top: 20px;
}

.schedule-section h5 {
  font-weight: 600;
}

.event-card.hidden {
  opacity: 0.5;
}

.schedule-section .form-control {
  border-radius: 8px;
}

.schedule-section button {
  margin-left: 8px;
}


body {
  font-family: sans-serif;
  background: #f8f8f8;
  padding: 20px;
}
h1 {
  text-align: center;
}
ul {
  list-style: none;
  max-width: 960px;
  margin: 0 auto;
  padding: 0;
}
li {
  background: #fff;
  margin-bottom: 30px;
  padding: 20px;
  border-radius: 12px;
  display: flex;
  gap: 20px;
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.05);
}
.event-image {
  width: 250px;
  height: 160px;
  object-fit: cover;
  border-radius: 10px;
}
.event-details {
  flex: 1;
}
.schedule {
  margin-top: 10px;
  background-color: #f0f0f0;
  padding: 10px;
  border-radius: 8px;
}
.empty-message {
  text-align: center;
  color: #999;
  margin-top: 40px;
}
.event-list {
  list-style: none;
  max-width: 960px;
  margin: 0 auto;
  padding: 0;
}

.event-card {
  margin-bottom: 30px;
  border-radius: 12px;
  overflow: hidden;
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.05);
}

.event-link {
  display: flex;
  flex-direction: row;
  text-decoration: none;
  color: inherit;
  width: 100%;
  background: #fff;
  padding: 20px;
  box-sizing: border-box;
}

.event-link:hover {
  background: #f9f9f9;
}

.event-image {
  width: 250px;
  height: 160px;
  object-fit: cover;
  border-radius: 10px;
  flex-shrink: 0;
}

.event-details {
  flex: 1;
  padding-left: 20px;
}

.schedule-box {
  margin-top: 10px;
  background-color: #f0f0f0;
  padding: 10px;
  border-radius: 8px;
  width: 100%;
  box-sizing: border-box;
}

.empty-message {
  text-align: center;
  color: #999;
  margin-top: 40px;
}
</style>
