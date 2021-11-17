
.headers on

-- take in data from given csv file
drop table given;
.mode csv
.import 'given.csv' given

-- populate user table
delete from user;

insert into user(username, password)
select distinct studentnames, 'password'
from given;

insert into user(username, password)
select distinct teachername, 'password'
from given;

-- populate teacher table
delete from teacher;

insert into teacher(name, user_id)
select distinct teachername, id
from given, user
where teachername != ''
and teachername = username;

-- populate student table
delete from student;

insert into student(name, user_id)
select distinct studentnames, id
from given, user
where studentnames != ''
and studentnames = username;

-- populate class
delete from class;

insert into class(course_name, teacher_id, enrolled, capacity, time)
select distinct classname, id, 0, capacity, time
from given, teacher
where teachername = name;

-- populate enrollment
delete from enrollment;

insert into enrollment(class_id, student_id, grade)
select  class.id, student.id, grades
from given, class as class, student as student
where class.course_name = classname
and studentnames = student.name;

-- after enrolled update class table
update class
set enrolled = given.count
from
    (
        select count(*) as count, classname as name
        from given
        group by classname
    ) as given
where given.name = class.course_name;

