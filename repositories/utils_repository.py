from psycopg2.extensions import connection as Connection

class UtilsRepository:
    def __init__(self, conn: Connection):
        self.__conn = conn

    def get_poder(self, id):
        cursor = self.__conn.cursor()
        cursor.execute(
            """
            SELECT * FROM poder WHERE id = %s
            """,
            (id,)
        )
        poder = cursor.fetchone()
        cursor.close()
        return poder
    
    def get_all_poderes(self):
        cursor = self.__conn.cursor()
        cursor.execute(
            """
            SELECT * FROM poder
            """
        )
        poderes = cursor.fetchall()
        cursor.close()
        return poderes
    
    def set_ficha_poder(self, ficha_id, poder_id):
        cursor = self.__conn.cursor()
        cursor.execute(
            """
            INSERT INTO ficha_poder(ficha_id, poder_id)
            VALUES(%s, %s)
            """,
            (ficha_id, poder_id)
        )
        self.__conn.commit()
        cursor.close()
    
    def remove_ficha_poder(self, ficha_id, poder_id):
        cursor = self.__conn.cursor()
        cursor.execute(
            """
            DELETE FROM ficha_poder
            WHERE ficha_id = %s AND poder_id = %s;
            """,
            (ficha_id, poder_id)
        )
        self.__conn.commit()
        cursor.close()
    
    def get_equipamento(self, id):
        cursor = self.__conn.cursor()
        cursor.execute(
            """
            SELECT * FROM equipamento WHERE id = %s
            """,
            (id,)
        )
        equipamento = cursor.fetchone()
        cursor.close()
        return equipamento
    
    def get_all_equipamentos(self):
        cursor = self.__conn.cursor()
        cursor.execute(
            """
            SELECT * FROM equipamento
            """
        )
        equipamentos = cursor.fetchall()
        cursor.close()
        return equipamentos
    
    def set_ficha_equipamento(self, ficha_id, equipamento_id):
        cursor = self.__conn.cursor()
        cursor.execute(
            """
            INSERT INTO ficha_equipamento(ficha_id, equipamento_id)
            VALUES(%s, %s)
            """,
            (ficha_id, equipamento_id)
        )
        self.__conn.commit()
        cursor.close()
    
    def remove_ficha_equipamento(self, ficha_id, equipamento_id):
        cursor = self.__conn.cursor()
        cursor.execute(
            """
            DELETE FROM ficha_equipamento
            WHERE ficha_id = %s AND equipamento_id = %s;
            """,
            (ficha_id, equipamento_id)
            )
        self.__conn.commit()
        cursor.close()