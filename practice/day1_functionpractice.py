def add_no(a: int, b: int ) -> int:
    res = a + b
    return res

x,y = map(int,input("Enter 2 nos. : ").split()) #Here the input() will always return a string, so we need the int to be casted here
#split will create a list of 2 strings but we cannot use the elements individually thus the use of map() which will convert the string to integers and inform the interpreter that the 2 nos. are to be treated as seperate nos.

res = add_no(x,y)
print(res)

def ispositive(a: float) -> bool:
    if(a>0):
        return True
    else:
        return False;

z = float(input("Enter a value: "))
print(ispositive(z))


"""An f-string (formatted string literal) is a way to insert variables or expressions directly inside a string in Python."""
def desc_transaction(amt: float, txt: str) -> str:
    print(f'Transaction of {txt} type for amount {amt} requested!!');

"""w/o f-string, the code beccomes"""
def desc_transaction_simple(amt: float, txt: str) -> str:
    print("Transaction of "+ txt +" type for amount " + str(amt) +" requested!!");

desc_transaction(50000 , "credit");
desc_transaction_simple(200000, "debit");

