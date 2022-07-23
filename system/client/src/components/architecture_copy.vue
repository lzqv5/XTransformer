<template>
    <div id="architectureDiv" style="height: 100%; width: 100%">
      <div id="container">
      </div>
    </div>
</template>

<script>
  /*
  This component use G6 to construct Architecture View for Transformer
  G6 github: https://github.com/antvis/G6
  G6 是一个图可视化引擎。它提供了图的绘制、布局、分析、交互、动画等基础的图可视化能力。旨在让关系变得透明，简单。让用户获得关系数据的 Insight.
   */
  // import * as d3 from "d3";
  import G6 from '@antv/g6'

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
        architectureData: {
          nodes: [],  // {id,label,type,style}
          edges: [],  // {source,target,type,id}
        },
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
      this.initArchitecture();
      // this.initGraph();
    },
    methods: {
      initArchitecture(){
        console.log("Intializing the Architecture View ...");

        const graph = new G6.Graph({  // 对图的初始化设置
          container: 'container', // 指定挂载容器
          width: 1600,   // 图的宽度  
          height: 750,  // 图的高度
          // 图的交互模式Mode设置
          // 如果要使用自定义的 behavior, 需要在定义图的时候先进行注册
          modes: {
            default:[
              // 'drag-canvas', 
              // 'zoom-canvas', 
              'collapse-expand-combo',
            ],
          },
          // plugins: [this.registerCustomizedDataTip()],
          plugins: [],
          // 图的布局设置
          layout: {
            type: 'dagre', // 层次布局
            rankdir: 'LR',
            align: 'UR',
            nodesep: 20,
            ranksep: 25,
            controlPoints: true,

          },
          // 图中节点的默认设置
          defaultNode: {
            type: 'rect', // 节点默认形状
            size: [20,120],    // 节点默认大小 
            color: '#5B8FF9', // 节点默认颜色
            // 该节点可选的连接点集合 - 边 连入 节点的相对位置
            anchorPoints: [
              [0, 0.5],
              [0.5, 0],
              [0.5, 1],
              [1, 0.5],
            ],
            style: {
              fill: '#9EC9FF',  // 节点填充色
              // lineWidth: 5,     // 节点描边色
              // cursor: "pointer",
              opacity: 0.7,
            },
            labelCfg: {
              position: "top",
              style: {    
                fill: '#000',   // 节点上的标签文字颜色
                fontSize: 10,   // 节点上的标签文字大小
                // cursor: "pointer",
              },
            },
          },
          // 图中边的默认设置
          defaultEdge: {
            type: "can-running-line", // 自定义的边
            style: {
              stroke: 'grey',  // 边的描边颜色
              opacity: 0.3,   // 边不透明度
              lineWidth: 2,
              endArrow:  {
                path: 'M 0,0 L -2,1 L -2,-1 Z',
                d: 1.5,
              }
              // cursor: "crosshair",
            },
          },
          nodeStateStyles: {
            'hover': {
              fill: '#d3adf7',
              opacity: 1,
            }
          },
          edgeStateStyles: {
            running: {
              stroke: 'black',  // 边的描边颜色
              opacity: 1,   // 边不透明度
            },
          },
          fitView: true,    // 设置是否将图适配到画布中
          fitViewPadding: [25, 25, 25, 25],  // 画布上四周的留白宽度
          renderer: 'svg',  // 指定渲染方式
          cursor: "default",
        });
        this.graph = graph;

        console.log("Register customized edges into Graph...");
        this.registerCustomizedEdge("can-running-line");
        this.registerCustomizedEdge("can-running-polyline");

        // 为每个节点初始化动画
        this.initNodesIteractState();

        // 初始化数据
        console.log("Initialize the data...");
        this.initArcitectureData();

        console.log("Load the data...");
        console.log(this.architectureData);
        graph.data(this.architectureData); // 加载数据

        console.log("Rendering...");
        graph.render();   // 渲染
        
      },

      initGraph(){
        console.log("initalize Graph Demo ...");
        console.log(G6.Global.version);
        // 设置数据
        // 引入 G6 的数据源为 JSON 格式的对象。该对象中需要有节点（nodes）和边（edges）字段，分别用数组表示
        const initData = {
          nodes: [  // 点集
            {
              id: 'node1',  // 节点的唯一标识
              label: '起始点', // 节点文本
              x: 150,   // 节点横坐标
              y: 150,   // 节点纵坐标
            },
            {
              id: 'node2',
              label: '目标点',
              x: 400,
              y: 150,
            },
          ],
          // 边集
          edges: [
            { // 表示一条从 node1 节点连接到 node2 节点的边;
              source: 'node1',    // 起始点 id
              target: 'node2',    // 目标点 id
              label:  '我是连线'   // 边的文本
            },
          ],
        };

        const graph = new G6.Graph({
          container: 'container', // 指定挂载容器
          width: 500,   // 图的宽度  
          height: 500,  // 图的高度
          defaultNode: {
            type: 'circle',
            size: [100],
            color: '#5B8FF9',
            style: {
              fill: '#9EC9FF',
              lineWidth: 3,
            },
            labelCfg: {
              style: {
                fill: '#fff',
                fontSize: 20,
              },
            },
          },
          defaultEdge: {
            style: {
              stroke: '#e2e2e2',
            },
          },
        });

        graph.data(initData); // 加载数据
        graph.render();   // 渲染
      },

      createInputNode(isEncoder=true){
        return {
          id: isEncoder == true ? "encoder-input" : "decoder-input",
          // label: isEncoder == true ? "Encoder Embedding" : "Decoder Embedding",
          label: "Input",
          type:"rect",
          style:{},
          y: isEncoder == true ? 100 : 300,
          layer: 0,
          // _order: isEncoder == true ? 1 : 2,
        }
      },

      createTokenizeNode(isEncoder=true){
        return {
          id: isEncoder == true ? "encoder-tokenize" : "decoder-tokenize",
          // label: isEncoder == true ? "Encoder Embedding" : "Decoder Embedding",
          label: "Tokenize",
          type:"rect",
          style:{},
          // y: isEncoder == true ? 100 : 300,
          layer: 1,
          // _order: isEncoder == true ? 1 : 2,
        }
      },

      createEmbeddingNode(isEncoder=true){
        return {
          id: isEncoder == true ? "encoder-embedding" : "decoder-embedding",
          // label: isEncoder == true ? "Encoder Embedding" : "Decoder Embedding",
          label: "Embedding",
          type:"rect",
          style:{},
          // y: isEncoder == true ? 100 : 300,
          layer: 2,
          // _order: isEncoder == true ? 1 : 2,
        }
      },

      createPositionalEncodingNode(isEncoder=true){
        return {
          id: isEncoder == true ? "encoder-PE" : "decoder-PE",
          // label: isEncoder == true ? "Encoder Positional Encoding" : "Decoder Positional Encoding",
          label: "Positional Encoding",
          type: "rect",
          style: {},
          // y: isEncoder == true ? 100 : 300,
          layer: 3,
          // _order: isEncoder == true ? 1 : 2,
        }
      },

      createAttentionNode(layerOrder, isEncoder=true, isSelf=true, isMasked=false){
          let coder = isEncoder ? "encoder-" : "decoder-";
          let mask = isMasked ? "masked-" : "full-", maskLabel = isMasked ? "Masked " : "Full ";
          let mechanism = isSelf ? "self-" : "cross-", mechanismLabel = isSelf ? "Self-" : "Cross-";
          return { 
            id: coder + layerOrder + "-" + mask + mechanism + "attention",
            label: maskLabel + mechanismLabel + "Attention",
            type:"rect",
            style: {},
            // layerOrder: layerOrder
            
          }
        },

      createAddNode(layerOrder, innerOrder, isEncoder=true) {
        let coder = isEncoder ? "encoder-" : "decoder-";
        return {
          id: coder + layerOrder + "-" + innerOrder + "-add",
          label: "Add",
          type: "circle",
          style: {},
          // layerOrder: layerOrder,
          // innerOrder: innerOrder
        }
      },

      createLayerNormNode(layerOrder, innerOrder,isEncoder=true){
        let coder = isEncoder ? "encoder-" : "decoder-";
        return {
          id: coder + layerOrder + "-" + innerOrder + "-LN",
          label: "Layer Norm",
          type: "rect",
          style: {},
          // layerOrder: layerOrder,
          // innerOrder: innerOrder
        }
      },

      createFeedForwardNode(layerOrder,isEncoder=true){
        let coder = isEncoder ? "encoder-" : "decoder-";
        return {
          id: coder + layerOrder + "-FF",
          label: "Feed Forward",
          type: "rect",
          style: {},
          // layerOrder: layerOrder
        }
      },

      createLinearNode(){
        return {
          id: "linear",
          label: "Linear",
          type: "rect",
          style: {},
        }
      },
      
      createSoftmaxNode(){
        return {
          id: "softmax",
          label: "Softmax",
          type: "rect",
          style: {},
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

      initArcitecture(){
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
        this.architecture;
      },

      convertArc2ArcDataNodes(){
        // 添加 Encoder 内部的节点
        let order = 0
        this.architecture.encoder.forEach(d => {
          if (d instanceof Array) {
            // d 是一个数组
            order += 1
            this.architectureData.nodes.push({
              id: "encoder-block-" + order,
              label: "Encoder Block",
              type: "rect",
              style: {},
              layer: 3+order,
              size: [90,120], 
            });
          } else {
            // d 是一个节点对象
            // console.log(d);
            this.architectureData.nodes.push(d);
          }
        });
        // 添加 Decoder 内部的节点
        order = 0
        this.architecture.decoder.forEach(d => {
          if (d instanceof Array) {
            // d 是一个数组
            order += 1
            this.architectureData.nodes.push({
              id: "decoder-block-" + order,
              label: "Decoder Block",
              type: "rect",
              style: {},
              layer: 3+order,
              size: [90,120], 
            });
          } else {
            // d 是一个节点对象
            // console.log(d);
            this.architectureData.nodes.push(d);
          }
        });
        // 添加 generator 内部的节点
        this.architecture.generator.forEach(d=>{
          this.architectureData.nodes.push(d);
        });
      },

      convertArc2ArcDataEdges(){
        let counter = 0;
        let id_source = "encoder-input";
        // 添加 Encoder 内部的所有边
        this.architecture.encoder.forEach(d => {
          if (d instanceof Array) {
            counter += 1;
            let id = "encoder-block-" + counter;
            // 这里的 can-running-line 是我们自定义的边, 其中定义了一些事件和动画
            let edge = {source: id_source, target: id, type: "can-running-line"}
            // console.log(edge);
            this.architectureData.edges.push(edge);
            id_source = id;
          } else {
            if (d.id != "encoder-input"){
              let edge = {source: id_source, target: d.id, type: "can-running-line"}
              // console.log(edge);
              this.architectureData.edges.push(edge);
              id_source = d.id;
            }
          }
        });
        // 添加 Decoer 内部的所有边
        let id_source_encoder_output = id_source;
        id_source = "decoder-input";
        counter = 0;
        this.architecture.decoder.forEach(d=>{
          if (d instanceof Array){
            counter += 1;
            let id = "decoder-block-" + counter
            let edge = {source:id_source, target:id, type:"can-running-line"};
            let edgeCross = {source:id_source_encoder_output, target:id, type:"can-running-polyline"};
            // console.log(edge);
            // console.log(edgeCross);
            this.architectureData.edges.push(edge);
            this.architectureData.edges.push(edgeCross);
            id_source = id;
          }else{
            if (d.id != "decoder-input"){
              let edge = {source:id_source, target:d.id, type:"can-running-line"};
              // console.log(edge);
              this.architectureData.edges.push(edge);
              id_source = d.id;
            }
          }
        });
        // 添加 Generator 内部的所有边
        this.architecture.generator.forEach(d => {
          let edge = {source:id_source, target:d.id, type:"can-running-line"};
          // console.log(edge);
          this.architectureData.edges.push(edge);
          id_source = d.id;
        });
      },

      initArcitectureData(){
        this.initArcitecture();
        this.convertArc2ArcDataNodes();
        this.convertArc2ArcDataEdges();
      },

      initNodesIteractState(){
        this.graph.on("node:mouseenter", (evt) => {
          const node = evt.item;
          this.graph.setItemState(node,'hover', true);
          // console.log(node.hasState('hover'));
        });
        this.graph.on("node:mouseleave", (evt) => {
          const node = evt.item;
          this.graph.setItemState(node,'hover', false);
          // console.log(node.hasState('hover'));
        });
        this.graph.on('node:click', (evt) => {
          const shape = evt.target;
          const node = evt.item;
          console.log('Event: ', evt);  // evt 是事件对象
          console.log('Shape: ', shape);  // shape 对应发生事件的图元
          console.log('Node: ', node);    // node 对应发生事件的节点
          console.log('Related Edges: ', node.getEdges());    
          console.log('Node info: ', node._cfg.model);
          console.log('this.graph.save(): ', this.graph.save());
        });
      },

      registerCustomizedEdge(edgeName){
        if (edgeName == "can-running-line"){
          const lineDash = [4, 2, 1, 2];
          let options = {
            // 复写 setState 方法 
            setState(name, value, item){
              // item: 需要修改状态的元素
              // name: 状态名
              // value: 修改状态的内容
              const shape = item.get('keyShape');
              // shape;
              // 监听 running 状态
              if (name == 'running') {
                // running 状态为 true 时
                if (value) {
                  let index = 0; // 边 path 图形的动画
                  shape.animate(
                    ()=>{
                      index++;
                      if (index > 9 ){
                        index = 0;
                      }
                      const res = {
                        lineDash,
                        lineDashOffset: -index,
                      };
                      //返回需要修改的参数集, 
                      return res;
                    },
                    {
                      repeat: true, // 动画重复
                      duration: 3000, // 一次动画持续时长
                    },
                  );
                
                } else {
                // running 状态 为 false
                // 结束动画
                shape.stopAnimate();
                // running 为 false 时，要停止动画，同时把 lineDash 清空
                shape.attr("lineDash", null);
                }
              }
            },
            stateStyles: {  // 当对应节点 or 边处于不同状态下时, 所需要呈现的视觉样式
              running: {
                stroke: 'black',  // 边的描边颜色
                opacity: 1,   // 边不透明度
              },
            },
          };
          G6.registerEdge(edgeName,options,"line");
          // 监听 mouseenter 事件
          this.graph.on('edge:mouseenter',(evt) => {
            // 获得当前鼠标操作的目标边
            const edge = evt.item;
            // 将当前边的 running 状态设置为 true
            this.graph.setItemState(edge, 'running', true);
            // 查看当前状态
            // console.log(evt.item.hasState('running'));  // true
          }); 
          // 监听 mouseleave 事件
          this.graph.on('edge:mouseleave',(evt) => {
            // 获得当前鼠标操作的目标边
            const edge = evt.item;
            // 将当前边的 running 状态设置为 false
            this.graph.setItemState(edge, 'running', false);
            // console.log(evt.item.hasState('running')); // false
          }); 
          // 监听 mouseclick 事件 - 显示对应数据流
          this.graph.on('edge:click',(evt)=>{
            evt;
            // ...
          });
        } else  if (edgeName == "can-running-polyline"){
          const lineDash = [4, 2, 1, 2];
          let options = {
            // 复写 setState 方法 
            setState(name, value, item){
              const shape = item.get('keyShape');
              // 监听 running 状态
              if (name == 'running') {
                // running 状态为 true 时
                if (value) {
                  let index = 0; // 边 path 图形的动画
                  shape.animate(
                    ()=>{
                      index++;
                      if (index > 9 ){
                        index = 0;
                      }
                      const res = {
                        lineDash,
                        lineDashOffset: -index,
                      };
                      //返回需要修改的参数集, 
                      return res;
                    },
                    {
                      repeat: true, // 动画重复
                      duration: 3000, // 一次动画持续时长
                    },
                  );
                } else {
                // running 状态 为 false
                // 结束动画
                shape.stopAnimate();
                // running 为 false 时，要停止动画，同时把 lineDash 清空
                shape.attr("lineDash", null);
                }
              }
            },
            stateStyles: {  // 当对应节点 or 边处于不同状态下时, 所需要呈现的视觉样式
              running: {
                stroke: 'black',  // 边的描边颜色
                opacity: 1,   // 边不透明度
              },
            },
          };
          G6.registerEdge(edgeName,options,"polyline");
          // 监听 mouseenter 事件
          this.graph.on('edge:mouseenter',(evt) => {
            // 获得当前鼠标操作的目标边
            const edge = evt.item;
            // 将当前边的 running 状态设置为 true
            this.graph.setItemState(edge, 'running', true);
          }); 
          // 监听 mouseleave 事件
          this.graph.on('edge:mouseleave',(evt) => {
            // 获得当前鼠标操作的目标边
            const edge = evt.item;
            // 将当前边的 running 状态设置为 false
            this.graph.setItemState(edge, 'running', false);
          }); 
          // 监听 mouseclick 事件 - 显示对应数据流
          this.graph.on('edge:click',(evt)=>{
            evt;
            // ...
          });
        }
      },

      registerCustomizedDataTip(){
        const tooltip = new G6.Tooltip({
          offsetX: 10,
          offsetY: 20,
          getContent(e) {
            const outDiv = document.createElement('div'); //  到时候可以替换为子组件
            outDiv.style.width = '180px';
            outDiv.innerHTML = `
              <h4>自定义tooltip</h4>
              <ul>
                <li>Label: ${e.item.getModel().label || e.item.getModel().id}</li>
              </ul>`
            return outDiv
          },
          itemTypes: ['edge'],
        });
        return tooltip;
      },
    }
  }
</script>

<style>
</style>