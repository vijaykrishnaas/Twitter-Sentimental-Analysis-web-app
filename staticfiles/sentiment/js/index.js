function preloader() {
    var styles = {
        "display": "block",
        "width": "100%",
        "height": "100%",
        "margin": "auto",
        "position": "absolute",
        "top": "35%",
        "text-align": "center"
    }
    document.getElementById("content").style.display = "none";
    document.getElementById("navigation").style.display = "none";
    document.documentElement.style.overflowY = "hidden";
    document.body.style.overflowY = "hidden";
    document.body.style.backgroundColor = "#f7f7f7";
    var obj = document.getElementById("loading");
    Object.assign(obj.style, styles);
}

function validateInput() {
    var query = $('#searchQuery').val();
    if (query) {
        $('#requiredMsg').hide();
        preloader();
        return true;
    } else {
        $('#requiredMsg').fadeIn();
        $('#searchQuery').focus();
        return false;
    }
}

function loadOnScreen(data) {
    var completePercentage = data.step * 20;
    $('#statusMsg').html(data.statusMsg + " ( " + completePercentage + "% )");
    $('#steps').css('width', completePercentage + '%');
    $('#steps').attr('aria-valuenow', data.step);
    $('#steps').attr('aria-valuemax', data.total);
}


// Socket Connection Handling 
var ws_scheme = window.location.protocol == "https:" ? "wss" : "ws";
var socketURL = ws_scheme + '://' + window.location.host + '/ws/connect/';
var socket = new ReconnectingWebSocket(socketURL);

// Show a connected message when the WebSocket is opened.
socket.onopen = function (event) {
    console.log('WebSocket Connected to' + socketURL);
};

// Handle messages sent by the server.
socket.onmessage = function (event) {
    var data = JSON.parse(event.data);
    loadOnScreen(data);
};

// Handle any errors that occur.
socket.onerror = function (error) {
    console.log('WebSocket Error: ' + error);
};

// Show a disconnected message when the WebSocket is closed.
socket.onclose = function (event) {
    console.error('WebSocket Closed Unexpectedly');
};