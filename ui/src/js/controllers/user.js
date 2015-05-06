app.controller('ProfileController', [
'$scope', 'UserService', 'FormHelper',
function($scope, UserService, FormHelper) {
    $scope.model = UserService.currentUser;

    $scope.$watch(function() {
        return UserService.currentUser;
    }, function(newValue, oldValue) {
        if (newValue !== oldValue) {
            $scope.model = newValue;
        }
    });
}]);