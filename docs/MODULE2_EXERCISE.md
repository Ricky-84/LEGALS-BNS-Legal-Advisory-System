# Module 2 Exercise: Create Your First Endpoint

## Task
Create a new endpoint that returns information about supported legal domains.

## Step 1: Create a new router file

Create file: `backend/app/routers/domains.py`

```python
"""
Legal domains information endpoint
"""
from fastapi import APIRouter

router = APIRouter()


@router.get("/")
async def get_domains():
    """Get list of supported legal domains"""
    return {
        "total_domains": 2,
        "domains": [
            {
                "name": "BNS Chapter 17",
                "description": "Offences Against Property",
                "sections": 32
            },
            {
                "name": "Motor Vehicle Act Chapter 13",
                "description": "Traffic Violations",
                "sections": "TBD"
            }
        ]
    }


@router.get("/{domain_name}")
async def get_domain_details(domain_name: str):
    """Get details of a specific domain"""
    # This uses path parameters!
    domains_data = {
        "bns": {
            "full_name": "Bharatiya Nyaya Sanhita Chapter 17",
            "coverage": "theft, robbery, extortion, cheating, etc.",
            "status": "active"
        },
        "mva": {
            "full_name": "Motor Vehicle Act Chapter 13",
            "coverage": "traffic violations, penalties",
            "status": "coming_soon"
        }
    }

    if domain_name in domains_data:
        return domains_data[domain_name]
    else:
        return {"error": "Domain not found"}
```

## Step 2: Register the router

Add to `backend/app/routers/__init__.py`:

```python
from .domains import router as domains_router

# Add to api_router
api_router.include_router(domains_router, prefix="/domains", tags=["domains"])
```

## Step 3: Test it

1. Run the backend: `uvicorn main:app --reload`
2. Visit: http://localhost:8000/api/v1/domains/
3. Visit: http://localhost:8000/api/v1/domains/bns
4. Visit: http://localhost:8000/api/docs (see your new endpoint!)

## Challenge Questions

1. What URL would you visit to see all domains?
2. What URL would you visit to see Motor Vehicle Act details?
3. What happens if you visit `/api/v1/domains/xyz`?
4. Can you add a third domain to the list?

---

## Concepts You Just Learned

1. **Path parameters**: `/{domain_name}` in the URL
2. **Router organization**: Separating endpoints into files
3. **API documentation**: FastAPI auto-generates docs
4. **JSON responses**: Returning dictionaries

**Ready to try this?** Create the file and test it, then tell me what happens!
