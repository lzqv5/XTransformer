<template>
<svg id="scaleoutSvg"></svg>
</template>

<script>
import * as d3 from "d3";
import {getVisualizationSizeConstraint, getDataRange, getGridData} from '../utils/detailview-utils'
// import {getDataRange} from '../utils/detailview-utils'
// import {config} from '../utils/config'
export default {
  name:"AttentionScaleOut",
  props:{
    QKT: {
      type: Array,
      default: function(){return [];},
    },
    QKTdivided: {
      type: Array,
      default: function(){return [];},
    },
    mask: {
      type: Array,
      default: function(){return [];},
    },
    maskedQKTdivided: {
      type: Array,
      default: function(){return [];},
    },
    coefficient: {
      type: Number,
      default: 8,
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
  emits:['cleanComponentView','changeScaleMaskHilights',],
  data(){
    return {
      svgLeftWidth:400,
    };
  },
  created(){
  },
  beforeUpdate(){
    // this.init();
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
      d3.selectAll('#scaleoutSvg > *').remove();
      d3.select('#scaleoutSvg').attr('width',1200).attr('height',260);
      
      let svg = d3.select('#scaleoutSvg');
      let fontSize = 20;
      let interval = 100;
      let maximumCellSize = 40;

      // 绘制 svg 标题
      let title = svg.append('text')//.attr("text-anchor","middle");
          title
            .attr('transform',`translate(${ 15 },${ 15 })`)
            .attr('class','title-text')
            .attr('dy','.3em')
            .style('font-weight','bold')
            .style('font-size',fontSize)
            .text('2. Scale and Mask');

      let colorScale = d3.interpolateRdBu;      
    
      let scoreGroupX = 80;
      let scoreGroupY = 75;
      let xSizeOfScoreGrid = 160;
      let ySizeOfScoreGrid = 160;
      let scoreData = this.QKT;
      let scoreDataRange = getDataRange(this.QKT);
      let scoreText = `Q*K.T (${scoreData.length},${scoreData[0].length})`;
      let scoreSymbol = null;
      
      let dividedScoreGroupX = scoreGroupX + xSizeOfScoreGrid + 2.5*interval;
      let dividedScoreGroupY = scoreGroupY;
      let xSizeOfDividedScoreGrid = 160;
      let ySizeOfDividedScoreGrid = 160;
      let dividedScoreData = this.QKTdivided;
      // let dividedScoreDataRange = getDataRange(this.QKTdivided);
      let dividedScoreText = `Q*K.T/coef   (${dividedScoreData.length},${dividedScoreData[0].length})`;
      let dividedScoreSymbol = null;
      
      let maskedScoreGroupX = dividedScoreGroupX + xSizeOfScoreGrid + 2.5*interval;
      let maskedScoreGroupY = dividedScoreGroupY;
      let xSizeOfMaskedScoreGrid = 160;
      let ySizeOfMaskedScoreGrid = 160;
      let maskedScoreData = this.maskedQKTdivided;
      // let dividedScoreDataRange = getDataRange(this.QKTdivided);
      let maskedScoreText = `Masked(Q*K.T/coef)   (${maskedScoreData.length},${maskedScoreData[0].length})`;
      let maskedScoreSymbol = null;
      
      let maskGroupX = dividedScoreGroupX + xSizeOfScoreGrid + (2.5*interval)/2;
      let maskGroupY = dividedScoreGroupY;
      let xSizeOfMaskGrid = 80;
      let ySizeOfMaskGrid = 80;
      let maskData = this.mask;
      // let dividedScoreDataRange = getDataRange(this.QKTdivided);
      let maskText = `Mask Op. (${maskData.length},${maskData[0].length})`;
      let maskSymbol = null;

      let scoreGroup = svg.append('g').attr('class','score-group')
          .attr('transform',`translate(${scoreGroupX},${scoreGroupY})`);
      let dividedScoreGroup = svg.append('g').attr('class','dividedScore-group')
          .attr('transform',`translate(${dividedScoreGroupX},${dividedScoreGroupY})`);
      let maskedScoreGroup = svg.append('g').attr('class','MaskedScore-group')
          .attr('transform',`translate(${maskedScoreGroupX},${maskedScoreGroupY})`);
      let maskGroup = svg.append('g').attr('class','MaskedScore-group')
          // .attr('transform',`translate(${maskGroupX-xSizeOfMaskGrid/2},${maskGroupY-ySizeOfMaskGrid/2})`);
          .attr('transform',`translate(${maskGroupX-xSizeOfMaskGrid/2},${maskGroupY-ySizeOfMaskGrid/2})`);

      drawMatrix.call(this, scoreGroup, 'score', scoreData, xSizeOfScoreGrid, ySizeOfScoreGrid, interval, maximumCellSize, scoreDataRange, colorScale, scoreText, scoreSymbol);
      drawMatrix.call(this, dividedScoreGroup, 'divide', dividedScoreData, xSizeOfDividedScoreGrid, ySizeOfDividedScoreGrid, interval, maximumCellSize, scoreDataRange, colorScale, dividedScoreText, dividedScoreSymbol);
      drawMatrix.call(this, maskedScoreGroup, 'masked', maskedScoreData, xSizeOfMaskedScoreGrid, ySizeOfMaskedScoreGrid, interval, maximumCellSize, scoreDataRange, colorScale, maskedScoreText, maskedScoreSymbol);
      drawMatrix.call(this, maskGroup, 'mask', maskData, xSizeOfMaskGrid, ySizeOfMaskGrid, interval, maximumCellSize, {max:1,min:0}, colorScale, maskText, maskSymbol);

      // draw Equation of divide
      let divideGroupX = scoreGroupX + xSizeOfScoreGrid + interval*0.58;
      let divideGroupY = scoreGroupY + ySizeOfScoreGrid/2;
      let divideGroup = svg.append('g').attr('class','divide-group')
          .attr('transform',`translate(${divideGroupX},${divideGroupY})`);
      let lineWidth = interval*0.5;
      let lineStrokeWidth = 2;
      divideGroup.append('line').attr('class', 'separation-line')
        .attr('x1',0).attr('y1',1).attr('x2',lineWidth).attr('y2',1)
        // .attr('fill','none')
        .style('stroke-width', lineStrokeWidth).style('stroke', 'gray');
      divideGroup.append('text').attr('class', 'denominator')
        .style("font-size", 16).style('text-anchor','middle')
        .attr('transform',`translate(${lineWidth/2},${maximumCellSize*0.6})`)
        // .text(this.coefficient);
        .text(`${this.coefficient}`);
      divideGroup.append('text').attr('class', 'equal')
        .style("font-size", 25).style("font-weight", 'bold')//.style('text-anchor','middle')
        .attr('transform',`translate(${lineWidth + maximumCellSize*0.4},${5})`)
        // .text(this.coefficient);
        .text('=');
      
      let divideNumeratorGridData = getGridData([[scoreData[this.highlights[0]][this.highlights[1]]]],maximumCellSize,maximumCellSize)
      let divideRow = divideGroup.selectAll(".rowNum")  // 绘制每一行
            .data(divideNumeratorGridData).enter().append('g').attr('class','rowNum')
            .attr('transform',`translate(${lineWidth/6},${-1.25*maximumCellSize})`);
        divideRow
          .selectAll(".square")
            .data(d=>d).enter().append('rect')
            .attr('class','square')
            .attr("x",d=>d.x).attr("y",d=>d.y)
            .attr("width",d=>d.width).attr("height",d=>d.height)
            .attr('opacity',0.9)
            .style('stroke','black')
            .style('stroke-width',1.2)
            .style('fill',d=>{
              let normlizedVal = (d.text-scoreDataRange.min)/(scoreDataRange.max-scoreDataRange.min);
              return colorScale(normlizedVal);
            });
        divideRow
          .selectAll(".text")
          .data(d=>d)
          .enter().append("text")
          .attr("class","text")
          .style("font-size", 10)
          .attr("x", d=>d.x+d.width/2)
          .attr("y", d=>d.y+d.height/2)
          .style("fill", d=>{  // 为颜色设置填充色
            // let normlizedVal = (d.text-this.dataRange.min)/(this.dataRange.max-this.dataRange.min);
            let normlizedVal = (d.text-scoreDataRange.min)/(scoreDataRange.max-scoreDataRange.min);
            if(normlizedVal < 0.2 || normlizedVal > 0.8){
              return 'white';
            } else {
              return 'black';
            }
          })
          .style("text-anchor","middle")
          .style("dominant-baseline","middle")
          .text(d=>d.text)
      
      let resGridData = getGridData([[dividedScoreData[this.highlights[0]][this.highlights[1]]]],maximumCellSize,maximumCellSize)
      let resGridRow = divideGroup.selectAll(".rowRes")  // 绘制每一行
            .data(resGridData).enter().append('g').attr('class','rowRes')
            .attr('transform',`translate(${lineWidth + maximumCellSize*1.2},${-maximumCellSize/1.6})`);
        resGridRow
          .selectAll(".square")
            .data(d=>d).enter().append('rect')
            .attr('class','square')
            .attr("x",d=>d.x).attr("y",d=>d.y)
            .attr("width",d=>d.width).attr("height",d=>d.height)
            .attr('opacity',0.9)
            .style('stroke','black')
            .style('stroke-width',1.2)
            .style('fill',d=>{
              let normlizedVal = (d.text-scoreDataRange.min)/(scoreDataRange.max-scoreDataRange.min);
              return colorScale(normlizedVal);
            });
        resGridRow
          .selectAll(".text")
          .data(d=>d)
          .enter().append("text")
          .attr("class","text")
          .style("font-size", 10)
          .attr("x", d=>d.x+d.width/2)
          .attr("y", d=>d.y+d.height/2)
          .style("fill", d=>{  // 为颜色设置填充色
            // let normlizedVal = (d.text-this.dataRange.min)/(this.dataRange.max-this.dataRange.min);
            let normlizedVal = (d.text-scoreDataRange.min)/(scoreDataRange.max-scoreDataRange.min);
            if(normlizedVal < 0.2 || normlizedVal > 0.8){
              return 'white';
            } else {
              return 'black';
            }
          })
          .style("text-anchor","middle")
          .style("dominant-baseline","middle")
          .text(d=>d.text)

        
      // draw Mask Equation
      let maskEqGroupX = dividedScoreGroupX + xSizeOfDividedScoreGrid + interval*0.58;
      let maskEqGroupY = dividedScoreGroupY + ySizeOfDividedScoreGrid/2;
      let maskEqGroup = svg.append('g').attr('class','mask-op-group')
          .attr('transform',`translate(${maskEqGroupX},${maskEqGroupY})`);
      let maskGridData = getGridData([[maskData[this.highlights[0]][this.highlights[1]]]],maximumCellSize,maximumCellSize)
      let maskedResGridData = getGridData([[maskedScoreData[this.highlights[0]][this.highlights[1]]]],maximumCellSize,maximumCellSize)
      
      maskEqGroup.append('line').attr('class', 'pipeline-line')
        .attr('x1',-maximumCellSize).attr('y1',maximumCellSize).attr('x2',maximumCellSize*4.2).attr('y2',maximumCellSize)
        .style('stroke-width', lineStrokeWidth).style('stroke', 'gray');
      maskEqGroup.append('text').attr('class', 'pipeline-text').style('text-anchor','middle')
        .attr('transform',`translate(${maximumCellSize*1.9},${maximumCellSize+25})`)
        .style('font-size', 20).text('Mask Operation');
        

      drawSingleGrid.call(this,maskEqGroup,resGridData, scoreDataRange, 'rowRes',-maximumCellSize * 0.75,-maximumCellSize/1.6)
      drawSingleGrid.call(this,maskEqGroup,maskGridData, {max:1,min:0}, 'rowMask',maximumCellSize ,-maximumCellSize/1.6)
      drawSingleGrid.call(this,maskEqGroup,maskedResGridData, scoreDataRange, 'rowMaskedRes',maximumCellSize*2.75,-maximumCellSize/1.6)

      function drawSingleGrid(group,gridData, dataRange, className,transX,transY){
        let row = group.selectAll(`.${className}`)  // 绘制每一行
            .data(gridData).enter().append('g').attr('class',className)
            .attr('transform',`translate(${transX},${transY})`);
        row
          .selectAll(".square")
            .data(d=>d).enter().append('rect')
            .attr('class','square')
            .attr("x",d=>d.x).attr("y",d=>d.y)
            .attr("width",d=>d.width).attr("height",d=>d.height)
            .attr('opacity',0.9)
            .style('stroke','black')
            .style('stroke-width',1.2)
            .style('fill',d=>{
              let normlizedVal = (d.text-dataRange.min)/(dataRange.max-dataRange.min);
              return colorScale(normlizedVal);
            });
        row
          .selectAll(".text")
          .data(d=>d)
          .enter().append("text")
          .attr("class","text")
          .style("font-size", 10)
          .attr("x", d=>d.x+d.width/2)
          .attr("y", d=>d.y+d.height/2)
          .style("fill", d=>{  // 为颜色设置填充色
            // let normlizedVal = (d.text-this.dataRange.min)/(this.dataRange.max-this.dataRange.min);
            let normlizedVal = (d.text-dataRange.min)/(dataRange.max-dataRange.min);
            if(normlizedVal < 0.2 || normlizedVal > 0.8){
              return 'white';
            } else {
              return 'black';
            }
          })
          .style("text-anchor","middle")
          .style("dominant-baseline","middle")
          .text(d=>{
            if(d.text<-1e5) return '-Inf';
            else return d.text;
          });
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
            .on('mouseover',(event,d)=>{
                if(type!='mask') this.$emit('changeScaleMaskHilights', [d.row,d.col]);
            })
            .style('stroke-width',1.5)
            .style('stroke',d=>{
              if(this.openHighlights){
                if(this.highlights[0]==d.row && this.highlights[1]==d.col) return 'purple';
                else return null;
              }
              return null;
            })
            .style('stroke-width',1.2)
            .style('fill',d=>{
              let normlizedVal = (d.text-dataRange.min)/(dataRange.max-dataRange.min);
              if (normlizedVal<0) normlizedVal = 0;
              else if (normlizedVal>1) normlizedVal = 1;
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