--
-- PostgreSQL database dump
--

\restrict UdqatscaE1PUVX4TTQ6sNx4X8wqk8AbambIzfgRZWfbaaLDIMOjVW4rPqYcuQNu

-- Dumped from database version 15.14
-- Dumped by pg_dump version 15.14

-- Started on 2025-08-28 13:37:42 UTC

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

DROP DATABASE IF EXISTS paqueteria;
--
-- TOC entry 3540 (class 1262 OID 16384)
-- Name: paqueteria; Type: DATABASE; Schema: -; Owner: -
--

CREATE DATABASE paqueteria WITH TEMPLATE = template0 ENCODING = 'UTF8' LOCALE_PROVIDER = libc LOCALE = 'en_US.utf8';


\unrestrict UdqatscaE1PUVX4TTQ6sNx4X8wqk8AbambIzfgRZWfbaaLDIMOjVW4rPqYcuQNu
\connect paqueteria
\restrict UdqatscaE1PUVX4TTQ6sNx4X8wqk8AbambIzfgRZWfbaaLDIMOjVW4rPqYcuQNu

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

--
-- TOC entry 4 (class 2615 OID 2200)
-- Name: public; Type: SCHEMA; Schema: -; Owner: -
--

CREATE SCHEMA public;


--
-- TOC entry 3541 (class 0 OID 0)
-- Dependencies: 4
-- Name: SCHEMA public; Type: COMMENT; Schema: -; Owner: -
--

COMMENT ON SCHEMA public IS 'standard public schema';


--
-- TOC entry 883 (class 1247 OID 24709)
-- Name: messagetype; Type: TYPE; Schema: public; Owner: -
--

CREATE TYPE public.messagetype AS ENUM (
    'internal',
    'support',
    'system'
);


--
-- TOC entry 877 (class 1247 OID 24680)
-- Name: notificationstatus; Type: TYPE; Schema: public; Owner: -
--

CREATE TYPE public.notificationstatus AS ENUM (
    'pending',
    'sent',
    'failed',
    'delivered'
);


--
-- TOC entry 874 (class 1247 OID 24673)
-- Name: notificationtype; Type: TYPE; Schema: public; Owner: -
--

CREATE TYPE public.notificationtype AS ENUM (
    'email',
    'sms',
    'push'
);


--
-- TOC entry 868 (class 1247 OID 24648)
-- Name: packagecondition; Type: TYPE; Schema: public; Owner: -
--

CREATE TYPE public.packagecondition AS ENUM (
    'bueno',
    'regular',
    'malo'
);


--
-- TOC entry 862 (class 1247 OID 24631)
-- Name: packagestatus; Type: TYPE; Schema: public; Owner: -
--

CREATE TYPE public.packagestatus AS ENUM (
    'anunciado',
    'recibido',
    'en_transito',
    'entregado',
    'cancelado'
);


--
-- TOC entry 865 (class 1247 OID 24642)
-- Name: packagetype; Type: TYPE; Schema: public; Owner: -
--

CREATE TYPE public.packagetype AS ENUM (
    'normal',
    'extra_dimensionado'
);


--
-- TOC entry 856 (class 1247 OID 24617)
-- Name: ratetype; Type: TYPE; Schema: public; Owner: -
--

CREATE TYPE public.ratetype AS ENUM (
    'storage',
    'delivery',
    'package_type'
);


--
-- TOC entry 898 (class 1247 OID 24772)
-- Name: userrole; Type: TYPE; Schema: public; Owner: -
--

CREATE TYPE public.userrole AS ENUM (
    'ADMIN',
    'OPERATOR',
    'USER'
);


SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- TOC entry 214 (class 1259 OID 24576)
-- Name: alembic_version; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.alembic_version (
    version_num character varying(32) NOT NULL
);


--
-- TOC entry 216 (class 1259 OID 24604)
-- Name: customers; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.customers (
    id uuid NOT NULL,
    created_at timestamp with time zone DEFAULT now(),
    updated_at timestamp with time zone DEFAULT now(),
    name character varying(100) NOT NULL,
    phone character varying(20) NOT NULL,
    tracking_number character varying(50) NOT NULL
);


