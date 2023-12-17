<template>
  <!-- <button style="text-align: center;align-items: center; justify-content: center;  ">按钮</button> -->
  <div>  
    <h1 class="artistic-title">游戏兴衰----电子游戏销量数据可视化</h1>  
    <!-- 其他页面内容 -->  
  </div>  
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
import Page1 from "./components/Page1.vue";
import Page3 from "./components/Page3.vue";
import Page2 from "./components/Page2.vue";
import Page5 from "./components/Page5.vue";
export default {
  components: { Page1, Page2, Page3, Page5 },
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
          console.log("post:", this.post);
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
.body {
  background-color: rgb(181, 190, 167);
}
.artistic-title {  
  font-family: 'Arial', sans-serif;  
  font-size: 40px;  
  text-align: center;  
  color: #333;  
  text-transform: uppercase;  
  letter-spacing: 2px;  
}  
</style>