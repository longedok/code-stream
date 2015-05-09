app.controller('StreamController', [
'$scope', '$http', 'stream',
function($scope, $http, stream) {
    $scope.stream = stream;

    $scope.input = {};
    $scope.chatMessages = [];

    var onMessage = function(msg) {
        $scope.$apply(function() {
            $scope.chatMessages.push(JSON.parse(msg));
        });
    };

    var ws4redis = new WS4Redis({
        uri: 'ws://127.0.0.1:8000/ws/streams?subscribe-broadcast&echo',
        receive_message: onMessage,
        heartbeat_msg: '-- hearbeat --'
    });

    $scope.sendChatMessage = function() {
        $http.post('/api/chat/post/' + $scope.stream.user.username + '/', $scope.input)
            .success(function() {
                $scope.input.text = '';
                $scope.input.code = false;
            });
    };

    $scope.$on('$destroy', function() {
        ws4redis.disconnect();
    });
}]);