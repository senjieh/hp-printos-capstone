<script>
import NavBar from '@/components/NavBar.vue'; 
import { state } from '@/store/store.js'; 

export default {
  components: {
    NavBar
  },
  setup() {
    return { state };
  }
}
</script>

<template>
  <div :class="{ 'dark-mode': state.isDarkMode }" class="main-h-container">
    <NavBar :dark_mode_setting = state.isDarkMode />
    <router-view :dark_mode_setting = state.isDarkMode />
  </div>
</template>
