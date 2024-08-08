document.getElementById('save').addEventListener('click', function () {
  var webhookUrl = document.getElementById('webhookUrl').value;
  chrome.storage.sync.set({
    slackWebhookUrl: webhookUrl
  }, function () {
    var status = document.getElementById('status');
    status.textContent = 'Options saved.';
    setTimeout(function () {
      status.textContent = '';
    }, 750);
  });
});

// Restores select box and checkbox state using the preferences
// stored in chrome.storage.
document.addEventListener('DOMContentLoaded', function () {
  chrome.storage.sync.get({
    slackWebhookUrl: ''
  }, function (items) {
    document.getElementById('webhookUrl').value = items.slackWebhookUrl;
  });
});