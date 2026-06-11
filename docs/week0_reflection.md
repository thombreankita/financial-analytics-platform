Q.What is the difference between raising an error and handling an error?
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

Q.When you run python -m ingestion.ingest from the project root — what do you think Python sets __name__ to inside ingest.py? Is it '__main__' or 'ingestion.ingest'?
Ans: in this case the __name__ is set to main.
==> __Main__ is the top level environment or can be said as the entry point of the program. When a script runs directly from the interpreter the __name__ is set to __main__ but when a script is imported inside another file, the __name__ of the imported script/module is set to the module name or to absolute module name/path.

Important point:
Relative imports work when running a file directly but break when the file is imported as part of a package. Absolute imports are the correct production style and require running with python -m or setting PYTHONPATH.
Meaning when I import the validate as below:
from validate import required_columns ==> this is a relative import and works in the python terminal bcoz the file is running inside the ingestion folder and finds the validate but this would give error if we import this validate in any other folder for ex. in Airflow folder. Thus always use the absolute path and that can be achieved by running python with -m or setting permanent path variable. For now lets move ahead with the -m. This -m tells python to start looking for the module from the root folder and run the current file as a module.
Thus while using absolute imports run from the bash and while using relative import we can use the python terminal

Why does requirements.txt pin exact versions with == rather than just listing package names?
Answer: thats bcoz if some one take the project from github it will run properly. Since some functions and methods might not be supported by other versions of the libraries. For ex. If pandas releases version 3.0 with a breaking change to how read_csv handles certain dtypes, a project pinned to 2.2.0 will always behave consistently regardless of when or where it is installed. Without pinning, two engineers installing the same project on different days could get different pandas versions and different behaviour."
