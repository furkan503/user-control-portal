
import { createRouter, createWebHistory } from 'vue-router';
import UserList from './pages/UserList.vue';
import UserDetails from './pages/UserDetails.vue';
import Todos from './pages/Todos.vue';
import Posts from './pages/Posts.vue';
import Albums from './pages/Albums.vue';
import Photos from './pages/Photos.vue';
import Login from './pages/Login.vue';
import Admin from './pages/Admin.vue';
import AdminUsers from './pages/AdminUsers.vue';
import AdminTodos from './pages/AdminTodos.vue';
import AdminPosts from './pages/AdminPosts.vue';
import AdminAlbums from './pages/AdminAlbums.vue';
import AdminPhotos from './pages/AdminPhotos.vue';
import AdminDetails from './pages/AdminDetails.vue';
import AdminComments from './pages/AdminComments.vue';
import AdminAdd from './pages/AdminAdd.vue';


function requireAuth(to, from, next) {
  const token = localStorage.getItem('accessToken');
  if (!token) {
    next({ path: '/login' });
  } else {
    next();
  }
}

// async function checkPermission(permission, next) {
//   const token = localStorage.getItem('accessToken');
//   if (!token) {
//     next({ path: '/login' });
//     return;
//   }

//   try {
//     const response = await fetch(`http://127.0.0.1:8000/api/todos/check_permission/?permission=${permission}`, {
//       method: 'GET',
//       headers: {
//         'Authorization': `Bearer ${token}`,
//         'Content-Type': 'application/json'
//       }
//     });

//     const data = await response.json();
//     if (data.has_permission) {
//       next();
//     } else {
//       next({ path: '/admin' }); 
//     }
//   } catch (error) {
//     console.error('Error checking permissions:', error);
//     next({ path: '/admin' });
//   }
// }



const router = createRouter({
  history: createWebHistory(),
  routes: [
    { path: '/', redirect: '/login' },
    { path: '/login', name: 'Login', component: Login },
    { 
      path: '/admin', 
      name: 'Admin', 
      component: Admin, 
      beforeEnter: requireAuth,
      children: [
         {path: 'users',
          name:'AdminUsers',
          component: AdminUsers},
          {path: 'add',
            name: 'AdminAdd',
            component: AdminAdd,
          }
      ]
    },
    {
      path: '/admin/users/:id',
      component: AdminDetails,
      beforeEnter: requireAuth,

      children: [
        { path: 'todos', name: 'admintodos', component: AdminTodos }, //beforeEnter: (to, from, next) => checkPermission('app.change_todo', next) }, 
        { path: 'posts', name: 'adminposts', component: AdminPosts, props: true, },
        {path: 'posts/comments/:postId', component: AdminComments, props:true,},
        {
          path: 'albums',
          name: 'adminalbums',
          component: AdminAlbums,
          children: [
            {
              path: 'photos/:albumId',
              component: AdminPhotos,
            },
          ],
        },
      ],
    },
    { path: '/users', component: UserList },
    {
      path: '/users/:id',
      component: UserDetails,
      props: true,
      children: [
        { path: 'todos', name: 'todos', component: Todos },
        { path: 'posts', name: 'posts', component: Posts },
        {
          path: 'albums',
          name: 'albums',
          component: Albums,
          children: [
            {
              path: 'photos/:albumId',
              component: Photos,
            },
          ],
        },
      ],
    },
  ],
});

export default router;
