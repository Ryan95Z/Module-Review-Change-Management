var deleted_records = []

// Takes a given elemenet, id prefix (for regex) and a new index
// and replaces all instances of child elements with the updated id
function updateIndex(element, prefix, newIndex) {
    var regex = new RegExp('(' + prefix + '-\\d+)');
    var replacement = prefix + "-" + newIndex;
    if(element.id) element.id = element.id.replace(regex, replacement)
    if(element.id.endsWith("id")) {
        if(!element.value && deleted_records.length > 0) {
            element.value = deleted_records.pop()
        }
    }
    if(element.name) element.name = element.name.replace(regex, replacement)
}
// Loops through each row and updates it's indexes so that they
// are sequential
function recalculateIndexes(formPrefix) {
    var formRows = $('#'+formPrefix+'-dynamic_form .dynamic-row');
    for(var i=0, rowCount=formRows.length; i<rowCount; i++) {
        formRow = $(formRows.get(i))
        $(formRows.get(i)).find(':input').each(function() {
            updateIndex(this, formPrefix, i)
        })

    }
}
// This function manages the order column. It updates
// all of the numbers so that they always remain consistent, and
// disables/reenables the up and down buttons. It also updates the
// value of the hidden order field. 
function recalculateOrder(formPrefix) {
    var rowOrderFields = $('.row-order');
    var total_forms = $('#id_'+formPrefix+'-TOTAL_FORMS').val();

    rowOrderFields.each(function(order) {
        $('#id_'+formPrefix+'-'+order+'-entity_order').val(order)
        $(this).text(order + 1);
        $(this).siblings(".move-up").prop('disabled', false)
        $(this).siblings(".move-down").prop('disabled', false)
        if(order == 0) {
            $(this).siblings(".move-up").prop('disabled', true)
        } 
        if(order + 1 >= total_forms) {
            $(this).siblings(".move-down").prop('disabled', true)
        }
    })
}
// Adds an additional row to the form, and updates all required ids
// for the form set. It creates the row by copying the empty form
function createFormRow(formPrefix) {
    var form_id = $('#id_'+formPrefix+'-TOTAL_FORMS').val();
    var form_order = $('#id_'+formPrefix+'-TOTAL_FORMS').val();
    $('#'+formPrefix+'-dynamic_form').append($('#'+formPrefix+'-empty_form').html().replace(/__prefix__/g, form_id));
    $('#id_'+formPrefix+'-TOTAL_FORMS').val(parseInt(form_id) + 1);
    $('#id_'+formPrefix+'-'+form_id+'-entity_order').val(form_order);
    recalculateIndexes(formPrefix)
}
// Removes a row and updates ids
function deleteFormRow(deleteButton, formPrefix) {
    row_id = deleteButton.closest(".dynamic-row").find(".dynamic-row-id").val()
    if(row_id) deleted_records.push(row_id)
    var total_forms = $('#id_'+formPrefix+'-TOTAL_FORMS').val();
    $('#id_'+formPrefix+'-TOTAL_FORMS').val(total_forms - 1);
    deleteButton.closest(".dynamic-row").remove()
    recalculateIndexes(formPrefix)
}
// Switches the position of the chosen row with the one above it, 
// unless it is the top element
function shiftUp(upButton, formPrefix) {
    var currentIndex = $('#'+formPrefix+'-dynamic_form .move-up').index(upButton)
    if(currentIndex < 2) {
        $('#'+formPrefix+'-dynamic_form').prepend(upButton.closest(".dynamic-row"));
    } else {
        $(upButton.closest(".dynamic-row")).insertAfter(".dynamic-row:eq("+ (currentIndex -2) + ")")
    }
    recalculateIndexes(formPrefix)
}
// Switches the position of the chosen row with the one below it, 
// unless it is the bottom element
function shiftdown(downButton, formPrefix) {
    var currentIndex = $('#'+formPrefix+'-dynamic_form .move-down').index(downButton)
    var totalForms = $('#id_'+formPrefix+'-TOTAL_FORMS').val();
    if(currentIndex >= totalForms - 1) {
        $('#'+formPrefix+'-dynamic_form').append(downButton.closest(".dynamic-row"));
    } else {
        $(downButton.closest(".dynamic-row")).insertAfter(".dynamic-row:eq("+ (currentIndex + 1) + ")")
    }
    recalculateIndexes(formPrefix)
}

// Setting up the event handlers. 
// All dynamically generated elements must use '.on()' instead of .click
$('body').on('click', '.add-row', function() {
    var formPrefix = $(this).attr("name")
    createFormRow(formPrefix)
    recalculateOrder(formPrefix);
});
$('body').on('click', '.delete-row', function() {
    var formPrefix = $(this).attr("name")
    deleteFormRow($(this), formPrefix)
    recalculateOrder(formPrefix)
})
$('body').on('click', '.move-up', function() {
    var formPrefix = $(this).attr("name")
    shiftUp($(this), formPrefix)
    recalculateOrder(formPrefix)
})
$('body').on('click', '.move-down', function() {
    var formPrefix = $(this).attr("name")
    shiftdown($(this), formPrefix)
    recalculateOrder(formPrefix)
})
