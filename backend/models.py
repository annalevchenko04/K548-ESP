from sqlalchemy import Column, Integer, String, CheckConstraint, ForeignKey, Float, func, DateTime
from sqlalchemy.orm import validates
from database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, index=True, nullable=False)
    name = Column(String(50), nullable=False)
    surname = Column(String(50), nullable=False)
    age = Column(Integer, nullable=False)
    gender = Column(String(10), nullable=False)
    email = Column(String(100), unique=True, index=True, nullable=False)
    phone = Column(String(100), unique=True, index=True, nullable=True)

    hashed_password = Column(String(255), nullable=False)
    role = Column(String(10), nullable=False)


    __table_args__ = (
        CheckConstraint(
            "role IN ('admin', 'member')", name="check_valid_roles"
        ),
        CheckConstraint(
            "gender IN ('male', 'female')", name="check_valid_genders"
        ),
    )

    @validates('age')
    def validate_age(self, key, value):
        """
        Validates that the age is between 0 and 120.
        """
        if not (0 <= value <= 120):
            raise ValueError("Age must be a positive integer between 0 and 120.")
        return value

    __mapper_args__ = {
        'polymorphic_identity': 'user',
        'polymorphic_on': role
    }


class Member(User):
    __tablename__ = "members"
    id = Column(Integer, ForeignKey("users.id"), primary_key=True)
    membership_status = Column(String(50), nullable=True)

    __mapper_args__ = {
        'polymorphic_identity': 'member',
    }


class Admin(User):
    __tablename__ = "admins"
    id = Column(Integer, ForeignKey("users.id"), primary_key=True)

    __mapper_args__ = {
        'polymorphic_identity': 'admin',
    }

class CarbonFootprint(Base):
    __tablename__ = "carbon_footprint"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    total_footprint = Column(Float, nullable=False)
    created_at = Column(DateTime, server_default=func.now())

class CarbonFootprintDetails(Base):
    __tablename__ = "carbon_footprint_details"

    id = Column(Integer, primary_key=True, index=True)
    footprint_id = Column(Integer, ForeignKey("carbon_footprint.id"))
    category = Column(String, nullable=False)
    value = Column(Float, nullable=False)

