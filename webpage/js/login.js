async function sendRequest(){

    let phpFile = `http://${location.host}/api/public/TokenConfiguration.php`;
    let response = await (await fetch(phpFile)).json();
    var token = response.result.replace(/\n/g, '');

    var username = document.getElementById("tbUsername").value;
    var password = document.getElementById("tbPassword").value;
    var url = `http://${location.host}:8080/login/${username}/${password}`;

    let loginResponse = await (await fetch(url, {
        method: 'GET',
        headers:{
            "Access-Control-Allow-Origin": "*",
            "Content-Type": "application/json; charset=UTF-8",
            "Authorization": token
        }
    })).json();
    console.log(loginResponse);

    login(loginResponse);

    return false;
}

function login(response){
    var label = document.getElementById("lblLoginStatus");

    if(response.status){
        window.open(`http://${location.host}/index.php?session=${response.sessionId}`, "_self");
    }
    else{
        label.innerHTML = "Uw wachtwoord of gebruikersnaam is verkeerd.";
    }
}

(function ($) {
    "use strict";


    /*==================================================================
    [ Validate ]*/
    var input = $('.validate-input .input100');

    $('.validate-form').on('submit',function(){
        var check = true;

        for(var i=0; i<input.length; i++) {
            if(validate(input[i]) == false){
                showValidate(input[i]);
                check=false;
            }
        }

        return check;
    });


    $('.validate-form .input100').each(function(){
        $(this).focus(function(){
           hideValidate(this);
        });
    });

    function validate (input) {
        if($(input).attr('type') == 'email' || $(input).attr('name') == 'email') {
            if($(input).val().trim().match(/^([a-zA-Z0-9_\-\.]+)@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.)|(([a-zA-Z0-9\-]+\.)+))([a-zA-Z]{1,5}|[0-9]{1,3})(\]?)$/) == null) {
                return false;
            }
        }
        else {
            if($(input).val().trim() == ''){
                return false;
            }
        }
    }

    function showValidate(input) {
        var thisAlert = $(input).parent();

        $(thisAlert).addClass('alert-validate');
    }

    function hideValidate(input) {
        var thisAlert = $(input).parent();

        $(thisAlert).removeClass('alert-validate');
    }
    
    

})(jQuery);