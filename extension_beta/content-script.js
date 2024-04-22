// Listen for the 'load' event
window.addEventListener('load', function() {
    // Set a timeout to execute an action after a delay
    setTimeout(renderButton, 3000);
});
let loader=null
//////////////////////////////////////////////////////////////////////////////////////////
function renderButton() {
    const parentDiv = document.getElementById("secondary");

    const newChildElement = document.createElement('div');
    newChildElement.innerHTML = `
        <div id="injectedDiv">
        <div id="injectedHeader"> SummaView</div>
        <div id="injectedLoader">Please wait for some time</div>
        <div id="injectedButton">
            <button id="sendUrl">Transcript</button>
            <button id="sendTranscript">Summarize</button>
            <button id="sendSRT">TimeStamps</button>


        </div>
            </div>
    `;
    chrome.runtime.sendMessage({ commentCat: true });
    chrome.runtime.sendMessage({ commentSentiment: true });
    let firstChild = parentDiv.firstChild;
    parentDiv.insertBefore(newChildElement, firstChild);
    console.log("DOM Modified")
     loader =  document.getElementById("injectedLoader")
     loader.style.display = "none";

//////////////////////////////////////////////////////////////////////////////////////////////
    document.getElementById("sendUrl").addEventListener("click", function () {
        // Communicate with background script to trigger the server request
        chrome.runtime.sendMessage({ clicked: true });////////////////////////////////////////////
        console.log("Request sent to background script")
        loader.style.display = "flex";
    });
    document.getElementById("sendTranscript").addEventListener("click", function () {
        // Communicate with background script to trigger the server request
        chrome.runtime.sendMessage({ summarize: true });////////////////////////////////////////////
        console.log("Request sent to background script")
        loader.style.display = "flex";
    });
    document.getElementById("sendSRT").addEventListener("click", function () {
        // Communicate with background script to trigger the server request
        chrome.runtime.sendMessage({ srt: true });////////////////////////////////////////////
        console.log("Request sent to background script")
        loader.style.display = "flex";
    });
}


////////////////////////////////////////////////////////////////////////////////////////////////

