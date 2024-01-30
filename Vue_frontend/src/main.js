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

// Define routes
const routes = [
  { path: '/', component: HomePage },
  {
    path: '/printers',
    name: 'PrinterList',
    component: PrinterPage,
    props: true
  },
  {
    path: '/printers/:id',
    name: 'PrinterDetails',
    component: PrinterDisplay,
    props: true
  },
  {
    path: '/login',
    name: 'LoginPage',
    component: LoginPage,
    props: true
  }
];

// Create router instance
const router = createRouter({
  history: createWebHistory(),
  routes,
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
