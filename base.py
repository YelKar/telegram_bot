from openpyxl import load_workbook, worksheet

bd = load_workbook("base.xlsx")


def print_table(page: str = "stickers"):
    for key, val in bd[page].values:
        print(key.ljust(20), val)


def about_sheet(table: worksheet.worksheet.Worksheet = bd["stickers"]):
    print("_" * 10 + "about".ljust(90, "_"))
    print("max_row:".ljust(20) + str(table.max_row))
    print("max_column:".ljust(20) + str(table.max_column))
    print("_" * 100)


# for i in bd:
#     i.f


stickers_page = bd["stickers"]

print(type(bd["stickers"]))
print(stickers_page.title)
print_table()

about_sheet()

