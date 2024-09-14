from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import numpy as np
from faiss_embedding import get_faiss_index, get_model, add_document_to_index
from models import User, Base
from database import engine, get_db
from sqlalchemy.orm import Session

app = FastAPI()

index = get_faiss_index()
model = get_model()

@app.get("/health")
async def health():
    return {"status": "active"}

documents = [
    "Jio AI-Cloud Welcome Offer: Reliance has announced the Jio AI-Cloud Welcome Offer to be launched this Diwali...",
    "Reliance is focusing on AI-driven services through Jio Phone and Jio Home IoT services...",
    "Jio TvOS and Jio Home IoT systems are part of their AI-Cloud offerings...",
    "Jio AI-Cloud Welcome Offer: Reliance has announced the Jio AI-Cloud Welcome Offer to be launched this Diwali...",
    "Jio AI-Cloud Welcome Offer: Reliance has announced the Jio AI-Cloud Welcome Offer to be launched this Diwali..."
]

add_document_to_index(documents[0])
add_document_to_index(documents[1])
add_document_to_index(documents[2])

def update_user_request_count(user_id: str, db: Session):
    user = db.query(User).filter(User.user_id == user_id).first()
    if user:
        user.request_count += 1
        db.commit()
    else:
        new_user = User(user_id=user_id, request_count=1)
        db.add(new_user)
        db.commit()

class SearchRequest(BaseModel):
    text: str = "example query"  
    top_k: int = 5               
    threshold: float = 0.5       

@app.post("/search")
async def search(search_request: SearchRequest):
    query_text = search_request.text
    top_k = search_request.top_k
    threshold = search_request.threshold

    query_embedding = model.encode([query_text])
    query_embedding = np.array(query_embedding).astype('float32')

    distances, indices = index.search(query_embedding, top_k)

    results = []
    print(distances)
    for i, distance in enumerate(distances[0]):
        print(distance)
        print(threshold)
        if distance <= threshold:
            doc_index = indices[0][i]
            results.append({
                "document": documents[doc_index],
                "distance": float(distance)
            })

    if not results:
        raise HTTPException(status_code=404, detail="No documents found matching the query.")

    return {"results": results}