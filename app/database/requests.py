from app.database.models import async_session, User, Category, Item
from sqlalchemy import select


async def set_user(tg_id):
    async with async_session() as session:
        user = await session.scalar(select(User).where(User.tg_id == tg_id))

        if not user:
            session.add(User(tg_id=tg_id))
            await session.commit()


async def get_categories():
    async with async_session() as session:
        return await session.scalars(select(Category))


async def get_items_by_category(category_id):
    async with async_session() as session:
        query = select(Item).where(Item.category == category_id)
        items = await session.scalars(query)
        items_list = items.all()
        return items_list


async def get_items(item_id):
    async with async_session() as session:
        item = await session.get(Item, item_id)
        return item
