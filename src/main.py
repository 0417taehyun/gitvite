import typer

from src.util import get_information, Worker

def app():
    """
    
    """
    typer.echo("깃헙 조직 초대를 시작합니다!")
    information = get_information()
    worker = Worker(information=information)
    
    if information.file_type == "csv":
        worker.write_csv()
    
    elif information.file_type == "excel":
        worker.write_csv()
    
    print()
    

if __name__ == "__main__":
    typer.run(app)
