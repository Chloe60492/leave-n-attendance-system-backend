from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session
from ..crud import user as user_crud
from ..schemas.user import UserOut, TeamListResponse
from ..utils.dependencies import get_current_user
from ..models.user import User
from ..database import get_db
import logging
import json

# 取得模組的日誌記錄器
logger = logging.getLogger(__name__)

router = APIRouter(
    prefix="/api/users",
    tags=["users"]
)

@router.get("/me", response_model=UserOut)
def get_my_profile(request: Request, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    client_ip = request.client.host
    logger.info(f"User {current_user.email} (ID: {current_user.id}) requesting profile from {client_ip}")
    
    user_id = current_user.id
    department_id = current_user.department_id

    logger.debug(f"Getting manager for user {user_id}")
    manager_id = user_crud.get_manager_id(db, user_id)
    logger.debug(f"Manager ID for user {user_id}: {manager_id}")
    
    if manager_id is None:
        manager = None
    else:
        manager = user_crud.get_manager(db, manager_id)
        # 安全地記錄管理者信息
        if manager:
            manager_info = {
                "id": manager.id,
                "name": f"{manager.first_name} {manager.last_name}",
            }
            # 使用內建函數序列化
            logger.debug(f"Manager info: {safe_json(manager_info)}")

    department = user_crud.get_department(db, department_id)
    logger.debug(f"Department for user {user_id}: {department}")
    
    result = {
        "id": user_id,
        "employee_id": current_user.employee_id,
        "first_name": current_user.first_name,
        "last_name": current_user.last_name,
        "email": current_user.email,
        "department": department,
        "position": current_user.position,
        "manager": manager,
        "hire_date": str(current_user.hire_date),
        "is_manager": current_user.is_manager
    }
    
    # 使用安全的 JSON 序列化
    filtered_result = {k: v for k, v in result.items() if k not in ['manager']}
    logger.debug(f"User profile data prepared: {object_to_dict(filtered_result)}")
    logger.info(f"Successfully returned profile for user {current_user.email} (ID: {user_id})")
    return result 


@router.get("/team", response_model=TeamListResponse)
def get_my_team(request: Request, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    client_ip = request.client.host
    logger.info(f"User {current_user.email} (ID: {current_user.id}) requesting team list from {client_ip}")
    
    if not current_user.is_manager:
        logger.warning(f"Non-manager user {current_user.email} (ID: {current_user.id}) attempted to access team list")
        raise HTTPException(status_code=403, detail="Only managers can access this resource.")
    
    members = user_crud.get_team_members(db, current_user.id)
    
    # 記錄團隊成員信息，但避免記錄敏感信息
    member_count = len(members) if members else 0
    logger.debug(f"Found {member_count} team members for manager {current_user.id}")
    if members:
        member_ids = [str(m.id) for m in members]
        logger.debug(f"Team member IDs: {', '.join(member_ids)}")
    
    logger.info(f"Successfully returned team list with {member_count} members for manager {current_user.email}")
    return {"team_members": members}