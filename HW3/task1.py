#task 1 Check for panlindrome
def check_panlindrome(word:str)-> bool:
    word = word.lower()   # lower case the string
    return word == word[::-1]  #reverse the string
check_panlindrome("civic")

