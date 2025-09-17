//export default {
  // users(state){
    //  console.log(state)
      //return state;
  // } 
//};

export default {
   async users(state) {
       const result = await someAsyncOperation(state);
       return result;
     } 
   };
 
 async function someAsyncOperation(state) {
   return new Promise((resolve) => {
     setTimeout(() => {
       resolve(state);
     }, 1000);
   });
 }
 