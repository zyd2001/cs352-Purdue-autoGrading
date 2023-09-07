// ==UserScript==
// @name         BrightSpace
// @namespace    http://tampermonkey.net/
// @version      0.1
// @description  try to take over the world!
// @author       Yida Zhang
// @match        https://purdue.brightspace.com/d2l/le/activities/iterator/*
// @icon         https://www.google.com/s2/favicons?sz=64&domain=brightspace.com
// @grant        none
// ==/UserScript==

(function() {
    'use strict';
    // Your code here...
    let test = JSON.parse('{"123":123}')
    let processed = {}
    var lastname = ''

    function checkLoaded(str) {
        if (document.getElementsByTagName('d2l-consistent-evaluation')[0].shadowRoot.children[0].shadowRoot.getElementById('evaluation-template').querySelectorAll('d2l-consistent-evaluation-learner-context-bar')[0].shadowRoot.querySelector('.d2l-skeleton-learner-context-bar').ariaHidden == 'true'){
            if (lastname == document.getElementsByTagName('d2l-consistent-evaluation')[0].shadowRoot.children[0].shadowRoot.getElementById('evaluation-template').querySelectorAll('d2l-consistent-evaluation-learner-context-bar')[0].shadowRoot.querySelectorAll('d2l-consistent-evaluation-lcb-user-context')[0].shadowRoot.children[0].getElementsByTagName('span')[0].innerText) {
                return false
            }
            else {
                return true
            }
        }
        else {
            return false
        }
    }

    function onReaderLoad(e) {
        var contents = e.target.result;
        let result = JSON.parse(contents)
        try {
            // let result = JSON.parse(contents)
            (function loop() {
               (function wait() {
                   if (!checkLoaded())
                       setTimeout(wait, 100)
                   else
                   {
                       let name = document.getElementsByTagName('d2l-consistent-evaluation')[0].shadowRoot.children[0].shadowRoot.getElementById('evaluation-template').querySelectorAll('d2l-consistent-evaluation-learner-context-bar')[0].shadowRoot.querySelectorAll('d2l-consistent-evaluation-lcb-user-context')[0].shadowRoot.children[0].getElementsByTagName('span')[0].innerText
                       let save = document.getElementsByTagName('d2l-consistent-evaluation')[0].shadowRoot.children[0].shadowRoot.getElementById('evaluation-template').querySelectorAll('d2l-consistent-evaluation-footer')[0].shadowRoot.children[0].querySelector('#consistent-evaluation-footer-save-draft').shadowRoot.children[0]
                       let next = document.getElementsByTagName('d2l-consistent-evaluation')[0].shadowRoot.children[0].shadowRoot.getElementById('evaluation-template').getElementsByTagName('d2l-consistent-evaluation-nav-bar')[0].shadowRoot.querySelectorAll('d2l-navigation-iterator')[0].shadowRoot.querySelectorAll('d2l-navigation-button-icon')[1].shadowRoot.children[0]
                       let input = document.getElementsByTagName('d2l-consistent-evaluation')[0].shadowRoot.children[0].shadowRoot.getElementById('evaluation-template').querySelectorAll('consistent-evaluation-right-panel')[0].shadowRoot.querySelector('consistent-evaluation-right-panel-evaluation').shadowRoot.querySelector('d2l-consistent-evaluation-right-panel-grade-result').shadowRoot.children[0].shadowRoot.querySelector('d2l-grade-result-numeric-score').shadowRoot.querySelector('d2l-input-number').shadowRoot.children[0].shadowRoot.querySelector('input')
                       lastname = name
                       //if (processed[name])
                       //    return
                       //processed[name] = true
                       if (name in result)
                       {
                           console.log(name + ' success')
                           let val = result[name].percent.toFixed(2)+'0'
                           input.value = val
                           input.focus()
                           input.setSelectionRange(val.length, val.length)
                           input.addEventListener('keypress', function (e) {
                               if (e.key === 'Enter') {
                                   save.click()
                                   setTimeout(function () {
                                       next.click()
                                       loop()
                                   }, 1000)
                               }
                           });
                       }
                       else
                       {
                           console.log(name + ' fail')
                           next.click()
                           loop()
                       }
                   }
               })()
            })()
        } catch (e) {
            alert(e.name + ": " + e.message);
        }
    }
    setTimeout(function() {
    // your code here
        let temp = document.getElementsByTagName('d2l-consistent-evaluation')[0].shadowRoot.children[0].shadowRoot.getElementById('evaluation-template').querySelectorAll('d2l-consistent-evaluation-footer')[0].shadowRoot.children[0]
        let elem = document.createElement('div')
        let i = document.createElement('div')
        i.innerHTML = '<input id="scriptInput" type="file" style="display:none" />'
        let input = i.children[0]
        elem.innerHTML = '<div class="d2l-button-container"><d2l-button primary="" id="start-script" type="button">Start Script</d2l-button></div>'
        elem.onclick = function () {
            input.click()
        }
        i.addEventListener('change', function (e) {
            var file = e.target.files[0];
            if (!file) {
                alert('no file')
                return;
            }
            var reader = new FileReader()
            reader.addEventListener('load', onReaderLoad)
            reader.readAsText(file);
        }, false);
        temp.insertBefore(elem, temp.children[0])
        temp.insertBefore(i, temp.children[0])
    }, 1000);

})();