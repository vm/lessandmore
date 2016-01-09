function getCurrentTabUrl(callback) {
  var queryInfo = {
    active: true,
    currentWindow: true
  };

  chrome.tabs.query(queryInfo, function(tabs) {
    var tab = tabs[0];
    var url = tab.url;
    callback(url);
  });
}

document.addEventListener('DOMContentLoaded', function() {
  document.getElementById("submit").onclick = function() {
    var less = document.getElementById('less').value;
    var more = document.getElementById('more').value;
    getCurrentTabUrl(function(url) {
      chrome.tabs.create({
        url: '127.0.0.1:5000/url=' + url + '&less=' + less + '&more=' + more
      })
    })
  });
});
