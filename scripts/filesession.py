from datetime import date
import pathlib
import os


from projectnumber import Projectnumber


EXPORTFOLDER = "data/Szállítólevelek/"
EXPORTEXTENSION = "txt"
STOCKNAME = "Raktárkészlet"


class FileSession:
    """Class for handling file operations.
    This inventory uses file handling in one way as writing only.
    One can export the stock or its selected items, and a waybill will be
    exported whenever the stock is changed.
    The waybill exports come to project folder divided into years and months,
    like: 24_001 -> 2024 -> June.
    The waybill has a number which looks like 24_001_12, the latter being a
    serial number, which is always +1 of all waybills in the projectfolder."""
    def __init__(self,
                 projectnumber:Projectnumber=None,
                 exportfolder:str=EXPORTFOLDER,
                 extension:str=EXPORTEXTENSION,
                 stockname:str=STOCKNAME) -> None:
        self._projectnumber = projectnumber
        self._exportfolder = pathlib.Path(exportfolder)
        self._extension = extension
        self._stockname = stockname
        self._create_folders()

    def _create_folders(self) -> None:
        try:
            os.mkdir(self._exportfolder)
        except FileExistsError:
            pass
        if self._projectnumber:
            self._exportfolder = self._get_folder()

    def export(self, content:str) -> None:
        if self._projectnumber:
            waybill_number = "{}_{}".format(self._projectnumber,
                                            self._count_waybills() + 1,)
            filename = "{}.{}".format(waybill_number, self._extension)
        else:
            d = date.today()
            filename = "{}_{}.{}".format(self._stockname,
                                         d.strftime("%Y%m%d"),
                                         self._extension)
        with open(self._exportfolder / filename, "w") as f:
            if self._projectnumber:
                f.write("{:>79}".format("Szállítólevél száma: {}\n"\
                                        .format(waybill_number)))
            f.write(content)

    def _get_folder(self) -> pathlib.Path:
        """Identify an existing or create a new folder for this export."""
        d = date.today()
        year = d.strftime("%Y")
        month = d.strftime("%B").capitalize()
        self._projectfolder = self._exportfolder / str(self._projectnumber)
        path = self._projectfolder / year / month
        for folder in self._exportfolder.iterdir():  # check existing folder
            if folder.is_dir():
                foldernumber = Projectnumber(folder.name)
                if foldernumber == self._projectnumber:
                    path = folder / year / month
                    self._projectfolder = folder
                    break
        os.makedirs(path, exist_ok=True)
        return path

    def _count_waybills(self) -> int:
        return sum([len(files) for r, d, files in os.walk(self._projectfolder)])