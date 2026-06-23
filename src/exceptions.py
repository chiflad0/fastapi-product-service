from uuid import UUID


class ItemNotFoundException(Exception):
    def __init__(self, item_id: UUID):
        # self.item_id = item_id
        super().__init__(f"Item with id {item_id} not found")
