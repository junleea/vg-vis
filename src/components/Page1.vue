<template>

  <div class="Echarts">
    <div id="pie" style="width: 600px; height: 400px"></div>
  </div>
  <div class="Echarts">
    <h1>不同游戏类型在不同地区销量</h1>
    <div id="blchart" style="width: 600px; height: 400px"></div>
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
      name: "",
      age: "",
      post: [],
    };
  },
  methods: {
    initData() {
      axios
        .get("http://114.115.206.93:5000/get_zx_info")
        .then((response) => {
          //由于桑吉图只需要nodes和links两个数据，所以只取这两个数据
          this.data = response.data.piechart;
		  this.data1 = response.data.blchart;
          this.initPie(); // 在数据获取后，再调用initBie()方法绘制图表
		  this.initBlchart();
        })
        .catch((error) => {
          console.error(error);
        });
    },
    initBlchart() {
      var chartDom = document.getElementById("blchart"); //渲染的位置
      var myChart = echarts.init(chartDom);
      var option;

      option = {
        title: {
          text: "",
        },
        tooltip: {
          trigger: "axis",
        },
        legend: {
          data: [
            "Action",
            "Adventure",
            "Fighting",
            "Misc",
            "Platform",
            "Puzzle",
            "Racing",
            "Role-Playing",
            "Shooter",
            "Simulation",
          ],
        },
        grid: {
          left: "3%",
          right: "6%",
          bottom: "3%",
          containLabel: true,
        },
        toolbox: {
          feature: {
            saveAsImage: {},
          },
        },
        xAxis: {
          type: "category",
          boundaryGap: false,
          data: ["EU_Sales", "JP_Sales", "NA_Sales", "Other_Sales"],
        },
        yAxis: {
          type: "value",
        },
        series: this.data1,
      };

      option && myChart.setOption(option);
    },
    initPie() {
      var chartDom = document.getElementById("pie"); //渲染的位置
      var myChart = echarts.init(chartDom);
      var option;

      option = {
        title: {
          text: "世界游戏公司销量占比",
          /*subtext: 'Fake Data',*/
          left: "center",
        },
        tooltip: {
          trigger: "item",
        },
        legend: {
          orient: "vertical",
          left: "left",
        },
        series: [
          {
            name: "Access From",
            center: ["75%", "62%"],
            type: "pie",
            radius: "50%",
            data: this.data,
            emphasis: {
              itemStyle: {
                shadowBlur: 10,
                shadowOffsetX: 0,
                shadowColor: "rgba(0, 0, 0, 0.5)",
              },
            },
          },
        ],
      };

      option && myChart.setOption(option);
    },
  },
  mounted() {
    this.initData();
  },
};
</script>