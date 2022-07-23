import axios from 'axios'

let DataService = {
  // 指明了后端服务器的地址, 以便访问数据
  // dataServerUrl: 'http://127.0.0.1:5000',
  // dataServerUrl: 'http://127.0.0.1:5050',
  // dataServerUrl: 'http://127.0.0.1:5055',
  dataServerUrl: 'http://10.192.9.11:5055',
  
  // 下面定义了一些 HTTP 访问请求, 这些访问请求用来访问后端服务器(dataServerUrl)
  // 后端服务器在 view.py 中定义好了对前端不同访问请求的不同处理方式 — 形成前端和后端的 交互
  
  // HTTP GET request 
  get(callback){
    axios.get(`${this.dataServerUrl}/get`)
      .then(response => {
        callback(response.data)
      }, errResponse => {
        console.log(errResponse)
      })
  },
  getData(callback){
    axios.get(`${this.dataServerUrl}/get_data`)
      .then(response => {
        callback(response.data)
      }, errResponse => {
        console.log(errResponse)
      })
  },

  // HTTP POST request
  post(param, callback){
    axios.post(`${this.dataServerUrl}/post`, param)
      .then(response => {
        callback(response.data)
      }, errResponse => {
        console.log(errResponse)
      })
  },

  // input the text from the frontend and get the data from the backend
  translate_input_text(text, callback){
    axios.post(`${this.dataServerUrl}/translate_input_text`, text)
      .then(response => { // 这里的 response 是后端返回的json对象(这个对象内部有很多内容, 我们只需要其中的data), 并将其中的数据作为参数传递到 callback 中
        // console.log('transmission begin ', new Date());
        // 大概要耗时 10s
        callback(response.data);
      }, errResponse => {
        console.log(errResponse)
      })
      .catch(err => {
        console.log('Error: ',err);
      });
  },
  
  // get params from the backend
  getParams(paramIndex, callback){
    axios.post(`${this.dataServerUrl}/getParams`, paramIndex)
      .then(response => { 
        callback(response.data);
      }, errResponse => {
        console.log(errResponse)
      })
      .catch(err => {
        console.log('Error: ',err);
      });
  },

}

export default DataService;
