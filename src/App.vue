<!--
 * @Author: lijun lijun@ljsea.top
 * @Date: 2023-10-07 17:18:45
 * @LastEditors: lijun 2021141461138@stu.scu.edu.cn
 * @LastEditTime: 2023-11-08 19:23:17
 * @FilePath: \undefinedf:\Code\WebStorm\vue-project\src\App.vue
 * @Description: -=>
 -->
<template>
  <div id="app">
    <div id="header">    
      <router-link to="/">Home</router-link>
      <router-link to="/Page1">Page1</router-link>
      <router-link to="/Page2">Page2</router-link>
      <router-link to="/Page3">Page3</router-link>
      <router-link to="/Page4">Page4</router-link>
    </div>
    <div id="page">
      <router-view></router-view>
    </div>   
  </div>
</template>  
  
<script>
import axios from "axios";
import { ref } from "vue";

export default {
  data() {
    return {
      items: [],
      name: "",
      age: "",
      post: [],
    };
  },

  methods: {
    initData() {
      axios
        .get("http://114.115.206.93:5000/get_info")
        .then((response) => {
          this.items = response.data;
        })
        .catch((error) => {
          console.error(error);
        });
    },
    postGetData() {
      axios
        .post("http://114.115.206.93:5000/post_info", {
          name: this.name,
          age: this.age,
        })
        .then((response) => {
          this.post = response.data;
          console.log(response.data);
        })
        .catch((error) => {
          console.error(error);
        });
    },
    mounted() {
      this.initData();
    },
    go() {
      console.log("Page1");
      this.$router.push("/Page1");
    },
  },
};
</script>