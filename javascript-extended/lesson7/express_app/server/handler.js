const fs = require('fs');
const cart = require('./cart');

const actions = {
  add: cart.add,
  change: cart.change
};

let handler = (req, res, action, file) => {
  fs.readFile(file, 'utf8', (err, data) => {
    if (err) {
      res.send({result: 0, text: 'error'});
    } else {
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