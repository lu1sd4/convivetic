(function(){
	
	'use strict';
	
	angular
		.module('app.controllers')
		.controller('signupController', signupController);
	
	signupController.$inject = ["$scope"];
	
	function signupController($scope){
		
		var that = this;

		that.pageOne = 1;		 
		that.pageTwo = 2;
		that.pageThree = 3;

		that.state = that.pageOne;
		that.isNext = true;
		that.isPrevious = false;

		that.nextPart = nextPart;
		that.previousPart = previousPart;
		that.changeState = changeState;

		function nextPart(){
			that.changeState(1);			
		}
		
		function previousPart(){
			that.changeState(-1);
		}

		function changeState(change){
			that.state += change;
			that.isPrevious = that.state > that.pageOne;
			that.isNext = that.state < that.pageThree;
			that.isLast = that.state == that.pageThree;
		}


		$('select').extendSelect({
			notSelectedTitle : 'Seleccione'
		});

	}
	
})();