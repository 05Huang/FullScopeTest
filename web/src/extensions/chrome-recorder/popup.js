/** FullScopeTest Recorder - Popup Script */

let steps = [];

const statusEl = document.getElementById("status");
const startBtn = document.getElementById("startBtn");
const stopBtn = document.getElementById("stopBtn");
const exportBtn = document.getElementById("exportBtn");
const stepsContainer = document.getElementById("stepsContainer");
const output = document.getElementById("output");

function updateUI(recording, stepList) {
  steps = stepList || steps;
  if (recording) {
    statusEl.textContent = "Recording... (" + steps.length + " steps)";
    statusEl.className = "status status-recording";
    startBtn.disabled = true;
    stopBtn.disabled = false;
    exportBtn.disabled = true;
  } else {
    statusEl.textContent = steps.length > 0 ? "Stopped (" + steps.length + " steps)" : "Ready";
    statusEl.className = "status status-idle";
    startBtn.disabled = false;
    stopBtn.disabled = true;
    exportBtn.disabled = steps.length === 0;
  }
  renderSteps();
}

function renderSteps() {
  stepsContainer.innerHTML = steps.map(function(s) {
    return "<div class="step"><span class="step-type">" + s.type + "</span>" +
      (s.selector || s.text || "").substring(0, 80) + "</div>";
  }).join("");
}

function exportToFullScope() {
  var exported = steps.map(function(s) {
    if (s.type === "click") {
      return { action: "click", selector: s.selector, value: "" };
    } else if (s.type === "input") {
      return { action: "fill", selector: s.selector, value: s.value };
    } else if (s.type === "select") {
      return { action: "select", selector: s.selector, value: s.value };
    }
    return { action: s.type, selector: s.selector || "", value: s.value || "" };
  });
  output.style.display = "block";
  output.value = JSON.stringify(exported, null, 2);
}

startBtn.addEventListener("click", function() {
  chrome.tabs.query({ active: true, currentWindow: true }, function(tabs) {
    chrome.tabs.sendMessage(tabs[0].id, { action: "startRecording" }, function(resp) {
      if (resp) updateUI(true, []);
    });
  });
});

stopBtn.addEventListener("click", function() {
  chrome.tabs.query({ active: true, currentWindow: true }, function(tabs) {
    chrome.tabs.sendMessage(tabs[0].id, { action: "stopRecording" }, function(resp) {
      if (resp) updateUI(false, resp.steps);
    });
  });
});

exportBtn.addEventListener("click", exportToFullScope);

chrome.runtime.onMessage.addListener(function(msg) {
  if (msg.action === "newStep") {
    steps.push(msg.step);
    updateUI(true);
  }
});

// Check initial status
chrome.tabs.query({ active: true, currentWindow: true }, function(tabs) {
  if (tabs[0]) {
    chrome.tabs.sendMessage(tabs[0].id, { action: "getStatus" }, function(resp) {
      if (resp) updateUI(resp.isRecording);
    });
  }
});
