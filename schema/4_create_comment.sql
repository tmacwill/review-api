create table comments (
    id bigserial not null primary key,
    file_id bigint not null,
    user_id bigint not null,
    start_line integer not null,
    end_line integer not null,
    content text not null
);

create index comments__file_id on comments (file_id);
create index comments__user_id on comments (user_id);
