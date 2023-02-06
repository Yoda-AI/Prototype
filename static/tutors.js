/**
 * Created by Ynon on 30/10/2017.
 */

// Controller for tutors management.
application.controller('tutorController', ["$scope", "$http", function ($scope, $http) {
    $scope.tutorNameToAdd = "";

    $scope.tutorFrom = "";
    $http.get("/get_tutors_from").then(function successCallback(response) {
        $scope.tutors_from = response.data;
    }, errorCallback);

    $scope.tutors = "";
    $http.get("/get_tutors").then(function successCallback(response) {
        $scope.tutors = response.data;

        $http.get("/get_current_tutors").then(function successCallback(response) {
            $scope.current_tutors = response.data;
            $("#tutor1select").val($scope.current_tutors[1]);
            $("#tutor2select").val($scope.current_tutors[2]);
            $("#tutor3select").val($scope.current_tutors[3]);
            $("#tutor4select").val($scope.current_tutors[4]);
            $("#tutor5select").val($scope.current_tutors[5]);
            $("#tutor6select").val($scope.current_tutors[6]);
			$("#tutor7select").val($scope.current_tutors[7]);
			$("#tutor8select").val($scope.current_tutors[8]);
			$("#tutor9select").val($scope.current_tutors[9]);
			$("#tutor10select").val($scope.current_tutors[10]);
			$("#tutor11select").val($scope.current_tutors[11]);
			$("#tutor12select").val($scope.current_tutors[12]);
			$("#tutor13select").val($scope.current_tutors[13]);
			$("#tutor14select").val($scope.current_tutors[14]);
			$("#tutor15select").val($scope.current_tutors[15]);
        }, errorCallback);

    }, errorCallback);

    $scope.deletedTutor = "";

    $scope.addTutor = function () {
        if (!$scope.tutorFrom in $scope.tutors_from) {
            alert("Please pick 7190, 7149, 8153, Matzov");
            return "";
        }
        if ($scope.tutorNameToAdd == "") {
            alert("Please fill in tutor name to add.");
            return "";
        }

        $http.post("/insert_new_tutor", [$scope.tutorFrom, $scope.tutorNameToAdd]).then(
            function successCallback(response) {
                alert(response.data);
                location.reload();
        }, errorCallback);
    }

    $scope.deleteTutor = function (tutor_id) {
        if (confirm("Are you sure you want to delete tutor information?")) {
            $http.post("/delete_tutor/" + tutor_id, '')
                .then(
                    function successCallback(response) {
                        alert(response.data);
                        window.location.reload();
                    },
                    errorCallback);
        }
    }

    $scope.updateTutors = function () {

        $http.get("/currentauthorization").then(function successCallback(response) {
            $scope.username = response.data.username;

            if ($scope.username[0] == 'H') {
                alert("No permissions to change tutors");
                return;
            }

            var groups_dict = {
                1: $("#tutor1select").val(),
                2: $("#tutor2select").val(),
                3: $("#tutor3select").val(),
                4: $("#tutor4select").val(),
                5: $("#tutor5select").val(),
                6: $("#tutor6select").val(),
				7: $("#tutor7select").val(),
				8: $("#tutor8select").val(),
				9: $("#tutor9select").val(),
				10: $("#tutor10select").val(),
				11: $("#tutor11select").val(),
				12: $("#tutor12select").val(),
				13: $("#tutor13select").val(),
				14: $("#tutor14select").val(),
				15: $("#tutor15select").val()
            }

            $http.post("/update_current_tutors", JSON.stringify(groups_dict)).then(
                function successCallback(response) {
                    alert(response.data);
                    location.reload();
                }, errorCallback);

        }, errorCallback);

    }

}]);

$( document ).ready(function() {
    $('#tutors-link').addClass('active')
});