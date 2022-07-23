<template>
<svg id="calScoreSvg"></svg>
</template>

<script>
import * as d3 from "d3";
import {getVisualizationSizeConstraint, getDataRange, getGridData} from '../utils/detailview-utils'
// import {getDataRange} from '../utils/detailview-utils'
// import {config} from '../utils/config'
export default {
  name:"AttentionCalScoreAnimator",
  props:{
    Q: {
      type: Array,
      default: function(){return [];},
    },
    K: {
      type: Array,
      default: function(){return [];},
    },
    QKT: {
      type: Array,
      default: function(){return [];},
    },
    highlights: {
      type: Array,
      default: function(){return [];},
    },
    openHighlights: {
      type: Boolean,
      default: true,
    },
  },
  emits:['cleanComponentView','changeCalScoreHilights',],
  data(){
    return {
      svgLeftWidth:400,
    };
  },
  created(){
    // console.log('Calculate Score Q mat:',this.Q);
    // console.log('Calculate Score K mat:',this.K);
    // console.log('Calculate Score QKT mat:',this.QKT);
  },
  beforeUpdate(){
    // this.init();
    this.redraw();
  },
  mounted(){
    // console.log('Calculate Score Q mat:',this.Q);
    // console.log('Calculate Score K mat:',this.K);
    // console.log('Calculate Score QKT mat:',this.QKT);
    // this.init();
    this.redraw();
  },
  methods:{
    onClean(){
      this.$emit('cleanComponentView');
    },
    init(){
   
    },

    redraw(){
      // 移除之前所绘制的内容
      d3.selectAll('#calScoreSvg > *').remove();
      d3.select('#calScoreSvg').attr('width',1200).attr('height',350);
      
      let svg = d3.select('#calScoreSvg');
      let fontSize = 20;
      let interval = 100;
      let maximumCellSize = 30;

      // 绘制 svg 标题
      let title = svg.append('text')//.attr("text-anchor","middle");
          title
            .attr('transform',`translate(${ 25 },${ 25 })`)
            .attr('class','title-text')
            .attr('dy','.3em')
            .style('font-weight','bold')
            .style('font-size',fontSize)
            .text('1. Calculate Score');

      let colorScale = d3.interpolateRdBu;


      let qGroupX = 75;
      let qGroupY = 115;
      let xSizeOfQGrid = 512;
      let ySizeOfQGrid = 160;
      let qData = this.Q;
      let qDataRange = getDataRange(this.Q);
      let qText = `Q (${qData.length},${qData[0].length})`;
      let qSymbol = '*';
      
      let kGroupX = qGroupX + xSizeOfQGrid + interval;
      let kGroupY = 35;
      let xSizeOfKGrid = ySizeOfQGrid;
      let ySizeOfKGrid = xSizeOfQGrid*3/5;
      let kData = transpose(this.K);
      let kDataRange = getDataRange(this.K);
      let kText = `K.T (${kData.length},${kData[0].length})`;
      let kSymbol = '=';
      
      let resGroupX = kGroupX + xSizeOfKGrid + interval;
      let resGroupY = qGroupY;
      let xSizeOfResGrid = ySizeOfQGrid;
      let ySizeOfResGrid = ySizeOfQGrid;
      let resData = this.QKT;
      let resDataRange = getDataRange(this.QKT);
      let resText = `Q*K.T (${resData.length},${resData[0].length})`;
      let resSymbol = null;

      let qGroup = svg.append('g').attr('class','query-group')
          .attr('transform',`translate(${qGroupX},${qGroupY})`);
      let kGroup = svg.append('g').attr('class','key-group')
          .attr('transform',`translate(${kGroupX},${kGroupY})`);
      let resGroup = svg.append('g').attr('class','multiplied-group')
          .attr('transform',`translate(${resGroupX},${resGroupY})`);

      drawMatrix.call(this, qGroup, 'Q', qData, xSizeOfQGrid, ySizeOfQGrid, interval, maximumCellSize, qDataRange, colorScale, qText, qSymbol);
      drawMatrix.call(this, kGroup, 'K', kData, xSizeOfKGrid, ySizeOfKGrid, interval, maximumCellSize, kDataRange, colorScale, kText, kSymbol);
      drawMatrix.call(this, resGroup, 'RES', resData, xSizeOfResGrid, ySizeOfResGrid, interval, maximumCellSize, resDataRange, colorScale, resText, resSymbol);

      function transpose(data){
        let rows = data.length;
        let cols = data[0].length;
        let transposedData = [];
        for(let c=0; c<cols; c++){
          let column = [];
          for(let r=0; r<rows; r++){
            column.push(data[r][c]);
          }
          transposedData.push(column);
        }
        return transposedData;
      }

      // function drawMatirx(group, data, sizeX, sizeY, maximumCellSize, dataRange, colorMapper, text, symbol){
      function drawMatrix(group, type, data, sizeX, sizeY, xInetrval, maximumCellSize, dataRange, colorMapper, text, symbol){

        let constraintGridCellWidth = getVisualizationSizeConstraint(data[0].length, 'x', sizeX, sizeY, maximumCellSize);
        let constraintGridCellHeight = getVisualizationSizeConstraint(data.length, 'y', sizeX, sizeY, maximumCellSize);

        let gridData = getGridData(data, constraintGridCellWidth, constraintGridCellHeight);
        let gridGroup = group.append("g").attr("class","grid")
        let gridRow = gridGroup.selectAll(".row")  // 绘制每一行
            .data(gridData).enter().append('g').attr('class','row');
        gridRow
          .selectAll(".square")
            .data(d=>d).enter().append('rect')
            .attr('class','square')
            .attr("x",d=>d.x).attr("y",d=>d.y)
            .attr("width",d=>d.width).attr("height",d=>d.height)
            .attr('opacity',0.9)
            .on('click',(event,d)=>{
              if(type=="RES"){
                if(this.highlights[0]!=d.row || this.highlights[1]!=d.col) this.$emit('changeCalScoreHilights', [d.row,d.col]);
                else this.$emit('changeCalScoreHilights', [-1,-1]);
              }
            })
            .style('stroke',d=>{
              if(this.openHighlights){
                if(type=="Q"){
                  if(this.highlights[0]==d.row) return 'purple';
                  else return null;
                } else if (type=="K") {
                  if(this.highlights[1]==d.col) return 'purple';
                  else return null;
                } else {
                  if(this.highlights[0]==d.row && this.highlights[1]==d.col) return 'purple';
                  else return null;
                }
              }
              return null;
            })
            .style('stroke-width',1.2)
            .style('fill',d=>{
              let normlizedVal = (d.text-dataRange.min)/(dataRange.max-dataRange.min);
              return colorMapper(normlizedVal);
            });
          

        let totalGridWidth = constraintGridCellWidth * data[0].length;
        let totalGridHeight = constraintGridCellHeight * data.length;

        let gridText = group.append('text').attr("text-anchor","middle");
          gridText
            .attr('transform',`translate(${ totalGridWidth/2},${-20})`)
            .attr('class','title-text')
            .attr('dy','.3em')
            .style('font-weight','bold')
            .style('font-size',fontSize/1.2)
            .text(text);

        if(symbol!=null){
          let symbolText = group.append('text').attr("text-anchor","middle");
          symbolText
            .attr('transform',`translate(${ totalGridWidth + xInetrval/2},${totalGridHeight/2})`)
            .attr('class','title-text')
            .attr('dy',symbol=="*"?'.55em':'.3em')
            .style('font-weight','bold')
            .style('font-size',symbol=="*"?fontSize*1.6:fontSize)
            .text(symbol);
        }
      }
    },
  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
.container {
  display: flex;
  flex-direction:row;
  justify-content: space-between;
  align-items: center;
  box-shadow: rgb(236, 231, 231) 2px 2px 11px;
  border-radius: .5rem;
  background-color: white;
  width:100%;
  height:100%;
}

.box {
  padding: 5px 15px 10px 15px;
  display: flex;
  flex-direction:column;
  justify-content: space-between;
  /* align-items: center; */
  align-items: stretch;
  width:100%;
  height:100%;
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
  /* font-weight: 500; */
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

/*
#left-column{
  width:60%;
  height:92%;
}

#right-column{
  width:40%;
  height:92%;
}
*/
</style>