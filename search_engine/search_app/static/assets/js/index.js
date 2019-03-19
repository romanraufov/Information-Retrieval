// Insert jquery Ajax calls here\

// Document ready -> wait for entire page to load before installing the event handlers.
$(function () {

    // Variable to hold request
    var request;

    $("#postData").submit(function(event) {

        // Prevent default posting of form - put here to work in case of errors
        event.preventDefault();

        // Abort any pending request
        if (request) {
            request.abort();
        }
        // setup some local variables
        var $form = $(this);

        // Let's select and cache all the fields
        var $inputs = $form.find("input, select, button, textarea");

        // Serialize the data in the form
        var serializedData = $form.serialize();

        // Let's disable the inputs for the duration of the Ajax request.
        // Note: we disable elements AFTER the form data has been serialized.
        // Disabled form elements will not be serialized.
        //$inputs.prop("disabled", true);
        $inputs.prop("disabled", false);

        // Fire off the request to /form.php
        request = $.ajax({
            url: "members_of_parliament.php",
            type: "post",
            data: serializedData
        });

        // Callback handler that will be called on success
        request.done(function (response, textStatus, jqXHR){
            // Log a message to the console
            $(".jq-pmember").html(response)
        });


        // Callback handler that will be called on failure
        request.fail(function (jqXHR, textStatus, errorThrown){
            // Log the error to the console
            console.error(
                "The following error occurred: "+
                textStatus, errorThrown
            );
        });

        // Callback handler that will be called regardless
        // if the request failed or succeeded
        request.always(function () {
            // Reenable the inputs
            $inputs.prop("disabled", false);
        });

    });

    // // Bind to the submit event of our form
    // $("#foo").submit(function(event){
    //
    //     // Prevent default posting of form - put here to work in case of errors
    //     event.preventDefault();
    //
    //     // Abort any pending request
    //     if (request) {
    //         request.abort();
    //     }
    //     // setup some local variables
    //     var $form = $(this);
    //
    //     // Let's select and cache all the fields
    //     var $inputs = $form.find("input, select, button, textarea");
    //
    //     // Serialize the data in the form
    //     var serializedData = $form.serialize();
    //
    //     // Let's disable the inputs for the duration of the Ajax request.
    //     // Note: we disable elements AFTER the form data has been serialized.
    //     // Disabled form elements will not be serialized.
    //     $inputs.prop("disabled", true);
    //
    //     // Fire off the request to /form.php
    //     request = $.ajax({
    //         url: "test.php",
    //         type: "post",
    //         data: serializedData
    //     });
    //
    //     // Callback handler that will be called on success
    //     request.done(function (response, textStatus, jqXHR){
    //         // Log a message to the console
    //         $(".jq-append").html(response)
    //
    //     });
    //
    //     // Callback handler that will be called on failure
    //     request.fail(function (jqXHR, textStatus, errorThrown){
    //         // Log the error to the console
    //         console.error(
    //             "The following error occurred: "+
    //             textStatus, errorThrown
    //         );
    //     });
    //
    //     // Callback handler that will be called regardless
    //     // if the request failed or succeeded
    //     request.always(function () {
    //         // Reenable the inputs
    //         $inputs.prop("disabled", false);
    //     });
    //
    // });

    // press enter to search
    $('body').keypress(function(event){ 
        var keyCode = (event.keyCode ? event.keyCode : event.which);   
        if (keyCode == 13) {
            $('#search_button').trigger('click');
        }
    });

    //TODO: build further on this jquery to enable pop-out of this element with clicked elements
    $(document).on("click",'.card', function(){
        console.log("#on click .card is clicked", $(this));
    })





});
