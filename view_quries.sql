--Views for Query 1
create view Profit
AS
select m.title,(m.budget-sum(a.salary)) as Income
From Movies M inner join ActorsInMovies A
on m.title=A.mTitle
group by m.title, m.budget;


create view betweenTop20
As
select m.title,m.genre
from movies m
where m.title in(select Top 20 title
                 from Profit
                 order by Income desc);


--Views for Query 2
create view ratingLess
as
select distinct w1.mTitle
from watching w1,watching w2
where w1.uID=w2.uID and w1.mTitle=w2.mTitle and w1.wDate>w2.wDate and w1.rating<=w2.rating;


create view ImprovedMovies
as
select distinct mtitle
from watching
except
select *
from ratingLess;


create view ActorInImproved
as
select a.aName
from ImprovedMovies I inner join ActorsInMovies A on
I.mtitle=A.mTitle
group by a.aName
having count(*)>=3;


--Views for Query 3
create view DidntWatch
as
select uid
from users
except
select distinct u.uid
from users u inner join watching w
on u.uid=w.uID
where w.mtitle in(select distinct a.mTitle
                      from ActorsInMovies A
                      where a.aName=u.favActor);


create view DnumofWatches
as
select d.uid,count(*) as numOfWatches
from DidntWatch D inner join watching w
on d.uid=w.uid
group by d.uid;


create view FakeWatcher
as
select d.uid,d.numOfWatches,u.country
from DnumofWatches D inner join users u
on d.uid=u.uID
where d.numOfWatches>(select avg(WatchesIncountry.num)
                      from (select distinct w.uid,count(*) as num
                            from users u1,watching w
                            where u.country=u1.country and u1.uid=w.uID
                            group by w.uid)as WatchesIncountry);


create view atLeastFiveC
as
select distinct f.country
from FakeWatcher F
group by f.country
having  count(*)>=5;