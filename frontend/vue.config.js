module.exports = {
  outputDir: "dist",
  assetsDir: "static",
  devServer: {
    port: 8080,
    host: "0.0.0.0",
    proxy: {
      "/api*": {
        target: "http://0.0.0.0:8000/"
        // target: "http://192.168.0.16:8000/"
        // target: "http://192.168.1.17:8000/"
      }
    }
  },
  css: {
    loaderOptions: {
      sass: {
        data: '@import "src/assets/scss/core.scss";'
      }
    }
  },
  chainWebpack: config => {
    config.output.filename("[name].[hash].js");

    config.optimization.splitChunks(false);

    config.resolve.alias.set("__STATIC__", "static");
  }
};
