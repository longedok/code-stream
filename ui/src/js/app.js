var app = angular.module('CodeStream', ['ngSanitize', 'ngResource', 'ui.bootstrap']);

app.config(['$httpProvider', '$resourceProvider', function($httpProvider, $resourceProvider) {
    //$resourceProvider.defaults.stripTrailingSlashes = false;

    $httpProvider.defaults.xsrfCookieName = 'csrftoken';
    $httpProvider.defaults.xsrfHeaderName = 'X-CSRFToken';
}]);

app.controller('ChatCtrl', ['$scope', '$http', function($scope, $http) {
    $scope.messages = [];
    $scope.input = {};
    $scope.send_enabled = false;

    var on_message = function(msg) {
        $scope.$apply(function() {
            $scope.messages.push(msg);
        });
    };

    var ws4redis = WS4Redis({
        uri: 'ws://127.0.0.1:8000/ws/foobar?subscribe-broadcast&publish-broadcast&echo',
        receive_message: on_message,
        heartbeat_msg: '-- hearbeat --'
    });

    $scope.send = function() {
        $http.post('/api/chat/post', $scope.input)
            .success(function() {
                $scope.input.text = '';
            });
    }
}]);

app.factory('Stream', ['$resource', function($resource) {
    return $resource('/api/streams/:id');
}]);

app.factory('StreamSeries', ['$resource', function($resource) {
    return $resource('/api/streamseries/:id');
}]);

app.factory('Technology', ['$resource', function($resource) {
    return $resource('/api/technologies/:id');
}]);

app.factory('User', ['$resource', function($resource) {
    return $resource('/api/users/:id/:action', null, {
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

app.factory('SubmitService', function() {
    return function(scope, Provider, providerAction, success) {
        var action = providerAction || 'save';
        scope.input = {};
        scope.errors = {};

        scope.submit = function() {
            Provider[action](scope.input, function(response) {
                scope.model = response.data;
                if (success !== undefined)
                    success(data);
            }, function(response) {
                if (response.status == 0) {
                    scope.errors.non_field_errors = 'Problems connecting to the server';
                } else {
                    scope.errors = response.data;
                }
            });
        }
    }
});

app.controller('StreamCreateCtrl', ['$scope', 'SubmitService', 'Stream', function ($scope, SubmitService, Stream) {
    SubmitService($scope, Stream);
}]);

app.controller('StreamSeriesCreateCtrl', ['$scope', 'SubmitService', 'StreamSeries', function ($scope, SubmitService, StreamSeries) {
    SubmitService($scope, StreamSeries);
}]);

app.controller('TechnologyCreateCtrl', ['$scope', 'SubmitService', 'Technology', function ($scope, SubmitService, Technology) {
    SubmitService($scope, Technology);
}]);

app.controller('MainCtrl', ['$scope', '$modal', '$http', 'Stream', function($scope, $modal, $http, Stream) {
    $scope.streams = Stream.query();

    $scope.login = function() {
        $modal.open({
            templateUrl: 'src/js/templates/login.html',
            controller: ['$scope', 'SubmitService', 'User', function($scope, SubmitService, User) {
                SubmitService($scope, User, 'login', function(data) {
                    $scope.$dismiss();
                });
            }]
        });
    };

    $scope.signup = function() {
        $modal.open({
            templateUrl: 'src/js/templates/register.html',
            controller: ['$scope', 'SubmitService', 'User', function($scope, SubmitService, User) {
                SubmitService($scope, User, 'register');
            }]
        });
    };

    $scope.logout = function() {
        $http.post('/api/users/logout')
    }
}]);