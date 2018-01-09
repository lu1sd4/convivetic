angular.module('app.factories')
  .factory('usernameservice', function($q, $http) {
  return function(username) {
    var deferred = $q.defer();
    // your api vall goes her
    $http.get('api/users/' + username).then(function() { // 
      // Found the user, therefore not unique.
      deferred.reject();
    }, function() {
      // User not found, therefore unique!
      deferred.resolve();
    });
    return deferred.promise;
  }
});