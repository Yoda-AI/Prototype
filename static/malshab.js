/**
 * Created by Ynon on 29/10/2017.
 */

function copyTextToClipboard(text) {
    var textArea = document.createElement("textarea");

    //
    // *** This styling is an extra step which is likely not required. ***
    //
    // Why is it here? To ensure:
    // 1. the element is able to have focus and selection.
    // 2. if element was to flash render it has minimal visual impact.
    // 3. less flakyness with selection and copying which **might** occur if
    //    the textarea element is not visible.
    //
    // The likelihood is the element won't even render, not even a flash,
    // so some of these are just precautions. However in IE the element
    // is visible whilst the popup box asking the user for permission for
    // the web page to copy to the clipboard.
    //

    // Place in top-left corner of screen regardless of scroll position.
    textArea.style.position = 'fixed';
    textArea.style.top = 0;
    textArea.style.left = 0;

    // Ensure it has a small width and height. Setting to 1px / 1em
    // doesn't work as this gives a negative w/h on some browsers.
    textArea.style.width = '2em';
    textArea.style.height = '2em';

    // We don't need padding, reducing the size if it does flash render.
    textArea.style.padding = 0;

    // Clean up any borders.
    textArea.style.border = 'none';
    textArea.style.outline = 'none';
    textArea.style.boxShadow = 'none';

    // Avoid flash of white box if rendered for any reason.
    textArea.style.background = 'transparent';


    textArea.value = text;

    document.body.appendChild(textArea);

    textArea.select();

    try {
        document.execCommand('copy');
    } catch (err) {
        $.notify("Could not copy to clipboard\n" + err  , "error", {position: 'bottom right'});
    }

    document.body.removeChild(textArea);
}

function getUserDir(user_dir) {
    copyTextToClipboard(user_dir);
}

