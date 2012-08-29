$(function() {
    $('#btn-new-job').click(btnNewJobTapped);
});

var btnNewJobTapped = function() {
    document.location.href = '/application/' + $('#app-name').val() + '/job/new';
};