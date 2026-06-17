#!/usr/bin/env python3
import sys, os, random, hashlib
from datetime import datetime, timedelta, timezone
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from app import create_app
from app.extensions import db
from app.models.user import User
from app.models.project import Project
from app.models.organization import Organization, OrganizationMember
from app.models.environment import Environment
from app.models.api_test_case import ApiTestCase, ApiTestCollection
from app.models.web_test_collection import WebTestCollection
from app.models.web_test_script import WebTestScript
from app.models.app_test_collection import AppTestCollection
from app.models.app_test_script import AppTestScript
from app.models.perf_test_scenario import PerfTestScenario
from app.models.perf_test_result import PerformanceTestResult, PerformanceMetricSample
from app.models.perf_test_alert import PerformanceAlertRule, PerformanceAlertLog
from app.models.test_run import TestRun
from app.models.test_report import TestReport
from app.models.test_document import TestDocument
from app.models.quality_gate import QualityGate, QualityGateEvaluation
from app.models.scheduled_task import ScheduledTask
from app.models.trigger_rule import TriggerRule
from app.models.audit_log import AuditLog
from app.models.notification_config import NotificationConfig
from app.models.ai_invocation_log import AIInvocationLog
from app.models.prompt_version import PromptVersion
from app.models.api_token import ApiToken
from app.models.test_plan import TestPlan, TestPlanRun
from app.models.issue_link import IssueLink
from app.models.comment import Comment

random.seed(42)
app = create_app("production")

def rp(days=90):
    return datetime.now(timezone.utc) - timedelta(days=random.randint(0,days), hours=random.randint(0,23), minutes=random.randint(0,59))

