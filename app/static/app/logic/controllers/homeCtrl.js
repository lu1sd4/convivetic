(function(){

	'use strict';

	angular
		.module('app.controllers')
		.controller('homeController', homeController);

	homeController.$inject = ["$scope", "$http"];

	function homeController($scope, $http){
		var that = this;

		that.mMenuIsActive = false;
		that.getMobileMenu = getMobileMenu;
		
		that.pendingExperiences = '';

		$http.get("/experiences/api/pendingexperiences").then(function(response) {
	        that.pendingExperiences = response.data.count;
	    });

		function getMobileMenu(){
			that.mMenuIsActive = !that.mMenuIsActive;
		}

		var fixmeTop = 325;       // get initial position of the element

		$(window).scroll(function() {                  // assign scroll event listener

		    var currentScroll = $(window).scrollTop(); // get current position

		    if (currentScroll >= fixmeTop) {           // apply position: fixed if you
		        $('.nav-c').css({                      // scroll to that element or below it
		            position: 'fixed',
		            background:'#fff',
		            top: '0',
		            width: '100%',
		            'z-index':10
		        });
		    } else {                                   // apply position: static
		        $('.nav-c').css({                      // if you scroll above it
		            position: 'static'
		        });
		    }

		    if (currentScroll >= fixmeTop) {           // apply position: fixed if you
		        $('.secondary-nav').css({                      // scroll to that element or below it
		            position: 'fixed',
		            top: '41px',
		            width: '100%',
		            'z-index':10
		        });
		    } else {                                   // apply position: static
		        $('.secondary-nav').css({                      // if you scroll above it
		            position: 'static'
		        });
		    }

		});

		var ihash = window.location.href.indexOf('#');
		if(ihash >= 0){
			var compSelector = window.location.href.substring(ihash, window.location.href.length);
			$('html, body').scrollTop($(compSelector).offset().top);
		}



	}

})();