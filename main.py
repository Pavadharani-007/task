from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from . import models, schemas
from .database import SessionLocal, engine

app = FastAPI()

models.Base.metadata.create_all(engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
@app.post("/employees/", response_model=schemas.Employee, tags=["Employee Operations"])
def create_employee(employee: schemas.EmployeeCreate, db: Session = Depends(get_db)):
    # Check if the company_id exists
    db_company = db.query(models.Company).filter(models.Company.id == employee.company_id).first()
    if db_company is None:
        raise HTTPException(status_code=404, detail="Company not found")

    db_employee = models.Employee(
        name=employee.name,
        email=employee.email,
        designation=employee.designation,
        payroll=employee.payroll,
        company_id=employee.company_id
    )
    db.add(db_employee)
    db.commit()
    db.refresh(db_employee)
    return db_employee


@app.get('/Employee', response_model=List[schemas.Employee], tags=['Details of Employee'])
def get_emp(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    employees = db.query(models.Employee).offset(skip).limit(limit).all()
    return employees

@app.get('/Employee/{Emp_id}', status_code=200, response_model=schemas.Employee, tags=['Details of Employee'])
def show_employee(employee_id: int, db: Session = Depends(get_db)):
    Employees = db.query(models.Employee).filter(models.Employee.id == employee_id).first()
    if not Employees:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Employee with id {employee_id} not found')
    return Employees

@app.delete('/Employee/{Emp_id}', status_code=status.HTTP_200_OK, tags=['Details of Employee'])
def destroy_employee(employee_id: int, db: Session = Depends(get_db)):
    deleted = db.query(models.Employee).filter(models.Employee.id == employee_id).delete(synchronize_session=False)
    db.commit()
    if not deleted:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Employee with id {employee_id} not found")
    return 'Deleted successfully'

@app.put('/Employees/{Emp_id}', status_code=status.HTTP_202_ACCEPTED, tags=['Details of Employee'])
def update_employee(employee_id: int, request: schemas.EmployeeCreate, db: Session = Depends(get_db)):
    Update = db.query(models.Employee).filter(models.Employee.id == employee_id).first()
    if not Update:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Employee not found")
    for key, value in request.dict().items():
        setattr(Update, key, value)
    db.commit()
    db.refresh(Update)
    return Update



@app.post('/Projects/', response_model=schemas.Project, tags=['Details of Project'])
def create_project(request: schemas.ProjectCreate, db: Session = Depends(get_db)):
    Project = models.Project(title=request.title, description=request.description)
    db.add(Project)
    db.commit()
    db.refresh(Project)
    return Project

@app.get('/Projects/', response_model=List[schemas.Project], tags=['Details of Project'])
def get_project(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    Getting_projects = db.query(models.Project).offset(skip).limit(limit).all()
    return Getting_projects

@app.get('/Projects/{Proj_id}', status_code=200, response_model=schemas.Project, tags=['Details of Project'])
def show_project(project_id: int, db: Session = Depends(get_db)):
    project = db.query(models.Project).filter(models.Project.id == project_id).first()
    if not project:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Project with id {project_id} not found')
    return project

@app.delete('/Projects/{Proj_id}', status_code=status.HTTP_200_OK, tags=['Details of Project'])
def destroy_project(project_id: int, db: Session = Depends(get_db)):
    deleted = db.query(models.Project).filter(models.Project.id == project_id).delete(synchronize_session=False)
    db.commit()
    if not deleted:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Project with id {project_id} not found")
    return 'Deleted Successfully'

@app.put('/Projects/{Proj_id}', status_code=status.HTTP_202_ACCEPTED, tags=['Details of Project'])
def update_project(project_id: int, request: schemas.ProjectCreate, db: Session = Depends(get_db)):
    db_project = db.query(models.Project).filter(models.Project.id == project_id).first()
    if not db_project:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Project not found")
    for key, value in request.dict().items():
        setattr(db_project, key, value)
    db.commit()
    db.refresh(db_project)
    return 'updated'



@app.post('/Projects/{Proj_id}/Employees/{Emp_id}', tags=['Assignment Projects and Employees'])
def employee_to_project(project_id: int, employee_id: int, db: Session = Depends(get_db)):
    project = db.query(models.Project).filter(models.Project.id == project_id).first()
    employee = db.query(models.Employee).filter(models.Employee.id == employee_id).first()
    if not project or not employee:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Project or Employee not found")
    project.employees.append(employee)
    db.commit()
    return 'Employee Assigned to project '

@app.post('/Employees/{Emp_id}/Projects/{Proj_id}', tags=['Assignment Projects and Employees'])
def project_to_employee(employee_id: int, project_id: int, db: Session = Depends(get_db)):
    project = db.query(models.Project).filter(models.Project.id == project_id).first()
    employee = db.query(models.Employee).filter(models.Employee.id == employee_id).first()
    if not project or not employee:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Project or Employee not found")
    employee.projects.append(project)
    db.commit()
    return 'Project assigned to Employee '


@app.get('/Employees/{Emp_id}/Projects', response_model=schemas.EmployeeWithProjects, tags=['Assignment Projects and Employees'])
def get_employee_project(employee_id: int, db: Session = Depends(get_db)):
    Employee = db.query(models.Employee).filter(models.Employee.id == employee_id).first()
    if not Employee:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Employee not found")
    return Employee


@app.get('/Projects/{Proj_id}/Employees', response_model=schemas.ProjectWithEmployees, tags=['Assignment Projects and Employees'])
def get_project_employee(project_id: int, db: Session = Depends(get_db)):
    Project = db.query(models.Project).filter(models.Project.id == project_id).first()
    if not Project:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Project not found")
    return Project


@app.post("/companies/", response_model=schemas.Company, tags=["Company Operations"])
def create_company(company: schemas.CompanyCreate, db: Session = Depends(get_db)):
    db_company = models.Company(name=company.name, gst_no=company.gst_no)
    db.add(db_company)
    db.commit()
    db.refresh(db_company)
    return db_company

@app.get("/{company_id}", response_model=schemas.Company)
def read_company(company_id: int, db: Session = Depends(get_db)):
    db_company = db.query(models.Company).filter(models.Company.id == company_id).first()
    if db_company is None:
        raise HTTPException(status_code=404, detail="Company not found")
    return db_company

@app.get("/", response_model=List[schemas.Company])
def read_companies(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    companies = db.query(models.Company).offset(skip).limit(limit).all()

@app.put("/{company_id}", response_model=schemas.Company)
def update_company(company_id: int, company: schemas.CompanyCreate, db: Session = Depends(get_db)):
    db_company = db.query(models.Company).filter(models.Company.id == company_id).first()
    if db_company is None:
        raise HTTPException(status_code=404, detail="Company not found")
    db_company.name = company.name
    db.commit()
    db.refresh(db_company)
    return db_company

@app.delete("/{company_id}")
def delete_company(company_id: int, db: Session = Depends(get_db)):
    db_company = db.query(models.Company).filter(models.Company.id == company_id).first()
    if db_company is None:
        raise HTTPException(status_code=404, detail="Company not found")
    db.delete(db_company)
    db.commit()
    return {"ok": True}


# @app.post('/Projects/', response_model=schemas.Project, tags=['Details of Project'])
# def create_project(request: schemas.ProjectCreate, db: Session = Depends(get_db)):
#     Project = models.Project(title=request.title, description=request.description)
#     db.add(Project)
#     db.commit()
#     db.refresh(Project)
#     return Project

# @app.get('/Projects/', response_model=List[schemas.Project], tags=['Details of Project'])
# def get_project(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
#     Getting_projects = db.query(models.Project).offset(skip).limit(limit).all()
#     return Getting_projects

# @app.get('/Projects/{Proj_id}', status_code=200, response_model=schemas.Project, tags=['Details of Project'])
# def show_project(project_id: int, db: Session = Depends(get_db)):
#     project = db.query(models.Project).filter(models.Project.id == project_id).first()
#     if not project:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Project with id {project_id} not found')
#     return project

# @app.delete('/Projects/{Proj_id}', status_code=status.HTTP_200_OK, tags=['Details of Project'])
# def destroy_project(project_id: int, db: Session = Depends(get_db)):
#     deleted = db.query(models.Project).filter(models.Project.id == project_id).delete(synchronize_session=False)
#     db.commit()
#     if not deleted:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Project with id {project_id} not found")
#     return 'Deleted Successfully'

# @app.put('/Projects/{Proj_id}', status_code=status.HTTP_202_ACCEPTED, tags=['Details of Project'])
# def update_project(project_id: int, request: schemas.ProjectCreate, db: Session = Depends(get_db)):
#     db_project = db.query(models.Project).filter(models.Project.id == project_id).first()
#     if not db_project:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Project not found")
#     for key, value in request.dict().items():
#         setattr(db_project, key, value)
#     db.commit()
#     db.refresh(db_project)
#     return 'updated'



# @app.post('/Projects/{Proj_id}/Employees/{Emp_id}', tags=['Assignment Projects and Employees'])
# def employee_to_project(project_id: int, employee_id: int, db: Session = Depends(get_db)):
#     project = db.query(models.Project).filter(models.Project.id == project_id).first()
#     employee = db.query(models.Employee).filter(models.Employee.id == employee_id).first()
#     if not project or not employee:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Project or Employee not found")
#     project.employees.append(employee)
#     db.commit()
#     return 'Employee Assigned to project '

# @app.post('/Employees/{Emp_id}/Projects/{Proj_id}', tags=['Assignment Projects and Employees'])
# def project_to_employee(employee_id: int, project_id: int, db: Session = Depends(get_db)):
#     project = db.query(models.Project).filter(models.Project.id == project_id).first()
#     employee = db.query(models.Employee).filter(models.Employee.id == employee_id).first()
#     if not project or not employee:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Project or Employee not found")
#     employee.projects.append(project)
#     db.commit()
#     return 'Project assigned to Employee '


# @app.get('/Employees/{Emp_id}/Projects', response_model=schemas.EmployeeWithProjects, tags=['Assignment Projects and Employees'])
# def get_employee_project(employee_id: int, db: Session = Depends(get_db)):
#     Employee = db.query(models.Employee).filter(models.Employee.id == employee_id).first()
#     if not Employee:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Employee not found")
#     return Employee


# @app.get('/Projects/{Proj_id}/Employees', response_model=schemas.ProjectWithEmployees, tags=['Assignment Projects and Employees'])
# def get_project_employee(project_id: int, db: Session = Depends(get_db)):
#     Project = db.query(models.Project).filter(models.Project.id == project_id).first()
#     if not Project:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Project not found")
#     return Project

# @app.post("/", response_model=schemas.Company)
# def create_company(company: schemas.CompanyCreate, db: Session = Depends(get_db)):
#     db_company = models.Company(name=company.name,gst_no=company.gst_no)
#     db.add(db_company)
#     db.commit()
#     db.refresh(db_company)
#     return db_company

# @app.get("/{company_id}", response_model=schemas.Company)
# def read_company(company_id: int, db: Session = Depends(get_db)):
#     db_company = db.query(models.Company).filter(models.Company.id == company_id).first()
#     if db_company is None:
#         raise HTTPException(status_code=404, detail="Company not found")
#     return db_company

# @app.get("/", response_model=List[schemas.Company])
# def read_companies(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
#     companies = db.query(models.Company).offset(skip).limit(limit).all()

# @app.put("/{company_id}", response_model=schemas.Company)
# def update_company(company_id: int, company: schemas.CompanyCreate, db: Session = Depends(get_db)):
#     db_company = db.query(models.Company).filter(models.Company.id == company_id).first()
#     if db_company is None:
#         raise HTTPException(status_code=404, detail="Company not found")
#     db_company.name = company.name
#     db.commit()
#     db.refresh(db_company)
#     return db_company

# @app.delete("/{company_id}")
# def delete_company(company_id: int, db: Session = Depends(get_db)):
#     db_company = db.query(models.Company).filter(models.Company.id == company_id).first()
#     if db_company is None:
#         raise HTTPException(status_code=404, detail="Company not found")
#     db.delete(db_company)
#     db.commit()
#     return {"ok": True}