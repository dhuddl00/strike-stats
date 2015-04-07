//Prototype overrides
Array.prototype.diff = function(a) {
    return this.filter(function(i) {return a.indexOf(i) < 0;});
};

//BEGIN REFRESH ENTRIES\\
function refreshEntriesTable() {
  game_id = getFormValues(["game_id"])["game_id"];
  url = "../api/Games/"+game_id+"/PitcherInnings";
  
  $.ajax({
    url: url,
    success: handleRefreshEntries,
    error: function(jqXHR, textStatus, errorThrown) {
      window.alert("get error: " + errorThrown + ", url: " + url);
    }
  });
}

function handleRefreshEntries(data) {
  FIELDS = ["inning","pitcher_name","shutdown_inning","less_than_13_pitches",
            "retired_first_batter","three_and_out","strikeouts","ended_inning"];
  thHtml="";
  for (ii=0; ii<FIELDS.length; ii++) {
    thHtml+="<th>"+FIELDS[ii]+"</th>";
  }
  $( '#entries-table thead' ).html($("<tr></tr>").append(thHtml));
  $( '#entries-table tbody' ).html("");
  for (i=0; i<data.length; i++) {
    tdHtml = "";
    for (ii=0; ii<FIELDS.length; ii++) {
      tdHtml+="<td>"+data[i][FIELDS[ii]]+"</td>";
    }
    $("<tr></tr>").append(tdHtml).appendTo( '#entries-table tbody' );
  }
}

function markupTableData(e) {
  return "<td>"+e.inning+"</td>"+
         "<td>"+e.pitcher_name+"</td>"+
         "<td>"+e.shutdown_inning+"</td>"
}
//END REFRESH ENTRIES\\

//BEGIN CREATE NEW ENTRY\\
function submitEntry() {
  var FIELDS = ["game_id","inning","pitcher_id","shutdown_inning",
                "less_than_13_pitches","retired_first_batter",
                "three_and_out","strikeouts","ended_inning"];

  //extract values from form
  var entryMap = getFormValues(FIELDS);
  clearFormValues(FIELDS.diff(["game_id","inning","pitcher_id"]));

  $.ajax({
    type: "POST",
    url: "../api/PitcherInnings",
    data: JSON.stringify(entryMap),
    dataType: "json",
    success: function(data, textStatus, jqXHR) {
      refreshEntriesTable();
    },
    error: function(jqXHR, textStatus, errorThrown) {
      window.alert("post error: " + textStatus + ", url: " + "../api/PitcherInnings");
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
