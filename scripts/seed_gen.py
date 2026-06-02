import json,random,hashlib
from datetime import datetime,timedelta
random.seed(42)
pw="scrypt:32768:8:1$WndhvdorMtHoID7P$fed763d0110cc7fa9d4edd4358ecf19a65ede4f828c813e5562d9fe501f336c97a0a58503f0d82dace43f082b2a6b1f69e360a019b92cefdadae7749f97ddb00"
def tk(n):return hashlib.sha256(f"fs_{n}_{random.randint(1000,9999)}".encode()).hexdigest()
def past(m=12):
 n=datetime(2026,6,2,10,0,0);d=timedelta(days=random.randint(1,m*30),hours=random.randint(0,23),minutes=random.randint(0,59));return(n-d).strftime("%Y-%m-%d %H:%M:%S")
def rec(d=30):
 n=datetime(2026,6,2,10,0,0);dt=timedelta(days=random.randint(0,d),hours=random.randint(0,23),minutes=random.randint(0,59));return(n-dt).strftime("%Y-%m-%d %H:%M:%S")
def ws():
 r=random.random()
 if r<.65:return"success"
 if r<.85:return"failed"
 if r<.92:return"running"
 if r<.97:return"pending"
 return"cancelled"
def v(val):return f"'{val}'" if val else"NULL"
def js(val):return json.dumps(val,ensure_ascii=False)
def e(s):return s.replace("'","''")
S=[]
# USERS
un=['alex.zhang','linda.wang','kevin.li','sarah.zhao','mike.liu','emma.chen','david.yang','lisa.huang','james.zhou','anna.wu','tom.xu','jenny.sun','bob.ma','amy.zhu','jack.hu','lucy.guo','henry.lin','grace.he','peter.gao','kate.luo','sam.liang','julia.song','frank.zheng','helen.xie','leo.han','ruby.tang','oscar.feng','iris.dong','max.xiao','chloe.cheng','eric.cao','vivian.yuan','ryan.deng','natalie.xu','adam.fu','sophia.shen','jason.peng','cindy.lv','nick.su','mia.lu','chris.jiang','penny.cai','derek.jia','vanessa.ding','bruce.wei','alice.xue','gavin.ye','monica.yan','raymond.yu','wendy.fan']
dm=['qq.com','163.com','gmail.com','outlook.com','foxmail.com','alibaba-inc.com','tencent.com','bytedance.com','meituan.com','jd.com']
for i,u in enumerate(un):
 uid=i+5;d=random.choice(dm);role='admin' if i<5 else random.choice(['member','member','member','viewer'])
 c=past(12);ll=rec(7) if random.random()>.2 else None;av=f'https://api.dicebear.com/7.x/avataaars/svg?seed={u}' if random.random()>.3 else None
 S.append(f"INSERT INTO users(id,username,email,password_hash,avatar,role,is_active,created_at,last_login)VALUES({uid},'{u}','{u}@{d}','{pw}',{v(av)},'{role}',true,'{c}',{v(ll)})ON CONFLICT(id)DO NOTHING;")
S.append("UPDATE users SET role='admin'WHERE id=1;")
S.append("UPDATE users SET role='admin'WHERE id=2;")
# ORGS
orgs=[(2,'星辰科技','startech','企业级SaaS'),(3,'云桥信息','yunbridge','金融科技'),(4,'锐智软件','ruizhi','电商平台'),(5,'蓝鲸数据','lanjing','大数据'),(6,'飞鸟网络','feiniao','社交内容'),(7,'铁壁安全','tiebi','网络安全'),(8,'灵犀AI','lingxi','人工智能'),(9,'翠竹教育','cuizhu','在线教育')]
for oid,nm,sl,ds in orgs:
 ow=random.choice([1,2,5,6,7]);S.append(f"INSERT INTO organizations(id,name,slug,description,owner_id,is_active,created_at,updated_at)VALUES({oid},'{nm}','{sl}','{ds}',{ow},true,'{past(10)}','{past(10)}')ON CONFLICT(id)DO NOTHING;")
