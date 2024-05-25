const path = require('path');

module.exports = {
    entry: './theme/static_src/js/index.jsx',  // 또는 './theme/static_src/ts/index.tsx' TypeScript 사용 시
    output: {
        path: path.resolve(__dirname, 'theme/static/dist'),
        filename: 'bundle.js',
    },
    module: {
        rules: [
            {
                test: /\.jsx?$/,
                exclude: /node_modules/,
                use: {
                    loader: 'babel-loader',
                    options: {
                        presets: ['@babel/preset-env', '@babel/preset-react'],
                    },
                },
            },
            {
                test: /\.tsx?$/,
                exclude: /node_modules/,
                use: 'ts-loader',
            },
        ],
    },
    resolve: {
        extensions: ['.js', '.jsx', '.ts', '.tsx'],
    },
};
