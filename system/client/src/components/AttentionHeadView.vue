<template>
<div class="container">
  <div class="box">
    <div class="control-pannel">
      <!--<button class="buttons" id="highlightsBtn" @click="onHighlights()">Close Highlights</button>-->
      <el-button type="primary" id="highlightsBtn" plain @click="onHighlights()">Close Highlights</el-button>
      <div class="title-text">
        Generate Query, Key and Value in each head from Input(s) 
      </div>
      <!--<button class="buttons" @click="onExit()">Exit</button>-->
      <el-tooltip content="Quit from Head View." placement="top" effect="dark">
        <el-button type="primary" :icon="CloseBold" plain circle @click="onExit()" />
      </el-tooltip>
    </div>
    <AttentionHeadSelfAnimator v-if="nodeType==='self_attn'"
      @changeOrderAndHilights = "onChangeOrderAndHilights"
      :nodeData = "nodeData"
      :highlights = "highlights"
      :curOrder = "order"
      :openHighlights = "openHighlights"
    />
    <AttentionHeadCrossAnimator v-else-if="nodeType==='cross_attn'"
      @changeOrderAndHilights = "onChangeOrderAndHilights"
      :nodeData = "nodeData"
      :highlights = "highlights"
      :curOrder = "order"
      :openHighlights = "openHighlights"
    />
  </div>
</div>
</template>

<script>
import AttentionHeadSelfAnimator from "./AttentionHeadSelfAnimator"
import AttentionHeadCrossAnimator from "./AttentionHeadCrossAnimator"
import { shallowRef } from "vue"
import { CloseBold,Switch } from '@element-plus/icons-vue'
export default {
  name:"AttentionHeadView",
  components:{
    AttentionHeadSelfAnimator,
    AttentionHeadCrossAnimator,
  },
  props:{
    nodeType:{
      type: String,
      default: '',
    },
    nodeData:{
      type: Object,
      default: function(){return {};},
    },
    
  },
  emits:["exit"],
  data(){
    return {
      CloseBold:shallowRef(CloseBold),
      Switch:shallowRef(Switch),
      highlights: [],
      order: 0,
      openHighlights:true,
    };
  },
  created(){
    console.log('this.type in AttentionHeadView.vue:', this.nodeType);
    console.log('this.nodeData in AttentionHeadView.vue:', this.nodeData);

  },
  beforeUpdate(){
  },
  methods:{
    onExit(){
      console.log("exit from the current detailview.");
      this.$emit('exit');
    },
    onHighlights(){
      // let content = document.getElementById('highlightsBtn').innerHTML;
      // if(content=='Close Highlights'){
      if(this.openHighlights){
        document.getElementById('highlightsBtn').innerHTML = 'Open  Highlights';
        this.openHighlights = false;
      } else {
        document.getElementById('highlightsBtn').innerHTML ='Close Highlights';
        this.openHighlights = true;
      }
    },
    onChangeOrderAndHilights(newValues){
      this.order = newValues.order;
      this.highlights = newValues.highlights;
    },
    // onNextToken(){
    //   console.log('this.curTokenIndex:',this.curTokenIndex);
    //   if(this.curTokenIndex == this.tokenNums-1){
    //     console.log('current token index reaches maximum.');
    //   } else {
    //     this.curTokenIndex += 1;
    //   }
    // },
    // onLastToken(){
    //   console.log('this.curTokenIndex:',this.curTokenIndex);
    //   if(this.curTokenIndex == 0){
    //     console.log('current token index reaches minimum.');
    //   } else {
    //     this.curTokenIndex -= 1;
    //   }
    // },
    // onChangeHilightsIndex(newHighlightsIndex){
    //   this.highlightsIndex = newHighlightsIndex;
    // },
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
  margin-left:5px;
  margin-right:5px;
  margin-top:5px;
  margin-bottom:5px;
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