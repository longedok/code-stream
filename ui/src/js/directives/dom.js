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

app.directive('csPreventSubmit', function() {
    return {
        link: function(scope, elm) {
            $(elm).find("input[type='text']").keypress(function(e) {
                if (e.which == 13) {
                    e.preventDefault();
                    e.stopPropagation();
                }
            });
        }
    }
});