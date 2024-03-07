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

            <!-- <div class="form-group">
                <label for="email">Email:</label>
                <input type="email" id="email" v-model="email" required>
            </div> -->

            <div class="form-group">
                <label for="password">Password:</label>
                <input :type="showPassword ? 'text' : 'password'" id="password" v-model="password" required>
            </div>
    
            <div class="form-group">
                <label for="retypedPassword">Retype Password:</label>
                <input :type="showPassword ? 'text' : 'password'" id="retypedPassword" v-model="retypedPassword" required>
            </div>
    
            <div class="form-group">
                <input type="checkbox" id="showPassword" v-model="showPassword">
                <label for="showPassword">Show Password</label>
            </div>
    
            <button type="submit">Register</button>
            <div @click="goToLoginPage" class="form-link-div"> 
                <p @click="goToLoginPage" class="form-link">Have an account? Log-In</p>
            </div>
        </form>
    </div>
</template>
  
<script>
import axios from 'axios';
  export default {
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
        retypedPassword: '',
        email: '',
        showPassword: false,
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
        goToLoginPage() {
            this.$router.push('/login');
        },
        async onSubmit() {
            if (this.password !== this.retypedPassword) {
                this.errorMessage = "Passwords do not match.";
                setTimeout(() => { this.errorMessage = ''; }, 3000);
                return;
            }
    

            const url = 'http://localhost:8080/registration';
            const response = await axios.post(url, {
              username: this.username,
              password: this.password,
              //email: this.email
            });
            console.log(response);


        // Temp
            this.setCookie('user-token', "testtoken", 7); // Example: Set a cookie for 7 days
    
            // Redirect after successful registration
            this.$router.push('/');
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
    .form-link-div{
        margin-top: 10px;
    }
    
    .login-container.dark-mode {
        color: white;
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