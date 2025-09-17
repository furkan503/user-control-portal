<template>
  <div class="admin-container">
    <div class="content">
      <h2>Manage Users</h2>

      <div class="search-bar">
        <input type="text" v-model="searchQuery" placeholder="Search users...">
      </div>

      <div class="table-container">
        <table class="user-table">
          <thead>
            <tr>
              <th>Name</th>
              <th>Email</th>
              <th>Phone</th>
              <th>Street</th>
              <th>Suite</th>
              <th>City</th>
              <th>Company</th>
              <th>Website</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="user in paginatedUsers" :key="user.id" @click="goToUserDetails(user.id)">
              <td>{{ user.name }}</td>
              <td>{{ user.email }}</td>
              <td>{{ user.phone }}</td>
              <td>{{ user.address.street }}</td>
              <td>{{ user.address.suite }}</td>
              <td>{{ user.address.city }}</td>
              <td>{{ user.company.name }}</td>
              <td>{{ user.website }}</td>
            </tr>
          </tbody>
        </table>
      </div>

      <div class="pagination">
        <button v-for="page in totalPages" :key="page" @click="goToPage(page)" :class="{ active: page === currentPage }">
          {{ page }}
        </button>
      </div>

      <form v-if="canViewUser" @submit.prevent="addUser" class="add-user-form">
        <h3>Add New User</h3>
        <label for="newUserName">Name:</label>
        <input id="newUserName" v-model="newUser.name" type="text" required>
        <label for="newUserEmail">Email:</label>
        <input id="newUserEmail" v-model="newUser.email" type="email" required>
        <label for="newUserphone">Phone:</label>
        <input id="newUserphone" v-model="newUser.phone" type="text">
        <label for="newUserstreet">Street:</label>
        <input id="newUserstreet" v-model="newUser.address.street" type="text">
        <label for="newUsersuite">Suite:</label>
        <input id="newUsersuite" v-model="newUser.address.suite" type="text">
        <label for="newUsercity">City:</label>
        <input id="newUsercity" v-model="newUser.address.city" type="text">
        <label for="newUsercompany">Company:</label>
        <input id="newUsercompany" v-model="newUser.company.name" type="text">
        <label for="newUserwebsite">Website:</label>
        <input id="newUserwebsite" v-model="newUser.website" type="text">
        <button type="submit">Add User</button>
      </form>
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      users: [],
      paginatedUsers: [],
      newUser: {
        name: '',
        email: '',
        phone: '',
        address: {
          street: '',
          suite: '',
          city: '',
        },
        company: {
          name: '',
        },
        website: ''
      },
      canViewUser: false,
      searchQuery: '',
      currentPage: 1,
      pageSize: 5
    };
  },
  watch: {
    searchQuery() {
      this.currentPage = 1;
      this.applyPagination();
    },
    users() {
      this.applyPagination();
    }
  },
  created() {
    this.fetchUsers();
  },
  async mounted() {
    await this.checkUserPermission();
  },
  computed: {
    filteringUsers() {
      if (!this.searchQuery) {
        return this.users;
      }
      return this.users.filter(user =>
        user.name.toLowerCase().includes(this.searchQuery.toLowerCase()) ||
        user.email.toLowerCase().includes(this.searchQuery.toLowerCase())
      );
    },
    totalPages() {
      return Math.ceil(this.filteringUsers.length / this.pageSize);
    }
  },
  methods: {
    async checkUserPermission() {
      const permission = 'user.change_user';
      this.canViewUser = await this.checkPermissionUser(permission);
    },
    async checkPermissionUser(permission) {
      const token = localStorage.getItem('accessToken');
      if (!token) {
        return false;
      }

      try {
        const response = await fetch(`http://127.0.0.1:8000/api/users/check_permission/?permission=${permission}`, {
          method: 'GET',
          headers: {
            'Authorization': `Bearer ${token}`,
            'Content-Type': 'application/json'
          }
        });

        const data = await response.json();
        return data.has_permission;
      } catch (error) {
        console.error('Error checking permissions:', error);
        return false;
      }
    },
    async fetchUsers(url = 'http://127.0.0.1:8000/api/users/') {
      try {
        const token = localStorage.getItem('accessToken');
        let allUsers = [];
        let nextUrl = url;

        while (nextUrl) {
          const response = await fetch(nextUrl, {
            headers: {
              'Authorization': `Bearer ${token}`,
            }
          });
          const data = await response.json();
          allUsers = allUsers.concat(data.results);
          nextUrl = data.next;
        }

        this.users = allUsers;
        this.applyPagination();
      } catch (error) {
        console.error('Error fetching users:', error);
      }
    },
    applyPagination() {
      const start = (this.currentPage - 1) * this.pageSize;
      const end = start + this.pageSize;
      this.paginatedUsers = this.filteringUsers.slice(start, end);
    },
    goToPage(page) {
      this.currentPage = page;
      this.applyPagination();
    },
    goToUserDetails(userId) {
      this.$router.push(`/admin/users/${userId}/`);
    },
    goToManageUsers() {
      this.$router.push('/admin/users');
    },
    goToManageAdmin() {
      this.$router.push('/admin/add');
    },
    async addUser() {
      try {
        const userPayload = {
          name: this.newUser.name,
          email: this.newUser.email,
          phone: this.newUser.phone,
          website: this.newUser.website,
          address: {
            street: this.newUser.address.street,
            suite: this.newUser.address.suite,
            city: this.newUser.address.city,
          },
          company: {
            name: this.newUser.company.name,
          }
        };

        const token = localStorage.getItem('accessToken');
        const response = await fetch('http://127.0.0.1:8000/api/users/multiple/', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${token}`
          },
          body: JSON.stringify([userPayload]),
        });

        if (response.ok) {
          alert('User added successfully');
          this.fetchUsers();
          this.resetForm();
        } else {
          alert('Failed to add user');
        }
      } catch (error) {
        console.error('Error adding user:', error);
      }
    },
    resetForm() {
      this.newUser = {
        name: '',
        email: '',
        phone: '',
        address: {
          street: '',
          suite: '',
          city: '',
        },
        company: {
          name: '',
        },
        website: ''
      };
    }
  }
};
</script>

<style scoped>
/* Sidebar */

.table-container {
  overflow-x: scroll;
  width: 900px;
}

.admin-container {
  display: flex;
}

.sidebar {
  width: 200px;
  background-color: #f0f0f0;
  padding: 20px;
  box-sizing: border-box;
}

.sidebar h2 {
  margin-bottom: 20px;
  text-align: center;
}

.sidebar-button {
  display: block;
  width: 100%;
  padding: 10px;
  background-color: blueviolet;
  color: white;
  border: none;
  border-radius: 3px;
  font-size: 16px;
  cursor: pointer;
  margin-bottom: 10px;
  text-align: left;
  transition: background-color 0.3s ease;
}

.sidebar-button:hover {
  background-color: #663399;
}

/* Content */
.content {
  flex: 1;
  padding: 20px;
}

/* User Table */
.user-table {
  width: 100%;
  border-collapse: collapse;
  margin-top: 20px;
}

.user-table th,
.user-table td {
  padding: 10px;
  border: 1px solid #ddd;
  text-align: left;
}

.user-table th {
  background-color: #f2f2f2;
  color: #333;
}

.user-table tr:hover {
  background-color: #f9f9f9;
}

/* Pagination */
.pagination {
  margin-top: 20px;
  text-align: center;
}

.pagination button {
  padding: 10px 15px;
  margin: 0 5px;
  border: 1px solid #ddd;
  background-color: white;
  cursor: pointer;
  transition: background-color 0.3s;
}

.pagination button.active {
  background-color: blueviolet;
  color: white;
  border-color: blueviolet;
}

.pagination button:hover {
  background-color: #f2f2f2;
}

/* Add User Form */
.add-user-form {
  margin-top: 30px;
}

.add-user-form h3 {
  margin-bottom: 20px;
}

.add-user-form label {
  display: block;
  margin-bottom: 5px;
}

.add-user-form input {
  width: 100%;
  padding: 10px;
  margin-bottom: 15px;
  border: 1px solid #ddd;
  border-radius: 3px;
  box-sizing: border-box;
}

.add-user-form button {
  padding: 10px 15px;
  background-color: blueviolet;
  color: white;
  border: none;
  border-radius: 3px;
  cursor: pointer;
}

.add-user-form button:hover {
  background-color: #663399;
}

/* Search Bar */
.search-bar {
  margin-bottom: 20px;
  text-align: center;
}

.search-bar input {
  padding: 10px;
  width: 80%;
  max-width: 500px;
  border: 1px solid #ddd;
  border-radius: 3px;
  box-sizing: border-box;
}
</style>
