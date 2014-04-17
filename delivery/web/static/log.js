Log = function() {
};

Log.prototype.addTimer = function(timer) {
	this.timer = timer;
};

Log.prototype.send = function() {
	$.post('log/timer', { timer: JSON.stringify(this.timer) });
};