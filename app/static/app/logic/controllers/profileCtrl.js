(function(){

	angular
		.module('app.controllers')
		.controller('profileController', profileController)

	profileController.$inject = ["$scope", "$http"]

	function profileController($scope, $http){

		var that = this;
		that.sectionOne = 1;
		that.sectionTwo = 2;
		that.sectionThree = 3;
		that.sectionNames = ['Personal', 'Contacto', 'Conflicto'];

		that.currentSection = that.sectionOne;
		that.sectionName = that.sectionNames[that.currentSection-1]

		that.changeState = changeState;

		function changeState(p){
			switch(p){
				case 1:
					that.currentSection = that.sectionOne;
					break
				case 2:
					that.currentSection = that.sectionTwo;
					break
				case 3:
					that.currentSection = that.sectionThree;
					break
				default:
					that.currentSection = that.sectionOne;
					break
			}

			that.sectionName = that.sectionNames[that.currentSection-1]

		}


	}

})();