<template>
  <div>
    <router-view></router-view>
    <div v-if="!isPhotosPage" class="block">
      <div v-for="album in albums" :key="album.id" class="album">
        <div class="album-thumbnails">
          <img
            v-for="photo in album.thumbnails"
            :key="photo.id"
            :src="photo.image_file ? photo.image_file : photo.thumbnailUrl"
            class="thumbnail"
          />
        </div>
        <button class="button" @click="gotoPhotos(album.id)">
          {{ album.title }}
        </button>
      </div>
    </div>
  </div>
</template>

<script>
import { useRoute, useRouter } from 'vue-router';

export default {
  props: ['id'],
  data() {
    return {
      albums: [],
    };
  },

  setup() {
    const route = useRoute();
    const router = useRouter();
    return { route, router };
  },

  computed: {
    isPhotosPage() {
      return this.route.path.includes('/albums/photos/');
    },
  },

  methods: {
    async fetchAlbums() {
      const userId = parseInt(this.route.params.id);
      const token = localStorage.getItem('accessToken');
      const response = await fetch(
        `http://127.0.0.1:8000/api/albums/user/${userId}`, {
        method: 'GET',
        headers: {
            'Authorization': `Bearer ${token}`,
            'Content-Type': 'application/json'
        }
      }
      );
      const albumsData = await response.json();

      for (const album of albumsData) {
        const token = localStorage.getItem('accessToken');
        const photoResponse = await fetch(
          `http://127.0.0.1:8000/api/photos/album/${album.id}`, {
        method: 'GET',
        headers: {
            'Authorization': `Bearer ${token}`,
            'Content-Type': 'application/json'
        }
      }
        );
        const photosData = await photoResponse.json();

        album.thumbnails = photosData.slice(0, 4).map((photo) => ({
          id: photo.id,
          thumbnailUrl: photo.thumbnail_url,
          image_file: photo.image_file
        }));
      }

      this.albums = albumsData.map((album) => ({
        id: album.id,
        title: album.title,
        thumbnails: album.thumbnails,
      
      }));
    },

    gotoPhotos(albumId) {
      this.router.push(
        `/users/${this.route.params.id}/albums/photos/${albumId}`
      );
    },
  },

  mounted() {
    this.fetchAlbums();
  },
};
</script>

<style scoped>
.block {
  display: flex;
  flex-wrap: wrap;
  gap: 20px;
}

.album {
  display: flex;
  flex-direction: column;
  align-items: center;
  margin: 10px;
  padding: 10px;
  border: 1px solid #ccc;
  border-radius: 5px;
  width: 300px;
}

.album-title {
  font-weight: bold;
  margin-bottom: 10px;
}

.album-thumbnails {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 5px;
}

.thumbnail {
  width: 100%;
  height: auto;
  object-fit: cover;
}

.button {
  margin-top: 10px;
  border: none;
  background-color: #ffffff;
  text-align: center;
  text-decoration: none;
  align-items: center;
  font-size: 14px;
  padding: 10px;
  width: 100%;
  cursor: pointer;
}
</style>
