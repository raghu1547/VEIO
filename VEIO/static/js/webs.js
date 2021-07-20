var loc = window.location;
var endpoint = "";
var wsStart = "ws://";
if (loc.protocol == "https:") {
  wsStart = "wss://";
}
endpoint = wsStart + loc.host + loc.pathname;
var socket = new ReconnectingWebSocket(endpoint);
socket.onmessage = function (e) {
  console.log("message", e);
  var data = JSON.parse(e.data);
  // console.log(data);
  setTable(data);
};
socket.onopen = function (e) {
  console.log("open", e);
  //   socket.send("krishna");
};
socket.onerror = function (e) {
  console.log("error", e);
};
socket.onclose = function (e) {
  console.log("close", e);
  // alert("went offline or disconnected from server ");
};

function setTable(data) {
  //   console.log($("#tablebody"));
  var index = data.length;
  $("#tablebody").html("");
  for (i of data) {
    const row = `<tr>
        <th scope="row">${index}</th>
        <td>${i.vn}</td>
        <td>${i.name}</td>
        <td>${i.nod}</td>
        <td>${i.firstentry}</td>
        <td>${i.timein}</td>
        <td>${i.contact}</td>
      </tr>`;
    index--;
    $("#tablebody").append(row);
  }

  $("#tablebody").fadeOut(100);
  $("#tablebody").fadeIn(100);
}