# ORG MEMBERS
mid=1
for oid,_,_,_ in orgs:
 ow=random.choice([1,2,5,6,7]);S.append(f"INSERT INTO organization_members(id,organization_id,user_id,role,is_active,created_at)VALUES({mid},{oid},{ow},'owner',true,'{past(10)}')ON CONFLICT DO NOTHING;");mid+=1
 for uid in random.sample(range(5,55),random.randint(3,8)):
  r=random.choice(['admin','member','member','viewer']);S.append(f"INSERT INTO organization_members(id,organization_id,user_id,role,is_active,created_at)VALUES({mid},{oid},{uid},'{r}',true,'{past(8)}')ON CONFLICT DO NOTHING;");mid+=1
for uid in[2,3,5,6,7,8,9,10]:
 r='admin' if uid in[2,5]else'member';S.append(f"INSERT INTO organization_members(id,organization_id,user_id,role,is_active,created_at)VALUES({mid},1,{uid},'{r}',true,'{past(10)}')ON CONFLICT DO NOTHING;");mid+=1
# PROJECTS
projs=[(2,'用户中心','用户注册登录权限',2,2),(3,'订单系统','订单支付退款',3,3),(4,'商品管理','商品CRUD库存',4,4),(5,'支付网关','聚合支付对账',1,5),(6,'消息中心','站内信Push短信',5,6),(7,'数据大屏','实时数据可视化',6,7),(8,'后台管理','运营管理后台',7,8),(9,'移动端H5','H5活动页小程序',8,9),(10,'开放平台','API网关文档',9,2),(11,'内容审核','AI图文审核',10,3),(12,'搜索服务','全文搜索推荐',5,4),(13,'营销系统','优惠券秒杀',6,5),(14,'BI报表','数据看板查询',7,6),(15,'客服系统','工单在线客服',8,7),(16,'供应链','采购仓储配送',9,8)]
for pid,nm,ds,ow,oi in projs:
 S.append(f"INSERT INTO projects(id,name,description,owner_id,organization_id,settings,created_at,updated_at)VALUES({pid},'{nm}','{ds}',{ow},{oi},'{{}}','{past(9)}','{rec(5)}')ON CONFLICT(id)DO NOTHING;")
# ENVS
eid=1;em={}
envs=[('开发环境','https://dev.example.com',False),('测试环境','https://test.example.com',True),('预发布','https://staging.example.com',False),('生产环境','https://api.example.com',False)]
for pid in range(1,17):
 em[pid]=[]
 for en,eu,ed in envs:
  S.append(f"INSERT INTO environments(id,project_id,name,base_url,variables,headers,is_default,created_at,updated_at)VALUES({eid},{pid},'{en}','{eu}','{{}}','{{}}',{str(ed).lower()},' {past(8)}','{rec(3)}')ON CONFLICT(id)DO NOTHING;");em[pid].append(eid);eid+=1
# API COLLECTIONS
acols=[('用户认证','登录注册重置'),('商品管理','CRUD搜索分类'),('订单交易','下单支付退款'),('消息通知','站内信Push'),('营销活动','优惠券秒杀'),('系统管理','配置日志'),('数据报表','统计导出'),('文件管理','上传下载')]
cid=1;cm={}
for pid in range(1,17):
 cm[pid]=[]
 for j,(cn,cd) in enumerate(acols):
  if random.random()<.12:continue
  uid=random.choice([1,2,5,6,7]);S.append(f"INSERT INTO api_test_collections(id,project_id,user_id,name,description,sort_order,created_at,updated_at)VALUES({cid},{pid},{uid},'{cn}','{cd}',{j},'{past(8)}','{rec(5)}')ON CONFLICT(id)DO NOTHING;");cm[pid].append(cid);cid+=1
