<!--
 * @Author: lijun lijun@ljsea.top
 * @Date: 2023-10-07 17:18:45
 * @LastEditors: lijun lijun@ljsea.top
 * @LastEditTime: 2023-10-08 16:36:08
 * @FilePath: \undefinedf:\Code\WebStorm\vue-project\src\App.vue
 * @Description: -=>
 -->
<template>
  <div>
    <div>GET返回数据:{{ items }}</div>
  </div>

  <div>
    <button @click="initData()">Get获取数据</button>
  </div>
  <div>
    <div class="form-group">
      <label for="name">Username:</label>  
      <input type="text" v-model="name" placeholder="input name" />
    </div>
    <div class="form-group">
      <label for="age">AGE:</label>  
      <input type="text" v-model="age" placeholder="input age" />
    </div>
    <div>name={{ name }},age={{ age }}</div>
    <div>
      <button @click="postGetData()">Post获取数据</button>
    </div>

    <div>post返回数据:{{ post }}</div>
  </div>
</template>  
  
<script>
import axios from 'axios'
import { ref } from 'vue'

export default {
  data() {
    return {
      items: [],
      name: "",
      age: "",
      post: []
    }
  },

  methods: {
    initData() {
      axios.get('http://114.115.206.93:5000/get_info')
        .then(response => {
          this.items = response.data
        })
        .catch(error => {
          console.error(error)
        })
    },
    postGetData() {
      axios.post('http://114.115.206.93:5000/post_info', {
        name: this.name,
        age: this.age,
      })
        .then(response => {
          this.post = response.data
          console.log(response.data)
        })
        .catch(error => {
          console.error(error)
        })
    },
    mounted() {
      this.initData();
    },
  }
}  
</script>