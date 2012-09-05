$(function() {
    $('#btn-new-job').click(btnNewJobTapped);
});

var btnNewJobTapped = function() {
    document.location.href = '/application/' + $('#app-name').val() + '/job/new';
};

var generateWorkunits = function(job_id) {
    document.location.href = '/application/' + $('#app-name').val() + '/job/' + job_id + '/generate_workunits';
};