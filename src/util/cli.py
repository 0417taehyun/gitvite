import os
import time

import typer
from pydantic import FilePath, HttpUrl, ValidationError

from src.schema import (
    BaseInformation,
    Information,
    InvalidPermissionException,
    NotFoundException,
)

app = typer.Typer()


@app.command()
def get_information() -> Information:
    """
    1. file_type
    2. file_path
    3. github_access_token
    4. github_organization_name
    """
    try:
        time.sleep(1)

        env_file_contents: str = ""
        information: dict[str, str | FilePath | HttpUrl] = dict(
            BaseInformation()
        )
        for key, value in information.items():
            field: str = key.upper()
            if key == "file_type" and not value:
                information[key] = (
                    file_type := typer.prompt(
                        "파일의 종류의 번호를 입력해주세요 [1: CSV, 2: EXCEL]"
                    )
                )
                env_file_contents += f"{field}={file_type}\n"

            elif key == "file_path" and not value:
                information[key] = (
                    file_path := typer.prompt("파일의 경로를 입력해주세요")
                )
                env_file_contents += f"{field}={file_path}\n"

            elif key == "github_account_column_name" and not value:
                information[key] = (
                    github_account_column_name := typer.prompt(
                        "멤버들의 깃헙 계정이 입력된 컬럼명을 입력해주세요"
                    )
                )
                env_file_contents += f"{field}={github_account_column_name}\n"

            elif key == "github_organization_teams_column_name" and not value:
                information[key] = (
                    github_organization_teams_column_name := typer.prompt(
                        "멤버들을 초대하려는 팀이 입력된 컬럼명을 입력해주세요"
                    )
                )
                env_file_contents += (
                    f"{field}={github_organization_teams_column_name}\n"
                )

            elif key == "github_access_token" and not value:
                information[key] = (
                    github_access_token := typer.prompt(
                        "조직 권한이 부여된 본인의 깃헙 액세스 토큰을 입력해주세요"
                    )
                )
                env_file_contents += f"{field}={github_access_token}\n"

            elif key == "github_organization_name" and not value:
                information[key] = (
                    github_organization_name := typer.prompt(
                        "초대하려는 깃헙 조직의 이름을 입력해주세요 ex.geultto"
                    )
                )
                env_file_contents += f"{field}={github_organization_name}\n"

            elif key == "github_organization_team_name" and not value:
                information[key] = (
                    github_organization_team_name := typer.prompt(
                        "사용자들을 초대하려는 팀 이름을 입력해주세요 ex.7기"
                    )
                )
                env_file_contents += (
                    f"{field}={github_organization_team_name}\n"
                )

        if env_file_contents:
            with open(".env", "a") as env_file:
                if os.stat(".env").st_size:
                    env_file_contents = "\n" + env_file_contents

                env_file.write(env_file_contents)

        information = Information(**information)
        return information

    except ValidationError as validation_error:
        print(str(validation_error))

    except InvalidPermissionException as invalid_permission_error:
        print(str(invalid_permission_error))

    except NotFoundException as not_found_error:
        print(str(not_found_error))

        error_type: str = not_found_error.get_error_type()
        if error_type == "file_path":
            information["file_path"] = typer.prompt("파일의 경로를 다시 입력해주세요")
