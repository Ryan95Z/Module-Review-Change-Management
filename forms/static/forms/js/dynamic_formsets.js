function updateIndex(element, prefix, newIndex) {
    var regex = new RegExp('(' + prefix + '-\\d+)');
    var replacement = prefix + "-" + newIndex;
    if(element.id) element.id = element.id.replace(regex, replacement)
    if(element.name) element.name = element.name.replace(regex, replacement)
}
function recalculateIndexes(prefix) {
    var formRows = $('.form_row');
    for(var i=0, rowCount=formRows.length; i<rowCount; i++) {
        $(formRows.get(i)).find(':input').each(function() {
            updateIndex(this, prefix, i)
        })
    }
}
function recalculateOrder() {
    var rowOrderFields = $('.row-order');
    var order = 1;
    rowOrderFields.each(function() {
        $(this).text(order);
        order++;
    })
}
function deleteFormRow(deleteButton) {
    var total_forms = $('#id_form-TOTAL_FORMS').val();
    $('#id_form-TOTAL_FORMS').val(total_forms - 1);
    deleteButton.closest(".form_row").remove()
    recalculateIndexes('form')
}
function shiftUp(upButton) {
    var currentIndex = $("#form_set .move-up").index(upButton)
    if(currentIndex < 2) {
        $('#form_set').prepend(upButton.closest(".form_row"));
    } else {
        $(upButton.closest(".form_row")).insertAfter(".form_row:eq("+ (currentIndex -2) + ")")
    }
    recalculateIndexes('form')
}
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
$('#add_row').click(function() {
    var form_id = $('#id_form-TOTAL_FORMS').val();
    var form_order = $('#id_form-TOTAL_FORMS').val();
    $('#form_set').append($('#empty_form').html().replace(/__prefix__/g, form_id));
    $('#id_form-TOTAL_FORMS').val(parseInt(form_id) + 1);
    $('#id_form-'+form_id+'-entity_order').val(form_order);
    recalculateOrder();
    
});

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