application.controller('malshabController', ["$scope", "$http", "$timeout",
    function ($scope, $http, $timeout) {

        var id = location.href.split("/").slice(-1);

        $http.get("/get_malshab_info/" + id).then(
            function successCallback(response) {
                $scope.malshab = response.data;
                document.title = ($scope.malshab.User + " - " + $scope.malshab.FirstName) + " - " + $scope.malshab.LastName
                $('#malshabLoadDialog').modal('hide');

                if ($scope.malshab.PassportID.length === 0 ||
                    $scope.malshab.FirstName === 0 ||
                    $scope.malshab.LastName === 0 ||
                    $scope.malshab.Gender === 0) {
                    $('#personal-info-toggle').click();
                }

                $scope.lowLevelMsg = "";
                $scope.highLevelMsg = "";
                $scope.blackBoxMsg = "";
                $scope.linuxMsg = "";
                $scope.webMsg = "";
                $scope.networksMsg = "";

                var allExModals = ['#HLModal','#LLModal', '#BBModal', '#LINModal', '#WEBModal', '#NETModal' ];

                function hideExercisesModals(current_modal) {
                    $(jQuery.grep(allExModals, function(value) {
                        return value != current_modal;
                    })).modal('hide');
                }

                function autofocusModalsText() {
                    allExModals.forEach(function(elem) {$(elem).on('shown.bs.modal', function() { $(this).find('textarea')[1].focus()})})
                }

                $(window).bind('keydown', function(event) {
                    if (event.ctrlKey || event.metaKey) {
                        switch (String.fromCharCode(event.which).toLowerCase()) {
                            case 's':
                                event.preventDefault();
                                $('#update-button').click();
                                break;
                        }

                        // check for enter
                        if (event.which == 13) {
                            if ($('#ll-msg').is(':focus')) {
                                $('#ll-msg-btn').click();
                            }
                            if ($('#hl-msg').is(':focus')) {
                                $('#hl-msg-btn').click();
                            }
                            if ($('#bb-msg').is(':focus')) {
                                $('#bb-msg-btn').click();
                            }
                            if ($('#lin-msg').is(':focus')) {
                                $('#lin-msg-btn').click();
                            }
                            if ($('#web-msg').is(':focus')) {
                                $('#web-msg-btn').click();
                            }
                            if ($('#net-msg').is(':focus')) {
                                $('#net-msg-btn').click();
                            }
                        }
                    }

                    else if (event.altKey) {
                        switch (String.fromCharCode(event.which).toLowerCase()) {
                            case '1':
                                event.preventDefault();
                                hideExercisesModals('#LLModal');
                                $('#LLModal').modal();
                                break;

                            case '2':
                                event.preventDefault();
                                hideExercisesModals('#HLModal');
                                $('#HLModal').modal();
                                break;

                            case '3':
                                event.preventDefault();
                                hideExercisesModals('#BBModal');
                                $('#BBModal').modal();
                                break;

                            case '4':
                                event.preventDefault();
                                hideExercisesModals('#LINModal');
                                $('#LINModal').modal();
                                break;

                            case '5':
                                event.preventDefault();
                                hideExercisesModals('#WEBModal');
                                $('#WEBModal').modal();
                                break;

                            case '6':
                                event.preventDefault();
                                hideExercisesModals('#NETModal');
                                $('#NETModal').modal();
                                break;
                        }
                    }
                });

                autofocusModalsText();

            },
            function (response) {
                alert("Failed to get malshab info");
            });
        $('#malshabLoadDialog').modal();

        // Reset missions function.
        $scope.resetExercise = function (missionId, exerciseName, userId) {
            if (confirm("Are you sure you want to reset the exercise " + exerciseName + "?") &&
                confirm("Please make sure you that you have backups\n" +
                    "of the solution files of your malshab if needed.\n" +
                    "You may cancel now and back them up.")) {
                $http.post("/reset_exercise/" + userId + "/" + missionId, '').then(
                    function successCallback() {
                        window.location.reload();
                        $('#pleaseWaitDialog').modal('hide');
                    }, errorCallback);
                $('#pleaseWaitDialog').modal();
            }
        };

        $scope.getUserDir = function (user_dir) {
            copyTextToClipboard(user_dir);
        }

        $scope.updateMalshab = function () {
            $http.post("/update_malshab", JSON.stringify($scope.malshab))
                .then(
                    function successCallback() {
                        $('.notifyjs-corner').empty();
                        $.notify("Changes saved!", "success", {position: 'bottom right'});
                    },
                    errorCallback);
            $.notify("Saving...", "info", {position: 'bottom right'});
        }

        $scope.missionIdToDescField = {
            1: "HLSummary",
            2: "LLSummary",
            3: "BlackBoxSummary",
            4: "LinuxSummary",
            5: "WebSummary",
            6: "NetworksSummary"
        }

        $scope.sendMessage = function(malshab_id, mission_id) {

            var message = "";
            var textarea = null;
            var $msg_field = null;

            switch (mission_id) {
                case 1:
                    message = $scope.highLevelMsg;
                    textarea = document.getElementById('hl-text');
                    $msg_field = $('#hl-msg');
                    break;
                case 2:
                    message = $scope.lowLevelMsg;
                    textarea = document.getElementById('ll-text');
                    $msg_field = $('#ll-msg');
                    break;
                case 3:
                    message = $scope.blackBoxMsg;
                    textarea = document.getElementById('bb-text');
                    $msg_field = $('#bb-msg');
                    break;
                case 4:
                    message = $scope.linuxMsg;
                    textarea = document.getElementById('lin-text');
                    $msg_field = $('#lin-msg');
                    break;
                case 5:
                    message = $scope.webMsg;
                    textarea = document.getElementById('web-text');
                    $msg_field = $('#web-msg');
                    break;
                case 6:
                    message = $scope.networksMsg;
                    textarea = document.getElementById('net-text');
                    $msg_field = $('#net-msg');
                    break;
            }

            if (message.length < 3) {
                $.notify("Message too short", "warning", {position: 'bottom right'});
                return;
            }

            $http.post("/send_message/" + malshab_id + "/" + mission_id, message)
                .then(
                    function successCallback(response) {
                        $('.notifyjs-corner').empty();
                        $.notify("Message received", "success", {position: 'bottom right'});
                        $scope.malshab[$scope.missionIdToDescField[mission_id]] = response.data;
                        $timeout(function () {
                            textarea.scrollTop = textarea.scrollHeight;
                            $msg_field.val("");
                        });
                    },
                    errorCallback);
            $.notify("Sending message...", "info", {position: 'bottom right'});
        }

        $scope.resetUser = function (user_id) {
            if (confirm("Are you sure you want to reset all user information for user id " + user_id  + "?")) {
                $http.post("/reset_user_info/" + user_id, '')
                    .then(
                        function successCallback() {
                            $('#pleaseWaitDialog').modal('hide');
                            window.location.reload();
                        },
                        errorCallback);
                $('#pleaseWaitDialog').modal();
            }
        }

        $scope.swapUsers = function (current_user_id) {
            var id = prompt("Insert a numeric user id to swap with (ie, 1,2,15..)");
            var numeric_id = parseInt(id);
            if (isNaN(numeric_id)) {
                $.notify("The inserted id: " + id + " is invalid", "error", {position: 'bottom right'});
                return;
            }

            if (confirm("Are you sure you want to swap all user information for user ids "
                    + current_user_id  + ", "
                    + id +"?")) {
                $http.post("/swap_users/" + current_user_id + "/" + id, '')
                    .then(
                        function successCallback(response) {
                            $('#pleaseWaitDialog').modal('hide');
                            $.notify(response.data, "info", {position: 'bottom right'});
                            if (response.data.indexOf("swapped successfully") != -1) {
                                setTimeout(function() { location.reload(); }, 2500);
                            }
                        },
                        errorCallback);
                $('#pleaseWaitDialog').modal();
            }
        }


        // Set malshab to the next level.
        $scope.nextLevel = function (missionId, user, currentLevel, maxLevel) {

            var errFunc = function (response) {
                $.notify("Could not advance to next stage, see log for response");
                console.log(response.data);
                $('#pleaseWaitDialog').modal('hide');
            };

            // Check for the various File API support.
            if (window.File && window.FileReader && window.FileList && window.Blob) {
                // Great success! All the File APIs are supported.
            } else {
                alert('The File APIs are not fully supported in this browser.');
                return;
            }

            if (currentLevel > maxLevel) {
                $.notify("All stages already cleared", "error", {position: 'bottom right'});
                return;
            }

            if (currentLevel == -1) {

                var data = JSON.stringify({
                    mission_id: missionId,
                    user: user,
                    file_name: "",
                    file_data: ""
                });

                $http.post("/next_level", data).then(
                    successCallbackWithWaitModal
                    , errFunc);

                $('#pleaseWaitDialog').modal();
            }

            else {
                var $file_input = $("#malshab-next-stage-upload");
                $file_input.unbind("change");

                $file_input.change(function(e){
                    var file = $file_input.prop('files')[0]

                    if (file.size == 0) {
                        $.notify("Cannot submit an empty file", "error");
                        return;
                    }

                    if (file.size > 1024 * 1024) {
                        $.notify("Uploaded file size cannot exceed 1MB", "error");
                        return;
                    }

                    var reader = new FileReader();
                    reader.onload = function(){

                        var data = JSON.stringify({
                            mission_id: missionId,
                            user: user,
                            file_name: file.name,
                            file_data: reader.result
                        });

                        $http.post("/next_level", data).then(
                            function(){
                                successCallbackWithWaitModal();
                            }
                            , errFunc);

                        $('#pleaseWaitDialog').modal();
                    }
                    reader.readAsBinaryString(file);
                });

                $file_input.click();
            }
        };

    }]);

$( document ).ready(function() {

    $("#workshop-info-toggle").click(function () {
        $("#workshop-info").toggle();
    });

    $("#convention-info-toggle").click(function () {
        $("#convention-info").toggle();
    });

    $("#personal-fields-toggle").click(function () {
        $("#personal-fields").toggle();
    });

});