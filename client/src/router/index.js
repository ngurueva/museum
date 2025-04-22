import { createRouter, createWebHistory } from 'vue-router'
import EventsView from '@/views/EventsView.vue'
import EventView from '@/views/EventView.vue'
import ReviewsView from '@/views/ReviewsView.vue'
import UsersView from '@/views/VisitorsView.vue'
import ReservationsView from '@/views/ReservationsView.vue'
import AboutView from '@/views/AboutView.vue'
import VisitorsView from '@/views/VisitorsView.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'EventsView',
      component: EventsView
    },
    {
      path: '/events/:id',
      name: 'EventView',
      component: EventView
    },
    {
      path: '/reviews', 
      name: 'ReviewsView',
      component: ReviewsView
    },
    {
      path: '/visitors', 
      name: 'VisitorsView',
      component: VisitorsView
    },
    {
      path: '/reservations', 
      name: 'ReservationsView',
      component: ReservationsView
    },
    {
      path: '/about', 
      name: 'AboutView',
      component: AboutView
    }
  ]
})

export default router
