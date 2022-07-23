<template>
<div class="container">
  <svg id="embeddingSvg" height="100%"></svg>
</div>
</template>

<script>
import * as d3 from "d3";
import {getVisualizationSizeConstraint, getDataRange, getGridData} from '../utils/detailview-utils'
import {getLegendGradient} from '../utils/draw-utils'
import {config} from '../utils/config'
export default {
  name:"EmbeddingAnimator",
  props:{
    highlightsIndex: {
      type: Number,
      default: 0,
    },
    curOutputColumnIndex: {
      type: Number,
      default: -1,
    },
    curTokenIndex: {
      type: Number,
      default: 0,
    },
    tokens: {
      type: Array,
      default: function(){return [2,3];},
    },
    embeddings: {
      type: Array,
      default: function(){return [];},
    },
    pe: {
      type: Array,
      default: function(){return [];}
    },
    output: {
      type: Array,
      default: function(){return [];},
    },
  },
  emits:['cleanComponentView','changeHilightsIndex'],
  data(){
    return {
      oldTokenIndex:0,
      oldInput:[],
      vocabSize:32000,
      legalHighlightsIndex:0,
      oldHighlightsIndex:0,
      // highlightsIndex:0,
      // embeddingsDataRange:{},
      // intermediateDataRange:{},
      // activationDataRange:{},
      // outputDataRange:{},
      
      // oldEquationIndex:0,
      // curEquationIndex:[0],

      // oldOutputColumnIndex:0,
      // curOutputColumnIndex:[-1],

      // intermediateColumnGridRow:{},
      // activationColumnGridRow:{},
      // outputGridRow:{},

      // symbolYInter:100,
      // symbolYOutput:100,
      embeddingsDataRange:{},
      outputDataRange:{},
      peDataRange:{},
    };
  },
  beforeUpdate(){
    if(this.oldHighlightsIndex != this.highlightsIndex){
      this.oldHighlightsIndex = this.highlightsIndex;
      this.legalHighlightsIndex = this.highlightsIndex;
    }
    if(this.highlightsIndex >= this.output.length * this.output[0].length){ // this.highlightsIndex 超出范围了
        this.oldHighlightsIndex = 0;
        this.legalHighlightsIndex = 0;
    }
    this.redraw();
  },
  mounted(){
    this.init();
    this.redraw();
  },
  methods:{
    onClean(){
      this.$emit('cleanComponentView');
    },
    init(){
      this.peDataRange = getDataRange(this.pe);
      this.embeddingsDataRange = getDataRange(this.embeddings);
      this.outputDataRange = getDataRange(this.output);
    },
    redrawLines(){
      // 移除之前所绘制的内容
      d3.select(this.$el).selectAll('#embeddingSvg > *').remove();
    },
    redraw(){
      // 初始化一些常量
      this.oldembeddings = this.embeddings;
      this.oldTokenIndex = this.curTokenIndex;

      // 移除之前所绘制的内容
      d3.select(this.$el).selectAll('#embeddingSvg > *').remove();

      // 获取画板
      let svg = d3.select(this.$el).select('#embeddingSvg').attr('width',1550);
      let svgWidth = +(svg.attr('width'));

      // 提前定义一些变量
      const fontSize = 20;
      const textConstraintDivisor = 2;
      let colorScale = d3.interpolateRdBu;
      let linkGen = d3.linkHorizontal().x(d => d.x).y(d => d.y);
      // let paramsColorScale = d3.interpolateBrBG;
      let embeddingsDataRange = this.embeddingsDataRange;
      let peDataRange = this.peDataRange;
      let outputDataRange = this.outputDataRange;
      let totalDataRange = {
        max: Math.max(embeddingsDataRange.max, peDataRange.max, outputDataRange.max),
        min: Math.min(embeddingsDataRange.min, peDataRange.min, outputDataRange.min),
      }

      // 获取颜色映射的scale
      // getLegendGradient = (g, colorScale, gradientName, min, max) => {}
      getLegendGradient(svg,colorScale,'embeddingsAndOutputGradient',totalDataRange.min,totalDataRange.max)
      getLegendGradient(svg,colorScale,'peGradient',peDataRange.min,peDataRange.max)


      // 绘制 tokens
      // 绘制 embeddings 
      let tokensGridGroupX = 0.025*svgWidth;
      let tokensGridGroupY = 50;
      let tokensConstraintGridCellWidth = getVisualizationSizeConstraint(1,'x',400,360,40);
      let tokensConstraintGridCellHeigh = getVisualizationSizeConstraint(this.tokens.length,'y',400,360,40);
      let tokensData = this.tokens.map(d=>[d]);
      let tokensGridData = getGridData(tokensData, tokensConstraintGridCellWidth, tokensConstraintGridCellHeigh);
      let tokensGridGroup = svg.append("g").attr("class","grid").attr("transform",`translate(${tokensGridGroupX},${tokensGridGroupY})`);
      let tokensGridRow = tokensGridGroup.selectAll(".row")  // 绘制每一行
          .data(tokensGridData).enter().append('g').attr('class','row');
      tokensGridRow
        .selectAll(".square")
          .data(d=>d).enter().append('rect')
          .attr('class','square')
          .attr("x",d=>d.x).attr("y",d=>d.y)
          .attr("width",d=>d.width).attr("height",d=>d.height)
          .attr('opacity',0.9)
          .style('stroke',d=>d.row==this.curTokenIndex?'black':null)
          // .style('fill',d=>{
          //   let normlizedVal = (d.text-embeddingsDataRange.min)/(embeddingsDataRange.max-embeddingsDataRange.min);
          //   return colorScale(normlizedVal);
          // });
          .style('fill','#ECE7E7');
      tokensGridRow
        .selectAll('.text').data(d=>d).enter().append('text').attr('class','text')
          .attr("x", d=>d.x+d.width/2).attr("y", d=>d.y+d.height/2)
          .style("text-anchor","middle").style("dominant-baseline","middle")
          .style('font-size',fontSize/(0.75*textConstraintDivisor))
          // .style('fill',d=>{
          //   let normalizedValue = (d.text-equationDataRange.min)/(equationDataRange.max-equationDataRange.min);
          //   if(normalizedValue < 0.2 || normalizedValue > 0.8){
          //     return 'white';
          //   } else {
          //     return 'black';
          //   }
          .style('fill','black')
          .text(d=>d.text);

      let tokensTotalGridWidth = tokensConstraintGridCellWidth;
      // let embeddingsTotalGridHeight = embeddingsConstraintGridCellHeight*this.embeddings.length;
      let tokensGridText = svg.append('text').attr("text-anchor","middle");
      tokensGridText
        .attr('transform',`translate(${ tokensGridGroupX + tokensTotalGridWidth/2 },${tokensGridGroupY/2})`)
        .attr('class','title-text')
        .attr('dy','.3em')
        .style('font-weight','bold')
        .style('font-size',fontSize)
        .text(`Tokens (${this.tokens.length})`);

      // 绘制 embedding matrix
      let embeddingMatrixGridGroupX = tokensGridGroupX + tokensTotalGridWidth + 0.025*svgWidth;
      let embeddingMatrixGridGroupY = tokensGridGroupY;
      let embeddingMatrixConstraintGridCellWidth = 300;
      let embeddingMatrixConstraintGridCellHeight = 360;
      let embeddingMatrixGridData = getGridData([[0]], embeddingMatrixConstraintGridCellWidth, embeddingMatrixConstraintGridCellHeight);
      let embeddingMatrixGridGroup = svg.append("g").attr("class","grid").attr("transform",`translate(${embeddingMatrixGridGroupX},${embeddingMatrixGridGroupY})`);
      let embeddingMatrixGridRow = embeddingMatrixGridGroup.selectAll(".row")  // 绘制每一行
          .data(embeddingMatrixGridData).enter().append('g').attr('class','row');
      embeddingMatrixGridRow
        .selectAll(".square")
          .data(d=>d).enter().append('rect')
          .attr('class','square')
          .attr("x",d=>d.x).attr("y",d=>d.y)
          .attr("width",d=>d.width).attr("height",d=>d.height)
          .attr('opacity',0.9)
          .style('fill','#ECE7E7');
      
      let embeddingMatrixTotalGridWidth = embeddingMatrixConstraintGridCellWidth;
      // let embeddingMatrixTotalGridHeight = embeddingMatrixConstraintGridCellHeight;
      let embeddingMatrixGridText = svg.append('text').attr("text-anchor","middle");
      embeddingMatrixGridText
        // .attr('transform',`translate(${ embeddingMatrixGridGroupX + embeddingMatrixTotalGridWidth/2 },${embeddingMatrixGridGroupY/2})`)
        .attr('transform',`translate(${ embeddingMatrixGridGroupX + embeddingMatrixTotalGridWidth/2 },${0})`)
        .attr('class','title-text')
        // .attr('dy','.3em')
        .style('text-anchor','middle')
        .style('font-weight','bold')
        .style('font-size',fontSize/1.5)
        .selectAll('.tspan')
        .data([`Embedding Matrix`, `(${this.vocabSize},${this.output[0].length})`])
        .enter().append('tspan')
        .attr('x',0)
        .attr('dy','1.5em')
        .text(d=>d);
        
        // 配置一些参数
        let xSize = 325;
        let ySize = 280;

        // 绘制 embeddings
        let embeddingsGridGroupX = embeddingMatrixGridGroupX + embeddingMatrixTotalGridWidth + 0.025*svgWidth;
        let embeddingsGridGroupY = embeddingMatrixGridGroupY;
        let embeddingsConstraintGridCellWidth = getVisualizationSizeConstraint(this.embeddings[0].length,'x',xSize,ySize,40);
        let embeddingsConstraintGridCellHeight = getVisualizationSizeConstraint(this.embeddings.length,'y',xSize,ySize,40);
        let embeddingsGridData = getGridData(this.embeddings, embeddingsConstraintGridCellWidth, embeddingsConstraintGridCellHeight);
        let embeddingsGridGroup = svg.append("g").attr("class","grid").attr("transform",`translate(${embeddingsGridGroupX},${embeddingsGridGroupY})`);
        let embeddingsGridRow = embeddingsGridGroup.selectAll(".row")  // 绘制每一行
            .data(embeddingsGridData).enter().append('g').attr('class','row');
        embeddingsGridRow.selectAll(".square")
            .data(d=>d).enter().append('rect')
            .attr('class','square')
            .attr("x",d=>d.x).attr("y",d=>d.y)
            .attr("width",d=>d.width).attr("height",d=>d.height)
            .attr('opacity',0.9)
            .style('stroke',d=>d.row*embeddingsGridData[0].length+d.col==this.legalHighlightsIndex?'black':null)
            .on('mouseover',(event,d)=>{
              this.$emit('changeHilightsIndex', d.row*embeddingsGridData[0].length+d.col)// this.$emit('changeEquationIndex',newEquationIndex)
            })
            .style('fill',d=>{
              let normlizedVal = (d.text-totalDataRange.min)/(totalDataRange.max-totalDataRange.min);
              return colorScale(normlizedVal);
            });
        let embeddingsTotalGridWidth = embeddingsConstraintGridCellWidth*this.embeddings[0].length;
        let embeddingsTotalGridHeight = embeddingsConstraintGridCellHeight*this.embeddings.length;
        let embeddingsGridText = svg.append('text').attr("text-anchor","middle");
        embeddingsGridText
          .attr('transform',`translate(${ embeddingsGridGroupX + embeddingsTotalGridWidth/2 },${embeddingsGridGroupY/2})`)
          .attr('class','title-text')
          .attr('dy','.3em')
          .style('font-weight','bold')
          .style('font-size',fontSize)
          .text(`embeddings (${this.embeddings.length},${this.embeddings[0].length})`);
      
      // 绘制 pe
      let peGridGroupX = embeddingsGridGroupX + embeddingsTotalGridWidth + 0.025*svgWidth;
      let peGridGroupY = embeddingsGridGroupY;
      let peConstraintGridCellWidth = getVisualizationSizeConstraint(this.pe[0].length,'x',xSize,ySize,40);
      let peConstraintGridCellHeight = getVisualizationSizeConstraint(this.pe.length,'y',xSize,ySize,40);
      let peGridData = getGridData(this.pe, peConstraintGridCellWidth, peConstraintGridCellHeight);
      let peGridGroup = svg.append("g").attr("class","grid").attr("transform",`translate(${peGridGroupX},${peGridGroupY})`);
      let peGridRow = peGridGroup.selectAll(".row")  // 绘制每一行
          .data(peGridData).enter().append('g').attr('class','row');
      peGridRow.selectAll(".square")
          .data(d=>d).enter().append('rect')
          .attr('class','square')
          .attr("x",d=>d.x).attr("y",d=>d.y)
          .attr("width",d=>d.width).attr("height",d=>d.height)
          .attr('opacity',0.9)
          .style('stroke',d=>d.row*peGridData[0].length+d.col==this.legalHighlightsIndex?'black':null)
          .on('mouseover',(event,d)=>{
            this.$emit('changeHilightsIndex', d.row*peGridData[0].length+d.col)// this.$emit('changeEquationIndex',newEquationIndex)
          })
          .style('fill',d=>{
            let normlizedVal = (d.text-peDataRange.min)/(peDataRange.max-peDataRange.min);
            return colorScale(normlizedVal);
          });
      let peTotalGridWidth = peConstraintGridCellWidth*this.pe[0].length;
      let peTotalGridHeight = peConstraintGridCellHeight*this.pe.length;
      let peGridText = svg.append('text').attr("text-anchor","middle");
      peGridText
        .attr('transform',`translate(${ peGridGroupX + peTotalGridWidth/2 },${peGridGroupY/2})`)
        .attr('class','title-text')
        .attr('dy','.3em')
        .style('text-anchor','middle')
        .style('font-weight','bold')
        .style('font-size',fontSize)
        .text(`Positional Encoding (${this.pe.length},${this.pe[0].length})`);

      // 绘制 output 
      let outputGridGroupX = peGridGroupX + peTotalGridWidth + 0.03*svgWidth;
      let outputGridGroupY = peGridGroupY;
      let outputConstraintGridCellWidth = getVisualizationSizeConstraint(this.output[0].length,'x',xSize,ySize,40);
      let outputConstraintGridCellHeight = getVisualizationSizeConstraint(this.output.length,'y',xSize,ySize,40);
      let outputGridData = getGridData(this.output, outputConstraintGridCellWidth, outputConstraintGridCellHeight);
      let outputGridGroup = svg.append("g").attr("class","grid").attr("transform",`translate(${outputGridGroupX},${outputGridGroupY})`);
      let outputGridRow = outputGridGroup.selectAll(".row")  // 绘制每一行
        .data(outputGridData).enter().append('g').attr('class','row');
      outputGridRow.selectAll(".square")
        .data(d=>d).enter().append('rect')
          .attr('class','square')
          .attr("x",d=>d.x).attr("y",d=>d.y)
          .attr("width",d=>d.width).attr("height",d=>d.height)
          .attr('opacity',0.9)
          .style('stroke',d=>d.row*outputGridData[0].length+d.col==this.legalHighlightsIndex?'black':null)
          .on('mouseover',(event,d)=>{
            this.$emit('changeHilightsIndex', d.row*outputGridData[0].length+d.col)// this.$emit('changeEquationIndex',newEquationIndex)
          })
          .style('fill',d=>{
            let normlizedVal = (d.text-totalDataRange.min)/(totalDataRange.max-totalDataRange.min);
            return colorScale(normlizedVal);
          });
      let outputTotalGridWidth = outputConstraintGridCellWidth*this.output[0].length;
      let outputTotalGridHeight = outputConstraintGridCellHeight*this.output.length;
      let outputGridText = svg.append('text').attr("text-anchor","middle");
      outputGridText
        .attr('transform',`translate(${ outputGridGroupX + outputTotalGridWidth/2 },${outputGridGroupY/2})`)
        .attr('class','title-text')
        .attr('dy','.3em')
        .style('text-anchor','middle')
        .style('font-weight','bold')
        .style('font-size',fontSize)
        .text(`Output (${this.output.length},${this.output[0].length})`);

      // 绘制 embedding single grid
      let gridLength = 40;
      let legendHeight = 5;
      let embeddingsSingleGridGroupX = embeddingsGridGroupX + embeddingsTotalGridWidth/2;
      let embeddingsSingleGridGroupY = embeddingsGridGroupY + embeddingsTotalGridHeight + 15;
      let embeddingsSingleConstraintGridCellWidth = getVisualizationSizeConstraint(1,'x',400,315,gridLength);
      let embeddingsSingleConstraintGridCellHeight = getVisualizationSizeConstraint(1,'y',400,315,gridLength);
      let embeddingsSingleGridData = getGridData([[this.embeddings[Math.floor(this.legalHighlightsIndex/this.embeddings[0].length)][this.legalHighlightsIndex%this.embeddings[0].length]]]
                                , embeddingsSingleConstraintGridCellWidth, embeddingsSingleConstraintGridCellHeight);
      let embeddingsSingleGridGroup = svg.append("g").attr("class","grid").attr("transform",`translate(${embeddingsSingleGridGroupX},${embeddingsSingleGridGroupY})`);
      let embeddingsSingleGridRow = embeddingsSingleGridGroup.selectAll(".row")  // 绘制每一行
        .data(embeddingsSingleGridData).enter().append('g').attr('class','row');
      embeddingsSingleGridRow
        .selectAll(".square")
        .data(d=>d).enter().append('rect')
          .attr('class','square')
          .attr("x",d=>d.x).attr("y",d=>d.y)
          .attr("width",d=>d.width).attr("height",d=>d.height)
          .attr('opacity',0.9)
          .style('stroke','black')
          .style('fill',d=>{
            let normlizedVal = (d.text-totalDataRange.min)/(totalDataRange.max-totalDataRange.min);
            return colorScale(normlizedVal);
          });
      embeddingsSingleGridRow
          .selectAll('.text').data(d=>d).enter().append('text').attr('class','text')
          .attr("x", d=>d.x+d.width/2).attr("y", d=>d.y+d.height/2)
          .style("text-anchor","middle").style("dominant-baseline","middle")
          .style('font-size',fontSize/textConstraintDivisor)
          .style('fill',d=>{
            let normalizedValue = (d.text-totalDataRange.min)/(totalDataRange.max-totalDataRange.min);
            if(normalizedValue < 0.2 || normalizedValue > 0.8){
              return 'white';
            } else {
              return 'black';
            }
          }).text(d=>d.text);
      let embedLegendScale = d3.scaleLinear()
      .range([0, 4 * gridLength])
      .domain([totalDataRange.min, totalDataRange.max]);
      let embedLegendAxis = d3.axisBottom()
      .scale(embedLegendScale)
      .tickFormat(d3.format('.2f'))
      .tickValues([totalDataRange.min, totalDataRange.min+(totalDataRange.max-totalDataRange.min)/2, totalDataRange.max]);
      let embedLegend = embeddingsSingleGridGroup.append('g')
        .attr('transform', `translate(${0}, ${1.25*gridLength})`);
      embedLegend.append('g')
        .attr('transform', `translate(${-2*gridLength}, ${legendHeight+2})`)
        .call(embedLegendAxis)
      embedLegend.append('rect')
        // .attr('x',-2*gridLength).attr('y',1.25*gridLength)
        .attr('transform', `translate(${-2*gridLength}, ${0})`)
        .attr('width', 4 * gridLength).attr('height', legendHeight)
        .style('fill', 'url(#embeddingsAndOutputGradient)');

      // 绘制 pe single grid
      let peSingleGridGroupX = peGridGroupX + peTotalGridWidth/2;
      let peSingleGridGroupY = peGridGroupY + peTotalGridHeight + 15;
      let peSingleConstraintGridCellWidth = getVisualizationSizeConstraint(1,'x',400,315,gridLength);
      let peSingleConstraintGridCellHeight = getVisualizationSizeConstraint(1,'y',400,315,gridLength);
      let peSingleGridData = getGridData([[this.pe[Math.floor(this.legalHighlightsIndex/this.pe[0].length)][this.legalHighlightsIndex%this.pe[0].length]]]
                                , peSingleConstraintGridCellWidth, peSingleConstraintGridCellHeight);
      let peSingleGridGroup = svg.append("g").attr("class","grid").attr("transform",`translate(${peSingleGridGroupX},${peSingleGridGroupY})`);
      let peSingleGridRow = peSingleGridGroup.selectAll(".row")  // 绘制每一行
        .data(peSingleGridData).enter().append('g').attr('class','row');
      peSingleGridRow
        .selectAll(".square")
        .data(d=>d).enter().append('rect')
          .attr('class','square')
          .attr("x",d=>d.x).attr("y",d=>d.y)
          .attr("width",d=>d.width).attr("height",d=>d.height)
          .attr('opacity',0.9)
          .style('stroke','black')
          .style('fill',d=>{
            let normlizedVal = (d.text-peDataRange.min)/(peDataRange.max-peDataRange.min);
            return colorScale(normlizedVal);
          });
      peSingleGridRow
          .selectAll('.text').data(d=>d).enter().append('text').attr('class','text')
          .attr("x", d=>d.x+d.width/2).attr("y", d=>d.y+d.height/2)
          .style("text-anchor","middle").style("dominant-baseline","middle")
          .style('font-size',fontSize/textConstraintDivisor)
          .style('fill',d=>{
            let normalizedValue = (d.text-peDataRange.min)/(peDataRange.max-peDataRange.min);
            if(normalizedValue < 0.2 || normalizedValue > 0.8){
              return 'white';
            } else {
              return 'black';
            }
          }).text(d=>d.text);
      let peLegendScale = d3.scaleLinear()
      .range([0, 4 * gridLength])
      .domain([peDataRange.min, peDataRange.max]);
      let peLegendAxis = d3.axisBottom()
      .scale(peLegendScale)
      .tickFormat(d3.format('.2f'))
      .tickValues([peDataRange.min, peDataRange.min+(peDataRange.max-peDataRange.min)/2, peDataRange.max]);
      let peLegend = peSingleGridGroup.append('g')
        .attr('transform', `translate(${0}, ${1.25*gridLength})`);
      peLegend.append('g')
        .attr('transform', `translate(${-2*gridLength}, ${legendHeight+2})`)
        .call(peLegendAxis)
      peLegend.append('rect')
        // .attr('x',-2*gridLength).attr('y',1.25*gridLength)
        .attr('transform', `translate(${-2*gridLength}, ${0})`)
        .attr('width', 4 * gridLength).attr('height', legendHeight)
        .style('fill', 'url(#peGradient)');
      

      // 绘制 output single grid
      let outputSingleGridGroupX = outputGridGroupX + outputTotalGridWidth/2;
      let outputSingleGridGroupY = outputGridGroupY + outputTotalGridHeight + 15;
      let outputSingleConstraintGridCellWidth = getVisualizationSizeConstraint(1,'x',400,315,gridLength);
      let outputSingleConstraintGridCellHeight = getVisualizationSizeConstraint(1,'y',400,315,gridLength);
      let outputSingleGridData = getGridData([[this.output[Math.floor(this.legalHighlightsIndex/this.output[0].length)][this.legalHighlightsIndex%this.output[0].length]]]
                                , outputSingleConstraintGridCellWidth, outputSingleConstraintGridCellHeight);
      let outputSingleGridGroup = svg.append("g").attr("class","grid").attr("transform",`translate(${outputSingleGridGroupX},${outputSingleGridGroupY})`);
      let outputSingleGridRow = outputSingleGridGroup.selectAll(".row")  // 绘制每一行
        .data(outputSingleGridData).enter().append('g').attr('class','row');
      outputSingleGridRow
        .selectAll(".square")
        .data(d=>d).enter().append('rect')
          .attr('class','square')
          .attr("x",d=>d.x).attr("y",d=>d.y)
          .attr("width",d=>d.width).attr("height",d=>d.height)
          .attr('opacity',0.9)
          .style('stroke','black')
          .style('fill',d=>{
            let normlizedVal = (d.text-totalDataRange.min)/(totalDataRange.max-totalDataRange.min);
            return colorScale(normlizedVal);
          });
      outputSingleGridRow
          .selectAll('.text').data(d=>d).enter().append('text').attr('class','text')
          .attr("x", d=>d.x+d.width/2).attr("y", d=>d.y+d.height/2)
          .style("text-anchor","middle").style("dominant-baseline","middle")
          .style('font-size',fontSize/textConstraintDivisor)
          .style('fill',d=>{
            let normalizedValue = (d.text-totalDataRange.min)/(totalDataRange.max-totalDataRange.min);
            if(normalizedValue < 0.2 || normalizedValue > 0.8){
              return 'white';
            } else {
              return 'black';
            }
          }).text(d=>d.text);
      let outputLegend = outputSingleGridGroup.append('g')
        .attr('transform', `translate(${0}, ${1.25*gridLength})`);
      outputLegend.append('g')
        .attr('transform', `translate(${-2*gridLength}, ${legendHeight+2})`)
        .call(embedLegendAxis)
      outputLegend.append('rect')
        // .attr('x',-2*gridLength).attr('y',1.25*gridLength)
        .attr('transform', `translate(${-2*gridLength}, ${0})`)
        .attr('width', 4 * gridLength).attr('height', legendHeight)
        .style('fill', 'url(#embeddingsAndOutputGradient)');
    

      // 绘制 ‘+’
      let plusX = embeddingsGridGroupX + embeddingsTotalGridWidth + 0.0125*svgWidth;
      let plusY = embeddingsGridGroupY + embeddingsTotalGridHeight/2;
      let plusGroup = svg.append('g').attr('class','equation').attr('transform',`translate(${plusX},${plusY})`)  
      plusGroup.append('text').attr('class','equation-text')
        .style('text-anchor','middle').style('font-weight','bold').style('font-size',fontSize*1.5)
        .text('+');  
      // plusGroup.append('text').attr('class','equation-text').attr('transform',`translate(${0},${embeddingsTotalGridHeight/2 + 15 + gridLength/2})`)
      //   .style('text-anchor','middle').style('font-weight','bold').style('font-size',fontSize*1.5)
      //   .text('+');  
      
      // 绘制 ‘=’
      let equalX = peGridGroupX + peTotalGridWidth + 0.015*svgWidth;
      let equalY = peGridGroupY + peTotalGridHeight/2;
      let equalGroup = svg.append('g').attr('class','equation').attr('transform',`translate(${equalX},${equalY})`)  
      equalGroup.append('text').attr('class','equation-text')
        .style('text-anchor','middle').style('font-weight','bold').style('font-size',fontSize*1.5)
        .text('=');  
      

      // 绘制 Positional Encoding 的说明性文字
      // let peDescriptionX = peGridGroupX;
      // this.output[Math.floor(this.legalHighlightsIndex/this.output[0].length)][this.legalHighlightsIndex%this.output[0].length]
      let rCord = Math.floor(this.legalHighlightsIndex/this.pe[0].length);
      let cCord = this.legalHighlightsIndex%this.pe[0].length;
      let peSingleDataText = cCord%2==0?`sin( [ ${rCord} ]/(10000^( [ ${cCord} ] / ${this.pe[0].length} ) ) = `:`cos( [ ${rCord} ]/(10000^( [ ${cCord-1} ] / ${this.pe[0].length} ) ) = `;
      // if(cCord%2==0){}
      peSingleGridGroup.append('text').attr('class','equation-text').attr('transform',`translate(${-gridLength*0.18},${gridLength*0.7})`)  
        .style('text-anchor','end').style('font-weight','bold').style('font-size',fontSize/1.2)
        .text(peSingleDataText);


      const edgeStrokeWidth = config.edgeStrokeWidth;
      const edgeOpacity = config.edgeOpacity; 
      let linkData = [{
        source:{
          x: tokensGridGroupX + tokensGridData[this.curTokenIndex][0].x + tokensGridData[this.curTokenIndex][0].width,
          y: tokensGridGroupY + tokensGridData[this.curTokenIndex][0].y + tokensGridData[this.curTokenIndex][0].height/2,
        },
        target:{
          x: embeddingMatrixGridGroupX + embeddingMatrixGridData[0][0].x,
          y: embeddingMatrixGridGroupY + embeddingMatrixGridData[0][0].y + (this.tokens[this.curTokenIndex]/this.vocabSize)*embeddingMatrixGridData[0][0].height,
        },
        id:'token-matrix-link'
      },{
        target:{
          x: embeddingMatrixGridGroupX + embeddingMatrixGridData[0][0].x + embeddingMatrixGridData[0][0].width,
          y: embeddingMatrixGridGroupY + embeddingMatrixGridData[0][0].y + (this.tokens[this.curTokenIndex]/this.vocabSize)*embeddingMatrixGridData[0][0].height,
        },
        source:{
          x: embeddingMatrixGridGroupX + embeddingMatrixGridData[0][0].x,
          y: embeddingMatrixGridGroupY + embeddingMatrixGridData[0][0].y + (this.tokens[this.curTokenIndex]/this.vocabSize)*embeddingMatrixGridData[0][0].height,
        },
      },{
        source:{
          x: embeddingMatrixGridGroupX + embeddingMatrixGridData[0][0].x + embeddingMatrixGridData[0][0].width,
          y: embeddingMatrixGridGroupY + embeddingMatrixGridData[0][0].y + (this.tokens[this.curTokenIndex]/this.vocabSize)*embeddingMatrixGridData[0][0].height,
        },
        target:{
          x: embeddingsGridGroupX + embeddingsGridData[this.curTokenIndex][0].x, 
          y: embeddingsGridGroupY + embeddingsGridData[this.curTokenIndex][0].y + embeddingsGridData[this.curTokenIndex][0].height/2,
        },
        id:'matrix-embeddings-link'
      },]
      let edgeGroup = svg.append("g").attr("class","edge-group");
      edgeGroup.selectAll("path.edge").data(linkData).enter().append('path')
        .attr('id',d=>d.id!=undefined?d.id:null).attr('class','edge')
        .attr('d',d=>linkGen({source:d.source, target:d.target}))
        .style('fill','none').style('stroke-width',edgeStrokeWidth).style('opacity',edgeOpacity)
        .style('stroke','black');

      // 绘制 说明性文字
      svg.append('text').attr('x',20).attr('y',10)
        .style('fill','steelblue').style('font-size',fontSize/1.5).style('font-weight','bold')
        .append('textPath').attr('xlink:href','#token-matrix-link')
        .text(`extract`);
      svg.append('text').attr('x',20).attr('y',10)
        .style('fill','steelblue').style('font-size',fontSize/1.5).style('font-weight','bold')
        .append('textPath').attr('xlink:href','#matrix-embeddings-link')
        .text(`* sqrt(${this.embeddings[0].length})`);
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