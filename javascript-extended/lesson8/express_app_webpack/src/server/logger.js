const moment = require('moment');
const fs = require('fs');

const logger = (name, action) => {
    fs.readFile('dist/server/db/stats.json', 'utf8', (err, data) => {
        if(err){
            console.log(err);
        } else {
            const stat = JSON.parse(data);
            stat.push({
                prod_name: name,
                action: action,
                time: moment().format('MMMM Do YYYY, h:mm:ss a')
            });
            fs.writeFile('dist/server/db/stats.json', JSON.stringify(stat, null, 4), (err) => {
                if (err) {
                    console.log(err)
                }
            })
        }
    })
};

module.exports = logger;