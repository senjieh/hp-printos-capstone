import { createApp } from 'vue';
import App from './App.vue';
import { createRouter, createWebHistory } from 'vue-router';

// Import PrimeVue and components
import PrimeVue from 'primevue/config';
import Button from 'primevue/button';
import InputText from 'primevue/inputtext';
import Calendar from 'primevue/calendar';
import Chart from 'primevue/chart';
import Card from 'primevue/card';
import InputSwitch from 'primevue/inputswitch';

// Import styles
import './assets/app.css';
import 'primevue/resources/themes/arya-purple/theme.css';
import 'primevue/resources/primevue.min.css';
import 'primeicons/primeicons.css';

// Import your page components
import HomePage from './pages/HomePage.vue';
import PrinterPage from './pages/PrinterPage.vue';
import PrinterDisplay from './pages/PrinterDisplay.vue';
import LoginPage from './pages/LoginPage.vue';
import RegistrationPage from './pages/RegistrationPage.vue';
import UserPage from './pages/UserPage.vue';

// Define routes
const routes = [
  { path: '/', component: HomePage },
  {
    path: '/printers',
    name: 'PrinterList',
    component: PrinterPage,
    meta: { requiresAuth: true },
    props: true
  },
  {
    path: '/printers/:id',
    name: 'PrinterDetails',
    component: PrinterDisplay,
    meta: { requiresAuth: true },
    props: true
  },
  {
    path: '/user',
    name: 'UserPage',
    component: UserPage,
    meta: { requiresAuth: true },
    props: true
  },
  {
    path: '/login',
    name: 'LoginPage',
    component: LoginPage,
    props: true
  },
  {
    path: '/register',
    name: 'RegistrationPage',
    component: RegistrationPage,
    props: true
  }
];

// Create router instance
const router = createRouter({
  history: createWebHistory(),
  routes,
});

function getCookie(name) {
  const nameEQ = name + "=";
  const ca = document.cookie.split(';');
  for(let i=0; i < ca.length; i++) {
    let c = ca[i];
    while (c.charAt(0) === ' ') c = c.substring(1, c.length);
    if (c.indexOf(nameEQ) === 0) return c.substring(nameEQ.length, c.length);
  }
  return null;
}


// Adding beforeEach navigation guard to the router
router.beforeEach((to, from, next) => {
  // Assuming 'user-token' is the name of your auth cookie
  const userToken = getCookie('user-token');

  if (to.matched.some(record => record.meta.requiresAuth) && !userToken) {
    // User is trying to access a protected route without being authenticated
    next({ name: 'LoginPage' });
  } else {
    // Proceed as normal
    next();
  }
});

// Create app instance
const app = createApp(App);

// Use the router
app.use(router);

// Use PrimeVue and register components
app.use(PrimeVue);
app.component('PrimeChart', Chart);
app.component('PrimeCard', Card);
app.component('PrimeCalendar', Calendar);
app.component('PrimeButton', Button);
app.component('InputText', InputText);
app.component('InputSwitch', InputSwitch);

// Mount the app
app.mount('#app');
