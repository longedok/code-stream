var app = angular.module('CodeStream', ['ngSanitize', 'ngResource', 'ui.bootstrap', 'angularMoment']);

app.config(['$httpProvider', '$resourceProvider', function($httpProvider, $resourceProvider) {
    $resourceProvider.defaults.stripTrailingSlashes = false;

    $httpProvider.defaults.xsrfCookieName = 'csrftoken';
    $httpProvider.defaults.xsrfHeaderName = 'X-CSRFToken';
}]);