--
-- TOC entry 221 (class 1259 OID 24729)
-- Name: files; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.files (
    id uuid NOT NULL,
    created_at timestamp with time zone DEFAULT now(),
    updated_at timestamp with time zone DEFAULT now(),
    package_id uuid,
    uploaded_by_user_id uuid,
    filename character varying(255) NOT NULL,
    file_path character varying(500) NOT NULL,
    file_size integer NOT NULL,
    mime_type character varying(100) NOT NULL,
    upload_date timestamp without time zone
);


--
-- TOC entry 220 (class 1259 OID 24715)
-- Name: messages; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.messages (
    id uuid NOT NULL,
    created_at timestamp with time zone DEFAULT now(),
    updated_at timestamp with time zone DEFAULT now(),
    sender_id uuid NOT NULL,
    subject character varying(200) NOT NULL,
    content text NOT NULL,
    message_type public.messagetype,
    is_read boolean,
    read_at timestamp without time zone
);


--
-- TOC entry 219 (class 1259 OID 24689)
-- Name: notifications; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.notifications (
    id uuid NOT NULL,
    created_at timestamp with time zone DEFAULT now(),
    updated_at timestamp with time zone DEFAULT now(),
    package_id uuid,
    user_id uuid,
    notification_type public.notificationtype NOT NULL,
    message text NOT NULL,
    status public.notificationstatus,
    sent_at timestamp without time zone,
    delivery_confirmation json
);


--
-- TOC entry 224 (class 1259 OID 24763)
-- Name: package_announcements; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.package_announcements (
    id uuid NOT NULL,
    customer_name character varying(100) NOT NULL,
    phone_number character varying(20) NOT NULL,
    guide_number character varying(50) NOT NULL,
    is_active boolean NOT NULL,
    is_processed boolean NOT NULL,
    announced_at timestamp without time zone NOT NULL,
    processed_at timestamp without time zone,
    customer_id uuid,
    package_id uuid,
    created_at timestamp without time zone NOT NULL,
    updated_at timestamp without time zone NOT NULL,
    tracking_code character varying(4) NOT NULL
);


--
-- TOC entry 218 (class 1259 OID 24655)
-- Name: packages; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.packages (
    id uuid NOT NULL,
    created_at timestamp with time zone DEFAULT now(),
    updated_at timestamp with time zone DEFAULT now(),
    tracking_number character varying(50) NOT NULL,
    customer_name character varying(100) NOT NULL,
    customer_phone character varying(20) NOT NULL,
    status public.packagestatus,
    package_type public.packagetype,
    package_condition public.packagecondition,
    storage_cost numeric(10,2),
    delivery_cost numeric(10,2),
    total_cost numeric(10,2),
    observations text,
    announced_at timestamp without time zone,
    received_at timestamp without time zone,
    delivered_at timestamp without time zone,
    customer_id uuid
);


--
-- TOC entry 223 (class 1259 OID 24749)
-- Name: password_reset_tokens; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.password_reset_tokens (
    id integer NOT NULL,
    token character varying(255) NOT NULL,
    user_id uuid NOT NULL,
    expires_at timestamp without time zone NOT NULL,
    used boolean NOT NULL,
    created_at timestamp without time zone NOT NULL
);


--
-- TOC entry 222 (class 1259 OID 24748)
-- Name: password_reset_tokens_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.password_reset_tokens_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- TOC entry 3542 (class 0 OID 0)
-- Dependencies: 222
-- Name: password_reset_tokens_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.password_reset_tokens_id_seq OWNED BY public.password_reset_tokens.id;


--
-- TOC entry 217 (class 1259 OID 24623)
-- Name: rates; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.rates (
    id uuid NOT NULL,
    created_at timestamp with time zone DEFAULT now(),
    updated_at timestamp with time zone DEFAULT now(),
    rate_type public.ratetype NOT NULL,
    base_price numeric(10,2) NOT NULL,
    daily_storage_rate numeric(10,2),
    delivery_rate numeric(10,2),
    package_type_multiplier numeric(10,2),
    is_active boolean,
    valid_from timestamp without time zone,
    valid_to timestamp without time zone
);


