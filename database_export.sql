--
-- PostgreSQL database dump
--

-- Dumped from database version 16.9
-- Dumped by pg_dump version 17.5

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET transaction_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: admins; Type: TABLE; Schema: public; Owner: neondb_owner
--

CREATE TABLE public.admins (
    id integer NOT NULL,
    email character varying(120) NOT NULL,
    password_hash character varying(256) NOT NULL,
    full_name character varying(100) NOT NULL,
    admin_id character varying(20) NOT NULL,
    role character varying(50),
    permissions text,
    is_active boolean,
    is_super_admin boolean,
    profile_image character varying(200),
    phone character varying(20),
    created_at timestamp without time zone,
    updated_at timestamp without time zone,
    last_login timestamp without time zone
);


ALTER TABLE public.admins OWNER TO neondb_owner;

--
-- Name: admins_id_seq; Type: SEQUENCE; Schema: public; Owner: neondb_owner
--

CREATE SEQUENCE public.admins_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.admins_id_seq OWNER TO neondb_owner;

--
-- Name: admins_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: neondb_owner
--

ALTER SEQUENCE public.admins_id_seq OWNED BY public.admins.id;


--
-- Name: applications; Type: TABLE; Schema: public; Owner: neondb_owner
--

CREATE TABLE public.applications (
    id integer NOT NULL,
    user_id integer,
    property_id character varying(50),
    property_name character varying(200) NOT NULL,
    complex_name character varying(200) NOT NULL,
    status character varying(20),
    message text,
    preferred_contact character varying(20),
    created_at timestamp without time zone,
    updated_at timestamp without time zone,
    contact_name character varying(200),
    contact_email character varying(120),
    contact_phone character varying(20)
);


ALTER TABLE public.applications OWNER TO neondb_owner;

--
-- Name: applications_id_seq; Type: SEQUENCE; Schema: public; Owner: neondb_owner
--

CREATE SEQUENCE public.applications_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.applications_id_seq OWNER TO neondb_owner;

--
-- Name: applications_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: neondb_owner
--

ALTER SEQUENCE public.applications_id_seq OWNED BY public.applications.id;


--
-- Name: blog_article_tags; Type: TABLE; Schema: public; Owner: neondb_owner
--

CREATE TABLE public.blog_article_tags (
    article_id integer NOT NULL,
    tag_id integer NOT NULL
);


ALTER TABLE public.blog_article_tags OWNER TO neondb_owner;

--
-- Name: blog_articles; Type: TABLE; Schema: public; Owner: neondb_owner
--

CREATE TABLE public.blog_articles (
    id integer NOT NULL,
    title character varying(200) NOT NULL,
    slug character varying(200) NOT NULL,
    excerpt character varying(500),
    content text NOT NULL,
    author_id integer NOT NULL,
    author_name character varying(100),
    category_id integer NOT NULL,
    status character varying(20),
    published_at timestamp without time zone,
    scheduled_at timestamp without time zone,
    meta_title character varying(200),
    meta_description character varying(300),
    meta_keywords character varying(500),
    featured_image character varying(300),
    featured_image_alt character varying(200),
    is_featured boolean,
    allow_comments boolean,
    views_count integer,
    reading_time integer,
    created_at timestamp without time zone,
    updated_at timestamp without time zone,
    category character varying(255)
);


ALTER TABLE public.blog_articles OWNER TO neondb_owner;

--
-- Name: blog_articles_id_seq; Type: SEQUENCE; Schema: public; Owner: neondb_owner
--

CREATE SEQUENCE public.blog_articles_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.blog_articles_id_seq OWNER TO neondb_owner;

--
-- Name: blog_articles_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: neondb_owner
--

ALTER SEQUENCE public.blog_articles_id_seq OWNED BY public.blog_articles.id;


--
-- Name: blog_categories; Type: TABLE; Schema: public; Owner: neondb_owner
--

CREATE TABLE public.blog_categories (
    id integer NOT NULL,
    name character varying(100) NOT NULL,
    slug character varying(100) NOT NULL,
    description text,
    color character varying(20),
    icon character varying(50),
    meta_title character varying(200),
    meta_description character varying(300),
    sort_order integer,
    is_active boolean,
    articles_count integer,
    views_count integer,
    created_at timestamp without time zone,
    updated_at timestamp without time zone
);


ALTER TABLE public.blog_categories OWNER TO neondb_owner;

--
-- Name: blog_categories_id_seq; Type: SEQUENCE; Schema: public; Owner: neondb_owner
--

CREATE SEQUENCE public.blog_categories_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.blog_categories_id_seq OWNER TO neondb_owner;

--
-- Name: blog_categories_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: neondb_owner
--

ALTER SEQUENCE public.blog_categories_id_seq OWNED BY public.blog_categories.id;


--
-- Name: blog_comments; Type: TABLE; Schema: public; Owner: neondb_owner
--

CREATE TABLE public.blog_comments (
    id integer NOT NULL,
    article_id integer NOT NULL,
    author_name character varying(100) NOT NULL,
    author_email character varying(120) NOT NULL,
    author_website character varying(200),
    user_id integer,
    content text NOT NULL,
    status character varying(20),
    ip_address character varying(50),
    user_agent character varying(300),
    parent_id integer,
    created_at timestamp without time zone,
    updated_at timestamp without time zone
);


ALTER TABLE public.blog_comments OWNER TO neondb_owner;

--
-- Name: blog_comments_id_seq; Type: SEQUENCE; Schema: public; Owner: neondb_owner
--

CREATE SEQUENCE public.blog_comments_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.blog_comments_id_seq OWNER TO neondb_owner;

--
-- Name: blog_comments_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: neondb_owner
--

ALTER SEQUENCE public.blog_comments_id_seq OWNED BY public.blog_comments.id;


--
-- Name: blog_posts; Type: TABLE; Schema: public; Owner: neondb_owner
--

CREATE TABLE public.blog_posts (
    id integer NOT NULL,
    title character varying(255) NOT NULL,
    slug character varying(255) NOT NULL,
    content text NOT NULL,
    excerpt text,
    meta_title character varying(255),
    meta_description text,
    meta_keywords character varying(500),
    status character varying(20),
    featured_image character varying(500),
    category character varying(100),
    tags text,
    author_id integer NOT NULL,
    published_at timestamp without time zone,
    scheduled_for timestamp without time zone,
    views_count integer,
    likes_count integer,
    created_at timestamp without time zone,
    updated_at timestamp without time zone
);


ALTER TABLE public.blog_posts OWNER TO neondb_owner;

--
-- Name: blog_posts_id_seq; Type: SEQUENCE; Schema: public; Owner: neondb_owner
--

CREATE SEQUENCE public.blog_posts_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.blog_posts_id_seq OWNER TO neondb_owner;

--
-- Name: blog_posts_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: neondb_owner
--

ALTER SEQUENCE public.blog_posts_id_seq OWNED BY public.blog_posts.id;


--
-- Name: blog_tags; Type: TABLE; Schema: public; Owner: neondb_owner
--

CREATE TABLE public.blog_tags (
    id integer NOT NULL,
    name character varying(50) NOT NULL,
    slug character varying(50) NOT NULL,
    description text,
    usage_count integer,
    created_at timestamp without time zone
);


ALTER TABLE public.blog_tags OWNER TO neondb_owner;

--
-- Name: blog_tags_id_seq; Type: SEQUENCE; Schema: public; Owner: neondb_owner
--

CREATE SEQUENCE public.blog_tags_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.blog_tags_id_seq OWNER TO neondb_owner;

--
-- Name: blog_tags_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: neondb_owner
--

ALTER SEQUENCE public.blog_tags_id_seq OWNED BY public.blog_tags.id;


--
-- Name: callback_requests; Type: TABLE; Schema: public; Owner: neondb_owner
--

CREATE TABLE public.callback_requests (
    id integer NOT NULL,
    name character varying(200) NOT NULL,
    phone character varying(20) NOT NULL,
    email character varying(120),
    preferred_time character varying(50),
    notes text,
    interest character varying(100),
    budget character varying(50),
    timing character varying(50),
    status character varying(50),
    assigned_manager_id integer,
    manager_notes text,
    created_at timestamp without time zone,
    processed_at timestamp without time zone
);


ALTER TABLE public.callback_requests OWNER TO neondb_owner;

--
-- Name: callback_requests_id_seq; Type: SEQUENCE; Schema: public; Owner: neondb_owner
--

CREATE SEQUENCE public.callback_requests_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.callback_requests_id_seq OWNER TO neondb_owner;

--
-- Name: callback_requests_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: neondb_owner
--

ALTER SEQUENCE public.callback_requests_id_seq OWNED BY public.callback_requests.id;


--
-- Name: cashback_applications; Type: TABLE; Schema: public; Owner: neondb_owner
--

CREATE TABLE public.cashback_applications (
    id integer NOT NULL,
    user_id integer NOT NULL,
    property_id character varying(50),
    property_name character varying(200) NOT NULL,
    property_type character varying(50) NOT NULL,
    property_size double precision NOT NULL,
    property_price integer NOT NULL,
    complex_name character varying(200) NOT NULL,
    developer_name character varying(200) NOT NULL,
    cashback_amount integer NOT NULL,
    cashback_percent double precision NOT NULL,
    status character varying(50),
    application_date timestamp without time zone,
    approved_date timestamp without time zone,
    payout_date timestamp without time zone,
    notes text,
    approved_by_manager_id integer,
    manager_notes text,
    created_at timestamp without time zone,
    updated_at timestamp without time zone
);


ALTER TABLE public.cashback_applications OWNER TO neondb_owner;

--
-- Name: cashback_applications_id_seq; Type: SEQUENCE; Schema: public; Owner: neondb_owner
--

CREATE SEQUENCE public.cashback_applications_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.cashback_applications_id_seq OWNER TO neondb_owner;

--
-- Name: cashback_applications_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: neondb_owner
--

ALTER SEQUENCE public.cashback_applications_id_seq OWNED BY public.cashback_applications.id;


--
-- Name: cashback_payouts; Type: TABLE; Schema: public; Owner: neondb_owner
--

CREATE TABLE public.cashback_payouts (
    id integer NOT NULL,
    user_id integer NOT NULL,
    amount numeric(15,2) NOT NULL,
    status character varying(50),
    payment_method character varying(100),
    admin_notes text,
    requested_at timestamp without time zone,
    processed_at timestamp without time zone
);


ALTER TABLE public.cashback_payouts OWNER TO neondb_owner;

--
-- Name: cashback_payouts_id_seq; Type: SEQUENCE; Schema: public; Owner: neondb_owner
--

CREATE SEQUENCE public.cashback_payouts_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.cashback_payouts_id_seq OWNER TO neondb_owner;

--
-- Name: cashback_payouts_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: neondb_owner
--

ALTER SEQUENCE public.cashback_payouts_id_seq OWNED BY public.cashback_payouts.id;


--
-- Name: cashback_records; Type: TABLE; Schema: public; Owner: neondb_owner
--

CREATE TABLE public.cashback_records (
    id integer NOT NULL,
    user_id integer NOT NULL,
    property_id integer,
    property_name character varying(200) NOT NULL,
    property_price double precision NOT NULL,
    amount double precision NOT NULL,
    percentage double precision NOT NULL,
    status character varying(20),
    created_at timestamp without time zone,
    approved_at timestamp without time zone,
    paid_at timestamp without time zone
);


ALTER TABLE public.cashback_records OWNER TO neondb_owner;

--
-- Name: cashback_records_id_seq; Type: SEQUENCE; Schema: public; Owner: neondb_owner
--

CREATE SEQUENCE public.cashback_records_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.cashback_records_id_seq OWNER TO neondb_owner;

--
-- Name: cashback_records_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: neondb_owner
--

ALTER SEQUENCE public.cashback_records_id_seq OWNED BY public.cashback_records.id;


--
-- Name: cities; Type: TABLE; Schema: public; Owner: neondb_owner
--

CREATE TABLE public.cities (
    id integer NOT NULL,
    name character varying(100) NOT NULL,
    slug character varying(100) NOT NULL,
    is_active boolean,
    is_default boolean,
    phone character varying(20),
    email character varying(120),
    address character varying(200),
    latitude double precision,
    longitude double precision,
    zoom_level integer,
    description text,
    meta_title character varying(200),
    meta_description character varying(300),
    created_at timestamp without time zone,
    updated_at timestamp without time zone
);


ALTER TABLE public.cities OWNER TO neondb_owner;

--
-- Name: cities_id_seq; Type: SEQUENCE; Schema: public; Owner: neondb_owner
--

CREATE SEQUENCE public.cities_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.cities_id_seq OWNER TO neondb_owner;

--
-- Name: cities_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: neondb_owner
--

ALTER SEQUENCE public.cities_id_seq OWNED BY public.cities.id;


--
-- Name: client_property_recommendations; Type: TABLE; Schema: public; Owner: neondb_owner
--

CREATE TABLE public.client_property_recommendations (
    id integer NOT NULL,
    manager_id integer NOT NULL,
    client_id integer NOT NULL,
    search_id integer NOT NULL,
    message text,
    sent_at timestamp without time zone,
    viewed_at timestamp without time zone
);


ALTER TABLE public.client_property_recommendations OWNER TO neondb_owner;

--
-- Name: client_property_recommendations_id_seq; Type: SEQUENCE; Schema: public; Owner: neondb_owner
--

CREATE SEQUENCE public.client_property_recommendations_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.client_property_recommendations_id_seq OWNER TO neondb_owner;

--
-- Name: client_property_recommendations_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: neondb_owner
--

ALTER SEQUENCE public.client_property_recommendations_id_seq OWNED BY public.client_property_recommendations.id;


--
-- Name: collection_properties; Type: TABLE; Schema: public; Owner: neondb_owner
--

CREATE TABLE public.collection_properties (
    id integer NOT NULL,
    collection_id integer NOT NULL,
    property_id character varying(100) NOT NULL,
    property_name character varying(255),
    property_price integer,
    complex_name character varying(255),
    property_type character varying(100),
    property_size double precision,
    manager_note text,
    order_index integer,
    created_at timestamp without time zone,
    added_at timestamp without time zone DEFAULT now()
);


ALTER TABLE public.collection_properties OWNER TO neondb_owner;

--
-- Name: collection_properties_id_seq; Type: SEQUENCE; Schema: public; Owner: neondb_owner
--

CREATE SEQUENCE public.collection_properties_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.collection_properties_id_seq OWNER TO neondb_owner;

--
-- Name: collection_properties_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: neondb_owner
--

ALTER SEQUENCE public.collection_properties_id_seq OWNED BY public.collection_properties.id;


--
-- Name: collections; Type: TABLE; Schema: public; Owner: neondb_owner
--

CREATE TABLE public.collections (
    id integer NOT NULL,
    title character varying(255) NOT NULL,
    description text,
    created_by_manager_id integer NOT NULL,
    assigned_to_user_id integer,
    status character varying(50),
    is_public boolean,
    tags text,
    created_at timestamp without time zone,
    updated_at timestamp without time zone,
    sent_at timestamp without time zone,
    viewed_at timestamp without time zone,
    name character varying(255)
);


ALTER TABLE public.collections OWNER TO neondb_owner;

--
-- Name: collections_id_seq; Type: SEQUENCE; Schema: public; Owner: neondb_owner
--

CREATE SEQUENCE public.collections_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.collections_id_seq OWNER TO neondb_owner;

--
-- Name: collections_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: neondb_owner
--

ALTER SEQUENCE public.collections_id_seq OWNED BY public.collections.id;


--
-- Name: developer_appointments; Type: TABLE; Schema: public; Owner: neondb_owner
--

CREATE TABLE public.developer_appointments (
    id integer NOT NULL,
    user_id integer NOT NULL,
    property_id character varying(50) NOT NULL,
    developer_name character varying(200) NOT NULL,
    complex_name character varying(200) NOT NULL,
    appointment_date timestamp without time zone NOT NULL,
    appointment_time character varying(10) NOT NULL,
    status character varying(50),
    client_name character varying(200) NOT NULL,
    client_phone character varying(20) NOT NULL,
    notes text,
    created_at timestamp without time zone
);


ALTER TABLE public.developer_appointments OWNER TO neondb_owner;

--
-- Name: developer_appointments_id_seq; Type: SEQUENCE; Schema: public; Owner: neondb_owner
--

CREATE SEQUENCE public.developer_appointments_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.developer_appointments_id_seq OWNER TO neondb_owner;

--
-- Name: developer_appointments_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: neondb_owner
--

ALTER SEQUENCE public.developer_appointments_id_seq OWNED BY public.developer_appointments.id;


--
-- Name: developers; Type: TABLE; Schema: public; Owner: neondb_owner
--

CREATE TABLE public.developers (
    id integer NOT NULL,
    name character varying(100) NOT NULL,
    slug character varying(100) NOT NULL
);


ALTER TABLE public.developers OWNER TO neondb_owner;

--
-- Name: developers_id_seq; Type: SEQUENCE; Schema: public; Owner: neondb_owner
--

CREATE SEQUENCE public.developers_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.developers_id_seq OWNER TO neondb_owner;

--
-- Name: developers_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: neondb_owner
--

ALTER SEQUENCE public.developers_id_seq OWNED BY public.developers.id;


--
-- Name: districts; Type: TABLE; Schema: public; Owner: neondb_owner
--

CREATE TABLE public.districts (
    id integer NOT NULL,
    name character varying(100) NOT NULL,
    slug character varying(100) NOT NULL,
    description text,
    city_id integer DEFAULT 1,
    coordinates character varying(100),
    is_active boolean DEFAULT true,
    latitude numeric(10,8),
    longitude numeric(11,8),
    created_at timestamp without time zone DEFAULT now(),
    updated_at timestamp without time zone DEFAULT now()
);


ALTER TABLE public.districts OWNER TO neondb_owner;

--
-- Name: districts_id_seq; Type: SEQUENCE; Schema: public; Owner: neondb_owner
--

CREATE SEQUENCE public.districts_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.districts_id_seq OWNER TO neondb_owner;

--
-- Name: districts_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: neondb_owner
--

ALTER SEQUENCE public.districts_id_seq OWNED BY public.districts.id;


--
-- Name: documents; Type: TABLE; Schema: public; Owner: neondb_owner
--

CREATE TABLE public.documents (
    id integer NOT NULL,
    user_id integer NOT NULL,
    filename character varying(200) NOT NULL,
    original_filename character varying(200) NOT NULL,
    file_type character varying(50) NOT NULL,
    file_size integer NOT NULL,
    file_path character varying(500) NOT NULL,
    document_type character varying(100),
    status character varying(50),
    reviewed_at timestamp without time zone,
    reviewer_notes text,
    reviewed_by_manager_id integer,
    created_at timestamp without time zone,
    updated_at timestamp without time zone
);


ALTER TABLE public.documents OWNER TO neondb_owner;

--
-- Name: documents_id_seq; Type: SEQUENCE; Schema: public; Owner: neondb_owner
--

CREATE SEQUENCE public.documents_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.documents_id_seq OWNER TO neondb_owner;

--
-- Name: documents_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: neondb_owner
--

ALTER SEQUENCE public.documents_id_seq OWNED BY public.documents.id;


--
-- Name: favorite_properties; Type: TABLE; Schema: public; Owner: neondb_owner
--

CREATE TABLE public.favorite_properties (
    id integer NOT NULL,
    user_id integer NOT NULL,
    property_id character varying(50),
    property_name character varying(200),
    property_type character varying(50),
    property_size double precision,
    property_price integer,
    complex_name character varying(200),
    developer_name character varying(200),
    property_image character varying(500),
    property_url character varying(500),
    cashback_amount integer,
    cashback_percent double precision,
    created_at timestamp without time zone
);


ALTER TABLE public.favorite_properties OWNER TO neondb_owner;

--
-- Name: favorite_properties_id_seq; Type: SEQUENCE; Schema: public; Owner: neondb_owner
--

CREATE SEQUENCE public.favorite_properties_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.favorite_properties_id_seq OWNER TO neondb_owner;

--
-- Name: favorite_properties_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: neondb_owner
--

