<template>
  <div>
    <div v-for="post in posts" :key="post.id">
      <h3>{{ post.title }}</h3>
      <p>{{ post.body }}</p>
      <div class="bored">
        <img class="onlyicon" src="/seemore.svg" />
        <button class="seemore" @click="openPopup(post)">See More</button>
      </div>
    </div>

    <div v-if="showPopup" class="popup">
      <div class="popup-content">
        <span class="close" @click="closePopup">&times;</span>
        <div style="display: flex">
          <div>
            <h2>{{ selectedPost.title }}</h2>
            <p>{{ selectedPost.body }}</p>
          </div>
          <div>
            <h3>Comments</h3>
            <ul>
              <li v-for="comment in comments" :key="comment.id">
                <img :src="comment.image_file ? comment.image_file : comment.imageUrl" />
                <strong>{{ comment.name }}</strong
                >: {{ comment.body }}
              </li>
            </ul>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { useRoute } from 'vue-router';
import md5 from 'blueimp-md5';

export default {
  props: ['id'],
  data() {
    return {
      posts: [],
      showPopup: false,
      selectedPost: null,
      comments: [],
    };
  },

  setup() {
    const route = useRoute();
    return { route };
  },

  methods: {
    
    commentImageSrc(comment) {
      return comment.image_file ? comment.image_file : this.fetchGravatar(comment.email);
    },

    async fetchPosts() {
      const userId = parseInt(this.route.params.id);
      const token = localStorage.getItem('accessToken');
      const response = await fetch(
        `http://127.0.0.1:8000/api/posts/user/${userId}`, {
        method: 'GET',
        headers: {
            'Authorization': `Bearer ${token}`,
            'Content-Type': 'application/json'
        }
      }
      );
      const postsData = await response.json();
      this.posts = postsData.map((post) => ({
        id: post.id,
        title: post.title,
        body: post.body,
      }));
    },

    async fetchComments() {
  if (!this.selectedPost) return;
  const postId = this.selectedPost.id;
  const token = localStorage.getItem('accessToken');
  const response = await fetch(
    `http://127.0.0.1:8000/api/comments/post/${postId}/`, {
        method: 'GET',
        headers: {
            'Authorization': `Bearer ${token}`,
            'Content-Type': 'application/json'
        }
      }
  );
  const commentsData = await response.json();
  
  
  this.comments = await Promise.all(commentsData.map(async (comment) => {
    const imageUrl = await this.fetchGravatar(comment.email);
    return {
      id: comment.id,
      name: comment.name,
      email: comment.email,
      body: comment.body,
      image_file: comment.image_file,
      imageUrl, 
    };
  }));
},

    openPopup(post) {
      this.selectedPost = post;
      this.showPopup = true;
      this.fetchComments();
    },

    closePopup() {
      this.showPopup = false;
      this.selectedPost = null;
      this.comments = [];
    },

    async fetchGravatar(email) {
      console.log('--------------------',email)
      const trimmedEmail = email.trim().toLowerCase();
      const emailHash = md5(trimmedEmail);
      const gravatarUrl = `https://www.gravatar.com/avatar/${emailHash}?d=identicon`;

      try {
        const response = await fetch(gravatarUrl);
        if (response.ok) {
          const blob = await response.blob();
          return URL.createObjectURL(blob);
        } else {
          return null;
        }
      } catch (error) {
        console.error(`Failed to fetch Gravatar image for ${email}:`, error);
        return null;
      }
    },
  },

  mounted() {
    this.fetchPosts();
  },
};
</script>

<style scoped>
.popup {
  display: flex;
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.5);
  justify-content: center;
  align-items: center;
}

.popup-content {
  background-color: white;
  padding: 20px;
  border-radius: 5px;
  max-width: 80%;
  max-height: 80%;
  overflow: auto;
}

.close {
  position: absolute;
  top: 10px;
  right: 10px;
  cursor: pointer;
  font-size: 20px;
}

ul {
  list-style-type: none;
}

img {
  width: 40px;
  border-radius: 50%;
}

.seemore {
  position: absolute;
  right: 100px;
  text-decoration: none;
  display: inline-block;
  background-color: #ffffff;
  border-right: none;
  border-top: none;
  border-bottom: none;
  border-left: none;
  font-size: 16px;
}

.onlyicon {
  width: 20px;
  position: absolute;
  right: 60px;
}

.bored {
  display: flex;
}
</style>
