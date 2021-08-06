const express = require('express');
const app = new express();
const server = require("http").createServer(app);
const io = require('socket.io')(server);

var port = process.env.PORT || 5000;
server.listen(port, () => {
    console.log("express server is listening on port " + port);
});

let finger = 0;
var window_count = -1;
var LED_count = -1;

io.sockets.on("connection", function(socket) {
    console.log("[connect client] " + socket.id);
    
    socket.on("finger_number", function(data){
        console.log("finger_number socket connect");
        console.log("data.numbers: " + JSON.parse(data).numbers);
        finger = JSON.parse(data).numbers;

        if (finger == 1) {  // 손가락 1일 경우
            window_count += 1;
            var status = window_count % 2 ;  // LED status: 1(open)/0(close)
            console.log("finger: " + finger + " status: " + status);
            io.sockets.emit("finger_send", {
                fingerNum : finger,
                status: status
            });
        }
        else if (finger == 2) { //손가락 2일 경우
            LED_count += 1;
            var status = LED_count % 2; // window status: 1(on)/0(off)
            console.log("finger: " + finger + " status: " + status);
            io.sockets.emit("finger_send", {
                fingerNum : finger,
                status: status
            });
        }
        else if (finger == 3) {
            var status = 0 ;
            console.log("finger: " + finger + " status: " + status);
            io.sockets.emit("finger_send", {
                fingerNum : finger,
                status: status
            });
        }
    });

    socket.on("test", function(data) {
        console.log("test: " + data);
    })

    socket.on("disconnection",function(reason){
        console.log(`disconnect id : ${socket.id} reason : ${reason}`);
        
    })
});
