import { createApp } from 'vue'
import App from './App.vue'
import PrimeVue from 'primevue/config'
import Button from 'primevue/button'
import InputText from 'primevue/inputtext'
import Calender from 'primevue/calendar'
import Chart from 'primevue/chart';

import './assets/app.css';
import 'primevue/resources/themes/arya-purple/theme.css';
import 'primevue/resources/primevue.min.css';
import 'primevue/resources/primevue.min.css';               // core css
import 'primeicons/primeicons.css';                         // icons


const app = createApp(App)
app.use(PrimeVue);

app.component('PrimeChart', Chart);
app.component('PrimeCalender', Calender);
app.component('PrimeButton', Button);
app.component('InputText', InputText);
app.mount('#app')