ALTER SEQUENCE public.favorite_properties_id_seq OWNED BY public.favorite_properties.id;


--
-- Name: favorites; Type: TABLE; Schema: public; Owner: neondb_owner
--

CREATE TABLE public.favorites (
    id integer NOT NULL,
    user_id integer NOT NULL,
    property_id integer NOT NULL,
    created_at timestamp without time zone
);


ALTER TABLE public.favorites OWNER TO neondb_owner;

--
-- Name: favorites_id_seq; Type: SEQUENCE; Schema: public; Owner: neondb_owner
--

CREATE SEQUENCE public.favorites_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.favorites_id_seq OWNER TO neondb_owner;

--
-- Name: favorites_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: neondb_owner
--

ALTER SEQUENCE public.favorites_id_seq OWNED BY public.favorites.id;


--
-- Name: manager_saved_searches; Type: TABLE; Schema: public; Owner: neondb_owner
--

CREATE TABLE public.manager_saved_searches (
    id integer NOT NULL,
    manager_id integer NOT NULL,
    name character varying(100) NOT NULL,
    description text,
    search_type character varying(20),
    location character varying(200),
    property_type character varying(50),
    price_min integer,
    price_max integer,
    size_min double precision,
    size_max double precision,
    developer character varying(200),
    complex_name character varying(200),
    floor_min integer,
    floor_max integer,
    cashback_min integer,
    additional_filters text,
    is_template boolean,
    usage_count integer,
    created_at timestamp without time zone,
    updated_at timestamp without time zone,
    last_used timestamp without time zone
);


ALTER TABLE public.manager_saved_searches OWNER TO neondb_owner;

--
-- Name: manager_saved_searches_id_seq; Type: SEQUENCE; Schema: public; Owner: neondb_owner
--

CREATE SEQUENCE public.manager_saved_searches_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.manager_saved_searches_id_seq OWNER TO neondb_owner;

--
-- Name: manager_saved_searches_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: neondb_owner
--

ALTER SEQUENCE public.manager_saved_searches_id_seq OWNED BY public.manager_saved_searches.id;


--
-- Name: managers; Type: TABLE; Schema: public; Owner: neondb_owner
--

CREATE TABLE public.managers (
    id integer NOT NULL,
    email character varying(120) NOT NULL,
    password_hash character varying(256) NOT NULL,
    first_name character varying(50) NOT NULL,
    last_name character varying(50) NOT NULL,
    phone character varying(20),
    "position" character varying(50),
    can_approve_cashback boolean,
    can_manage_documents boolean,
    can_create_collections boolean,
    max_cashback_approval integer,
    is_active boolean,
    profile_image character varying(200),
    manager_id character varying(20) NOT NULL,
    created_at timestamp without time zone,
    updated_at timestamp without time zone,
    last_login timestamp without time zone
);


ALTER TABLE public.managers OWNER TO neondb_owner;

--
-- Name: managers_id_seq; Type: SEQUENCE; Schema: public; Owner: neondb_owner
--

CREATE SEQUENCE public.managers_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.managers_id_seq OWNER TO neondb_owner;

--
-- Name: managers_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: neondb_owner
--

ALTER SEQUENCE public.managers_id_seq OWNED BY public.managers.id;


--
-- Name: notifications; Type: TABLE; Schema: public; Owner: neondb_owner
--

CREATE TABLE public.notifications (
    id integer NOT NULL,
    user_id integer NOT NULL,
    title character varying(200) NOT NULL,
    message text NOT NULL,
    type character varying(50),
    icon character varying(50),
    is_read boolean,
    created_at timestamp without time zone
);


ALTER TABLE public.notifications OWNER TO neondb_owner;

--
-- Name: notifications_id_seq; Type: SEQUENCE; Schema: public; Owner: neondb_owner
--

CREATE SEQUENCE public.notifications_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.notifications_id_seq OWNER TO neondb_owner;

--
-- Name: notifications_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: neondb_owner
--

ALTER SEQUENCE public.notifications_id_seq OWNED BY public.notifications.id;


--
-- Name: recommendation_categories; Type: TABLE; Schema: public; Owner: neondb_owner
--

CREATE TABLE public.recommendation_categories (
    id integer NOT NULL,
    name character varying(255) NOT NULL,
    description text,
    manager_id integer NOT NULL,
    client_id integer NOT NULL,
    color character varying(20),
    is_active boolean,
    recommendations_count integer,
    last_used timestamp without time zone,
    created_at timestamp without time zone,
    updated_at timestamp without time zone
);


ALTER TABLE public.recommendation_categories OWNER TO neondb_owner;

--
-- Name: recommendation_categories_id_seq; Type: SEQUENCE; Schema: public; Owner: neondb_owner
--

CREATE SEQUENCE public.recommendation_categories_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.recommendation_categories_id_seq OWNER TO neondb_owner;

--
-- Name: recommendation_categories_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: neondb_owner
--

ALTER SEQUENCE public.recommendation_categories_id_seq OWNED BY public.recommendation_categories.id;


--
-- Name: recommendation_templates; Type: TABLE; Schema: public; Owner: neondb_owner
--

CREATE TABLE public.recommendation_templates (
    id integer NOT NULL,
    manager_id integer NOT NULL,
    name character varying(255) NOT NULL,
    description text,
    recommendation_type character varying(20) NOT NULL,
    default_title character varying(255),
    default_description text,
    default_notes text,
    default_highlighted_features text,
    default_priority character varying(20),
    is_active boolean,
    usage_count integer,
    created_at timestamp without time zone,
    updated_at timestamp without time zone,
    last_used timestamp without time zone
);


ALTER TABLE public.recommendation_templates OWNER TO neondb_owner;

--
-- Name: recommendation_templates_id_seq; Type: SEQUENCE; Schema: public; Owner: neondb_owner
--

CREATE SEQUENCE public.recommendation_templates_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.recommendation_templates_id_seq OWNER TO neondb_owner;

--
-- Name: recommendation_templates_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: neondb_owner
--

ALTER SEQUENCE public.recommendation_templates_id_seq OWNED BY public.recommendation_templates.id;


--
-- Name: recommendations; Type: TABLE; Schema: public; Owner: neondb_owner
--

CREATE TABLE public.recommendations (
    id integer NOT NULL,
    manager_id integer NOT NULL,
    client_id integer NOT NULL,
    category_id integer,
    title character varying(255) NOT NULL,
    description text,
    recommendation_type character varying(20) NOT NULL,
    item_id character varying(100) NOT NULL,
    item_name character varying(255) NOT NULL,
    item_data text,
    manager_notes text,
    highlighted_features text,
    priority_level character varying(20),
    status character varying(20),
    viewed_at timestamp without time zone,
    responded_at timestamp without time zone,
    client_response character varying(20),
    client_notes text,
    viewing_requested boolean,
    viewing_scheduled_at timestamp without time zone,
    created_at timestamp without time zone,
    sent_at timestamp without time zone,
    expires_at timestamp without time zone,
    user_id integer,
    property_id character varying(255),
    created_by_manager_id integer,
    recommendation_reason text,
    updated_at timestamp without time zone DEFAULT now()
);


ALTER TABLE public.recommendations OWNER TO neondb_owner;

--
-- Name: recommendations_id_seq; Type: SEQUENCE; Schema: public; Owner: neondb_owner
--

CREATE SEQUENCE public.recommendations_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.recommendations_id_seq OWNER TO neondb_owner;

--
-- Name: recommendations_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: neondb_owner
--

ALTER SEQUENCE public.recommendations_id_seq OWNED BY public.recommendations.id;


--
-- Name: residential_complexes; Type: TABLE; Schema: public; Owner: neondb_owner
--

CREATE TABLE public.residential_complexes (
    id integer NOT NULL,
    name character varying(100) NOT NULL,
    slug character varying(100) NOT NULL,
    district_id integer,
    developer_id integer,
    description text,
    short_description text,
    street_id integer,
    address character varying(500),
    property_class character varying(100),
    building_type character varying(100),
    total_buildings integer DEFAULT 0,
    total_floors integer DEFAULT 0,
    total_apartments integer DEFAULT 0,
    construction_status character varying(50),
    construction_year integer,
    delivery_quarter character varying(50),
    latitude numeric(10,8),
    longitude numeric(11,8),
    min_price bigint DEFAULT 0,
    max_price bigint DEFAULT 0,
    price_per_sqm integer DEFAULT 0,
    parking boolean DEFAULT false,
    playground boolean DEFAULT false,
    security boolean DEFAULT false,
    concierge boolean DEFAULT false,
    gym boolean DEFAULT false,
    kindergarten boolean DEFAULT false,
    metro_distance integer,
    school_distance integer,
    hospital_distance integer,
    gallery text,
    main_image character varying(500),
    video_url character varying(500),
    mortgage_available boolean DEFAULT true,
    family_mortgage boolean DEFAULT false,
    it_mortgage boolean DEFAULT false,
    preferential_mortgage boolean DEFAULT false,
    meta_title character varying(200),
    meta_description character varying(500),
    is_active boolean DEFAULT true,
    is_featured boolean DEFAULT false,
    views integer DEFAULT 0,
    created_at timestamp without time zone DEFAULT now(),
    updated_at timestamp without time zone DEFAULT now()
);


ALTER TABLE public.residential_complexes OWNER TO neondb_owner;

--
-- Name: residential_complexes_id_seq; Type: SEQUENCE; Schema: public; Owner: neondb_owner
--

CREATE SEQUENCE public.residential_complexes_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.residential_complexes_id_seq OWNER TO neondb_owner;

--
-- Name: residential_complexes_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: neondb_owner
--

ALTER SEQUENCE public.residential_complexes_id_seq OWNED BY public.residential_complexes.id;


--
-- Name: room_types; Type: TABLE; Schema: public; Owner: neondb_owner
--

CREATE TABLE public.room_types (
    id integer NOT NULL,
    name character varying(50) NOT NULL,
    rooms_count integer
);


ALTER TABLE public.room_types OWNER TO neondb_owner;

--
-- Name: room_types_id_seq; Type: SEQUENCE; Schema: public; Owner: neondb_owner
--

CREATE SEQUENCE public.room_types_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.room_types_id_seq OWNER TO neondb_owner;

--
-- Name: room_types_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: neondb_owner
--

ALTER SEQUENCE public.room_types_id_seq OWNED BY public.room_types.id;


--
-- Name: saved_searches; Type: TABLE; Schema: public; Owner: neondb_owner
--

CREATE TABLE public.saved_searches (
    id integer NOT NULL,
    user_id integer NOT NULL,
    name character varying(100) NOT NULL,
    description text,
    search_type character varying(20),
    location character varying(200),
    property_type character varying(50),
    price_min integer,
    price_max integer,
    size_min double precision,
    size_max double precision,
    developer character varying(200),
    complex_name character varying(200),
    floor_min integer,
    floor_max integer,
    cashback_min integer,
    additional_filters text,
    notify_new_matches boolean,
    last_notification_sent timestamp without time zone,
    created_from_quiz boolean,
    created_at timestamp without time zone,
    updated_at timestamp without time zone,
    last_used timestamp without time zone,
    search_name character varying(255),
    search_criteria text,
    email_notifications boolean DEFAULT true,
    telegram_notifications boolean DEFAULT false,
    is_active boolean DEFAULT true,
    last_checked timestamp without time zone
);


ALTER TABLE public.saved_searches OWNER TO neondb_owner;

--
-- Name: saved_searches_id_seq; Type: SEQUENCE; Schema: public; Owner: neondb_owner
--

CREATE SEQUENCE public.saved_searches_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.saved_searches_id_seq OWNER TO neondb_owner;

--
-- Name: saved_searches_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: neondb_owner
--

ALTER SEQUENCE public.saved_searches_id_seq OWNED BY public.saved_searches.id;


--
-- Name: search_categories; Type: TABLE; Schema: public; Owner: neondb_owner
--

CREATE TABLE public.search_categories (
    id integer NOT NULL,
    name character varying(100) NOT NULL,
    category_type character varying(50) NOT NULL,
    slug character varying(100) NOT NULL,
    created_at timestamp without time zone
);


ALTER TABLE public.search_categories OWNER TO neondb_owner;

--
-- Name: search_categories_id_seq; Type: SEQUENCE; Schema: public; Owner: neondb_owner
--

CREATE SEQUENCE public.search_categories_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.search_categories_id_seq OWNER TO neondb_owner;

--
-- Name: search_categories_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: neondb_owner
--

ALTER SEQUENCE public.search_categories_id_seq OWNED BY public.search_categories.id;


--
-- Name: sent_searches; Type: TABLE; Schema: public; Owner: neondb_owner
--

CREATE TABLE public.sent_searches (
    id integer NOT NULL,
    manager_id integer NOT NULL,
    client_id integer NOT NULL,
    manager_search_id integer,
    name character varying(100) NOT NULL,
    description text,
    additional_filters text,
    status character varying(20),
    viewed_at timestamp without time zone,
    applied_at timestamp without time zone,
    expires_at timestamp without time zone,
    sent_at timestamp without time zone
);


ALTER TABLE public.sent_searches OWNER TO neondb_owner;

--
-- Name: sent_searches_id_seq; Type: SEQUENCE; Schema: public; Owner: neondb_owner
--

CREATE SEQUENCE public.sent_searches_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.sent_searches_id_seq OWNER TO neondb_owner;

--
-- Name: sent_searches_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: neondb_owner
--

ALTER SEQUENCE public.sent_searches_id_seq OWNED BY public.sent_searches.id;


--
-- Name: streets; Type: TABLE; Schema: public; Owner: neondb_owner
--

CREATE TABLE public.streets (
    id integer NOT NULL,
    name character varying(100) NOT NULL,
    slug character varying(100) NOT NULL,
    district_id integer
);


ALTER TABLE public.streets OWNER TO neondb_owner;

--
-- Name: streets_id_seq; Type: SEQUENCE; Schema: public; Owner: neondb_owner
--

CREATE SEQUENCE public.streets_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.streets_id_seq OWNER TO neondb_owner;

--
-- Name: streets_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: neondb_owner
--

ALTER SEQUENCE public.streets_id_seq OWNED BY public.streets.id;


--
-- Name: user_notifications; Type: TABLE; Schema: public; Owner: neondb_owner
--

CREATE TABLE public.user_notifications (
    id integer NOT NULL,
    user_id integer NOT NULL,
    title character varying(200) NOT NULL,
    message text NOT NULL,
    notification_type character varying(50),
    icon character varying(50),
    is_read boolean,
    action_url character varying(500),
    created_at timestamp without time zone,
    read_at timestamp without time zone
);


ALTER TABLE public.user_notifications OWNER TO neondb_owner;

--
-- Name: user_notifications_id_seq; Type: SEQUENCE; Schema: public; Owner: neondb_owner
--

CREATE SEQUENCE public.user_notifications_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.user_notifications_id_seq OWNER TO neondb_owner;

--
-- Name: user_notifications_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: neondb_owner
--

ALTER SEQUENCE public.user_notifications_id_seq OWNED BY public.user_notifications.id;


--
-- Name: users; Type: TABLE; Schema: public; Owner: neondb_owner
--

CREATE TABLE public.users (
    id integer NOT NULL,
    email character varying(120) NOT NULL,
    phone character varying(20),
    telegram_id character varying(50),
    full_name character varying(100) NOT NULL,
    password_hash character varying(256),
    preferred_contact character varying(20),
    email_notifications boolean,
    telegram_notifications boolean,
    notify_recommendations boolean,
    notify_saved_searches boolean,
    notify_applications boolean,
    notify_cashback boolean,
    notify_marketing boolean,
    profile_image character varying(200),
    user_id character varying(20) NOT NULL,
    role character varying(20),
    is_active boolean,
    is_verified boolean,
    verification_token character varying(100),
    is_demo boolean,
    verified boolean,
    registration_source character varying(50),
    client_notes text,
    assigned_manager_id integer,
    client_status character varying(50),
    preferred_district character varying(100),
    property_type character varying(50),
    room_count character varying(20),
    budget_range character varying(50),
    quiz_completed boolean,
    created_at timestamp without time zone,
    updated_at timestamp without time zone,
    last_login timestamp without time zone
);


ALTER TABLE public.users OWNER TO neondb_owner;

--
-- Name: users_id_seq; Type: SEQUENCE; Schema: public; Owner: neondb_owner
--

CREATE SEQUENCE public.users_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.users_id_seq OWNER TO neondb_owner;

--
-- Name: users_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: neondb_owner
--

ALTER SEQUENCE public.users_id_seq OWNED BY public.users.id;


--
-- Name: admins id; Type: DEFAULT; Schema: public; Owner: neondb_owner
--

ALTER TABLE ONLY public.admins ALTER COLUMN id SET DEFAULT nextval('public.admins_id_seq'::regclass);


--
-- Name: applications id; Type: DEFAULT; Schema: public; Owner: neondb_owner
--

ALTER TABLE ONLY public.applications ALTER COLUMN id SET DEFAULT nextval('public.applications_id_seq'::regclass);


--
-- Name: blog_articles id; Type: DEFAULT; Schema: public; Owner: neondb_owner
--

ALTER TABLE ONLY public.blog_articles ALTER COLUMN id SET DEFAULT nextval('public.blog_articles_id_seq'::regclass);


--
-- Name: blog_categories id; Type: DEFAULT; Schema: public; Owner: neondb_owner
--

ALTER TABLE ONLY public.blog_categories ALTER COLUMN id SET DEFAULT nextval('public.blog_categories_id_seq'::regclass);


--
-- Name: blog_comments id; Type: DEFAULT; Schema: public; Owner: neondb_owner
--

ALTER TABLE ONLY public.blog_comments ALTER COLUMN id SET DEFAULT nextval('public.blog_comments_id_seq'::regclass);


--
-- Name: blog_posts id; Type: DEFAULT; Schema: public; Owner: neondb_owner
--

ALTER TABLE ONLY public.blog_posts ALTER COLUMN id SET DEFAULT nextval('public.blog_posts_id_seq'::regclass);


--
-- Name: blog_tags id; Type: DEFAULT; Schema: public; Owner: neondb_owner
--

ALTER TABLE ONLY public.blog_tags ALTER COLUMN id SET DEFAULT nextval('public.blog_tags_id_seq'::regclass);


--
-- Name: callback_requests id; Type: DEFAULT; Schema: public; Owner: neondb_owner
--

ALTER TABLE ONLY public.callback_requests ALTER COLUMN id SET DEFAULT nextval('public.callback_requests_id_seq'::regclass);


--
-- Name: cashback_applications id; Type: DEFAULT; Schema: public; Owner: neondb_owner
--

ALTER TABLE ONLY public.cashback_applications ALTER COLUMN id SET DEFAULT nextval('public.cashback_applications_id_seq'::regclass);


--
-- Name: cashback_payouts id; Type: DEFAULT; Schema: public; Owner: neondb_owner
--

ALTER TABLE ONLY public.cashback_payouts ALTER COLUMN id SET DEFAULT nextval('public.cashback_payouts_id_seq'::regclass);


--
-- Name: cashback_records id; Type: DEFAULT; Schema: public; Owner: neondb_owner
--

ALTER TABLE ONLY public.cashback_records ALTER COLUMN id SET DEFAULT nextval('public.cashback_records_id_seq'::regclass);


--
-- Name: cities id; Type: DEFAULT; Schema: public; Owner: neondb_owner
--

ALTER TABLE ONLY public.cities ALTER COLUMN id SET DEFAULT nextval('public.cities_id_seq'::regclass);


--
-- Name: client_property_recommendations id; Type: DEFAULT; Schema: public; Owner: neondb_owner
--

ALTER TABLE ONLY public.client_property_recommendations ALTER COLUMN id SET DEFAULT nextval('public.client_property_recommendations_id_seq'::regclass);


--
-- Name: collection_properties id; Type: DEFAULT; Schema: public; Owner: neondb_owner
--

ALTER TABLE ONLY public.collection_properties ALTER COLUMN id SET DEFAULT nextval('public.collection_properties_id_seq'::regclass);


--
-- Name: collections id; Type: DEFAULT; Schema: public; Owner: neondb_owner
--

