import sqlite3
import time
from .builder import QueryBuilder, RawExpression
from .querylog import QueryLog


class DB:
    """Thin wrapper around SQLite that uses QueryBuilder and QueryLog."""

    _query_log = QueryLog()

    def __init__(self, db_path):
        self._db_path = db_path
        self._connection = sqlite3.connect(db_path)
        self._connection.row_factory = sqlite3.Row

    @classmethod
    def raw(cls, expression):
        """Create a raw SQL expression that won't be quoted."""
        return RawExpression(expression)

    @classmethod
    def enable_query_log(cls):
        """Enable the global query log."""
        cls._query_log.enable()

    @classmethod
    def disable_query_log(cls):
        """Disable the global query log."""
        cls._query_log.disable()

    @classmethod
    def get_query_log(cls):
        """Get all logged queries."""
        return cls._query_log.get_log()

    @classmethod
    def clear_query_log(cls):
        """Clear the query log."""
        cls._query_log.clear()

    def query(self):
        """Return a new QueryBuilder instance."""
        return QueryBuilder(connection=self._connection)

    def execute(self, query_builder):
        """Execute a query built with QueryBuilder and return results."""
        sql = query_builder.to_sql()
        bindings = query_builder.get_bindings()

        start = time.time()
        cursor = self._connection.execute(sql.replace('`', '"'), bindings)
        elapsed = time.time() - start

        self._query_log.log_query(sql, bindings, elapsed)

        return cursor.fetchall()

    def close(self):
        """Close the database connection."""
        self._connection.close()