# API CASES
eps=[('用户登录','POST','/api/v1/auth/login',['auth','P0']),('用户信息','GET','/api/v1/users/me',['user','P0']),('更新资料','PUT','/api/v1/users/me',['user','P1']),('商品列表','GET','/api/v1/products',['product','P0']),('创建订单','POST','/api/v1/orders',['order','P0']),('订单详情','GET','/api/v1/orders/1001',['order','P0']),('取消订单','POST','/api/v1/orders/1001/cancel',['order','P1']),('发起支付','POST','/api/v1/payments',['payment','P0']),('支付状态','GET','/api/v1/payments/1001',['payment','P1']),('申请退款','POST','/api/v1/refunds',['payment','P1']),('消息列表','GET','/api/v1/messages',['message','P1']),('标记已读','PUT','/api/v1/messages/1001',['message','P2']),('搜索商品','GET','/api/v1/search',['search','P1']),('推荐列表','GET','/api/v1/recommendations',['recommendation','P2']),('上传图片','POST','/api/v1/upload',['upload','P1']),('获取配置','GET','/api/v1/config',['config','P2']),('提交反馈','POST','/api/v1/feedback',['feedback','P2']),('优惠券','GET','/api/v1/coupons',['marketing','P1']),('领取券','POST','/api/v1/coupons/1001',['marketing','P1']),('健康检查','GET','/api/v1/health',['health','P0'])]
case_id=1
for pid in range(1,17):
 for pcid in cm.get(pid,[]):
  for j,ep in enumerate(random.sample(eps,random.randint(3,8))):
   uid=random.choice([1,2,5,6,7]);env=random.choice(em.get(pid,[1]));st=ws();lr=rec(15)if st!='pending'else None;pri=random.choice([1,1,2,2,2,3])
   S.append(f"INSERT INTO api_test_cases(id,collection_id,project_id,user_id,environment_id,name,description,method,url,headers,params,body,body_type,assertions,timeout,retry_count,tags,priority,is_enabled,sort_order,last_run_at,last_status,created_at,updated_at)VALUES({case_id},{pcid},{pid},{uid},{env},'{ep[0]}','验证{ep[0]}','{ep[1]}','{ep[2]}','{{}}','{{}}',NULL,'json','[]',30,0,'{js(ep[3])}',{pri},true,{j},{v(lr)},{v(st)},'{past(7)}','{rec(3)}')ON CONFLICT(id)DO NOTHING;")
   case_id+=1
# WEB COLLECTIONS + SCRIPTS
wcid=1;wsid=1
wcs=[('冒烟测试集','核心冒烟'),('回归测试集','版本回归'),('UI兼容性','多浏览器')]
wss=[('用户登录流程','验证登录','https://example.com/login',['smoke','P0']),('商品搜索','验证搜索','https://example.com/products',['smoke','P0']),('购物车','验证购物车','https://example.com/cart',['regression','P1']),('订单支付','端到端支付','https://example.com/checkout',['smoke','P0']),('后台用户列表','后台管理','https://admin.example.com/users',['regression','P1']),('响应式布局','多设备','https://example.com',['visual','P2']),('表单验证','注册校验','https://example.com/register',['regression','P1']),('文件上传','头像上传','https://example.com/profile',['regression','P2'])]
for pid in range(1,17):
 if random.random()<.2:continue
 for jj,(cn,cd) in enumerate(wcs):
  if random.random()<.3:continue
  uid=random.choice([1,2,5,6,7]);S.append(f"INSERT INTO web_test_collections(id,project_id,user_id,name,description,sort_order,created_at,updated_at)VALUES({wcid},{pid},{uid},'{cn}','{cd}',{jj},'{past(7)}','{rec(3)}')ON CONFLICT(id)DO NOTHING;")
  for k,ws_ in enumerate(random.sample(wss,random.randint(2,5))):
   st=ws();lr=rec(10)if st!='pending'else None;dur=round(random.uniform(5,120),1)if lr else None
   S.append(f"INSERT INTO web_test_scripts(id,project_id,collection_id,user_id,name,description,script_content,script_type,target_url,browser,headless,timeout,step_count,status,last_status,last_run_at,last_run_duration,tags,is_enabled,sort_order,created_at,updated_at)VALUES({wsid},{pid},{wcid},{uid},'{ws_[0]}','{ws_[1]}','from playwright.sync_api import Page','playwright','{ws_[2]}','chromium',true,30000,{random.randint(3,12)},'{st}',{v(st)},{v(lr)},{dur if dur else 'NULL'},'{js(ws_[3])}',true,{k},'{past(6)}','{rec(3)}')ON CONFLICT(id)DO NOTHING;")
   wsid+=1
  wcid+=1
