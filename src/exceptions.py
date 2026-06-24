from uuid import UUID


class ItemNotFoundException(Exception):
    def __init__(self, item_id: UUID):
        super().__init__(f"Item with id {item_id} not found")
