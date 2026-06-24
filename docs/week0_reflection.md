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
Ans: in this case the __name__ is set to '__main__'.
==> __Main__ is the top level environment or can be said as the entry point of the program. When a script runs directly from the interpreter the __name__ is set to __main__ but when a script is imported inside another file, the __name__ of the imported script/module is set to the module name or to absolute module name/path.

Important point:
Relative imports work when running a file directly but break when the file is imported as part of a package. Absolute imports are the correct production style and require running with python -m or setting PYTHONPATH.
Meaning when I import the validate as below:
from validate import required_columns ==> this is a relative import and works in the python terminal bcoz the file is running inside the ingestion folder and finds the validate but this would give error if we import this validate in any other folder for ex. in Airflow folder. Thus always use the absolute path and that can be achieved by running python with -m or setting permanent path variable. For now lets move ahead with the -m. This -m tells python to start looking for the module from the root folder and run the current file as a module.
Thus while using absolute imports run from the bash and while using relative import we can use the python terminal.
Absolute imports work correctly when running from the project root with python -m. Relative imports like from validate import x only work when running a file directly from inside its own folder — this breaks in production where files import each other across packages. Always use absolute imports in this project

Why does requirements.txt pin exact versions with == rather than just listing package names?
Answer: thats bcoz if some one take the project from github it will run properly. Since some functions and methods might not be supported by other versions of the libraries. For ex. If pandas releases version 3.0 with a breaking change to how read_csv handles certain dtypes, a project pinned to 2.2.0 will always behave consistently regardless of when or where it is installed. Without pinning, two engineers installing the same project on different days could get different pandas versions and different behaviour."

Q1: What is the difference between a parameter and an argument in Python?
Ans: Parameter is present in the function definition using type hints. Argument is passed when the funtion is called. A parameter is the variable name defined in the function signature. An argument is the actual value passed when the function is called. Example: in def load_raw_data(fp: Path), fp is the parameter. When you call load_raw_data(filepath), filepath is the argument.
 
Q4: Why would you use pathlib.Path instead of a plain string for file paths?
Ans: Path provides more functions and methods for file manipulation.pathlib.Path handles Windows and Mac path differences automatically — on Windows paths use backslashes, on Mac forward slashes. Path also provides useful attributes like .suffix, .stem, .parent, and methods like .exists() and .stat() that would require os.path and separate imports with plain strings.

Q5: You call a function that returns None but you expected a DataFrame. What are the two most likely causes?
Ans: Consider this example: def write_partitioned_output(df: pd.DataFrame, opfile: str | Path) -> None:
if this function is called as 
result = write_partitioned_output(df, output_path)
print(result)
then the reult will store as None and print as None. If u are expecting a dataframe then give type hint dataframe

Even consider this function def check_number(value: float) -> str:
    if value > 0:
        return "positive"
        
print(check_number(-5)) --> here the output will be assigned as NULL implicitly

What does nrows=None as a default parameter mean? What is this pattern called in Python?
nrows=None in the function defn as a argument specifies that it is ok if no parameter is passed to the function for this attribute

Q2: Why is VIOLATION_THRESHOLD = 0.05 at the top of the file better than 0.05 hardcoded inside the function?
because the constant once declare won't change through out the program niether can it be updated '

Q3. Finally block should not print completed always I can add a variable of flag that checks if no error is raised and only in that case it will print completed

## QUESTIONS ##
Phase 1 Interview Questions — Prepare These Now
You will answer these in writing on Day 20 but start thinking about them now:
Q1: What is the difference between hard validation and soft validation? Give an example of each from your pipeline.
Q2: Your ingestion script takes 73 seconds on 6.3M rows. An interviewer asks how you would make it faster. What are three specific things you would try?
Q3: What does idempotent mean and how did you verify your pipeline is idempotent?
Q4: Walk me through what happens when load_raw_data is called with a path to a file that does not exist. Trace the exact execution path.
Q5: Why did you separate validate_schema and validate_business_rules into two functions instead of one?


## IMPORTANT POINTS ##
- df_type.to_csv(o_file, index=False) overwrites by default. That makes your pipeline IDEMPOTENT — run it twice, same result.
- PARAMETERISED EXECUTION where in for testing a case, instead of running the case on entire dataset it will be executed on for a part of dataset. Very helpful for testing purpose.