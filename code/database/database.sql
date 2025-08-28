--
-- PostgreSQL database dump
--

\restrict pTKP4g2pHHESwoAx0XsPZj36jQCVlcTXBm1TFnKlcrF92Y8mFs4hmuwGSbRa4DF

-- Dumped from database version 15.14
-- Dumped by pg_dump version 15.14

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
-- Name: messagetype; Type: TYPE; Schema: public; Owner: paqueteria_user
--

CREATE TYPE public.messagetype AS ENUM (
    'INTERNAL',
    'TICKET'
);


ALTER TYPE public.messagetype OWNER TO paqueteria_user;

--
-- Name: notificationtype; Type: TYPE; Schema: public; Owner: paqueteria_user
--

CREATE TYPE public.notificationtype AS ENUM (
    'EMAIL',
    'SMS',
    'WHATSAPP'
);


ALTER TYPE public.notificationtype OWNER TO paqueteria_user;

--
-- Name: packagestatus; Type: TYPE; Schema: public; Owner: paqueteria_user
--

CREATE TYPE public.packagestatus AS ENUM (
    'ANUNCIADO',
    'RECIBIDO',
    'EN_TRANSITO',
    'ENTREGADO',
    'CANCELADO'
);


ALTER TYPE public.packagestatus OWNER TO paqueteria_user;

--
-- Name: userrole; Type: TYPE; Schema: public; Owner: paqueteria_user
--

CREATE TYPE public.userrole AS ENUM (
    'ADMIN',
    'OPERATOR',
    'USER'
);


ALTER TYPE public.userrole OWNER TO paqueteria_user;

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: alembic_version; Type: TABLE; Schema: public; Owner: paqueteria_user
--

CREATE TABLE public.alembic_version (
    version_num character varying(32) NOT NULL
);


ALTER TABLE public.alembic_version OWNER TO paqueteria_user;

--
-- Name: customers; Type: TABLE; Schema: public; Owner: paqueteria_user
--

CREATE TABLE public.customers (
    id uuid NOT NULL,
    name character varying(255) NOT NULL,
    phone character varying(20) NOT NULL,
    tracking_number character varying(50) NOT NULL,
    created_at timestamp without time zone,
    updated_at timestamp without time zone
);


ALTER TABLE public.customers OWNER TO paqueteria_user;

--
-- Name: files; Type: TABLE; Schema: public; Owner: paqueteria_user
--

CREATE TABLE public.files (
    id uuid NOT NULL,
    package_id uuid,
    uploaded_by_user_id uuid,
    filename character varying(255) NOT NULL,
    file_path character varying(500) NOT NULL,
    file_size integer NOT NULL,
    mime_type character varying(100) NOT NULL,
    upload_date timestamp without time zone,
    created_at timestamp without time zone
);


ALTER TABLE public.files OWNER TO paqueteria_user;

--
-- Name: messages; Type: TABLE; Schema: public; Owner: paqueteria_user
--

CREATE TABLE public.messages (
    id uuid NOT NULL,
    sender_id uuid,
    subject character varying(255) NOT NULL,
    content text NOT NULL,
    message_type public.messagetype,
    is_read boolean,
    read_at timestamp without time zone,
    created_at timestamp without time zone
);


ALTER TABLE public.messages OWNER TO paqueteria_user;

--
-- Name: notifications; Type: TABLE; Schema: public; Owner: paqueteria_user
--

CREATE TABLE public.notifications (
    id uuid NOT NULL,
    package_id uuid,
    notification_type public.notificationtype NOT NULL,
    message text NOT NULL,
    status character varying(20),
    sent_at timestamp without time zone,
    delivery_confirmation json,
    created_at timestamp without time zone
);


ALTER TABLE public.notifications OWNER TO paqueteria_user;

--
-- Name: packages; Type: TABLE; Schema: public; Owner: paqueteria_user
--

CREATE TABLE public.packages (
    id uuid NOT NULL,
    tracking_number character varying(50) NOT NULL,
    customer_name character varying(255) NOT NULL,
    customer_phone character varying(20) NOT NULL,
    status public.packagestatus,
    package_type character varying(50),
    package_condition character varying(20),
    storage_cost numeric(10,2),
    delivery_cost numeric(10,2),
    total_cost numeric(10,2),
    observations text,
    announced_at timestamp without time zone,
    received_at timestamp without time zone,
    delivered_at timestamp without time zone,
    created_at timestamp without time zone,
    updated_at timestamp without time zone,
    customer_id uuid
);


