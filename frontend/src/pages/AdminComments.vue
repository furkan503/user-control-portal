<template>
  <div>
    <div v-for="(comment, index) in comments" :key="index" class="comment-container">
      <form @submit.prevent="saveChanges(comment)">
        <label :for="'name-' + index">Name:</label>
        <input :id="'name-' + index" v-model="comment.name" type="text">

        <label :for="'email-' + index">Email:</label>
        <input :id="'email-' + index" v-model="comment.email" type="email">

        <label :for="'body-' + index">Body:</label>
        <textarea :id="'body-' + index" v-model="comment.body"></textarea>

        <!-- Image display -->
        <div class="image-container">
          <img v-if="comment.image_file" :src="comment.image_file" alt="Comment Image">
          <img v-else :src="gravatarUrl(comment.email)" alt="Gravatar">
        </div>

        <!-- Image upload for each comment -->
        <div v-if="!comment.isEditingImage">
          <label :for="'image-' + index">Change Image:</label>
          <input :id="'image-' + index" type="file" @change="startImageEditing(comment)" accept="image/*" />
        </div>

        <!-- Editing controls -->
        <div v-if="comment.isEditingImage">
          <input type="file" @change="uploadImage(comment, $event)" accept="image/*" />
          <button type="button" @click="cancelImageEditing(comment)">Cancel</button>
        </div>

        <button type="submit">Save Changes</button>
        <button type="button" @click="deleteComment(comment)">Delete</button>
      </form>
    </div>

    <form @submit.prevent="addComment" class="comment-container">
      <label for="newCommentName">Name:</label>
      <input id="newCommentName" v-model="newComment.name" type="text">

      <label for="newCommentEmail">Email:</label>
      <input id="newCommentEmail" v-model="newComment.email" type="email">

      <label for="newCommentBody">Body:</label>
      <textarea id="newCommentBody" v-model="newComment.body"></textarea>

      <!-- Image upload for new comment -->
      <label for="newCommentImage">Image:</label>
      <input id="newCommentImage" type="file" @change="handleNewCommentImage" accept="image/*" />

      <button type="submit">Add Comment</button>
    </form>
  </div>
</template>

<script>
import md5 from 'blueimp-md5';

