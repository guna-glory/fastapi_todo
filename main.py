from fastapi import FastAPI,Depends,HTTPException
from schemas import Todo as TodoSchema ,TodoCreate
from database import SessionLocal,Base,engine
from sqlalchemy.orm import Session
from models import Todo

app=FastAPI()
@app.on_event("startup")
def startup_event():
    Base.metadata.create_all(bind=engine)


def get_db():
    db=SessionLocal()
    try:
        yield db
    finally:
        db.close()
@app.post("/todos",response_model=TodoSchema)
def create_todo(todo:TodoCreate, db: Session = Depends(get_db)):
    db_todo=Todo(**todo.model_dump())
    db.add(db_todo)
    db.commit()
    db.refresh(db_todo)
    return db_todo

@app.get("/todos",response_model=list[TodoSchema])
def read_todos(db: Session = Depends(get_db)):
    return db.query(Todo).all()

@app.get("/todos/{todo_id}",response_model=TodoSchema)
def read_todo(todo_id : int,db: Session = Depends(get_db)):
    todo=db.query(Todo).filter(Todo.id==todo_id).first()
    if not Todo:
        raise HTTPException(status_code=404,delail="Todo not found")
    return todo

@app.put("/todos/{todo_id}",response_model=TodoSchema)
def updeate_todo(todo_id : int, updated : TodoCreate,db:Session=Depends(get_db)):
    todo=db.query(Todo).filter(Todo.id==todo_id).first()
    if not Todo:
        raise HTTPException(status_code=404,delail="Todo not found")
    for key,value in updated.model_dump().items():
        setattr(todo,key,value)
    db.commit()
    db.refresh(todo)
    return todo
@app.delete("/todos/{todo_id}")
def delete_todo(todo_id :int,db:Session=Depends(get_db)):
    todo=db.query(Todo).filter(Todo.id==todo_id).first()
    if not Todo:
        raise HTTPException(status_code=404,delail="Todo not found")
    db.delete(todo)
    db.commit()
    return {"message":"Todo deleted successfully"}
    
