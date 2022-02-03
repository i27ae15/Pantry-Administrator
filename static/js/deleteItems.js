
document.get


function deleteItem(item_id, item_type, name, rowName, food) {
  $.ajax({
    type: 'DELETE',
    url: "/deleteItem",
    data: JSON.stringify({
      'food': food,
      'id': item_id,
      'item_type': item_type,
      'name': name
    }),

    contentType: 'application/json; charset=utf-8',
    success: function (data) {
      deleteRow(rowName)
    }
  });

}

function deleteRow(rowName){
  document.getElementById(rowName).remove();
}