$( document ).ready(function() {

  allIngr = []
  //get all unique ingr and append to search list
  $.get('/getIngredients',  // url
      function (data, textStatus, jqXHR) {  // success callback
          //alert('status: ' + textStatus + ', data:' + data);
          allIngr = data.data;
          for (var key in allIngr) {
            var optionElement = document.createElement("option");
            optionElement.value = allIngr[key];
            document.getElementById("allIngr").appendChild(optionElement);
          }
  });

  //Get Unique Ingredients list
  function getIngredients() {
    $.get('/getIngredients',  // url
      function (data, textStatus, jqXHR) {  // success callback
          //alert('status: ' + textStatus + ', data:' + data);
          return data.data;
    });
  }

  $("#recommed-button").click(function(){
    //alert("recommend something");
    var ul = document.getElementById("final-recipe");
    var items = ul.getElementsByTagName("li");
    var ingr = []
    for (i = 0; i < items.length; i++) {
        ingr.push(items[i].innerText);
    }

    $.post( "/recommendTopIngr", {
     list_ingr: JSON.stringify(ingr)
    }, function(err, req, resp){
      var obj = JSON.parse(resp.responseText)
      var key = Object.keys(obj)[0];
      alert(obj[key]);
      $('#eval_score').val(parseFloat(key).toFixed(2));
      //window.location.href = "/results/"+resp["responseJSON"]["uuid"];
    });
  });

  $("#add-ingr").click(function(){
    //alert("adding items");
    var item = $("#searchBar").val();
    var row = "<li class='list-group-item'>" + item + "</li>";
    $("#final-recipe").append(row);
  });

  $('#surprise-button').click(function(){
    // Shuffle array
    var shuffled = allIngr.sort(() => 0.5 - Math.random());
    // Get sub-array of first n elements after shuffled
    var selectedIngr = shuffled.slice(0, 3);
    $("#try-ingrList").html("");
    for(var ingr in selectedIngr){
      var row = "<li class='list-group-item'>" + selectedIngr[ingr] + "</li>";
      $("#try-ingrList").append(row);
    }
  });

});
