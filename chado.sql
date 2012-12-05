--
-- PostgreSQL database dump
--

SET statement_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = off;
SET check_function_bodies = false;
SET client_min_messages = warning;
SET escape_string_warning = off;

SET search_path = public, pg_catalog;

ALTER TABLE ONLY public.mycoplasma_home_taggroup DROP CONSTRAINT user_fkey;
ALTER TABLE ONLY public.mycoplasma_home_tag DROP CONSTRAINT user_fkey;
ALTER TABLE ONLY public.mycoplasma_home_recentlyviewedpicture DROP CONSTRAINT user_fkey;
ALTER TABLE ONLY public.mycoplasma_home_taggroup DROP CONSTRAINT picture_fkey;
ALTER TABLE ONLY public.mycoplasma_home_recentlyviewedpicture DROP CONSTRAINT picture_fkey;
ALTER TABLE ONLY public.mycoplasma_home_picture DROP CONSTRAINT "originalUser_fkey";
ALTER TABLE ONLY public.mycoplasma_home_tagpoint DROP CONSTRAINT mycoplasma_home_tagpoint_group_id_fkey;
ALTER TABLE ONLY public.mycoplasma_home_tag DROP CONSTRAINT mycoplasma_home_taggroup_color_fkey;
ALTER TABLE ONLY public.mycoplasma_home_pictureprop DROP CONSTRAINT mycoplasma_home_pictureprops_type_id_id_fkey;
ALTER TABLE ONLY public.mycoplasma_home_pictureprop DROP CONSTRAINT mycoplasma_home_pictureprops_picture_id_id_fkey;
ALTER TABLE ONLY public.mycoplasma_home_picturedefinitiontag DROP CONSTRAINT mycoplasma_home_picturedefinitiontag_picture_id_fkey;
ALTER TABLE ONLY public.mycoplasma_home_dropdownitem DROP CONSTRAINT "mycoplasma_home_dropdownitem_navBarOpt_id_fkey";
ALTER TABLE ONLY public.multiuploader_image DROP CONSTRAINT multiuploader_user_id_fkey;
ALTER TABLE ONLY public.django_admin_log DROP CONSTRAINT django_admin_log_user_id_fkey;
ALTER TABLE ONLY public.django_admin_log DROP CONSTRAINT django_admin_log_content_type_id_fkey;
ALTER TABLE ONLY public.auth_permission DROP CONSTRAINT content_type_id_refs_id_728de91f;
ALTER TABLE ONLY public.auth_user_user_permissions DROP CONSTRAINT auth_user_user_permissions_user_id_fkey;
ALTER TABLE ONLY public.auth_user_user_permissions DROP CONSTRAINT auth_user_user_permissions_permission_id_fkey;
ALTER TABLE ONLY public.auth_user_groups DROP CONSTRAINT auth_user_groups_user_id_fkey;
ALTER TABLE ONLY public.auth_user_groups DROP CONSTRAINT auth_user_groups_group_id_fkey;
ALTER TABLE ONLY public.auth_message DROP CONSTRAINT auth_message_user_id_fkey;
ALTER TABLE ONLY public.auth_group_permissions DROP CONSTRAINT auth_group_permissions_permission_id_fkey;
ALTER TABLE ONLY public.auth_group_permissions DROP CONSTRAINT auth_group_permissions_group_id_fkey;
DROP INDEX public.mycoplasma_home_tagpoint_group_id;
DROP INDEX public.mycoplasma_home_pictureprops_type_id_id;
DROP INDEX public.mycoplasma_home_pictureprops_picture_id_id;
DROP INDEX public."mycoplasma_home_dropdownitem_navBarOpt_id";
DROP INDEX public.django_admin_log_user_id;
DROP INDEX public.django_admin_log_content_type_id;
DROP INDEX public.auth_permission_content_type_id;
DROP INDEX public.auth_message_user_id;
ALTER TABLE ONLY public.thumbnail_kvstore DROP CONSTRAINT thumbnail_kvstore_pkey;
ALTER TABLE ONLY public.mycoplasma_home_taggroup DROP CONSTRAINT name_unique;
ALTER TABLE ONLY public.mycoplasma_home_tagpoint DROP CONSTRAINT mycoplasma_home_tagpoint_pkey;
ALTER TABLE ONLY public.mycoplasma_home_taggroup DROP CONSTRAINT mycoplasma_home_taggroup_pkey;
ALTER TABLE ONLY public.mycoplasma_home_tagcolor DROP CONSTRAINT mycoplasma_home_tagcolor_pkey;
ALTER TABLE ONLY public.mycoplasma_home_tag DROP CONSTRAINT mycoplasma_home_tag_pkey;
ALTER TABLE ONLY public.mycoplasma_home_recentlyviewedpicture DROP CONSTRAINT mycoplasma_home_recentlyviewedpicture_uniqueness;
ALTER TABLE ONLY public.mycoplasma_home_recentlyviewedpicture DROP CONSTRAINT mycoplasma_home_recentlyviewedpicture_pkey;
ALTER TABLE ONLY public.mycoplasma_home_picturetype DROP CONSTRAINT mycoplasma_home_picturetypes_pkey;
ALTER TABLE ONLY public.mycoplasma_home_picture DROP CONSTRAINT mycoplasma_home_pictures_pkey;
ALTER TABLE ONLY public.mycoplasma_home_pictureprop DROP CONSTRAINT mycoplasma_home_pictureprops_pkey;
ALTER TABLE ONLY public.mycoplasma_home_pictureprop DROP CONSTRAINT mycoplasma_home_pictureprops_picture_id_id_key;
ALTER TABLE ONLY public.mycoplasma_home_picturedefinitiontag DROP CONSTRAINT mycoplasma_home_picturedefinitiontag_pkey;
ALTER TABLE ONLY public.mycoplasma_home_navbaroption DROP CONSTRAINT mycoplasma_home_navbaroption_pkey;
ALTER TABLE ONLY public.mycoplasma_home_landmark DROP CONSTRAINT mycoplasma_home_landmark_pkey;
ALTER TABLE ONLY public.mycoplasma_home_dropdownitem DROP CONSTRAINT mycoplasma_home_dropdownitem_pkey;
ALTER TABLE ONLY public.mycoplasma_home_blastupload DROP CONSTRAINT mycoplasma_home_blastupload_pkey;
ALTER TABLE ONLY public.multiuploader_image DROP CONSTRAINT multiuploader_image_pkey;
ALTER TABLE ONLY public.multiuploader_image DROP CONSTRAINT multiuploader_image_key_data_key;
ALTER TABLE ONLY public.django_site DROP CONSTRAINT django_site_pkey;
ALTER TABLE ONLY public.django_session DROP CONSTRAINT django_session_pkey;
ALTER TABLE ONLY public.django_content_type DROP CONSTRAINT django_content_type_pkey;
ALTER TABLE ONLY public.django_content_type DROP CONSTRAINT django_content_type_app_label_key;
ALTER TABLE ONLY public.django_admin_log DROP CONSTRAINT django_admin_log_pkey;
ALTER TABLE ONLY public.auth_user DROP CONSTRAINT auth_user_username_key;
ALTER TABLE ONLY public.auth_user_user_permissions DROP CONSTRAINT auth_user_user_permissions_user_id_key;
ALTER TABLE ONLY public.auth_user_user_permissions DROP CONSTRAINT auth_user_user_permissions_pkey;
ALTER TABLE ONLY public.auth_user DROP CONSTRAINT auth_user_pkey;
ALTER TABLE ONLY public.auth_user_groups DROP CONSTRAINT auth_user_groups_user_id_key;
ALTER TABLE ONLY public.auth_user_groups DROP CONSTRAINT auth_user_groups_pkey;
ALTER TABLE ONLY public.auth_permission DROP CONSTRAINT auth_permission_pkey;
ALTER TABLE ONLY public.auth_permission DROP CONSTRAINT auth_permission_content_type_id_key;
ALTER TABLE ONLY public.auth_message DROP CONSTRAINT auth_message_pkey;
ALTER TABLE ONLY public.auth_group DROP CONSTRAINT auth_group_pkey;
ALTER TABLE ONLY public.auth_group_permissions DROP CONSTRAINT auth_group_permissions_pkey;
ALTER TABLE ONLY public.auth_group_permissions DROP CONSTRAINT auth_group_permissions_group_id_key;
ALTER TABLE ONLY public.auth_group DROP CONSTRAINT auth_group_name_key;
ALTER TABLE public.mycoplasma_home_tagpoint ALTER COLUMN id DROP DEFAULT;
ALTER TABLE public.mycoplasma_home_taggroup ALTER COLUMN id DROP DEFAULT;
ALTER TABLE public.mycoplasma_home_tagcolor ALTER COLUMN id DROP DEFAULT;
ALTER TABLE public.mycoplasma_home_tag ALTER COLUMN id DROP DEFAULT;
ALTER TABLE public.mycoplasma_home_recentlyviewedpicture ALTER COLUMN id DROP DEFAULT;
ALTER TABLE public.mycoplasma_home_picturetype ALTER COLUMN id DROP DEFAULT;
ALTER TABLE public.mycoplasma_home_pictureprop ALTER COLUMN id DROP DEFAULT;
ALTER TABLE public.mycoplasma_home_picturedefinitiontag ALTER COLUMN id DROP DEFAULT;
ALTER TABLE public.mycoplasma_home_picture ALTER COLUMN id DROP DEFAULT;
ALTER TABLE public.mycoplasma_home_navbaroption ALTER COLUMN id DROP DEFAULT;
ALTER TABLE public.mycoplasma_home_landmark ALTER COLUMN id DROP DEFAULT;
ALTER TABLE public.mycoplasma_home_genomeupload ALTER COLUMN id DROP DEFAULT;
ALTER TABLE public.mycoplasma_home_dropdownitem ALTER COLUMN id DROP DEFAULT;
ALTER TABLE public.mycoplasma_home_blastupload ALTER COLUMN id DROP DEFAULT;
ALTER TABLE public.multiuploader_image ALTER COLUMN id DROP DEFAULT;
ALTER TABLE public.django_site ALTER COLUMN id DROP DEFAULT;
ALTER TABLE public.django_content_type ALTER COLUMN id DROP DEFAULT;
ALTER TABLE public.django_admin_log ALTER COLUMN id DROP DEFAULT;
ALTER TABLE public.auth_user_user_permissions ALTER COLUMN id DROP DEFAULT;
ALTER TABLE public.auth_user_groups ALTER COLUMN id DROP DEFAULT;
ALTER TABLE public.auth_user ALTER COLUMN id DROP DEFAULT;
ALTER TABLE public.auth_permission ALTER COLUMN id DROP DEFAULT;
ALTER TABLE public.auth_message ALTER COLUMN id DROP DEFAULT;
ALTER TABLE public.auth_group_permissions ALTER COLUMN id DROP DEFAULT;
ALTER TABLE public.auth_group ALTER COLUMN id DROP DEFAULT;
DROP TABLE public.thumbnail_kvstore;
DROP SEQUENCE public.mycoplasma_home_tagpoint_id_seq;
DROP TABLE public.mycoplasma_home_tagpoint;
DROP SEQUENCE public.mycoplasma_home_taggroup_id_seq1;
DROP SEQUENCE public.mycoplasma_home_taggroup_id_seq;
DROP TABLE public.mycoplasma_home_taggroup;
DROP SEQUENCE public.mycoplasma_home_tagcolor_id_seq;
DROP TABLE public.mycoplasma_home_tagcolor;
DROP TABLE public.mycoplasma_home_tag;
DROP SEQUENCE public.mycoplasma_home_recentlyviewedpicture_id_seq;
DROP TABLE public.mycoplasma_home_recentlyviewedpicture;
DROP SEQUENCE public.mycoplasma_home_picturetypes_id_seq;
DROP TABLE public.mycoplasma_home_picturetype;
DROP SEQUENCE public.mycoplasma_home_pictures_id_seq;
DROP SEQUENCE public.mycoplasma_home_pictureprops_id_seq;
DROP TABLE public.mycoplasma_home_pictureprop;
DROP SEQUENCE public.mycoplasma_home_picturedefinitiontag_id_seq;
DROP TABLE public.mycoplasma_home_picturedefinitiontag;
DROP TABLE public.mycoplasma_home_picture;
DROP SEQUENCE public.mycoplasma_home_navbaroption_id_seq;
DROP TABLE public.mycoplasma_home_navbaroption;
DROP SEQUENCE public.mycoplasma_home_landmark_id_seq;
DROP TABLE public.mycoplasma_home_landmark;
DROP SEQUENCE public.mycoplasma_home_genomeupload_id_seq;
DROP TABLE public.mycoplasma_home_genomeupload;
DROP SEQUENCE public.mycoplasma_home_dropdownitem_id_seq;
DROP TABLE public.mycoplasma_home_dropdownitem;
DROP SEQUENCE public.mycoplasma_home_blastupload_id_seq;
DROP TABLE public.mycoplasma_home_blastupload;
DROP SEQUENCE public.multiuploader_image_id_seq;
DROP TABLE public.multiuploader_image;
DROP SEQUENCE public.django_site_id_seq;
DROP TABLE public.django_site;
DROP TABLE public.django_session;
DROP SEQUENCE public.django_content_type_id_seq;
DROP TABLE public.django_content_type;
DROP SEQUENCE public.django_admin_log_id_seq;
DROP TABLE public.django_admin_log;
DROP SEQUENCE public.auth_user_user_permissions_id_seq;
DROP TABLE public.auth_user_user_permissions;
DROP SEQUENCE public.auth_user_id_seq;
DROP SEQUENCE public.auth_user_groups_id_seq;
DROP TABLE public.auth_user_groups;
DROP TABLE public.auth_user;
DROP SEQUENCE public.auth_permission_id_seq;
DROP TABLE public.auth_permission;
DROP SEQUENCE public.auth_message_id_seq;
DROP TABLE public.auth_message;
DROP SEQUENCE public.auth_group_permissions_id_seq;
DROP TABLE public.auth_group_permissions;
DROP SEQUENCE public.auth_group_id_seq;
DROP TABLE public.auth_group;
DROP SCHEMA public;
--
-- Name: public; Type: SCHEMA; Schema: -; Owner: postgres
--

CREATE SCHEMA public;


ALTER SCHEMA public OWNER TO postgres;

--
-- Name: SCHEMA public; Type: COMMENT; Schema: -; Owner: postgres
--

COMMENT ON SCHEMA public IS 'standard public schema';


SET search_path = public, pg_catalog;

SET default_tablespace = '';

SET default_with_oids = false;

--
-- Name: auth_group; Type: TABLE; Schema: public; Owner: mycoplasma; Tablespace: 
--

CREATE TABLE auth_group (
    id integer NOT NULL,
    name character varying(80) NOT NULL
);


ALTER TABLE public.auth_group OWNER TO mycoplasma;

--
-- Name: auth_group_id_seq; Type: SEQUENCE; Schema: public; Owner: mycoplasma
--

CREATE SEQUENCE auth_group_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MAXVALUE
    NO MINVALUE
    CACHE 1;


ALTER TABLE public.auth_group_id_seq OWNER TO mycoplasma;

--
-- Name: auth_group_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: mycoplasma
--

ALTER SEQUENCE auth_group_id_seq OWNED BY auth_group.id;


--
-- Name: auth_group_id_seq; Type: SEQUENCE SET; Schema: public; Owner: mycoplasma
--

SELECT pg_catalog.setval('auth_group_id_seq', 1, false);


--
-- Name: auth_group_permissions; Type: TABLE; Schema: public; Owner: mycoplasma; Tablespace: 
--

CREATE TABLE auth_group_permissions (
    id integer NOT NULL,
    group_id integer NOT NULL,
    permission_id integer NOT NULL
);


ALTER TABLE public.auth_group_permissions OWNER TO mycoplasma;

--
-- Name: auth_group_permissions_id_seq; Type: SEQUENCE; Schema: public; Owner: mycoplasma
--

CREATE SEQUENCE auth_group_permissions_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MAXVALUE
    NO MINVALUE
    CACHE 1;


ALTER TABLE public.auth_group_permissions_id_seq OWNER TO mycoplasma;

--
-- Name: auth_group_permissions_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: mycoplasma
--

ALTER SEQUENCE auth_group_permissions_id_seq OWNED BY auth_group_permissions.id;


--
-- Name: auth_group_permissions_id_seq; Type: SEQUENCE SET; Schema: public; Owner: mycoplasma
--

SELECT pg_catalog.setval('auth_group_permissions_id_seq', 1, false);


--
-- Name: auth_message; Type: TABLE; Schema: public; Owner: mycoplasma; Tablespace: 
--

CREATE TABLE auth_message (
    id integer NOT NULL,
    user_id integer NOT NULL,
    message text NOT NULL
);


ALTER TABLE public.auth_message OWNER TO mycoplasma;

--
-- Name: auth_message_id_seq; Type: SEQUENCE; Schema: public; Owner: mycoplasma
--

CREATE SEQUENCE auth_message_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MAXVALUE
    NO MINVALUE
    CACHE 1;


ALTER TABLE public.auth_message_id_seq OWNER TO mycoplasma;

--
-- Name: auth_message_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: mycoplasma
--

ALTER SEQUENCE auth_message_id_seq OWNED BY auth_message.id;


--
-- Name: auth_message_id_seq; Type: SEQUENCE SET; Schema: public; Owner: mycoplasma
--

SELECT pg_catalog.setval('auth_message_id_seq', 75, true);


--
-- Name: auth_permission; Type: TABLE; Schema: public; Owner: mycoplasma; Tablespace: 
--

CREATE TABLE auth_permission (
    id integer NOT NULL,
    name character varying(50) NOT NULL,
    content_type_id integer NOT NULL,
    codename character varying(100) NOT NULL
);


ALTER TABLE public.auth_permission OWNER TO mycoplasma;

--
-- Name: auth_permission_id_seq; Type: SEQUENCE; Schema: public; Owner: mycoplasma
--

CREATE SEQUENCE auth_permission_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MAXVALUE
    NO MINVALUE
    CACHE 1;


ALTER TABLE public.auth_permission_id_seq OWNER TO mycoplasma;

--
-- Name: auth_permission_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: mycoplasma
--

ALTER SEQUENCE auth_permission_id_seq OWNED BY auth_permission.id;


--
-- Name: auth_permission_id_seq; Type: SEQUENCE SET; Schema: public; Owner: mycoplasma
--

SELECT pg_catalog.setval('auth_permission_id_seq', 627, true);


--
-- Name: auth_user; Type: TABLE; Schema: public; Owner: mycoplasma; Tablespace: 
--

CREATE TABLE auth_user (
    id integer NOT NULL,
    username character varying(30) NOT NULL,
    first_name character varying(30) NOT NULL,
    last_name character varying(30) NOT NULL,
    email character varying(75) NOT NULL,
    password character varying(128) NOT NULL,
    is_staff boolean NOT NULL,
    is_active boolean NOT NULL,
    is_superuser boolean NOT NULL,
    last_login timestamp with time zone NOT NULL,
    date_joined timestamp with time zone NOT NULL
);


ALTER TABLE public.auth_user OWNER TO mycoplasma;

--
-- Name: auth_user_groups; Type: TABLE; Schema: public; Owner: mycoplasma; Tablespace: 
--

CREATE TABLE auth_user_groups (
    id integer NOT NULL,
    user_id integer NOT NULL,
    group_id integer NOT NULL
);


ALTER TABLE public.auth_user_groups OWNER TO mycoplasma;

--
-- Name: auth_user_groups_id_seq; Type: SEQUENCE; Schema: public; Owner: mycoplasma
--

CREATE SEQUENCE auth_user_groups_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MAXVALUE
    NO MINVALUE
    CACHE 1;


ALTER TABLE public.auth_user_groups_id_seq OWNER TO mycoplasma;

--
-- Name: auth_user_groups_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: mycoplasma
--

ALTER SEQUENCE auth_user_groups_id_seq OWNED BY auth_user_groups.id;


--
-- Name: auth_user_groups_id_seq; Type: SEQUENCE SET; Schema: public; Owner: mycoplasma
--

SELECT pg_catalog.setval('auth_user_groups_id_seq', 1, false);


--
-- Name: auth_user_id_seq; Type: SEQUENCE; Schema: public; Owner: mycoplasma
--

CREATE SEQUENCE auth_user_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MAXVALUE
    NO MINVALUE
    CACHE 1;


ALTER TABLE public.auth_user_id_seq OWNER TO mycoplasma;

--
-- Name: auth_user_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: mycoplasma
--

ALTER SEQUENCE auth_user_id_seq OWNED BY auth_user.id;


--
-- Name: auth_user_id_seq; Type: SEQUENCE SET; Schema: public; Owner: mycoplasma
--

SELECT pg_catalog.setval('auth_user_id_seq', 4, true);


--
-- Name: auth_user_user_permissions; Type: TABLE; Schema: public; Owner: mycoplasma; Tablespace: 
--

CREATE TABLE auth_user_user_permissions (
    id integer NOT NULL,
    user_id integer NOT NULL,
    permission_id integer NOT NULL
);


ALTER TABLE public.auth_user_user_permissions OWNER TO mycoplasma;

--
-- Name: auth_user_user_permissions_id_seq; Type: SEQUENCE; Schema: public; Owner: mycoplasma
--

CREATE SEQUENCE auth_user_user_permissions_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MAXVALUE
    NO MINVALUE
    CACHE 1;


ALTER TABLE public.auth_user_user_permissions_id_seq OWNER TO mycoplasma;

--
-- Name: auth_user_user_permissions_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: mycoplasma
--

ALTER SEQUENCE auth_user_user_permissions_id_seq OWNED BY auth_user_user_permissions.id;


--
-- Name: auth_user_user_permissions_id_seq; Type: SEQUENCE SET; Schema: public; Owner: mycoplasma
--

SELECT pg_catalog.setval('auth_user_user_permissions_id_seq', 96, true);


--
-- Name: django_admin_log; Type: TABLE; Schema: public; Owner: mycoplasma; Tablespace: 
--

CREATE TABLE django_admin_log (
    id integer NOT NULL,
    action_time timestamp with time zone NOT NULL,
    user_id integer NOT NULL,
    content_type_id integer,
    object_id text,
    object_repr character varying(200) NOT NULL,
    action_flag smallint NOT NULL,
    change_message text NOT NULL,
    CONSTRAINT django_admin_log_action_flag_check CHECK ((action_flag >= 0))
);


ALTER TABLE public.django_admin_log OWNER TO mycoplasma;

--
-- Name: django_admin_log_id_seq; Type: SEQUENCE; Schema: public; Owner: mycoplasma
--

CREATE SEQUENCE django_admin_log_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MAXVALUE
    NO MINVALUE
    CACHE 1;


ALTER TABLE public.django_admin_log_id_seq OWNER TO mycoplasma;

--
-- Name: django_admin_log_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: mycoplasma
--

ALTER SEQUENCE django_admin_log_id_seq OWNED BY django_admin_log.id;


--
-- Name: django_admin_log_id_seq; Type: SEQUENCE SET; Schema: public; Owner: mycoplasma
--

SELECT pg_catalog.setval('django_admin_log_id_seq', 309, true);


--
-- Name: django_content_type; Type: TABLE; Schema: public; Owner: mycoplasma; Tablespace: 
--

CREATE TABLE django_content_type (
    id integer NOT NULL,
    name character varying(100) NOT NULL,
    app_label character varying(100) NOT NULL,
    model character varying(100) NOT NULL
);


ALTER TABLE public.django_content_type OWNER TO mycoplasma;

--
-- Name: django_content_type_id_seq; Type: SEQUENCE; Schema: public; Owner: mycoplasma
--

CREATE SEQUENCE django_content_type_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MAXVALUE
    NO MINVALUE
    CACHE 1;


ALTER TABLE public.django_content_type_id_seq OWNER TO mycoplasma;

--
-- Name: django_content_type_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: mycoplasma
--

ALTER SEQUENCE django_content_type_id_seq OWNED BY django_content_type.id;


--
-- Name: django_content_type_id_seq; Type: SEQUENCE SET; Schema: public; Owner: mycoplasma
--

SELECT pg_catalog.setval('django_content_type_id_seq', 209, true);


--
-- Name: django_session; Type: TABLE; Schema: public; Owner: mycoplasma; Tablespace: 
--

CREATE TABLE django_session (
    session_key character varying(40) NOT NULL,
    session_data text NOT NULL,
    expire_date timestamp with time zone NOT NULL
);


ALTER TABLE public.django_session OWNER TO mycoplasma;

--
-- Name: django_site; Type: TABLE; Schema: public; Owner: mycoplasma; Tablespace: 
--

CREATE TABLE django_site (
    id integer NOT NULL,
    domain character varying(100) NOT NULL,
    name character varying(50) NOT NULL
);


ALTER TABLE public.django_site OWNER TO mycoplasma;

--
-- Name: django_site_id_seq; Type: SEQUENCE; Schema: public; Owner: mycoplasma
--

CREATE SEQUENCE django_site_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MAXVALUE
    NO MINVALUE
    CACHE 1;


ALTER TABLE public.django_site_id_seq OWNER TO mycoplasma;

--
-- Name: django_site_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: mycoplasma
--

ALTER SEQUENCE django_site_id_seq OWNED BY django_site.id;


--
-- Name: django_site_id_seq; Type: SEQUENCE SET; Schema: public; Owner: mycoplasma
--

SELECT pg_catalog.setval('django_site_id_seq', 1, true);


--
-- Name: multiuploader_image; Type: TABLE; Schema: public; Owner: mycoplasma; Tablespace: 
--

CREATE TABLE multiuploader_image (
    id integer NOT NULL,
    filename character varying(60),
    image character varying(100) NOT NULL,
    key_data character varying(90),
    upload_date timestamp with time zone NOT NULL,
    user_id integer NOT NULL
);


ALTER TABLE public.multiuploader_image OWNER TO mycoplasma;

--
-- Name: multiuploader_image_id_seq; Type: SEQUENCE; Schema: public; Owner: mycoplasma
--

CREATE SEQUENCE multiuploader_image_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MAXVALUE
    NO MINVALUE
    CACHE 1;


ALTER TABLE public.multiuploader_image_id_seq OWNER TO mycoplasma;

--
-- Name: multiuploader_image_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: mycoplasma
--

ALTER SEQUENCE multiuploader_image_id_seq OWNED BY multiuploader_image.id;


--
-- Name: multiuploader_image_id_seq; Type: SEQUENCE SET; Schema: public; Owner: mycoplasma
--

SELECT pg_catalog.setval('multiuploader_image_id_seq', 150, true);


--
-- Name: mycoplasma_home_blastupload; Type: TABLE; Schema: public; Owner: mycoplasma; Tablespace: 
--

CREATE TABLE mycoplasma_home_blastupload (
    id integer NOT NULL,
    fasta_file character varying(100) NOT NULL,
    name text NOT NULL
);


ALTER TABLE public.mycoplasma_home_blastupload OWNER TO mycoplasma;

--
-- Name: mycoplasma_home_blastupload_id_seq; Type: SEQUENCE; Schema: public; Owner: mycoplasma
--

CREATE SEQUENCE mycoplasma_home_blastupload_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MAXVALUE
    NO MINVALUE
    CACHE 1;


ALTER TABLE public.mycoplasma_home_blastupload_id_seq OWNER TO mycoplasma;

--
-- Name: mycoplasma_home_blastupload_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: mycoplasma
--

ALTER SEQUENCE mycoplasma_home_blastupload_id_seq OWNED BY mycoplasma_home_blastupload.id;


--
-- Name: mycoplasma_home_blastupload_id_seq; Type: SEQUENCE SET; Schema: public; Owner: mycoplasma
--

SELECT pg_catalog.setval('mycoplasma_home_blastupload_id_seq', 56, true);


--
-- Name: mycoplasma_home_dropdownitem; Type: TABLE; Schema: public; Owner: mycoplasma; Tablespace: 
--

CREATE TABLE mycoplasma_home_dropdownitem (
    id integer NOT NULL,
    "itemName" character varying(20) NOT NULL,
    "navBarOpt_id" integer NOT NULL,
    href character varying(100),
    rank integer
);


ALTER TABLE public.mycoplasma_home_dropdownitem OWNER TO mycoplasma;

--
-- Name: mycoplasma_home_dropdownitem_id_seq; Type: SEQUENCE; Schema: public; Owner: mycoplasma
--

CREATE SEQUENCE mycoplasma_home_dropdownitem_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MAXVALUE
    NO MINVALUE
    CACHE 1;


ALTER TABLE public.mycoplasma_home_dropdownitem_id_seq OWNER TO mycoplasma;

--
-- Name: mycoplasma_home_dropdownitem_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: mycoplasma
--

ALTER SEQUENCE mycoplasma_home_dropdownitem_id_seq OWNED BY mycoplasma_home_dropdownitem.id;


--
-- Name: mycoplasma_home_dropdownitem_id_seq; Type: SEQUENCE SET; Schema: public; Owner: mycoplasma
--

SELECT pg_catalog.setval('mycoplasma_home_dropdownitem_id_seq', 4, true);


--
-- Name: mycoplasma_home_genomeupload; Type: TABLE; Schema: public; Owner: mycoplasma; Tablespace: 
--

CREATE TABLE mycoplasma_home_genomeupload (
    genbank_file character varying(100),
    name text,
    id integer NOT NULL
);


ALTER TABLE public.mycoplasma_home_genomeupload OWNER TO mycoplasma;

--
-- Name: mycoplasma_home_genomeupload_id_seq; Type: SEQUENCE; Schema: public; Owner: mycoplasma
--

CREATE SEQUENCE mycoplasma_home_genomeupload_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MAXVALUE
    NO MINVALUE
    CACHE 1;


ALTER TABLE public.mycoplasma_home_genomeupload_id_seq OWNER TO mycoplasma;

--
-- Name: mycoplasma_home_genomeupload_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: mycoplasma
--

ALTER SEQUENCE mycoplasma_home_genomeupload_id_seq OWNED BY mycoplasma_home_genomeupload.id;


--
-- Name: mycoplasma_home_genomeupload_id_seq; Type: SEQUENCE SET; Schema: public; Owner: mycoplasma
--

SELECT pg_catalog.setval('mycoplasma_home_genomeupload_id_seq', 47, true);


--
-- Name: mycoplasma_home_landmark; Type: TABLE; Schema: public; Owner: mycoplasma; Tablespace: 
--

CREATE TABLE mycoplasma_home_landmark (
    name character varying(10),
    organism_id integer,
    id integer NOT NULL
);


ALTER TABLE public.mycoplasma_home_landmark OWNER TO mycoplasma;

--
-- Name: mycoplasma_home_landmark_id_seq; Type: SEQUENCE; Schema: public; Owner: mycoplasma
--

CREATE SEQUENCE mycoplasma_home_landmark_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MAXVALUE
    NO MINVALUE
    CACHE 1;


ALTER TABLE public.mycoplasma_home_landmark_id_seq OWNER TO mycoplasma;

--
-- Name: mycoplasma_home_landmark_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: mycoplasma
--

ALTER SEQUENCE mycoplasma_home_landmark_id_seq OWNED BY mycoplasma_home_landmark.id;


--
-- Name: mycoplasma_home_landmark_id_seq; Type: SEQUENCE SET; Schema: public; Owner: mycoplasma
--

SELECT pg_catalog.setval('mycoplasma_home_landmark_id_seq', 61, true);


