playing = true
$(document).ready(function(){
    
    /**
     * function create when the user open the game page
     * It creates the socket for the communication
     */
    var socket = io() 
    socket.on('connect', function() {
        console.log("connected")
        socket.emit("startInfo")
    });
    
    

    socket.on("message", function(msg) {
        if(msg == "red"){
            $("#containGame").css("background-color", "red")
        }else if(msg == "yellow"){
            $("#containGame").css("background-color", "yellow")
        }
    });

    /**
     * function called when we want to update the avaiable room
     */
    socket.on("load_avaiable_rooms", function(data) {
        $('#avaiableRooms').empty();
        Object.keys(data).forEach(key => {
            var room_button = $('<input type="button" value=' + data[key] + '"/>')
            .attr('class', 'enter_room')
            .attr('id', key)
            .click(f => {
                console.log("test funziona");
                socket.emit('enter_existing_room',{"room": "room", "username":key});
            });
            room_button.appendTo($("#avaiableRooms"));
        });
    });

    /**
     * function called when a user enter the game page
     */
    socket.on("setup", function(data) {
        $('#avaiableRooms').empty();
        Object.keys(data).forEach(key => {
            var room_button = $('<input type="button" value=' + data[key] + '"/>')
            .attr('class', 'enter_room')
            .attr('id', key)
            .click(f => {
                console.log("test funziona");
                socket.emit('enter_existing_room',{"room": "room", "username":key});
            });
            room_button.appendTo($("#avaiableRooms"));
        });
    });

    $('#start').click(function(){
        socket.emit("change_color", "red") 
    });

    $('#finish').click(function(){
        socket.emit("change_color", "yellow") 
    });
    
    $('#match').click(match_room)
    //$(document).on('click', '.enter_room', enter_room);

    function match_room(){
        socket.emit('join',{"room": "room", "username":"username"});
    };
})