//Prototype overrides
Array.prototype.diff = function(a) {
    return this.filter(function(i) {return a.indexOf(i) < 0;});
};

//BEGIN REFRESH ENTRIES\\
function refreshEntriesTable() {
  url = "../api/Games";
  $.ajax({
    url: url,
    success: handleRefreshEntries,
    error: function(jqXHR, textStatus, errorThrown) {
      window.alert("post error: " + textStatus);
    }
  });
}

function handleRefreshEntries(data) {
  for (i=0; i<data.length; i++) {
    var e = data[i];
    $("<tr></tr>").append("<td>"+e.opponent+"</td><td>"+e.game_date+"</td>").appendTo( '#entries-table tbody' );
  }
}
//END REFRESH ENTRIES\\

//BEGIN CREATE NEW ENTRY\\
function submitEntry() {
  var FIELDS = ["game_id","inning","pitcher_id","shutdown_inning",
                "less_than_13_pitches","retired_first_batter",
                "three_and_out","strikeouts","ended_inning"];

  //extract values from form
  var entryMap = getFormValues(FIELDS);
  window.alert("diff: " + FIELDS.diff(["game_id","inning","pitcher_id"]));
  clearFormValues(FIELDS.diff(["game_id","inning","pitcher_id"]));

  window.alert("form: " + JSON.stringify(entryMap)); 

  $.ajax({
    type: "POST",
    url: "../api/PitcherInnings",
    data: JSON.stringify(entryMap),
    dataType: "json",
    success: function(data, textStatus, jqXHR) {
      window.alert("post success: " + JSON.stringify(data) + " | " + textStatus);
      refreshEntriesTable();
    },
    error: function(jqXHR, textStatus, errorThrown) {
      window.alert("post error: " + textStatus);
    }
  });

  
}

function getFormValues(fields) {
  var entryMap = {}; 
  for (i=0; i<fields.length; i++) {
    var e = $("#in_"+fields[i]);
    var val = null;
    if (e.prop('type') == "checkbox") {
      val = e.prop('checked');
    } else {
      val = e.val();  
    }
    entryMap[fields[i]] = val;
  }
  return entryMap;
}

function clearFormValues(fields) {
  for (i=0; i<fields.length; i++) {
    var e = $("#in_"+fields[i]);
    var val = null;
    if (e.prop('type') == "checkbox") {
      e.prop('checked',false);
    } else if (e.prop('type') == "select-one") {
//      window.alert("select one: " + e[0].prop('value'));
//      e[0].selectedIndex = 0;
      //e.filter(":first").prop('selected',true);
      //TODO: Fix this to be dynamic
      val = e.val('');  
    } else {
      val = e.val('');  
    }
  }
  return 0;
}
//END CREATE NEW ENTRY\\
