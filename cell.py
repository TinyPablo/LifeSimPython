from typing import Optional
from entity import Entity


class Cell:
    def __init__(self) -> None:
        self.object: Optional[Entity] = None

    def set_object(self, object: Optional[Entity]) -> None:
        self.object = object

    def reset(self) -> None:
        self.object = None

    @property
    def is_free(self) -> bool:
        return self.object is None
    
    @property
    def is_occupied(self) -> bool:
        return not self.is_free
   
    @property
    def is_entity(self) -> bool:
        return type(self.object) == Entity
    
    def __str__(self) -> str:
        return f'C_{self.object.__str__()[0]}'
    
    def __repr__(self) -> str:
        return self.__str__()