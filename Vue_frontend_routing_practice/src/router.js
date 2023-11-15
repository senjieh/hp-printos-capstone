import { createRouter, createWebHistory } from 'vue-router';
import Printer1 from './components/Printer1.vue';
import Printer2 from './components/Printer2.vue';
import Home from './components/Home.vue';

const router = createRouter({
    history: createWebHistory(), // This replaces 'mode: 'history'' from Vue 2
    routes: [
        {
            path: '/',
            component: Home
        },
        {
            path: '/printer1',
            component: Printer1
        },
        {
            path: '/printer2',
            component: Printer2
        }
    ]
});

export default router;