(function(){

	'use strict';

	angular
		.module('app.controllers')
		.controller('indexController', indexController);

	indexController.$inject = ["$scope", "$http"];

	function indexController($scope, $http){
		var that = this;

		that.successToast = successToast;

		function successToast(message){
			swal(message, {
				icon: "success"
			})
		}

	}

})();