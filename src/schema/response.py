class InvalidPermissionException(Exception):
    def __init__(self, github_access_token: str, *args: object) -> None:
        self.github_access_token = github_access_token
        super().__init__(*args)


    def __str__(self) -> str:
        return f"입력하신 깃헙 액세스 토큰 {self.github_access_token} 이 권한이 없습니다."


class NotFoundException(Exception):
    def __init__(self, name: str, type: str, *args: object) -> None:
        self.name = name
        self.type = type
        super().__init__(*args)
    
    def __str__(self) -> str:
        return super().__str__()

    def get_error_type(self) -> str:
        return self.type
    