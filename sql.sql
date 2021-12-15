-- create table public.users (
--  id serial primary key not null,
-- 	first_name varchar not null,
-- 	last_name varchar not null,
-- 	email varchar not null,
--  password_hash varchar TODO not null?
-- );

create table public.trucks (
  id serial primary key not null,
	name varchar not null,
	plate varchar not null
);

create table public.reservations (
  id serial primary key not null,
	user_id uuid not null,
	truck_id integer not null,
	start_dt timestamp with time zone not null,
	end_dt timestamp with time zone not null
);
-- alter table public.reservations
--   add constraint reservation_user_id_fkey foreign key (user_id) references public.users(id);
alter table public.reservations
  add constraint reservation_truck_id_fkey foreign key (truck_id) references public.trucks(id);

CREATE EXTENSION btree_gist;
alter table reservations
  add constraint no_overlapping
  exclude using gist (truck_id with =, tstzrange("start_dt", "end_dt", '[]') WITH &&);

create index reservations_user_id_index ON reservations (user_id);

-- insert into users (first_name, last_name, email) values
-- 	('David','Rose','david@roseapothecary.com'),
-- 	('Stevie','Budd','stevie@rosebudmotel.com'),
-- 	('Alexis','Rose','alexis@alittlebitalexis.com'),

insert into trucks (name, plate) values
	('8'' Pickup Truck', 'abc001'),
	('9'' Cargo Van', 'abc002'),
	('9'' Cargo Van', 'abc003'),
	('10'' Truck', 'abc004'),
	('10'' Truck', 'abc005'),
	('10'' Truck', 'abc006'),
	('15'' Truck', 'abc007'),
	('15'' Truck', 'abc008'),
	('20'' Truck', 'abc009'),
	('26'' Truck', 'abc010');
