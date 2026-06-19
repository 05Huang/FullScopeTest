/**
 * FullScopeTest Recorder - Content Script
 *
 * Runs on web pages to record user interactions:
 * - Click events
 * - Input/change events
 * - Navigation events
 * - Select events
 */

(function() {
  "use strict";

  let isRecording = false;
  let recordedSteps = [];
  let stepCounter = 0;

  /** Generate a CSS selector for an element */
  function getSelector(el) {
    if (el.id) return "#" + el.id;
    if (el.name) return el.tagName.toLowerCase() + "[name="" + el.name + ""]";
    const parts = [];
    let current = el;
    while (current && current !== document.body) {
      let selector = current.tagName.toLowerCase();
      if (current.id) { selector = "#" + current.id; parts.unshift(selector); break; }
      if (current.className && typeof current.className === "string") {
        selector += "." + current.className.trim().split(/s+/).slice(0, 2).join(".");
      }
      const parent = current.parentElement;
      if (parent) {
        const siblings = Array.from(parent.children).filter(c => c.tagName === current.tagName);
        if (siblings.length > 1) {
          const index = siblings.indexOf(current) + 1;
          selector += ":nth-of-type(" + index + ")";
        }
      }
      parts.unshift(selector);
      current = current.parentElement;
    }
    return parts.join(" > ");
  }

  /** Record a step */
  function recordStep(type, data) {
    if (!isRecording) return;
    const step = {
      id: ++stepCounter,
      type: type,
      timestamp: Date.now(),
      url: window.location.href,
      ...data
    };
    recordedSteps.push(step);
    chrome.runtime.sendMessage({ action: "stepRecorded", step: step });
  }

  /** Event listeners */
  document.addEventListener("click", function(e) {
    if (!isRecording) return;
    const el = e.target;
    const tag = el.tagName.toLowerCase();
    if (["a", "button", "input"].includes(tag) || el.onclick || el.getAttribute("role") === "button") {
      recordStep("click", {
        selector: getSelector(el),
        tagName: tag,
        text: (el.textContent || "").trim().substring(0, 100),
        href: el.href || null
      });
    }
  }, true);

  document.addEventListener("input", function(e) {
    if (!isRecording) return;
    const el = e.target;
    if (["input", "textarea"].includes(el.tagName.toLowerCase())) {
      recordStep("input", {
        selector: getSelector(el),
        inputType: el.type || "text",
        value: el.value
      });
    }
  }, true);

  document.addEventListener("change", function(e) {
    if (!isRecording) return;
    const el = e.target;
    if (el.tagName.toLowerCase() === "select") {
      recordStep("select", {
        selector: getSelector(el),
        value: el.value,
        text: el.options[el.selectedIndex]?.text || ""
      });
    }
  }, true);

  /** Message handler */
  chrome.runtime.onMessage.addListener(function(msg, sender, sendResponse) {
    if (msg.action === "startRecording") {
      isRecording = true;
      recordedSteps = [];
      stepCounter = 0;
      sendResponse({ status: "recording" });
    } else if (msg.action === "stopRecording") {
      isRecording = false;
      sendResponse({ status: "stopped", steps: recordedSteps });
    } else if (msg.action === "getStatus") {
      sendResponse({ isRecording: isRecording, stepCount: recordedSteps.length });
    } else if (msg.action === "getSteps") {
      sendResponse({ steps: recordedSteps });
    }
    return true;
  });
})();
