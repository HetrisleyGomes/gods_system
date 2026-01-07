import uuid

class FichaController:
    def __init__(self, repository):
        self.__repository = repository

    def create(self, ficha):
        try:
            id = str(uuid.uuid4())
            ficha["id"] = id
            self.__repository.set_ficha(ficha)
            return {
                "body": id,
                "status": 200,
            }
        except Exception as e:
            return {
                "body": str(e),
                "status": 400,
            }

    def get_ficha(self, id):
        try:
            cursor = self.__repository.get_ficha(id)
            data = self.dict_convert(cursor, True)
            return {
                "body": data, "status": 200,
            }
        except Exception as e:
            return {
                "body": str(e), "status": 400,
            }

    def get_fichas(self):
        try:
            cursor = self.__repository.get_all_fichas()
            data = self.dict_convert(cursor)
            return {
                "body": data, "status": 200,
            }
        except Exception as e:
            return {
                "body": str(e), "status": 400,
            }

    def edit_ficha(self, id, ficha):
        try:
            self.__repository.edit_ficha(id, ficha)
            return {
                "body": True, "status": 200,
            }
        except Exception as e:
            return {
                "body": str(e), "status": 400,
            }
        
    def set_vida(self, id, valor):
        try:
            self.__repository.set_vida(id, valor)
            return {
                "body": True, "status": 200,
            }
        except Exception as e:
            return {
                "body": str(e), "status": 400,
            }
    
    def set_energia(self, id, valor):
        try:
            self.__repository.set_energia(id, valor)
            return {
                "body": True, "status": 200,
            }
        except Exception as e:
            return {
                "body": str(e), "status": 400,
            }

    def delete_ficha(self, id):
        try:
            self.__repository.delete_ficha(id)
            return {
                "body": True, "status": 200,
            }
        except Exception as e:
            return {
                "body": str(e), "status": 400,
            }
    
    def get_fichas_por_sala(self, sala_id):
        try:
            cursor = self.__repository.get_fichas_por_sala(sala_id)
            data = self.dict_convert(cursor)
            return {
                "body": data, "status": 200,
            }
        except Exception as e:
            return {
                "body": str(e), "status": 400,
            }
        
    def get_ficha_tudo(self, id):
        try:
            rows = self.__repository.get_ficha_poderes(id)
            data = {
                "id": rows[0][0],
                "sala_id": rows[0][1],
                "nome_personagem": rows[0][2],
                "vida": rows[0][3],
                "energia": rows[0][4],
                "armadura": rows[0][5],
                "nivel": rows[0][6],
                "xp": rows[0][7],
                "cor": rows[0][8],
                "especie": rows[0][9],
                "arquetipo": rows[0][10],
                "forca": rows[0][11],
                "constituicao": rows[0][12],
                "inteligencia": rows[0][13],
                "destreza": rows[0][14],
                "carisma": rows[0][15],
                "combate": rows[0][16],
                "atletismo": rows[0][17],
                "tecnologia": rows[0][18],
                "percepcao": rows[0][19],
                "conhecimento": rows[0][20],
                "pontaria": rows[0][21],
                "furtividade": rows[0][22],
                "atuacao": rows[0][23],
                "iniciativa": rows[0][24],
                "vida_atual": rows[0][25],
                "energia_atual": rows[0][26],
                "poderes": [],
                "equipamentos": []
            }
            equipamentos_ids = []
            poderes_ids = []

            for row in rows:
                if row[27] is not None and row[27] not in poderes_ids:
                    poderes_ids.append(row[27])
                    data["poderes"].append({
                        "id": row[27],
                        "nome": row[28],
                        "descricao": row[29]
                    })
            
            for row in rows:
                if row[30] is not None and row[30] not in equipamentos_ids:
                    equipamentos_ids.append(row[30])
                    data["equipamentos"].append({
                        "id": row[30],
                        "nome": row[31],
                        "tipo_arma": row[32],
                        "tipo_dano": row[33],
                        "efeito": row[34],
                        "dano": row[35]
                    })

            return {
                "body": data, "status": 200,
            }
        except Exception as e:
            return {
                "body": str(e), "status": 400,
            }
    

    def dict_convert(self, raw, single=False):
        keys = ["id", "sala_id", "nome_personagem", "vida", "energia", "armadura", "nivel", "xp", "cor", "especie", "arquetipo", "forca", "constituicao", "inteligencia", "destreza", "carisma", "combate", "atletismo", "tecnologia", "percepcao", "conhecimento", "pontaria", "furtividade", "atuacao", "iniciativa", "vida_atual", "energia_atual"]
        if single:
            return dict(zip(keys, raw))
        else:
            data = [
                dict(zip(keys, row))
                for row in raw
            ]
        return data