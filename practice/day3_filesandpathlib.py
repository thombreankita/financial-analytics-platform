from pathlib import Path

#print(Path.cwd())  

for p in Path().iterdir():  #by default path will show current working directory
    print(p)

my_file = Path("day1_functionpractice.py")

print(my_file.name)
print(my_file.suffix)
print(my_file.stem)
print(f'The parent is : {my_file.parent}')
print(f'The absolute path is : {my_file.parent.absolute()}') # or my_file.absolute()
print(f'The resolved path is : {my_file.resolve()}') # this method give a absolute path and also gives reletive directory references.

p = Path.home()
print(p) #prints the user home directory
#can also be achieved by 
p2= Path("Users\Admin").expanduser()
print(p2)

#searching the files using glob()
d = Path(my_file.parent)

for p in d.glob("*day*"): #searhes all files that have 'day' in the file name
    print(p)

#by default glob searchs only the directory and not the subdir. so for the subdirs we have recursive glob
for p in d.rglob("*day*"):
    print(p)

#File access

a = Path.home() / "Documents" / "Sample.txt"

try:
    if(print(a.exists())):
        with a.open() as f :
            print(f.read())
    else:
        raise FileExistsError (f'{a} File Do not exist!!');
except FileExistsError as e:
    print(e)

print(my_file.stem)
with open(my_file) as f:
    print(f.read())
