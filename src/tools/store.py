import sqlite3

from os import path, getcwd, chmod

from typing import Union

class Store:
    __DB_FILE_PATH = 'data/store.db'

    __INIT_SQL = '''
        CREATE TABLE cards (
            hash      text,
            url       text,
            title     text,
            price     integer,
            image_url text,

            UNIQUE (hash) ON CONFLICT REPLACE
        );
    '''

    __INSERT_SQL = '''
        INSERT INTO cards
        VALUES (:hash, :url, :title, :price, :image_url);
    '''

    __SELECT_SQL = '''
        SELECT
            url,
            title,
            price,
            image_url
        FROM cards
        WHERE hash = ?;
    '''

    __dbConnection = None

    def __init__(self):
        dbFilePath = self.__getDBFilePath()

        if not path.exists(dbFilePath) or not path.isfile(dbFilePath):
            self.__initStore()
            chmod(dbFilePath, 0o755)

    def getRowByHash(self, hash: str) -> Union[tuple, None]:
        if self.__dbConnection is None:
            self.__connect()

        cursor = self.__dbConnection.cursor()

        cursor.execute(self.__SELECT_SQL, (hash,))

        return cursor.fetchone()

    def insertRow(
        self,
        hash:     str,
        url:      str,
        title:    Union[str, None],
        price:    Union[int, None],
        imageUrl: Union[str, None]
    ) -> bool:
        if self.__dbConnection is None:
            self.__connect()

        cursor = self.__dbConnection.cursor()

        row = {
            'hash':      hash,
            'url':       url,
            'title':     str(title),
            'price':     price,
            'image_url': str(imageUrl)
        }

        cursor.execute(self.__INSERT_SQL, row)

        self.__dbConnection.commit()

        return True

    def close(self):
        if self.__dbConnection is not None:
            self.__dbConnection.close()
            self.__dbConnection = None

    def __connect(self):
        dbFilePath = self.__getDBFilePath()

        self.__dbConnection = sqlite3.connect(dbFilePath)

    def __getDBFilePath(self) -> str:
        return '%s/%s' % (getcwd(), self.__DB_FILE_PATH)

    def __initStore(self) -> str:
        if self.__dbConnection is None:
            self.__connect()

        cursor = self.__dbConnection.cursor()

        cursor.execute(self.__INIT_SQL)

        self.__dbConnection.commit()
