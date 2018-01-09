(function(){

	'use strict';

	angular
		.module('app.controllers')
		.controller('homeController', homeController);

	homeController.$inject = ["$scope"];

	function homeController($scope){
		var that = this;

		that.mMenuIsActive = false;
		that.getMobileMenu = getMobileMenu;

		function getMobileMenu(){
			that.mMenuIsActive = !that.mMenuIsActive;

			//$(".menu-list").css("max-height:720px !important");
		}

	}

})();