<template>
    <div id="architectureDiv" style="height: 100%; width: 100%">
    </div>
</template>

<script>
  /*
  This component demonstrates one way to construct d3 visualization.
  d3 example source: https://observablehq.com/@d3/sortable-bar-chart
   */
  import * as d3 from "d3";
  import * as dagreD3 from "dagre-d3"

  // https://www.pianshen.com/article/20641621990/
  // Dagre-D3最大的优点就是可以实现自动布局，你只需要put数据就可以了，
  // 但是缺点就是自动布局后的连线会比较乱，而且连线不是横平竖直的，
  // 对于流程图不复杂的还好，稍微复杂点画出来的连线就没法看。最后还是被pass了。

  export default {
    name: "cpnArchitecture",
    props: {
      // loadData: Object,
    },
    // emits: ['selected'], // 子组件发射事件, 父组件接收事件并完成相应数据交互
    emits: [], // 子组件发射事件, 父组件接收事件并完成相应数据交互
    data() {
      return {
        // svg: null,
        architecture: null,
        // edges: [],
        graph: null,
        render: null,
        // focus = 0,1,2,3,4 ;
        // 0 表示没有放大, 1-2表示放大encoder, 3-4表示放大decoder
        focus: 0,
      }
    },
    watch: {
      // loadData: function () {
      //   // When data is changed in parent, render this component
      //   this.renderBarChart();
      // },
    },
    mounted() {
      // this.initTest();
      // this.initDemo();
      // this.initArchitecture();
      this.initArc2();
    },
    methods: {
      initTest() {
        // 设置画布大小 - 四周留间距
        console.log("initialize architecture...");
        let architectureVieWidth = 1600 ,architectureViewHeight = 700; 
        let margin = {top: 10, right: 30, bottom: 30, left: 40},
          width = architectureVieWidth - margin.right - margin.left,
          height = architectureViewHeight - margin.top - margin.bottom;

        // 创建 SVG 元素并添加到 对应的 html 元素中
        let svg = d3.select("#architectureDiv")
        .append("svg")
        .attr("width", width + margin.right + margin.left )
        .attr("height", height + margin.top + margin.bottom);

        // 创建 dagre 的 graph 对象
        let g = new dagreD3.graphlib.Graph()
        .setGraph({})
        .setDefaultEdgeLabel(function(){
          return {};
        });

        // 声明 nodes 与 links
        let infos = {
          nodeInfos:[
            {
              id: "node1",
              label: "节点1"
            },
            {
              id: "node2",
              label: "节点2"
            },
            {
              id: "node3",
              label: "节点3"
            },
            {
              id: "node4",
              label: "节点4"
            },
          ],
          edges: [
            {
              source: "node1",
              target: "node2"
            },
            {
              source: "node2",
              target: "node3"
            },
            {
              source: "node2",
              target: "node4"
            },
          ]
        }

        // 向图中添加节点
        infos.nodeInfos.forEach(d=>{
          g.setNode(d.id, { // 第一个参数, 节点的 id, 第二个参数, 节点的相关属性对象
            id: d.id,
            label: d.label,
            class: "type-1",
            style: "stroke: #0fb2cc; fill: #ffffff;"
          });
        });

        infos.edges.forEach(d=>{
          g.setEdge(d.source,d.target,{
            style: "stroke: #0fb2cc; fill:none;",
            arrowheadStyle: "fill: #0fb2cc; stroke: #0fb2cc;",
            arrowhead: "vee"
          });
        });

        g.nodes().forEach(v=>{
          let node = g.node(v);
          node.rx = node.ry = 5;
        })

        // 渲染
        let render = new dagreD3.render();

        svg.select("g").remove(); // 删除以前的节点
        let svgGroup = svg.append("g");

        render(d3.select("svg g"), g);

        let xCenterOffset = (svg.attr("width") - g.graph().width) / 2;
        svgGroup.attr("transform", "translate(" + xCenterOffset + ", 20)");
        svg.attr("height", g.graph().height + 40);
      },

      initDemo(){
        // 设置画布大小 - 四周留间距
        console.log("initialize architecture...");
        let architectureVieWidth = 1600 ,architectureViewHeight = 700; 
        let margin = {top: 10, right: 30, bottom: 30, left: 40},
          width = architectureVieWidth - margin.right - margin.left,
          height = architectureViewHeight - margin.top - margin.bottom;

        // 创建 SVG 元素并添加到 对应的 html 元素中
        let svg = d3.select("#architectureDiv")
        .append("svg")
        .attr("width", width + margin.right + margin.left )
        .attr("height", height + margin.top + margin.bottom);

        let g = new dagreD3.graphlib.Graph({compound:true})
        .setGraph({rankdir:'LR'})
        .setDefaultEdgeLabel(function(){ return {}; })

        g.setNode('a',{ // 第一个参数, 节点的 id, 第二个参数, 节点的相关属性对象
          label: 'A'
        })
        g.setNode('a',{ // 第一个参数, 节点的 id, 第二个参数, 节点的相关属性对象
          label: 'A'
        })
        g.setNode('b',{ // 第一个参数, 节点的 id, 第二个参数, 节点的相关属性对象
          label: 'B'
        })
        g.setNode('c',{ // 第一个参数, 节点的 id, 第二个参数, 节点的相关属性对象
          label: 'C'
        })
        g.setNode('d',{ // 第一个参数, 节点的 id, 第二个参数, 节点的相关属性对象
          label: 'D'
        })
        g.setNode('e',{ // 第一个参数, 节点的 id, 第二个参数, 节点的相关属性对象
          label: 'E'
        })
        g.setNode('f',{ // 第一个参数, 节点的 id, 第二个参数, 节点的相关属性对象
          label: 'F'
        })
        g.setNode('g',{ // 第一个参数, 节点的 id, 第二个参数, 节点的相关属性对象
          label: 'G'
        })
        g.setNode('group', {
          label: 'Group', 
          clusterLabelPos: 'top', // 这个只用来说明 label 相对于这个 node 的位置
          style:'fill: #d3d7e8'
        })
        g.setNode('top_group', {
          label: 'Top Group', 
          clusterLabelPos: 'bottom', 
          style:'fill: #ffd47f'
        })
        g.setNode('bottom_group', {
          label: 'Bottom Group', 
          // clusterLabelPos: 'top', // clusterLabelPos 没有指明就默认中间位置
          clusterLabelPos: 'bottom',
          style:'fill: #5f9488'
        })
        // Set the parents to define which nodes belong to which cluster
        g.setParent('top_group', 'group');  // node 1 belongs to node 2
        g.setParent('bottom_group', 'group');
        g.setParent('b', 'top_group');
        g.setParent('c', 'bottom_group');
        g.setParent('d', 'bottom_group');
        g.setParent('e', 'bottom_group');
        g.setParent('f', 'bottom_group');

        g.setEdge('a', 'b');
        g.setEdge('b', 'c');
        g.setEdge('b', 'd');
        g.setEdge('b', 'e');
        g.setEdge('b', 'f');
        g.setEdge('b', 'g');

        // Create the renderer
        var render = new dagreD3.render();

        // Set up an SVG group so that we can translate the final graph.
        let svgGroup = svg.append("g");

        // Run the renderer. This is what draws the final graph.
        render(d3.select("svg g"), g);

        // Center the graph
        let xCenterOffset = (svg.attr("width") - g.graph().width) / 2;
        svgGroup.attr("transform", "translate(" + xCenterOffset + ", 20)");
        svg.attr("height", g.graph().height + 40);
      },

      initArchitecture(){
        // 设置画布大小 - 四周留间距
        console.log("initialize architecture...");
        let architectureVieWidth = 1600 ,architectureViewHeight = 700; 
        let margin = {top: 10, right: 30, bottom: 30, left: 40},
          width = architectureVieWidth - margin.right - margin.left,
          height = architectureViewHeight - margin.top - margin.bottom;

        // 创建 SVG 元素并添加到 对应的 html 元素中
        let svg = d3.select("#architectureDiv")
        .append("svg")
        .attr("width", width + margin.right + margin.left )
        .attr("height", height + margin.top + margin.bottom);
        svg;

        // 创建 small-transoformer 所需要的所有结点
        this.architecture = {
          encoder: [
            this.createInputNode(true),
            this.createTokenizeNode(true),
            this.createEmbeddingNode(true),
            this.createPositionalEncodingNode(true),
          ],
          decoder: [
            this.createInputNode(false),
            this.createTokenizeNode(false),
            this.createEmbeddingNode(false),
            this.createPositionalEncodingNode(false),
          ],
          generator: [
            this.createLinearNode(),
            this.createSoftmaxNode(),
          ]
        }
        this.createEncoderLayer(1).forEach(node=>{
          this.architecture.encoder.push(node);
        });
        this.createEncoderLayer(2).forEach(node=>{
          this.architecture.encoder.push(node);
        });
        this.createDecoderLayer(1).forEach(node=>{
          this.architecture.decoder.push(node);
        });
        this.createDecoderLayer(2).forEach(node=>{
          this.architecture.decoder.push(node);
        });

        // 创建流程图
        let g = new dagreD3.graphlib.Graph({
          directed: true,
          compound: true,
          multigraph: false})
        .setGraph({
          ranker: "network-simplex",
          rankdir:'LR' ,// 将流程图的排列方式设置为水平排列
          aligh: "DR",
          nodesep: 10,
          edgesep: 10,
          ranksep: 20
        }) // 将流程图的排列方式设置为水平排列
        .setDefaultEdgeLabel(function(){ return {}; });
        this.graph = g;

        // 向流程图中加入 Node 和 Edge
        // 加入输入文本结点
        this.addNodesIntoGraph();

        // 向流程图中加入 Edge
        this.addEdgesIntoGraph();

        // 为各个结点分组
        this.addClustesIntoGraph();

        // console.log(this.graph.node("encoder-input").rank);
        // console.log(this.graph.node("decoder-input").rank);
        // this.graph.setNode("root",{
        //   id: "root",
        //   label: "Root",
        //   class: "root"
        // })
        // this.graph.setEdge("root","encoder-input");
        // this.graph.setEdge("root","decoder-input");
        // this.graph.setParent("encoder-input","root");
        // this.graph.setParent("decoder-input","root");

        // Create the renderer
        let render = new dagreD3.render();

        // Set up an SVG group so that we can translate the final graph.
        let svgGroup = svg.append("g");

        // Run the renderer. This is what draws the final graph.
        render(d3.select("svg g"), g);

        // Center the graph
        let xCenterOffset = (svg.attr("width") - g.graph().width) / 2;
        svgGroup.attr("transform", "translate(" + xCenterOffset + ", 20)");
        svg.attr("height", g.graph().height + 40);
      },

      initArc2(){
         // 设置画布大小 - 四周留间距
        console.log("initialize architecture...");
        let architectureVieWidth = 1600 ,architectureViewHeight = 700; 
        let margin = {top: 10, right: 30, bottom: 30, left: 40},
          width = architectureVieWidth - margin.right - margin.left,
          height = architectureViewHeight - margin.top - margin.bottom;

        // 创建 SVG 元素并添加到 对应的 html 元素中
        let svg = d3.select("#architectureDiv")
        .append("svg")
        .attr("width", width + margin.right + margin.left )
        .attr("height", height + margin.top + margin.bottom);
        svg;

        // 创建 small-transoformer 所需要的所有结点的信息
        this.architecture = {
          encoder: [
            this.createInputNode(true),
            this.createTokenizeNode(true),
            this.createEmbeddingNode(true),
            this.createPositionalEncodingNode(true),
            this.createEncoderLayer(1), // 一个数组
            this.createEncoderLayer(2), // 一个数组
          ],
          decoder: [
            this.createInputNode(false),
            this.createTokenizeNode(false),
            this.createEmbeddingNode(false),
            this.createPositionalEncodingNode(false),
            this.createDecoderLayer(1),
            this.createDecoderLayer(2),
          ],
          generator: [
            this.createLinearNode(),
            this.createSoftmaxNode(),
          ]
        }

        // 创建流程图
        let g = new dagreD3.graphlib.Graph({
          directed: true,
          compound: true,
          multigraph: false})
        .setGraph({
          ranker: "network-simplex",
          rankdir:'LR' ,// 将流程图的排列方式设置为水平排列
          aligh: "UL",
          // nodesep: 10,
          // edgesep: 10,
          // ranksep: 20
        }) // 将流程图的排列方式设置为水平排列
        .setDefaultEdgeLabel(function(){ return {}; });
        this.graph = g;

        // 创建流程图中所需要的结点
        this.createGraphNodes();

        // 构建流程图中结点的位置;  — rank constraint

        //  创建流程图中所有需要可能需要的边
        this.createGraphEdges();

        // Create the renderer
        let render = new dagreD3.render();
        this.render = render;

        // Set up an SVG group so that we can translate the final graph.
        let svgGroup = svg.append("g");
        svgGroup;
        // Run the renderer. This is what draws the final graph.
        render(d3.select("svg g"), this.graph);

        // Center the graph
        let xCenterOffset = (svg.attr("width") - g.graph().width) / 2;
        svgGroup.attr("transform", "translate(" + xCenterOffset + ", 30)");
        svg.attr("height", g.graph().height + 40);
        
        // svg.select("#encoder-input").attr("transform",`translate(${10},${10})`);

      },

      createInputNode(isEncoder=true){
        return {
          id: isEncoder == true ? "encoder-input" : "decoder-input",
          // label: isEncoder == true ? "Encoder Embedding" : "Decoder Embedding",
          label: "Input",
          class:"input"
        }
      },

      createTokenizeNode(isEncoder=true){
        return {
          id: isEncoder == true ? "encoder-tokenize" : "decoder-tokenize",
          // label: isEncoder == true ? "Encoder Embedding" : "Decoder Embedding",
          label: "Tokenize",
          class:"tokenize"
        }
      },

      createEmbeddingNode(isEncoder=true){
        return {
          id: isEncoder == true ? "encoder-embedding" : "decoder-embedding",
          // label: isEncoder == true ? "Encoder Embedding" : "Decoder Embedding",
          label: "Embedding",
          class:"embedding"
        }
      },

      createPositionalEncodingNode(isEncoder=true){
        return {
          id: isEncoder == true ? "encoder-PE" : "decoder-PE",
          // label: isEncoder == true ? "Encoder Positional Encoding" : "Decoder Positional Encoding",
          label: "Positional Encoding",
          class: "PE"
        }
      },

      createAttentionNode(layerOrder, isEncoder=true, isSelf=true, isMasked=false){
          let coder = isEncoder ? "encoder-" : "decoder-";
          let mask = isMasked ? "masked-" : "full-", maskLabel = isMasked ? "Masked " : "Full ";
          let mechanism = isSelf ? "self-" : "cross-", mechanismLabel = isSelf ? "Self-" : "Cross-";
          return { 
            id: coder + layerOrder + "-" + mask + mechanism + "attention",
            label: maskLabel + mechanismLabel + "Attention",
            class:"attention",
            layerOrder: layerOrder
          }
        },

      createAddNode(layerOrder, innerOrder, isEncoder=true) {
        let coder = isEncoder ? "encoder-" : "decoder-";
        return {
          id: coder + layerOrder + "-" + innerOrder + "-add",
          label: "Add",
          class: "add",
          layerOrder: layerOrder,
          innerOrder: innerOrder
        }
      },

      createLayerNormNode(layerOrder, innerOrder,isEncoder=true){
        let coder = isEncoder ? "encoder-" : "decoder-";
        return {
          id: coder + layerOrder + "-" + innerOrder + "-LN",
          label: "Layer Norm",
          class: "LN",
          layerOrder: layerOrder,
          innerOrder: innerOrder
        }
      },

      createFeedForwardNode(layerOrder,isEncoder=true){
        let coder = isEncoder ? "encoder-" : "decoder-";
        return {
          id: coder + layerOrder + "-FF",
          label: "Feed Forward",
          class: "FF",
          layerOrder: layerOrder
        }
      },

      createLinearNode(){
        return {
          id: "linear",
          label: "Linear",
          class: "linear"
        }
      },
      
      createSoftmaxNode(){
        return {
          id: "softmax",
          label: "Softmax",
          class: "softmax"
        }
      },

      createEncoderLayer(layerOrder){
        return [
          // this.createAttentionNode(layerOrder=layerOrder, isEncoder=true, isSelf=true, isMasked=false),
          this.createAttentionNode(layerOrder, true, true, false),
          // this.createAddNode(layerOrder=layerOrder, innerOrder=1, isEncoder=true),
          this.createAddNode(layerOrder, 1, true),
          // this.createLayerNormNode(layerOrder=layerOrder, innerOrder=1, isEncoder=true),
          this.createLayerNormNode(layerOrder, 1, true),
          // this.createFeedForwardNode(layerOrder=layerOrder, isEncoder=true),
          this.createFeedForwardNode(layerOrder, true),
          // this.createAddNode(layerOrder=layerOrder, innerOrder=2, isEncoder=true),
          this.createAddNode(layerOrder, 2, true),
          // this.createLayerNormNode(layerOrder=layerOrder, innerOrder=2, isEncoder=true),
          this.createLayerNormNode(layerOrder, 2, true),
        ]
      },

      createDecoderLayer(layerOrder){
        return [
          // this.createAttentionNode(layerOrder=layerOrder, isEncoder=false, isSelf=true, isMasked=true),
          this.createAttentionNode(layerOrder, false, true, true),
          // this.createAddNode(layerOrder=layerOrder, innerOrder=1, isEncoder=false),
          this.createAddNode(layerOrder, 1, false),
          // this.createLayerNormNode(layerOrder=layerOrder, innerOrder=1, isEncoder=false),
          this.createLayerNormNode(layerOrder, 1, false),
          // this.createAttentionNode(layerOrder=layerOrder, isEncoder=false, isSelf=false, isMasked=false),
          this.createAttentionNode(layerOrder, false, false, false),
          // this.createAddNode(layerOrder=layerOrder, innerOrder=2, isEncoder=false),
          this.createAddNode(layerOrder, 2, false),
          // this.createLayerNormNode(layerOrder=layerOrder, innerOrder=2, isEncoder=false),
          this.createLayerNormNode(layerOrder, 2, false),
          // this.createFeedForwardNode(layerOrder=layerOrder, isEncoder=false),
          this.createFeedForwardNode(layerOrder, false),
          // this.createAddNode(layerOrder=layerOrder, innerOrder=3, isEncoder=false),
          this.createAddNode(layerOrder, 3, false),
          // this.createLayerNormNode(layerOrder=layerOrder, innerOrder=3, isEncoder=false),
          this.createLayerNormNode(layerOrder, 3, false),
        ]
      },
      
      createGraphNodes(){
        // focus == 0
        let counter = 0; 
        let rank = 0;
        this.architecture.encoder.forEach(item => {
          rank += 1;
          if (item instanceof Array){
            counter += 1;
            let props = {
              id: "encoder-block-" + counter,
              label: "Encoder Block",
              class: "transformer-block",
              rank: rank
            }
            this.graph.setNode(props.id,props);
          }else{
            item.rank = rank;
            this.graph.setNode(item.id,item);
          }
        });
        counter = 0;
        rank = 0
        this.architecture.decoder.forEach(item => {
          rank += 1;
          if (item instanceof Array){
            counter = counter + 1;
            let props = {
              id: "decoder-block-" + counter,
              label: "Decoder Block",
              class: "transformer-block",
              rank: rank
            }
            this.graph.setNode(props.id,props);
          }else{
            item.rank = rank;
            this.graph.setNode(item.id,item);
          }
        });
        this.architecture.generator.forEach(item => {
          rank += 1;
          item.rank = rank;
          this.graph.setNode(item.id, item);
        });
      },

      createGraphEdges(){
        // focus == 0
        let counter = 0;
        let id_source = "encoder-input";
        this.architecture.encoder.forEach(item => {
          if (item instanceof Array){
            counter += 1;
            let id = "encoder-block-" + counter
            this.graph.setEdge(id_source, id);
            id_source = id;
          }else{
            if (item.id != "encoder-input"){
              this.graph.setEdge(id_source, item.id);
              id_source = item.id;
            }
          }
        });
        let id_source_encoder_output = id_source;
        id_source = "decoder-input";
        counter = 0;
        this.architecture.decoder.forEach(item => {
          if (item instanceof Array){
            counter += 1;
            let id = "decoder-block-" + counter
            this.graph.setEdge(id_source, id);
            this.graph.setEdge(id_source_encoder_output, id);
            id_source = id;
          }else{
            if (item.id != "decoder-input"){
              this.graph.setEdge(id_source, item.id);
              id_source = item.id;
            }
          }
        });
        this.architecture.generator.forEach(item => {
          this.graph.setEdge(id_source,item.id);
          id_source = item.id;
        });
      },
      
      changeGraphEdges(focus){ // 根据 focus 来动态地改变视图;
        focus;
      },

      addNodesIntoGraph(){ 
        this.architecture.encoder.forEach(item => {
          // item.width = 15;
          // item.height = 10;
          this.graph.setNode(item.id, item);
        });
        this.architecture.decoder.forEach(item => {
          // item.width = 15;
          // item.height = 10;
          this.graph.setNode(item.id, item);
        });
        this.architecture.generator.forEach(item => {
          // item.width = 15;
          // item.height = 10;
          this.graph.setNode(item.id, item);
        });
      },
      
      addEdgesIntoGraph(){ 
        let id_source = "encoder-input"
        let id_source_residual_connection = null;
        this.architecture.encoder.forEach(item => {
          if (item.id != "encoder-input"){
            this.graph.setEdge(id_source,item.id);
            if(item.class == "PE" || item.class == "LN") {
              id_source_residual_connection = item.id;
            } else if (item.class == "add") {
              this.graph.setEdge(id_source_residual_connection,item.id);
            }
            id_source = item.id;
          } 
        });
        // id_encoder_output = "encoder-2-2-LN"
        let id_encoder_output = id_source;
        id_source_residual_connection = null;
        id_source = "decoder-input";
        this.architecture.decoder.forEach(item => {
          if (item.id != "decoder-input"){
            this.graph.setEdge(id_source,item.id);
            if (item.id.match("cross") != null) { // cross-attention
              this.graph.setEdge(id_encoder_output,item.id);
            } else if(item.class == "PE" || item.class == "LN") { // beginning of residual connection
              id_source_residual_connection = item.id;
            } else if (item.class == "add") { // end of residual connection
              this.graph.setEdge(id_source_residual_connection,item.id);
            }
            id_source = item.id;
          } 
        });
        // id_source = "decoder-2-3-LN"
        this.architecture.generator.forEach(item => {
          this.graph.setEdge(id_source,item.id);
          id_source = item.id;
        });
      },

      addClustesIntoGraph(){
        console.log("addClustesIntoGraph...");
        this.graph.setNode("encoder-block-1", {
          id: "encoder-block-1",
          label: "Transformer Block",
          class: "transformer-block",
          clusterLabelPos: "top",
          style: 'fill: #ffd47f'
        });
        this.graph.setNode("encoder-block-2", {
          id: "encoder-block-2",
          label: "Transformer Block",
          class: "transformer-block",
          clusterLabelPos: "top",
          style: 'fill: #ffd47f'
        });
        this.graph.setNode("encoder", {
          id: "encoder",
          label: "Encoder",
          clusterLabelPos: "top",
          style: 'fill: #87CEFA'
        });
        this.graph.setParent("encoder-block-1", "encoder");
        this.graph.setParent("encoder-block-2", "encoder");
        this.graph.setNode("decoder-block-1", {
          id: "decoder-block-1",
          label: "Transformer Block",
          class: "transformer-block",
          clusterLabelPos: "top",
          style: 'fill: #ffd47f'
        });
        this.graph.setNode("decoder-block-2", {
          id: "decoder-block-2",
          label: "Transformer Block",
          class: "transformer-block",
          clusterLabelPos: "top",
          style: 'fill: #ffd47f'
        });
        this.graph.setNode("decoder", {
          id: "decoder",
          label: "Decoder",
          clusterLabelPos: "top",
          style: 'fill: #87CEFA'
        });
        this.graph.setParent("decoder-block-1", "decoder");
        this.graph.setParent("decoder-block-2", "decoder");
        this.architecture.encoder.forEach(item => {
          if (item.layerOrder == 1){
            this.graph.setParent(item.id,"encoder-block-1");
          } else if (item.layerOrder == 2){
            this.graph.setParent(item.id,"encoder-block-2");
          }
        });
        this.architecture.decoder.forEach(item => {
          if (item.layerOrder == 1){
            this.graph.setParent(item.id,"decoder-block-1");
          } else if (item.layerOrder == 2){
            this.graph.setParent(item.id,"decoder-block-2");
          }
        });
      },
    }
      
  }
  
</script>

<style>

#translateText {
  width: 50%;
  margin-right: 3px;
}

.clusters rect {
  fill: #00ffd0;
  stroke: #999;
  stroke-width: 1.5px;
}

text {
  font-weight: 300;
  font-family: "Helvetica Neue", Helvetica, Arial, sans-serf;
  font-size: 14px;
}

.node rect {
  stroke: #999;
  fill: #fff;
  stroke-width: 1.5px;
}

.edgePath path {
  stroke: #333;
  stroke-width: 1.5px;
}

</style>