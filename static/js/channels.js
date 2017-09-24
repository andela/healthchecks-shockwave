$(function() {
    var placeholders = {
        email: "address@example.org",
        webhook: "http://",
        slack: "https://hooks.slack.com/...",
        hipchat: "https://api.hipchat.com/...",
        pd: "service key"
    }

    $("#add-channel-kind").change(function() {
        $(".channels-add-help p").hide();

        var v = $("#add-channel-kind").val();
        $(".channels-add-help p." + v).show();

        $("#add-channel-value").attr("placeholder", placeholders[v]);
    });

    $(".edit-checks").click(function() {
        $("#checks-modal").modal("show");
        var url = $(this).attr("href");
        $.ajax(url).done(function(data) {
            $("#checks-modal .modal-content").html(data);

        })


        return false;
    });


    $(".edit-delete-webhooks").click(function() {
        $("#webhooks-modal").modal("show");
        var url = $(this).attr("href");
        $.ajax(url).done(function(data) {
            $("#webhooks-modal .modal-content").html(data);

        })

        return false;
    });


    $(".add-webhook").click(function() {
        $("#add-webhooks-modal").modal("show");
        var url = $(this).attr("href");
        $.ajax(url).done(function(data) {
            $("#add-webhooks-modal .modal-content").html(data);

        })

        return false;
    });


    var $cm = $("#checks-modal");
    $cm.on("click", "#toggle-all", function() {
        var value = $(this).prop("checked");
        $cm.find(".toggle").prop("checked", value);
        console.log("aaa", value);

    });

    $(".channel-remove").click(function() {
        var $this = $(this);

        $("#remove-channel-form").attr("action", $this.data("url"));
        $(".remove-channel-name").text($this.data("name"));
        $('#remove-channel-modal').modal("show");

        return false;
    });


    $(".integration-remove").click(function() {
        var $this = $(this);

        $("#remove-integration-form").attr("action", $this.data("url"));
        $(".remove-integration-name").text($this.data("name"));
        $('#remove-integration-modal').modal("show");

        return false;
    });

    $('[data-toggle="tooltip"]').tooltip();

});