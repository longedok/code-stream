app.controller('MainController', [
'$scope', '$modal', '$http', 'BackendData', 'UserService',
function($scope, $modal, $http, BackendData, UserService) {
    $scope.currentUser = UserService.currentUser = BackendData.user;
    $scope.streams = BackendData.streams;
    $scope.technologies = BackendData.technologies;

    function onStreamsUpdated() {
        Stream.query(function(streams) {
            $scope.streams = streams;
        });
    }

    var ws4redis = new WS4Redis({
        uri: 'ws://127.0.0.1:8000/ws/streams?subscribe-broadcast&echo',
        receive_message: onStreamsUpdated,
        heartbeat_msg: '-- hearbeat --'
    });

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
            templateUrl: 'templates/forms/stream.html',
            controller: 'CreateStreamController'
        });
    };

    $scope.logout = function() {
        $http.post('/api/users/logout/').then(function() {
            $scope.$broadcast('users.logged-out');
        })
    };
}]);

app.controller('CreateStreamController', [
'$scope', '$state', '$modal', '$modalInstance', 'Stream', 'UserService', 'FormHelper',
function($scope, $state, $modal, $modalInstance, Stream, UserService, FormHelper) {
    var formHelper = FormHelper($scope);

    $scope.input = {};
    $scope.user = UserService.currentUser;

    $scope.submit = function() {
        formHelper.submit($scope.input, Stream.save).then(function(stream) {
            $modalInstance.close();

            $state.go('main.stream', {username: $scope.user.username, stream: stream});
        });
    };

    $scope.createNewSeries = function(seriesTitle) {
        $modal.open({
            templateUrl: 'templates/forms/series.html',
            controller: [
            '$scope', '$modalInstance', 'Series', 'FormHelper',
            function($scope, $modalInstance, Series, FormHelper) {
                var formHelper = FormHelper($scope);

                $scope.input = {
                    title: seriesTitle
                };

                $scope.submit = function() {
                    formHelper.submit($scope.input, Series.save).then(function(series) {
                        $modalInstance.close(series);
                    });
                };
            }]
        }).result.then(function(series) {
                UserService.currentUser.series.push(series);
                console.log(UserService.currentUser);
                $scope.input.series = series.id;
            })
    };
}]);