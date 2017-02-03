/*
Write an SQL file that:
- truncates the mentor_candidates table
- puts 10,000 (yep, TEN THOUSAND) records into the mentor_candidates table
  - first_name possible values are: Miklós, Tamás, Dániel, Mateusz, Attila, Pál, Sándor, Prezmek, John, Tim, Matthew, Andy, Giancarlo
  - last_name possible values are: Beöthy, Tompa, Salamon, Ostafil, Molnár, Monoczki, Szodoray, Ciacka, Carrey, Obama, Lebron, Hamilton, Fisichella
  - birth_year should be between 1960-1995
  - email should be a random, but valid email
  - city possible values are: Budapest, Miskolc, Krakow, Barcelona, New York
  - phone_number should be a random 10 digit number, with a plus sign at the beginnin
  - level should be between 1-10
- does all of this in a transaction

How should you generate an SQL big like this? :-) Our advices is just one word: Python...
*/
BEGIN;
TRUNCATE TABLE mentor_candidates;
COPY mentor_candidates(first_name, last_name, phone_number, email, city, level, birth_year)
FROM '/home/okocsis90/codecool/8th_si_week/sql_remote_repo/sql_application_3/mentor_candidates.csv' DELIMITER ',' CSV;
COMMIT;