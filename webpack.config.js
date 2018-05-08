const path = require('path'),
  webpack = require('webpack');
const PROD = JSON.parse(process.env.PROD_ENV || '0');
let plugins;

if (PROD) {
  plugins = [
    new webpack.optimize.UglifyJsPlugin({minimize: true})
  ];
} else {
  plugins = [];
}

module.exports = {
  entry: {
    admin: './web/src/admin/index.js',
    client: './web/src/client/index.js',
    authentication: './web/src/admin/authentication.js'
  },
  output: {
    filename: '[name]_bundle.js',
    path: path.resolve(__dirname, 'web/static')
  },
  devServer: {
    contentBase: './templates',
    historyApiFallback: true,
    inline: true
  },
  module: {
    loaders: [
      {
        test: /\.js$/,
        exclude: /node_modules/,
        loader: 'babel-loader',
        query: {
          presets: ['es2015', 'react']
        }
      }, {
        test: /\.(png|jpg|gif)$/,
        loader: 'file-loader?name=img/[name].[ext]'
      }, {
        test: /\.(scss|css)$/,
        use: [{
          loader: "style-loader"
        }, {
          loader: "css-loader"
        }, {
          loader: "sass-loader"
        }]
      }, {
        test: /\.(eot|woff|woff2|svg|ttf)([\?]?.*)$/,
        loader: "file-loader"
      }]
  },
  stats: {
    colors: true
  },
  devtool: 'source-map',
  plugins: plugins,
};
