import sqlite3

AMV_PROPERTIES = {
    "video_id":0
    ,"video_title":1
    ,"primary_editor_username":2
    ,"addl_editors":3
    ,"studio":4
    ,"release_date":5
    ,"video_footage":6
    ,"song_artist":7
    ,"song_title":8
    ,"song_genre":9
    ,"tags_1":10
    ,"contests_entered":11
    ,"video_description":12
    ,"tags_2":13
    ,"tags_3":14
    ,"vid_thumb_path":15
    ,"play_count":16
    ,"local_file":17
    ,"favorite":18
    ,"my_rating":19
    ,"tags_4":20
    ,"tags_5":21
    ,"tags_6":22
}

class Amv(object):
    def __init__(self, rowData):
        self.rowData = rowData

    def getId(self) -> str:
        return self.rowData[0]
    def getTitle(self) -> str:
        return self.rowData[1]
    def getEditors(self) -> list:
        return [self.rowData[2]] if len(self.rowData[3]) == 0 else [self.rowData[2]] + self.rowData[3].split("; ")
    def getStudio(self) -> str:
        return self.rowData[4]
    def getReleaseDate(self) -> str:
        return self.rowData[5].replace("/", "-")
    def getGenres(self) -> list:
        return self.rowData[10].split("; ")
    def getSongArtist(self) -> str:
        return self.rowData[7]
    def getSongTitle(self) -> str:
        return self.rowData[8]
    def getSongGenre(self) -> str:
        return self.rowData[9]
    def getAnimes(self) -> list:
        return self.rowData[6].split("; ")
    def getContests(self) -> list:
        return self.rowData[11].split("\n")
    def getPlaycount(self) -> str:
        return self.rowData[16]
    def getThumbnailPath(self) -> str:
        return self.rowData[15]
    def isFavorite(self) -> bool:
        return self.rowData[18] == 1
    def getUserRating(self) -> float:
        return self.rowData[19]
    def getFilepath(self) -> str:
        return self.rowData[17]
    def getTag2(self) -> str:
        return self.rowData[13]
    def getTag3(self) -> str:
        return self.rowData[14]
    def getTag4(self) -> str:
        return self.rowData[20]
    def getTag5(self) -> str:
        return self.rowData[21]
    def getTag6(self) -> str:
        return self.rowData[22]
    

class AmvResultList(object):
    def __init__(self, rowList):
        self.rowList = rowList
        self.rowListIter = iter(self.rowList)

    def __iter__(self):
        return self
    
    def __next__(self) -> Amv:
        return Amv(next(self.rowListIter))