# PERF SCENARIOS
pss=[('首页并发','大量用户访问','https://example.com/','GET',100,10,300),('登录压测','登录高并发','https://example.com/api/v1/auth/login','POST',200,20,180),('商品查询','缓存性能','https://example.com/api/v1/products','GET',150,15,300),('下单全流程','完整业务','https://example.com/api/v1/orders','POST',50,5,600),('搜索压测','全文搜索','https://example.com/api/v1/search','GET',100,10,180)]
ppid=1;pm={}
for pid in range(1,17):
 pm[pid]=[]
 if random.random()<.3:continue
 for sc in random.sample(pss,random.randint(1,3)):
  uid=random.choice([1,2,5,6,7]);st=random.choice(['completed','completed','completed','pending','failed'])
  art=round(random.uniform(20,500),1);mxt=round(art*random.uniform(3,10),1);mnt=round(art*random.uniform(.1,.5),1);tp=round(random.uniform(50,2000),1);er=round(random.uniform(0,5),2);lr=rec(20)if st!='pending'else None
  S.append(f"INSERT INTO perf_test_scenarios(id,project_id,user_id,name,description,target_url,method,headers,script_content,user_count,spawn_rate,duration,status,last_run_at,avg_response_time,max_response_time,min_response_time,throughput,error_rate,tags,is_enabled,created_at,updated_at)VALUES({ppid},{pid},{uid},'{sc[0]}','{sc[1]}','{sc[2]}','{sc[3]}','{{}}','from locust import HttpUser',{sc[4]},{sc[5]},{sc[6]},'{st}',{v(lr)},{art},{mxt},{mnt},{tp},{er},'[\"performance\"]',true,'{past(6)}','{rec(5)}')ON CONFLICT(id)DO NOTHING;")
  pm[pid].append(ppid);ppid+=1
# PERF RESULTS
rrid=1;rm={}
for pid in range(1,17):
 for sid in pm.get(pid,[]):
  rm[sid]=[]
  for _ in range(random.randint(3,6)):
   sa=past(5);dur=random.randint(60,600);sdt=datetime.strptime(sa,"%Y-%m-%d %H:%M:%S");fa=(sdt+timedelta(seconds=dur)).strftime("%Y-%m-%d %H:%M:%S")
   st=random.choice(['completed','completed','completed','failed']);tr=random.randint(1000,50000);tf=int(tr*random.uniform(0,.05));er=round(tf/tr*100,2)if tr>0 else 0;rps=round(random.uniform(50,3000),1);art=round(random.uniform(15,400),1)
   S.append(f"INSERT INTO performance_test_results(id,scenario_id,project_id,user_count,spawn_rate,duration,target_url,status,started_at,finished_at,total_requests,total_failures,error_rate,rps,avg_response_time,min_response_time,max_response_time,p50_response_time,p75_response_time,p95_response_time,p99_response_time,created_at,updated_at)VALUES({rrid},{sid},{pid},{random.randint(10,200)},{random.randint(1,20)},{dur},'https://example.com/api','{st}','{sa}','{fa}',{tr},{tf},{er},{rps},{art},{round(art*.3,1)},{round(art*5,1)},{round(art*.7,1)},{round(art*1.3,1)},{round(art*2.5,1)},{round(art*4,1)},'{sa}','{fa}')ON CONFLICT(id)DO NOTHING;")
   rm[sid].append(rrid)
   # metric samples
   for ss in range(min(dur,8)):
    st2=(sdt+timedelta(seconds=ss)).strftime("%Y-%m-%d %H:%M:%S")
    S.append(f"INSERT INTO performance_metric_samples(test_result_id,timestamp,elapsed_seconds,rps,active_users,avg_response_time,min_response_time,max_response_time,p95_response_time,p99_response_time,request_count,failure_count,error_rate)VALUES({rrid},'{st2}',{ss},{round(rps*random.uniform(.7,1.3),1)},{min(random.randint(1,200),(ss+1)*3)},{round(art*random.uniform(.8,1.2),1)},{round(art*.3,1)},{round(art*3,1)},{round(art*2,1)},{round(art*4,1)},{int(tr*(ss+1)/min(dur,8))},{int(tf*(ss+1)/min(dur,8))},{round(random.uniform(0,3),2)});")
   rrid+=1