ALTER TABLE public.packages OWNER TO paqueteria_user;

--
-- Name: rates; Type: TABLE; Schema: public; Owner: paqueteria_user
--

CREATE TABLE public.rates (
    id uuid NOT NULL,
    rate_type character varying(50) NOT NULL,
    base_price numeric(10,2) NOT NULL,
    daily_storage_rate numeric(10,2) NOT NULL,
    delivery_rate numeric(10,2) NOT NULL,
    package_type_multiplier numeric(3,2),
    is_active boolean,
    valid_from timestamp without time zone,
    valid_to timestamp without time zone,
    created_at timestamp without time zone,
    updated_at timestamp without time zone
);


ALTER TABLE public.rates OWNER TO paqueteria_user;

--
-- Name: users; Type: TABLE; Schema: public; Owner: paqueteria_user
--

CREATE TABLE public.users (
    id uuid NOT NULL,
    username character varying(50) NOT NULL,
    email character varying(100) NOT NULL,
    password_hash character varying(255) NOT NULL,
    first_name character varying(50) NOT NULL,
    last_name character varying(50) NOT NULL,
    phone character varying(20),
    is_active boolean,
    role public.userrole,
    permissions json,
    last_login timestamp without time zone,
    created_at timestamp without time zone,
    updated_at timestamp without time zone
);


ALTER TABLE public.users OWNER TO paqueteria_user;

--
-- Data for Name: alembic_version; Type: TABLE DATA; Schema: public; Owner: paqueteria_user
--

COPY public.alembic_version (version_num) FROM stdin;
001
\.


--
-- Data for Name: customers; Type: TABLE DATA; Schema: public; Owner: paqueteria_user
--

COPY public.customers (id, name, phone, tracking_number, created_at, updated_at) FROM stdin;
0350ccf7-d995-43bb-ab43-a4e9a7f6bc0d	Juan Pérez	3334004007	PAP20250124001	2025-08-24 19:02:07.659606	2025-08-24 19:02:07.659611
51ae6616-cf6a-46ab-b982-9bc0adcd1a04	María García	3001234567	PAP20250124002	2025-08-24 19:02:07.65962	2025-08-24 19:02:07.65962
1c714d79-e484-4f26-9f2f-6dcdd1c3c372	Juan Pérez	3001234567	PAP202508244C58986A	\N	\N
e1b4d450-d531-48e3-a4a3-8f78cd8fc74c	Juan Pérez	3001234567	PAP202508243CF6C344	\N	\N
9ba69762-4625-448c-b123-58de37e5e98f	Juan Pérez	3334004007	PAP20250824BA15FF24	\N	\N
\.


--
-- Data for Name: files; Type: TABLE DATA; Schema: public; Owner: paqueteria_user
--

COPY public.files (id, package_id, uploaded_by_user_id, filename, file_path, file_size, mime_type, upload_date, created_at) FROM stdin;
\.


--
-- Data for Name: messages; Type: TABLE DATA; Schema: public; Owner: paqueteria_user
--

COPY public.messages (id, sender_id, subject, content, message_type, is_read, read_at, created_at) FROM stdin;
\.


--
-- Data for Name: notifications; Type: TABLE DATA; Schema: public; Owner: paqueteria_user
--

COPY public.notifications (id, package_id, notification_type, message, status, sent_at, delivery_confirmation, created_at) FROM stdin;
\.


--
-- Data for Name: packages; Type: TABLE DATA; Schema: public; Owner: paqueteria_user
--

