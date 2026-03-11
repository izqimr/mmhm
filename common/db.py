from common.yml import Yml

try:
    import pymysql
except Exception:  # pragma: no cover - import-time optional dependency
    pymysql = None


class DB:
    def __init__(self, db_key="franchise"):
        self.yml = Yml()
        if db_key == "franchise":
            self._db = self.yml.get_franchiseDB_info()
        elif db_key == "store":
            self._db = self.yml.get_storeDB_info()
        else:
            raise ValueError(f"unknown db_key: {db_key}")

    def connect(self):
        """
        连接数据库，返回 pymysql connection
        """
        if pymysql is None:
            raise RuntimeError("pymysql 未安装，无法连接数据库")
        return pymysql.connect(
            host=self._db["DB_host"],
            user=self._db["DB_user"],
            password=self._db["DB_password"],
            port=int(self._db["DB_port"]),
            database=self._db["DataBase"],
            charset="utf8mb4",
            autocommit=True,
        )
    
    def fetchone(self, sql, params=None):
        """
        执行查询并返回一条记录
        """
        conn = self.connect()
        try:
            with conn.cursor() as cursor:
                cursor.execute(sql, params)
                return cursor.fetchone()
        finally:
            conn.close()

    def fetchall(self, sql, params=None):
        """
        执行查询并返回多条记录
        """
        conn = self.connect()
        try:
            with conn.cursor() as cursor:
                cursor.execute(sql, params)
                return cursor.fetchall()
        finally:
            conn.close()

    def execute(self, sql, params=None):
        """
        执行写入/更新/删除
        """
        conn = self.connect()
        try:
            with conn.cursor() as cursor:
                rows = cursor.execute(sql, params)
                return rows
        finally:
            conn.close()
