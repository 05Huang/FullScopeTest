"""输入验证模块测试"""

import pytest
from app.utils.input_validation import (
    sanitize_html,
    validate_string_length,
    validate_email,
    validate_url,
    sanitize_script_content,
    detect_script_danger,
)


class TestSanitizeHtml:
    def test_escape_basic_tags(self):
        assert sanitize_html('<script>alert(1)</script>') == '&lt;script&gt;alert(1)&lt;/script&gt;'
        assert sanitize_html('<img src="x">') == '&lt;img src=&quot;x&quot;&gt;'

    def test_escape_ampersand(self):
        assert sanitize_html('a & b') == 'a &amp; b'

    def test_empty_input(self):
        assert sanitize_html('') == ''
        assert sanitize_html(None) is None


class TestValidateStringLength:
    def test_valid_string(self):
        assert validate_string_length('hello', min_len=1, max_len=10) is None

    def test_too_short(self):
        result = validate_string_length('hi', min_len=5, field_name='name')
        assert '至少' in result

    def test_too_long(self):
        result = validate_string_length('a' * 100, max_len=50, field_name='name')
        assert '不能超过' in result

    def test_none_with_min_one(self):
        assert validate_string_length(None, min_len=1) == 'input 不能为空'

    def test_none_with_min_zero(self):
        assert validate_string_length(None, min_len=0) is None


class TestValidateEmail:
    def test_valid_emails(self):
        assert validate_email('user@example.com') is True
        assert validate_email('test.user@domain.co.uk') is True

    def test_invalid_emails(self):
        assert validate_email('not-an-email') is False
        assert validate_email('@domain.com') is False
        assert validate_email('user@') is False


class TestSanitizeScript:
    def test_block_subprocess(self):
        result = sanitize_script_content('import subprocess')
        assert 'BLOCKED' in result

    def test_block_exec(self):
        result = sanitize_script_content('exec(code)')
        assert 'BLOCKED' in result

    def test_block_eval(self):
        result = sanitize_script_content('eval(user_input)')
        assert 'BLOCKED' in result

    def test_clean_shebang(self):
        result = sanitize_script_content('#!/usr/bin/env python\nprint("hello")')
        assert result == 'print("hello")'

    def test_empty_content(self):
        assert sanitize_script_content('') == ''
        assert sanitize_script_content(None) is None


class TestDetectDanger:
    def test_no_threats(self):
        threats = detect_script_danger('print("hello")')
        assert len(threats) == 0

    def test_detect_subprocess(self):
        threats = detect_script_danger('import subprocess')
        assert len(threats) == 1
        assert threats[0]['count'] == 1

    def test_multiple_threats(self):
        threats = detect_script_danger('import subprocess\nos.system("ls")')
        assert len(threats) >= 2
