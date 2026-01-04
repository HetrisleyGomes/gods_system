from psycopg2.extensions import connection as Connection
import json

class MechaRepository:
    def __init__(self, conn: Connection):
        self.__conn = conn
    
    def set_mecha(self, mecha):
        cursor = self.__conn.cursor()
        cursor.execute(
            """
            INSERT INTO mecha (
                nome, ficha_id,
                vida, vida_atual,
                armadura, combate, pontaria, defesa, forca,
                armas, habilidades
            ) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
            """, (
                mecha["nome"],
                mecha["ficha_id"],
                mecha["vida"],
                mecha["vida"],
                mecha["armadura"],
                mecha["combate"],
                mecha["pontaria"],
                mecha["defesa"],
                mecha["forca"],
                json.dumps(mecha["armas"]),
                json.dumps(mecha["habilidades"])
                )
        )
        self.__conn.commit()
        cursor.close()
    
    def get_mecha(self, id):
        cursor = self.__conn.cursor()
        cursor.execute(
            """
            SELECT id, nome, ficha_id, vida, vida_atual, armadura, combate, pontaria, defesa, forca, habilidades, armas FROM mecha WHERE id = %s
            """,
            (id,)
        )
        mecha = cursor.fetchone()
        cursor.close()
        return mecha
    
    def get_mecha_by_ficha_id(self, id):
        cursor = self.__conn.cursor()
        cursor.execute(
            """
            SELECT id, nome, ficha_id, vida, vida_atual, armadura, combate, pontaria, defesa, forca, habilidades, armas FROM mecha WHERE ficha_id = %s
            """,
            (id,)
        )
        mecha = cursor.fetchone()
        cursor.close()
        return mecha
    
    def edit_mecha(self, id, mecha):
        cursor = self.__conn.cursor()
        cursor.execute(
            """
            UPDATE mecha
            SET nome = %s,
            vida = %s,
            vida_atual = %s,
            armadura = %s,
            combate = %s,
            pontaria = %s,
            defesa = %s,
            forca = %s,
            armas = %s,
            habilidades = %s
            WHERE id = %s
            """, (
                mecha["nome"],
                mecha["vida"],
                mecha["vida_atual"],
                mecha["armadura"],
                mecha["combate"],
                mecha["pontaria"],
                mecha["defesa"],
                mecha["forca"],
                json.dumps(mecha["armas"]),
                json.dumps(mecha["habilidades"]),
                id
            )
        )
        self.__conn.commit()
        cursor.close()

    def set_vida(self, id, valor):
        cursor = self.__conn.cursor()
        cursor.execute(
            """
            UPDATE mecha
            SET vida_atual = %s
            WHERE id = %s
            """,
            (valor, id)
        )
        self.__conn.commit()
        cursor.close()

    def delete_mecha(self, id):
        cursor = self.__conn.cursor()
        cursor.execute(
            """
            DELETE FROM mecha WHERE id = %s
            """,
            (id,)
        )
        self.__conn.commit()
        cursor.close()