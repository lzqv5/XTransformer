<template>
  <div class="container">
    <div class="box">
      <div class="column " id="left-column">
        <div class="control-pannel">
          <div></div>
          <div class="title-text">
            Linear Projection View
          </div>
          <div></div>
        </div>
        <div class="container">
          <LinearView
          :input="input"
          :output="output"
          :bias="bias"
          :logSoftmax="logSoftmax"
          :predict="predict"/>
        </div>
      </div>
      <div class="column " id="right-column">
        <div class="control-pannel">
          <div></div>
          <div class="title-text">
            Softmax View
          </div>
          <!--<button @click="onClean()">x</button>-->
          <el-tooltip content="Quit from LinearSoftmax View." placement="top" effect="dark">
            <el-button type="primary" :icon="CloseBold" plain circle @click="onClean()" />
          </el-tooltip>
        </div>
        <div class="container">
          <SoftmaxView
          :output="output"
          :logSoftmax="logSoftmax"
          :cumulativeProb="cumulativeProb"
          :predict="predict"/>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import LinearView from './LinearView'
import SoftmaxView from './SoftmaxView'

import { shallowRef } from "vue"
import { CloseBold } from '@element-plus/icons-vue'
export default {
  name:"LinearSoftmaxView",
  components:{
    LinearView,
    SoftmaxView,
  },
  props:{
    input: {
      type: Array,
      default: function(){return [];},
    },
    output: {
      type: Array,
      default: function(){return [];},
    },
    bias: {
      type: Array,
      default: function(){return [];},
    },
    logSoftmax: {
      type: Array,
      default: function(){return [];}
    },
    cumulativeProb: {
      type: Number,
      default: 0,
    },
    predict: {
      type: Object,
      default: function(){return {};}
    },
  },
  emits:["exit","cleanComponentView"],
  data(){
    return {
      CloseBold:shallowRef(CloseBold),
    };
  },
  mounted(){
    this.redraw();
  },
  methods:{
    onClean(){
      console.log("exit from the current component view.");
      this.$emit('cleanComponentView');
    },
    redraw(){
      console.log("Enter LinearSoftmax.vue");
      console.log("LinearSoftmax - this.cumulativeProb:",this.cumulativeProb);
    }
  },
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
  flex-direction:row;
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

#left-column{
  width:60%;
  height:92%;
}

#right-column{
  width:40%;
  height:92%;
}
</style>