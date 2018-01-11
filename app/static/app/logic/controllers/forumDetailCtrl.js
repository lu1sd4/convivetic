(function(){
	angular
		.module('app.controllers')
		.controller('forumDetailController', forumDetailController)

	forumDetailController.$inject = ["$scope", "$http"];

	function forumDetailController($scope, $http){
		var that = this;
		that.id = -1;

		that.vote = vote;

		function vote(){

		}

		
		$http.get("/forums/")





		
	}


})();