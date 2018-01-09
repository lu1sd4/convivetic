var conviveticApp = angular.module
(
    'conviveticApp', 
    ['ngMessages', 'ngAnimate','app.controllers', 'app.factories', 'app.directives']
).config(function($interpolateProvider){
    $interpolateProvider.startSymbol('{[{').endSymbol('}]}');
});

angular.module('app.controllers', []);
angular.module('app.factories', []);
angular.module('app.directives', []);
