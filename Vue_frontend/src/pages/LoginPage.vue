<template>
  <div :class="{ 'dark-mode': dark_mode_setting }" class="login-container">
    <!-- Error Message Dropdown -->
    <div v-if="errorMessage" class="error-dropdown">
      {{ errorMessage }}
    </div>

    <!-- Login Form -->
    <form @submit.prevent="onSubmit">
      <div class="form-group">
        <label for="username">Username:</label>
        <input type="text" id="username" v-model="username" required>
      </div>

      <div class="form-group">
        <label for="password">Password:</label>
        <input type="password" id="password" v-model="password" required>
      </div>

      <button type="submit">Login</button>

      <div @click="goToRegistrationPage" class="form-link-div"> 
        <p @click="goToRegistrationPage" class="form-link">New User? Make an Account.</p>
      </div>

      <!-- <LoginWGithub></LoginWGithub> -->

    </form>
  </div>
</template>

<script>
import axios from 'axios';
import LoginWGithub from '@/components/LoginWGithub.vue';

export default {
  components: {
    LoginWGithub
  },
  props: {
    dark_mode_setting: {
      type: Boolean,
      default: false
    }
  },
  data() {
    return {
      username: '',
      password: '',
      errorMessage: ''
    }
  },
  methods: {
    setCookie(name, value, days) {
      let expires = "";
      if (days) {
        const date = new Date();
        date.setTime(date.getTime() + (days * 24 * 60 * 60 * 1000));
        expires = "; expires=" + date.toUTCString();
      }
      document.cookie = name + "=" + (value || "") + expires + "; path=/";
    },
    goToRegistrationPage() {
      this.$router.push('/register');
    },
    async onSubmit() {
      try {
        const url = 'https://indacloudtoo.com/login';
        const response = await axios.post(url, {
          username: this.username,
          password: this.password
        });
        console.log(response);
        // Set a cookie without a library

        this.setCookie('user-token', "testtoken", 7);
        // this.setCookie('user-token', response.data.token, 7);

        // Redirect after successful login
        this.$router.push('/');
      } catch (error) {
        if (error.response) {
          this.errorMessage = error.response.data.message || `Error: ${error.response.status}`;
        } else if (error.request) {
          this.errorMessage = "No response from server";
        } else {
          this.errorMessage = "Error in sending request";
        }

        setTimeout(() => { this.errorMessage = ''; }, 3000);
      }
    }
  }
}
</script>


<style>
.login-container {
  max-width: 300px;
  margin: auto;
  padding: 20px;
  border: 1px solid #ccc;
  border-radius: 5px;
  color: black;
}

.login-container.dark-mode {
  color: white;
}

.form-link-div{
  margin-top: 10px;
}

.form-group {
  margin-bottom: 15px;
}

.form-link {
  font-size: 15px;
  text-decoration: underline;
}

.form-group label {
  display: block;
  margin-bottom: 5px;
}

.form-group input {
  width: 100%;
  padding: 8px;
  border: 1px solid #ccc;
  border-radius: 4px;
}

/* Style for the error dropdown */
.error-dropdown {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  background-color: #ff3333; /* Red background */
  color: white;
  text-align: center;
  padding: 10px;
  z-index: 100;
}
</style>