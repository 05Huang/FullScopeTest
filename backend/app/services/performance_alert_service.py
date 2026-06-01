"""Performance Alert Service"""

from ..core.logging import get_logger
from ..extensions import db

logger = get_logger(__name__)


# 指标名称到字段的映射
METRIC_FIELD_MAP = {
    "p95_response_time": "p95_response_time",
    "p99_response_time": "p99_response_time",
    "error_rate": "error_rate",
    "rps": "rps",
    "avg_response_time": "avg_response_time",
    "min_response_time": "min_response_time",
    "max_response_time": "max_response_time",
}


class PerformanceAlertService:
    """性能告警服务"""

    def evaluate_rules(self, test_result_id: int):
        """评估所有启用的告警规则，触发符合条件的告警"""
        from ..models.perf_test_result import PerformanceTestResult
        from ..models.perf_test_alert import PerformanceAlertRule, PerformanceAlertLog

        test_result = PerformanceTestResult.query.get(test_result_id)
        if not test_result:
            logger.warning("评估告警规则失败：测试结果不存在", test_result_id=test_result_id)
            return []

        rules = PerformanceAlertRule.query.filter_by(enabled=True).all()
        triggered_alerts = []

        for rule in rules:
            try:
                alerts = self._evaluate_single_rule(rule, test_result)
                triggered_alerts.extend(alerts)
            except Exception as e:
                logger.error("评估告警规则失败", rule_id=rule.id, rule_name=rule.name, error=str(e))

        return triggered_alerts

    def _evaluate_single_rule(self, rule, test_result):
        """评估单个告警规则，返回触发的告警列表"""
        from ..models.perf_test_alert import PerformanceAlertLog

        if rule.scenario_id and rule.scenario_id != test_result.scenario_id:
            return []

        alerts = []

        # 绝对值告警检查
        absolute_checks = [
            ("p95_response_time", rule.p95_threshold, ">"),
            ("p99_response_time", rule.p99_threshold, ">"),
            ("error_rate", rule.error_rate_threshold, ">"),
            ("rps", rule.rps_min_threshold, "<"),
        ]

        for metric_name, threshold, operator in absolute_checks:
            if threshold is None:
                continue
            metric_field = METRIC_FIELD_MAP.get(metric_name)
            if not metric_field:
                continue
            current_value = getattr(test_result, metric_field, None)
            if current_value is None:
                continue

            triggered = False
            if operator == ">":
                triggered = current_value > threshold
            elif operator == "<":
                triggered = current_value < threshold

            if triggered:
                alert_log = PerformanceAlertLog(
                    rule_id=rule.id,
                    result_id=test_result.id,
                    alert_type="absolute",
                    metric_name=metric_name,
                    threshold_value=threshold,
                    actual_value=current_value,
                    message=f"[{rule.name}] {metric_name} ({current_value}) {operator} {threshold}",
                    notification_sent=False,
                )
                db.session.add(alert_log)
                alerts.append(alert_log)

        # 相对劣化告警检查
        relative_checks = [
            ("p95_response_time", rule.relative_p95_degradation),
            ("rps", rule.relative_rps_degradation),
            ("error_rate", rule.relative_error_rate_degradation),
        ]

        previous_result = self._get_previous_result(test_result.scenario_id, test_result.id)
        if previous_result:
            for metric_name, degradation_threshold in relative_checks:
                if degradation_threshold is None:
                    continue
                metric_field = METRIC_FIELD_MAP.get(metric_name)
                if not metric_field:
                    continue
                current_value = getattr(test_result, metric_field, None)
                previous_value = getattr(previous_result, metric_field, None)
                if current_value is None or previous_value is None or previous_value == 0:
                    continue

                degradation_pct = ((current_value - previous_value) / previous_value) * 100
                if degradation_pct > degradation_threshold:
                    alert_log = PerformanceAlertLog(
                        rule_id=rule.id,
                        result_id=test_result.id,
                        alert_type="relative",
                        metric_name=metric_name,
                        threshold_value=degradation_threshold,
                        actual_value=round(degradation_pct, 2),
                        message=f"[{rule.name}] {metric_name} 劣化 {degradation_pct:.1f}% (当前: {current_value}, 上次: {previous_value})",
                        notification_sent=False,
                    )
                    db.session.add(alert_log)
                    alerts.append(alert_log)

        if alerts:
            db.session.flush()

            # 更新规则统计
            rule.last_triggered_at = db.func.now()
            rule.trigger_count = (rule.trigger_count or 0) + len(alerts)

            # 发送通知
            if rule.notify_webhook:
                for alert_log in alerts:
                    try:
                        self._send_webhook_notification(alert_log, rule.notify_webhook)
                        alert_log.notification_sent = True
                    except Exception as e:
                        alert_log.notification_error = str(e)

            db.session.commit()

        return [
            {
                "id": a.id,
                "rule_id": rule.id,
                "rule_name": rule.name,
                "metric": a.metric_name,
                "alert_type": a.alert_type,
                "current_value": a.actual_value,
                "threshold_value": a.threshold_value,
                "message": a.message,
            }
            for a in alerts
        ]

    def _get_previous_result(self, scenario_id, current_result_id):
        """获取上一次测试运行的结果"""
        from ..models.perf_test_result import PerformanceTestResult
        return PerformanceTestResult.query.filter(
            PerformanceTestResult.scenario_id == scenario_id,
            PerformanceTestResult.id != current_result_id,
            PerformanceTestResult.status == "completed",
        ).order_by(PerformanceTestResult.created_at.desc()).first()

    def _send_webhook_notification(self, alert_log, webhook_url):
        """发送 Webhook 通知"""
        import requests
        payload = {
            "msgtype": "markdown",
            "markdown": {
                "title": f"性能测试告警",
                "text": (
                    f"**告警规则**: {alert_log.rule.name}\n"
                    f"**指标**: {alert_log.metric_name}\n"
                    f"**当前值**: {alert_log.actual_value}\n"
                    f"**阈值**: {alert_log.threshold_value}\n"
                    f"**类型**: {alert_log.alert_type}\n"
                    f"**消息**: {alert_log.message}"
                ),
            },
        }
        response = requests.post(webhook_url, json=payload, timeout=10)
        response.raise_for_status()
        logger.info("告警通知已发送", webhook=webhook_url)


alert_service = PerformanceAlertService()