--
-- Name: mycoplasma_home_navbaroption; Type: TABLE; Schema: public; Owner: mycoplasma; Tablespace: 
--

CREATE TABLE mycoplasma_home_navbaroption (
    id integer NOT NULL,
    "optionName" character varying(20) NOT NULL,
    href character varying(100),
    rank integer
);


ALTER TABLE public.mycoplasma_home_navbaroption OWNER TO mycoplasma;

--
-- Name: mycoplasma_home_navbaroption_id_seq; Type: SEQUENCE; Schema: public; Owner: mycoplasma
--

CREATE SEQUENCE mycoplasma_home_navbaroption_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MAXVALUE
    NO MINVALUE
    CACHE 1;


ALTER TABLE public.mycoplasma_home_navbaroption_id_seq OWNER TO mycoplasma;

--
-- Name: mycoplasma_home_navbaroption_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: mycoplasma
--

ALTER SEQUENCE mycoplasma_home_navbaroption_id_seq OWNED BY mycoplasma_home_navbaroption.id;


--
-- Name: mycoplasma_home_navbaroption_id_seq; Type: SEQUENCE SET; Schema: public; Owner: mycoplasma
--

SELECT pg_catalog.setval('mycoplasma_home_navbaroption_id_seq', 10, true);


--
-- Name: mycoplasma_home_picture; Type: TABLE; Schema: public; Owner: mycoplasma; Tablespace: 
--

CREATE TABLE mycoplasma_home_picture (
    id integer NOT NULL,
    description text,
    "imageName" character varying(100) NOT NULL,
    publication character varying(50),
    "altText" text,
    user_id integer NOT NULL,
    "uploadDate" timestamp with time zone NOT NULL,
    "isPrivate" boolean DEFAULT false NOT NULL
);


ALTER TABLE public.mycoplasma_home_picture OWNER TO mycoplasma;

--
-- Name: mycoplasma_home_picturedefinitiontag; Type: TABLE; Schema: public; Owner: mycoplasma; Tablespace: 
--

CREATE TABLE mycoplasma_home_picturedefinitiontag (
    id integer NOT NULL,
    picture_id integer,
    organism_id integer,
    name text
);


ALTER TABLE public.mycoplasma_home_picturedefinitiontag OWNER TO mycoplasma;

--
-- Name: mycoplasma_home_picturedefinitiontag_id_seq; Type: SEQUENCE; Schema: public; Owner: mycoplasma
--

CREATE SEQUENCE mycoplasma_home_picturedefinitiontag_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MAXVALUE
    NO MINVALUE
    CACHE 1;


ALTER TABLE public.mycoplasma_home_picturedefinitiontag_id_seq OWNER TO mycoplasma;

--
-- Name: mycoplasma_home_picturedefinitiontag_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: mycoplasma
--

ALTER SEQUENCE mycoplasma_home_picturedefinitiontag_id_seq OWNED BY mycoplasma_home_picturedefinitiontag.id;


--
-- Name: mycoplasma_home_picturedefinitiontag_id_seq; Type: SEQUENCE SET; Schema: public; Owner: mycoplasma
--

SELECT pg_catalog.setval('mycoplasma_home_picturedefinitiontag_id_seq', 14, true);


--
-- Name: mycoplasma_home_pictureprop; Type: TABLE; Schema: public; Owner: mycoplasma; Tablespace: 
--

CREATE TABLE mycoplasma_home_pictureprop (
    id integer NOT NULL,
    picture_id_id integer NOT NULL,
    type_id_id integer NOT NULL
);


ALTER TABLE public.mycoplasma_home_pictureprop OWNER TO mycoplasma;

--
-- Name: mycoplasma_home_pictureprops_id_seq; Type: SEQUENCE; Schema: public; Owner: mycoplasma
--

CREATE SEQUENCE mycoplasma_home_pictureprops_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MAXVALUE
    NO MINVALUE
    CACHE 1;


ALTER TABLE public.mycoplasma_home_pictureprops_id_seq OWNER TO mycoplasma;

--
-- Name: mycoplasma_home_pictureprops_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: mycoplasma
--

ALTER SEQUENCE mycoplasma_home_pictureprops_id_seq OWNED BY mycoplasma_home_pictureprop.id;


--
-- Name: mycoplasma_home_pictureprops_id_seq; Type: SEQUENCE SET; Schema: public; Owner: mycoplasma
--

SELECT pg_catalog.setval('mycoplasma_home_pictureprops_id_seq', 32, true);


--
-- Name: mycoplasma_home_pictures_id_seq; Type: SEQUENCE; Schema: public; Owner: mycoplasma
--

CREATE SEQUENCE mycoplasma_home_pictures_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MAXVALUE
    NO MINVALUE
    CACHE 1;


ALTER TABLE public.mycoplasma_home_pictures_id_seq OWNER TO mycoplasma;

--
-- Name: mycoplasma_home_pictures_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: mycoplasma
--

ALTER SEQUENCE mycoplasma_home_pictures_id_seq OWNED BY mycoplasma_home_picture.id;


--
-- Name: mycoplasma_home_pictures_id_seq; Type: SEQUENCE SET; Schema: public; Owner: mycoplasma
--

SELECT pg_catalog.setval('mycoplasma_home_pictures_id_seq', 51, true);


--
-- Name: mycoplasma_home_picturetype; Type: TABLE; Schema: public; Owner: mycoplasma; Tablespace: 
--

CREATE TABLE mycoplasma_home_picturetype (
    id integer NOT NULL,
    description character varying(50) NOT NULL,
    "imageType" character varying(15) NOT NULL
);


ALTER TABLE public.mycoplasma_home_picturetype OWNER TO mycoplasma;

--
-- Name: mycoplasma_home_picturetypes_id_seq; Type: SEQUENCE; Schema: public; Owner: mycoplasma
--

CREATE SEQUENCE mycoplasma_home_picturetypes_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MAXVALUE
    NO MINVALUE
    CACHE 1;


ALTER TABLE public.mycoplasma_home_picturetypes_id_seq OWNER TO mycoplasma;

--
-- Name: mycoplasma_home_picturetypes_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: mycoplasma
--

ALTER SEQUENCE mycoplasma_home_picturetypes_id_seq OWNED BY mycoplasma_home_picturetype.id;


--
-- Name: mycoplasma_home_picturetypes_id_seq; Type: SEQUENCE SET; Schema: public; Owner: mycoplasma
--

SELECT pg_catalog.setval('mycoplasma_home_picturetypes_id_seq', 4, true);


--
-- Name: mycoplasma_home_recentlyviewedpicture; Type: TABLE; Schema: public; Owner: mycoplasma; Tablespace: 
--

CREATE TABLE mycoplasma_home_recentlyviewedpicture (
    picture_id integer,
    user_id integer,
    "lastDateViewed" timestamp with time zone NOT NULL,
    id integer NOT NULL
);


ALTER TABLE public.mycoplasma_home_recentlyviewedpicture OWNER TO mycoplasma;

--
-- Name: mycoplasma_home_recentlyviewedpicture_id_seq; Type: SEQUENCE; Schema: public; Owner: mycoplasma
--

CREATE SEQUENCE mycoplasma_home_recentlyviewedpicture_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MAXVALUE
    NO MINVALUE
    CACHE 1;


ALTER TABLE public.mycoplasma_home_recentlyviewedpicture_id_seq OWNER TO mycoplasma;

--
-- Name: mycoplasma_home_recentlyviewedpicture_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: mycoplasma
--

ALTER SEQUENCE mycoplasma_home_recentlyviewedpicture_id_seq OWNED BY mycoplasma_home_recentlyviewedpicture.id;


--
-- Name: mycoplasma_home_recentlyviewedpicture_id_seq; Type: SEQUENCE SET; Schema: public; Owner: mycoplasma
--

SELECT pg_catalog.setval('mycoplasma_home_recentlyviewedpicture_id_seq', 1, true);


--
-- Name: mycoplasma_home_tag; Type: TABLE; Schema: public; Owner: mycoplasma; Tablespace: 
--

CREATE TABLE mycoplasma_home_tag (
    id integer NOT NULL,
    description character varying(150) NOT NULL,
    color_id integer NOT NULL,
    user_id integer,
    group_id integer
);


ALTER TABLE public.mycoplasma_home_tag OWNER TO mycoplasma;

--
-- Name: mycoplasma_home_tagcolor; Type: TABLE; Schema: public; Owner: mycoplasma; Tablespace: 
--

CREATE TABLE mycoplasma_home_tagcolor (
    id integer NOT NULL,
    red integer NOT NULL,
    green integer NOT NULL,
    blue integer NOT NULL
);


ALTER TABLE public.mycoplasma_home_tagcolor OWNER TO mycoplasma;

--
-- Name: mycoplasma_home_tagcolor_id_seq; Type: SEQUENCE; Schema: public; Owner: mycoplasma
--

CREATE SEQUENCE mycoplasma_home_tagcolor_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MAXVALUE
    NO MINVALUE
    CACHE 1;


ALTER TABLE public.mycoplasma_home_tagcolor_id_seq OWNER TO mycoplasma;

--
-- Name: mycoplasma_home_tagcolor_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: mycoplasma
--

ALTER SEQUENCE mycoplasma_home_tagcolor_id_seq OWNED BY mycoplasma_home_tagcolor.id;


--
-- Name: mycoplasma_home_tagcolor_id_seq; Type: SEQUENCE SET; Schema: public; Owner: mycoplasma
--

SELECT pg_catalog.setval('mycoplasma_home_tagcolor_id_seq', 1, true);


--
-- Name: mycoplasma_home_taggroup; Type: TABLE; Schema: public; Owner: mycoplasma; Tablespace: 
--

CREATE TABLE mycoplasma_home_taggroup (
    name text,
    user_id integer NOT NULL,
    "dateCreated" timestamp with time zone NOT NULL,
    "lastModified" timestamp with time zone NOT NULL,
    id integer NOT NULL,
    picture_id integer
);


ALTER TABLE public.mycoplasma_home_taggroup OWNER TO mycoplasma;

--
-- Name: mycoplasma_home_taggroup_id_seq; Type: SEQUENCE; Schema: public; Owner: mycoplasma
--

CREATE SEQUENCE mycoplasma_home_taggroup_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MAXVALUE
    NO MINVALUE
    CACHE 1;


ALTER TABLE public.mycoplasma_home_taggroup_id_seq OWNER TO mycoplasma;

--
-- Name: mycoplasma_home_taggroup_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: mycoplasma
--

ALTER SEQUENCE mycoplasma_home_taggroup_id_seq OWNED BY mycoplasma_home_tag.id;


--
-- Name: mycoplasma_home_taggroup_id_seq; Type: SEQUENCE SET; Schema: public; Owner: mycoplasma
--

SELECT pg_catalog.setval('mycoplasma_home_taggroup_id_seq', 1, true);


--
-- Name: mycoplasma_home_taggroup_id_seq1; Type: SEQUENCE; Schema: public; Owner: mycoplasma
--

CREATE SEQUENCE mycoplasma_home_taggroup_id_seq1
    START WITH 1
    INCREMENT BY 1
    NO MAXVALUE
    NO MINVALUE
    CACHE 1;


ALTER TABLE public.mycoplasma_home_taggroup_id_seq1 OWNER TO mycoplasma;

--
-- Name: mycoplasma_home_taggroup_id_seq1; Type: SEQUENCE OWNED BY; Schema: public; Owner: mycoplasma
--

ALTER SEQUENCE mycoplasma_home_taggroup_id_seq1 OWNED BY mycoplasma_home_taggroup.id;


--
-- Name: mycoplasma_home_taggroup_id_seq1; Type: SEQUENCE SET; Schema: public; Owner: mycoplasma
--

SELECT pg_catalog.setval('mycoplasma_home_taggroup_id_seq1', 1, true);


--
-- Name: mycoplasma_home_tagpoint; Type: TABLE; Schema: public; Owner: mycoplasma; Tablespace: 
--

CREATE TABLE mycoplasma_home_tagpoint (
    id integer NOT NULL,
    tag_id integer NOT NULL,
    "pointX" integer NOT NULL,
    "pointY" integer NOT NULL,
    rank integer NOT NULL
);


ALTER TABLE public.mycoplasma_home_tagpoint OWNER TO mycoplasma;

--
-- Name: mycoplasma_home_tagpoint_id_seq; Type: SEQUENCE; Schema: public; Owner: mycoplasma
--

CREATE SEQUENCE mycoplasma_home_tagpoint_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MAXVALUE
    NO MINVALUE
    CACHE 1;


ALTER TABLE public.mycoplasma_home_tagpoint_id_seq OWNER TO mycoplasma;

--
-- Name: mycoplasma_home_tagpoint_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: mycoplasma
--

ALTER SEQUENCE mycoplasma_home_tagpoint_id_seq OWNED BY mycoplasma_home_tagpoint.id;


--
-- Name: mycoplasma_home_tagpoint_id_seq; Type: SEQUENCE SET; Schema: public; Owner: mycoplasma
--

SELECT pg_catalog.setval('mycoplasma_home_tagpoint_id_seq', 8781, true);


--
-- Name: thumbnail_kvstore; Type: TABLE; Schema: public; Owner: mycoplasma; Tablespace: 
--

CREATE TABLE thumbnail_kvstore (
    key character varying(200) NOT NULL,
    value text NOT NULL
);


ALTER TABLE public.thumbnail_kvstore OWNER TO mycoplasma;

--
-- Name: id; Type: DEFAULT; Schema: public; Owner: mycoplasma
--

