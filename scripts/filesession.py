import pathlib
import os


from misc import valid_projectnr, fmt_projectnr


EXPORTFOLDER = "data/Szállítólevelek/"
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
    
    def lookup_projectfolder(self, projectnumber:str) -> pathlib.Path:
        """Identify an existing or create a new folder for this project number.
        projectnumber: expected in yy_sss format"""
        for folder in self._waybillfolder.iterdir():
            if folder.is_dir():
                extract = valid_projectnr(str(folder))
                if extract and (fmt_projectnr(extract) == projectnumber):
                    return folder
        folder = self._waybillfolder / projectnumber
        os.mkdir(folder)
        return folder