# TEST RUNS
run_id=5;runm={}
for pid in range(1,17):
 runm[pid]=[]
 for _ in range(random.randint(8,20)):
  tt=random.choice(['api','api','api','web','web','performance']);st=ws();tc=random.randint(5,100);pa=int(tc*random.uniform(.7,1));fa2=tc-pa;sk=random.randint(0,3);er=random.randint(0,2);dur=round(random.uniform(10,600),1);sa=past(6)
  sdt=datetime.strptime(sa,"%Y-%m-%d %H:%M:%S");fat=(sdt+timedelta(seconds=int(dur))).strftime("%Y-%m-%d %H:%M:%S")if st in['success','failed','cancelled']else None
  tb=random.choice(['manual','schedule','ci','trigger']);tu=random.choice([1,2,5,6,7]);en=random.choice(['开发环境','测试环境','预发布']);on=random.choice(['冒烟测试','回归测试','接口自动化','UI自动化','性能压测'])
  S.append(f"INSERT INTO test_runs(id,project_id,test_type,test_object_name,status,total_cases,passed,failed,skipped,error,duration,started_at,finished_at,environment_name,triggered_by,triggered_user_id,created_at)VALUES({run_id},{pid},'{tt}','{on}',{v(st)},{tc},{pa},{fa2},{sk},{er},{dur},'{sa}',{v(fat)},'{en}','{tb}',{tu},'{sa}')ON CONFLICT(id)DO NOTHING;")
  runm[pid].append(run_id);run_id+=1
# REPORTS
rpt=1
for pid in range(1,17):
 for tr in runm.get(pid,[])[:6]:
  tt=random.choice(['api','web','performance']);title=f'{tt.upper()}报告-{rec(30)[:10]}';sm=js({"total":random.randint(10,100),"passed":random.randint(8,95),"pass_rate":round(random.uniform(85,100),1)})
  S.append(f"INSERT INTO test_reports(id,test_run_id,project_id,test_type,title,summary,status,created_at,updated_at)VALUES({rpt},{tr},{pid},'{tt}','{title}','{sm}','generated','{past(5)}','{rec(2)}')ON CONFLICT(id)DO NOTHING;");rpt+=1
# DOCUMENTS
dcs=[('API接口测试规范','test_plan','API测试规范文档',['规范','API']),('Q3测试计划','test_plan','Q3测试计划',['计划','Q3']),('用户中心用例','test_case','用户中心测试用例',['用例','用户']),('性能测试报告','test_report','性能测试报告',['报告','性能']),('自动化说明','other','自动化测试说明',['文档']),('订单测试方案','test_plan','订单模块方案',['方案']),('安全检查清单','test_case','安全测试检查',['安全'])]
did=1
for pid in range(1,17):
 for dt,dc,dc2,tg in random.sample(dcs,random.randint(2,4)):
  uid=random.choice([1,2,5,6,7])
  S.append(f"INSERT INTO test_documents(id,project_id,title,content,category,version,created_by,updated_by,tags,is_published,created_at,updated_at)VALUES({did},{pid},'{dt}','{e(dc2)}','{dc}','{random.randint(1,3)}.{random.randint(0,9)}',{uid},{uid},'{js(tg)}',{str(random.choice([True,True,True,False])).lower()},' {past(8)}','{rec(5)}')ON CONFLICT(id)DO NOTHING;");did+=1
# QUALITY GATES
qgid=1;qgm={}
for pid in range(1,17):
 qgm[pid]=[]
 for gn,gd,mr,mx,mv in[('冒烟门禁','核心冒烟',95.0,500,5.0),('回归门禁','全量回归',90.0,1000,10.0),('性能门禁','P95响应',85.0,2000,None)]:
  if random.random()<.2:continue
  uid=random.choice([1,2,5]);mvv=f"{mv}"if mv else"NULL"
  S.append(f"INSERT INTO quality_gates(id,project_id,name,description,is_active,min_pass_rate,max_p95_response_time,max_visual_diff_percentage,created_by,created_at,updated_at)VALUES({qgid},{pid},'{gn}','{gd}',true,{mr},{mx},{mvv},{uid},'{past(6)}','{rec(5)}')ON CONFLICT(id)DO NOTHING;");qgm[pid].append(qgid);qgid+=1
