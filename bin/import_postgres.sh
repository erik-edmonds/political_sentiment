#!/bin/bash
sudo mv ../data/* /var/lib/postgresql/10/main/

psql -U erikedmonds -d data -c "
DROP TABLE IF EXISTS senate;
CREATE TABLE senate(question_id INT, poll_id INT, cycle INT, state TEXT, pollster_id INT,pollster TEXT, sponsor_ids TEXT, sponsors TEXT, display_name TEXT, pollster_rating_id INT, pollster_rating_name TEXT, fte_grade TEXT,
sample_size DECIMAL, population TEXT, population_full TEXT, methodology TEXT,
office_type TEXT, seat_number INT, seat_name TEXT, start_date DATE, end_date DATE,
election_date DATE, sponsor_candidate TEXT, internal TEXT, partisan TEXT,
tracking TEXT, nationwide_batch TEXT, ranked_choice_reallocated TEXT,
created_at TIMESTAMP, notes TEXT, url TEXT, stage TEXT, answer TEXT, candidate_name TEXT, candidate_party TEXT, pct TEXT);

copy senate FROM 'senate_polls.csv' DELIMITER ',' CSV HEADER;
" 
