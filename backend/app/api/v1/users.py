from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import Any, List, Optional
from pydantic import BaseModel, EmailStr

from ...models.user import User, UserRole
from ...config.database import get_db
from ...utils.auth import get_password_hash
from .auth import get_current_active_user, UserResponse

# Create router
router = APIRouter(prefix="/users", tags=["Users"])

# User update model
class UserUpdate(BaseModel):
    full_name: Optional[str] = None
    email: Optional[EmailStr] = None
    password: Optional[str] = None
    role: Optional[str] = None
    department: Optional[str] = None
    position: Optional[str] = None
    is_active: Optional[bool] = None

# Get all users endpoint
@router.get("/", response_model=List[UserResponse])
async def get_users(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
) -> Any:
    """
    Get all users.
    """
    # Only admin and managers can access all users
    if current_user.role not in [UserRole.ADMIN, UserRole.MANAGER, UserRole.HR]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions",
        )
    
    users = db.query(User).offset(skip).limit(limit).all()
    return users

# Get user by ID endpoint
@router.get("/{user_id}", response_model=UserResponse)
async def get_user(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
) -> Any:
    """
    Get user by ID.
    """
    # Check if user has permissions to access this user
    if current_user.id != user_id and current_user.role not in [UserRole.ADMIN, UserRole.MANAGER, UserRole.HR]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions",
        )
    
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )
    
    return user

# Update user endpoint
@router.put("/{user_id}", response_model=UserResponse)
async def update_user(
    user_id: int,
    user_data: UserUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
) -> Any:
    """
    Update user by ID.
    """
    # Check if user has permissions to update this user
    if current_user.id != user_id and current_user.role != UserRole.ADMIN:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions",
        )
    
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )
    
    # Update user fields
    if user_data.full_name:
        user.full_name = user_data.full_name
    if user_data.email:
        # Check if email already exists
        if db.query(User).filter(User.email == user_data.email, User.id != user_id).first():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered",
            )
        user.email = user_data.email
    if user_data.password:
        user.hashed_password = get_password_hash(user_data.password)
    
    # Only admin can update role and active status
    if current_user.role == UserRole.ADMIN:
        if user_data.role:
            user.role = user_data.role
        if user_data.is_active is not None:
            user.is_active = user_data.is_active
        if user_data.department:
            user.department = user_data.department
        if user_data.position:
            user.position = user_data.position
    
    db.commit()
    db.refresh(user)
    
    return user

# Delete user endpoint
@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
) -> Any:
    """
    Delete user by ID.
    """
    # Only admin can delete users
    if current_user.role != UserRole.ADMIN:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions",
        )
    
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )
    
    # Prevent deleting self
    if user.id == current_user.id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Cannot delete own user",
        )
    
    db.delete(user)
    db.commit()
    
    return None 