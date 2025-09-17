<template>
  <div class="login-container">
    <h2>Login</h2>
    <form @submit.prevent="login" class="login-form">
      <label>Username:</label>
      <input type="text" v-model="username" required><br><br>
      <label>Password:</label>
      <input type="password" v-model="password" required><br><br>
      <button type="submit">Login</button>
      <router-link to="/users" class="users">Go to Users Page</router-link>
    </form>
  </div>
</template>

<script>
export default {
  data() {
    return {
      username: '',
      password: '',
    };
  },
  methods: {
    async login() {
      try {
        const response = await fetch('http://127.0.0.1:8000/api/login/custom_login/', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({
            username: this.username,
            password: this.password
          })
        });

        console.log('HTTP status:', response.status);

        if (response.ok) {
          const data = await response.json();
          if (data.access != undefined) {
              localStorage.setItem('accessToken', data.access); 
              localStorage.setItem('refreshToken', data.refresh);
              this.$router.push('/admin');
              console.log('Login response:', data.message);
          }
        } else {
          console.log('Login failed');
        }
      } catch (error) {
        console.error('Login failed:', error);
        alert('An error occurred while logging in.');
      }
    }
  }
}
</script>

<style scoped>
.login-container {
  max-width: 400px;
  margin: 0 auto;
  padding: 20px;
  border: 1px solid #ccc;
  border-radius: 5px;
  background-color: #f9f9f9;
}

h2 {
  text-align: center;
}

.login-form {
  display: flex;
  flex-direction: column;
}

label {
  margin-bottom: 10px;
}

input[type="text"],
input[type="password"] {
  padding: 10px;
  margin-bottom: 15px;
  border: 1px solid #ccc;
  border-radius: 3px;
  font-size: 16px;
}

button {
  padding: 10px 20px;
  background-color: blueviolet;
  color: white;
  border: none;
  border-radius: 3px;
  font-size: 16px;
  cursor: pointer;
}

button:hover {
  background-color: blueviolet;
}

.users {
  padding: 10px 20px;
  color: blueviolet;
  border: none;
  border-radius: 3px;
  font-size: 16px;
  cursor: pointer;
  text-decoration: none;
}
</style>
