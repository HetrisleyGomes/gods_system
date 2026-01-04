import uuid

class UtilsController:
    def __init__(self, repository):
        self.__repository = repository
    
    def get_poder(self, id):
        try:
            cursor = self.__repository.get_poder(id)
            data = self.format_poderes(cursor, True)
            return {
                "body": data, "status": 200,
            }
        except Exception as e:
            return {
                "body": str(e), "status": 400,
            }
    
    def get_all_poderes(self):
        try:
            cursor = self.__repository.get_all_poderes()
            data = self.format_poderes(cursor)
            return {
                "body": data, "status": 200,
            }
        except Exception as e:
            return {
                "body": str(e), "status": 400,
            }
        
    def set_ficha_poder(self, ficha_id, poder_id):
        try:
            self.__repository.set_ficha_poder(ficha_id, poder_id)
            return {
                "body": True, "status": 200,
            }
        except Exception as e:
            return {
                "body": str(e), "status": 400,
            }
    
    def remove_ficha_poder(self, ficha_id, poder_id):
        try:
            self.__repository.remove_ficha_poder(ficha_id, poder_id)
            return {
                "body": True, "status": 200,
            }
        except Exception as e:
            return {
                "body": str(e), "status": 400,
            }
    
    def get_equipamento(self, id):
        try:
            cursor = self.__repository.get_equipamento(id)
            data = self.format_equipamentos(cursor, True)
            return {
                "body": data, "status": 200,
            }
        except Exception as e:
            return {
                "body": str(e), "status": 400,
            }
    
    def get_all_equipamentos(self):
        try:
            cursor = self.__repository.get_all_equipamentos()
            data = self.format_equipamentos(cursor)
            return {
                "body": data, "status": 200,
            }
        except Exception as e:
            return {
                "body": str(e), "status": 400,
            }
    
    def set_ficha_equipamento(self, ficha_id, equipamento_id):
        try:
            self.__repository.set_ficha_equipamento(ficha_id, equipamento_id)
            return {
                "body": True, "status": 200,
            }
        except Exception as e:
            return {
                "body": str(e), "status": 400,
            }
    
    def remove_ficha_equipamento(self, ficha_id, equipamento_id):
        try:
            self.__repository.remove_ficha_equipamento(ficha_id, equipamento_id)
            return {
                "body": True, "status": 200,
            }
        except Exception as e:
            return {
                "body": str(e), "status": 400,
            }
    
    def format_equipamentos(self, raw, single=False):
        keys = ["id", "nome", "tipo_arma", "tipo_dano", "efeito", "dano"]
        if single:
            return dict(zip(keys, raw))
        else:
            data = [
                dict(zip(keys, row))
                for row in raw
            ]
        return data
    
    def format_poderes(self, raw, single=False):
        keys = ["id", "nome", "descricao"]
        if single:
            return dict(zip(keys, raw))
        else:
            data = [
                dict(zip(keys, row))
                for row in raw
            ]
        return data