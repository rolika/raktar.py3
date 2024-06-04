import databasesession as dbs, logbook as lb, climenu as clm


class App():
    def __init__(self, db="data/adatok.db") -> None:
        self._dbs = dbs.DatabaseSession(db)

    def run(self) -> None:
        print(clm.headline("utókalkulátor"))
        while True:
            month = self._choose_month()
            logbook = self._choose_project(month)
            print(clm.line())
            print(clm.header(megnevezés=30, változás=12, egységár=19, érték=1))
            for record in logbook.records:
                print(record)
            print(clm.line())
            print("{:>51} {:>14} Ft".format("Összesen:", logbook.total))
            print(clm.line())

    def _choose_month(self) -> str:
        months = [month[0] for month in self._dbs.query_months()]
        month_menu = clm.CliMenu(months, title="Válassz hónapot!")
        month_menu.show()
        choice = month_menu.listen()
        return months[choice]

    def _choose_project(self, month:str) -> str:
        logbooks = [lb.LogBook(self._dbs.query_log(project[0], month))\
                    for project in self._dbs.query_projects(month)]
        project_menu = clm.CliMenu(logbooks, title="Válassz projektet!")
        project_menu.show()
        choice = project_menu.listen()
        return logbooks[choice]


if __name__ == "__main__":
    app = App()
    app.run()
