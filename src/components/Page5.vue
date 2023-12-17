<template>
  <div id="race-chart">
    <div id="selectSection">
      <select v-model="selectCategory" name="category" id="category">
        <option value="publisher">发行商</option>
        <option value="platform">游戏平台</option>
      </select>
      <select v-model="selectArea" name="area" id="area">
        <option value="Global_Sales">所有地区</option>
        <option value="EU_Sales">欧洲</option>
        <option value="JP_Sales">日本</option>
        <option value="NA_Sales">北美</option>
        <option value="Other_Sales">其它地区</option>
      </select>
      <button @click="onGenerate">播放</button>
    </div>
    <div>
      <h1>竞赛条形图----展示随时间变化的给厂商或平台的发售数据</h1>
      <p>选择发行商或平台，选择地区，点击播放按钮</p>
      <p>单位：十万美元</p>
    </div>
    <div id="race-chart-graph" style="width: 800px; height: 600px"></div>
    <div>
      <h1>词云图----展示所选中的类型,厂商或平台的前二十.</h1>
    </div>
    <div id="word-cloud-graph" style="width: 600px; height: 400px"></div>
  </div>
</template>
  
  <script>
import axios from "axios";
import * as d3 from "d3";
import * as cloud from "d3-cloud";
import * as echarts from "echarts";
import "echarts-wordcloud/dist/echarts-wordcloud";
import "echarts-wordcloud/dist/echarts-wordcloud.min";

// 原始数据
console.log("begin to get data!");
var rawData = [];
// 筛选发行商/平台销售的数据
var data = [];
// 展示前n名
var n = 12;
var barSize = 40;
var margin = {
  top: 16,
  right: 6,
  bottom: 6,
  left: 0,
};
var height = margin.top + barSize * n + margin.bottom;
var width = 800;

var names;
var datevalues;
var k = 10;
var duration = 140;

function rank(value) {
  const data = Array.from(names, (name) => ({
    name,
    value: value(name),
  }));
  data.sort((a, b) => d3.descending(a.value, b.value));
  for (let i = 0; i < data.length; ++i) data[i].rank = Math.min(n, i);
  return data;
}

// 关键帧
function keyframes() {
  const keyframes = [];
  let ka, a, kb, b;
  console.log("datevalues", datevalues);
  for ([[ka, a], [kb, b]] of d3.pairs(datevalues)) {
    for (let i = 0; i < k; ++i) {
      const t = i / k;
      keyframes.push([
        new Date(ka * (1 - t) + kb * t),
        rank((name) => (a.get(name) || 0) * (1 - t) + (b.get(name) || 0) * t),
      ]);
    }
  }
  console.log("b=", b);
  keyframes.push([new Date(kb), rank((name) => b.get(name) || 0)]);
  return keyframes;
}

var nameframes;
var prev;
var next;
var svg;

var x = d3.scaleLinear([0, 1], [margin.left, width - margin.right]);
var y = d3
  .scaleBand()
  .domain(d3.range(n + 1))
  .rangeRound([margin.top, margin.top + barSize * (n + 1 + 0.1)])
  .padding(0.1);

function procData(category) {
  data = rawData.map((d) => ({
    year: d.year,
    name: d.name,
    value: d.value,
  }));
  return data;
}

