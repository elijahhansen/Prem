import pymssql
import sys
servername = 'elijahhansen.database.windows.net'
login = 'ReadWriteUser'
pwd = 'nu!cs2022'
dbname = 'Premier_League_Matches'
print('**Trying to connect to Premier_League_Matches in Microsoft Azure cloud...')
print()
try:
 dbConn = pymssql.connect(server=servername,
 user=login,
password=pwd,
 database=dbname)
 print("**connected!")
except Exception as err:
 print("Error:", err)
 print("failed to connect :-(")
 sys.exit()
finally:
 print()
## additional code here
'''
sql = """Select count(Match_ID) from Matches"""
dbCursor = dbConn.cursor()
dbCursor.execute(sql)
rows = dbCursor.fetchone()
print("# of matches from 2009 to 2019", ":", f"{rows[0]:,}")
sql = """Select count(Referee_ID) from Referees"""
dbCursor = dbConn.cursor()
dbCursor.execute(sql)
rows = dbCursor.fetchone()
print("# of refs from 2009 to 2019", ":", f"{rows[0]:,}")
sql = """Select count(City_ID) from Cities"""
dbCursor = dbConn.cursor()
dbCursor.execute(sql)
rows = dbCursor.fetchone()
print("# of cities", ":", f"{rows[0]:,}")
sql = """Select count(Club_ID) from Clubs"""
dbCursor = dbConn.cursor()
dbCursor.execute(sql)
rows = dbCursor.fetchone()
print("# of clubs from 2009 to 2019", ":", f"{rows[0]:,}")
'''
dbCursor = dbConn.cursor()

def harshest_ref(dbCursor):
  #ref = cmd("Enter Referee's Name (e.g. 'M Clattenburg'): ")
  sql = """Select top(5) (Select Referee from Referees where Referee_ID = Matches.Referee_ID), count(HC+AC)
  from Matches 
  inner join Referees on Matches.Referee_ID = Referees.Referee_ID
  group by Matches.Referee_ID
  order by count(HC+AC) desc;"""
  dbCursor.execute(sql)
  rows = dbCursor.fetchall()
  for row in rows:
    print("Referee:", row[0],"|", "Cards Given:", row[1])

def games_by_city(dbCursor):
  city = input("Enter City (e.g. '%london%'): ")
  pattern = "%" + city + "%"
  sql = """Select count(Match_ID)
  from Matches 
  where City_ID = (Select City_ID from Cities where City like %s);"""
  dbCursor.execute(sql,(pattern))
  rows = dbCursor.fetchone()
  print(city, "|", "Games Played:", rows[0])

def team_results(dbCursor):
  team = input("Enter Club Name (e.g. '%Liverpool%'): ")
  pattern = "%" + team + "%"
  question = input("Inquire about a specific year? [yes/no] ")
  if question == "yes" or question == "y":
    y = input("Enter a year: ")
    sql = """Select (Select Clubs.Club_Name from Clubs where Club_ID = Home_Team_ID), (Select Clubs.Club_Name from Clubs where Club_ID = Away_Team_ID) , Date,Year(Date), (Select Results.Result_Name from Results where Result_ID = FTR_ID)
    from Matches 
    left join Results on Matches.FTR_ID = Results.Result_ID
    where Year(Date) = %d and (Home_Team_ID = (Select Clubs.Club_ID from Clubs where Club_Name like %s) or (Away_Team_ID = (Select Clubs.Club_ID from Clubs where Club_Name like %s)));"""
    dbCursor.execute(sql,(y,pattern, pattern))
    rows = dbCursor.fetchmany(20)
    if len(rows) == 20:
      while True:
        if len(rows) == 0:
          print("no matches found")
          break
        else:
          for row in rows:
            print(row[1],"at",row[0],"|",row[2],"|","Result:",row[4])
        print()
        more = input("Display more? [yes/no] ")
        if more == "y" or more == "yes":
          rows = dbCursor.fetchmany(20)
        else:
          break
    elif len(rows) == 0:
      print("no matches found")
    else:
      for row in rows:
        print(row[1],"at",row[0],"|",row[2],"|",row[4])
  else:
    sql = """Select (Select Clubs.Club_Name from Clubs where Club_ID = Home_Team_ID), (Select Clubs.Club_Name from Clubs where Club_ID = Away_Team_ID) , Date, (Select Results.Result_Name from Results where Result_ID = FTR_ID)
    from Matches 
    left join Results on Matches.FTR_ID = Results.Result_ID
    where Home_Team_ID = (Select Clubs.Club_ID from Clubs where Club_Name like %s) or Away_Team_ID = (Select Clubs.Club_ID from Clubs where Club_Name like %s);"""
    
    dbCursor.execute(sql, (pattern, pattern))
    rows = dbCursor.fetchmany(20)
    if len(rows) == 20:
      while True:
        if len(rows) == 0:
          print("no matches found")
          break
        else:
          for row in rows:
            print(row[1],"at",row[0],"|",row[2],"|","Result:",row[3])
        print()
        more = input("Display more? [yes/no] ")
        if more == "y" or more == "yes":
          rows = dbCursor.fetchmany(20)
        else:
          break
    elif len(rows) == 0:
      print("no matches found")
    else:
      for row in rows:
        print(row[1],"at",row[0],"|",row[2],"|",row[3])

def highest_scoring_games(dbCursor):
  sql = """Select Top(10) (Select Clubs.Club_Name from Clubs where Club_ID = Matches.Home_Team_ID), (Select Clubs.Club_Name from Clubs where Club_ID = Matches.Away_Team_ID), Date, (FTHG+FTAG)
  from Matches
  left join Clubs on Matches.Home_Team_ID = Clubs.Club_ID
  order by FTHG+FTAG desc;"""
  dbCursor.execute(sql)
  rows = dbCursor.fetchall()
  for row in rows:
    print(row[1], "at", row[0], "|", "Date:",row[2],"|", "Goals Scored:", row[3])

def blowouts(dbCursor):
  sql = """Select Top(10) (Select Clubs.Club_Name from Clubs where Club_ID = Matches.Home_Team_ID), (Select Clubs.Club_Name from Clubs where Club_ID = Matches.Away_Team_ID), Date, FTHG, FTAG, ABS(FTHG-FTAG) as diff
  from Matches
  left join Clubs on Matches.Home_Team_ID = Clubs.Club_ID
  order by diff desc;"""
  dbCursor.execute(sql)
  rows = dbCursor.fetchall()
  for row in rows:
    print(row[1], "at", row[0], "|", "Date:",row[2],"|","Score:", row[3], row[4])
  
cmd = input("Please enter a command (1-5, x to exit): ")
while cmd != "x":
  if cmd == "1":
    harshest_ref(dbCursor)
  elif cmd == "2": 
    games_by_city(dbCursor)
  elif cmd == "3":
    team_results(dbCursor)
  elif cmd == "4":
    highest_scoring_games(dbCursor)
  elif cmd == "5":
    blowouts(dbCursor)
  else:
    print("**Error, unknown command, try again...")
  print()
  cmd = input("Please enter a command (1-5, x to exit): ")
  
print()
print("** Done **")