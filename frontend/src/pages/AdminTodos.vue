<template>
  
  <div>
    <div v-for="(todoItem, index) in todos" :key="index">
      <form @submit.prevent="saveChanges(todoItem)">
        <label :for="'title-' + index">Title:</label>
        <input :id="'title-' + index" v-model="todoItem.title" type="text" class="form-input">

        <label :for="'completed-' + index" class="checkbox-container">Is Completed:
          <input :id="'completed-' + index" v-model="todoItem.completed" type="checkbox">
          <span class="checkmark"></span>
        </label>

        <button type="submit" class="btn btn-bluviolet">Save Changes</button>
        <button type="button" @click="deleteTodo(todoItem)" class="btn btn-danger">Delete</button>
      </form>
    </div>

    <form @submit.prevent="addTodo">
      <label for="newTodoTitle">New Todo Title:</label>
      <input id="newTodoTitle" v-model="newTodo.title" type="text" class="form-input">

      <label for="newTodoCompleted" class="checkbox-container">Is Completed:
        <input id="newTodoCompleted" v-model="newTodo.completed" type="checkbox">
        <span class="checkmark"></span>
      </label>

      <button type="submit" class="btn btn-bluviolet">Add Todo</button>
    </form>
  </div>
</template>

<script>
export default {
  data() {
    return {
      todos: [],
      newTodo: {
        title: '',
        user: this.$route.params.id,
        completed: false
      }
    };
  },
  created() {
    this.fetchTodoDetails();
  },
  methods: {
    async fetchTodoDetails() {
      try {
        const token = localStorage.getItem('accessToken');
        const response = await fetch(`http://127.0.0.1:8000/api/todos/user/${this.$route.params.id}/`, {
        method: 'GET',
        headers: {
            'Authorization': `Bearer ${token}`,
            'Content-Type': 'application/json'
        }
      });
        const data = await response.json();
        this.todos.splice(0, this.todos.length, ...data);
      } catch (error) {
        console.error('Error fetching todos:', error);
      }
    },
    async saveChanges(todoItem) {
      try {
        const token = localStorage.getItem('accessToken');
        const response = await fetch(`http://127.0.0.1:8000/api/todos/${todoItem.id}/`, {
          method: 'PUT',
          headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${token}`,           
          },
          body: JSON.stringify(todoItem),
        });
        if (response.ok) {
          alert('Todo updated');
        } else {
          alert('Failed to update todo');
        }
      } catch (error) {
        console.error('Error updating todo:', error);
      }
    },
    async deleteTodo(todoItem) {
      try {
        const token = localStorage.getItem('accessToken');
        const response = await fetch(`http://127.0.0.1:8000/api/todos/${todoItem.id}/`, {
          method: 'DELETE',
          headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${token}`,           
          },
        });
        if (response.ok) {
          this.todos = this.todos.filter(todo => todo.id !== todoItem.id);
          alert('Todo deleted');
        } else {
          alert('Failed to delete todo');
        }
      } catch (error) {
        console.error('Error deleting user:', error);
      }
    },
    async addTodo() {
      try {
        const token = localStorage.getItem('accessToken');
        const response = await fetch(`http://127.0.0.1:8000/api/todos/`, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${token}`,           
          },
          body: JSON.stringify(this.newTodo),
        });
        if (response.ok) {
          const data = await response.json();
          this.todos.push(data);
          alert('Todo added successfully');
          this.newTodo.title = '';
          this.newTodo.completed = false;
        } else {
          alert('Failed to add todo');
        }
      } catch (error) {
        console.error('Error adding todo:', error);
      }
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

.checkbox-container {
  display: block;
  position: relative;
  padding-left: 35px;
  margin-top: 10px;
  cursor: pointer;
  font-size: 16px;
}

.checkbox-container input {
  position: absolute;
  opacity: 0;
  cursor: pointer;
  height: 0;
  width: 0;
}

.checkmark {
  position: absolute;
  top: 0;
  left: 0;
  height: 25px;
  width: 25px;
  background-color: #eee;
  border-radius: 5px;
}

.checkbox-container:hover input ~ .checkmark {
  background-color: #ccc;
}

.checkbox-container input:checked ~ .checkmark {
  background-color: blueviolet;
}

.checkmark:after {
  content: '';
  position: absolute;
  display: none;
}

.checkbox-container input:checked ~ .checkmark:after {
  display: block;
}

.checkbox-container .checkmark:after {
  left: 9px;
  top: 5px;
  width: 5px;
  height: 10px;
  border: solid white;
  border-width: 0 3px 3px 0;
  transform: rotate(45deg);
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
