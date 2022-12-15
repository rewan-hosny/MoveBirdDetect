
from app.etl.DataSources.IDataSource import IDataSource
from app.etl.Move_Bird import bird

class Media(IDataSource):
    def __init__(self, type) -> None:
        super().__init__(type)

    def extract(self, file_path):
        data = bird.birds.count_birds(file_path)
        return data
    def load(self, file_path):
        print('not supported')
