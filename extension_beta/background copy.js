chrome.runtime.onMessage.addListener(function (request, sender, sendResponse) {
  if (request.clicked) //whether it was clicked or not
  {
    async function getCurrentTab() {
      let queryOptions = {
        active: true,
        lastFocusedWindow: true
      };
      // `tab` will either be a `tabs.Tab` instance or `undefined`.
      let [tab] = await chrome.tabs.query(queryOptions);
      return tab;
    }

    // Use an async function to handle the promise
    async function sendUrl() {
      let currentTab = await getCurrentTab();
      // Extract the URL from the tab object
      if (currentTab) {
        console.log('URL:', currentTab.url);
        fetch('http://127.0.0.1:5000/process-url', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json'
          },
          body: JSON.stringify({
            url: currentTab.url
          })
        })

          // data recieved here!
          .then(response => response.json())
          .then(data => {
            console.log('Received response from Flask:', data);
            // Send the response back to the content script
            chrome.runtime.sendMessage({
              dataFromBackground: data
            });
          })
          .catch(error => {
            console.error('Error:', error);
          });
      } else {
        console.log('No active tab found.');
        return null;
      }
    }
    sendUrl()


  }
});