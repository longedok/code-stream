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