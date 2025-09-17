<template>
  <div class="admin-container">
    <!-- Add New Admin Form -->
    <form  v-if="canViewAdmin" @submit.prevent="addAdmin" class="add-admin-form">
      <h3>Add New Admin</h3>
      <label for="newAdminUsername">Username:</label>
      <input id="newAdminUsername" v-model="newAdmin.username" type="text">

      <label for="newAdminEmail">Email:</label>
      <input id="newAdminEmail" v-model="newAdmin.email" type="text">

      <label for="newAdminPassword">Password:</label>
      <input id="newAdminPassword" v-model="newAdmin.password" type="password">

      <label for="newAdminFirstName">First Name:</label>
      <input id="newAdminFirstName" v-model="newAdmin.first_name" type="text">

      <label for="newAdminLastName">Last Name:</label>
      <input id="newAdminLastName" v-model="newAdmin.last_name" type="text">

      <div v-for="permission in user_permissions" :key="permission.id">
        <label>
          <input type="checkbox" :value="permission.id" v-model="newAdmin.user_permissions">
          {{ permission.name }}
        </label>
      </div>

      <button type="submit" class="btn">Add Admin</button>
    </form>

    <!-- List of Admins -->
    <ul class="admin-list">
      <li v-for="admin in admins" :key="admin.id">
        <div>Username: <input v-model="admin.username" type="text"></div>
        <div>Email: <input v-model="admin.email" type="text"></div>
        <div>First Name: <input v-model="admin.first_name" type="text"></div>
        <div>Last Name: <input v-model="admin.last_name" type="text"></div>
        <div>New Password: <input v-model="admin.password" type="password" placeholder="New Password"></div>
        
        <!-- <div v-for="permission in user_permissions" :key="permission.id">
          <label>
            <input type="checkbox" :value="permission.id" v-model="user_permissions">
            {{ permission.name }}
          </label>
        </div> -->
        <button @click="updateAdmin(admin)" class="btn btn-success">Update</button>
        <button @click="deleteAdmin(admin.id)" class="btn btn-danger">Delete</button>
      </li>
    </ul>


    <!-- Update Permissions Form -->
    <form v-if="canViewPermissions" @submit.prevent="updatePermissions(adminId)" class="update-permissions-form">
      <h3>Update Permissions</h3>
      <div class="form-group">
        <label for="selectedAdmin">Select Admin:</label>
        <select id="selectedAdmin" v-model="adminId" class="form-control">
          <option v-for="admin in admins" :key="admin.id" :value="admin.id">
            {{ admin.username }}
          </option>
        </select>
      </div>

      <div class="form-group">
        <label for="selectedPermissions">Select Permissions:</label>
        <div class="checkbox-list">
          <label v-for="permission in user_permissions" :key="permission.id" class="checkbox-label">
            <input type="checkbox" :value="permission.id" v-model="selectedPermissions" class="form-check-input">
            {{ permission.name }}
          </label>
        </div>
      </div>

      <button type="submit" class="btn btn-primary">Update Permissions</button>
    </form>
  </div>
</template>


