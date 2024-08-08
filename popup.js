let currentTabId;

document.addEventListener('DOMContentLoaded', function () {
  const sendUrlButton = document.getElementById('sendUrlButton');

  chrome.tabs.query({active: true, currentWindow: true}, function (tabs) {
    currentTabId = tabs[0].id;
  });

  sendUrlButton.addEventListener('click', function () {
    chrome.tabs.query({active: true, currentWindow: true}, function (tabs) {
      const currentUrl = tabs[0].url;
      chrome.storage.sync.get(['slackWebhookUrl'], function (result) {
        if (result.slackWebhookUrl) {
          sendSlackNotification(result.slackWebhookUrl, currentUrl);
          sendUrlButton.disabled = true;
        } else {
          alert('Slack Webhook URLを拡張機能のオプションで設定してください。');
        }
      });
    });
  });
});

function sendSlackNotification(webhookUrl, currentUrl) {
  fetch(webhookUrl, {
    method: 'POST', headers: {
      'Content-Type': 'application/json; charset=utf-8'
    }, body: JSON.stringify({
      text: `<${currentUrl}>`,
      unfurl_links: true,
      unfurl_media: true
    })
  })
    .then(response => {
      if (response.ok) {
        alert('URLがSlackに通知されました！');
      } else {
        alert('Slackへの通知に失敗しました。');
        document.getElementById('sendUrlButton').disabled = false;
      }
    })
    .catch(error => {
      alert(`エラー: ${error.message}`);
      document.getElementById('sendUrlButton').disabled = false;
    });
}

chrome.tabs.onUpdated.addListener(function (tabId, changeInfo, tab) {
  if (tabId === currentTabId && changeInfo.status === 'complete') {
    document.getElementById('sendUrlButton').disabled = false;
  }
});