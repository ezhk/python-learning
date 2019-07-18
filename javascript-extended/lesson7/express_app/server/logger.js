const fs = require('fs');
const moment = require('moment');

const util = require('util');
const readFileAsync = util.promisify(fs.readFile);

const logFile = 'server/db/stats.json';

async function logger(action, status, payload, req) {
  let logfileObject = [];
  let productName;

  try {
    logfileObject = JSON.parse(await readFileAsync(logFile, 'utf8'));
  } catch (err) {
    console.log(err.message);
  }

  switch (status) {
    case 'failed':
      break;
    case 'successful':
      // add action contains productName in body
      if (req.body.product_name) {
        productName = req.body.product_name;
        break;
      }

      let find = payload.contents.find(el => el.id_product === +req.params.id);
      if (find && find.product_name) {
        productName = find.product_name;
      }
      break;
  }

  logfileObject.push({
    timestamp: moment().toISOString(),
    action,
    productName,
    body: req.body,
    status,
  });

  fs.writeFile(logFile, JSON.stringify(logfileObject, null, 4), (err) => {
    if (err) {
      console.log(err);
    }
  });
}

module.exports = logger;
