from psycopg2.extensions import connection as Connection
from psycopg2.extras import DictCursor

class FichaRepository:
    def __init__(self, conn: Connection):
        self.__conn = conn

    def set_ficha(self, ficha):
        cursor = self.__conn.cursor()
        cursor.execute(
            """
               INSERT INTO ficha
                   (id, sala_id,nome_personagem, vida, energia, armadura, nivel, xp, cor, especie, arquetipo, forca, constituicao, inteligencia, destreza, carisma, combate, atletismo, tecnologia, percepcao, conhecimento, pontaria, furtividade, atuacao, iniciativa, vida_atual, energia_atual)
               VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s, %s, %s)
           """, (
            ficha["id"],
            ficha["sala_id"],
            ficha["nome_personagem"],
            ficha["vida"],
            ficha["energia"],
            ficha["armadura"],
            ficha["nivel"],
            ficha["xp"],
            ficha["cor"],
            ficha["especie"],
            ficha["arquetipo"],
            ficha["forca"],
            ficha["constituicao"],
            ficha["inteligencia"],
            ficha["destreza"],
            ficha["carisma"],
            ficha["combate"],
            ficha["atletismo"],
            ficha["tecnologia"],
            ficha["percepcao"],
            ficha["conhecimento"],
            ficha["pontaria"],
            ficha["furtividade"],
            ficha["atuacao"],
            ficha["iniciativa"],
            ficha["vida"],
            ficha["energia"],
            )
        )
        self.__conn.commit()
        cursor.close()

    def get_all_ficha(self):
        cursor = self.__conn.cursor()
        cursor.execute(
            """
            SELECT *
            FROM ficha
            """
        )
        data = cursor.fetchall()
        cursor.close()
        return data

    def get_ficha(self, ficha_id):
        cursor = self.__conn.cursor()
        cursor.execute(
            """
            SELECT "id", "sala_id", "nome_personagem", "vida", "energia", "armadura", "nivel", "xp", "cor", "especie", "arquetipo", "forca", "constituicao", "inteligencia", "destreza", "carisma", "combate", "atletismo", "tecnologia", "percepcao", "conhecimento", "pontaria", "furtividade", "atuacao", "iniciativa", "vida_atual", "energia_atual"
            FROM ficha
            WHERE id = %s
            """,
            (ficha_id,),
        )
        data = cursor.fetchone()
        cursor.close()
        return data

    def edit_ficha(self, id, ficha):
        cursor = self.__conn.cursor()
        cursor.execute(
            """
            UPDATE ficha
            SET nome_personagem = %s,
            vida = %s,
            energia = %s,
            armadura = %s,
            nivel = %s,
            xp = %s,
            cor = %s,
            especie = %s,
            arquetipo = %s,
            forca = %s,
            constituicao = %s,
            inteligencia = %s,
            destreza = %s,
            carisma = %s,
            combate = %s,
            atletismo = %s,
            tecnologia = %s,
            percepcao = %s,
            conhecimento = %s,
            pontaria = %s,
            furtividade = %s,
            atuacao = %s,
            iniciativa = %s,
            vida_atual = %s,
            energia_atual = %s
            WHERE id = %s""",
            (
                ficha["nome_personagem"],
                ficha["vida"],
                ficha["energia"],
                ficha["armadura"],
                ficha["nivel"],
                ficha["xp"],
                ficha["cor"],
                ficha["especie"],
                ficha["arquetipo"],
                ficha["forca"],
                ficha["constituicao"],
                ficha["inteligencia"],
                ficha["destreza"],
                ficha["carisma"],
                ficha["combate"],
                ficha["atletismo"],
                ficha["tecnologia"],
                ficha["percepcao"],
                ficha["conhecimento"],
                ficha["pontaria"],
                ficha["furtividade"],
                ficha["atuacao"],
                ficha["iniciativa"],
                ficha["vida_atual"],
                ficha["energia_atual"],
                id,
            )
        )
        self.__conn.commit()
        cursor.close()

    def set_vida(self, id, valor):
        cursor = self.__conn.cursor()
        cursor.execute(
            """
            UPDATE ficha
            SET vida_atual = %s
            WHERE id = %s
            """,
            (valor, id)
        )
        self.__conn.commit()
        cursor.close()
    
    def set_energia(self, id, valor):
        cursor = self.__conn.cursor()
        cursor.execute(
            """
            UPDATE ficha
            SET energia_atual = %s
            WHERE id = %s
            """,
            (valor, id)
        )
        self.__conn.commit()
        cursor.close()

    def delete_ficha(self, id):
        cursor = self.__conn.cursor()
        cursor.execute(
            """
            DELETE FROM ficha WHERE id = %s
            """, (id)
        )
        self.__conn.commit()
        cursor.close()
    
    def get_fichas_por_sala(self, sala_id):
        cursor = self.__conn.cursor()
        cursor.execute("""
            SELECT "id", "sala_id", "nome_personagem", "vida", "energia", "armadura", "nivel", "xp", "cor", "especie", "arquetipo", "forca", "constituicao", "inteligencia", "destreza", "carisma", "combate", "atletismo", "tecnologia", "percepcao", "conhecimento", "pontaria", "furtividade", "atuacao", "iniciativa", "vida_atual", "energia_atual" FROM ficha
            WHERE sala_id = %s
        """, (sala_id,))
        return cursor.fetchall()

    def get_ficha_poderes(self, id):
        cursor = self.__conn.cursor(cursor_factory=DictCursor)
        cursor.execute(
            """
                SELECT 
                f.id, f.sala_id, f.nome_personagem, f.vida, f.energia, f.armadura, f.nivel, f.xp, f.cor, f.especie, f.arquetipo, f.forca, f.constituicao, f.inteligencia, f.destreza, f.carisma, f.combate, f.atletismo, f.tecnologia, f.percepcao, f.conhecimento, f.pontaria, f.furtividade, f.atuacao, f.iniciativa, f.vida_atual, f.energia_atual,
                p.id AS poder_id, p.nome AS poder_nome, p.descricao AS poder_descricao,
                e.id AS equipamento_id, e.nome AS equipamento_nome, e.tipo_arma, e.tipo_dano, e.efeito, e.dano
                FROM ficha AS f
                LEFT JOIN ficha_poder ON f.id = ficha_poder.ficha_id
                LEFT JOIN poder AS p ON ficha_poder.poder_id = p.id
                LEFT JOIN ficha_equipamento ON f.id = ficha_equipamento.ficha_id
                LEFT JOIN equipamento AS e ON ficha_equipamento.equipamento_id = e.id
                WHERE f.id = %s;
            """, (id,)
            )
        
        data = cursor.fetchall()
        cursor.close()
        return data