$(function() {
    $('#btn-login').click(btnLoginTapped);
    $('#btn-register').click(btnRegisterTapped);
});

var btnLoginTapped = function() {
    $('#form-login').submit();
};

var btnRegisterTapped = function() {
    location.href = '/register';
};