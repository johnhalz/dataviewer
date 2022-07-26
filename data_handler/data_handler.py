import h5py


class DataHandler:
    def __init__(self, file_list: list = None) -> None:

        if file_list is None:
            self.files = dict()


    def add_files(self, files):

        self.newly_added_files = dict()

        # If only one file is opened
        if isinstance(files, str):
            if files not in self.files.keys() and files[-3:] == '.h5':
                self.newly_added_files[files] = h5py.File(files, 'r')
            
        # If multiple files are opened
        elif isinstance(files, list):
            for file in files:
                if file in self.files.keys() or file[-3:] != '.h5':
                    continue
                else:
                    self.newly_added_files[file] = h5py.File(file, 'r')

        self.files.update(self.newly_added_files)
