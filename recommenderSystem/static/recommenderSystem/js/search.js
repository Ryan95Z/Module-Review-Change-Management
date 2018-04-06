function getLastInputRow() {
  var rows = $("#software_form-dynamic_form .dynamic-row");
  if (rows.length > 0) { //check if rows has length of more than 0
    var last = $(rows[rows.length - 1]);

    var hasContent = false; // loop over each input to see if it is empty - we don't want to overwrite
    last.find('input').each(function () {
      if (!hasContent && $(this).val()) {
        hasContent = true;
      }
    });
    $("#add-button").click(); //this ensures that each time you click there is a new emtpy row for the user
    if (!hasContent) {
      return last; //return the last empty row if found.
    }
    else {

      return getLastInputRow(); //if no empty row was found previously, then a new row was created so now return the last one
    }
  }
}
  $(function() {
    $("#software-search-button").click(function (e) {
      /*
        Catch the search click, send request to backend via AJAX
      */
      e.preventDefault()
      var search_term = $("#id_software_name").val();
      $("#search-results").html("<br> <div class='row'>" +
        "<div class='col-md-3'>Software</div>" +
        "<div class='col-md-3'>Module</div>" +
        "<div class='col-md-3'>Package</div>" +
        "<div class='col-md-3'>Version</div>" +
        "</div>");
      // this is the request to the backend
      $.get('/module_leader/software-search/?search_term=' + search_term, function (response) {
        /* for each result, add a row */
        var items = JSON.parse(response);
        if (items.results.length === 0) {
          $("#search-results").html("<div class='alert alert-danger'>No results founds</div>");
        }
        items.results.forEach(function (item) {
          var row = $("<div class='row'>" +
            "<div class='col-md-3'>" + item.software + "</div>" +
            "<div class='col-md-3'>" + item.module + "</div>" +
            "<div class='col-md-3'>" + item.package + "</div>" +
            "<div class='col-md-3'>" + item.version + "</div>" +
            "</div>");
            $("#search-results").append(row);
            row.click(function () {
              /* when a row is clicked, find the last empty row of data to enter */
              inputRow = getLastInputRow();
              var arr = [item.software, item.version, item.package];
              counter = 0;
              inputRow.find('input[type=text]').each(function () {
                /* insert values into the columns */
                $(this).val(arr[counter]);
                counter++;
              })
            })

        })
      })
    })
  })
