--create table Employee
--(id int primary key,
-- salary int)

--Insert into Employee values (1  , 100)    
--Insert into Employee values (2  , 200)  
--Insert into Employee values (3  , 300)  

select * from Employee

select coalesce((
select distinct a.salary
from(
select salary, DENSE_RANK() over(order by salary desc) 'salary_order'
from Employee) a
where salary_order = 2),null) as b



CREATE FUNCTION getNthHighestSalary(@N INT) RETURNS INT AS
BEGIN
    RETURN (
        /* Write your T-SQL query statement below. */
        select coalesce((
        select distinct a.salary
        from(
        select salary, DENSE_RANK() over(order by salary desc) 'salary_order'
        from Employee) a
        where salary_order = @N),null) as b

    );
END

select dbo.getNthHighestSalary(4)