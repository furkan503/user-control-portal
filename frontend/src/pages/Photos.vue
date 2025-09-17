<template>
  <div class="photoscontainer">
    <div v-for="photo in photos" :key="photo.id" class="photowrapper">
      <img class="photos" :src="photo.image_file ? photo.image_file : photo.url" />
    </div>
  </div>
</template>

<script>
import { useRoute, useRouter } from 'vue-router';

export default {
  props: ['id'],
  data() {
    return {
      photos: [],
    };
  },
  setup() {
    const route = useRoute();
    const router = useRouter();
    return { route, router };
  },
  methods: {
    async fetchPhotos() {
      const albumId = parseInt(this.route.params.albumId);
      console.log('--->',albumId );
      console.log(albumId);
      const token = localStorage.getItem('accessToken');
      const response = await fetch(
        `http://127.0.0.1:8000/api/photos/album/${albumId}`, {
        method: 'GET',
        headers: {
            'Authorization': `Bearer ${token}`,
            'Content-Type': 'application/json'
        }
      }
      );
      const photosData = await response.json();
      this.photos = photosData.map((photo) => ({
        id: photo.id,
        url: photo.url,
        image_file: photo.image_file
      }));
    },
  },
  mounted() {
    this.fetchPhotos();
  },
};
</script>

<style scoped>
.photoscontainer {
  display: flex;
  flex-wrap: wrap;
}

.photowrapper {
  margin: 5px;
}

.photos {
  width: 150px;
}
</style>
