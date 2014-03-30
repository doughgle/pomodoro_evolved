var seconds = 1;

$(document).ready(function(){
	
	timer = new Timer(whenTimeup, durationInMins=0.03);
	drawClock();
	
	$('#start').click(function() {
		onStart();
		$("#start").attr("disabled", "disabled");
		console.log("started!")
	});

	$('#stop').click(function() {
		onStop();
		$("#start").removeAttr("disabled");
		console.log("stopped!")
	});
	
});
 
function onStart() {
	drawClock();
	timer.start();
}

function onStop() {
	clearInterval(countdownTimer);
}

function tick() {
	timer.tick();
	drawClock();
}

function whenTimeup() {
	alert("Time's up!");
}

function drawClock() {
	  var seconds = timer.durationInSeconds;
	  var minutes = Math.round((seconds - 30)/60);
	  var remainingSeconds = Math.ceil(seconds % 60);
	  if (remainingSeconds < 10) {
	    remainingSeconds = "0" + remainingSeconds;  
	  }
	  document.getElementById('countdown').innerHTML = minutes + ":" + remainingSeconds;

	  if (seconds <= 0) {
	    document.getElementById('countdown').innerHTML = "00:00";
	  }
}

Timer = function(whenTimeup, durationInMins) {
	this.whenTimeup = whenTimeup;
	this.durationInSeconds = durationInMins * 60;
};

Timer.prototype.start = function() {
	countdownTimer = setInterval('tick()', 1000);
};

Timer.prototype.tick = function() {
	if(this.durationInSeconds <= 0) {
		clearInterval(countdownTimer);
		this.whenTimeup();
	}
	else this.durationInSeconds--;
};

