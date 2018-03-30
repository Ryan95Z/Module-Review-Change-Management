// Function which iterates over each assessment and sets their numbers. This
// will correct them whenever an assessment is added or removed
function recalculateAssessmentNumbers() {
    var assessmentNumbers = $('.assessment-number');
    assessmentNumbers.each(function(index) {
        $(this).text("Assessment " + (index + 1))
    })
}

// When the form is submitted we remove any values in the support fields if 
// the support required checkbox is not checked.
$('#tracking-form').submit(function(event) {
    var lab_support_required = $('#id_lab_support_required').is(':checked')
    var tutorial_support_required = $('#id_tutorial_support_required').is(':checked')
    if(!lab_support_required) {
        $('#id_lab_support_skills').val('')
        $('#id_lab_support_notes').val('')
    }
    if(!tutorial_support_required) {
        $('#id_tutorial_support_skills').val('')
        $('#id_tutorial_support_notes').val('')
    }
})

// When an assessment is added or removed, trigger the recalculate function.
// This assumes that the dynamic form script is loaded before this one, so
// that is will trigger after a new form has been added.
$('body').on('click', '.add-row, .delete-row', function() {
    recalculateAssessmentNumbers()
});

// When the page first loads we need to check to see whether the lab/tutorial
// support fields should be shown or collapsed.
$(document).ready(function(){
    var changes_to_outcomes_checked = $('#id_changes_to_outcomes').is(':checked')
    var changes_to_teaching_checked = $('#id_changes_to_teaching').is(':checked')
    var changes_to_assessments_checked = $('#id_changes_to_assessments').is(':checked')
    var changes_other_checked = $('#id_changes_other').is(':checked')
    var lab_support_required = $('#id_lab_support_required').is(':checked')
    var tutorial_support_required = $('#id_tutorial_support_required').is(':checked')
    if(changes_to_outcomes_checked) {
        $('#changes_to_outcomes_collapse').addClass('show')
    }
    if(changes_to_teaching_checked) {
        $('#changes_to_teaching_collapse').addClass('show')
    }
    if(changes_to_assessments_checked) {
        $('#changes_to_assessments_collapse').addClass('show')
    }
    if(changes_other_checked) {
        $('#changes_other_collapse').addClass('show')
    }
    if(lab_support_required) {
        $('#lab_support_collapse').addClass('show')
    }
    if(tutorial_support_required) {
        $('#tutorial_support_collapse').addClass('show')
    }
})