<script>
export default {
  data() {
    return {
      newAdmin: {
        username: '',
        email: '',
        password: '',
        first_name: '',
        last_name: '',
        is_staff: false,
        user_permissions: [],
      },
      admins: [],

      user_permissions: [], 
      selectedPermissions: [],
      canViewPermissions: false,
      canViewAdmin: false,
    };
  },
  created() {
    this.fetchAdmins();
    this.fetchPermissions(); 
  },
  async mounted() {
    await this.checkPermissionsPermission();
    await this.checkAdminPermission();


  },
  methods: {
    async checkPermissionsPermission() {
      const permission = 'auth.change_permission'; 
      this.canViewPermissions = await this.checkPermissionPermissions(permission);
    },

    async  checkPermissionPermissions(permission) {
      const token = localStorage.getItem('accessToken');
      if (!token) {
        return false;
      }

      try {
        const response = await fetch(`http://127.0.0.1:8000/api/permissions/check_permission/?permission=${permission}`, {
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
    async checkAdminPermission() {
      const permission = 'auth.change_user'; 
      this.canViewAdmin = await this.checkPermissionAdmin(permission);
    },

    async  checkPermissionAdmin(permission) {
      const token = localStorage.getItem('accessToken');
      if (!token) {
        return false;
      }

      try {
        const response = await fetch(`http://127.0.0.1:8000/api/login/check_permission/?permission=${permission}`, {
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

    async fetchAdmins() {
      try {
        const token = localStorage.getItem('accessToken');
        const response = await fetch('http://127.0.0.1:8000/api/login/', {
          headers: {
            'Authorization': `Bearer ${token}`,
          },
        });
        if (response.ok) {
          this.admins = await response.json();
        } else {
          console.error('Failed to fetch admins');
        }
      } catch (error) {
        console.error('Error fetching admins:', error);
      }
    },
    async fetchPermissions() {
      try {
        const token = localStorage.getItem('accessToken');
        const response = await fetch('http://127.0.0.1:8000/api/permissions/', {
          headers: {
            'Authorization': `Bearer ${token}`,
          },
        });
        if (response.ok) {
          this.user_permissions = await response.json();
        } else {
          console.error('Failed to fetch permissions');
        }
      } catch (error) {
        console.error('Error fetching permissions:', error);
      }
    },
    async addAdmin() {
      try {
        const adminPayload = {
            username: this.newAdmin.username,
            email: this.newAdmin.email,
            password: this.newAdmin.password,
            first_name: this.newAdmin.first_name,
            last_name: this.newAdmin.last_name,
            user_permissions: this.newAdmin.user_permissions,
          };
  
        const token = localStorage.getItem('accessToken');
        const response = await fetch('http://127.0.0.1:8000/api/login/add_admin/', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${token}`,
          },
          body: JSON.stringify([adminPayload]), 
        });
        if (response.ok) {
          alert('Admin added successfully');
          this.resetAdminForm();
          this.fetchAdmins(); 
        } else {
          const errorData = await response.json();
          alert('Failed to add admin');
          console.error('Error response:', errorData);
        }
      } catch (error) {
        console.error('Error adding admin:', error);
      }
    },
    async updateAdmin(admin) {
      try {
        const token = localStorage.getItem('accessToken');
        const response = await fetch(`http://127.0.0.1:8000/api/login/${admin.id}/`, {
          method: 'PUT',
          headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${token}`,
          },
          body: JSON.stringify(admin),
        });
        if (response.ok) {
          alert('Admin updated successfully');
          this.fetchAdmins(); 
        } else {
          const errorData = await response.json();
          alert('Failed to update admin');
          console.error('Error response:', errorData);
        }
      } catch (error) {
        console.error('Error updating admin:', error);
        alert('Error updating admin');
      }
    },
    async deleteAdmin(adminId) {
      try {
        const token = localStorage.getItem('accessToken');
        const response = await fetch(`http://127.0.0.1:8000/api/login/${adminId}/`, {
          method: 'DELETE',
          headers: {
            'Authorization': `Bearer ${token}`,
          },
        });
        if (response.ok) {
          alert('Admin deleted successfully');
          this.fetchAdmins(); 
        } else {
          const errorData = await response.json();
          alert('Failed to delete admin');
          console.error('Error response:', errorData);
        }
      } catch (error) {
        console.error('Error deleting admin:', error);
        alert('Error deleting admin');
      }
    },

    async updatePermissions(adminId) {
      try {
        if (!adminId) {
          alert('Please select an admin to update permissions.');
          return;
        }

        const token = localStorage.getItem('accessToken');
        const payload = {
          user_permissions: this.selectedPermissions,
        };
        const response = await fetch(`http://127.0.0.1:8000/api/login/${adminId}/update_permissions/`, {
          method: 'PUT',
          headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${token}`,
          },
          body: JSON.stringify(payload),
        });
        if (response.ok) {
          alert('Permissions updated successfully');
          this.fetchAdmins(); // Refresh admin list after update
        } else {
          const errorData = await response.json();
          alert('Failed to update permissions');
          console.error('Error response:', errorData);
        }
      } catch (error) {
        console.error('Error updating permissions:', error);
        alert('Error updating permissions');
      }
    },
    resetAdminForm() {
      this.newAdmin = {
        username: '',
        email: '',
        password: '',
        first_name: '',
        last_name: '',
        is_staff: false,
        user_permissions: [],
      };
    }
  }
};
</script>

  <style scoped>
  
  .admin-container {
    width: 100%;
    padding: 0px;
    box-sizing: border-box;
  }
  
  .add-admin-form {
    margin-top: 20px;
    background-color: #f7f7f7;
    padding: 20px;
    border-radius: 5px;
    box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
  }
  
  .add-admin-form h3 {
    margin-bottom: 15px;
    color: blueviolet;
  }
  
  .add-admin-form label {
    display: block;
    margin-bottom: 5px;
    color: #333;
  }
  
  .add-admin-form input[type="text"],
  .add-admin-form input[type="password"] {
    width: calc(100% - 22px);
    padding: 8px;
    border: 1px solid #ccc;
    border-radius: 3px;
  }
  
  .add-admin-form input[type="checkbox"] {
    width: auto;
  }
  
  .add-admin-form button {
    width: 100%;
    padding: 10px 20px;
    background-color: blueviolet;
    color: white;
    border: none;
    border-radius: 3px;
    cursor: pointer;
    transition: background-color 0.3s ease;
  }
  
  .add-admin-form button:hover {
    background-color: darkviolet;
  }
  
  .admin-list {
    margin-top: 20px;
    list-style-type: none;
    padding: 0;
    display: flex;
    flex-direction: row;
  }
  
  .admin-list li {
    margin-bottom: 20px;
    padding: 15px;
    background-color: #f0f0f0;
    border-radius: 5px;
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  }
  
  .admin-list li div {
    margin-bottom: 10px;
  }
  
  .admin-list li input[type="text"],
  .admin-list li input[type="password"] {
    width: calc(100% - 22px);
    padding: 8px;
    border: 1px solid #ccc;
    border-radius: 3px;
  }
  
  .admin-list li input[type="checkbox"] {
    width: auto;
  }
  
  .admin-list li button {
    margin-top: 10px;
    padding: 8px 12px;
    background-color: blueviolet;
    color: white;
    border: none;
    border-radius: 3px;
    cursor: pointer;
    transition: background-color 0.3s ease;
  }
  
  .admin-list li button.btn-danger {
    background-color: #dc3545;
  }
  
  .admin-list li button.btn-success {
    background-color: #28a745;
  }
  
  .admin-list li button:hover {
    background-color: darkviolet;
  }

  .update-permissions-form {
    background-color: #f7f7f7;
    padding: 20px;
    border-radius: 5px;
    box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
  }


  .update-permissions-form h3 {
    margin-bottom: 15px;
    color: blueviolet;
  }

  .update-permissions-form .form-group {
    margin-bottom: 15px;
  }

  .update-permissions-form label {
    display: block;
    margin-bottom: 5px;
    color: #333;
  }
  
  .update-permissions-form select,
  .update-permissions-form .checkbox-list {
    width: 100%;
    padding: 8px;
    border: 1px solid #ccc;
    border-radius: 3px;

  }
  .update-permissions-form .checkbox-label {
    display: block;
    margin-bottom: 5px;
  }
  
  .update-permissions-form button {
    width: 100%;
    padding: 10px 20px;
    background-color: blueviolet;
    color: white;
    border: none;
    border-radius: 3px;
    cursor: pointer;
    transition: background-color 0.3s ease;
  }
  
  .update-permissions-form button:hover {
    background-color: darkviolet;
  }
  
</style>

  
<!-- 
  async updateAdmin(admin) {
        try {
          const token = localStorage.getItem('accessToken');
          const response = await fetch(`http://127.0.0.1:8000/api/login/${admin.id}/`, {
            method: 'PUT',
            headers: {
              'Content-Type': 'application/json',
              'Authorization': `Bearer ${token}`,
            },
            body: JSON.stringify(admin),
          });
          if (response.ok) {
            alert('Admin updated successfully');
            this.fetchAdmins(); 
          } else {
            const errorData = await response.json();
            alert('Failed to update admin');
            console.error('Error response:', errorData);
          }
        } catch (error) {
          console.error('Error updating admin:', error);
          alert('Error updating admin');
        }
      },
      async deleteAdmin(adminId) {
        try {
          const token = localStorage.getItem('accessToken');
          const response = await fetch(`http://127.0.0.1:8000/api/login/${adminId}/`, {
            method: 'DELETE',
            headers: {
              'Authorization': `Bearer ${token}`,
            },
          });
          if (response.ok) {
            alert('Admin deleted successfully');
            this.fetchAdmins(); 
          } else {
            const errorData = await response.json();
            alert('Failed to delete admin');
            console.error('Error response:', errorData);
          }
        } catch (error) {
          console.error('Error deleting admin:', error);
          alert('Error deleting admin');
        }
      },

  
  -->