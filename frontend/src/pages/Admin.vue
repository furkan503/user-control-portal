<template>
  <div class="admin-container">
    <div class="sidebar">
      <h2>Admin Panel</h2>
      <router-link to="/admin/users" class="sidebar-link">Manage Users</router-link>
      <router-link to="/admin/add" class="sidebar-link">Manage Admin</router-link>
      <button @click="logout" class="sidebar-button">Logout</button>
    </div>
    <div class="content">
      <h2>Admin Page</h2>
      <router-view></router-view>
    </div>
  </div>
</template>

<script>
export default {
  methods: {
    logout() {
      localStorage.removeItem('accessToken');
      localStorage.removeItem('refreshToken');
      this.$router.push('/login');
    }
  }
}
</script>

<style scoped>
.admin-container {
  display: flex;
  max-width: 1200px; /* Adjust max-width as needed */
  margin: 20px auto;
  overflow: hidden; /* Prevents horizontal scrollbars */
}

.sidebar {
  width: 20%;
  padding: 20px;
  background-color: #f5f5f5;
  border-right: 1px solid #ccc;
  position: fixed; /* Fixes the sidebar */
  left: 0; /* Positions sidebar at the left edge */
  top: 0; /* Ensures sidebar starts at the top */
  bottom: 0; /* Expands sidebar to the bottom */
}

.content {
  flex: 1;
  padding: 20px;
  margin-left: 20%; /* Adjusts content margin to accommodate sidebar width */
}

.sidebar h2 {
  margin-bottom: 20px;
  font-size: 24px;
}

.sidebar-link {
  display: block;
  padding: 10px 20px;
  background-color: blueviolet;
  color: white;
  text-decoration: none;
  border-radius: 3px;
  font-size: 16px;
  margin-bottom: 10px;
}

.sidebar-link:hover {
  background-color: #8a2be2; /* Darker shade of blueviolet on hover */
}

.sidebar-button {
  width: 100%;
  padding: 10px 20px;
  background-color: #f44336;
  color: white;
  border: none;
  border-radius: 3px;
  font-size: 16px;
  cursor: pointer;
  margin-top: 20px;
}

.sidebar-button:hover {
  background-color: #d32f2f; /* Darker shade of red on hover */
}
</style>
