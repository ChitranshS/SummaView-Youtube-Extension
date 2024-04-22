chrome.runtime.onMessage.addListener(function(request, sender, sendResponse) {
  if (request.clicked) {
      // Extract the URL from the tab object
      chrome.tabs.query({ active: true, currentWindow: true }, function (tabs) {
          const tab = tabs[0];
          const url = tab.url;
          console.log('Request sent to:',url);
          fetch('http://127.0.0.1:5000/transcripted', {
              method: 'POST',
              headers: {
                  'Content-Type': 'application/json'
              },
              body: JSON.stringify({
                  url: url
              })
          })
          .then(response => response.json())
          .then(data => {
              console.log('Received response from Flask:', data);
              // Send the response back to the content script
              chrome.tabs.sendMessage(sender.tab.id, { dataFromBackground: data });
              console.log('Data sent to content-script');
            })
          .catch(error => {
              console.error('Error:', error);
          });
      });
  }



  if (request.summarize) {
    chrome.tabs.query({ active: true, currentWindow: true }, function (tabs) {
          const tab = tabs[0];
          const url = tab.url;
          console.log('Request sent to:',url);
          fetch('http://127.0.0.1:5000/summary', {
              method: 'POST',
              headers: {
                  'Content-Type': 'application/json'
              },
              body: JSON.stringify({
                  url: url
              })
          })
          .then(response => response.json())
          .then(data => {
              console.log('Received response from Flask:', data);
              // Send the response back to the content script
              chrome.tabs.sendMessage(sender.tab.id, { summarizedData: data });
              console.log('Data sent to content-script');
            })
          .catch(error => {
              console.error('Error:', error);
          });
      });
}
if (request.srt) {
    chrome.tabs.query({ active: true, currentWindow: true }, function (tabs) {
          const tab = tabs[0];
          const url = tab.url;
          console.log('Request sent to:',url);
          fetch('http://127.0.0.1:5000/timestamp', {
              method: 'POST',
              headers: {
                  'Content-Type': 'application/json'
              },
              body: JSON.stringify({
                  url: url
              })
          })
          .then(response => response.json())
          .then(data => {
              console.log('Received response from Flask:', data);
              // Send the response back to the content script
              chrome.tabs.sendMessage(sender.tab.id, { srtData: data });
              console.log('Data sent to content-script');
            })
          .catch(error => {
              console.error('Error:', error);
          });
      });
}

if (request.commentCat) {
    chrome.tabs.query({ active: true, currentWindow: true }, function (tabs) {
          const tab = tabs[0];
          const url = tab.url;
          console.log('Request sent to:',url);
          fetch('http://127.0.0.1:5000/commentcat', {
              method: 'POST',
              headers: {
                  'Content-Type': 'application/json'
              },
              body: JSON.stringify({
                  url: url
              })
          })
          .then(response => response.json())
          .then(data => {
              console.log('Received response from Flask:', data);
              // Send the response back to the content script
              chrome.tabs.sendMessage(sender.tab.id, { categoryData: data });
              console.log('Data sent to content-script');
            })
          .catch(error => {
              console.error('Error:', error);
          });
      });
}

if (request.commentSentiment) {
    chrome.tabs.query({ active: true, currentWindow: true }, function (tabs) {
          const tab = tabs[0];
          const url = tab.url;
          console.log('Request sent to:',url);
          fetch('http://127.0.0.1:5000/commentSentiment', {
              method: 'POST',
              headers: {
                  'Content-Type': 'application/json'
              },
              body: JSON.stringify({
                  url: url
              })
          })
          .then(response => response.json())
          .then(data => {
              console.log('Received response from Flask:', data);
              // Send the response back to the content script
              chrome.tabs.sendMessage(sender.tab.id, { sentimentData: data });
              console.log('Data sent to content-script');
            })
          .catch(error => {
              console.error('Error:', error);
          });
      });
}
});
