from extensions import db
from flask_login import UserMixin
from sqlalchemy import Integer, String, Boolean
from sqlalchemy.orm import Mapped, mapped_column

class Entry(db.Model):
    id: Mapped[int] = mapped_column(Integer, primary_key=True, nullable=False)
    age: Mapped[int] = mapped_column(Integer, nullable=False)
    city_of_residence: Mapped[str] = mapped_column(String, nullable=False)
    zipcode: Mapped[int] = mapped_column(Integer, nullable=False)
    referred_by: Mapped[str] = mapped_column(String, nullable=False)
    education: Mapped[str] = mapped_column(String, nullable=False)
    gender: Mapped[str] = mapped_column(String, nullable=False)
    ethnicity: Mapped[str] = mapped_column(String, nullable=False)
    race: Mapped[str] = mapped_column(String, nullable=False)
    housing: Mapped[str] = mapped_column(String, nullable=False)
    household_income: Mapped[int] = mapped_column(Integer, nullable=False)
    number_of_dependants: Mapped[int] = mapped_column(Integer, nullable=False)
    language: Mapped[str] = mapped_column(String, nullable=False)
    employment: Mapped[str] = mapped_column(String, nullable=False)
    health_coverage: Mapped[str] = mapped_column(String, nullable=False)
    hiv_status: Mapped[str] = mapped_column(String, nullable=False)
    lgbtq_status: Mapped[str] = mapped_column(String, nullable=False)
    veteran: Mapped[bool] = mapped_column(Boolean, nullable=False)

class User(UserMixin, db.Model):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    password: Mapped[str] = mapped_column(String(100))
    name: Mapped[str] = mapped_column(String(1000))
    is_admin: Mapped[bool] = mapped_column(Boolean, nullable=False)