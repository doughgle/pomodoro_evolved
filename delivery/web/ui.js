
$(document).ready(function(){
	
	technique = new Technique(0.01, 0.01, 0.01); 
	technique.newTimer();
	
	$('#start').click(function() {
		onStart();
		$('#completedPomodoros').fadeOut();
	});

	$('#stop').click(function() {
		onStop();
	});
	
});



Technique = function(pomodoroDurationMins, shortBreakDurationMins, longBreakDurationMins) {
	this.pomodoroDurationMins = pomodoroDurationMins;
	this.shortBreakDurationMins = shortBreakDurationMins;
	this.longBreakDurationMins = longBreakDurationMins;
	this.completedPomodoros = 0;
};

Technique.prototype.newTimer = function(prevTimer) {

	timer = new Timer(whenTimeup, durationInMins=this.pomodoroDurationMins, name="Pomodoro");

    if(typeof prevTimer !== 'undefined') {
    	if(prevTimer.name === 'Pomodoro') {
    		this.completedPomodoros++;
    		if(this.completedPomodoros % 4 == 0) {
    			timer = new Timer(whenTimeup, this.longBreakDurationMins, name="Long Break");
    		}
    		else {
    			timer = new Timer(whenTimeup, this.shortBreakDurationMins, name="Short Break");    		
    		}
    	}
    }
    
    drawStatus();
    drawClock();
    drawCompleted(this.completedPomodoros);
};

function onStart() {
	drawClock();
	timer.start();
	showStopButton();
}

function showStopButton() {
	$('#start').hide();
	$('#start').siblings('button').show();
}

function onStop() {
	if(confirm("Void this " + timer.name + "?")) {
		clearInterval(countdownTimer);
		technique.newTimer();
		showStartButton();
	}
	else {
		
	}
}

function showStartButton() {
	$('#stop').hide();
	$('#stop').siblings('button').show();
}

function tick() {
	timer.tick();
	drawClock();
}

function whenTimeup() {
	alert("Time's up!");
	technique.newTimer(timer);
	showStartButton();
}

function toggleButton(button) {
	button.hide();
	button.siblings('button').show();	
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

function drawCompleted(completedPomodoros) {
	$('#completed').text(completedPomodoros);
	$("#completedPomodoros").fadeIn();
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
