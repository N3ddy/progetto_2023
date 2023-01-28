playing = true
$(document).ready(function(){
    //actions
    var socket = io() 
    socket.on('connect', function() {
        console.log("connected")
    });
    
    $('#start').click(function(){
        console.log("test")
        socket.emit("change_color", "red") 
    })

    $('#finish').click(function(){
        console.log("test")
        socket.emit("change_color", "yellow") 
    })

    socket.on("message", function(msg) {
        console.log(msg)
        if(msg == "red"){
            $("#containGame").css("background-color", "red")
        }else if(msg == "yellow"){
            $("#containGame").css("background-color", "yellow")
        }
    })

    /*
    $('#match').click(function(){
        socket.emit('join',{"room": "general", "username":"username"});
        
    })
    socket.on("join", function(data){
        console.log(data);
        if (data.error) 
            console.log('Something went wrong on the server');

        if (data.ok)
            console.log('Event was processed successfully');
    });*/
})