ALTER TABLE ONLY public.collections ALTER COLUMN id SET DEFAULT nextval('public.collections_id_seq'::regclass);


--
-- Name: developer_appointments id; Type: DEFAULT; Schema: public; Owner: neondb_owner
--

ALTER TABLE ONLY public.developer_appointments ALTER COLUMN id SET DEFAULT nextval('public.developer_appointments_id_seq'::regclass);


--
-- Name: developers id; Type: DEFAULT; Schema: public; Owner: neondb_owner
--

ALTER TABLE ONLY public.developers ALTER COLUMN id SET DEFAULT nextval('public.developers_id_seq'::regclass);


--
-- Name: districts id; Type: DEFAULT; Schema: public; Owner: neondb_owner
--

ALTER TABLE ONLY public.districts ALTER COLUMN id SET DEFAULT nextval('public.districts_id_seq'::regclass);


--
-- Name: documents id; Type: DEFAULT; Schema: public; Owner: neondb_owner
--

ALTER TABLE ONLY public.documents ALTER COLUMN id SET DEFAULT nextval('public.documents_id_seq'::regclass);


--
-- Name: favorite_properties id; Type: DEFAULT; Schema: public; Owner: neondb_owner
--

ALTER TABLE ONLY public.favorite_properties ALTER COLUMN id SET DEFAULT nextval('public.favorite_properties_id_seq'::regclass);


--
-- Name: favorites id; Type: DEFAULT; Schema: public; Owner: neondb_owner
--

ALTER TABLE ONLY public.favorites ALTER COLUMN id SET DEFAULT nextval('public.favorites_id_seq'::regclass);


--
-- Name: manager_saved_searches id; Type: DEFAULT; Schema: public; Owner: neondb_owner
--

ALTER TABLE ONLY public.manager_saved_searches ALTER COLUMN id SET DEFAULT nextval('public.manager_saved_searches_id_seq'::regclass);


--
-- Name: managers id; Type: DEFAULT; Schema: public; Owner: neondb_owner
--

ALTER TABLE ONLY public.managers ALTER COLUMN id SET DEFAULT nextval('public.managers_id_seq'::regclass);


--
-- Name: notifications id; Type: DEFAULT; Schema: public; Owner: neondb_owner
--

ALTER TABLE ONLY public.notifications ALTER COLUMN id SET DEFAULT nextval('public.notifications_id_seq'::regclass);


--
-- Name: recommendation_categories id; Type: DEFAULT; Schema: public; Owner: neondb_owner
--

ALTER TABLE ONLY public.recommendation_categories ALTER COLUMN id SET DEFAULT nextval('public.recommendation_categories_id_seq'::regclass);


--
-- Name: recommendation_templates id; Type: DEFAULT; Schema: public; Owner: neondb_owner
--

ALTER TABLE ONLY public.recommendation_templates ALTER COLUMN id SET DEFAULT nextval('public.recommendation_templates_id_seq'::regclass);


--
-- Name: recommendations id; Type: DEFAULT; Schema: public; Owner: neondb_owner
--

ALTER TABLE ONLY public.recommendations ALTER COLUMN id SET DEFAULT nextval('public.recommendations_id_seq'::regclass);


--
-- Name: residential_complexes id; Type: DEFAULT; Schema: public; Owner: neondb_owner
--

ALTER TABLE ONLY public.residential_complexes ALTER COLUMN id SET DEFAULT nextval('public.residential_complexes_id_seq'::regclass);


--
-- Name: room_types id; Type: DEFAULT; Schema: public; Owner: neondb_owner
--

ALTER TABLE ONLY public.room_types ALTER COLUMN id SET DEFAULT nextval('public.room_types_id_seq'::regclass);


--
-- Name: saved_searches id; Type: DEFAULT; Schema: public; Owner: neondb_owner
--

ALTER TABLE ONLY public.saved_searches ALTER COLUMN id SET DEFAULT nextval('public.saved_searches_id_seq'::regclass);


--
-- Name: search_categories id; Type: DEFAULT; Schema: public; Owner: neondb_owner
--

ALTER TABLE ONLY public.search_categories ALTER COLUMN id SET DEFAULT nextval('public.search_categories_id_seq'::regclass);


--
-- Name: sent_searches id; Type: DEFAULT; Schema: public; Owner: neondb_owner
--

ALTER TABLE ONLY public.sent_searches ALTER COLUMN id SET DEFAULT nextval('public.sent_searches_id_seq'::regclass);


--
-- Name: streets id; Type: DEFAULT; Schema: public; Owner: neondb_owner
--

ALTER TABLE ONLY public.streets ALTER COLUMN id SET DEFAULT nextval('public.streets_id_seq'::regclass);


--
-- Name: user_notifications id; Type: DEFAULT; Schema: public; Owner: neondb_owner
--

ALTER TABLE ONLY public.user_notifications ALTER COLUMN id SET DEFAULT nextval('public.user_notifications_id_seq'::regclass);


--
-- Name: users id; Type: DEFAULT; Schema: public; Owner: neondb_owner
--

ALTER TABLE ONLY public.users ALTER COLUMN id SET DEFAULT nextval('public.users_id_seq'::regclass);


--
-- Data for Name: admins; Type: TABLE DATA; Schema: public; Owner: neondb_owner
--

COPY public.admins (id, email, password_hash, full_name, admin_id, role, permissions, is_active, is_super_admin, profile_image, phone, created_at, updated_at, last_login) FROM stdin;
1	admin@inback.ru	scrypt:32768:8:1$JVCqHauCtXuI7no4$1ce6e42a1cbda23c0dda818f5df6247c3208931ffa0221ee645f5084daa99a591db021681cdb348c5d07386c3f9f77bbe6f97471efe5996c87fc60b6b12b2d0d	Главный Администратор	ADM89406111	super_admin	{"all": true}	t	f	https://randomuser.me/api/portraits/men/1.jpg	\N	2025-08-12 19:11:43.594249	2025-08-13 00:34:01.261443	2025-08-13 00:34:01.259939
\.


--
-- Data for Name: applications; Type: TABLE DATA; Schema: public; Owner: neondb_owner
--

COPY public.applications (id, user_id, property_id, property_name, complex_name, status, message, preferred_contact, created_at, updated_at, contact_name, contact_email, contact_phone) FROM stdin;
1	14	\N	Подбор квартиры	По предпочтениям	new	Заявка на подбор квартиры:\nРайон: Центральный\nТип: Квартира\nКомнат: 2\nБюджет: 4-6 млн	email	2025-08-11 21:58:55.280646	2025-08-11 21:58:55.280649	\N	\N	\N
2	\N	\N	Подбор квартиры	По предпочтениям	new	Заявка на подбор квартиры:\nИмя: Петр Смирнов\nEmail: petr.smirnov@example.com\nТелефон: +7 (918) 777-88-99\nРайон: Прикубанский\nТип: Квартира\nКомнат: 3\nБюджет: 5-7 млн	email	2025-08-12 18:36:27.349754	2025-08-12 18:36:27.349757	Петр Смирнов	petr.smirnov@example.com	+7 (918) 777-88-99
3	\N	\N	Подбор квартиры	По предпочтениям	new	Заявка на подбор квартиры:\nИмя: Иван\nEmail: bithome@mail.ru\nТелефон: 8 (912) 391-23-33\nРайон: Центральный\nТип: Таунхаус\nКомнат: 2\nБюджет: 5-8 млн	email	2025-08-12 18:40:52.249665	2025-08-12 18:40:52.249669	Иван	bithome@mail.ru	8 (912) 391-23-33
4	\N	\N	Подбор квартиры	По предпочтениям	new	Заявка на подбор квартиры:\nИмя: Тестовый Пользователь\nEmail: test.user@example.com\nТелефон: +7 (918) 555-99-88\nРайон: Центральный\nТип: Квартира\nКомнат: 2\nБюджет: 4-6 млн	email	2025-08-12 18:43:15.237826	2025-08-12 18:43:15.23783	Тестовый Пользователь	test.user@example.com	+7 (918) 555-99-88
\.


--
-- Data for Name: blog_article_tags; Type: TABLE DATA; Schema: public; Owner: neondb_owner
--

COPY public.blog_article_tags (article_id, tag_id) FROM stdin;
\.


--
-- Data for Name: blog_articles; Type: TABLE DATA; Schema: public; Owner: neondb_owner
--

COPY public.blog_articles (id, title, slug, excerpt, content, author_id, author_name, category_id, status, published_at, scheduled_at, meta_title, meta_description, meta_keywords, featured_image, featured_image_alt, is_featured, allow_comments, views_count, reading_time, created_at, updated_at, category) FROM stdin;
1	Тестовая	тестовая	<p>тестовая</p>	<h1>Тестовая<br><br></h1>\r\n<p>тестовая<br><em>тествоая</em></p>	1	\N	7	published	2025-08-12 19:25:50.600504	\N	тестовая	тестовая	тестовая		\N	f	t	0	1	2025-08-12 19:25:50.6023	2025-08-12 19:25:50.602302	\N
2	район	район	<p>район</p>	<h1>Район<br><br><br><br><br></h1>\r\n<p>район</p>	1	\N	2	published	2025-08-12 19:37:36.556582	\N	район 	район 	район		\N	t	t	0	1	2025-08-12 19:37:36.558346	2025-08-12 19:37:36.558347	\N
5	Тестовая статья 123	test-123	Краткое описание	Содержание тестовой статьи 123	1	\N	1	published	\N	\N	\N	\N	\N	/static/uploads/components-charts-intro2x_1755036639.png	\N	\N	\N	9	\N	2025-08-12 22:53:43.138568	2025-08-12 22:55:07.012039	Тест
\.


--
-- Data for Name: blog_categories; Type: TABLE DATA; Schema: public; Owner: neondb_owner
--

COPY public.blog_categories (id, name, slug, description, color, icon, meta_title, meta_description, sort_order, is_active, articles_count, views_count, created_at, updated_at) FROM stdin;
5	Советы покупателям	tips	Полезные советы при покупке новостроек	orange	fas fa-lightbulb	\N	\N	5	t	1	0	2025-08-11 19:25:42.735161	2025-08-11 19:25:42.735161
8	Новая категория	новая-категория	Описание новой категории	blue	\N	\N	\N	0	t	0	0	2025-08-12 19:21:24.642429	2025-08-12 19:21:24.642433
9	Тестович	тестович	фыв	blue	fas fa-folder	\N	\N	0	t	0	0	2025-08-12 19:24:18.603589	2025-08-12 19:24:18.603595
3	Ипотека	mortgage	Всё об ипотечном кредитовании	purple	fas fa-home	\N	\N	3	t	1	0	2025-08-11 19:25:42.735161	2025-08-12 19:42:35.801967
4	ЖК и застройщики	developers	Обзоры жилых комплексов	red	fas fa-building	\N	\N	4	t	0	0	2025-08-11 19:25:42.735161	2025-08-12 19:42:36.002124
6	Инвестиции	investments	Статьи об инвестициях в недвижимость	yellow	fas fa-chart-line	\N	\N	6	t	1	0	2025-08-11 19:25:42.735161	2025-08-12 19:42:36.306085
10	Аналитика	аналитика	Статьи по теме Аналитика	blue	\N	\N	\N	0	t	1	0	2025-08-12 19:34:28.463696	2025-08-12 19:42:36.807321
11	Кешбек	кешбек	Статьи по теме Кешбек	blue	\N	\N	\N	0	t	1	0	2025-08-12 19:34:28.463703	2025-08-12 20:04:57.675998
12	Тестовая категория	тестовая-категория	Описание тестовой категории	blue	\N	\N	\N	0	t	0	0	2025-08-12 21:57:49.985087	2025-08-12 21:57:49.985091
13	123333	123333	123333	blue	\N	\N	\N	0	t	1	0	2025-08-12 22:37:35.030717	2025-08-12 23:16:45.945831
1	Новости рынка	market-news	Актуальные новости рынка недвижимости	blue	fas fa-newspaper	\N	\N	1	t	1	0	2025-08-11 19:25:42.735161	2025-08-12 19:42:35.601745
2	Районы Краснодара	districts	Обзоры районов города	green	fas fa-map-marker-alt	\N	\N	2	t	1	0	2025-08-11 19:25:42.735161	2025-08-12 19:42:37.206307
7	Тест	test	Тестовая категория	gray	fas fa-folder	\N	\N	7	t	1	0	2025-08-11 19:25:42.735161	2025-08-12 22:51:44.539529
\.


--
-- Data for Name: blog_comments; Type: TABLE DATA; Schema: public; Owner: neondb_owner
--

COPY public.blog_comments (id, article_id, author_name, author_email, author_website, user_id, content, status, ip_address, user_agent, parent_id, created_at, updated_at) FROM stdin;
\.


--
-- Data for Name: blog_posts; Type: TABLE DATA; Schema: public; Owner: neondb_owner
--

COPY public.blog_posts (id, title, slug, content, excerpt, meta_title, meta_description, meta_keywords, status, featured_image, category, tags, author_id, published_at, scheduled_for, views_count, likes_count, created_at, updated_at) FROM stdin;
4	Ипотечные программы 2024: льготы и условия	ipotechnye-programmy-2024-lgoty-i-usloviya	Обзор актуальных ипотечных программ 2024 года.\n\nСемейная ипотека:\n- Ставка от 5.5% годовых\n- Для семей с детьми\n- Первоначальный взнос от 20%\n\nIT-ипотека:\n- Ставка от 5.0% годовых  \n- Для IT-специалистов\n- Первоначальный взнос от 15%\n\nВоенная ипотека:\n- Льготные условия для военнослужащих\n- Государственная поддержка\n- Особые требования к объектам\n\nМатеринский капитал:\n- Можно использовать как первоначальный взнос\n- Дополнительные льготы\n- Упрощенная процедура оформления	Подробный обзор ипотечных программ и льгот, доступных в 2024 году	Ипотечные программы 2024: льготы и условия	Подробный обзор ипотечных программ и льгот, доступных в 2024 году	\N	published	/attached_assets/Screenshot_101_1754873881260.jpg	Ипотека	["ипотека", "льготы", "2024"]	1	2025-08-12 19:19:17.119603	\N	0	0	2025-08-12 19:19:17.119611	2025-08-12 19:19:52.371541
5	Инвестиции в недвижимость Краснодара: аналитика рынка	investitsii-v-nedvizhimost-krasnodara-analitika-rynka	Краснодар остается одним из наиболее привлекательных городов для инвестиций в недвижимость.\n\nКлючевые факторы роста:\n- Активное развитие инфраструктуры\n- Приток населения из других регионов\n- Развитие IT-сектора\n- Близость к морю и туристическим зонам\n\nПерспективные районы:\n1. Центральный - стабильный рост стоимости\n2. Карасунский - новые жилые комплексы\n3. Прикубанский - развитая инфраструктура\n\nРекомендации инвесторам:\n- Выбирайте объекты в перспективных локациях\n- Учитывайте транспортную доступность\n- Обращайте внимание на качество застройщика\n- Рассматривайте возможности сдачи в аренду	Анализ инвестиционной привлекательности недвижимости Краснодара	Инвестиции в недвижимость Краснодара: аналитика рынка	Анализ инвестиционной привлекательности недвижимости Краснодара	\N	published	/attached_assets/Screenshot_102_1754876855770.jpg	Инвестиции	["инвестиции", "Краснодар", "аналитика"]	1	2025-08-12 19:19:17.32618	\N	0	0	2025-08-12 19:19:17.326187	2025-08-12 19:19:52.371542
3	Как выбрать квартиру в новостройке: полное руководство	kak-vybrat-kvartiru-v-novostroyke-polnoe-rukovodstvo	При выборе квартиры в новостройке важно учитывать множество факторов. \n            \nОсновные критерии:\n1. Репутация застройщика - изучите его предыдущие проекты\n2. Документы на строительство - все должно быть в порядке\n3. Расположение - транспортная доступность и инфраструктура\n4. Планировка и качество отделки\n5. Сроки сдачи и возможные риски\n\nФинансовые аспекты:\n- Сравните цены с аналогичными объектами\n- Узнайте о возможностях рассрочки и ипотеки\n- Рассчитайте дополнительные расходы\n\nПравовые моменты:\n- Проверьте все документы на землю и строительство\n- Изучите договор долевого участия\n- Узнайте о страховании	Подробное руководство по выбору квартиры в новостройке с учетом всех важных факторов	Как выбрать квартиру в новостройке: полное руководство	Подробное руководство по выбору квартиры в новостройке с учетом всех важных факторов	\N	published	/attached_assets/Screenshot_100_1754873602744.jpg	Советы покупателям	["новостройка", "покупка", "советы"]	1	2025-08-12 19:19:16.904686	\N	1	0	2025-08-12 19:19:16.904696	2025-08-12 22:52:47.660453
6	Кешбек при покупке недвижимости: как получить максимум	keshbek-pri-pokupke-nedvizhimosti-kak-poluchit-maksimum	Кешбек при покупке недвижимости - отличная возможность сэкономить.\n\nВиды кешбека:\n- От застройщика (обычно 1-3% от стоимости)\n- От банка при оформлении ипотеки\n- От агентства недвижимости\n- Специальные акции и программы лояльности\n\nКак увеличить кешбек:\n1. Участвуйте в акциях застройщика\n2. Выбирайте правильное время покупки\n3. Используйте партнерские программы\n4. Оформляйте ипотеку в банках-партнерах\n\nУсловия получения:\n- Соблюдение сроков сделки\n- Предоставление всех документов\n- Выполнение условий программы\n\nНалоговые аспекты:\n- Кешбек может облагаться налогом\n- Ведите учет всех выплат\n- Консультируйтесь с налоговыми консультантами	Как максимально использовать программы кешбека при покупке недвижимости	Кешбек при покупке недвижимости: как получить максимум	Как максимально использовать программы кешбека при покупке недвижимости	\N	published	/attached_assets/Screenshot_104_1754918829200.jpg	Кешбек	["кешбек", "экономия", "покупка"]	1	2025-08-12 19:19:17.531338	\N	0	0	2025-08-12 19:19:17.531344	2025-08-12 19:19:52.371542
10	Лучшие районы Краснодара для инвестиций	лучшие-районы-краснодара-для-инвестиций	Подробный анализ районов города с точки зрения инвестиций в недвижимость	Анализ перспективных районов Краснодара для покупки недвижимости	\N	\N	\N	published		Районы Краснодара	районы, инвестиции, краснодар	1	2025-08-12 19:40:29.836905	\N	0	0	2025-08-12 19:40:29.838672	2025-08-12 19:40:29.838674
11	Статья без изображения	статья-без-изображения	<p>Содержание статьи без изображения</p>	<p>Краткое описание</p>	Статья без изображения	Краткое описание	\N	draft	/uploads/Screenshot_62_1755029158.png	Тест		1	2025-08-12 19:47:11.118292	\N	0	0	2025-08-12 19:47:11.120373	2025-08-12 20:06:01.88409
12	Тестовая статья	testovaya-statya	Содержание тестовой статьи	Краткое описание статьи	\N	\N	\N	draft	\N	Новости	\N	1	\N	\N	0	0	2025-08-12 21:58:01.764612	2025-08-12 21:58:01.764615
8	Тестовая статья в категории Тест	testovaya-statya-v-kategorii-test	Это тестовая статья для проверки отображения категорий в блоге.	Тестовая статья для проверки категорий	\N	\N	\N	published	\N	Тест	тест, категория	1	2025-08-12 19:29:17.877043	\N	2	0	2025-08-12 19:29:17.982118	2025-08-12 19:46:33.74723
13	123	123	<p>123<img src="../../uploads/components-charts-intro2x_1755036639.png" alt="Изображение" style="max-width: 100%; height: auto;"></p>	123	123	123	123	published	https://images.unsplash.com/photo-1560472354-b33ff0c44a43?w=400&h=250&fit=crop	Тест	Недвижимость и точка	1	2025-08-12 22:13:18.340498	\N	24	0	2025-08-12 22:11:04.043595	2025-08-12 22:53:40.815791
9	Обзор районов Краснодара: где лучше купить квартиру	obzor-rajonov-krasnodara	<p>Краснодар - динамично развивающийся город с множеством привлекательных районов для покупки недвижимости. В этом обзоре мы рассмотрим основные районы города и их особенности.</p><h3>Центральный район</h3><p>Сердце города с развитой инфраструктурой и высокими ценами на недвижимость.</p><h3>Прикубанский район</h3><p>Один из самых престижных районов с парками и современными ЖК.</p>	Подробный обзор лучших районов Краснодара для покупки недвижимости с анализом инфраструктуры и цен.	\N	\N	\N	published	\N	Районы Краснодара	районы, краснодар, недвижимость, инфраструктура	1	2025-08-12 19:39:31.807738	\N	1	0	2025-08-12 19:39:31.81034	2025-08-12 22:22:12.494365
14	123	123-1	<p>123</p>	123	123	123	123	published		Тест		1	2025-08-12 22:51:43.804984	\N	0	0	2025-08-12 22:51:43.804887	2025-08-12 22:51:43.806595
7	Тенденции рынка недвижимости в 2024 году	tendentsii-rynka-nedvizhimosti-v-2024-godu	Рынок недвижимости в 2024 году показывает интересные тенденции.\n\nОсновные тренды:\n- Рост спроса на комфорт-класс\n- Увеличение популярности готового жилья\n- Развитие пригородной недвижимости\n- Внедрение smart-технологий в ЖК\n\nРегиональные особенности:\n- Краснодар: стабильный рост цен\n- Сочи: высокий инвестиционный потенциал\n- Анапа: развитие курортной недвижимости\n\nПрогнозы на год:\n- Умеренный рост цен (5-10%)\n- Развитие ипотечного кредитования\n- Увеличение объемов строительства\n- Новые технологии в отрасли\n\nРекомендации покупателям:\n- Не откладывайте покупку надолго\n- Изучайте новые проекты\n- Следите за изменениями в законодательстве	Обзор ключевых тенденций и прогнозов развития рынка недвижимости	Тенденции рынка недвижимости в 2024 году	Обзор ключевых тенденций и прогнозов развития рынка недвижимости	\N	published	/attached_assets/Screenshot_105_1754923069170.jpg	Аналитика	["тенденции", "прогноз", "рынок"]	1	2025-08-12 19:19:17.734633	\N	1	0	2025-08-12 19:19:17.734641	2025-08-12 19:19:52.371545
15	фффф	ffff	<p>ффф</p>	ффф	ффф	ффф	фф	published		123333		1	2025-08-12 23:16:45.210947	\N	1	0	2025-08-12 23:16:45.210863	2025-08-12 23:16:45.212505
\.


