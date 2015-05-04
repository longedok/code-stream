app.controller('MainController', [
'$scope', '$modal', '$http', 'Stream',
function($scope, $modal, $http, Stream) {
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
            controller: [
            '$scope', '$modalInstance', 'Stream', 'FormHelper',
            function($scope, $modalInstance, Stream, FormHelper) {
                var formHelper = FormHelper($scope);

                $scope.input = {};

                $scope.submit = function() {
                    formHelper.submit($scope.input, Stream.save).then($modalInstance.close);
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