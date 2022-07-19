import pandas
import h5py

class DataHandler:
    def __init__(self, file_list: list = []) -> None:
        self.file_list: list = file_list

    def add_files(self, files: list):
        self.file_list.append(files)
        print(self.file_list)