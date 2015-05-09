app.controller('TechnologiesController', [
'$scope', '$modal', 'Technology', 'Material',
function($scope, $modal, Technology, Material) {
    $scope.add = function() {
        $modal.open({
            templateUrl: 'templates/forms/technology.html',
            controller: [
            '$scope', '$modalInstance', 'FormHelper',
            function($scope, $modalInstance, FormHelper) {
                var formHelper = FormHelper($scope);

                $scope.input = {};

                $scope.submit = function() {
                    formHelper.submit($scope.input, Technology.save).then(function(createdTechnology) {
                        $modalInstance.close(createdTechnology);
                    });
                };
            }]
        }).result.then(function(createdTechnology) {
            $scope.technologies.push(createdTechnology);
        });
    };

    $scope.addMaterial = function(technology) {
        $modal.open({
            templateUrl: 'templates/forms/material.html',
            controller: [
            '$scope', '$modalInstance', 'FormHelper',
            function($scope, $modalInstance, FormHelper) {
                var formHelper = FormHelper($scope);

                $scope.input = {
                    technology: technology.id
                };

                $scope.submit = function() {
                    formHelper.submit($scope.input, Material.save).then(function(createdMaterial) {
                        $modalInstance.close(createdMaterial);
                    });
                };
            }]
        }).result.then(function(createdMaterial) {
            technology.materials.push(createdMaterial);
        });
    };
}]);