--
-- Data for Name: blog_tags; Type: TABLE DATA; Schema: public; Owner: neondb_owner
--

COPY public.blog_tags (id, name, slug, description, usage_count, created_at) FROM stdin;
\.


--
-- Data for Name: callback_requests; Type: TABLE DATA; Schema: public; Owner: neondb_owner
--

COPY public.callback_requests (id, name, phone, email, preferred_time, notes, interest, budget, timing, status, assigned_manager_id, manager_notes, created_at, processed_at) FROM stdin;
1	Тестовый Клиент	+7 (900) 123-45-67	test@example.com	Сейчас	Тестовая заявка на звонок	Квартира в новостройке	3-5 млн руб	В ближайшие месяцы	Новая	2	\N	2025-08-11 21:55:57.379475	\N
2	Тест Клиент	+7 (900) 123-45-67	test.client@example.com	Утром (9:00-12:00)	Интересует 2-комнатная квартира в центре	Квартира в новостройке	4-6 млн руб	В ближайшие месяцы	Новая	2	\N	2025-08-11 21:59:04.99879	\N
\.


--
-- Data for Name: cashback_applications; Type: TABLE DATA; Schema: public; Owner: neondb_owner
--

COPY public.cashback_applications (id, user_id, property_id, property_name, property_type, property_size, property_price, complex_name, developer_name, cashback_amount, cashback_percent, status, application_date, approved_date, payout_date, notes, approved_by_manager_id, manager_notes, created_at, updated_at) FROM stdin;
\.


--
-- Data for Name: cashback_payouts; Type: TABLE DATA; Schema: public; Owner: neondb_owner
--

COPY public.cashback_payouts (id, user_id, amount, status, payment_method, admin_notes, requested_at, processed_at) FROM stdin;
\.


--
-- Data for Name: cashback_records; Type: TABLE DATA; Schema: public; Owner: neondb_owner
--

COPY public.cashback_records (id, user_id, property_id, property_name, property_price, amount, percentage, status, created_at, approved_at, paid_at) FROM stdin;
\.


--
-- Data for Name: cities; Type: TABLE DATA; Schema: public; Owner: neondb_owner
--

COPY public.cities (id, name, slug, is_active, is_default, phone, email, address, latitude, longitude, zoom_level, description, meta_title, meta_description, created_at, updated_at) FROM stdin;
\.


--
-- Data for Name: client_property_recommendations; Type: TABLE DATA; Schema: public; Owner: neondb_owner
--

COPY public.client_property_recommendations (id, manager_id, client_id, search_id, message, sent_at, viewed_at) FROM stdin;
\.


--
-- Data for Name: collection_properties; Type: TABLE DATA; Schema: public; Owner: neondb_owner
--

COPY public.collection_properties (id, collection_id, property_id, property_name, property_price, complex_name, property_type, property_size, manager_note, order_index, created_at, added_at) FROM stdin;
1	1	coll_1_0	2-комн квартира	11602832	ЖК Солнечный	2	70	Отличный вариант для лучшие предложения для молодой семьи. Рекомендую к рассмотрению.	\N	2025-08-10 21:32:12	2025-08-11 19:34:22.168825
2	1	coll_1_1	3-комн квартира	11280681	ЖК Центральный	3	133	Отличный вариант для лучшие предложения для молодой семьи. Рекомендую к рассмотрению.	\N	2025-08-10 21:32:12	2025-08-11 19:34:22.168825
3	1	coll_1_2	1-комн квартира	6708374	ЖК Солнечный	1	143	Отличный вариант для лучшие предложения для молодой семьи. Рекомендую к рассмотрению.	\N	2025-08-10 21:32:12	2025-08-11 19:34:22.168825
4	1	coll_1_3	4-комн квартира	10225712	ЖК Центральный	4	85	Отличный вариант для лучшие предложения для молодой семьи. Рекомендую к рассмотрению.	\N	2025-08-10 21:32:12	2025-08-11 19:34:22.168825
5	1	coll_1_4	4-комн квартира	6133606	ЖК Солнечный	4	122	Отличный вариант для лучшие предложения для молодой семьи. Рекомендую к рассмотрению.	\N	2025-08-10 21:32:12	2025-08-11 19:34:22.168825
6	1	coll_1_5	1-комн квартира	9985210	ЖК Солнечный	1	68	Отличный вариант для лучшие предложения для молодой семьи. Рекомендую к рассмотрению.	\N	2025-08-10 21:32:12	2025-08-11 19:34:22.168825
7	2	coll_2_0	3-комн квартира	4192814	ЖК Центральный	3	75	Отличный вариант для инвестиционный портфель: стабильный доход. Рекомендую к рассмотрению.	\N	2025-08-10 21:32:12	2025-08-11 19:34:22.168825
8	2	coll_2_1	4-комн квартира	10273272	ЖК Центральный	4	122	Отличный вариант для инвестиционный портфель: стабильный доход. Рекомендую к рассмотрению.	\N	2025-08-10 21:32:12	2025-08-11 19:34:22.168825
9	2	coll_2_2	2-комн квартира	7343963	ЖК Центральный	2	144	Отличный вариант для инвестиционный портфель: стабильный доход. Рекомендую к рассмотрению.	\N	2025-08-10 21:32:12	2025-08-11 19:34:22.168825
10	2	coll_2_3	2-комн квартира	5701393	ЖК Премьер	2	91	Отличный вариант для инвестиционный портфель: стабильный доход. Рекомендую к рассмотрению.	\N	2025-08-10 21:32:12	2025-08-11 19:34:22.168825
11	2	coll_2_4	1-комн квартира	7434352	ЖК Премьер	1	136	Отличный вариант для инвестиционный портфель: стабильный доход. Рекомендую к рассмотрению.	\N	2025-08-10 21:32:12	2025-08-11 19:34:22.168825
12	2	coll_2_5	3-комн квартира	17953304	ЖК Премьер	3	105	Отличный вариант для инвестиционный портфель: стабильный доход. Рекомендую к рассмотрению.	\N	2025-08-10 21:32:12	2025-08-11 19:34:22.168825
13	2	coll_2_6	1-комн квартира	4591414	ЖК Центральный	1	43	Отличный вариант для инвестиционный портфель: стабильный доход. Рекомендую к рассмотрению.	\N	2025-08-10 21:32:12	2025-08-11 19:34:22.168825
14	2	coll_2_7	1-комн квартира	9716633	ЖК Премьер	1	148	Отличный вариант для инвестиционный портфель: стабильный доход. Рекомендую к рассмотрению.	\N	2025-08-10 21:32:12	2025-08-11 19:34:22.168825
15	3	coll_3_0	2-комн квартира	7010179	ЖК Солнечный	2	79	Отличный вариант для первое жилье: доступные варианты. Рекомендую к рассмотрению.	\N	2025-08-10 21:32:12	2025-08-11 19:34:22.168825
16	3	coll_3_1	1-комн квартира	4594590	ЖК Центральный	1	61	Отличный вариант для первое жилье: доступные варианты. Рекомендую к рассмотрению.	\N	2025-08-10 21:32:12	2025-08-11 19:34:22.168825
17	3	coll_3_2	3-комн квартира	8953925	ЖК Премьер	3	57	Отличный вариант для первое жилье: доступные варианты. Рекомендую к рассмотрению.	\N	2025-08-10 21:32:12	2025-08-11 19:34:22.168825
18	4	coll_4_0	4-комн квартира	13116774	ЖК Центральный	4	40	Отличный вариант для премиум класс: эксклюзивные предложения. Рекомендую к рассмотрению.	\N	2025-08-10 21:32:13	2025-08-11 19:34:22.168825
19	4	coll_4_1	3-комн квартира	13062480	ЖК Центральный	3	75	Отличный вариант для премиум класс: эксклюзивные предложения. Рекомендую к рассмотрению.	\N	2025-08-10 21:32:13	2025-08-11 19:34:22.168825
20	4	coll_4_2	3-комн квартира	17348821	ЖК Центральный	3	81	Отличный вариант для премиум класс: эксклюзивные предложения. Рекомендую к рассмотрению.	\N	2025-08-10 21:32:13	2025-08-11 19:34:22.168825
21	4	coll_4_3	4-комн квартира	15573976	ЖК Солнечный	4	121	Отличный вариант для премиум класс: эксклюзивные предложения. Рекомендую к рассмотрению.	\N	2025-08-10 21:32:13	2025-08-11 19:34:22.168825
22	4	coll_4_4	2-комн квартира	14573178	ЖК Центральный	2	56	Отличный вариант для премиум класс: эксклюзивные предложения. Рекомендую к рассмотрению.	\N	2025-08-10 21:32:13	2025-08-11 19:34:22.168825
23	4	coll_4_5	2-комн квартира	6710869	ЖК Солнечный	2	90	Отличный вариант для премиум класс: эксклюзивные предложения. Рекомендую к рассмотрению.	\N	2025-08-10 21:32:13	2025-08-11 19:34:22.168825
24	4	coll_4_6	3-комн квартира	5802683	ЖК Солнечный	3	110	Отличный вариант для премиум класс: эксклюзивные предложения. Рекомендую к рассмотрению.	\N	2025-08-10 21:32:13	2025-08-11 19:34:22.168825
25	4	coll_4_7	3-комн квартира	12981631	ЖК Премьер	3	84	Отличный вариант для премиум класс: эксклюзивные предложения. Рекомендую к рассмотрению.	\N	2025-08-10 21:32:13	2025-08-11 19:34:22.168825
26	5	coll_5_0	4-комн квартира	15838576	ЖК Центральный	4	110	Отличный вариант для студии и 1-комнатные: компактный комфорт. Рекомендую к рассмотрению.	\N	2025-08-10 21:32:13	2025-08-11 19:34:22.168825
27	5	coll_5_1	3-комн квартира	17469722	ЖК Солнечный	3	134	Отличный вариант для студии и 1-комнатные: компактный комфорт. Рекомендую к рассмотрению.	\N	2025-08-10 21:32:13	2025-08-11 19:34:22.168825
28	5	coll_5_2	2-комн квартира	5339128	ЖК Премьер	2	94	Отличный вариант для студии и 1-комнатные: компактный комфорт. Рекомендую к рассмотрению.	\N	2025-08-10 21:32:13	2025-08-11 19:34:22.168825
29	5	coll_5_3	2-комн квартира	17023966	ЖК Премьер	2	45	Отличный вариант для студии и 1-комнатные: компактный комфорт. Рекомендую к рассмотрению.	\N	2025-08-10 21:32:13	2025-08-11 19:34:22.168825
30	5	coll_5_4	1-комн квартира	10122351	ЖК Премьер	1	102	Отличный вариант для студии и 1-комнатные: компактный комфорт. Рекомендую к рассмотрению.	\N	2025-08-10 21:32:13	2025-08-11 19:34:22.168825
31	5	coll_5_5	4-комн квартира	8844352	ЖК Солнечный	4	46	Отличный вариант для студии и 1-комнатные: компактный комфорт. Рекомендую к рассмотрению.	\N	2025-08-10 21:32:13	2025-08-11 19:34:22.168825
\.


--
-- Data for Name: collections; Type: TABLE DATA; Schema: public; Owner: neondb_owner
--

COPY public.collections (id, title, description, created_by_manager_id, assigned_to_user_id, status, is_public, tags, created_at, updated_at, sent_at, viewed_at, name) FROM stdin;
1	Лучшие предложения для молодой семьи	Подборка 2-3 комнатных квартир в семейных районах с развитой инфраструктурой	1	2	Просмотрена	f	\N	2025-08-05 21:32:12	\N	\N	\N	\N
2	Инвестиционный портфель: стабильный доход	Квартиры с высоким потенциалом роста стоимости и возможностью сдачи в аренду	1	5	Отправлена	t	\N	2025-08-05 21:32:12	\N	\N	\N	\N
3	Первое жилье: доступные варианты	Бюджетные варианты для покупки первой квартиры с возможностью ипотеки	1	3	Просмотрена	t	\N	2025-08-05 21:32:12	\N	\N	\N	\N
4	Премиум класс: эксклюзивные предложения	Элитные квартиры в престижных районах с уникальными характеристиками	1	4	Отправлена	f	\N	2025-07-27 21:32:13	\N	\N	\N	\N
5	Студии и 1-комнатные: компактный комфорт	Небольшие, но функциональные квартиры для одного человека или пары	1	6	Черновик	t	\N	2025-07-12 21:32:13	\N	\N	\N	\N
\.


--
-- Data for Name: developer_appointments; Type: TABLE DATA; Schema: public; Owner: neondb_owner
--

COPY public.developer_appointments (id, user_id, property_id, developer_name, complex_name, appointment_date, appointment_time, status, client_name, client_phone, notes, created_at) FROM stdin;
\.


--
-- Data for Name: developers; Type: TABLE DATA; Schema: public; Owner: neondb_owner
--

COPY public.developers (id, name, slug) FROM stdin;
1	Стандартный застройщик	default-developer
\.


--
-- Data for Name: districts; Type: TABLE DATA; Schema: public; Owner: neondb_owner
--

COPY public.districts (id, name, slug, description, city_id, coordinates, is_active, latitude, longitude, created_at, updated_at) FROM stdin;
1	Карасунский	karasunskiy	\N	1	\N	t	\N	\N	2025-08-11 19:25:13.628254	2025-08-11 19:25:13.628254
2	Юбилейный	yubileynyy	\N	1	\N	t	\N	\N	2025-08-11 19:25:13.628254	2025-08-11 19:25:13.628254
3	Западный	zapadnyy	\N	1	\N	t	\N	\N	2025-08-11 19:25:13.628254	2025-08-11 19:25:13.628254
4	Центральный	tsentralnyy	\N	1	\N	t	\N	\N	2025-08-11 19:25:13.628254	2025-08-11 19:25:13.628254
5	Прикубанский округ	prikubanskiy-okrug	\N	1	\N	t	\N	\N	2025-08-11 19:25:13.628254	2025-08-11 19:25:13.628254
6	Фестивальный	festivalnyy	\N	1	\N	t	\N	\N	2025-08-11 19:25:13.628254	2025-08-11 19:25:13.628254
7	Комсомольский	komsomolskiy	\N	1	\N	t	\N	\N	2025-08-11 19:25:13.628254	2025-08-11 19:25:13.628254
8	Прикубанский	prikubanskiy	\N	1	\N	t	\N	\N	2025-08-11 19:25:13.628254	2025-08-11 19:25:13.628254
\.


--
-- Data for Name: documents; Type: TABLE DATA; Schema: public; Owner: neondb_owner
--

COPY public.documents (id, user_id, filename, original_filename, file_type, file_size, file_path, document_type, status, reviewed_at, reviewer_notes, reviewed_by_manager_id, created_at, updated_at) FROM stdin;
\.


--
-- Data for Name: favorite_properties; Type: TABLE DATA; Schema: public; Owner: neondb_owner
--

