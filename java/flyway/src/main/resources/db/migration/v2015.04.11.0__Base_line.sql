--
-- PostgreSQL database dump
--

SET statement_timeout = 0;
SET lock_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SET check_function_bodies = false;
SET client_min_messages = warning;

--
-- Name: plpgsql; Type: EXTENSION; Schema: -; Owner: 
--

CREATE EXTENSION IF NOT EXISTS plpgsql WITH SCHEMA pg_catalog;


--
-- Name: EXTENSION plpgsql; Type: COMMENT; Schema: -; Owner: 
--

COMMENT ON EXTENSION plpgsql IS 'PL/pgSQL procedural language';


SET search_path = public, pg_catalog;

SET default_tablespace = '';

SET default_with_oids = false;

--
-- Name: first; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE first (
    id integer NOT NULL,
    second_id integer NOT NULL,
    name character varying NOT NULL
);


ALTER TABLE public.first OWNER TO postgres;

--
-- Name: first_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE first_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.first_id_seq OWNER TO postgres;

--
-- Name: first_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE first_id_seq OWNED BY first.id;


--
-- Name: second; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE second (
    id integer NOT NULL,
    description text NOT NULL
);


ALTER TABLE public.second OWNER TO postgres;

--
-- Name: second_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE second_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.second_id_seq OWNER TO postgres;

--
-- Name: second_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE second_id_seq OWNED BY second.id;


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY first ALTER COLUMN id SET DEFAULT nextval('first_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY second ALTER COLUMN id SET DEFAULT nextval('second_id_seq'::regclass);


--
-- Name: first_id; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY first
    ADD CONSTRAINT first_id PRIMARY KEY (id);


--
-- Name: second_id; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY second
    ADD CONSTRAINT second_id PRIMARY KEY (id);


--
-- Name: public; Type: ACL; Schema: -; Owner: postgres
--

REVOKE ALL ON SCHEMA public FROM PUBLIC;
REVOKE ALL ON SCHEMA public FROM postgres;
GRANT ALL ON SCHEMA public TO postgres;
GRANT ALL ON SCHEMA public TO PUBLIC;


--
-- PostgreSQL database dump complete
--

