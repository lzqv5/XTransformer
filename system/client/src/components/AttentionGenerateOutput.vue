<template>
<svg id="attentionOuputSvg"></svg>
</template>

<script>
import * as d3 from "d3";
// import {getVisualizationSizeConstraint, getDataRange, getGridData} from '../utils/detailview-utils'
import {getVisualizationSizeConstraint, getGridData} from '../utils/detailview-utils'
// import {getDataRange} from '../utils/detailview-utils'
// import {config} from '../utils/config'
export default {
  name:"AttentionGenerateOutput",
  props:{
    V: {
      type: Array,
      default: function(){return [[0]];},
    },
    afterSoftmax: {
      type: Array,
      default: function(){return [];},
    },
    output: {
      type: Array,
      default: function(){return [];},
    },
    attentionOuputTotalDataRange: {
      type: Array,
      default: function(){return [];},
    },
    headNum: {
      type: Number,
      default: 0,
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
  emits:['cleanComponentView','changeOutputHilights',],
  data(){
    return {
      svgLeftWidth:400,
    };
  },
  created(){
  },
  beforeUpdate(){
    this.redraw();
  },
  mounted(){
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
      d3.selectAll('#attentionOuputSvg > *').remove();
      d3.select('#attentionOuputSvg').attr('width',1200).attr('height',260);
      
      let svg = d3.select('#attentionOuputSvg');
      let fontSize = 20;
      let interval = 80;
      let maximumCellSize = 30;

      // 绘制 svg 标题
      let title = svg.append('text')//.attr("text-anchor","middle");
          title
            .attr('transform',`translate(${ 25 },${ 25 })`)
            .attr('class','title-text')
            .attr('dy','.3em')
            .style('font-weight','bold')
            .style('font-size',fontSize)
            .text(`4. Calculate output in head ${1 + this.headNum}`);

      let colorScale = d3.interpolateRdBu;

      let softmaxGroupX = 75;
      let softmaxGroupY = 75;
      let xSizeOfSoftmaxGrid = 160;
      let ySizeOfSoftmaxGrid = 160;
      let softmaxData = this.afterSoftmax;
      let singleGridWidth = Math.max(xSizeOfSoftmaxGrid/softmaxData[0].length, maximumCellSize)
      let xRealSize = singleGridWidth*softmaxData[0].length;
      let softmaxDataRange = {max:1,min:0};
      let softmaxText = `Normalized Score (${softmaxData.length},${softmaxData[0].length})`;
      let softmaxSymbol = '*';

      let vGroupX = softmaxGroupX + xRealSize + interval ;
      let vGroupY = softmaxGroupY;
      let xSizeOfVGrid = 384;
      let ySizeOfVGrid = 160;
      let vData = this.V;
      // let vDataRange = getDataRange(this.V);
      let vDataRange = this.attentionOuputTotalDataRange;
      let vText = `V (${vData.length},${vData[0].length})`;
      let vSymbol = '=';
      
      let outputGroupX = vGroupX + xSizeOfVGrid + interval;
      let outputGroupY = vGroupY;
      let xSizeOfOutputGrid = xSizeOfVGrid;
      let ySizeOfOutputGrid = ySizeOfVGrid;
      let outputData = this.output;
      console.log('this.output:',this.output);
      // let kDataRange = getDataRange(this.K);
      let outputDataRange = this.attentionOuputTotalDataRange;
      console.log('this.attentionOuputTotalDataRange:',this.attentionOuputTotalDataRange);
      let outputText = `output (${outputData.length},${outputData[0].length})`;
      // let outputText = `output `;
      let outputSymbol = null;

      let softmaxGroup = svg.append('g').attr('class','softmax-weight-group')
          .attr('transform',`translate(${softmaxGroupX},${softmaxGroupY})`);
      let vGroup = svg.append('g').attr('class','value-group')
          .attr('transform',`translate(${vGroupX},${vGroupY})`);
      let outputGroup = svg.append('g').attr('class','output-group')
          .attr('transform',`translate(${outputGroupX},${outputGroupY})`);

      drawMatrix.call(this, softmaxGroup, 'softmax', softmaxData, xSizeOfSoftmaxGrid, ySizeOfSoftmaxGrid, interval, maximumCellSize, softmaxDataRange, colorScale, softmaxText, softmaxSymbol);
      drawMatrix.call(this, vGroup, 'V', vData, xSizeOfVGrid, ySizeOfVGrid, interval, maximumCellSize, vDataRange, colorScale, vText, vSymbol);
      drawMatrix.call(this, outputGroup, 'output', outputData, xSizeOfOutputGrid, ySizeOfOutputGrid, interval, maximumCellSize, outputDataRange, colorScale, outputText, outputSymbol);

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
              if(type=="output"){
                if(this.highlights[0]!=d.row || this.highlights[1]!=d.col) this.$emit('changeOutputHilights', [d.row,d.col]);
                else this.$emit('changeOutputHilights', [-1,-1]);
              }
            })
            .style('stroke',d=>{
              if(this.openHighlights){
                if(type=="softmax"){
                  if(this.highlights[0]==d.row) return 'black';
                  else return null;
                } else if (type=="V") {
                  if(this.highlights[1]==d.col) return 'black';
                  else return null;
                } else {
                  if(this.highlights[0]==d.row && this.highlights[1]==d.col) return 'black';
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