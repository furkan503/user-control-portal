<template>
  <section>
    <div class="layout" style="display: flex">
      <div class="first-half" style="width: 20%">
        <img class="n2-mobile" src="/n2mobile.svg" />
        <p class="users">
          <img class="submit" src="/submit.svg" /><router-link to="/users"
            >Users</router-link
          >
        </p>
        <router-link to="/admin" class="admin">Go to Admin Page</router-link>
      </div>
      <div class="second-half" style="width: 80%">
        <h3>All Users</h3>
        <div class="search-bar">
          <input
            type="text"
            v-model="searchQuery"
            placeholder="Search users..."
          />
        </div>
        <div class="controls">
          <ul>
            <user-item
              v-for="user in filteredUsers"
              :key="user.id"
              :id="user.id"
              :name="user.name"
              :email="user.email"
              :street="user.address.street"
              :suite="user.address.suite"
              :city="user.address.city"
              :phone="user.phone"
              :website="user.website"
              :company="user.company.name"
              :image_file="user.image_file"
            />
          </ul>
        </div>
        <div class="pagination">
          <button
            v-for="page in totalPages"
            :key="page"
            @click="goToPage(page)"
            :class="{ active: page === currentPage }"
          >
            {{ page }}
          </button>
        </div>
      </div>
    </div>
  </section>
</template>

<script>
import UserItem from '../components/users/UserItem.vue';
import { mapGetters, mapActions } from 'vuex';

export default {
  components: {
    UserItem,
  },
  data() {
    return {
      searchQuery: '',
    };
  },
  computed: {
    ...mapGetters(['paginatedUsers', 'totalPages']),
    filteredUsers() {
      if (!this.searchQuery) {
        return this.paginatedUsers;
      }
      return this.paginatedUsers.filter(
        (user) =>
          user.name.toLowerCase().includes(this.searchQuery.toLowerCase()) ||
          user.email.toLowerCase().includes(this.searchQuery.toLowerCase())
      );
    },
    currentPage() {
      return this.$store.state.currentPage;
    },
  },
  methods: {
    ...mapActions(['fetchUsers', 'goToPage']),
  },
  created() {
    this.fetchUsers();
  },
};
</script>

<style scoped>
.users {
  color: blueviolet;
  border-left: 5px solid blueviolet;
  border-top-left-radius: 5px;
  border-bottom-left-radius: 5px;
  background-color: ghostwhite;
  text-align: center;
  font-size: 20px;
}

.admin {
  color: blueviolet;
  background-color: ghostwhite;
  text-align: center;
  font-size: 17px;
}

a {
  margin-left: 10px;
  text-decoration: none;
  color: blueviolet;
}

ul {
  list-style: none;
  margin: 10px;
  padding: 0;
  display: flex; /* Changed to flex to display items in a row */
  flex-wrap: wrap;
}

ul li {
  margin-right: 10px; /* Adjust the right margin for spacing between cards */
}

.controls {
  display: flex;
  flex-direction: row; /* Ensure controls are displayed in a row */
  flex-wrap: wrap;
}

.first-half {
  background-color: #f5f5f5;
}

.second-half {
  background-color: #ffffff;
}

.layout {
  gap: 25px;
  display: flex; /* Ensure the entire layout is flex */
  flex-direction: row; /* Display items in a row */
}

.n2-mobile {
  position: fixed;
  bottom: 0;
  left: 6%;
  width: 8%;
}
</style>