COPY public.packages (id, tracking_number, customer_name, customer_phone, status, package_type, package_condition, storage_cost, delivery_cost, total_cost, observations, announced_at, received_at, delivered_at, created_at, updated_at, customer_id) FROM stdin;
676baf06-6f7b-41ab-800f-f5e125d6f330	PAP20250124001	Juan Pérez	3334004007	ANUNCIADO	documentos	bueno	2000.00	3000.00	5000.00	Paquete con documentos importantes	2025-08-24 19:02:07.657269	\N	\N	2025-08-24 19:02:07.662129	2025-08-24 19:02:07.662131	\N
ee784dda-87e9-490c-a207-c83819270182	PAP20250124002	María García	3001234567	RECIBIDO	ropa	excelente	4000.00	3000.00	7000.00	Ropa nueva	2025-08-24 19:02:07.657418	2025-08-24 19:02:07.657419	\N	2025-08-24 19:02:07.662135	2025-08-24 19:02:07.662136	\N
2cce9175-56ab-4415-8c2b-5e4f3fb44dc6	PAP202508244C58986A	Juan Pérez	3001234567	ANUNCIADO	NORMAL	BUENO	1000.00	1500.00	2500.00	Paquete de prueba	2025-08-24 19:16:21.037216	\N	\N	\N	\N	\N
81f31b6a-ce05-4ad3-94c4-5c72d2634fce	PAP202508243CF6C344	Juan Pérez	3001234567	ANUNCIADO	NORMAL	BUENO	1000.00	1500.00	2500.00	Paquete de prueba	2025-08-24 19:16:58.49761	\N	\N	\N	\N	\N
28c3a5bc-d100-41e2-8fbc-1872abd615fc	PAP20250824BA15FF24	Juan Pérez	3334004007	ANUNCIADO	NORMAL	BUENO	1000.00	1500.00	2500.00	Paquete de prueba	2025-08-24 19:17:15.494505	\N	\N	\N	\N	\N
\.


--
-- Data for Name: rates; Type: TABLE DATA; Schema: public; Owner: paqueteria_user
--

COPY public.rates (id, rate_type, base_price, daily_storage_rate, delivery_rate, package_type_multiplier, is_active, valid_from, valid_to, created_at, updated_at) FROM stdin;
e970573c-0558-42d8-a004-6edc83daa5c2	estandar	5000.00	2000.00	3000.00	1.00	t	\N	\N	2025-08-24 19:02:07.664648	2025-08-24 19:02:07.664651
d0826140-4c70-42f4-b71e-05a83461d2f7	premium	8000.00	3000.00	5000.00	1.50	t	\N	\N	2025-08-24 19:02:07.664655	2025-08-24 19:02:07.664655
\.


--
-- Data for Name: users; Type: TABLE DATA; Schema: public; Owner: paqueteria_user
--

COPY public.users (id, username, email, password_hash, first_name, last_name, phone, is_active, role, permissions, last_login, created_at, updated_at) FROM stdin;
5a88c348-941a-4eaf-9802-c78c1d95378a	admin	admin@papyrus.com.co	$2b$12$N7lHYCVNx65pC.aZPSgHeuPBPJW4x2LW3ceTnsqmE3c4/RS/P09yy	Administrador	Sistema	3334004007	t	ADMIN	{}	2025-08-24 19:02:36.417787	2025-08-24 19:02:07.650167	2025-08-24 19:02:36.150244
0fcb3609-728e-4d7d-997e-d34e665ba5f6	testuser	test@papyrus.com.co	$2b$12$CeCDLN53YA827hg/tKnd8u9KkMjyu8lC1vrDLH8sf0ZHm253j/S7W	Usuario	Prueba	\N	t	USER	{}	\N	\N	\N
341363e1-e2da-4214-a061-808f7c94ed01	testuser2	test2@example.com	$2b$12$gMO53eGK1dcLRkutNvIxi.A4HwJylVMJfE9rAvhJsiRTHc.mopwtC	Test	User	\N	t	USER	{}	\N	\N	\N
259c16f2-0733-46e8-aa17-3ad2bdf246c1	testuser3	test3@example.com	$2b$12$XljtkxZVDgAmMX48NTGSGeApDvpcKpn12g5nYrSr44IUg2NkNquG6	Test	User	\N	t	USER	{}	\N	\N	\N
c3608b3e-67f1-4a46-b945-57cc00130d69	newuser123	newuser123@example.com	$2b$12$z85YnzYg/iQg/HmY1VNf.ufLjR7NV3e7Y5lj6ntE1UTAIwqIyJw/G	New	User	\N	t	USER	{}	2025-08-24 19:14:25.754833	\N	2025-08-24 19:14:25.514167
be349987-8284-4997-92a4-d6e6264b7f07	superadmin	superadmin@papyrus.com.co	$2b$12$eat2RjzCRO8aTP0tyiAWV.jcQgXB849CZOARC98oPEHS39nvu1eJi	Super	Administrador	\N	t	ADMIN	{}	\N	\N	\N
\.


