from django.shortcuts import render
from django.db import connection


def dictfetchall(cursor):
    "Return all rows from a cursor as a dict"
    columns = [col[0] for col in cursor.description]
    return [dict(zip(columns, row)) for row in cursor.fetchall()]


def index(request):
    return render(request, 'index.html')

def Query_Results(request):
    with connection.cursor() as cursor:
        cursor.execute("""
                        select t.genre,count(distinct t.title) as numOfMovies,ROUND(AVG(CAST(w.rating AS float)), 2) as avgR
                        from betweenTop20 T left outer join watching w on w.mtitle=T.title
                        group by t.genre
                        order by numOfMovies desc;
                        """)
        sql_res1 = dictfetchall(cursor)
    with connection.cursor() as cursor:
        cursor.execute("""
                        select a.aname,count(a.mTitle) as numOfMovies
                        from ActorsInMovies A inner join ActorInImproved AI on
                        AI.aName=A.aName
                        where ai.aName not in(select distinct favActor
                                              from users)
                        group by a.aname;
                        """)
        sql_res2 = dictfetchall(cursor)
    with connection.cursor() as cursor:
        cursor.execute("""
                        select f.country,f.uid
                        from atLeastFiveC C inner join FakeWatcher F on C.country = F.country
                        except
                        select f1.country,f1.uid
                        from atLeastFiveC C1 inner join FakeWatcher F1 on C1.country = F1.country
                        where f1.numOfWatches<any(select distinct f2.numOfWatches
                                                  from FakeWatcher f2
                                                  where F1.country=f2.country)
                        order by country;
                        """)
        sql_res3 = dictfetchall(cursor)
    return render(request,'Query_Results.html',{'sql_res1':sql_res1,'sql_res2':sql_res2,
                                           'sql_res3': sql_res3})

def add_Actor(request):
    if request.method == 'POST' and request.POST:
       Actor=request.POST['aname']
       Movie=request.POST['mname']
       Salary=int(request.POST['salary'])
       flag=False
       flag1=False
       flag2=False
       flag3=False
       with connection.cursor() as cursor:#changed here-returning the budget alone
           cursor.execute("""
                               SELECT budget FROM Movies WHERE title = %s
                           """, [Movie])
           res1=dictfetchall(cursor)
           movie_budget =res1[0]['budget'] if res1 and res1[0]['budget'] is not None else 0
       with connection.cursor() as cursor:#changed here-returning total salaries alone
           cursor.execute("""
              SELECT SUM(salary) as Total_Salaries FROM Actorsinmovies WHERE mTitle = %s
               """, [Movie])
           res2 =dictfetchall(cursor)
           Total_Salaries = res2[0]['Total_Salaries'] if res2 and res2[0]['Total_Salaries'] is not None else 0
       Income=0#changed here-computing the income alone
       if Total_Salaries>0:
           Income=movie_budget-Total_Salaries
       else:
           Income=movie_budget
       with connection.cursor() as cursor:
           cursor.execute("""
                           select *
                           from Movies M
                           where m.title=%s;
                           """,[Movie])
           result=dictfetchall(cursor)
           if not result:
               flag=True
               #return render(request, 'Add_Actor_to_Movie.html',{'flag': flag})
           elif result:
               with connection.cursor() as cursor:
                   cursor.execute("""
                                   select *
                                   from ActorsInMovies A
                                   where a.mtitle=%s and a.aname=%s;
                                   """, [Movie,Actor])
                   result1 = dictfetchall(cursor)
               if result1:
                   flag1=True
                   #return render(request, 'Add_Actor_to_Movie.html', {'flag1': flag1})
               elif not result1:
                       if Salary>Income:#changed here
                           flag2=True
                           #return render(request, 'Add_Actor_to_Movie.html', {'flag2': flag2})
                       else :
                            flag3=True
                            with connection.cursor() as cursor:
                                cursor.execute("""
                                                INSERT INTO ActorsInMovies (aName, mTitle, salary)
                                                VALUES (%s, %s,%s);
                                               """, [Actor, Movie, Salary])
       with connection.cursor() as cursor:#changed here also in order to show top 5 movies anyway
          cursor.execute("""
             select Top 5 m.title,m.genre,m.releaseDate
             from Movies M inner join actorsinmovies a
             on m.title=a.mtitle
             where %s=a.aname
             order by m.releaseDate desc
             """, [Actor])
          sql_res=dictfetchall(cursor)
          return render(request, 'Add_Actor_to_Movie.html', {'sql_res': sql_res,
                        'flag': flag,'flag1': flag1,'flag2': flag2,'flag3': flag3})
    return render(request, 'Add_Actor_to_Movie.html')

def record_watching(request):
    with connection.cursor() as cursor:
        cursor.execute("""
                        select uid
                        from users;
                        """)
        sql_res = dictfetchall(cursor)
    with connection.cursor() as cursor:
        cursor.execute("""
                        select title
                        from movies;
                        """)
        sql_res1 = dictfetchall(cursor)
    if request.method == 'POST' and request.POST:
      with connection.cursor() as cursor:
        user=request.POST['list']
        Movie=request.POST['list1']
        date=request.POST['Date']
        rating=request.POST['rating']
        cursor.execute("""
                       select *
                           from watching w
                           where w.mtitle=%s and w.uid=%s and w.wDate=%s;
                           """, [Movie, user, date])
        result=dictfetchall(cursor)
        if result:
            flag = True
            return render(request, 'Record_Watching.html', {'flag': flag,'sql_res': sql_res, 'sql_res1': sql_res1})
        elif not result:
            with connection.cursor() as cursor:
                cursor.execute("""
                                       select *
                                       from watching w
                                       where w.mtitle=%s and %s<w.wdate and w.uid=%s;
                                       """, [Movie, date,user])
                result1 = dictfetchall(cursor)
            if result1:
                flag1 = True
                return render(request, 'Record_Watching.html', {'flag1': flag1,'sql_res': sql_res, 'sql_res1': sql_res1})
            elif not result1:
                with connection.cursor() as cursor:
                    cursor.execute("""
                                           select *
                                           from Movies M 
                                           where m.title=%s and %s<m.releaseDate;
                                           """, [Movie,date])
                    result2 = dictfetchall(cursor)
                    if result2:
                        flag2 = True
                        return render(request, 'Record_Watching.html', {'flag2': flag2,'sql_res': sql_res, 'sql_res1': sql_res1})
                    else:
                        with connection.cursor() as cursor:
                            cursor.execute("""
                                                    INSERT INTO watching (uid, mtitle, wdate,rating)
                                                    VALUES (%s, %s,%s,%s);
                                                   """, [user,Movie, date,rating])
                            flag3 = True
                            return render(request, 'Record_Watching.html',{'flag3':flag3,'sql_res': sql_res, 'sql_res1': sql_res1})
    return render(request, 'Record_Watching.html', {'sql_res': sql_res, 'sql_res1': sql_res1})

