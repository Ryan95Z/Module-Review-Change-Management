// Takes a given elemenet, id prefix (for regex) and a new index
// and replaces all instances of child elements with the updated id
function updateIndex(element, prefix, newIndex) {
    var regex = new RegExp('(' + prefix + '-\\d+)');
    var replacement = prefix + "-" + newIndex;
    if(element.id) element.id = element.id.replace(regex, replacement)
    if(element.name) element.name = element.name.replace(regex, replacement)
}
// Loops through each row and updates it's indexes so that they
// are sequential
function recalculateIndexes(prefix) {
    var formRows = $('.form_row');
    for(var i=0, rowCount=formRows.length; i<rowCount; i++) {
        $(formRows.get(i)).find(':input').each(function() {
            updateIndex(this, prefix, i)
        })
    }
}
// This function manages the order column. It updates
// all of the numbers so that they always remain consistent, and
// disables/reenables the up and down buttons 
function recalculateOrder() {
    var rowOrderFields = $('.row-order');
    var total_forms = $('#id_form-TOTAL_FORMS').val();

    var order = 1;
    rowOrderFields.each(function() {
        $(this).text(order);
        $(this).siblings(".move-up").prop('disabled', false)
        $(this).siblings(".move-down").prop('disabled', false)
        if(order - 1 == 0) {
            $(this).siblings(".move-up").prop('disabled', true)
        } 
        if(order >= total_forms) {
            $(this).siblings(".move-down").prop('disabled', true)
        }
        order++;
    })
}
// Adds an additional row to the form, and updates all required ids
// for the form set. It creates the row by copying the empty form
function createFormRow() {
    var form_id = $('#id_form-TOTAL_FORMS').val();
    var form_order = $('#id_form-TOTAL_FORMS').val();
    $('#form_set').append($('#empty_form').html().replace(/__prefix__/g, form_id));
    $('#id_form-TOTAL_FORMS').val(parseInt(form_id) + 1);
    $('#id_form-'+form_id+'-entity_order').val(form_order);
    recalculateIndexes('form')
}
// Removes a row and updates ids
function deleteFormRow(deleteButton) {
    var total_forms = $('#id_form-TOTAL_FORMS').val();
    $('#id_form-TOTAL_FORMS').val(total_forms - 1);
    deleteButton.closest(".form_row").remove()
    recalculateIndexes('form')
}
// Switches the position of the chosen row with the one above it, 
// unless it is the top element
function shiftUp(upButton) {
    var currentIndex = $("#form_set .move-up").index(upButton)
    if(currentIndex < 2) {
        $('#form_set').prepend(upButton.closest(".form_row"));
    } else {
        $(upButton.closest(".form_row")).insertAfter(".form_row:eq("+ (currentIndex -2) + ")")
    }
    recalculateIndexes('form')
}
// Switches the position of the chosen row with the one below it, 
// unless it is the bottom element
function shiftdown(downButton) {
    var currentIndex = $("#form_set .move-down").index(downButton)
    var totalForms = $('#id_form-TOTAL_FORMS').val();
    if(currentIndex >= totalForms - 1) {
        $('#form_set').append(downButton.closest(".form_row"));
    } else {
        $(downButton.closest(".form_row")).insertAfter(".form_row:eq("+ (currentIndex + 1) + ")")
    }
    recalculateIndexes('form')
}

// Setting up the event handlers. 
$('#add_row').click(function() {
    createFormRow()
    recalculateOrder();
});

// All generated elements must use '.on()' instead of .click
$('table').on('click', '.delete-row', function() {
    deleteFormRow($(this))
    recalculateOrder()
})
$('table').on('click', '.move-up', function() {
    shiftUp($(this))
    recalculateOrder()
})
$('table').on('click', '.move-down', function() {
    shiftdown($(this))
    recalculateOrder()
})
