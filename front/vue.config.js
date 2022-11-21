module.exports = {
    publicPath: process.env.NODE_ENV === 'production'
      ? '/immoML/'
      : '/',
    devServer: {
        proxy: 'https://europe-west1-ml-immo-paris.cloudfunctions.net/function-1'
    }
  }