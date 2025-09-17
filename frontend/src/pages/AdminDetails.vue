<template>
  <div class="edit-user-page">
    <router-link to="/admin/" class="home">Go Home</router-link>
    <p></p>
    <form @submit.prevent="saveChanges" class="edit-user-form">
      <label for="name">Name:</label>
      <input id="name" v-model="user.name" type="text" />

      <label for="email">Email:</label>
      <input id="email" v-model="user.email" type="email" />

      <!-- Image upload section -->
      <div v-if="!isEditingImage" class="image-upload">
        <label for="image">Choose a file to change profile picture</label>
        <input id="image" type="file" @change="uploadImage" accept="image/*" class="file-input" />
      </div>
      <img v-if="user.image_file" :src="user.image_file" alt="User Image" class="user-image" />

      <label for="phone">Phone:</label>
      <input id="phone" v-model="user.phone" type="text" />

      <label for="street">Street:</label>
      <input id="street" v-model="user.address.street" type="text" />

      <label for="suite">Suite:</label>
      <input id="suite" v-model="user.address.suite" type="text" />

      <label for="city">City:</label>
      <input id="city" v-model="user.address.city" type="text" />

      <label for="company">Company:</label>
      <input id="company" v-model="user.company.name" type="text" />

      <label for="website">Website:</label>
      <input id="website" v-model="user.website" type="text" />

      <button type="submit" class="btn">Save Changes</button>
      <button type="button" @click="deleteUser" class="btn btn-danger">Delete User</button>
    </form>

    <ul class="user-nav">
      <li v-if="canViewTodos" @click="goToTodos(user.id)">Todos</li>
      <li v-if="canViewPosts" @click="goToPosts(user.id)">Posts</li>
      <li v-if="canViewAlbums" @click="goToAlbums(user.id)">Albums</li>
    </ul>

    <router-view></router-view>
  </div>
</template>

<script>
import md5 from 'blueimp-md5';



