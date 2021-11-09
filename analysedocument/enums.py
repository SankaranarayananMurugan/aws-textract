from enum import Enum

class BlockType(Enum):
    PAGE = 'PAGE'
    LINE = 'LINE'
    KEY_VALUE_SET = 'KEY_VALUE_SET'
    WORD = 'WORD'

    @classmethod
    def _missing_(cls, value):
        return None

    def __str__(self):
        return self.value

class EntityType(Enum):
    KEY = 'KEY'
    VALUE = 'VALUE'

    @classmethod
    def _missing_(cls, value):
        return None

    def __str__(self):
        return self.value

class RelationshipType(Enum):
    CHILD = 'CHILD'
    VALUE = 'VALUE'

    @classmethod
    def _missing_(cls, value):
        return None

    def __str__(self):
        return self.value
