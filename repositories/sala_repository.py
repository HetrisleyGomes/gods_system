import psycopg2
class SalaRepository:
    def __init__(self, conn):
        self.__conn = conn

    def set_sala(self, sala):
        cursor = self.__conn.cursor()
        cursor.execute(
            """
            INSERT INTO sala(id, codigo, nome, senha)
            VALUES(%s, %s, %s, %s)
            """,
            (sala["id"], sala["codigo"], sala["nome"], sala["senha"])
        )
        self.__conn.commit()
        cursor.close()

    def get_sala_by_code(self, codigo):
        cursor = self.__conn.cursor()
        cursor.execute(
            """
            SELECT * FROM sala WHERE codigo = %s
            """,
            (codigo,)
        )
        sala = cursor.fetchone()
        cursor.close()
        return sala
    
    def get_sala_by_id(self, id):
        cursor = self.__conn.cursor()
        cursor.execute(
            """
            SELECT * FROM sala WHERE id = %s
            """,
            (id,)
        )
        sala = cursor.fetchone()
        cursor.close()
        return sala

    def get_salas(self):
        cursor = self.__conn.cursor()
        cursor.execute(
            """
            SELECT * FROM sala
            """
        )
        salas = cursor.fetchall()
        cursor.close()
        return salas

    def get_notes(self, id):
        cursor = self.__conn.cursor()
        cursor.execute(
            """
            SELECT notes FROM sala WHERE id = %s
            """,
            (id,)
        )
        notas = cursor.fetchone()
        cursor.close()
        return notas

    def set_ficha(self, id, ficha_id):
        cursor = self.__conn.cursor()
        cursor.execute(
            """
            UPDATE sala SET fichas = %s WHERE id = %s
            """,
            (ficha_id, id)
        )
        self.__conn.commit()
        cursor.close()

    def remove_fichas(self, ficha_id):
        cursor = self.__conn.cursor()
        cursor.execute(
            """
            DELETE FROM sala WHERE fichas = %s
            """,
            (ficha_id,)
        )
        self.__conn.commit()
        self.__conn.close()