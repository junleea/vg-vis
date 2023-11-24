<template>
  <h1>河流图----每年游戏类型数目</h1>
  <div class="Echarts">
    <div id="page2" style="width: 600px; height: 400px"></div>
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
      legend: [],
      data: [],
      post: [],
    };
  },
  methods: {
    initData() {
      axios
        .get("http://114.115.206.93:5000/get_type_data")
        .then((Response) => {
          this.items = Response.data;
          this.legend = this.items.Genre;
          this.data = this.items.data;
          this.legend = JSON.parse(this.legend.replace(/'/g, '"'));
          this.data = JSON.parse(this.data.replace(/'/g, '"'));
          this.myEcharts();
        })
        .catch((error) => {
          console.error(error);
        });
    },
    myEcharts() {
      // 基于准备好的dom，初始化echarts实例
      var myChart = echarts.init(document.getElementById("page2"));

      // 指定图表的配置项和数据
      var option = {
        tooltip: {
          trigger: "axis",
          axisPointer: {
            type: "line",
            lineStyle: {
              color: "rgba(0,0,0,0.2)",
              width: 1,
              type: "solid",
            },
          },
        },
        legend: {
          data: this.legend,
          //data: this.te
        },
        singleAxis: {
          top: 50,
          bottom: 50,
          min: 1980,
          max: 2016,
          axisTick: {},
          axisLabel: {},
          type: "value",
          axisPointer: {
            animation: true,
            label: {
              show: true,
            },
          },
          splitLine: {
            show: true,
            lineStyle: {
              type: "dashed",
              opacity: 0.2,
            },
          },
        },
        series: [
          {
            type: "themeRiver",
            emphasis: {
              itemStyle: {
                shadowBlur: 20,
                shadowColor: "rgba(0, 0, 0, 0.8)",
              },
            },
            data: this.data,
            //data:this.td
          },
        ],
      };

      if (option && typeof option === "object") {
        myChart.setOption(option);
      }
    },
  },
  mounted() {
    this.initData();
  },
};
</script>
