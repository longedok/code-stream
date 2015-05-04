var app = angular.module('CodeStream', [
    'ngSanitize', 'ngResource', 'ui.bootstrap', 'ui.select', 'ui.router', 'angularMoment'
]);

app.config(['$httpProvider', '$resourceProvider', function($httpProvider, $resourceProvider) {
    $resourceProvider.defaults.stripTrailingSlashes = false;

    $httpProvider.defaults.xsrfCookieName = 'csrftoken';
    $httpProvider.defaults.xsrfHeaderName = 'X-CSRFToken';
}]);

app.config(['uiSelectConfig', function(uiSelectConfig) {
    uiSelectConfig.theme = 'bootstrap';
}]);

app.config(['$stateProvider', '$urlRouterProvider', function($stateProvider, $urlRouterProvider) {
    $urlRouterProvider.otherwise("/");

    $stateProvider
        .state('main', {
            abstract: true,
            url: '/',
            controller: 'MainController',
            templateUrl: "templates/main.html"
        })
            .state('main.index', {
                url: '',
                controller: 'IndexController',
                templateUrl: 'templates/index.html'
            })
            .state('main.stream', {
                url: 'stream/:username',
                controller: 'StreamController',
                templateUrl: 'templates/stream.html'
            })
}]);