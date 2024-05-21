CREATE EXTENSION "pgcrypto";
CREATE TYPE userType AS ENUM ('user', 'admin');

CREATE TABLE "public"."users" (
  "id" serial primary key NOT null,
  "user_id" UUID NOT null,
  "username" varchar(255) NOT null,
  "password" varchar(255) NOT null,
  "email" varchar(255) NOT null,
  "user_type" userType NOT null,
  "created_at" timestamp NOT null DEFAULT NOW()
  );

CREATE TABLE "public"."upload_data" (
  "id" serial primary key NOT NULL,
  "file_id" UUID NOT NULL,
  "file_name" varchar(255) NOT NULL,
  "file_path" varchar(255) NOT NULL,
  "file_owner" varchar(255) NOT NULL,
  "file_type" varchar(255) NOT NULL,
  "created_at" timestamp NOT NULL DEFAULT NOW()
  );