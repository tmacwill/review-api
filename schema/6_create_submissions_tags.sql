create table submissions_tags (
    id bigserial not null primary key,
    submission_id bigint not null,
    tag_id bigint not null
);

create index submissions_tags__submission_id on submissions_tags (submission_id);
create index submissions_tags__tag_id on submissions_tags (tag_id);
