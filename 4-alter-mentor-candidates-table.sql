/*
Write an SQL file here, which changes the mentor_candidates table's schema with the following:
- adds a new autoincremented field with the name 'id'
*/
ALTER TABLE mentor_candidates ADD id SERIAL;