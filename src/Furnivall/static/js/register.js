$(function() {
    $('#btn-save-user').click(btnSaveUserTapped);
});

var btnSaveUserTapped = function() {
    $('#form-save-user').submit();
};