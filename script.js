var seconds = 1500;

$(document).ready(function(){
	
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
	countdownTimer = setInterval('drawClock()', 1000);
}

function onStop() {
	clearInterval(countdownTimer);
}

function drawClock() {
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
