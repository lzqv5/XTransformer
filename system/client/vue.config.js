const config = {
  configureWebpack: {
    resolve: {
      // .mjs needed for https://github.com/graphql/graphql-js/issues/1272
      extensions: ['*', '.mjs', '.js', '.vue', '.json', '.gql', '.graphql']
    },
    module: {
      rules: [ // fixes https://github.com/graphql/graphql-js/issues/1272
        {
          test: /\.mjs$/,
          include: /node_modules/,
          type: 'javascript/auto'
        }
      ]
    },
    devServer:{
      port: 8090,
      proxy:{
        ["/api"]:{
          // target: 'http://127.0.0.1:5050',
          target: 'http://127.0.0.1:5055',
          ws: true,
          changeOrigin: true,
          pathRewrite:{
            "^/api":"",
          }
        }
      },
      // overlay:{
      //   warnings: false,
      //   erros: true,
      // },
    }
  }
 }
 
 module.exports = config