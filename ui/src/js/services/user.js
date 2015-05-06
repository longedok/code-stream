app.factory('User', ['$resource', function($resource) {
    return $resource('/api/users/:id/:action/', null, {
        login: {
            params: {action: 'login'},
            method: 'POST'
        },
        register: {
            params: {action: 'register'},
            method: 'POST'
        }
    });
}]);

app.service('UserService', function() {
    this.currentUser = undefined;
});