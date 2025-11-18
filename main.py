import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Any, Dict

from database import create_document, get_documents, db
from schemas import Member, Post, Event

app = FastAPI(title="Civic Site Backend")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def read_root():
    return {"message": "Backend running", "endpoints": ["/api/posts", "/api/events", "/api/members", "/test", "/schema"]}


# Public content endpoints
@app.get("/api/posts")
def list_posts(limit: int | None = 10):
    try:
        docs = get_documents("post", {}, limit)
        # Convert ObjectId to string for JSON
        for d in docs:
            if "_id" in d:
                d["id"] = str(d.pop("_id"))
        return {"items": docs}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/events")
def list_events(limit: int | None = 10):
    try:
        docs = get_documents("event", {}, limit)
        for d in docs:
            if "_id" in d:
                d["id"] = str(d.pop("_id"))
        return {"items": docs}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# Membership signup
@app.post("/api/members")
def create_member(member: Member):
    try:
        new_id = create_document("member", member)
        return {"id": new_id, "status": "ok"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/test")
def test_database():
    """Test endpoint to check if database is available and accessible"""
    response: Dict[str, Any] = {
        "backend": "✅ Running",
        "database": "❌ Not Available",
        "database_url": None,
        "database_name": None,
        "connection_status": "Not Connected",
        "collections": []
    }

    try:
        if db is not None:
            response["database"] = "✅ Available"
            response["database_url"] = "✅ Configured"
            response["database_name"] = getattr(db, 'name', '✅ Connected')
            response["connection_status"] = "Connected"
            try:
                collections = db.list_collection_names()
                response["collections"] = collections[:10]
                response["database"] = "✅ Connected & Working"
            except Exception as e:
                response["database"] = f"⚠️  Connected but Error: {str(e)[:50]}"
        else:
            response["database"] = "⚠️  Available but not initialized"
    except Exception as e:
        response["database"] = f"❌ Error: {str(e)[:50]}"

    response["database_url"] = "✅ Set" if os.getenv("DATABASE_URL") else "❌ Not Set"
    response["database_name"] = "✅ Set" if os.getenv("DATABASE_NAME") else "❌ Not Set"

    return response


# Expose schemas for tooling/viewers
@app.get("/schema")
def get_schema():
    return {
        "member": Member.model_json_schema(),
        "post": Post.model_json_schema(),
        "event": Event.model_json_schema(),
    }


if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
