$(document).ready(function(){
	
	newTimer();
	
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

function newTimer(prevTimer) {

	timer = new Timer(whenTimeup, durationInMins=0.03, name="Pomodoro");

    if(typeof prevTimer !== 'undefined') {
    	if(prevTimer.name === 'Pomodoro') {
    		timer = new Timer(whenTimeup, durationInMins=0.01, name="Short Break");    		
    	}
    }
    
    drawClock();
    drawStatus();
}

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
	newTimer(timer);
	$("#start").removeAttr("disabled");
}

function drawStatus() {
	$('#timerName').text(timer.name);
}

function drawClock() {
	  var seconds = timer.durationInSeconds;
	  var minutes = Math.round((seconds - 30)/60);
	  if(minutes < 10) {
		  minutes = "0" + minutes;  
	  }
	  var remainingSeconds = Math.ceil(seconds % 60);
	  if(remainingSeconds < 10) {
	    remainingSeconds = "0" + remainingSeconds;  
	  }
	  document.getElementById('countdown').innerHTML = minutes + ":" + remainingSeconds;

	  if (seconds <= 0) {
	    document.getElementById('countdown').innerHTML = "00:00";
	  }
}

Timer = function(whenTimeup, durationInMins, name) {
	this.whenTimeup = whenTimeup;
	this.durationInSeconds = durationInMins * 60;
	this.name = name;
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
