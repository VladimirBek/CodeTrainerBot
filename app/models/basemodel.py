from sqlalchemy.orm import declared_attr
import re


class ModelBase:
    __name__: str

    # Generate __tablename__ automatically
    @declared_attr
    def __tablename__(cls) -> str:
        new_name_lst = re.sub(r"([A-Z])", r" \1", cls.__name__).split()
        new_name = '_'.join(new_name_lst)
        return new_name.lower()
