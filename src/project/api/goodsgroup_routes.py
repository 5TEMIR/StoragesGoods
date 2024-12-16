from fastapi import APIRouter, HTTPException, status, Depends

from project.schemas.user import UserSchema

from project.api.depends import database, goodsgroup_repo, get_current_user, check_for_admin_access
from project.schemas.goodsgroup import *
from project.core.exceptions import *

goodsgroup_router = APIRouter()


@goodsgroup_router.get(
    "/all_goodsgroups",
    response_model=list[GoodsGroupSchema],
    status_code=status.HTTP_200_OK
)
async def get_all_goods_groups() -> list[GoodsGroupSchema]:
    async with database.session() as session:
        all_goodsgroups = await goodsgroup_repo.get_all_goods_groups(session=session)

    return all_goodsgroups


@goodsgroup_router.get(
    "/goodsgroup/{goods_group_id}",
    response_model=GoodsGroupSchema,
    status_code=status.HTTP_200_OK
)
async def get_goods_group_by_id(
        goods_group_id: int,
) -> GoodsGroupSchema:
    try:
        async with database.session() as session:
            goods_group = await goodsgroup_repo.get_goods_group_by_id(session=session, goods_group_id=goods_group_id)
    except GoodsGroupNotFound as error:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=error.message)
    return goods_group


@goodsgroup_router.post("/add_goodsgroup", response_model=GoodsGroupSchema, status_code=status.HTTP_201_CREATED)
async def add_goods_group(
        goods_group_dto: GoodsGroupCreateUpdateSchema,
        current_user: UserSchema = Depends(get_current_user),
) -> GoodsGroupSchema:
    check_for_admin_access(user=current_user)
    try:
        async with database.session() as session:
            new_goods_group = await goodsgroup_repo.create_goods_group(session=session, goods_group=goods_group_dto)
    except GoodsGroupAlreadyExists as error:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=error.message)
    return new_goods_group


@goodsgroup_router.put(
    "/update_goodsgroup/{goods_group_id}",
    response_model=GoodsGroupSchema,
    status_code=status.HTTP_200_OK,
)
async def update_goods_group(
        goods_group_id: int,
        goods_group_dto: GoodsGroupCreateUpdateSchema,
        current_user: UserSchema = Depends(get_current_user),
) -> GoodsGroupSchema:
    check_for_admin_access(user=current_user)
    try:
        async with database.session() as session:
            updated_goods_group = await goodsgroup_repo.update_goods_group(
                session=session,
                goods_group_id=goods_group_id,
                goods_group=goods_group_dto,
            )
    except GoodsGroupNotFound as error:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=error.message)
    return updated_goods_group


@goodsgroup_router.delete("/delete_goodsgroup/{goods_group_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_goods_group(
        goods_group_id: int,
        current_user: UserSchema = Depends(get_current_user),
) -> None:
    check_for_admin_access(user=current_user)
    try:
        async with database.session() as session:
            goodsgroup = await goodsgroup_repo.delete_goods_group(session=session, goods_group_id=goods_group_id)
    except GoodsGroupNotFound as error:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=error.message)
    return goodsgroup
