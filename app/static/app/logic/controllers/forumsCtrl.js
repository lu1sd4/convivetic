(function(){

	angular
		.module('app.controllers')
		.controller('forumsController', forumController)

		forumController.$inject = ["$scope"]

		function forumController($scope){

			var that = this;

			//Estados del header
			that.normalState = 'NORMAL_STATE';
			that.newState = 'NEW_STATE';

			that.currentState = that.normalState;
			

			that.newDiscussion = newDiscussion;
			that.cancelNewDiscussion = cancelNewDiscussion;

			function newDiscussion(){
				that.currentState = that.newState;
			}

			function cancelNewDiscussion(){
				that.currentState = that.normalState;
			}

		}

})();