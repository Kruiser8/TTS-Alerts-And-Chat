/*
 This overlay was made  by Kruiser8 (https://twitch.tv/kruiser8)
      and is licensed under the Creative Commmons Attribution 4.0 International License (CC BY 4.0)

      For License information, visit https://creativecommons.org/licenses/by/4.0/
*/

function animateIn(selector, animationIn) {
  var animationEnd = 'webkitAnimationEnd mozAnimationEnd MSAnimationEnd oanimationend animationend';
  $( selector ).css("visibility","visible");
  $( selector ).addClass('animated ' + animationIn).on(animationEnd, function() {
    $( selector ).css("visibility","visible");
    $( selector ).removeClass('animated ' + animationIn);
  });
}
function animateOut(selector, animationOut) {
  var animationEnd = 'webkitAnimationEnd mozAnimationEnd MSAnimationEnd oanimationend animationend';
  $( selector).addClass('animated ' + animationOut).on(animationEnd, function() {
    $( selector ).css("visibility","hidden");
    $( selector ).removeClass('animated ' + animationOut);
  });
}

var animationQueue = async.queue(async function (data, callback) {
  $('.overlay').css({
    'background': data.useBackground ? data.background : 'transparent',
    'border-color': data.useBorder ? data.border : 'transparent',
    'border-style': data.useBorder ? 'solid' : 'none',
    'color': data.fontColor,
    'font-size': data.fontSize,
    'font-family': data.font ? data.font : 'Courier New'
  })
  $('#message').text(data.message);
  animateIn('.overlay', data.animateIn);
  await timeout(1000 + data.time * 1000);
  animateOut('.overlay', data.animateOut);
  await timeout(1100);
}, 1);

function timeout(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
}

// Do stuff if the document is fully loaded
$(document).ready(function() {
	// Show an error message if the API key file is not loaded
	if (typeof API_Key === "undefined") {
		$("body").html("No API Key found or load!<br>Right-click on the script in Streamlabs and select \"Insert API Key\"");
		$("body").css({"font-size": "20px", "color": "#ff8080", "text-align": "center"});
	}
	// Connect to the Streamlabs Chatbot websocket
	else {
		connectWebsocket();
	}
});

// Function to connect and authenticate to the Streamlabs Chatbot webosocket
// Automatically tries to reconnect after connection has been closed
// Handles received registered websocket events from Streamlabs Chatbot
function connectWebsocket() {
	// Create the websocket connection
	var socket = new WebSocket(API_Socket);

	// WS OnOpen event : authenticate
	socket.onopen = function() {
		// Create authentication payload and request required events
		var auth = {
			author: "Kruiser8",
			website: "http://www.twitch.tv/kruiser8",
			api_key: API_Key,
			events: [
				"EVENT_TTS_AC_OVERLAY"
			]
		};
		// Send authentication payload to Streamlabs Chatbot
		socket.send(JSON.stringify(auth));
	};

	// Ws OnClose : try reconnect
	socket.onclose = function() {
		socket = null;
		setTimeout(connectWebsocket, 5000);
	};

	// WS OnMessage event : handle events
	socket.onmessage = function (message) {
		// Parse message data to extract event name
		var socketMessage = JSON.parse(message.data);
    console.log(socketMessage);

		// EVENT_TTS_AC_OVERLAY
		if (socketMessage.event == "EVENT_TTS_AC_OVERLAY") {
			var eventData = JSON.parse(socketMessage.data);
      animationQueue.push(eventData);
		}
	};
};