# QG EVALUATIONS
evid=1
for pid in range(1,17):
 for qg in qgm.get(pid,[]):
  for tr in runm.get(pid,[])[:5]:
   p=random.choice([True,True,True,True,False]);d=js({"pass_rate":round(random.uniform(80,100),1),"met":p})
   S.append(f"INSERT INTO quality_gate_evaluations(id,quality_gate_id,test_run_id,passed,evaluation_details,created_at)VALUES({evid},{qg},{tr},{str(p).lower()},'{d}','{past(4)}')ON CONFLICT(id)DO NOTHING;");evid+=1
# TRIGGER RULES
trid=1
for pid in range(1,17):
 for rn,ev,br,tt,ty in[('Push冒烟','push',['main','develop'],['api'],'api_collection'),('PR回归','pull_request',['main'],['api','web'],'api_collection'),('Release全量','tag',[],['api','web','perf'],'web_collection')]:
  if random.random()<.3:continue
  uid=random.choice([1,2,5])
  S.append(f"INSERT INTO trigger_rules(id,project_id,name,description,is_active,trigger_event,target_branches,test_types,target_type,created_by,created_at,updated_at)VALUES({trid},{pid},'{rn}','自动{rn}',true,'{ev}','{js(br)}','{js(tt)}','{ty}',{uid},'{past(5)}','{rec(3)}')ON CONFLICT(id)DO NOTHING;");trid+=1
# SCHEDULED TASKS
stid=1
for pid in range(1,17):
 for sn,cron,ty in[('每日冒烟','0 9 * * *','api_collection'),('每周回归','0 2 * * 1','api_collection'),('性能巡检','0 3 * * *','perf_scenario'),('周末全量','0 1 * * 6','web_collection')]:
  if random.random()<.3:continue
  tid=random.choice(cm.get(pid,[1])or[1]);wh=random.choice(["'https://oapi.dingtalk.com/robot/send?access_token=xxx'","'https://open.feishu.cn/open-apis/bot/v2/hook/xxx'","NULL"])
  S.append(f"INSERT INTO scheduled_tasks(id,project_id,name,cron_expression,target_type,target_id,is_active,notify_webhook,notify_events,created_at,updated_at)VALUES({stid},{pid},'{sn}','{cron}','{ty}',{tid},true,{wh},'all','{past(6)}','{rec(3)}')ON CONFLICT(id)DO NOTHING;");stid+=1
# API TOKENS
tkid=1
for uid in[1,2,5,6,7]:
 for tn,pm2 in[('CI/CD Token',['read','write']),('监控Token',['read']),('调试Token',['read','write'])]:
  if random.random()<.4:continue
  S.append(f"INSERT INTO api_tokens(id,user_id,name,token_hash,permissions,expires_at,is_active,last_used_at,created_at)VALUES({tkid},{uid},'{tn}','{tk(tn)}','{js(pm2)}','{'2027-06-01 00:00:00'}',true,'{rec(3)}','{past(6)}')ON CONFLICT(id)DO NOTHING;");tkid+=1
# PROMPT VERSIONS
pvid=1
pvs=[('copilot','AI助手','你是专业测试助手'),('script_gen','脚本生成','生成Playwright脚本'),('swagger_gen','用例生成','根据OpenAPI生成'),('dedup','用例去重','语义相似度分析'),('review','代码审查','审查代码质量')]
for feat,nm,sp in pvs:
 for ver in range(1,random.randint(2,4)):
  act=(ver==2);ti=random.randint(50,2000);sc2=int(ti*random.uniform(.85,.99))
  S.append(f"INSERT INTO prompt_versions(id,feature,name,version,is_active,system_prompt,temperature,model_name,total_invocations,success_count,failure_count,avg_latency_ms,avg_tokens,avg_cost,traffic_weight,created_by,created_at,updated_at)VALUES({pvid},'{feat}','{nm}v{ver}',{ver},{str(act).lower()},'{e(sp)}',{round(random.uniform(.1,.7),1)},'gpt-4o',{ti},{sc2},{ti-sc2},{round(random.uniform(500,5000),0)},{round(random.uniform(200,3000),0)},{round(random.uniform(.001,.05),4)},{1.0 if act else round(random.uniform(0,.3),2)},1,'{past(8)}','{rec(5)}')ON CONFLICT(id)DO NOTHING;")
  pvid+=1
