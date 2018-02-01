angular.module('app.directives')
	.directive('input', function ($parse) {
	  return {
	    restrict: 'E',
	    require: '?ngModel',
	    link: function (scope, element, attrs) {
	      if (attrs.ngModel && attrs.value) {
	        $parse(attrs.ngModel).assign(scope, attrs.value);
	      }
	    }
	  };
});