<template>
  <h1>桑吉图--游戏、类型、各地区销量关系</h1>
  <div class="Echarts">
    <div id="page3" style="width: 800px; height: 600px"></div>
  </div>
  <div>
    <input type="number" v-model="min" placeholder="输入最小值" />
    <input type="range" v-model="min" min="0" max="10000" />

    <input type="number" v-model="max" placeholder="输入最大值" />
    <input type="range" v-model="max" min="0" max="10000" />
    <p>输入的最大区间100</p>
    <p v-if="outOfRange">输入值超出范围！</p>
    <button @click="validateInput">获取数据</button>
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
      min: 1,
      max: 50,
      outOfRange: false,
      set_color: [
        "#FFDAB9",
        "#F0FFF0",
        "#6A5ACD",
        "#5470c6",
        "#91cc75",
        "#fac858",
        "#ee6666",
        "#73c0de",
        "#3ba272",
        "#fc8452",
        "#9a60b4",
        "#ea7ccc",
      ],
    };
  },
  computed: {
    isValid() {
      return this.min > 0 && this.min < this.max && this.max < 100;
    },
  },
  created() {
    this.initData(); // 在组件挂载时首先获取数据
  },
  methods: {
    validateInput() {
      const min = Number(this.min);
      const max = Number(this.max);
      if (isNaN(min) || isNaN(max)) {
        // 如果输入的不是数字，将输入框内容置空并给予用户提示
        this.min = "";
        this.max = "";
        alert("请输入有效的数字");
      } else if (min < 0 || max > 10000 || min >= max || max - min > 100) {
        // 如果不满足条件，将输入框内容置为最后一次有效输入的值并给予用户提示
        this.min = this.max = "";
        alert(
          "请满足条件：最小值 > 0, 最大值 < 10000, 最小值 < 最大值, 最大值-最小值 < 100"
        );
      } else {
        // 如果满足条件，更新最小值和最大值
        this.min = min;
        this.max = max;
        this.initData();
      }
    },
    initData() {
      console.log(this.min);
      axios
        .post("http://114.115.206.93:5000/get_sankey_data", {
          min: this.min,
          max: this.max,
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

    myEcharts() {
      let diff = this.max - this.min; // 计算(max - min)
      // 修改前(max - min)个节点数据，为每个节点添加新的值字段
      for (let i = 0; i < this.source.length; i++) {
        if (this.name[i]) {
          // 确保索引在有效范围内
          let nodeValue = this.value[i]; // 获取节点的原始值
          if (i < diff) {
            if (diff < 10) {
              this.name[i].value = 200 / diff; // 使用公式计算新的值
            } else if (diff > 10 && diff < 50) {
              this.name[i].value = 600 / diff; // 使用公式计算新的值
            } else {
              this.name[i].value = 100 / diff; // 使用公式计算新的值
            }
          } else {
            this.name[i].color = set_color[i - diff];
          }
        }

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
              color: "links",
              curveness: 0.5,
            },
          },
        };
        // 使用刚指定的配置项和数据显示图表。
        myChart.setOption(option);
      }
    },
  },
  getNodeColor(node) {
    // 根据节点数据返回相应的颜色值
    // 这里是一个示例，你可以根据自己的需求进行修改
    if (node.name === "Sports") {
      return "#FFDAB9"; // 红色
    } else if (node.name === "Platform") {
      return "#F0FFF0"; // 绿色
    } else if (node.name === "Racing") {
      return "#6A5ACD"; // 绿色
    } else if (node.name === "Role-Playing") {
      return "#5470c6"; // 绿色
    } else if (node.name === "Puzzle") {
      return "#91cc75"; // 绿色
    } else if (node.name === "Misc") {
      return "#fac858"; // 绿色
    } else if (node.name === "Shooter") {
      return "#ee6666"; // 绿色
    } else if (node.name === "Simulation") {
      return "#73c0de"; // 绿色
    } else if (node.name === "Action") {
      return "#3ba272"; // 绿色
    } else {
      return "#3ba272";
    }
  },
};
</script>
