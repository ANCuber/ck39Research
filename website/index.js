var express = require('express');
var fs = require('fs');

var port = 3000;
var app = express();

app.use(express.static('public'));
app.get('/start', function (req, res) {  
  res.render('suggestion.ejs');
}); 

app.get('/send',function(req,res){
    res.render('send.ejs');
});


app.get('*',function(req,res){
    res.send('404 error!!!!!  what are you doing?');
});


app.listen(port, function(err){
    if(err){
        console.log(err);
    }else{
        console.log('http://localhost:' + port);
    }
});