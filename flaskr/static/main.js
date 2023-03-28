playing = true
$(document).ready(function(){
    
    $("#exit_room").hide();
    $("#start_game").hide();
    /**
     * function create when the user open the game page
     * It creates the socket for the communication
     */
    var socket = io() 
    socket.on('connect', function() {
        console.log("connected")
        socket.emit("startInfo")
    });
    
    
    /**
     * after testing delete this
     */
    socket.on("color", function(msg) {
        if(msg == "red"){
            console.log("test_red")
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
            var room_button = $('<input type="button" value=' + key + '"/>')
            .attr('class', 'enter_room')
            .attr('id', key)
            .click(f => {
                socket.emit('enter_existing_room',{"room": key, "username":"username"});
                $('#avaiableRooms').hide();
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
            var room_button = $('<input type="button" value=' + key + '"/>')
            .attr('class', 'enter_room')
            .attr('id', key)
            .click(f => {
                socket.emit('enter_existing_room', {"room": key, "username":"username"});
                $('#avaiableRooms').hide();
            });
            room_button.appendTo($("#avaiableRooms"));
        });
    });

    /**
     * function used to save the current room for the user
     */
    socket.on("send_current_room", function(data) {
        localStorage.setItem("current_room", data)
        $('#create_room').hide();
        $("#exit_room").show();
    });

    /**
     * when the first player start the game every user will generate the new page
     */
    socket.on("load_game_page", function(data) {
        $("body").load("/game_page/");
    });
    
    $('#start').click(function(){
        socket.emit("change_color", {"color":"red", "current_room": localStorage.getItem("current_room")}) 
    });

    $('#finish').click(function(){
        socket.emit("change_color", {"color":"yellow", "current_room": localStorage.getItem("current_room")}) 
    });
    
    /**
     * function called when we want to create a new room
     */
    $('#create_room').click(function(){
        socket.emit('join', {"room": "room", "username":"username"});
        $('#avaiableRooms').hide();
        $('#start_game').show();
    });

    /**
     * function called when the user want to exit the current room
     */
    $('#exit_room').click(function(){
        console.log("exit_room")
        socket.emit('leave_room', {"room": localStorage.getItem("current_room")}); 
        $('#create_room').show();
        $('#avaiableRooms').show();
        $("#exit_room").hide();
        $('#start_game').hide();
    });
    
    $("#start_game").click(function() {
        socket.emit("start_game", {"room": localStorage.getItem("current_room")})
    });


    /*function match_room(){
        socket.emit('join',{"room": "room", "username":"username"});
    };*/
})