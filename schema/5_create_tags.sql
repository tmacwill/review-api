create table tags (
    id bigserial not null primary key,
    name varchar(255) not null
);

create index tags__name on tags (name);
