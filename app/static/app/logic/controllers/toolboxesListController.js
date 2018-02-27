(function(){

	'use strict';

	angular
		.module('app.controllers')
		.controller('toolboxesListController', toolboxesListController);

	toolboxesListController.$inject = ["$scope", "$http"];

	function toolboxesListController($scope, $http){
		
		var that = this;

		that.PENDING_TAB = 1;
		that.COMMENTED_TAB = 2;

		that.current_tab = that.PENDING_TAB;
		
		that.switchTab = switchTab;

		function switchTab(newTab){
			that.current_tab = newTab;
		}

	}

})();