export default {
  data() {
    return {
      user: {
        id: '',
        name: '',
        email: '',
        phone: '',
        address: {
          street: '',
          suite: '',
          city: ''
        },
        company: {
          name: ''
        },
        website: '',
        image_file: '' 
      },
      isEditingImage: false,
      canViewTodos: false,
      canViewPosts: false,
      canViewAlbums: false,
    };
  },
  created() {
    this.fetchUserDetails();
  },
  async mounted() {
    await this.checkTodosPermission();
    await this.checkPostsPermission();
    await this.checkAlbumsPermission();

  },
  methods: {

    goToTodos(userId) {
      this.$router.push(`/admin/users/${userId}/todos`);
    },

    async checkTodosPermission() {
      const permission = 'users.change_todo'; 
      this.canViewTodos = await this.checkPermissionTodos(permission);
    },

    async  checkPermissionTodos(permission) {
      const token = localStorage.getItem('accessToken');
      if (!token) {
        return false;
      }

      try {
        const response = await fetch(`http://127.0.0.1:8000/api/todos/check_permission/?permission=${permission}`, {
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
    async checkPostsPermission() {
      const permission = 'users.change_post'; 
      this.canViewPosts = await this.checkPermissionPosts(permission);
    },

    async  checkPermissionPosts(permission) {
      const token = localStorage.getItem('accessToken');
      if (!token) {
        return false;
      }

      try {
        const response = await fetch(`http://127.0.0.1:8000/api/posts/check_permission/?permission=${permission}`, {
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
    async checkAlbumsPermission() {
      const permission = 'users.change_album'; 
      this.canViewAlbums = await this.checkPermissionAlbums(permission);
    },

    async  checkPermissionAlbums(permission) {
      const token = localStorage.getItem('accessToken');
      if (!token) {
        return false;
      }

      try {
        const response = await fetch(`http://127.0.0.1:8000/api/albums/check_permission/?permission=${permission}`, {
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

    goToPosts(userId) {
      this.$router.push(`/admin/users/${userId}/posts`);
    },
    goToAlbums(userId) {
      this.$router.push(`/admin/users/${userId}/albums`);
    },
    async fetchUserDetails() {
      try {
        const userId = this.$route.params.id;
        const token = localStorage.getItem('accessToken');
        const response = await fetch(`http://127.0.0.1:8000/api/users/${userId}/`, {
        method: 'GET',
        headers: {
            'Authorization': `Bearer ${token}`,
        }
      });
        this.user = await response.json();
        
        if (!this.user.image_file) {
          this.user.image_file = this.gravatarUrl(this.user.email);
        }
      } catch (error) {
        console.error('Error fetching user details:', error);
      }
    },
    async saveChanges() {
      try {
        delete this.user.image_file; 
        const userId = this.$route.params.id;
        const token = localStorage.getItem('accessToken');
        const response = await fetch(`http://127.0.0.1:8000/api/users/${userId}/`, {
          method: 'PUT',
          headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${token}`,
          },
          body: JSON.stringify(this.user),
        });
        if (response.ok) {
          alert('User details updated');
        } else {
          alert('User details could not be updated');
        }
      } catch (error) {
        console.error('Error updating user details:', error);
        alert('Error updating user details');
      }
    },
    async deleteUser() {
      try {
        const userId = this.$route.params.id;
        const token = localStorage.getItem('accessToken');
        const response = await fetch(`http://127.0.0.1:8000/api/users/${userId}/`, {
          method: 'DELETE',
          headers: {
            'Authorization': `Bearer ${token}`,
        }
        });
        if (response.ok) {
          alert('User deleted');
          this.$router.push('/admin/users');
        } else {
          alert('Failed to delete user');
        }
      } catch (error) {
        console.error('Error deleting user:', error);
        alert('Error deleting user');
      }
    },
    async uploadImage(event) {
      const file = event.target.files[0];
      if (!file) return;
      
      const formData = new FormData();
      formData.append('image', file); 
      
      try {
        const userId = this.$route.params.id;
        const token = localStorage.getItem('accessToken');
        const response = await fetch(`http://127.0.0.1:8000/api/users/${userId}/upload-image/`, {
          method: 'POST',
          body: formData,
          headers: {
            'Authorization': `Bearer ${token}`,        }
        });
        if (response.ok) {
          const updatedUser = await response.json();
          this.user.image_file = updatedUser.image_file; 
          alert('Profile image updated successfully');
        } else {
          console.error('Failed to upload image');
          alert('Failed to upload profile image');
        }
      } catch (error) {
        console.error('Error uploading image:', error);
        alert('Error uploading profile image');
      }
    },
    gravatarUrl(email) {
      const emailHash = md5(email.trim().toLowerCase());
      return `https://www.gravatar.com/avatar/${emailHash}?d=identicon`;
    },
  },
};
</script>

<style scoped>

.home {
  text-decoration: none;
  font-size: 20px;
  color: black;
}

.edit-user-page {
  width: 100%;
  padding: 20px;
  box-sizing: border-box;
}

.edit-user-form {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  grid-gap: 20px;
}

.edit-user-form label {
  font-weight: bold;
}

.edit-user-form input[type="text"],
.edit-user-form input[type="email"],
.edit-user-form input[type="file"] {
  width: calc(100% - 22px); /* Adjust for padding and border */
  padding: 8px;
  border: 1px solid #ccc;
  border-radius: 3px;
}

.file-input {
  display: none; /* Hide the default file input */
}

.file-upload-btn {
  display: inline-block;
  padding: 8px 12px;
  background-color: blueviolet;
  color: white;
  border: none;
  border-radius: 3px;
  cursor: pointer;
}

.file-upload-btn:hover {
  background-color: blueviolet;
}

.user-image {
  max-width: 100px;
  max-height: 100px;
  border-radius: 50%;
  margin-top: 10px;
  background-color: blueviolet;
}

.user-nav {
  display: flex;
  justify-content: center;
  list-style-type: none;
  padding: 0;
}

.user-nav li {
  cursor: pointer;
  padding: 10px 20px;
  margin: 0 10px;
  background-color: blueviolet;
  color: white;
  border-radius: 5px;
  font-size: 16px;
}

.user-nav li:hover {
  background-color: blueviolet;
}

.user-nav li:first-child {
  margin-left: 0;
}

.user-nav li:last-child {
  margin-right: 0;
}

.btn {
  padding: 10px 20px;
  background-color: blueviolet;
  color: white;
  border: none;
  border-radius: 5px;
  cursor: pointer;
}

.btn:hover {
  background-color: blueviolet;
}

.btn-danger {
  background-color: #dc3545;
}

.btn-danger:hover {
  background-color: #c82333;
}
</style>