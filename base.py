from openpyxl import load_workbook, worksheet

bd = load_workbook("base.xlsx")
sticker_page: worksheet.worksheet.Worksheet = bd["stickers"]
print(type(sticker_page) == worksheet.worksheet.Worksheet)


def print_table(page: str = "stickers"):
    for key, val, ans in bd[page].values:
        print(str(key).ljust(20), str(val).ljust(80), str(ans))


def get_stickers(sticker_name: str = None, page: str = "stickers"):
    db = load_workbook("base.xlsx")
    return get_stickers(page=page).get(sticker_name, None)\
        if sticker_name \
        else {key: val for key, *val in db[page].values}


def about_sheet(table: worksheet.worksheet.Worksheet = bd["stickers"]):
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

    def new_user(self, user):
        db = load_workbook(self.route)
        page = db["users"]
        row = page.max_row + 1
        for col, val in enumerate(user):
            page.cell(row=row, column=col+1).value = val

    def stickers(self):
        db = load_workbook(self.route)
        page = db["stickers"]
        stickers_dict = {
            key: {
                "sticker": sticker,
                "answer": answer
            }
            for key, sticker, answer
            in page.values
        }
        db.close()
        return stickers_dict


if __name__ == '__main__':

    print(type(bd["stickers"].values))
    print(sticker_page.title)
    print_table()

    about_sheet()
