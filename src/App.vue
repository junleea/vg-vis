<template>
  <!-- <div id="app">
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
    <div>
      <div style="margin-top: 20px;">
        <Page1 style="left: 20px;"></Page1>
        <Page2 style="right: 20px;"></Page2>
      </div>
      <Page3></Page3>
    </div>
  </div> -->
  <div class="container">
    <div class="part1">
      <Page3></Page3>
    </div>

    <div class="part2">
      <Page2></Page2>
    </div>
    <div class="part5">
      <Page5></Page5>
    </div>
    <div>
      <Page1></Page1>
    </div>
  </div>
</template>  
  
<script>
import axios from "axios";
import { ref } from "vue";
import Page1 from "./components/Page1.vue";
import Page3 from "./components/Page3.vue";
import Page2 from "./components/Page2.vue";
import Page5 from "./components/Page5.vue";
export default {
  components: { Page1, Page2, Page3 , Page5},
  data() {
    return {
      items: [],
      name: "",
      age: "",
      post: [],
    };
  },

  methods: {
    async initData() {
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
          min: 0, 
          max: 100,
        })
        .then((response) => {
          this.post = response.data;
          console.log("post:",this.post);
        })
        .catch((error) => {
          console.error(error);
        });
    },
    mounted() {
      this.postGetData();
    },
    created() {
      this.postGetData();
      console.log(this.post);
    },
  },
};
</script>
<style>
.page1 {
  position: relative;
  top: auto !important;
  left: auto !important;
}
.container {
  display: grid;
  grid-template-columns: repeat(2, 1fr);

  grid-gap: 20px;
}
body {  
background-color: white;  

}  
</style>