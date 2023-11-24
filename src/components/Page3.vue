<template>
  <h1>桑吉图--游戏、类型、各地区销量关系</h1>
  <div class="Echarts">
    <div id="page3" style="width: 800px; height: 600px"></div>
  </div>
</template>
   <script>
import { ref } from "vue";
import axios from "axios";
import * as echarts from "echarts";

export default {
  data() {
    return {
      items: [],
      name: [],
      source: [],
      target: [],
      value: [],
      post: [],
    };
  },
  methods: {
    initData() {
      axios
        .post("http://114.115.206.93:5000/get_sankey_data",{
          "min":0,
          "max":50
        })
        .then((response) => {
          //由于桑吉图只需要nodes和links两个数据，所以只取这两个数据
          this.name = response.data.nodes;
          this.source = response.data.links;
          this.myEcharts(); // 在数据获取后，再调用myEcharts()方法绘制图表
        })
        .catch((error) => {
          console.error(error);
        });
    },
    postGetData() {
      axios
        .post("http://114.115.206.93:5000/post_sankey_data")
        .then((response) => {
          this.post = response.data;
          console.log(response.data);
        })
        .catch((error) => {
          console.error(error);
        });
    },
    async mounted() {
      await this.initData();
      console.log(this.items);
    },
    created() {
      this.initData();
      console.log(this.items);
    },

    myEcharts() {
      // 基于准备好的dom，初始化echarts实例
      var myChart = echarts.init(document.getElementById("page3"));
      // 指定图表的配置项和数据
      var option = {
        series: {
          type: "sankey",
          layout: "none",
          focusNodeAdjacency: "true",
          data: this.name,
          links: this.source,
          emphasis: {
            focus: "adjacency",
          },
          lineStyle: {
            color: "gradient",
            curveness: 0.5,
          },
        },
      };
      // 使用刚指定的配置项和数据显示图表。
      myChart.setOption(option);
    },
  },
  mounted() {
    this.initData(); // 在组件挂载时首先获取数据
  },
};
</script>