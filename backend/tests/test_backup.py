"""
数据备份策略测试

覆盖：备份脚本结构验证、备份目录创建、文档完整性
"""
import os
import stat


# ══════════════════════════════════════════════════════════════════════════════
# 一、备份脚本结构测试
# ══════════════════════════════════════════════════════════════════════════════

class TestBackupScript:
    """备份脚本结构验证"""

    def test_backup_script_exists(self):
        script_path = os.path.join(os.path.dirname(__file__), '..', '..', 'scripts', 'backup.sh')
        assert os.path.exists(script_path), "backup.sh 不存在"

    def test_backup_script_is_executable(self):
        script_path = os.path.join(os.path.dirname(__file__), '..', '..', 'scripts', 'backup.sh')
        st = os.stat(script_path)
        # Windows 不支持 Unix 权限位，跳过执行权限检查
        if os.name != 'nt':
            assert st.st_mode & stat.S_IXUSR, "backup.sh 应该有执行权限"

    def test_backup_script_has_shebang(self):
        script_path = os.path.join(os.path.dirname(__file__), '..', '..', 'scripts', 'backup.sh')
        with open(script_path, 'r', encoding='utf-8') as f:
            first_line = f.readline().strip()
        assert first_line.startswith('#!'), "脚本应有 shebang 行"

    def test_backup_script_has_postgres_function(self):
        script_path = os.path.join(os.path.dirname(__file__), '..', '..', 'scripts', 'backup.sh')
        with open(script_path, 'r', encoding='utf-8') as f:
            content = f.read()
        assert 'backup_postgres()' in content
        assert 'pg_dump' in content

    def test_backup_script_has_redis_function(self):
        script_path = os.path.join(os.path.dirname(__file__), '..', '..', 'scripts', 'backup.sh')
        with open(script_path, 'r', encoding='utf-8') as f:
            content = f.read()
        assert 'backup_redis()' in content
        assert 'BGSAVE' in content or 'redis' in content.lower()

    def test_backup_script_has_file_backup(self):
        script_path = os.path.join(os.path.dirname(__file__), '..', '..', 'scripts', 'backup.sh')
        with open(script_path, 'r', encoding='utf-8') as f:
            content = f.read()
        assert 'backup_files()' in content
        assert 'uploads' in content
        assert 'reports' in content

    def test_backup_script_has_cleanup(self):
        script_path = os.path.join(os.path.dirname(__file__), '..', '..', 'scripts', 'backup.sh')
        with open(script_path, 'r', encoding='utf-8') as f:
            content = f.read()
        assert 'cleanup_old_backups' in content
        assert 'BACKUP_RETENTION' in content

    def test_backup_script_has_restore(self):
        script_path = os.path.join(os.path.dirname(__file__), '..', '..', 'scripts', 'backup.sh')
        with open(script_path, 'r', encoding='utf-8') as f:
            content = f.read()
        assert '--restore' in content
        assert 'restore_latest' in content or 'restore' in content.lower()

    def test_backup_script_has_date_naming(self):
        script_path = os.path.join(os.path.dirname(__file__), '..', '..', 'scripts', 'backup.sh')
        with open(script_path, 'r', encoding='utf-8') as f:
            content = f.read()
        assert 'DATE' in content
        assert '%Y%m%d' in content

    def test_backup_script_has_gzip_compression(self):
        script_path = os.path.join(os.path.dirname(__file__), '..', '..', 'scripts', 'backup.sh')
        with open(script_path, 'r', encoding='utf-8') as f:
            content = f.read()
        assert 'gzip' in content


# ══════════════════════════════════════════════════════════════════════════════
# 二、备份文档测试
# ══════════════════════════════════════════════════════════════════════════════

class TestBackupDocs:
    """备份文档完整性测试"""

    def test_backup_doc_exists(self):
        doc_path = os.path.join(os.path.dirname(__file__), '..', '..', 'docs', 'BACKUP.md')
        assert os.path.exists(doc_path), "BACKUP.md 不存在"

    def test_backup_doc_has_quick_start(self):
        doc_path = os.path.join(os.path.dirname(__file__), '..', '..', 'docs', 'BACKUP.md')
        with open(doc_path, 'r', encoding='utf-8') as f:
            content = f.read()
        assert '快速开始' in content

    def test_backup_doc_has_restore_section(self):
        doc_path = os.path.join(os.path.dirname(__file__), '..', '..', 'docs', 'BACKUP.md')
        with open(doc_path, 'r', encoding='utf-8') as f:
            content = f.read()
        assert '恢复' in content

    def test_backup_doc_has_env_vars(self):
        doc_path = os.path.join(os.path.dirname(__file__), '..', '..', 'docs', 'BACKUP.md')
        with open(doc_path, 'r', encoding='utf-8') as f:
            content = f.read()
        assert 'BACKUP_DIR' in content
        assert 'BACKUP_RETENTION' in content
        assert 'DATABASE_URL' in content

    def test_backup_doc_has_cron_example(self):
        doc_path = os.path.join(os.path.dirname(__file__), '..', '..', 'docs', 'BACKUP.md')
        with open(doc_path, 'r', encoding='utf-8') as f:
            content = f.read()
        assert 'cron' in content.lower() or 'crontab' in content.lower()

    def test_backup_doc_has_docker_compose(self):
        doc_path = os.path.join(os.path.dirname(__file__), '..', '..', 'docs', 'BACKUP.md')
        with open(doc_path, 'r', encoding='utf-8') as f:
            content = f.read()
        assert 'docker-compose' in content.lower() or 'docker compose' in content.lower()


# ══════════════════════════════════════════════════════════════════════════════
# 三、备份目录测试
# ══════════════════════════════════════════════════════════════════════════════

class TestBackupDirectory:
    """备份目录测试"""

    def test_scripts_directory_exists(self):
        scripts_dir = os.path.join(os.path.dirname(__file__), '..', '..', 'scripts')
        assert os.path.isdir(scripts_dir), "scripts/ 目录不存在"

    def test_docs_directory_exists(self):
        docs_dir = os.path.join(os.path.dirname(__file__), '..', '..', 'docs')
        assert os.path.isdir(docs_dir), "docs/ 目录不存在"