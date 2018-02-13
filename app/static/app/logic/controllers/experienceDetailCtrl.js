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
		that.admurl = '/experiences/modify';
		that.url = window.location.href;

		that.vote = vote;
		that.unvote = unvote;
		that.init = init;
		that.updateViews = updateViews;
		that.modify = modify;
		that.successToast = successToast;
		that.warningToast = warningToast;
		that.deleteExperience = deleteExperience;

		(function(d, s, id) {
		  	var js, fjs = d.getElementsByTagName(s)[0];
		  	if (d.getElementById(id)) return;
		  	js = d.createElement(s); js.id = id;
		  	js.src = 'https://connect.facebook.net/es_LA/sdk.js#xfbml=1&version=v2.12';
		  	fjs.parentNode.insertBefore(js, fjs);
		}(document, 'script', 'facebook-jssdk'));

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

		function modify(type){
			console.log("here");
			var csrf = Cookies.get('csrftoken');			
			var data = { 'action' : type, 'pk' : that.id };
			$http.post(that.admurl, data, { "X-CSRFToken" : csrf }).then(function(){
				location.reload();
			});
		}

		function successToast(message){
			swal(message, {
				icon: "success"
			})
		}

		function warningToast(message){
			swal(message, {
				icon: "warning"
			})
		}		

		function deleteExperience(){
			swal({
				title: "Estás seguro?",
				text: "Si borras tu experiencia, desaparecerá de ConviveTIC",
				icon: "warning",
				buttons: ['Cancelar', 'Borrar'],
				dangerMode: true,
			})
			.then((willDelete) => {
				if (willDelete) {
					var data = {'pk' : that.id};
					$http.post("/experiences/api/delete_experience", data).then(function(response) {
							swal("Se ha borrado la experiencia", {
								icon: "success"
							}).then(function(){
								location.reload();
							});	
						},function(response){
							if(response.data.error){
								swal({
									title: "Error al borrar la experiencia",
									text: response.data.message,
									icon : "error"
								});
							}
						}
				    );
				}
			});
		}

	}

	

})();