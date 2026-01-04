import uuid
import json

class MechaController:
    def __init__(self, repository):
        self.__repository = repository

    def set_mecha(self, mecha):
        try:
            self.__repository.set_mecha(mecha)
            
            return {
                "body": mecha["id"], "status": 200,
            }
        except Exception as e:
            return {
                "body": str(e), "status": 400,
            }
    
    def get_mecha(self, id):
        try:
            cursor = self.__repository.get_mecha(id)
            data = self.format_mechas(cursor)
            return {
                "body": data, "status": 200,
            }
        except Exception as e:
            return {
                "body": str(e), "status": 400,
            }
    
    def get_mecha_by_ficha_id(self, id):
        try:
            cursor = self.__repository.get_mecha_by_ficha_id(id)
            data = self.format_mechas(cursor)
            return {
                "body": data, "status": 200,
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
    
    def edit_mecha(self, id, mecha):
        try:
            self.__repository.edit_mecha(id, mecha)

            return {
                "body": True, "status": 200,
            }
        except Exception as e:
            return {
                "body": str(e), "status": 400,
            }
        
    def delete_mecha(self, id):
        try:
            self.__repository.delete_mecha(id)
            return {
                "body": True, "status": 200,
            }
        except Exception as e:
            return {
                "body": str(e), "status": 400,
            }
        
    def format_mechas(self, raw):
        keys = ["id", "nome", "ficha_id", "vida", "vida_atual", "armadura", "combate", "pontaria", "defesa", "forca", "habilidades", "armas"]

        data = dict(zip(keys, raw))

        # Desserializa JSON
        data["armas"] = json.loads(data["armas"]) if data["armas"] else []
        data["habilidades"] = json.loads(data["habilidades"]) if data["habilidades"] else []

        return data
#(1, 'Emperor Rex', 100, 8, 3, 3, 3, 3, '["C\\u00e9lere: Equipado com propulsores. Aumentando velocidade e permitindo esquivas.", "Tra\\u00e7\\u00e3o Motora: A pot\\u00eancia de seu zord \\u00e9 aprimorada, permitindo uma melhor movimenta\\u00e7\\u00e3o, consumindo 2 pontos de energia, voc\\u00ea recebe +3 em a\\u00e7\\u00f5es f\\u00edsicas e Imunidade a controle coletivo."]', '07110f59-18fe-4d73-a7aa-1e6e0ddd4fd9', '[{"nome": "Presas de metal", "dano": "2d8", "tipo": "Perfurante", "efeito": "Cr\\u00edtico: Uma rolagem cr\\u00edtica de ataque dobra o resultado do dano."}]')