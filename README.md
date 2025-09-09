a Multi-agent-system that handles:
1. processing video input as given task
2. using VLM (GLM4.5v) for auto processing video contents and return a coding prompt for coding LLM (gpt4o)
3. coding LLM (gpt4o) using VLM's output for auto generating 'playwright' python script.
4. VLM (GLM4.5v) auto detecting & judging whether the pyhton script written by coding LLM (gpt4o) complete the given task.
5. While script being invalid, auto taking browser screenshoot & downloading html page source code for error handling & code updates.
6. feeding the info gethered in step 5 back to codding LLM and establish the loop of self-evloving & self-checking ai coding system.
 
