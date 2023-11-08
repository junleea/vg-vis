import { createRouter, createWebHistory } from 'vue-router'  
import Page1 from '../components/Page1.vue'  
  
const routes = [  
  { path: '/Page1', component: Page1 },  
]  
  
const router = createRouter({  
  history: createWebHistory(),  
  routes,
})  
  
export default router