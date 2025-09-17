<template>
  <div>
    <div v-for="(album, index) in albums" :key="index" class="album-container">
      <form @submit.prevent="saveChanges(album)">
        <label :for="'title-' + index">Title:</label>
        <input :id="'title-' + index" v-model="album.title" type="text">
  
        <button type="submit">Save Changes</button>
        <button type="button" @click="deleteAlbum(album)">Delete</button>
        <router-link :to="`/admin/users/${this.$route.params.id}/albums/photos/${album.id}`">
          <button type="button">Go to Photos</button>
        </router-link>
      </form>
    </div>

    <form @submit.prevent="addAlbum" class="album-container">
      <label for="newAlbumTitle">New Album Title:</label>
      <input id="newAlbumTitle" v-model="newAlbum.title" type="text">
  
      <button type="submit">Add Album</button>
    </form>
  </div>

  <router-view></router-view>
</template>

<script>
export default {
  data() {
    return {
      albums: [],
      newAlbum: {
        title: '',
        user: this.$route.params.id,
      }
    };
  },
  created() {
    this.fetchAlbumDetails();
  },
  methods: {
    async fetchAlbumDetails() {
      try {
        const token = localStorage.getItem('accessToken');
        const response = await fetch(`http://127.0.0.1:8000/api/albums/user/${this.$route.params.id}/`, {
        method: 'GET',
        headers: {
            'Authorization': `Bearer ${token}`,
            'Content-Type': 'application/json'
        }
      });
        const data = await response.json();
        this.albums.splice(0, this.albums.length, ...data);
      } catch (error) {
        console.error('Error fetching albums:', error);
      }
    },
    async saveChanges(album) {
      try {
        const token = localStorage.getItem('accessToken');
        const response = await fetch(`http://127.0.0.1:8000/api/albums/${album.id}/`, {
          method: 'PUT',
          headers: {
            'Authorization': `Bearer ${token}`,
          },
          body: JSON.stringify(album),
        });
        if (response.ok) {
          alert('Album updated');
        } else {
          alert('Failed to update album');
        }
      } catch (error) {
        console.error('Error updating album:', error);
      }
    },
    async deleteAlbum(album) {
      try {
        const token = localStorage.getItem('accessToken');
        const response = await fetch(`http://127.0.0.1:8000/api/albums/${album.id}/`, {
          method: 'DELETE',
          headers: {
            'Authorization': `Bearer ${token}`,
          },
        });
        if (response.ok) {
          this.albums = this.albums.filter(item => item.id !== album.id);
          alert('Album deleted');
        } else {
          alert('Failed to delete album');
        }
      } catch (error) {
        console.error('Error deleting album:', error);
      }
    },
    async addAlbum() {
      try {
        const token = localStorage.getItem('accessToken');
        const response = await fetch(`http://127.0.0.1:8000/api/albums/`, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${token}`,
          },
          body: JSON.stringify(this.newAlbum),
        });
        if (response.ok) {
          const data = await response.json();
          this.albums.push(data);
          alert('Album added successfully');
          this.newAlbum.title = '';
        } else {
          alert('Failed to add album');
        }
      } catch (error) {
        console.error('Error adding album:', error);
      }
    }
  }
};
</script>

<style scoped>
/* Container for each album */
.album-container {
  margin-bottom: 20px;
  padding: 15px;
  border: 1px solid #ccc;
  border-radius: 8px;
  background-color: #f9f9f9;
}

/* Labels */
.album-container label {
  font-weight: bold;
  margin-bottom: 8px;
  display: block;
}

/* Inputs and buttons */
.album-container input[type="text"] {
  width: calc(100% - 20px);
  padding: 8px;
  font-size: 16px;
  margin-bottom: 12px;
  border: 1px solid #ccc;
  border-radius: 4px;
  box-sizing: border-box;
}

.album-container button {
  cursor: pointer;
  padding: 8px 16px;
  margin-right: 10px;
  border: none;
  border-radius: 4px;
  font-size: 14px;
  text-transform: uppercase;
  outline: none;
  transition: background-color 0.3s ease;
}

.album-container button[type="submit"] {
  background-color: blueviolet;
  color: white;
}

.album-container button[type="button"] {
  background-color: red;
  color: white;
}

.album-container button[type="submit"]:hover,
.album-container button[type="button"]:hover {
  background-color: #8a2be2;
}
</style>
