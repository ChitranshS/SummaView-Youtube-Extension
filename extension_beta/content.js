// Listen for messages from the background script
if (window.location.href.includes('https://www.youtube.com/')) { // Replace 'example.com' with your target website
    const extensionDiv = document.createElement('div');
    extensionDiv.innerHTML = `
        <div style="position: fixed; top: 20px; right: 20px; z-index: 9999; background: white; padding: 10px;">
            <button id="extensionButton">Extension Button</button>
        </div>
    `;
    document.body.appendChild(extensionDiv);

    // Add an event listener to the button
    document.getElementById('extensionButton').addEventListener('click', function() {
        // When the button is clicked, communicate with the background script
        chrome.runtime.sendMessage({ action: 'buttonClicked' });
    });
}

chrome.runtime.onMessage.addListener(function(message, sender, sendResponse) {
    if (message.dataFromBackground) {
        const receivedData = message.dataFromBackground;
        
        // Process received data and manipulate the DOM
        console.log('Received data in content script:', receivedData);
        alert("recived")
        // Example: Create a new DOM element and add data to the webpage
        const newDataElement = document.createElement('div');
        newDataElement.textContent = JSON.stringify(receivedData.text); // Displaying data as text

        // Append the new element to the webpage
        document.body.appendChild('<p>${newDataElement}</p>');
    }
});