function renderText(data,name) {
    const parentDiv = document.getElementById("injectedDiv");
    // let randomInt = Math.randomInt(0,1);
    // let emoji = ["&#x1f4d6;","&#x1F4DD;"];
    const newChildElement = document.createElement('div');
    newChildElement.innerHTML = `
        <div id="injectedName">${name}</div>
        <div id="injectedText">
        ${data}
        </div>
    `;////////////////////////////////////////////////////////////////
    newChildElement.style.overflow = 'scroll'; // Enable scrolling

    let thirdChild = parentDiv.children[1];
    parentDiv.insertBefore(newChildElement, thirdChild);
    console.log("DOM Modified")

   
}
///////////////////////////////////////////////////////////////////////////////////////////
function renderSentiment(data,name) {
    const parentDiv = document.getElementById("below");
    // let randomInt = Math.randomInt(0,1);
    // let emoji = ["&#x1f4d6;","&#x1F4DD;"];
    const newChildElement = document.createElement('div');
    newChildElement.innerHTML = `
        <div id="injectedCategoryItem" style="background-color: rgba(255,255,255,0.102); border-radius: 8px; padding-bottom: 1px;" class="yt-core-attributed-string--highlight-text-decorator">
        <div id="injectedName">${name}</div>
        <div id="injectedDistributionBar""></div>
        <div id="injectedCatText">
        <div>Overall Sentiment: <b> ${data['overall']}</b></div>
        <div>Spam Comments: ${data['spam']}</div>
        <div>Unique Comments: ${data['unique']}</div>
        </div>
        </div>
    `;////////////////////////////////////////////////////////////////
    newChildElement.style.overflow = 'scroll'; // Enable scrolling

    let thirdChild = parentDiv.children[9];
    parentDiv.insertBefore(newChildElement, thirdChild);
    console.log("DOM Modified")
    // Define the percentages for each color
let percentages = [];
percentages.push(data['per']['pos'])
percentages.push(data['per']['neutral']) 
percentages.push(data['per']['neg']) 
console.log(percentages)
// Three colors with percentages 30%, 40%, and 30%

// Define the colors
const colors = ['#17eb3d', '#ebca11', '#e86c6c']; 

const distributionBar = document.getElementById('injectedDistributionBar');
let currentPos = 0;

// Create div elements representing each color segment based on percentages
percentages.forEach((percentage, index) => {
  const segment = document.createElement('div');
  segment.style.width = percentage + '%';
  segment.style.height = '100%';
  segment.style.float = 'left';
  segment.style.backgroundColor = colors[index];

  distributionBar.appendChild(segment);
});


   
}
///////////////////////////////////////////////////////////////////////////////////////////////
function renderCategory(data,name) {
    const parentDiv = document.getElementById("below");
    // let randomInt = Math.randomInt(0,1);
    // let emoji = ["&#x1f4d6;","&#x1F4DD;"];
    const newChildElement = document.createElement('div');
    newChildElement.innerHTML = `
    <div id="injectedCategoryItem" style="background-color: rgba(255,255,255,0.102); border-radius: 8px; padding-bottom: 1px;" class="yt-core-attributed-string--highlight-text-decorator">
        <div id="injectedName">${name}</div>
        
        <div id = "injectedCategory" >Text Here
    </div>
    </div>
        
    `;////////////////////////////////////////////////////////////////
    // newChildElement.style.overflow = 'scroll'; // Enable scrolling

    let thirdChild = parentDiv.children[9];
    parentDiv.insertBefore(newChildElement, thirdChild);
    console.log("DOM Modified")
// Replace this with your actual data

// Assuming 'newChildElement' is the HTML element where you want to add buttons
const buttonWrapper = document.getElementById('injectedCategory'); // Replace 'yourElementId' with your element's ID

// Clear the inner HTML content of the element before adding new buttons
buttonWrapper.innerHTML = '';

// Loop through the 'data' array and create buttons based on its length
data.forEach(buttonText => {
    const button = document.createElement('button');
    button.textContent = buttonText;

    // Append each button to the 'newChildElement'
    buttonWrapper.appendChild(button);
});


   
}


///////////////////////////////////////////////////////////////////////////////////////////////
// Listen for responses from the background script
chrome.runtime.onMessage.addListener(function(message, sender, sendResponse) {
    if (message.dataFromBackground) {
        const receivedData = message.dataFromBackground;
        // alert(receivedData['key']);
        console.log(receivedData);
        loader.style.display = "none";
        renderText(receivedData['text'],"Transcript &#x1f4d6;"); /////////////////////////////////////////////////////
    }
    if (message.summarizedData) {
        const receivedData = message.summarizedData;
        // alert(receivedData['key']);
        console.log(receivedData);
        loader.style.display = "none";
        renderText(receivedData['text'],"Summary &#x1F4DD;"); /////////////////////////////////////////////////////
    }
    if (message.srtData) {
        const receivedData = message.srtData;
        // alert(receivedData['key']);
        console.log(receivedData);
        loader.style.display = "none";
        renderText(receivedData['srt'],"TimeStamps &#x23F0;"); /////////////////////////////////////////////////////
    }
    if (message.categoryData) {
        const receivedData = message.categoryData;
        // alert(receivedData['key']);
        console.log(receivedData);
        renderCategory(receivedData['text'],"Highlighted Words &#x1F4DD;"); /////////////////////////////////////////////////////
    }
    if (message.sentimentData) {
        const receivedData = message.sentimentData;
        // alert(receivedData['key']);
        console.log(receivedData);
        renderSentiment(receivedData,"Comment Sentiment Analysis &#x1f4ca;"); /////////////////////////////////////////////////////
    }


});

