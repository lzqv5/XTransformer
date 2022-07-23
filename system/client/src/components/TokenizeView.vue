<template>
  <div class="container">
    <div class="box">
      <div class="control-pannel">
        <div></div>
        <div class="title-text">
          Tokenize - From Text to Tokens
        </div>
        <div class="buttons">
          <!--<div class="delete-button control-button" tilte="Close"
            @click="onExit()">
            <button>x</button>
          </div>-->
          <el-tooltip content="Quit from Tokenize View." placement="top" effect="dark">
            <el-button type="primary" :icon="CloseBold" plain circle @click="onExit()" />
          </el-tooltip>
        </div>
      </div>
      <div class="container" id="svgContainer">
        <svg  id="mainSvg">
        </svg>
      </div>
    </div>
  </div>
</template>

<script>
import * as d3 from "d3";
import { shallowRef } from "vue"
import { CloseBold } from '@element-plus/icons-vue'
export default {
  name:"TokenizeView",
  props:{
    // node: {
    //   type: Object,
    //   default: function(){return {}},
    // },
    id: {
      type: String,
      default: "",
    },
    text: {
      type: String,
      default: "",
    },
    pieces: {
      type: Array,
      default: function(){return [];},
    },
    tokens: {
      type: Array,
      default: function(){return [];},
    },
  },
  emits:["exit"],
  data(){
    return {
       CloseBold:shallowRef(CloseBold),
    };
  },
  mounted(){
    this.redraw();
  },
  methods:{
    onClick(){
      console.log("click TokenizeView Btn...");
    },
    onExit(){
      console.log("exit from the current view.");
      this.$emit('exit');
    },
    redraw(){
      // 移除原来已绘制的所有图元, 并在后续根据新的数据重新绘制
      d3.select("#svgContainer").selectAll('#mainSvg > *').remove();
      // console.log(this.id);
      // console.log(this.text);
      // console.log(this.pieces);
      // console.log(this.tokens);

      let fontSize = 20;
      let type =this.id.split("-")[0];
      let tokenUnitLength = 10;
      let unitLength = type=="encoder"?10:15;

      let textLength = this.text.length * unitLength;
      let piecesLength = this.pieces.toString().length * unitLength;
      let tokensLength = this.tokens.toString().length * tokenUnitLength;
      let maxLength = Math.max(textLength, piecesLength, tokensLength);

      let reservedWidth = 25;
      let reservedHeight = 20;
      let lineLength = 50;
      // let rectWidth = numTokens*spacePerToken;
      let rectWidth = Math.ceil( maxLength * 1.4);
      let rectHeight = 40;
      let svgWidth = rectWidth + reservedWidth * 2;
      let svgHeight = rectHeight * 3 + reservedHeight * 2 + lineLength * 2;
      let g1TransY = reservedHeight,
          g2TransY = reservedHeight+rectHeight+lineLength,
          g3TransY = reservedHeight+2*rectHeight+2*lineLength;
      
      let line1Start = {x:reservedWidth+rectWidth/2, y:reservedHeight + rectHeight},
          line1End = {x:reservedWidth+rectWidth/2, y:reservedHeight + rectHeight + lineLength},
          line2Start = {x:reservedWidth+rectWidth/2, y:reservedHeight + 2*rectHeight + lineLength},
          line2End = {x:reservedWidth+rectWidth/2, y:reservedHeight + 2*rectHeight + 2*lineLength};

      let lineText1 = {x:reservedWidth + rectWidth/2 , y:reservedHeight + rectHeight + lineLength/2},
          lineText2 = {x:reservedWidth + rectWidth/2 , y:reservedHeight + rectHeight*2 + lineLength*3/2};

      let margin = {top:10,right:30,bottom:30,left:10},
        width = svgWidth - margin.left - margin.right,
        height = svgHeight - margin.top - margin.bottom;
      
      let svg = d3.select('#mainSvg')
        .attr('width',width + margin.left + margin.right)
        .attr('height',height + margin.top + margin.bottom);
      
      // 添加矩形
      let g1 = svg.append('g').attr('transform',`translate(${reservedWidth},${g1TransY})`);
          // .style('text-align','center'); 
      g1.append('rect')
        .attr('width',rectWidth)
        .attr('height',rectHeight)
        .attr('fill',"#fff")
        .attr('stroke',"#000");
      g1.append('text')
        .style("text-anchor","middle")
        .style("dominant-baseline","middle")
        .attr("x", rectWidth/2)
        .attr("y", rectHeight/2)
        .attr("font-size",fontSize+'px')
        .text(this.text);
      
      let g2 = svg.append('g').attr('transform',`translate(${reservedWidth},${g2TransY})`);
      g2.append('rect')
        .attr('width',rectWidth)
        .attr('height',rectHeight)
        .attr('fill',"#fff")
        .attr('stroke',"#000");
      g2.append('text')
        .style("text-anchor","middle")
        .style("dominant-baseline","middle")
        .attr("x", rectWidth/2)
        .attr("y", rectHeight/2)
        .attr("font-size",fontSize+'px')
        // .text("[" + this.pieces.toString().split(",").join(", ") + "]");
        .text("[" + this.pieces.toString() + "]");
      
      let g3 = svg.append('g').attr('transform',`translate(${reservedWidth},${g3TransY})`);
      g3.append('rect')
        .attr('width',rectWidth)
        .attr('height',rectHeight)
        .attr('fill',"#fff")
        .attr('stroke',"#000");
      g3.append('text')
        .style("text-anchor","middle")
        .style("dominant-baseline","middle")
        .attr("x", rectWidth/2)
        .attr("y", rectHeight/2)
        .attr("font-size",fontSize+'px')
        .text("[" + this.tokens.toString() + "]");
    
      // 添加 marker(箭头)
      svg.append('g')
        .append("marker")
        .attr("id", "resolved")
        .attr("markerUnits","userSpaceOnUse")
        .attr("viewBox", "0 -5 10 10")//坐标系的区域
        .attr("refX",10)//箭头坐标
        .attr("refY", 0)
        .attr("markerWidth", 4)//标识的大小
        .attr("markerHeight", 8)
        .attr("orient", "auto")//绘制方向，可设定为：auto（自动确认方向）和 角度值
        .attr("stroke-width",4)//箭头宽度
        .append("path")
        .attr("d", "M0,-5L10,0L0,5")//箭头的路径     
        .attr("stroke-opacity", 0.2);
      
      // 添加边线
      svg.append('line')
        .attr('x1',line1Start.x)
        .attr('x2',line1End.x)
        .attr('y1',line1Start.y)
        .attr('y2',line1End.y)
        .attr('stroke','#000')
        .attr('stroke-width',1)
        .attr("marker-end", "url(#resolved)");
      svg.append('line')
        .attr('x1',line2Start.x)
        .attr('x2',line2End.x)
        .attr('y1',line2Start.y)
        .attr('y2',line2End.y)
        .attr('stroke','#000')
        .attr('stroke-width',1)
        .attr("marker-end", "url(#resolved)");
      
      // 添加注释
      svg.append('text')
        .attr("x", lineText1.x)
        .attr("y", lineText1.y)
        .attr("dx", ".3em")
        .attr("dy", ".3em")
        // .attr("font-size",fontSize/2+'px')
        .text('Text-to-Pieces');
      svg.append('text')
        .attr("x", lineText2.x)
        .attr("y", lineText2.y)
        .attr("dx", ".3em")
        .attr("dy", ".3em")
        // .attr("font-size",fontSize/2+'px')
        .text('Pieces-to-Tokens');
    }
  },
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
.container {
  display: flex;
  justify-content: space-between;
  align-items: center;
  box-shadow: rgb(236, 231, 231) 2px 2px 11px;
  border-radius: .5rem;
  background-color: white;
}

.box {
  padding: 5px 15px 10px 15px;
}

.control-pannel {
  display: flex;
  position: relative;
  flex-direction: row;
  /* justify-content: center; */
  justify-content: space-between;
  align-items: center;
}

.title-text {
  font-size: 1.2em;
  font-weight: bold;
  color: #4a4a4a;
}

.buttons {
  cursor: pointer;
  display:flex;
  flex-direction: row;
}

.control-button {
  color: gray;
  /* font-size: 15px; */
  opacity: 0.8;
  cursor: pointer;
  margin-bottom: 2.5px;
}

.control-button:not(:first-child) {
  margin-left: 5px;
}
</style>