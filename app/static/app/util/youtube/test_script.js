var STATUS_POLLING_INTERVAL_MILLIS = 20 * 1000; // One minute.

/**
 * YouTube video uploader class
 *
 * @constructor
 */
var UploadVideo = function() {
  /**
   * The array of tags for the new YouTube video.
   *
   * @attribute tags
   * @type Array.<string>
   * @default ['google-cors-upload']
   */
  this.tags = ['youtube-cors-upload'];

  /**
   * The numeric YouTube
   * [category id](https://developers.google.com/apis-explorer/#p/youtube/v3/youtube.videoCategories.list?part=snippet&regionCode=us).
   *
   * @attribute categoryId
   * @type number
   * @default 22
   */
  this.categoryId = 22;

  /**
   * The id of the new video.
   *
   * @attribute videoId
   * @type string
   * @default ''
   */
  this.videoId = '';

  this.uploadStartTime = 0;
};


UploadVideo.prototype.ready = function(accessToken, apiKey) {
  this.accessToken = accessToken;
  this.apiKey = apiKey;
  this.authenticated = true;
  $('#button').on("click", this.handleUploadClicked.bind(this));
};

/**
 * Uploads a video file to YouTube.
 *
 * @method uploadFile
 * @param {object} file File object corresponding to the video to upload.
 */
UploadVideo.prototype.uploadFile = function(file) {
  var metadata = {
    snippet: {
      title: $('#title').val(),
      description: $('#description').text(),
      tags: this.tags,
      categoryId: this.categoryId
    },
    status: {
      privacyStatus: $('#privacy-status option:selected').text()
    }
  };
  var uploader = new MediaUploader({
    baseUrl: 'https://www.googleapis.com/upload/youtube/v3/videos',
    file: file,
    token: this.accessToken,
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
      var bytesPerSecond = bytesUploaded / ((currentTime - this.uploadStartTime) / 1000);
      var estimatedSecondsRemaining = (totalBytes - bytesUploaded) / bytesPerSecond;
      var percentageComplete = (bytesUploaded * 100) / totalBytes;

      $('#upload-progress').attr({
        value: bytesUploaded,
        max: totalBytes
      });

      $('#percent-transferred').text(percentageComplete);
      $('#bytes-transferred').text(bytesUploaded);
      $('#total-bytes').text(totalBytes);

      $('.during-upload').show();
    }.bind(this),
    onComplete: function(data) {
      var uploadResponse = JSON.parse(data);
      this.videoId = uploadResponse.id;
      $('#video-id').text(this.videoId);
      $('.post-upload').show();      
      this.pollForVideoStatus();
    }.bind(this)
  });
  // This won't correspond to the *exact* start of the upload, but it should be close enough.
  this.uploadStartTime = Date.now();
  uploader.upload();
};

UploadVideo.prototype.handleUploadClicked = function() {
  $('#button').attr('disabled', true);
  this.uploadFile($('#file').get(0).files[0]);
};

UploadVideo.prototype.pollForVideoStatus = function() {  
  $.ajax({
    type : 'GET',
    url : 'https://www.googleapis.com/youtube/v3/videos',
    data : {
      id : this.videoId,
      part : 'status,player',
      key : this.apiKey
    },
    success : function(response){            
      console.log(response)
      var uploadStatus = response.items[0].status.uploadStatus;
      switch (uploadStatus) {
        // This is a non-final status, so we need to poll again.
        case 'uploaded':
          $('#post-upload-status').append('<li>Upload status: ' + uploadStatus + '</li>');
          setTimeout(this.pollForVideoStatus.bind(this), STATUS_POLLING_INTERVAL_MILLIS);
          break;
        // The video was successfully transcoded and is available.
        case 'processed':
          $('#player').append(response.items[0].player.embedHtml);
          $('#post-upload-status').append('<li>Final status.</li>');
          break;
        // All other statuses indicate a permanent transcoding failure.
        default:
          $('#post-upload-status').append('<li>Transcoding failed.</li>');
          break;
      }
    }.bind(this),
    error : function(response){
      console.log(response.error.message)
      setTimeout(this.pollForVideoStatus.bind(this), STATUS_POLLING_INTERVAL_MILLIS);
    }.bind(this)
  })
};

$(function(){

  function initStuff(){

    $.ajax({
      type: 'POST',
      url: 'youtube_token',
      success : function(data){
        var uploadVideo = new UploadVideo();
        uploadVideo.ready(data.token, data.apiKey);  
      },
      error : function(data){
        console.log('error');
        console.log(data);
      }
    });
  };

  initStuff();

})
