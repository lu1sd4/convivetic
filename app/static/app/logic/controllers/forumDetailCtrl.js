(function(){

	'use strict';

	angular
		.module('app.controllers')
		.controller('forumDetailController', forumDetailController)

	forumDetailController.$inject = ["$scope", "$http"];

	function forumDetailController($scope, $http){
		var that = this;
		that.id = -1;
		that.likes = -1;
		that.views = -1;
		that.commentContent = "";

		that.init = init;
		that.vote = vote;
		that.unvote = unvote;
		that.comment = comment;


		function init(id, likes, dislikes, views){
			that.id = id;
			that.likes = likes - dislikes;
			that.views = views;

			updateViews();
		}

		function vote(){

			$(".social-btns").remove()

			$http.get("/forums/"+that.id+"/vote").then(function successCallback(response){
				if(parseInt(response.data) != NaN){
					that.likes = response.data;
				}
				
			}, function errorCallback(response){

				console.log("Error en likes");
			
			});

		}

		function unvote(){

			$(".social-btns").remove()

			$http.get("/forums/"+that.id+"/unvote").then(function successCallback(response){

				if(parseInt(response.data) != NaN){
					that.likes = response.data;
				}

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


		function comment(){
			$http.get("/forums/"+that.id+"/comment/"+that.commentContent).then(function successCallback(response){
				console.log(response);

			}, function errorCallback(){

				console.log(response);
			});
		}


	}


})();