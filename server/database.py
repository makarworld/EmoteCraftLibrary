from typing import *
from mwsqlite import MWBase, Row
from mwsqlite.utils import tuple_to_dict
from loguru import logger 


try:
    from .utils import Singleton
except:
    from utils import Singleton

class ManageDB(Singleton):
    def __init__(self):
        self.base = MWBase(
            filename = "emotes.db",
            tables = {
                'emotes': {
                    'name':        str,
                    'lname':       str,
                    'author':      str,
                    'description': str,
                    'uuid':        str,
                    'tag':         str,
                    'degrees':     bool,
                    'nsfw':        bool,
                    'loop':        bool
                },
                "categories": {
                    "name": str
                },
                "tags": {
                    "name": str
                },
                "emotes_tags": {
                    "eid": int,
                    "tid": int
                },
                "emotes_categories": {
                    "eid": int,
                    "cid": int
                }
            }
        )
        self.return_values = ["name", "author", "description", "uuid", "tag", "nsfw"]
        self.return_valuesf = ', '.join(self.return_values)
        
    
    def eid_to_row(self, eids: List[int]) -> List[Row]:
        results = self.base.emotes.execute(
            cmd      = "SELECT {} FROM emotes WHERE id IN ({})".format(self.return_valuesf, ",".join(["?"] * len(eids))),
            values   = eids if [isinstance(eids, list) or isinstance(eids, tuple)] else [eids],
            fetchall = True
        )
        return self._tuples_to_row_emote(results)
    
    def _tuples_to_row_emote(self, tuples: Tuple) -> Row:
        resp = []
        for _tuple in tuples:
            resp.append(Row(self, **tuple_to_dict(_tuple, {col: v for col, v in self.base.emotes.columns.items() if col in self.return_values})))
        return resp

    def _category_to_cid(self, categories: List[int]) -> List[Row]:
        if not categories: return []

        result = self.base.emotes_categories.execute(
            cmd      = "SELECT id FROM categories WHERE name IN ({})".format(",".join(["?"] * len(categories))),
            values   = categories if [isinstance(categories, list) or isinstance(categories, tuple)] else [categories],
            fetchall = True
        )
        if result:
            # [(), ()] to []
            result = [x[0] for x in set(result)]

        return result
    
    def _tags_to_tid(self, tags: List[int]) -> List[Row]:
        if not tags: return []
        result = self.base.emotes_categories.execute(
            cmd      = "SELECT id FROM tags WHERE name IN ({})".format(",".join(["?"] * len(tags))),
            values   = tags if [isinstance(tags, list) or isinstance(tags, tuple)] else [tags],
            fetchall = True
        )
        if result:
            # [(), ()] to []
            result = [x[0] for x in set(result)]

        return result


    def _search_query(self, query: str, eids: List[int] = None, limit: int = 30, offset: int = 0) -> List[int]:
        query = query.lower()
        if eids:
            result = self.base.emotes.execute(
                cmd      = "SELECT id FROM emotes WHERE lname LIKE ? AND id IN ({}) LIMIT ? OFFSET ?".format(",".join(["?"] * len(eids))),
                values   = [query] + list(eids) + [limit, offset],
                fetchall = True
            )
        else:
            result = self.base.emotes.execute(
                cmd      = "SELECT id FROM emotes WHERE lname LIKE ? LIMIT ? OFFSET ?",
                values   = [query, limit, offset],
                fetchall = True
            )
        if result:
            # [(), ()] to []
            result = [x[0] for x in set(result)]

        return result
    
    def _search_authors(self, authors: list, eids: List[int] = None, limit: int = 30, offset: int = 0) -> List[int]:
        if eids:
            result = self.base.emotes.execute(
                cmd      = "SELECT id FROM emotes WHERE author IN ({}) AND id IN ({}) LIMIT ? OFFSET ?".format(",".join(["?"] * len(authors)), ",".join(["?"] * len(eids))),
                values   = authors + list(eids) + [limit, offset],
                fetchall = True
            )
        else:
            result = self.base.emotes.execute(
                cmd      = "SELECT id FROM emotes WHERE author IN ({}) LIMIT ? OFFSET ?".format(",".join(["?"] * len(authors))),
                values   = authors + [limit, offset],
                fetchall = True
            )

        if result:
            # [(), ()] to []
            result = [x[0] for x in set(result)]

        return result

    def _search_tags(self, tags: list, eids: List[int] = None, limit: int = 30, offset: int = 0) -> List[int]:
        if eids:
            result = self.base.emotes_tags.execute(
                #"SELECT eid FROM emotes_tags WHERE tid IN ({}) AND eid IN ({})".format(",".join(["?"] * len(tags)), ",".join(["?"] * len(eids))),
                cmd      = ("SELECT emotes.id, emotes.name FROM emotes "
                            "INNER JOIN emotes_tags ON emotes.id = emotes_tags.eid "
                            "INNER JOIN tags ON emotes_tags.tid = tags.id "
                            "WHERE tags.name IN ({}) AND tags.eid IN ({}) "
                            "GROUP BY emotes.id, emotes.name "
                            "HAVING COUNT(*) = ? "
                            "LIMIT ? OFFSET ?").format(
                                    ",".join(["?"] * len(tags)), 
                                    ",".join(["?"] * len(eids))),

                values   = list(set(tags)) + list(eids) + [len(tags), limit, offset],
                fetchall = True
            )
        else:
            result = self.base.emotes_tags.execute(
                cmd      = ("SELECT emotes.id, emotes.name FROM emotes "
                            "INNER JOIN emotes_tags ON emotes.id = emotes_tags.eid "
                            "INNER JOIN tags ON emotes_tags.tid = tags.id "
                            "WHERE tags.name IN ({}) "
                            "GROUP BY emotes.id, emotes.name "
                            "HAVING COUNT(*) = ? "
                            "LIMIT ? OFFSET ?").format(
                                    ",".join(["?"] * len(tags))),
                values   = list(set(tags)) + [len(tags), limit, offset], # [[x, y] for x, y in zip(a, b)]
                fetchall = True
            )
        if result:
            # [(), ()] to []
            result = [x[0] for x in set(result)]

        return result


    def _search_categories(self, categories: list, eids: List[int] = None, limit: int = 30, offset: int = 0) -> List[int]:
        if eids:
            result = self.base.emotes_categories.execute(
                #cmd      = "SELECT eid FROM emotes_categories WHERE cid IN ({}) AND eid IN ({})".format(",".join(["?"] * len(categories)), ",".join(["?"] * len(eids))),
                cmd      = ("SELECT emotes.id, emotes.name FROM emotes "
                            "INNER JOIN emotes_categories ON emotes.id = emotes_categories.eid "
                            "INNER JOIN categories ON emotes_categories.cid = emotes_categories.id "
                            "WHERE categories.name IN ({}) AND categories.eid IN ({}) "
                            "GROUP BY emotes.id, emotes.name "
                            "HAVING COUNT(*) = ? "
                            "LIMIT ? OFFSET ?").format(
                                    ",".join(["?"] * len(categories)), 
                                    ",".join(["?"] * len(eids))), 
                values   = list(set(categories)) + list(eids) + [len(categories), limit, offset],
                fetchall = True
            )
        else:
            result = self.base.emotes_categories.execute(
                cmd      = ("SELECT emotes.id, emotes.name FROM emotes "
                            "INNER JOIN emotes_categories ON emotes.id = emotes_categories.eid "
                            "INNER JOIN categories ON emotes_categories.cid = categories.id "
                            "WHERE categories.name IN ({}) "
                            "GROUP BY emotes.id, emotes.name "
                            "HAVING COUNT(*) = ? "
                            "LIMIT ? OFFSET ?").format(
                                    ",".join(["?"] * len(categories))), 
                values   = list(set(categories)) + [len(categories), limit, offset],
                fetchall = True
            )
        if result:
            # [(), ()] to []
            result = [x[0] for x in set(result)]

        return result


    def search(self, 
               query: str = None, 
               authors: list = [],
               categories: list = [], 
               tags: list = [], 
               page: int = 1,
               limit: int = 30) -> List[Row]:
        limit = limit
        offset = (page - 1) * limit

        if (not query
            and not authors
            and not categories
            and not tags):

            return self._tuples_to_row_emote(
                self.base.emotes.execute("SELECT {} FROM emotes LIMIT ? OFFSET ?".format(self.return_valuesf), (limit, offset), fetchall=True
            ))
        
        result     = None
        query      = f"%{query}%" if query                       else None
        authors    = [authors]    if isinstance(authors, str)    else authors
        categories = [categories] if isinstance(categories, str) else categories
        tags       = [tags]       if isinstance(tags, str)       else tags

        for variant, value in [
                               ["authors",    authors],
                               ["query",      query], 
                               ["categories", categories], 
                               ["tags",       tags]]:
            if value:
                result = self.__getattribute__(f"_search_{variant}")(value, result, limit=limit, offset=offset) 
                if not result: return []
                logger.info(f"{variant} - {result}")

        if result:
            # eids to rows
            result = self.eid_to_row(result)

        return result


if __name__ == "__main__":
    db = ManageDB()

    #result = db.search(
    #    authors = ["SPEmotes"],
    #    categories = db._category_to_cid(["RUN"]),  
    #    tags = db._tags_to_tid(["JUMP"])
    #)
    #for s in result:
    #    print(s)



    names = ("Куроко", "Писи", "Пуки", "Каки", "Какашечки", "Попки", "Жопки", "Писечные Мышцы", "Чебоксар", "Маслёнок")
    authors = ("SPEmotes", "ЗАРАЗЕН", "ЗАРАЗЕН", "SPEmotes", "Милян", "Милян", "говно", "говно", "говно", "говно")
    for i in range(10):
        db.base.emotes.add(
            name        = names[i],
            lname       = names[i].lower(),
            author      = authors[i],
            description = "test",
            uuid        = "test",
            tag         = "test",
            path        = "test",
            image       = "test",
            gif         = "test",
            nsfw        = True
        )