const { time } = require('console');
var express = require('express');
var fs = require('fs');
const { waitForDebugger } = require('inspector');
var Latex = "  \\frac{1}{2} ";
var port = 3000;
var app = express();
app.set('views', './views');
app.set('view engine', 'ejs');
app.use(express.static('public'));
app.use(express.urlencoded({
  extended: true
}))
function startpage(req,res){
    res.render('newindex',{
      latex : Latex
  });
}
function wait(ms) {
    return new Promise(resolve =>setTimeout(() =>resolve(), ms));
};
app.get('/start', function (req, res) {  
  startpage(req,res);
}); 
app.post('/start',function(req,res){
    //do something
    startpage(req,res);
});
app.post('/send',function(req,res){ 
    var content = req.body.answer;
    if(content == ""){
        //res.send("NO~~ you enter a empty response")

        res.redirect('https://www.youtube.com/watch?v=dQw4w9WgXcQ');
        

    }else{
      console.log(content);
    res.render('newsend',{
        yourres : content
    });   
    }
   
   
    
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