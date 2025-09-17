<template>
  <section>
    <div class="first-half" style="width: 20%">
      <div class="userblock">
        <img :src="gravatarUrl(selectedUser.email)" />
        <div class="text">
          <h3>{{ selectedUser.name }}</h3>
          <p>{{ selectedUser.email }}</p>
        </div>
      </div>
      <div class="routes">
        <button class="users" @click="test">
          <img class="checkboxes" src="/todos.svg" alt="Todos" />Todos
        </button>
        <button class="post" @click="post">
          <img class="checkboxes" src="/posts.svg" alt="Posts" />Posts
        </button>
        <button class="album" @click="album">
          <img class="checkboxes" src="/albums.svg" alt="Albums" />Albums
        </button>
      </div>
      <img class="n2-mobile" src="/n2mobile.svg" />
    </div>
    <div class="second-half" style="width: 80%">
      <div class="idk">
        <img class="gohomeicon" src="/gohome.svg" />
        <button class="gohome" @click="home">
          {{ route.path.includes('/albums/photos') ? 'Go Albums' : 'Go Home' }}
        </button>
      </div>
      <router-view></router-view>
    </div>
  </section>
</template>

<script>
import { useRoute, useRouter } from 'vue-router';
import md5 from 'blueimp-md5';

export default {
  props: ['id'],
  data() {
    return {
      selectedUser: null,
    };
  },

  setup() {
    const route = useRoute();
    const router = useRouter();

    return {
      route,
      router,
    };
  },
  methods: {
    test() {
      return this.router.push({
        path: '/users' + '/' + this.id + '/todos',
        params: { id: this.id },
      });
    },

    post() {
      return this.router.push({ path: '/users' + '/' + this.id + '/posts' });
    },
    album() {
      return this.router.push({ path: '/users' + '/' + this.id + '/albums' });
    },

    home() {
      const currentPath = this.route.path;

      if (currentPath.includes('/albums/photos')) {
        return this.router.push({
          path: `/users/${this.id}/albums/`,
        });
      } else {
        return this.router.push({ path: '/users' });
      }
    },

    gravatarUrl(email) {
      const emailHash = md5(email.trim().toLowerCase());
      return `https://www.gravatar.com/avatar/${emailHash}?d=identicon`;
    },
  },

  async created() {
    const dummy = await this.$store.getters.users;
    this.selectedUser = dummy.find(
      (user) => parseInt(user.id) === parseInt(this.id)
    );
  },
};
</script>

<style scoped>
.users,
.post,
.album {
  color: blueviolet;
  border-left: 5px solid blueviolet;
  border-top-left-radius: 5px;
  border-bottom-left-radius: 5px;
  background-color: ghostwhite;
  text-align: center;
  text-decoration: none;
  display: flex;
  align-items: center;
  border-right: none;
  border-top: none;
  border-bottom: none;
  font-size: 18px;
  padding: 10px;
  height: 50px;
}

.users:hover,
.post:hover,
.album:hover {
  background-color: #ffffff;
}

.checkboxes {
  width: 30px;
  margin-right: 8px;
}

.userblock {
  display: flex;
  gap: 10px;
}

img {
  border-radius: 50%;
  width: 80px;
  height: 80px;
}

.n2-mobile {
  position: fixed;
  bottom: 0;
  left: 6%;
  width: 8%;
}

.routes {
  display: flex;
  flex-direction: column;
  background-color: #f5f5f5;
  gap: 20px;
}

.first-half {
  background-color: #f5f5f5;
  display: flex;
  flex-direction: column;
  gap: 50px;
  min-height: 200vh;
  overflow-y: auto;
}

.second-half {
  background-color: #ffffff;
  position: absolute;
  left: 23%;
  top: 30px;
}

p {
  font-size: 15px;
}

.gohome {
  text-decoration: none;
  display: inline-block;
  background-color: #ffffff;
  border-right: none;
  border-top: none;
  border-bottom: none;
  border-left: none;
  font-size: 28px;
}

.gohomeicon {
  width: 32px;
}

.idk {
  display: flex;
  gap: 20px;
}
</style>
