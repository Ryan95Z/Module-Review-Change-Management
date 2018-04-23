function getLastInputRow() {
  //select rows by id
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
  // ensure that the function is called once all the DOM elements of the page are ready
  $(function() {
    //e = event oject which will be passed to handler
    $("#software-search-button").click(function (e) {
      /*
        Catch the search click, send request to backend via AJAX
      */
      e.preventDefault() //prevent from submitting a form
      var search_term = $("#id_software_name").val(); //create a variable and store value of software name in it
      //set the HTML content of each matched element
      $("#search-results").html(
        "<br> <table class='table'>" + "<thead class='thead-light'>" + "<tr>" +
        "<th scope='col' style='font-weight: bold; text-align: left;'>Software</th>" +
        "<th scope='col' style='font-weight: bold; text-align: left;'>Module name</th>" +
        "<th scope='col' style='font-weight: bold; text-align: left;'>Package</th>" +
        "<th scope='col' style='font-weight: bold; text-align: left;'>Version</th>" +
        "</tr>" +
        "<thead>" +
        "</table>");
      // this is the request to the backend
      $.get('/module_leader/software-search/?search_term=' + search_term, function (response) {
        /* for each result, add a row */
        var items = JSON.parse(response); //parse data to javascript object and store it in 'items'
        // show alert if no results are found
        if (items.results.length === 0) {
          $("#search-results").html("<div class='alert alert-danger'>No results founds</div>");
        }
        //executes the function once for each array element.
        items.results.forEach(function (item) {
          var row = $("<table class='table table-hover table-bordered'  style='border-left: 6px solid black;'>" +
          "<tbody>" + "<tr>" +
            "<th width='20%' scope='col' style='font-weight: bold; text-transform: uppercase;' id='s_name'>" + item.software + "</th>" +
            "<th width='30%' scope='col' style='background-color: #f0f3f5; '>" + item.module + "</th>" +
            "<th width='20%' scope='col' style='font-weight: bold;'>" + item.package + "</th>" +
            "<th width='20%' scope='col' style='font-weight: bold; color:red; background-color: #f0f3f5; '>" + item.version + "</th>" +
            "</tr>" +
            "</tbody>" +
            "</table>");
            $("#search-results").append(row);
            $("tbody").hover(function(){
              $(this).css("cursor", "pointer");
            });
            row.click(function () {
              /* when a row is clicked, find the last empty row of data to enter */
              inputRow = getLastInputRow();
              var arr = [item.software, item.version, item.package];
              counter = 0;
              inputRow.find('input[type=text]').each(function () {
                /* insert values into the columns */
                $(this).val(arr[counter]);
                counter++;
                $(this).css("background", "#f7e0da");
              })
              // alert user that selected option is added
              alert("Option is added");
            })
        })
      })
    })
  })
