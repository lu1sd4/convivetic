(function(){
	
	'use strict';
	
	angular
		.module('app.controllers')
		.controller('signupController', signupController);
	
	signupController.$inject = ["$scope"];
	
	function signupController($scope){
		
		var that = this;

		that.pageOne = 1;
		that.pageOneSubmitted = false; 
		that.pageTwo = 2;
		that.pageTwoSubmitted = false; 
		that.pageThree = 3;

		that.state = 2;
		that.isPrevious = false;
		that.isLast = false;
		that.nextText = 'Siguiente';

		that.nextPart = nextPart;
		that.previousPart = previousPart;
		that.changeState = changeState;

		$scope.is_conflict_participant = 'False';
		$scope.is_conflict_victim = 'False';
		$scope.is_living_in_conflict_zone = 'False';

		function nextPart(){
			if(that.state == that.pageOne){
				that.pageOneSubmitted = true;
				if($scope.partOneForm.$valid)
					that.changeState(1);				
			} else if(that.state == that.pageTwo){
				that.pageTwoSubmitted = true;
				if($scope.partTwoForm.$valid)
					that.changeState(1);
			} else if(that.state == that.pageThree){
				that.pageThreeSubmitted = true;
				if($scope.partThreeForm.$valid)
					document.getElementById('userRegistrationForm').submit()
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

		$("select").extendSelect();

	}
	
})();