$(document).ready(function(){
    function getCookie(name) {
        const value = `; ${document.cookie}`;
        console.log(value);
        const parts = value.split(`; ${name}=`);
        if (parts.length === 2) return parts.pop().split(';').shift();
    }
    let csrf_token;
    $.get('/', function(response){
        csrf_token = getCookie("CSRF-TOKEN");
    });
    $('#confirm_button').click(function(){
        let user_email = $('input[name=user_email]').val();
        let new_password = $('input[name=new_password]').val();
        let confirm_password = $('input[name=confirm_password]').val();
        if (new_password != confirm_password){
            alert('Passwords do not match');
            return false;
        }
        $.ajax({
            type: 'PATCH',
            url: '/changePassword',
            headers: {
                'X-CSRF-Token': csrf_token
            },
            data: JSON.stringify({
                'email': user_email,
                'newPassword': new_password,
                'confirmPassword': confirm_password
            }),
            contentType: 'application/json',
            dataType: 'json',
            success: function(response){
                alert(response['message']);
            },
            error: function(error){
                console.log(error);
            }
        });
        $('input[name=user_email]').val("");
        $('input[name=new_password]').val("");
        $('input[name=confirm_password]').val("");
    });
})