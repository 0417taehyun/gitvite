import typer

from pydantic import FilePath

from src.schema import FileType, Information, NotFoundException


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
        file_type: FileType = typer.prompt("파일의 종류를 입력해주세요 ex.excel, csv")
        file_path: FilePath = typer.prompt("파일의 경로를 입력해주세요")
        github_access_token: str = typer.prompt("본인의 깃헙 액세스 토큰을 입력해주세요")
        github_organization_name: str = typer.prompt("초대하려는 깃헙 조직의 이름을 입력해주세요 ex.geultto")
        github_organization_team_name: str = typer.prompt("사용자들을 초대하려는 팀 이름을 입력해주세요 ex.7기")
        
        information: Information = Information(
            file_type=file_type,
            file_path=file_path,
            github_access_token=github_access_token,
            github_organization_name=github_organization_name,
            github_organization_team_name=github_organization_team_name,
        )
        
        if file_type == FileType.EXCEL:
            sheet_name: str = typer.prompt("데이터가 저장된 시트의 이름을 입력해주세요 ex.sheet1")        
            information.sheet_name = sheet_name
        
        return information

    except NotFoundException as not_found_error:
        print(str(not_found_error))
        
        error_type: str = not_found_error.get_error_type()
        if error_type == "file_path":
            information.file_path: FilePath = typer.prompt(
                "파일의 경로를 다시 입력해주세요"
            )
        elif error_type == "sheet_name":
            information.sheet_name: str = typer.prompt(
                "엑셀 시트의 이름을 다시 입력해주세요"
            )
        