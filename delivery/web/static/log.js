Log = function() {
};

Log.prototype.addTimer = function(timer) {
	this.timer = timer;
};

Log.prototype.send = function() {
	$.post('log/timer', { log: JSON.stringify({timer: this.timer}) });
};