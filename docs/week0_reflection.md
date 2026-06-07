What is the difference between raising an error and handling an error?
Ans: Handling an error is basically when the we try to make the program execute without any failure even if the user inputs invalid data. Whereas raising intentionally and actively interrupting the flow of the program so that the error raised/ occured can be actively handled. Once an error is raised the execution stops and an error object is thrown up the stack so it can be handled there either by the user defined handling function or by the interpreter or runtime.
An example is that in the missing column function we raisedthe error so that if any missing column is found the execution stops there itself, preventing user from procedding further without giving correct columns. But the error is not handled there as it is not specified what exactly to do if any such error arises. An example of handling would be in main() wrapping the call in a try/except — if required_columns raises a ValueError, main() catches it, logs the message, and exits gracefully instead of crashing."

Point 2:
When ingest.py imports from validate.py, both files are inside the ingestion/ folder. For Python to resolve from ingestion.validate import required_columns correctly, you must always run your scripts from the project root, not from inside a subfolder.
This is why every script in your project will be run as:
bashcd d:/Financial-analytics-platform
python -m ingestion.ingest
Not as:
bashcd d:/Financial-analytics-platform/ingestion
python ingest.py