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

app.factory('Event', ['$resource', function($resource) {
    return $resource('/api/streams/events/:id/:action/', {id: '@id'}, {
        'query': {
            method: 'GET',
            isArray: false
        }
    });
}]);

app.service('EventsService', ['Event', function(Event) {
    var self = this;
    var nextPage;

    function loadData(cursor) {
        return Event.query({'cursor': cursor}).$promise.then(function(data) {
            nextPage = data['next'];
            self.hasNext = nextPage !== null;

            return data['results'];
        });
    }

    this.loadMore = function() {
        return loadData(nextPage);
    };
}]);