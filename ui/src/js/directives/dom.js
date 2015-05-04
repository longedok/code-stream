app.directive('csPlayerHeightResize', function() {
    return {
        link: function(scope, element) {
            element.height($(this).height() * 0.75);

            $(window).resize(function() {
                element.height($(this).height() * 0.75);
            })
        }
    }
});