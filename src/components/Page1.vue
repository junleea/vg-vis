<!--
 * @Author: lijun lijun.lj@foxmail.com
 * @Date: 2023-11-02 17:49:12
 * @LastEditors: lijun lijun.lj@foxmail.com
 * @LastEditTime: 2023-11-02 20:00:42
 * @FilePath: \vue-project\src\components\Page1.vue
 * @Description: 这是默认设置,请设置`customMade`, 打开koroFileHeader查看配置 进行设置: https://github.com/OBKoro1/koro1FileHeader/wiki/%E9%85%8D%E7%BD%AE
-->

<template>
	<h1>Chart</h1>
	<div class="Echarts">
    <div id="main" style="width: 600px;height:400px;"></div>
  </div>
</template>
    
<script>
import { ref } from 'vue'
import axios from 'axios'
import * as  echarts from 'echarts'
  
export default {
    data() {
      return {
        items: [],
        name: "",
        age: "",
        post: []
      }
    },
    methods:{
	  myEcharts(){
		  // 基于准备好的dom，初始化echarts实例
		  var myChart = this.$echarts.init(document.getElementById('main'));

		  // 指定图表的配置项和数据
		  var option = {
			  title: {
				  text: 'ECharts 入门示例'
			  },
			  tooltip: {},
			  legend: {
				  data:['销量']
			  },
			  xAxis: {
				  data: ["衬衫","羊毛衫","雪纺衫","裤子","高跟鞋","袜子"]
			  },
			  yAxis: {},
			  series: [{
				  name: '销量',
				  type: 'bar',
				  data: [5, 20, 36, 10, 10, 20]
			  }]
		  };

		  // 使用刚指定的配置项和数据显示图表。
		  myChart.setOption(option);
		  }
  },
  mounted() {
  	this.myEcharts();
  }
}

</script>