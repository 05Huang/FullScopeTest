"""
AI 测试数据工厂服务
"""

import random
import time
from typing import Dict, Any, List
from ...core.logging import get_logger

logger = get_logger(__name__)

BUILTIN_TEMPLATES = {
    "user": {
        "name": "用户数据",
        "fields": {
            "username": {"type": "string", "pattern": "user_{random_int}"},
            "email": {"type": "string", "pattern": "user_{random_int}@test.com"},
            "phone": {"type": "string", "pattern": "138{random_int_8}"},
            "age": {"type": "integer", "min": 18, "max": 65},
            "status": {"type": "enum", "values": ["active", "inactive", "pending"]},
        },
    },
    "order": {
        "name": "订单数据",
        "fields": {
            "order_no": {"type": "string", "pattern": "ORD{timestamp}"},
            "amount": {"type": "float", "min": 10.0, "max": 10000.0},
            "status": {"type": "enum", "values": ["pending", "paid", "completed"]},
        },
    },
    "product": {
        "name": "商品数据",
        "fields": {
            "name": {"type": "string", "pattern": "商品_{random_int}"},
            "price": {"type": "float", "min": 1.0, "max": 9999.0},
            "stock": {"type": "integer", "min": 0, "max": 1000},
        },
    },
}


class DataFactoryService:
    """测试数据工厂服务"""

    def __init__(self):
        self._generated = {}
        self._id_counter = {}

    def get_templates(self):
        return [{"name": k, "display_name": v["name"], "fields": list(v["fields"].keys())}
                for k, v in BUILTIN_TEMPLATES.items()]

    def generate(self, template_name, count=1, custom_rules=None, seed=None):
        template = BUILTIN_TEMPLATES.get(template_name)
        if not template:
            raise ValueError(f"模板 {template_name} 不存在")
        if count < 1 or count > 10000:
            raise ValueError("生成数量必须在 1-10000 之间")
        if seed is not None:
            random.seed(seed)

        data = []
        for i in range(count):
            item = self._generate_one(template, template_name, custom_rules)
            data.append(item)

        if template_name not in self._generated:
            self._generated[template_name] = []
        self._generated[template_name].extend(data)

        logger.info("测试数据生成完成", template=template_name, count=count)
        return {"template": template_name, "count": count, "data": data}

    def cleanup(self, template_name=None):
        if template_name:
            count = len(self._generated.get(template_name, []))
            self._generated.pop(template_name, None)
            self._id_counter.pop(template_name, None)
        else:
            count = sum(len(v) for v in self._generated.values())
            self._generated.clear()
            self._id_counter.clear()
        logger.info("测试数据已清理", template=template_name, count=count)
        return {"cleaned": count}

    def _generate_one(self, template, template_name, custom_rules=None):
        item = {}
        timestamp = int(time.time() * 1000)
        random_int = random.randint(10000, 99999)
        random_int_8 = str(random.randint(10000000, 99999999))

        if template_name not in self._id_counter:
            self._id_counter[template_name] = 0
        self._id_counter[template_name] += 1
        item_id = self._id_counter[template_name]

        for field_name, field_def in template["fields"].items():
            if custom_rules and field_name in custom_rules:
                rule = custom_rules[field_name]
                # 如果是字典规则（如 {"min": 20, "max": 30}），生成随机值
                if isinstance(rule, dict) and "min" in rule and "max" in rule:
                    if field_def.get("type") == "integer":
                        item[field_name] = random.randint(rule["min"], rule["max"])
                    elif field_def.get("type") == "float":
                        item[field_name] = round(random.uniform(rule["min"], rule["max"]), 2)
                    else:
                        item[field_name] = rule
                else:
                    item[field_name] = rule
                continue

            field_type = field_def.get("type", "string")
            if field_type == "string":
                pattern = field_def.get("pattern", "")
                value = pattern.replace("{random_int}", str(random_int))
                value = value.replace("{random_int_8}", random_int_8)
                value = value.replace("{timestamp}", str(timestamp))
                item[field_name] = value
            elif field_type == "integer":
                item[field_name] = random.randint(field_def.get("min", 0), field_def.get("max", 100))
            elif field_type == "float":
                item[field_name] = round(random.uniform(field_def.get("min", 0), field_def.get("max", 100)), 2)
            elif field_type == "enum":
                item[field_name] = random.choice(field_def.get("values", ["default"]))

        item["id"] = item_id
        return item


_instance = None

def get_data_factory_service():
    global _instance
    if _instance is None:
        _instance = DataFactoryService()
    return _instance
