# Vue Data Scraper 

Description: Quick comissioned data scraper designed to collect data on makeup brands and products. *Out Of Date*

soup.py (makeupalley.com)

soup.py mines data from the makeupalley review website and appends it to a json document called “makeupalley.json”.

Before running the program from the beginning, the contents of makeupalley.json should read only:
 
“products” : {


The easiest way to run the python crawler is to open up your terminal, change directories to the VueScraper folder and run the code using built in python (preferably a version of python 3.x, or it’ll run dangerously slow). The command for that is usually 
>>>  python soup.py

A list of the products parsed and mined will be printed onto the terminal as the code does its thing. The data will be written automatically to the makeupalley.json script.

NOTE: You should make an account with makeupalley and be signed into it on your browser before running the script, otherwise you will likely quickly run into errors.  

shoppersscraper.py (shoppers drugmart)

The shoppers crawler works the exact same way. “shoppers.json” should read

“products” : {


prior to running the code. The typical terminal command is 

>>> python shoppers scraper.py

You don’t need to be signed into shoppers drug mark makeup page for this one.



———————————————————————————————————————————————————————

Note for the aggregator: One thing worth mentioing; within the python code for soup.py, there is included a method specifically for parsing multiple pages of comments. This code is not used and the base code defaults to pulling the top 10 most helpful comments. Within that method is a method to write CSV code. CSV, however, works very very poorly with NLS (natural language syntax) and running this will not only throw several errors into the resulting code, but will render it indecipherable by NoSQL databases. Naturally people tend to use both quotation marks and commas in their natural writing, messing with the format. I’ve found a few work arounds, but I recommend against using it. 

Hope it works for ya! 

Let me know if you run into any issues or errors. ^_^ 
