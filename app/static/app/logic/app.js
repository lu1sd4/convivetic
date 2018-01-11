var conviveticApp = angular.module
(
    'conviveticApp', 
    ['ngMessages', 'ngAnimate','app.controllers', 'app.factories', 'app.directives']
).config(function($interpolateProvider, $httpProvider){
    $interpolateProvider.startSymbol('{[{').endSymbol('}]}');
    
    $httpProvider.defaults.xsrfCookieName = 'csrftoken';
	$httpProvider.defaults.xsrfHeaderName = 'X-CSRFToken';
});

angular.module('app.controllers', []);
angular.module('app.factories', []);
angular.module('app.directives', []);
