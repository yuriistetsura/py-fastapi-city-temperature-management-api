from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from city import schemas, models
from city.models import City


async def create_city(
        db: AsyncSession,
        city: schemas.CityCreate
) -> models.City:
    city = models.City(
        name=city.name,
        additional_info=city.additional_info,
    )
    db.add(city)
    await db.commit()
    await db.refresh(city)

    return city


async def get_cities(db: AsyncSession) -> list[City]:
    result = await db.scalars(select(models.City))
    return list(result.all())


async def get_city_by_id(
    db: AsyncSession, city_id: int
) -> models.City:
    return await db.scalar(
        select(models.City).where(models.City.id == city_id)
    )


async def update_city(
    db: AsyncSession, city_id: int, city_data: schemas.CityCreate
) -> models.City | None:
    city = await db.scalar(
        select(models.City).where(models.City.id == city_id)
    )

    if not city:
        return None

    city.name = city_data.name
    city.additional_info = city_data.additional_info
    await db.commit()
    await db.refresh(city)
    return city


async def delete_city(db: AsyncSession, city_id: int) -> bool:
    city = await db.scalar(
        select(models.City).where(models.City.id == city_id)
    )

    if not city:
        return False

    await db.delete(city)
    await db.commit()
    return True
