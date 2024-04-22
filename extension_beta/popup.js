// document.addEventListener("DOMContentLoaded", function () {
//   document.getElementById("sendUrl").addEventListener("click", function () {
//       chrome.tabs.query({ active: true, currentWindow: true }, function (tabs) {
//           const tab = tabs[0];
//           const url = tab.url;
//           console.log(url)
//           // Communicate with background script to pass URL to Python script
//           chrome.runtime.sendMessage({ url: url });
//       });
//   });

// //   chrome.runtime.onMessage.addListener(function (message, sender, sendResponse) {
// //       if (message.dataFromBackground) {
// //           const receivedData = message.dataFromBackground;
// //           const url = receivedData.key
// //           // Handle the received data in the popup
// //           alert(url);
// //           // Perform actions with the received data in the popup
// //       }
// //   });
// });
