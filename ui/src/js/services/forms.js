app.factory('FormHelper', ['$q', function($q) {
    function FormHelper(scope) {
        this.submit = function(model, action) {
            return $q(function(resolve, reject) {
                action.apply(null, [model]).$promise.then(function(response) {
                    scope.$broadcast('forms.success', response.data);
                    resolve(response.data);
                }, function(response) {
                    scope.$broadcast('forms.errors', response.data);
                    reject(response.data);
                });
            });
        };
    }

    return function(scope) {
        return new FormHelper(scope);
    }
}]);