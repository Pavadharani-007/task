from typing import List,Optional
from pydantic import BaseModel


class EmployeeBase(BaseModel):
    name: str
    email: str
    designation: str
    payroll: str
    company_id: int 

class ProjectBase(BaseModel):
    title: str
    description: str

class ProjectCreate(ProjectBase):
    pass

class EmployeeCreate(EmployeeBase):
    pass

class Employee(EmployeeBase):
    id: int
    
    class Config:
        orm_mode = True

class Project(ProjectBase):
    id: int
    class Config:
        orm_mode = True

class EmployeeWithProjects(EmployeeBase):
    id: int
    projects: List[Project] = []
    class Config:
        orm_mode = True

class ProjectWithEmployees(ProjectBase):
    id: int
    employees: List[Employee] = []
    class Config:
        orm_mode = True

class CompanyBase(BaseModel):
    name: str
    gst_no:str

class CompanyCreate(CompanyBase):
    pass

class Company(CompanyBase):
    id: int
    

    class Config:
        orm_mode = True


# class EmployeeBase(BaseModel):
#     name: str
#     email: str
#     designation: str
#     payroll: str
    

# class ProjectBase(BaseModel):
#     title: str
#     description: str

# class ProjectCreate(ProjectBase):
#     pass

# class EmployeeCreate(EmployeeBase):
#     pass

# class Employee(EmployeeBase):
#     id: int
#     class Config:
#         orm_mode = True

# class Project(ProjectBase):
#     id: int
#     class Config:
#         orm_mode = True

# class EmployeeWithProjects(EmployeeBase):
#     id: int
#     projects: List[Project] = []
#     class Config:
#         orm_mode = True

# class ProjectWithEmployees(ProjectBase):
#     id: int
#     employees: List[Employee] = []
#     class Config:
#         orm_mode = True


# class CompanyBase(BaseModel):
#     name: str
#     gst_no:str

# class CompanyCreate(CompanyBase):
#     pass

# class Company(CompanyBase):
#     id: int
#     employees: List[EmployeeWithProjects] = []  # List of employees with their associated projects

#     class Config:
#         orm_mode = True