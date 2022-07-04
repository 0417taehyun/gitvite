import re
import requests

from pydantic import HttpUrl, EmailStr


class GitHub:
    def __init__(self, access_token: str, organization_name: str) -> None:
        """
        
        """
        self.base_url: HttpUrl = f"https://api.github.com/orgs/{organization_name}"
        self.headers: dict[str, str] = {
            "Accept": "application/vnd.github.v3+json",
            "Authorization": f"token {access_token}"
        }
    
    def get_team_id_by_name(self, team_name: str) -> int | None:
        response = requests.get(
            url=self.base_url + f"/teams/{team_name}",
            headers=self.headers,
        )
        
        print(response.json())
        
        if response.status_code == 404:
            return None
        
        else:
            team_id: int = response.json()["id"]
            return team_id
    
    
    def create_team(self, team_name: str) -> int:
        data: dict[str, str] = { "name": team_name }
        response = requests.post(
            url=self.base_url + "/teams",
            headers=self.headers,
            data=data
        )
        
        print(response.json())
        
        if response.status_code == 201:
            team_id: int = response.json()["id"]
            return team_id
    
        elif response.status_code == 403:
            print("403 오류")
            raise 
    
        elif response.status_code == 422:
            print("422 오류")
            raise ValueError("")

        else:
            print("500 오류")
            raise Exception()
    
        
    def send_invitation(self, user_id: str | EmailStr, team_id: int):
        """
        
        """
        data: dict[str, str | EmailStr | int] = {
            "team_id": team_id,
        }        
        if re.match(
            pattern="^.+@[0-9a-zA-Z]([-_.]?[0-9a-zA-Z])+\.[a-z]{2,3}",
            string=user_id,
        ):
            data["email"] = user_id
            
        else:
            data["invitee_id"] = user_id
        
        response = requests.post(
            url=self.base_url + "/invitations",
            headers=self.headers,
            data=data,
        )
        
        print(response.json())
        
