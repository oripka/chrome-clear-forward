// Copyright (c) 2012 The Chromium Authors. All rights reserved.
// Use of this source code is governed by a BSD-style license that can be
// found in the LICENSE file.

// Simple extension to replace lolcat images from
// http://icanhascheezburger.com/ with loldog images instead.

// includes post date
chrome.webRequest.onBeforeRequest.addListener(
  function(info) {
    if(info.method == "GET"){
      return;
    }
    else if(info.url.includes("localhost")){
      return;
    }else if(info.type == "ping"){
      return;
    }else{
      sendToAggregator(info);
      console.log("onBeforeRequest intercepted: " + JSON.stringify(info));
    }
  },
  // filters
  {urls: ["<all_urls>"]},
  // extraInfoSpec
  ["requestBody","blocking"]);

// includes get data
chrome.webRequest.onBeforeSendHeaders.addListener(
  function(info) {
    var headers = info.requestHeaders;

    if(info.url.includes("localhost")){
      return {requestHeaders: headers};
    }else if(info.type == "ping"){
      return {requestHeaders: headers};
    }else{
      sendToAggregator(info);
      console.log("onBeforeSendHeaders intercepted: " + JSON.stringify(info));
    }

    return {requestHeaders: headers};
  },
  // filters
  {urls: ["<all_urls>"]},
  // extraInfoSpec
  ["requestHeaders","blocking"]);

/*chrome.devtools.network.onRequestFinished.addListener(function(req) {
  // Displayed sample TCP connection time here
  if(req.url.includes("localhost")){
    return
  }
  else {
    console.log(JSON.stringify(req));
  }
});*/


function sendToAggregator(info) {
  var xhr = new XMLHttpRequest();
  var url = "http://localhost:8000";
  xhr.open("POST", url, true);
  xhr.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
  xhr.send(JSON.stringify(info));

  var result = xhr.responseText;
}
