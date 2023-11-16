import { createRouter, createWebHistory } from 'vue-router'
import Page1 from '../components/Page1.vue'
import Page2 from '../components/Page2.vue'
import Page3 from '../components/Page3.vue'
import Page4 from '../components/Page4.vue'
import App from '../App.vue'
const routes = [
  { path: '/', component: App },
  { path: '/Page1', component: Page1 },
  { path: '/Page2', component: Page2 },
  { path: '/Page3', component: Page3 },
  { path: '/Page4', component: Page4 },
]

const router = createRouter({
  history: createWebHistory(),
  routes,
})

export default router