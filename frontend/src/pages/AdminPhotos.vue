<template>
  <div>
    <h2>Photos in Album</h2>
    <div v-for="(photo, index) in photos" :key="index" class="photo-container">
      <img :src="photo.image_file ? photo.image_file : photo.url" alt="Photo" width="100">
      <button @click="deletePhoto(photo.id)">Delete</button>
    </div>

    <form @submit.prevent="uploadPhoto" class="photo-upload-form">
      <label for="newPhotoTitle">New Photo Title:</label>
      <input id="newPhotoTitle" v-model="newPhoto.title" type="text">
      
      <label for="newPhotoFile">Upload Photo:</label>
      <input id="newPhotoFile" type="file" @change="handleFileUpload">

      <button type="submit">Add Photo</button>
    </form>
  </div>
</template>

<script>
export default {
  data() {
    return {
      photos: [],
      newPhoto: {
        title: '',
        file: null,
        albumId: this.$route.params.albumId  
      }
    };
  },
  created() {
    this.fetchPhotos();
  },
  watch: {
    '$route.params.albumId': 'fetchPhotos'
  },
  methods: {
    async fetchPhotos() {
      try {
        const token = localStorage.getItem('accessToken');
        const response = await fetch(`http://127.0.0.1:8000/api/photos/album/${this.$route.params.albumId}/`, {
        headers: {
            'Authorization': `Bearer ${token}`,
        }
      });
        this.photos = await response.json();
      } catch (error) {
        console.error('Error fetching photos:', error);
      }
    },
    handleFileUpload(event) {
      const file = event.target.files[0];
      if (!file) return;
      this.newPhoto.file = file;
    },
    async uploadPhoto() {
      const file = this.newPhoto.file;
      const albumId = this.newPhoto.albumId; 
      
      if (!file || !albumId) {
        alert('Please select an image file and provide an album.');
        return;
      }

      const formData = new FormData();
      formData.append('image', file);
      formData.append('title', this.newPhoto.title); 
      formData.append('album_id', albumId); 

      try {
        const token = localStorage.getItem('accessToken');
        const response = await fetch('http://127.0.0.1:8000/api/photos/upload_photo/', {
          method: 'POST',
          body: formData,
          headers: {
            'Authorization': `Bearer ${token}`,
        }
        });

        if (response.ok) {
          const newPhoto = await response.json();
          this.photos.push(newPhoto);
          alert('Photo added successfully');
          this.newPhoto.title = '';
          this.newPhoto.file = null;
        } else {
          console.error('Failed to add photo');
          alert('Failed to add photo');
        }
      } catch (error) {
        console.error('Error adding photo:', error);
        alert('Error adding photo');
      }
    },
    async deletePhoto(photoId) {
      try {
        const token = localStorage.getItem('accessToken');
        const response = await fetch(`http://127.0.0.1:8000/api/photos/${photoId}/`, {
          method: 'DELETE',
          headers: {
            'Authorization': `Bearer ${token}`,        }
        });
        if (response.ok) {
          this.photos = this.photos.filter(photo => photo.id !== photoId);
          alert('Photo deleted');
        } else {
          alert('Failed to delete photo');
        }
      } catch (error) {
        console.error('Error deleting photo:', error);
      }
    }
  }
};
</script>

<style scoped>
.photo-container {
  display: inline-block;
  margin: 10px;
}

.photo-container img {
  margin-bottom: 5px;
}

.photo-upload-form {
  margin-top: 20px;
}

.photo-upload-form label {
  display: block;
  margin-bottom: 5px;
}

.photo-upload-form input[type="text"],
.photo-upload-form input[type="file"],
.photo-upload-form button {
  margin-bottom: 10px;
}

.photo-upload-form input[type="file"] {
  display: block;
}
</style>
