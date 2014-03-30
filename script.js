var seconds = 1500;

$(document).ready(function(){
	
	$('#start').click(function() {
		start();
		$("#start").attr("disabled", "disabled");
		console.log("started!")
	});

	$('#stop').click(function() {
		stop();
		$("#start").removeAttr("disabled");
		console.log("stopped!")
	});
	
});
 
function start() {
	secondPassed();
	countdownTimer = setInterval('secondPassed()', 1000);
}

function stop() {
	clearInterval(countdownTimer);
}

function secondPassed() {
	  var minutes = Math.round((seconds - 30)/60),
	      remainingSeconds = seconds % 60;
	  
	  if (remainingSeconds < 10) {
	    remainingSeconds = "0" + remainingSeconds;  
	  }
	  
	  document.getElementById('countdown').innerHTML = minutes + ":" + remainingSeconds;
	  if (seconds == 0) {
	    clearInterval(countdownTimer);
	    document.getElementById('countdown').innerHTML = "00:00";
	  } else {
	    seconds--;
	  }
}

