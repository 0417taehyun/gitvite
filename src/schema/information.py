from enum import Enum
from os.path import exists

import requests  # type: ignore
from pydantic import (
    BaseModel,
    BaseSettings,
    Field,
    FilePath,
    HttpUrl,
    validator,
)

from src.schema.response import InvalidPermissionException, NotFoundException


class FileType(Enum):
    """ """

    CSV = 1
    EXCEL = 2


class BaseInformation(BaseSettings):
    """ """

    file_type: str | None = Field(env="FILE_TYPE")
    file_path: FilePath | None = Field(env="FILE_PATH")

    github_account_column_name: str | None = Field(
        env="GITHUB_ACCOUNT_COLUMN_NAME"
    )
    github_organization_teams_column_name: str | None = Field(
        env="GITHUB_ORGANIZATION_TEAMS_COLUMN_NAME"
    )

    github_access_token: str | None = Field(env="GITHUB_ACCESS_TOKEN")
    github_organization_name: str | None = Field(
        env="GITHUB_ORGANIZATION_NAME"
    )
    github_organization_team_name: str | None = Field(
        env="GITHUB_ORGANIZATION_TEAM_NAME"
    )
    github_base_url: HttpUrl = "https://api.github.com/orgs"

    class Config:
        env_file = ".env"


class Information(BaseModel):
    """ """

    file_type: str
    file_path: FilePath

    github_account_column_name: str
    github_organization_teams_column_name: str

    github_access_token: str
    github_organization_name: str
    github_organization_team_name: str
    github_base_url: HttpUrl = "https://api.github.com/orgs"

    @validator("file_path")
    def validate_file(cls, value: FilePath) -> FilePath:
        """ """
        if not exists(value):
            raise NotFoundException("입력하신 파일이 존재하지 않습니다.", type="file_path")

        else:
            return value

    @validator("github_organization_name")
    def validate_github(
        cls,
        value: str,
        values: dict,
    ) -> str:
        """ """
        github_access_token: str = values["github_access_token"]
        response = requests.get(
            url=f"https://api.github.com/orgs/{value}",
            headers={
                "Accept": "aaplication/vnd.github.v3+json",
                "Authorization": f"token {github_access_token}",
            },
        )

        if response == 401:
            raise InvalidPermissionException("유효한 액세스 토큰이 아닙니다.")

        elif response == 404:
            raise NotFoundException("해당 조직을 찾을 수 없습니다.", type=value)

        else:
            return value
