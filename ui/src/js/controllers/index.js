app.controller('IndexController',
['$scope', 'Stream', 'BackendData',
function($scope, Stream, BackendData) {
    $scope.streams = BackendData.streams;

    function onStreamsUpdated() {
        Stream.query(function(streams) {
            $scope.streams = streams;
        });
    }

    WS4Redis({
        uri: 'ws://127.0.0.1:8000/ws/streams?subscribe-broadcast&publish-broadcast&echo',
        receive_message: onStreamsUpdated,
        heartbeat_msg: '-- hearbeat --'
    });
}]);