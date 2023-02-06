/**
 * Created by Ynon on 30/10/2017.
 */

application.controller('importController', ["$scope", "$http", function ($scope, $http) {
    $scope.importRawData = "";
    $scope.numberOfTutors = 5;

    $scope.submitStudents = function students() {
        $http.post("/import_malshabs", [$scope.importRawData, $scope.numberOfTutors]).then(
            function successCallback(response) {
                var number_of_malshabs = response.data;
                $.notify("Successfully inserted " + number_of_malshabs + " malshabs", "info");
            }, errorCallback);
        $.notify("Processing malshab information", "info");
    }
}]);

$( document ).ready(function() {
    $('#import-link').addClass('active')
});