--
-- Name: alembic_version alembic_version_pkc; Type: CONSTRAINT; Schema: public; Owner: paqueteria_user
--

ALTER TABLE ONLY public.alembic_version
    ADD CONSTRAINT alembic_version_pkc PRIMARY KEY (version_num);


--
-- Name: customers customers_pkey; Type: CONSTRAINT; Schema: public; Owner: paqueteria_user
--

ALTER TABLE ONLY public.customers
    ADD CONSTRAINT customers_pkey PRIMARY KEY (id);


--
-- Name: files files_pkey; Type: CONSTRAINT; Schema: public; Owner: paqueteria_user
--

ALTER TABLE ONLY public.files
    ADD CONSTRAINT files_pkey PRIMARY KEY (id);


--
-- Name: messages messages_pkey; Type: CONSTRAINT; Schema: public; Owner: paqueteria_user
--

ALTER TABLE ONLY public.messages
    ADD CONSTRAINT messages_pkey PRIMARY KEY (id);


--
-- Name: notifications notifications_pkey; Type: CONSTRAINT; Schema: public; Owner: paqueteria_user
--

ALTER TABLE ONLY public.notifications
    ADD CONSTRAINT notifications_pkey PRIMARY KEY (id);


--
-- Name: packages packages_pkey; Type: CONSTRAINT; Schema: public; Owner: paqueteria_user
--

ALTER TABLE ONLY public.packages
    ADD CONSTRAINT packages_pkey PRIMARY KEY (id);


--
-- Name: rates rates_pkey; Type: CONSTRAINT; Schema: public; Owner: paqueteria_user
--

ALTER TABLE ONLY public.rates
    ADD CONSTRAINT rates_pkey PRIMARY KEY (id);


--
-- Name: users users_pkey; Type: CONSTRAINT; Schema: public; Owner: paqueteria_user
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_pkey PRIMARY KEY (id);


--
-- Name: ix_customers_tracking_number; Type: INDEX; Schema: public; Owner: paqueteria_user
--

CREATE UNIQUE INDEX ix_customers_tracking_number ON public.customers USING btree (tracking_number);


--
-- Name: ix_packages_tracking_number; Type: INDEX; Schema: public; Owner: paqueteria_user
--

CREATE UNIQUE INDEX ix_packages_tracking_number ON public.packages USING btree (tracking_number);


--
-- Name: ix_users_email; Type: INDEX; Schema: public; Owner: paqueteria_user
--

CREATE UNIQUE INDEX ix_users_email ON public.users USING btree (email);


--
-- Name: ix_users_username; Type: INDEX; Schema: public; Owner: paqueteria_user
--

CREATE UNIQUE INDEX ix_users_username ON public.users USING btree (username);


--
-- Name: files files_package_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: paqueteria_user
--

ALTER TABLE ONLY public.files
    ADD CONSTRAINT files_package_id_fkey FOREIGN KEY (package_id) REFERENCES public.packages(id);


--
-- Name: files files_uploaded_by_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: paqueteria_user
--

ALTER TABLE ONLY public.files
    ADD CONSTRAINT files_uploaded_by_user_id_fkey FOREIGN KEY (uploaded_by_user_id) REFERENCES public.users(id);


--
-- Name: messages messages_sender_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: paqueteria_user
--

ALTER TABLE ONLY public.messages
    ADD CONSTRAINT messages_sender_id_fkey FOREIGN KEY (sender_id) REFERENCES public.users(id);


--
-- Name: notifications notifications_package_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: paqueteria_user
--

ALTER TABLE ONLY public.notifications
    ADD CONSTRAINT notifications_package_id_fkey FOREIGN KEY (package_id) REFERENCES public.packages(id);


--
-- Name: packages packages_customer_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: paqueteria_user
--

ALTER TABLE ONLY public.packages
    ADD CONSTRAINT packages_customer_id_fkey FOREIGN KEY (customer_id) REFERENCES public.customers(id);


--
-- PostgreSQL database dump complete
--

\unrestrict pTKP4g2pHHESwoAx0XsPZj36jQCVlcTXBm1TFnKlcrF92Y8mFs4hmuwGSbRa4DF

