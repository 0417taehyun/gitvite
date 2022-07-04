import requests

import pandas as pd

from enum import Enum
from os.path import exists

from pydantic import BaseModel, validator, HttpUrl, FilePath

from src.schema.response import NotFoundException, InvalidPermissionException


class FileType(str, Enum):
    """
    
    """
    CSV = "csv"
    EXCEL = "excel"


class Information(BaseModel):
    """
    
    """    
    file_type: FileType
    file_path: FilePath
    sheet_name: str | None
    github_access_token: str
    github_organization_name: str = "geultto"
    github_organization_team_name: str
    github_base_url: HttpUrl = "https://api.github.com/orgs"
    
    
    @validator("file_path")
    def validate_file(cls, value: FilePath) -> FilePath:
        """
        
        """
        if not exists(value):
            raise NotFoundException("입력하신 파일이 존재하지 않습니다.", type="file_path")
        
        else:
            return value
    
    
    @validator("sheet_name")
    def validate_sheet_name(cls, value: str, **kwargs) -> str:
        """
        """
        if not pd.read_excel(filepath=kwargs["file_path"], sheet_name=value):
            raise ValueError("입력하신 시트가 존재하지 않습니다.", type="sheet_name")
        
    

    @validator("github_organization_name")
    def validate_github(cls, value: str, values: dict,) -> str:
        """
        
        """
        github_access_token: str = values["github_access_token"]
        response = requests.get(
            url=f"https://api.github.com/orgs/{value}",
            headers={
                "Accept": "aaplication/vnd.github.v3+json",
                "Authorization": f"token {github_access_token}",
            }
        )
        
        print(response)
        print(response.json())
        
        if response == 401:
            raise InvalidPermissionException("유효한 액세스 토큰이 아닙니다.")
        
        elif response == 404:
            raise NotFoundException("해당 조직을 찾을 수 없습니다.", type=value)
        
        else:
            return value
        