import uuid

class SalaController:
    def __init__(self, repository):
        self.__repository = repository

    def create(self, body):
        try:
            body = {
                "id": str(uuid.uuid4()),
                "nome": body["nome"],
                "codigo": body["codigo"],
                "senha": body["senha"],
            }
            self.__repository.set_sala(body)

            return {
                "body": True, "status": 200,
            }
        except Exception as e:
            return {
                "body": str(e), "status": 400,
            }

    def get_sala(self, id):
        try:
            raw = self.__repository.get_sala_by_id(id)
            keys = ["id", "codigo", "nome", "senha", "notes"]

            data = dict(zip(keys, raw))
            
            return {
                "body": data, "status": 200,
            }
        except Exception as e:
            return {
                "body": str(e), "status": 400,
            }

    def get_salas(self):
        try:
            raw = self.__repository.get_salas()
            keys = ["id", "codigo", "nome", "senha"]

            data = [
                dict(zip(keys, row))
                for row in raw
            ]
            return {
                "body": data, "status": 200,
            }
        except Exception as e:
            return {
                "body": str(e), "status": 400,
            }
        
    def set_ficha(self, id, id_ficha):
        try:
            self.__repository.set_ficha(id, id_ficha)
            return {
                "body": True, "status": 200,
            }
        except Exception as e:
            return {
                "body": str(e), "status": 400,
            }

    def remove_ficha(self, id):
        try:
            self.__repository.remove_ficha(id)
            return {
                "body": True, "status": 200,
            }
        except Exception as e:
            return {
                "body": str(e), "status": 400,
            }
    
    def get_notes(self, id):
        try:
            raw = self.__repository.get_notes(id)
            return {
                "body": raw, "status": 200,
            }
        except Exception as e:
            return {
                "body": str(e), "status": 400,
            }
    
    def set_notes(self, id, notes):
        try:
            raw = self.__repository.set_notes(id, notes)
            return {
                "body": raw, "status": 200,
            }
        except Exception as e:
            return {
                "body": str(e), "status": 400,
            }