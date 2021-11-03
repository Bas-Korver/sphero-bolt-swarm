module.exports = {
  chainWebpack: (config) => {
    config.plugin("html").tap((args) => {
      args[0].title = "Sphero BOLT Swarm application";

      return args;
    });
  },

  publicPath: './static/',
  assetsDir: '../static',
  outputDir: '../templates'
};
