import sys
from typing import Dict

from PyQt5 import QtCore, QtWidgets
from PyQt5.QtSql import (
    QSqlDatabase,
    QSqlRelationalTableModel,
    QSqlTableModel,
    QSqlRelationalDelegate,
    QSqlRelation,
)


DEFAULT_DATABASE_PATH = "db.sqlite3"


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self) -> None:
        super().__init__()

        self.db = QSqlDatabase.addDatabase("QSQLITE")
        self.dbpath = DEFAULT_DATABASE_PATH
        self.qmainwindow = QtWidgets.QMainWindow()

        # define buttons vehaviour
        self.button_actions: Dict[str, QtWidgets.QAction] = {}
        self.define_buttons()

        # UI variables
        self.label = QtWidgets.QLabel()
        self.combo_box = QtWidgets.QComboBox()
        self.table_model = QSqlRelationalTableModel()
        self.table_view = QtWidgets.QTableView()

        # create window and show it
        self.draw()
        self.qmainwindow.show()

    def draw(self) -> None:
        self.qmainwindow.setObjectName("MainWindow")
        self.qmainwindow.resize(800, 600)
        self.qmainwindow.setWindowTitle("Database manager")

        widget = QtWidgets.QWidget(self.qmainwindow)
        widget.setObjectName("widget")
        self.qmainwindow.setCentralWidget(widget)

        self.toolbar = self.qmainwindow.addToolBar("ToolBar")
        for _, action in self.button_actions.items():
            self.toolbar.addAction(action)

        _ = QtWidgets.QLabel(widget)
        _.setGeometry(QtCore.QRect(QtCore.QPoint(10, 10), QtCore.QSize(105, 16)))
        _.setText("Database path: ")
        self.label = QtWidgets.QLabel(widget)
        self.label.setGeometry(QtCore.QRect(QtCore.QPoint(110, 10), QtCore.QSize(750, 16)))
        self.label.setText(self.dbpath)

        _ = QtWidgets.QLabel(widget)
        _.setGeometry(QtCore.QRect(QtCore.QPoint(10, 30), QtCore.QSize(105, 16)))
        _.setText("Choosen table: ")
        self.combo_box = QtWidgets.QComboBox(self.qmainwindow)
        self.combo_box.setGeometry(QtCore.QRect(QtCore.QPoint(100, 55), QtCore.QSize(200, 16)))
        self.combo_box.currentIndexChanged.connect(self.update_table)

        _ = QtWidgets.QLabel(widget)
        _.setGeometry(QtCore.QRect(QtCore.QPoint(10, 65), QtCore.QSize(105, 16)))
        _.setText("Table")

        self.table_view = QtWidgets.QTableView(self.qmainwindow)
        self.table_view.setObjectName("tableView")
        self.table_view.setGeometry(QtCore.QRect(QtCore.QPoint(10, 115), QtCore.QSize(780, 475)))
        self.table_view.setShowGrid(False)

    def define_buttons(self) -> None:
        def _exit_action() -> None:
            QtWidgets.qApp.quit()

        def _show_dialog() -> None:
            self.dbpath, _ = QtWidgets.QFileDialog.getOpenFileName(self, "Open file")
            self.label.setText(self.dbpath)

        def _load_database() -> None:
            self.db.setDatabaseName(self.dbpath)
            self.db.open()

            # update selectors
            self.combo_box.clear()
            for tbl in self.db.tables():
                self.combo_box.addItem(tbl)
            self.update_table()

        def _save_database() -> None:
            self.table_model.submitAll()

        def _insert_row() -> None:
            self.table_model.insertRows(self.table_model.rowCount(), 1)

        def _remove_row() -> None:
            for idx in self.table_view.selectedIndexes():
                self.table_model.removeRows(idx.row(), 1)

        self.button_actions.update({"exit": QtWidgets.QAction("Exit", self.qmainwindow)})
        self.button_actions["exit"].triggered.connect(_exit_action)

        self.button_actions.update(
            {"dbpath": QtWidgets.QAction("Set database path", self.qmainwindow)}
        )
        self.button_actions["dbpath"].triggered.connect(_show_dialog)

        self.button_actions.update({"load": QtWidgets.QAction("Load database", self.qmainwindow)})
        self.button_actions["load"].triggered.connect(_load_database)

        self.button_actions.update({"save": QtWidgets.QAction("Save database", self.qmainwindow)})
        self.button_actions["save"].triggered.connect(_save_database)

        self.button_actions.update({"insert": QtWidgets.QAction("Insert row", self.qmainwindow)})
        self.button_actions["insert"].triggered.connect(_insert_row)

        self.button_actions.update({"remove": QtWidgets.QAction("Remove row", self.qmainwindow)})
        self.button_actions["remove"].triggered.connect(_remove_row)

    def update_table(self) -> None:
        self.table_model = QSqlRelationalTableModel()

        tablename = self.combo_box.currentText()
        self.table_model.setTable(tablename)

        # foreign key logic
        if tablename == "goods":
            self.table_model.setRelation(2, QSqlRelation("units", "id", "unit"))
            self.table_model.setRelation(3, QSqlRelation("categories", "id", "name"))
        elif tablename == "employees":
            self.table_model.setRelation(2, QSqlRelation("positions", "id", "position"))
        elif tablename == "vendors":
            self.table_model.setRelation(2, QSqlRelation("ownerships", "id", "ownership"))

        self.table_model.select()
        self.table_model.setEditStrategy(QSqlTableModel.OnManualSubmit)

        self.table_view.setModel(self.table_model)
        self.table_view.setItemDelegate(QSqlRelationalDelegate(self.table_view))

        # define header width
        self.table_view.horizontalHeader().setStretchLastSection(False)
        self.table_view.resizeColumnsToContents()
        self.table_view.horizontalHeader().setMinimumSectionSize(50)
        self.table_view.horizontalHeader().setStretchLastSection(True)


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    main_window = MainWindow()
    sys.exit(app.exec())
