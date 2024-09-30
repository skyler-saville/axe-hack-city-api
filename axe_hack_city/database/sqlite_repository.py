# database/sqlite_repository.py
import sqlite3
import json
from typing import Type, List, Any
from pydantic import BaseModel
from .create_tables import create_tables
from ..config.settings import settings

class SQLiteRepository:
    def __init__(self, db_path: str = settings.database_url):
        self.db_path = db_path
        self.create_tables()

    def create_tables(self):
        # Use the imported create_tables function to create the necessary tables
        with sqlite3.connect(self.db_path) as conn:
            create_tables(conn)

    def create(self, model: Type[BaseModel]) -> BaseModel:
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            # Get the table name from the model class
            table_name = model.__class__.__name__.lower() + 's'
            # Build the INSERT query dynamically based on the model's fields
            fields = ', '.join(model.model_fields.keys())
            placeholders = ', '.join(['?' for _ in model.model_fields])
            query = f"INSERT INTO {table_name} ({fields}) VALUES ({placeholders})"
            # Convert the model instance to a list of values (handle JSON serialization)
            values = [json.dumps(value) if isinstance(value, (list, dict)) else value for value in model.model_dump().values()]
            cursor.execute(query, values)
            conn.commit()
            # Retrieve the newly created record and return it as a model instance
            record_id = cursor.lastrowid
            return self.get(model.__class__, record_id)

    def get(self, model: Type[BaseModel], id: int) -> BaseModel:
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            # Get the table name from the model class
            table_name = model.__name__.lower() + 's'
            query = f"SELECT * FROM {table_name} WHERE id = ?"
            cursor.execute(query, (id,))
            row = cursor.fetchone()
            if row:
                # Convert the row to a dictionary and deserialize JSON fields
                data = {field: (json.loads(value) if isinstance(model.model_fields[field].type_, (list, dict)) else value)
                        for field, value in zip(model.model_fields, row)}
                return model(**data)
            else:
                return None

    def update(self, model: BaseModel) -> BaseModel:
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            # Get the table name from the model class
            table_name = model.__class__.__name__.lower() + 's'
            # Build the UPDATE query dynamically based on the model's fields
            set_clause = ', '.join(f"{field} = ?" for field in model.model_fields)
            query = f"UPDATE {table_name} SET {set_clause} WHERE id = ?"
            # Convert the model instance to a list of values (handle JSON serialization)
            values = [json.dumps(value) if isinstance(value, (list, dict)) else value for value in model.model_dump().values()] + [model.id]
            cursor.execute(query, values)
            conn.commit()
            return model

    def delete(self, model: Type[BaseModel], id: int) -> None:
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            # Get the table name from the model class
            table_name = model.__name__.lower() + 's'
            query = f"DELETE FROM {table_name} WHERE id = ?"
            cursor.execute(query, (id,))
            conn.commit()

    def list(self, model: Type[BaseModel], **filters) -> List[BaseModel]:
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            # Get the table name from the model class
            table_name = model.__name__.lower() + 's'
            # Build the SELECT query dynamically based on the filters
            where_clause = ' AND '.join(f"{field} = ?" for field in filters)
            query = f"SELECT * FROM {table_name}"
            if where_clause:
                query += f" WHERE {where_clause}"
            # Execute the query and convert the rows to model instances
            cursor.execute(query, list(filters.values()))
            rows = cursor.fetchall()
            return [model(**{field: (json.loads(value) if isinstance(model.model_fields[field].type_, (list, dict)) else value)
                            for field, value in zip(model.model_fields, row)})
                    for row in rows]
