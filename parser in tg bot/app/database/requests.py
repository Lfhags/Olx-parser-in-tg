from sqlalchemy import select
from .models import User, Link, async_session

async def set_user(tg_id: int):
    async with async_session() as session:
        query = select(User).where(User.tg_id == tg_id)
        result = await session.execute(query)
        user = result.scalar_one_or_none()
        
        if not user:
            user = User(tg_id=tg_id)
            session.add(user)
            await session.commit()


async def set_link(text):
    async with async_session() as session:
        # Перевіряємо чи посилання вже існує
        query = select(Link).where(Link.link == text)
        result = await session.execute(query)
        link = result.scalar_one_or_none()
        
        if not link:
            # Створюємо новий запис посилання
            new_link = Link(link=text)
            session.add(new_link)
            await session.commit()
            return new_link.id
        return link.id


async def get_links():
    async with async_session() as session:
        query = select(Link).order_by(Link.id.desc())
        result = await session.execute(query)
        links = result.scalars().all()
        return links

            
