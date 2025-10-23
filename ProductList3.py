import sys
from typing import Optional, Tuple
from PyQt5.QtWidgets import QApplication, QMainWindow, QTableWidgetItem, QMessageBox
from PyQt5.QtCore import Qt
from PyQt5 import uic
import sqlite3
import os.path

# 상수 정의
DB_NAME = "ProductList.db"
UI_FILE = "ProductList3.ui"
TABLE_COLUMNS = ["제품ID", "제품명", "가격"]
COLUMN_WIDTHS = [100, 200, 100]

class DatabaseManager:
    def __init__(self, db_name: str):
        self.db_name = db_name
        self.connection = None
        self.cursor = None
        self.initialize_db()

    def initialize_db(self) -> None:
        is_new_db = not os.path.exists(self.db_name)
        self.connection = sqlite3.connect(self.db_name)
        self.cursor = self.connection.cursor()
        
        if is_new_db:
            self.cursor.execute(
                "CREATE TABLE Products (id INTEGER PRIMARY KEY AUTOINCREMENT, Name TEXT, Price INTEGER);"
            )

    def insert_product(self, name: str, price: str) -> None:
        try:
            self.cursor.execute("INSERT INTO Products (Name, Price) VALUES (?, ?);", 
                              (name, price))
            self.connection.commit()
        except sqlite3.Error as e:
            QMessageBox.critical(None, "데이터베이스 오류", f"제품 추가 실패: {str(e)}")

    def update_product(self, product_id: str, name: str, price: str) -> None:
        try:
            self.cursor.execute("UPDATE Products SET Name=?, Price=? WHERE id=?;", 
                              (name, price, product_id))
            self.connection.commit()
        except sqlite3.Error as e:
            QMessageBox.critical(None, "데이터베이스 오류", f"제품 수정 실패: {str(e)}")

    def delete_product(self, product_id: str) -> None:
        try:
            self.cursor.execute("DELETE FROM Products WHERE id=?;", (product_id,))
            self.connection.commit()
        except sqlite3.Error as e:
            QMessageBox.critical(None, "데이터베이스 오류", f"제품 삭제 실패: {str(e)}")

    def get_all_products(self) -> list:
        return self.cursor.execute("SELECT * FROM Products;").fetchall()

class ProductWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.db_manager = DatabaseManager(DB_NAME)
        self.setup_ui()
        self.initialize_ui()

    def setup_ui(self) -> None:
        form_class = uic.loadUiType(UI_FILE)[0]
        self.ui = form_class()
        self.ui.setupUi(self)
        
        # 테이블 위젯 설정
        self.setup_table_widget()
        
        # 이벤트 연결
        self.connect_events()

    def initialize_ui(self) -> None:
        self.clear_input_fields()
        self.refresh_product_list()

    def setup_table_widget(self) -> None:
        # 컬럼 설정
        for idx, width in enumerate(COLUMN_WIDTHS):
            self.ui.tableWidget.setColumnWidth(idx, width)
        
        self.ui.tableWidget.setHorizontalHeaderLabels(TABLE_COLUMNS)
        self.ui.tableWidget.setTabKeyNavigation(False)

    def connect_events(self) -> None:
        # 버튼 이벤트
        self.ui.btnAdd.clicked.connect(self.btnAdd_clicked)
        self.ui.btnUpdate.clicked.connect(self.btnUpdate_clicked)
        self.ui.btnDel.clicked.connect(self.btnDel_clicked)
        
        # 엔터키 이벤트
        self.ui.prodID.returnPressed.connect(self.focus_next_child)
        self.ui.prodName.returnPressed.connect(self.focus_next_child)
        self.ui.prodPrice.returnPressed.connect(self.focus_next_child)
        
        # 더블클릭 이벤트
        self.ui.tableWidget.doubleClicked.connect(self.tableWidget_doubleClicked)

    def clear_input_fields(self) -> None:
        self.ui.prodID.clear()
        self.ui.prodName.clear()
        self.ui.prodPrice.clear()

    def get_input_values(self) -> Tuple[str, str, str]:
        return (
            self.ui.prodID.text().strip(),
            self.ui.prodName.text().strip(),
            self.ui.prodPrice.text().strip()
        )

    def btnAdd_clicked(self) -> None:
        _, name, price = self.get_input_values()
        if name and price:
            self.db_manager.insert_product(name, price)
            self.refresh_product_list()
            self.clear_input_fields()
        else:
            QMessageBox.warning(self, "입력 오류", "제품명과 가격을 입력하세요.")

    def btnUpdate_clicked(self) -> None:
        product_id, name, price = self.get_input_values()
        if product_id and name and price:
            self.db_manager.update_product(product_id, name, price)
            self.refresh_product_list()
            self.clear_input_fields()
        else:
            QMessageBox.warning(self, "입력 오류", "모든 필드를 입력하세요.")

    def btnDel_clicked(self) -> None:
        product_id = self.ui.prodID.text().strip()
        if product_id:
            reply = QMessageBox.question(self, '삭제 확인', 
                                       '선택한 제품을 삭제하시겠습니까?',
                                       QMessageBox.Yes | QMessageBox.No)
            if reply == QMessageBox.Yes:
                self.db_manager.delete_product(product_id)
                self.refresh_product_list()
                self.clear_input_fields()
        else:
            QMessageBox.warning(self, "선택 오류", "삭제할 제품을 선택하세요.")

    def refresh_product_list(self) -> None:
        self.ui.tableWidget.clearContents()
        products = self.db_manager.get_all_products()
        
        for row, product in enumerate(products):
            self.set_table_row(row, product)

    def set_table_row(self, row: int, product: tuple) -> None:
        # ID 설정
        id_item = QTableWidgetItem(f"{product[0]:10}")
        id_item.setTextAlignment(Qt.AlignRight)
        self.ui.tableWidget.setItem(row, 0, id_item)
        
        # 제품명 설정
        name_item = QTableWidgetItem(product[1])
        self.ui.tableWidget.setItem(row, 1, name_item)
        
        # 가격 설정
        price_item = QTableWidgetItem(f"{product[2]:10}")
        price_item.setTextAlignment(Qt.AlignRight)
        self.ui.tableWidget.setItem(row, 2, price_item)

    def tableWidget_doubleClicked(self) -> None:
        current_row = self.ui.tableWidget.currentRow()
        self.ui.prodID.setText(self.ui.tableWidget.item(current_row, 0).text().strip())
        self.ui.prodName.setText(self.ui.tableWidget.item(current_row, 1).text().strip())
        self.ui.prodPrice.setText(self.ui.tableWidget.item(current_row, 2).text().strip())

def main():
    app = QApplication(sys.argv)
    window = ProductWindow()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()