COPY public.favorite_properties (id, user_id, property_id, property_name, property_type, property_size, property_price, complex_name, developer_name, property_image, property_url, cashback_amount, cashback_percent, created_at) FROM stdin;
1	2	fav_2_0	1-комн квартира	3.0	35.2	2850000	ЖК Тестовый-1	ГК «Адмирал»	\N	\N	61655	\N	2025-08-10 21:30:56
2	2	fav_2_1	2-комн квартира	1.0	52.8	4200000	ЖК Тестовый-2	СК «Морская волна»	\N	\N	65402	\N	2025-08-10 21:30:56
3	2	fav_2_2	3-комн квартира	1.0	78.5	5890000	ЖК Тестовый-3	ГК «Солнечный дом»	\N	\N	94847	\N	2025-08-10 21:30:56
4	2	fav_2_3	0-комн квартира	2.0	28.3	2450000	ЖК Тестовый-4	ССК «Высота»	\N	\N	42374	\N	2025-08-10 21:30:57
5	2	fav_2_4	2-комн квартира	2.0	61.2	4750000	ЖК Тестовый-5	ГК «Парк Девелопмент»	\N	\N	113378	\N	2025-08-10 21:30:57
6	2	fav_2_5	4-комн квартира	1.0	98.7	8950000	ЖК Тестовый-6	ГК «Премиум строй»	\N	\N	147415	\N	2025-08-10 21:30:57
7	5	fav_5_0	1-комн квартира	3.0	35.2	2850000	ЖК Тестовый-1	ГК «Адмирал»	\N	\N	67972	\N	2025-08-10 21:30:57
8	5	fav_5_1	2-комн квартира	3.0	52.8	4200000	ЖК Тестовый-2	СК «Морская волна»	\N	\N	69760	\N	2025-08-10 21:30:57
9	5	fav_5_2	3-комн квартира	3.0	78.5	5890000	ЖК Тестовый-3	ГК «Солнечный дом»	\N	\N	99816	\N	2025-08-10 21:30:57
10	5	fav_5_3	0-комн квартира	2.0	28.3	2450000	ЖК Тестовый-4	ССК «Высота»	\N	\N	57524	\N	2025-08-10 21:30:57
11	5	fav_5_4	2-комн квартира	1.0	61.2	4750000	ЖК Тестовый-5	ГК «Парк Девелопмент»	\N	\N	89701	\N	2025-08-10 21:30:57
12	3	fav_3_0	1-комн квартира	3.0	35.2	2850000	ЖК Тестовый-1	ГК «Адмирал»	\N	\N	61807	\N	2025-08-10 21:30:57
13	3	fav_3_1	2-комн квартира	3.0	52.8	4200000	ЖК Тестовый-2	СК «Морская волна»	\N	\N	102707	\N	2025-08-10 21:30:57
14	3	fav_3_2	3-комн квартира	1.0	78.5	5890000	ЖК Тестовый-3	ГК «Солнечный дом»	\N	\N	90158	\N	2025-08-10 21:30:57
15	3	fav_3_3	0-комн квартира	1.0	28.3	2450000	ЖК Тестовый-4	ССК «Высота»	\N	\N	37072	\N	2025-08-10 21:30:57
16	3	fav_3_4	2-комн квартира	2.0	61.2	4750000	ЖК Тестовый-5	ГК «Парк Девелопмент»	\N	\N	109013	\N	2025-08-10 21:30:57
17	3	fav_3_5	4-комн квартира	1.0	98.7	8950000	ЖК Тестовый-6	ГК «Премиум строй»	\N	\N	215999	\N	2025-08-10 21:30:57
18	3	fav_3_6	1-комн квартира	1.0	42.1	3150000	ЖК Тестовый-7	СК «Современник»	\N	\N	78157	\N	2025-08-10 21:30:58
19	4	fav_4_0	1-комн квартира	2.0	35.2	2850000	ЖК Тестовый-1	ГК «Адмирал»	\N	\N	62912	\N	2025-08-10 21:30:58
20	4	fav_4_1	2-комн квартира	2.0	52.8	4200000	ЖК Тестовый-2	СК «Морская волна»	\N	\N	97821	\N	2025-08-10 21:30:58
21	4	fav_4_2	3-комн квартира	3.0	78.5	5890000	ЖК Тестовый-3	ГК «Солнечный дом»	\N	\N	94452	\N	2025-08-10 21:30:58
22	4	fav_4_3	0-комн квартира	2.0	28.3	2450000	ЖК Тестовый-4	ССК «Высота»	\N	\N	51737	\N	2025-08-10 21:30:58
23	2	fav_2_6	1-комн квартира	2.0	42.1	3150000	ЖК Тестовый-7	СК «Современник»	\N	\N	57502	\N	2025-08-10 21:31:48
24	5	fav_5_5	4-комн квартира	1.0	98.7	8950000	ЖК Тестовый-6	ГК «Премиум строй»	\N	\N	180185	\N	2025-08-10 21:31:49
25	4	fav_4_4	2-комн квартира	1.0	61.2	4750000	ЖК Тестовый-5	ГК «Парк Девелопмент»	\N	\N	112388	\N	2025-08-10 21:32:08
26	4	fav_4_5	4-комн квартира	2.0	98.7	8950000	ЖК Тестовый-6	ГК «Премиум строй»	\N	\N	163683	\N	2025-08-10 21:32:08
27	4	fav_4_6	1-комн квартира	2.0	42.1	3150000	ЖК Тестовый-7	СК «Современник»	\N	\N	68879	\N	2025-08-10 21:32:08
28	2	52	Квартира	2-комнатная	0	3130925			\N	\N	156546	\N	2025-08-10 22:44:26
\.


--
-- Data for Name: favorites; Type: TABLE DATA; Schema: public; Owner: neondb_owner
--

COPY public.favorites (id, user_id, property_id, created_at) FROM stdin;
\.


--
-- Data for Name: manager_saved_searches; Type: TABLE DATA; Schema: public; Owner: neondb_owner
--

COPY public.manager_saved_searches (id, manager_id, name, description, search_type, location, property_type, price_min, price_max, size_min, size_max, developer, complex_name, floor_min, floor_max, cashback_min, additional_filters, is_template, usage_count, created_at, updated_at, last_used) FROM stdin;
\.


--
-- Data for Name: managers; Type: TABLE DATA; Schema: public; Owner: neondb_owner
--

COPY public.managers (id, email, password_hash, first_name, last_name, phone, "position", can_approve_cashback, can_manage_documents, can_create_collections, max_cashback_approval, is_active, profile_image, manager_id, created_at, updated_at, last_login) FROM stdin;
2	manager2@inback.ru	scrypt:32768:8:1$IFd63Sugr9ETxqJh$5037b8cd882ea012f7a882fde228003b9f10e3b6d57c62f28d6d6c4342f43653e509bc07414205ed44e6c0804bd0c198c7b3154c0557551ebfef4bd1654acb78	Анна	Петрова	+7 (999) 234-56-78	Менеджер по продажам	\N	\N	\N	\N	t	\N	anna_mgr	2025-08-11 19:25:42.735161	2025-08-11 21:53:04.242931	\N
1	manager@inback.ru	scrypt:32768:8:1$g8ISprLJeH77Uuv5$b878fda08b06bfbc240dfcc3fc983ebfe44c289552374309239ac9d65ee1f792553631f824c41ca4fa7cfebc83cb336e807de9809a15023cb3c5725a8567d687	Станислав	Менеджер	+7 (999) 123-45-67	Старший менеджер	\N	\N	\N	\N	t	\N	stanislaw_mgr	2025-08-11 19:25:42.735161	2025-08-12 21:42:06.966967	2025-08-12 21:42:06.965408
\.


--
-- Data for Name: notifications; Type: TABLE DATA; Schema: public; Owner: neondb_owner
--

COPY public.notifications (id, user_id, title, message, type, icon, is_read, created_at) FROM stdin;
\.


--
-- Data for Name: recommendation_categories; Type: TABLE DATA; Schema: public; Owner: neondb_owner
--

COPY public.recommendation_categories (id, name, description, manager_id, client_id, color, is_active, recommendations_count, last_used, created_at, updated_at) FROM stdin;
\.


--
-- Data for Name: recommendation_templates; Type: TABLE DATA; Schema: public; Owner: neondb_owner
--

COPY public.recommendation_templates (id, manager_id, name, description, recommendation_type, default_title, default_description, default_notes, default_highlighted_features, default_priority, is_active, usage_count, created_at, updated_at, last_used) FROM stdin;
\.


--
-- Data for Name: recommendations; Type: TABLE DATA; Schema: public; Owner: neondb_owner
--

COPY public.recommendations (id, manager_id, client_id, category_id, title, description, recommendation_type, item_id, item_name, item_data, manager_notes, highlighted_features, priority_level, status, viewed_at, responded_at, client_response, client_notes, viewing_requested, viewing_scheduled_at, created_at, sent_at, expires_at, user_id, property_id, created_by_manager_id, recommendation_reason, updated_at) FROM stdin;
1	1	2	\N	Рекомендую: Объект 52	123	property	52	Объект 52	\N	\N	\N	\N	viewed	\N	\N	\N	\N	\N	\N	2025-08-10 21:34:16	2025-08-10 21:34:16	\N	\N	\N	\N	\N	2025-08-11 19:34:12.969348
2	1	2	\N	Отличная квартира в центре	Рекомендую эту квартиру для вашего бюджета. Отличное расположение и хорошая цена.	property	1	Квартира в ЖК Солнечный	\N	\N	\N	\N	viewed	\N	\N	\N	\N	\N	\N	2025-08-11 12:34:54	2025-08-11 12:34:54	\N	\N	\N	\N	\N	2025-08-11 19:34:12.969348
3	1	2	\N	Премиум ЖК с инфраструктурой	Этот жилой комплекс имеет развитую инфраструктуру и подходит для семьи с детьми.	complex	1	ЖК Премиум класса	\N	\N	\N	\N	viewed	\N	\N	\N	\N	\N	\N	2025-08-11 12:34:54	2025-08-11 12:34:54	\N	\N	\N	\N	\N	2025-08-11 19:34:12.969348
4	1	2	\N	Выгодное предложение	Квартира с хорошим кэшбеком в новом районе города.	property	10	Квартира с видом на парк	\N	\N	\N	\N	viewed	\N	\N	\N	\N	\N	\N	2025-08-11 12:34:54	2025-08-11 12:34:54	\N	\N	\N	\N	\N	2025-08-11 19:34:12.969348
6	1	14	\N	Рекомендую: Объект 52	123	property	52	Объект 52	\N	\N	\N	\N	sent	\N	\N	\N	\N	\N	\N	2025-08-11 15:59:40	2025-08-11 15:59:40	\N	\N	\N	\N	\N	2025-08-11 19:34:12.969348
7	1	14	\N	Рекомендую: Объект 76	123333	property	76	Объект 76	\N	\N	\N	\N	sent	\N	\N	\N	\N	\N	\N	2025-08-11 16:04:07	2025-08-11 16:04:07	\N	\N	\N	\N	\N	2025-08-11 19:34:12.969348
8	1	14	\N	Рекомендую: Объект 2	5674	property	2	Объект 2	\N	\N	\N	\N	sent	\N	\N	\N	\N	\N	\N	2025-08-11 16:09:36	2025-08-11 16:09:36	\N	\N	\N	\N	\N	2025-08-11 19:34:12.969348
9	1	14	\N	Рекомендую: Объект 162	тест	property	162	Объект 162	\N	\N	\N	\N	sent	\N	\N	\N	\N	\N	\N	2025-08-11 16:22:36	2025-08-11 16:22:36	\N	\N	\N	\N	\N	2025-08-11 19:34:12.969348
10	1	14	\N	Рекомендую: Объект 15	123	property	15	Объект 15	\N	\N	\N	\N	sent	\N	\N	\N	\N	\N	\N	2025-08-11 16:27:52	2025-08-11 16:27:52	\N	\N	\N	\N	\N	2025-08-11 19:34:12.969348
11	1	14	\N	Рекомендую: Объект 162	333	property	162	Объект 162	\N	\N	\N	\N	sent	\N	\N	\N	\N	\N	\N	2025-08-11 16:34:38	2025-08-11 16:34:38	\N	\N	\N	\N	\N	2025-08-11 19:34:12.969348
12	1	14	\N	Рекомендую: Объект 26	3333	property	26	Объект 26	\N	\N	\N	\N	sent	\N	\N	\N	\N	\N	\N	2025-08-11 16:36:55	2025-08-11 16:36:55	\N	\N	\N	\N	\N	2025-08-11 19:34:12.969348
13	1	14	\N	Рекомендую: Объект 26	ооо	property	26	Объект 26	\N	\N	\N	\N	sent	\N	\N	\N	\N	\N	\N	2025-08-11 16:39:14	2025-08-11 16:39:14	\N	\N	\N	\N	\N	2025-08-11 19:34:12.969348
15	1	14	\N	Рекомендую ЖК "ЖК «Аврора»"		complex	2	ЖК «Аврора»	\N	\N	\N	\N	sent	\N	\N	\N	\N	\N	\N	2025-08-11 16:56:10	2025-08-11 16:56:10	\N	\N	\N	\N	\N	2025-08-11 19:34:12.969348
16	1	14	\N	Рекомендую: Объект 52		property	52	Объект 52	\N	\N	\N	\N	sent	\N	\N	\N	\N	\N	\N	2025-08-11 17:01:30	2025-08-11 17:01:30	\N	\N	\N	\N	\N	2025-08-11 19:34:12.969348
5	1	2	\N	Рекомендую: Объект 52	тест	property	52	Объект 52	\N	\N	\N	\N	viewed	2025-08-11 19:41:54.401334	\N	\N	\N	\N	\N	2025-08-11 15:14:39	2025-08-11 15:14:39	\N	\N	\N	\N	\N	2025-08-11 19:34:12.969348
17	1	14	\N	Рекомендую ЖК "ЖК «Аврора»"	888	complex	2	ЖК «Аврора»	{}		\N	high	sent	\N	\N	\N	\N	f	\N	2025-08-12 18:56:01.881178	2025-08-12 18:56:01.881182	\N	\N	\N	\N	\N	2025-08-12 18:56:01.724958
18	1	14	\N	Рекомендую ЖК "ЖК «Белые паруса»"	99	complex	17	ЖК «Белые паруса»	{}		\N	medium	sent	\N	\N	\N	\N	f	\N	2025-08-12 18:56:28.444433	2025-08-12 18:56:28.444436	\N	\N	\N	\N	\N	2025-08-12 18:56:28.291204
19	1	2	\N	Рекомендую ЖК "ЖК «Весенний»"	88	complex	8	ЖК «Весенний»	{}		\N	medium	sent	\N	\N	\N	\N	f	\N	2025-08-12 18:56:58.712571	2025-08-12 18:56:58.712573	\N	\N	\N	\N	\N	2025-08-12 18:56:58.560259
20	1	2	\N	Рекомендую: Объект 52	111	property	52	Объект 52	{}		\N	normal	sent	\N	\N	\N	\N	f	\N	2025-08-12 19:04:38.121124	2025-08-12 19:04:38.121126	\N	\N	\N	\N	\N	2025-08-12 19:04:37.965105
21	1	20	\N	Рекомендую: Объект 52		property	52	Объект 52	{}		\N	normal	sent	\N	\N	\N	\N	f	\N	2025-08-12 19:04:53.7078	2025-08-12 19:04:53.707803	\N	\N	\N	\N	\N	2025-08-12 19:04:53.555968
22	1	14	\N	Рекомендую: Объект 52		property	52	Объект 52	{}		\N	normal	sent	\N	\N	\N	\N	f	\N	2025-08-12 19:05:12.865151	2025-08-12 19:05:12.865155	\N	\N	\N	\N	\N	2025-08-12 19:05:12.712805
\.


--
-- Data for Name: residential_complexes; Type: TABLE DATA; Schema: public; Owner: neondb_owner
--

COPY public.residential_complexes (id, name, slug, district_id, developer_id, description, short_description, street_id, address, property_class, building_type, total_buildings, total_floors, total_apartments, construction_status, construction_year, delivery_quarter, latitude, longitude, min_price, max_price, price_per_sqm, parking, playground, security, concierge, gym, kindergarten, metro_distance, school_distance, hospital_distance, gallery, main_image, video_url, mortgage_available, family_mortgage, it_mortgage, preferential_mortgage, meta_title, meta_description, is_active, is_featured, views, created_at, updated_at) FROM stdin;
1	ЖК «Первое место»	zhk-pervoe-mesto	5	1	ЖК «Первое место» — это современный жилой комплекс комфорт-класса в Краснодаре.	\N	\N	\N	\N	\N	0	0	0	\N	\N	\N	\N	\N	7055000	8950000	0	f	f	f	f	f	f	\N	\N	\N	\N	\N	\N	t	f	f	f	\N	\N	t	f	0	2025-08-11 19:25:42.735161	2025-08-11 19:25:42.735161
2	ЖК Вишневый Сад	zhk-vishnevyy-sad	4	1	Современный жилой комплекс с развитой инфраструктурой в центре Краснодара	\N	\N	\N	\N	\N	0	0	0	\N	\N	\N	\N	\N	3900000	3900000	0	f	f	f	f	f	f	\N	\N	\N	\N	\N	\N	t	f	f	f	\N	\N	t	f	0	2025-08-11 19:25:42.735161	2025-08-11 19:25:42.735161
3	ЖК на Герцена	zhk-na-gertsena	2	1	Жилой комплекс в историческом центре города	\N	\N	\N	\N	\N	0	0	0	\N	\N	\N	\N	\N	4500000	6200000	0	f	f	f	f	f	f	\N	\N	\N	\N	\N	\N	t	f	f	f	\N	\N	t	f	0	2025-08-11 19:25:42.735161	2025-08-11 19:25:42.735161
4	ЖК Южный парк	zhk-yuzhnyy-park	1	1	Современный жилой комплекс с парковой зоной	\N	\N	\N	\N	\N	0	0	0	\N	\N	\N	\N	\N	5200000	7800000	0	f	f	f	f	f	f	\N	\N	\N	\N	\N	\N	t	f	f	f	\N	\N	t	f	0	2025-08-11 19:25:42.735161	2025-08-11 19:25:42.735161
5	ЖК Европейский	zhk-evropeyskiy	3	1	Жилой комплекс европейского уровня	\N	\N	\N	\N	\N	0	0	0	\N	\N	\N	\N	\N	6100000	8500000	0	f	f	f	f	f	f	\N	\N	\N	\N	\N	\N	t	f	f	f	\N	\N	t	f	0	2025-08-11 19:25:42.735161	2025-08-11 19:25:42.735161
\.


--
-- Data for Name: room_types; Type: TABLE DATA; Schema: public; Owner: neondb_owner
--

COPY public.room_types (id, name, rooms_count) FROM stdin;
\.


--
-- Data for Name: saved_searches; Type: TABLE DATA; Schema: public; Owner: neondb_owner
--

