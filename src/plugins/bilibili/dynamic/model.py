import json
import typing as T
from pathlib import Path

from pydantic import BaseModel, ValidationError, validator, validate_arguments

from .config import plugin_config

Path(plugin_config.data_path).mkdir(exist_ok=True)
SAVE_FILE = Path(plugin_config.data_path).joinpath('bili_dynamic.json')


class Target(BaseModel):
    uid: str
    name: str = None
    groups: T.Set[int] = set()
    users: T.Set[int] = set()

    @validator('name')
    def _(cls, v: T.Any, values: T.Dict[str, T.Any]) -> str:
        return v or values['uid']

    def update(self, other: "Target", remove: bool = False) -> bool:
        if self.uid == other.uid:
            old_groups = self.groups
            old_users = self.users
            if remove is False:
                self.groups |= other.groups
                self.users |= other.users
            else:
                self.groups -= other.groups
                self.users -= other.users
            return (old_groups != self.groups) or (old_users != self.users)
        else:
            raise ValueError("UID doesn't match.")

    class Config:
        extra = 'ignore'


class Database(BaseModel):
    __root__: T.List[Target] = []

    @classmethod
    def load(cls) -> "Database":
        try:
            db: Database = cls.parse_file(SAVE_FILE)
        except (FileNotFoundError, json.JSONDecodeError, ValidationError):
            db = cls()
        return db

    def save_to_file(self) -> None:
        with SAVE_FILE.open('w', encoding='utf8') as f:
            f.write(self.json(ensure_ascii=False, indent=2))

    @classmethod
    def update(cls, *data_array: Target, remove: bool = False) -> int:
        db: Database = cls.load()
        count = 0
        for data in data_array:
            for saved_target in db.__root__:
                if saved_target.uid == data.uid:
                    count += saved_target.update(data, remove=remove)
                    break
            else:
                db.__root__.append(data)
                count += 1
        db.save_to_file()
        return count

    @classmethod
    def add(cls, *data_array: Target) -> int:
        return cls.update(*data_array)

    @classmethod
    def remove(cls, *data_array: Target) -> int:
        return cls.update(*data_array, remove=True)

    @classmethod
    @validate_arguments
    def show(cls, groups: T.Set[int] = None, users: T.Set[int] = None) -> T.List[str]:
        db: Database = cls.load()
        ret = [saved_target.name for saved_target in db.__root__
               if groups & saved_target.groups or users & saved_target.users]
        return ret
