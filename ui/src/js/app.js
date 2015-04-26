var app = angular.module('CodeStream', ['ngSanitize', 'ngResource', 'ui.bootstrap']);

app.config(['$httpProvider', '$resourceProvider', function($httpProvider, $resourceProvider) {
    $resourceProvider.defaults.stripTrailingSlashes = false;

    $httpProvider.defaults.xsrfCookieName = 'csrftoken';
    $httpProvider.defaults.xsrfHeaderName = 'X-CSRFToken';
}]);

app.controller('ChatCtrl', ['$scope', '$http', function($scope, $http) {
    $scope.messages = [];
    $scope.input = {};
    $scope.sendingDisabled = true;

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
        $http.post('/api/chat/post/', $scope.input)
            .success(function() {
                $scope.input.text = '';
            });
    }
}]);

app.factory('Stream', ['$resource', function($resource) {
    return $resource('/api/streams/streams/:id/');
}]);

app.factory('StreamSeries', ['$resource', function($resource) {
    return $resource('/api/streamseries/:id/');
}]);

app.factory('Technology', ['$resource', function($resource) {
    return $resource('/api/technologies/:id/');
}]);

app.factory('User', ['$resource', function($resource) {
    return $resource('/api/users/:id/:action/', null, {
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

app.controller('MainController', ['$scope', '$modal', '$http', 'Stream', function($scope, $modal, $http, Stream) {
    $scope.streams = Stream.query();

    function onMessage(message) {
        $scope.streams = Stream.query();
        console.log(message);
    }

    var wsStreams = WS4Redis({
        uri: 'ws://127.0.0.1:8000/ws/streams?subscribe-broadcast&publish-broadcast&echo',
        receive_message: onMessage,
        heartbeat_msg: '-- hearbeat --'
    });

    this.login = function() {
        $modal.open({
            templateUrl: 'src/js/templates/login.html',
            controller: ['$scope', '$modalInstance', 'User', function($scope, $modalInstance, User) {
                $scope.input = {};

                $scope.submit = function() {
                    User.login($scope.input, function() {
                        $modalInstance.close();
                    }, function(response) {
                        $scope.errors = response.data;
                    });
                };
            }]
        }).result.then(function() {
            location.reload();
        });
    };

    this.createAccount = function() {
        $modal.open({
            templateUrl: 'src/js/templates/register.html',
            controller: ['$scope', '$modalInstance', 'User', function($scope, $modalInstance, User) {
                $scope.input = {};

                User.register($scope.input, function() {
                    $modalInstance.close();
                }, function(response) {
                    $scope.errors = response.data;
                });
            }]
        }).result.then(function() {
            location.reload();
        })
    };

    this.startStream = function() {
        $modal.open({
            templateUrl: 'src/js/templates/stream.html',
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

    this.logout = function() {
        $http.post('/api/users/logout/').then(function() {
            location.reload();
        })
    };
}]);

app.directive('csFormGroup', function() {
    return {
        require: '^form',
        link: function(scope, element, attributes, formController) {
            var inputName = $(element).find('input').attr('name');

            scope.$watch(function() {
                return formController[inputName].$invalid && formController[inputName].$pristine;
            }, function (invalidity){
                $(element).toggleClass('has-error', invalidity);

                if (formController[inputName]) {
                    if (invalidity) {
                        $(element).append($('<span class="help-block error"></span>').text(formController[inputName].$error.remote));
                    } else {
                        $(element).find('.help-block.error').remove();
                    }
                }

            });
        }
    }
});

app.directive('csForm', function() {
    return {
        require: 'form',
        link: function(scope, element, attrs, formController) {
            // set invalidity of form fields based on the server's response
            scope.$on('csform.errors', function(event, errors) {
                Object.keys(errors).forEach(function(fieldName) {
                    formController[fieldName].$setValidity('remote', false);
                    formController[fieldName].$error.remote = errors[fieldName];
                });
            });

            // clear all the error messages on submit
            $(element).on('submit', function() {
                $(this).find('.form-group').each(function(index, formGroup) {
                    $(formGroup).removeClass('has-error');
                    $(formGroup).find('.help-block').remove();
                });
            });
        }
    }
});