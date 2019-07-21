const fs = require('fs');
const cart = require('./cart');
const logger = require('./logger');

const actions = {
    add: cart.add,
    change: cart.change,
    remove: cart.remove
};

let handler = (req, res, action, file) => {
    fs.readFile(file, 'utf8', (err, data) => {
        if(err){
            res.send({result: 0, text: 'error'});
        } else {
            let {name, newCart} = actions[action](JSON.parse(data), req);
            fs.writeFile(file, newCart, (err) => {
                if(err){
                    res.send({result: 0, text: 'error'});
                } else {
                    logger(name, action);
                    res.send({result: 1, text: 'ok'});
                }
            })
        }
    })
};

module.exports = handler;