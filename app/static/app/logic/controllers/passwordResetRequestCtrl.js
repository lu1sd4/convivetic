(function(){
	
	'use strict';
	
	angular
		.module('app.controllers')
		.controller('passwordResetRequestController', passwordResetRequestController);
	
	passwordResetRequestController.$inject = ["$scope"];
	
	function passwordResetRequestController($scope){
		
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