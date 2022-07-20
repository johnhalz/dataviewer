from gui.main_view import MainView

from data_handler.data_handler import DataHandler

def main():
    # Start handling classes
    data_handler = DataHandler()

    # Start GUI
    MainView(data_handler)

if __name__ == "__main__":
    main()