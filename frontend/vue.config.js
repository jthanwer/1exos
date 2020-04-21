module.exports = {
  outputDir: 'dist',
  assetsDir: 'static',
  // baseUrl: IS_PRODUCTION
  // ? 'http://cdn123.com'
  // : '/',
  // For Production, replace set baseUrl to CDN
  // And set the CDN origin to `yourdomain.com/static`
  // Whitenoise will serve once to CDN which will then cache
  // and distribute
  devServer: {
    proxy: {
      '/api*': {
        // Forward frontend dev server request for /api to django dev server
        target: 'http://localhost:8000/',
      }
    }
  },
  chainWebpack: config => {
    config.output
      .filename('bundle.js')

    config.optimization
      .splitChunks(false)

    config.resolve.alias
      .set('__STATIC__', 'static')

    config.devServer
      // the first 3 lines of the following code have been added to the configuration
      .public('http://localhost:8080')
      .host('127.0.0.1')
      .port(8080)
      .hotOnly(true)
      .watchOptions({ poll: 1000 })
      .https(false)
      .disableHostCheck(true)
      .headers({ "Access-Control-Allow-Origin": ["\*"] })
  }
}

// const BundleTracker = require("webpack-bundle-tracker");
//
// const ENV_STAGE = process.env.ENV || "http://localhost:8080/";
//
// const path = require('path');
// module.exports = {
//   publicPath: ENV_STAGE === "PRODUCTION" ? "./static/" : "http://localhost:8080/",
//   outputDir: './dist/',
//
//   chainWebpack: config => {
//
//     config
//       .plugin('BundleTracker')
//       .use(BundleTracker, [{ filename: './webpack-stats.json' }])
//
//     config.output
//       .filename('bundle.js')
//
//     config.optimization
//       .splitChunks(false)
//
//     config.resolve.alias
//       .set('__STATIC__', 'static')
//
//     config.devServer
//       // the first 3 lines of the following code have been added to the configuration
//       .public('http://localhost:8080')
//       .host('127.0.0.1')
//       .port(8080)
//       .hotOnly(true)
//       .watchOptions({ poll: 1000 })
//       .https(false)
//       .disableHostCheck(true)
//       .headers({ "Access-Control-Allow-Origin": ["\*"] })
//   },
//
//   // uncomment before executing 'npm run build'
//   css: {
//     extract: {
//       filename: 'bundle.css',
//       chunkFilename: 'bundle.css',
//     },
//   }
//
// };