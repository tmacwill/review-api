create table users (
    id bigserial not null primary key,
    facebook_id text not null,
    facebook_token text not null,
    email text not null,
    name text not null,
    token text not null
);

create index users__facebook_id on users (facebook_id);
create index users__token on users (token);
