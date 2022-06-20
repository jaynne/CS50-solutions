-- Keep a log of any SQL queries you execute as you solve the mystery.
SELECT description FROM crime_scene_reports WHERE month=7 AND day=28 AND street="Chamberlin Street";
-- Description below
-- Theft of the CS50 duck took place at 10:15am at the Chamberlin Street courthouse. Interviews were conducted today with three witnesses who were present at the time — each of their interview transcripts mentions the courthouse.

-- To see activity match in hour 10
SELECT * FROM courthouse_security_logs WHERE hour=10 AND  month=7 AND day=28;

-- Transcripts from people in month 7 and day 28
SELECT transcript,name,id FROM interviews WHERE month=7 AND day=28;

-- Selecting tables of ATM transactions (according to Eugene's interview)
SELECT * FROM atm_transactions WHERE month=7 AND day=28 AND transaction_type='withdraw' AND atm_location='Fifer Street';

-- Selecting name of people who withdrawed money that day (Eugene's interview)
SELECT name FROM people WHERE id IN (SELECT person_id FROM bank_accounts WHERE account_number IN (SELECT account_number FROM atm_transactions WHERE month=7 AND day=28 AND transaction_type='withdraw' AND atm_location='Fifer Street'));

-- Selecting name from people where license_plate is in set described by Ruth's interview
SELECT name FROM people WHERE license_plate IN (SELECT license_plate FROM courthouse_security_logs WHERE hour=10 AND  month=7 AND day=28 AND activity='exit' AND minute < 25);

-- Now we have the names that appear in both tables. Let's see the airport name to follow the next steps
SELECT * FROM airports WHERE city='Fiftyville';

-- Phone calls within 10 min from crime
SELECT * FROM phone_calls WHERE month=7 AND day=28 AND duration <=60;

-- Select name from people who made these calls
SELECT name FROM people WHERE phone_number IN (SELECT caller FROM phone_calls WHERE month=7 AND day=28 AND duration <=60);

-- Let's filter flights next day, earliest
SELECT * FROM flights WHERE origin_airport_id=8 AND month=7 AND day=29 ORDER BY hour ASC LIMIT 1;

-- Filter passengers from last flight
SELECT name FROM people WHERE passport_number IN (SELECT passport_number FROM flights WHERE id=36);
-- Final suspects: Russell, Ernest
-- But we still have to discover who is the thief and who is the accomplice

-- Let's see who was the receiver for Ernest's call
SELECT name FROM people WHERE phone_number IN (SELECT receiver FROM phone_calls WHERE caller IN (SELECT phone_number FROM people WHERE name='Ernest') AND month=7 AND day=28 AND duration <=60);
-- It was Berthold

-- Let's see who was the receiver for Russell's call
SELECT name FROM people WHERE phone_number IN (SELECT receiver FROM phone_calls WHERE caller IN (SELECT phone_number FROM people WHERE name='Russell') AND month=7 AND day=28 AND duration <=60);
-- It was Philip, but he is in the passengers list

-- Now let's see the city they escaped to
SELECT city FROM airports WHERE id IN (SELECT destination_airport_id FROM flights WHERE id=36);