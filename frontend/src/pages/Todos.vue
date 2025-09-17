<template>
  <div>
    <ul>
      <div>
        <li v-for="todo in todos" :key="todo.id">
          <input
            type="checkbox"
            class="custom-checkbox"
            :checked="todo.completed"
            @change="toggleTodo(todo.id, $event)"
          />
          {{ todo.title }}
        </li>
      </div>
    </ul>
  </div>
</template>

<script>
import { useRoute } from 'vue-router';

export default {
  props: ['id'],
  data() {
    return {
      todos: [],
    };
  },

  setup() {
    const route = useRoute();
    return { route };
  },

  methods: {
    async fetchTodos() {
      const userId = parseInt(this.route.params.id);
      const token = localStorage.getItem('accessToken');
      const response = await fetch(`http://localhost:8000/api/todos/user/${userId}`, {
        method: 'GET',
        headers: {
            'Authorization': `Bearer ${token}`,
            'Content-Type': 'application/json'
        }
      });
      const todosData = await response.json();
      this.todos = todosData.map((todo) => ({
        id: todo.id,
        title: todo.title,
        completed: todo.completed,
      }));
    },
    toggleTodo(id, event) {
      const todo = this.todos.find((t) => t.id === id);
      if (todo) {
        todo.completed = event.target.checked;
      }
    },
  },

  mounted() {
    this.fetchTodos();
  },
};
</script>

<style scoped>
ul {
  list-style-type: none;
}

li {
  display: flex;
  align-items: center;
  margin-bottom: 25px;
  font-size: 14px;
}

.custom-checkbox {
  position: relative;
  appearance: none;
  -webkit-appearance: none;
  width: 20px;
  height: 20px;
  margin-right: 8px;
  border: 2px solid black;
  border-radius: 3px;
  outline: none;
  cursor: pointer;
}

.custom-checkbox:checked {
  background-color: blueviolet;
  border-color: blueviolet;
}

.custom-checkbox:checked::before {
  content: '\2714';
  display: block;
  color: white;
  font-weight: bold;
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  font-size: 16px;
}
</style>