--
-- TOC entry 215 (class 1259 OID 24589)
-- Name: users; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.users (
    id uuid NOT NULL,
    created_at timestamp with time zone DEFAULT now(),
    updated_at timestamp with time zone DEFAULT now(),
    username character varying(50) NOT NULL,
    email character varying(100) NOT NULL,
    password_hash character varying(255) NOT NULL,
    first_name character varying(50) NOT NULL,
    last_name character varying(50) NOT NULL,
    phone character varying(20),
    is_active boolean,
    role public.userrole,
    permissions json,
    last_login timestamp without time zone
);


--
-- TOC entry 3334 (class 2604 OID 24752)
-- Name: password_reset_tokens id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.password_reset_tokens ALTER COLUMN id SET DEFAULT nextval('public.password_reset_tokens_id_seq'::regclass);


--
-- TOC entry 3524 (class 0 OID 24576)
-- Dependencies: 214
-- Data for Name: alembic_version; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.alembic_version (version_num) FROM stdin;
004_add_tracking_code
\.


--
-- TOC entry 3526 (class 0 OID 24604)
-- Dependencies: 216
-- Data for Name: customers; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.customers (id, created_at, updated_at, name, phone, tracking_number) FROM stdin;
\.


--
-- TOC entry 3531 (class 0 OID 24729)
-- Dependencies: 221
-- Data for Name: files; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.files (id, created_at, updated_at, package_id, uploaded_by_user_id, filename, file_path, file_size, mime_type, upload_date) FROM stdin;
\.


--
-- TOC entry 3530 (class 0 OID 24715)
-- Dependencies: 220
-- Data for Name: messages; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.messages (id, created_at, updated_at, sender_id, subject, content, message_type, is_read, read_at) FROM stdin;
\.


--
-- TOC entry 3529 (class 0 OID 24689)
-- Dependencies: 219
-- Data for Name: notifications; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.notifications (id, created_at, updated_at, package_id, user_id, notification_type, message, status, sent_at, delivery_confirmation) FROM stdin;
\.


