"""
P22 前端体验增强后端服务测试
"""

import pytest


class TestNotificationCenter:
    """通知中心服务测试"""

    def test_send_notification(self, app):
        """发送通知"""
        with app.app_context():
            from app.services.notification_center import NotificationCenter
            center = NotificationCenter()
            notification = center.send(user_id=1, notification_type="test_complete", title="测试完成")
            assert notification.user_id == 1
            assert notification.is_read is False

    def test_get_notifications(self, app):
        """获取通知列表"""
        with app.app_context():
            from app.services.notification_center import NotificationCenter
            center = NotificationCenter()
            center.send(user_id=1, notification_type="test", title="通知1")
            center.send(user_id=1, notification_type="test", title="通知2")
            center.send(user_id=2, notification_type="test", title="其他用户通知")
            notifications = center.get_notifications(user_id=1)
            assert len(notifications) == 2

    def test_unread_count(self, app):
        """未读计数"""
        with app.app_context():
            from app.services.notification_center import NotificationCenter
            center = NotificationCenter()
            center.send(user_id=1, notification_type="test", title="通知1")
            center.send(user_id=1, notification_type="test", title="通知2")
            assert center.get_unread_count(user_id=1) == 2

    def test_mark_read(self, app):
        """标记已读"""
        with app.app_context():
            from app.services.notification_center import NotificationCenter
            center = NotificationCenter()
            n = center.send(user_id=1, notification_type="test", title="通知")
            assert center.get_unread_count(user_id=1) == 1
            center.mark_read(user_id=1, notification_id=n.id)
            assert center.get_unread_count(user_id=1) == 0

    def test_mark_all_read(self, app):
        """全部标记已读"""
        with app.app_context():
            from app.services.notification_center import NotificationCenter
            center = NotificationCenter()
            center.send(user_id=1, notification_type="test", title="通知1")
            center.send(user_id=1, notification_type="test", title="通知2")
            center.send(user_id=1, notification_type="test", title="通知3")
            count = center.mark_all_read(user_id=1)
            assert count == 3
            assert center.get_unread_count(user_id=1) == 0

    def test_notification_types(self, app):
        """不同通知类型"""
        with app.app_context():
            from app.services.notification_center import NotificationCenter
            center = NotificationCenter()
            center.send(user_id=1, notification_type="test_complete", title="测试完成")
            center.send(user_id=1, notification_type="alert", title="告警")
            center.send(user_id=1, notification_type="mention", title="@提及")
            unread = center.get_notifications(user_id=1, unread_only=True)
            assert len(unread) == 3


class TestChartDataService:
    """图表数据服务测试"""

    def test_build_line_chart(self, app):
        """折线图配置"""
        with app.app_context():
            from app.services.chart_data_service import ChartDataService
            svc = ChartDataService()
            config = svc.build_line_chart("趋势图", ["Mon", "Tue", "Wed"], [{"name": "通过率", "data": [90, 85, 95]}])
            assert config["type"] == "line"
            assert config["title"] == "趋势图"
            assert len(config["xAxis"]["data"]) == 3

    def test_build_bar_chart(self, app):
        """柱状图配置"""
        with app.app_context():
            from app.services.chart_data_service import ChartDataService
            svc = ChartDataService()
            config = svc.build_bar_chart("统计图", ["P0", "P1", "P2"], [10, 20, 30])
            assert config["type"] == "bar"
            assert config["series"][0]["data"] == [10, 20, 30]

    def test_build_pie_chart(self, app):
        """饼图配置"""
        with app.app_context():
            from app.services.chart_data_service import ChartDataService
            svc = ChartDataService()
            config = svc.build_pie_chart("分布图", [{"name": "通过", "value": 80}, {"name": "失败", "value": 20}])
            assert config["type"] == "pie"

    def test_build_gauge_chart(self, app):
        """仪表盘配置"""
        with app.app_context():
            from app.services.chart_data_service import ChartDataService
            svc = ChartDataService()
            config = svc.build_gauge_chart("通过率", 95.5)
            assert config["type"] == "gauge"
            assert config["series"][0]["data"][0]["value"] == 95.5

    def test_chart_colors(self, app):
        """配色方案应符合规范"""
        with app.app_context():
            from app.services.chart_data_service import CHART_COLORS
            assert CHART_COLORS["primary"] == "#2D6A64"
            assert len(CHART_COLORS) >= 5


class TestOfflineService:
    """离线支持服务测试"""

    def test_enqueue_request(self, app):
        """入队请求"""
        with app.app_context():
            from app.services.offline_service import OfflineQueue
            queue = OfflineQueue()
            queue.enqueue({"method": "POST", "path": "/api/test", "data": {}})
            assert queue.pending_count == 1

    def test_dequeue_all(self, app):
        """取出所有请求"""
        with app.app_context():
            from app.services.offline_service import OfflineQueue
            queue = OfflineQueue()
            queue.enqueue({"method": "POST", "path": "/a"})
            queue.enqueue({"method": "POST", "path": "/b"})
            requests = queue.dequeue_all()
            assert len(requests) == 2
            assert queue.pending_count == 0

    def test_online_status(self, app):
        """在线状态管理"""
        with app.app_context():
            from app.services.offline_service import OfflineQueue
            queue = OfflineQueue()
            assert queue.is_online is True
            queue.set_online(False)
            assert queue.is_online is False
