(function(){
	
	'use strict';
	
	angular
		.module('app.controllers')
		.controller('passwordResetConfirmController', passwordResetConfirmController);
	
	passwordResetConfirmController.$inject = ["$scope"];
	
	function passwordResetConfirmController($scope){
		
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