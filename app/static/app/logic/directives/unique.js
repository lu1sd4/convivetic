angular.module('app.directives')
   .directive('unique', function(usernameservice) {
	  return {
	    restrict: 'A',
	    require: 'ngModel',
	    link: function(scope, element, attrs, ngModel) {
	      ngModel.$asyncValidators.unique = usernameservice;
	    }
	  };
});