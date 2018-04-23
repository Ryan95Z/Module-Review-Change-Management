// Determines whether or not the choice field should be enabled
// depending on the value of the type field.
function evaluateTypeField(typeField) {
    var select_id = typeField.attr("id")
    var row_id = select_id.substring(0, select_id.lastIndexOf("-"))
    if(typeField.val() == 'multi-choice' || typeField.val() == 'radio-buttons') {
        $("#"+row_id+"-entity_choices").attr("disabled", false)
    } else {
        $("#"+row_id+"-entity_choices").val("")
        $("#"+row_id+"-entity_choices").attr("disabled", true)
    }

    if(typeField.val() == 'multi-choice' || typeField.val() == 'radio-buttons' || typeField.val() == 'check-box') {
        var max_length = 0
        var choices = $("#"+row_id+"-entity_choices").val().split(",")
        for (var i = 0; i < choices.length; i++) {
            if (choices[i].trim().length > max_length) max_length = choices[i].trim().length
        }
        if(typeField.val() == 'check-box') $("#"+row_id+"-entity_max_length").val(1)
        else $("#"+row_id+"-entity_max_length").val(max_length)
        $("#"+row_id+"-entity_max_length").attr("readonly", true)
    } else {
        $("#"+row_id+"-entity_max_length").val(500)
        $("#"+row_id+"-entity_max_length").attr("readonly", false)
    }

}

// Whenever a select box is changed or created, check the choice field
// Likewise, if an input changes, we want to do the same
$('table').on('change load', 'select', function() {
    evaluateTypeField($(this))
})
$('table').on('change', '.choices-field input', function() {
    var input_id = $(this).attr("id")
    var select_id = input_id.replace("entity_choices", "entity_type")
    evaluateTypeField($('#' + select_id))
})

// When the page loads, check all of the choice fields
$(document).ready(function(){
    $(".type-field select").each(function() {
        evaluateTypeField($(this))
    })

})