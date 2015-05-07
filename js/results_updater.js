function getHighestItem() {
  var results_els = $('.result_item');
  var highest_result = 0;
  $.each(results_els, function(i, el) {
    highest_result = Math.max(highest_result, $(el).data('item_id'))
  });
  return highest_result;
}
window.next_id = getHighestItem() + 1;

function tryNextPage(next_id) {
  var new_content = jQuery.get('/rss/' + window.next_id + '/', function(data) {
    var data = data;
    if (data.replace(/^\s+|\s+$/g, '') != "") {

      $('#result_items').prepend($(data).hide().fadeIn(1000, function() {
        window.next_id = getHighestItem() + 1;
      }));
    }
  });
}

setInterval(function() {
  tryNextPage();
}, 300000);
