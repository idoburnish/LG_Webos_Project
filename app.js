const express = require('express');
const app = new express();
const server = require("http").createServer(app);
const io = require('socket.io')(server);

var port = process.env.PORT || 5000;
server.listen(port, () => {
    console.log("express server is listening on port " + port);
});

let finger = 0;

// app.get("/", function(req, res) {
//     console.log('from opencv (POST)');
//     var temp = req.body
//     console.log(temp);
// })

io.on("connection", function(socket) {
    console.log("connect client " + socket.id);

    socket.emit("example", "example from server");
    
    socket.on("finger_number", function(data){
        console.log("finger_number socket connect");
        console.log("data: " + data);
        console.log("data.numbers: " + JSON.parse(data).numbers);
        finger = data.finger_number;
        socket.emit("finger_number",{
            fingerNum : finger
        });
    })

    socket.emit("finger_number", "dd");


    socket.on("disconnection",function(reason){
        console.log(`disconnect id : ${socket.id} reason : ${reason}`);
        
    })
});
