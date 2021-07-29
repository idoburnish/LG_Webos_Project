const express = require('express');
const app = new express();
const server = require("http").createServer(app);
const io = require('socket.io')(server);

var port = process.env.PORT || 5000;
server.listen(port, () => {
    console.log("express server is listening on port " + port);
});

let finger = 0;

io.on("connection", function(socket) {
    console.log("connect client " + socket.id);

    socket.emit("example", "example from server");
    
    socket.on("finger_number", function(data){
        finger = data.finger_number;
        socket.emit("finger_number",{
            fingerNum : finger
        });
    })


    socket.on("disconnection",function(reason){
        console.log(`disconnect id : ${socket.id} reason : ${reason}`);
        
    })
});
