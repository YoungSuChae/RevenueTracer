# Class Department
# Designed by Owen Oliveira
# Version 1.0.6
import csv

#Define a class Department to hold all of departments functionality 
class Department:
#Getters and setters for each function
    def __init__(self, department_name, department_description):
        self._department_name = department_name
        self._department_description = department_description

    def __str__(self) -> str:
        return f"{self._department_name},{self._department_description}\n"

    def get_department_name(self):
        return self._department_name

    def set_department_name(self, value):
        self._department_name = value

    def get_department_description(self):
        return self._department_description

    def set_department_description(self, value):
        self._department_description = value

    # Function to write to the file
    @staticmethod
    def write_to_file(department_list):
        with open('departmentInfo.csv', 'w') as file:
            for department in department_list:
                file.write(str(department))

    # Remove a department that the user specifies
    @staticmethod
    def delete_from_file(department_name):
        with open("department.csv", "r") as file:
            reader = csv.reader(file)
            departments = list(reader)

        department_del = False

        # Iterate through stores and remove the one that matches the name
        for department in departments:
            if department[0] == department_name:
                departments.remove(department)
                department_del = True
                break  # Stop iteration after deleting the store

        # Rewrite the updated list of stores back to the CSV file
        if department_del:
            with open("department.csv", "w", newline="") as file:
                writer = csv.writer(file)
                writer.writerows(departments)
            return f"Department {department} was deleted successfully"
        else:
            return f"Department {department[0]} was not found"

    # Function to add a department and name
    @staticmethod
    def add_department(department_name, department_description):
        new_department = Department(department_name, department_description)
        with open('department.csv', 'a') as file:
            file.write(str(new_department))
        return f"Department {department_name} was added successfully"

    # Function to search the csv file for the name of the department
    @staticmethod
    def search_file(search_name):
        with open('department.csv', 'r') as file:
            for line in file:
                fields = line.strip().split(',')
                if len(fields) == 2:
                    department_name, department_desc = fields
                    if search_name == department_name:
                        return f"Department Name: {department_name}, Description: {department_desc}"
        return "Department not found"
