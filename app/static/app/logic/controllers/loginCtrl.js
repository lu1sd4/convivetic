(function(){
	
	'use strict';
	
	angular
		.module('app.controllers')
		.controller('loginController', loginController);
	
	loginController.$inject = ["$scope"];
	
	function loginController($scope){
		
		var that = this;
		that.formSubmitted = false;

		that.sendForm = sendForm;

		function sendForm(){
			that.formSubmitted = true;
			if($scope.form.$valid)
				$("#form").submit();
		}

	}
	
})();