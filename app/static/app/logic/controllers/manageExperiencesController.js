(function(){

	'use strict';

	angular
		.module('app.controllers')
		.controller('manageExperiencesController', manageExperiencesController);

	manageExperiencesController.$inject = ["$scope", "$http"];

	function manageExperiencesController($scope, $http){
		
		var that = this;

		that.pending_tab = 1;
		that.approved_tab = 2;
		that.rejected_tab = 3;

		that.current_tab = that.pending_tab;
		
		that.switchTab = switchTab;

		function switchTab(newTab){
			that.current_tab = newTab;
		}

	}

})();