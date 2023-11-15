import { createApp } from 'vue';
import App from './App.vue';
import router from './router';
import PrimeVue from 'primevue/config';
import Button from 'primevue/button'
// import InputText from 'primevue/inputtext'
// import Calender from 'primevue/calendar'
// import Chart from 'primevue/chart';
import Card from 'primevue/card';

// import './assets/app.css';
// import 'primevue/resources/themes/arya-purple/theme.css';
// import 'primevue/resources/primevue.min.css';
// import 'primevue/resources/primevue.min.css';               // core css
// import 'primeicons/primeicons.css';                         // icons

const app = createApp(App);
// apply any components to app below
app.use(router);
app.use(PrimeVue);
app.component('PrimeButton', Button);
app.component('PrimeCard', Card);
// allows app to render on page
app.mount('#app');
