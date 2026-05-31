def salary_calculation(sal : int) -> int:
    if (sal<0):
        raise ValueError("Salary cannot be negative!!")
    return 1000/sal

try:
    salary = int(input("Please enter your current salary: "))
    bonus = salary_calculation(salary)
    print(bonus)
except ValueError as e:
    print(e)
except ZeroDivisionError as e:
    print(e)
finally: #Always executes
    print("Process Finished!!!")

############################################################################################################################################################################################

def load_data():
    try:
        int("abc")
    except ValueError as e:
        raise RuntimeError("Data Pipeline failed!") from e; # Python chains the exceptions automatically using from e after raising the error thus preserving the original cause of exception.

#load_data() # Gives entire stack trace if the function is not explicitly handled.

try:
    load_data() # If the fucntion is handled then it only prints -->"Pipeline Failed: Data Pipeline failed!"
except RuntimeError as e:
    print(f"Pipeline Failed: {e}"); 

###############################################################################################################################################################################################

# employee = {
#     name: "Ankita",
#     department: "IT"
# }

try:
    file = open("employee.txt")
    print(employee[salary]) #When the file do not exist this line is not executed as the except stmt would be searched for.
except FileNotFoundError:
    print("File dosen't exist");
except KeyError:
    print("Salary key Missing");
except Exception as e:
    print(f"Unexpected Error: {e}");
