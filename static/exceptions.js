/**
 * Created by Ynon on 30/10/2017.
 */

// Controller for tutors management.
application.controller('exceptionsController', ["$scope", "$http", function ($scope, $http) {
    $scope.newExceptionID = "";
    $scope.newExceptionFirstName = "";
    $scope.newExceptionLastName = "";
    $scope.newExceptionDescription = "";

    $scope.editedExceptionID = "";
    $scope.editedExceptionFirstName = "";
    $scope.editedExceptionLastName = "";
    $scope.editedExceptionDescription = "";

    $scope.exceptions = "";
    $http.get("/get_exceptions").then(function successCallback(response) {
        $scope.exceptions = response.data;
    }, errorCallback);

    $scope.deletedException = "";

    $scope.addException = function () {

        $http.post("/insert_new_exception", [
            $scope.newExceptionID,
            $scope.newExceptionFirstName,
            $scope.newExceptionLastName,
            $scope.newExceptionDescription]).then(
            function successCallback(response) {
                $.notify(response.data, "info")
            }, errorCallback);
    };

    $scope.update = function () {

        for (var i = 0; i < $scope.exceptions.length; i++) {
            var curr = $scope.exceptions[i];
            if (curr.ID == $scope.editedExceptionID) {
                $("#editFN").val(curr.FirstName);
                $("#editLN").val(curr.LastName);
                $("#editDESC").val(curr.Description);
                return;
            }
        }
    }

    $scope.editException = function () {

        $http.post("/update_exception", [
            $scope.editedExceptionID,
            $("#editFN").val(),
            $("#editLN").val(),
            $("#editDESC").val()]
        )
            .then(function successCallback(response) {
                $.notify(response.data, "info")
            }, errorCallback);
    };

    $scope.deleteException = function (exception_id) {
        if (confirm("Are you sure you want to delete exception information for id: " + exception_id + "?")) {
            $http.post("/delete_exception/" + exception_id, '')
                .then(
                    function successCallback(response) {
                        $.notify(response.data, "info")
                    },
                    errorCallback);
        }
    }
}]);

$( document ).ready(function() {
    $('#exceptions-link').addClass('active')
});