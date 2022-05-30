const mysql = require('mysql');
const db = mysql.createConnection({
    user: "willy",
    host: "localhost",
    password: "1818",
    database: "latex"
});

var fs = require('fs');

fs.readFile('tex.txt', function (err, data) {
    if (err) throw err;
    for(var i in data.toString().split(/\r?\n/)){
        let sql = "INSERT INTO data(latex) VALUE (\""+data.toString().split('\n')[i].replace(/[\r\n]/gm, '')+"\")";
        console.log(sql);
        db.query(sql,(err,res)=>{
            if(err) throw err;
        })
    }
    
});