export default {
  data() {
    return {
      comments: [],
      newComment: {
        name: '',
        email: '',
        body: '',
        image_file: null,
      }
    };
  },
  created() {
    this.fetchCommentDetails();
  },
  methods: {
    async fetchCommentDetails() {
      try {
        const token = localStorage.getItem('accessToken');
        const response = await fetch(`http://127.0.0.1:8000/api/comments/post/${this.$route.params.postId}/`, {
        method: 'GET',
        headers: {
            'Authorization': `Bearer ${token}`,
            'Content-Type': 'application/json'
        }
      });
        const data = await response.json();
        this.comments = data.map(comment => ({
          ...comment,
          image_file: comment.image_file || this.gravatarUrl(comment.email),
        }));
      } catch (error) {
        console.error('Error fetching comments:', error);
      }
    },
    async saveChanges(comment) {
      try {
        delete comment.image_file;
        const token = localStorage.getItem('accessToken');
        const response = await fetch(`http://127.0.0.1:8000/api/comments/${comment.id}/`, {
          method: 'PUT',
          headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${token}`,
          },
          body: JSON.stringify(comment),
        });
        if (response.ok) {
          alert('Comment updated');
        } else {
          alert('Failed to update comment');
        }
      } catch (error) {
        console.error('Error updating comment:', error);
      }
    },
    async deleteComment(comment) {
      try {
        const token = localStorage.getItem('accessToken');
        const response = await fetch(`http://127.0.0.1:8000/api/comments/${comment.id}/`, {
          method: 'DELETE',
          headers: {
            'Authorization': `Bearer ${token}`,
        }
        });
        if (response.ok) {
          this.comments = this.comments.filter(c => c.id !== comment.id);
          alert('Comment deleted');
        } else {
          alert('Failed to delete comment');
        }
      } catch (error) {
        console.error('Error deleting comment:', error);
      }
    },
    async addComment() {
      try {
        const formData = new FormData();
        formData.append('name', this.newComment.name);
        formData.append('email', this.newComment.email);
        formData.append('body', this.newComment.body);
        formData.append('post_id', this.$route.params.postId);
        if (this.newComment.image_file) {
          formData.append('image', this.newComment.image_file);
        }

        const token = localStorage.getItem('accessToken');

        const response = await fetch(`http://127.0.0.1:8000/api/comments/upload-comment-image/`, {
          method: 'POST',
          headers: {
            'Authorization': `Bearer ${token}`,
          },
          body: formData,
        });

        if (response.ok) {
          const data = await response.json();
          this.comments.push(data);
          alert('Comment added successfully');
          this.newComment.name = '';
          this.newComment.email = '';
          this.newComment.body = '';
          this.newComment.image_file = null;
        } else {
          alert('Failed to add comment');
        }
      } catch (error) {
        console.error('Error adding comment:', error);
      }
    },
    startImageEditing(comment) {
      comment.isEditingImage = true;
    },
    cancelImageEditing(comment) {
      delete comment.isEditingImage;
    },
    async uploadImage(comment, event) {
      const file = event.target.files[0];
      if (!file) return;

      const formData = new FormData();
      formData.append('image', file);

      try {
        const token = localStorage.getItem('accessToken');
        const response = await fetch(`http://127.0.0.1:8000/api/comments/${comment.id}/upload-image/`, {
          method: 'POST',
          headers: {
            'Authorization': `Bearer ${token}`,
        },
          body: formData,
        });

        if (response.ok) {
          const updatedComment = await response.json();
          comment.image_file = updatedComment.image_file || this.gravatarUrl(comment.email);
          alert('Image updated successfully');
        } else {
          console.error('Failed to upload image');
          alert('Failed to upload image');
        }
      } catch (error) {
        console.error('Error uploading image:', error);
        alert('Error uploading image');
      } finally {
        delete comment.isEditingImage;
      }
    },
    handleNewCommentImage(event) {
      this.newComment.image_file = event.target.files[0];
    },
    gravatarUrl(email) {
      const emailHash = md5(email.trim().toLowerCase());
      return `https://www.gravatar.com/avatar/${emailHash}?d=identicon`;
    },
  }
};
</script>

<style scoped>
  /* Container for each comment */
  .comment-container {
    margin-bottom: 20px;
    padding: 15px;
    border: 1px solid #ccc;
    border-radius: 8px;
    background-color: #f9f9f9;
  }

  /* Labels */
  .comment-container label {
    font-weight: bold;
    margin-bottom: 8px;
    display: block;
  }

  /* Inputs and textarea */
  .comment-container input[type="text"],
  .comment-container input[type="email"],
  .comment-container textarea {
    width: 100%;
    padding: 8px;
    font-size: 16px;
    margin-bottom: 12px;
    border: 1px solid #ccc;
    border-radius: 4px;
    box-sizing: border-box;
  }

  /* Image container */
  .comment-container .image-container {
    display: flex;
    align-items: center;
    margin-bottom: 12px;
  }

  .comment-container .image-container img {
    max-width: 100px;
    max-height: 100px;
    border-radius: 50%;
    margin-right: 10px;
    border: 1px solid #ccc;
  }

  /* Buttons */
  .comment-container button {
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

  .comment-container button[type="submit"] {
    background-color: blueviolet;
    color: white;
  }

  .comment-container button[type="button"] {
    background-color: red;
    color: white;
  }

  .comment-container button[type="submit"]:hover,
  .comment-container button[type="button"]:hover {
    background-color: #8a2be2;
  }

  /* File input */
  .comment-container input[type="file"] {
    margin-bottom: 12px;
  }
</style>
