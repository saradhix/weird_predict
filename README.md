# Weird news prediction model
Usage:
python weird_predict.py <news.json>

Each line in news.json is a json.
Each json should contain the 'title' attribute
It can have any number of other attributes, but the model uses only the title
The filtered weird news are placed in output.json. Subsequent runs will overwrite the file. Please take a copy of it before running the program again.
Only weird news items are stored in output.json

Comments and suggestions can be mailed to saradhix@yahoo.com.

##Getting started ##
python weird_predict.py sample.json
cat output.json
