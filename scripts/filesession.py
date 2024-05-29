import pathlib
import os


EXPORTFOLDER = "data/szallitolevelek/"
EXPORTEXTENSION = "txt"


class FileSession:
    """Class to handle file operations."""
    def __init__(self,
                 stockfolder:str=EXPORTFOLDER,
                 waybillfolder:str=EXPORTFOLDER,
                 extension:str=EXPORTEXTENSION) -> None:
        self._stockfolder = pathlib.Path(stockfolder)
        self._waybillfolder = pathlib.Path(waybillfolder)
        self._extension = "." + extension
        self._create_folders()

    def _create_folders(self) -> None:
        try:
            os.mkdir(self._stockfolder)
        except FileExistsError:
            pass
        try:
            os.mkdir(self._waybillfolder)
        except FileExistsError:
            pass

    def export(self, filename:str, content:str, waybill=True) -> None:
        destination = self._waybillfolder if waybill else self._stockfolder
        filename = filename + self._extension
        with open(destination / filename, "w") as f:
            f.write(content)