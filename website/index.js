var express = require('express');
var fs = require('fs');
const { waitForDebugger, Session } = require('inspector');

const mysql = require('mysql');
const db = mysql.createConnection({
    user: "willy",
    host: "localhost",
    password: "1818",
    database: "latex"
});

var port = 3000;
var app = express();
app.set('views', './views');
app.set('view engine', 'ejs');
app.use(express.static('public'));
app.use(express.urlencoded({
    extended: true
}))

function startpage(req, res) {
    let sql = "SELECT * from data WHERE done=0 ORDER BY RAND() LIMIT 1"
    db.query(sql,(err,result)=>{
        if(err){
            throw err;
        }else{
            if(result[0]==undefined){
                res.render('thanks');
            }else{
            res.render('newindex', {
            latex: result[0].latex,
            dbid : result[0].id
            });   
        }
        }
       
    });
   
}


app.get('/start', function (req, res) {
    startpage(req, res);
});

app.post('/submit', function (req, res) {
    if(req.body.bt=="確認答案"){
        console.log(req.body.dbid);
        var descriptionsql ="UPDATE DATA SET description=\""+req.body.description+"\" WHERE id="+req.body.dbid;
        var donesql = "UPDATE DATA SET done=1 WHERE id="+req.body.dbid;
        console.log(descriptionsql);
        db.query(descriptionsql,(err,res)=>{
            if(err) throw err;
            console.log("update completed");
        })
        db.query(donesql,(err,res)=>{
            if(err) throw err;
            console.log("done status updated");
        })
    }
    res.redirect("/start");
});

app.post('/send', function (req, res) {
    var content = req.body.answer;
    if (content == "" || content.indexOf(' ')>=0  || content.indexOf(';')>=0 ) {
        res.redirect('https://www.youtube.com/watch?v=dQw4w9WgXcQ');
    } else {
        console.log(content);
        res.render('newsend', {
            yourres: content,
            dbid : req.body.dbid
        });
    }
});


app.get('*', function (req, res) {
    res.redirect("/start");
});


app.listen(port, function (err) {
    if (err) {
        console.log(err);
    } else {
        console.log('http://localhost:' + port + "/start");
    }
});