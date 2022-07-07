from datetime import datetime, timedelta, timezone

import pandas as pd
import typer
from pydantic import FilePath

from src.schema import Information
from src.util.github import GitHub


class Worker(GitHub):
    def __init__(self, information: Information) -> None:
        """ """
        self.information = information
        super().__init__(
            access_token=information.github_access_token,
            organization_name=information.github_organization_name,
        )

    def write_excel(self):
        """ """
        file_path: FilePath = self.information.file_path
        team_name: str = self.information.github_organization_team_name

        df_excel: pd.DataFrame = pd.read_excel(
            io=file_path,
            na_filter=False,
        )

        columns: list[str] = df_excel.columns
        if "초대여부" not in columns:
            df_excel["초대여부"] = ""

        if "실패원인" not in columns:
            df_excel["실패원인"] = ""

        if "마지막 초대일자" not in columns:
            df_excel["마지막 초대일자"] = ""

        if not (team_id := self.get_team_id_by_name(team_name=team_name)):
            team_id = self.create_team(team_name=team_name)

        with typer.progressbar(
            df_excel.iterrows(),
            length=df_excel.shape[0],
            label="진행 현황",
        ) as progress:
            for index, row in progress:
                data: dict = row.to_dict()

                if team_name in [
                    team.strip() for team in data["기수"].split(",")
                ]:
                    result: dict[str, str | int] = self.send_invitation(
                        user_id=data["깃헙계정"], team_id=team_id
                    )

                    if result["status_code"] == 201:
                        data["초대여부"] = "성공"
                        data["실패원인"] = ""

                    else:
                        data["초대여부"] = "실패"
                        data["실패원인"] = result["content"]

                    data["마지막 초대일자"] = datetime.strftime(
                        datetime.now(tz=timezone(timedelta(hours=9))),
                        "%Y년 %m월 %d일 %H시 %M분 %S초",
                    )

                new_df: pd.DataFrame = pd.DataFrame(data=data, index=[index])
                df_excel.update(new_df)

        df_excel = df_excel.loc[:, ~new_df.columns.str.contains("^Unnamed")]
        df_excel.to_excel(excel_writer=file_path)

    def write_csv(self):
        """
        To-do
        """
        pass