--
-- TOC entry 3534 (class 0 OID 24763)
-- Dependencies: 224
-- Data for Name: package_announcements; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.package_announcements (id, customer_name, phone_number, guide_number, is_active, is_processed, announced_at, processed_at, customer_id, package_id, created_at, updated_at, tracking_code) FROM stdin;
928fdcc8-6fb7-4bdc-8f4f-27abf5337584	Test User	3001234567	123456789	t	f	2025-08-27 14:23:41.143494	\N	\N	\N	2025-08-27 14:23:41.143496	2025-08-27 14:23:41.143497	GC54
de162beb-2234-4c2d-96d8-05b4a5263e55	Juan Pérez	3009876543	987654321	t	f	2025-08-27 14:24:21.100788	\N	\N	\N	2025-08-27 14:24:21.100791	2025-08-27 14:24:21.100792	TEHL
6f68d666-235c-4104-9cb1-7def944b2caf	JESUS VILLALOBOS	3002596319	99776644	t	f	2025-08-27 19:16:24.790439	\N	\N	\N	2025-08-27 19:16:24.790442	2025-08-27 19:16:24.790442	A1W5
c57147bc-ec07-44b9-b072-560713adcb37	MARIA GONZALEZ	3001234567	GUIA000	t	f	2025-08-27 19:24:20.677577	\N	\N	\N	2025-08-27 19:24:20.67758	2025-08-27 19:24:20.677581	YJWX
84eeff21-4e38-4635-8ca7-b2b48700af0a	ANA MARTINEZ	3003456789	GUIA002	t	f	2025-08-27 19:24:35.488534	\N	\N	\N	2025-08-27 19:24:35.488537	2025-08-27 19:24:35.488538	J1NK
05ea009f-99ef-4088-9c36-fff999e22ee2	CARLOS RODRIGUEZ	3002345678	GUIA001	t	f	2025-08-27 19:24:56.654059	\N	\N	\N	2025-08-27 19:24:56.654062	2025-08-27 19:24:56.654063	Z7UH
cc1096ef-20eb-49da-9da4-cae5e41519ae	ANGELICA ARRAZOLA	3008103849	4466	t	f	2025-08-27 20:05:08.8925	\N	\N	\N	2025-08-27 20:05:08.892503	2025-08-27 20:05:08.892503	S7MJ
73b8b01b-f899-4096-adb3-78bc5f448ade	JESUS VILLALOBOS	3002596319	159951	t	f	2025-08-27 20:05:35.559987	\N	\N	\N	2025-08-27 20:05:35.559989	2025-08-27 20:05:35.55999	WDCK
c2e69786-9167-4591-87f5-1ad03e21136f	JESUS VILLALOBOS	3002596319	YJWX	t	f	2025-08-27 20:09:42.959589	\N	\N	\N	2025-08-27 20:09:42.959591	2025-08-27 20:09:42.959592	1I7D
08470785-0ed8-4bf9-9ebe-288fec9f4ab5	Test User	3001234567	TEST123	t	f	2025-08-27 20:14:52.267115	\N	\N	\N	2025-08-27 20:14:52.267131	2025-08-27 20:14:52.267131	UDE7
82b56a95-169f-430b-85e5-4f807fb637c0	JESUS VILLALOBOS	3002596319	1599513	t	f	2025-08-27 20:17:44.149581	\N	\N	\N	2025-08-27 20:17:44.149586	2025-08-27 20:17:44.149588	WTIU
20dd52ca-71e6-4c28-973d-baabbbbc3860	JESUS VILLALOBOS	3002596319	WTIU	t	f	2025-08-27 20:17:53.129194	\N	\N	\N	2025-08-27 20:17:53.129199	2025-08-27 20:17:53.129201	5BX4
bad0d505-c9c5-4571-827a-1712e34908d1	JESUS VILLALOBOS	3002596319	YJWXE	t	f	2025-08-27 20:26:04.001187	\N	\N	\N	2025-08-27 20:26:04.001193	2025-08-27 20:26:04.001194	Q4N6
4d03fcce-a09c-45a6-86a3-0587e26be5f7	JESUS VILLALOBOS	3002596319	159951DF	t	f	2025-08-27 20:32:45.876921	\N	\N	\N	2025-08-27 20:32:45.876923	2025-08-27 20:32:45.876924	7BSS
4affcc3d-81e2-4654-9e6d-53cfed252df4	7BSS	3002596319	7BSSDFF	t	f	2025-08-27 20:33:10.428908	\N	\N	\N	2025-08-27 20:33:10.428917	2025-08-27 20:33:10.428921	PWRT
5e9883b9-1a57-469e-9404-46705d616c09	JESUS VILLALOBOS	+13002596319	159951QQ	t	f	2025-08-27 20:35:14.999848	\N	\N	\N	2025-08-27 20:35:14.99985	2025-08-27 20:35:14.999851	F6CG
7c18cf53-6989-4349-97e8-197e5c29fa0b	JESUS VILLALOBOS	3002596319	159951Q	t	f	2025-08-27 20:36:01.311076	\N	\N	\N	2025-08-27 20:36:01.311083	2025-08-27 20:36:01.311085	BUPJ
3a1eb28c-4390-4204-81b3-9c40ee054a6a	JESUS VILLALOBOS	3002596319	159951QQQ	t	f	2025-08-27 20:38:13.75589	\N	\N	\N	2025-08-27 20:38:13.755893	2025-08-27 20:38:13.755895	5LHA
b6455dce-c5c9-45a6-9371-7d2dbd1e4c0e	ANGELICA ARRAZOLA	3008103849	995511775533	t	f	2025-08-27 20:44:07.273651	\N	\N	\N	2025-08-27 20:44:07.273654	2025-08-27 20:44:07.273655	64XM
b5be912a-8f2d-46d2-9cb9-373a99c4aafe	sdfsadf	+1231 212312112	ASDAA	t	f	2025-08-27 21:34:38.569326	\N	\N	\N	2025-08-27 21:34:38.569328	2025-08-27 21:34:38.569329	RC7E
aebe9338-4a82-4c40-96e7-e0adfc6673ac	asdasd	+57 300 259 6319	123EQASD	t	f	2025-08-27 21:34:51.311076	\N	\N	\N	2025-08-27 21:34:51.311082	2025-08-27 21:34:51.311084	EV4N
d4c19e22-ab4f-463f-879d-a2f8b05ac91b	JESUS VILLALOBOS	+5730 02596319	554477	t	f	2025-08-27 21:35:29.535589	\N	\N	\N	2025-08-27 21:35:29.535592	2025-08-27 21:35:29.535593	6LMU
906dc018-6792-4a2a-9ca5-6fe7d7808849	gfsdfsdf	3002596319	SDFSDFSDFSDF	t	f	2025-08-27 21:38:04.729185	\N	\N	\N	2025-08-27 21:38:04.729189	2025-08-27 21:38:04.72919	RNNT
\.


