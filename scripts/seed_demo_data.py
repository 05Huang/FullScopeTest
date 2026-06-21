#!/usr/bin/env python3
"""seed demo data for customer service project"""
import sys, os, random
from datetime import datetime, timedelta
sys.path.insert(0, '/app')
os.environ['FLASK_ENV'] = 'production'
from app import create_app
from app.extensions import db
from sqlalchemy import text

app = create_app('production')
with app.app_context():
    # 客服系统项目 id=15, 组织 id=1 (默认组织), huangxuan user_id=57
    pid = 15
    uid = 57
    print(f'project_id={pid}, user_id={uid}')

    # 先清理已有数据（幂等执行，先删子表）
    db.session.execute(text(f"DELETE FROM api_test_cases WHERE collection_id IN (SELECT id FROM api_test_collections WHERE project_id={pid})"))
    db.session.execute(text(f"DELETE FROM api_test_collections WHERE project_id={pid}"))
    db.session.execute(text(f"DELETE FROM web_test_scripts WHERE project_id={pid}"))
    db.session.execute(text(f"DELETE FROM perf_test_scenarios WHERE project_id={pid}"))
    db.session.execute(text(f"DELETE FROM visual_diffs WHERE test_run_id IN (SELECT id FROM test_runs WHERE project_id={pid})"))
    db.session.execute(text(f"DELETE FROM test_reports WHERE test_run_id IN (SELECT id FROM test_runs WHERE project_id={pid})"))
    db.session.execute(text(f"DELETE FROM test_runs WHERE project_id={pid}"))
    db.session.commit()
    print('Cleaned existing data')

    collections = {
        '客服会话管理': [('创建会话','POST','/api/v1/conversations'),('创建会话-缺少客户ID','POST','/api/v1/conversations'),('获取会话列表','GET','/api/v1/conversations?page=1'),('获取会话详情','GET','/api/v1/conversations/5001'),('更新会话状态','PATCH','/api/v1/conversations/5001'),('关闭会话','POST','/api/v1/conversations/5001/close'),('搜索会话','GET','/api/v1/conversations?q=test'),('批量关闭会话','POST','/api/v1/conversations/batch-close'),('获取会话统计','GET','/api/v1/conversations/stats')],
        '工单系统': [('创建工单','POST','/api/v1/tickets'),('创建工单-标题为空','POST','/api/v1/tickets'),('工单列表-待处理','GET','/api/v1/tickets?status=open'),('工单列表-已关闭','GET','/api/v1/tickets?status=closed'),('分配工单','POST','/api/v1/tickets/3001/assign'),('添加工单备注','POST','/api/v1/tickets/3001/notes'),('更新工单优先级','PATCH','/api/v1/tickets/3001'),('关闭工单','POST','/api/v1/tickets/3001/close'),('工单统计','GET','/api/v1/tickets/stats'),('SLA报告','GET','/api/v1/tickets/sla-report'),('导出工单','GET','/api/v1/tickets/export'),('创建工单-无效邮箱','POST','/api/v1/tickets')],
        '知识库管理': [('文章列表','GET','/api/v1/kb/articles'),('搜索知识库','GET','/api/v1/kb/search?q=test'),('创建文章','POST','/api/v1/kb/articles'),('文章详情','GET','/api/v1/kb/articles/4001'),('更新文章','PUT','/api/v1/kb/articles/4001'),('删除文章-无权限','DELETE','/api/v1/kb/articles/4001'),('热门文章','GET','/api/v1/kb/articles/popular'),('分类统计','GET','/api/v1/kb/categories/stats')],
        '客户信息管理': [('客户列表','GET','/api/v1/customers'),('创建客户','POST','/api/v1/customers'),('客户详情','GET','/api/v1/customers/1001'),('更新客户','PUT','/api/v1/customers/1001'),('客户会话历史','GET','/api/v1/customers/1001/conversations'),('客户标签','POST','/api/v1/customers/1001/tags'),('满意度调查','GET','/api/v1/customers/1001/satisfaction'),('批量导入','POST','/api/v1/customers/import')],
        '坐席管理': [('坐席列表','GET','/api/v1/agents'),('状态切换','PATCH','/api/v1/agents/201/status'),('工作量','GET','/api/v1/agents/201/workload'),('排班查询','GET','/api/v1/agents/schedule'),('绩效统计','GET','/api/v1/agents/performance'),('分配会话','POST','/api/v1/agents/201/assign'),('在线坐席','GET','/api/v1/agents?status=online')],
    }
    for cname, cases in collections.items():
        db.session.execute(text(f"INSERT INTO api_test_collections(name,project_id,user_id,created_at,updated_at) VALUES('{cname}',{pid},{uid},NOW(),NOW())"))
        cid = db.session.execute(text('SELECT id FROM api_test_collections ORDER BY id DESC LIMIT 1')).fetchone()[0]
        for mname, mmethod, murl in cases:
            db.session.execute(text(f"INSERT INTO api_test_cases(name,collection_id,user_id,method,url,body,created_at,updated_at) VALUES('{mname}',{cid},{uid},'{mmethod}','{murl}','{{}}',NOW(),NOW())"))
        db.session.commit()
        print(f'  {cname}: {len(cases)} cases')

    web_scripts = [('客服登录流程','passed',12.5,'https://cs.example.com/login'),('创建工单全流程','passed',18.3,'https://cs.example.com/tickets/new'),('客户信息搜索','passed',8.7,'https://cs.example.com/customers'),('会话转接功能','failed',25.1,'https://cs.example.com/conversations'),('知识库搜索','passed',6.2,'https://cs.example.com/kb'),('工单批量操作','passed',15.8,'https://cs.example.com/tickets'),('客服报表页面','passed',9.4,'https://cs.example.com/reports'),('满意度评分','passed',11.2,'https://cs.example.com/survey'),('会话历史记录','passed',7.8,'https://cs.example.com/history'),('坐席工作台布局','passed',10.5,'https://cs.example.com/workspace'),('多标签页会话','failed',30.2,'https://cs.example.com/tabs'),('快捷回复功能','passed',5.3,'https://cs.example.com/quick-reply')]
    for sname,sstatus,sdur,surl in web_scripts:
        sc = f'from playwright.sync_api import sync_playwright; p=sync_playwright().start(); b=p.chromium.launch(); pg=b.new_page(); pg.goto(\"{surl}\"); b.close(); p.stop()'
        db.session.execute(text(f"INSERT INTO web_test_scripts(name,project_id,user_id,script_content,target_url,status,last_run_duration,created_at,updated_at) VALUES('{sname}',{pid},{uid},'{sc}','{surl}','{sstatus}',{sdur},NOW(),NOW())"))
    db.session.commit()
    print(f'  Web scripts: {len(web_scripts)}')

    perf_scenes = [('客服系统首页压测',100,300,'https://cs.example.com'),('会话创建接口压测',50,180,'https://cs.example.com/api/v1/conversations'),('知识库搜索压测',200,300,'https://cs.example.com/kb'),('工单列表查询压测',80,240,'https://cs.example.com/api/v1/tickets'),('坐席状态轮询压测',300,600,'https://cs.example.com/api/v1/agents/status'),('消息推送WebSocket压测',500,300,'wss://cs.example.com/ws')]
    for sname,suser,sdur,surl in perf_scenes:
        db.session.execute(text(f"INSERT INTO perf_test_scenarios(name,project_id,user_id,target_url,user_count,duration,created_at,updated_at) VALUES('{sname}',{pid},{uid},'{surl}',{suser},{sdur},NOW(),NOW())"))
    db.session.commit()
    print(f'  Perf scenarios: {len(perf_scenes)}')

    now = datetime.now()
    for i in range(30):
        d = now - timedelta(days=29-i)
        ds = d.strftime('%Y-%m-%d')
        wd = d.weekday()
        factor = 1.2 if wd < 5 else 0.6
        trend = 1 + (i/30)*0.3
        api_p = max(5, int((35+random.randint(-8,8))*factor*trend))
        api_f = random.randint(0,5) if wd<5 else random.randint(0,2)
        api_s = 'success' if api_f==0 else 'failed'
        db.session.execute(text(f"INSERT INTO test_runs(project_id,triggered_user_id,test_type,status,total_cases,passed,failed,started_at,finished_at,created_at) VALUES({pid},{uid},'api','{api_s}',{api_p+api_f},{api_p},{api_f},'{ds} 10:00:00+00','{ds} 10:0{random.randint(1,5)}:00+00','{ds} 10:00:00+00')"))
        web_t = random.randint(3,8)
        web_p = random.randint(max(1,web_t-3),web_t)
        web_f = web_t-web_p
        web_s = 'success' if web_f==0 else 'failed'
        db.session.execute(text(f"INSERT INTO test_runs(project_id,triggered_user_id,test_type,status,total_cases,passed,failed,started_at,finished_at,created_at) VALUES({pid},{uid},'web','{web_s}',{web_t},{web_p},{web_f},'{ds} 14:00:00+00','{ds} 14:0{random.randint(1,9)}:00+00','{ds} 14:00:00+00')"))
        if wd in [0,2,4]:
            perf_t = random.randint(100,300)
            perf_p = random.randint(int(perf_t*0.92),perf_t)
            perf_f = perf_t-perf_p
            perf_s = 'success' if perf_f==0 else 'failed'
            db.session.execute(text(f"INSERT INTO test_runs(project_id,triggered_user_id,test_type,status,total_cases,passed,failed,started_at,finished_at,created_at) VALUES({pid},{uid},'perf','{perf_s}',{perf_t},{perf_p},{perf_f},'{ds} 02:00:00+00','{ds} 02:{random.randint(10,59)}:00+00','{ds} 02:00:00+00')"))
    db.session.commit()

    tc = db.session.execute(text('SELECT COUNT(*) FROM api_test_cases')).fetchone()[0]
    wc = db.session.execute(text('SELECT COUNT(*) FROM web_test_scripts')).fetchone()[0]
    pc = db.session.execute(text('SELECT COUNT(*) FROM perf_test_scenarios')).fetchone()[0]
    rc = db.session.execute(text(f'SELECT COUNT(*) FROM test_runs WHERE project_id={pid}')).fetchone()[0]
    print(f'API: {tc}, Web: {wc}, Perf: {pc}, Runs: {rc}')
    print('DONE')
