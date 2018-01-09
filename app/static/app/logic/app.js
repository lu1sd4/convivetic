var conviveticApp = angular.module
(
    'conviveticApp', 
    ['ngMessages', 'ngAnimate','app.controllers']
).config(function($interpolateProvider){
    $interpolateProvider.startSymbol('{[{').endSymbol('}]}');
});

angular.module('app.controllers', []);