--
-- TOC entry 3528 (class 0 OID 24655)
-- Dependencies: 218
-- Data for Name: packages; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.packages (id, created_at, updated_at, tracking_number, customer_name, customer_phone, status, package_type, package_condition, storage_cost, delivery_cost, total_cost, observations, announced_at, received_at, delivered_at, customer_id) FROM stdin;
\.


--
-- TOC entry 3533 (class 0 OID 24749)
-- Dependencies: 223
-- Data for Name: password_reset_tokens; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.password_reset_tokens (id, token, user_id, expires_at, used, created_at) FROM stdin;
1	93f63a81-6fd3-44fc-83e5-afe547c2606c	26af2c6f-c2d7-4b73-a8fc-2444cc9a0370	2025-08-28 02:51:50.846009	f	2025-08-28 01:51:50.847502
2	33549884-512b-4183-abad-de2fb7e18e20	26af2c6f-c2d7-4b73-a8fc-2444cc9a0370	2025-08-28 02:56:39.266051	f	2025-08-28 01:56:39.266397
3	2d64aa91-a5c0-461a-9e47-122f48ec0a65	26af2c6f-c2d7-4b73-a8fc-2444cc9a0370	2025-08-28 02:57:26.556471	f	2025-08-28 01:57:26.556866
4	de51fedc-0e5d-4022-a2c2-285bca9df6df	26af2c6f-c2d7-4b73-a8fc-2444cc9a0370	2025-08-28 03:02:01.043235	f	2025-08-28 02:02:01.043517
5	bc0810d5-d206-4d0d-87f3-ee25cddcc128	26af2c6f-c2d7-4b73-a8fc-2444cc9a0370	2025-08-28 03:05:43.630939	f	2025-08-28 02:05:43.632928
6	87d9903e-5ef6-4044-b278-7d9b3a4b7016	26af2c6f-c2d7-4b73-a8fc-2444cc9a0370	2025-08-28 03:08:00.811205	f	2025-08-28 02:08:00.812916
7	8793d85e-e3de-49db-aadb-93f23af176c7	26af2c6f-c2d7-4b73-a8fc-2444cc9a0370	2025-08-28 03:08:28.590741	f	2025-08-28 02:08:28.592945
8	4bf03b94-2ca5-44ce-ac62-1ea4ff8dea25	26af2c6f-c2d7-4b73-a8fc-2444cc9a0370	2025-08-28 03:09:04.584566	f	2025-08-28 02:09:04.585935
9	84b21725-1354-4232-bc17-fc662d45710d	26af2c6f-c2d7-4b73-a8fc-2444cc9a0370	2025-08-28 03:09:38.181242	f	2025-08-28 02:09:38.183474
10	6f6aad95-02f3-49ec-8be7-274aa681c938	26af2c6f-c2d7-4b73-a8fc-2444cc9a0370	2025-08-28 03:10:16.442648	f	2025-08-28 02:10:16.4442
11	54fcc0d3-705d-4ae5-ba11-29f14341451c	26af2c6f-c2d7-4b73-a8fc-2444cc9a0370	2025-08-28 03:12:15.308236	t	2025-08-28 02:12:15.308592
12	08638ac4-49d8-4b0a-a2e0-a0064e3bf9ac	26af2c6f-c2d7-4b73-a8fc-2444cc9a0370	2025-08-28 03:14:51.66503	f	2025-08-28 02:14:51.665717
13	542eb41d-1b94-461e-9bdf-54e510457a11	26af2c6f-c2d7-4b73-a8fc-2444cc9a0370	2025-08-28 03:15:08.095997	f	2025-08-28 02:15:08.09739
14	93cbf30b-02ef-466b-89e8-021b37c7905e	26af2c6f-c2d7-4b73-a8fc-2444cc9a0370	2025-08-28 03:16:23.29354	f	2025-08-28 02:16:23.294813
15	0e882012-ec98-4733-8b0f-5c661a0e197a	26af2c6f-c2d7-4b73-a8fc-2444cc9a0370	2025-08-28 03:17:31.307348	t	2025-08-28 02:17:31.308393
16	2c41dadb-9acf-4725-bf64-9deaf5e6e334	26af2c6f-c2d7-4b73-a8fc-2444cc9a0370	2025-08-28 03:18:48.362573	t	2025-08-28 02:18:48.363481
17	3d68ea3a-d2a1-491f-a75c-56c74a412e01	26af2c6f-c2d7-4b73-a8fc-2444cc9a0370	2025-08-28 12:04:59.682381	f	2025-08-28 11:04:59.683684
\.


