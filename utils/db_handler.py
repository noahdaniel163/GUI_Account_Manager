import os
import sqlite3
import pyodbc
from .logger import Logger
from queue import Queue
from threading import Lock
import threading

logger = Logger('database')

class DatabaseHandler:
    def __init__(self):
        self.conn = None
        self.conn_str = (
            "DRIVER={ODBC Driver 17 for SQL Server};"
            "SERVER=10.8.103.21;"
            "DATABASE=simo;"
            "UID=sa;"
            "PWD=q;"
            "Connection Timeout=30;"
            "Pooling=true;"  # Enable connection pooling
            "Max Pool Size=10;"  # Maximum connections in pool
        )
        self._lock = Lock()
        self._connection_pool = Queue(maxsize=10)
        self._init_connection_pool()

    def _init_connection_pool(self):
        """Initialize connection pool with a few connections"""
        try:
            for _ in range(3):  # Start with 3 connections
                conn = pyodbc.connect(self.conn_str)
                self._connection_pool.put(conn)
        except Exception as e:
            logger.error(f"Error initializing connection pool: {str(e)}")

    def get_connection(self):
        """Get a connection from the pool or create new if needed"""
        try:
            # Try to get a connection from the pool
            conn = self._connection_pool.get(block=True, timeout=5)
            try:
                # Test if connection is still alive
                conn.execute("SELECT 1").fetchone()
                return conn
            except:
                # Connection is dead, create new one
                return pyodbc.connect(self.conn_str)
        except:
            # Pool is empty, create new connection
            return pyodbc.connect(self.conn_str)

    def return_connection(self, conn):
        """Return a connection to the pool"""
        try:
            self._connection_pool.put(conn, block=False)
        except:
            try:
                conn.close()
            except:
                pass

    def execute_query(self, query, params=None, fetchall=True):
        """Execute query with automatic connection management"""
        conn = None
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            
            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)
                
            if fetchall:
                result = cursor.fetchall()
            else:
                result = cursor.fetchone()
                
            conn.commit()
            return result
        except Exception as e:
            if conn:
                try:
                    conn.rollback()
                except:
                    pass
            raise e
        finally:
            if conn:
                self.return_connection(conn)
    
    def close_all(self):
        """Close all connections in the pool"""
        while not self._connection_pool.empty():
            try:
                conn = self._connection_pool.get_nowait()
                conn.close()
            except:
                continue

    def close(self):
        if self.conn:
            self.conn.close()
            logger.info("Đã đóng kết nối database")