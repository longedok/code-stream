app.controller('StreamController', [
'$scope', 'stream',
function($scope, stream) {
    $scope.stream = stream;

    $scope.chatMessage = {};
    $scope.chatMessages = [];

    var onMessage = function(msg) {
        $scope.$apply(function() {
            $scope.messages.push(msg);
        });
    };

    var ws4redis = WS4Redis({
        uri: 'ws://127.0.0.1:8000/ws/chat?subscribe-broadcast&publish-broadcast&echo',
        receive_message: onMessage,
        heartbeat_msg: '-- hearbeat --'
    });

    $scope.sendChatMessage = function() {
        $http.post('/api/chat/post/', $scope.chatMessage)
            .success(function() {
                $scope.input.text = '';
            });
    };

    $scope.$on('$destroy', function() {
        ws4redis.disconnect();
    });
}]);