def seed():
    with app.app_context():
        uc = User.query.count()
        if uc > 5:
            print(f"Users: {uc} (skip)")
            users = User.query.all()
        else:
            users = []
            for u, e, r in [("admin","admin@fullscopetest.com","admin"),("alice","alice@example.com","admin"),("bob","bob@example.com","member"),("charlie","charlie@example.com","member"),("diana","diana@example.com","member"),("eve","eve@example.com","viewer"),("frank","frank@example.com","member"),("grace","grace@example.com","member"),("henry","henry@example.com","viewer"),("iris","iris@example.com","member")]:
                o = User(username=u, email=e, role=r, password_hash=hashlib.sha256(u.encode()).hexdigest(), is_active=True, last_login=rp(7))
                db.session.add(o)
                users.append(o)
            db.session.flush()
            print(f"Created {len(users)} users")
        admin = users[0]

        if Organization.query.count() > 0:
            orgs = Organization.query.all()
        else:
            orgs = []
            for n, s, d in [("FullScope Team","fullscope-team","Core dev team"),("QA Engineering","qa-engineering","QA department"),("Backend Dev","backend-dev","Backend team"),("Infra Team","infra-team","Infrastructure team")]:
                o = Organization(name=n, slug=s, description=d, owner_id=admin.id, is_active=True)
                db.session.add(o)
                orgs.append(o)
            db.session.flush()
            for org in orgs:
                for u in users:
                    db.session.add(OrganizationMember(organization_id=org.id, user_id=u.id, role="owner" if u.id==admin.id else random.choice(["admin","member","viewer"]), invited_by=admin.id, is_active=True))
            db.session.flush()
            print(f"Created {len(orgs)} orgs")

        if Project.query.count() > 3:
            projects = Project.query.all()
        else:
            projects = []
            for i, (n, d) in enumerate([("E-Commerce API","E-commerce core API testing"),("FinTech Trading","High concurrency trading tests"),("Social Network","Social platform API tests"),("IoT Platform","IoT device management tests"),("Healthcare System","Medical system security tests"),("Education Platform","Online education tests"),("Logistics System","Logistics scheduling tests"),("CMS System","Content management tests"),("Payment Gateway","Payment integration tests"),("AI Inference","LLM API performance baseline")]):
                p = Project(name=n, description=d, owner_id=random.choice(users[:3]).id, organization_id=orgs[i%len(orgs)].id, created_at=rp(60))
                db.session.add(p)
                projects.append(p)
            db.session.flush()
            print(f"Created {len(projects)} projects")

        if Environment.query.count() <= 5:
            for proj in projects:
                for en, eu, ed in [("Development","http://dev.example.com",True),("Testing","http://test.example.com",False),("Staging","https://staging.example.com",False),("Production","https://api.example.com",False)]:
                    db.session.add(Environment(project_id=proj.id, name=en, base_url=eu, variables={"API_KEY":"key_"+str(proj.id)}, headers={"Content-Type":"application/json"}, is_default=ed))
            db.session.flush()

        if ApiTestCollection.query.count() <= 5:
            colls = []
            for proj in projects:
                for n, d in [("User Mgmt","User CRUD"),("Product Mgmt","Product CRUD"),("Order System","Order flow"),("Payment","Payment integration"),("Notification","Push notifications"),("File Upload","File handling"),("RBAC","Permission mgmt"),("Reports","Analytics"),("Search","Full-text search"),("Settings","Config mgmt")]:
                    c = ApiTestCollection(project_id=proj.id, user_id=admin.id, name=n, description=d, created_at=rp(45))
                    db.session.add(c)
                    colls.append(c)
            db.session.flush()
            cc = 0
            cases = [("Register","POST","/api/v1/auth/register",["auth"],1),("Login","POST","/api/v1/auth/login",["auth"],1),("Get User","GET","/api/v1/users/me",["user"],1),("Product List","GET","/api/v1/products",["product"],1),("Product Detail","GET","/api/v1/products/1",["product"],2),("Create Order","POST","/api/v1/orders",["order"],1),("Pay Order","POST","/api/v1/orders/1/pay",["payment"],1),("Refund","POST","/api/v1/orders/1/refund",["order"],2),("Send Notify","POST","/api/v1/notifications",["notif"],2),("Search","GET","/api/v1/search",["search"],2),("Roles","GET","/api/v1/roles",["rbac"],2),("Export","GET","/api/v1/reports/export",["report"],3)]
            for coll in colls:
                for j in range(random.randint(5, 15)):
                    cn, cm, cu, ct, cp = random.choice(cases)
                    s = random.choice(["passed","passed","passed","failed","pending"])
                    db.session.add(ApiTestCase(collection_id=coll.id, project_id=coll.project_id, user_id=admin.id, name=cn+(" #"+str(j+1) if j>0 else ""), method=cm, url=cu, headers={"Content-Type":"application/json"}, body_type="json", assertions=[{"type":"status_code","expected":200}], tags=ct, priority=cp, is_enabled=random.random()>0.1, last_status=s if random.random()>0.2 else None, last_run_at=rp(7) if s!="pending" else None, timeout=30, created_at=rp(30)))
                    cc += 1
            db.session.flush()
            print(f"API: {len(colls)} colls, {cc} cases")

        if WebTestCollection.query.count() <= 3:
            wcs = []
            for proj in projects[:5]:
                for cn in ["Core Features","Regression","Smoke Tests"]:
                    wc = WebTestCollection(project_id=proj.id, user_id=admin.id, name=cn, created_at=rp(30))
                    db.session.add(wc)
                    wcs.append(wc)
            db.session.flush()
            for proj in projects[:5]:
                for wn, wu, wb, ws, wt in [("Login E2E","https://example.com/login","chromium",5,["login"]),("Product List","https://example.com/products","chromium",4,["product"]),("Cart Flow","https://example.com/cart","chromium",6,["cart"]),("Search Test","https://example.com","chromium",5,["search"]),("Register","https://example.com/register","chromium",6,["register"]),("Payment Page","https://example.com/checkout","chromium",4,["payment"]),("Profile","https://example.com/profile","chromium",5,["profile"]),("Order History","https://example.com/orders","chromium",4,["order"])]:
                    st = random.choice(["passed","passed","failed","pending"])
                    db.session.add(WebTestScript(project_id=proj.id, user_id=admin.id, name=wn, script_content="# Playwright: "+wn, target_url=wu, browser=wb, step_count=ws, tags=wt, status=st, last_status=st if st!="pending" else None, last_run_at=rp(7) if st!="pending" else None, last_run_duration=round(random.uniform(5,120),2) if st!="pending" else None, is_enabled=True, created_at=rp(30)))
            db.session.flush()
            print("Web scripts created")

        if AppTestCollection.query.count() <= 1:
            acs = []
            for proj in projects[:3]:
                ac = AppTestCollection(project_id=proj.id, user_id=admin.id, name=proj.name+" APP")
                db.session.add(ac)
                acs.append(ac)
            db.session.flush()
            for proj in projects[:3]:
                for pl, pk, ae in [("android","com.example.app","UiAutomator2"),("ios","com.example.app","XCUITest")]:
                    db.session.add(AppTestScript(name=proj.name+"-"+pl, project_id=proj.id, collection_id=random.choice(acs).id, user_id=admin.id, platform=pl, app_package=pk, automation_name=ae, script_content="# "+pl+" test", status=random.choice(["passed","failed","pending"]), last_run_at=rp(7), is_enabled=True, created_at=rp(20)))
            db.session.flush()

        if PerfTestScenario.query.count() <= 5:
            scs = []
            for proj in projects:
                for pn, pu, pm, pc, psr, pd in [("Homepage Load","https://example.com/","GET",100,10,300),("Product List","https://example.com/api/products","GET",200,20,600),("Login Stress","https://example.com/api/auth/login","POST",50,5,120),("Order Flow","https://example.com/api/orders","POST",100,10,300),("Search Load","https://example.com/api/search","GET",150,15,300),("Payment Callback","https://example.com/api/payments/notify","POST",30,3,180)][:random.randint(3,6)]:
                    s = PerfTestScenario(project_id=proj.id, user_id=admin.id, name=pn, target_url=pu, method=pm, user_count=pc, spawn_rate=psr, duration=pd, status=random.choice(["completed","completed","pending"]), last_run_at=rp(14), avg_response_time=round(random.uniform(50,800),2), max_response_time=round(random.uniform(1000,5000),2), min_response_time=round(random.uniform(10,50),2), throughput=round(random.uniform(100,2000),2), error_rate=round(random.uniform(0,5),2), is_enabled=True, created_at=rp(45))
                    db.session.add(s)
                    scs.append(s)
            db.session.flush()
            rs = []
            for s in scs:
                for _ in range(random.randint(3, 8)):
                    r = PerformanceTestResult(scenario_id=s.id, project_id=s.project_id, status="completed", triggered_by=random.choice(["manual","schedule","ci"]), p50_response_time=round(random.uniform(30,200),2), p90_response_time=round(random.uniform(100,500),2), p95_response_time=round(random.uniform(200,800),2), p99_response_time=round(random.uniform(500,2000),2), avg_response_time=round(random.uniform(50,300),2), max_response_time=round(random.uniform(1000,5000),2), min_response_time=round(random.uniform(5,30),2), total_requests=random.randint(10000,500000), rps=round(random.uniform(100,3000),2), error_count=random.randint(0,50), error_rate=round(random.uniform(0,3),4), active_users=s.user_count, duration=round(random.uniform(60,s.duration),2), started_at=rp(30), finished_at=rp(29), created_at=rp(30))
                    db.session.add(r)
                    rs.append(r)
            db.session.flush()
            for r in rs[:20]:
                for i in range(20):
                    db.session.add(PerformanceMetricSample(result_id=r.id, timestamp=rp(10), active_users=random.randint(1,r.active_users), current_rps=round(r.rps*random.uniform(0.7,1.3),2), avg_response_time=round(r.avg_response_time*random.uniform(0.8,1.2),2), error_rate=round(r.error_rate*random.uniform(0.5,1.5),4)))
            db.session.flush()
            for s in scs[:5]:
                for rn, th in [("P95 Alert",{"p95_threshold":500}),("P99 Alert",{"p99_threshold":1000}),("Error Rate",{"error_rate_threshold":1.0}),("Min RPS",{"rps_min_threshold":100})]:
                    db.session.add(PerformanceAlertRule(name=rn, scenario_id=s.id, notify_webhook="https://hooks.example.com/alert", enabled=True, trigger_count=random.randint(0,10), last_triggered_at=rp(14), **th))
            db.session.flush()
            all_rules = PerformanceAlertRule.query.all()
            for rule in all_rules:
                for _ in range(random.randint(0, 5)):
                    db.session.add(PerformanceAlertLog(rule_id=rule.id, result_id=random.choice(rs).id, alert_type="absolute", metric_name="P95", threshold_value=500, actual_value=round(random.uniform(500,2000),2), message="P95 exceeded", notification_sent=random.random()>0.2, created_at=rp(14)))
            db.session.flush()
            print(f"Perf: {len(scs)} scenarios, {len(rs)} results")

        if TestRun.query.count() <= 50:
            runs = []
            for proj in projects:
                for _ in range(random.randint(8, 20)):
                    tt = random.choice(["api","web","performance"])
                    t = random.randint(10, 200)
                    p = random.randint(int(t*0.7), t)
                    st = random.choice(["success","success","success","failed","cancelled"])
                    s = rp(30)
                    d = round(random.uniform(10,600), 2)
                    run = TestRun(project_id=proj.id, test_type=tt, test_object_name="User Mgmt", status=st, total_cases=t, passed=p, failed=t-p, duration=d, started_at=s, finished_at=s+timedelta(seconds=d), environment_name=random.choice(["Development","Testing","Staging"]), triggered_by=random.choice(["manual","schedule","ci"]), triggered_user_id=admin.id, created_at=s)
                    db.session.add(run)
                    runs.append(run)
            db.session.flush()
            for run in runs:
                db.session.add(TestReport(test_run_id=run.id, project_id=run.project_id, test_type=run.test_type, title=run.test_type.upper()+" Report", summary={"total":run.total_cases,"passed":run.passed,"failed":run.failed}, status="generated", created_at=run.created_at))
            db.session.flush()
            print(f"Runs: {len(runs)}")

        if QualityGate.query.count() <= 5:
            gates = []
            for proj in projects:
                for gn, gr, gp, gv in [("API Smoke Gate",95.0,500,None),("E2E Core Gate",90.0,1000,5.0),("Perf Baseline Gate",99.0,300,None),("Regression Gate",85.0,800,None),("Release Gate",95.0,500,2.0)]:
                    g = QualityGate(project_id=proj.id, name=gn, min_pass_rate=gr, max_p95_response_time=gp, max_visual_diff_percentage=gv, is_active=True, created_by=admin.id, created_at=rp(30))
                    db.session.add(g)
                    gates.append(g)
            db.session.flush()
            all_runs = TestRun.query.limit(20).all()
            for g in gates:
                for r in random.sample(all_runs, min(5, len(all_runs))):
                    db.session.add(QualityGateEvaluation(quality_gate_id=g.id, test_run_id=r.id, passed=random.random()>0.2, evaluation_details={"pass_rate":round(r.passed/r.total_cases*100,1) if r.total_cases>0 else 0}, created_at=r.created_at))
            db.session.flush()
            print(f"Gates: {len(gates)}")

        if ScheduledTask.query.count() <= 5:
            for proj in projects[:5]:
                for cn, cr in [("Daily Regression","0 2 * * *"),("Hourly Smoke","0 * * * *"),("Perf Test","0 6 * * *"),("Weekly Full","0 3 * * 1"),("Health Check","*/30 * * * *")]:
                    db.session.add(ScheduledTask(project_id=proj.id, name=proj.name+"-"+cn, cron_expression=cr, target_type="api_collection", target_id=random.randint(1,100), is_active=True, created_at=rp(30)))
            db.session.flush()

        if TriggerRule.query.count() <= 5:
            for proj in projects[:5]:
                for tn, te, tv in [("Git Push","git_push","push"),("PR Create","github_pr","pull_request"),("Tag Release","git_tag","tag"),("Schedule","schedule","schedule"),("Manual","manual","manual")]:
                    db.session.add(TriggerRule(project_id=proj.id, user_id=admin.id, name=proj.name+"-"+tn, event_type=te, event_name=tv, target_type="api_collection", target_id=random.randint(1,50), is_active=True, created_at=rp(20)))
            db.session.flush()

        if AuditLog.query.count() <= 50:
            for _ in range(100):
                db.session.add(AuditLog(user_id=random.choice(users[:5]).id, organization_id=random.choice(orgs).id if orgs else None, action=random.choice(["create","update","delete","login","logout"]), resource_type=random.choice(["project","test_case","test_run"]), resource_id=random.randint(1,100), ip_address="192.168.1."+str(random.randint(1,254)), user_agent="Chrome/120", created_at=rp(60)))
            db.session.flush()

        if NotificationConfig.query.count() <= 3:
            for u in users[:5]:
                for cn, cc in [("DingTalk","dingtalk"),("Feishu","feishu"),("Slack","slack")]:
                    db.session.add(NotificationConfig(user_id=u.id, name=u.username+"-"+cn, channel=cc, webhook_url="https://hooks.example.com/test", events=["test_completed"], is_active=True))
            db.session.flush()

        if AIInvocationLog.query.count() <= 30:
            for _ in range(80):
                tt, m = random.choice([("gen_case","deepseek-chat"),("analyze","deepseek-chat"),("visual","qwen3.6-plus")])
                db.session.add(AIInvocationLog(user_id=random.choice(users[:5]).id, task_type=tt, model_name=m, input_tokens=random.randint(100,5000), output_tokens=random.randint(50,2000), duration_ms=random.randint(500,15000), status="success" if random.random()>0.1 else "error", created_at=rp(30)))
            db.session.flush()

        if PromptVersion.query.count() <= 3:
            for pn in ["case_gen","result_analyze","assert_suggest","script_gen"]:
                for v in range(1, 4):
                    db.session.add(PromptVersion(prompt_name=pn, version=v, content="Prompt v"+str(v), is_active=(v==3), created_by=admin.id, created_at=rp(30)))
            db.session.flush()

        if ApiToken.query.count() <= 3:
            for u in users[:5]:
                for tn in ["CI/CD","Script","3rdParty"]:
                    db.session.add(ApiToken(user_id=u.id, name=u.username+"-"+tn, token_hash=hashlib.sha256((u.username+tn+str(random.random())).encode()).hexdigest(), permissions=["read","write"], is_active=True, expires_at=datetime.now(timezone.utc)+timedelta(days=90), last_used_at=rp(3), created_at=rp(30)))
            db.session.flush()

        if TestPlan.query.count() <= 3:
            plans = []
            for proj in projects[:5]:
                for pn, ps in [("v2.5 Release","active"),("Daily Smoke","active"),("Perf Baseline","active"),("Security Audit","draft"),("Payment Test","active")]:
                    p = TestPlan(project_id=proj.id, user_id=admin.id, organization_id=proj.organization_id, name=proj.name+"-"+pn, status=ps, include_cases=[{"case_type":"api","case_id":random.randint(1,100)}], tags=["regression"], total_runs=random.randint(1,20), last_run_at=rp(7) if ps=="active" else None, last_pass_rate=round(random.uniform(85,100),1) if ps=="active" else None, created_at=rp(30))
                    db.session.add(p)
                    plans.append(p)
            db.session.flush()
            for p in plans:
                if p.status != "active": continue
                for _ in range(random.randint(2, 8)):
                    t = random.randint(10, 50)
                    pp = random.randint(int(t*0.8), t)
                    db.session.add(TestPlanRun(plan_id=p.id, user_id=admin.id, status="completed", total_cases=t, passed=pp, failed=t-pp, pass_rate=round(pp/t*100,1), started_at=rp(14), finished_at=rp(13), duration=round(random.uniform(30,300),2), environment_name="Testing", triggered_by=random.choice(["manual","schedule","ci"]), created_at=rp(14)))
            db.session.flush()
            print(f"Plans: {len(plans)}")

        if TestDocument.query.count() <= 10:
            for proj in projects:
                for dn, dc in [("API Spec","# API Test Specification\n\n## Naming\n- Use Chinese descriptions"),("Perf Plan","# Performance Test Plan\n\n## Goals\n- P95 < 500ms\n- Error rate < 1%"),("Automation Guide","# Automation Guide\n\n## Stack\n- API: pytest\n- E2E: Playwright"),("Env Config","# Environment Config\n\n## Dev\n- URL: dev.example.com"),("Release Checklist","# Release Checklist\n\n- [ ] Smoke passed\n- [ ] Perf baseline OK")]:
                    db.session.add(TestDocument(project_id=proj.id, user_id=admin.id, title=proj.name+"-"+dn, content=dc, doc_type="markdown", created_at=rp(30)))
            db.session.flush()

        if IssueLink.query.count() <= 10:
            for r in TestRun.query.limit(30).all():
                tracker = random.choice(["jira","feishu","github"])
                key_prefix = random.choice(["TEST","QA","DEV","BUG"])
                issue_key = f"{key_prefix}-{random.randint(100,999)}"
                db.session.add(IssueLink(test_run_id=r.id, project_id=r.project_id, tracker=tracker, issue_key=issue_key, issue_url=f"https://{tracker}.example.com/browse/{issue_key}", issue_title=random.choice(["API 500 error","Perf degradation 20%","Login timeout","Search inaccurate","Payment callback failed"]), status=random.choice(["open","closed","in_progress"]), created_by="manual", user_id=admin.id, created_at=rp(20)))
            db.session.flush()

        if Comment.query.count() <= 10:
            for r in TestRun.query.limit(20).all():
                for _ in range(random.randint(1, 3)):
                    db.session.add(Comment(resource_type="test_run", resource_id=r.id, user_id=random.choice(users[:5]).id, content=random.choice(["Response time high, optimize query","Fixed concurrency issue","Pass rate dropped, check env","Add boundary test cases","Baseline updated","Added idempotency check"]), created_at=rp(10)))
            db.session.flush()

        db.session.commit()
        print("\nDone!")
        for n, m in [("users",User),("projects",Project),("api_cases",ApiTestCase),("web_scripts",WebTestScript),("perf",PerfTestScenario),("runs",TestRun),("gates",QualityGate),("plans",TestPlan),("audit",AuditLog)]:
            print(f"  {n}: {m.query.count()}")

if __name__ == "__main__":
    seed()
