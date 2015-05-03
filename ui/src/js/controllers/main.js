app.controller('MainController', [
'$scope', '$modal', '$http', 'Stream',
function($scope, $modal, $http, Stream) {
    $scope.streams = Stream.query();

    function onMessage(message) {
        $scope.streams = Stream.query();
        console.log(message);
    }

    WS4Redis({
        uri: 'ws://127.0.0.1:8000/ws/streams?subscribe-broadcast&publish-broadcast&echo',
        receive_message: onMessage,
        heartbeat_msg: '-- hearbeat --'
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
                    formHelper.submit($scope.input, User.login).then($modalInstance.close);
                };
            }]
        }).result.then(function() {
            location.reload();
        });
    };

    $scope.createAccount = function() {
        $modal.open({
            templateUrl: 'templates/forms/register.html',
            controller: ['$scope', '$modalInstance', 'User', function($scope, $modalInstance, User) {
                $scope.input = {};

                $scope.submit = function() {
                    User.register($scope.input, function () {
                        $modalInstance.close();
                    }, function (response) {
                        $scope.errors = response.data;
                    });
                };
            }]
        }).result.then(function() {
            location.reload();
        })
    };

    $scope.startStream = function() {
        $modal.open({
            templateUrl: 'templates/forms/stream.html',
            controller: ['$scope', '$modalInstance', 'Stream', function($scope, $modalInstance, Stream) {
                $scope.input = {};

                $scope.submit = function() {
                    Stream.save($scope.input, function() {
                        $modalInstance.close();
                    }, function(response) {
                        $scope.errors = response.data;
                    });
                };
            }]
        });
    };

    $scope.logout = function() {
        $http.post('/api/users/logout/').then(function() {
            location.reload();
        })
    };
}]);