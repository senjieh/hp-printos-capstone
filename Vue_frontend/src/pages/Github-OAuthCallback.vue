<template>
    <div class="oauth-callback">
      Redirecting...
    </div>
  </template>
  
  <script>
  export default {
    name: 'OAuthCallback',
    mounted() {
      const code = this.$route.query.code;
      if (code) {
        this.sendCodeToBackend(code);
      } else {
        console.error('No code found in callback URL');
        // Handle error, perhaps redirect to login page
      }
    },
    methods: {
      async sendCodeToBackend(code) {
        try {
          // Replace with your backend endpoint that handles the authorization code
          const response = await this.$axios.post('http://localhost:8080/gh-oauth', { code });
          console.log(response);
          // Assuming the backend responds with a JWT
          const jwt = response.data.jwt;
          // Store JWT in local storage, cookie, or however you prefer
          localStorage.setItem('jwt', jwt);
          // Redirect to the home page or dashboard
          this.$router.push('/');
        } catch (error) {
          console.error('Failed to exchange code for token', error);
          // Handle failure, e.g., redirect to the login page
        }
      }
    }
  };
  </script>
  