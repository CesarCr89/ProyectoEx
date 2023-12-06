import pymysql

class BD:
    _instancia = None
    conn = ""
    cursor = ""
    def __new__(cls):
        if cls._instancia is None:
            cls._instancia = super(BD, cls).__new__(cls)
        return cls._instancia

    def connect(self):
        try:
            self.conn=pymysql.connect(
            host='localhost',
            port=3305,
            user='root',
            password='12345',  # ¡Asegúrate de que la contraseña sea correcta!
            db='sitio'
                                    )
            self.cursor=self.conn.cursor()
        except  Exception as e:
            print(e)

    def close(self):
        try:
            self.cursor.close()
            self.conn.close()
        except Exception as e:
            print(e)

if __name__ == "__main__":
    bd = BD()