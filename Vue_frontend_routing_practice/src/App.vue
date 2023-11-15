<template>
    <div class="nav-bar">
      <PrimeButton label="Home" @click="goToHome"></PrimeButton>
    </div>
    <div class="printer-container">
      <PrimeCard class="printer-card" @click="goToPrinter1">
        <template #title>
          <h1>Printer 1</h1>
        </template>
      </PrimeCard>
      <PrimeCard class="printer-card" @click="goToPrinter2">
        <template #title>
          <h1>Printer 2</h1>
        </template>
      </PrimeCard>
    </div>
    <router-view/>
</template>

<script>
import { useRouter } from 'vue-router';
export default {
  name: 'App',
  setup() {
    const router = useRouter();

    function goToHome() {
      router.push('/');
    }

    function goToPrinter1() {
      router.push('/printer1');
    }

    function goToPrinter2() {
      router.push('/printer2');
    }

    return { goToHome, goToPrinter1, goToPrinter2 };
  }
}
</script>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  margin-top: 60px;
}
.nav-bar {
  background-color: #000000; /* Dark blue background */
  padding: 10px 0; /* Top and bottom padding */
  display: flex; /* Use flexbox for layout */
  flex-direction: column; /* Stack items vertically */
  align-items: center; /* Center the items horizontally */
  height: 100vh; /* Full height of the viewport */
  width: 100px; /* Width of the nav bar */
  position: fixed; /* Fixed on the side */
  top: 0; /* Align to the top */
  left: 0; /* Align to the left */
  z-index: 1000; /* Ensure it's above other content */
  box-shadow: 2px 0 5px rgba(0, 0, 0, 0.1); /* Shadow on the right side */
}
.printer-container{
  display: flex;
  justify-content: flex-start; /* Aligns cards to the start of the container */
  align-items: flex-start; /* Aligns cards to the top */
  gap: 10px; /* How far apart each card should be */
  margin: 120px; /* To avoid having printer cards overlap with navbar */
}
.printer-card{
  border: 1.5px solid #000000;
  padding: .75rem 1.25rem;
}
</style>
