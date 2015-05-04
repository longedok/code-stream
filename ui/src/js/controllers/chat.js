app.controller('ChatController', [
'$scope', '$http',
function($scope, $http) {
    $scope.messages = [];
    $scope.input = {};
    $scope.sendingDisabled = true;

    var onMessage = function(msg) {
        $scope.$apply(function() {
            $scope.messages.push(msg);
        });
    };

    WS4Redis({
        uri: 'http://127.0.0.1:8000/ws/chat?subscribe-broadcast&publish-broadcast&echo',
        receive_message: onMessage,
        heartbeat_msg: '-- hearbeat --'
    });

    $scope.send = function() {
        $http.post('/api/chat/post/', $scope.input)
            .success(function() {
                $scope.input.text = '';
            });
    }
}]);