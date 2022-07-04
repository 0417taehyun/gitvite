import pandas as pd

from src.schema import Information
from src.util.github import GitHub


class Worker(GitHub):
    def __init__(self, information: Information) -> None:
        """
        
        """
        self.information = information
        super().__init__(
            access_token=information.github_access_token,
            organization_name=information.github_organization_name,
        )


    def write_excel(self):
        """
        
        """
        df_excel = pd.read_excel(
            filepath=self.information.file_path,
            sheet_name=self.information.sheet_name,
            engine="python",
            encoding="utf-8",
        )
        if not (team_id := self.get_team_id_by_name(
            team_name=self.information.github_organization_team_name,
        )):
            team_id = self.create_team(
                team_name=self.information.github_organization_team_name,
            )
        
        print(df_excel.columns)
        print("----")
        print(df_excel.shape)
        
        # result: bool = self.send_invitation(
            
        #     team_id=team_id
        # )
        
        # if result:
        #     pass
        # else:
        
    
    def write_csv(self):
        """
        To-do
        """
        df_csv = pd.read_csv(self.information.file_path)
        
        