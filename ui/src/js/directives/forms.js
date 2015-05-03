app.directive('csForm', function() {
    return {
        require: 'form',
        link: function(scope, element, attrs, formController) {
            var nonFieldErrorKeys = ['non_field_errors'];
            
            scope.$on('forms.errors', function(event, errors) {
                formController.nonFieldErrors = '';

                Object.keys(errors).forEach(function(fieldName) {
                    var errorText = errors[fieldName].join('\n');

                    if (nonFieldErrorKeys.indexOf(fieldName) > -1) {
                        formController.nonFieldErrors = errorText;
                    } else {
                        formController[fieldName].$setValidity('remote', false);
                        formController[fieldName].$error.remote = errorText;

                        var formGroup = $('*[name=' + fieldName + ']').parent();
                        if (!formGroup.hasClass('has-error')) {
                            formGroup.addClass('has-error');
                            formGroup.append($('<span class="help-block error"></span>').text(errorText));
                        }
                    }
                });
            });

            scope.$on('forms.success', function() {
                formController.$setPristine();

                element.find('.form-group').each(function(index, formGroup) {
                    element.find('.alert-danger').remove();
                    $(formGroup).removeClass('has-error');
                    $(formGroup).find('.help-block').remove();
                });                
            });
        }
    }
});        

app.directive('csFormGroup', function() {
    return {
        require: '^form',
        link: function(scope, element, attributes, formController) {
            var inputName = $(element).find('input').attr('name');

            scope.$watch(function() {
                return formController[inputName].$pristine;
            }, function (pristinity){
                if (pristinity === false) {
                    formController.nonFieldError = '';

                    element.removeClass('has-error');
                    element.find('.help-block.error').remove();
                }
            });
        }
    }
});

app.directive('csNonFieldErrors', function() {
    return {
        require: '^form',
        template: "<div class='alert alert-danger' role='alert' ng-if='form.nonFieldErrors'>{{ form.nonFieldErrors }}</div>",
        link: function(scope, element, attributes, formController) {
            scope.form = formController;
        }
    }
});