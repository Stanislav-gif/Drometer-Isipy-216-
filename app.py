import datetime
from typing import List, Optional
from fastapi import FastAPI, Form
from fastapi.responses import HTMLResponse
from pydantic import BaseModel

class Request(BaseModel):
    number: int
    data: datetime.date
    typeEquip: str
    modul: str
    problemDescription: str
    clientName: str
    phoneNumber: str
    status: str = "Новая заявка"
    responsible: Optional[str] = None
    comments: Optional[List[str]] = []
    parts: Optional[List[str]] = []


repo = [
    Request(
        number=1,
        data=datetime.date(2020, 7, 16),
        typeEquip="Клавиатура",
        modul="ARDOR",
        problemDescription="Залипает клавиша",
        clientName="Иван Иванов Александрович",
        phoneNumber="+79521859240"
    ),
    Request(
        number=2,
        data=datetime.date(2021, 6, 15),
        typeEquip="Мышь",
        modul="DEXP",
        problemDescription="Залипает кнопка",
        clientName="Иван Иванов Александрович",
        phoneNumber="+79521859240"
    ),
    Request(
        number=3,
        data=datetime.date(2021, 6, 15),
        typeEquip="Мышь",
        modul="DEXP",
        problemDescription="Залипает кнопка",
        clientName="Иван Иванов Александрович",
        phoneNumber="+79521859240"
    )
]

app = FastAPI()

@app.get("/requests/", response_model=List[Request])
def get_requests():
    return repo

@app.post("/requests/")
def create_request(
    number: int = Form(...),
    data: str = Form(...),
    typeEquipce: str = Form(...),
    modul: str = Form(...),
    problemDescription: str = Form(...),
    clientName: str = Form(...),
    phoneNumber: str = Form(...)
):
    new_request = Request(
        number = number,
        data=data,
        typeEquipce=typeEquipce,
        modul=modul,
        problemDescription=problemDescription,
        clientName=clientName,
        phoneNumber=phoneNumber
    )
    repo.append(new_request)
    return new_request

@app.put("/requests/{request_number}")
def edit_request(request_number: int, updated_request: Request):
    for request in repo:
        if request.number == request_number:
            request.status = updated_request.status
            request.problemDescription = updated_request.problemDescription
            request.responsible = updated_request.responsible
            request.comments = updated_request.comments
            request.parts = updated_request.parts
            return {"message": "Request updated successfully", "request": request}
    return {"error": "Request not found"}

@app.put("/requests/{request_number}/assign")
def assign_technician(request_number: int, responsible_name: str):
    for request in repo:
        if request.number == request_number:
            request.responsible = responsible_name
            return {"message": "Technician assigned", "request": request}
    return {"error": "Request not found"}


@app.get("/requests/status/{request_number}", response_model=Request)
def get_request_status(request_number: int):
    for request in repo:
        if request.number == request_number:
            return request
    return {"error": "Request not found"}

@app.put("/requests/{request_number}/comment")
def add_comment(request_number: int, comment: str):
    for request in repo:
        if request.number == request_number:
            request.comments.append(comment)
            return {"message": "Comment added", "request": request}
    return {"error": "Request not found"}

@app.put("/requests/{request_number}/parts")
def add_parts(request_number: int, parts: List[str]):
    for request in repo:
        if request.number == request_number:
            request.parts.extend(parts)
            return {"message": "Parts added", "request": request}
    return {"error": "Request not found"}

@app.get("/statistics/")
def get_statistics():
    completed_requests = [req for req in repo if req.status == "Завершена"]
    average_time = None
    if completed_requests:
        total_time = sum([(datetime.date.today() - req.data).days for req in completed_requests])
        average_time = total_time / len(completed_requests)
    issues_stats = {}
    for req in repo:
        if req.problemDescription in issues_stats:
            issues_stats[req.problemDescription] += 1
        else:
            issues_stats[req.problemDescription] = 1

    return {
        "total_requests": len(repo),
        "completed_requests": len(completed_requests),
        "average_completion_time": average_time,
        "issues_statistics": issues_stats
    }

