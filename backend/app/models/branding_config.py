"""
品牌配置模型

支持企业客户自定义品牌外观：
- 平台名称
- Logo URL
- Favicon URL
- 主色调
- 登录页背景图
- Footer 文案
"""
from datetime import datetime
from ..extensions import db


class BrandingConfig(db.Model):
    """品牌配置表"""
    __tablename__ = 'branding_configs'

    id = db.Column(db.Integer, primary_key=True)
    organization_id = db.Column(db.Integer, db.ForeignKey('organizations.id'), nullable=True, comment='组织 ID（NULL 为全局默认）')
    platform_name = db.Column(db.String(100), default='FullScopeTest', comment='平台名称')
    logo_url = db.Column(db.String(500), comment='Logo URL')
    favicon_url = db.Column(db.String(500), comment='Favicon URL')
    primary_color = db.Column(db.String(20), default='#5FA59B', comment='主色调')
    login_background_url = db.Column(db.String(500), comment='登录页背景图 URL')
    footer_text = db.Column(db.String(200), comment='Footer 文案')
    custom_css = db.Column(db.Text, comment='自定义 CSS')

    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # 关联
    organization = db.relationship('Organization', backref='branding_config')

    def to_dict(self):
        return {
            'id': self.id,
            'organization_id': self.organization_id,
            'platform_name': self.platform_name,
            'logo_url': self.logo_url,
            'favicon_url': self.favicon_url,
            'primary_color': self.primary_color,
            'login_background_url': self.login_background_url,
            'footer_text': self.footer_text,
            'custom_css': self.custom_css,
        }
