app.controller('MainController', [
'$scope', '$modal', '$http', 'BackendData', 'UserService', 'EventsService', 'Stream', 'Technology',
function($scope, $modal, $http, BackendData, UserService, EventsService, Stream, Technology) {
    $scope.currentUser = UserService.currentUser = BackendData.user;
    $scope.streams = BackendData.streams;
    $scope.technologies = BackendData.technologies;

    EventsService.loadMore().then(function(events) {
        $scope.events = events;
        $scope.moreEventsAvailable = EventsService.hasNext;
    });


    var ws = new WebSocket('ws://127.0.0.1:8000/ws/main?subscribe-broadcast&echo');

    ws.onmessage = function (event) {
        var message = event.data;

        var parsedMessage = JSON.parse(message),
            type = parsedMessage['action'];

        if (type == 'streams-updated') {
            $scope.$apply(function() {
                Stream.query(function(streams) {
                    $scope.streams = streams;
                });
            });
        } else if (type == 'events-updated') {
            $scope.$apply(function() {
                $scope.events = Event.query();
            });
        }
    };

    $scope.$on('$destroy', function() {
        ws4redis.disconnect();
    });

    $scope.$on('users.logged-in', function(event, user) {
        user.is_authenticated = true;
        UserService.currentUser = $scope.currentUser = user;
    });

    $scope.$on('users.logged-out', function() {
        $scope.currentUser = UserService.currentUser = {is_authenticated: false};
    });

    $scope.login = function() {
        $modal.open({
            templateUrl: 'templates/forms/login.html',
            controller: [
            '$scope', '$modalInstance', 'User', 'FormHelper',
            function($scope, $modalInstance, User, FormHelper) {
                var formHelper = FormHelper($scope);

                $scope.input = {};

                $scope.submit = function() {
                    formHelper.submit($scope.input, User.login).then(function(authenticatedUser) {
                        $modalInstance.close(authenticatedUser.data);
                    });
                };
            }]
        }).result.then(function(authenticatedUser) {
            $scope.$broadcast('users.logged-in', authenticatedUser);
        });
    };

    $scope.createAccount = function() {
        $modal.open({
            templateUrl: 'templates/forms/register.html',
            controller: [
            '$scope', '$modalInstance', 'User', 'FormHelper',
            function($scope, $modalInstance, User, FormHelper) {
                var formHelper = FormHelper($scope);

                $scope.input = {};

                $scope.submit = function() {
                    formHelper.submit($scope.input, User.register).then($modalInstance.close);
                };
            }]
        });
    };

    $scope.startStream = function() {
        $modal.open({
            scope: $scope,
            templateUrl: 'templates/forms/stream.html',
            controller: 'CreateStreamController',
            resolve: {
                technologies: function() {
                    return Technology.query().$promise;
                }
            }
        });
    };

    $scope.logout = function() {
        $http.post('/api/users/logout/').then(function() {
            $scope.$broadcast('users.logged-out');
        })
    };

    $scope.loadMoreEvents = function() {
        EventsService.loadMore().then(function(events) {
            Array.prototype.push.apply($scope.events, events);
            $scope.moreEventsAvailable = EventsService.hasNext;
        });
    }
}]);

app.controller('CreateStreamController', [
'$scope', '$state', '$modal', '$modalInstance', 'Stream', 'UserService', 'FormHelper', 'technologies',
function($scope, $state, $modal, $modalInstance, Stream, UserService, FormHelper, technologies) {
    var formHelper = FormHelper($scope);

    $scope.technologies = technologies;
    $scope.input = {};
    $scope.user = UserService.currentUser;

    $scope.submit = function() {
        formHelper.submit($scope.input, Stream.save).then(function(stream) {
            $modalInstance.close();
        });
    };

    $scope.createNewSeries = function(seriesTitle) {
        $modal.open({
            templateUrl: 'templates/forms/series.html',
            controller: [
            '$scope', '$modalInstance', 'Series', 'FormHelper', 'technologies',
            function($scope, $modalInstance, Series, FormHelper, technologies) {
                $scope.technologies = technologies;

                var formHelper = FormHelper($scope);

                $scope.input = {
                    title: seriesTitle
                };

                $scope.submit = function() {
                    formHelper.submit($scope.input, Series.save).then(function(series) {
                        $modalInstance.close(series);
                    });
                };
            }],
            resolve: {
                technologies: function() {
                    return $scope.technologies.$promise;
                }
            }
        }).result.then(function(series) {
                UserService.currentUser.series.push(series);
                $scope.input.series = series.id;
            })
    };
}]);