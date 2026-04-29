from sqlalchemy import text
from config.database import engine


class SuperModel:

    allowed_tables = ["users"]

    @staticmethod
    def add(table, data):
        if table not in SuperModel.allowed_tables:
            return False

        fields = ", ".join(data.keys())
        placeholders = ", ".join([f":{k}" for k in data.keys()])

        query = text(f"INSERT INTO {table} ({fields}) VALUES ({placeholders})")

        try:
            with engine.begin() as conn:   # auto commit
                conn.execute(query, data)
            return True

        except Exception as e:
            print("Error:", e)
            return False

    @staticmethod
    def get_single_record(table, where_dict=None, select="*"):
        if table not in SuperModel.allowed_tables:
            return None

        query = f"SELECT {select} FROM {table}"
        params = {}

        if where_dict:
            clauses = []
            for key, value in where_dict.items():
                clauses.append(f"{key} = :{key}")
                params[key] = value

            query += " WHERE " + " AND ".join(clauses)

        query += " LIMIT 1"

        try:
            with engine.connect() as conn:
                result = conn.execute(text(query), params)
                row = result.fetchone()
                return dict(row._mapping) if row else None

        except Exception as e:
            print("Error:", e)
            return None

    @staticmethod
    def all_records(table):
        if table not in SuperModel.allowed_tables:
            return []

        try:
            with engine.connect() as conn:
                result = conn.execute(text(f"SELECT * FROM {table}"))
                rows = result.fetchall()
                return [dict(row._mapping) for row in rows]

        except Exception as e:
            print("Error:", e)
            return []