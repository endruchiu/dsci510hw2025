#!/usr/bin/env python
# coding: utf-8

# In[1]:


#task 1 tuple transformation  | Tuples in chapter 10 
def transform_tuple(original_tuple) -> (int, int):    # num for num to iterate through the tuple
    even_sum = sum(num for num in original_tuple if num % 2 == 0) #234 + 324 == compare if remainder is 0 which is even
    odd_sum = sum(num for num in original_tuple if num % 2 == 1) # compare if remainder is 1 which means odd num
    return (even_sum, odd_sum)

transform_tuple((234, 324, 5, 53, 75))


# In[2]:


#task 2 unique letters  | set lecture 2/12 and set operations in PFE
def unique_letters(string1:str, string2:str) -> (set,set,set):
    firstset = set(string1)
    secondset = set(string2)
    return (firstset - secondset, secondset- firstset, firstset&secondset) #unqiue 1, unique2, intersection

unique_letters("Alexy Tregubov", "Srinath Begudem")  #capitalize letters count as unique letter as well 


# In[14]:


#task 3 grade summary function  | dictionary chapter 9 , sorting (lecture 2/12)
def grade_summary(student_grades:dict) -> dict:
    result = {
        student: { "average": round(sum(grades) / len(grades), 2), "highest": max(grades) }  #len(grades) count how many grades
        for student, grades in student_grades.items() } #key value pair student, grades
    return result

grades= {"Bob": [75, 78, 80], "Alice": [88, 92, 100]}  #Without sorting bob will come first
print(grade_summary(grades))
    


# In[13]:


#task 3 grade summary function extra credit | dictionary chapter 9 , sorting (lecture 2/12) 
def grade_summary(student_grades:dict) -> dict:
    result = {
        student: { "average": round(sum(grades) / len(grades), 2), "highest": max(grades) }  #len(grades) count how many grades
        for student, grades in student_grades.items() } #key value pair student, grades
    return dict(sorted(result.items()))  #sorted function for the key value pair of student, grades 

grades= {"Bob": [75, 78, 80], "Alice": [88, 92, 100]}   # Alice comes first even If i put bob first
print(grade_summary(grades))
    


# In[2]:


#Task 4 grade summary program
import csv
import argparse

def read_students(file:str) -> dict:
    students = {}
    with open(file, newline= "") as csvfile:
        reader = csv.reader(csvfile)
        next(reader)
        for row in reader:
            student_id, name, *grades = row
            grades = [int(g) for g in grades if g.strip().isdigit()]
            students[name] = grades
        return students

def grade_summary(students: dict) -> dict:
    result = {
        student: { "average": round(sum(grades) / len(grades), 2), "highest": max(grades) }  
        for student, grades in students.items() } 
    return dict(sorted(result.items()))  

def write_averages(file:str, averages: dict):
    with open(file, "w", newline= "") as csvfile:
        writer= csv.writer(csvfile)
        writer.writerow(["student_name", "average_grade", "highest"])
        for student, stats in averages.items():
            writer.writerow([student, stats["average"], stats["highest"]])

def main():
    parser = argparse.ArgumentParser(description='Process student grades.')
    parser.add_argument('input_file', type=str, help='csv file with student grades')
    parser.add_argument('output_file', type=str, help='csv file to write summaries')
    
    args = parser.parse_args()
    students = read_students(args.input_file)
    summaries = grade_summary(students)
    write_averages(args.output_file, summaries)

if __name__ == "__main__":
    main()

    



# In[ ]:




