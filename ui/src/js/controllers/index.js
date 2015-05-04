app.controller('IndexController',
['$scope', 'Stream',
function($scope, Stream) {
    $scope.streams = Stream.query();

    function onMessage(message) {
        $scope.streams = Stream.query();
        console.log(message);
    }

    WS4Redis({
        uri: 'ws://127.0.0.1:8000/ws/streams?subscribe-broadcast&publish-broadcast&echo',
        receive_message: onMessage,
        heartbeat_msg: '-- hearbeat --'
    });
}]);