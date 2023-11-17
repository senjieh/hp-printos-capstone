<script>
import NavBar from '@/components/NavBar.vue'; 

export default {
  components: {
    NavBar
  }
}
</script>

<template>
  <div class="h-container">
    <NavBar/>
    <router-view/>
  </div>
</template>
