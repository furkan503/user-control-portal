import getters from './getters.js';
import mutations from './mutations.js';
import actions from './actions.js';

export default {
  async state() {
    const token = localStorage.getItem('accessToken');
    const responseUser = await fetch(
      'http://localhost:8000/api/users/', {
        method: 'GET',
        headers: {
            'Authorization': `Bearer ${token}`,
            'Content-Type': 'application/json'
        }
      }
    );
    const responseDataUser = await responseUser.json();
    
    const users = [];

    for (const key in responseDataUser) {
      const user = {
        id: responseDataUser[key].id,
        name: responseDataUser[key].name,
        email: responseDataUser[key].email,
        phone: responseDataUser[key].phone,
        street: responseDataUser[key].address.street,
        suite: responseDataUser[key].address.suite,
        city: responseDataUser[key].address.city,
        company: responseDataUser[key].company.name,
        website: responseDataUser[key].website,
        image_file: responseDataUser[key].image_file,
      };
      users.push(user);
    }
    console.log(users)

    return users;
  },
  getters,
  mutations,
  actions,
};

