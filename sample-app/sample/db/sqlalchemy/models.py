from sqlalchemy import Column, Index, schema
from sqlalchemy.types import TEXT
from sqlalchemy.ext.declarative import declared_attr, declarative_base


def passby(value):
    return value


class BaseModel(object):
    @declared_attr
    def __tablename__(self):
        return self.__name__.lower()

    @classmethod
    def get_id(cls):
        pass

    def to_dict(self):
        intersection = set(self.__table__.columns.keys()) & set(self.FIELDS)
        return dict(
            [
                (
                    key,
                    (
                        lambda value: self.FIELDS[key](value)
                        if value is not None
                        else None
                    )(getattr(self, key)),
                )
                for key in intersection
            ]
        )

    FIELDS = {}


Base = declarative_base(cls=BaseModel)

class User(Base):
    __tablename__ = "user"
    __table_args__ = (
        Index("phone_idx", "phone"),
        Index("email_idx", "email"),
        schema.UniqueConstraint(
            "phone",
            "email",
            name="uniq_user_phone_email",
        ),
        schema.PrimaryKeyConstraint("phone", "email", name="user_pk"),
    )

    name = Column(TEXT)
    phone = Column(TEXT)
    email = Column(TEXT)

    FIELDS = {
        "name": str,
        "phone": str,
        "email": str
    }