# AI LOGS
aifeats=['copilot','script_gen','swagger_gen','dedup','review']
mdls=['gpt-4o','gpt-4o-mini','claude-3-opus','claude-3-sonnet']
for i in range(150):
 uid=random.choice([1,2,5,6,7,8,9,10]);feat=random.choice(aifeats);model=random.choice(mdls);ok=random.random()>.08;lat=random.randint(200,8000);pt=random.randint(100,4000);ct=random.randint(50,2000);cost=round((pt+ct)*.00003,4)
 emsg="'timeout'"if not ok else"NULL"
 S.append(f"INSERT INTO ai_invocation_logs(user_id,feature,model_name,prompt,response,success,error_message,error_type,latency_ms,prompt_tokens,completion_tokens,total_tokens,cost_estimate,created_at)VALUES({uid},'{feat}','{model}','{e(f'生成{feat}测试用例')}','{e('好的已生成')if ok else'NULL'}',{str(ok).lower()},{emsg},{emsg},{lat},{pt},{ct},{pt+ct},{cost},'{past(6)}');")
# ALERT RULES
arid=1
for pid in range(1,17):
 for sid in pm.get(pid,[]):
  for rn,p95,err in[('P95告警',1000,None),('错误率告警',None,5.0),('劣化告警',None,None)]:
   if random.random()<.5:continue
   tc2=random.randint(0,15);lt=rec(20)if tc2>0 else None
   p95v=f"{p95}"if p95 else"NULL";errv=f"{err}"if err else"NULL";dv=f"{30}"if'劣化'in rn else"NULL"
   S.append(f"INSERT INTO performance_alert_rules(id,name,description,scenario_id,p95_threshold,error_rate_threshold,relative_p95_degradation,notify_webhook,enabled,last_triggered_at,trigger_count,created_at,updated_at)VALUES({arid},'{rn}','监控性能',{sid},{p95v},{errv},{dv},'https://oapi.dingtalk.com/robot/send?access_token=xxx',true,{v(lt)},{tc2},'{past(5)}','{rec(3)}')ON CONFLICT(id)DO NOTHING;")
   arid+=1
# ALERT LOGS
for i in range(35):
 metric=random.choice(['p95_response_time','error_rate','rps']);th=round(random.uniform(100,2000),1);ac=round(th*random.uniform(1.1,2.0),1)
 S.append(f"INSERT INTO performance_alert_logs(rule_id,result_id,alert_type,metric_name,threshold_value,actual_value,message,notification_sent,created_at)VALUES({random.randint(1,max(1,arid-1))},{random.randint(1,max(1,rrid-1))},'absolute','{metric}',{th},{ac},'{e(f'告警:{metric}={ac}>{th}')}',{str(random.random()>.1).lower()},'{past(4)}');")
# VISUAL BASELINES
vbid=1
for pid in range(1,17):
 if random.random()<.5:continue
 for step in range(random.randint(2,5)):
  S.append(f"INSERT INTO visual_baselines(id,test_case_id,test_type,project_id,step_index,step_name,baseline_image_path,viewport_width,viewport_height,status,version,approved_by,approved_at,created_at,updated_at)VALUES({vbid},{random.randint(1,100)},'web',{pid},{step},'步骤{step+1}','/baselines/p{pid}/s{step}.png',1920,1080,'active',{random.randint(1,5)},1,'{past(3)}','{past(6)}','{rec(3)}')ON CONFLICT(id)DO NOTHING;")
  vbid+=1
