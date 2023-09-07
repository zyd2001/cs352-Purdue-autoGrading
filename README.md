# Grading

1. Require Pandas
2. Put the llvm build in the toplevel folder.
3. Put all the downloaded zip file in the PA* folder.
![Alt text](https://github.com/zyd2001/cs352-Purdue-autoGrading/assets/25120292/2ea324b6-ed1b-4d64-9e52-6aef236c7750)
4. Execute ./grading.py PA*
5. Result will be in `result.csv`

# Browser Script

1. Add browser extension Tampermonkey
2. Add the BrowserScript.js to Tampermonkey (copy paste)
3. Open one student's submission
![Alt text](https://github.com/zyd2001/cs352-Purdue-autoGrading/assets/25120292/1e2e6336-d22b-4dfe-9e7c-e0b08c3a039e)
4. There should be a new button (Start Script). Click the button and choose the result.json file
5. The script will fill the score with a trailing `0` and make the browser focus on the textbox. Just hit `Backspace` to delete the `0` and hit `Enter`, the script will go to the next students automatically. The script will skip students with no submission.
![Alt text](https://github.com/zyd2001/cs352-Purdue-autoGrading/assets/25120292/da695721-ab6d-4748-a6d5-74a75cef26ec)

The website prevents script input, so a user keyboard action is required.

There is also a `resultForImport.csv` for importing grades.