class AmvTrackerDao(object):
    dbFilePath = None

    def init(dbFilePath):
        AmvTrackerDao.dbFilePath = dbFilePath

    def getColumns():
        return ", ".join(AMV_PROPERTIES.keys())

    def getAmv(amvid: str) -> Amv:
        with sqlite3.connect(AmvTrackerDao.dbFilePath) as con:
            cur = con.cursor()
            res = cur.execute("SELECT " + AmvTrackerDao.getColumns() + " FROM sub_db_0 WHERE video_id = ?", [amvid])
            return Amv(res.fetchone())

    def getAllAmvs() -> AmvResultList:
        with sqlite3.connect(AmvTrackerDao.dbFilePath) as con:
            cur = con.cursor()
            res = cur.execute("SELECT " + AmvTrackerDao.getColumns() + " FROM sub_db_0 WHERE local_file <> ''")
            return AmvResultList(res.fetchall())

    def getAllFavorites() -> AmvResultList:
        with sqlite3.connect(AmvTrackerDao.dbFilePath) as con:
            cur = con.cursor()
            res = cur.execute("SELECT " + AmvTrackerDao.getColumns() + " FROM sub_db_0 WHERE local_file <> '' AND favorite = 1")
            return AmvResultList(res.fetchall())

    def getAllEditors():
        with sqlite3.connect(AmvTrackerDao.dbFilePath) as con:
            cur = con.cursor()
            res = cur.execute(
            """
            WITH RECURSIVE Splitter AS (
                SELECT
                    SUBSTR(addl_editors, 1, INSTR(addl_editors, '; ') - 1) AS part,
                    SUBSTR(addl_editors, INSTR(addl_editors, '; ') + 2) AS remainder
                FROM
                    sub_db_0
                WHERE addl_editors <> ''
                UNION ALL
                SELECT
                    SUBSTR(remainder, 1, INSTR(remainder, '; ') - 1) AS part,
                    SUBSTR(remainder, INSTR(remainder, '; ') + 2) AS remainder
                FROM
                    Splitter
                WHERE
                    remainder != ''
            )

            SELECT editor, COUNT(DISTINCT video_id) AS nbAmv
            FROM (
                SELECT DISTINCT part AS editor
                FROM Splitter
                WHERE part <> ''

                UNION

                SELECT DISTINCT(primary_editor_username) AS editor FROM sub_db_0
                )
            JOIN sub_db_0 ON local_file <> ''
                AND (primary_editor_username = editor
                    OR addl_editors = editor
                    OR addl_editors LIKE ("%; " || editor)
                    OR addl_editors LIKE (editor || "; %")
                    OR addl_editors LIKE ("%; " || editor || "; %"))
            GROUP BY editor
            """)
            return res.fetchall()
    
    def getEditorAmvs(editor: str) -> AmvResultList:
         with sqlite3.connect(AmvTrackerDao.dbFilePath) as con:
            cur = con.cursor()
            res = cur.execute(
            "SELECT " + AmvTrackerDao.getColumns() + """ FROM sub_db_0
            WHERE local_file <> '' 
                AND (primary_editor_username = ?
                    OR addl_editors = ?
                    OR addl_editors LIKE ?
                    OR addl_editors LIKE ?
                    OR addl_editors LIKE ?
                )
            """, [editor, editor, "%; "+editor, editor+"; %", "%; "+editor+"; %"])
            return AmvResultList(res.fetchall())

    def getStudios():
        with sqlite3.connect(AmvTrackerDao.dbFilePath) as con:
            cur = con.cursor()
            res = cur.execute("SELECT DISTINCT studio, COUNT(*) FROM sub_db_0 WHERE local_file <> '' GROUP BY studio")
            return res.fetchall()

    def getStudioAmvs(studio: str) -> AmvResultList:
        with sqlite3.connect(AmvTrackerDao.dbFilePath) as con:
            cur = con.cursor()
            res = cur.execute("SELECT " + AmvTrackerDao.getColumns() + " FROM sub_db_0 WHERE studio = ?", [studio])
            return AmvResultList(res.fetchall())
    
    def getGenres():
        with sqlite3.connect(AmvTrackerDao.dbFilePath) as con:
            cur = con.cursor()
            res = cur.execute(
            """
            SELECT DISTINCT tag_name, COUNT(DISTINCT video_id) FROM tags_1
            LEFT OUTER JOIN sub_db_0 ON local_file <> ''
                AND (tags_1 = LOWER(tag_name)
                    OR tags_1 LIKE ("%; " || LOWER(tag_name))
                    OR tags_1 LIKE (LOWER(tag_name) || "; %")
                    OR tags_1 LIKE ("%; " || LOWER(tag_name) || "; %")
                )
            GROUP BY tag_name
            ORDER BY sort_order
            """)
            return res.fetchall()

    def getGenreAmvs(genre: str) -> AmvResultList:
        with sqlite3.connect(AmvTrackerDao.dbFilePath) as con:
            cur = con.cursor()
            res = cur.execute("SELECT " + AmvTrackerDao.getColumns() + """ FROM sub_db_0 
            WHERE local_file <> ''
                AND (tags_1 = LOWER(?)
                    OR tags_1 LIKE ("%; " || LOWER(?))
                    OR tags_1 LIKE (LOWER(?) || "; %")
                    OR tags_1 LIKE ("%; " || LOWER(?) || "; %")
                )""", [genre, genre, genre, genre])
            return AmvResultList(res.fetchall())

    def getYears():
        with sqlite3.connect(AmvTrackerDao.dbFilePath) as con:
            cur = con.cursor()
            res = cur.execute(
            """
            SELECT DISTINCT SUBSTR(release_date, 1, 4), COUNT(*) FROM sub_db_0 
            WHERE local_file <> '' AND SUBSTR(release_date, 1, 4) <> ''
            GROUP BY SUBSTR(release_date, 1, 4)
            """)
            return res.fetchall()

    def getYearAmvs(year: str) -> AmvResultList:
        with sqlite3.connect(AmvTrackerDao.dbFilePath) as con:
            cur = con.cursor()
            res = cur.execute("SELECT " + AmvTrackerDao.getColumns() + " FROM sub_db_0 WHERE SUBSTR(release_date, 1, 4) = ? AND local_file <> ''", [year,])
            return AmvResultList(res.fetchall())

    def getContests():
        with sqlite3.connect(AmvTrackerDao.dbFilePath) as con:
            contestSet = list()
            resultList = list()
            cur = con.cursor()
            res = cur.execute("SELECT contests_entered FROM sub_db_0 WHERE contests_entered <> '' AND local_file <> ''")
            rowlist = res.fetchall()
            for row in rowlist:
                for contest in row[0].split("\n"):
                    if not contest in contestSet:
                        contestSet.append(contest)
                        res2 = cur.execute("SELECT COUNT(DISTINCT video_id) FROM sub_db_0 \
                        WHERE local_file <> '' \
                            AND (contests_entered = ? \
	                            OR contests_entered LIKE (? || char(0x0a) || \"%\") \
	                            OR contests_entered LIKE (\"%\" || char(0x0a) || ?) \
	                            OR contests_entered LIKE (\"%\" || char(0x0a) || ? || char(0x0a) || \"%\"))"
                        , [contest, contest, contest, contest])
                        amvCount = res2.fetchone()[0]
                        resultList.append((contest, amvCount))
            return resultList

    def getContestAmvs(contest: str) -> AmvResultList:
        with sqlite3.connect(AmvTrackerDao.dbFilePath) as con:
            cur = con.cursor()
            res = cur.execute("SELECT " + AmvTrackerDao.getColumns() + " FROM sub_db_0 \
                WHERE local_file <> '' \
                    AND (contests_entered = ? \
                        OR contests_entered LIKE (? || char(0x0a) || \"%\") \
                        OR contests_entered LIKE (\"%\" || char(0x0a) || ?) \
                        OR contests_entered LIKE (\"%\" || char(0x0a) || ? || char(0x0a) || \"%\"))"
                , [contest, contest, contest, contest])
            return AmvResultList(res.fetchall())

    def getAnimes() -> list:
        with sqlite3.connect(AmvTrackerDao.dbFilePath) as con:
            animeSet = list()
            resultList = list()
            cur = con.cursor()
            res = cur.execute("SELECT video_footage FROM sub_db_0 WHERE video_footage <> '' AND local_file <> ''")
            rowlist = res.fetchall()
            for row in rowlist:
                for anime in row[0].split("; "):
                    if not anime in animeSet:
                        animeSet.append(anime)
                        res2 = cur.execute(
                        """SELECT COUNT(DISTINCT video_id) FROM sub_db_0
                        WHERE local_file <> ''
                            AND ( video_footage = ?
                                OR video_footage LIKE ("%; " || ?)
                                OR video_footage LIKE (? || "; %")
                                OR video_footage LIKE ("%; " || ? || "; %"))
                        """, [anime, anime, anime, anime])
                        amvCount = res2.fetchone()[0]
                        resultList.append((anime, amvCount))
            return resultList
    
    def getAnimeAmvs(anime: str) -> AmvResultList:
        with sqlite3.connect(AmvTrackerDao.dbFilePath) as con:
            cur = con.cursor()
            res = cur.execute(
            "SELECT " + AmvTrackerDao.getColumns() + """ FROM sub_db_0
            WHERE local_file <> ''
                AND ( video_footage = ?
                    OR video_footage LIKE ("%; " || ?)
                    OR video_footage LIKE (? || "; %")
                    OR video_footage LIKE ("%; " || ? || "; %"))
            """, [anime, anime, anime, anime])
            return AmvResultList(res.fetchall())

    def getArtists():
        with sqlite3.connect(AmvTrackerDao.dbFilePath) as con:
            cur = con.cursor()
            res = cur.execute("SELECT DISTINCT song_artist, COUNT(*) FROM sub_db_0 WHERE local_file <> '' GROUP BY song_artist")
            return res.fetchall()

    def getArtistAmvs(artist: str) -> AmvResultList:
        with sqlite3.connect(AmvTrackerDao.dbFilePath) as con:
            cur = con.cursor()
            res = cur.execute("SELECT " + AmvTrackerDao.getColumns() + " FROM sub_db_0 WHERE song_artist = ?", [artist])
            return AmvResultList(res.fetchall())

    def getSongGenres():
        with sqlite3.connect(AmvTrackerDao.dbFilePath) as con:
            cur = con.cursor()
            res = cur.execute("SELECT DISTINCT song_genre, COUNT(*) FROM sub_db_0 WHERE local_file <> '' GROUP BY song_genre")
            return res.fetchall()

    def getSongGenreAmvs(genre: str) -> AmvResultList:
        with sqlite3.connect(AmvTrackerDao.dbFilePath) as con:
            cur = con.cursor()
            res = cur.execute("SELECT " + AmvTrackerDao.getColumns() + " FROM sub_db_0 WHERE song_genre = ?", [genre])
            return AmvResultList(res.fetchall())

    def getAllCustomLists():
        with sqlite3.connect(AmvTrackerDao.dbFilePath) as con:
            cur = con.cursor()
            res = cur.execute(
            """
            SELECT list_name
                ,CASE WHEN vid_ids = '' THEN 0
                    ELSE LENGTH(vid_ids) - LENGTH(REPLACE(vid_ids, ";", "")) + 1
                    END AS amvCount
            FROM custom_lists
            """)
            return res.fetchall()

    def getCustomListsWithAmv(amvId: str):
        with sqlite3.connect(AmvTrackerDao.dbFilePath) as con:
            cur = con.cursor()
            res = cur.execute("SELECT list_name FROM custom_lists WHERE vid_ids LIKE ?", ["%"+amvId+"%"])
            return res.fetchall()

    def getCustomListsWithoutAmv(amvId: str):
        with sqlite3.connect(AmvTrackerDao.dbFilePath) as con:
            cur = con.cursor()
            res = cur.execute("SELECT list_name FROM custom_lists WHERE NOT vid_ids LIKE ?", ["%"+amvId+"%"])
            return res.fetchall()

    def getCustomListAmvs(listName: str) -> AmvResultList:
        with sqlite3.connect(AmvTrackerDao.dbFilePath) as con:
            cur = con.cursor()
            res = cur.execute("SELECT vid_ids FROM custom_lists WHERE list_name = ?", [listName])
            row = res.fetchone()
            amvIds = row[0].split("; ")
            res2 = cur.execute("SELECT " + AmvTrackerDao.getColumns() + " FROM sub_db_0 WHERE video_id IN ('" + "','".join(amvIds) + "')")
            return AmvResultList(res2.fetchall())

    def getTagName(tagId: int) -> str:
        with sqlite3.connect(AmvTrackerDao.dbFilePath) as con:
            cur = con.cursor()
            res = cur.execute("SELECT user_field_name FROM tags_lookup WHERE internal_field_name = ? AND in_use = 1", ["tags_"+str(tagId)])
            row = res.fetchone()
            if row is not None and len(row) > 0:
                return row[0]
            else:
                return ""
    
    def getTagList(tagId: int) -> list:
        strTagNum = str(tagId)
        resultList = list()
        with sqlite3.connect(AmvTrackerDao.dbFilePath) as con:
            cur = con.cursor()
            res = cur.execute("SELECT tag_name FROM tags_"+strTagNum)
            rowlist = res.fetchall()
            for row in rowlist:
                tagName = row[0].lower()
                res2 = cur.execute("SELECT COUNT(DISTINCT video_id) FROM sub_db_0 \
                    WHERE local_file <> '' \
                    AND ( tags_"+strTagNum+" = ? \
                        OR tags_"+strTagNum+" LIKE ('%; ' || ?) \
                        OR tags_"+strTagNum+" LIKE (? || '; %') \
                        OR tags_"+strTagNum+" LIKE ('%; ' || ? || '; %')) "
                    , [tagName, tagName, tagName, tagName])
                amvCount = res2.fetchone()[0]
                resultList.append((row[0], amvCount))
            return resultList
    
    def getTagAmvs(tagId: int, tagName: str) -> AmvResultList:
        strTagNum = str(tagId)
        tagName = tagName.lower()
        with sqlite3.connect(AmvTrackerDao.dbFilePath) as con:
            cur = con.cursor()
            res = cur.execute(
                "SELECT "+ AmvTrackerDao.getColumns() +" FROM sub_db_0 \
                WHERE local_file <> '' \
                    AND ( tags_"+strTagNum+" = ? \
                        OR tags_"+strTagNum+" LIKE ('%; ' || ?) \
                        OR tags_"+strTagNum+" LIKE (? || '; %') \
                        OR tags_"+strTagNum+" LIKE ('%; ' || ? || '; %')) "
                ,[tagName, tagName, tagName, tagName])
            return AmvResultList(res.fetchall())

    def addToCustomList(amvId: str, listName: str):
        with sqlite3.connect(AmvTrackerDao.dbFilePath) as con:
            cur = con.cursor()
            res = cur.execute("SELECT vid_ids FROM custom_lists WHERE list_name = ?", [listName])
            row = res.fetchone()
            amvIds = row[0].split("; ")
            if not amvId in amvIds:
                amvIds.append(amvId)
                cur.execute("UPDATE custom_lists SET vid_ids = ? WHERE list_name = ?", ["; ".join(amvIds), listName])

    def removeFromCustomList(amvId: str, listName: str):
        with sqlite3.connect(AmvTrackerDao.dbFilePath) as con:
            cur = con.cursor()
            res = cur.execute("SELECT vid_ids FROM custom_lists WHERE list_name = ?", [listName])
            row = res.fetchone()
            amvIds = row[0].split("; ")
            if amvId in amvIds:
                amvIds.remove(amvId)
                cur.execute("UPDATE custom_lists SET vid_ids = ? WHERE list_name = ?", ["; ".join(amvIds), listName])

    def addAmvToFavorites(amvId: str):
        with sqlite3.connect(AmvTrackerDao.dbFilePath) as con:
            cur = con.cursor()
            cur.execute("UPDATE sub_db_0 SET favorite = 1 WHERE video_id = ?", [amvId])
    def removeAmvFromFavorites(amvId: str):
        with sqlite3.connect(AmvTrackerDao.dbFilePath) as con:
            cur = con.cursor()
            cur.execute("UPDATE sub_db_0 SET favorite = 0 WHERE video_id = ?", [amvId])
    
    def setRating(amvId: str, rating: float):
        with sqlite3.connect(AmvTrackerDao.dbFilePath) as con:
            cur = con.cursor()
            cur.execute("UPDATE sub_db_0 SET my_rating = ? WHERE video_id = ?", [rating, amvId])

    def incrementPlaycount(amvId: str):
        with sqlite3.connect(AmvTrackerDao.dbFilePath) as con:
            cur = con.cursor()
            cur.execute("UPDATE sub_db_0 SET play_count = play_count + 1 WHERE video_id = ?", [amvId])