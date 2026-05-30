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

# 运算符映射
OPERATOR_MAP = {
    ">": lambda a, b: a > b,
    "<": lambda a, b: a < b,
    ">=": lambda a, b: a >= b,
    "<=": lambda a, b: a <= b,
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

        rules = PerformanceAlertRule.query.filter_by(is_enabled=True).all()
        triggered_alerts = []

        for rule in rules:
            try:
                alert = self._evaluate_single_rule(rule, test_result)
                if alert:
                    triggered_alerts.append(alert)
            except Exception as e:
                logger.error("评估告警规则失败", rule_id=rule.id, rule_name=rule.name, error=str(e))

        return triggered_alerts

    def _evaluate_single_rule(self, rule, test_result):
        """评估单个告警规则"""
        from ..models.perf_test_alert import PerformanceAlertLog

        if rule.scenario_id and rule.scenario_id != test_result.scenario_id:
            return None

        triggered = False
        current_value = None
        threshold_value = None
        message = ""
        severity = "warning"

        if rule.condition_type == "absolute":
            metric_field = METRIC_FIELD_MAP.get(rule.metric_name)
            if not metric_field:
                return None
            current_value = getattr(test_result, metric_field, None)
            if current_value is None:
                return None
            threshold_value = rule.threshold_value
            operator_func = OPERATOR_MAP.get(rule.operator)
            if not operator_func:
                return None
            triggered = operator_func(current_value, threshold_value)
            message = f"{rule.metric_name} ({current_value}) {rule.operator} {threshold_value}"

        elif rule.condition_type == "relative":
            metric_field = METRIC_FIELD_MAP.get(rule.relative_metric)
            if not metric_field:
                return None
            current_value = getattr(test_result, metric_field, None)
            if current_value is None:
                return None
            previous_result = self._get_previous_result(test_result.scenario_id, test_result.id)
            if not previous_result:
                return None
            previous_value = getattr(previous_result, metric_field, None)
            if previous_value is None or previous_value == 0:
                return None
            degradation_pct = ((current_value - previous_value) / previous_value) * 100
            threshold_value = rule.degradation_percentage
            triggered = degradation_pct > threshold_value
            message = f"{rule.relative_metric} 劣化 {degradation_pct:.1f}% (当前: {current_value}, 上次: {previous_value})"
            current_value = degradation_pct

        if not triggered:
            return None

        if rule.condition_type == "absolute" and rule.metric_name in ("p99_response_time", "error_rate"):
            severity = "critical"
        elif rule.condition_type == "relative" and rule.degradation_percentage and rule.degradation_percentage > 50:
            severity = "critical"

        alert_log = PerformanceAlertLog(
            rule_id=rule.id,
            test_result_id=test_result.id,
            metric_name=rule.metric_name or rule.relative_metric,
            current_value=current_value,
            threshold_value=threshold_value,
            message=f"[{rule.name}] {message}",
            severity=severity,
            notification_sent=False,
        )
        db.session.add(alert_log)
        db.session.flush()

        if rule.notify_webhook:
            try:
                self._send_webhook_notification(alert_log, rule.notify_webhook)
                alert_log.notification_sent = True
            except Exception as e:
                alert_log.notification_error = str(e)

        db.session.commit()

        return {
            "id": alert_log.id,
            "rule_id": rule.id,
            "rule_name": rule.name,
            "metric": rule.metric_name or rule.relative_metric,
            "current_value": current_value,
            "threshold_value": threshold_value,
            "message": alert_log.message,
            "severity": severity,
            "notification_sent": alert_log.notification_sent,
        }

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
                "title": f"性能测试告警 - {alert_log.severity.upper()}",
                "text": (
                    f"**告警规则**: {alert_log.rule.name}\n"
                    f"**指标**: {alert_log.metric_name}\n"
                    f"**当前值**: {alert_log.current_value}\n"
                    f"**阈值**: {alert_log.threshold_value}\n"
                    f"**严重程度**: {alert_log.severity}\n"
                    f"**消息**: {alert_log.message}"
                ),
            },
        }
        response = requests.post(webhook_url, json=payload, timeout=10)
        response.raise_for_status()
        logger.info("告警通知已发送", webhook=webhook_url, severity=alert_log.severity)


alert_service = PerformanceAlertService()
