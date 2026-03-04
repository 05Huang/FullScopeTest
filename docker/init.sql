-- FullScopeTest 数据库初始化脚本

-- 创建开发数据库
SELECT 'CREATE DATABASE fullscopetest_dev'
WHERE NOT EXISTS (SELECT FROM pg_database WHERE datname = 'fullscopetest_dev')\gexec

-- 创建测试数据库
SELECT 'CREATE DATABASE fullscopetest_test'
WHERE NOT EXISTS (SELECT FROM pg_database WHERE datname = 'fullscopetest_test')\gexec

-- 授权
GRANT ALL PRIVILEGES ON DATABASE fullscopetest_dev TO fullscopetest;
GRANT ALL PRIVILEGES ON DATABASE fullscopetest_test TO fullscopetest;