--
-- TOC entry 3527 (class 0 OID 24623)
-- Dependencies: 217
-- Data for Name: rates; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.rates (id, created_at, updated_at, rate_type, base_price, daily_storage_rate, delivery_rate, package_type_multiplier, is_active, valid_from, valid_to) FROM stdin;
\.


--
-- TOC entry 3525 (class 0 OID 24589)
-- Dependencies: 215
-- Data for Name: users; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.users (id, created_at, updated_at, username, email, password_hash, first_name, last_name, phone, is_active, role, permissions, last_login) FROM stdin;
26af2c6f-c2d7-4b73-a8fc-2444cc9a0370	2025-08-27 22:06:26.352624+00	2025-08-28 02:19:17.127603+00	jveyes	jveyes@gmail.com	$2b$12$3rsPzcNY6VgmEsIvs9nx0efwHdyamcL/ABqOALsjaZyhkeu8KVvsq	Jesus	Villalobos	\N	t	USER	\N	\N
\.


--
-- TOC entry 3543 (class 0 OID 0)
-- Dependencies: 222
-- Name: password_reset_tokens_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.password_reset_tokens_id_seq', 17, true);


--
-- TOC entry 3336 (class 2606 OID 24580)
-- Name: alembic_version alembic_version_pkc; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.alembic_version
    ADD CONSTRAINT alembic_version_pkc PRIMARY KEY (version_num);


--
-- TOC entry 3346 (class 2606 OID 24610)
-- Name: customers customers_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.customers
    ADD CONSTRAINT customers_pkey PRIMARY KEY (id);


--
-- TOC entry 3348 (class 2606 OID 24612)
-- Name: customers customers_tracking_number_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.customers
    ADD CONSTRAINT customers_tracking_number_key UNIQUE (tracking_number);


--
-- TOC entry 3364 (class 2606 OID 24737)
-- Name: files files_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.files
    ADD CONSTRAINT files_pkey PRIMARY KEY (id);


--
-- TOC entry 3362 (class 2606 OID 24723)
-- Name: messages messages_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.messages
    ADD CONSTRAINT messages_pkey PRIMARY KEY (id);


--
-- TOC entry 3360 (class 2606 OID 24697)
-- Name: notifications notifications_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.notifications
    ADD CONSTRAINT notifications_pkey PRIMARY KEY (id);


--
-- TOC entry 3374 (class 2606 OID 24767)
-- Name: package_announcements package_announcements_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.package_announcements
    ADD CONSTRAINT package_announcements_pkey PRIMARY KEY (id);


--
-- TOC entry 3356 (class 2606 OID 24663)
-- Name: packages packages_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.packages
    ADD CONSTRAINT packages_pkey PRIMARY KEY (id);


--
-- TOC entry 3358 (class 2606 OID 24665)
-- Name: packages packages_tracking_number_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.packages
    ADD CONSTRAINT packages_tracking_number_key UNIQUE (tracking_number);


--
-- TOC entry 3369 (class 2606 OID 24754)
-- Name: password_reset_tokens password_reset_tokens_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.password_reset_tokens
    ADD CONSTRAINT password_reset_tokens_pkey PRIMARY KEY (id);


--
-- TOC entry 3353 (class 2606 OID 24629)
-- Name: rates rates_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.rates
    ADD CONSTRAINT rates_pkey PRIMARY KEY (id);


--
-- TOC entry 3340 (class 2606 OID 24599)
-- Name: users users_email_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_email_key UNIQUE (email);


--
-- TOC entry 3342 (class 2606 OID 24597)
-- Name: users users_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_pkey PRIMARY KEY (id);


--
-- TOC entry 3344 (class 2606 OID 24601)
-- Name: users users_username_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_username_key UNIQUE (username);


--
-- TOC entry 3349 (class 1259 OID 24613)
-- Name: idx_customer_name; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX idx_customer_name ON public.customers USING btree (name);


