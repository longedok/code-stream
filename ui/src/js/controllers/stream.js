app.controller('StreamController', [
'$scope', '$http', 'stream',
function($scope, $http, stream) {
    $scope.stream = stream;

    $scope.input = {};
    $scope.chatMessages = [];

    var ws = new WebSocket('ws://127.0.0.1:8000/ws/chat-' + $scope.stream.user.username + '?subscribe-broadcast&echo');

    ws.onmessage = function(event) {
        $scope.$apply(function() {
            $scope.chatMessages.push(JSON.parse(event.data));
        });
    };

    $scope.sendChatMessage = function() {
        $http.post('/api/chat/post/' + $scope.stream.user.username + '/', $scope.input)
            .success(function() {
                $scope.input.text = '';
                $scope.input.code = false;
            });
    };

    $scope.$on('$destroy', function() {
        ws.close();
    });
}]);