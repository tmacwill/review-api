create table files (
    id bigserial not null primary key,
    submission_id bigint not null,
    title text not null,
    content text not null
);

create index files__submission_id on files (submission_id);