COPY public.saved_searches (id, user_id, name, description, search_type, location, property_type, price_min, price_max, size_min, size_max, developer, complex_name, floor_min, floor_max, cashback_min, additional_filters, notify_new_matches, last_notification_sent, created_from_quiz, created_at, updated_at, last_used, search_name, search_criteria, email_notifications, telegram_notifications, is_active, last_checked) FROM stdin;
1	2	2-3 комнатные в центре		properties	Центральный	2-комн	\N	\N	\N	\N			\N	\N	\N		t	\N	\N	2025-06-30 21:32:09	2025-08-10 23:53:37	2025-08-10 23:53:37	\N	\N	t	f	t	\N
2	2	1-комнатные до 6 млн		properties		1-комн	\N	6000000	\N	\N			\N	\N	\N		t	\N	\N	2025-07-04 21:32:09	2025-08-10 21:32:09	2025-08-10 21:32:09	\N	\N	t	f	t	\N
3	2	Семейные квартиры		properties		3-комн	\N	\N	80	\N			\N	\N	\N		t	\N	\N	2025-08-03 21:32:09	2025-08-10 21:32:09	2025-08-10 21:32:09	\N	\N	t	f	t	\N
4	2	Студии до 4 млн		properties		студия	\N	4000000	\N	\N			\N	\N	\N		f	\N	\N	2025-06-17 21:32:09	2025-08-10 23:11:35	2025-08-10 23:11:35	\N	\N	t	f	t	\N
5	5	Студии до 4 млн		properties		студия	\N	4000000	\N	\N			\N	\N	\N		t	\N	\N	2025-08-09 21:32:09	2025-08-10 21:32:09	2025-08-10 21:32:09	\N	\N	t	f	t	\N
6	5	Премиум квартиры	Элитное жилье премиум-класса	properties			12000000	\N	\N	\N			\N	\N	\N		f	\N	\N	2025-06-18 21:32:09	2025-08-10 21:32:09	2025-08-10 21:32:09	\N	\N	t	f	t	\N
7	5	2-3 комнатные в центре		properties	Центральный	2-комн	\N	\N	\N	\N			\N	\N	\N		t	\N	\N	2025-07-06 21:32:10	2025-08-10 21:32:10	2025-08-10 21:32:10	\N	\N	t	f	t	\N
8	3	Студии до 4 млн		properties		студия	\N	4000000	\N	\N			\N	\N	\N		f	\N	\N	2025-07-08 21:32:10	2025-08-10 21:32:10	2025-08-10 21:32:10	\N	\N	t	f	t	\N
9	3	2-3 комнатные в центре		properties	Центральный	2-комн	\N	\N	\N	\N			\N	\N	\N		f	\N	\N	2025-06-25 21:32:10	2025-08-10 21:32:10	2025-08-10 21:32:10	\N	\N	t	f	t	\N
10	3	Премиум квартиры	Элитное жилье премиум-класса	properties			12000000	\N	\N	\N			\N	\N	\N		t	\N	\N	2025-07-27 21:32:10	2025-08-10 21:32:10	2025-08-10 21:32:10	\N	\N	t	f	t	\N
11	4	Премиум квартиры	Элитное жилье премиум-класса	properties			12000000	\N	\N	\N			\N	\N	\N		t	\N	\N	2025-07-07 21:32:10	2025-08-10 21:32:10	2025-08-10 21:32:10	\N	\N	t	f	t	\N
12	4	1-комнатные до 6 млн		properties		1-комн	\N	6000000	\N	\N			\N	\N	\N		f	\N	\N	2025-07-23 21:32:10	2025-08-10 21:32:10	2025-08-10 21:32:10	\N	\N	t	f	t	\N
13	6	Студии до 4 млн		properties		студия	\N	4000000	\N	\N			\N	\N	\N		t	\N	\N	2025-06-14 21:32:10	2025-08-10 21:32:10	2025-08-10 21:32:10	\N	\N	t	f	t	\N
14	6	Премиум квартиры	Элитное жилье премиум-класса	properties			12000000	\N	\N	\N			\N	\N	\N		t	\N	\N	2025-06-19 21:32:10	2025-08-10 21:32:10	2025-08-10 21:32:10	\N	\N	t	f	t	\N
15	6	2-3 комнатные в центре		properties	Центральный	2-комн	\N	\N	\N	\N			\N	\N	\N		t	\N	\N	2025-08-04 21:32:10	2025-08-10 21:32:10	2025-08-10 21:32:10	\N	\N	t	f	t	\N
16	7	Премиум квартиры	Элитное жилье премиум-класса	properties			12000000	\N	\N	\N			\N	\N	\N		t	\N	\N	2025-07-02 21:32:10	2025-08-10 21:32:10	2025-08-10 21:32:10	\N	\N	t	f	t	\N
17	7	Семейные квартиры		properties		3-комн	\N	\N	80	\N			\N	\N	\N		t	\N	\N	2025-07-18 21:32:10	2025-08-10 21:32:10	2025-08-10 21:32:10	\N	\N	t	f	t	\N
18	2	От менеджера: Поиск 2-комн , 0-50 млн	123	properties			\N	\N	\N	\N			\N	\N	\N		t	\N	\N	2025-08-10 21:33:50	2025-08-10 21:33:50	2025-08-10 21:33:50	\N	\N	t	f	t	\N
19	2	Ага		properties			\N	\N	\N	\N			\N	\N	\N	{"rooms": ["\\u0441\\u0442\\u0443\\u0434\\u0438\\u044f"], "priceTo": "30"}	t	\N	\N	2025-08-10 23:02:00	2025-08-10 23:08:56	2025-08-10 23:08:56	\N	\N	t	f	t	\N
20	2	От менеджера: Поиск 3-комн , 0-33 млн	ну вот	properties			\N	\N	\N	\N			\N	\N	\N		t	\N	\N	2025-08-10 23:23:28	2025-08-10 23:34:02	2025-08-10 23:34:02	\N	\N	t	f	t	\N
21	2	От менеджера: Отладка фильтров	123	properties			\N	\N	\N	\N			\N	\N	\N		t	\N	\N	2025-08-10 23:44:46	2025-08-10 23:44:46	2025-08-10 23:44:46	\N	\N	t	f	t	\N
22	2	От менеджера: Финальный тест	123	properties			\N	\N	\N	\N			\N	\N	\N		t	\N	\N	2025-08-10 23:54:54	2025-08-10 23:54:54	2025-08-10 23:54:54	\N	\N	t	f	t	\N
23	2	Логирование		properties			\N	\N	\N	\N			\N	\N	\N	{"rooms": ["3-\\u043a\\u043e\\u043c\\u043d"], "priceTo": "33"}	t	\N	\N	2025-08-10 23:57:21	2025-08-10 23:57:21	2025-08-10 23:57:21	\N	\N	t	f	t	\N
24	2	От менеджера: Исправлено	123333	properties			\N	\N	\N	\N			\N	\N	\N		t	\N	\N	2025-08-11 00:00:35	2025-08-11 00:00:35	2025-08-11 00:00:35	\N	\N	t	f	t	\N
25	2	От менеджера: Финальный тест 2		properties			\N	\N	\N	\N			\N	\N	\N		t	\N	\N	2025-08-11 00:02:49	2025-08-11 00:02:49	2025-08-11 00:02:49	\N	\N	t	f	t	\N
26	2	От менеджера: Отладка статуса		properties			\N	\N	\N	\N			\N	\N	\N		t	\N	\N	2025-08-11 00:04:49	2025-08-11 00:04:49	2025-08-11 00:04:49	\N	\N	t	f	t	\N
27	2	От менеджера: Исправлено полностью	123	properties			\N	\N	\N	\N			\N	\N	\N	{"districts": [], "developers": [], "rooms": ["3-\\u043a\\u043e\\u043c\\u043d"], "completion": [], "priceFrom": "", "priceTo": "33", "areaFrom": "", "areaTo": ""}	t	\N	\N	2025-08-11 00:07:20	2025-08-11 19:53:23.533636	2025-08-11 19:53:23.532285	\N	\N	t	f	t	\N
\.


--
-- Data for Name: search_categories; Type: TABLE DATA; Schema: public; Owner: neondb_owner
--

COPY public.search_categories (id, name, category_type, slug, created_at) FROM stdin;
\.


--
-- Data for Name: sent_searches; Type: TABLE DATA; Schema: public; Owner: neondb_owner
--

COPY public.sent_searches (id, manager_id, client_id, manager_search_id, name, description, additional_filters, status, viewed_at, applied_at, expires_at, sent_at) FROM stdin;
\.


--
-- Data for Name: streets; Type: TABLE DATA; Schema: public; Owner: neondb_owner
--

COPY public.streets (id, name, slug, district_id) FROM stdin;
1	Гаврилова ул.	гаврилова-ул	\N
2	Гагарина ул.	гагарина-ул	\N
3	Гагаринский бульвар	гагаринскии-бульвар	\N
4	Газовиков ул.	газовиков-ул	\N
5	Галльская ул.	галльская-ул	\N
6	Гамбургская ул.	гамбургская-ул	\N
7	Ганноверская ул.	ганноверская-ул	\N
8	Гаражная ул.	гаражная-ул	\N
9	Гаражный пер.	гаражныи-пер	\N
10	Гасконская ул.	гасконская-ул	\N
11	Гастелло ул.	гастелло-ул	\N
12	Геленджикская ул.	геленджикская-ул	\N
13	Геленджикский проезд	геленджикскии-проезд	\N
14	Генерала Мищенко ул.	генерала-мищенко-ул	\N
15	Генерала Петрова ул.	генерала-петрова-ул	\N
16	Генерала Трошева ул.	генерала-трошева-ул	\N
17	Генеральная ул.	генеральная-ул	\N
18	Геодезическая ул.	геодезическая-ул	\N
19	Геологическая ул.	геологическая-ул	\N
20	Геологический пер.	геологическии-пер	\N
21	Георгия Димитрова пл.	георгия-димитрова-пл	\N
22	Героев-Разведчиков ул.	героев-разведчиков-ул	\N
23	Героя Аверкиева ул.	героя-аверкиева-ул	\N
24	Героя Владислава Посадского ул.	героя-владислава-посадского-ул	\N
25	Героя Сарабеева ул.	героя-сарабеева-ул	\N
26	Героя Яцкова ул.	героя-яцкова-ул	\N
27	Герцена проезд	герцена-проезд	\N
28	Герцена ул.	герцена-ул	\N
29	Гёте пр-кт.	гете-пр-кт	\N
30	Гиагинская ул.	гиагинская-ул	\N
31	Гидростроителей ул.	гидростроителеи-ул	\N
32	Гимназическая ул.	гимназическая-ул	\N
33	Глинки ул.	глинки-ул	\N
34	Глиняный пер.	глиняныи-пер	\N
35	Глубинный пер.	глубинныи-пер	\N
36	Глухой пер.	глухои-пер	\N
37	Гоголя ул.	гоголя-ул	\N
38	Гоголя пер.	гоголя-пер	\N
39	Гоголя (Пашковский) ул.	гоголя-пашковскии-ул	\N
40	Голубиная ул.	голубиная-ул	\N
41	Голубицкая ул.	голубицкая-ул	\N
42	Гомельская ул.	гомельская-ул	\N
43	Гончарная ул.	гончарная-ул	\N
44	Горная ул.	горная-ул	\N
45	Горогороды ул.	горогороды-ул	\N
46	Горького ул.	горького-ул	\N
47	Горького сквер	горького-сквер	\N
48	Горячеключевская ул.	горячеключевская-ул	\N
49	Грабина ул.	грабина-ул	\N
50	Гражданская ул.	гражданская-ул	\N
51	Гранатовая ул.	гранатовая-ул	\N
52	Гренадерская ул.	гренадерская-ул	\N
53	Грибоедова ул.	грибоедова-ул	\N
54	Григория Пономаренко ул.	григория-пономаренко-ул	\N
55	Грозненская ул.	грозненская-ул	\N
56	Грушевая ул.	грушевая-ул	\N
57	Грушевая (СНТ Ветерок) ул.	грушевая-снт-ветерок-ул	\N
58	Грушевая (СНТ Животновод) ул.	грушевая-снт-животновод-ул	\N
59	Грушевая (СНТ Радист) ул.	грушевая-снт-радист-ул	\N
60	Грушевая (СНТ Урожай) ул.	грушевая-снт-урожаи-ул	\N
61	Грушевая (СНТ Янтарь) ул.	грушевая-снт-янтарь-ул	\N
62	Гуденко ул.	гуденко-ул	\N
63	Гудимы ул.	гудимы-ул	\N
64	Дагестанская ул.	дагестанская-ул	\N
65	Дальний бульвар	дальнии-бульвар	\N
66	Дальний проезд	дальнии-проезд	\N
67	Дальняя ул.	дальняя-ул	\N
68	Дальняя (СНТ Солнышко) ул.	дальняя-снт-солнышко-ул	\N
69	Дамаева ул.	дамаева-ул	\N
70	Дачная ул.	дачная-ул	\N
71	Дворцовая ул.	дворцовая-ул	\N
72	Дежнёва ул.	дежнева-ул	\N
73	Декабристов ул.	декабристов-ул	\N
74	Декоративная ул.	декоративная-ул	\N
75	Дементия Красюка ул.	дементия-красюка-ул	\N
76	Демидовская ул.	демидовская-ул	\N
77	Демидовский проезд	демидовскии-проезд	\N
78	Дёмина ул.	демина-ул	\N
79	Демуса ул.	демуса-ул	\N
80	Деповская ул.	деповская-ул	\N
81	Деповской проезд	деповскои-проезд	\N
82	Депутатская ул.	депутатская-ул	\N
83	Дербентская ул.	дербентская-ул	\N
84	Дербентский проезд	дербентскии-проезд	\N
85	Детский сквер	детскии-сквер	\N
86	Джубгинская ул.	джубгинская-ул	\N
87	Дзержинского ул.	дзержинского-ул	\N
88	Дикуна ул.	дикуна-ул	\N
89	Димитрова ул.	димитрова-ул	\N
90	Динской проезд	динскои-проезд	\N
91	Длинная ул.	длинная-ул	\N
92	Дмитриевская Дамба ул.	дмитриевская-дамба-ул	\N
93	Дмитрия Благоева ул.	дмитрия-благоева-ул	\N
94	Дмитрия Донского ул.	дмитрия-донского-ул	\N
95	Дмитрия Пожарского ул.	дмитрия-пожарского-ул	\N
96	Днепровская ул.	днепровская-ул	\N
97	Днестровская ул.	днестровская-ул	\N
98	Добрая ул.	добрая-ул	\N
99	Дозорная ул.	дозорная-ул	\N
100	Докучаева пер.	докучаева-пер	\N
101	Должанская ул.	должанская-ул	\N
102	Домбайская ул.	домбаиская-ул	\N
103	Донская ул.	донская-ул	\N
104	Дорожная ул.	дорожная-ул	\N
105	Достоевского ул.	достоевского-ул	\N
106	Драгунская ул.	драгунская-ул	\N
107	Драгунский проезд	драгунскии-проезд	\N
108	Дрезденская ул.	дрезденская-ул	\N
109	Дружная ул.	дружная-ул	\N
110	Дружный проезд	дружныи-проезд	\N
111	Дубинский сквер	дубинскии-сквер	\N
112	Дубинский пер.	дубинскии-пер	\N
113	Дубравная ул.	дубравная-ул	\N
114	Думенко ул.	думенко-ул	\N
115	Думская ул.	думская-ул	\N
116	Думский пер.	думскии-пер	\N
117	Дунаевского ул.	дунаевского-ул	\N
118	Дунайская ул.	дунаиская-ул	\N
119	Душистая ул.	душистая-ул	\N
120	Дядьковская ул.	дядьковская-ул	\N
121	Евгении Жигуленко ул.	евгении-жигуленко-ул	\N
122	Евгения Сизоненко ул.	евгения-сизоненко-ул	\N
123	Евдокии Бершанской ул.	евдокии-бершанскои-ул	\N
124	Евдокии Сокол ул.	евдокии-сокол-ул	\N
125	Европейский ул.	европеискии-ул	\N
126	Ейская ул.	еиская-ул	\N
127	Екатериновская ул.	екатериновская-ул	\N
128	Екатеринодарская ул.	екатеринодарская-ул	\N
129	Екатерины пл.	екатерины-пл	\N
130	Екатерины Великой ул.	екатерины-великои-ул	\N
131	Елецкая ул.	елецкая-ул	\N
132	Елизаветинская ул.	елизаветинская-ул	\N
133	Елисейская ул.	елисеиская-ул	\N
134	Еловая ул.	еловая-ул	\N
135	Енисейская ул.	енисеиская-ул	\N
136	Есаульская ул.	есаульская-ул	\N
137	Есенина пер.	есенина-пер	\N
138	Есенина ул.	есенина-ул	\N
139	Ессентукская ул.	ессентукская-ул	\N
140	Железнодорожная ул.	железнодорожная-ул	\N
141	Железнодорожная (Индустриальный) ул.	железнодорожная-индустриальныи-ул	\N
142	Жемчужная ул.	жемчужная-ул	\N
143	Живило ул.	живило-ул	\N
144	Живописная ул.	живописная-ул	\N
145	Жигулёвская ул.	жигулевская-ул	\N
146	Жлобы ул.	жлобы-ул	\N
147	Жуковского ул.	жуковского-ул	\N
148	Журавлиная ул.	журавлиная-ул	\N
149	Заводская ул.	заводская-ул	\N
150	Заводская (Пашковский) ул.	заводская-пашковскии-ул	\N
151	Загорская ул.	загорская-ул	\N
152	Закатная ул.	закатная-ул	\N
153	Западная ул.	западная-ул	\N
154	Западно-Кругликовская ул.	западно-кругликовская-ул	\N
155	Западный Обход ул.	западныи-обход-ул	\N
156	Заполярная ул.	заполярная-ул	\N
157	Запорожская ул.	запорожская-ул	\N
158	Заречный пер.	заречныи-пер	\N
159	Затонная ул.	затонная-ул	\N
160	Затонный проезд	затонныи-проезд	\N
161	Захарова ул.	захарова-ул	\N
162	Защитников Отечества ул.	защитников-отечества-ул	\N
163	Званая ул.	званая-ул	\N
164	Звездная ул.	звездная-ул	\N
165	Звездный пер.	звездныи-пер	\N
166	Звездопадная ул.	звездопадная-ул	\N
167	Звенигородская ул.	звенигородская-ул	\N
168	Звенящая ул.	звенящая-ул	\N
169	Зеленоградская ул.	зеленоградская-ул	\N
170	Земляничная ул.	земляничная-ул	\N
171	Земляничная (Северный) ул.	земляничная-северныи-ул	\N
172	Зенитчиков сквер	зенитчиков-сквер	\N
173	Зины Портновой ул.	зины-портновои-ул	\N
174	Зиповская ул.	зиповская-ул	\N
175	Знаменская ул.	знаменская-ул	\N
176	Зои Космодемьянской ул.	зои-космодемьянскои-ул	\N
177	Зональная ул.	зональная-ул	\N
178	Зоотехническая ул.	зоотехническая-ул	\N
179	Ивана Кияшко пер.	ивана-кияшко-пер	\N
180	Ивана Кияшко ул.	ивана-кияшко-ул	\N
181	Ивана Кожедуба ул.	ивана-кожедуба-ул	\N
182	Ивана Рослого ул.	ивана-рослого-ул	\N
183	Ивана Сусанина ул.	ивана-сусанина-ул	\N
184	Ивановская ул.	ивановская-ул	\N
185	Ивдельская ул.	ивдельская-ул	\N
186	Игнатова ул.	игнатова-ул	\N
187	Игоря Агаркова ул.	игоря-агаркова-ул	\N
188	Измаильская ул.	измаильская-ул	\N
189	Изобильная ул.	изобильная-ул	\N
190	Изосимова ул.	изосимова-ул	\N
191	Изумрудная ул.	изумрудная-ул	\N
192	Изумрудный проезд	изумрудныи-проезд	\N
193	Ильинская ул.	ильинская-ул	\N
194	Ильский пер.	ильскии-пер	\N
195	имени Г.К. Жукова сквер	имени-гк-жукова-сквер	\N
196	имени Гатова сквер	имени-гатова-сквер	\N
197	имени Доватора ул.	имени-доватора-ул	\N
198	имени Л.Н. Толстого сквер	имени-лн-толстого-сквер	\N
199	имени Ломоносова ул.	имени-ломоносова-ул	\N
200	имени Суворова (Пашковский) ул.	имени-суворова-пашковскии-ул	\N
201	имени Ф.Э. Дзержинского сквер	имени-фэ-дзержинского-сквер	\N
202	имени Челюскина ул.	имени-челюскина-ул	\N
203	Индустриальная ул.	индустриальная-ул	\N
204	Индустриальный проезд	индустриальныи-проезд	\N
205	Инициативная ул.	инициативная-ул	\N
206	Институтская ул.	институтская-ул	\N
207	Интернациональный бульвар	интернациональныи-бульвар	\N
208	Ипподромная ул.	ипподромная-ул	\N
209	Ипподромная (СНТ Урожай) ул.	ипподромная-снт-урожаи-ул	\N
210	Ипподромный проезд	ипподромныи-проезд	\N
211	Ирклиевская ул.	ирклиевская-ул	\N
212	Иркутская ул.	иркутская-ул	\N
213	Историческая ул.	историческая-ул	\N
214	Ишунина пер.	ишунина-пер	\N
\.


--
-- Data for Name: user_notifications; Type: TABLE DATA; Schema: public; Owner: neondb_owner
--

COPY public.user_notifications (id, user_id, title, message, notification_type, icon, is_read, action_url, created_at, read_at) FROM stdin;
\.


--
-- Data for Name: users; Type: TABLE DATA; Schema: public; Owner: neondb_owner
--

