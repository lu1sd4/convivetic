(function(){
	angular
		.module('app.controllers')
		.controller('forumDetailController', forumDetailController)

	forumDetailController.$inject = ["$scope", "$http"];

	function forumDetailController($scope, $http){
		var that = this;
		that.id = -1;
		that.likes = -1;
		that.views = -1;

		that.init = init;
		that.vote = vote;
		that.unvote = unvote;


		function init(id, likes, views){
			that.id = id;
			that.likes = likes;
			that.views = views;

			updateViews();
		}

		function vote(){
			
			$http.get("/forums/"+that.id+"/vote").then(function successCallback(response){
				that.likes = response.data;
				
			}, function errorCallback(response){

				console.log("Error en likes");
			
			});

		}

		function unvote(){

			$http.get("/forums/"+that.id+"/unvote").then(function successCallback(response){
				that.likes = response.data;

			}, function errorCallback(response){
				console.log("Error en dislikes");
			});

		}

		function updateViews(){

			$http.get("/forums/"+that.id+"/view").then(function successCallback(response){
				that.views = response.data;

			}, function errorCallback(response){
				console.log("Error en Views");
			});
		}


	}


})();