from openpyxl import load_workbook
from openpyxl.worksheet.worksheet import Worksheet

bd = load_workbook("base.xlsx")
sticker_page: Worksheet = bd["stickers"]
print(type(sticker_page) == Worksheet)


def print_table(page: str = "stickers"):
    for key, val, ans in bd[page].values:
        print(str(key).ljust(20), str(val).ljust(80), str(ans))


def get_stickers(sticker_name: str = None, page: str = "stickers"):
    db = load_workbook("base.xlsx")
    return get_stickers(page=page).get(sticker_name, None)\
        if sticker_name \
        else {key: val for key, *val in db[page].values}


def about_sheet(table: Worksheet = bd["stickers"]):
    print("_" * 10 + "about".ljust(90, "_"))
    print("max_row:".ljust(20) + str(table.max_row))
    print("max_column:".ljust(20) + str(table.max_column))
    print("_" * 100)


def insert_sticker(keyword, sticker, answer):
    row = sticker_page.max_row + 1
    sticker_page.cell(row=row, column=1).value = keyword
    sticker_page.cell(row=row, column=2).value = sticker
    sticker_page.cell(row=row, column=3).value = answer
    bd.save("base.xlsx")


class DB:
    def __init__(self):
        self.route = "base.xlsx"

    def users(self):
        db = load_workbook(self.route)
        page = db["users"]
        user_dict = {
            key: {
                "name": name,
                "sex": sex,
                "grade": grade
            }
            for key, name, sex, grade
            in page.values
        }
        db.close()
        return user_dict

    def new_user(self, user: list):
        db = load_workbook(self.route)
        page = db["users"]
        row = page.max_row + 1
        for col, val in enumerate(user):
            page.cell(row=row, column=col+1).value = val
        db.save(self.route)
        db.close()

    def stickers(self):
        db = load_workbook(self.route)
        page = db["stickers"]
        stickers_dict = {
            file_unique_id: {
                "file_id": file_id,
                "keyword": keyword,
                "answer": answer
            }
            for keyword, file_id, answer, file_unique_id
            in page.values
        }
        db.close()
        return stickers_dict

    def new_sticker(self, keyword: str, file_id: str, answer: str, file_unique_id: str):
        db = load_workbook(self.route)
        page: Worksheet = db["stickers"]
        cell = page.cell
        row = page.max_row + 1
        cell(row, 1).value = keyword
        cell(row, 2).value = file_id
        cell(row, 3).value = answer
        cell(row, 4).value = file_unique_id
        db.save(self.route)
        db.close()


if __name__ == '__main__':

    print(type(bd["stickers"].values))
    print(sticker_page.title)
    print_table()

    about_sheet()