COPY public.users (id, email, phone, telegram_id, full_name, password_hash, preferred_contact, email_notifications, telegram_notifications, notify_recommendations, notify_saved_searches, notify_applications, notify_cashback, notify_marketing, profile_image, user_id, role, is_active, is_verified, verification_token, is_demo, verified, registration_source, client_notes, assigned_manager_id, client_status, preferred_district, property_type, room_count, budget_range, quiz_completed, created_at, updated_at, last_login) FROM stdin;
3	manager@inback.ru			Демо Менеджер	scrypt:32768:8:1$yBxWMnshg9JxxFuY$fd92a8332fbe40fafe78992b52903a725f00219c39cf1efb970fe2ef3b936c2cb8cc435e343d3dca6d4aedeadcc39cea34dde806541abd9df8ecad75bd66eb2e	email	t	f	\N	\N	\N	\N	\N	\N	CB87654321	manager	t	f		\N	\N	Website		\N	Новый					f	2025-08-10 21:05:25	2025-08-11 19:29:16.802443	2025-08-11 19:29:16.80245
4	admin@inback.ru			Администратор	scrypt:32768:8:1$yBxWMnshg9JxxFuY$fd92a8332fbe40fafe78992b52903a725f00219c39cf1efb970fe2ef3b936c2cb8cc435e343d3dca6d4aedeadcc39cea34dde806541abd9df8ecad75bd66eb2e	email	t	f	\N	\N	\N	\N	\N	\N	CB11111111	admin	t	f		\N	\N	Website		\N	Новый					f	2025-08-10 21:05:25	2025-08-11 19:29:16.905601	2025-08-11 19:29:16.905608
5	ivan.petrov@email.ru	+7-918-234-56-78		Иван Петров	scrypt:32768:8:1$yBxWMnshg9JxxFuY$fd92a8332fbe40fafe78992b52903a725f00219c39cf1efb970fe2ef3b936c2cb8cc435e343d3dca6d4aedeadcc39cea34dde806541abd9df8ecad75bd66eb2e	email	t	f	\N	\N	\N	\N	\N	\N	CB39259319	buyer	f	f		\N	\N	Website		\N	Активный					f	2025-08-10 21:24:54	2025-08-11 15:00:39	2025-08-11 19:29:17.009097
2	demo@inback.ru			Демо Покупатель	scrypt:32768:8:1$yBxWMnshg9JxxFuY$fd92a8332fbe40fafe78992b52903a725f00219c39cf1efb970fe2ef3b936c2cb8cc435e343d3dca6d4aedeadcc39cea34dde806541abd9df8ecad75bd66eb2e	email	t	f	\N	\N	\N	\N	\N	\N	CB12345678	buyer	t	f		\N	\N	Website		\N	Новый					f	2025-08-10 21:05:25	2025-08-11 19:30:48.227681	2025-08-11 19:30:48.225822
6	maria.sidorova@email.ru	+7-918-345-67-89		Мария Сидорова	scrypt:32768:8:1$yBxWMnshg9JxxFuY$fd92a8332fbe40fafe78992b52903a725f00219c39cf1efb970fe2ef3b936c2cb8cc435e343d3dca6d4aedeadcc39cea34dde806541abd9df8ecad75bd66eb2e	email	t	f	\N	\N	\N	\N	\N	\N	CB54057265	buyer	t	f		\N	\N	Website		\N	Новый					f	2025-08-10 21:24:54	2025-08-10 21:24:54	2025-08-11 19:29:17.112029
7	alex.kozlov@email.ru	+7-918-456-78-90		Александр Козлов	scrypt:32768:8:1$yBxWMnshg9JxxFuY$fd92a8332fbe40fafe78992b52903a725f00219c39cf1efb970fe2ef3b936c2cb8cc435e343d3dca6d4aedeadcc39cea34dde806541abd9df8ecad75bd66eb2e	email	t	f	\N	\N	\N	\N	\N	\N	CB69534545	buyer	t	f		\N	\N	Website		\N	В работе					f	2025-08-10 21:24:55	2025-08-10 21:24:55	2025-08-11 19:29:17.214715
8	elena.smirnova@email.ru	+7-918-567-89-01		Елена Смирнова	scrypt:32768:8:1$yBxWMnshg9JxxFuY$fd92a8332fbe40fafe78992b52903a725f00219c39cf1efb970fe2ef3b936c2cb8cc435e343d3dca6d4aedeadcc39cea34dde806541abd9df8ecad75bd66eb2e	email	t	f	\N	\N	\N	\N	\N	\N	CB78733862	buyer	t	f		\N	\N	Website		\N	Активный					f	2025-08-10 21:24:55	2025-08-10 21:24:55	2025-08-11 19:29:17.320234
9	dmitry.volkov@email.ru	+7-918-678-90-12		Дмитрий Волков	scrypt:32768:8:1$yBxWMnshg9JxxFuY$fd92a8332fbe40fafe78992b52903a725f00219c39cf1efb970fe2ef3b936c2cb8cc435e343d3dca6d4aedeadcc39cea34dde806541abd9df8ecad75bd66eb2e	email	t	f	\N	\N	\N	\N	\N	\N	CB31150897	buyer	t	f		\N	\N	Website		\N	Новый					f	2025-08-10 21:24:55	2025-08-10 21:24:55	2025-08-11 19:29:17.423519
10	test@inback.ru	+7900123456		Тестовый Пользователь	scrypt:32768:8:1$yBxWMnshg9JxxFuY$fd92a8332fbe40fafe78992b52903a725f00219c39cf1efb970fe2ef3b936c2cb8cc435e343d3dca6d4aedeadcc39cea34dde806541abd9df8ecad75bd66eb2e	email	t	f	\N	\N	\N	\N	\N	\N	CB49690145	buyer	t	f		\N	\N	Website		\N	Новый					f	2025-08-10 23:18:17	2025-08-10 23:18:17	2025-08-11 19:29:17.527442
12	email_only@inback.ru			Email Пользователь	scrypt:32768:8:1$yBxWMnshg9JxxFuY$fd92a8332fbe40fafe78992b52903a725f00219c39cf1efb970fe2ef3b936c2cb8cc435e343d3dca6d4aedeadcc39cea34dde806541abd9df8ecad75bd66eb2e	email	t	f	\N	\N	\N	\N	\N	\N	CB71638148	buyer	t	f		\N	\N	Website		\N	Новый					f	2025-08-11 15:40:09	2025-08-11 15:40:09	2025-08-11 19:29:17.636464
13	whatsapp@inback.ru	+7-918-999-88-77		WhatsApp Пользователь	scrypt:32768:8:1$yBxWMnshg9JxxFuY$fd92a8332fbe40fafe78992b52903a725f00219c39cf1efb970fe2ef3b936c2cb8cc435e343d3dca6d4aedeadcc39cea34dde806541abd9df8ecad75bd66eb2e	email	f	f	\N	\N	\N	\N	\N	\N	CB34634650	buyer	t	f		\N	\N	Website		\N	Новый					f	2025-08-11 15:40:10	2025-08-11 15:40:10	2025-08-11 19:29:17.739908
15	new.client@example.com	+7-918-123-45-67	\N	Новый Клиент	scrypt:32768:8:1$m1BwNh41dLNQDJob$5a7d95e056f43ef6f482b6678c0712f78603319025c1c0364e01ba049f3d6f7c8174e1a79d5d0519aad4d7d8f1b22c783e2c165892c7cd8c5fe95dbba0f0ca03	email	t	f	t	t	t	t	f	https://randomuser.me/api/portraits/men/32.jpg	CB94206088	buyer	t	f	\N	f	f	Website	\N	1	Новый	\N	\N	\N	\N	f	2025-08-12 18:43:08.064375	2025-08-12 18:43:08.064382	\N
16	working.test.client@example.com	+7-918-666-55-44	\N	Рабочий Тест Клиент	\N	email	t	f	t	t	t	t	f	https://randomuser.me/api/portraits/men/32.jpg	CB50027764	buyer	t	f	\N	f	f	Manager	\N	1	Новый	\N	\N	\N	\N	f	2025-08-12 18:44:41.904825	2025-08-12 18:44:41.90483	\N
17	bithomghse@mail.ru	+7-952-490-42-60	\N	Станислав hg	\N	email	t	f	t	t	t	t	f	https://randomuser.me/api/portraits/men/32.jpg	CB85827310	buyer	t	f	\N	f	f	Manager	\N	1	Новый	\N	\N	\N	\N	f	2025-08-12 18:52:06.547753	2025-08-12 18:52:06.547756	\N
18	test.password.client@example.com	+7-918-555-44-33	\N	Тест Пароль Клиент	scrypt:32768:8:1$8Bl7ZVq9sksCfixj$a4636e9f2913acc28a254456bd8f1e45e18aee120d1e8ef03abd08129991598410d7e323f7216cf8bdb35e2c2b8f20905aed9f66883ff03c00dbfd5943b07496	email	t	f	t	t	t	t	f	https://randomuser.me/api/portraits/men/32.jpg	CB11464389	buyer	t	f	\N	f	f	Manager	\N	1	Новый	\N	\N	\N	\N	f	2025-08-12 18:53:51.96034	2025-08-12 18:54:22.79387	2025-08-12 18:54:22.791864
19	new.client.final@example.com	+7-952-490-42-69	\N	Станислав Новый Клиент	scrypt:32768:8:1$1NgPsQCL2woWR2er$7420839dc57598241c819ffabfe384490a3b564a81a2dd0fa169a0ff4663bbca746106bd47a857d43239c5ced498a4ce361633fbe5f804959faae0cf11a5eba6	email	t	f	t	t	t	t	f	https://randomuser.me/api/portraits/men/32.jpg	CB13122017	buyer	t	f	\N	f	f	Manager	\N	1	Новый	\N	\N	\N	\N	f	2025-08-12 18:55:04.179486	2025-08-12 18:55:04.179489	\N
20	ultimaten@inback.ru	+7-952-490-82-69	730764738	Станислав Ультимейт	\N	\N	\N	t	t	\N	\N	\N	\N	\N	ULT17550252	buyer	t	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	2025-08-12 19:00:14.629974	2025-08-12 19:00:14.629974	\N
14	bithome@mail.ru	+7-952-490-82-69	730764738	Станислав Врублевский	scrypt:32768:8:1$yBxWMnshg9JxxFuY$fd92a8332fbe40fafe78992b52903a725f00219c39cf1efb970fe2ef3b936c2cb8cc435e343d3dca6d4aedeadcc39cea34dde806541abd9df8ecad75bd66eb2e	both	t	t	t	\N	\N	\N	\N	\N	CB76327433	buyer	t	f		\N	\N	Website		1	Новый	Центральный	Квартира	2	4-6 млн	f	2025-08-11 15:59:11	2025-08-11 21:58:55.177116	2025-08-11 16:14:50
\.


--
-- Name: admins_id_seq; Type: SEQUENCE SET; Schema: public; Owner: neondb_owner
--

SELECT pg_catalog.setval('public.admins_id_seq', 1, true);


--
-- Name: applications_id_seq; Type: SEQUENCE SET; Schema: public; Owner: neondb_owner
--

SELECT pg_catalog.setval('public.applications_id_seq', 4, true);


--
-- Name: blog_articles_id_seq; Type: SEQUENCE SET; Schema: public; Owner: neondb_owner
--

SELECT pg_catalog.setval('public.blog_articles_id_seq', 5, true);


--
-- Name: blog_categories_id_seq; Type: SEQUENCE SET; Schema: public; Owner: neondb_owner
--

SELECT pg_catalog.setval('public.blog_categories_id_seq', 13, true);


--
-- Name: blog_comments_id_seq; Type: SEQUENCE SET; Schema: public; Owner: neondb_owner
--

SELECT pg_catalog.setval('public.blog_comments_id_seq', 1, false);


--
-- Name: blog_posts_id_seq; Type: SEQUENCE SET; Schema: public; Owner: neondb_owner
--

SELECT pg_catalog.setval('public.blog_posts_id_seq', 15, true);


--
-- Name: blog_tags_id_seq; Type: SEQUENCE SET; Schema: public; Owner: neondb_owner
--

SELECT pg_catalog.setval('public.blog_tags_id_seq', 1, false);


--
-- Name: callback_requests_id_seq; Type: SEQUENCE SET; Schema: public; Owner: neondb_owner
--

SELECT pg_catalog.setval('public.callback_requests_id_seq', 2, true);


--
-- Name: cashback_applications_id_seq; Type: SEQUENCE SET; Schema: public; Owner: neondb_owner
--

SELECT pg_catalog.setval('public.cashback_applications_id_seq', 1, false);


--
-- Name: cashback_payouts_id_seq; Type: SEQUENCE SET; Schema: public; Owner: neondb_owner
--

SELECT pg_catalog.setval('public.cashback_payouts_id_seq', 1, false);


--
-- Name: cashback_records_id_seq; Type: SEQUENCE SET; Schema: public; Owner: neondb_owner
--

SELECT pg_catalog.setval('public.cashback_records_id_seq', 1, false);


--
-- Name: cities_id_seq; Type: SEQUENCE SET; Schema: public; Owner: neondb_owner
--

SELECT pg_catalog.setval('public.cities_id_seq', 1, false);


--
-- Name: client_property_recommendations_id_seq; Type: SEQUENCE SET; Schema: public; Owner: neondb_owner
--

SELECT pg_catalog.setval('public.client_property_recommendations_id_seq', 1, false);


--
-- Name: collection_properties_id_seq; Type: SEQUENCE SET; Schema: public; Owner: neondb_owner
--

SELECT pg_catalog.setval('public.collection_properties_id_seq', 1, false);


--
-- Name: collections_id_seq; Type: SEQUENCE SET; Schema: public; Owner: neondb_owner
--

SELECT pg_catalog.setval('public.collections_id_seq', 1, false);


--
-- Name: developer_appointments_id_seq; Type: SEQUENCE SET; Schema: public; Owner: neondb_owner
--

SELECT pg_catalog.setval('public.developer_appointments_id_seq', 1, false);


--
-- Name: developers_id_seq; Type: SEQUENCE SET; Schema: public; Owner: neondb_owner
--

SELECT pg_catalog.setval('public.developers_id_seq', 1, false);


--
-- Name: districts_id_seq; Type: SEQUENCE SET; Schema: public; Owner: neondb_owner
--

SELECT pg_catalog.setval('public.districts_id_seq', 1, false);


--
-- Name: documents_id_seq; Type: SEQUENCE SET; Schema: public; Owner: neondb_owner
--

SELECT pg_catalog.setval('public.documents_id_seq', 1, false);


--
-- Name: favorite_properties_id_seq; Type: SEQUENCE SET; Schema: public; Owner: neondb_owner
--

SELECT pg_catalog.setval('public.favorite_properties_id_seq', 1, false);


--
-- Name: favorites_id_seq; Type: SEQUENCE SET; Schema: public; Owner: neondb_owner
--

SELECT pg_catalog.setval('public.favorites_id_seq', 1, false);


--
-- Name: manager_saved_searches_id_seq; Type: SEQUENCE SET; Schema: public; Owner: neondb_owner
--

SELECT pg_catalog.setval('public.manager_saved_searches_id_seq', 1, false);


--
-- Name: managers_id_seq; Type: SEQUENCE SET; Schema: public; Owner: neondb_owner
--

SELECT pg_catalog.setval('public.managers_id_seq', 1, true);


--
-- Name: notifications_id_seq; Type: SEQUENCE SET; Schema: public; Owner: neondb_owner
--

SELECT pg_catalog.setval('public.notifications_id_seq', 1, false);


--
-- Name: recommendation_categories_id_seq; Type: SEQUENCE SET; Schema: public; Owner: neondb_owner
--

SELECT pg_catalog.setval('public.recommendation_categories_id_seq', 1, false);


--
-- Name: recommendation_templates_id_seq; Type: SEQUENCE SET; Schema: public; Owner: neondb_owner
--

SELECT pg_catalog.setval('public.recommendation_templates_id_seq', 1, false);


--
-- Name: recommendations_id_seq; Type: SEQUENCE SET; Schema: public; Owner: neondb_owner
--

SELECT pg_catalog.setval('public.recommendations_id_seq', 22, true);


--
-- Name: residential_complexes_id_seq; Type: SEQUENCE SET; Schema: public; Owner: neondb_owner
--

SELECT pg_catalog.setval('public.residential_complexes_id_seq', 1, false);


--
-- Name: room_types_id_seq; Type: SEQUENCE SET; Schema: public; Owner: neondb_owner
--

SELECT pg_catalog.setval('public.room_types_id_seq', 1, false);


--
-- Name: saved_searches_id_seq; Type: SEQUENCE SET; Schema: public; Owner: neondb_owner
--

SELECT pg_catalog.setval('public.saved_searches_id_seq', 1, false);


--
-- Name: search_categories_id_seq; Type: SEQUENCE SET; Schema: public; Owner: neondb_owner
--

SELECT pg_catalog.setval('public.search_categories_id_seq', 1, false);


--
-- Name: sent_searches_id_seq; Type: SEQUENCE SET; Schema: public; Owner: neondb_owner
--

SELECT pg_catalog.setval('public.sent_searches_id_seq', 1, false);


--
-- Name: streets_id_seq; Type: SEQUENCE SET; Schema: public; Owner: neondb_owner
--

SELECT pg_catalog.setval('public.streets_id_seq', 214, true);


--
-- Name: user_notifications_id_seq; Type: SEQUENCE SET; Schema: public; Owner: neondb_owner
--

SELECT pg_catalog.setval('public.user_notifications_id_seq', 1, false);


--
-- Name: users_id_seq; Type: SEQUENCE SET; Schema: public; Owner: neondb_owner
--

SELECT pg_catalog.setval('public.users_id_seq', 20, true);


--
-- Name: admins admins_admin_id_key; Type: CONSTRAINT; Schema: public; Owner: neondb_owner
--

ALTER TABLE ONLY public.admins
    ADD CONSTRAINT admins_admin_id_key UNIQUE (admin_id);


--
-- Name: admins admins_pkey; Type: CONSTRAINT; Schema: public; Owner: neondb_owner
--

ALTER TABLE ONLY public.admins
    ADD CONSTRAINT admins_pkey PRIMARY KEY (id);


--
-- Name: applications applications_pkey; Type: CONSTRAINT; Schema: public; Owner: neondb_owner
--

ALTER TABLE ONLY public.applications
    ADD CONSTRAINT applications_pkey PRIMARY KEY (id);


--
-- Name: blog_article_tags blog_article_tags_pkey; Type: CONSTRAINT; Schema: public; Owner: neondb_owner
--

ALTER TABLE ONLY public.blog_article_tags
    ADD CONSTRAINT blog_article_tags_pkey PRIMARY KEY (article_id, tag_id);


--
-- Name: blog_articles blog_articles_pkey; Type: CONSTRAINT; Schema: public; Owner: neondb_owner
--

ALTER TABLE ONLY public.blog_articles
    ADD CONSTRAINT blog_articles_pkey PRIMARY KEY (id);


--
-- Name: blog_articles blog_articles_slug_key; Type: CONSTRAINT; Schema: public; Owner: neondb_owner
--

ALTER TABLE ONLY public.blog_articles
    ADD CONSTRAINT blog_articles_slug_key UNIQUE (slug);


--
-- Name: blog_categories blog_categories_name_key; Type: CONSTRAINT; Schema: public; Owner: neondb_owner
--

ALTER TABLE ONLY public.blog_categories
    ADD CONSTRAINT blog_categories_name_key UNIQUE (name);


--
-- Name: blog_categories blog_categories_pkey; Type: CONSTRAINT; Schema: public; Owner: neondb_owner
--

ALTER TABLE ONLY public.blog_categories
    ADD CONSTRAINT blog_categories_pkey PRIMARY KEY (id);


--
-- Name: blog_categories blog_categories_slug_key; Type: CONSTRAINT; Schema: public; Owner: neondb_owner
--

ALTER TABLE ONLY public.blog_categories
    ADD CONSTRAINT blog_categories_slug_key UNIQUE (slug);


--
-- Name: blog_comments blog_comments_pkey; Type: CONSTRAINT; Schema: public; Owner: neondb_owner
--

ALTER TABLE ONLY public.blog_comments
    ADD CONSTRAINT blog_comments_pkey PRIMARY KEY (id);


--
-- Name: blog_posts blog_posts_pkey; Type: CONSTRAINT; Schema: public; Owner: neondb_owner
--

ALTER TABLE ONLY public.blog_posts
    ADD CONSTRAINT blog_posts_pkey PRIMARY KEY (id);


--
-- Name: blog_posts blog_posts_slug_key; Type: CONSTRAINT; Schema: public; Owner: neondb_owner
--

ALTER TABLE ONLY public.blog_posts
    ADD CONSTRAINT blog_posts_slug_key UNIQUE (slug);


--
-- Name: blog_tags blog_tags_name_key; Type: CONSTRAINT; Schema: public; Owner: neondb_owner
--

ALTER TABLE ONLY public.blog_tags
    ADD CONSTRAINT blog_tags_name_key UNIQUE (name);


--
-- Name: blog_tags blog_tags_pkey; Type: CONSTRAINT; Schema: public; Owner: neondb_owner
--

ALTER TABLE ONLY public.blog_tags
    ADD CONSTRAINT blog_tags_pkey PRIMARY KEY (id);


--
-- Name: blog_tags blog_tags_slug_key; Type: CONSTRAINT; Schema: public; Owner: neondb_owner
--

ALTER TABLE ONLY public.blog_tags
    ADD CONSTRAINT blog_tags_slug_key UNIQUE (slug);


--
-- Name: callback_requests callback_requests_pkey; Type: CONSTRAINT; Schema: public; Owner: neondb_owner
--

ALTER TABLE ONLY public.callback_requests
    ADD CONSTRAINT callback_requests_pkey PRIMARY KEY (id);


--
-- Name: cashback_applications cashback_applications_pkey; Type: CONSTRAINT; Schema: public; Owner: neondb_owner
--

ALTER TABLE ONLY public.cashback_applications
    ADD CONSTRAINT cashback_applications_pkey PRIMARY KEY (id);


