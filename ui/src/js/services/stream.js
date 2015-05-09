app.factory('Stream', ['$resource', function($resource) {
    return $resource('/api/streams/streams/:id/:action/', {id: '@id'}, {
        getActive: {
            method: 'GET',
            params: {
                action: 'get_active'
            }
        }
    });
}]);

app.factory('Series', ['$resource', function($resource) {
    return $resource('/api/streams/series/:id/:action/', {id: '@id'});
}]);

app.factory('Technology', ['$resource', function($resource) {
    return $resource('/api/streams/technologies/:id/:action/', {id: '@id'});
}]);

app.factory('Material', ['$resource', function($resource) {
    return $resource('/api/streams/materials/:id/:action/', {id: '@id'});
}]);