# VISUAL DIFFS
for i in range(20):
 dp=round(random.uniform(0,15),2);st='visual_pass'if dp<5 else random.choice(['visual_fail','approved'])
 S.append(f"INSERT INTO visual_diffs(test_run_id,baseline_id,test_case_id,test_type,step_index,step_name,current_image_path,diff_image_path,diff_percentage,diff_pixel_count,total_pixel_count,similarity_score,viewport_width,viewport_height,threshold,status,created_at,updated_at)VALUES({random.randint(5,max(5,run_id-1))},{random.randint(1,max(1,vbid-1))},{random.randint(1,100)},'web',{random.randint(0,4)},'页面截图','/runs/cur.png','/runs/diff.png',{dp},{random.randint(100,10000)},{1920*1080},{round(1-dp/100,3)},1920,1080,5.0,'{st}','{past(4)}','{rec(2)}');")
# AUDIT LOGS
acts=[('login','user'),('logout','user'),('create','project'),('update','project'),('create','test_case'),('create','test_run'),('create','environment'),('create','organization'),('export','report')]
ips=['192.168.1.100','192.168.1.101','10.0.0.50','10.0.0.51','172.16.0.10','223.5.5.5']
uas=['Mozilla/5.0 Windows Chrome/120','Mozilla/5.0 Mac Safari/605','Mozilla/5.0 iPhone Mobile']
for i in range(200):
 uid=random.choice([1,2,5,6,7,8,9,10]);act,res=random.choice(acts);rid3=random.randint(1,50);oid=random.choice([1,2,3,4,5])
 S.append(f"INSERT INTO audit_logs(user_id,organization_id,action,resource_type,resource_id,changes,ip_address,user_agent,created_at)VALUES({uid},{oid},'{act}','{res}',{rid3},'{{}}','{random.choice(ips)}','{random.choice(uas)}','{past(10)}');")
# GITHUB
for i,(ow,repo,uid) in enumerate([(1,'fullscope-backend',1),(2,'fullscope-frontend',1),(3,'user-center',2)]):
 S.append(f"INSERT INTO github_integrations(id,user_id,repo_owner,repo_name,webhook_secret,is_active,created_at,updated_at)VALUES({i+1},{uid},'{ow}','{repo}','whsec_{random.randint(100000,999999)}',true,'{past(8)}','{rec(5)}')ON CONFLICT(id)DO NOTHING;")
# WEBHOOK TOKENS
for pid in range(1,9):
 S.append(f"INSERT INTO webhook_tokens(id,project_id,name,token,is_active,created_at)VALUES({pid},{pid},'Webhook-{pid}','wh_{hashlib.md5(str(pid).encode()).hexdigest()[:16]}',true,'{past(6)}')ON CONFLICT(id)DO NOTHING;")
# SEQS
for sq,vl in[('users_id_seq',55),('organizations_id_seq',10),('organization_members_id_seq',200),('projects_id_seq',20),('environments_id_seq',70),('api_test_collections_id_seq',150),('api_test_cases_id_seq',1000),('web_test_collections_id_seq',50),('web_test_scripts_id_seq',200),('perf_test_scenarios_id_seq',30),('performance_test_results_id_seq',200),('test_runs_id_seq',500),('test_reports_id_seq',200),('test_documents_id_seq',80),('quality_gates_id_seq',30),('quality_gate_evaluations_id_seq',300),('trigger_rules_id_seq',30),('scheduled_tasks_id_seq',30),('api_tokens_id_seq',20),('prompt_versions_id_seq',30),('ai_invocation_logs_id_seq',300),('performance_alert_rules_id_seq',50),('performance_alert_logs_id_seq',60),('visual_baselines_id_seq',50),('visual_diffs_id_seq',40),('audit_logs_id_seq',400),('github_integrations_id_seq',10),('webhook_tokens_id_seq',10)]:
 S.append(f"SELECT setval('{sq}',{vl});")
# WRITE
with open('scripts/seed_data.sql','w',encoding='utf-8')as f:
 f.write('BEGIN;\n\n')
 for s in S:f.write(s.strip()+'\n\n')
 f.write('COMMIT;\n')
print(f"Generated {len(S)} SQL statements -> scripts/seed_data.sql")
