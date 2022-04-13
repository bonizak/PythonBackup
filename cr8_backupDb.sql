-- Drop Database if exists BKUP.;

-- CREATE DATABASE BKUP.;

-- Table: BKUP.BackupSets
-- Drop SCHEMA if exists BKUP;
CREATE SCHEMA if not exists BKUP;

DROP TABLE IF EXISTS BKUP."BackupSets";

CREATE TABLE IF NOT EXISTS BKUP."BackupSets"
(
    "ID" serial NOT NULL,
    "BackupSetName" character varying(64) COLLATE pg_catalog."default" NOT NULL,
    "StorageSetID" integer NOT NULL,
    "FileSetID" integer NOT NULL,
    "Versions" smallint NOT NULL,
    "FrequencyID" integer NOT NULL,
    CONSTRAINT "BackupSets_pkey" PRIMARY KEY ("ID")
)

TABLESPACE pg_default;

ALTER TABLE IF EXISTS BKUP."BackupSets"
    OWNER to postgres;
    
    -- Table: BKUP.AppConfig

DROP TABLE IF EXISTS BKUP."AppConfig";

CREATE TABLE IF NOT EXISTS BKUP."AppConfig"
(
    id serial NOT NULL ,
    key character varying COLLATE pg_catalog."default" NOT NULL,
    value character varying COLLATE pg_catalog."default" NOT NULL,
    CONSTRAINT "AppConfig_pkey" PRIMARY KEY (id)
)

TABLESPACE pg_default;

ALTER TABLE IF EXISTS BKUP."AppConfig"
    OWNER to postgres;
    
    -- Table: BKUP.Devices

DROP TABLE IF EXISTS BKUP."Devices";

CREATE TABLE IF NOT EXISTS BKUP."Devices"
(
    "ID" serial NOT NULL,
    "Device" character varying(32) COLLATE pg_catalog."default" NOT NULL,
    CONSTRAINT "Devices_pkey" PRIMARY KEY ("ID")
)

TABLESPACE pg_default;

ALTER TABLE IF EXISTS BKUP."Devices"
    OWNER to postgres;
    
    -- Table: BKUP.FileSets

DROP TABLE IF EXISTS BKUP."FileSets";

CREATE TABLE IF NOT EXISTS BKUP."FileSets"
(
    "ID" Serial NOT NULL,
    "FileSetName" character varying(64) COLLATE pg_catalog."default" NOT NULL,
    "Includes" character varying(256) COLLATE pg_catalog."default" NOT NULL,
    "Excludes" character varying(256) COLLATE pg_catalog."default" NOT NULL,
    "Compress" boolean NOT NULL DEFAULT true,
    "Recursive" boolean NOT NULL DEFAULT false,
    "EstimatedSize" bigint,
    CONSTRAINT "FileSets_pkey" PRIMARY KEY ("ID")
)

TABLESPACE pg_default;

ALTER TABLE IF EXISTS BKUP."FileSets"
    OWNER to postgres;
    
-- Table: BKUP.Frequencies

DROP TABLE IF EXISTS BKUP."Frequencies";

CREATE TABLE IF NOT EXISTS BKUP."Frequencies"
(
    "ID" Serial NOT NULL,
    "Frequency" character varying(32) COLLATE pg_catalog."default" NOT NULL,
    CONSTRAINT "Frequencies_pkey" PRIMARY KEY ("ID")
)

TABLESPACE pg_default;

ALTER TABLE IF EXISTS BKUP."Frequencies"
    OWNER to postgres;    
    
-- Table: BKUP.LogLevels

DROP TABLE IF EXISTS BKUP."LogLevels";

CREATE TABLE IF NOT EXISTS BKUP."LogLevels"
(
    "ID" Serial NOT NULL,
    "LogLevel" character varying(16) COLLATE pg_catalog."default" NOT NULL,
    CONSTRAINT "LogLevels_pkey" PRIMARY KEY ("ID")
)

TABLESPACE pg_default;

ALTER TABLE IF EXISTS BKUP."LogLevels"
    OWNER to postgres;    
    
-- Table: BKUP.RootPaths

DROP TABLE IF EXISTS BKUP."RootPaths";

CREATE TABLE IF NOT EXISTS BKUP."RootPaths"
(
    "ID" Serial NOT NULL,
    "Rootpath" character varying(256) COLLATE pg_catalog."default" NOT NULL,
    "MaxDepth" smallint NOT NULL,
    "FilesFolders" character varying(8) COLLATE pg_catalog."default" NOT NULL
)

TABLESPACE pg_default;

ALTER TABLE IF EXISTS BKUP."RootPaths"
    OWNER to postgres;    
    
-- Table: BKUP.StorageSets

DROP TABLE IF EXISTS BKUP."StorageSets";

CREATE TABLE IF NOT EXISTS BKUP."StorageSets"
(
    "ID" Serial NOT NULL,
    "StorageSetname" character varying(128) COLLATE pg_catalog."default" NOT NULL,
    "StoragePath" character varying(256) COLLATE pg_catalog."default" NOT NULL,
    "DevicePathId" integer NOT NULL,
    CONSTRAINT "StorageSets_pkey" PRIMARY KEY ("ID")
)

TABLESPACE pg_default;

ALTER TABLE IF EXISTS BKUP."StorageSets"
    OWNER to postgres;


-- Table: bkup.FileSetNames

DROP TABLE IF EXISTS bkup."FileSetNames";

CREATE TABLE IF NOT EXISTS bkup."FileSetNames"
(
    "ID" Serial NOT NULL,
    "FileSetName" character varying(64) COLLATE pg_catalog."default" NOT NULL,
    CONSTRAINT "FileSetNames_pkey" PRIMARY KEY ("ID")
)

TABLESPACE pg_default;

ALTER TABLE IF EXISTS bkup."FileSetNames"
    OWNER to postgres;