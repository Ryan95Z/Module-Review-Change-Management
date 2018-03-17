// Determines whether or not the choice field should be enabled
// depending on the value of the type field.
function evaluateChoiceField(typeField) {
    var select_id = typeField.attr("id")
    var row_id = select_id.substring(0, select_id.length - "-entity_type".length)
    if(typeField.val() == 'multi-choice' || typeField.val() == 'check-boxes') {
        $("#"+row_id+"-entity_choices").attr("disabled", false)
    } else {
        $("#"+row_id+"-entity_choices").val("")
        $("#"+row_id+"-entity_choices").attr("disabled", true)
    }
}

// Whenever a select box is changed or created, check the choice field
$('table').on('change load', 'select', function() {
    evaluateChoiceField($(this))
})

// When the page loads, check all of the choice fields
$(document).ready(function(){
    $(".type-field select").each(function() {
        evaluateChoiceField($(this))
    })
})