export default {
  name: "RaceChart",
  data() {
    return {
      raceChartData: [],
      wordcloud: [],
      selectArea: "Global_Sales",
      selectCategory: "publisher",
    };
  },
  created() {
    this.onGenerate();
  },
  methods: {
    async init() {
      rawData = await this.loadData();
      console.log("rawData", rawData[0]);
      console.log("word", this.wordcloud[0]);
      names = new Set(rawData.map((d) => d.name));
      await d3.select("#race-chart-graph").select("svg").remove();
      //svg画布
      svg = d3
        .select("#race-chart-graph")
        .append("svg")
        .attr("width", width + margin.left + margin.right)
        .attr("height", height + margin.top + margin.bottom);
    },
    initwordchart() {
      var myChart = echarts.init(document.getElementById("word-cloud-graph"));
      const option = {
        title: {
          text: "",
          x: "center",
        },
        backgroundColor: "#fff",
        // tooltip: {
        //   pointFormat: "{series.name}: <b>{point.percentage:.1f}%</b>"
        // },
        series: [
          {
            type: "wordCloud",
            //用来调整词之间的距离
            gridSize: 10,
            //用来调整字的大小范围
            // Text size range which the value in data will be mapped to.
            // Default to have minimum 12px and maximum 60px size.
            sizeRange: [14, 40],
            // Text rotation range and step in degree. Text will be rotated randomly in range [-90,                                                                             90] by rotationStep 45
            //用来调整词的旋转方向，，[0,0]--代表着没有角度，也就是词为水平方向，需要设置角度参考注释内容
            // rotationRange: [-45, 0, 45, 90],
            // rotationRange: [ 0,90],
            rotationRange: [-45, 0, 45, 90],
            //随机生成字体颜色
            // maskImage: maskImage,
            textStyle: {
              color: function () {
                return (
                  "rgb(" +
                  Math.round(Math.random() * 255) +
                  ", " +
                  Math.round(Math.random() * 255) +
                  ", " +
                  Math.round(Math.random() * 255) +
                  ")"
                );
              },
            },
            //位置相关设置
            // Folllowing left/top/width/height/right/bottom are used for positioning the word cloud
            // Default to be put in the center and has 75% x 80% size.
            left: "center",
            top: "center",
            right: null,
            bottom: null,
            width: "100%",
            height: "100%",
            //数据
            data: this.wordcloud,
          },
        ],
      };
      myChart.setOption(option);
      // 点击某个字
      myChart.on("click", function (params) {
        console.log("myChart----click---:", params, "------", params.data);
      });
    },

    //读取数据
    async loadData() {
      var raceChartData = [];
      await axios
        .post("http://114.115.206.93:5000/get_race_chart_data", {
          type: this.selectCategory,
          area: this.selectArea,
        })
        .then((response) => {
          raceChartData = response.data.race;
          this.wordcloud = response.data.word;
        })
        .catch((error) => {
          console.error(error);
        });
      return raceChartData;
    },
    //播放函数
    play: async function (data) {
      const updateBars = bars(svg);
      const updateAxis = axis(svg);
      const updateLabels = labels(svg);
      const updateTicker = ticker(svg);

      for (const keyframe of keyframes()) {
        const transition = svg
          .transition()
          .duration(duration)
          .ease(d3.easeLinear);
        // Extract the top bar’s value.
        x.domain([0, keyframe[1][0].value + 500]);
        updateAxis(keyframe, transition);
        updateBars(keyframe, transition);
        updateLabels(keyframe, transition);
        updateTicker(keyframe, transition);

        await transition.end();
      }
    },
    //按钮点击播放后处理函数
    async onGenerate() {
      let category = this.selectCategory;
      await this.init();
      procData(category);
      console.log("begin to category");
      this.initwordchart();
      datevalues = Array.from(
        d3.rollup(
          data,
          ([d]) => d.value,
          (d) => d.year,
          (d) => d.name
        )
      )
        .map(([date, data]) => [new Date(date), data])
        .sort(([a], [b]) => d3.ascending(a, b));
      nameframes = d3.groups(
        keyframes().flatMap(([, data]) => data),
        (d) => d.name
      );
      prev = new Map(
        nameframes.flatMap(([, data]) => d3.pairs(data, (a, b) => [b, a]))
      );
      next = new Map(nameframes.flatMap(([, data]) => d3.pairs(data)));
      this.play(data);
    },
  },
};

function bars(svg) {
  let bar = svg.append("g").attr("fill-opacity", 0.6).selectAll("rect");
  // 创建一个线性颜色比例尺
  var colorScale = d3
    .scaleLinear()
    .domain([0, 100]) // 输入范围从0到100
    .range(["red", "purple"]); // 输出范围从红色到绿色
  return ([date, data], transition) =>
    (bar = bar
      .data(data.slice(0, n), (d) => d.name)
      .join(
        (enter) =>
          enter
            .append("rect")
            .attr("fill", (d, i) => d3.schemeTableau10[d3.randomInt(14)()]) //(d, i) => d3.schemeTableau10[d3.randomInt(12)()]
            .attr("height", y.bandwidth())
            .attr("x", x(0))
            .attr("y", (d) => y((prev.get(d) || d).rank))
            .attr("width", (d) => x((prev.get(d) || d).value) - x(0)),
        (update) => update,
        (exit) =>
          exit
            .transition(transition)
            .remove()
            .attr("y", (d) => y((next.get(d) || d).rank))
            .attr("width", (d) => x((next.get(d) || d).value) - x(0))
      )
      .call((bar) =>
        bar
          .transition(transition)
          .attr("y", (d) => y(d.rank))
          .attr("width", (d) => x(d.value) - x(0))
      ));
}

