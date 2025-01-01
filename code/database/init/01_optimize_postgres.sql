-- ========================================
-- PAQUETES EL CLUB v3.1 - Optimizaciones PostgreSQL para 1GB RAM
-- ========================================

-- Configuraciones de memoria optimizadas para 1GB RAM
ALTER SYSTEM SET shared_buffers = '128MB';
ALTER SYSTEM SET effective_cache_size = '256MB';
ALTER SYSTEM SET work_mem = '4MB';
ALTER SYSTEM SET maintenance_work_mem = '32MB';
ALTER SYSTEM SET max_connections = 50;

-- Configuraciones de WAL optimizadas
ALTER SYSTEM SET wal_buffers = '4MB';
ALTER SYSTEM SET checkpoint_completion_target = 0.9;
ALTER SYSTEM SET checkpoint_timeout = '15min';
ALTER SYSTEM SET max_wal_size = '1GB';
ALTER SYSTEM SET min_wal_size = '80MB';

-- Configuraciones de consultas optimizadas
ALTER SYSTEM SET default_statistics_target = 100;
ALTER SYSTEM SET random_page_cost = 1.1;
ALTER SYSTEM SET effective_io_concurrency = 200;

-- Configuraciones de logging optimizadas
ALTER SYSTEM SET log_min_duration_statement = 1000;
ALTER SYSTEM SET log_checkpoints = on;
ALTER SYSTEM SET log_connections = off;
ALTER SYSTEM SET log_disconnections = off;
ALTER SYSTEM SET log_lock_waits = on;
ALTER SYSTEM SET log_temp_files = 0;

-- Configuraciones de autovacuum optimizadas
ALTER SYSTEM SET autovacuum = on;
ALTER SYSTEM SET autovacuum_max_workers = 2;
ALTER SYSTEM SET autovacuum_naptime = '1min';
ALTER SYSTEM SET autovacuum_vacuum_threshold = 50;
ALTER SYSTEM SET autovacuum_analyze_threshold = 50;

-- Recargar configuración
SELECT pg_reload_conf();

-- Crear índices optimizados para las tablas principales
CREATE INDEX IF NOT EXISTS idx_packages_tracking_number ON packages(tracking_number);
CREATE INDEX IF NOT EXISTS idx_packages_status ON packages(status);
CREATE INDEX IF NOT EXISTS idx_packages_customer_id ON packages(customer_id);
CREATE INDEX IF NOT EXISTS idx_packages_created_at ON packages(created_at);

CREATE INDEX IF NOT EXISTS idx_customers_tracking_number ON customers(tracking_number);
CREATE INDEX IF NOT EXISTS idx_customers_phone ON customers(phone);

CREATE INDEX IF NOT EXISTS idx_users_username ON users(username);
CREATE INDEX IF NOT EXISTS idx_users_email ON users(email);

CREATE INDEX IF NOT EXISTS idx_notifications_package_id ON notifications(package_id);
CREATE INDEX IF NOT EXISTS idx_notifications_status ON notifications(status);

-- Configurar estadísticas
ANALYZE;
