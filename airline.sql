alter table user
change create_time creation_time timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP;