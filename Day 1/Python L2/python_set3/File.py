
def count_word(input):
    try:
        with open(input,"r") as file:
            text=file.read()
            words=text.split()
            return len(words)
    except FileNotFoundError:
        return "File not Found"
    
    
res=count_word("input.txt")
print(res)