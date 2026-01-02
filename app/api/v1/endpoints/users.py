from typing import Any, List, Optional
from fastapi import APIRouter, Body, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from sqlalchemy import or_, asc, desc

from app import crud, models, schemas
from app.api import deps

router = APIRouter()

@router.get("/", response_model=schemas.UserPaginatedResponse)
def read_users(
    db: Session = Depends(deps.get_db),
    page: int = 1,
    limit: int = 100,
    search: str | None = None,
    scope: str = "all",
    role: str | None = None,
    sortBy: str | None = "id:asc",
    current_user: models.User = Depends(deps.get_current_active_admin),
) -> Any:
    """
    Retrieve users with advanced filtering, sorting, and pagination.
    Only Admins can list all users.
    """
    query = db.query(models.User)

    # 1. Filter by Role
    if role:
        query = query.filter(models.User.role == role)

    # 2. Search Logic
    if search:
        search_int = int(search) if search.isdigit() else None
        
        if scope == "id":
            if search_int is not None:
                query = query.filter(models.User.id == search_int)
            else:
                query = query.filter(models.User.id == -1) 
        
        elif scope == "name":
            query = query.filter(models.User.name.ilike(f"%{search}%"))
            
        elif scope == "email":
            query = query.filter(models.User.email.ilike(f"%{search}%"))
            
        elif scope == "all":
            conditions = [
                models.User.name.ilike(f"%{search}%"),
                models.User.email.ilike(f"%{search}%"),
            ]
            if search_int is not None:
                conditions.append(models.User.id == search_int)
            
            query = query.filter(or_(*conditions))

    # 3. Sorting Logic
    if sortBy:
        try:
            if ":" in sortBy:
                field_name, direction = sortBy.split(":")
            else:
                field_name, direction = sortBy, "asc"

            if hasattr(models.User, field_name):
                column = getattr(models.User, field_name)
                if direction.lower() == "desc":
                    query = query.order_by(desc(column))
                else:
                    query = query.order_by(asc(column))
            else:
                 query = query.order_by(models.User.id.asc())
        except Exception:
            query = query.order_by(models.User.id.asc())
    else:
        query = query.order_by(models.User.id.asc())

    # 4. Pagination Logic
    total_count = query.count()
    skip = (page - 1) * limit
    users = query.offset(skip).limit(limit).all()

    return {
        "results": users,
        "count": total_count,
        "page": page,
        "limit": limit,
        "total_pages": (total_count + limit - 1) // limit if limit > 0 else 1
    }

@router.post("/", response_model=schemas.UserResponse, status_code=201)
def create_user(
    *,
    db: Session = Depends(deps.get_db),
    user_in: schemas.UserCreate,
    current_user: models.User = Depends(deps.get_current_active_admin),
) -> Any:
    """
    Create new user. Only Admins can create users directly via this endpoint.
    """
    user = crud.user.get_by_email(db, email=user_in.email)
    if user:
        raise HTTPException(
            status_code=400,
            detail="The user with this email already exists in the system",
        )
    user = crud.user.create(db, obj_in=user_in)
    return user

@router.get("/{user_id}", response_model=schemas.UserResponse)
def read_user_by_id(
    user_id: int,
    current_user: models.User = Depends(deps.get_current_active_user),
    db: Session = Depends(deps.get_db),
) -> Any:
    """
    Get a specific user by id.
    """
    user = crud.user.get(db, id=user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    if user.id != current_user.id and current_user.role != "admin":
        raise HTTPException(
            status_code=403, detail="Not enough permissions"
        )
    return user

@router.patch("/{user_id}", response_model=schemas.UserResponse)
def update_user(
    *,
    db: Session = Depends(deps.get_db),
    user_id: int,
    user_in: schemas.UserUpdate,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Update a user.
    """
    user = crud.user.get(db, id=user_id)
    if not user:
        raise HTTPException(
            status_code=404,
            detail="User not found",
        )
    if user.id != current_user.id and current_user.role != "admin":
        raise HTTPException(
            status_code=403, detail="Not enough permissions"
        )
        
    user = crud.user.update(db, db_obj=user, obj_in=user_in)
    return user

@router.delete("/{user_id}", status_code=204)
def delete_user(
    *,
    db: Session = Depends(deps.get_db),
    user_id: int,
    current_user: models.User = Depends(deps.get_current_active_admin),
) -> None:
    """
    Delete a user. Only Admins can delete users.
    """
    user = crud.user.get(db, id=user_id)
    if not user:
        raise HTTPException(
            status_code=404,
            detail="User not found",
        )
    if user.id == current_user.id:
        raise HTTPException(
            status_code=400, detail="Users cannot delete themselves"
        )
    crud.user.remove(db, id=user_id)
    return None