--
-- Name: cashback_payouts cashback_payouts_pkey; Type: CONSTRAINT; Schema: public; Owner: neondb_owner
--

ALTER TABLE ONLY public.cashback_payouts
    ADD CONSTRAINT cashback_payouts_pkey PRIMARY KEY (id);


--
-- Name: cashback_records cashback_records_pkey; Type: CONSTRAINT; Schema: public; Owner: neondb_owner
--

ALTER TABLE ONLY public.cashback_records
    ADD CONSTRAINT cashback_records_pkey PRIMARY KEY (id);


--
-- Name: cities cities_name_key; Type: CONSTRAINT; Schema: public; Owner: neondb_owner
--

ALTER TABLE ONLY public.cities
    ADD CONSTRAINT cities_name_key UNIQUE (name);


--
-- Name: cities cities_pkey; Type: CONSTRAINT; Schema: public; Owner: neondb_owner
--

ALTER TABLE ONLY public.cities
    ADD CONSTRAINT cities_pkey PRIMARY KEY (id);


--
-- Name: cities cities_slug_key; Type: CONSTRAINT; Schema: public; Owner: neondb_owner
--

ALTER TABLE ONLY public.cities
    ADD CONSTRAINT cities_slug_key UNIQUE (slug);


--
-- Name: client_property_recommendations client_property_recommendations_pkey; Type: CONSTRAINT; Schema: public; Owner: neondb_owner
--

ALTER TABLE ONLY public.client_property_recommendations
    ADD CONSTRAINT client_property_recommendations_pkey PRIMARY KEY (id);


--
-- Name: collection_properties collection_properties_pkey; Type: CONSTRAINT; Schema: public; Owner: neondb_owner
--

ALTER TABLE ONLY public.collection_properties
    ADD CONSTRAINT collection_properties_pkey PRIMARY KEY (id);


--
-- Name: collections collections_pkey; Type: CONSTRAINT; Schema: public; Owner: neondb_owner
--

ALTER TABLE ONLY public.collections
    ADD CONSTRAINT collections_pkey PRIMARY KEY (id);


--
-- Name: developer_appointments developer_appointments_pkey; Type: CONSTRAINT; Schema: public; Owner: neondb_owner
--

ALTER TABLE ONLY public.developer_appointments
    ADD CONSTRAINT developer_appointments_pkey PRIMARY KEY (id);


--
-- Name: developers developers_pkey; Type: CONSTRAINT; Schema: public; Owner: neondb_owner
--

ALTER TABLE ONLY public.developers
    ADD CONSTRAINT developers_pkey PRIMARY KEY (id);


--
-- Name: developers developers_slug_key; Type: CONSTRAINT; Schema: public; Owner: neondb_owner
--

ALTER TABLE ONLY public.developers
    ADD CONSTRAINT developers_slug_key UNIQUE (slug);


--
-- Name: districts districts_pkey; Type: CONSTRAINT; Schema: public; Owner: neondb_owner
--

ALTER TABLE ONLY public.districts
    ADD CONSTRAINT districts_pkey PRIMARY KEY (id);


--
-- Name: districts districts_slug_key; Type: CONSTRAINT; Schema: public; Owner: neondb_owner
--

ALTER TABLE ONLY public.districts
    ADD CONSTRAINT districts_slug_key UNIQUE (slug);


--
-- Name: documents documents_pkey; Type: CONSTRAINT; Schema: public; Owner: neondb_owner
--

ALTER TABLE ONLY public.documents
    ADD CONSTRAINT documents_pkey PRIMARY KEY (id);


--
-- Name: favorite_properties favorite_properties_pkey; Type: CONSTRAINT; Schema: public; Owner: neondb_owner
--

ALTER TABLE ONLY public.favorite_properties
    ADD CONSTRAINT favorite_properties_pkey PRIMARY KEY (id);


--
-- Name: favorites favorites_pkey; Type: CONSTRAINT; Schema: public; Owner: neondb_owner
--

ALTER TABLE ONLY public.favorites
    ADD CONSTRAINT favorites_pkey PRIMARY KEY (id);


--
-- Name: manager_saved_searches manager_saved_searches_pkey; Type: CONSTRAINT; Schema: public; Owner: neondb_owner
--

ALTER TABLE ONLY public.manager_saved_searches
    ADD CONSTRAINT manager_saved_searches_pkey PRIMARY KEY (id);


--
-- Name: managers managers_manager_id_key; Type: CONSTRAINT; Schema: public; Owner: neondb_owner
--

ALTER TABLE ONLY public.managers
    ADD CONSTRAINT managers_manager_id_key UNIQUE (manager_id);


--
-- Name: managers managers_pkey; Type: CONSTRAINT; Schema: public; Owner: neondb_owner
--

ALTER TABLE ONLY public.managers
    ADD CONSTRAINT managers_pkey PRIMARY KEY (id);


--
-- Name: notifications notifications_pkey; Type: CONSTRAINT; Schema: public; Owner: neondb_owner
--

ALTER TABLE ONLY public.notifications
    ADD CONSTRAINT notifications_pkey PRIMARY KEY (id);


--
-- Name: recommendation_categories recommendation_categories_pkey; Type: CONSTRAINT; Schema: public; Owner: neondb_owner
--

ALTER TABLE ONLY public.recommendation_categories
    ADD CONSTRAINT recommendation_categories_pkey PRIMARY KEY (id);


--
-- Name: recommendation_templates recommendation_templates_pkey; Type: CONSTRAINT; Schema: public; Owner: neondb_owner
--

ALTER TABLE ONLY public.recommendation_templates
    ADD CONSTRAINT recommendation_templates_pkey PRIMARY KEY (id);


--
-- Name: recommendations recommendations_pkey; Type: CONSTRAINT; Schema: public; Owner: neondb_owner
--

ALTER TABLE ONLY public.recommendations
    ADD CONSTRAINT recommendations_pkey PRIMARY KEY (id);


--
-- Name: residential_complexes residential_complexes_pkey; Type: CONSTRAINT; Schema: public; Owner: neondb_owner
--

ALTER TABLE ONLY public.residential_complexes
    ADD CONSTRAINT residential_complexes_pkey PRIMARY KEY (id);


--
-- Name: residential_complexes residential_complexes_slug_key; Type: CONSTRAINT; Schema: public; Owner: neondb_owner
--

ALTER TABLE ONLY public.residential_complexes
    ADD CONSTRAINT residential_complexes_slug_key UNIQUE (slug);


--
-- Name: room_types room_types_pkey; Type: CONSTRAINT; Schema: public; Owner: neondb_owner
--

ALTER TABLE ONLY public.room_types
    ADD CONSTRAINT room_types_pkey PRIMARY KEY (id);


--
-- Name: saved_searches saved_searches_pkey; Type: CONSTRAINT; Schema: public; Owner: neondb_owner
--

ALTER TABLE ONLY public.saved_searches
    ADD CONSTRAINT saved_searches_pkey PRIMARY KEY (id);


--
-- Name: search_categories search_categories_pkey; Type: CONSTRAINT; Schema: public; Owner: neondb_owner
--

ALTER TABLE ONLY public.search_categories
    ADD CONSTRAINT search_categories_pkey PRIMARY KEY (id);


--
-- Name: sent_searches sent_searches_pkey; Type: CONSTRAINT; Schema: public; Owner: neondb_owner
--

ALTER TABLE ONLY public.sent_searches
    ADD CONSTRAINT sent_searches_pkey PRIMARY KEY (id);


--
-- Name: streets streets_pkey; Type: CONSTRAINT; Schema: public; Owner: neondb_owner
--

ALTER TABLE ONLY public.streets
    ADD CONSTRAINT streets_pkey PRIMARY KEY (id);


--
-- Name: streets streets_slug_key; Type: CONSTRAINT; Schema: public; Owner: neondb_owner
--

ALTER TABLE ONLY public.streets
    ADD CONSTRAINT streets_slug_key UNIQUE (slug);


--
-- Name: favorites unique_user_property; Type: CONSTRAINT; Schema: public; Owner: neondb_owner
--

ALTER TABLE ONLY public.favorites
    ADD CONSTRAINT unique_user_property UNIQUE (user_id, property_id);


--
-- Name: user_notifications user_notifications_pkey; Type: CONSTRAINT; Schema: public; Owner: neondb_owner
--

ALTER TABLE ONLY public.user_notifications
    ADD CONSTRAINT user_notifications_pkey PRIMARY KEY (id);


--
-- Name: users users_pkey; Type: CONSTRAINT; Schema: public; Owner: neondb_owner
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_pkey PRIMARY KEY (id);


--
-- Name: users users_user_id_key; Type: CONSTRAINT; Schema: public; Owner: neondb_owner
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_user_id_key UNIQUE (user_id);


--
-- Name: ix_admins_email; Type: INDEX; Schema: public; Owner: neondb_owner
--

CREATE UNIQUE INDEX ix_admins_email ON public.admins USING btree (email);


--
-- Name: ix_managers_email; Type: INDEX; Schema: public; Owner: neondb_owner
--

CREATE UNIQUE INDEX ix_managers_email ON public.managers USING btree (email);


--
-- Name: ix_users_email; Type: INDEX; Schema: public; Owner: neondb_owner
--

CREATE UNIQUE INDEX ix_users_email ON public.users USING btree (email);


--
-- Name: applications applications_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: neondb_owner
--

ALTER TABLE ONLY public.applications
    ADD CONSTRAINT applications_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(id);


--
-- Name: blog_article_tags blog_article_tags_article_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: neondb_owner
--

ALTER TABLE ONLY public.blog_article_tags
    ADD CONSTRAINT blog_article_tags_article_id_fkey FOREIGN KEY (article_id) REFERENCES public.blog_articles(id);


--
-- Name: blog_article_tags blog_article_tags_tag_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: neondb_owner
--

ALTER TABLE ONLY public.blog_article_tags
    ADD CONSTRAINT blog_article_tags_tag_id_fkey FOREIGN KEY (tag_id) REFERENCES public.blog_tags(id);


--
-- Name: blog_articles blog_articles_author_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: neondb_owner
--

ALTER TABLE ONLY public.blog_articles
    ADD CONSTRAINT blog_articles_author_id_fkey FOREIGN KEY (author_id) REFERENCES public.managers(id);


--
-- Name: blog_articles blog_articles_category_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: neondb_owner
--

ALTER TABLE ONLY public.blog_articles
    ADD CONSTRAINT blog_articles_category_id_fkey FOREIGN KEY (category_id) REFERENCES public.blog_categories(id);


--
-- Name: blog_comments blog_comments_article_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: neondb_owner
--

ALTER TABLE ONLY public.blog_comments
    ADD CONSTRAINT blog_comments_article_id_fkey FOREIGN KEY (article_id) REFERENCES public.blog_articles(id);


--
-- Name: blog_comments blog_comments_parent_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: neondb_owner
--

ALTER TABLE ONLY public.blog_comments
    ADD CONSTRAINT blog_comments_parent_id_fkey FOREIGN KEY (parent_id) REFERENCES public.blog_comments(id);


--
-- Name: blog_comments blog_comments_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: neondb_owner
--

ALTER TABLE ONLY public.blog_comments
    ADD CONSTRAINT blog_comments_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(id);


--
-- Name: blog_posts blog_posts_author_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: neondb_owner
--

ALTER TABLE ONLY public.blog_posts
    ADD CONSTRAINT blog_posts_author_id_fkey FOREIGN KEY (author_id) REFERENCES public.admins(id);


--
-- Name: callback_requests callback_requests_assigned_manager_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: neondb_owner
--

ALTER TABLE ONLY public.callback_requests
    ADD CONSTRAINT callback_requests_assigned_manager_id_fkey FOREIGN KEY (assigned_manager_id) REFERENCES public.managers(id);


--
-- Name: cashback_applications cashback_applications_approved_by_manager_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: neondb_owner
--

ALTER TABLE ONLY public.cashback_applications
    ADD CONSTRAINT cashback_applications_approved_by_manager_id_fkey FOREIGN KEY (approved_by_manager_id) REFERENCES public.managers(id);


--
-- Name: cashback_applications cashback_applications_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: neondb_owner
--

ALTER TABLE ONLY public.cashback_applications
    ADD CONSTRAINT cashback_applications_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(id);


--
-- Name: cashback_payouts cashback_payouts_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: neondb_owner
--

ALTER TABLE ONLY public.cashback_payouts
    ADD CONSTRAINT cashback_payouts_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(id);


--
-- Name: cashback_records cashback_records_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: neondb_owner
--

ALTER TABLE ONLY public.cashback_records
    ADD CONSTRAINT cashback_records_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(id);


--
-- Name: client_property_recommendations client_property_recommendations_client_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: neondb_owner
--

ALTER TABLE ONLY public.client_property_recommendations
    ADD CONSTRAINT client_property_recommendations_client_id_fkey FOREIGN KEY (client_id) REFERENCES public.users(id);


--
-- Name: client_property_recommendations client_property_recommendations_manager_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: neondb_owner
--

ALTER TABLE ONLY public.client_property_recommendations
    ADD CONSTRAINT client_property_recommendations_manager_id_fkey FOREIGN KEY (manager_id) REFERENCES public.users(id);


--
-- Name: client_property_recommendations client_property_recommendations_search_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: neondb_owner
--

ALTER TABLE ONLY public.client_property_recommendations
    ADD CONSTRAINT client_property_recommendations_search_id_fkey FOREIGN KEY (search_id) REFERENCES public.saved_searches(id);


--
-- Name: collection_properties collection_properties_collection_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: neondb_owner
--

ALTER TABLE ONLY public.collection_properties
    ADD CONSTRAINT collection_properties_collection_id_fkey FOREIGN KEY (collection_id) REFERENCES public.collections(id);


--
-- Name: collections collections_assigned_to_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: neondb_owner
--

ALTER TABLE ONLY public.collections
    ADD CONSTRAINT collections_assigned_to_user_id_fkey FOREIGN KEY (assigned_to_user_id) REFERENCES public.users(id);


--
-- Name: collections collections_created_by_manager_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: neondb_owner
--

ALTER TABLE ONLY public.collections
    ADD CONSTRAINT collections_created_by_manager_id_fkey FOREIGN KEY (created_by_manager_id) REFERENCES public.managers(id);


--
-- Name: developer_appointments developer_appointments_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: neondb_owner
--

ALTER TABLE ONLY public.developer_appointments
    ADD CONSTRAINT developer_appointments_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(id);


--
-- Name: documents documents_reviewed_by_manager_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: neondb_owner
--

ALTER TABLE ONLY public.documents
    ADD CONSTRAINT documents_reviewed_by_manager_id_fkey FOREIGN KEY (reviewed_by_manager_id) REFERENCES public.managers(id);


--
-- Name: documents documents_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: neondb_owner
--

ALTER TABLE ONLY public.documents
    ADD CONSTRAINT documents_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(id);


--
-- Name: favorite_properties favorite_properties_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: neondb_owner
--

ALTER TABLE ONLY public.favorite_properties
    ADD CONSTRAINT favorite_properties_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(id);


--
-- Name: favorites favorites_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: neondb_owner
--

ALTER TABLE ONLY public.favorites
    ADD CONSTRAINT favorites_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(id);


--
-- Name: manager_saved_searches manager_saved_searches_manager_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: neondb_owner
--

ALTER TABLE ONLY public.manager_saved_searches
    ADD CONSTRAINT manager_saved_searches_manager_id_fkey FOREIGN KEY (manager_id) REFERENCES public.managers(id);


--
-- Name: notifications notifications_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: neondb_owner
--

ALTER TABLE ONLY public.notifications
    ADD CONSTRAINT notifications_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(id);


--
-- Name: recommendation_categories recommendation_categories_client_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: neondb_owner
--

ALTER TABLE ONLY public.recommendation_categories
    ADD CONSTRAINT recommendation_categories_client_id_fkey FOREIGN KEY (client_id) REFERENCES public.users(id);


--
-- Name: recommendation_categories recommendation_categories_manager_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: neondb_owner
--

ALTER TABLE ONLY public.recommendation_categories
    ADD CONSTRAINT recommendation_categories_manager_id_fkey FOREIGN KEY (manager_id) REFERENCES public.managers(id);


--
-- Name: recommendation_templates recommendation_templates_manager_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: neondb_owner
--

ALTER TABLE ONLY public.recommendation_templates
    ADD CONSTRAINT recommendation_templates_manager_id_fkey FOREIGN KEY (manager_id) REFERENCES public.managers(id);


--
-- Name: recommendations recommendations_category_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: neondb_owner
--

ALTER TABLE ONLY public.recommendations
    ADD CONSTRAINT recommendations_category_id_fkey FOREIGN KEY (category_id) REFERENCES public.recommendation_categories(id);


--
-- Name: recommendations recommendations_client_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: neondb_owner
--

ALTER TABLE ONLY public.recommendations
    ADD CONSTRAINT recommendations_client_id_fkey FOREIGN KEY (client_id) REFERENCES public.users(id);


--
-- Name: recommendations recommendations_manager_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: neondb_owner
--

ALTER TABLE ONLY public.recommendations
    ADD CONSTRAINT recommendations_manager_id_fkey FOREIGN KEY (manager_id) REFERENCES public.managers(id);


--
-- Name: residential_complexes residential_complexes_developer_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: neondb_owner
--

ALTER TABLE ONLY public.residential_complexes
    ADD CONSTRAINT residential_complexes_developer_id_fkey FOREIGN KEY (developer_id) REFERENCES public.developers(id);


--
-- Name: residential_complexes residential_complexes_district_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: neondb_owner
--

ALTER TABLE ONLY public.residential_complexes
    ADD CONSTRAINT residential_complexes_district_id_fkey FOREIGN KEY (district_id) REFERENCES public.districts(id);


--
-- Name: saved_searches saved_searches_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: neondb_owner
--

ALTER TABLE ONLY public.saved_searches
    ADD CONSTRAINT saved_searches_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(id);


--
-- Name: sent_searches sent_searches_client_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: neondb_owner
--

ALTER TABLE ONLY public.sent_searches
    ADD CONSTRAINT sent_searches_client_id_fkey FOREIGN KEY (client_id) REFERENCES public.users(id);


--
-- Name: sent_searches sent_searches_manager_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: neondb_owner
--

ALTER TABLE ONLY public.sent_searches
    ADD CONSTRAINT sent_searches_manager_id_fkey FOREIGN KEY (manager_id) REFERENCES public.managers(id);


--
-- Name: sent_searches sent_searches_manager_search_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: neondb_owner
--

ALTER TABLE ONLY public.sent_searches
    ADD CONSTRAINT sent_searches_manager_search_id_fkey FOREIGN KEY (manager_search_id) REFERENCES public.manager_saved_searches(id);


--
-- Name: streets streets_district_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: neondb_owner
--

ALTER TABLE ONLY public.streets
    ADD CONSTRAINT streets_district_id_fkey FOREIGN KEY (district_id) REFERENCES public.districts(id);


--
-- Name: user_notifications user_notifications_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: neondb_owner
--

ALTER TABLE ONLY public.user_notifications
    ADD CONSTRAINT user_notifications_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(id);


--
-- Name: users users_assigned_manager_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: neondb_owner
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_assigned_manager_id_fkey FOREIGN KEY (assigned_manager_id) REFERENCES public.managers(id);


--
-- Name: DEFAULT PRIVILEGES FOR SEQUENCES; Type: DEFAULT ACL; Schema: public; Owner: cloud_admin
--

ALTER DEFAULT PRIVILEGES FOR ROLE cloud_admin IN SCHEMA public GRANT ALL ON SEQUENCES TO neon_superuser WITH GRANT OPTION;


--
-- Name: DEFAULT PRIVILEGES FOR TABLES; Type: DEFAULT ACL; Schema: public; Owner: cloud_admin
--

ALTER DEFAULT PRIVILEGES FOR ROLE cloud_admin IN SCHEMA public GRANT SELECT,INSERT,REFERENCES,DELETE,TRIGGER,TRUNCATE,UPDATE ON TABLES TO neon_superuser WITH GRANT OPTION;


--
-- PostgreSQL database dump complete
--

