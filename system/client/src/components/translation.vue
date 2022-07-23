<template>
    <div id="translateDiv" style="height: 100%; width: 100%">
      <el-row align="middle">
        <el-col :span="8">
          <span id = "translateStepwiseSpan"> Translation until current iteration:  </span>
        </el-col>
        
        <el-col :span="12" >
          <!--<input id="translateStepwise" :disabled='disableControl' class="translateText" type="text" 
            :value = "currentTranslation" readonly>-->
            <el-input v-model="currentTranslationData" disabled>
              <template #append>
                <el-button-group>
                  <el-tooltip content="Last predicted word" placement="bottom" effect="light">
                    <el-button type="primary" plain @click="onLast($event)">
                      <el-icon class="el-icon--right" ><ArrowLeftBold /></el-icon>
                    </el-button>
                  </el-tooltip>
                  <el-tooltip content="Next predicted word" placement="bottom" effect="light">
                    <el-button type="primary" plain @click="onNext($event)">
                      <el-icon class="el-icon--right" ><ArrowRightBold /></el-icon>
                    </el-button>
                  </el-tooltip>
                </el-button-group>
              </template>
            </el-input>
        </el-col>

      </el-row>
      
      <el-row align="middle" >
        <el-col :span="8">
          <span id = "predictionOfCurrentIterationSpan"> Prediction in current iteration: </span>
        </el-col>
        
        <el-col :span="12">
          <span id = "predictionOfCurrentIteration" text-align="left"
            :innerHTML = "currentPredictionData"></span>
        </el-col>

      </el-row>
      
      <el-row align="middle" >
        <el-col :span="8">
          <span id="translateOnceSpan"> Full Translation: </span> 
        </el-col>
        
        <el-col :span="12">
          <el-input v-model="fullTranslationData" disabled>
            <template #append>
              <el-tooltip content="The text displayed on the left is the final translation of the source text." placement="top" effect="dark">
                <el-icon><InfoFilled /></el-icon>
              </el-tooltip>
            </template>
          </el-input>
        </el-col>

      </el-row>
    </div>
</template>

<script>
  /*
  This component demonstrates one way to construct d3 visualization.
  d3 example source: https://observablehq.com/@d3/sortable-bar-chart
   */
  // import * as d3 from "d3";
  // import {shallowRef} from "vue"
  import { InfoFilled} from '@element-plus/icons-vue'
  import { ArrowLeftBold, ArrowRightBold } from '@element-plus/icons-vue'
  export default {
    name: "cpnTranslation",
    components:{
      ArrowLeftBold,
      ArrowRightBold,
      InfoFilled,
    },
    props: {
      fullTranslation: {
        type: String,
        default: '',
      },
      currentTranslation: {
        type: String,
        default: '',
      },
      currentPrediction: {
        type: String,
        default: '',
      },
      disableControl: {
        type: Boolean,
        default: false,
      },
    },
    // emits: ['selected'], // 子组件发射事件, 父组件接收事件并完成相应数据交互
    emits: ["last","next"], // 子组件发射事件, 父组件接收事件并完成相应数据交互
    data() {
      return {
        // svg: null,
        currentTranslationData:'',
        currentPredictionData:'',
        fullTranslationData:'',
      }
    },
    watch: {
      // loadData: function () {
      //   // When data is changed in parent, render this component
      //   this.renderBarChart();
      // },
    },
    beforeUpdate(){
      this.currentTranslationData = this.currentTranslation;
      this.currentPredictionData = this.currentPrediction;
      this.fullTranslationData = this.fullTranslation;
    },
    mounted() {

    },
    methods: {
      onLast(e){
        // console.log(e);
        e.stopPropagation();
        this.$emit('last');
      },
      onNext(e){
        // console.log(e);
        e.stopPropagation();
        this.$emit('next');
      },
    }
  }
</script>

<style scoped>
.el-row {
  margin-top: 2px;
  margin-bottom: 2px;
}
.translateText {
  width: 30%; 
  /* width: 200px; */
  /* margin-right: 3px; */
  margin: 3px 3px 3px 3px;
}

</style>