(function(){

	'use strict';

	angular
		.module('app.controllers')
		.controller('commentToolboxController', commentToolboxController);

	commentToolboxController.$inject = ["$scope", "$http"];

	function commentToolboxController($scope, $http){
		
		var that = this;

		that.user_id = '';
		that.toolbox_id = '';

		that.comment = [];

		that.init = init;
		that.commentToString = commentToString;		

		function init(uid, tbid){
			that.user_id = uid;
			that.toolbox_id = tbid;
		}

		function commentToString(){
			var result = "";
			for(var c in that.comment){
				if(that.comment[c]){
					result += that.comment[c] + '<br>';
				}
			}
			return result;
		}

		function saveComment(){
			var data = {
				user_id = that.user_id,
				toolbox_id = that.toolbox_id,
				comment = that.commentToString()
			};
			$http.post('/toolbox/api/comment', data).then(function(){
				location.replace('/guides/manage');
			});
		}

	}

})();