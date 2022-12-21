-- 
-- depends: 
create table "users"(
	id serial primary key,
	tg_user_id integer unique,
	username text,
	fullname text
);

create table "users_etis"(
    id serial primary key,
    user_id integer references users (id),
    email text,
    password text
);
