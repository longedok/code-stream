app.controller('MainController', [
'$scope', '$modal', '$http', 'BackendData',
function($scope, $modal, $http, BackendData) {
    $scope.currentUser = BackendData.user;

    $scope.$on('users.logged-in', function(user) {
        $scope.currentUser = user;
        $scope.currentUser.is_authenticated = true;
    });

    $scope.$on('users.logged-out', function() {
        $scope.currentUser = {is_authenticated: false};
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
                        $modalInstance.close(authenticatedUser);
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
        }).result.then(function() {
            location.reload();
        })
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
'$scope', '$modalInstance', 'Stream', 'FormHelper',
function($scope, $modalInstance, Stream, FormHelper) {
    var formHelper = FormHelper($scope);

    $scope.input = {};

    $scope.submit = function() {
        formHelper.submit($scope.input, Stream.save).then($modalInstance.close);
    };
}]);