from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from ..database import get_db
from ..models import Asset as AssetModel, AssetType, AssetStatus
from ..schemas import Asset, AssetCreate, AssetUpdate, ResponseModel

router = APIRouter()

@router.get("/assets", response_model=List[Asset], summary="获取资产列表")
async def get_assets(
    asset_type: Optional[AssetType] = Query(None, description="按资产类型筛选"),
    status: Optional[AssetStatus] = Query(None, description="按状态筛选"),
    skip: int = Query(0, description="跳过的记录数"),
    limit: int = Query(100, description="返回的记录数"),
    db: Session = Depends(get_db)
):
    """获取资产列表，支持按类型和状态筛选"""
    query = db.query(AssetModel)
    
    if asset_type:
        query = query.filter(AssetModel.asset_type == asset_type)
    if status:
        query = query.filter(AssetModel.status == status)
    
    assets = query.offset(skip).limit(limit).all()
    return assets

@router.get("/assets/{asset_id}", response_model=Asset, summary="获取单个资产详情")
async def get_asset(asset_id: int, db: Session = Depends(get_db)):
    """获取指定ID的资产详情"""
    asset = db.query(AssetModel).filter(AssetModel.id == asset_id).first()
    if not asset:
        raise HTTPException(status_code=404, detail="资产不存在")
    return asset

@router.post("/assets", response_model=Asset, summary="添加新资产")
async def create_asset(asset: AssetCreate, db: Session = Depends(get_db)):
    """添加新资产"""
    # 检查IP地址是否已存在
    existing_asset = db.query(AssetModel).filter(AssetModel.ip_address == asset.ip_address).first()
    if existing_asset:
        raise HTTPException(status_code=400, detail="IP地址已存在")
    
    db_asset = AssetModel(**asset.dict())
    db.add(db_asset)
    db.commit()
    db.refresh(db_asset)
    return db_asset

@router.put("/assets/{asset_id}", response_model=Asset, summary="更新资产信息")
async def update_asset(asset_id: int, asset: AssetUpdate, db: Session = Depends(get_db)):
    """更新指定ID的资产信息"""
    db_asset = db.query(AssetModel).filter(AssetModel.id == asset_id).first()
    if not db_asset:
        raise HTTPException(status_code=404, detail="资产不存在")
    
    # 只更新提供的字段
    update_data = asset.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_asset, field, value)
    
    db.commit()
    db.refresh(db_asset)
    return db_asset

@router.delete("/assets/{asset_id}", response_model=ResponseModel, summary="删除资产")
async def delete_asset(asset_id: int, db: Session = Depends(get_db)):
    """删除指定ID的资产"""
    db_asset = db.query(AssetModel).filter(AssetModel.id == asset_id).first()
    if not db_asset:
        raise HTTPException(status_code=404, detail="资产不存在")
    
    db.delete(db_asset)
    db.commit()
    return ResponseModel(message=f"资产 {db_asset.name} 删除成功") 