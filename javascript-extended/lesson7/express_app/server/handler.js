const fs = require('fs');
const cart = require('./cart');
const logger = require('./logger');

const actions = {
  add: cart.add,
  change: cart.change,
  delete: cart.remove,
};

let handler = (req, res, action, file) => {

  fs.readFile(file, 'utf8', (err, data) => {
    if (err) {
      logger(action, 'failed', err.message, null);
      res.send({result: 0, text: 'error'});
    } else {
      logger(action, 'successful', JSON.parse(data), req);
      let newCart = actions[action](JSON.parse(data), req);
      fs.writeFile(file, newCart, (err) => {
        if (err) {
          res.send({result: 0, text: 'error'});
        } else {
          res.send({result: 1, text: 'ok'});
        }
      })
    }
  })
};

module.exports = handler;