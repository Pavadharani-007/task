from sqlalchemy import Column, Integer, String, ForeignKey, Table
from sqlalchemy.orm import relationship
from .database import Base

employee_project = Table('Employee_project', Base.metadata,
    Column('employee_id', Integer, ForeignKey('employees.id')),
    Column('project_id', Integer, ForeignKey('projects.id'))
)


class Employee(Base):
    __tablename__ = 'employees'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    email = Column(String, unique=True, index=True)
    designation = Column(String, index=True)
    payroll = Column(String, index=True)
    company_id = Column(Integer, ForeignKey('companies.id'))
    projects = relationship('Project', secondary=employee_project, back_populates='employees')
    company = relationship("Company", back_populates="employees")

class Project(Base):
    __tablename__ = 'projects'
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(String, index=True)
    employees = relationship('Employee', secondary=employee_project, back_populates='projects')

class Company(Base):
    __tablename__ = "companies"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    gst_no = Column(String, unique=True, index=True)
    
    employees = relationship("Employee", back_populates="company")




# association_table = Table('association', Base.metadata,
#     Column('employee_id', Integer, ForeignKey('employees.id')),
#     Column('project_id', Integer, ForeignKey('projects.id'))
# )

# class Employee(Base):
#     __tablename__ = "employees"
    
#     id = Column(Integer, primary_key=True, index=True)
#     name = Column(String, index=True)
#     designation = Column(String)
#     payroll = Column(String)
#     company_id = Column(Integer, ForeignKey('companies.id'))
    
#     company = relationship("Company", back_populates="employees")
#     projects = relationship("Project", secondary=association_table, back_populates="employees")

# class Project(Base):
#     __tablename__ = "projects"
    
#     id = Column(Integer, primary_key=True, index=True)
#     title = Column(String, index=True)
#     description = Column(String)
    
#     employees = relationship("Employee", secondary=association_table, back_populates="projects")

# class Company(Base):
#     __tablename__ = "companies"
    
#     id = Column(Integer, primary_key=True, index=True)
#     name = Column(String, index=True)
#     gst_no = Column(String, unique=True, index=True)
    
#     employees = relationship("Employee", back_populates="company")
