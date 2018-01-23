(function(){
	'use strict';

	angular
		.module('app.controllers')
		.controller('experienceDetailCtrl', experienceDetailController)

	experienceDetailController.$inject = ["$scope", "$http"];

	function experienceDetailController($scope, $http){
		var that = this;
		that.likes = -1;
		that.views = -1;
		that.id = -1;

		that.vote = vote;
		that.unvote = unvote;
		that.init = init;
		that.updateViews = updateViews;

		function init(id, likes, dislikes, views){
			that.id = id;
			that.likes = likes - dislikes;
			that.views = views;

			updateViews();
		}

		function updateViews(){

			$http.get("/experiences/"+that.id+"/view").then(function successCallback(response){
				that.views = response.data;

			}, function errorCallback(response){
				console.log("Error en Views");
			});
		}

		function vote(){

			$(".social-btns").remove()

			$http.get("/experiences/"+that.id+"/vote").then(function successCallback(response){
				if(parseInt(response.data) != NaN){
					that.likes = response.data;
				}
				
			}, function errorCallback(response){

				console.log("Error en likes");
			
			});

		}

		function unvote(){

			$(".social-btns").remove()

			$http.get("/experiences/"+that.id+"/unvote").then(function successCallback(response){

				if(parseInt(response.data) != NaN){
					that.likes = response.data;
				}

			}, function errorCallback(response){
				console.log("Error en dislikes");
			});

		}


	}

	

})();