$(function(){
	var FOLDER_ID = "1PXtw_L0urVh8VdToKUthWT-FiR4ZsKZl";	

	$("#uploadBtn").click(function(){
		$.ajax({
	    	type: 'POST',
	    	url: 'youtube_token',
	    	success : function(data){
	    		console.log("success")					    		
	    		accessToken = data.token;
	    		uploadFile(accessToken);
	    		// var uploadVideo = new UploadVideo();
	    		// uploadVideo.ready(data.token, data.apiKey);  								    		
	    	},
	    	error : function(data){
	    		console.log('error');
	    		console.log(data);
	    	}
	    });
	})

	function uploadFile(accessToken){

		var file = $("#fileUpload").get(0).files[0];

		var metadata = {
			'title': file.name,
			'description': "Archivo convivetic",
			'mimeType': file.type || 'application/octet-stream',
			"parents": [{
				"kind": "drive#file",
				"id": FOLDER_ID
			}]
		};

		var arrayBufferView = new Uint8Array(file);
		var uploadData = new Blob(arrayBufferView, {type: file.type || 'application/octet-stream'});

		try{
			var uploader =new MediaUploader({
				file: file,
				token: accessToken,
				metadata: metadata,
				onError: function(response){
					var errorResponse = JSON.parse(response);
					console.log("Error: " + errorResponse.error.message);
					$("#status").html("Error")
					$("#fUpload").val("");
				},
				onComplete: function(response){
					var errorResponse = JSON.parse(response);
					if(errorResponse.message != null){
						$("#status").html("Error");
						console.log("Error: " + errorResponse.error.message);
						$("#fUpload").val("");
					}else{
						$("#status").html("Completado");
						response = JSON.parse(response)
						$("#result").html("<iframe frameborder='0' width='300' height='150' src='"+response.embedLink+"'></iframe>")
					}
				},
				onProgress: function(event) {
					$("#upload-progress").attr({
						value : event.loaded,
						max :event.total
					})
				},
				params: {
					convert:false,
					ocr: false
				}
			});
			uploader.upload();
		}catch(exc){
			console.log(exc);
			$("#status").html("Error");
			$("#fUpload").val("");
		}
	}

	

});