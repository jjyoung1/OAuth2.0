 console.log('login.js loaded')

function signInCallback(authResult) {
    if (authResult['code']) {
        // Hide the sign-in button now that the user is authorized
//        $('#signInButton').attr('style', 'display: none');

        // Send the one-time-use code to the server, if the server
        // responds, write a 'login successful' message to the web page
        // and then redirect back to the main restaurants page
        $.ajax({
            type: 'POST',
            url: '/gconnect?state=' + STATE,
            processData: false,  // Don't want jQuery to process the response into a string
            contentType: 'application/octet-stream; charset=utf-8', // indicates we're sending an arbitrary stream of data
            data: authResult['code'],
            // when we receive a 200 or successful response code from our server run the function
            success: function (result) {
                if (result) {
                    $('#result').html('Login Successful!</br>' + result + '</bt>Redirecting...');
                    setTimeout(function () {
                        window.location.href = "/restaurant";
                    }, 4000);
                } else if (authResult['error']) {
                    console.log('There was an error: ' + authResult['error']);
                } else {
                    $('#result').html('Failed to make a server-side call,' +
                        'Check your configuration and console.');
                }
            }
        });
    }
}

window.fbAsyncInit = function () {
    FB.init({
        appId: '1900210546966002',
        cookie: true,
        xfbml: true,
        version: 'v2.2'
    });
    FB.AppEvents.logPageView();
};

(function (d, s, id) {
    var js, fjs = d.getElementsByTagName(s)[0];
    if (d.getElementById(id)) {
        return;
    }
    js = d.createElement(s);
    js.id = id;
    // js.src = "//connect.facebook.net/en_US/sdk.js";
    js.src = "//connect.facebook.net/en_US/sdk/debug.js";
    fjs.parentNode.insertBefore(js, fjs);
}(document, 'script', 'facebook-jssdk'));

// Here we run a very simple test of the Graph API after login is
// successful.  See statusChangeCallback() for when this call is made.
function sendTokenToServer(state) {
    var access_token = FB.getAuthResponse()['accessToken'];
    console.log(access_token)
    console.log('Welcome!  Fetching your information.... ');
    FB.api('/me', {fields: 'id, name'}, function (response) {
        console.log('(FB.api)Successful login for: ' + response.name);
        $.ajax({
            type: 'POST',
            url: '/fbconnect?state=' + state,
            processData: false,
            data: access_token,
            contentType: 'application/octet-stream; charset=utf-8',
            success: function (result) {
                // Handle or verify the server response if necessary.
                if (result) {
                    $('#result').html('Login Successful!</br>' + result + '</br>Redirecting...')
                    setTimeout(function () {
                        window.location.href = "/restaurant";
                    }, 4000);


                } else {
                    $('#result').html('Failed to make a server-side call. Check your configuration and console.');
                }
            }
        });
    });
}

