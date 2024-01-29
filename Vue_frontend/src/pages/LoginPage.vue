<template>
  <div class="login-container">
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
    </form>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  data() {
    return {
      username: '',
      password: '',
      errorMessage: ''
    }
  },
  methods: {
    async onSubmit() {
      try {
        const url = 'http://ec2-3-145-70-195.us-east-2.compute.amazonaws.com/printers/1/printer-details'; // Replace with your actual URL
        const response = await axios.post(url, {
          username: this.username,
          password: this.password
        });

        console.log(response.data);
      } catch (error) {
        // Check if the error is a response from the server
        if (error.response) {
          // Server responded with a status code outside the 2xx range
          this.errorMessage = error.response.data.message || `Error: ${error.response.status}`;
        } else if (error.request) {
          // The request was made but no response was received
          this.errorMessage = "No response from server";
        } else {
          // Something happened in setting up the request that triggered an Error
          this.errorMessage = "Error in sending request";
        }

        setTimeout(() => { this.errorMessage = ''; }, 3000); // Clear the message after 3 seconds
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
}

.form-group {
  margin-bottom: 15px;
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