//设置标签
function labels(svg) {
  let label = svg
    .append("g")
    .style("font", "bold 12px var(--Helvetica)")
    .style("font-variant-numeric", "tabular-nums")
    .attr("text-anchor", "end")
    .selectAll("text");

  return ([date, data], transition) =>
    (label = label
      .data(data.slice(0, n), (d) => d.name)
      .join(
        (enter) =>
          enter
            .append("text")
            .attr(
              "transform",
              (d) =>
                `translate(${x((prev.get(d) || d).value)},${y(
                  (prev.get(d) || d).rank
                )})`
            )
            .attr("y", y.bandwidth() / 2)
            .attr("x", -6)
            .attr("dy", "0.18em")
            .text((d) => d.name)
            .call((text) =>
              text
                .append("tspan")
                .attr("fill-opacity", 1)
                .attr("font-weight", "normal")
                .attr("x", 46)
                .attr("dy", "0.15em")
            ),
        (update) => update,
        (exit) =>
          exit
            .transition(transition)
            .remove()
            .attr(
              "transform",
              (d) =>
                `translate(${x((next.get(d) || d).value)},${y(
                  (next.get(d) || d).rank
                )})`
            )
            .call((g) =>
              g
                .select("tspan")
                .tween("text", (d) =>
                  textTween(d.value, (next.get(d) || d).value)
                )
            )
      )
      .call((bar) =>
        bar
          .transition(transition)
          .attr("transform", (d) => `translate(${x(d.value)},${y(d.rank)})`)
          .call((g) =>
            g
              .select("tspan")
              .tween("text", (d) =>
                textTween((prev.get(d) || d).value, d.value)
              )
          )
      ));
}

function textTween(a, b) {
  const i = d3.interpolateNumber(a, b);
  return function (t) {
    this.textContent = formatNumber(i(t));
  };
}

var formatNumber = d3.format(",d");

function axis(svg) {
  const g = svg
    .append("g")
    .attr("transform", "translate(0,16)")
    .style("font-size", "15px");

  const axis = d3
    .axisTop(x)
    .ticks(width / 160)
    .tickSizeOuter(0)
    .tickSizeInner(-barSize * (n + y.padding()));

  return (_, transition) => {
    g.transition(transition).call(axis);
    g.select(".tick:first-of-type text").remove();
    g.selectAll(".tick:not(:first-of-type) line").attr("stroke", "white");
    g.select(".domain").remove();
  };
}

var formatDate = d3.utcFormat("%Y");

function ticker(svg) {
  const now = svg
    .append("text")
    .style("font-size", "40px")
    .style("font-weight", "bold")
    .style("font-variant-numeric", "tabular-nums")
    .attr("text-anchor", "end")
    .attr("x", width - 6)
    .attr("y", margin.top + barSize * (n - 0.45))
    .attr("dy", "0.32em");

  return ([date], transition) => {
    transition.end().then(() => now.text(formatDate(date)));
  };
}
</script>
  
  <style>
#selectSection {
  margin-top: 1.25rem;
  margin-bottom: 1.25rem;
}
#category {
  color: #273747;
  font-family: helvetica;
  font-size: 0.875rem;
  width: 5.625rem;
  height: 1.75rem;
  border: 0.125rem solid rgb(43, 189, 218);
  appearance: none;
  background-color: rgb(235, 239, 242);
  background: url(../assets/down.png) 4.0625rem center no-repeat;
  padding-left: 0.3125rem;
}
#area {
  color: rgb(63, 71, 39);
  font-family: helvetica;
  font-size: 0.875rem;
  width: 5.625rem;
  height: 1.75rem;
  border: 0.125rem solid rgb(43, 189, 218);
  appearance: none;
  background-color: rgb(235, 239, 242);
  background: url(../assets/down.png) 4.0625rem center no-repeat;
  padding-left: 0.3125rem;
}
button {
  color: #273747;
  margin-left: 0.625rem;
  font-family: helvetica;
  font-size: 0.875rem;
  width: 5.625rem;
  height: 1.75rem;
  border: 0.125rem solid rgb(247, 105, 25);
  appearance: none;
  background-color: rgb(235, 239, 242);
  padding-left: 0.3125rem;
}
#category:hover {
  background-color: rgba(189, 196, 202, 70%);
}
button:hover {
  background-color: rgba(189, 196, 202, 70%);
}
</style>
  