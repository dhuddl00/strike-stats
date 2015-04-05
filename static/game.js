function callRefreshEntries() {
  url = "../api/Games";
  $.ajax({
    url: url,
    success: handleRefreshEntries
  });
}

function handleRefreshEntries(data) {
  for (i=0; i<data.length; i++) {
    var e = data[i];
    $("<tr></tr>").append("<td>"+e.opponent+"</td><td>"+e.game_date+"</td>").appendTo( '#entries-table tbody' );
  }
}

