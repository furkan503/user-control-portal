<template>
    <li @click="navigateToTodos">
      <div class="firstblock">
        <img class="img" :src="userImageSrc" />
        <div class="middleblock">
          <h4>{{ name }}</h4>
          <p>{{ email }}</p>
          <p>{{ phone }}</p>
        </div>
      </div>
      <div class="secondblock">
        <div class="align">
          <img class="icon" src="/location.svg" />
          <h4>Location</h4>
        </div>
        <div class="address">
          <span>{{ street }}</span>
          <span>{{ suite }}</span>
        </div>
        <p>{{ city }}</p>
        <div class="align">
          <img class="icon" src="/company.svg" />
          <h4>Company</h4>
        </div>
        <p>{{ company }}</p>
        <div class="align">
          <img class="icon" src="/website.svg" />
          <h4>Website</h4>
        </div>
        <p>{{ website }}</p>
      </div>
    </li>
  </template>
  
  <script>
  import md5 from 'blueimp-md5';
  import { useRouter } from 'vue-router';
  import { computed } from 'vue';
  
  export default {
    props: [
      'name',
      'id',
      'email',
      'street',
      'suite',
      'city',
      'phone',
      'website',
      'company',
      'image_file',
    ],
    setup(props) {
      const router = useRouter();
  
      const navigateToTodos = () => {
        router.push(`/users/${props.id}/todos`);
      };
  
      const gravatarUrl = (email) => {
        if (!email) {
          return '';
        }
        const emailHash = md5(email.trim().toLowerCase());
        return `https://www.gravatar.com/avatar/${emailHash}?d=identicon`;
      };
  
      const userImageSrc = computed(() => {
        return props.image_file ? props.image_file : gravatarUrl(props.email);
      });
  
      return {
        navigateToTodos,
        userImageSrc,
      };
    },
  };
  </script>
  

<style scoped>
    li {
        margin: 1rem 0;
        width: 90%;
        border: 1px solid #bcb6b6;
        border-radius: 25px;
        padding: 1rem;
        font-size:13px;

    }
    
    h3 {
        font-size: 1.5rem;
    }
    
    h4 {
        margin: 0.5rem 0;
    }
    
    .address {
        display:flex;
        gap: 10px;
    }

    .firstblock {
        display: flex;
        gap: 30px;

    }

    .img {
        width: 100px;
        border-radius: 50%;
    }

    .icon {
        width: 30px;
    }

    .align {
        display:flex;
        gap: 8px;
    }

</style>