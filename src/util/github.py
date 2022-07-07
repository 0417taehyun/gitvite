import json
import re

import requests  # type: ignore
from pydantic import EmailStr, HttpUrl


class GitHub:
    def __init__(self, access_token: str, organization_name: str) -> None:
        """ """
        self.base_url: HttpUrl = (
            f"https://api.github.com/orgs/{organization_name}"
        )
        self.headers: dict[str, str] = {
            "Accept": "application/vnd.github.v3+json",
            "Authorization": f"token {access_token}",
        }

    def get_team_id_by_name(self, team_name: str) -> int | None:
        """ """
        response = requests.get(
            url=self.base_url + "/teams",
            headers=self.headers,
        )

        if response.status_code == 404:
            return None

        else:
            for team in response.json():
                if team["name"] == team_name:
                    team_id: int = team["id"]

            return team_id

    def create_team(self, team_name: str) -> int:
        """ """
        data: dict[str, str] = {"name": team_name}
        response = requests.post(
            url=self.base_url + "/teams",
            headers=self.headers,
            data=json.dumps(data),
        )

        if response.status_code == 201:
            team_id: int = response.json()["id"]
            return team_id

        elif response.status_code == 403:
            raise

        elif response.status_code == 422:
            raise ValueError("")

        else:
            raise Exception()

    def send_invitation(
        self, user_id: str | EmailStr, team_id: int
    ) -> dict[str, str | int]:
        """ """
        result: dict[str, str | int] = {
            "status_code": 0,
            "content": "",
        }
        data: dict[str, str | EmailStr | int] = {
            "team_id": team_id,
        }
        if re.match(
            pattern=r"^.+@[0-9a-zA-Z]([-_.]?[0-9a-zA-Z])+\.[a-z]{2,3}",
            string=user_id,
        ):
            data["email"] = user_id

        else:
            response = requests.get(
                url=f"https://api.github.com/users/{user_id}",
                headers=self.headers,
            )

            if (status_code := response.status_code) == 200:
                data["invitee_id"] = response.json()["id"]

            else:
                result["status_code"] = status_code
                if status_code == 403:
                    result["content"] = "API 호출 횟수 제한"

                else:
                    result["content"] = "존재하지 않는 깃헙 계정"

                return result

        response = requests.post(
            url=self.base_url + "/invitations",
            headers=self.headers,
            data=json.dumps(data),
        )
        result["status_code"] = response.status_code

        return result
