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

		that.submitClicked = false;

		that.changeState = changeState;
		that.submitClick = submitClick;
		that.successToast = successToast;

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

		function submitClick(){
			that.submitClicked = true;
			if(!$scope.formOne.$valid)
				that.changeState(1);
			else if(!$scope.formTwo.$valid)
				that.changeState(2);			
			if($scope.form.$valid)
				$("#form").submit();
		}
		
		function successToast(message){
			swal(message, {
				icon: "success"
			})
		}

	}

})();