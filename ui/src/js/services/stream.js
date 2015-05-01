app.factory('Stream', ['$resource', function($resource) {
    return $resource('/api/streams/:id/');
}]);