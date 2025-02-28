from dataclasses import dataclass
from app.persistance.model import Season, WishItem
from app.persistance.configuration import SeasonRepository, WishItemsRepository
from app.service.dto import CreatFinalWishItemDto


@dataclass
class FinalWishItemService:
    season_repository: SeasonRepository
    wishlist_repository: WishItemsRepository

    def add_wishlist_item(self, item: CreatFinalWishItemDto) -> int:
        season_id = self.season_repository.insert(item=Season(name=item.season_name))

        return self.wishlist_repository.insert(
            item=WishItem(
                name=item.name, image_data=item.image_data, season_id=season_id
            )
        )

