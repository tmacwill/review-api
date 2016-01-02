create table submissions (
    id bigserial not null primary key,
    user_id bigint not null,
    slug varchar(8) not null,
    title text not null
);

create index submissions__user_id on submissions (user_id);
create index submissions__slug on submissions (slug);