--
-- TOC entry 3350 (class 1259 OID 24614)
-- Name: idx_customer_phone; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX idx_customer_phone ON public.customers USING btree (phone);


--
-- TOC entry 3351 (class 1259 OID 24615)
-- Name: ix_customers_tracking_number; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX ix_customers_tracking_number ON public.customers USING btree (tracking_number);


--
-- TOC entry 3370 (class 1259 OID 24768)
-- Name: ix_package_announcements_guide_number; Type: INDEX; Schema: public; Owner: -
--

CREATE UNIQUE INDEX ix_package_announcements_guide_number ON public.package_announcements USING btree (guide_number);


--
-- TOC entry 3371 (class 1259 OID 24769)
-- Name: ix_package_announcements_id; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX ix_package_announcements_id ON public.package_announcements USING btree (id);


--
-- TOC entry 3372 (class 1259 OID 24770)
-- Name: ix_package_announcements_tracking_code; Type: INDEX; Schema: public; Owner: -
--

CREATE UNIQUE INDEX ix_package_announcements_tracking_code ON public.package_announcements USING btree (tracking_code);


--
-- TOC entry 3354 (class 1259 OID 24666)
-- Name: ix_packages_tracking_number; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX ix_packages_tracking_number ON public.packages USING btree (tracking_number);


--
-- TOC entry 3365 (class 1259 OID 24762)
-- Name: ix_password_reset_tokens_expires_at; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX ix_password_reset_tokens_expires_at ON public.password_reset_tokens USING btree (expires_at);


--
-- TOC entry 3366 (class 1259 OID 24760)
-- Name: ix_password_reset_tokens_token; Type: INDEX; Schema: public; Owner: -
--

CREATE UNIQUE INDEX ix_password_reset_tokens_token ON public.password_reset_tokens USING btree (token);


--
-- TOC entry 3367 (class 1259 OID 24761)
-- Name: ix_password_reset_tokens_user_id; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX ix_password_reset_tokens_user_id ON public.password_reset_tokens USING btree (user_id);


--
-- TOC entry 3337 (class 1259 OID 24602)
-- Name: ix_users_email; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX ix_users_email ON public.users USING btree (email);


--
-- TOC entry 3338 (class 1259 OID 24603)
-- Name: ix_users_username; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX ix_users_username ON public.users USING btree (username);


--
-- TOC entry 3379 (class 2606 OID 24738)
-- Name: files files_package_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.files
    ADD CONSTRAINT files_package_id_fkey FOREIGN KEY (package_id) REFERENCES public.packages(id);


--
-- TOC entry 3380 (class 2606 OID 24743)
-- Name: files files_uploaded_by_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.files
    ADD CONSTRAINT files_uploaded_by_user_id_fkey FOREIGN KEY (uploaded_by_user_id) REFERENCES public.users(id);


--
-- TOC entry 3378 (class 2606 OID 24724)
-- Name: messages messages_sender_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.messages
    ADD CONSTRAINT messages_sender_id_fkey FOREIGN KEY (sender_id) REFERENCES public.users(id);


--
-- TOC entry 3376 (class 2606 OID 24698)
-- Name: notifications notifications_package_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.notifications
    ADD CONSTRAINT notifications_package_id_fkey FOREIGN KEY (package_id) REFERENCES public.packages(id);


--
-- TOC entry 3377 (class 2606 OID 24703)
-- Name: notifications notifications_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.notifications
    ADD CONSTRAINT notifications_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(id);


--
-- TOC entry 3375 (class 2606 OID 24667)
-- Name: packages packages_customer_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.packages
    ADD CONSTRAINT packages_customer_id_fkey FOREIGN KEY (customer_id) REFERENCES public.customers(id);


--
-- TOC entry 3381 (class 2606 OID 24755)
-- Name: password_reset_tokens password_reset_tokens_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.password_reset_tokens
    ADD CONSTRAINT password_reset_tokens_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(id) ON DELETE CASCADE;


-- Completed on 2025-08-28 13:37:43 UTC

--
-- PostgreSQL database dump complete
--

\unrestrict UdqatscaE1PUVX4TTQ6sNx4X8wqk8AbambIzfgRZWfbaaLDIMOjVW4rPqYcuQNu

