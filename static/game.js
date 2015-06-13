//Prototype overrides
Array.prototype.diff = function(a) {
    return this.filter(function(i) {return a.indexOf(i) < 0;});
};

//BEGIN REFRESH ENTRIES\\
function refreshEntriesTable() {
  console.log("refreshEntriesTable()");
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

function updateStrikeoutsValueBox(newValue) {
  $( '#strikeouts_value_box' ).html(newValue);
}

function handleRefreshEntries(data) {
  console.log("handleRefreshEntries(): " + JSON.stringify(data));
  var FIELDS = ["inning","pitcher_name","shutdown_inning","less_than_13_pitches",
            "retired_first_batter","three_and_out","strikeouts","ended_inning"];

  //Sort data in appropriate order
  data = data.sort(function(a,b) { 
      var aKey = a.inning + a.pitcher_name;
      var bKey = b.inning + b.pitcher_name;
      //window.alert("aKey: " + aKey + ", bKey: " + bKey);
      return aKey.localeCompare(bKey); 
        } );
  
  headHtml="<tr>";
  for (ii=0; ii<FIELDS.length; ii++) {
    headHtml+='<th class="h5">'+FIELDS[ii].replace(/_/g," ")+"</th>";
  }
  headHtml+="</tr>";
  $( '#entries-table thead' ).html(headHtml);

  bodyHtml="";
  for (i=0; i<data.length; i++) {
    bodyHtml += "<tr>";
    for (ii=0; ii<FIELDS.length; ii++) {
      d = data[i][FIELDS[ii]];
      val = "";
      if (typeof d == "boolean") {
        if (d) { val = "&#10004;"; } else { val = " "; } 
      } else if (FIELDS[ii] == 'strikeouts') {
        s = "&#10008";
        if (d == 0) val = " ";
          else if (d == 1) val = s;
          else if (d == 2) val = s+s;
          else if (d == 3) val = s+s+s;
          else val = "ERROR";
      } else {
        val = d;
      }

      bodyHtml+='<td class="center">'+ val +"</td>";
    }
    bodyHtml += "</tr>";
  $( '#entries-table tbody' ).html(bodyHtml);
  }
}

//END REFRESH ENTRIES\\

//BEGIN CREATE NEW ENTRY\\
function submitEntry() {
  console.log("submitEntry()");
  var FIELDS = ["game_id","inning","pitcher_id","shutdown_inning","less_than_13_pitches",
            "retired_first_batter","three_and_out","strikeouts","ended_inning"];
  //extract values from form
  var entryMap = getFormValues(FIELDS);
  //window.alert("data: " + JSON.stringify(entryMap));

  $.ajax({
    type: "POST",
    url: "../api/PitcherInnings",
    data: JSON.stringify(entryMap),
    dataType: "json",
    success: function(data, textStatus, jqXHR) {
      refreshEntriesTable();
      clearFormValues(FIELDS.diff(["game_id","inning","pitcher_id"]));
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
    if (e.prop('type') == "checkbox") {
      e.prop('checked',false);
    } else if (e.prop('type') == "select-one") {
      //TODO: Fix this to be dynamic
      e.val('');  
    } else if (e.prop('type') == "range") {
      e.val(0);  
      updateStrikeoutsValueBox(0); 
    } else {
      e.val('');  
    }
  }
  return 0;
}
//END CREATE NEW ENTRY\\