ALTER TABLE ONLY auth_group ALTER COLUMN id SET DEFAULT nextval('auth_group_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: mycoplasma
--

ALTER TABLE ONLY auth_group_permissions ALTER COLUMN id SET DEFAULT nextval('auth_group_permissions_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: mycoplasma
--

ALTER TABLE ONLY auth_message ALTER COLUMN id SET DEFAULT nextval('auth_message_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: mycoplasma
--

ALTER TABLE ONLY auth_permission ALTER COLUMN id SET DEFAULT nextval('auth_permission_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: mycoplasma
--

ALTER TABLE ONLY auth_user ALTER COLUMN id SET DEFAULT nextval('auth_user_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: mycoplasma
--

ALTER TABLE ONLY auth_user_groups ALTER COLUMN id SET DEFAULT nextval('auth_user_groups_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: mycoplasma
--

ALTER TABLE ONLY auth_user_user_permissions ALTER COLUMN id SET DEFAULT nextval('auth_user_user_permissions_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: mycoplasma
--

ALTER TABLE ONLY django_admin_log ALTER COLUMN id SET DEFAULT nextval('django_admin_log_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: mycoplasma
--

ALTER TABLE ONLY django_content_type ALTER COLUMN id SET DEFAULT nextval('django_content_type_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: mycoplasma
--

ALTER TABLE ONLY django_site ALTER COLUMN id SET DEFAULT nextval('django_site_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: mycoplasma
--

ALTER TABLE ONLY multiuploader_image ALTER COLUMN id SET DEFAULT nextval('multiuploader_image_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: mycoplasma
--

ALTER TABLE ONLY mycoplasma_home_blastupload ALTER COLUMN id SET DEFAULT nextval('mycoplasma_home_blastupload_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: mycoplasma
--

ALTER TABLE ONLY mycoplasma_home_dropdownitem ALTER COLUMN id SET DEFAULT nextval('mycoplasma_home_dropdownitem_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: mycoplasma
--

ALTER TABLE ONLY mycoplasma_home_genomeupload ALTER COLUMN id SET DEFAULT nextval('mycoplasma_home_genomeupload_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: mycoplasma
--

ALTER TABLE ONLY mycoplasma_home_landmark ALTER COLUMN id SET DEFAULT nextval('mycoplasma_home_landmark_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: mycoplasma
--

ALTER TABLE ONLY mycoplasma_home_navbaroption ALTER COLUMN id SET DEFAULT nextval('mycoplasma_home_navbaroption_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: mycoplasma
--

ALTER TABLE ONLY mycoplasma_home_picture ALTER COLUMN id SET DEFAULT nextval('mycoplasma_home_pictures_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: mycoplasma
--

ALTER TABLE ONLY mycoplasma_home_picturedefinitiontag ALTER COLUMN id SET DEFAULT nextval('mycoplasma_home_picturedefinitiontag_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: mycoplasma
--

ALTER TABLE ONLY mycoplasma_home_pictureprop ALTER COLUMN id SET DEFAULT nextval('mycoplasma_home_pictureprops_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: mycoplasma
--

ALTER TABLE ONLY mycoplasma_home_picturetype ALTER COLUMN id SET DEFAULT nextval('mycoplasma_home_picturetypes_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: mycoplasma
--

ALTER TABLE ONLY mycoplasma_home_recentlyviewedpicture ALTER COLUMN id SET DEFAULT nextval('mycoplasma_home_recentlyviewedpicture_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: mycoplasma
--

ALTER TABLE ONLY mycoplasma_home_tag ALTER COLUMN id SET DEFAULT nextval('mycoplasma_home_taggroup_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: mycoplasma
--

ALTER TABLE ONLY mycoplasma_home_tagcolor ALTER COLUMN id SET DEFAULT nextval('mycoplasma_home_tagcolor_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: mycoplasma
--

ALTER TABLE ONLY mycoplasma_home_taggroup ALTER COLUMN id SET DEFAULT nextval('mycoplasma_home_taggroup_id_seq1'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: mycoplasma
--

ALTER TABLE ONLY mycoplasma_home_tagpoint ALTER COLUMN id SET DEFAULT nextval('mycoplasma_home_tagpoint_id_seq'::regclass);


--
-- Data for Name: auth_group; Type: TABLE DATA; Schema: public; Owner: mycoplasma
--

COPY auth_group (id, name) FROM stdin;
\.


--
-- Data for Name: auth_group_permissions; Type: TABLE DATA; Schema: public; Owner: mycoplasma
--

COPY auth_group_permissions (id, group_id, permission_id) FROM stdin;
\.


--
-- Data for Name: auth_message; Type: TABLE DATA; Schema: public; Owner: mycoplasma
--

COPY auth_message (id, user_id, message) FROM stdin;
\.


--
-- Data for Name: auth_permission; Type: TABLE DATA; Schema: public; Owner: mycoplasma
--

COPY auth_permission (id, name, content_type_id, codename) FROM stdin;
1	Can add permission	1	add_permission
2	Can change permission	1	change_permission
3	Can delete permission	1	delete_permission
4	Can add group	2	add_group
5	Can change group	2	change_group
6	Can delete group	2	delete_group
7	Can add user	3	add_user
8	Can change user	3	change_user
9	Can delete user	3	delete_user
10	Can add message	4	add_message
11	Can change message	4	change_message
12	Can delete message	4	delete_message
13	Can add content type	5	add_contenttype
14	Can change content type	5	change_contenttype
15	Can delete content type	5	delete_contenttype
16	Can add session	6	add_session
17	Can change session	6	change_session
18	Can delete session	6	delete_session
19	Can add site	7	add_site
20	Can change site	7	change_site
21	Can delete site	7	delete_site
22	Can add nav bar option	8	add_navbaroption
23	Can change nav bar option	8	change_navbaroption
24	Can delete nav bar option	8	delete_navbaroption
25	Can add log entry	9	add_logentry
26	Can change log entry	9	change_logentry
27	Can delete log entry	9	delete_logentry
28	Can add drop down item	10	add_dropdownitem
29	Can change drop down item	10	change_dropdownitem
30	Can delete drop down item	10	delete_dropdownitem
46	Can add tag group	16	add_taggroup
47	Can change tag group	16	change_taggroup
48	Can delete tag group	16	delete_taggroup
49	Can add tag point	17	add_tagpoint
50	Can change tag point	17	change_tagpoint
51	Can delete tag point	17	delete_tagpoint
52	Can add blast upload	18	add_blastupload
53	Can change blast upload	18	change_blastupload
54	Can delete blast upload	18	delete_blastupload
55	Can add tableinfo	19	add_tableinfo
56	Can change tableinfo	19	change_tableinfo
57	Can delete tableinfo	19	delete_tableinfo
58	Can add db	20	add_db
59	Can change db	20	change_db
60	Can delete db	20	delete_db
61	Can add dbxref	21	add_dbxref
62	Can change dbxref	21	change_dbxref
63	Can delete dbxref	21	delete_dbxref
64	Can add db dbxref count	22	add_dbdbxrefcount
65	Can change db dbxref count	22	change_dbdbxrefcount
66	Can delete db dbxref count	22	delete_dbdbxrefcount
67	Can add cv	23	add_cv
68	Can change cv	23	change_cv
69	Can delete cv	23	delete_cv
70	Can add cvterm	24	add_cvterm
71	Can change cvterm	24	change_cvterm
72	Can delete cvterm	24	delete_cvterm
73	Can add cvterm relationship	25	add_cvtermrelationship
74	Can change cvterm relationship	25	change_cvtermrelationship
75	Can delete cvterm relationship	25	delete_cvtermrelationship
76	Can add project	26	add_project
77	Can change project	26	change_project
78	Can delete project	26	delete_project
79	Can add cvtermpath	27	add_cvtermpath
80	Can change cvtermpath	27	change_cvtermpath
81	Can delete cvtermpath	27	delete_cvtermpath
82	Can add cv leaf	28	add_cvleaf
83	Can change cv leaf	28	change_cvleaf
84	Can delete cv leaf	28	delete_cvleaf
85	Can add dbxrefprop	29	add_dbxrefprop
86	Can change dbxrefprop	29	change_dbxrefprop
87	Can delete dbxrefprop	29	delete_dbxrefprop
88	Can add cvtermprop	30	add_cvtermprop
89	Can change cvtermprop	30	change_cvtermprop
90	Can delete cvtermprop	30	delete_cvtermprop
91	Can add cvtermsynonym	31	add_cvtermsynonym
92	Can change cvtermsynonym	31	change_cvtermsynonym
93	Can delete cvtermsynonym	31	delete_cvtermsynonym
94	Can add common ancestor cvterm	32	add_commonancestorcvterm
95	Can change common ancestor cvterm	32	change_commonancestorcvterm
96	Can delete common ancestor cvterm	32	delete_commonancestorcvterm
97	Can add cvterm dbxref	33	add_cvtermdbxref
98	Can change cvterm dbxref	33	change_cvtermdbxref
99	Can delete cvterm dbxref	33	delete_cvtermdbxref
100	Can add common descendant cvterm	34	add_commondescendantcvterm
101	Can change common descendant cvterm	34	change_commondescendantcvterm
102	Can delete common descendant cvterm	34	delete_commondescendantcvterm
103	Can add cv root	35	add_cvroot
104	Can change cv root	35	change_cvroot
105	Can delete cv root	35	delete_cvroot
106	Can add stats paths to root	36	add_statspathstoroot
107	Can change stats paths to root	36	change_statspathstoroot
108	Can delete stats paths to root	36	delete_statspathstoroot
109	Can add cv cvterm count	37	add_cvcvtermcount
110	Can change cv cvterm count	37	change_cvcvtermcount
111	Can delete cv cvterm count	37	delete_cvcvtermcount
112	Can add cv cvterm count with obs	38	add_cvcvtermcountwithobs
113	Can change cv cvterm count with obs	38	change_cvcvtermcountwithobs
114	Can delete cv cvterm count with obs	38	delete_cvcvtermcountwithobs
115	Can add cv link count	39	add_cvlinkcount
116	Can change cv link count	39	change_cvlinkcount
117	Can delete cv link count	39	delete_cvlinkcount
118	Can add cv path count	40	add_cvpathcount
119	Can change cv path count	40	change_cvpathcount
120	Can delete cv path count	40	delete_cvpathcount
121	Can add pub	41	add_pub
122	Can change pub	41	change_pub
123	Can delete pub	41	delete_pub
124	Can add pub relationship	42	add_pubrelationship
125	Can change pub relationship	42	change_pubrelationship
126	Can delete pub relationship	42	delete_pubrelationship
127	Can add pubprop	43	add_pubprop
128	Can change pubprop	43	change_pubprop
129	Can delete pubprop	43	delete_pubprop
130	Can add pub dbxref	44	add_pubdbxref
131	Can change pub dbxref	44	change_pubdbxref
132	Can delete pub dbxref	44	delete_pubdbxref
133	Can add pubauthor	45	add_pubauthor
134	Can change pubauthor	45	change_pubauthor
135	Can delete pubauthor	45	delete_pubauthor
136	Can add organism	46	add_organism
137	Can change organism	46	change_organism
138	Can delete organism	46	delete_organism
139	Can add organism dbxref	47	add_organismdbxref
140	Can change organism dbxref	47	change_organismdbxref
141	Can delete organism dbxref	47	delete_organismdbxref
142	Can add feature	48	add_feature
143	Can change feature	48	change_feature
144	Can delete feature	48	delete_feature
145	Can add featureloc	49	add_featureloc
146	Can change featureloc	49	change_featureloc
147	Can delete featureloc	49	delete_featureloc
148	Can add featureloc pub	50	add_featurelocpub
149	Can change featureloc pub	50	change_featurelocpub
150	Can delete featureloc pub	50	delete_featurelocpub
151	Can add organismprop	51	add_organismprop
152	Can change organismprop	51	change_organismprop
153	Can delete organismprop	51	delete_organismprop
154	Can add feature pub	52	add_featurepub
155	Can change feature pub	52	change_featurepub
156	Can delete feature pub	52	delete_featurepub
157	Can add feature pubprop	53	add_featurepubprop
158	Can change feature pubprop	53	change_featurepubprop
159	Can delete feature pubprop	53	delete_featurepubprop
160	Can add featureprop	54	add_featureprop
161	Can change featureprop	54	change_featureprop
162	Can delete featureprop	54	delete_featureprop
163	Can add feature relationship	55	add_featurerelationship
164	Can change feature relationship	55	change_featurerelationship
165	Can delete feature relationship	55	delete_featurerelationship
166	Can add feature relationship pub	56	add_featurerelationshippub
167	Can change feature relationship pub	56	change_featurerelationshippub
168	Can delete feature relationship pub	56	delete_featurerelationshippub
169	Can add featureprop pub	57	add_featureproppub
170	Can change featureprop pub	57	change_featureproppub
171	Can delete featureprop pub	57	delete_featureproppub
172	Can add feature dbxref	58	add_featuredbxref
173	Can change feature dbxref	58	change_featuredbxref
174	Can delete feature dbxref	58	delete_featuredbxref
175	Can add feature cvterm	59	add_featurecvterm
176	Can change feature cvterm	59	change_featurecvterm
177	Can delete feature cvterm	59	delete_featurecvterm
178	Can add feature cvtermprop	60	add_featurecvtermprop
179	Can change feature cvtermprop	60	change_featurecvtermprop
180	Can delete feature cvtermprop	60	delete_featurecvtermprop
181	Can add feature relationshipprop	61	add_featurerelationshipprop
182	Can change feature relationshipprop	61	change_featurerelationshipprop
183	Can delete feature relationshipprop	61	delete_featurerelationshipprop
184	Can add feature relationshipprop pub	62	add_featurerelationshipproppub
185	Can change feature relationshipprop pub	62	change_featurerelationshipproppub
186	Can delete feature relationshipprop pub	62	delete_featurerelationshipproppub
187	Can add feature cvterm pub	63	add_featurecvtermpub
188	Can change feature cvterm pub	63	change_featurecvtermpub
189	Can delete feature cvterm pub	63	delete_featurecvtermpub
190	Can add feature cvterm dbxref	64	add_featurecvtermdbxref
191	Can change feature cvterm dbxref	64	change_featurecvtermdbxref
192	Can delete feature cvterm dbxref	64	delete_featurecvtermdbxref
193	Can add synonym	65	add_synonym
194	Can change synonym	65	change_synonym
195	Can delete synonym	65	delete_synonym
196	Can add feature synonym	66	add_featuresynonym
197	Can change feature synonym	66	change_featuresynonym
198	Can delete feature synonym	66	delete_featuresynonym
199	Can add type feature count	67	add_typefeaturecount
200	Can change type feature count	67	change_typefeaturecount
201	Can delete type feature count	67	delete_typefeaturecount
202	Can add protein coding gene	68	add_proteincodinggene
203	Can change protein coding gene	68	change_proteincodinggene
204	Can delete protein coding gene	68	delete_proteincodinggene
205	Can add intron combined view	69	add_introncombinedview
206	Can change intron combined view	69	change_introncombinedview
207	Can delete intron combined view	69	delete_introncombinedview
208	Can add intronloc view	70	add_intronlocview
209	Can change intronloc view	70	change_intronlocview
210	Can delete intronloc view	70	delete_intronlocview
211	Can add analysis	71	add_analysis
212	Can change analysis	71	change_analysis
213	Can delete analysis	71	delete_analysis
214	Can add analysisfeature	72	add_analysisfeature
215	Can change analysisfeature	72	change_analysisfeature
216	Can delete analysisfeature	72	delete_analysisfeature
217	Can add analysisfeatureprop	73	add_analysisfeatureprop
218	Can change analysisfeatureprop	73	change_analysisfeatureprop
219	Can delete analysisfeatureprop	73	delete_analysisfeatureprop
220	Can add analysisprop	74	add_analysisprop
221	Can change analysisprop	74	change_analysisprop
222	Can delete analysisprop	74	delete_analysisprop
223	Can add phenotype	75	add_phenotype
224	Can change phenotype	75	change_phenotype
225	Can delete phenotype	75	delete_phenotype
226	Can add phenotype cvterm	76	add_phenotypecvterm
227	Can change phenotype cvterm	76	change_phenotypecvterm
228	Can delete phenotype cvterm	76	delete_phenotypecvterm
229	Can add feature phenotype	77	add_featurephenotype
230	Can change feature phenotype	77	change_featurephenotype
231	Can delete feature phenotype	77	delete_featurephenotype
232	Can add environment	78	add_environment
233	Can change environment	78	change_environment
234	Can delete environment	78	delete_environment
235	Can add genotype	79	add_genotype
236	Can change genotype	79	change_genotype
237	Can delete genotype	79	delete_genotype
238	Can add environment cvterm	80	add_environmentcvterm
239	Can change environment cvterm	80	change_environmentcvterm
240	Can delete environment cvterm	80	delete_environmentcvterm
241	Can add feature genotype	81	add_featuregenotype
242	Can change feature genotype	81	change_featuregenotype
243	Can delete feature genotype	81	delete_featuregenotype
244	Can add phenstatement	82	add_phenstatement
245	Can change phenstatement	82	change_phenstatement
246	Can delete phenstatement	82	delete_phenstatement
247	Can add phenotype comparison	83	add_phenotypecomparison
248	Can change phenotype comparison	83	change_phenotypecomparison
249	Can delete phenotype comparison	83	delete_phenotypecomparison
250	Can add phendesc	84	add_phendesc
251	Can change phendesc	84	change_phendesc
252	Can delete phendesc	84	delete_phendesc
253	Can add phenotype comparison cvterm	85	add_phenotypecomparisoncvterm
254	Can change phenotype comparison cvterm	85	change_phenotypecomparisoncvterm
255	Can delete phenotype comparison cvterm	85	delete_phenotypecomparisoncvterm
256	Can add featuremap	86	add_featuremap
257	Can change featuremap	86	change_featuremap
258	Can delete featuremap	86	delete_featuremap
259	Can add featurerange	87	add_featurerange
260	Can change featurerange	87	change_featurerange
261	Can delete featurerange	87	delete_featurerange
262	Can add featurepos	88	add_featurepos
263	Can change featurepos	88	change_featurepos
264	Can delete featurepos	88	delete_featurepos
265	Can add phylotree	89	add_phylotree
266	Can change phylotree	89	change_phylotree
267	Can delete phylotree	89	delete_phylotree
268	Can add phylonode	90	add_phylonode
269	Can change phylonode	90	change_phylonode
270	Can delete phylonode	90	delete_phylonode
271	Can add phylonode dbxref	91	add_phylonodedbxref
272	Can change phylonode dbxref	91	change_phylonodedbxref
273	Can delete phylonode dbxref	91	delete_phylonodedbxref
274	Can add featuremap pub	92	add_featuremappub
275	Can change featuremap pub	92	change_featuremappub
276	Can delete featuremap pub	92	delete_featuremappub
277	Can add phylotree pub	93	add_phylotreepub
278	Can change phylotree pub	93	change_phylotreepub
279	Can delete phylotree pub	93	delete_phylotreepub
280	Can add phylonode pub	94	add_phylonodepub
281	Can change phylonode pub	94	change_phylonodepub
282	Can delete phylonode pub	94	delete_phylonodepub
283	Can add phylonode organism	95	add_phylonodeorganism
284	Can change phylonode organism	95	change_phylonodeorganism
285	Can delete phylonode organism	95	delete_phylonodeorganism
286	Can add phylonodeprop	96	add_phylonodeprop
287	Can change phylonodeprop	96	change_phylonodeprop
288	Can delete phylonodeprop	96	delete_phylonodeprop
289	Can add contact	97	add_contact
290	Can change contact	97	change_contact
291	Can delete contact	97	delete_contact
292	Can add contact relationship	98	add_contactrelationship
293	Can change contact relationship	98	change_contactrelationship
294	Can delete contact relationship	98	delete_contactrelationship
295	Can add phylonode relationship	99	add_phylonoderelationship
296	Can change phylonode relationship	99	change_phylonoderelationship
297	Can delete phylonode relationship	99	delete_phylonoderelationship
298	Can add expression	100	add_expression
299	Can change expression	100	change_expression
300	Can delete expression	100	delete_expression
301	Can add expression cvterm	101	add_expressioncvterm
302	Can change expression cvterm	101	change_expressioncvterm
303	Can delete expression cvterm	101	delete_expressioncvterm
304	Can add expression cvtermprop	102	add_expressioncvtermprop
305	Can change expression cvtermprop	102	change_expressioncvtermprop
306	Can delete expression cvtermprop	102	delete_expressioncvtermprop
307	Can add expressionprop	103	add_expressionprop
308	Can change expressionprop	103	change_expressionprop
309	Can delete expressionprop	103	delete_expressionprop
310	Can add feature expression	104	add_featureexpression
311	Can change feature expression	104	change_featureexpression
312	Can delete feature expression	104	delete_featureexpression
313	Can add expression pub	105	add_expressionpub
314	Can change expression pub	105	change_expressionpub
315	Can delete expression pub	105	delete_expressionpub
316	Can add feature expressionprop	106	add_featureexpressionprop
317	Can change feature expressionprop	106	change_featureexpressionprop
318	Can delete feature expressionprop	106	delete_featureexpressionprop
319	Can add eimage	107	add_eimage
320	Can change eimage	107	change_eimage
321	Can delete eimage	107	delete_eimage
322	Can add expression image	108	add_expressionimage
323	Can change expression image	108	change_expressionimage
324	Can delete expression image	108	delete_expressionimage
325	Can add mageml	109	add_mageml
326	Can change mageml	109	change_mageml
327	Can delete mageml	109	delete_mageml
328	Can add magedocumentation	110	add_magedocumentation
329	Can change magedocumentation	110	change_magedocumentation
330	Can delete magedocumentation	110	delete_magedocumentation
331	Can add channel	111	add_channel
332	Can change channel	111	change_channel
333	Can delete channel	111	delete_channel
334	Can add protocol	112	add_protocol
335	Can change protocol	112	change_protocol
336	Can delete protocol	112	delete_protocol
337	Can add protocolparam	113	add_protocolparam
338	Can change protocolparam	113	change_protocolparam
339	Can delete protocolparam	113	delete_protocolparam
340	Can add arraydesign	114	add_arraydesign
341	Can change arraydesign	114	change_arraydesign
342	Can delete arraydesign	114	delete_arraydesign
343	Can add arraydesignprop	115	add_arraydesignprop
344	Can change arraydesignprop	115	change_arraydesignprop
345	Can delete arraydesignprop	115	delete_arraydesignprop
346	Can add assay	116	add_assay
347	Can change assay	116	change_assay
348	Can delete assay	116	delete_assay
349	Can add assay project	117	add_assayproject
350	Can change assay project	117	change_assayproject
351	Can delete assay project	117	delete_assayproject
352	Can add assayprop	118	add_assayprop
353	Can change assayprop	118	change_assayprop
354	Can delete assayprop	118	delete_assayprop
355	Can add biomaterial	119	add_biomaterial
356	Can change biomaterial	119	change_biomaterial
357	Can delete biomaterial	119	delete_biomaterial
358	Can add biomaterial dbxref	120	add_biomaterialdbxref
359	Can change biomaterial dbxref	120	change_biomaterialdbxref
360	Can delete biomaterial dbxref	120	delete_biomaterialdbxref
361	Can add biomaterial relationship	121	add_biomaterialrelationship
362	Can change biomaterial relationship	121	change_biomaterialrelationship
363	Can delete biomaterial relationship	121	delete_biomaterialrelationship
364	Can add biomaterialprop	122	add_biomaterialprop
365	Can change biomaterialprop	122	change_biomaterialprop
366	Can delete biomaterialprop	122	delete_biomaterialprop
367	Can add treatment	123	add_treatment
368	Can change treatment	123	change_treatment
369	Can delete treatment	123	delete_treatment
370	Can add biomaterial treatment	124	add_biomaterialtreatment
371	Can change biomaterial treatment	124	change_biomaterialtreatment
372	Can delete biomaterial treatment	124	delete_biomaterialtreatment
373	Can add assay biomaterial	125	add_assaybiomaterial
374	Can change assay biomaterial	125	change_assaybiomaterial
375	Can delete assay biomaterial	125	delete_assaybiomaterial
376	Can add acquisition	126	add_acquisition
377	Can change acquisition	126	change_acquisition
378	Can delete acquisition	126	delete_acquisition
379	Can add acquisition relationship	127	add_acquisitionrelationship
380	Can change acquisition relationship	127	change_acquisitionrelationship
381	Can delete acquisition relationship	127	delete_acquisitionrelationship
382	Can add acquisitionprop	128	add_acquisitionprop
383	Can change acquisitionprop	128	change_acquisitionprop
384	Can delete acquisitionprop	128	delete_acquisitionprop
385	Can add quantification	129	add_quantification
386	Can change quantification	129	change_quantification
387	Can delete quantification	129	delete_quantification
388	Can add quantificationprop	130	add_quantificationprop
389	Can change quantificationprop	130	change_quantificationprop
390	Can delete quantificationprop	130	delete_quantificationprop
391	Can add quantification relationship	131	add_quantificationrelationship
392	Can change quantification relationship	131	change_quantificationrelationship
393	Can delete quantification relationship	131	delete_quantificationrelationship
394	Can add control	132	add_control
395	Can change control	132	change_control
396	Can delete control	132	delete_control
397	Can add element	133	add_element
398	Can change element	133	change_element
399	Can delete element	133	delete_element
400	Can add elementresult	134	add_elementresult
401	Can change elementresult	134	change_elementresult
402	Can delete elementresult	134	delete_elementresult
403	Can add element relationship	135	add_elementrelationship
404	Can change element relationship	135	change_elementrelationship
405	Can delete element relationship	135	delete_elementrelationship
406	Can add study	136	add_study
407	Can change study	136	change_study
408	Can delete study	136	delete_study
409	Can add study assay	137	add_studyassay
410	Can change study assay	137	change_studyassay
411	Can delete study assay	137	delete_studyassay
412	Can add elementresult relationship	138	add_elementresultrelationship
413	Can change elementresult relationship	138	change_elementresultrelationship
414	Can delete elementresult relationship	138	delete_elementresultrelationship
415	Can add studydesign	139	add_studydesign
416	Can change studydesign	139	change_studydesign
417	Can delete studydesign	139	delete_studydesign
418	Can add studydesignprop	140	add_studydesignprop
419	Can change studydesignprop	140	change_studydesignprop
420	Can delete studydesignprop	140	delete_studydesignprop
421	Can add studyprop	141	add_studyprop
422	Can change studyprop	141	change_studyprop
423	Can delete studyprop	141	delete_studyprop
424	Can add studyprop feature	142	add_studypropfeature
425	Can change studyprop feature	142	change_studypropfeature
426	Can delete studyprop feature	142	delete_studypropfeature
427	Can add studyfactor	143	add_studyfactor
428	Can change studyfactor	143	change_studyfactor
429	Can delete studyfactor	143	delete_studyfactor
430	Can add studyfactorvalue	144	add_studyfactorvalue
431	Can change studyfactorvalue	144	change_studyfactorvalue
432	Can delete studyfactorvalue	144	delete_studyfactorvalue
433	Can add stock	145	add_stock
434	Can change stock	145	change_stock
435	Can delete stock	145	delete_stock
436	Can add stock pub	146	add_stockpub
437	Can change stock pub	146	change_stockpub
438	Can delete stock pub	146	delete_stockpub
439	Can add stock relationship	147	add_stockrelationship
440	Can change stock relationship	147	change_stockrelationship
441	Can delete stock relationship	147	delete_stockrelationship
442	Can add stock relationship pub	148	add_stockrelationshippub
443	Can change stock relationship pub	148	change_stockrelationshippub
444	Can delete stock relationship pub	148	delete_stockrelationshippub
445	Can add stockprop	149	add_stockprop
446	Can change stockprop	149	change_stockprop
447	Can delete stockprop	149	delete_stockprop
448	Can add stockprop pub	150	add_stockproppub
449	Can change stockprop pub	150	change_stockproppub
450	Can delete stockprop pub	150	delete_stockproppub
451	Can add stock dbxref	151	add_stockdbxref
452	Can change stock dbxref	151	change_stockdbxref
453	Can delete stock dbxref	151	delete_stockdbxref
454	Can add stock cvterm	152	add_stockcvterm
455	Can change stock cvterm	152	change_stockcvterm
456	Can delete stock cvterm	152	delete_stockcvterm
457	Can add stock genotype	153	add_stockgenotype
458	Can change stock genotype	153	change_stockgenotype
459	Can delete stock genotype	153	delete_stockgenotype
460	Can add stockcollection	154	add_stockcollection
461	Can change stockcollection	154	change_stockcollection
462	Can delete stockcollection	154	delete_stockcollection
463	Can add stockcollection stock	155	add_stockcollectionstock
464	Can change stockcollection stock	155	change_stockcollectionstock
465	Can delete stockcollection stock	155	delete_stockcollectionstock
466	Can add stockcollectionprop	156	add_stockcollectionprop
467	Can change stockcollectionprop	156	change_stockcollectionprop
468	Can delete stockcollectionprop	156	delete_stockcollectionprop
469	Can add library	157	add_library
470	Can change library	157	change_library
471	Can delete library	157	delete_library
472	Can add libraryprop	158	add_libraryprop
473	Can change libraryprop	158	change_libraryprop
474	Can delete libraryprop	158	delete_libraryprop
475	Can add libraryprop pub	159	add_libraryproppub
476	Can change libraryprop pub	159	change_libraryproppub
477	Can delete libraryprop pub	159	delete_libraryproppub
478	Can add library synonym	160	add_librarysynonym
479	Can change library synonym	160	change_librarysynonym
480	Can delete library synonym	160	delete_librarysynonym
481	Can add library pub	161	add_librarypub
482	Can change library pub	161	change_librarypub
483	Can delete library pub	161	delete_librarypub
484	Can add library feature	162	add_libraryfeature
485	Can change library feature	162	change_libraryfeature
486	Can delete library feature	162	delete_libraryfeature
487	Can add library cvterm	163	add_librarycvterm
488	Can change library cvterm	163	change_librarycvterm
489	Can delete library cvterm	163	delete_librarycvterm
490	Can add library dbxref	164	add_librarydbxref
491	Can change library dbxref	164	change_librarydbxref
492	Can delete library dbxref	164	delete_librarydbxref
493	Can add cell line	165	add_cellline
494	Can change cell line	165	change_cellline
495	Can delete cell line	165	delete_cellline
496	Can add cell line feature	166	add_celllinefeature
497	Can change cell line feature	166	change_celllinefeature
498	Can delete cell line feature	166	delete_celllinefeature
499	Can add cell lineprop	167	add_celllineprop
500	Can change cell lineprop	167	change_celllineprop
501	Can delete cell lineprop	167	delete_celllineprop
502	Can add cell lineprop pub	168	add_celllineproppub
503	Can change cell lineprop pub	168	change_celllineproppub
504	Can delete cell lineprop pub	168	delete_celllineproppub
505	Can add cell line relationship	169	add_celllinerelationship
506	Can change cell line relationship	169	change_celllinerelationship
507	Can delete cell line relationship	169	delete_celllinerelationship
508	Can add cell line dbxref	170	add_celllinedbxref
509	Can change cell line dbxref	170	change_celllinedbxref
510	Can delete cell line dbxref	170	delete_celllinedbxref
511	Can add cell line synonym	171	add_celllinesynonym
512	Can change cell line synonym	171	change_celllinesynonym
513	Can delete cell line synonym	171	delete_celllinesynonym
514	Can add cell line cvterm	172	add_celllinecvterm
515	Can change cell line cvterm	172	change_celllinecvterm
516	Can delete cell line cvterm	172	delete_celllinecvterm
517	Can add cell line cvtermprop	173	add_celllinecvtermprop
518	Can change cell line cvtermprop	173	change_celllinecvtermprop
519	Can delete cell line cvtermprop	173	delete_celllinecvtermprop
520	Can add feature disjoint	174	add_featuredisjoint
521	Can change feature disjoint	174	change_featuredisjoint
522	Can delete feature disjoint	174	delete_featuredisjoint
523	Can add feature union	175	add_featureunion
524	Can change feature union	175	change_featureunion
525	Can delete feature union	175	delete_featureunion
526	Can add cell line pub	176	add_celllinepub
527	Can change cell line pub	176	change_celllinepub
528	Can delete cell line pub	176	delete_celllinepub
529	Can add feature intersection	177	add_featureintersection
530	Can change feature intersection	177	change_featureintersection
531	Can delete feature intersection	177	delete_featureintersection
532	Can add feature difference	178	add_featuredifference
533	Can change feature difference	178	change_featuredifference
534	Can delete feature difference	178	delete_featuredifference
535	Can add feature distance	179	add_featuredistance
536	Can change feature distance	179	change_featuredistance
537	Can delete feature distance	179	delete_featuredistance
538	Can add cell line library	180	add_celllinelibrary
539	Can change cell line library	180	change_celllinelibrary
540	Can delete cell line library	180	delete_celllinelibrary
541	Can add gff3 view	181	add_gff3view
542	Can change gff3 view	181	change_gff3view
543	Can delete gff3 view	181	delete_gff3view
544	Can add all feature names	182	add_allfeaturenames
545	Can change all feature names	182	change_allfeaturenames
546	Can delete all feature names	182	delete_allfeaturenames
547	Can add dfeatureloc	183	add_dfeatureloc
548	Can change dfeatureloc	183	change_dfeatureloc
549	Can delete dfeatureloc	183	delete_dfeatureloc
550	Can add f type	184	add_ftype
551	Can change f type	184	change_ftype
552	Can delete f type	184	delete_ftype
553	Can add fnr type	185	add_fnrtype
554	Can change fnr type	185	change_fnrtype
555	Can delete fnr type	185	delete_fnrtype
556	Can add f loc	186	add_floc
557	Can change f loc	186	change_floc
558	Can delete f loc	186	delete_floc
559	Can add fp key	187	add_fpkey
560	Can change fp key	187	change_fpkey
561	Can delete fp key	187	delete_fpkey
562	Can add feature meets	188	add_featuremeets
563	Can change feature meets	188	change_featuremeets
564	Can delete feature meets	188	delete_featuremeets
565	Can add feature meets on same strand	189	add_featuremeetsonsamestrand
566	Can change feature meets on same strand	189	change_featuremeetsonsamestrand
567	Can delete feature meets on same strand	189	delete_featuremeetsonsamestrand
568	Can add feature contains	190	add_featurecontains
569	Can change feature contains	190	change_featurecontains
570	Can delete feature contains	190	delete_featurecontains
571	Can add featureset meets	191	add_featuresetmeets
572	Can change featureset meets	191	change_featuresetmeets
573	Can delete featureset meets	191	delete_featuresetmeets
574	Can add materialized view	192	add_materializedview
575	Can change materialized view	192	change_materializedview
576	Can delete materialized view	192	delete_materializedview
577	Can add gff sort tmp	193	add_gffsorttmp
578	Can change gff sort tmp	193	change_gffsorttmp
579	Can delete gff sort tmp	193	delete_gffsorttmp
580	Can add gff meta	194	add_gffmeta
581	Can change gff meta	194	change_gffmeta
582	Can delete gff meta	194	delete_gffmeta
583	Can add ortholog graph	195	add_orthologgraph
584	Can change ortholog graph	195	change_orthologgraph
585	Can delete ortholog graph	195	delete_orthologgraph
586	Can add tmp gff load cache	196	add_tmpgffloadcache
587	Can change tmp gff load cache	196	change_tmpgffloadcache
588	Can delete tmp gff load cache	196	delete_tmpgffloadcache
589	Can add tmp cds handler	197	add_tmpcdshandler
590	Can change tmp cds handler	197	change_tmpcdshandler
591	Can delete tmp cds handler	197	delete_tmpcdshandler
592	Can add tmp cds handler relationship	198	add_tmpcdshandlerrelationship
593	Can change tmp cds handler relationship	198	change_tmpcdshandlerrelationship
594	Can delete tmp cds handler relationship	198	delete_tmpcdshandlerrelationship
595	Can add landmark	199	add_landmark
596	Can change landmark	199	change_landmark
597	Can delete landmark	199	delete_landmark
598	Can add picture definition tag	200	add_picturedefinitiontag
599	Can change picture definition tag	200	change_picturedefinitiontag
600	Can delete picture definition tag	200	delete_picturedefinitiontag
601	Can add kv store	201	add_kvstore
602	Can change kv store	201	change_kvstore
603	Can delete kv store	201	delete_kvstore
604	Can add image	202	add_image
605	Can change image	202	change_image
606	Can delete image	202	delete_image
607	Can add genome upload	203	add_genomeupload
608	Can change genome upload	203	change_genomeupload
609	Can delete genome upload	203	delete_genomeupload
610	Can add tag color	204	add_tagcolor
611	Can change tag color	204	change_tagcolor
612	Can delete tag color	204	delete_tagcolor
613	Can add picture	205	add_picture
614	Can change picture	205	change_picture
615	Can delete picture	205	delete_picture
616	Can add picture type	206	add_picturetype
617	Can change picture type	206	change_picturetype
618	Can delete picture type	206	delete_picturetype
619	Can add picture prop	207	add_pictureprop
620	Can change picture prop	207	change_pictureprop
621	Can delete picture prop	207	delete_pictureprop
622	Can add recently viewed picture	208	add_recentlyviewedpicture
623	Can change recently viewed picture	208	change_recentlyviewedpicture
624	Can delete recently viewed picture	208	delete_recentlyviewedpicture
625	Can add tag	209	add_tag
626	Can change tag	209	change_tag
627	Can delete tag	209	delete_tag
\.


--
-- Data for Name: auth_user; Type: TABLE DATA; Schema: public; Owner: mycoplasma
--

COPY auth_user (id, username, first_name, last_name, email, password, is_staff, is_active, is_superuser, last_login, date_joined) FROM stdin;
2	balishmf	Mitchell	Balish	balishmf@muohio.edu	sha1$c8bd2$bb8b0e9c26f254a8ed0d2bf17b7676719bc6a892	t	t	t	2011-07-18 15:51:51.368252-04	2011-07-05 11:02:33-04
4	siebenmc				sha1$6ac49$43a6ac6e4a27ec163b79a38a04989675e3c298a7	t	t	f	2012-02-20 14:03:22.33559-05	2011-08-15 14:55:57-04
3	trial_not_staff	Someone	Else	someone@somewhere.com	sha1$c7cd3$f90c1945b8788f6e0ebcbb328ab6fae2fc63e737	f	t	f	2012-10-18 16:31:55.051707-04	2011-07-15 10:48:21-04
1	oberliat	Andrew	Oberlin	oberliat@muohio.edu	sha1$c51ba$9d439c085bd5d4e2a867ee85c8175fc5fb850aad	t	t	t	2012-11-02 14:30:24.188731-04	2011-06-14 17:23:27-04
\.


--
-- Data for Name: auth_user_groups; Type: TABLE DATA; Schema: public; Owner: mycoplasma
--

COPY auth_user_groups (id, user_id, group_id) FROM stdin;
\.


--
-- Data for Name: auth_user_user_permissions; Type: TABLE DATA; Schema: public; Owner: mycoplasma
--

COPY auth_user_user_permissions (id, user_id, permission_id) FROM stdin;
1	2	1
2	2	2
3	2	3
4	2	4
5	2	5
6	2	6
7	2	7
8	2	8
9	2	9
10	2	10
11	2	11
12	2	12
13	2	13
14	2	14
15	2	15
16	2	16
17	2	17
18	2	18
19	2	19
20	2	20
21	2	21
22	2	22
23	2	23
24	2	24
25	2	25
26	2	26
27	2	27
28	2	28
29	2	29
30	2	30
43	2	46
44	2	47
45	2	48
46	2	49
47	2	50
48	2	51
49	1	1
50	1	2
51	1	3
52	1	4
53	1	5
54	1	6
55	1	7
56	1	8
57	1	9
58	1	10
59	1	11
60	1	12
61	1	13
62	1	14
63	1	15
64	1	16
65	1	17
66	1	18
67	1	19
68	1	20
69	1	21
70	1	22
71	1	23
72	1	24
73	1	25
74	1	26
75	1	27
76	1	28
77	1	29
78	1	30
91	1	46
92	1	47
93	1	48
94	1	49
95	1	50
96	1	51
\.


--
-- Data for Name: django_admin_log; Type: TABLE DATA; Schema: public; Owner: mycoplasma
--

COPY django_admin_log (id, action_time, user_id, content_type_id, object_id, object_repr, action_flag, change_message) FROM stdin;
1	2011-06-14 17:52:39.394679-04	1	8	1	Dummy1	2	No fields changed.
2	2011-06-14 17:52:48.73084-04	1	8	2	Dummy2	1	
3	2011-06-14 17:52:53.544377-04	1	8	3	Dummy3	1	
4	2011-06-14 17:52:56.509594-04	1	8	4	Dummy4	1	
5	2011-06-14 17:53:05.948305-04	1	8	5	Dummy5	1	
6	2011-06-15 16:21:32.858105-04	1	10	2	Child 1.2	1	
15	2011-06-20 13:01:54.317736-04	1	8	5	Pictures	2	Changed optionName.
22	2011-06-20 17:10:56.185904-04	1	8	5	Pictures	2	Changed href.
23	2011-06-20 17:11:12.151639-04	1	8	2	Dummy2	2	Changed href.
24	2011-06-20 18:00:21.385853-04	1	8	1	Home	2	Changed optionName and href.
25	2011-06-20 18:04:46.263771-04	1	10	2	Child 1.2	2	Changed navBarOpt and href.
26	2011-06-20 18:04:52.18935-04	1	10	1	Child 1.1	2	Changed navBarOpt and href.
27	2011-06-20 18:04:58.788489-04	1	10	2	Child 3.2	2	Changed itemName.
28	2011-06-20 18:05:03.528742-04	1	10	1	Child 3.1	2	Changed itemName.
29	2011-06-20 18:31:51.933198-04	1	10	3	2.1	1	
32	2011-06-23 13:42:10.448232-04	1	16	1	Key	3	
39	2011-06-24 11:30:39.348841-04	1	16	3	Petal	3	
40	2011-06-24 11:33:17.507711-04	1	17	4	(404,70)	3	
41	2011-06-24 11:33:23.782036-04	1	16	4	Petal	3	
49	2011-06-24 12:14:18.368751-04	1	16	5	Petal	2	No fields changed.
50	2011-06-24 12:42:15.515781-04	1	16	5	Petal	3	
52	2011-06-24 12:49:35.988502-04	1	16	6	Hello	3	
53	2011-06-27 11:45:51.47587-04	1	16	2	First Tag	3	
54	2011-06-28 11:28:57.929676-04	1	16	9	TagThree	3	
55	2011-06-28 11:28:58.028916-04	1	16	8	TagTwo	3	
56	2011-06-28 11:28:58.037045-04	1	16	7	TagOne	3	
57	2011-06-28 11:36:26.858269-04	1	16	15	TagFive	3	
58	2011-06-28 11:36:26.877989-04	1	16	14	TagFour	3	
59	2011-06-28 11:36:26.886117-04	1	16	13	TagFour	3	
60	2011-06-28 11:36:26.894395-04	1	16	12	TagThree	3	
61	2011-06-28 11:36:26.902848-04	1	16	11	TagTwo	3	
62	2011-06-28 11:36:26.911025-04	1	16	10	TagOne	3	
63	2011-06-28 12:01:25.880481-04	1	16	18	TagTwo	3	
64	2011-06-28 12:01:25.902082-04	1	16	17	TagOne	3	
65	2011-06-28 12:01:25.91024-04	1	16	16	TagOne	3	
66	2011-06-28 12:12:44.382922-04	1	16	21	TagThree	3	
67	2011-06-28 12:12:44.47513-04	1	16	20	TagTwo	3	
68	2011-06-28 12:12:44.483302-04	1	16	19	TagOne	3	
69	2011-06-28 12:39:30.32523-04	1	16	29	TagEight	3	
70	2011-06-28 12:39:30.334348-04	1	16	28	TagSeven	3	
71	2011-06-28 12:39:30.342679-04	1	16	27	TagSix	3	
72	2011-06-28 12:39:30.351083-04	1	16	26	TagFive	3	
73	2011-06-28 12:39:30.359429-04	1	16	25	TagFour	3	
74	2011-06-28 12:39:30.367945-04	1	16	24	TagThree	3	
75	2011-06-28 12:39:30.376104-04	1	16	23	TagTwo	3	
76	2011-06-28 12:39:30.384439-04	1	16	22	TagOne	3	
77	2011-06-29 10:51:49.662522-04	1	16	34	Tag Trial	3	
78	2011-06-29 10:51:49.784885-04	1	16	33	This is a thingamajig	3	
79	2011-06-29 10:51:49.792996-04	1	16	32	TagThree	3	
80	2011-06-29 10:51:49.801331-04	1	16	31	TagTwo	3	
81	2011-06-29 10:51:49.809641-04	1	16	30	TagOne	3	
82	2011-06-29 11:01:21.490117-04	1	16	39	TagFive	3	
83	2011-06-29 11:01:21.506752-04	1	16	38	TagFour	3	
84	2011-06-29 11:01:21.515036-04	1	16	37	TagThree	3	
85	2011-06-29 11:01:21.523174-04	1	16	36	TagTwo	3	
86	2011-06-29 11:01:21.531664-04	1	16	35	TagOne	3	
87	2011-06-29 16:40:00.425176-04	1	16	47	This is possibly the longest tag there is in this image and I want to see how it will be rendered. 	3	
88	2011-06-29 16:40:00.438071-04	1	16	46	Anotehr tag	3	
89	2011-06-29 16:40:00.446035-04	1	16	45	Craziness	3	
90	2011-06-29 16:40:00.454431-04	1	16	44	River	3	
91	2011-06-29 16:40:00.462728-04	1	16	43	TagFour	3	
92	2011-06-29 16:40:00.471281-04	1	16	42	TagThree	3	
93	2011-06-29 16:40:00.479437-04	1	16	41	TagTwo	3	
94	2011-06-29 16:40:00.487778-04	1	16	40	TagOne	3	
98	2011-06-30 15:01:13.337045-04	1	10	3	2.1	3	
99	2011-06-30 15:01:38.94194-04	1	8	2	Gbrowse	2	Changed optionName.
100	2011-06-30 15:09:56.992078-04	1	8	2	GBrowse	2	Changed optionName.
101	2011-07-01 11:41:55.248104-04	1	8	4	Dummy4	3	
102	2011-07-01 11:41:55.364715-04	1	8	3	Dummy3	3	
108	2011-07-05 11:02:33.238016-04	1	3	2	balishmf	1	
109	2011-07-05 11:03:54.344614-04	1	3	2	balishmf	2	Changed first_name, last_name, email, is_staff, is_superuser and user_permissions.
110	2011-07-05 11:04:09.981699-04	1	3	1	oberliat	2	Changed first_name, last_name and user_permissions.
122	2011-07-06 15:43:43.594395-04	1	18	2	nc_000912.fasta	3	
123	2011-07-06 15:43:43.675697-04	1	18	1	nc_000912.fasta	3	
124	2011-07-06 18:09:29.713702-04	1	18	14	nc_000912.fasta	3	
125	2011-07-06 18:09:29.725636-04	1	18	13	nc_000912.fasta	3	
126	2011-07-06 18:09:29.733902-04	1	18	12	nc_000912.fasta	3	
127	2011-07-06 18:09:29.742421-04	1	18	11	nc_000912.fasta	3	
128	2011-07-06 18:09:29.750538-04	1	18	10	nc_000912.fasta	3	
129	2011-07-06 18:09:29.758859-04	1	18	9	nc_000912.fasta	3	
130	2011-07-06 18:09:29.767178-04	1	18	8	nc_000912.fasta	3	
131	2011-07-06 18:09:29.775729-04	1	18	7	nc_000912.fasta	3	
132	2011-07-06 18:09:29.78387-04	1	18	6	nc_000912.fasta	3	
133	2011-07-06 18:09:29.79218-04	1	18	5	nc_000912.fasta	3	
134	2011-07-06 18:09:29.800598-04	1	18	4	nc_000912.fasta	3	
135	2011-07-06 18:09:29.809117-04	1	18	3	nc_000912.fasta	3	
136	2011-07-06 19:00:07.643575-04	1	18	19	nc_000912.fasta	3	
137	2011-07-06 19:00:07.660796-04	1	18	18	nc_000912.fasta	3	
138	2011-07-06 19:00:07.668718-04	1	18	17	nc_000912.fasta	3	
139	2011-07-06 19:00:07.677332-04	1	18	16	nc_000912.fasta	3	
140	2011-07-06 19:00:07.727363-04	1	18	15	nc_000912.fasta	3	
141	2011-07-07 17:07:40.328629-04	1	8	6	BLAST	1	
142	2011-07-07 17:11:24.933791-04	1	8	6	BLAST	3	
143	2011-07-07 17:11:24.950798-04	1	8	5	Pictures	3	
144	2011-07-07 17:11:24.959271-04	1	8	2	GBrowse	3	
145	2011-07-07 17:11:24.967455-04	1	8	1	Home	3	
146	2011-07-07 17:16:32.386894-04	1	8	7	Home	1	
147	2011-07-07 17:16:50.448225-04	1	8	8	GBrowse	1	
148	2011-07-07 17:17:06.734438-04	1	8	9	BLAST	1	
149	2011-07-07 17:17:26.658759-04	1	8	10	Pictures	1	
150	2011-07-07 17:57:34.217574-04	1	199	1	NC_000908	1	
151	2011-07-07 17:58:05.436778-04	1	199	2	NC_000912	1	
152	2011-07-07 17:59:50.18674-04	1	199	3	NC_013948	1	
153	2011-07-07 18:00:33.392029-04	1	199	4	NC_011025	1	
154	2011-07-07 18:01:14.006756-04	1	199	5	NC_007633	1	
155	2011-07-07 18:02:31.113434-04	1	199	6	NC_012806	1	
156	2011-07-07 18:03:03.038583-04	1	199	7	NC_014014	1	
157	2011-07-07 18:03:58.355801-04	1	199	8	NC_004829	1	
158	2011-07-07 18:04:27.640021-04	1	199	9	NC_014970	1	
159	2011-07-07 18:05:09.721771-04	1	199	10	NC_013511	1	
160	2011-07-07 18:05:54.635716-04	1	199	11	NC_006908	1	
161	2011-07-07 18:06:25.343861-04	1	199	12	NC_005364	1	
162	2011-07-07 18:07:36.105145-04	1	199	13	NC_004432	1	
163	2011-07-07 18:08:58.092095-04	1	199	14	NC_002771	1	
164	2011-07-07 18:09:43.88373-04	1	199	15	NC_007294	1	
165	2011-07-07 18:11:08.808541-04	1	18	21	nc_000912.fasta	3	
166	2011-07-07 18:19:01.807202-04	1	18	22	nc_000912.fasta	3	
167	2011-07-13 12:03:51.247956-04	1	8	8	GBrowse	2	Changed href.
168	2011-07-15 10:48:21.200008-04	1	3	3	trial_not_staff	1	
169	2011-07-15 10:49:19.449799-04	1	3	3	trial_not_staff	2	Changed first_name, last_name and email.
170	2011-07-18 14:46:47.76957-04	1	200	1	6, Mycoplasma pneumoniae	1	
171	2011-07-22 12:10:17.186896-04	1	202	1	multiuploader_images/2SL31-mycoplasma.jpg	3	
172	2011-07-22 12:28:35.700292-04	1	202	6	multiuploader_images/2SL31-mycoplasma_2.jpg	3	
173	2011-07-22 12:28:35.743243-04	1	202	5	multiuploader_images/DatabaseBanner1.jpg	3	
174	2011-07-22 12:28:35.751416-04	1	202	4	multiuploader_images/arrow-left_1.png	3	
175	2011-07-22 12:28:35.759919-04	1	202	3	multiuploader_images/arrow-left.png	3	
176	2011-07-22 12:28:35.768206-04	1	202	2	multiuploader_images/2SL31-mycoplasma_1.jpg	3	
177	2011-07-22 14:38:40.159826-04	1	202	12	multiuploader_images/DatabaseBanner1.jpg	3	
178	2011-07-22 14:38:40.172193-04	1	202	11	multiuploader_images/2SL31-mycoplasma_4.jpg	3	
179	2011-07-22 14:38:40.180468-04	1	202	10	multiuploader_images/2SL31-mycoplasma_3.jpg	3	
180	2011-07-22 14:38:40.18872-04	1	202	9	multiuploader_images/2SL31-mycoplasma_2.jpg	3	
181	2011-07-22 14:38:40.197054-04	1	202	8	multiuploader_images/2SL31-mycoplasma_1.jpg	3	
182	2011-07-22 14:38:40.205442-04	1	202	7	multiuploader_images/2SL31-mycoplasma.jpg	3	
183	2011-07-22 14:53:07.655154-04	1	202	15	multiuploader_images/2SL31-mycoplasma_7.jpg	3	
184	2011-07-22 14:53:07.673636-04	1	202	14	multiuploader_images/2SL31-mycoplasma_6.jpg	3	
185	2011-07-22 14:53:07.681974-04	1	202	13	multiuploader_images/2SL31-mycoplasma_5.jpg	3	
186	2011-07-22 15:54:14.56506-04	1	202	36	multiuploader_images/touche_raccoon_1.jpg	3	
187	2011-07-22 15:54:14.586758-04	1	202	35	multiuploader_images/touche_raccoon.jpg	3	
188	2011-07-22 15:54:14.595055-04	1	202	34	multiuploader_images/2SL31-mycoplasma_24.jpg	3	
189	2011-07-22 15:54:14.603226-04	1	202	33	multiuploader_images/2SL31-mycoplasma_23.jpg	3	
190	2011-07-22 15:54:14.611748-04	1	202	32	multiuploader_images/2SL31-mycoplasma_22.jpg	3	
191	2011-07-22 15:54:14.619897-04	1	202	31	multiuploader_images/2SL31-mycoplasma_21.jpg	3	
192	2011-07-22 15:54:14.628219-04	1	202	30	multiuploader_images/DatabaseBanner1.png	3	
193	2011-07-22 15:54:14.636605-04	1	202	29	multiuploader_images/2SL31-mycoplasma_20.jpg	3	
194	2011-07-22 15:54:14.645065-04	1	202	28	multiuploader_images/2SL31-mycoplasma_19.jpg	3	
195	2011-07-22 15:54:14.653183-04	1	202	27	multiuploader_images/2SL31-mycoplasma_18.jpg	3	
196	2011-07-22 15:54:14.661502-04	1	202	26	multiuploader_images/2SL31-mycoplasma_17.jpg	3	
197	2011-07-22 15:54:14.66983-04	1	202	25	multiuploader_images/2SL31-mycoplasma_16.jpg	3	
198	2011-07-22 15:54:14.678322-04	1	202	24	multiuploader_images/2SL31-mycoplasma_15.jpg	3	
199	2011-07-22 15:54:14.686587-04	1	202	23	multiuploader_images/2SL31-mycoplasma_14.jpg	3	
200	2011-07-22 15:54:14.694995-04	1	202	22	multiuploader_images/lady_in_forest.jpg	3	
201	2011-07-22 15:54:14.703165-04	1	202	21	multiuploader_images/2SL31-mycoplasma_13.jpg	3	
202	2011-07-22 15:54:14.711533-04	1	202	20	multiuploader_images/2SL31-mycoplasma_12.jpg	3	
203	2011-07-22 15:54:14.719946-04	1	202	19	multiuploader_images/2SL31-mycoplasma_11.jpg	3	
204	2011-07-22 15:54:14.728126-04	1	202	18	multiuploader_images/2SL31-mycoplasma_10.jpg	3	
205	2011-07-22 15:54:14.736601-04	1	202	17	multiuploader_images/2SL31-mycoplasma_9.jpg	3	
206	2011-07-22 15:54:14.753184-04	1	202	16	multiuploader_images/2SL31-mycoplasma_8.jpg	3	
207	2011-07-25 17:43:18.145734-04	1	202	48	multiuploader_images/arrow-right.png	3	
208	2011-07-25 17:43:18.25093-04	1	202	47	multiuploader_images/DatabaseBanner1_1.jpg	3	
224	2011-07-27 14:40:24.355699-04	1	202	90	multiuploader_images/arrow-right.png	3	
225	2011-08-15 14:55:57.812614-04	1	3	4	siebenmc	1	
226	2011-08-15 14:56:14.752792-04	1	3	4	siebenmc	2	Changed is_staff.
231	2011-08-19 12:03:30.113064-04	1	202	127	multiuploader_images/c211f99aded854b0211a6c798a22394b.png	3	
241	2011-08-19 12:12:58.600313-04	1	202	135	multiuploader_images/272913d897024486748b12c7364f5edd.png	3	
244	2011-08-19 17:10:39.499849-04	1	46	12	dicty	3	
245	2011-08-19 17:10:39.512344-04	1	46	11	frog	3	
246	2011-08-19 17:10:39.520438-04	1	46	10	yeast	3	
247	2011-08-19 17:10:39.528746-04	1	46	9	rice	3	
248	2011-08-19 17:10:39.537107-04	1	46	8	zebrafish	3	
249	2011-08-19 17:10:39.545404-04	1	46	7	worm	3	
250	2011-08-19 17:10:39.553721-04	1	46	6	mouse-ear cress	3	
251	2011-08-19 17:10:39.562075-04	1	46	5	rat	3	
252	2011-08-19 17:10:39.570579-04	1	46	4	mosquito	3	
253	2011-08-19 17:10:39.578738-04	1	46	3	mouse	3	
254	2011-08-19 17:10:39.587024-04	1	46	2	fruitfly	3	
255	2011-08-19 17:10:39.595339-04	1	46	1	human	3	
256	2011-08-19 17:14:42.322731-04	1	46	56	Mycoplasma insons	1	
257	2011-08-19 17:15:11.874006-04	1	46	57	Mycoplasma gallinarium	1	
258	2011-08-19 17:15:55.068481-04	1	46	58	Mycoplasma agassizii	1	
259	2012-02-15 15:07:58.790162-05	1	46	59	Mycoplasma bovis_pg45_uid60859	3	
260	2012-02-15 15:08:09.890814-05	1	199	17	NC_014760	3	
261	2012-02-15 15:17:53.909915-05	1	46	59	Mycoplasma bovis_pg45_uid60859	3	
262	2012-02-15 15:18:02.720568-05	1	199	18	NC_014760	3	
263	2012-02-20 14:54:29.365392-05	1	46	59	Mycoplasma bovis_pg45_uid60859	3	
264	2012-02-20 15:00:48.285916-05	1	199	24	NC_014760	3	
265	2012-02-20 15:00:55.960949-05	1	199	19	NC_014760	3	
266	2012-02-20 15:05:43.247763-05	1	199	25	NC_014760	3	
267	2012-02-20 15:05:52.613343-05	1	46	59	Mycoplasma bovis_pg45_uid60859	3	
268	2012-02-20 15:12:14.973543-05	1	46	56	Mycoplasma insons	2	Changed genus.
269	2012-02-20 15:25:17.935603-05	1	46	60	Mycoplasma bovis_pg45_uid60859_temp	3	
270	2012-02-20 15:25:17.946527-05	1	46	59	Mycoplasma bovis_pg45_uid60859	3	
271	2012-02-20 15:25:35.712323-05	1	199	27	NC_014760	3	
272	2012-02-20 15:25:35.719218-05	1	199	26	NC_014760	3	
273	2012-03-12 14:44:35.933185-04	1	46	42	Mycoplasma hyorhinis HUB 1 uid51695	2	Changed species, common_name and comment.
274	2012-03-12 14:47:30.486647-04	1	46	42	Mycoplasma hyorhinis HUB 1 uid51695	2	Changed abbreviation.
275	2012-03-14 14:06:10.675761-04	1	46	42	Mycoplasma hyorhinis HUB 1 uid51695	3	
276	2012-03-30 15:12:59.625245-04	1	46	60	Mycoplasma hyorhinis hub 1 uid51695_temp	3	
277	2012-03-30 15:13:07.628833-04	1	199	52	NC_014448	3	
278	2012-03-30 15:13:32.71235-04	1	8	7	Home	2	Changed href.
279	2012-03-30 15:13:40.346278-04	1	8	8	GBrowse	2	Changed href.
280	2012-03-30 15:13:44.642354-04	1	8	9	BLAST	2	Changed href.
281	2012-03-30 15:13:49.279293-04	1	8	10	Pictures	2	Changed href.
282	2012-04-13 14:04:59.93496-04	1	46	61	Mycoplasma hyorhinis_hub_1_uid51695	3	
283	2012-04-13 14:05:12.090926-04	1	199	59	NC_014448	3	
290	2012-08-20 13:47:39.813695-04	1	8	10	Images	2	Changed optionName and href.
291	2012-10-11 13:51:28.171487-04	1	204	1	R: 256, G: 0, B: 0	1	
292	2012-10-11 13:52:03.067264-04	1	16	1	Test tag group	1	
293	2012-10-11 13:53:46.897603-04	1	17	8780	(200,300) Test tag group	1	
294	2012-10-11 13:54:00.202881-04	1	17	8781	(343,213) Test tag group	1	
295	2012-10-11 13:56:57.767637-04	1	17	8781	(343,213) Test tag group	3	
296	2012-10-11 13:56:57.782676-04	1	17	8780	(200,300) Test tag group	3	
297	2012-10-11 13:57:11.763817-04	1	16	1	Test tag group	3	
298	2012-10-15 16:00:17.758461-04	1	202	149	multiuploader_images/9d3a6cc6b9734a3354192ca8daa705d4_1.png	3	
299	2012-10-15 16:00:17.804162-04	1	202	148	multiuploader_images/9d3a6cc6b9734a3354192ca8daa705d4.png	3	
300	2012-10-15 16:02:43.344142-04	1	202	150	multiuploader_images/8978a2e09c84af067ec38b8abb493a81.png	3	
301	2012-10-17 14:49:56.393549-04	1	205	42	oberliat: pictures/9d3a6cc6b9734a3354192ca8daa705d4_3.png	3	
302	2012-10-17 14:49:56.460465-04	1	205	41	oberliat: pictures/9d3a6cc6b9734a3354192ca8daa705d4_2.png	3	
303	2012-10-17 14:49:56.468787-04	1	205	40	oberliat: pictures/9d3a6cc6b9734a3354192ca8daa705d4_1.png	3	
304	2012-10-17 14:49:56.477356-04	1	205	39	oberliat: pictures/9d3a6cc6b9734a3354192ca8daa705d4.png	3	
305	2012-10-17 14:58:25.196395-04	1	205	46	pictures/9d3a6cc6b9734a3354192ca8daa705d4_3.png	3	
306	2012-10-17 14:58:25.21533-04	1	205	45	pictures/9d3a6cc6b9734a3354192ca8daa705d4_2.png	3	
307	2012-10-17 14:58:25.223533-04	1	205	44	pictures/9d3a6cc6b9734a3354192ca8daa705d4_1.png	3	
308	2012-10-17 14:58:25.231906-04	1	205	43	pictures/9d3a6cc6b9734a3354192ca8daa705d4.png	3	
309	2012-11-05 15:09:35.86253-05	1	16	1	Andy's Super Awesome Tag Group	1	
\.


--
-- Data for Name: django_content_type; Type: TABLE DATA; Schema: public; Owner: mycoplasma
--

COPY django_content_type (id, name, app_label, model) FROM stdin;
1	permission	auth	permission
2	group	auth	group
3	user	auth	user
4	message	auth	message
5	content type	contenttypes	contenttype
6	session	sessions	session
7	site	sites	site
8	nav bar option	mycoplasma_home	navbaroption
9	log entry	admin	logentry
10	drop down item	mycoplasma_home	dropdownitem
16	tag group	mycoplasma_home	taggroup
17	tag point	mycoplasma_home	tagpoint
18	blast upload	mycoplasma_home	blastupload
19	tableinfo	mycoplasma_home	tableinfo
20	db	mycoplasma_home	db
21	dbxref	mycoplasma_home	dbxref
22	db dbxref count	mycoplasma_home	dbdbxrefcount
23	cv	mycoplasma_home	cv
24	cvterm	mycoplasma_home	cvterm
25	cvterm relationship	mycoplasma_home	cvtermrelationship
26	project	mycoplasma_home	project
27	cvtermpath	mycoplasma_home	cvtermpath
28	cv leaf	mycoplasma_home	cvleaf
29	dbxrefprop	mycoplasma_home	dbxrefprop
30	cvtermprop	mycoplasma_home	cvtermprop
31	cvtermsynonym	mycoplasma_home	cvtermsynonym
32	common ancestor cvterm	mycoplasma_home	commonancestorcvterm
33	cvterm dbxref	mycoplasma_home	cvtermdbxref
34	common descendant cvterm	mycoplasma_home	commondescendantcvterm
35	cv root	mycoplasma_home	cvroot
36	stats paths to root	mycoplasma_home	statspathstoroot
37	cv cvterm count	mycoplasma_home	cvcvtermcount
38	cv cvterm count with obs	mycoplasma_home	cvcvtermcountwithobs
39	cv link count	mycoplasma_home	cvlinkcount
40	cv path count	mycoplasma_home	cvpathcount
41	pub	mycoplasma_home	pub
42	pub relationship	mycoplasma_home	pubrelationship
43	pubprop	mycoplasma_home	pubprop
44	pub dbxref	mycoplasma_home	pubdbxref
45	pubauthor	mycoplasma_home	pubauthor
46	organism	mycoplasma_home	organism
47	organism dbxref	mycoplasma_home	organismdbxref
48	feature	mycoplasma_home	feature
49	featureloc	mycoplasma_home	featureloc
50	featureloc pub	mycoplasma_home	featurelocpub
51	organismprop	mycoplasma_home	organismprop
52	feature pub	mycoplasma_home	featurepub
53	feature pubprop	mycoplasma_home	featurepubprop
54	featureprop	mycoplasma_home	featureprop
55	feature relationship	mycoplasma_home	featurerelationship
56	feature relationship pub	mycoplasma_home	featurerelationshippub
57	featureprop pub	mycoplasma_home	featureproppub
58	feature dbxref	mycoplasma_home	featuredbxref
59	feature cvterm	mycoplasma_home	featurecvterm
60	feature cvtermprop	mycoplasma_home	featurecvtermprop
61	feature relationshipprop	mycoplasma_home	featurerelationshipprop
62	feature relationshipprop pub	mycoplasma_home	featurerelationshipproppub
63	feature cvterm pub	mycoplasma_home	featurecvtermpub
64	feature cvterm dbxref	mycoplasma_home	featurecvtermdbxref
65	synonym	mycoplasma_home	synonym
66	feature synonym	mycoplasma_home	featuresynonym
67	type feature count	mycoplasma_home	typefeaturecount
68	protein coding gene	mycoplasma_home	proteincodinggene
69	intron combined view	mycoplasma_home	introncombinedview
70	intronloc view	mycoplasma_home	intronlocview
71	analysis	mycoplasma_home	analysis
72	analysisfeature	mycoplasma_home	analysisfeature
73	analysisfeatureprop	mycoplasma_home	analysisfeatureprop
74	analysisprop	mycoplasma_home	analysisprop
75	phenotype	mycoplasma_home	phenotype
76	phenotype cvterm	mycoplasma_home	phenotypecvterm
77	feature phenotype	mycoplasma_home	featurephenotype
78	environment	mycoplasma_home	environment
79	genotype	mycoplasma_home	genotype
80	environment cvterm	mycoplasma_home	environmentcvterm
81	feature genotype	mycoplasma_home	featuregenotype
82	phenstatement	mycoplasma_home	phenstatement
83	phenotype comparison	mycoplasma_home	phenotypecomparison
84	phendesc	mycoplasma_home	phendesc
85	phenotype comparison cvterm	mycoplasma_home	phenotypecomparisoncvterm
86	featuremap	mycoplasma_home	featuremap
87	featurerange	mycoplasma_home	featurerange
88	featurepos	mycoplasma_home	featurepos
89	phylotree	mycoplasma_home	phylotree
90	phylonode	mycoplasma_home	phylonode
91	phylonode dbxref	mycoplasma_home	phylonodedbxref
92	featuremap pub	mycoplasma_home	featuremappub
93	phylotree pub	mycoplasma_home	phylotreepub
94	phylonode pub	mycoplasma_home	phylonodepub
95	phylonode organism	mycoplasma_home	phylonodeorganism
96	phylonodeprop	mycoplasma_home	phylonodeprop
97	contact	mycoplasma_home	contact
98	contact relationship	mycoplasma_home	contactrelationship
99	phylonode relationship	mycoplasma_home	phylonoderelationship
100	expression	mycoplasma_home	expression
101	expression cvterm	mycoplasma_home	expressioncvterm
102	expression cvtermprop	mycoplasma_home	expressioncvtermprop
103	expressionprop	mycoplasma_home	expressionprop
104	feature expression	mycoplasma_home	featureexpression
105	expression pub	mycoplasma_home	expressionpub
106	feature expressionprop	mycoplasma_home	featureexpressionprop
107	eimage	mycoplasma_home	eimage
108	expression image	mycoplasma_home	expressionimage
109	mageml	mycoplasma_home	mageml
110	magedocumentation	mycoplasma_home	magedocumentation
111	channel	mycoplasma_home	channel
112	protocol	mycoplasma_home	protocol
113	protocolparam	mycoplasma_home	protocolparam
114	arraydesign	mycoplasma_home	arraydesign
115	arraydesignprop	mycoplasma_home	arraydesignprop
116	assay	mycoplasma_home	assay
117	assay project	mycoplasma_home	assayproject
118	assayprop	mycoplasma_home	assayprop
119	biomaterial	mycoplasma_home	biomaterial
120	biomaterial dbxref	mycoplasma_home	biomaterialdbxref
121	biomaterial relationship	mycoplasma_home	biomaterialrelationship
122	biomaterialprop	mycoplasma_home	biomaterialprop
123	treatment	mycoplasma_home	treatment
124	biomaterial treatment	mycoplasma_home	biomaterialtreatment
125	assay biomaterial	mycoplasma_home	assaybiomaterial
126	acquisition	mycoplasma_home	acquisition
127	acquisition relationship	mycoplasma_home	acquisitionrelationship
128	acquisitionprop	mycoplasma_home	acquisitionprop
129	quantification	mycoplasma_home	quantification
130	quantificationprop	mycoplasma_home	quantificationprop
131	quantification relationship	mycoplasma_home	quantificationrelationship
132	control	mycoplasma_home	control
133	element	mycoplasma_home	element
134	elementresult	mycoplasma_home	elementresult
135	element relationship	mycoplasma_home	elementrelationship
136	study	mycoplasma_home	study
137	study assay	mycoplasma_home	studyassay
138	elementresult relationship	mycoplasma_home	elementresultrelationship
139	studydesign	mycoplasma_home	studydesign
140	studydesignprop	mycoplasma_home	studydesignprop
141	studyprop	mycoplasma_home	studyprop
142	studyprop feature	mycoplasma_home	studypropfeature
143	studyfactor	mycoplasma_home	studyfactor
144	studyfactorvalue	mycoplasma_home	studyfactorvalue
145	stock	mycoplasma_home	stock
146	stock pub	mycoplasma_home	stockpub
147	stock relationship	mycoplasma_home	stockrelationship
148	stock relationship pub	mycoplasma_home	stockrelationshippub
149	stockprop	mycoplasma_home	stockprop
150	stockprop pub	mycoplasma_home	stockproppub
151	stock dbxref	mycoplasma_home	stockdbxref
152	stock cvterm	mycoplasma_home	stockcvterm
153	stock genotype	mycoplasma_home	stockgenotype
154	stockcollection	mycoplasma_home	stockcollection
155	stockcollection stock	mycoplasma_home	stockcollectionstock
156	stockcollectionprop	mycoplasma_home	stockcollectionprop
157	library	mycoplasma_home	library
158	libraryprop	mycoplasma_home	libraryprop
159	libraryprop pub	mycoplasma_home	libraryproppub
160	library synonym	mycoplasma_home	librarysynonym
161	library pub	mycoplasma_home	librarypub
162	library feature	mycoplasma_home	libraryfeature
163	library cvterm	mycoplasma_home	librarycvterm
164	library dbxref	mycoplasma_home	librarydbxref
165	cell line	mycoplasma_home	cellline
166	cell line feature	mycoplasma_home	celllinefeature
167	cell lineprop	mycoplasma_home	celllineprop
168	cell lineprop pub	mycoplasma_home	celllineproppub
169	cell line relationship	mycoplasma_home	celllinerelationship
170	cell line dbxref	mycoplasma_home	celllinedbxref
171	cell line synonym	mycoplasma_home	celllinesynonym
172	cell line cvterm	mycoplasma_home	celllinecvterm
173	cell line cvtermprop	mycoplasma_home	celllinecvtermprop
174	feature disjoint	mycoplasma_home	featuredisjoint
175	feature union	mycoplasma_home	featureunion
176	cell line pub	mycoplasma_home	celllinepub
177	feature intersection	mycoplasma_home	featureintersection
178	feature difference	mycoplasma_home	featuredifference
179	feature distance	mycoplasma_home	featuredistance
180	cell line library	mycoplasma_home	celllinelibrary
181	gff3 view	mycoplasma_home	gff3view
182	all feature names	mycoplasma_home	allfeaturenames
183	dfeatureloc	mycoplasma_home	dfeatureloc
184	f type	mycoplasma_home	ftype
185	fnr type	mycoplasma_home	fnrtype
186	f loc	mycoplasma_home	floc
187	fp key	mycoplasma_home	fpkey
188	feature meets	mycoplasma_home	featuremeets
189	feature meets on same strand	mycoplasma_home	featuremeetsonsamestrand
190	feature contains	mycoplasma_home	featurecontains
191	featureset meets	mycoplasma_home	featuresetmeets
192	materialized view	mycoplasma_home	materializedview
193	gff sort tmp	mycoplasma_home	gffsorttmp
194	gff meta	mycoplasma_home	gffmeta
195	ortholog graph	mycoplasma_home	orthologgraph
196	tmp gff load cache	mycoplasma_home	tmpgffloadcache
197	tmp cds handler	mycoplasma_home	tmpcdshandler
198	tmp cds handler relationship	mycoplasma_home	tmpcdshandlerrelationship
199	landmark	mycoplasma_home	landmark
200	picture definition tag	mycoplasma_home	picturedefinitiontag
201	kv store	thumbnail	kvstore
202	image	multiuploader	image
203	genome upload	mycoplasma_home	genomeupload
204	tag color	mycoplasma_home	tagcolor
205	picture	mycoplasma_home	picture
206	picture type	mycoplasma_home	picturetype
207	picture prop	mycoplasma_home	pictureprop
208	recently viewed picture	mycoplasma_home	recentlyviewedpicture
209	tag	mycoplasma_home	tag
\.


--
-- Data for Name: django_session; Type: TABLE DATA; Schema: public; Owner: mycoplasma
--

COPY django_session (session_key, session_data, expire_date) FROM stdin;
eea7067be428ab1377005959fc11a597	Y2RmNDRkYTQ3ZDYzYTA2OTUxOTg5YzIyZDcxZmQ3OTJjMDU3OTBhNTqAAn1xAShVEl9hdXRoX3Vz\nZXJfYmFja2VuZHECVSlkamFuZ28uY29udHJpYi5hdXRoLmJhY2tlbmRzLk1vZGVsQmFja2VuZHED\nVQ1fYXV0aF91c2VyX2lkcQRLBHUu\n	2011-09-01 14:08:40.518721-04
49b11abf392ef220f8948080ce7bb023	MDcyYjJlODM1NGUxMDk5ZGJhNTRjZDlhYzhiMDZkODdiOTQxMTdmMzqAAn1xAShVEl9hdXRoX3Vz\nZXJfYmFja2VuZHECVSlkamFuZ28uY29udHJpYi5hdXRoLmJhY2tlbmRzLk1vZGVsQmFja2VuZHED\nVQ1fYXV0aF91c2VyX2lkcQRLAXUu\n	2011-08-10 19:07:20.201583-04
160ea5c63c8bdb7bd60821ed31e6cb50	gAJ9cQEoVRJfYXV0aF91c2VyX2JhY2tlbmRxAlUpZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5k\ncy5Nb2RlbEJhY2tlbmRxA1UNX2F1dGhfdXNlcl9pZHEESwF1LjVlZmUyNjY0NzEzOTdhMjRhNmMw\nODdjZTMxMDU1NGQy\n	2011-06-29 16:21:05.121926-04
982095523d1d48b3b6cd1b873226a41e	MDcyYjJlODM1NGUxMDk5ZGJhNTRjZDlhYzhiMDZkODdiOTQxMTdmMzqAAn1xAShVEl9hdXRoX3Vz\nZXJfYmFja2VuZHECVSlkamFuZ28uY29udHJpYi5hdXRoLmJhY2tlbmRzLk1vZGVsQmFja2VuZHED\nVQ1fYXV0aF91c2VyX2lkcQRLAXUu\n	2011-08-11 11:27:03.665972-04
ed1b3701431dbd6e06e4d3d08d1868c6	MDcyYjJlODM1NGUxMDk5ZGJhNTRjZDlhYzhiMDZkODdiOTQxMTdmMzqAAn1xAShVEl9hdXRoX3Vz\nZXJfYmFja2VuZHECVSlkamFuZ28uY29udHJpYi5hdXRoLmJhY2tlbmRzLk1vZGVsQmFja2VuZHED\nVQ1fYXV0aF91c2VyX2lkcQRLAXUu\n	2011-08-05 15:51:33.087145-04
7fb48136b0c948b5aef82e98baa594a7	MDcyYjJlODM1NGUxMDk5ZGJhNTRjZDlhYzhiMDZkODdiOTQxMTdmMzqAAn1xAShVEl9hdXRoX3Vz\nZXJfYmFja2VuZHECVSlkamFuZ28uY29udHJpYi5hdXRoLmJhY2tlbmRzLk1vZGVsQmFja2VuZHED\nVQ1fYXV0aF91c2VyX2lkcQRLAXUu\n	2011-08-11 18:24:59.261908-04
d3bb80bae1159e51ad5a6d44aae4df6d	MDcyYjJlODM1NGUxMDk5ZGJhNTRjZDlhYzhiMDZkODdiOTQxMTdmMzqAAn1xAShVEl9hdXRoX3Vz\nZXJfYmFja2VuZHECVSlkamFuZ28uY29udHJpYi5hdXRoLmJhY2tlbmRzLk1vZGVsQmFja2VuZHED\nVQ1fYXV0aF91c2VyX2lkcQRLAXUu\n	2011-08-12 11:31:08.999957-04
9e419067b692e7fa168804109df866d4	OGJkMzg1NGYxMzlhZGFhM2VhNTc4MTc2NzBkMTZiYTE1NTIyMjRkNjqAAn1xAShVEl9hdXRoX3Vz\nZXJfYmFja2VuZHECVSlkamFuZ28uY29udHJpYi5hdXRoLmJhY2tlbmRzLk1vZGVsQmFja2VuZHED\nVQ1fYXV0aF91c2VyX2lkcQRLAnUu\n	2011-08-01 15:51:51.382659-04
9063d67768181bdcd69e6c8b2d394eb8	Y2RmNDRkYTQ3ZDYzYTA2OTUxOTg5YzIyZDcxZmQ3OTJjMDU3OTBhNTqAAn1xAShVEl9hdXRoX3Vz\nZXJfYmFja2VuZHECVSlkamFuZ28uY29udHJpYi5hdXRoLmJhY2tlbmRzLk1vZGVsQmFja2VuZHED\nVQ1fYXV0aF91c2VyX2lkcQRLBHUu\n	2011-09-01 18:08:03.124622-04
6f0b3225e2f4b271d5ce2c802edc23c9	Y2RmNDRkYTQ3ZDYzYTA2OTUxOTg5YzIyZDcxZmQ3OTJjMDU3OTBhNTqAAn1xAShVEl9hdXRoX3Vz\nZXJfYmFja2VuZHECVSlkamFuZ28uY29udHJpYi5hdXRoLmJhY2tlbmRzLk1vZGVsQmFja2VuZHED\nVQ1fYXV0aF91c2VyX2lkcQRLBHUu\n	2011-09-02 11:46:25.210505-04
3b712b092844b482fdfdedee04cc0cf0	gAJ9cQEoVRJfYXV0aF91c2VyX2JhY2tlbmRxAlUpZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5k\ncy5Nb2RlbEJhY2tlbmRxA1UNX2F1dGhfdXNlcl9pZHEESwF1LjVlZmUyNjY0NzEzOTdhMjRhNmMw\nODdjZTMxMDU1NGQy\n	2011-07-04 18:04:31.439521-04
5e6315a5a43c4f95932e22e1a4c60c8f	gAJ9cQEoVRJfYXV0aF91c2VyX2JhY2tlbmRxAlUpZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5k\ncy5Nb2RlbEJhY2tlbmRxA1UNX2F1dGhfdXNlcl9pZHEESwF1LjVlZmUyNjY0NzEzOTdhMjRhNmMw\nODdjZTMxMDU1NGQy\n	2011-07-07 12:39:55.881104-04
4d2f93832b791a32a4cc9103f0d2d143	MDcyYjJlODM1NGUxMDk5ZGJhNTRjZDlhYzhiMDZkODdiOTQxMTdmMzqAAn1xAShVEl9hdXRoX3Vz\nZXJfYmFja2VuZHECVSlkamFuZ28uY29udHJpYi5hdXRoLmJhY2tlbmRzLk1vZGVsQmFja2VuZHED\nVQ1fYXV0aF91c2VyX2lkcQRLAXUu\n	2011-07-19 16:38:00.550523-04
d1b3feb17f22d0e88639154e4d155fbe	gAJ9cQEoVRJfYXV0aF91c2VyX2JhY2tlbmRxAlUpZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5k\ncy5Nb2RlbEJhY2tlbmRxA1UNX2F1dGhfdXNlcl9pZHEESwF1LjVlZmUyNjY0NzEzOTdhMjRhNmMw\nODdjZTMxMDU1NGQy\n	2011-07-08 11:14:07.396387-04
c0ccc82dbed31729dc064c8b1472bb72	Y2RmNDRkYTQ3ZDYzYTA2OTUxOTg5YzIyZDcxZmQ3OTJjMDU3OTBhNTqAAn1xAShVEl9hdXRoX3Vz\nZXJfYmFja2VuZHECVSlkamFuZ28uY29udHJpYi5hdXRoLmJhY2tlbmRzLk1vZGVsQmFja2VuZHED\nVQ1fYXV0aF91c2VyX2lkcQRLBHUu\n	2011-09-02 11:55:20.2938-04
b7bd4902748626c0065b9f14edecbd3c	Y2RmNDRkYTQ3ZDYzYTA2OTUxOTg5YzIyZDcxZmQ3OTJjMDU3OTBhNTqAAn1xAShVEl9hdXRoX3Vz\nZXJfYmFja2VuZHECVSlkamFuZ28uY29udHJpYi5hdXRoLmJhY2tlbmRzLk1vZGVsQmFja2VuZHED\nVQ1fYXV0aF91c2VyX2lkcQRLBHUu\n	2011-09-01 12:51:49.706274-04
484f21d4fcccd3ab81761d9a62ec6ee4	Y2RmNDRkYTQ3ZDYzYTA2OTUxOTg5YzIyZDcxZmQ3OTJjMDU3OTBhNTqAAn1xAShVEl9hdXRoX3Vz\nZXJfYmFja2VuZHECVSlkamFuZ28uY29udHJpYi5hdXRoLmJhY2tlbmRzLk1vZGVsQmFja2VuZHED\nVQ1fYXV0aF91c2VyX2lkcQRLBHUu\n	2011-09-02 12:37:19.000786-04
94b93bb54b5a24867affbd55f0b246a8	MDcyYjJlODM1NGUxMDk5ZGJhNTRjZDlhYzhiMDZkODdiOTQxMTdmMzqAAn1xAShVEl9hdXRoX3Vz\nZXJfYmFja2VuZHECVSlkamFuZ28uY29udHJpYi5hdXRoLmJhY2tlbmRzLk1vZGVsQmFja2VuZHED\nVQ1fYXV0aF91c2VyX2lkcQRLAXUu\n	2011-09-02 17:22:37.730118-04
439e55f8c8dad7facc8c006e1c0b2bef	MDcyYjJlODM1NGUxMDk5ZGJhNTRjZDlhYzhiMDZkODdiOTQxMTdmMzqAAn1xAShVEl9hdXRoX3Vz\nZXJfYmFja2VuZHECVSlkamFuZ28uY29udHJpYi5hdXRoLmJhY2tlbmRzLk1vZGVsQmFja2VuZHED\nVQ1fYXV0aF91c2VyX2lkcQRLAXUu\n	2011-09-02 15:59:03.528691-04
caaa29e6df05ca956d8f04827ec10e09	MDcyYjJlODM1NGUxMDk5ZGJhNTRjZDlhYzhiMDZkODdiOTQxMTdmMzqAAn1xAShVEl9hdXRoX3Vz\nZXJfYmFja2VuZHECVSlkamFuZ28uY29udHJpYi5hdXRoLmJhY2tlbmRzLk1vZGVsQmFja2VuZHED\nVQ1fYXV0aF91c2VyX2lkcQRLAXUu\n	2011-09-08 14:13:36.852297-04
a4d2a1ab99dc0b9f8868c9a867db03b5	MDcyYjJlODM1NGUxMDk5ZGJhNTRjZDlhYzhiMDZkODdiOTQxMTdmMzqAAn1xAShVEl9hdXRoX3Vz\nZXJfYmFja2VuZHECVSlkamFuZ28uY29udHJpYi5hdXRoLmJhY2tlbmRzLk1vZGVsQmFja2VuZHED\nVQ1fYXV0aF91c2VyX2lkcQRLAXUu\n	2011-08-05 19:05:26.023895-04
8ce2222844e6965df1fe3c243e49e257	MDcyYjJlODM1NGUxMDk5ZGJhNTRjZDlhYzhiMDZkODdiOTQxMTdmMzqAAn1xAShVEl9hdXRoX3Vz\nZXJfYmFja2VuZHECVSlkamFuZ28uY29udHJpYi5hdXRoLmJhY2tlbmRzLk1vZGVsQmFja2VuZHED\nVQ1fYXV0aF91c2VyX2lkcQRLAXUu\n	2011-08-05 15:50:45.775119-04
95a5de1627e26effa08274a1cf2599af	MDcyYjJlODM1NGUxMDk5ZGJhNTRjZDlhYzhiMDZkODdiOTQxMTdmMzqAAn1xAShVEl9hdXRoX3Vz\nZXJfYmFja2VuZHECVSlkamFuZ28uY29udHJpYi5hdXRoLmJhY2tlbmRzLk1vZGVsQmFja2VuZHED\nVQ1fYXV0aF91c2VyX2lkcQRLAXUu\n	2011-08-08 10:57:28.644477-04
b4704ae7e5536e348d3bfef63794ae92	MDcyYjJlODM1NGUxMDk5ZGJhNTRjZDlhYzhiMDZkODdiOTQxMTdmMzqAAn1xAShVEl9hdXRoX3Vz\nZXJfYmFja2VuZHECVSlkamFuZ28uY29udHJpYi5hdXRoLmJhY2tlbmRzLk1vZGVsQmFja2VuZHED\nVQ1fYXV0aF91c2VyX2lkcQRLAXUu\n	2011-08-10 13:38:02.693415-04
819e5a3dbb2b8374aa90ab8982c3f99d	MDcyYjJlODM1NGUxMDk5ZGJhNTRjZDlhYzhiMDZkODdiOTQxMTdmMzqAAn1xAShVEl9hdXRoX3Vz\nZXJfYmFja2VuZHECVSlkamFuZ28uY29udHJpYi5hdXRoLmJhY2tlbmRzLk1vZGVsQmFja2VuZHED\nVQ1fYXV0aF91c2VyX2lkcQRLAXUu\n	2011-08-10 16:20:21.635883-04
7d2ee883df8afbbe5f40e7c64c0700ed	NWQ0YTI1YWRiMDIyNzVmOWI4YThjZTRiNzE5NDYxZjQxOGMxN2ZmZDqAAn1xAShVCnRlc3Rjb29r\naWVxAlUGd29ya2VkcQNVEl9hdXRoX3VzZXJfYmFja2VuZHEEVSlkamFuZ28uY29udHJpYi5hdXRo\nLmJhY2tlbmRzLk1vZGVsQmFja2VuZHEFVQ1fYXV0aF91c2VyX2lkcQZLAXUu\n	2011-09-23 15:18:36.71996-04
c419db0f73b70d419b0f5e2c97323282	MDcyYjJlODM1NGUxMDk5ZGJhNTRjZDlhYzhiMDZkODdiOTQxMTdmMzqAAn1xAShVEl9hdXRoX3Vz\nZXJfYmFja2VuZHECVSlkamFuZ28uY29udHJpYi5hdXRoLmJhY2tlbmRzLk1vZGVsQmFja2VuZHED\nVQ1fYXV0aF91c2VyX2lkcQRLAXUu\n	2011-09-30 21:50:29.264877-04
c34e95ec8bb687dd39ab3f71f8ca4e20	YjQ1ZjBhNWViOGFhNmJiMDFlNjFhOTBiOGM5MWFjODVkYTFlYjk4NzqAAn1xAS4=\n	2011-10-11 12:35:24.715674-04
04ac7f4ae427512e0c72a97159095a78	MDcyYjJlODM1NGUxMDk5ZGJhNTRjZDlhYzhiMDZkODdiOTQxMTdmMzqAAn1xAShVEl9hdXRoX3Vz\nZXJfYmFja2VuZHECVSlkamFuZ28uY29udHJpYi5hdXRoLmJhY2tlbmRzLk1vZGVsQmFja2VuZHED\nVQ1fYXV0aF91c2VyX2lkcQRLAXUu\n	2011-12-02 14:55:22.235099-05
e84370222b082953f2ae25c0035efb2b	YjQ1ZjBhNWViOGFhNmJiMDFlNjFhOTBiOGM5MWFjODVkYTFlYjk4NzqAAn1xAS4=\n	2011-12-20 12:17:21.279196-05
bcbf04090d7d455c7078895c95dffd17	MDcyYjJlODM1NGUxMDk5ZGJhNTRjZDlhYzhiMDZkODdiOTQxMTdmMzqAAn1xAShVEl9hdXRoX3Vz\nZXJfYmFja2VuZHECVSlkamFuZ28uY29udHJpYi5hdXRoLmJhY2tlbmRzLk1vZGVsQmFja2VuZHED\nVQ1fYXV0aF91c2VyX2lkcQRLAXUu\n	2011-12-31 19:14:02.798985-05
1cb961721dceb14e2a53381186c61f60	Y2RmNDRkYTQ3ZDYzYTA2OTUxOTg5YzIyZDcxZmQ3OTJjMDU3OTBhNTqAAn1xAShVEl9hdXRoX3Vz\nZXJfYmFja2VuZHECVSlkamFuZ28uY29udHJpYi5hdXRoLmJhY2tlbmRzLk1vZGVsQmFja2VuZHED\nVQ1fYXV0aF91c2VyX2lkcQRLBHUu\n	2012-02-17 10:44:59.642501-05
dc6ace61cc1a686e3ae2ccf3298213d3	Y2RmNDRkYTQ3ZDYzYTA2OTUxOTg5YzIyZDcxZmQ3OTJjMDU3OTBhNTqAAn1xAShVEl9hdXRoX3Vz\nZXJfYmFja2VuZHECVSlkamFuZ28uY29udHJpYi5hdXRoLmJhY2tlbmRzLk1vZGVsQmFja2VuZHED\nVQ1fYXV0aF91c2VyX2lkcQRLBHUu\n	2012-02-17 11:23:10.411423-05
a1891bb656e76ef9e50cab5b530810bc	Y2Y2OTVlNjUzOWQ1ODFhNWY1MmM0ZDc4MTA0Y2JkYjdhNTM0YWMyNzqAAn1xAVUKdGVzdGNvb2tp\nZXECVQZ3b3JrZWRxA3Mu\n	2012-02-20 11:08:12.626304-05
689cc354b2bd8f9cae5378a7a65408ee	MDcyYjJlODM1NGUxMDk5ZGJhNTRjZDlhYzhiMDZkODdiOTQxMTdmMzqAAn1xAShVEl9hdXRoX3Vz\nZXJfYmFja2VuZHECVSlkamFuZ28uY29udHJpYi5hdXRoLmJhY2tlbmRzLk1vZGVsQmFja2VuZHED\nVQ1fYXV0aF91c2VyX2lkcQRLAXUu\n	2012-02-20 12:37:11.912165-05
f0237015852c692474d30ed121685a93	YjQ1ZjBhNWViOGFhNmJiMDFlNjFhOTBiOGM5MWFjODVkYTFlYjk4NzqAAn1xAS4=\n	2012-02-20 14:33:23.182752-05
b601ca31bf8a6c86d942afce7bd88729	ZGJmYzU0ZGQxYTVlZGY0MWIzNDkwN2VmNzVjMmViNTU0MDFhYTBmNDqAAn1xAShYEwAAAGJvdmlz\nX3BnNDVfdWlkNjA4NTlxAlUBNmNkamFuZ28uZGIubW9kZWxzLmJhc2UKbW9kZWxfdW5waWNrbGUK\ncQNjbXljb3BsYXNtYV9ob21lLmNoYWRvCk9yZ2FuaXNtCnEEXWNkamFuZ28uZGIubW9kZWxzLmJh\nc2UKc2ltcGxlX2NsYXNzX2ZhY3RvcnkKcQWHUnEGfXEHKFUHY29tbWVudHEIVQBVBl9zdGF0ZXEJ\nY2RqYW5nby5kYi5tb2RlbHMuYmFzZQpNb2RlbFN0YXRlCnEKKYFxC31xDChVBmFkZGluZ3ENiVUC\nZGJxDlUFY2hhZG9xD3ViVQtvcmdhbmlzbV9pZHEQSztVDGFiYnJldmlhdGlvbnERWBYAAABNLiBi\nb3Zpc19wZzQ1X3VpZDYwODU5cRJVC2NvbW1vbl9uYW1lcRNYHgAAAE15Y29wbGFzbWEgYm92aXNf\ncGc0NV91aWQ2MDg1OXEUVQVnZW51c3EVVQpNeWNvcGxhc21hcRZVB3NwZWNpZXNxF2gCdWJVATBY\nCQAAAHRlbXBvcmFyeXEYVQE2VRJfYXV0aF91c2VyX2JhY2tlbmRxGVUpZGphbmdvLmNvbnRyaWIu\nYXV0aC5iYWNrZW5kcy5Nb2RlbEJhY2tlbmRxGlUNX2F1dGhfdXNlcl9pZHEbSwF1Lg==\n	2012-03-05 15:47:15.740411-05
1fccae6acacf9f1a828eadc17df6f0fe	MDcyYjJlODM1NGUxMDk5ZGJhNTRjZDlhYzhiMDZkODdiOTQxMTdmMzqAAn1xAShVEl9hdXRoX3Vz\nZXJfYmFja2VuZHECVSlkamFuZ28uY29udHJpYi5hdXRoLmJhY2tlbmRzLk1vZGVsQmFja2VuZHED\nVQ1fYXV0aF91c2VyX2lkcQRLAXUu\n	2012-03-13 16:07:56.970734-04
f2934b9efa85132186efec7c67a3419a	YjQ1ZjBhNWViOGFhNmJiMDFlNjFhOTBiOGM5MWFjODVkYTFlYjk4NzqAAn1xAS4=\n	2012-03-05 14:13:22.673953-05
27f7bc3c295ca6025c61415992822e78	MDcyYjJlODM1NGUxMDk5ZGJhNTRjZDlhYzhiMDZkODdiOTQxMTdmMzqAAn1xAShVEl9hdXRoX3Vz\nZXJfYmFja2VuZHECVSlkamFuZ28uY29udHJpYi5hdXRoLmJhY2tlbmRzLk1vZGVsQmFja2VuZHED\nVQ1fYXV0aF91c2VyX2lkcQRLAXUu\n	2012-03-13 16:09:01.726658-04
9913c2888ed3d2cc0c12126b6be9933f	MDcyYjJlODM1NGUxMDk5ZGJhNTRjZDlhYzhiMDZkODdiOTQxMTdmMzqAAn1xAShVEl9hdXRoX3Vz\nZXJfYmFja2VuZHECVSlkamFuZ28uY29udHJpYi5hdXRoLmJhY2tlbmRzLk1vZGVsQmFja2VuZHED\nVQ1fYXV0aF91c2VyX2lkcQRLAXUu\n	2012-03-13 16:25:21.679485-04
fc226b22dddba06fa6ceb32976529f93	MDcyYjJlODM1NGUxMDk5ZGJhNTRjZDlhYzhiMDZkODdiOTQxMTdmMzqAAn1xAShVEl9hdXRoX3Vz\nZXJfYmFja2VuZHECVSlkamFuZ28uY29udHJpYi5hdXRoLmJhY2tlbmRzLk1vZGVsQmFja2VuZHED\nVQ1fYXV0aF91c2VyX2lkcQRLAXUu\n	2012-03-13 16:28:25.966446-04
bcfd66627385feeca34fd192028b25a5	YmM1MTNkMGIzNWJiMmI4MjI1N2VlMmVmYzEyOGIxODM1ZjYzN2FkMzqAAn1xAShVDV9hdXRoX3Vz\nZXJfaWRxAksBWBgAAABoeW9yaGluaXMgaHViIDEgdWlkNTE2OTVxA1UBNlUSX2F1dGhfdXNlcl9i\nYWNrZW5kcQRVKWRqYW5nby5jb250cmliLmF1dGguYmFja2VuZHMuTW9kZWxCYWNrZW5kcQVjZGph\nbmdvLmRiLm1vZGVscy5iYXNlCm1vZGVsX3VucGlja2xlCnEGY215Y29wbGFzbWFfaG9tZS5jaGFk\nbwpPcmdhbmlzbQpxB11jZGphbmdvLmRiLm1vZGVscy5iYXNlCnNpbXBsZV9jbGFzc19mYWN0b3J5\nCnEIh1JxCX1xCihVB2NvbW1lbnRxC1UAVQZfc3RhdGVxDGNkamFuZ28uZGIubW9kZWxzLmJhc2UK\nTW9kZWxTdGF0ZQpxDSmBcQ59cQ8oVQZhZGRpbmdxEIlVAmRicRFVBWNoYWRvcRJ1YlULb3JnYW5p\nc21faWRxE05VDGFiYnJldmlhdGlvbnEUWBgAAABNLiBsZWFjaGlpX3BnNTBfdWlkNjA4NDlxFVUL\nY29tbW9uX25hbWVxFlggAAAATXljb3BsYXNtYSBsZWFjaGlpX3BnNTBfdWlkNjA4NDlxF1UFZ2Vu\ndXNxGFUKTXljb3BsYXNtYXEZVQdzcGVjaWVzcRpYFQAAAGxlYWNoaWlfcGc1MF91aWQ2MDg0OXEb\ndWJVATBoG1UBNmgGaAddaAiHUnEcfXEdKFUHY29tbWVudHEeVQBVBl9zdGF0ZXEfaA0pgXEgfXEh\nKFUGYWRkaW5ncSKJVQJkYnEjVQVjaGFkb3EkdWJVC29yZ2FuaXNtX2lkcSVOVQxhYmJyZXZpYXRp\nb25xJlgbAAAATS4gaHlvcmhpbmlzIGh1YiAxIHVpZDUxNjk1cSdVC2NvbW1vbl9uYW1lcShYIwAA\nAE15Y29wbGFzbWEgaHlvcmhpbmlzIGh1YiAxIHVpZDUxNjk1cSlVBWdlbnVzcSpVCk15Y29wbGFz\nbWFxK1UHc3BlY2llc3EsaAN1YlUBMHUu\n	2012-03-28 14:08:14.917343-04
51d4f48aa6f3a95fc4b4c7f3fd9cecf0	MzViYTNlMjk0ZjA5NjAxODZlNjIyOWJiM2UyYmU5M2NiMmYzMDE2YTqAAn1xAShVDV9hdXRoX3Vz\nZXJfaWRxAksBWBMAAABib3Zpc19wZzQ1X3VpZDYwODU5cQNVATZYFQAAAGxlYWNoaWlfcGc0NV91\naWQ2MDg0OXEEVQE2VRJfYXV0aF91c2VyX2JhY2tlbmRxBVUpZGphbmdvLmNvbnRyaWIuYXV0aC5i\nYWNrZW5kcy5Nb2RlbEJhY2tlbmRxBlgVAAAAbGVhY2hpaSBwZzUwIHVpZDYwODQ5cQdVATZjZGph\nbmdvLmRiLm1vZGVscy5iYXNlCm1vZGVsX3VucGlja2xlCnEIY215Y29wbGFzbWFfaG9tZS5jaGFk\nbwpPcmdhbmlzbQpxCV1jZGphbmdvLmRiLm1vZGVscy5iYXNlCnNpbXBsZV9jbGFzc19mYWN0b3J5\nCnEKh1JxC31xDChVB2NvbW1lbnRxDVUAVQZfc3RhdGVxDmNkamFuZ28uZGIubW9kZWxzLmJhc2UK\nTW9kZWxTdGF0ZQpxDymBcRB9cREoVQZhZGRpbmdxEolVAmRicRNVBWNoYWRvcRR1YlULb3JnYW5p\nc21faWRxFU5VDGFiYnJldmlhdGlvbnEWWBYAAABNLiBib3Zpc19wZzQ1X3VpZDYwODU5cRdVC2Nv\nbW1vbl9uYW1lcRhYHgAAAE15Y29wbGFzbWEgYm92aXNfcGc0NV91aWQ2MDg1OXEZVQVnZW51c3Ea\nVQpNeWNvcGxhc21hcRtVB3NwZWNpZXNxHGgDdWJVATBYFQAAAGxlYWNoaWlfcGc1MF91aWQ2MDg0\nOXEdVQE2aAhoCV1oCodScR59cR8oVQdjb21tZW50cSBYAAAAAFUGX3N0YXRlcSFoDymBcSJ9cSMo\nVQZhZGRpbmdxJIlVAmRicSVVBWNoYWRvcSZ1YlULb3JnYW5pc21faWRxJ05VDGFiYnJldmlhdGlv\nbnEoWBgAAABNLiBsZWFjaGlpX3BnNTBfdWlkNjA4NDlxKVULY29tbW9uX25hbWVxKlggAAAATXlj\nb3BsYXNtYSBsZWFjaGlpX3BnNTBfdWlkNjA4NDlxK1UFZ2VudXNxLFgKAAAATXljb3BsYXNtYXEt\nVQdzcGVjaWVzcS5YFQAAAGxlYWNoaWlfcGc1MF91aWQ2MDg0OXEvdWJVATB1Lg==\n	2012-03-26 15:12:18.96835-04
019e3b747e85b696c8a233bfb746981f	YjM1ZWQ4MTQxZTgzNzMyYmVkNTFmM2Y4MWMzODE3NmRjMTYwNzNkYzqAAn1xAShVDV9hdXRoX3Vz\nZXJfaWRxAksBWBgAAABoeW9yaGluaXMgaHViIDEgdWlkNTE2OTVxA1UBNlUKdGVzdGNvb2tpZXEE\nVQZ3b3JrZWRxBVUSX2F1dGhfdXNlcl9iYWNrZW5kcQZVKWRqYW5nby5jb250cmliLmF1dGguYmFj\na2VuZHMuTW9kZWxCYWNrZW5kcQdYGAAAAG15Y29pZGVzX3NjX3BnMV91aWQ1ODAzMXEIVQE2WBYA\nAABzdWlzX2lsbGlub2lzX3VpZDYxODk3cQlVATZjZGphbmdvLmRiLm1vZGVscy5iYXNlCm1vZGVs\nX3VucGlja2xlCnEKY215Y29wbGFzbWFfaG9tZS5jaGFkbwpPcmdhbmlzbQpxC11jZGphbmdvLmRi\nLm1vZGVscy5iYXNlCnNpbXBsZV9jbGFzc19mYWN0b3J5CnEMh1JxDX1xDihVB2NvbW1lbnRxD1UA\nVQZfc3RhdGVxEGNkamFuZ28uZGIubW9kZWxzLmJhc2UKTW9kZWxTdGF0ZQpxESmBcRJ9cRMoVQZh\nZGRpbmdxFIlVAmRicRVVBWNoYWRvcRZ1YlULb3JnYW5pc21faWRxF0s7VQxhYmJyZXZpYXRpb25x\nGFgbAAAATS4gaHlvcmhpbmlzIGh1YiAxIHVpZDUxNjk1cRlVC2NvbW1vbl9uYW1lcRpYIwAAAE15\nY29wbGFzbWEgaHlvcmhpbmlzIGh1YiAxIHVpZDUxNjk1cRtVBWdlbnVzcRxVCk15Y29wbGFzbWFx\nHVUHc3BlY2llc3EeaAN1YlUBMGgKaAtdaAyHUnEffXEgKFUHY29tbWVudHEhVQBVBl9zdGF0ZXEi\naBEpgXEjfXEkKFUGYWRkaW5ncSWJVQJkYnEmVQVjaGFkb3EndWJVC29yZ2FuaXNtX2lkcShLPFUM\nYWJicmV2aWF0aW9ucSlYGQAAAE0uIHN1aXNfaWxsaW5vaXNfdWlkNjE4OTdxKlULY29tbW9uX25h\nbWVxK1ghAAAATXljb3BsYXNtYSBzdWlzX2lsbGlub2lzX3VpZDYxODk3cSxVBWdlbnVzcS1VCk15\nY29wbGFzbWFxLlUHc3BlY2llc3EvaAl1YlUBMHUu\n	2012-04-16 14:34:21.421049-04
99c2aeb4bf01f129e996aa0ceb272f78	MDcyYjJlODM1NGUxMDk5ZGJhNTRjZDlhYzhiMDZkODdiOTQxMTdmMzqAAn1xAShVEl9hdXRoX3Vz\nZXJfYmFja2VuZHECVSlkamFuZ28uY29udHJpYi5hdXRoLmJhY2tlbmRzLk1vZGVsQmFja2VuZHED\nVQ1fYXV0aF91c2VyX2lkcQRLAXUu\n	2012-04-11 17:05:03.208559-04
c68e0fe3b2a9721de61170b2d56b6d46	MDcyYjJlODM1NGUxMDk5ZGJhNTRjZDlhYzhiMDZkODdiOTQxMTdmMzqAAn1xAShVEl9hdXRoX3Vz\nZXJfYmFja2VuZHECVSlkamFuZ28uY29udHJpYi5hdXRoLmJhY2tlbmRzLk1vZGVsQmFja2VuZHED\nVQ1fYXV0aF91c2VyX2lkcQRLAXUu\n	2012-04-21 00:50:14.506873-04
ab243bed41ce2f69cea4cf185a3ca1a5	MDcyYjJlODM1NGUxMDk5ZGJhNTRjZDlhYzhiMDZkODdiOTQxMTdmMzqAAn1xAShVEl9hdXRoX3Vz\nZXJfYmFja2VuZHECVSlkamFuZ28uY29udHJpYi5hdXRoLmJhY2tlbmRzLk1vZGVsQmFja2VuZHED\nVQ1fYXV0aF91c2VyX2lkcQRLAXUu\n	2012-04-21 17:38:03.345604-04
837ac30554096bd7659105077d86a6c6	MDcyYjJlODM1NGUxMDk5ZGJhNTRjZDlhYzhiMDZkODdiOTQxMTdmMzqAAn1xAShVEl9hdXRoX3Vz\nZXJfYmFja2VuZHECVSlkamFuZ28uY29udHJpYi5hdXRoLmJhY2tlbmRzLk1vZGVsQmFja2VuZHED\nVQ1fYXV0aF91c2VyX2lkcQRLAXUu\n	2012-04-21 17:41:50.549587-04
8625d6100f8160f610d763b592d10ae5	MDcyYjJlODM1NGUxMDk5ZGJhNTRjZDlhYzhiMDZkODdiOTQxMTdmMzqAAn1xAShVEl9hdXRoX3Vz\nZXJfYmFja2VuZHECVSlkamFuZ28uY29udHJpYi5hdXRoLmJhY2tlbmRzLk1vZGVsQmFja2VuZHED\nVQ1fYXV0aF91c2VyX2lkcQRLAXUu\n	2012-04-22 21:28:41.534735-04
5480664dab4d28d39e2e8ead6e7842fc	MDIyMmZiZDhmZjc3MjFiODFkMDNkM2Q4NTUyZGUwZmRmNmEzMGU2NzqAAn1xAShYGAAAAGh5b3Jo\naW5pc19odWJfMV91aWQ1MTY5NXECVQE2VQ1fYXV0aF91c2VyX2lkcQNLAVgYAAAAaHlvcmhpbmlz\nIGh1YiAxIHVpZDUxNjk1cQRVATZVEl9hdXRoX3VzZXJfYmFja2VuZHEFVSlkamFuZ28uY29udHJp\nYi5hdXRoLmJhY2tlbmRzLk1vZGVsQmFja2VuZHEGY2RqYW5nby5kYi5tb2RlbHMuYmFzZQptb2Rl\nbF91bnBpY2tsZQpxB2NteWNvcGxhc21hX2hvbWUuY2hhZG8KT3JnYW5pc20KcQhdY2RqYW5nby5k\nYi5tb2RlbHMuYmFzZQpzaW1wbGVfY2xhc3NfZmFjdG9yeQpxCYdScQp9cQsoVQdjb21tZW50cQxV\nAFUGX3N0YXRlcQ1jZGphbmdvLmRiLm1vZGVscy5iYXNlCk1vZGVsU3RhdGUKcQ4pgXEPfXEQKFUG\nYWRkaW5ncRGJVQJkYnESVQVjaGFkb3ETdWJVC29yZ2FuaXNtX2lkcRROVQxhYmJyZXZpYXRpb25x\nFVgbAAAATS4gaHlvcmhpbmlzIGh1YiAxIHVpZDUxNjk1cRZVC2NvbW1vbl9uYW1lcRdYIwAAAE15\nY29wbGFzbWEgaHlvcmhpbmlzIGh1YiAxIHVpZDUxNjk1cRhVBWdlbnVzcRlVCk15Y29wbGFzbWFx\nGlUHc3BlY2llc3EbaAR1YlUBMFgXAAAAYWdhbGFjdGlhZV9wZzJfdWlkNjE2MTlxHFUBNmgHaAhd\naAmHUnEdfXEeKFUHY29tbWVudHEfVQBVBl9zdGF0ZXEgaA4pgXEhfXEiKFUGYWRkaW5ncSOJVQJk\nYnEkVQVjaGFkb3EldWJVC29yZ2FuaXNtX2lkcSZLPlUMYWJicmV2aWF0aW9ucSdYGgAAAE0uIGFn\nYWxhY3RpYWVfcGcyX3VpZDYxNjE5cShVC2NvbW1vbl9uYW1lcSlYIgAAAE15Y29wbGFzbWEgYWdh\nbGFjdGlhZV9wZzJfdWlkNjE2MTlxKlUFZ2VudXNxK1UKTXljb3BsYXNtYXEsVQdzcGVjaWVzcS1o\nHHViVQEwdS4=\n	2012-04-27 14:39:52.102036-04
c8d6d2ea687187707126c09ecfee98ff	MDcyYjJlODM1NGUxMDk5ZGJhNTRjZDlhYzhiMDZkODdiOTQxMTdmMzqAAn1xAShVEl9hdXRoX3Vz\nZXJfYmFja2VuZHECVSlkamFuZ28uY29udHJpYi5hdXRoLmJhY2tlbmRzLk1vZGVsQmFja2VuZHED\nVQ1fYXV0aF91c2VyX2lkcQRLAXUu\n	2012-05-02 21:58:16.723026-04
4bd75cc14f9572cd188b13251bf7fb0f	MDcyYjJlODM1NGUxMDk5ZGJhNTRjZDlhYzhiMDZkODdiOTQxMTdmMzqAAn1xAShVEl9hdXRoX3Vz\nZXJfYmFja2VuZHECVSlkamFuZ28uY29udHJpYi5hdXRoLmJhY2tlbmRzLk1vZGVsQmFja2VuZHED\nVQ1fYXV0aF91c2VyX2lkcQRLAXUu\n	2012-10-29 15:22:27.051489-04
cb43767944415b18ca56bc4c272aa554	MDcyYjJlODM1NGUxMDk5ZGJhNTRjZDlhYzhiMDZkODdiOTQxMTdmMzqAAn1xAShVEl9hdXRoX3Vz\nZXJfYmFja2VuZHECVSlkamFuZ28uY29udHJpYi5hdXRoLmJhY2tlbmRzLk1vZGVsQmFja2VuZHED\nVQ1fYXV0aF91c2VyX2lkcQRLAXUu\n	2012-11-01 16:33:41.296627-04
f61827c83b9bbb8e738b36078b433067	MDcyYjJlODM1NGUxMDk5ZGJhNTRjZDlhYzhiMDZkODdiOTQxMTdmMzqAAn1xAShVEl9hdXRoX3Vz\nZXJfYmFja2VuZHECVSlkamFuZ28uY29udHJpYi5hdXRoLmJhY2tlbmRzLk1vZGVsQmFja2VuZHED\nVQ1fYXV0aF91c2VyX2lkcQRLAXUu\n	2012-09-06 16:20:41.442395-04
29663f2f6bf20aa00a0defb5a0696705	MDcyYjJlODM1NGUxMDk5ZGJhNTRjZDlhYzhiMDZkODdiOTQxMTdmMzqAAn1xAShVEl9hdXRoX3Vz\nZXJfYmFja2VuZHECVSlkamFuZ28uY29udHJpYi5hdXRoLmJhY2tlbmRzLk1vZGVsQmFja2VuZHED\nVQ1fYXV0aF91c2VyX2lkcQRLAXUu\n	2012-09-10 11:26:43.988977-04
7872b3f06b3809bf70faad57c90da488	MDcyYjJlODM1NGUxMDk5ZGJhNTRjZDlhYzhiMDZkODdiOTQxMTdmMzqAAn1xAShVEl9hdXRoX3Vz\nZXJfYmFja2VuZHECVSlkamFuZ28uY29udHJpYi5hdXRoLmJhY2tlbmRzLk1vZGVsQmFja2VuZHED\nVQ1fYXV0aF91c2VyX2lkcQRLAXUu\n	2012-09-21 15:31:31.586186-04
b8a5bd619d9701662c752a45f53cc25d	MDcyYjJlODM1NGUxMDk5ZGJhNTRjZDlhYzhiMDZkODdiOTQxMTdmMzqAAn1xAShVEl9hdXRoX3Vz\nZXJfYmFja2VuZHECVSlkamFuZ28uY29udHJpYi5hdXRoLmJhY2tlbmRzLk1vZGVsQmFja2VuZHED\nVQ1fYXV0aF91c2VyX2lkcQRLAXUu\n	2012-10-10 15:23:50.876331-04
451803deac939c4847347251a772d799	MDcyYjJlODM1NGUxMDk5ZGJhNTRjZDlhYzhiMDZkODdiOTQxMTdmMzqAAn1xAShVEl9hdXRoX3Vz\nZXJfYmFja2VuZHECVSlkamFuZ28uY29udHJpYi5hdXRoLmJhY2tlbmRzLk1vZGVsQmFja2VuZHED\nVQ1fYXV0aF91c2VyX2lkcQRLAXUu\n	2012-10-22 13:10:34.481433-04
9c10971131be10df29c0ef4c10b0e7ea	MDcyYjJlODM1NGUxMDk5ZGJhNTRjZDlhYzhiMDZkODdiOTQxMTdmMzqAAn1xAShVEl9hdXRoX3Vz\nZXJfYmFja2VuZHECVSlkamFuZ28uY29udHJpYi5hdXRoLmJhY2tlbmRzLk1vZGVsQmFja2VuZHED\nVQ1fYXV0aF91c2VyX2lkcQRLAXUu\n	2012-10-30 13:29:17.584675-04
f7491f88b24198177f851976a4a5d6e2	MDcyYjJlODM1NGUxMDk5ZGJhNTRjZDlhYzhiMDZkODdiOTQxMTdmMzqAAn1xAShVEl9hdXRoX3Vz\nZXJfYmFja2VuZHECVSlkamFuZ28uY29udHJpYi5hdXRoLmJhY2tlbmRzLk1vZGVsQmFja2VuZHED\nVQ1fYXV0aF91c2VyX2lkcQRLAXUu\n	2012-10-22 14:40:57.504987-04
4297c663a7b30b637b1bfcfe577c342b	MDcyYjJlODM1NGUxMDk5ZGJhNTRjZDlhYzhiMDZkODdiOTQxMTdmMzqAAn1xAShVEl9hdXRoX3Vz\nZXJfYmFja2VuZHECVSlkamFuZ28uY29udHJpYi5hdXRoLmJhY2tlbmRzLk1vZGVsQmFja2VuZHED\nVQ1fYXV0aF91c2VyX2lkcQRLAXUu\n	2012-10-29 12:44:55.991284-04
46e969c8f952430f8db8b3b705463fbf	MDcyYjJlODM1NGUxMDk5ZGJhNTRjZDlhYzhiMDZkODdiOTQxMTdmMzqAAn1xAShVEl9hdXRoX3Vz\nZXJfYmFja2VuZHECVSlkamFuZ28uY29udHJpYi5hdXRoLmJhY2tlbmRzLk1vZGVsQmFja2VuZHED\nVQ1fYXV0aF91c2VyX2lkcQRLAXUu\n	2012-10-29 12:46:34.021142-04
8bcbf90e1bcd950b0ba6fa5e62d47455	MDcyYjJlODM1NGUxMDk5ZGJhNTRjZDlhYzhiMDZkODdiOTQxMTdmMzqAAn1xAShVEl9hdXRoX3Vz\nZXJfYmFja2VuZHECVSlkamFuZ28uY29udHJpYi5hdXRoLmJhY2tlbmRzLk1vZGVsQmFja2VuZHED\nVQ1fYXV0aF91c2VyX2lkcQRLAXUu\n	2012-10-29 13:30:54.63688-04
657aee02d56964a0fe9c75839d50812d	MDcyYjJlODM1NGUxMDk5ZGJhNTRjZDlhYzhiMDZkODdiOTQxMTdmMzqAAn1xAShVEl9hdXRoX3Vz\nZXJfYmFja2VuZHECVSlkamFuZ28uY29udHJpYi5hdXRoLmJhY2tlbmRzLk1vZGVsQmFja2VuZHED\nVQ1fYXV0aF91c2VyX2lkcQRLAXUu\n	2012-10-29 13:41:23.794792-04
3ad8bafd4f68b24716807beb9984c7f2	MDcyYjJlODM1NGUxMDk5ZGJhNTRjZDlhYzhiMDZkODdiOTQxMTdmMzqAAn1xAShVEl9hdXRoX3Vz\nZXJfYmFja2VuZHECVSlkamFuZ28uY29udHJpYi5hdXRoLmJhY2tlbmRzLk1vZGVsQmFja2VuZHED\nVQ1fYXV0aF91c2VyX2lkcQRLAXUu\n	2012-10-30 13:33:26.406119-04
0682987e40b26dbb50b32babc63b5060	NWQ0YTI1YWRiMDIyNzVmOWI4YThjZTRiNzE5NDYxZjQxOGMxN2ZmZDqAAn1xAShVCnRlc3Rjb29r\naWVxAlUGd29ya2VkcQNVEl9hdXRoX3VzZXJfYmFja2VuZHEEVSlkamFuZ28uY29udHJpYi5hdXRo\nLmJhY2tlbmRzLk1vZGVsQmFja2VuZHEFVQ1fYXV0aF91c2VyX2lkcQZLAXUu\n	2012-11-15 09:36:46.228803-05
c51e38e224614a45ac446c0021c0d82d	MDcyYjJlODM1NGUxMDk5ZGJhNTRjZDlhYzhiMDZkODdiOTQxMTdmMzqAAn1xAShVEl9hdXRoX3Vz\nZXJfYmFja2VuZHECVSlkamFuZ28uY29udHJpYi5hdXRoLmJhY2tlbmRzLk1vZGVsQmFja2VuZHED\nVQ1fYXV0aF91c2VyX2lkcQRLAXUu\n	2012-11-16 14:30:24.241453-05
\.


--
-- Data for Name: django_site; Type: TABLE DATA; Schema: public; Owner: mycoplasma
--

COPY django_site (id, domain, name) FROM stdin;
1	example.com	example.com
\.


--
-- Data for Name: multiuploader_image; Type: TABLE DATA; Schema: public; Owner: mycoplasma
--

COPY multiuploader_image (id, filename, image, key_data, upload_date, user_id) FROM stdin;
\.


--
-- Data for Name: mycoplasma_home_blastupload; Type: TABLE DATA; Schema: public; Owner: mycoplasma
--

COPY mycoplasma_home_blastupload (id, fasta_file, name) FROM stdin;
\.


--
-- Data for Name: mycoplasma_home_dropdownitem; Type: TABLE DATA; Schema: public; Owner: mycoplasma
--

COPY mycoplasma_home_dropdownitem (id, "itemName", "navBarOpt_id", href, rank) FROM stdin;
\.


--
-- Data for Name: mycoplasma_home_genomeupload; Type: TABLE DATA; Schema: public; Owner: mycoplasma
--

COPY mycoplasma_home_genomeupload (genbank_file, name, id) FROM stdin;
genbank_files/Tagger_4.png	Tagger.png	1
genbank_files/Tagger_5.png	Tagger.png	2
genbank_files/Tagger_4.png	Tagger.png	1
genbank_files/Tagger_5.png	Tagger.png	2
\.


--
-- Data for Name: mycoplasma_home_landmark; Type: TABLE DATA; Schema: public; Owner: mycoplasma
--

COPY mycoplasma_home_landmark (name, organism_id, id) FROM stdin;
NC_000908	15	1
NC_000912	55	2
NC_013948	17	3
NC_011025	19	4
NC_007633	28	5
NC_012806	30	6
NC_014014	32	7
NC_004829	36	8
NC_014970	38	9
NC_013511	40	10
NC_006908	45	11
NC_005364	47	12
NC_004432	49	13
NC_002771	51	14
NC_007294	53	15
NC_005364	59	55
NC_015155	60	56
NC_01448	61	60
NC_009497	62	61
\.


--
-- Data for Name: mycoplasma_home_navbaroption; Type: TABLE DATA; Schema: public; Owner: mycoplasma
--

COPY mycoplasma_home_navbaroption (id, "optionName", href, rank) FROM stdin;
7	Home	index.html	1
8	GBrowse	genome_browser	2
9	BLAST	blast	3
10	Images	images	4
\.


--
-- Data for Name: mycoplasma_home_picture; Type: TABLE DATA; Schema: public; Owner: mycoplasma
--

COPY mycoplasma_home_picture (id, description, "imageName", publication, "altText", user_id, "uploadDate", "isPrivate") FROM stdin;
31	The banner for the website	pictures/DatabaseBanner1_1.png	none	Website Banner	1	2012-10-11 10:34:28.154468-04	f
32	Mycoplasma genitalium	pictures/7567b275b9a5bb652d688f896b3e4e05.png	none	Mycoplasma genitalium	1	2012-10-11 10:34:28.154468-04	f
33	Mycoplasma mobile	pictures/272913d897024486748b12c7364f5edd.png	none	Mycoplasma mobile	1	2012-10-11 10:34:28.154468-04	f
34	Mycoplasma pneumoniae	pictures/bf18767fa2cd28aa44f101fe926131eb.png	none	Mycoplasma pneumoniae	1	2012-10-11 10:34:28.154468-04	f
35	Mycoplasma penetrans	pictures/2e3f1eccb748bd03b3f334fc601f5f59.png	none	Mycoplasma penetrans	1	2012-10-11 10:34:28.154468-04	f
36	Mycoplasma pneumoniae	pictures/65041f08998e601ccfa82998a2263198.png	none	Mycoplasma pneumoniae	1	2012-10-11 10:34:28.154468-04	f
37	Mycoplamsa agassizii	pictures/644fc7bafed9f4d66f4b5f721a2ab585.png	none	Mycoplasma agassizii	1	2012-10-11 10:34:28.154468-04	f
38	Mycoplasma gallinarium	pictures/03eeef201f51345b898237ec79c5a4b3.png	none	Mycoplasma gallinarium	1	2012-10-11 10:34:28.154468-04	f
\.


--
-- Data for Name: mycoplasma_home_picturedefinitiontag; Type: TABLE DATA; Schema: public; Owner: mycoplasma
--

COPY mycoplasma_home_picturedefinitiontag (id, picture_id, organism_id, name) FROM stdin;
8	32	15	Mycoplasma genitalium
9	33	45	Mycoplasma mobile
10	34	55	Mycoplasma pneumoniae
11	35	49	Mycoplasma penetrans
12	36	55	Mycoplasma pneumoniae
13	37	58	Mycoplasma agassizii
14	38	57	Mycoplasma gallinarium
\.


--
-- Data for Name: mycoplasma_home_pictureprop; Type: TABLE DATA; Schema: public; Owner: mycoplasma
--

COPY mycoplasma_home_pictureprop (id, picture_id_id, type_id_id) FROM stdin;
25	31	1
26	32	3
27	33	3
28	34	3
29	35	3
30	36	3
31	37	3
32	38	3
\.


--
-- Data for Name: mycoplasma_home_picturetype; Type: TABLE DATA; Schema: public; Owner: mycoplasma
--

COPY mycoplasma_home_picturetype (id, description, "imageType") FROM stdin;
1	The banner for the website	banner
2	Pictures used as icons	icon
3	Photo to be displayed as part of the database	database_photo
4	a bubble used for tagging	tag_bubble
\.


--
-- Data for Name: mycoplasma_home_recentlyviewedpicture; Type: TABLE DATA; Schema: public; Owner: mycoplasma
--

COPY mycoplasma_home_recentlyviewedpicture (picture_id, user_id, "lastDateViewed", id) FROM stdin;
33	3	2012-10-18 16:30:43.429259-04	1
\.


--
-- Data for Name: mycoplasma_home_tag; Type: TABLE DATA; Schema: public; Owner: mycoplasma
--

COPY mycoplasma_home_tag (id, description, color_id, user_id, group_id) FROM stdin;
\.


--
-- Data for Name: mycoplasma_home_tagcolor; Type: TABLE DATA; Schema: public; Owner: mycoplasma
--

COPY mycoplasma_home_tagcolor (id, red, green, blue) FROM stdin;
1	256	0	0
\.


--
-- Data for Name: mycoplasma_home_taggroup; Type: TABLE DATA; Schema: public; Owner: mycoplasma
--

COPY mycoplasma_home_taggroup (name, user_id, "dateCreated", "lastModified", id, picture_id) FROM stdin;
Andy's Super Awesome Tag Group	1	2012-11-05 15:09:35.851847-05	2012-11-05 15:09:35.851896-05	1	32
\.


--
-- Data for Name: mycoplasma_home_tagpoint; Type: TABLE DATA; Schema: public; Owner: mycoplasma
--

COPY mycoplasma_home_tagpoint (id, tag_id, "pointX", "pointY", rank) FROM stdin;
\.


--
-- Data for Name: thumbnail_kvstore; Type: TABLE DATA; Schema: public; Owner: mycoplasma
--

COPY thumbnail_kvstore (key, value) FROM stdin;
sorl-thumbnail||image||75cc9eb914e74b32fb3ed7052433887c	{"storage": "django.core.files.storage.FileSystemStorage", "name": "multiuploader_images/2SL31-mycoplasma.jpg", "size": [345, 279]}
sorl-thumbnail||image||2bee8bb6f18c716f5f684174d89fa171	{"storage": "django.core.files.storage.FileSystemStorage", "name": "cache/48/a0/48a031e32ccc84ca66970c29dc18a0e6.jpg", "size": [80, 65]}
sorl-thumbnail||thumbnails||75cc9eb914e74b32fb3ed7052433887c	["2bee8bb6f18c716f5f684174d89fa171"]
sorl-thumbnail||image||4e8951036da8ac665b8b20dbda3c22d0	{"storage": "django.core.files.storage.FileSystemStorage", "name": "multiuploader_images/2SL31-mycoplasma_1.jpg", "size": [345, 279]}
sorl-thumbnail||image||96488ffefc675f2f556e5c3c3e80bdaf	{"storage": "django.core.files.storage.FileSystemStorage", "name": "cache/0e/3b/0e3ba29fdccbf96892cc6eaea62d7fcf.jpg", "size": [80, 65]}
sorl-thumbnail||thumbnails||4e8951036da8ac665b8b20dbda3c22d0	["96488ffefc675f2f556e5c3c3e80bdaf"]
sorl-thumbnail||image||693c2fd6bbccac81cb44812b018508d2	{"storage": "django.core.files.storage.FileSystemStorage", "name": "multiuploader_images/arrow-left.png", "size": [150, 150]}
sorl-thumbnail||image||e3f733203539cf8b2e34e54024c2544a	{"storage": "django.core.files.storage.FileSystemStorage", "name": "cache/52/88/5288849b54bf059081005fcf7bea91ec.jpg", "size": [80, 80]}
sorl-thumbnail||thumbnails||693c2fd6bbccac81cb44812b018508d2	["e3f733203539cf8b2e34e54024c2544a"]
sorl-thumbnail||image||cb11f48f1c17f4dee4dfa31c982eda9a	{"storage": "django.core.files.storage.FileSystemStorage", "name": "multiuploader_images/arrow-left_1.png", "size": [150, 150]}
sorl-thumbnail||image||32ce7e0b6173f08d8b939b5c001d9612	{"storage": "django.core.files.storage.FileSystemStorage", "name": "cache/fb/fc/fbfc002268101c776d424228673359eb.jpg", "size": [80, 80]}
sorl-thumbnail||thumbnails||cb11f48f1c17f4dee4dfa31c982eda9a	["32ce7e0b6173f08d8b939b5c001d9612"]
sorl-thumbnail||image||9c093ae0d8a5b605e76b669c228391f0	{"storage": "django.core.files.storage.FileSystemStorage", "name": "multiuploader_images/DatabaseBanner1.jpg", "size": [790, 360]}
sorl-thumbnail||image||d6012e47a2a51026e8a54489d76828cd	{"storage": "django.core.files.storage.FileSystemStorage", "name": "cache/56/8d/568d2124bd1a539abbc9e5eb129d8f9b.jpg", "size": [80, 36]}
sorl-thumbnail||thumbnails||9c093ae0d8a5b605e76b669c228391f0	["d6012e47a2a51026e8a54489d76828cd"]
sorl-thumbnail||image||754dd3f4ad7c4ddcb58a38e87d099b69	{"storage": "django.core.files.storage.FileSystemStorage", "name": "multiuploader_images/2SL31-mycoplasma_2.jpg", "size": [345, 279]}
sorl-thumbnail||image||70cf99792ed5efa39a4477acbe973f3b	{"storage": "django.core.files.storage.FileSystemStorage", "name": "cache/b0/93/b093f14ee45f53002a05e0609a9d550b.jpg", "size": [80, 65]}
sorl-thumbnail||thumbnails||754dd3f4ad7c4ddcb58a38e87d099b69	["70cf99792ed5efa39a4477acbe973f3b"]
sorl-thumbnail||image||29a57bfcc7b1fce1bcec2a326fa2ef16	{"storage": "django.core.files.storage.FileSystemStorage", "name": "multiuploader_images/2SL31-mycoplasma_3.jpg", "size": [345, 279]}
sorl-thumbnail||image||e0cdfc24faf4fa563a1077ee115c2da6	{"storage": "django.core.files.storage.FileSystemStorage", "name": "cache/28/d7/28d7753ca22216c7f15564b33088c672.jpg", "size": [80, 65]}
sorl-thumbnail||thumbnails||29a57bfcc7b1fce1bcec2a326fa2ef16	["e0cdfc24faf4fa563a1077ee115c2da6"]
sorl-thumbnail||image||b0cd99048e6f63abeba74a7118ea34b4	{"storage": "django.core.files.storage.FileSystemStorage", "name": "multiuploader_images/2SL31-mycoplasma_4.jpg", "size": [345, 279]}
sorl-thumbnail||image||3f36d7c39d654775040d91673bf5f3c6	{"storage": "django.core.files.storage.FileSystemStorage", "name": "cache/67/11/67117864812434cb0ce884d25f6cc775.jpg", "size": [80, 65]}
sorl-thumbnail||thumbnails||b0cd99048e6f63abeba74a7118ea34b4	["3f36d7c39d654775040d91673bf5f3c6"]
sorl-thumbnail||image||260e25252824bb3a6ee61cc057391c3c	{"storage": "django.core.files.storage.FileSystemStorage", "name": "multiuploader_images/2SL31-mycoplasma_5.jpg", "size": [345, 279]}
sorl-thumbnail||image||d09f755d7ff882ac45788ffac869592a	{"storage": "django.core.files.storage.FileSystemStorage", "name": "cache/e5/1e/e51e0c188c76d0c38aba034b35110103.jpg", "size": [80, 65]}
sorl-thumbnail||thumbnails||260e25252824bb3a6ee61cc057391c3c	["d09f755d7ff882ac45788ffac869592a"]
sorl-thumbnail||image||3b88c773198405a456749c2edd8093e5	{"storage": "django.core.files.storage.FileSystemStorage", "name": "multiuploader_images/2SL31-mycoplasma_6.jpg", "size": [345, 279]}
sorl-thumbnail||image||4556df48c95d1e847114bdb5f2ef65fa	{"storage": "django.core.files.storage.FileSystemStorage", "name": "cache/2d/0d/2d0ddb7b9cb0cc5c0b67437136816ee2.jpg", "size": [80, 65]}
sorl-thumbnail||thumbnails||3b88c773198405a456749c2edd8093e5	["4556df48c95d1e847114bdb5f2ef65fa"]
sorl-thumbnail||image||368e9ac704d1d3a8d5e51c96a68ce289	{"storage": "django.core.files.storage.FileSystemStorage", "name": "multiuploader_images/2SL31-mycoplasma_7.jpg", "size": [345, 279]}
sorl-thumbnail||image||b27da19aada29735be3a3ed52c11f355	{"storage": "django.core.files.storage.FileSystemStorage", "name": "cache/1e/93/1e93a080c6751c49e5f4fb67defbb7d2.jpg", "size": [80, 65]}
sorl-thumbnail||thumbnails||368e9ac704d1d3a8d5e51c96a68ce289	["b27da19aada29735be3a3ed52c11f355"]
sorl-thumbnail||image||21aeca03caf1aa1c2d5c59f5421b14e3	{"storage": "django.core.files.storage.FileSystemStorage", "name": "multiuploader_images/2SL31-mycoplasma_8.jpg", "size": [345, 279]}
sorl-thumbnail||image||d68eba9c7387c3087bdde61798864787	{"storage": "django.core.files.storage.FileSystemStorage", "name": "cache/e4/ea/e4eac9c7eaf50d999f3da030c2151549.jpg", "size": [80, 65]}
sorl-thumbnail||thumbnails||21aeca03caf1aa1c2d5c59f5421b14e3	["d68eba9c7387c3087bdde61798864787"]
sorl-thumbnail||image||f18b0171e930faedd3d7fc4ed5722731	{"storage": "django.core.files.storage.FileSystemStorage", "name": "multiuploader_images/2SL31-mycoplasma_9.jpg", "size": [345, 279]}
sorl-thumbnail||image||c2d4bd44b74f2f15bed072061036a3e3	{"storage": "django.core.files.storage.FileSystemStorage", "name": "cache/15/e1/15e14bb5bd58b00466d1186af3df65b7.jpg", "size": [80, 65]}
sorl-thumbnail||thumbnails||f18b0171e930faedd3d7fc4ed5722731	["c2d4bd44b74f2f15bed072061036a3e3"]
sorl-thumbnail||image||dc7bc725857aed8c009b46e8ec11c570	{"storage": "django.core.files.storage.FileSystemStorage", "name": "multiuploader_images/2SL31-mycoplasma_10.jpg", "size": [345, 279]}
sorl-thumbnail||image||01296923f981de5805a0f867a4190238	{"storage": "django.core.files.storage.FileSystemStorage", "name": "cache/db/7f/db7f2695c0bea6e66c4343ac6b04aa2c.jpg", "size": [80, 65]}
sorl-thumbnail||thumbnails||dc7bc725857aed8c009b46e8ec11c570	["01296923f981de5805a0f867a4190238"]
sorl-thumbnail||image||bb5adbde7cf70f90e2b695d11c78dec5	{"storage": "django.core.files.storage.FileSystemStorage", "name": "multiuploader_images/2SL31-mycoplasma_11.jpg", "size": [345, 279]}
sorl-thumbnail||image||584db767698cb14835eaa5f54a7f0ce5	{"storage": "django.core.files.storage.FileSystemStorage", "name": "cache/4f/f8/4ff879631fae5e5cc5cfecfb6d3ceaee.jpg", "size": [80, 65]}
sorl-thumbnail||thumbnails||bb5adbde7cf70f90e2b695d11c78dec5	["584db767698cb14835eaa5f54a7f0ce5"]
sorl-thumbnail||image||96c652d7fddcd373108a086d19a2ac87	{"storage": "django.core.files.storage.FileSystemStorage", "name": "multiuploader_images/2SL31-mycoplasma_12.jpg", "size": [345, 279]}
sorl-thumbnail||image||90a28d1104fe60cf31d024f4e24b1e16	{"storage": "django.core.files.storage.FileSystemStorage", "name": "cache/fe/a8/fea841906d386a5eb60facd0aa33196a.jpg", "size": [80, 65]}
sorl-thumbnail||thumbnails||96c652d7fddcd373108a086d19a2ac87	["90a28d1104fe60cf31d024f4e24b1e16"]
sorl-thumbnail||image||57ba0094faf2f52cc03eeb4dc4f5ec8f	{"storage": "django.core.files.storage.FileSystemStorage", "name": "multiuploader_images/2SL31-mycoplasma_13.jpg", "size": [345, 279]}
sorl-thumbnail||image||c2237ddf74afd5f7d5351b8251633484	{"storage": "django.core.files.storage.FileSystemStorage", "name": "cache/7e/4b/7e4b08d1585cbef0879ec8c551a1d128.jpg", "size": [80, 65]}
sorl-thumbnail||thumbnails||57ba0094faf2f52cc03eeb4dc4f5ec8f	["c2237ddf74afd5f7d5351b8251633484"]
sorl-thumbnail||image||fd1d9794ff24cb9e059739ef997425c3	{"storage": "django.core.files.storage.FileSystemStorage", "name": "multiuploader_images/lady_in_forest.jpg", "size": [1280, 1024]}
sorl-thumbnail||image||802b54d272dd87ddaf683c3ec8068713	{"storage": "django.core.files.storage.FileSystemStorage", "name": "cache/3e/dd/3edd70a7a5f1cdc6b22ba839d9e2e430.jpg", "size": [80, 64]}
sorl-thumbnail||thumbnails||fd1d9794ff24cb9e059739ef997425c3	["802b54d272dd87ddaf683c3ec8068713"]
sorl-thumbnail||image||e90bbfc9c817535820638ae961d025cb	{"storage": "django.core.files.storage.FileSystemStorage", "name": "multiuploader_images/2SL31-mycoplasma_14.jpg", "size": [345, 279]}
sorl-thumbnail||image||2c308586a4cad47bb7164d48316c8afd	{"storage": "django.core.files.storage.FileSystemStorage", "name": "cache/67/db/67db341dd44eed84342084b465c2b468.jpg", "size": [80, 65]}
sorl-thumbnail||thumbnails||e90bbfc9c817535820638ae961d025cb	["2c308586a4cad47bb7164d48316c8afd"]
sorl-thumbnail||image||a30a2a4b200a0aa1c61c18135e574ab7	{"storage": "django.core.files.storage.FileSystemStorage", "name": "multiuploader_images/2SL31-mycoplasma_15.jpg", "size": [345, 279]}
sorl-thumbnail||image||616ed3b3bb4265aaeec54623655717b0	{"storage": "django.core.files.storage.FileSystemStorage", "name": "cache/14/c8/14c8dd9d8e7bfaa57637c9e63066f279.jpg", "size": [80, 65]}
sorl-thumbnail||thumbnails||a30a2a4b200a0aa1c61c18135e574ab7	["616ed3b3bb4265aaeec54623655717b0"]
sorl-thumbnail||image||48fbac27a8a6dde250cc5c731730eba2	{"storage": "django.core.files.storage.FileSystemStorage", "name": "multiuploader_images/2SL31-mycoplasma_16.jpg", "size": [345, 279]}
sorl-thumbnail||image||db025c8a87f55ff67ff14b00b960cf6b	{"storage": "django.core.files.storage.FileSystemStorage", "name": "cache/06/fe/06fe3db836878bf5c4933f5a48d067d7.jpg", "size": [80, 65]}
sorl-thumbnail||thumbnails||48fbac27a8a6dde250cc5c731730eba2	["db025c8a87f55ff67ff14b00b960cf6b"]
sorl-thumbnail||image||8de2d4f747449861b87e39fdf6e4f41c	{"storage": "django.core.files.storage.FileSystemStorage", "name": "multiuploader_images/2SL31-mycoplasma_17.jpg", "size": [345, 279]}
sorl-thumbnail||image||b8d6ba2d9947a7a8a46bb476c10da998	{"storage": "django.core.files.storage.FileSystemStorage", "name": "cache/65/61/6561d934c88ae2b5987ebf7866d75448.jpg", "size": [80, 65]}
sorl-thumbnail||thumbnails||8de2d4f747449861b87e39fdf6e4f41c	["b8d6ba2d9947a7a8a46bb476c10da998"]
sorl-thumbnail||image||7d103804c50217f52fb43fc1f6adb1da	{"storage": "django.core.files.storage.FileSystemStorage", "name": "multiuploader_images/2SL31-mycoplasma_18.jpg", "size": [345, 279]}
sorl-thumbnail||image||3235192708c7d34b836e9e400d3bc54f	{"storage": "django.core.files.storage.FileSystemStorage", "name": "cache/c4/ba/c4baed57bdd443f7483759cf9544165f.jpg", "size": [80, 65]}
sorl-thumbnail||thumbnails||7d103804c50217f52fb43fc1f6adb1da	["3235192708c7d34b836e9e400d3bc54f"]
sorl-thumbnail||image||de2574dee00ae7e93ee2f91ed901562b	{"storage": "django.core.files.storage.FileSystemStorage", "name": "multiuploader_images/2SL31-mycoplasma_19.jpg", "size": [345, 279]}
sorl-thumbnail||image||ba204fa320a4e70509e85892fbfbbb19	{"storage": "django.core.files.storage.FileSystemStorage", "name": "cache/5f/13/5f1333e3920073d233b6100222875373.jpg", "size": [80, 65]}
sorl-thumbnail||thumbnails||de2574dee00ae7e93ee2f91ed901562b	["ba204fa320a4e70509e85892fbfbbb19"]
sorl-thumbnail||image||1154a52809951f2ac5ed8d877e6acbb2	{"storage": "django.core.files.storage.FileSystemStorage", "name": "multiuploader_images/2SL31-mycoplasma_20.jpg", "size": [345, 279]}
sorl-thumbnail||image||33629342705a615ace19ae53d03660cb	{"storage": "django.core.files.storage.FileSystemStorage", "name": "cache/0d/76/0d76554ff2cff89ea8c88a6a1d626ddd.jpg", "size": [80, 65]}
sorl-thumbnail||thumbnails||1154a52809951f2ac5ed8d877e6acbb2	["33629342705a615ace19ae53d03660cb"]
sorl-thumbnail||image||697642516ed88f55dae3d303003ad1b9	{"storage": "django.core.files.storage.FileSystemStorage", "name": "multiuploader_images/DatabaseBanner1.png", "size": [310, 210]}
sorl-thumbnail||image||4e2642fd4a0ffc79d10b88bf2916a967	{"storage": "django.core.files.storage.FileSystemStorage", "name": "cache/88/af/88af723958b6ef090b590b6e9e558963.jpg", "size": [80, 54]}
sorl-thumbnail||thumbnails||697642516ed88f55dae3d303003ad1b9	["4e2642fd4a0ffc79d10b88bf2916a967"]
sorl-thumbnail||image||63cb766e0f6dcb22b2cce78eff314884	{"storage": "django.core.files.storage.FileSystemStorage", "name": "multiuploader_images/2SL31-mycoplasma_21.jpg", "size": [345, 279]}
sorl-thumbnail||image||2cb95a93bcde178a63ac8f2c9cc96a5a	{"storage": "django.core.files.storage.FileSystemStorage", "name": "cache/1c/aa/1caad6f464160559bdcb5b0a0a31a8ec.jpg", "size": [80, 65]}
sorl-thumbnail||thumbnails||63cb766e0f6dcb22b2cce78eff314884	["2cb95a93bcde178a63ac8f2c9cc96a5a"]
sorl-thumbnail||image||c769fab089884fdc308fd087f6af5354	{"storage": "django.core.files.storage.FileSystemStorage", "name": "multiuploader_images/2SL31-mycoplasma_22.jpg", "size": [345, 279]}
sorl-thumbnail||thumbnails||7a518c5d85ec9facc11c619bc57ec397	["fd9b81678a0bd7f162e5643a3209c258"]
sorl-thumbnail||image||bcb4268bce7780591783c8fe66ee19e8	{"storage": "django.core.files.storage.FileSystemStorage", "name": "cache/44/f4/44f4f4ca9c62c19974f6019a20b00265.jpg", "size": [80, 65]}
sorl-thumbnail||thumbnails||c769fab089884fdc308fd087f6af5354	["bcb4268bce7780591783c8fe66ee19e8"]
sorl-thumbnail||image||45b075b051a7bae4bdcc279bc12c928a	{"storage": "django.core.files.storage.FileSystemStorage", "name": "multiuploader_images/2SL31-mycoplasma_23.jpg", "size": [345, 279]}
sorl-thumbnail||image||0d15d9d3d43192d7a3587c0323fd2aa6	{"storage": "django.core.files.storage.FileSystemStorage", "name": "cache/61/69/6169306ab992ff07722cf601a0e52e47.jpg", "size": [80, 65]}
sorl-thumbnail||thumbnails||45b075b051a7bae4bdcc279bc12c928a	["0d15d9d3d43192d7a3587c0323fd2aa6"]
sorl-thumbnail||image||a2bf695744ba156affa3199561ec97f7	{"storage": "django.core.files.storage.FileSystemStorage", "name": "multiuploader_images/2SL31-mycoplasma_24.jpg", "size": [345, 279]}
sorl-thumbnail||image||82ae2fe484f18446557c392dc15afdd8	{"storage": "django.core.files.storage.FileSystemStorage", "name": "cache/87/56/875660dad5ec4e24371a878d9233f164.jpg", "size": [80, 65]}
sorl-thumbnail||thumbnails||a2bf695744ba156affa3199561ec97f7	["82ae2fe484f18446557c392dc15afdd8"]
sorl-thumbnail||image||9a967304bf7ea3e57f58e4ac58f1adb1	{"storage": "django.core.files.storage.FileSystemStorage", "name": "multiuploader_images/touche_raccoon.jpg", "size": [800, 600]}
sorl-thumbnail||image||20b41b8670993b6adfad3379db4b3bf9	{"storage": "django.core.files.storage.FileSystemStorage", "name": "cache/e5/07/e507baf8b9444ade205c37bedd486d79.jpg", "size": [80, 60]}
sorl-thumbnail||thumbnails||9a967304bf7ea3e57f58e4ac58f1adb1	["20b41b8670993b6adfad3379db4b3bf9"]
sorl-thumbnail||image||cd02af312e4a35b10cdbf671571ed8ea	{"storage": "django.core.files.storage.FileSystemStorage", "name": "multiuploader_images/touche_raccoon_1.jpg", "size": [800, 600]}
sorl-thumbnail||image||76ff0095333f3cf3e148a07cd310ffb8	{"storage": "django.core.files.storage.FileSystemStorage", "name": "cache/4f/08/4f08e9394b430d7da6bffe8998a5a78e.jpg", "size": [80, 60]}
sorl-thumbnail||thumbnails||cd02af312e4a35b10cdbf671571ed8ea	["76ff0095333f3cf3e148a07cd310ffb8"]
sorl-thumbnail||image||1db8bff10db12d6c186eada4f8f48056	{"storage": "django.core.files.storage.FileSystemStorage", "name": "multiuploader_images/arrow-right.png", "size": [150, 150]}
sorl-thumbnail||image||f4c8e0574de26c7014ef060893c02696	{"storage": "django.core.files.storage.FileSystemStorage", "name": "cache/a3/13/a3133445cb583ff453a0f46cf4f3cc4d.jpg", "size": [80, 80]}
sorl-thumbnail||thumbnails||1db8bff10db12d6c186eada4f8f48056	["f4c8e0574de26c7014ef060893c02696"]
sorl-thumbnail||image||b925f108d965e5680598735df97e0eb4	{"storage": "django.core.files.storage.FileSystemStorage", "name": "multiuploader_images/needle_thing.jpg", "size": [250, 201]}
sorl-thumbnail||image||3fd4606453cb411cdd774e851395516d	{"storage": "django.core.files.storage.FileSystemStorage", "name": "cache/ae/50/ae505fae4db46c7ee1b1aef668510703.jpg", "size": [80, 64]}
sorl-thumbnail||thumbnails||b925f108d965e5680598735df97e0eb4	["3fd4606453cb411cdd774e851395516d"]
sorl-thumbnail||image||97f17eca111e396600774e80f7defe9c	{"storage": "django.core.files.storage.FileSystemStorage", "name": "multiuploader_images/floral-paintings.jpg", "size": [400, 299]}
sorl-thumbnail||image||fef771ced92db6b24ee8ae5cd81a79ca	{"storage": "django.core.files.storage.FileSystemStorage", "name": "cache/43/fe/43fe241d73c583132621bb16643e348d.jpg", "size": [80, 60]}
sorl-thumbnail||thumbnails||97f17eca111e396600774e80f7defe9c	["fef771ced92db6b24ee8ae5cd81a79ca"]
sorl-thumbnail||image||8949c706f622265f1e6e44bb8f0f7392	{"storage": "django.core.files.storage.FileSystemStorage", "name": "multiuploader_images/electronmicrograph.jpg", "size": [369, 335]}
sorl-thumbnail||image||9924ed9b727f5a9d41cf9d6c21f24b42	{"storage": "django.core.files.storage.FileSystemStorage", "name": "cache/2f/33/2f332d0934bd0259d61bba7d1df1d58c.jpg", "size": [80, 73]}
sorl-thumbnail||thumbnails||8949c706f622265f1e6e44bb8f0f7392	["9924ed9b727f5a9d41cf9d6c21f24b42"]
sorl-thumbnail||image||8c2f602f2b92b07a2dd3f645d71eab8b	{"storage": "django.core.files.storage.FileSystemStorage", "name": "multiuploader_images/DatabaseBanner1_1.jpg", "size": [790, 360]}
sorl-thumbnail||image||eee2a974684100994fe1c8ea0fcc0a30	{"storage": "django.core.files.storage.FileSystemStorage", "name": "cache/7e/72/7e72d5b9c1bdf77b60f1007994a5a982.jpg", "size": [80, 36]}
sorl-thumbnail||thumbnails||8c2f602f2b92b07a2dd3f645d71eab8b	["eee2a974684100994fe1c8ea0fcc0a30"]
sorl-thumbnail||image||20b7a3c20e3ea54887a8fd4223aa82e1	{"storage": "django.core.files.storage.FileSystemStorage", "name": "multiuploader_images/rectButtonIcon.png", "size": [168, 155]}
sorl-thumbnail||image||22ffa6ca7401312b8c54a0574a8b9807	{"storage": "django.core.files.storage.FileSystemStorage", "name": "cache/29/d1/29d16ee4bcf88bb20072f07b8e176298.jpg", "size": [80, 74]}
sorl-thumbnail||thumbnails||20b7a3c20e3ea54887a8fd4223aa82e1	["22ffa6ca7401312b8c54a0574a8b9807"]
sorl-thumbnail||image||6f2d623ad430ce120d4f040ca7d0782a	{"storage": "django.core.files.storage.FileSystemStorage", "name": "multiuploader_images/mycoplasma_cultures.gif", "size": [443, 386]}
sorl-thumbnail||image||ef3ab31f88c7460efb38b0f3c60f066e	{"storage": "django.core.files.storage.FileSystemStorage", "name": "cache/61/00/61002dfab40d2836ebc34902189eb13d.jpg", "size": [80, 70]}
sorl-thumbnail||thumbnails||6f2d623ad430ce120d4f040ca7d0782a	["ef3ab31f88c7460efb38b0f3c60f066e"]
sorl-thumbnail||image||8f228afd040aaf42e69c97bbd1359f32	{"storage": "django.core.files.storage.FileSystemStorage", "name": "multiuploader_images/mycoplasma.jpg", "size": [400, 556]}
sorl-thumbnail||image||72b9d79d3ca6b3102471c4a148800ca0	{"storage": "django.core.files.storage.FileSystemStorage", "name": "cache/3a/fc/3afc9576038af09d15fbdaddeca53654.jpg", "size": [58, 80]}
sorl-thumbnail||thumbnails||8f228afd040aaf42e69c97bbd1359f32	["72b9d79d3ca6b3102471c4a148800ca0"]
sorl-thumbnail||image||78f880ea42f2dc68e62489d20a994c03	{"storage": "django.core.files.storage.FileSystemStorage", "name": "multiuploader_images/polygonButtonIcon.png", "size": [256, 256]}
sorl-thumbnail||image||1958d97ca426ee19f8bee57d8c70a1df	{"storage": "django.core.files.storage.FileSystemStorage", "name": "cache/aa/1d/aa1dd8449ef04d4f16873293298aa0cc.jpg", "size": [80, 80]}
sorl-thumbnail||thumbnails||78f880ea42f2dc68e62489d20a994c03	["1958d97ca426ee19f8bee57d8c70a1df"]
sorl-thumbnail||image||8ad9493223f029a75ebd65bb7f406847	{"storage": "django.core.files.storage.FileSystemStorage", "name": "multiuploader_images/arrow-right_1.png", "size": [150, 150]}
sorl-thumbnail||image||7d45cd042a678a21f64c45455bf1dc0c	{"storage": "django.core.files.storage.FileSystemStorage", "name": "cache/57/75/5775d739ff1f3aaa085b73ce5afe6a5b.jpg", "size": [80, 80]}
sorl-thumbnail||thumbnails||8ad9493223f029a75ebd65bb7f406847	["7d45cd042a678a21f64c45455bf1dc0c"]
sorl-thumbnail||image||2e69c663da8a83b6991567e277e684ac	{"storage": "django.core.files.storage.FileSystemStorage", "name": "multiuploader_images/CatherinPhoto.jpg", "size": [180, 119]}
sorl-thumbnail||image||00b472fe170713056e2dfa201298da53	{"storage": "django.core.files.storage.FileSystemStorage", "name": "cache/aa/76/aa76bdbdb7342e4ffa5811a7e132c94d.jpg", "size": [80, 53]}
sorl-thumbnail||thumbnails||2e69c663da8a83b6991567e277e684ac	["00b472fe170713056e2dfa201298da53"]
sorl-thumbnail||image||bf99af8b5c302978d301fb3d2dc80d01	{"storage": "django.core.files.storage.FileSystemStorage", "name": "multiuploader_images/Mycoplasma_mobile.JPG", "size": [156, 217]}
sorl-thumbnail||image||8e6ec05641b77144b4cc4ccbd956148e	{"storage": "django.core.files.storage.FileSystemStorage", "name": "cache/5b/82/5b82903bc490a0cbe5b7c335da350aa0.jpg", "size": [58, 80]}
sorl-thumbnail||thumbnails||bf99af8b5c302978d301fb3d2dc80d01	["8e6ec05641b77144b4cc4ccbd956148e"]
sorl-thumbnail||image||fa061e5bc66b990ef52a9f9651622534	{"storage": "django.core.files.storage.FileSystemStorage", "name": "multiuploader_images/M._pneumo_M129_20K_a.tif", "size": [1024, 768]}
sorl-thumbnail||image||08ead9d1f6634a31c9559483afe9591a	{"storage": "django.core.files.storage.FileSystemStorage", "name": "cache/d1/d2/d1d24129570416055b7c6ed345a9cd89.jpg", "size": [80, 60]}
sorl-thumbnail||thumbnails||fa061e5bc66b990ef52a9f9651622534	["08ead9d1f6634a31c9559483afe9591a"]
sorl-thumbnail||image||f457a55dcd758afafc5a07fcd48b967d	{"storage": "django.core.files.storage.FileSystemStorage", "name": "multiuploader_images/M._pneumo_M129_20K_a_1.tif", "size": [1024, 768]}
sorl-thumbnail||image||896661023357d28d0d28a01023262451	{"storage": "django.core.files.storage.FileSystemStorage", "name": "cache/07/e8/07e8702636f4d7eaa648cf5639b036c5.jpg", "size": [80, 60]}
sorl-thumbnail||thumbnails||f457a55dcd758afafc5a07fcd48b967d	["896661023357d28d0d28a01023262451"]
sorl-thumbnail||image||4d37189fc94ded9e45275830beac8d28	{"storage": "django.core.files.storage.FileSystemStorage", "name": "multiuploader_images/M._pneumo_M129_20K_a_2.tif", "size": [1024, 768]}
sorl-thumbnail||image||591a9d224c10fb9307d6d817ae48a20f	{"storage": "django.core.files.storage.FileSystemStorage", "name": "cache/61/44/6144826be0ac833022096bf801eac185.jpg", "size": [80, 60]}
sorl-thumbnail||thumbnails||4d37189fc94ded9e45275830beac8d28	["591a9d224c10fb9307d6d817ae48a20f"]
sorl-thumbnail||image||135dbc0d6a3ba9174ddaac25fff2160d	{"storage": "django.core.files.storage.FileSystemStorage", "name": "multiuploader_images/M.gallinarum_5K-h1.tif", "size": [250, 250]}
sorl-thumbnail||image||087f749c5cd1c284df35cf8873b013d8	{"storage": "django.core.files.storage.FileSystemStorage", "name": "cache/91/3b/913bf9d7720e149cc419be3483eb8752.jpg", "size": [80, 80]}
sorl-thumbnail||thumbnails||135dbc0d6a3ba9174ddaac25fff2160d	["087f749c5cd1c284df35cf8873b013d8"]
sorl-thumbnail||image||5ebd0f84e0b498fdecf1ec944755f3c3	{"storage": "django.core.files.storage.FileSystemStorage", "name": "multiuploader_images/M.genitalium_5K-d1.tif", "size": [250, 250]}
sorl-thumbnail||image||7da6fd98ac89b0b948d40db66bef813e	{"storage": "django.core.files.storage.FileSystemStorage", "name": "cache/60/cf/60cf9a88899a9ad1d3981a333d759849.jpg", "size": [80, 80]}
sorl-thumbnail||thumbnails||5ebd0f84e0b498fdecf1ec944755f3c3	["7da6fd98ac89b0b948d40db66bef813e"]
sorl-thumbnail||image||adb96766f5777c09c0d439ac879c19b6	{"storage": "django.core.files.storage.FileSystemStorage", "name": "multiuploader_images/M.insons_5K-C1.tif", "size": [250, 250]}
sorl-thumbnail||image||bb92854616b036502855ddcc4250837d	{"storage": "django.core.files.storage.FileSystemStorage", "name": "cache/99/05/990576f6390e1b7798a7043a1e6b34e8.jpg", "size": [80, 80]}
sorl-thumbnail||thumbnails||adb96766f5777c09c0d439ac879c19b6	["bb92854616b036502855ddcc4250837d"]
sorl-thumbnail||image||fd08a69b5a2f24e6efdb56bac5df0cab	{"storage": "django.core.files.storage.FileSystemStorage", "name": "multiuploader_images/M.penetrans_5K-b1.tif", "size": [250, 250]}
sorl-thumbnail||image||aa78aedb90546ee964fba6f445f5bce4	{"storage": "django.core.files.storage.FileSystemStorage", "name": "cache/56/30/56308be6a5d18d97b905c228c45d0989.jpg", "size": [80, 80]}
sorl-thumbnail||thumbnails||fd08a69b5a2f24e6efdb56bac5df0cab	["aa78aedb90546ee964fba6f445f5bce4"]
sorl-thumbnail||image||73ef5f7c2763b0554d441b079994c083	{"storage": "django.core.files.storage.FileSystemStorage", "name": "multiuploader_images/M.pneumoniae_5K-c1.tif", "size": [250, 250]}
sorl-thumbnail||image||5e19aa3757457d521e34b5eda6d647a6	{"storage": "django.core.files.storage.FileSystemStorage", "name": "cache/48/45/4845415bd61ee83b5a08ad4f54df666f.jpg", "size": [80, 80]}
sorl-thumbnail||thumbnails||73ef5f7c2763b0554d441b079994c083	["5e19aa3757457d521e34b5eda6d647a6"]
sorl-thumbnail||image||6ef8657ab7755d087bac3b3c60f505b0	{"storage": "django.core.files.storage.FileSystemStorage", "name": "multiuploader_images/Mycoplasma_agassizii.JPG", "size": [131, 244]}
sorl-thumbnail||image||c51fe828487b9daf560343c5b1ff7c30	{"storage": "django.core.files.storage.FileSystemStorage", "name": "cache/bc/6d/bc6da3577e6e60e6d82812bafd179510.jpg", "size": [43, 80]}
sorl-thumbnail||thumbnails||6ef8657ab7755d087bac3b3c60f505b0	["c51fe828487b9daf560343c5b1ff7c30"]
sorl-thumbnail||image||19d6a97b4dbec418e08ce164490cc26f	{"storage": "django.core.files.storage.FileSystemStorage", "name": "multiuploader_images/Mycoplasma_genitalium.JPG", "size": [250, 250]}
sorl-thumbnail||image||9c74fd857a5be7fa8c414c5ffe619d5c	{"storage": "django.core.files.storage.FileSystemStorage", "name": "cache/1e/08/1e0816b19717ae883bc9a84da8a6d66a.jpg", "size": [80, 80]}
sorl-thumbnail||thumbnails||19d6a97b4dbec418e08ce164490cc26f	["9c74fd857a5be7fa8c414c5ffe619d5c"]
sorl-thumbnail||image||1f7c021a06c83117ed786addc33ed419	{"storage": "django.core.files.storage.FileSystemStorage", "name": "multiuploader_images/Mycoplasma_insons.JPG", "size": [107, 111]}
sorl-thumbnail||image||cb582fdcd21c2dfc5cf2abf87b112bce	{"storage": "django.core.files.storage.FileSystemStorage", "name": "cache/29/6c/296c67032794bd72a27d672f0edba685.jpg", "size": [77, 80]}
sorl-thumbnail||thumbnails||1f7c021a06c83117ed786addc33ed419	["cb582fdcd21c2dfc5cf2abf87b112bce"]
sorl-thumbnail||image||722552fd86fe54ec681224514ab8f651	{"storage": "django.core.files.storage.FileSystemStorage", "name": "multiuploader_images/Mycoplasma_iowae_dividing.JPG", "size": [178, 196]}
sorl-thumbnail||image||9e134be9c9c61c7bd75af1f663f2bd75	{"storage": "django.core.files.storage.FileSystemStorage", "name": "cache/6b/2e/6b2e2389626503dfd5c0538c9376dba1.jpg", "size": [73, 80]}
sorl-thumbnail||thumbnails||722552fd86fe54ec681224514ab8f651	["9e134be9c9c61c7bd75af1f663f2bd75"]
sorl-thumbnail||image||430b833ce266e6f9ff6ec0eacc5c105d	{"storage": "django.core.files.storage.FileSystemStorage", "name": "multiuploader_images/M._pneumo_M129_20K_a_3.tif", "size": [1024, 768]}
sorl-thumbnail||image||652c849a9bded5557353bf8cd2540052	{"storage": "django.core.files.storage.FileSystemStorage", "name": "cache/d9/25/d92599b6537451642bbc9af1ccf4d38f.jpg", "size": [80, 60]}
sorl-thumbnail||thumbnails||430b833ce266e6f9ff6ec0eacc5c105d	["652c849a9bded5557353bf8cd2540052"]
sorl-thumbnail||image||4ab6a7a86b3b3756bb7a5c5666e59b1a	{"storage": "django.core.files.storage.FileSystemStorage", "name": "multiuploader_images/M.pneumoniae_5K-c1_1.tif", "size": [250, 250]}
sorl-thumbnail||image||9d79229499c9e71b96caf37aa0813247	{"storage": "django.core.files.storage.FileSystemStorage", "name": "cache/6a/55/6a55833215d08dae9124d4dd7c0bc97e.jpg", "size": [80, 80]}
sorl-thumbnail||thumbnails||4ab6a7a86b3b3756bb7a5c5666e59b1a	["9d79229499c9e71b96caf37aa0813247"]
sorl-thumbnail||image||1d6df611afb9b62757ed62a801bf3b1d	{"storage": "django.core.files.storage.FileSystemStorage", "name": "multiuploader_images/M.pneumoniae_5K-c1_2.tif", "size": [250, 250]}
sorl-thumbnail||image||7c5ece92b51f2f4e2318eca437bee416	{"storage": "django.core.files.storage.FileSystemStorage", "name": "cache/36/4b/364b29f4d43cc9f3a35dc49727547152.jpg", "size": [80, 80]}
sorl-thumbnail||thumbnails||1d6df611afb9b62757ed62a801bf3b1d	["7c5ece92b51f2f4e2318eca437bee416"]
sorl-thumbnail||image||f202f5a33d1c2c5a9ddb5cab6ffd7c32	{"storage": "django.core.files.storage.FileSystemStorage", "name": "multiuploader_images/bc2abbb1f8778e518fdebab434fa3d03.png", "size": [250, 250]}
sorl-thumbnail||image||e24c9862c636367eb8938c29044a423f	{"storage": "django.core.files.storage.FileSystemStorage", "name": "cache/b3/96/b396938988755440c6ec2293c3f1efd8.jpg", "size": [80, 80]}
sorl-thumbnail||thumbnails||f202f5a33d1c2c5a9ddb5cab6ffd7c32	["e24c9862c636367eb8938c29044a423f"]
sorl-thumbnail||image||bcdac257fb48ed9fdc59590d390745e8	{"storage": "django.core.files.storage.FileSystemStorage", "name": "multiuploader_images/bf18767fa2cd28aa44f101fe926131eb.png", "size": [1024, 768]}
sorl-thumbnail||image||5b0972114ea2559a6fdec9cef24b987d	{"storage": "django.core.files.storage.FileSystemStorage", "name": "cache/52/58/525869ccfe225eef8a409e9b6e41180a.jpg", "size": [80, 60]}
sorl-thumbnail||thumbnails||bcdac257fb48ed9fdc59590d390745e8	["5b0972114ea2559a6fdec9cef24b987d"]
sorl-thumbnail||image||512fe1c2d1cc450cf134dd6e11b0d59c	{"storage": "django.core.files.storage.FileSystemStorage", "name": "multiuploader_images/a1f0849f698d146bae16f675553d0529.png", "size": [790, 360]}
sorl-thumbnail||image||8e7a34eebcb8dc7ad662e7d0e11bd3c6	{"storage": "django.core.files.storage.FileSystemStorage", "name": "cache/1f/b3/1fb3ad66d70789950eaa040416c0b37a.jpg", "size": [80, 36]}
sorl-thumbnail||thumbnails||512fe1c2d1cc450cf134dd6e11b0d59c	["8e7a34eebcb8dc7ad662e7d0e11bd3c6"]
sorl-thumbnail||image||94fd2060a6f1e0ee2ec7be806aaa95c0	{"storage": "django.core.files.storage.FileSystemStorage", "name": "multiuploader_images/ae9934e518a081feb26cf09b51e18641.png", "size": [790, 360]}
sorl-thumbnail||image||0bf0463f8a4028055100e2a9c2ad991c	{"storage": "django.core.files.storage.FileSystemStorage", "name": "cache/93/3a/933a644d684e81392dc02d0b16a83363.jpg", "size": [80, 36]}
sorl-thumbnail||thumbnails||94fd2060a6f1e0ee2ec7be806aaa95c0	["0bf0463f8a4028055100e2a9c2ad991c"]
sorl-thumbnail||image||c0d00fa07fb9ae687c8bddf8dc6ba9cb	{"storage": "django.core.files.storage.FileSystemStorage", "name": "multiuploader_images/03eeef201f51345b898237ec79c5a4b3.png", "size": [250, 250]}
sorl-thumbnail||image||4e5a1885bfca2b1d84208d4165124bb8	{"storage": "django.core.files.storage.FileSystemStorage", "name": "cache/39/76/3976ff867a08dc364d6f903ec95c682b.jpg", "size": [80, 80]}
sorl-thumbnail||thumbnails||c0d00fa07fb9ae687c8bddf8dc6ba9cb	["4e5a1885bfca2b1d84208d4165124bb8"]
sorl-thumbnail||image||595c28b08a09db0268cf3f17c124fc37	{"storage": "django.core.files.storage.FileSystemStorage", "name": "multiuploader_images/c211f99aded854b0211a6c798a22394b.png", "size": [250, 250]}
sorl-thumbnail||image||aa91cea43b09e6acbcfc407fc028b429	{"storage": "django.core.files.storage.FileSystemStorage", "name": "cache/a2/92/a292fa327cd97e543afe5d7d2dce3241.jpg", "size": [80, 80]}
sorl-thumbnail||thumbnails||595c28b08a09db0268cf3f17c124fc37	["aa91cea43b09e6acbcfc407fc028b429"]
sorl-thumbnail||image||b0ef42f3a758a198f1a7b53df7dea8e8	{"storage": "django.core.files.storage.FileSystemStorage", "name": "multiuploader_images/41210ad0d6aa4623508c9f519d9021a1.png", "size": [250, 250]}
sorl-thumbnail||image||a82a7bc9ee84b9e501feeb2b80382baa	{"storage": "django.core.files.storage.FileSystemStorage", "name": "cache/d2/67/d26758343b58caa1f7176b463652d8b6.jpg", "size": [80, 80]}
sorl-thumbnail||thumbnails||b0ef42f3a758a198f1a7b53df7dea8e8	["a82a7bc9ee84b9e501feeb2b80382baa"]
sorl-thumbnail||image||a99ad4bfc12a3a3bb7f83d85096d7f1a	{"storage": "django.core.files.storage.FileSystemStorage", "name": "multiuploader_images/2e3f1eccb748bd03b3f334fc601f5f59.png", "size": [250, 250]}
sorl-thumbnail||image||9df8f53b0d365b3eb77ca1df027fc1a3	{"storage": "django.core.files.storage.FileSystemStorage", "name": "cache/e1/6a/e16a407fdde9ffe4c86fdf4764761351.jpg", "size": [80, 80]}
sorl-thumbnail||thumbnails||a99ad4bfc12a3a3bb7f83d85096d7f1a	["9df8f53b0d365b3eb77ca1df027fc1a3"]
sorl-thumbnail||image||5e2b480343eea6834c78ad274be3a54b	{"storage": "django.core.files.storage.FileSystemStorage", "name": "multiuploader_images/65041f08998e601ccfa82998a2263198.png", "size": [250, 250]}
sorl-thumbnail||image||d1d832d3d97c7c4359862717ecdbcc95	{"storage": "django.core.files.storage.FileSystemStorage", "name": "cache/76/03/760375bdef9afe4a6e1fb9baa00032ad.jpg", "size": [80, 80]}
sorl-thumbnail||thumbnails||5e2b480343eea6834c78ad274be3a54b	["d1d832d3d97c7c4359862717ecdbcc95"]
sorl-thumbnail||image||b2bd139d0051c11aec757ecfaca08b48	{"storage": "django.core.files.storage.FileSystemStorage", "name": "multiuploader_images/644fc7bafed9f4d66f4b5f721a2ab585.png", "size": [131, 244]}
sorl-thumbnail||image||67d45b5aa14c36f0c9731ce69ef0fb61	{"storage": "django.core.files.storage.FileSystemStorage", "name": "cache/20/8c/208c1a42fbab82bc45f9491f3927214b.jpg", "size": [43, 80]}
sorl-thumbnail||thumbnails||b2bd139d0051c11aec757ecfaca08b48	["67d45b5aa14c36f0c9731ce69ef0fb61"]
sorl-thumbnail||image||e0db0901e0022b6e3e6f953103a18fb5	{"storage": "django.core.files.storage.FileSystemStorage", "name": "multiuploader_images/7567b275b9a5bb652d688f896b3e4e05.png", "size": [250, 250]}
sorl-thumbnail||image||42781083ca0d43defab47f35ea5afc46	{"storage": "django.core.files.storage.FileSystemStorage", "name": "cache/e4/24/e424cfa5f3351e7be01aab36e2fdff0c.jpg", "size": [80, 80]}
sorl-thumbnail||thumbnails||e0db0901e0022b6e3e6f953103a18fb5	["42781083ca0d43defab47f35ea5afc46"]
sorl-thumbnail||image||0ee9bb1624bbcb07d3053e6a035f066d	{"storage": "django.core.files.storage.FileSystemStorage", "name": "multiuploader_images/5888786cafbcd1bd0b3eaaaba1130603.png", "size": [107, 111]}
sorl-thumbnail||image||6e0ecb75052a7086ae30eb39ae289fc0	{"storage": "django.core.files.storage.FileSystemStorage", "name": "cache/ea/d5/ead5a807a1b2cdb20906a299cbedb58c.jpg", "size": [77, 80]}
sorl-thumbnail||thumbnails||0ee9bb1624bbcb07d3053e6a035f066d	["6e0ecb75052a7086ae30eb39ae289fc0"]
sorl-thumbnail||image||8dc1ebb8651301d8e5a8135f97faaf3b	{"storage": "django.core.files.storage.FileSystemStorage", "name": "multiuploader_images/1c7a078627995d8c52124aa1e27b1b64.png", "size": [178, 196]}
sorl-thumbnail||image||828f390cd0ad8f625139b25426790309	{"storage": "django.core.files.storage.FileSystemStorage", "name": "cache/39/90/3990265fde9b1a760b37bccf84f3ba92.jpg", "size": [73, 80]}
sorl-thumbnail||thumbnails||8dc1ebb8651301d8e5a8135f97faaf3b	["828f390cd0ad8f625139b25426790309"]
sorl-thumbnail||image||4e34d52b916874d5f7867d9314449c2e	{"storage": "django.core.files.storage.FileSystemStorage", "name": "multiuploader_images/272913d897024486748b12c7364f5edd.png", "size": [156, 217]}
sorl-thumbnail||image||723f8d1142641a0b600324b29f8309db	{"storage": "django.core.files.storage.FileSystemStorage", "name": "cache/a3/01/a301f333abf5e63779465e719d4d35fa.jpg", "size": [58, 80]}
sorl-thumbnail||thumbnails||4e34d52b916874d5f7867d9314449c2e	["723f8d1142641a0b600324b29f8309db"]
sorl-thumbnail||image||247d4b4c945c4f90898b2497a9fcee50	{"storage": "django.core.files.storage.FileSystemStorage", "name": "multiuploader_images/981fe7e184c9a8a1a454094866bbc8fe.png", "size": [408, 260]}
sorl-thumbnail||image||21391513757e07d3da4506242df6d89d	{"storage": "django.core.files.storage.FileSystemStorage", "name": "cache/6e/af/6eaf8bdb2e570710ed7fa0195981655b.jpg", "size": [80, 51]}
sorl-thumbnail||thumbnails||247d4b4c945c4f90898b2497a9fcee50	["21391513757e07d3da4506242df6d89d"]
sorl-thumbnail||image||8a0b025c0a092fc0faa5a4edb27a7108	{"storage": "django.core.files.storage.FileSystemStorage", "name": "multiuploader_images/2a18c4f110734378cc9129b5b02a420b.png", "size": [150, 150]}
sorl-thumbnail||image||4f28ca9d358c7ce9699309ead87f95c9	{"storage": "django.core.files.storage.FileSystemStorage", "name": "cache/45/13/4513ca0da2ee327b7a4ad59fe7a698cf.jpg", "size": [80, 80]}
sorl-thumbnail||thumbnails||8a0b025c0a092fc0faa5a4edb27a7108	["4f28ca9d358c7ce9699309ead87f95c9"]
sorl-thumbnail||image||04f94499b96f5ecb55b824816c10ec8c	{"storage": "django.core.files.storage.FileSystemStorage", "name": "multiuploader_images/1d2dfa61129f34d23bf8be7210756612.png", "size": [345, 279]}
sorl-thumbnail||image||1cf7a0411113b7bd6e4ac8c7acd3b018	{"storage": "django.core.files.storage.FileSystemStorage", "name": "cache/d6/9e/d69e1a14e9968e3cb71c1c41ea56082d.jpg", "size": [80, 65]}
sorl-thumbnail||thumbnails||04f94499b96f5ecb55b824816c10ec8c	["1cf7a0411113b7bd6e4ac8c7acd3b018"]
sorl-thumbnail||image||380dee7f3486cfba59e9e0a2507c7528	{"storage": "django.core.files.storage.FileSystemStorage", "name": "multiuploader_images/1d67db9c5ee4a8832b16a81efab102a7.png", "size": [345, 279]}
sorl-thumbnail||image||69bc813b14d3eb45706794dccbf4479a	{"storage": "django.core.files.storage.FileSystemStorage", "name": "cache/44/cc/44ccfeef2975c767a0dbc67e86a03ceb.jpg", "size": [80, 65]}
sorl-thumbnail||thumbnails||380dee7f3486cfba59e9e0a2507c7528	["69bc813b14d3eb45706794dccbf4479a"]
sorl-thumbnail||image||b8d617aa62e42bcf5be6e428cf4c9b1e	{"storage": "django.core.files.storage.FileSystemStorage", "name": "multiuploader_images/b28a48b283b758a4188a188be80c9ca5.png", "size": [1246, 850]}
sorl-thumbnail||image||b466c03897c9665a824694f18602928c	{"storage": "django.core.files.storage.FileSystemStorage", "name": "cache/c1/f9/c1f9a0d962502df576d619a95721b334.jpg", "size": [80, 55]}
sorl-thumbnail||thumbnails||b8d617aa62e42bcf5be6e428cf4c9b1e	["b466c03897c9665a824694f18602928c"]
sorl-thumbnail||image||41145208a366564842c0075038e52b0b	{"storage": "django.core.files.storage.FileSystemStorage", "name": "multiuploader_images/954eec29e05a8c2276b668dc00b4f1cd.png", "size": [1249, 836]}
sorl-thumbnail||image||f3178afd94fd075558b62019f209ef44	{"storage": "django.core.files.storage.FileSystemStorage", "name": "cache/47/ae/47aec2787b6fafaad662e4b6b6279164.jpg", "size": [80, 54]}
sorl-thumbnail||thumbnails||41145208a366564842c0075038e52b0b	["f3178afd94fd075558b62019f209ef44"]
sorl-thumbnail||image||67dfc974d058a4bf57431a7f2a44621d	{"storage": "django.core.files.storage.FileSystemStorage", "name": "multiuploader_images/e476b1ca4950a45d165e5afc5041847d.png", "size": [1251, 851]}
sorl-thumbnail||image||58a997a42b0d903b38297ac8fc1439be	{"storage": "django.core.files.storage.FileSystemStorage", "name": "cache/0e/c2/0ec2de9522fad6714c73fd8c729251f3.jpg", "size": [80, 54]}
sorl-thumbnail||thumbnails||67dfc974d058a4bf57431a7f2a44621d	["58a997a42b0d903b38297ac8fc1439be"]
sorl-thumbnail||image||a948e204735bcb62b29a450f57772a0a	{"storage": "django.core.files.storage.FileSystemStorage", "name": "multiuploader_images/068d11d47b67f9f0a4aa83652c15f5c0.png", "size": [920, 400]}
sorl-thumbnail||image||b4f90036b3851db79a25ccd690526d91	{"storage": "django.core.files.storage.FileSystemStorage", "name": "cache/2c/42/2c42b77b16d85a4a686c46d60b6a5d7c.jpg", "size": [80, 35]}
sorl-thumbnail||thumbnails||a948e204735bcb62b29a450f57772a0a	["b4f90036b3851db79a25ccd690526d91"]
sorl-thumbnail||image||7a518c5d85ec9facc11c619bc57ec397	{"storage": "django.core.files.storage.FileSystemStorage", "name": "multiuploader_images/df82521e9738d275d478c09e2c3a6f10.png", "size": [920, 175]}
sorl-thumbnail||image||fd9b81678a0bd7f162e5643a3209c258	{"storage": "django.core.files.storage.FileSystemStorage", "name": "cache/e6/b0/e6b00e666dd9c8539fef7de1765525ed.jpg", "size": [80, 15]}
sorl-thumbnail||image||67f2b8508d1b2ec028e22298437b5ac3	{"storage": "django.core.files.storage.FileSystemStorage", "name": "multiuploader_images/9d3a6cc6b9734a3354192ca8daa705d4_1.png", "size": [1600, 1200]}
sorl-thumbnail||image||e724f3efc0c03d3beb88718c95934a35	{"storage": "django.core.files.storage.FileSystemStorage", "name": "cache/c8/9c/c89c4594ff253ce1d1189cffb77f8859.jpg", "size": [80, 60]}
sorl-thumbnail||thumbnails||67f2b8508d1b2ec028e22298437b5ac3	["e724f3efc0c03d3beb88718c95934a35"]
sorl-thumbnail||image||45d6ed8986c59d722ff2406191355525	{"storage": "django.core.files.storage.FileSystemStorage", "name": "multiuploader_images/8978a2e09c84af067ec38b8abb493a81.png", "size": [1600, 1200]}
sorl-thumbnail||image||88ea7047f02073ca07fc4844f3a6d62d	{"storage": "django.core.files.storage.FileSystemStorage", "name": "cache/b2/53/b253b1c3ddc52ac9adf6fe1a1615e24f.jpg", "size": [80, 60]}
sorl-thumbnail||thumbnails||45d6ed8986c59d722ff2406191355525	["88ea7047f02073ca07fc4844f3a6d62d"]
sorl-thumbnail||image||39f6fc59e786c23610fd1a95a3466fbd	{"storage": "django.core.files.storage.FileSystemStorage", "name": "pictures/9d3a6cc6b9734a3354192ca8daa705d4_1.png", "size": [1600, 1200]}
sorl-thumbnail||image||63637180278a87c03c199bff9e8f028f	{"storage": "django.core.files.storage.FileSystemStorage", "name": "cache/87/91/8791387de12736e7025692f9939b3314.jpg", "size": [80, 60]}
sorl-thumbnail||thumbnails||39f6fc59e786c23610fd1a95a3466fbd	["63637180278a87c03c199bff9e8f028f"]
sorl-thumbnail||image||fdd10f49105b8c8aa0ea7963e85e8f60	{"storage": "django.core.files.storage.FileSystemStorage", "name": "pictures/9d3a6cc6b9734a3354192ca8daa705d4_2.png", "size": [1600, 1200]}
sorl-thumbnail||image||82941b756b4319ddad051ebf3fc98935	{"storage": "django.core.files.storage.FileSystemStorage", "name": "cache/b4/ed/b4ed420d1a68aa79e569feb9f2dd64cb.jpg", "size": [80, 60]}
sorl-thumbnail||thumbnails||fdd10f49105b8c8aa0ea7963e85e8f60	["82941b756b4319ddad051ebf3fc98935"]
sorl-thumbnail||image||8bedab6a06012a96a39a0174ff3a7af8	{"storage": "django.core.files.storage.FileSystemStorage", "name": "pictures/9d3a6cc6b9734a3354192ca8daa705d4_3.png", "size": [1600, 1200]}
sorl-thumbnail||image||eeb8358e2feecfc781605e25e71dbf42	{"storage": "django.core.files.storage.FileSystemStorage", "name": "cache/33/a9/33a960afa319402095be768ce2666eb9.jpg", "size": [80, 60]}
sorl-thumbnail||thumbnails||8bedab6a06012a96a39a0174ff3a7af8	["eeb8358e2feecfc781605e25e71dbf42"]
sorl-thumbnail||image||572d66dba28e119759cfe69452a0752f	{"storage": "django.core.files.storage.FileSystemStorage", "name": "pictures/8978a2e09c84af067ec38b8abb493a81.png", "size": [1600, 1200]}
sorl-thumbnail||image||99b00c038de40a7ffd4f028c3c79f3bf	{"storage": "django.core.files.storage.FileSystemStorage", "name": "cache/7f/05/7f05ba73349392d9643843884f9a7b34.jpg", "size": [80, 60]}
sorl-thumbnail||thumbnails||572d66dba28e119759cfe69452a0752f	["99b00c038de40a7ffd4f028c3c79f3bf"]
sorl-thumbnail||image||d25a8b95f0ddaaa98ca3c337c74da89d	{"storage": "django.core.files.storage.FileSystemStorage", "name": "pictures/9d3a6cc6b9734a3354192ca8daa705d4.png", "size": [1600, 1200]}
sorl-thumbnail||image||74ce4fd08d4bb16233b7566b88629ed9	{"storage": "django.core.files.storage.FileSystemStorage", "name": "cache/88/fe/88fe2f27e67b333e5ef5adbaeb7d66bb.jpg", "size": [80, 60]}
sorl-thumbnail||thumbnails||d25a8b95f0ddaaa98ca3c337c74da89d	["74ce4fd08d4bb16233b7566b88629ed9"]
\.


--
-- Name: auth_group_name_key; Type: CONSTRAINT; Schema: public; Owner: mycoplasma; Tablespace: 
--

ALTER TABLE ONLY auth_group
    ADD CONSTRAINT auth_group_name_key UNIQUE (name);


--
-- Name: auth_group_permissions_group_id_key; Type: CONSTRAINT; Schema: public; Owner: mycoplasma; Tablespace: 
--

ALTER TABLE ONLY auth_group_permissions
    ADD CONSTRAINT auth_group_permissions_group_id_key UNIQUE (group_id, permission_id);


--
-- Name: auth_group_permissions_pkey; Type: CONSTRAINT; Schema: public; Owner: mycoplasma; Tablespace: 
--

ALTER TABLE ONLY auth_group_permissions
    ADD CONSTRAINT auth_group_permissions_pkey PRIMARY KEY (id);


--
-- Name: auth_group_pkey; Type: CONSTRAINT; Schema: public; Owner: mycoplasma; Tablespace: 
--

ALTER TABLE ONLY auth_group
    ADD CONSTRAINT auth_group_pkey PRIMARY KEY (id);


--
-- Name: auth_message_pkey; Type: CONSTRAINT; Schema: public; Owner: mycoplasma; Tablespace: 
--

ALTER TABLE ONLY auth_message
    ADD CONSTRAINT auth_message_pkey PRIMARY KEY (id);


--
-- Name: auth_permission_content_type_id_key; Type: CONSTRAINT; Schema: public; Owner: mycoplasma; Tablespace: 
--

ALTER TABLE ONLY auth_permission
    ADD CONSTRAINT auth_permission_content_type_id_key UNIQUE (content_type_id, codename);


--
-- Name: auth_permission_pkey; Type: CONSTRAINT; Schema: public; Owner: mycoplasma; Tablespace: 
--

ALTER TABLE ONLY auth_permission
    ADD CONSTRAINT auth_permission_pkey PRIMARY KEY (id);


--
-- Name: auth_user_groups_pkey; Type: CONSTRAINT; Schema: public; Owner: mycoplasma; Tablespace: 
--

ALTER TABLE ONLY auth_user_groups
    ADD CONSTRAINT auth_user_groups_pkey PRIMARY KEY (id);


--
-- Name: auth_user_groups_user_id_key; Type: CONSTRAINT; Schema: public; Owner: mycoplasma; Tablespace: 
--

ALTER TABLE ONLY auth_user_groups
    ADD CONSTRAINT auth_user_groups_user_id_key UNIQUE (user_id, group_id);


--
-- Name: auth_user_pkey; Type: CONSTRAINT; Schema: public; Owner: mycoplasma; Tablespace: 
--

ALTER TABLE ONLY auth_user
    ADD CONSTRAINT auth_user_pkey PRIMARY KEY (id);


--
-- Name: auth_user_user_permissions_pkey; Type: CONSTRAINT; Schema: public; Owner: mycoplasma; Tablespace: 
--

ALTER TABLE ONLY auth_user_user_permissions
    ADD CONSTRAINT auth_user_user_permissions_pkey PRIMARY KEY (id);


--
-- Name: auth_user_user_permissions_user_id_key; Type: CONSTRAINT; Schema: public; Owner: mycoplasma; Tablespace: 
--

ALTER TABLE ONLY auth_user_user_permissions
    ADD CONSTRAINT auth_user_user_permissions_user_id_key UNIQUE (user_id, permission_id);


--
-- Name: auth_user_username_key; Type: CONSTRAINT; Schema: public; Owner: mycoplasma; Tablespace: 
--

ALTER TABLE ONLY auth_user
    ADD CONSTRAINT auth_user_username_key UNIQUE (username);


--
-- Name: django_admin_log_pkey; Type: CONSTRAINT; Schema: public; Owner: mycoplasma; Tablespace: 
--

ALTER TABLE ONLY django_admin_log
    ADD CONSTRAINT django_admin_log_pkey PRIMARY KEY (id);


--
-- Name: django_content_type_app_label_key; Type: CONSTRAINT; Schema: public; Owner: mycoplasma; Tablespace: 
--

ALTER TABLE ONLY django_content_type
    ADD CONSTRAINT django_content_type_app_label_key UNIQUE (app_label, model);


--
-- Name: django_content_type_pkey; Type: CONSTRAINT; Schema: public; Owner: mycoplasma; Tablespace: 
--

ALTER TABLE ONLY django_content_type
    ADD CONSTRAINT django_content_type_pkey PRIMARY KEY (id);


--
-- Name: django_session_pkey; Type: CONSTRAINT; Schema: public; Owner: mycoplasma; Tablespace: 
--

ALTER TABLE ONLY django_session
    ADD CONSTRAINT django_session_pkey PRIMARY KEY (session_key);


--
-- Name: django_site_pkey; Type: CONSTRAINT; Schema: public; Owner: mycoplasma; Tablespace: 
--

ALTER TABLE ONLY django_site
    ADD CONSTRAINT django_site_pkey PRIMARY KEY (id);


--
-- Name: multiuploader_image_key_data_key; Type: CONSTRAINT; Schema: public; Owner: mycoplasma; Tablespace: 
--

ALTER TABLE ONLY multiuploader_image
    ADD CONSTRAINT multiuploader_image_key_data_key UNIQUE (key_data);


--
-- Name: multiuploader_image_pkey; Type: CONSTRAINT; Schema: public; Owner: mycoplasma; Tablespace: 
--

ALTER TABLE ONLY multiuploader_image
    ADD CONSTRAINT multiuploader_image_pkey PRIMARY KEY (id);


--
-- Name: mycoplasma_home_blastupload_pkey; Type: CONSTRAINT; Schema: public; Owner: mycoplasma; Tablespace: 
--

ALTER TABLE ONLY mycoplasma_home_blastupload
    ADD CONSTRAINT mycoplasma_home_blastupload_pkey PRIMARY KEY (id);


--
-- Name: mycoplasma_home_dropdownitem_pkey; Type: CONSTRAINT; Schema: public; Owner: mycoplasma; Tablespace: 
--

ALTER TABLE ONLY mycoplasma_home_dropdownitem
    ADD CONSTRAINT mycoplasma_home_dropdownitem_pkey PRIMARY KEY (id);


--
-- Name: mycoplasma_home_landmark_pkey; Type: CONSTRAINT; Schema: public; Owner: mycoplasma; Tablespace: 
--

ALTER TABLE ONLY mycoplasma_home_landmark
    ADD CONSTRAINT mycoplasma_home_landmark_pkey PRIMARY KEY (id);


--
-- Name: mycoplasma_home_navbaroption_pkey; Type: CONSTRAINT; Schema: public; Owner: mycoplasma; Tablespace: 
--

ALTER TABLE ONLY mycoplasma_home_navbaroption
    ADD CONSTRAINT mycoplasma_home_navbaroption_pkey PRIMARY KEY (id);


--
-- Name: mycoplasma_home_picturedefinitiontag_pkey; Type: CONSTRAINT; Schema: public; Owner: mycoplasma; Tablespace: 
--

ALTER TABLE ONLY mycoplasma_home_picturedefinitiontag
    ADD CONSTRAINT mycoplasma_home_picturedefinitiontag_pkey PRIMARY KEY (id);


--
-- Name: mycoplasma_home_pictureprops_picture_id_id_key; Type: CONSTRAINT; Schema: public; Owner: mycoplasma; Tablespace: 
--

ALTER TABLE ONLY mycoplasma_home_pictureprop
    ADD CONSTRAINT mycoplasma_home_pictureprops_picture_id_id_key UNIQUE (picture_id_id, type_id_id);


--
-- Name: mycoplasma_home_pictureprops_pkey; Type: CONSTRAINT; Schema: public; Owner: mycoplasma; Tablespace: 
--

ALTER TABLE ONLY mycoplasma_home_pictureprop
    ADD CONSTRAINT mycoplasma_home_pictureprops_pkey PRIMARY KEY (id);


--
-- Name: mycoplasma_home_pictures_pkey; Type: CONSTRAINT; Schema: public; Owner: mycoplasma; Tablespace: 
--

ALTER TABLE ONLY mycoplasma_home_picture
    ADD CONSTRAINT mycoplasma_home_pictures_pkey PRIMARY KEY (id);


--
-- Name: mycoplasma_home_picturetypes_pkey; Type: CONSTRAINT; Schema: public; Owner: mycoplasma; Tablespace: 
--

ALTER TABLE ONLY mycoplasma_home_picturetype
    ADD CONSTRAINT mycoplasma_home_picturetypes_pkey PRIMARY KEY (id);


--
-- Name: mycoplasma_home_recentlyviewedpicture_pkey; Type: CONSTRAINT; Schema: public; Owner: mycoplasma; Tablespace: 
--

ALTER TABLE ONLY mycoplasma_home_recentlyviewedpicture
    ADD CONSTRAINT mycoplasma_home_recentlyviewedpicture_pkey PRIMARY KEY (id);


--
-- Name: mycoplasma_home_recentlyviewedpicture_uniqueness; Type: CONSTRAINT; Schema: public; Owner: mycoplasma; Tablespace: 
--

ALTER TABLE ONLY mycoplasma_home_recentlyviewedpicture
    ADD CONSTRAINT mycoplasma_home_recentlyviewedpicture_uniqueness UNIQUE (picture_id, user_id);


--
-- Name: mycoplasma_home_tag_pkey; Type: CONSTRAINT; Schema: public; Owner: mycoplasma; Tablespace: 
--

ALTER TABLE ONLY mycoplasma_home_tag
    ADD CONSTRAINT mycoplasma_home_tag_pkey PRIMARY KEY (id);


--
-- Name: mycoplasma_home_tagcolor_pkey; Type: CONSTRAINT; Schema: public; Owner: mycoplasma; Tablespace: 
--

ALTER TABLE ONLY mycoplasma_home_tagcolor
    ADD CONSTRAINT mycoplasma_home_tagcolor_pkey PRIMARY KEY (id);


--
-- Name: mycoplasma_home_taggroup_pkey; Type: CONSTRAINT; Schema: public; Owner: mycoplasma; Tablespace: 
--

ALTER TABLE ONLY mycoplasma_home_taggroup
    ADD CONSTRAINT mycoplasma_home_taggroup_pkey PRIMARY KEY (id);


--
-- Name: mycoplasma_home_tagpoint_pkey; Type: CONSTRAINT; Schema: public; Owner: mycoplasma; Tablespace: 
--

ALTER TABLE ONLY mycoplasma_home_tagpoint
    ADD CONSTRAINT mycoplasma_home_tagpoint_pkey PRIMARY KEY (id);


--
-- Name: name_unique; Type: CONSTRAINT; Schema: public; Owner: mycoplasma; Tablespace: 
--

ALTER TABLE ONLY mycoplasma_home_taggroup
    ADD CONSTRAINT name_unique UNIQUE (name);


--
-- Name: thumbnail_kvstore_pkey; Type: CONSTRAINT; Schema: public; Owner: mycoplasma; Tablespace: 
--

ALTER TABLE ONLY thumbnail_kvstore
    ADD CONSTRAINT thumbnail_kvstore_pkey PRIMARY KEY (key);


--
-- Name: auth_message_user_id; Type: INDEX; Schema: public; Owner: mycoplasma; Tablespace: 
--

CREATE INDEX auth_message_user_id ON auth_message USING btree (user_id);


--
-- Name: auth_permission_content_type_id; Type: INDEX; Schema: public; Owner: mycoplasma; Tablespace: 
--

CREATE INDEX auth_permission_content_type_id ON auth_permission USING btree (content_type_id);


--
-- Name: django_admin_log_content_type_id; Type: INDEX; Schema: public; Owner: mycoplasma; Tablespace: 
--

CREATE INDEX django_admin_log_content_type_id ON django_admin_log USING btree (content_type_id);


--
-- Name: django_admin_log_user_id; Type: INDEX; Schema: public; Owner: mycoplasma; Tablespace: 
--

CREATE INDEX django_admin_log_user_id ON django_admin_log USING btree (user_id);


--
-- Name: mycoplasma_home_dropdownitem_navBarOpt_id; Type: INDEX; Schema: public; Owner: mycoplasma; Tablespace: 
--

CREATE INDEX "mycoplasma_home_dropdownitem_navBarOpt_id" ON mycoplasma_home_dropdownitem USING btree ("navBarOpt_id");


--
-- Name: mycoplasma_home_pictureprops_picture_id_id; Type: INDEX; Schema: public; Owner: mycoplasma; Tablespace: 
--

CREATE INDEX mycoplasma_home_pictureprops_picture_id_id ON mycoplasma_home_pictureprop USING btree (picture_id_id);


--
-- Name: mycoplasma_home_pictureprops_type_id_id; Type: INDEX; Schema: public; Owner: mycoplasma; Tablespace: 
--

CREATE INDEX mycoplasma_home_pictureprops_type_id_id ON mycoplasma_home_pictureprop USING btree (type_id_id);


--
-- Name: mycoplasma_home_tagpoint_group_id; Type: INDEX; Schema: public; Owner: mycoplasma; Tablespace: 
--

CREATE INDEX mycoplasma_home_tagpoint_group_id ON mycoplasma_home_tagpoint USING btree (tag_id);


--
-- Name: auth_group_permissions_group_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: mycoplasma
--

ALTER TABLE ONLY auth_group_permissions
    ADD CONSTRAINT auth_group_permissions_group_id_fkey FOREIGN KEY (group_id) REFERENCES auth_group(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: auth_group_permissions_permission_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: mycoplasma
--

ALTER TABLE ONLY auth_group_permissions
    ADD CONSTRAINT auth_group_permissions_permission_id_fkey FOREIGN KEY (permission_id) REFERENCES auth_permission(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: auth_message_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: mycoplasma
--

ALTER TABLE ONLY auth_message
    ADD CONSTRAINT auth_message_user_id_fkey FOREIGN KEY (user_id) REFERENCES auth_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: auth_user_groups_group_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: mycoplasma
--

ALTER TABLE ONLY auth_user_groups
    ADD CONSTRAINT auth_user_groups_group_id_fkey FOREIGN KEY (group_id) REFERENCES auth_group(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: auth_user_groups_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: mycoplasma
--

ALTER TABLE ONLY auth_user_groups
    ADD CONSTRAINT auth_user_groups_user_id_fkey FOREIGN KEY (user_id) REFERENCES auth_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: auth_user_user_permissions_permission_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: mycoplasma
--

ALTER TABLE ONLY auth_user_user_permissions
    ADD CONSTRAINT auth_user_user_permissions_permission_id_fkey FOREIGN KEY (permission_id) REFERENCES auth_permission(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: auth_user_user_permissions_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: mycoplasma
--

ALTER TABLE ONLY auth_user_user_permissions
    ADD CONSTRAINT auth_user_user_permissions_user_id_fkey FOREIGN KEY (user_id) REFERENCES auth_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: content_type_id_refs_id_728de91f; Type: FK CONSTRAINT; Schema: public; Owner: mycoplasma
--

ALTER TABLE ONLY auth_permission
    ADD CONSTRAINT content_type_id_refs_id_728de91f FOREIGN KEY (content_type_id) REFERENCES django_content_type(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: django_admin_log_content_type_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: mycoplasma
--

ALTER TABLE ONLY django_admin_log
    ADD CONSTRAINT django_admin_log_content_type_id_fkey FOREIGN KEY (content_type_id) REFERENCES django_content_type(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: django_admin_log_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: mycoplasma
--

ALTER TABLE ONLY django_admin_log
    ADD CONSTRAINT django_admin_log_user_id_fkey FOREIGN KEY (user_id) REFERENCES auth_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: multiuploader_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: mycoplasma
--

ALTER TABLE ONLY multiuploader_image
    ADD CONSTRAINT multiuploader_user_id_fkey FOREIGN KEY (user_id) REFERENCES auth_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: mycoplasma_home_dropdownitem_navBarOpt_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: mycoplasma
--

ALTER TABLE ONLY mycoplasma_home_dropdownitem
    ADD CONSTRAINT "mycoplasma_home_dropdownitem_navBarOpt_id_fkey" FOREIGN KEY ("navBarOpt_id") REFERENCES mycoplasma_home_navbaroption(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: mycoplasma_home_picturedefinitiontag_picture_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: mycoplasma
--

ALTER TABLE ONLY mycoplasma_home_picturedefinitiontag
    ADD CONSTRAINT mycoplasma_home_picturedefinitiontag_picture_id_fkey FOREIGN KEY (picture_id) REFERENCES mycoplasma_home_picture(id);


--
-- Name: mycoplasma_home_pictureprops_picture_id_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: mycoplasma
--

ALTER TABLE ONLY mycoplasma_home_pictureprop
    ADD CONSTRAINT mycoplasma_home_pictureprops_picture_id_id_fkey FOREIGN KEY (picture_id_id) REFERENCES mycoplasma_home_picture(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: mycoplasma_home_pictureprops_type_id_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: mycoplasma
--

ALTER TABLE ONLY mycoplasma_home_pictureprop
    ADD CONSTRAINT mycoplasma_home_pictureprops_type_id_id_fkey FOREIGN KEY (type_id_id) REFERENCES mycoplasma_home_picturetype(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: mycoplasma_home_taggroup_color_fkey; Type: FK CONSTRAINT; Schema: public; Owner: mycoplasma
--

ALTER TABLE ONLY mycoplasma_home_tag
    ADD CONSTRAINT mycoplasma_home_taggroup_color_fkey FOREIGN KEY (color_id) REFERENCES mycoplasma_home_tagcolor(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: mycoplasma_home_tagpoint_group_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: mycoplasma
--

ALTER TABLE ONLY mycoplasma_home_tagpoint
    ADD CONSTRAINT mycoplasma_home_tagpoint_group_id_fkey FOREIGN KEY (tag_id) REFERENCES mycoplasma_home_tag(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: originalUser_fkey; Type: FK CONSTRAINT; Schema: public; Owner: mycoplasma
--

ALTER TABLE ONLY mycoplasma_home_picture
    ADD CONSTRAINT "originalUser_fkey" FOREIGN KEY (user_id) REFERENCES auth_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: picture_fkey; Type: FK CONSTRAINT; Schema: public; Owner: mycoplasma
--

ALTER TABLE ONLY mycoplasma_home_recentlyviewedpicture
    ADD CONSTRAINT picture_fkey FOREIGN KEY (picture_id) REFERENCES mycoplasma_home_picture(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: picture_fkey; Type: FK CONSTRAINT; Schema: public; Owner: mycoplasma
--

ALTER TABLE ONLY mycoplasma_home_taggroup
    ADD CONSTRAINT picture_fkey FOREIGN KEY (picture_id) REFERENCES mycoplasma_home_picture(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: user_fkey; Type: FK CONSTRAINT; Schema: public; Owner: mycoplasma
--

ALTER TABLE ONLY mycoplasma_home_recentlyviewedpicture
    ADD CONSTRAINT user_fkey FOREIGN KEY (user_id) REFERENCES auth_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: user_fkey; Type: FK CONSTRAINT; Schema: public; Owner: mycoplasma
--

ALTER TABLE ONLY mycoplasma_home_tag
    ADD CONSTRAINT user_fkey FOREIGN KEY (user_id) REFERENCES auth_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: user_fkey; Type: FK CONSTRAINT; Schema: public; Owner: mycoplasma
--

ALTER TABLE ONLY mycoplasma_home_taggroup
    ADD CONSTRAINT user_fkey FOREIGN KEY (user_id) REFERENCES auth_user(id) DEFERRABLE INITIALLY DEFERRED;


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

