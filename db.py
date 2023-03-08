import sqlite3, random

# populatets database with example/test data

conn = sqlite3.connect('test.db')
c = conn.cursor()
employeesTable = """ CREATE TABLE IF NOT EXISTS employees (
    [employee_id] INTEGER PRIMARY KEY,
    [name] TEXT NOT NULL,
    [pay] INTEGER,
    [title] TEXT,
    [date_hired] TEXT,
    [description] TEXT,
    [portrait] BLOB)"""
names = ["Riley Reid",
    "Angela White",
    "Abella Danger",
    "Mia Khalifa",
    "Ava Addams",
    "Lana Rhoades",
    "Brandi Love",
    "Lisa Ann",
    "Lena Paul",
    "Sara Jay",
    "Violet Myers",
    "Kendra Lust",
    "Cory Chase",
    "Mia Malkova",
    "Dillion Harper",
    "Natasha Nice",
    "Alexis Fawx",
    "Emily Willis",
    "Kenzie Reeves",
    "Adriana Chechik",
    "Eva Lovia",
    "Lauren Phillips",
    "Dee Williams",
    "Lexi Luna",
    "Elsa Jean",
    "Piper Perri",
    "Gabbie Carter",
    "Nicole Aniston",
    "Autumn Falls",
    "Alexis Texas",
    "Gianna Michaels",
    "Cherie Deville",
    "Eliza Ibarra",
    "Gina Valentina",
    "Skylar Vox",
    "Dani Daniels",
    "Madison Ivy",
    "Valentina Nappi",
    "Phoenix Marie",
    "Alison Tyler"]
def pay():
    return random.randint(22000, 240000)
title = "Conductor"
date_hired = [
    "01-01-2001",
    "02-02-2002",
    "03-03-2003",
    "04-04-2004",
    "05-05-2005",
    "06-06-2006",
    "07-07-2007",
    "08-08-2008",
    "09-09-2009",
    "00-00-2000",
    "10-01-2001",
    "21-02-2002",
    "32-03-2003",
    "43-04-2004",
    "54-05-2005",
    "65-06-2006",
    "76-07-2007",
    "87-08-2008",
    "98-09-2009",
    "09-00-2000",
    "10-01-2001",
    "21-02-2002",
    "32-03-2003",
    "43-04-2004",
    "54-05-2005",
    "65-06-2006",
    "76-07-2007",
    "87-08-2008",
    "98-09-2009",
    "09-00-2000",
    "10-01-2001",
    "20-02-2002",
    "30-03-2003",
    "40-04-2004",
    "50-05-2005",
    "60-06-2006",
    "70-07-2007",
    "80-08-2008",
    "90-09-2009",
    "00-00-2000"]
desc = "spongebob square hat"
id = 1
for i in names:
    c.execute("INSERT INTO employees VALUES (:employee_id, :name, :pay, :title, :date_hired, :description, :portrait)",
              {
                  'employee_id': id,
                  'name': i,
                  'pay': pay(),
                  'title': title,
                  'date_hired': date_hired[names.index(i)],
                  'description': desc,
                  'portrait': "headshot.png"
              }
              )
    id += 1
conn.commit()
conn.close()