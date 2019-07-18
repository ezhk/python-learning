const func = require('./func');
const os = require('os');
const fs = require('fs');
const http = require('http');

// fs.writeFile('some.txt', `i i'm new string`, (err) => {
//     if(err){
//         console.log(err);
//     }
// });
// fs.readFile('some.txt', 'utf8', (err, data) => {
//     console.log(data);
// });
// console.log(os.platform());
// console.log(os.cpus());
// console.log(os.type());

// const server = http.createServer((req, res) => {
//     if(req.url === '/'){
//         res.write('Hello World');
//         res.end();
//     }
// });
// server.listen(3000);
// server.on('connection', () => {
//    console.log('new connection');
// });
// console.log('Server stat at port 3000...');

// console.log(a(30));
// console.log(func(40));