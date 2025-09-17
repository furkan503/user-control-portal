<template>
  <div>
    <div v-for="(postItem, index) in posts" :key="index">
      <form @submit.prevent="saveChanges(postItem)">
        <label :for="'title-' + index">Title:</label>
        <input :id="'title-' + index" v-model="postItem.title" type="text" class="form-input">

        <label :for="'body-' + index">Body:</label>
        <input :id="'body-' + index" v-model="postItem.body" type="text" class="form-input">

        <button type="submit" class="btn btn-bluviolet">Save Changes</button>
        <button type="button" @click="deletePost(postItem)" class="btn btn-danger">Delete</button>
        <button v-if="canViewComments" type="button" @click="commentsPost(postItem)" class="btn btn-primary">Go to Comments</button>
      </form>
    </div>

    <form @submit.prevent="addPost">
      <label for="newPostTitle">New Post Title:</label>
      <input id="newPostTitle" v-model="newPost.title" type="text" class="form-input">

      <label for="newPostBody">Body:</label>
      <input id="newPostBody" v-model="newPost.body" type="text" class="form-input">

      <button type="submit" class="btn btn-bluviolet">Add Post</button>
    </form>
  </div>
</template>

<script>
export default {
  data() {
    return {
      posts: [],
      newPost: {
        title: '',
        user: this.$route.params.id,
        body: ''
      },
      canViewComments: false,
    };
  },
  created() {
    this.fetchPostDetails();
  },
  async mounted() {
    await this.checkCommentsPermission();

  },
  methods: {
    
    async checkCommentsPermission() {
      const permission = 'users.change_comment'; 
      this.canViewComments = await this.checkPermissionComments(permission);
    },

    async  checkPermissionComments(permission) {
      const token = localStorage.getItem('accessToken');
      if (!token) {
        return false;
      }

      try {
        const response = await fetch(`http://127.0.0.1:8000/api/comments/check_permission/?permission=${permission}`, {
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
    async fetchPostDetails() {
      try {
        const token = localStorage.getItem('accessToken');
        const response = await fetch(`http://127.0.0.1:8000/api/posts/user/${this.$route.params.id}/`, {
        headers: {
            'Authorization': `Bearer ${token}`,
        }
      });
        const data = await response.json();
        this.posts.splice(0, this.posts.length, ...data);
      } catch (error) {
        console.error('Error fetching posts:', error);
      }
    },
    async saveChanges(postItem) {
      try {
        const token = localStorage.getItem('accessToken');
        const response = await fetch(`http://127.0.0.1:8000/api/posts/${postItem.id}/`, {
          method: 'PUT',
          headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${token}`,
          },
          body: JSON.stringify(postItem),
        });
        if (response.ok) {
          alert('Post updated');
        } else {
          alert('Failed to update post');
        }
      } catch (error) {
        console.error('Error updating post:', error);
      }
    },
    async deletePost(postItem) {
      try {
        const token = localStorage.getItem('accessToken');
        const response = await fetch(`http://127.0.0.1:8000/api/posts/${postItem.id}/`, {
          method: 'DELETE',
          headers: {
            'Authorization': `Bearer ${token}`,
        }
        });
        if (response.ok) {
          this.posts = this.posts.filter(post => post.id !== postItem.id);
          alert('Post deleted');
        } else {
          alert('Failed to delete post');
        }
      } catch (error) {
        console.error('Error deleting post:', error);
      }
    },
    async addPost() {
      try {
        const token = localStorage.getItem('accessToken');
        const response = await fetch(`http://127.0.0.1:8000/api/posts/`, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${token}`,
          },
          body: JSON.stringify(this.newPost),
        });

        if (response.ok) {
          const data = await response.json();
          this.posts.push(data);
          alert('Post added successfully');
          this.newPost.title = '';
          this.newPost.body = '';
        } else {
          alert('Failed to add post');
        }
      } catch (error) {
        console.error('Error adding post:', error);
      }
    },
    commentsPost(postItem) {
      this.$router.push(`/admin/users/${this.$route.params.id}/posts/comments/${postItem.id}`);
    }
  }
};
</script>

<style scoped>
.btn {
  padding: 10px 20px;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  margin-right: 10px;
}

.btn-bluviolet {
  background-color: blueviolet;
  color: white;
}

.btn-bluviolet:hover {
  background-color: darkviolet;
}

.btn-danger {
  background-color: #dc3545;
  color: white;
}

.btn-danger:hover {
  background-color: #c82333;
}

.btn-primary {
  background-color: #007bff;
  color: white;
}

.btn-primary:hover {
  background-color: #0069d9;
}

.form-input {
  width: calc(100% - 22px); /* Adjust for padding and border */
  padding: 8px;
  border: 1px solid #ccc;
  border-radius: 3px;
  margin-top: 5px;
  margin-bottom: 10px;
}
</style>
