(function(){

	'use strict';

	angular
		.module('app.controllers')
		.controller('forumDetailController', forumDetailController)

	forumDetailController.$inject = ["$scope", "$http"];

	function forumDetailController($scope, $http){
		var that = this;

		that.accessToken = '';
		that.apiKey = '';
		that.publishClicked = false;
		that.isUploading = false;
		that.fileMissingError = false;
		that.videoTypes = ['video/x-msvideo', 'video/mpeg', 'video/ogg', 'video/webm', 'video/3gpp', 'video/3gpp2', 'video/H264', 'video/mp4', 'video/quicktime']
		that.audioTypes = ['audio/mpeg', 'audio/mp3', 'audio/wav', 'audio/flac', 'audio/ogg', 'audio/webm']
		that.imgTypes = ['image/png', 'image/gif', 'image/png', 'image/jpeg', 'image/bmp', 'image/webp']
		that.uploadStartTime = 0;
		that.videoId = '';
		that.audioUrl
		that.uploadComplete = false;
		that.status_polling_interval = 10 * 1000;
		that.folderId = "1PXtw_L0urVh8VdToKUthWT-FiR4ZsKZl";

		that.id = -1;
		that.likes = -1;
		that.views = -1;
		that.commentContent = "";

		that.option_text = 1
		that.option_video = 2
		that.option_audio = 3
		that.option_img = 4

		that.mediaOption = that.option_text;

		that.init = init;
		that.vote = vote;
		that.unvote = unvote;
		that.comment = comment;
		that.setMediaOption = setMediaOption;
		that.showFileError = showFileError;
		that.disableInputs = disableInputs;
		that.hideFileError = hideFileError;
		that.postVideo = postVideo;
		that.postAudio = postAudio;
		that.postImg = postImg;
		that.uploadVideo = uploadVideo;
		that.uploadAudio = uploadAudio;
		that.pollForVideoStatus = pollForVideoStatus;
		that.saveVideoPost = saveVideoPost;
		that.saveAudioPost = saveAudioPost;
		that.disableInputs = disableInputs;
		that.successToast = successToast;
		that.extractId = extractId;

		that.commentClicked = false;
		that.audio_id = "";


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

		// Tipo de archivo
		function setMediaOption(newOption){
			that.hideFileError();
			that.mediaOption = newOption;
		}

		// Click en publicar discusión
		function comment(){
			that.commentClicked = true;
			var file = $("#mediaFile").get(0);
			switch(that.mediaOption){
				case that.option_video:
					if(file.files[0]){
						file = file.files[0];
						var fileType = file['type'];
						if(that.videoTypes.indexOf(fileType) < 0){
							that.showFileError();
						} else {
							that.fileMissingError = false;			
							if($scope.form.$valid)
							    that.postVideo(file);
						}
					} else {
						that.showFileError();
					}
					break;
				case that.option_audio:
					if(file.files[0]){
						file = file.files[0];
						var fileType = file['type'];
						if(that.audioTypes.indexOf(fileType) < 0){
							that.showFileError();
						} else {
							that.fileMissingError = false;
							if($scope.form.$valid)
							    that.postAudio(file);								
						}
					} else {
						that.showFileError();
					}
					break;
				case that.option_img:
					file = $("#id_img").get(0);
					if(file.files[0]){
						file = file.files[0];
						var fileType = file['type'];
						if(that.imgTypes.indexOf(fileType) < 0){							
							that.showFileError();
						} else {
							that.fileMissingError = false;
							if($scope.form.$valid)
							    that.postImg(file);						
						}
					} else {
						that.showFileError();
					}
					break;
				default:
					if($scope.form.$valid)
						$("#form").submit();
					break;
				}
		}

		function showFileError(){
			that.fileMissingError = true;
			$(".bootstrap-filestyle .form-control").addClass("ng-invalid");
			$(".bootstrap-filestyle .btn").addClass("ng-invalid");
		}

		function hideFileError(){
			that.commentClicked = false;
			that.fileMissingError = false;
			$(".bootstrap-filestyle .form-control").removeClass("ng-invalid");
			$(".bootstrap-filestyle .btn").removeClass("ng-invalid");	
		}

		function disableInputs(){
			$(".bootstrap-filestyle .form-control").removeClass("ng-invalid");
			$(".bootstrap-filestyle .btn").removeClass("ng-invalid");
			$(".btn-outline-primary").addClass("disabled");
			$(".group-span-filestyle .btn").addClass("disabled");
			$("textarea").prop("readonly", "true");
		}

		// Todo bien para subir el audio
		function postAudio(file){
			that.isUploading = true;
			that.disableInputs();
			
			$.ajax({
		    	type: 'POST',
		    	url: '../../youtube_token',
		    	success : function(data){
		    		console.log("success")		    		
		    		that.accessToken = data.token;			    		
		    		that.uploadAudio(file);								    		
		    	},
		    	error : function(data){
		    		console.log('error');
		    		console.log(data);
		    	}
		    });
		    //*/
		}

		// Todo bien para subir el video
		function postVideo(file){
			that.isUploading = true;
			that.disableInputs();
			
			$.ajax({
		    	type: 'POST',
		    	url: '../../youtube_token',
		    	success : function(data){
		    		console.log("success")								    		
		    		that.accessToken = data.token;
		    		that.apiKey = data.apiKey;
		    		that.uploadVideo(file);							    		
		    	},
		    	error : function(data){
		    		console.log('error');
		    		console.log(data);
		    	}
		    });
		    //*/
		}

		// Imagen
		function postImg(file){
			$("#mediaFile").val('');				
			$("#form").submit();
		}

		function uploadAudio(file){

			var metadata = {
				'title': file.name,
				'description': "Archivo convivetic",
				'mimeType': file.type || 'application/octet-stream',
				"parents": [{
					"kind": "drive#file",
					"id": that.folderId
				}]
			};

			var uploader =new MediaUploader({
				file: file,
				token: that.accessToken,
				metadata: metadata,
				onError: function(response){
					var message = data;
			    	// Assuming the error is raised by the YouTube API, data will be
			    	// a JSON string with error.message set. That may not be the
			    	// only time onError will be raised, though.
			    	try {
			    		var errorResponse = JSON.parse(data);
			    		message = errorResponse.error.message;
			    	} finally {
			    		alert(message);
			    	}
				},
				onComplete: function(data){

					var uploadResponse = JSON.parse(data);
					if(uploadResponse.message != null){
						console.log("Error: " + errorResponse.error.message);
					}else{
						that.audioUrl = uploadResponse.embedLink;
						that.uploadComplete = true;
						$scope.$apply();							
						$('#upload-status').html("Completado");
						$('#player').html("<iframe frameborder='0' width='350' height='150' src='"+that.audioUrl+"'></iframe>")
						that.saveAudioPost();
					}
				},
				onProgress: function(data) {

					var currentTime = Date.now();
				  	var bytesUploaded = data.loaded;
				  	var totalBytes = data.total;

					var percentageComplete = (bytesUploaded * 100) / totalBytes;

					$('#upload-progress').attr({
						value: bytesUploaded,
						max: totalBytes
					});

					$('#percent-transferred').text(percentageComplete.toFixed(2)+"%");
				},
				params: {
					convert:false,
					ocr: false
				}
			});
			uploader.upload();

		}

		function uploadVideo(file){
			var metadata = {
				snippet: {
					title: $('#id_content').val().substring(0, 40),
					description: $('#id_content').val(),
					tags: ['convivetic', 'conflicto', 'colombia', 'samaná'],
					categoryId: 22
				},
				status: {
					privacyStatus: 'public'
				}
			};

			var uploader = new MediaUploader({
				baseUrl: 'https://www.googleapis.com/upload/youtube/v3/videos',
				file: file,
				token: that.accessToken,
				metadata: metadata,
				params: {
					part: Object.keys(metadata).join(',')
				},
				onError: function(data) {
					var message = data;
			    	// Assuming the error is raised by the YouTube API, data will be
			    	// a JSON string with error.message set. That may not be the
			    	// only time onError will be raised, though.
			    	try {
			    		var errorResponse = JSON.parse(data);
			    		message = errorResponse.error.message;
			    	} finally {
			    		alert(message);
			    	}
				}.bind(this),
				onProgress: function(data) {
				  	var currentTime = Date.now();
				  	var bytesUploaded = data.loaded;
				  	var totalBytes = data.total;
					// The times are in millis, so we need to divide by 1000 to get seconds.
					var bytesPerSecond = bytesUploaded / ((currentTime - that.uploadStartTime) / 1000);
					var estimatedSecondsRemaining = (totalBytes - bytesUploaded) / bytesPerSecond;
					var percentageComplete = (bytesUploaded * 100) / totalBytes;

					$('#upload-progress').attr({
						value: bytesUploaded,
						max: totalBytes
					});

					$('#percent-transferred').text(percentageComplete.toFixed(2)+"%");
				}.bind(this),
				onComplete: function(data) {
					var uploadResponse = JSON.parse(data);
					that.videoId = uploadResponse.id;
					that.uploadComplete = true;
					$scope.$apply();
					$("#upload-progress").attr({value: ''});
					that.pollForVideoStatus();
				}.bind(this)
			});
			// This won't correspond to the *exact* start of the upload, but it should be close enough.
			that.uploadStartTime = Date.now();
			uploader.upload();
		}

		function pollForVideoStatus(){
			$.ajax({
				type : 'GET',
				url : 'https://www.googleapis.com/youtube/v3/videos',
				data : {
					id : that.videoId,
					part : 'status,player',
					key : that.apiKey
				},
				success : function(response){
					var uploadStatus = response.items[0].status.uploadStatus;
					switch (uploadStatus) {
						// This is a non-final status, so we need to poll again.
						case 'uploaded':
							setTimeout(that.pollForVideoStatus.bind(this), that.status_polling_interval);
							break;
						// The video was successfully transcoded and is available.
						case 'processed':
							$('#upload-status').html("Completado");
							$('#player').append(response.items[0].player.embedHtml);
							that.saveVideoPost();
							break;
							// All other statuses indicate a permanent transcoding failure.
						default:
							$('#upload-status').html('Algo salió mal, vuelve a intentarlo');
							break;
					}
				}.bind(this),
				error : function(response){
					console.log(response.error.message)
					setTimeout(that.pollForVideoStatus.bind(this), that.status_polling_interval);
				}.bind(this)
			})
		}

		function saveVideoPost(){
			$("#id_img_url").val('');
			$("#id_video_url").val(that.videoId);
			$("#form").submit();
		}

		function saveAudioPost(){
			$("#id_img_url").val('');
			$("#id_audio_url").val(that.audioUrl);
			$("#form").submit();
		}

		function successToast(message){
			swal(message, {
				icon: "success"
			})
		}

		function extractId(audio_url){

			let a_id = audio_url.split("d/")[1];
			a_id = a_id.split("/p")[0];
			that.audio_id = a_id;
			$("audio").load();
			
		}

	}


})();