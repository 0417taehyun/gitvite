import typer

from src.schema import FileType
from src.util import Worker, get_information


def app() -> None:
    """ """
    typer.echo("깃헙 조직 초대를 시작합니다!")
    information = get_information()
    worker = Worker(information=information)

    if information.file_type == str(FileType.CSV.value):
        worker.write_csv()

    elif information.file_type == str(FileType.EXCEL.value):
        worker.write_excel()

    typer.echo("깃헙 조직 초대가 끝났습니다!")


if __name__ == "__main__":
    typer.run(app)
