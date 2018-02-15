(function(){
	'use strict';

	angular
		.module('app.controllers')
		.controller('experienceDetailCtrl', experienceDetailController)

	experienceDetailController.$inject = ["$scope", "$http"];

	function experienceDetailController($scope, $http){
		var that = this;
		that.likes = -1;
		that.dislikes = -1;
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
		that.extractCId = extractCId;
		that.loadAudios = loadAudios;
		that.addLike = addLike;
		that.addDislike = addDislike;
		that.removeLike = removeLike;
		that.removeDislike = removeDislike;
		that.updateLikes = updateLikes;

		(function(d, s, id) {
		  	var js, fjs = d.getElementsByTagName(s)[0];
		  	if (d.getElementById(id)) return;
		  	js = d.createElement(s); js.id = id;
		  	js.src = 'https://connect.facebook.net/es_LA/sdk.js#xfbml=1&version=v2.12';
		  	fjs.parentNode.insertBefore(js, fjs);
		}(document, 'script', 'facebook-jssdk'));

		that.like_no_like = 'no_like';
		that.like_like = 'like';
		that.like_dislike = 'dislike';
		that.likeStatus = '';

		function init(id, likes, dislikes, views, parentUrl, likeStatus){
			that.id = id;
			that.likes = likes;
			that.dislikes = dislikes;
			that.views = views;
			that.parentUrl = parentUrl;
			that.likeStatus = likeStatus;
			updateViews();
		}

		function vote(){

			if(that.likeStatus == that.like_no_like){
				that.addLike();
				that.likeStatus = that.like_like;
			}
			else if(that.likeStatus == that.like_like){
				that.removeLike();
				that.likeStatus = that.like_no_like;			
			}
			else if(that.likeStatus == that.like_dislike){				
				that.removeDislike(that.addLike);
				that.likeStatus = that.like_like;		
			}

		}

		function unvote(){

			if(that.likeStatus == that.like_no_like){
				that.addDislike();
				that.likeStatus = that.like_dislike;
			}
			else if(that.likeStatus == that.like_dislike){
				that.removeDislike();
				that.likeStatus = that.like_no_like;				
			}
			else if(that.likeStatus == that.like_like){				
				that.removeLike(that.addDislike);
				that.likeStatus = that.like_dislike;	
			}

		}

		function addLike(f){
			$http.get("/experiences/"+that.id+"/like").then(function successCallback(response){
				if(f)
					f();
				else
					that.updateLikes(response.data);
			}, function errorCallback(response){
				console.log("Error en likes");		
			});
		}

		function removeLike(f){
			$http.get("/experiences/"+that.id+"/removeLike").then(function successCallback(response){
				if(f)
					f();
				else
					that.updateLikes(response.data);
			}, function errorCallback(response){
				console.log("Error en likes");			
			});
		}

		function addDislike(f){
			$http.get("/experiences/"+that.id+"/dislike").then(function successCallback(response){
				if(f)
					f();
				else
					that.updateLikes(response.data);
			}, function errorCallback(response){
				console.log("Error en likes");			
			});
		}

		function removeDislike(f){
			$http.get("/experiences/"+that.id+"/removeDislike").then(function successCallback(response){
				if(f)
					f();
				else
					that.updateLikes(response.data);
			}, function errorCallback(response){
				console.log("Error en likes");			
			});
		}

		function updateLikes(data){
			that.likes = data.likes;
			that.dislikes = data.dislikes;
		}

		function updateViews(){

			$http.get("/experiences/"+that.id+"/view").then(function successCallback(response){
				that.views = response.data;
			}, function errorCallback(response){
				console.log("Error en Views");
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

		function extractCId(audio_url){

			let a_id = audio_url.split("d/")[1];
			a_id = a_id.split("/p")[0];		
			return a_id;			
			
		}	

		function loadAudios(){
			$("audio").load();
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
								window.location.replace(that.parentUrl);
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