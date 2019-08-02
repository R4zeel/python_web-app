const http = require('http');
const port = process.env.PORT || 5000;

const requestHandler = (request, response) => {
    const date = new Date();
    console.log(request.url);
    response.write('It\'s a simple Node.js server which was deployed to Heroku\n');
    response.write(`Now is ${date.getDate()}.${(date.getMonth() + 1)}.${date.getFullYear()}, ${date.getHours()}:${date.getSeconds()} \n`);
    response.end('You\'re on ' + request.url);
}
const server = http.createServer(requestHandler);

server.listen(port, (err) => {
    if (err) {
        return console.error('something bad happened', err);
    }
    console.log(`server is listening on ${port}`);
})