import os
import sqlite3
import random
import string
import time


class ProductDB:
    def __init__(self, db_filename="MyProduct.db"):
        # DB 파일은 현재 스크립트 폴더(c:\work)에 생성됩니다
        base = os.path.dirname(__file__) or os.getcwd()
        self.db_path = db_filename if os.path.isabs(db_filename) else os.path.join(base, db_filename)

    def _connect(self):
        con = sqlite3.connect(self.db_path, timeout=30)
        con.execute("PRAGMA journal_mode = WAL;")
        con.execute("PRAGMA synchronous = NORMAL;")
        return con

    def create_table(self):
        with self._connect() as con:
            con.execute(
                """
                CREATE TABLE IF NOT EXISTS Products (
                    productID INTEGER PRIMARY KEY,
                    productName TEXT NOT NULL,
                    productPrice INTEGER NOT NULL
                )
                """
            )

    def insert_product(self, productID: int, productName: str, productPrice: int):
        with self._connect() as con:
            con.execute(
                "INSERT INTO Products(productID, productName, productPrice) VALUES (?, ?, ?)",
                (productID, productName, productPrice),
            )

    def bulk_insert_products(self, products, batch_size=5000):
        """
        products: iterable of (productID, productName, productPrice)
        batch_size: 한 번에 커밋할 배치 크기 (성능/메모리 고려)
        """
        with self._connect() as con:
            cur = con.cursor()
            it = iter(products)
            while True:
                batch = []
                try:
                    for _ in range(batch_size):
                        batch.append(next(it))
                except StopIteration:
                    pass
                if not batch:
                    break
                cur.executemany(
                    "INSERT OR IGNORE INTO Products(productID, productName, productPrice) VALUES (?, ?, ?)",
                    batch,
                )
                con.commit()

    def update_product(self, productID: int, productName: str = None, productPrice: int = None):
        if productName is None and productPrice is None:
            return
        parts = []
        params = []
        if productName is not None:
            parts.append("productName = ?")
            params.append(productName)
        if productPrice is not None:
            parts.append("productPrice = ?")
            params.append(productPrice)
        params.append(productID)
        sql = f"UPDATE Products SET {', '.join(parts)} WHERE productID = ?"
        with self._connect() as con:
            con.execute(sql, params)

    def delete_product(self, productID: int):
        with self._connect() as con:
            con.execute("DELETE FROM Products WHERE productID = ?", (productID,))

    def select_product(self, productID: int):
        with self._connect() as con:
            cur = con.execute("SELECT productID, productName, productPrice FROM Products WHERE productID = ?", (productID,))
            return cur.fetchone()

    def select_all(self, limit=100, offset=0):
        with self._connect() as con:
            cur = con.execute(
                "SELECT productID, productName, productPrice FROM Products ORDER BY productID LIMIT ? OFFSET ?",
                (limit, offset),
            )
            return cur.fetchall()

    def count(self):
        with self._connect() as con:
            cur = con.execute("SELECT COUNT(1) FROM Products")
            return cur.fetchone()[0]

    def generate_sample_and_insert(self, target_count=100000, start_id=1, batch_size=5000):
        """
        target_count: 총 목표 레코드 수 (예: 100000)
        start_id: 시작 productID (기본 1)
        batch_size: 한 번에 삽입하는 배치 크기
        """
        existing = self.count()
        if existing >= target_count:
            return  # 이미 충분히 데이터가 있음
        needed = target_count - existing
        next_id = start_id + existing
        def product_gen():
            nonlocal next_id, needed
            for i in range(needed):
                pid = next_id + i
                name = f"Product_{pid}"
                price = random.randint(100, 100000)
                yield (pid, name, price)

        t0 = time.time()
        self.bulk_insert_products(product_gen(), batch_size=batch_size)
        t1 = time.time()
        print(f"Inserted {needed} rows in {t1 - t0:.2f}s. DB path: {self.db_path}")


if __name__ == "__main__":
    db = ProductDB()  # c:\work\MyProduct.db 생성
    db.create_table()
    # 샘플 100,000개 준비 (이미 있으면 건너뜀)
    db.generate_sample_and_insert(target_count=100000, batch_size=5000)

    # 예시 사용법
    print("총 레코드:", db.count())
    print("샘플 조회:", db.select_product(1))
    db.update_product(1, productName="Updated_Product_1", productPrice=9999)
    print("업데이트 후 조회:", db.select_product(1))
    db.delete_product(1)
    print("삭제 후 조회(없으면 None):", db.select_product(1))