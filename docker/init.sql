-- EasyTest 数据库初始化脚本

-- 创建开发数据库
SELECT 'CREATE DATABASE easytest_dev'
WHERE NOT EXISTS (SELECT FROM pg_database WHERE datname = 'easytest_dev')\gexec

-- 创建测试数据库
SELECT 'CREATE DATABASE easytest_test'
WHERE NOT EXISTS (SELECT FROM pg_database WHERE datname = 'easytest_test')\gexec

-- 授权
GRANT ALL PRIVILEGES ON DATABASE easytest_dev TO easytest;
GRANT ALL PRIVILEGES ON DATABASE easytest_test TO easytest;
