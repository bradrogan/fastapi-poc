import abc
from typing import Any
import httpx
from app.domains.recipe import RedditSort
from app.dto.recipe import RecipeSocialResponse, RecipesSocialResponse


class RedditRecipeClientInterface(abc.ABC):
    @staticmethod
    @abc.abstractmethod
    async def get_reddit(
        sub_reddit: str,
        sort: RedditSort,
        limit: int,
    ) -> RecipesSocialResponse:
        ...


class RedditRecipeClient(RedditRecipeClientInterface):
    @staticmethod
    async def get_reddit(
        sub_reddit: str = "recipes",
        sort: RedditSort | None = RedditSort.TOP,
        limit: int = 3,
    ) -> RecipesSocialResponse:
        async with httpx.AsyncClient() as client:
            response: httpx.Response = await client.get(
                f"https://www.reddit.com/r/{sub_reddit}/{sort}.json?sort={sort}&t=day&limit={limit}",
                headers={"User-agent": "harmless fun"},
            )
        json_posts = response.json()
        return_data: list[RecipeSocialResponse] = []

        # TODO: Access the response in a safe manner for missing keys
        for post in json_posts["data"]["children"]:
            if not RedditRecipeClient._reddit_is_pinned(post):
                recipe: RecipeSocialResponse = RecipeSocialResponse(
                    title=post["data"]["title"],
                    score=int(post["data"]["score"]),
                    url=post["data"]["url"],
                )
                if recipe:
                    return_data.append(recipe)

        return RecipesSocialResponse(results=return_data)

    @staticmethod
    def _reddit_is_pinned(post: Any) -> bool:
        if post["data"]["pinned"] or post["data"]["distinguished"]:
            return True
        return False
