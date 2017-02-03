/*
Write an SQL file which adds indexes to tables in order to optimize the following queries:

SELECT mentor_candidates.*, schools.name AS school_name, mentors.email AS mentor_email
FROM mentor_candidates
INNER JOIN schools ON mentor_candidates.city = schools.city
INNER JOIN mentors ON schools.contact_person = mentors.id
WHERE mentor_candidates.city IN ('Budapest', 'Miskolc', 'Krakow');

SELECT mentor_candidates.*, schools.name AS school_name, mentors.email AS mentor_email
FROM mentor_candidates
INNER JOIN schools ON mentor_candidates.city = schools.city
INNER JOIN mentors ON schools.contact_person = mentors.id
WHERE mentor_candidates.city IN ('Budapest', 'Miskolc', 'Krakow') AND birth_year > 1980 AND level > 6;

Don't give custom names for the indexes, but when you create a multiple column index, please list the
columns in alphavetical order.
*/
CREATE INDEX mentor_candidates_birth_year_city_idx ON mentor_candidates(birth_year, city);
CREATE INDEX mentor_candidates_city_idx ON mentor_candidates(city);
CREATE INDEX schools_city_idx ON schools(city);