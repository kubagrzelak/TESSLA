from logging import getLogger
from utils import setup_logging
import nnunet_file_management

setup_logging()
log = getLogger('main')

def main():
    nnunet_file_management.rename_input_task001_blood()

if __name__ == "__main__":
    main()