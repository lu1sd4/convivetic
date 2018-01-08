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
		that.isPrevious = false;
		that.isLast = false;
		that.nextText = 'Siguiente';

		that.nextPart = nextPart;
		that.previousPart = previousPart;
		that.changeState = changeState;

		function nextPart(){
			if(that.state < that.pageThree){
				if($scope.partOneForm.$valid){
					alert("valid");
					that.changeState(1);		
				} else {
					alert("wdf")
				}
			}
		}
		
		function previousPart(){
			that.changeState(-1);
		}

		function changeState(change){			
			that.state += change;		
			that.isPrevious = that.state > that.pageOne;
			if(that.state == that.pageThree){
				that.isLast = true;
				that.nextText = 'Guardar';
			}
			else{
				that.isLast = false;
				that.nextText = 'Siguiente';
			}
		}


		$('select').extendSelect({
			notSelectedTitle : 'Seleccione'
		});

	}
	
})();