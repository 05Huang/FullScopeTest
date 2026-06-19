/** FullScopeTest Recorder - Background Service Worker */

let recordingTabId = null;

chrome.runtime.onMessage.addListener(function(msg, sender, sendResponse) {
  if (msg.action === "startRecording") {
    recordingTabId = sender.tab?.id || null;
    chrome.action.setBadgeText({ text: "REC" });
    chrome.action.setBadgeBackgroundColor({ color: "#ff4d4f" });
  } else if (msg.action === "stopRecording") {
    recordingTabId = null;
    chrome.action.setBadgeText({ text: "" });
  } else if (msg.action === "stepRecorded") {
    // Forward step to popup if open
    chrome.runtime.sendMessage({ action: "newStep", step: msg.step }).catch(() => {});
  }
});

chrome.runtime.onInstalled.addListener(function() {
  console.log("FullScopeTest Recorder installed");
});
