import json
from fastapi import FastAPI, HTTPException, Path, Query

app = FastAPI()

# Robust Helper Function with error trapping
def loadData():
    try:
        with open("students.json", "r") as file:
            return json.load(file)
    except FileNotFoundError:
        # Prevents a complete crash if the file is missing
        return {} 
    except json.JSONDecodeError:
        return {}

@app.get('/students')
def students():
    return loadData()

@app.get('/students/{std_id}')
def getStudentById(
    std_id: str = Path(
        ...,
        description="Required parameter",
        openapi_examples={
            "default": {
                "summary": "Example Student ID",
                "value": "S001"
            }
        }
    )
):
    data = loadData()
    if std_id not in data:
        raise HTTPException(status_code=404, detail=f"Student with this id: {std_id} not found")
    return data[std_id]

@app.get('/filter')
def toFilterStudent(
    course: str = Query(
        None,
        description="Show enrolled students only",
        openapi_examples={
            "default": {
                "summary": "Example Course Name",
                "value": "Python"
            }
        }
    )
):
    data = loadData()
    if course is None:
        return data
    
    filteredDict = {}
    for std_id, info in data.items():
        # Safely handle missing 'course' keys inside students.json entries
        student_course = info.get("course")
        if student_course and student_course.lower() == course.lower():
            filteredDict[std_id] = info
            
    return filteredDict


SORTED_FILTERATIONS = ["name", "age", "marks"]
# Standardized to "desc" to match common query patterns
SORTED_ORDERS = ["asc", "desc"]

@app.get("/sort")
def sortStudents(
    sortedBy: str = Query(
        "marks",  # Provide a default fallback value instead of None
        description="Field to sort students by",
        openapi_examples={
            "default": {
                "summary": "Example sorted by marks, age, or name",
                "value": "marks"
            }
        }
    ),
    orderBy: str = Query(
        "asc",  # Provide a default fallback value instead of None
        description="Order direction: asc or desc",
        openapi_examples={
            "default": {
                "summary": "Example ordered by asc or desc",
                "value": "desc"
            }
        }
    )
):
    data = loadData()
    
    # 1. Validate inputs (Ensure inputs are strictly within permitted options)
    if sortedBy not in SORTED_FILTERATIONS:
        # Added the missing 'f' for proper string interpolation
        raise HTTPException(status_code=400, detail=f"Invalid sorting field '{sortedBy}'. Choose from {SORTED_FILTERATIONS}") 
        
    if orderBy not in SORTED_ORDERS:
        raise HTTPException(status_code=400, detail=f"Invalid sorting order '{orderBy}'. Choose from {SORTED_ORDERS}") 
    
    # 2. Reformat the dictionary dataset into a sortable flat list
    studentsList = []
    for sid, info in data.items():
        # Using .copy() avoids permanently mutating your original loaded dataset references
        student_copy = info.copy()
        student_copy['id'] = sid
        studentsList.append(student_copy)
    
    # 3. Apply sorting logic cleanly
    is_reverse = (orderBy == "desc")
    
    # Lambda safely reads the chosen property, tracking asc vs desc perfectly
    sortedStudentList = sorted(studentsList, key=lambda s: s.get(sortedBy), reverse=is_reverse)
    
    return sortedStudentList


# paginations
@app.get("/pagination")
def paginations(page:int=Query(
        1, ge=1, # Provide a default fallback value instead of None
        description="Paginations of records",
        openapi_examples={
            "default": {
                "summary": "Paginations in num of records",
                "value": "1"
            }
        }
    ),limit:int=Query(
        2,ge=1,le=100,  # Provide a default fallback value instead of None
        description="Limitation per page",
        openapi_examples={
            "default": {
                "summary": "Limitation in num per page",
                "value": "2"
            }
        }
    )):
    data = loadData()
    # conversion dictionary to list
    studentsList = []
    for sid, info in data.items():
        # Using .copy() avoids permanently mutating your original loaded dataset references
        student_copy = info.copy()
        student_copy['id'] = sid
        studentsList.append(student_copy)
    
    startValue = (page-1) * limit
    endValue = startValue + limit
    studentsPerPage = studentsList[startValue:endValue]
    totalStudents = len(studentsList)
    return {
        "page":page,
        "limit":limit,
        "total_students":totalStudents,
        "students_per_page":studentsPerPage,
    }
    