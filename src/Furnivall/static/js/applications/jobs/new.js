$(function(){
    $('#btn-save-job').click(btnSaveJobTapped);
});

var btnSaveJobTapped = function() {
    $('#form-save-job').submit();
};