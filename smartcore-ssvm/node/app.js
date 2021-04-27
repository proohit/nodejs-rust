const { say, basic_prediction2, load_model, create_file, read_file } = require('../pkg/ssvm_nodejs_starter_lib.js');

const http = require('http');
const url = require('url');
const hostname = '0.0.0.0';
const port = 3000;

const server = http.createServer((req, res) => {
  create_file("/hello.txt", "Hello WASI SSVM\nThis is in the `pkg` folder\n");

  const queryObject = url.parse(req.url, true).query;
  if (!queryObject['name']) {
    res.end(`Please use command curl http://${hostname}:${port}/?name=MyName \n`);
  } else {
    console.log( read_file("/hello.txt") );

    res.end(load_model());
    // res.end(say(queryObject['name']) + '\n');
  }
});

server.listen(port, hostname, () => {
  console.log(`Server running at http://${hostname}:${port}/`);
});
