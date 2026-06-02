INSERT INTO users(id,username,email,password_hash,avatar,role,is_active,created_at,last_login)VALUES(5,'alex.zhang','alex.zhang@163.com','scrypt:32768:8:1$WndhvdorMtHoID7P$fed763d0110cc7fa9d4edd4358ecf19a65ede4f828c813e5562d9fe501f336c97a0a58503f0d82dace43f082b2a6b1f69e360a019b92cefdadae7749f97ddb00','https://api.dicebear.com/7.x/avataaars/svg?seed=alex.zhang','admin',true,'2026-05-19 10:43:00','2026-05-30 10:54:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO users(id,username,email,password_hash,avatar,role,is_active,created_at,last_login)VALUES(6,'linda.wang','linda.wang@meituan.com','scrypt:32768:8:1$WndhvdorMtHoID7P$fed763d0110cc7fa9d4edd4358ecf19a65ede4f828c813e5562d9fe501f336c97a0a58503f0d82dace43f082b2a6b1f69e360a019b92cefdadae7749f97ddb00',NULL,'admin',true,'2026-04-17 15:33:00',NULL)ON CONFLICT(id)DO NOTHING;

INSERT INTO users(id,username,email,password_hash,avatar,role,is_active,created_at,last_login)VALUES(7,'kevin.li','kevin.li@outlook.com','scrypt:32768:8:1$WndhvdorMtHoID7P$fed763d0110cc7fa9d4edd4358ecf19a65ede4f828c813e5562d9fe501f336c97a0a58503f0d82dace43f082b2a6b1f69e360a019b92cefdadae7749f97ddb00','https://api.dicebear.com/7.x/avataaars/svg?seed=kevin.li','admin',true,'2025-09-15 14:59:00','2026-05-27 02:32:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO users(id,username,email,password_hash,avatar,role,is_active,created_at,last_login)VALUES(8,'sarah.zhao','sarah.zhao@qq.com','scrypt:32768:8:1$WndhvdorMtHoID7P$fed763d0110cc7fa9d4edd4358ecf19a65ede4f828c813e5562d9fe501f336c97a0a58503f0d82dace43f082b2a6b1f69e360a019b92cefdadae7749f97ddb00','https://api.dicebear.com/7.x/avataaars/svg?seed=sarah.zhao','admin',true,'2026-03-11 11:33:00','2026-05-31 03:12:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO users(id,username,email,password_hash,avatar,role,is_active,created_at,last_login)VALUES(9,'mike.liu','mike.liu@163.com','scrypt:32768:8:1$WndhvdorMtHoID7P$fed763d0110cc7fa9d4edd4358ecf19a65ede4f828c813e5562d9fe501f336c97a0a58503f0d82dace43f082b2a6b1f69e360a019b92cefdadae7749f97ddb00','https://api.dicebear.com/7.x/avataaars/svg?seed=mike.liu','admin',true,'2025-11-19 06:38:00','2026-05-29 08:14:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO users(id,username,email,password_hash,avatar,role,is_active,created_at,last_login)VALUES(10,'emma.chen','emma.chen@163.com','scrypt:32768:8:1$WndhvdorMtHoID7P$fed763d0110cc7fa9d4edd4358ecf19a65ede4f828c813e5562d9fe501f336c97a0a58503f0d82dace43f082b2a6b1f69e360a019b92cefdadae7749f97ddb00','https://api.dicebear.com/7.x/avataaars/svg?seed=emma.chen','viewer',true,'2026-04-21 16:42:00','2026-05-27 15:48:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO users(id,username,email,password_hash,avatar,role,is_active,created_at,last_login)VALUES(11,'david.yang','david.yang@qq.com','scrypt:32768:8:1$WndhvdorMtHoID7P$fed763d0110cc7fa9d4edd4358ecf19a65ede4f828c813e5562d9fe501f336c97a0a58503f0d82dace43f082b2a6b1f69e360a019b92cefdadae7749f97ddb00','https://api.dicebear.com/7.x/avataaars/svg?seed=david.yang','member',true,'2026-01-04 07:06:00','2026-05-31 21:43:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO users(id,username,email,password_hash,avatar,role,is_active,created_at,last_login)VALUES(12,'lisa.huang','lisa.huang@alibaba-inc.com','scrypt:32768:8:1$WndhvdorMtHoID7P$fed763d0110cc7fa9d4edd4358ecf19a65ede4f828c813e5562d9fe501f336c97a0a58503f0d82dace43f082b2a6b1f69e360a019b92cefdadae7749f97ddb00',NULL,'member',true,'2025-11-23 22:47:00','2026-05-31 14:20:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO users(id,username,email,password_hash,avatar,role,is_active,created_at,last_login)VALUES(13,'james.zhou','james.zhou@outlook.com','scrypt:32768:8:1$WndhvdorMtHoID7P$fed763d0110cc7fa9d4edd4358ecf19a65ede4f828c813e5562d9fe501f336c97a0a58503f0d82dace43f082b2a6b1f69e360a019b92cefdadae7749f97ddb00','https://api.dicebear.com/7.x/avataaars/svg?seed=james.zhou','member',true,'2025-10-07 21:43:00','2026-05-29 12:40:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO users(id,username,email,password_hash,avatar,role,is_active,created_at,last_login)VALUES(14,'anna.wu','anna.wu@qq.com','scrypt:32768:8:1$WndhvdorMtHoID7P$fed763d0110cc7fa9d4edd4358ecf19a65ede4f828c813e5562d9fe501f336c97a0a58503f0d82dace43f082b2a6b1f69e360a019b92cefdadae7749f97ddb00','https://api.dicebear.com/7.x/avataaars/svg?seed=anna.wu','member',true,'2026-05-15 23:35:00','2026-05-29 15:04:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO users(id,username,email,password_hash,avatar,role,is_active,created_at,last_login)VALUES(15,'tom.xu','tom.xu@outlook.com','scrypt:32768:8:1$WndhvdorMtHoID7P$fed763d0110cc7fa9d4edd4358ecf19a65ede4f828c813e5562d9fe501f336c97a0a58503f0d82dace43f082b2a6b1f69e360a019b92cefdadae7749f97ddb00',NULL,'viewer',true,'2025-11-10 13:31:00',NULL)ON CONFLICT(id)DO NOTHING;

INSERT INTO users(id,username,email,password_hash,avatar,role,is_active,created_at,last_login)VALUES(16,'jenny.sun','jenny.sun@meituan.com','scrypt:32768:8:1$WndhvdorMtHoID7P$fed763d0110cc7fa9d4edd4358ecf19a65ede4f828c813e5562d9fe501f336c97a0a58503f0d82dace43f082b2a6b1f69e360a019b92cefdadae7749f97ddb00','https://api.dicebear.com/7.x/avataaars/svg?seed=jenny.sun','member',true,'2025-08-05 20:03:00','2026-05-28 02:52:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO users(id,username,email,password_hash,avatar,role,is_active,created_at,last_login)VALUES(17,'bob.ma','bob.ma@163.com','scrypt:32768:8:1$WndhvdorMtHoID7P$fed763d0110cc7fa9d4edd4358ecf19a65ede4f828c813e5562d9fe501f336c97a0a58503f0d82dace43f082b2a6b1f69e360a019b92cefdadae7749f97ddb00','https://api.dicebear.com/7.x/avataaars/svg?seed=bob.ma','member',true,'2026-04-06 05:20:00',NULL)ON CONFLICT(id)DO NOTHING;

INSERT INTO users(id,username,email,password_hash,avatar,role,is_active,created_at,last_login)VALUES(18,'amy.zhu','amy.zhu@jd.com','scrypt:32768:8:1$WndhvdorMtHoID7P$fed763d0110cc7fa9d4edd4358ecf19a65ede4f828c813e5562d9fe501f336c97a0a58503f0d82dace43f082b2a6b1f69e360a019b92cefdadae7749f97ddb00','https://api.dicebear.com/7.x/avataaars/svg?seed=amy.zhu','member',true,'2025-11-15 21:22:00','2026-05-28 16:05:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO users(id,username,email,password_hash,avatar,role,is_active,created_at,last_login)VALUES(19,'jack.hu','jack.hu@163.com','scrypt:32768:8:1$WndhvdorMtHoID7P$fed763d0110cc7fa9d4edd4358ecf19a65ede4f828c813e5562d9fe501f336c97a0a58503f0d82dace43f082b2a6b1f69e360a019b92cefdadae7749f97ddb00','https://api.dicebear.com/7.x/avataaars/svg?seed=jack.hu','member',true,'2025-07-07 23:53:00','2026-05-30 20:00:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO users(id,username,email,password_hash,avatar,role,is_active,created_at,last_login)VALUES(20,'lucy.guo','lucy.guo@foxmail.com','scrypt:32768:8:1$WndhvdorMtHoID7P$fed763d0110cc7fa9d4edd4358ecf19a65ede4f828c813e5562d9fe501f336c97a0a58503f0d82dace43f082b2a6b1f69e360a019b92cefdadae7749f97ddb00','https://api.dicebear.com/7.x/avataaars/svg?seed=lucy.guo','member',true,'2025-09-15 06:05:00','2026-05-30 05:37:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO users(id,username,email,password_hash,avatar,role,is_active,created_at,last_login)VALUES(21,'henry.lin','henry.lin@meituan.com','scrypt:32768:8:1$WndhvdorMtHoID7P$fed763d0110cc7fa9d4edd4358ecf19a65ede4f828c813e5562d9fe501f336c97a0a58503f0d82dace43f082b2a6b1f69e360a019b92cefdadae7749f97ddb00','https://api.dicebear.com/7.x/avataaars/svg?seed=henry.lin','member',true,'2025-07-29 23:29:00',NULL)ON CONFLICT(id)DO NOTHING;

INSERT INTO users(id,username,email,password_hash,avatar,role,is_active,created_at,last_login)VALUES(22,'grace.he','grace.he@foxmail.com','scrypt:32768:8:1$WndhvdorMtHoID7P$fed763d0110cc7fa9d4edd4358ecf19a65ede4f828c813e5562d9fe501f336c97a0a58503f0d82dace43f082b2a6b1f69e360a019b92cefdadae7749f97ddb00','https://api.dicebear.com/7.x/avataaars/svg?seed=grace.he','member',true,'2026-05-03 02:04:00','2026-06-01 07:14:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO users(id,username,email,password_hash,avatar,role,is_active,created_at,last_login)VALUES(23,'peter.gao','peter.gao@163.com','scrypt:32768:8:1$WndhvdorMtHoID7P$fed763d0110cc7fa9d4edd4358ecf19a65ede4f828c813e5562d9fe501f336c97a0a58503f0d82dace43f082b2a6b1f69e360a019b92cefdadae7749f97ddb00','https://api.dicebear.com/7.x/avataaars/svg?seed=peter.gao','member',true,'2026-03-27 12:30:00','2026-05-31 01:27:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO users(id,username,email,password_hash,avatar,role,is_active,created_at,last_login)VALUES(24,'kate.luo','kate.luo@tencent.com','scrypt:32768:8:1$WndhvdorMtHoID7P$fed763d0110cc7fa9d4edd4358ecf19a65ede4f828c813e5562d9fe501f336c97a0a58503f0d82dace43f082b2a6b1f69e360a019b92cefdadae7749f97ddb00','https://api.dicebear.com/7.x/avataaars/svg?seed=kate.luo','member',true,'2025-08-28 10:16:00','2026-05-28 21:18:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO users(id,username,email,password_hash,avatar,role,is_active,created_at,last_login)VALUES(25,'sam.liang','sam.liang@bytedance.com','scrypt:32768:8:1$WndhvdorMtHoID7P$fed763d0110cc7fa9d4edd4358ecf19a65ede4f828c813e5562d9fe501f336c97a0a58503f0d82dace43f082b2a6b1f69e360a019b92cefdadae7749f97ddb00',NULL,'viewer',true,'2026-04-01 02:46:00',NULL)ON CONFLICT(id)DO NOTHING;

INSERT INTO users(id,username,email,password_hash,avatar,role,is_active,created_at,last_login)VALUES(26,'julia.song','julia.song@meituan.com','scrypt:32768:8:1$WndhvdorMtHoID7P$fed763d0110cc7fa9d4edd4358ecf19a65ede4f828c813e5562d9fe501f336c97a0a58503f0d82dace43f082b2a6b1f69e360a019b92cefdadae7749f97ddb00','https://api.dicebear.com/7.x/avataaars/svg?seed=julia.song','member',true,'2025-08-04 03:00:00',NULL)ON CONFLICT(id)DO NOTHING;

INSERT INTO users(id,username,email,password_hash,avatar,role,is_active,created_at,last_login)VALUES(27,'frank.zheng','frank.zheng@outlook.com','scrypt:32768:8:1$WndhvdorMtHoID7P$fed763d0110cc7fa9d4edd4358ecf19a65ede4f828c813e5562d9fe501f336c97a0a58503f0d82dace43f082b2a6b1f69e360a019b92cefdadae7749f97ddb00',NULL,'member',true,'2026-05-15 23:56:00','2026-05-28 12:29:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO users(id,username,email,password_hash,avatar,role,is_active,created_at,last_login)VALUES(28,'helen.xie','helen.xie@gmail.com','scrypt:32768:8:1$WndhvdorMtHoID7P$fed763d0110cc7fa9d4edd4358ecf19a65ede4f828c813e5562d9fe501f336c97a0a58503f0d82dace43f082b2a6b1f69e360a019b92cefdadae7749f97ddb00','https://api.dicebear.com/7.x/avataaars/svg?seed=helen.xie','viewer',true,'2026-01-27 18:09:00','2026-06-01 06:18:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO users(id,username,email,password_hash,avatar,role,is_active,created_at,last_login)VALUES(29,'leo.han','leo.han@tencent.com','scrypt:32768:8:1$WndhvdorMtHoID7P$fed763d0110cc7fa9d4edd4358ecf19a65ede4f828c813e5562d9fe501f336c97a0a58503f0d82dace43f082b2a6b1f69e360a019b92cefdadae7749f97ddb00','https://api.dicebear.com/7.x/avataaars/svg?seed=leo.han','viewer',true,'2025-10-04 10:57:00','2026-06-01 08:35:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO users(id,username,email,password_hash,avatar,role,is_active,created_at,last_login)VALUES(30,'ruby.tang','ruby.tang@163.com','scrypt:32768:8:1$WndhvdorMtHoID7P$fed763d0110cc7fa9d4edd4358ecf19a65ede4f828c813e5562d9fe501f336c97a0a58503f0d82dace43f082b2a6b1f69e360a019b92cefdadae7749f97ddb00','https://api.dicebear.com/7.x/avataaars/svg?seed=ruby.tang','member',true,'2026-02-23 03:26:00','2026-05-27 04:43:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO users(id,username,email,password_hash,avatar,role,is_active,created_at,last_login)VALUES(31,'oscar.feng','oscar.feng@163.com','scrypt:32768:8:1$WndhvdorMtHoID7P$fed763d0110cc7fa9d4edd4358ecf19a65ede4f828c813e5562d9fe501f336c97a0a58503f0d82dace43f082b2a6b1f69e360a019b92cefdadae7749f97ddb00','https://api.dicebear.com/7.x/avataaars/svg?seed=oscar.feng','viewer',true,'2025-08-24 06:57:00','2026-06-02 07:01:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO users(id,username,email,password_hash,avatar,role,is_active,created_at,last_login)VALUES(32,'iris.dong','iris.dong@outlook.com','scrypt:32768:8:1$WndhvdorMtHoID7P$fed763d0110cc7fa9d4edd4358ecf19a65ede4f828c813e5562d9fe501f336c97a0a58503f0d82dace43f082b2a6b1f69e360a019b92cefdadae7749f97ddb00','https://api.dicebear.com/7.x/avataaars/svg?seed=iris.dong','member',true,'2025-11-04 18:30:00','2026-05-27 08:50:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO users(id,username,email,password_hash,avatar,role,is_active,created_at,last_login)VALUES(33,'max.xiao','max.xiao@tencent.com','scrypt:32768:8:1$WndhvdorMtHoID7P$fed763d0110cc7fa9d4edd4358ecf19a65ede4f828c813e5562d9fe501f336c97a0a58503f0d82dace43f082b2a6b1f69e360a019b92cefdadae7749f97ddb00',NULL,'member',true,'2025-10-12 00:33:00','2026-05-26 05:48:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO users(id,username,email,password_hash,avatar,role,is_active,created_at,last_login)VALUES(34,'chloe.cheng','chloe.cheng@qq.com','scrypt:32768:8:1$WndhvdorMtHoID7P$fed763d0110cc7fa9d4edd4358ecf19a65ede4f828c813e5562d9fe501f336c97a0a58503f0d82dace43f082b2a6b1f69e360a019b92cefdadae7749f97ddb00',NULL,'member',true,'2025-12-23 08:57:00','2026-05-31 08:28:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO users(id,username,email,password_hash,avatar,role,is_active,created_at,last_login)VALUES(35,'eric.cao','eric.cao@gmail.com','scrypt:32768:8:1$WndhvdorMtHoID7P$fed763d0110cc7fa9d4edd4358ecf19a65ede4f828c813e5562d9fe501f336c97a0a58503f0d82dace43f082b2a6b1f69e360a019b92cefdadae7749f97ddb00','https://api.dicebear.com/7.x/avataaars/svg?seed=eric.cao','member',true,'2025-08-01 07:17:00','2026-05-27 06:04:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO users(id,username,email,password_hash,avatar,role,is_active,created_at,last_login)VALUES(36,'vivian.yuan','vivian.yuan@jd.com','scrypt:32768:8:1$WndhvdorMtHoID7P$fed763d0110cc7fa9d4edd4358ecf19a65ede4f828c813e5562d9fe501f336c97a0a58503f0d82dace43f082b2a6b1f69e360a019b92cefdadae7749f97ddb00','https://api.dicebear.com/7.x/avataaars/svg?seed=vivian.yuan','member',true,'2025-07-19 07:34:00','2026-05-28 01:47:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO users(id,username,email,password_hash,avatar,role,is_active,created_at,last_login)VALUES(37,'ryan.deng','ryan.deng@alibaba-inc.com','scrypt:32768:8:1$WndhvdorMtHoID7P$fed763d0110cc7fa9d4edd4358ecf19a65ede4f828c813e5562d9fe501f336c97a0a58503f0d82dace43f082b2a6b1f69e360a019b92cefdadae7749f97ddb00','https://api.dicebear.com/7.x/avataaars/svg?seed=ryan.deng','member',true,'2026-01-16 21:52:00','2026-05-28 19:40:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO users(id,username,email,password_hash,avatar,role,is_active,created_at,last_login)VALUES(38,'natalie.xu','natalie.xu@163.com','scrypt:32768:8:1$WndhvdorMtHoID7P$fed763d0110cc7fa9d4edd4358ecf19a65ede4f828c813e5562d9fe501f336c97a0a58503f0d82dace43f082b2a6b1f69e360a019b92cefdadae7749f97ddb00','https://api.dicebear.com/7.x/avataaars/svg?seed=natalie.xu','member',true,'2025-10-09 14:24:00','2026-05-31 16:47:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO users(id,username,email,password_hash,avatar,role,is_active,created_at,last_login)VALUES(39,'adam.fu','adam.fu@gmail.com','scrypt:32768:8:1$WndhvdorMtHoID7P$fed763d0110cc7fa9d4edd4358ecf19a65ede4f828c813e5562d9fe501f336c97a0a58503f0d82dace43f082b2a6b1f69e360a019b92cefdadae7749f97ddb00','https://api.dicebear.com/7.x/avataaars/svg?seed=adam.fu','member',true,'2026-04-27 02:37:00','2026-05-25 16:15:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO users(id,username,email,password_hash,avatar,role,is_active,created_at,last_login)VALUES(40,'sophia.shen','sophia.shen@meituan.com','scrypt:32768:8:1$WndhvdorMtHoID7P$fed763d0110cc7fa9d4edd4358ecf19a65ede4f828c813e5562d9fe501f336c97a0a58503f0d82dace43f082b2a6b1f69e360a019b92cefdadae7749f97ddb00',NULL,'member',true,'2025-06-24 16:41:00','2026-06-01 05:44:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO users(id,username,email,password_hash,avatar,role,is_active,created_at,last_login)VALUES(41,'jason.peng','jason.peng@163.com','scrypt:32768:8:1$WndhvdorMtHoID7P$fed763d0110cc7fa9d4edd4358ecf19a65ede4f828c813e5562d9fe501f336c97a0a58503f0d82dace43f082b2a6b1f69e360a019b92cefdadae7749f97ddb00','https://api.dicebear.com/7.x/avataaars/svg?seed=jason.peng','member',true,'2026-01-13 00:22:00','2026-05-28 03:17:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO users(id,username,email,password_hash,avatar,role,is_active,created_at,last_login)VALUES(42,'cindy.lv','cindy.lv@foxmail.com','scrypt:32768:8:1$WndhvdorMtHoID7P$fed763d0110cc7fa9d4edd4358ecf19a65ede4f828c813e5562d9fe501f336c97a0a58503f0d82dace43f082b2a6b1f69e360a019b92cefdadae7749f97ddb00','https://api.dicebear.com/7.x/avataaars/svg?seed=cindy.lv','viewer',true,'2026-01-24 08:55:00','2026-05-29 09:00:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO users(id,username,email,password_hash,avatar,role,is_active,created_at,last_login)VALUES(43,'nick.su','nick.su@gmail.com','scrypt:32768:8:1$WndhvdorMtHoID7P$fed763d0110cc7fa9d4edd4358ecf19a65ede4f828c813e5562d9fe501f336c97a0a58503f0d82dace43f082b2a6b1f69e360a019b92cefdadae7749f97ddb00',NULL,'member',true,'2026-03-10 10:32:00','2026-05-26 17:00:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO users(id,username,email,password_hash,avatar,role,is_active,created_at,last_login)VALUES(44,'mia.lu','mia.lu@gmail.com','scrypt:32768:8:1$WndhvdorMtHoID7P$fed763d0110cc7fa9d4edd4358ecf19a65ede4f828c813e5562d9fe501f336c97a0a58503f0d82dace43f082b2a6b1f69e360a019b92cefdadae7749f97ddb00',NULL,'member',true,'2025-11-23 15:25:00',NULL)ON CONFLICT(id)DO NOTHING;

INSERT INTO users(id,username,email,password_hash,avatar,role,is_active,created_at,last_login)VALUES(45,'chris.jiang','chris.jiang@foxmail.com','scrypt:32768:8:1$WndhvdorMtHoID7P$fed763d0110cc7fa9d4edd4358ecf19a65ede4f828c813e5562d9fe501f336c97a0a58503f0d82dace43f082b2a6b1f69e360a019b92cefdadae7749f97ddb00','https://api.dicebear.com/7.x/avataaars/svg?seed=chris.jiang','member',true,'2026-05-11 22:47:00','2026-05-31 22:11:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO users(id,username,email,password_hash,avatar,role,is_active,created_at,last_login)VALUES(46,'penny.cai','penny.cai@tencent.com','scrypt:32768:8:1$WndhvdorMtHoID7P$fed763d0110cc7fa9d4edd4358ecf19a65ede4f828c813e5562d9fe501f336c97a0a58503f0d82dace43f082b2a6b1f69e360a019b92cefdadae7749f97ddb00','https://api.dicebear.com/7.x/avataaars/svg?seed=penny.cai','member',true,'2026-01-31 04:09:00','2026-05-27 09:49:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO users(id,username,email,password_hash,avatar,role,is_active,created_at,last_login)VALUES(47,'derek.jia','derek.jia@alibaba-inc.com','scrypt:32768:8:1$WndhvdorMtHoID7P$fed763d0110cc7fa9d4edd4358ecf19a65ede4f828c813e5562d9fe501f336c97a0a58503f0d82dace43f082b2a6b1f69e360a019b92cefdadae7749f97ddb00','https://api.dicebear.com/7.x/avataaars/svg?seed=derek.jia','viewer',true,'2025-06-23 10:09:00','2026-05-30 11:54:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO users(id,username,email,password_hash,avatar,role,is_active,created_at,last_login)VALUES(48,'vanessa.ding','vanessa.ding@qq.com','scrypt:32768:8:1$WndhvdorMtHoID7P$fed763d0110cc7fa9d4edd4358ecf19a65ede4f828c813e5562d9fe501f336c97a0a58503f0d82dace43f082b2a6b1f69e360a019b92cefdadae7749f97ddb00','https://api.dicebear.com/7.x/avataaars/svg?seed=vanessa.ding','viewer',true,'2026-02-08 03:08:00','2026-05-28 00:08:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO users(id,username,email,password_hash,avatar,role,is_active,created_at,last_login)VALUES(49,'bruce.wei','bruce.wei@outlook.com','scrypt:32768:8:1$WndhvdorMtHoID7P$fed763d0110cc7fa9d4edd4358ecf19a65ede4f828c813e5562d9fe501f336c97a0a58503f0d82dace43f082b2a6b1f69e360a019b92cefdadae7749f97ddb00',NULL,'member',true,'2026-05-19 12:48:00','2026-05-29 07:11:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO users(id,username,email,password_hash,avatar,role,is_active,created_at,last_login)VALUES(50,'alice.xue','alice.xue@meituan.com','scrypt:32768:8:1$WndhvdorMtHoID7P$fed763d0110cc7fa9d4edd4358ecf19a65ede4f828c813e5562d9fe501f336c97a0a58503f0d82dace43f082b2a6b1f69e360a019b92cefdadae7749f97ddb00','https://api.dicebear.com/7.x/avataaars/svg?seed=alice.xue','viewer',true,'2025-06-18 16:39:00','2026-06-01 01:49:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO users(id,username,email,password_hash,avatar,role,is_active,created_at,last_login)VALUES(51,'gavin.ye','gavin.ye@foxmail.com','scrypt:32768:8:1$WndhvdorMtHoID7P$fed763d0110cc7fa9d4edd4358ecf19a65ede4f828c813e5562d9fe501f336c97a0a58503f0d82dace43f082b2a6b1f69e360a019b92cefdadae7749f97ddb00','https://api.dicebear.com/7.x/avataaars/svg?seed=gavin.ye','member',true,'2026-04-06 14:33:00','2026-05-27 20:22:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO users(id,username,email,password_hash,avatar,role,is_active,created_at,last_login)VALUES(52,'monica.yan','monica.yan@163.com','scrypt:32768:8:1$WndhvdorMtHoID7P$fed763d0110cc7fa9d4edd4358ecf19a65ede4f828c813e5562d9fe501f336c97a0a58503f0d82dace43f082b2a6b1f69e360a019b92cefdadae7749f97ddb00','https://api.dicebear.com/7.x/avataaars/svg?seed=monica.yan','viewer',true,'2025-08-10 03:44:00',NULL)ON CONFLICT(id)DO NOTHING;

INSERT INTO users(id,username,email,password_hash,avatar,role,is_active,created_at,last_login)VALUES(53,'raymond.yu','raymond.yu@meituan.com','scrypt:32768:8:1$WndhvdorMtHoID7P$fed763d0110cc7fa9d4edd4358ecf19a65ede4f828c813e5562d9fe501f336c97a0a58503f0d82dace43f082b2a6b1f69e360a019b92cefdadae7749f97ddb00','https://api.dicebear.com/7.x/avataaars/svg?seed=raymond.yu','member',true,'2025-11-26 20:56:00','2026-05-27 14:40:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO users(id,username,email,password_hash,avatar,role,is_active,created_at,last_login)VALUES(54,'wendy.fan','wendy.fan@163.com','scrypt:32768:8:1$WndhvdorMtHoID7P$fed763d0110cc7fa9d4edd4358ecf19a65ede4f828c813e5562d9fe501f336c97a0a58503f0d82dace43f082b2a6b1f69e360a019b92cefdadae7749f97ddb00','https://api.dicebear.com/7.x/avataaars/svg?seed=wendy.fan','member',true,'2025-09-15 00:18:00','2026-05-26 11:42:00')ON CONFLICT(id)DO NOTHING;

UPDATE users SET role='admin'WHERE id=1;

UPDATE users SET role='admin'WHERE id=2;

INSERT INTO organizations(id,name,slug,description,owner_id,is_active,created_at,updated_at)VALUES(2,'星辰科技','startech','企业级SaaS',2,true,'2025-10-28 12:36:00','2026-03-03 14:24:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO organizations(id,name,slug,description,owner_id,is_active,created_at,updated_at)VALUES(3,'云桥信息','yunbridge','金融科技',5,true,'2025-11-05 16:07:00','2026-06-01 00:42:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO organizations(id,name,slug,description,owner_id,is_active,created_at,updated_at)VALUES(4,'锐智软件','ruizhi','电商平台',2,true,'2025-10-23 15:22:00','2025-12-18 19:32:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO organizations(id,name,slug,description,owner_id,is_active,created_at,updated_at)VALUES(5,'蓝鲸数据','lanjing','大数据',6,true,'2026-02-11 17:30:00','2026-03-06 12:55:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO organizations(id,name,slug,description,owner_id,is_active,created_at,updated_at)VALUES(6,'飞鸟网络','feiniao','社交内容',5,true,'2025-09-10 12:20:00','2025-12-12 07:08:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO organizations(id,name,slug,description,owner_id,is_active,created_at,updated_at)VALUES(7,'铁壁安全','tiebi','网络安全',2,true,'2025-12-25 02:09:00','2026-02-20 05:59:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO organizations(id,name,slug,description,owner_id,is_active,created_at,updated_at)VALUES(8,'灵犀AI','lingxi','人工智能',1,true,'2026-01-26 18:21:00','2026-04-24 19:34:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO organizations(id,name,slug,description,owner_id,is_active,created_at,updated_at)VALUES(9,'翠竹教育','cuizhu','在线教育',7,true,'2026-02-21 11:16:00','2025-11-16 18:35:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO organization_members(id,organization_id,user_id,role,is_active,created_at)VALUES(1,2,2,'owner',true,'2026-03-17 13:16:00')ON CONFLICT DO NOTHING;

INSERT INTO organization_members(id,organization_id,user_id,role,is_active,created_at)VALUES(2,2,53,'viewer',true,'2026-04-06 04:09:00')ON CONFLICT DO NOTHING;

INSERT INTO organization_members(id,organization_id,user_id,role,is_active,created_at)VALUES(3,2,54,'viewer',true,'2026-05-19 16:45:00')ON CONFLICT DO NOTHING;

INSERT INTO organization_members(id,organization_id,user_id,role,is_active,created_at)VALUES(4,2,11,'admin',true,'2026-02-05 05:09:00')ON CONFLICT DO NOTHING;

INSERT INTO organization_members(id,organization_id,user_id,role,is_active,created_at)VALUES(5,3,6,'owner',true,'2025-09-02 16:22:00')ON CONFLICT DO NOTHING;

INSERT INTO organization_members(id,organization_id,user_id,role,is_active,created_at)VALUES(6,3,53,'viewer',true,'2025-10-31 16:32:00')ON CONFLICT DO NOTHING;

INSERT INTO organization_members(id,organization_id,user_id,role,is_active,created_at)VALUES(7,3,33,'member',true,'2025-11-22 18:32:00')ON CONFLICT DO NOTHING;

INSERT INTO organization_members(id,organization_id,user_id,role,is_active,created_at)VALUES(8,3,44,'member',true,'2025-11-21 02:07:00')ON CONFLICT DO NOTHING;

INSERT INTO organization_members(id,organization_id,user_id,role,is_active,created_at)VALUES(9,3,51,'member',true,'2025-11-16 17:29:00')ON CONFLICT DO NOTHING;

INSERT INTO organization_members(id,organization_id,user_id,role,is_active,created_at)VALUES(10,3,37,'member',true,'2026-03-22 19:56:00')ON CONFLICT DO NOTHING;

INSERT INTO organization_members(id,organization_id,user_id,role,is_active,created_at)VALUES(11,4,5,'owner',true,'2026-02-01 01:39:00')ON CONFLICT DO NOTHING;

INSERT INTO organization_members(id,organization_id,user_id,role,is_active,created_at)VALUES(12,4,39,'viewer',true,'2025-12-06 05:15:00')ON CONFLICT DO NOTHING;

INSERT INTO organization_members(id,organization_id,user_id,role,is_active,created_at)VALUES(13,4,10,'member',true,'2026-05-15 20:34:00')ON CONFLICT DO NOTHING;

INSERT INTO organization_members(id,organization_id,user_id,role,is_active,created_at)VALUES(14,4,13,'member',true,'2026-01-13 19:34:00')ON CONFLICT DO NOTHING;

INSERT INTO organization_members(id,organization_id,user_id,role,is_active,created_at)VALUES(15,4,14,'admin',true,'2026-04-09 20:36:00')ON CONFLICT DO NOTHING;

INSERT INTO organization_members(id,organization_id,user_id,role,is_active,created_at)VALUES(16,4,19,'admin',true,'2025-10-24 15:36:00')ON CONFLICT DO NOTHING;

INSERT INTO organization_members(id,organization_id,user_id,role,is_active,created_at)VALUES(17,5,6,'owner',true,'2026-05-28 22:41:00')ON CONFLICT DO NOTHING;

INSERT INTO organization_members(id,organization_id,user_id,role,is_active,created_at)VALUES(18,5,31,'viewer',true,'2026-04-06 01:33:00')ON CONFLICT DO NOTHING;

INSERT INTO organization_members(id,organization_id,user_id,role,is_active,created_at)VALUES(19,5,39,'viewer',true,'2026-05-24 21:39:00')ON CONFLICT DO NOTHING;

INSERT INTO organization_members(id,organization_id,user_id,role,is_active,created_at)VALUES(20,5,52,'viewer',true,'2025-11-28 04:07:00')ON CONFLICT DO NOTHING;

INSERT INTO organization_members(id,organization_id,user_id,role,is_active,created_at)VALUES(21,5,53,'viewer',true,'2025-10-09 05:21:00')ON CONFLICT DO NOTHING;

INSERT INTO organization_members(id,organization_id,user_id,role,is_active,created_at)VALUES(22,5,43,'admin',true,'2025-10-11 21:23:00')ON CONFLICT DO NOTHING;

INSERT INTO organization_members(id,organization_id,user_id,role,is_active,created_at)VALUES(23,5,19,'admin',true,'2026-05-10 13:33:00')ON CONFLICT DO NOTHING;

INSERT INTO organization_members(id,organization_id,user_id,role,is_active,created_at)VALUES(24,6,2,'owner',true,'2025-10-08 04:57:00')ON CONFLICT DO NOTHING;

INSERT INTO organization_members(id,organization_id,user_id,role,is_active,created_at)VALUES(25,6,29,'viewer',true,'2026-03-21 20:44:00')ON CONFLICT DO NOTHING;

INSERT INTO organization_members(id,organization_id,user_id,role,is_active,created_at)VALUES(26,6,25,'admin',true,'2026-02-01 09:13:00')ON CONFLICT DO NOTHING;

INSERT INTO organization_members(id,organization_id,user_id,role,is_active,created_at)VALUES(27,6,18,'admin',true,'2026-03-04 02:19:00')ON CONFLICT DO NOTHING;

INSERT INTO organization_members(id,organization_id,user_id,role,is_active,created_at)VALUES(28,6,34,'admin',true,'2025-11-13 13:58:00')ON CONFLICT DO NOTHING;

INSERT INTO organization_members(id,organization_id,user_id,role,is_active,created_at)VALUES(29,6,26,'admin',true,'2026-03-30 03:07:00')ON CONFLICT DO NOTHING;

INSERT INTO organization_members(id,organization_id,user_id,role,is_active,created_at)VALUES(30,7,1,'owner',true,'2026-03-15 02:52:00')ON CONFLICT DO NOTHING;

INSERT INTO organization_members(id,organization_id,user_id,role,is_active,created_at)VALUES(31,7,47,'member',true,'2025-11-16 22:50:00')ON CONFLICT DO NOTHING;

INSERT INTO organization_members(id,organization_id,user_id,role,is_active,created_at)VALUES(32,7,12,'admin',true,'2025-11-14 04:41:00')ON CONFLICT DO NOTHING;

INSERT INTO organization_members(id,organization_id,user_id,role,is_active,created_at)VALUES(33,7,41,'admin',true,'2026-01-04 09:01:00')ON CONFLICT DO NOTHING;

INSERT INTO organization_members(id,organization_id,user_id,role,is_active,created_at)VALUES(34,7,18,'member',true,'2026-01-04 12:02:00')ON CONFLICT DO NOTHING;

INSERT INTO organization_members(id,organization_id,user_id,role,is_active,created_at)VALUES(35,7,34,'viewer',true,'2026-02-19 11:48:00')ON CONFLICT DO NOTHING;

INSERT INTO organization_members(id,organization_id,user_id,role,is_active,created_at)VALUES(36,7,49,'admin',true,'2025-12-31 11:07:00')ON CONFLICT DO NOTHING;

INSERT INTO organization_members(id,organization_id,user_id,role,is_active,created_at)VALUES(37,8,2,'owner',true,'2026-04-09 11:11:00')ON CONFLICT DO NOTHING;

INSERT INTO organization_members(id,organization_id,user_id,role,is_active,created_at)VALUES(38,8,48,'member',true,'2026-01-15 20:18:00')ON CONFLICT DO NOTHING;

INSERT INTO organization_members(id,organization_id,user_id,role,is_active,created_at)VALUES(39,8,43,'member',true,'2026-05-14 17:19:00')ON CONFLICT DO NOTHING;

INSERT INTO organization_members(id,organization_id,user_id,role,is_active,created_at)VALUES(40,8,12,'member',true,'2026-05-28 20:08:00')ON CONFLICT DO NOTHING;

INSERT INTO organization_members(id,organization_id,user_id,role,is_active,created_at)VALUES(41,8,41,'viewer',true,'2026-05-04 20:37:00')ON CONFLICT DO NOTHING;

INSERT INTO organization_members(id,organization_id,user_id,role,is_active,created_at)VALUES(42,8,7,'viewer',true,'2025-12-02 05:33:00')ON CONFLICT DO NOTHING;

INSERT INTO organization_members(id,organization_id,user_id,role,is_active,created_at)VALUES(43,9,2,'owner',true,'2025-09-06 13:43:00')ON CONFLICT DO NOTHING;

INSERT INTO organization_members(id,organization_id,user_id,role,is_active,created_at)VALUES(44,9,39,'member',true,'2025-11-01 07:43:00')ON CONFLICT DO NOTHING;

INSERT INTO organization_members(id,organization_id,user_id,role,is_active,created_at)VALUES(45,9,35,'viewer',true,'2026-03-30 19:24:00')ON CONFLICT DO NOTHING;

INSERT INTO organization_members(id,organization_id,user_id,role,is_active,created_at)VALUES(46,9,34,'viewer',true,'2026-03-07 09:29:00')ON CONFLICT DO NOTHING;

INSERT INTO organization_members(id,organization_id,user_id,role,is_active,created_at)VALUES(47,9,32,'member',true,'2026-04-15 18:47:00')ON CONFLICT DO NOTHING;

INSERT INTO organization_members(id,organization_id,user_id,role,is_active,created_at)VALUES(48,9,42,'member',true,'2025-11-09 01:39:00')ON CONFLICT DO NOTHING;

INSERT INTO organization_members(id,organization_id,user_id,role,is_active,created_at)VALUES(49,9,22,'member',true,'2025-10-18 14:16:00')ON CONFLICT DO NOTHING;

INSERT INTO organization_members(id,organization_id,user_id,role,is_active,created_at)VALUES(50,9,25,'member',true,'2026-01-10 09:27:00')ON CONFLICT DO NOTHING;

INSERT INTO organization_members(id,organization_id,user_id,role,is_active,created_at)VALUES(51,1,2,'admin',true,'2026-02-24 07:45:00')ON CONFLICT DO NOTHING;

INSERT INTO organization_members(id,organization_id,user_id,role,is_active,created_at)VALUES(52,1,3,'member',true,'2025-11-04 18:25:00')ON CONFLICT DO NOTHING;

INSERT INTO organization_members(id,organization_id,user_id,role,is_active,created_at)VALUES(53,1,5,'admin',true,'2026-01-28 11:30:00')ON CONFLICT DO NOTHING;

INSERT INTO organization_members(id,organization_id,user_id,role,is_active,created_at)VALUES(54,1,6,'member',true,'2025-09-22 19:10:00')ON CONFLICT DO NOTHING;

INSERT INTO organization_members(id,organization_id,user_id,role,is_active,created_at)VALUES(55,1,7,'member',true,'2026-05-24 07:42:00')ON CONFLICT DO NOTHING;

INSERT INTO organization_members(id,organization_id,user_id,role,is_active,created_at)VALUES(56,1,8,'member',true,'2026-02-07 21:16:00')ON CONFLICT DO NOTHING;

INSERT INTO organization_members(id,organization_id,user_id,role,is_active,created_at)VALUES(57,1,9,'member',true,'2026-01-28 00:18:00')ON CONFLICT DO NOTHING;

INSERT INTO organization_members(id,organization_id,user_id,role,is_active,created_at)VALUES(58,1,10,'member',true,'2025-08-07 22:30:00')ON CONFLICT DO NOTHING;

INSERT INTO projects(id,name,description,owner_id,organization_id,settings,created_at,updated_at)VALUES(2,'用户中心','用户注册登录权限',2,2,'{}','2025-12-06 20:13:00','2026-05-28 23:38:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO projects(id,name,description,owner_id,organization_id,settings,created_at,updated_at)VALUES(3,'订单系统','订单支付退款',3,3,'{}','2025-10-12 01:41:00','2026-05-31 02:53:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO projects(id,name,description,owner_id,organization_id,settings,created_at,updated_at)VALUES(4,'商品管理','商品CRUD库存',4,4,'{}','2026-02-22 23:53:00','2026-05-27 16:12:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO projects(id,name,description,owner_id,organization_id,settings,created_at,updated_at)VALUES(5,'支付网关','聚合支付对账',1,5,'{}','2026-02-27 03:47:00','2026-05-27 18:43:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO projects(id,name,description,owner_id,organization_id,settings,created_at,updated_at)VALUES(6,'消息中心','站内信Push短信',5,6,'{}','2025-09-05 14:42:00','2026-06-02 03:42:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO projects(id,name,description,owner_id,organization_id,settings,created_at,updated_at)VALUES(7,'数据大屏','实时数据可视化',6,7,'{}','2026-02-04 22:49:00','2026-05-31 09:15:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO projects(id,name,description,owner_id,organization_id,settings,created_at,updated_at)VALUES(8,'后台管理','运营管理后台',7,8,'{}','2026-03-29 01:58:00','2026-06-01 16:42:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO projects(id,name,description,owner_id,organization_id,settings,created_at,updated_at)VALUES(9,'移动端H5','H5活动页小程序',8,9,'{}','2026-03-28 13:05:00','2026-05-30 06:05:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO projects(id,name,description,owner_id,organization_id,settings,created_at,updated_at)VALUES(10,'开放平台','API网关文档',9,2,'{}','2026-05-25 15:42:00','2026-05-29 18:32:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO projects(id,name,description,owner_id,organization_id,settings,created_at,updated_at)VALUES(11,'内容审核','AI图文审核',10,3,'{}','2025-12-09 04:57:00','2026-05-30 18:53:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO projects(id,name,description,owner_id,organization_id,settings,created_at,updated_at)VALUES(12,'搜索服务','全文搜索推荐',5,4,'{}','2026-04-28 21:29:00','2026-06-01 15:20:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO projects(id,name,description,owner_id,organization_id,settings,created_at,updated_at)VALUES(13,'营销系统','优惠券秒杀',6,5,'{}','2026-05-05 05:51:00','2026-05-29 00:55:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO projects(id,name,description,owner_id,organization_id,settings,created_at,updated_at)VALUES(14,'BI报表','数据看板查询',7,6,'{}','2026-01-25 06:25:00','2026-05-29 14:22:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO projects(id,name,description,owner_id,organization_id,settings,created_at,updated_at)VALUES(15,'客服系统','工单在线客服',8,7,'{}','2026-02-05 17:36:00','2026-05-29 19:41:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO projects(id,name,description,owner_id,organization_id,settings,created_at,updated_at)VALUES(16,'供应链','采购仓储配送',9,8,'{}','2025-10-25 00:24:00','2026-05-29 08:21:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO environments(id,project_id,name,base_url,variables,headers,is_default,created_at,updated_at)VALUES(1,1,'开发环境','https://dev.example.com','{}','{}',false,' 2025-11-24 06:12:00','2026-05-31 13:47:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO environments(id,project_id,name,base_url,variables,headers,is_default,created_at,updated_at)VALUES(2,1,'测试环境','https://test.example.com','{}','{}',true,' 2026-03-25 12:55:00','2026-06-01 02:49:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO environments(id,project_id,name,base_url,variables,headers,is_default,created_at,updated_at)VALUES(3,1,'预发布','https://staging.example.com','{}','{}',false,' 2026-01-11 07:50:00','2026-06-01 20:32:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO environments(id,project_id,name,base_url,variables,headers,is_default,created_at,updated_at)VALUES(4,1,'生产环境','https://api.example.com','{}','{}',false,' 2025-12-06 14:30:00','2026-05-31 08:46:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO environments(id,project_id,name,base_url,variables,headers,is_default,created_at,updated_at)VALUES(5,2,'开发环境','https://dev.example.com','{}','{}',false,' 2026-03-19 11:42:00','2026-05-30 07:17:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO environments(id,project_id,name,base_url,variables,headers,is_default,created_at,updated_at)VALUES(6,2,'测试环境','https://test.example.com','{}','{}',true,' 2026-04-03 01:10:00','2026-05-31 20:53:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO environments(id,project_id,name,base_url,variables,headers,is_default,created_at,updated_at)VALUES(7,2,'预发布','https://staging.example.com','{}','{}',false,' 2026-01-13 02:19:00','2026-06-01 01:08:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO environments(id,project_id,name,base_url,variables,headers,is_default,created_at,updated_at)VALUES(8,2,'生产环境','https://api.example.com','{}','{}',false,' 2026-04-26 07:57:00','2026-06-01 00:22:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO environments(id,project_id,name,base_url,variables,headers,is_default,created_at,updated_at)VALUES(9,3,'开发环境','https://dev.example.com','{}','{}',false,' 2025-11-21 15:02:00','2026-05-30 19:53:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO environments(id,project_id,name,base_url,variables,headers,is_default,created_at,updated_at)VALUES(10,3,'测试环境','https://test.example.com','{}','{}',true,' 2026-02-01 11:41:00','2026-05-30 01:28:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO environments(id,project_id,name,base_url,variables,headers,is_default,created_at,updated_at)VALUES(11,3,'预发布','https://staging.example.com','{}','{}',false,' 2026-01-13 18:32:00','2026-06-01 14:58:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO environments(id,project_id,name,base_url,variables,headers,is_default,created_at,updated_at)VALUES(12,3,'生产环境','https://api.example.com','{}','{}',false,' 2025-10-16 20:13:00','2026-05-30 14:44:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO environments(id,project_id,name,base_url,variables,headers,is_default,created_at,updated_at)VALUES(13,4,'开发环境','https://dev.example.com','{}','{}',false,' 2026-05-26 07:46:00','2026-06-01 12:08:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO environments(id,project_id,name,base_url,variables,headers,is_default,created_at,updated_at)VALUES(14,4,'测试环境','https://test.example.com','{}','{}',true,' 2026-03-24 15:58:00','2026-05-31 18:27:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO environments(id,project_id,name,base_url,variables,headers,is_default,created_at,updated_at)VALUES(15,4,'预发布','https://staging.example.com','{}','{}',false,' 2025-12-16 19:02:00','2026-05-31 04:23:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO environments(id,project_id,name,base_url,variables,headers,is_default,created_at,updated_at)VALUES(16,4,'生产环境','https://api.example.com','{}','{}',false,' 2026-02-09 13:08:00','2026-05-30 07:30:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO environments(id,project_id,name,base_url,variables,headers,is_default,created_at,updated_at)VALUES(17,5,'开发环境','https://dev.example.com','{}','{}',false,' 2026-03-03 20:39:00','2026-05-30 12:54:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO environments(id,project_id,name,base_url,variables,headers,is_default,created_at,updated_at)VALUES(18,5,'测试环境','https://test.example.com','{}','{}',true,' 2025-10-25 04:39:00','2026-05-29 11:29:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO environments(id,project_id,name,base_url,variables,headers,is_default,created_at,updated_at)VALUES(19,5,'预发布','https://staging.example.com','{}','{}',false,' 2026-03-19 12:35:00','2026-06-01 19:55:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO environments(id,project_id,name,base_url,variables,headers,is_default,created_at,updated_at)VALUES(20,5,'生产环境','https://api.example.com','{}','{}',false,' 2026-03-13 01:40:00','2026-06-01 21:05:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO environments(id,project_id,name,base_url,variables,headers,is_default,created_at,updated_at)VALUES(21,6,'开发环境','https://dev.example.com','{}','{}',false,' 2026-01-21 09:18:00','2026-05-29 20:57:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO environments(id,project_id,name,base_url,variables,headers,is_default,created_at,updated_at)VALUES(22,6,'测试环境','https://test.example.com','{}','{}',true,' 2026-04-13 17:37:00','2026-05-29 13:32:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO environments(id,project_id,name,base_url,variables,headers,is_default,created_at,updated_at)VALUES(23,6,'预发布','https://staging.example.com','{}','{}',false,' 2025-11-19 08:47:00','2026-05-30 16:52:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO environments(id,project_id,name,base_url,variables,headers,is_default,created_at,updated_at)VALUES(24,6,'生产环境','https://api.example.com','{}','{}',false,' 2025-10-07 00:32:00','2026-05-30 06:59:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO environments(id,project_id,name,base_url,variables,headers,is_default,created_at,updated_at)VALUES(25,7,'开发环境','https://dev.example.com','{}','{}',false,' 2025-12-21 14:09:00','2026-05-31 11:50:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO environments(id,project_id,name,base_url,variables,headers,is_default,created_at,updated_at)VALUES(26,7,'测试环境','https://test.example.com','{}','{}',true,' 2026-03-13 17:00:00','2026-05-30 07:46:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO environments(id,project_id,name,base_url,variables,headers,is_default,created_at,updated_at)VALUES(27,7,'预发布','https://staging.example.com','{}','{}',false,' 2025-10-29 06:31:00','2026-06-01 13:07:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO environments(id,project_id,name,base_url,variables,headers,is_default,created_at,updated_at)VALUES(28,7,'生产环境','https://api.example.com','{}','{}',false,' 2026-04-22 18:01:00','2026-05-30 17:15:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO environments(id,project_id,name,base_url,variables,headers,is_default,created_at,updated_at)VALUES(29,8,'开发环境','https://dev.example.com','{}','{}',false,' 2026-03-23 20:07:00','2026-05-29 18:45:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO environments(id,project_id,name,base_url,variables,headers,is_default,created_at,updated_at)VALUES(30,8,'测试环境','https://test.example.com','{}','{}',true,' 2026-02-04 16:51:00','2026-05-30 03:02:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO environments(id,project_id,name,base_url,variables,headers,is_default,created_at,updated_at)VALUES(31,8,'预发布','https://staging.example.com','{}','{}',false,' 2025-12-29 17:13:00','2026-06-01 07:43:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO environments(id,project_id,name,base_url,variables,headers,is_default,created_at,updated_at)VALUES(32,8,'生产环境','https://api.example.com','{}','{}',false,' 2025-11-15 20:39:00','2026-05-31 09:42:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO environments(id,project_id,name,base_url,variables,headers,is_default,created_at,updated_at)VALUES(33,9,'开发环境','https://dev.example.com','{}','{}',false,' 2025-11-28 00:07:00','2026-05-30 05:32:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO environments(id,project_id,name,base_url,variables,headers,is_default,created_at,updated_at)VALUES(34,9,'测试环境','https://test.example.com','{}','{}',true,' 2026-01-14 18:38:00','2026-05-30 16:12:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO environments(id,project_id,name,base_url,variables,headers,is_default,created_at,updated_at)VALUES(35,9,'预发布','https://staging.example.com','{}','{}',false,' 2026-01-12 21:31:00','2026-05-31 03:16:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO environments(id,project_id,name,base_url,variables,headers,is_default,created_at,updated_at)VALUES(36,9,'生产环境','https://api.example.com','{}','{}',false,' 2026-03-31 15:36:00','2026-05-31 20:58:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO environments(id,project_id,name,base_url,variables,headers,is_default,created_at,updated_at)VALUES(37,10,'开发环境','https://dev.example.com','{}','{}',false,' 2026-03-11 10:30:00','2026-05-29 21:18:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO environments(id,project_id,name,base_url,variables,headers,is_default,created_at,updated_at)VALUES(38,10,'测试环境','https://test.example.com','{}','{}',true,' 2025-11-10 13:51:00','2026-05-30 08:52:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO environments(id,project_id,name,base_url,variables,headers,is_default,created_at,updated_at)VALUES(39,10,'预发布','https://staging.example.com','{}','{}',false,' 2026-01-23 15:39:00','2026-06-01 19:54:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO environments(id,project_id,name,base_url,variables,headers,is_default,created_at,updated_at)VALUES(40,10,'生产环境','https://api.example.com','{}','{}',false,' 2026-01-17 20:00:00','2026-05-31 20:05:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO environments(id,project_id,name,base_url,variables,headers,is_default,created_at,updated_at)VALUES(41,11,'开发环境','https://dev.example.com','{}','{}',false,' 2025-12-16 05:56:00','2026-05-30 01:39:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO environments(id,project_id,name,base_url,variables,headers,is_default,created_at,updated_at)VALUES(42,11,'测试环境','https://test.example.com','{}','{}',true,' 2025-12-23 11:35:00','2026-06-01 23:06:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO environments(id,project_id,name,base_url,variables,headers,is_default,created_at,updated_at)VALUES(43,11,'预发布','https://staging.example.com','{}','{}',false,' 2025-12-10 16:36:00','2026-05-30 13:15:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO environments(id,project_id,name,base_url,variables,headers,is_default,created_at,updated_at)VALUES(44,11,'生产环境','https://api.example.com','{}','{}',false,' 2025-10-16 18:05:00','2026-06-01 14:56:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO environments(id,project_id,name,base_url,variables,headers,is_default,created_at,updated_at)VALUES(45,12,'开发环境','https://dev.example.com','{}','{}',false,' 2026-04-01 13:17:00','2026-05-31 02:13:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO environments(id,project_id,name,base_url,variables,headers,is_default,created_at,updated_at)VALUES(46,12,'测试环境','https://test.example.com','{}','{}',true,' 2026-05-08 20:54:00','2026-06-01 19:50:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO environments(id,project_id,name,base_url,variables,headers,is_default,created_at,updated_at)VALUES(47,12,'预发布','https://staging.example.com','{}','{}',false,' 2025-12-06 00:03:00','2026-06-02 08:40:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO environments(id,project_id,name,base_url,variables,headers,is_default,created_at,updated_at)VALUES(48,12,'生产环境','https://api.example.com','{}','{}',false,' 2025-11-10 08:42:00','2026-05-30 22:33:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO environments(id,project_id,name,base_url,variables,headers,is_default,created_at,updated_at)VALUES(49,13,'开发环境','https://dev.example.com','{}','{}',false,' 2026-04-25 02:27:00','2026-05-29 15:17:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO environments(id,project_id,name,base_url,variables,headers,is_default,created_at,updated_at)VALUES(50,13,'测试环境','https://test.example.com','{}','{}',true,' 2025-11-11 04:50:00','2026-06-01 07:21:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO environments(id,project_id,name,base_url,variables,headers,is_default,created_at,updated_at)VALUES(51,13,'预发布','https://staging.example.com','{}','{}',false,' 2025-10-21 21:21:00','2026-05-31 18:02:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO environments(id,project_id,name,base_url,variables,headers,is_default,created_at,updated_at)VALUES(52,13,'生产环境','https://api.example.com','{}','{}',false,' 2026-01-03 05:46:00','2026-05-29 13:44:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO environments(id,project_id,name,base_url,variables,headers,is_default,created_at,updated_at)VALUES(53,14,'开发环境','https://dev.example.com','{}','{}',false,' 2026-02-04 01:18:00','2026-06-01 19:03:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO environments(id,project_id,name,base_url,variables,headers,is_default,created_at,updated_at)VALUES(54,14,'测试环境','https://test.example.com','{}','{}',true,' 2026-03-19 12:26:00','2026-06-01 07:32:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO environments(id,project_id,name,base_url,variables,headers,is_default,created_at,updated_at)VALUES(55,14,'预发布','https://staging.example.com','{}','{}',false,' 2026-03-04 15:41:00','2026-05-29 11:44:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO environments(id,project_id,name,base_url,variables,headers,is_default,created_at,updated_at)VALUES(56,14,'生产环境','https://api.example.com','{}','{}',false,' 2026-02-05 00:48:00','2026-05-29 18:54:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO environments(id,project_id,name,base_url,variables,headers,is_default,created_at,updated_at)VALUES(57,15,'开发环境','https://dev.example.com','{}','{}',false,' 2026-04-01 21:24:00','2026-05-30 15:42:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO environments(id,project_id,name,base_url,variables,headers,is_default,created_at,updated_at)VALUES(58,15,'测试环境','https://test.example.com','{}','{}',true,' 2025-12-04 00:59:00','2026-05-30 02:00:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO environments(id,project_id,name,base_url,variables,headers,is_default,created_at,updated_at)VALUES(59,15,'预发布','https://staging.example.com','{}','{}',false,' 2026-01-07 12:11:00','2026-06-01 14:13:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO environments(id,project_id,name,base_url,variables,headers,is_default,created_at,updated_at)VALUES(60,15,'生产环境','https://api.example.com','{}','{}',false,' 2026-01-25 00:11:00','2026-05-31 14:09:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO environments(id,project_id,name,base_url,variables,headers,is_default,created_at,updated_at)VALUES(61,16,'开发环境','https://dev.example.com','{}','{}',false,' 2026-03-03 02:20:00','2026-05-31 14:44:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO environments(id,project_id,name,base_url,variables,headers,is_default,created_at,updated_at)VALUES(62,16,'测试环境','https://test.example.com','{}','{}',true,' 2025-12-09 10:11:00','2026-05-31 13:54:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO environments(id,project_id,name,base_url,variables,headers,is_default,created_at,updated_at)VALUES(63,16,'预发布','https://staging.example.com','{}','{}',false,' 2025-10-12 13:19:00','2026-06-02 00:10:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO environments(id,project_id,name,base_url,variables,headers,is_default,created_at,updated_at)VALUES(64,16,'生产环境','https://api.example.com','{}','{}',false,' 2026-02-09 08:23:00','2026-05-30 10:52:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO api_test_collections(id,project_id,user_id,name,description,sort_order,created_at,updated_at)VALUES(1,1,6,'商品管理','CRUD搜索分类',1,'2026-04-18 03:52:00','2026-05-28 22:27:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO api_test_collections(id,project_id,user_id,name,description,sort_order,created_at,updated_at)VALUES(2,1,5,'订单交易','下单支付退款',2,'2025-11-01 04:44:00','2026-05-30 00:13:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO api_test_collections(id,project_id,user_id,name,description,sort_order,created_at,updated_at)VALUES(3,1,1,'消息通知','站内信Push',3,'2026-02-02 07:51:00','2026-05-31 12:14:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO api_test_collections(id,project_id,user_id,name,description,sort_order,created_at,updated_at)VALUES(4,1,6,'营销活动','优惠券秒杀',4,'2025-10-27 16:37:00','2026-06-01 22:00:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO api_test_collections(id,project_id,user_id,name,description,sort_order,created_at,updated_at)VALUES(5,1,1,'系统管理','配置日志',5,'2026-02-04 22:17:00','2026-05-27 12:44:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO api_test_collections(id,project_id,user_id,name,description,sort_order,created_at,updated_at)VALUES(6,1,5,'数据报表','统计导出',6,'2026-05-04 12:46:00','2026-05-30 09:21:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO api_test_collections(id,project_id,user_id,name,description,sort_order,created_at,updated_at)VALUES(7,1,7,'文件管理','上传下载',7,'2026-03-09 14:46:00','2026-05-28 07:20:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO api_test_collections(id,project_id,user_id,name,description,sort_order,created_at,updated_at)VALUES(8,2,5,'用户认证','登录注册重置',0,'2025-12-16 20:53:00','2026-06-01 08:58:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO api_test_collections(id,project_id,user_id,name,description,sort_order,created_at,updated_at)VALUES(9,2,6,'商品管理','CRUD搜索分类',1,'2026-05-03 06:45:00','2026-05-29 05:36:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO api_test_collections(id,project_id,user_id,name,description,sort_order,created_at,updated_at)VALUES(10,2,7,'订单交易','下单支付退款',2,'2026-02-13 15:13:00','2026-05-28 05:04:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO api_test_collections(id,project_id,user_id,name,description,sort_order,created_at,updated_at)VALUES(11,2,1,'消息通知','站内信Push',3,'2025-10-30 18:21:00','2026-05-30 01:58:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO api_test_collections(id,project_id,user_id,name,description,sort_order,created_at,updated_at)VALUES(12,2,2,'营销活动','优惠券秒杀',4,'2026-02-07 19:45:00','2026-05-31 06:17:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO api_test_collections(id,project_id,user_id,name,description,sort_order,created_at,updated_at)VALUES(13,2,5,'系统管理','配置日志',5,'2026-05-16 21:43:00','2026-06-01 06:06:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO api_test_collections(id,project_id,user_id,name,description,sort_order,created_at,updated_at)VALUES(14,2,1,'数据报表','统计导出',6,'2025-12-14 03:19:00','2026-05-27 14:59:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO api_test_collections(id,project_id,user_id,name,description,sort_order,created_at,updated_at)VALUES(15,3,2,'用户认证','登录注册重置',0,'2025-11-11 15:47:00','2026-06-01 16:47:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO api_test_collections(id,project_id,user_id,name,description,sort_order,created_at,updated_at)VALUES(16,3,2,'商品管理','CRUD搜索分类',1,'2026-03-09 05:10:00','2026-05-29 09:43:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO api_test_collections(id,project_id,user_id,name,description,sort_order,created_at,updated_at)VALUES(17,3,2,'订单交易','下单支付退款',2,'2026-04-28 16:44:00','2026-06-01 06:18:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO api_test_collections(id,project_id,user_id,name,description,sort_order,created_at,updated_at)VALUES(18,3,2,'消息通知','站内信Push',3,'2026-05-28 22:10:00','2026-05-31 15:40:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO api_test_collections(id,project_id,user_id,name,description,sort_order,created_at,updated_at)VALUES(19,3,2,'系统管理','配置日志',5,'2025-11-23 20:27:00','2026-06-01 10:56:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO api_test_collections(id,project_id,user_id,name,description,sort_order,created_at,updated_at)VALUES(20,3,5,'数据报表','统计导出',6,'2026-01-20 15:54:00','2026-05-29 17:46:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO api_test_collections(id,project_id,user_id,name,description,sort_order,created_at,updated_at)VALUES(21,3,1,'文件管理','上传下载',7,'2025-11-26 12:27:00','2026-05-30 19:19:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO api_test_collections(id,project_id,user_id,name,description,sort_order,created_at,updated_at)VALUES(22,4,1,'用户认证','登录注册重置',0,'2026-01-29 21:33:00','2026-05-28 06:29:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO api_test_collections(id,project_id,user_id,name,description,sort_order,created_at,updated_at)VALUES(23,4,6,'商品管理','CRUD搜索分类',1,'2026-05-14 07:40:00','2026-05-29 05:56:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO api_test_collections(id,project_id,user_id,name,description,sort_order,created_at,updated_at)VALUES(24,4,7,'订单交易','下单支付退款',2,'2025-12-20 15:25:00','2026-05-27 23:36:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO api_test_collections(id,project_id,user_id,name,description,sort_order,created_at,updated_at)VALUES(25,4,7,'消息通知','站内信Push',3,'2026-03-17 19:28:00','2026-05-28 20:54:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO api_test_collections(id,project_id,user_id,name,description,sort_order,created_at,updated_at)VALUES(26,4,1,'营销活动','优惠券秒杀',4,'2025-10-25 13:19:00','2026-05-28 10:05:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO api_test_collections(id,project_id,user_id,name,description,sort_order,created_at,updated_at)VALUES(27,4,6,'系统管理','配置日志',5,'2025-10-17 02:34:00','2026-05-30 19:35:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO api_test_collections(id,project_id,user_id,name,description,sort_order,created_at,updated_at)VALUES(28,4,1,'数据报表','统计导出',6,'2026-03-12 20:40:00','2026-05-28 01:37:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO api_test_collections(id,project_id,user_id,name,description,sort_order,created_at,updated_at)VALUES(29,4,6,'文件管理','上传下载',7,'2026-05-15 07:07:00','2026-06-02 07:33:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO api_test_collections(id,project_id,user_id,name,description,sort_order,created_at,updated_at)VALUES(30,5,2,'商品管理','CRUD搜索分类',1,'2026-01-10 08:23:00','2026-05-28 16:39:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO api_test_collections(id,project_id,user_id,name,description,sort_order,created_at,updated_at)VALUES(31,5,6,'订单交易','下单支付退款',2,'2026-03-02 12:12:00','2026-05-29 10:57:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO api_test_collections(id,project_id,user_id,name,description,sort_order,created_at,updated_at)VALUES(32,5,7,'消息通知','站内信Push',3,'2026-03-13 22:54:00','2026-05-28 17:47:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO api_test_collections(id,project_id,user_id,name,description,sort_order,created_at,updated_at)VALUES(33,5,6,'营销活动','优惠券秒杀',4,'2026-04-05 06:38:00','2026-05-28 22:53:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO api_test_collections(id,project_id,user_id,name,description,sort_order,created_at,updated_at)VALUES(34,5,7,'系统管理','配置日志',5,'2026-04-04 20:06:00','2026-05-28 14:21:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO api_test_collections(id,project_id,user_id,name,description,sort_order,created_at,updated_at)VALUES(35,5,7,'数据报表','统计导出',6,'2026-05-25 14:01:00','2026-05-27 11:43:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO api_test_collections(id,project_id,user_id,name,description,sort_order,created_at,updated_at)VALUES(36,6,5,'用户认证','登录注册重置',0,'2025-10-08 23:38:00','2026-06-02 04:05:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO api_test_collections(id,project_id,user_id,name,description,sort_order,created_at,updated_at)VALUES(37,6,6,'商品管理','CRUD搜索分类',1,'2026-05-15 05:13:00','2026-05-28 09:55:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO api_test_collections(id,project_id,user_id,name,description,sort_order,created_at,updated_at)VALUES(38,6,2,'订单交易','下单支付退款',2,'2026-02-24 20:31:00','2026-05-31 04:37:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO api_test_collections(id,project_id,user_id,name,description,sort_order,created_at,updated_at)VALUES(39,6,5,'消息通知','站内信Push',3,'2025-11-14 15:22:00','2026-06-02 08:51:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO api_test_collections(id,project_id,user_id,name,description,sort_order,created_at,updated_at)VALUES(40,6,7,'营销活动','优惠券秒杀',4,'2026-05-19 12:55:00','2026-05-30 19:18:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO api_test_collections(id,project_id,user_id,name,description,sort_order,created_at,updated_at)VALUES(41,6,7,'系统管理','配置日志',5,'2026-02-07 20:43:00','2026-05-31 17:53:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO api_test_collections(id,project_id,user_id,name,description,sort_order,created_at,updated_at)VALUES(42,6,1,'数据报表','统计导出',6,'2026-03-20 12:17:00','2026-05-28 18:27:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO api_test_collections(id,project_id,user_id,name,description,sort_order,created_at,updated_at)VALUES(43,6,1,'文件管理','上传下载',7,'2026-04-05 21:22:00','2026-06-02 09:47:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO api_test_collections(id,project_id,user_id,name,description,sort_order,created_at,updated_at)VALUES(44,7,2,'用户认证','登录注册重置',0,'2025-11-17 05:12:00','2026-05-31 00:40:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO api_test_collections(id,project_id,user_id,name,description,sort_order,created_at,updated_at)VALUES(45,7,6,'订单交易','下单支付退款',2,'2026-04-18 05:36:00','2026-05-28 11:46:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO api_test_collections(id,project_id,user_id,name,description,sort_order,created_at,updated_at)VALUES(46,7,5,'消息通知','站内信Push',3,'2026-05-13 21:05:00','2026-05-28 08:33:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO api_test_collections(id,project_id,user_id,name,description,sort_order,created_at,updated_at)VALUES(47,7,5,'系统管理','配置日志',5,'2026-01-04 20:24:00','2026-05-29 11:20:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO api_test_collections(id,project_id,user_id,name,description,sort_order,created_at,updated_at)VALUES(48,7,1,'数据报表','统计导出',6,'2026-02-18 09:40:00','2026-05-31 14:31:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO api_test_collections(id,project_id,user_id,name,description,sort_order,created_at,updated_at)VALUES(49,7,5,'文件管理','上传下载',7,'2026-05-09 20:06:00','2026-06-02 02:33:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO api_test_collections(id,project_id,user_id,name,description,sort_order,created_at,updated_at)VALUES(50,8,7,'用户认证','登录注册重置',0,'2026-05-11 21:05:00','2026-05-30 10:39:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO api_test_collections(id,project_id,user_id,name,description,sort_order,created_at,updated_at)VALUES(51,8,2,'商品管理','CRUD搜索分类',1,'2026-05-12 17:20:00','2026-06-01 17:28:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO api_test_collections(id,project_id,user_id,name,description,sort_order,created_at,updated_at)VALUES(52,8,5,'订单交易','下单支付退款',2,'2026-03-03 10:08:00','2026-05-28 05:45:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO api_test_collections(id,project_id,user_id,name,description,sort_order,created_at,updated_at)VALUES(53,8,2,'营销活动','优惠券秒杀',4,'2025-12-29 05:12:00','2026-05-28 07:49:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO api_test_collections(id,project_id,user_id,name,description,sort_order,created_at,updated_at)VALUES(54,8,6,'系统管理','配置日志',5,'2026-02-02 15:12:00','2026-05-28 19:17:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO api_test_collections(id,project_id,user_id,name,description,sort_order,created_at,updated_at)VALUES(55,8,7,'数据报表','统计导出',6,'2025-12-18 13:21:00','2026-05-30 13:40:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO api_test_collections(id,project_id,user_id,name,description,sort_order,created_at,updated_at)VALUES(56,8,1,'文件管理','上传下载',7,'2026-01-31 19:20:00','2026-05-31 01:23:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO api_test_collections(id,project_id,user_id,name,description,sort_order,created_at,updated_at)VALUES(57,9,5,'商品管理','CRUD搜索分类',1,'2026-02-02 19:58:00','2026-06-01 22:07:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO api_test_collections(id,project_id,user_id,name,description,sort_order,created_at,updated_at)VALUES(58,9,1,'订单交易','下单支付退款',2,'2025-12-25 14:28:00','2026-05-29 19:23:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO api_test_collections(id,project_id,user_id,name,description,sort_order,created_at,updated_at)VALUES(59,9,1,'消息通知','站内信Push',3,'2026-02-05 15:19:00','2026-05-31 23:22:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO api_test_collections(id,project_id,user_id,name,description,sort_order,created_at,updated_at)VALUES(60,9,2,'营销活动','优惠券秒杀',4,'2026-05-16 19:54:00','2026-05-30 11:55:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO api_test_collections(id,project_id,user_id,name,description,sort_order,created_at,updated_at)VALUES(61,9,2,'系统管理','配置日志',5,'2026-05-22 02:15:00','2026-05-29 19:27:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO api_test_collections(id,project_id,user_id,name,description,sort_order,created_at,updated_at)VALUES(62,9,2,'数据报表','统计导出',6,'2026-02-27 22:02:00','2026-05-30 21:34:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO api_test_collections(id,project_id,user_id,name,description,sort_order,created_at,updated_at)VALUES(63,9,7,'文件管理','上传下载',7,'2026-05-18 13:19:00','2026-05-31 07:39:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO api_test_collections(id,project_id,user_id,name,description,sort_order,created_at,updated_at)VALUES(64,10,5,'商品管理','CRUD搜索分类',1,'2026-03-28 10:06:00','2026-05-27 14:05:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO api_test_collections(id,project_id,user_id,name,description,sort_order,created_at,updated_at)VALUES(65,10,1,'订单交易','下单支付退款',2,'2026-01-02 12:51:00','2026-05-31 00:19:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO api_test_collections(id,project_id,user_id,name,description,sort_order,created_at,updated_at)VALUES(66,10,6,'消息通知','站内信Push',3,'2026-04-28 14:15:00','2026-06-02 00:25:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO api_test_collections(id,project_id,user_id,name,description,sort_order,created_at,updated_at)VALUES(67,10,5,'营销活动','优惠券秒杀',4,'2025-11-05 05:18:00','2026-05-27 10:17:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO api_test_collections(id,project_id,user_id,name,description,sort_order,created_at,updated_at)VALUES(68,10,1,'系统管理','配置日志',5,'2025-12-17 12:33:00','2026-05-28 22:59:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO api_test_collections(id,project_id,user_id,name,description,sort_order,created_at,updated_at)VALUES(69,10,2,'数据报表','统计导出',6,'2026-04-07 23:11:00','2026-05-30 03:46:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO api_test_collections(id,project_id,user_id,name,description,sort_order,created_at,updated_at)VALUES(70,10,2,'文件管理','上传下载',7,'2026-05-13 00:06:00','2026-06-01 17:11:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO api_test_collections(id,project_id,user_id,name,description,sort_order,created_at,updated_at)VALUES(71,11,7,'用户认证','登录注册重置',0,'2026-05-22 12:39:00','2026-05-29 05:22:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO api_test_collections(id,project_id,user_id,name,description,sort_order,created_at,updated_at)VALUES(72,11,2,'商品管理','CRUD搜索分类',1,'2026-04-15 11:11:00','2026-05-29 04:14:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO api_test_collections(id,project_id,user_id,name,description,sort_order,created_at,updated_at)VALUES(73,11,6,'订单交易','下单支付退款',2,'2026-02-27 12:14:00','2026-05-31 19:21:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO api_test_collections(id,project_id,user_id,name,description,sort_order,created_at,updated_at)VALUES(74,11,6,'消息通知','站内信Push',3,'2026-04-02 16:45:00','2026-05-30 18:03:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO api_test_collections(id,project_id,user_id,name,description,sort_order,created_at,updated_at)VALUES(75,11,5,'营销活动','优惠券秒杀',4,'2025-12-09 15:32:00','2026-05-30 00:11:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO api_test_collections(id,project_id,user_id,name,description,sort_order,created_at,updated_at)VALUES(76,11,7,'系统管理','配置日志',5,'2026-02-14 04:08:00','2026-05-31 14:52:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO api_test_collections(id,project_id,user_id,name,description,sort_order,created_at,updated_at)VALUES(77,11,1,'数据报表','统计导出',6,'2025-12-18 18:05:00','2026-05-30 16:01:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO api_test_collections(id,project_id,user_id,name,description,sort_order,created_at,updated_at)VALUES(78,12,1,'用户认证','登录注册重置',0,'2026-03-21 07:12:00','2026-06-01 01:32:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO api_test_collections(id,project_id,user_id,name,description,sort_order,created_at,updated_at)VALUES(79,12,2,'商品管理','CRUD搜索分类',1,'2025-10-31 20:55:00','2026-05-31 19:04:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO api_test_collections(id,project_id,user_id,name,description,sort_order,created_at,updated_at)VALUES(80,12,1,'订单交易','下单支付退款',2,'2026-02-15 08:35:00','2026-05-28 22:45:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO api_test_collections(id,project_id,user_id,name,description,sort_order,created_at,updated_at)VALUES(81,12,1,'消息通知','站内信Push',3,'2026-02-26 02:59:00','2026-05-31 06:07:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO api_test_collections(id,project_id,user_id,name,description,sort_order,created_at,updated_at)VALUES(82,12,5,'营销活动','优惠券秒杀',4,'2025-11-11 05:52:00','2026-06-02 00:02:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO api_test_collections(id,project_id,user_id,name,description,sort_order,created_at,updated_at)VALUES(83,12,2,'系统管理','配置日志',5,'2025-11-18 11:30:00','2026-05-29 15:00:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO api_test_collections(id,project_id,user_id,name,description,sort_order,created_at,updated_at)VALUES(84,12,1,'数据报表','统计导出',6,'2026-03-28 03:07:00','2026-05-31 16:14:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO api_test_collections(id,project_id,user_id,name,description,sort_order,created_at,updated_at)VALUES(85,12,6,'文件管理','上传下载',7,'2026-05-04 00:45:00','2026-05-31 06:57:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO api_test_collections(id,project_id,user_id,name,description,sort_order,created_at,updated_at)VALUES(86,13,7,'用户认证','登录注册重置',0,'2026-02-04 07:53:00','2026-05-29 14:26:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO api_test_collections(id,project_id,user_id,name,description,sort_order,created_at,updated_at)VALUES(87,13,2,'订单交易','下单支付退款',2,'2025-11-30 05:42:00','2026-05-30 09:21:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO api_test_collections(id,project_id,user_id,name,description,sort_order,created_at,updated_at)VALUES(88,13,7,'消息通知','站内信Push',3,'2026-02-15 04:18:00','2026-05-28 07:27:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO api_test_collections(id,project_id,user_id,name,description,sort_order,created_at,updated_at)VALUES(89,13,1,'营销活动','优惠券秒杀',4,'2026-01-17 16:28:00','2026-05-28 16:59:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO api_test_collections(id,project_id,user_id,name,description,sort_order,created_at,updated_at)VALUES(90,13,6,'系统管理','配置日志',5,'2026-05-20 13:36:00','2026-05-31 01:13:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO api_test_collections(id,project_id,user_id,name,description,sort_order,created_at,updated_at)VALUES(91,13,5,'文件管理','上传下载',7,'2026-03-31 10:18:00','2026-05-28 06:11:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO api_test_collections(id,project_id,user_id,name,description,sort_order,created_at,updated_at)VALUES(92,14,5,'用户认证','登录注册重置',0,'2026-04-28 08:38:00','2026-05-28 23:08:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO api_test_collections(id,project_id,user_id,name,description,sort_order,created_at,updated_at)VALUES(93,14,6,'商品管理','CRUD搜索分类',1,'2025-12-04 18:20:00','2026-06-01 05:56:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO api_test_collections(id,project_id,user_id,name,description,sort_order,created_at,updated_at)VALUES(94,14,6,'订单交易','下单支付退款',2,'2026-05-23 00:48:00','2026-06-02 03:04:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO api_test_collections(id,project_id,user_id,name,description,sort_order,created_at,updated_at)VALUES(95,14,7,'营销活动','优惠券秒杀',4,'2026-02-19 16:30:00','2026-05-31 08:12:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO api_test_collections(id,project_id,user_id,name,description,sort_order,created_at,updated_at)VALUES(96,14,5,'系统管理','配置日志',5,'2026-03-02 08:05:00','2026-05-27 23:43:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO api_test_collections(id,project_id,user_id,name,description,sort_order,created_at,updated_at)VALUES(97,14,5,'数据报表','统计导出',6,'2026-02-09 21:13:00','2026-05-29 21:39:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO api_test_collections(id,project_id,user_id,name,description,sort_order,created_at,updated_at)VALUES(98,14,6,'文件管理','上传下载',7,'2025-12-05 18:37:00','2026-05-29 01:09:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO api_test_collections(id,project_id,user_id,name,description,sort_order,created_at,updated_at)VALUES(99,15,6,'商品管理','CRUD搜索分类',1,'2025-12-29 04:26:00','2026-05-30 23:54:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO api_test_collections(id,project_id,user_id,name,description,sort_order,created_at,updated_at)VALUES(100,15,5,'消息通知','站内信Push',3,'2026-02-06 14:15:00','2026-05-30 04:16:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO api_test_collections(id,project_id,user_id,name,description,sort_order,created_at,updated_at)VALUES(101,15,6,'营销活动','优惠券秒杀',4,'2026-05-21 10:05:00','2026-05-30 14:33:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO api_test_collections(id,project_id,user_id,name,description,sort_order,created_at,updated_at)VALUES(102,15,1,'系统管理','配置日志',5,'2026-05-12 12:20:00','2026-05-29 22:28:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO api_test_collections(id,project_id,user_id,name,description,sort_order,created_at,updated_at)VALUES(103,15,2,'数据报表','统计导出',6,'2026-05-25 05:06:00','2026-05-28 12:10:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO api_test_collections(id,project_id,user_id,name,description,sort_order,created_at,updated_at)VALUES(104,15,2,'文件管理','上传下载',7,'2026-05-15 02:11:00','2026-05-27 22:37:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO api_test_collections(id,project_id,user_id,name,description,sort_order,created_at,updated_at)VALUES(105,16,7,'用户认证','登录注册重置',0,'2026-05-23 14:51:00','2026-05-27 19:37:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO api_test_collections(id,project_id,user_id,name,description,sort_order,created_at,updated_at)VALUES(106,16,1,'商品管理','CRUD搜索分类',1,'2026-01-06 05:27:00','2026-05-30 21:40:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO api_test_collections(id,project_id,user_id,name,description,sort_order,created_at,updated_at)VALUES(107,16,2,'订单交易','下单支付退款',2,'2026-05-03 09:13:00','2026-05-31 18:27:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO api_test_collections(id,project_id,user_id,name,description,sort_order,created_at,updated_at)VALUES(108,16,7,'消息通知','站内信Push',3,'2026-05-02 01:11:00','2026-05-30 11:32:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO api_test_collections(id,project_id,user_id,name,description,sort_order,created_at,updated_at)VALUES(109,16,7,'营销活动','优惠券秒杀',4,'2026-03-19 11:02:00','2026-05-30 03:53:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO api_test_collections(id,project_id,user_id,name,description,sort_order,created_at,updated_at)VALUES(110,16,1,'系统管理','配置日志',5,'2026-02-06 04:03:00','2026-05-27 19:55:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO api_test_collections(id,project_id,user_id,name,description,sort_order,created_at,updated_at)VALUES(111,16,5,'数据报表','统计导出',6,'2025-12-12 22:15:00','2026-06-01 16:26:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO api_test_collections(id,project_id,user_id,name,description,sort_order,created_at,updated_at)VALUES(112,16,5,'文件管理','上传下载',7,'2025-10-27 04:15:00','2026-05-27 11:20:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO api_test_cases(id,collection_id,project_id,user_id,environment_id,name,description,method,url,headers,params,body,body_type,assertions,timeout,retry_count,tags,priority,is_enabled,sort_order,last_run_at,last_status,created_at,updated_at)VALUES(1,1,1,2,2,'标记已读','验证标记已读','PUT','/api/v1/messages/1001','{}','{}',NULL,'json','[]',30,0,'["message", "P2"]',2,true,0,'2026-05-18 09:37:00','success','2026-01-05 22:31:00','2026-05-31 14:04:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO api_test_cases(id,collection_id,project_id,user_id,environment_id,name,description,method,url,headers,params,body,body_type,assertions,timeout,retry_count,tags,priority,is_enabled,sort_order,last_run_at,last_status,created_at,updated_at)VALUES(2,1,1,1,1,'提交反馈','验证提交反馈','POST','/api/v1/feedback','{}','{}',NULL,'json','[]',30,0,'["feedback", "P2"]',2,true,1,'2026-05-17 17:34:00','success','2026-01-05 07:52:00','2026-05-30 13:56:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO api_test_cases(id,collection_id,project_id,user_id,environment_id,name,description,method,url,headers,params,body,body_type,assertions,timeout,retry_count,tags,priority,is_enabled,sort_order,last_run_at,last_status,created_at,updated_at)VALUES(3,1,1,6,4,'发起支付','验证发起支付','POST','/api/v1/payments','{}','{}',NULL,'json','[]',30,0,'["payment", "P0"]',2,true,2,'2026-05-22 05:04:00','failed','2025-12-19 15:49:00','2026-05-31 20:28:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO api_test_cases(id,collection_id,project_id,user_id,environment_id,name,description,method,url,headers,params,body,body_type,assertions,timeout,retry_count,tags,priority,is_enabled,sort_order,last_run_at,last_status,created_at,updated_at)VALUES(4,1,1,1,1,'商品列表','验证商品列表','GET','/api/v1/products','{}','{}',NULL,'json','[]',30,0,'["product", "P0"]',2,true,3,'2026-05-24 04:50:00','success','2025-12-02 02:38:00','2026-05-31 07:44:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO api_test_cases(id,collection_id,project_id,user_id,environment_id,name,description,method,url,headers,params,body,body_type,assertions,timeout,retry_count,tags,priority,is_enabled,sort_order,last_run_at,last_status,created_at,updated_at)VALUES(5,2,1,7,1,'优惠券','验证优惠券','GET','/api/v1/coupons','{}','{}',NULL,'json','[]',30,0,'["marketing", "P1"]',1,true,0,'2026-05-27 15:23:00','success','2026-04-18 12:21:00','2026-05-30 15:58:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO api_test_cases(id,collection_id,project_id,user_id,environment_id,name,description,method,url,headers,params,body,body_type,assertions,timeout,retry_count,tags,priority,is_enabled,sort_order,last_run_at,last_status,created_at,updated_at)VALUES(6,2,1,1,1,'支付状态','验证支付状态','GET','/api/v1/payments/1001','{}','{}',NULL,'json','[]',30,0,'["payment", "P1"]',2,true,1,'2026-05-24 13:47:00','success','2026-02-14 14:20:00','2026-06-01 18:04:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO api_test_cases(id,collection_id,project_id,user_id,environment_id,name,description,method,url,headers,params,body,body_type,assertions,timeout,retry_count,tags,priority,is_enabled,sort_order,last_run_at,last_status,created_at,updated_at)VALUES(7,2,1,7,3,'创建订单','验证创建订单','POST','/api/v1/orders','{}','{}',NULL,'json','[]',30,0,'["order", "P0"]',3,true,2,'2026-05-23 18:45:00','success','2026-02-18 00:31:00','2026-06-01 11:57:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO api_test_cases(id,collection_id,project_id,user_id,environment_id,name,description,method,url,headers,params,body,body_type,assertions,timeout,retry_count,tags,priority,is_enabled,sort_order,last_run_at,last_status,created_at,updated_at)VALUES(8,2,1,2,4,'申请退款','验证申请退款','POST','/api/v1/refunds','{}','{}',NULL,'json','[]',30,0,'["payment", "P1"]',2,true,3,'2026-05-19 03:39:00','success','2026-04-25 23:05:00','2026-05-30 10:05:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO api_test_cases(id,collection_id,project_id,user_id,environment_id,name,description,method,url,headers,params,body,body_type,assertions,timeout,retry_count,tags,priority,is_enabled,sort_order,last_run_at,last_status,created_at,updated_at)VALUES(9,3,1,5,2,'搜索商品','验证搜索商品','GET','/api/v1/search','{}','{}',NULL,'json','[]',30,0,'["search", "P1"]',1,true,0,'2026-05-24 19:45:00','success','2026-05-08 08:42:00','2026-05-29 14:34:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO api_test_cases(id,collection_id,project_id,user_id,environment_id,name,description,method,url,headers,params,body,body_type,assertions,timeout,retry_count,tags,priority,is_enabled,sort_order,last_run_at,last_status,created_at,updated_at)VALUES(10,3,1,2,2,'创建订单','验证创建订单','POST','/api/v1/orders','{}','{}',NULL,'json','[]',30,0,'["order", "P0"]',1,true,1,'2026-05-23 03:12:00','failed','2026-01-24 17:31:00','2026-05-30 00:29:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO api_test_cases(id,collection_id,project_id,user_id,environment_id,name,description,method,url,headers,params,body,body_type,assertions,timeout,retry_count,tags,priority,is_enabled,sort_order,last_run_at,last_status,created_at,updated_at)VALUES(11,3,1,1,1,'标记已读','验证标记已读','PUT','/api/v1/messages/1001','{}','{}',NULL,'json','[]',30,0,'["message", "P2"]',2,true,2,NULL,'pending','2026-02-04 02:47:00','2026-05-31 08:57:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO api_test_cases(id,collection_id,project_id,user_id,environment_id,name,description,method,url,headers,params,body,body_type,assertions,timeout,retry_count,tags,priority,is_enabled,sort_order,last_run_at,last_status,created_at,updated_at)VALUES(12,3,1,5,4,'提交反馈','验证提交反馈','POST','/api/v1/feedback','{}','{}',NULL,'json','[]',30,0,'["feedback", "P2"]',1,true,3,'2026-05-18 00:26:00','success','2026-05-04 20:52:00','2026-05-30 10:37:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO api_test_cases(id,collection_id,project_id,user_id,environment_id,name,description,method,url,headers,params,body,body_type,assertions,timeout,retry_count,tags,priority,is_enabled,sort_order,last_run_at,last_status,created_at,updated_at)VALUES(13,3,1,6,3,'商品列表','验证商品列表','GET','/api/v1/products','{}','{}',NULL,'json','[]',30,0,'["product", "P0"]',1,true,4,'2026-05-31 15:25:00','success','2026-02-28 16:42:00','2026-06-01 21:28:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO api_test_cases(id,collection_id,project_id,user_id,environment_id,name,description,method,url,headers,params,body,body_type,assertions,timeout,retry_count,tags,priority,is_enabled,sort_order,last_run_at,last_status,created_at,updated_at)VALUES(14,4,1,5,3,'优惠券','验证优惠券','GET','/api/v1/coupons','{}','{}',NULL,'json','[]',30,0,'["marketing", "P1"]',2,true,0,'2026-05-22 05:48:00','success','2026-01-21 21:28:00','2026-06-02 08:58:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO api_test_cases(id,collection_id,project_id,user_id,environment_id,name,description,method,url,headers,params,body,body_type,assertions,timeout,retry_count,tags,priority,is_enabled,sort_order,last_run_at,last_status,created_at,updated_at)VALUES(15,4,1,2,3,'支付状态','验证支付状态','GET','/api/v1/payments/1001','{}','{}',NULL,'json','[]',30,0,'["payment", "P1"]',2,true,1,'2026-05-19 05:22:00','failed','2026-04-26 23:01:00','2026-05-31 04:35:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO api_test_cases(id,collection_id,project_id,user_id,environment_id,name,description,method,url,headers,params,body,body_type,assertions,timeout,retry_count,tags,priority,is_enabled,sort_order,last_run_at,last_status,created_at,updated_at)VALUES(16,4,1,7,3,'商品列表','验证商品列表','GET','/api/v1/products','{}','{}',NULL,'json','[]',30,0,'["product", "P0"]',2,true,2,'2026-05-17 11:24:00','success','2026-01-31 09:37:00','2026-05-30 12:53:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO api_test_cases(id,collection_id,project_id,user_id,environment_id,name,description,method,url,headers,params,body,body_type,assertions,timeout,retry_count,tags,priority,is_enabled,sort_order,last_run_at,last_status,created_at,updated_at)VALUES(17,4,1,6,3,'创建订单','验证创建订单','POST','/api/v1/orders','{}','{}',NULL,'json','[]',30,0,'["order", "P0"]',2,true,3,'2026-06-01 14:30:00','failed','2025-12-15 15:24:00','2026-05-31 10:57:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO api_test_cases(id,collection_id,project_id,user_id,environment_id,name,description,method,url,headers,params,body,body_type,assertions,timeout,retry_count,tags,priority,is_enabled,sort_order,last_run_at,last_status,created_at,updated_at)VALUES(18,4,1,7,4,'健康检查','验证健康检查','GET','/api/v1/health','{}','{}',NULL,'json','[]',30,0,'["health", "P0"]',3,true,4,'2026-05-21 05:08:00','success','2026-03-31 08:24:00','2026-06-02 03:59:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO api_test_cases(id,collection_id,project_id,user_id,environment_id,name,description,method,url,headers,params,body,body_type,assertions,timeout,retry_count,tags,priority,is_enabled,sort_order,last_run_at,last_status,created_at,updated_at)VALUES(19,4,1,6,3,'取消订单','验证取消订单','POST','/api/v1/orders/1001/cancel','{}','{}',NULL,'json','[]',30,0,'["order", "P1"]',2,true,5,'2026-05-19 11:47:00','success','2026-01-23 14:02:00','2026-05-29 10:14:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO api_test_cases(id,collection_id,project_id,user_id,environment_id,name,description,method,url,headers,params,body,body_type,assertions,timeout,retry_count,tags,priority,is_enabled,sort_order,last_run_at,last_status,created_at,updated_at)VALUES(20,5,1,7,3,'创建订单','验证创建订单','POST','/api/v1/orders','{}','{}',NULL,'json','[]',30,0,'["order", "P0"]',2,true,0,'2026-05-17 17:36:00','cancelled','2026-04-17 19:02:00','2026-05-30 16:38:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO api_test_cases(id,collection_id,project_id,user_id,environment_id,name,description,method,url,headers,params,body,body_type,assertions,timeout,retry_count,tags,priority,is_enabled,sort_order,last_run_at,last_status,created_at,updated_at)VALUES(21,5,1,5,4,'提交反馈','验证提交反馈','POST','/api/v1/feedback','{}','{}',NULL,'json','[]',30,0,'["feedback", "P2"]',2,true,1,'2026-05-26 01:25:00','success','2026-04-05 00:11:00','2026-05-30 11:47:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO api_test_cases(id,collection_id,project_id,user_id,environment_id,name,description,method,url,headers,params,body,body_type,assertions,timeout,retry_count,tags,priority,is_enabled,sort_order,last_run_at,last_status,created_at,updated_at)VALUES(22,5,1,6,3,'取消订单','验证取消订单','POST','/api/v1/orders/1001/cancel','{}','{}',NULL,'json','[]',30,0,'["order", "P1"]',2,true,2,'2026-05-25 00:53:00','success','2025-12-09 16:36:00','2026-05-29 22:11:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO api_test_cases(id,collection_id,project_id,user_id,environment_id,name,description,method,url,headers,params,body,body_type,assertions,timeout,retry_count,tags,priority,is_enabled,sort_order,last_run_at,last_status,created_at,updated_at)VALUES(23,6,1,5,4,'申请退款','验证申请退款','POST','/api/v1/refunds','{}','{}',NULL,'json','[]',30,0,'["payment", "P1"]',2,true,0,'2026-05-18 03:48:00','failed','2026-03-23 16:16:00','2026-05-31 05:54:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO api_test_cases(id,collection_id,project_id,user_id,environment_id,name,description,method,url,headers,params,body,body_type,assertions,timeout,retry_count,tags,priority,is_enabled,sort_order,last_run_at,last_status,created_at,updated_at)VALUES(24,6,1,7,2,'用户信息','验证用户信息','GET','/api/v1/users/me','{}','{}',NULL,'json','[]',30,0,'["user", "P0"]',1,true,1,'2026-05-25 13:46:00','success','2026-05-06 20:39:00','2026-05-30 06:17:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO api_test_cases(id,collection_id,project_id,user_id,environment_id,name,description,method,url,headers,params,body,body_type,assertions,timeout,retry_count,tags,priority,is_enabled,sort_order,last_run_at,last_status,created_at,updated_at)VALUES(25,6,1,2,1,'健康检查','验证健康检查','GET','/api/v1/health','{}','{}',NULL,'json','[]',30,0,'["health", "P0"]',1,true,2,NULL,'pending','2026-02-16 13:01:00','2026-05-29 18:19:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO api_test_cases(id,collection_id,project_id,user_id,environment_id,name,description,method,url,headers,params,body,body_type,assertions,timeout,retry_count,tags,priority,is_enabled,sort_order,last_run_at,last_status,created_at,updated_at)VALUES(26,6,1,2,3,'更新资料','验证更新资料','PUT','/api/v1/users/me','{}','{}',NULL,'json','[]',30,0,'["user", "P1"]',2,true,3,'2026-06-01 07:19:00','success','2026-04-02 16:13:00','2026-06-02 04:34:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO api_test_cases(id,collection_id,project_id,user_id,environment_id,name,description,method,url,headers,params,body,body_type,assertions,timeout,retry_count,tags,priority,is_enabled,sort_order,last_run_at,last_status,created_at,updated_at)VALUES(27,7,1,5,1,'用户信息','验证用户信息','GET','/api/v1/users/me','{}','{}',NULL,'json','[]',30,0,'["user", "P0"]',2,true,0,'2026-05-29 23:42:00','success','2025-12-18 16:27:00','2026-05-30 05:06:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO api_test_cases(id,collection_id,project_id,user_id,environment_id,name,description,method,url,headers,params,body,body_type,assertions,timeout,retry_count,tags,priority,is_enabled,sort_order,last_run_at,last_status,created_at,updated_at)VALUES(28,7,1,7,4,'搜索商品','验证搜索商品','GET','/api/v1/search','{}','{}',NULL,'json','[]',30,0,'["search", "P1"]',3,true,1,'2026-05-29 23:50:00','success','2026-02-03 13:44:00','2026-06-01 09:13:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO api_test_cases(id,collection_id,project_id,user_id,environment_id,name,description,method,url,headers,params,body,body_type,assertions,timeout,retry_count,tags,priority,is_enabled,sort_order,last_run_at,last_status,created_at,updated_at)VALUES(29,7,1,5,3,'获取配置','验证获取配置','GET','/api/v1/config','{}','{}',NULL,'json','[]',30,0,'["config", "P2"]',3,true,2,'2026-05-27 04:21:00','success','2026-02-17 20:28:00','2026-05-31 07:35:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO api_test_cases(id,collection_id,project_id,user_id,environment_id,name,description,method,url,headers,params,body,body_type,assertions,timeout,retry_count,tags,priority,is_enabled,sort_order,last_run_at,last_status,created_at,updated_at)VALUES(30,7,1,1,2,'订单详情','验证订单详情','GET','/api/v1/orders/1001','{}','{}',NULL,'json','[]',30,0,'["order", "P0"]',1,true,3,'2026-05-17 23:01:00','cancelled','2026-05-31 01:36:00','2026-05-31 19:12:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO api_test_cases(id,collection_id,project_id,user_id,environment_id,name,description,method,url,headers,params,body,body_type,assertions,timeout,retry_count,tags,priority,is_enabled,sort_order,last_run_at,last_status,created_at,updated_at)VALUES(31,8,2,2,5,'消息列表','验证消息列表','GET','/api/v1/messages','{}','{}',NULL,'json','[]',30,0,'["message", "P1"]',2,true,0,'2026-05-19 00:50:00','failed','2025-12-07 17:01:00','2026-05-30 11:53:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO api_test_cases(id,collection_id,project_id,user_id,environment_id,name,description,method,url,headers,params,body,body_type,assertions,timeout,retry_count,tags,priority,is_enabled,sort_order,last_run_at,last_status,created_at,updated_at)VALUES(32,8,2,5,7,'申请退款','验证申请退款','POST','/api/v1/refunds','{}','{}',NULL,'json','[]',30,0,'["payment", "P1"]',1,true,1,'2026-05-26 05:30:00','success','2026-02-04 10:22:00','2026-05-30 20:16:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO api_test_cases(id,collection_id,project_id,user_id,environment_id,name,description,method,url,headers,params,body,body_type,assertions,timeout,retry_count,tags,priority,is_enabled,sort_order,last_run_at,last_status,created_at,updated_at)VALUES(33,8,2,7,8,'用户登录','验证用户登录','POST','/api/v1/auth/login','{}','{}',NULL,'json','[]',30,0,'["auth", "P0"]',2,true,2,'2026-05-27 02:17:00','failed','2025-11-12 07:27:00','2026-05-29 17:15:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO api_test_cases(id,collection_id,project_id,user_id,environment_id,name,description,method,url,headers,params,body,body_type,assertions,timeout,retry_count,tags,priority,is_enabled,sort_order,last_run_at,last_status,created_at,updated_at)VALUES(34,8,2,5,5,'支付状态','验证支付状态','GET','/api/v1/payments/1001','{}','{}',NULL,'json','[]',30,0,'["payment", "P1"]',2,true,3,'2026-05-30 08:07:00','running','2026-01-23 03:24:00','2026-06-01 04:40:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO api_test_cases(id,collection_id,project_id,user_id,environment_id,name,description,method,url,headers,params,body,body_type,assertions,timeout,retry_count,tags,priority,is_enabled,sort_order,last_run_at,last_status,created_at,updated_at)VALUES(35,8,2,7,8,'标记已读','验证标记已读','PUT','/api/v1/messages/1001','{}','{}',NULL,'json','[]',30,0,'["message", "P2"]',2,true,4,'2026-05-26 11:23:00','success','2026-05-08 17:32:00','2026-06-01 19:52:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO api_test_cases(id,collection_id,project_id,user_id,environment_id,name,description,method,url,headers,params,body,body_type,assertions,timeout,retry_count,tags,priority,is_enabled,sort_order,last_run_at,last_status,created_at,updated_at)VALUES(36,9,2,6,7,'推荐列表','验证推荐列表','GET','/api/v1/recommendations','{}','{}',NULL,'json','[]',30,0,'["recommendation", "P2"]',1,true,0,'2026-05-26 15:56:00','failed','2026-02-12 22:16:00','2026-06-01 16:57:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO api_test_cases(id,collection_id,project_id,user_id,environment_id,name,description,method,url,headers,params,body,body_type,assertions,timeout,retry_count,tags,priority,is_enabled,sort_order,last_run_at,last_status,created_at,updated_at)VALUES(37,9,2,1,8,'上传图片','验证上传图片','POST','/api/v1/upload','{}','{}',NULL,'json','[]',30,0,'["upload", "P1"]',1,true,1,'2026-05-20 04:11:00','success','2025-11-16 13:14:00','2026-05-29 22:03:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO api_test_cases(id,collection_id,project_id,user_id,environment_id,name,description,method,url,headers,params,body,body_type,assertions,timeout,retry_count,tags,priority,is_enabled,sort_order,last_run_at,last_status,created_at,updated_at)VALUES(38,9,2,6,8,'用户信息','验证用户信息','GET','/api/v1/users/me','{}','{}',NULL,'json','[]',30,0,'["user", "P0"]',3,true,2,'2026-05-20 21:55:00','running','2025-12-13 16:52:00','2026-05-31 06:49:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO api_test_cases(id,collection_id,project_id,user_id,environment_id,name,description,method,url,headers,params,body,body_type,assertions,timeout,retry_count,tags,priority,is_enabled,sort_order,last_run_at,last_status,created_at,updated_at)VALUES(39,9,2,7,8,'领取券','验证领取券','POST','/api/v1/coupons/1001','{}','{}',NULL,'json','[]',30,0,'["marketing", "P1"]',1,true,3,'2026-05-26 09:12:00','success','2026-03-16 19:17:00','2026-05-29 16:36:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO api_test_cases(id,collection_id,project_id,user_id,environment_id,name,description,method,url,headers,params,body,body_type,assertions,timeout,retry_count,tags,priority,is_enabled,sort_order,last_run_at,last_status,created_at,updated_at)VALUES(40,9,2,2,6,'申请退款','验证申请退款','POST','/api/v1/refunds','{}','{}',NULL,'json','[]',30,0,'["payment", "P1"]',3,true,4,'2026-05-29 01:48:00','success','2025-11-18 06:58:00','2026-05-29 14:11:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO api_test_cases(id,collection_id,project_id,user_id,environment_id,name,description,method,url,headers,params,body,body_type,assertions,timeout,retry_count,tags,priority,is_enabled,sort_order,last_run_at,last_status,created_at,updated_at)VALUES(41,9,2,1,6,'标记已读','验证标记已读','PUT','/api/v1/messages/1001','{}','{}',NULL,'json','[]',30,0,'["message", "P2"]',2,true,5,'2026-05-29 14:58:00','success','2025-12-29 12:15:00','2026-06-02 02:13:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO api_test_cases(id,collection_id,project_id,user_id,environment_id,name,description,method,url,headers,params,body,body_type,assertions,timeout,retry_count,tags,priority,is_enabled,sort_order,last_run_at,last_status,created_at,updated_at)VALUES(42,9,2,1,8,'用户登录','验证用户登录','POST','/api/v1/auth/login','{}','{}',NULL,'json','[]',30,0,'["auth", "P0"]',2,true,6,'2026-05-27 08:52:00','success','2026-03-19 02:08:00','2026-05-30 15:22:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO api_test_cases(id,collection_id,project_id,user_id,environment_id,name,description,method,url,headers,params,body,body_type,assertions,timeout,retry_count,tags,priority,is_enabled,sort_order,last_run_at,last_status,created_at,updated_at)VALUES(43,10,2,1,6,'消息列表','验证消息列表','GET','/api/v1/messages','{}','{}',NULL,'json','[]',30,0,'["message", "P1"]',1,true,0,'2026-05-19 16:29:00','success','2026-03-04 13:18:00','2026-05-29 17:40:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO api_test_cases(id,collection_id,project_id,user_id,environment_id,name,description,method,url,headers,params,body,body_type,assertions,timeout,retry_count,tags,priority,is_enabled,sort_order,last_run_at,last_status,created_at,updated_at)VALUES(44,10,2,6,8,'发起支付','验证发起支付','POST','/api/v1/payments','{}','{}',NULL,'json','[]',30,0,'["payment", "P0"]',2,true,1,'2026-05-21 04:12:00','success','2026-01-31 02:06:00','2026-06-01 00:06:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO api_test_cases(id,collection_id,project_id,user_id,environment_id,name,description,method,url,headers,params,body,body_type,assertions,timeout,retry_count,tags,priority,is_enabled,sort_order,last_run_at,last_status,created_at,updated_at)VALUES(45,10,2,2,8,'申请退款','验证申请退款','POST','/api/v1/refunds','{}','{}',NULL,'json','[]',30,0,'["payment", "P1"]',2,true,2,'2026-05-19 20:25:00','running','2026-04-27 21:45:00','2026-05-31 03:39:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO api_test_cases(id,collection_id,project_id,user_id,environment_id,name,description,method,url,headers,params,body,body_type,assertions,timeout,retry_count,tags,priority,is_enabled,sort_order,last_run_at,last_status,created_at,updated_at)VALUES(46,10,2,1,8,'创建订单','验证创建订单','POST','/api/v1/orders','{}','{}',NULL,'json','[]',30,0,'["order", "P0"]',1,true,3,'2026-05-30 16:14:00','failed','2026-05-19 01:36:00','2026-06-02 07:48:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO api_test_cases(id,collection_id,project_id,user_id,environment_id,name,description,method,url,headers,params,body,body_type,assertions,timeout,retry_count,tags,priority,is_enabled,sort_order,last_run_at,last_status,created_at,updated_at)VALUES(47,10,2,7,6,'领取券','验证领取券','POST','/api/v1/coupons/1001','{}','{}',NULL,'json','[]',30,0,'["marketing", "P1"]',1,true,4,'2026-05-23 00:02:00','success','2026-04-08 03:13:00','2026-06-01 10:12:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO api_test_cases(id,collection_id,project_id,user_id,environment_id,name,description,method,url,headers,params,body,body_type,assertions,timeout,retry_count,tags,priority,is_enabled,sort_order,last_run_at,last_status,created_at,updated_at)VALUES(48,10,2,6,6,'取消订单','验证取消订单','POST','/api/v1/orders/1001/cancel','{}','{}',NULL,'json','[]',30,0,'["order", "P1"]',1,true,5,'2026-05-26 21:02:00','failed','2026-01-10 23:11:00','2026-05-30 21:31:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO api_test_cases(id,collection_id,project_id,user_id,environment_id,name,description,method,url,headers,params,body,body_type,assertions,timeout,retry_count,tags,priority,is_enabled,sort_order,last_run_at,last_status,created_at,updated_at)VALUES(49,10,2,7,7,'提交反馈','验证提交反馈','POST','/api/v1/feedback','{}','{}',NULL,'json','[]',30,0,'["feedback", "P2"]',2,true,6,'2026-05-21 17:04:00','success','2026-02-02 06:09:00','2026-05-29 23:02:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO api_test_cases(id,collection_id,project_id,user_id,environment_id,name,description,method,url,headers,params,body,body_type,assertions,timeout,retry_count,tags,priority,is_enabled,sort_order,last_run_at,last_status,created_at,updated_at)VALUES(50,10,2,2,7,'推荐列表','验证推荐列表','GET','/api/v1/recommendations','{}','{}',NULL,'json','[]',30,0,'["recommendation", "P2"]',1,true,7,'2026-05-31 15:05:00','success','2025-11-24 05:59:00','2026-05-30 16:01:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO api_test_cases(id,collection_id,project_id,user_id,environment_id,name,description,method,url,headers,params,body,body_type,assertions,timeout,retry_count,tags,priority,is_enabled,sort_order,last_run_at,last_status,created_at,updated_at)VALUES(51,11,2,6,6,'领取券','验证领取券','POST','/api/v1/coupons/1001','{}','{}',NULL,'json','[]',30,0,'["marketing", "P1"]',2,true,0,'2026-05-23 01:12:00','success','2025-11-27 13:13:00','2026-05-29 19:50:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO api_test_cases(id,collection_id,project_id,user_id,environment_id,name,description,method,url,headers,params,body,body_type,assertions,timeout,retry_count,tags,priority,is_enabled,sort_order,last_run_at,last_status,created_at,updated_at)VALUES(52,11,2,5,6,'推荐列表','验证推荐列表','GET','/api/v1/recommendations','{}','{}',NULL,'json','[]',30,0,'["recommendation", "P2"]',2,true,1,'2026-05-18 04:02:00','success','2025-12-19 08:27:00','2026-06-02 07:08:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO api_test_cases(id,collection_id,project_id,user_id,environment_id,name,description,method,url,headers,params,body,body_type,assertions,timeout,retry_count,tags,priority,is_enabled,sort_order,last_run_at,last_status,created_at,updated_at)VALUES(53,11,2,1,5,'申请退款','验证申请退款','POST','/api/v1/refunds','{}','{}',NULL,'json','[]',30,0,'["payment", "P1"]',1,true,2,'2026-05-26 07:15:00','success','2026-05-30 03:28:00','2026-05-29 22:57:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO api_test_cases(id,collection_id,project_id,user_id,environment_id,name,description,method,url,headers,params,body,body_type,assertions,timeout,retry_count,tags,priority,is_enabled,sort_order,last_run_at,last_status,created_at,updated_at)VALUES(54,11,2,7,8,'创建订单','验证创建订单','POST','/api/v1/orders','{}','{}',NULL,'json','[]',30,0,'["order", "P0"]',2,true,3,'2026-06-02 09:26:00','failed','2026-02-16 09:59:00','2026-05-30 16:42:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO api_test_cases(id,collection_id,project_id,user_id,environment_id,name,description,method,url,headers,params,body,body_type,assertions,timeout,retry_count,tags,priority,is_enabled,sort_order,last_run_at,last_status,created_at,updated_at)VALUES(55,11,2,1,8,'取消订单','验证取消订单','POST','/api/v1/orders/1001/cancel','{}','{}',NULL,'json','[]',30,0,'["order", "P1"]',1,true,4,'2026-05-28 06:02:00','failed','2026-01-18 05:45:00','2026-05-31 14:27:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO api_test_cases(id,collection_id,project_id,user_id,environment_id,name,description,method,url,headers,params,body,body_type,assertions,timeout,retry_count,tags,priority,is_enabled,sort_order,last_run_at,last_status,created_at,updated_at)VALUES(56,11,2,5,7,'订单详情','验证订单详情','GET','/api/v1/orders/1001','{}','{}',NULL,'json','[]',30,0,'["order", "P0"]',2,true,5,'2026-05-21 07:37:00','success','2026-02-03 15:45:00','2026-06-01 00:17:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO api_test_cases(id,collection_id,project_id,user_id,environment_id,name,description,method,url,headers,params,body,body_type,assertions,timeout,retry_count,tags,priority,is_enabled,sort_order,last_run_at,last_status,created_at,updated_at)VALUES(57,11,2,1,5,'商品列表','验证商品列表','GET','/api/v1/products','{}','{}',NULL,'json','[]',30,0,'["product", "P0"]',2,true,6,'2026-05-20 21:25:00','success','2026-05-17 14:00:00','2026-06-01 07:29:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO api_test_cases(id,collection_id,project_id,user_id,environment_id,name,description,method,url,headers,params,body,body_type,assertions,timeout,retry_count,tags,priority,is_enabled,sort_order,last_run_at,last_status,created_at,updated_at)VALUES(58,12,2,2,8,'消息列表','验证消息列表','GET','/api/v1/messages','{}','{}',NULL,'json','[]',30,0,'["message", "P1"]',2,true,0,'2026-05-30 12:01:00','success','2026-01-12 15:18:00','2026-06-02 04:01:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO api_test_cases(id,collection_id,project_id,user_id,environment_id,name,description,method,url,headers,params,body,body_type,assertions,timeout,retry_count,tags,priority,is_enabled,sort_order,last_run_at,last_status,created_at,updated_at)VALUES(59,12,2,5,5,'领取券','验证领取券','POST','/api/v1/coupons/1001','{}','{}',NULL,'json','[]',30,0,'["marketing", "P1"]',2,true,1,NULL,'pending','2026-04-25 11:08:00','2026-05-30 07:41:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO api_test_cases(id,collection_id,project_id,user_id,environment_id,name,description,method,url,headers,params,body,body_type,assertions,timeout,retry_count,tags,priority,is_enabled,sort_order,last_run_at,last_status,created_at,updated_at)VALUES(60,12,2,2,6,'商品列表','验证商品列表','GET','/api/v1/products','{}','{}',NULL,'json','[]',30,0,'["product", "P0"]',2,true,2,'2026-05-20 12:03:00','success','2026-03-08 21:12:00','2026-05-31 11:14:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO api_test_cases(id,collection_id,project_id,user_id,environment_id,name,description,method,url,headers,params,body,body_type,assertions,timeout,retry_count,tags,priority,is_enabled,sort_order,last_run_at,last_status,created_at,updated_at)VALUES(61,12,2,1,7,'提交反馈','验证提交反馈','POST','/api/v1/feedback','{}','{}',NULL,'json','[]',30,0,'["feedback", "P2"]',1,true,3,'2026-05-20 02:07:00','success','2026-03-05 14:11:00','2026-05-29 23:59:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO api_test_cases(id,collection_id,project_id,user_id,environment_id,name,description,method,url,headers,params,body,body_type,assertions,timeout,retry_count,tags,priority,is_enabled,sort_order,last_run_at,last_status,created_at,updated_at)VALUES(62,12,2,5,8,'用户信息','验证用户信息','GET','/api/v1/users/me','{}','{}',NULL,'json','[]',30,0,'["user", "P0"]',2,true,4,'2026-05-21 16:36:00','success','2026-04-14 12:23:00','2026-05-30 07:11:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO api_test_cases(id,collection_id,project_id,user_id,environment_id,name,description,method,url,headers,params,body,body_type,assertions,timeout,retry_count,tags,priority,is_enabled,sort_order,last_run_at,last_status,created_at,updated_at)VALUES(63,12,2,7,7,'优惠券','验证优惠券','GET','/api/v1/coupons','{}','{}',NULL,'json','[]',30,0,'["marketing", "P1"]',1,true,5,'2026-05-31 07:43:00','failed','2026-02-23 11:10:00','2026-05-31 10:36:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO api_test_cases(id,collection_id,project_id,user_id,environment_id,name,description,method,url,headers,params,body,body_type,assertions,timeout,retry_count,tags,priority,is_enabled,sort_order,last_run_at,last_status,created_at,updated_at)VALUES(64,13,2,6,7,'标记已读','验证标记已读','PUT','/api/v1/messages/1001','{}','{}',NULL,'json','[]',30,0,'["message", "P2"]',1,true,0,'2026-05-30 05:55:00','failed','2026-02-10 19:25:00','2026-05-30 06:59:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO api_test_cases(id,collection_id,project_id,user_id,environment_id,name,description,method,url,headers,params,body,body_type,assertions,timeout,retry_count,tags,priority,is_enabled,sort_order,last_run_at,last_status,created_at,updated_at)VALUES(65,13,2,1,7,'商品列表','验证商品列表','GET','/api/v1/products','{}','{}',NULL,'json','[]',30,0,'["product", "P0"]',2,true,1,'2026-05-22 22:00:00','success','2026-02-15 21:11:00','2026-06-01 10:03:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO api_test_cases(id,collection_id,project_id,user_id,environment_id,name,description,method,url,headers,params,body,body_type,assertions,timeout,retry_count,tags,priority,is_enabled,sort_order,last_run_at,last_status,created_at,updated_at)VALUES(66,13,2,7,6,'更新资料','验证更新资料','PUT','/api/v1/users/me','{}','{}',NULL,'json','[]',30,0,'["user", "P1"]',1,true,2,'2026-05-27 12:36:00','success','2026-04-27 01:41:00','2026-05-30 18:51:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO api_test_cases(id,collection_id,project_id,user_id,environment_id,name,description,method,url,headers,params,body,body_type,assertions,timeout,retry_count,tags,priority,is_enabled,sort_order,last_run_at,last_status,created_at,updated_at)VALUES(67,13,2,1,6,'用户登录','验证用户登录','POST','/api/v1/auth/login','{}','{}',NULL,'json','[]',30,0,'["auth", "P0"]',1,true,3,'2026-05-20 00:30:00','success','2026-03-01 01:45:00','2026-05-29 14:21:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO api_test_cases(id,collection_id,project_id,user_id,environment_id,name,description,method,url,headers,params,body,body_type,assertions,timeout,retry_count,tags,priority,is_enabled,sort_order,last_run_at,last_status,created_at,updated_at)VALUES(68,13,2,2,8,'申请退款','验证申请退款','POST','/api/v1/refunds','{}','{}',NULL,'json','[]',30,0,'["payment", "P1"]',2,true,4,'2026-05-24 09:35:00','success','2025-12-24 21:09:00','2026-05-30 19:39:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO api_test_cases(id,collection_id,project_id,user_id,environment_id,name,description,method,url,headers,params,body,body_type,assertions,timeout,retry_count,tags,priority,is_enabled,sort_order,last_run_at,last_status,created_at,updated_at)VALUES(69,14,2,5,6,'健康检查','验证健康检查','GET','/api/v1/health','{}','{}',NULL,'json','[]',30,0,'["health", "P0"]',2,true,0,NULL,'pending','2026-03-18 10:16:00','2026-05-29 15:10:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO api_test_cases(id,collection_id,project_id,user_id,environment_id,name,description,method,url,headers,params,body,body_type,assertions,timeout,retry_count,tags,priority,is_enabled,sort_order,last_run_at,last_status,created_at,updated_at)VALUES(70,14,2,2,7,'创建订单','验证创建订单','POST','/api/v1/orders','{}','{}',NULL,'json','[]',30,0,'["order", "P0"]',2,true,1,'2026-05-20 22:53:00','success','2026-04-10 15:26:00','2026-05-31 12:11:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO api_test_cases(id,collection_id,project_id,user_id,environment_id,name,description,method,url,headers,params,body,body_type,assertions,timeout,retry_count,tags,priority,is_enabled,sort_order,last_run_at,last_status,created_at,updated_at)VALUES(71,14,2,7,5,'申请退款','验证申请退款','POST','/api/v1/refunds','{}','{}',NULL,'json','[]',30,0,'["payment", "P1"]',2,true,2,NULL,'pending','2025-12-02 03:32:00','2026-05-30 11:56:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO api_test_cases(id,collection_id,project_id,user_id,environment_id,name,description,method,url,headers,params,body,body_type,assertions,timeout,retry_count,tags,priority,is_enabled,sort_order,last_run_at,last_status,created_at,updated_at)VALUES(72,14,2,6,8,'消息列表','验证消息列表','GET','/api/v1/messages','{}','{}',NULL,'json','[]',30,0,'["message", "P1"]',3,true,3,'2026-05-24 02:44:00','success','2026-04-22 11:33:00','2026-05-30 07:32:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO api_test_cases(id,collection_id,project_id,user_id,environment_id,name,description,method,url,headers,params,body,body_type,assertions,timeout,retry_count,tags,priority,is_enabled,sort_order,last_run_at,last_status,created_at,updated_at)VALUES(73,14,2,7,8,'取消订单','验证取消订单','POST','/api/v1/orders/1001/cancel','{}','{}',NULL,'json','[]',30,0,'["order", "P1"]',2,true,4,'2026-05-19 16:58:00','success','2025-12-03 16:22:00','2026-06-02 06:11:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO api_test_cases(id,collection_id,project_id,user_id,environment_id,name,description,method,url,headers,params,body,body_type,assertions,timeout,retry_count,tags,priority,is_enabled,sort_order,last_run_at,last_status,created_at,updated_at)VALUES(74,14,2,2,7,'发起支付','验证发起支付','POST','/api/v1/payments','{}','{}',NULL,'json','[]',30,0,'["payment", "P0"]',3,true,5,'2026-05-31 15:19:00','success','2025-12-17 21:12:00','2026-05-30 20:54:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO api_test_cases(id,collection_id,project_id,user_id,environment_id,name,description,method,url,headers,params,body,body_type,assertions,timeout,retry_count,tags,priority,is_enabled,sort_order,last_run_at,last_status,created_at,updated_at)VALUES(75,15,3,7,10,'商品列表','验证商品列表','GET','/api/v1/products','{}','{}',NULL,'json','[]',30,0,'["product", "P0"]',3,true,0,'2026-05-20 19:11:00','success','2026-01-01 11:28:00','2026-05-31 22:59:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO api_test_cases(id,collection_id,project_id,user_id,environment_id,name,description,method,url,headers,params,body,body_type,assertions,timeout,retry_count,tags,priority,is_enabled,sort_order,last_run_at,last_status,created_at,updated_at)VALUES(76,15,3,6,9,'支付状态','验证支付状态','GET','/api/v1/payments/1001','{}','{}',NULL,'json','[]',30,0,'["payment", "P1"]',3,true,1,'2026-05-31 06:07:00','success','2026-04-25 22:41:00','2026-05-30 19:10:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO api_test_cases(id,collection_id,project_id,user_id,environment_id,name,description,method,url,headers,params,body,body_type,assertions,timeout,retry_count,tags,priority,is_enabled,sort_order,last_run_at,last_status,created_at,updated_at)VALUES(77,15,3,2,12,'发起支付','验证发起支付','POST','/api/v1/payments','{}','{}',NULL,'json','[]',30,0,'["payment", "P0"]',3,true,2,'2026-05-29 19:14:00','success','2026-02-05 23:56:00','2026-05-31 08:09:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO api_test_cases(id,collection_id,project_id,user_id,environment_id,name,description,method,url,headers,params,body,body_type,assertions,timeout,retry_count,tags,priority,is_enabled,sort_order,last_run_at,last_status,created_at,updated_at)VALUES(78,16,3,7,10,'商品列表','验证商品列表','GET','/api/v1/products','{}','{}',NULL,'json','[]',30,0,'["product", "P0"]',2,true,0,'2026-05-22 16:33:00','success','2026-04-02 21:20:00','2026-06-01 04:20:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO api_test_cases(id,collection_id,project_id,user_id,environment_id,name,description,method,url,headers,params,body,body_type,assertions,timeout,retry_count,tags,priority,is_enabled,sort_order,last_run_at,last_status,created_at,updated_at)VALUES(79,16,3,6,12,'用户登录','验证用户登录','POST','/api/v1/auth/login','{}','{}',NULL,'json','[]',30,0,'["auth", "P0"]',2,true,1,'2026-05-26 19:23:00','success','2026-02-22 09:15:00','2026-06-01 03:43:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO api_test_cases(id,collection_id,project_id,user_id,environment_id,name,description,method,url,headers,params,body,body_type,assertions,timeout,retry_count,tags,priority,is_enabled,sort_order,last_run_at,last_status,created_at,updated_at)VALUES(80,16,3,1,9,'消息列表','验证消息列表','GET','/api/v1/messages','{}','{}',NULL,'json','[]',30,0,'["message", "P1"]',1,true,2,'2026-05-27 22:40:00','failed','2026-02-04 06:44:00','2026-05-29 17:20:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO api_test_cases(id,collection_id,project_id,user_id,environment_id,name,description,method,url,headers,params,body,body_type,assertions,timeout,retry_count,tags,priority,is_enabled,sort_order,last_run_at,last_status,created_at,updated_at)VALUES(81,16,3,5,12,'健康检查','验证健康检查','GET','/api/v1/health','{}','{}',NULL,'json','[]',30,0,'["health", "P0"]',2,true,3,'2026-05-29 22:38:00','success','2025-12-25 04:08:00','2026-05-30 14:23:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO api_test_cases(id,collection_id,project_id,user_id,environment_id,name,description,method,url,headers,params,body,body_type,assertions,timeout,retry_count,tags,priority,is_enabled,sort_order,last_run_at,last_status,created_at,updated_at)VALUES(82,16,3,1,10,'订单详情','验证订单详情','GET','/api/v1/orders/1001','{}','{}',NULL,'json','[]',30,0,'["order", "P0"]',1,true,4,'2026-05-26 00:53:00','success','2026-02-25 11:51:00','2026-05-29 20:22:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO api_test_cases(id,collection_id,project_id,user_id,environment_id,name,description,method,url,headers,params,body,body_type,assertions,timeout,retry_count,tags,priority,is_enabled,sort_order,last_run_at,last_status,created_at,updated_at)VALUES(83,16,3,2,12,'上传图片','验证上传图片','POST','/api/v1/upload','{}','{}',NULL,'json','[]',30,0,'["upload", "P1"]',3,true,5,'2026-05-17 13:26:00','success','2025-12-18 04:25:00','2026-05-31 18:42:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO api_test_cases(id,collection_id,project_id,user_id,environment_id,name,description,method,url,headers,params,body,body_type,assertions,timeout,retry_count,tags,priority,is_enabled,sort_order,last_run_at,last_status,created_at,updated_at)VALUES(84,16,3,2,10,'标记已读','验证标记已读','PUT','/api/v1/messages/1001','{}','{}',NULL,'json','[]',30,0,'["message", "P2"]',2,true,6,'2026-05-18 14:57:00','success','2026-05-29 18:52:00','2026-05-31 21:25:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO api_test_cases(id,collection_id,project_id,user_id,environment_id,name,description,method,url,headers,params,body,body_type,assertions,timeout,retry_count,tags,priority,is_enabled,sort_order,last_run_at,last_status,created_at,updated_at)VALUES(85,16,3,7,12,'提交反馈','验证提交反馈','POST','/api/v1/feedback','{}','{}',NULL,'json','[]',30,0,'["feedback", "P2"]',2,true,7,'2026-05-17 20:15:00','success','2026-01-27 04:55:00','2026-06-02 02:42:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO api_test_cases(id,collection_id,project_id,user_id,environment_id,name,description,method,url,headers,params,body,body_type,assertions,timeout,retry_count,tags,priority,is_enabled,sort_order,last_run_at,last_status,created_at,updated_at)VALUES(86,17,3,5,10,'支付状态','验证支付状态','GET','/api/v1/payments/1001','{}','{}',NULL,'json','[]',30,0,'["payment", "P1"]',1,true,0,'2026-05-17 16:28:00','failed','2026-01-06 06:43:00','2026-05-30 16:08:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO api_test_cases(id,collection_id,project_id,user_id,environment_id,name,description,method,url,headers,params,body,body_type,assertions,timeout,retry_count,tags,priority,is_enabled,sort_order,last_run_at,last_status,created_at,updated_at)VALUES(87,17,3,1,12,'发起支付','验证发起支付','POST','/api/v1/payments','{}','{}',NULL,'json','[]',30,0,'["payment", "P0"]',3,true,1,'2026-05-20 06:13:00','success','2025-11-21 02:41:00','2026-06-01 19:44:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO api_test_cases(id,collection_id,project_id,user_id,environment_id,name,description,method,url,headers,params,body,body_type,assertions,timeout,retry_count,tags,priority,is_enabled,sort_order,last_run_at,last_status,created_at,updated_at)VALUES(88,17,3,5,9,'优惠券','验证优惠券','GET','/api/v1/coupons','{}','{}',NULL,'json','[]',30,0,'["marketing", "P1"]',3,true,2,'2026-05-30 02:47:00','success','2026-01-01 11:38:00','2026-05-30 04:21:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO api_test_cases(id,collection_id,project_id,user_id,environment_id,name,description,method,url,headers,params,body,body_type,assertions,timeout,retry_count,tags,priority,is_enabled,sort_order,last_run_at,last_status,created_at,updated_at)VALUES(89,18,3,7,11,'取消订单','验证取消订单','POST','/api/v1/orders/1001/cancel','{}','{}',NULL,'json','[]',30,0,'["order", "P1"]',2,true,0,'2026-05-27 23:15:00','success','2026-03-18 15:43:00','2026-06-02 05:12:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO api_test_cases(id,collection_id,project_id,user_id,environment_id,name,description,method,url,headers,params,body,body_type,assertions,timeout,retry_count,tags,priority,is_enabled,sort_order,last_run_at,last_status,created_at,updated_at)VALUES(90,18,3,6,9,'健康检查','验证健康检查','GET','/api/v1/health','{}','{}',NULL,'json','[]',30,0,'["health", "P0"]',1,true,1,'2026-05-28 11:05:00','cancelled','2026-03-30 05:15:00','2026-05-31 02:12:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO api_test_cases(id,collection_id,project_id,user_id,environment_id,name,description,method,url,headers,params,body,body_type,assertions,timeout,retry_count,tags,priority,is_enabled,sort_order,last_run_at,last_status,created_at,updated_at)VALUES(91,18,3,6,12,'用户信息','验证用户信息','GET','/api/v1/users/me','{}','{}',NULL,'json','[]',30,0,'["user", "P0"]',2,true,2,'2026-05-24 13:34:00','success','2026-02-06 07:20:00','2026-06-01 21:28:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO api_test_cases(id,collection_id,project_id,user_id,environment_id,name,description,method,url,headers,params,body,body_type,assertions,timeout,retry_count,tags,priority,is_enabled,sort_order,last_run_at,last_status,created_at,updated_at)VALUES(92,18,3,5,11,'标记已读','验证标记已读','PUT','/api/v1/messages/1001','{}','{}',NULL,'json','[]',30,0,'["message", "P2"]',1,true,3,'2026-05-17 23:23:00','success','2025-11-14 10:55:00','2026-05-29 13:18:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO api_test_cases(id,collection_id,project_id,user_id,environment_id,name,description,method,url,headers,params,body,body_type,assertions,timeout,retry_count,tags,priority,is_enabled,sort_order,last_run_at,last_status,created_at,updated_at)VALUES(93,19,3,6,11,'标记已读','验证标记已读','PUT','/api/v1/messages/1001','{}','{}',NULL,'json','[]',30,0,'["message", "P2"]',2,true,0,'2026-05-23 23:25:00','success','2026-04-28 15:06:00','2026-05-29 23:03:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO api_test_cases(id,collection_id,project_id,user_id,environment_id,name,description,method,url,headers,params,body,body_type,assertions,timeout,retry_count,tags,priority,is_enabled,sort_order,last_run_at,last_status,created_at,updated_at)VALUES(94,19,3,1,9,'更新资料','验证更新资料','PUT','/api/v1/users/me','{}','{}',NULL,'json','[]',30,0,'["user", "P1"]',1,true,1,'2026-05-19 09:53:00','success','2026-02-08 20:00:00','2026-05-30 03:16:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO api_test_cases(id,collection_id,project_id,user_id,environment_id,name,description,method,url,headers,params,body,body_type,assertions,timeout,retry_count,tags,priority,is_enabled,sort_order,last_run_at,last_status,created_at,updated_at)VALUES(95,19,3,2,11,'优惠券','验证优惠券','GET','/api/v1/coupons','{}','{}',NULL,'json','[]',30,0,'["marketing", "P1"]',2,true,2,'2026-05-25 07:19:00','success','2026-03-29 07:37:00','2026-06-01 08:35:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO api_test_cases(id,collection_id,project_id,user_id,environment_id,name,description,method,url,headers,params,body,body_type,assertions,timeout,retry_count,tags,priority,is_enabled,sort_order,last_run_at,last_status,created_at,updated_at)VALUES(96,19,3,5,10,'搜索商品','验证搜索商品','GET','/api/v1/search','{}','{}',NULL,'json','[]',30,0,'["search", "P1"]',1,true,3,'2026-05-30 11:54:00','success','2026-04-07 18:56:00','2026-05-31 15:46:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO api_test_cases(id,collection_id,project_id,user_id,environment_id,name,description,method,url,headers,params,body,body_type,assertions,timeout,retry_count,tags,priority,is_enabled,sort_order,last_run_at,last_status,created_at,updated_at)VALUES(97,19,3,7,12,'取消订单','验证取消订单','POST','/api/v1/orders/1001/cancel','{}','{}',NULL,'json','[]',30,0,'["order", "P1"]',2,true,4,'2026-05-23 06:05:00','success','2025-12-06 05:30:00','2026-06-02 02:36:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO api_test_cases(id,collection_id,project_id,user_id,environment_id,name,description,method,url,headers,params,body,body_type,assertions,timeout,retry_count,tags,priority,is_enabled,sort_order,last_run_at,last_status,created_at,updated_at)VALUES(98,19,3,1,9,'获取配置','验证获取配置','GET','/api/v1/config','{}','{}',NULL,'json','[]',30,0,'["config", "P2"]',2,true,5,'2026-05-22 00:52:00','success','2025-11-15 05:19:00','2026-06-01 07:27:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO api_test_cases(id,collection_id,project_id,user_id,environment_id,name,description,method,url,headers,params,body,body_type,assertions,timeout,retry_count,tags,priority,is_enabled,sort_order,last_run_at,last_status,created_at,updated_at)VALUES(99,19,3,7,9,'推荐列表','验证推荐列表','GET','/api/v1/recommendations','{}','{}',NULL,'json','[]',30,0,'["recommendation", "P2"]',3,true,6,'2026-05-27 19:38:00','success','2026-04-07 13:13:00','2026-05-31 20:21:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO api_test_cases(id,collection_id,project_id,user_id,environment_id,name,description,method,url,headers,params,body,body_type,assertions,timeout,retry_count,tags,priority,is_enabled,sort_order,last_run_at,last_status,created_at,updated_at)VALUES(100,19,3,6,10,'商品列表','验证商品列表','GET','/api/v1/products','{}','{}',NULL,'json','[]',30,0,'["product", "P0"]',1,true,7,'2026-05-30 05:12:00','success','2026-01-01 10:36:00','2026-05-30 20:40:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO api_test_cases(id,collection_id,project_id,user_id,environment_id,name,description,method,url,headers,params,body,body_type,assertions,timeout,retry_count,tags,priority,is_enabled,sort_order,last_run_at,last_status,created_at,updated_at)VALUES(101,20,3,7,11,'发起支付','验证发起支付','POST','/api/v1/payments','{}','{}',NULL,'json','[]',30,0,'["payment", "P0"]',2,true,0,'2026-06-01 12:04:00','failed','2026-04-09 17:22:00','2026-05-31 10:35:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO api_test_cases(id,collection_id,project_id,user_id,environment_id,name,description,method,url,headers,params,body,body_type,assertions,timeout,retry_count,tags,priority,is_enabled,sort_order,last_run_at,last_status,created_at,updated_at)VALUES(102,20,3,5,9,'支付状态','验证支付状态','GET','/api/v1/payments/1001','{}','{}',NULL,'json','[]',30,0,'["payment", "P1"]',1,true,1,'2026-05-25 18:36:00','failed','2026-03-31 18:20:00','2026-06-01 17:04:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO api_test_cases(id,collection_id,project_id,user_id,environment_id,name,description,method,url,headers,params,body,body_type,assertions,timeout,retry_count,tags,priority,is_enabled,sort_order,last_run_at,last_status,created_at,updated_at)VALUES(103,20,3,1,11,'更新资料','验证更新资料','PUT','/api/v1/users/me','{}','{}',NULL,'json','[]',30,0,'["user", "P1"]',1,true,2,NULL,'pending','2026-02-21 15:34:00','2026-05-30 16:17:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO api_test_cases(id,collection_id,project_id,user_id,environment_id,name,description,method,url,headers,params,body,body_type,assertions,timeout,retry_count,tags,priority,is_enabled,sort_order,last_run_at,last_status,created_at,updated_at)VALUES(104,20,3,2,12,'健康检查','验证健康检查','GET','/api/v1/health','{}','{}',NULL,'json','[]',30,0,'["health", "P0"]',1,true,3,NULL,'pending','2026-05-27 15:56:00','2026-06-02 01:47:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO api_test_cases(id,collection_id,project_id,user_id,environment_id,name,description,method,url,headers,params,body,body_type,assertions,timeout,retry_count,tags,priority,is_enabled,sort_order,last_run_at,last_status,created_at,updated_at)VALUES(105,21,3,5,12,'用户信息','验证用户信息','GET','/api/v1/users/me','{}','{}',NULL,'json','[]',30,0,'["user", "P0"]',2,true,0,'2026-05-21 07:20:00','success','2026-01-14 14:51:00','2026-05-31 07:41:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO api_test_cases(id,collection_id,project_id,user_id,environment_id,name,description,method,url,headers,params,body,body_type,assertions,timeout,retry_count,tags,priority,is_enabled,sort_order,last_run_at,last_status,created_at,updated_at)VALUES(106,21,3,1,10,'搜索商品','验证搜索商品','GET','/api/v1/search','{}','{}',NULL,'json','[]',30,0,'["search", "P1"]',2,true,1,'2026-05-28 16:40:00','cancelled','2026-01-01 13:12:00','2026-06-02 00:16:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO api_test_cases(id,collection_id,project_id,user_id,environment_id,name,description,method,url,headers,params,body,body_type,assertions,timeout,retry_count,tags,priority,is_enabled,sort_order,last_run_at,last_status,created_at,updated_at)VALUES(107,21,3,6,10,'提交反馈','验证提交反馈','POST','/api/v1/feedback','{}','{}',NULL,'json','[]',30,0,'["feedback", "P2"]',2,true,2,'2026-05-30 20:53:00','success','2025-12-26 14:57:00','2026-05-30 12:13:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO api_test_cases(id,collection_id,project_id,user_id,environment_id,name,description,method,url,headers,params,body,body_type,assertions,timeout,retry_count,tags,priority,is_enabled,sort_order,last_run_at,last_status,created_at,updated_at)VALUES(108,22,4,7,15,'订单详情','验证订单详情','GET','/api/v1/orders/1001','{}','{}',NULL,'json','[]',30,0,'["order", "P0"]',2,true,0,'2026-05-28 10:11:00','success','2025-11-26 06:11:00','2026-06-01 23:09:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO api_test_cases(id,collection_id,project_id,user_id,environment_id,name,description,method,url,headers,params,body,body_type,assertions,timeout,retry_count,tags,priority,is_enabled,sort_order,last_run_at,last_status,created_at,updated_at)VALUES(109,22,4,6,15,'商品列表','验证商品列表','GET','/api/v1/products','{}','{}',NULL,'json','[]',30,0,'["product", "P0"]',3,true,1,'2026-05-24 11:24:00','success','2026-05-12 18:31:00','2026-05-31 08:29:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO api_test_cases(id,collection_id,project_id,user_id,environment_id,name,description,method,url,headers,params,body,body_type,assertions,timeout,retry_count,tags,priority,is_enabled,sort_order,last_run_at,last_status,created_at,updated_at)VALUES(110,22,4,7,14,'用户登录','验证用户登录','POST','/api/v1/auth/login','{}','{}',NULL,'json','[]',30,0,'["auth", "P0"]',2,true,2,'2026-05-25 06:03:00','success','2025-12-10 10:53:00','2026-05-31 10:28:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO api_test_cases(id,collection_id,project_id,user_id,environment_id,name,description,method,url,headers,params,body,body_type,assertions,timeout,retry_count,tags,priority,is_enabled,sort_order,last_run_at,last_status,created_at,updated_at)VALUES(111,22,4,1,13,'创建订单','验证创建订单','POST','/api/v1/orders','{}','{}',NULL,'json','[]',30,0,'["order", "P0"]',2,true,3,'2026-06-02 02:58:00','running','2026-02-27 21:02:00','2026-06-01 04:01:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO api_test_cases(id,collection_id,project_id,user_id,environment_id,name,description,method,url,headers,params,body,body_type,assertions,timeout,retry_count,tags,priority,is_enabled,sort_order,last_run_at,last_status,created_at,updated_at)VALUES(112,22,4,1,16,'优惠券','验证优惠券','GET','/api/v1/coupons','{}','{}',NULL,'json','[]',30,0,'["marketing", "P1"]',3,true,4,'2026-05-25 20:02:00','success','2026-03-12 01:08:00','2026-06-01 15:37:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO api_test_cases(id,collection_id,project_id,user_id,environment_id,name,description,method,url,headers,params,body,body_type,assertions,timeout,retry_count,tags,priority,is_enabled,sort_order,last_run_at,last_status,created_at,updated_at)VALUES(113,22,4,1,13,'更新资料','验证更新资料','PUT','/api/v1/users/me','{}','{}',NULL,'json','[]',30,0,'["user", "P1"]',2,true,5,'2026-05-31 21:56:00','success','2026-03-21 00:40:00','2026-06-01 16:31:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO api_test_cases(id,collection_id,project_id,user_id,environment_id,name,description,method,url,headers,params,body,body_type,assertions,timeout,retry_count,tags,priority,is_enabled,sort_order,last_run_at,last_status,created_at,updated_at)VALUES(114,22,4,1,15,'发起支付','验证发起支付','POST','/api/v1/payments','{}','{}',NULL,'json','[]',30,0,'["payment", "P0"]',1,true,6,'2026-05-23 10:21:00','success','2026-02-02 22:23:00','2026-05-30 03:14:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO api_test_cases(id,collection_id,project_id,user_id,environment_id,name,description,method,url,headers,params,body,body_type,assertions,timeout,retry_count,tags,priority,is_enabled,sort_order,last_run_at,last_status,created_at,updated_at)VALUES(115,22,4,7,14,'健康检查','验证健康检查','GET','/api/v1/health','{}','{}',NULL,'json','[]',30,0,'["health", "P0"]',2,true,7,'2026-05-20 09:46:00','success','2026-03-04 13:07:00','2026-06-02 00:00:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO api_test_cases(id,collection_id,project_id,user_id,environment_id,name,description,method,url,headers,params,body,body_type,assertions,timeout,retry_count,tags,priority,is_enabled,sort_order,last_run_at,last_status,created_at,updated_at)VALUES(116,23,4,2,15,'搜索商品','验证搜索商品','GET','/api/v1/search','{}','{}',NULL,'json','[]',30,0,'["search", "P1"]',3,true,0,'2026-05-25 17:34:00','success','2026-02-25 19:13:00','2026-06-01 15:54:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO api_test_cases(id,collection_id,project_id,user_id,environment_id,name,description,method,url,headers,params,body,body_type,assertions,timeout,retry_count,tags,priority,is_enabled,sort_order,last_run_at,last_status,created_at,updated_at)VALUES(117,23,4,7,14,'申请退款','验证申请退款','POST','/api/v1/refunds','{}','{}',NULL,'json','[]',30,0,'["payment", "P1"]',2,true,1,'2026-05-21 07:23:00','success','2026-05-16 20:18:00','2026-06-01 02:42:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO api_test_cases(id,collection_id,project_id,user_id,environment_id,name,description,method,url,headers,params,body,body_type,assertions,timeout,retry_count,tags,priority,is_enabled,sort_order,last_run_at,last_status,created_at,updated_at)VALUES(118,23,4,5,15,'商品列表','验证商品列表','GET','/api/v1/products','{}','{}',NULL,'json','[]',30,0,'["product", "P0"]',2,true,2,NULL,'pending','2025-12-03 10:40:00','2026-05-30 19:43:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO api_test_cases(id,collection_id,project_id,user_id,environment_id,name,description,method,url,headers,params,body,body_type,assertions,timeout,retry_count,tags,priority,is_enabled,sort_order,last_run_at,last_status,created_at,updated_at)VALUES(119,23,4,2,13,'取消订单','验证取消订单','POST','/api/v1/orders/1001/cancel','{}','{}',NULL,'json','[]',30,0,'["order", "P1"]',1,true,3,NULL,'pending','2025-11-13 15:54:00','2026-06-01 06:50:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO api_test_cases(id,collection_id,project_id,user_id,environment_id,name,description,method,url,headers,params,body,body_type,assertions,timeout,retry_count,tags,priority,is_enabled,sort_order,last_run_at,last_status,created_at,updated_at)VALUES(120,23,4,6,16,'发起支付','验证发起支付','POST','/api/v1/payments','{}','{}',NULL,'json','[]',30,0,'["payment", "P0"]',1,true,4,'2026-05-29 16:38:00','success','2026-02-06 00:31:00','2026-05-31 06:55:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO api_test_cases(id,collection_id,project_id,user_id,environment_id,name,description,method,url,headers,params,body,body_type,assertions,timeout,retry_count,tags,priority,is_enabled,sort_order,last_run_at,last_status,created_at,updated_at)VALUES(121,23,4,2,15,'提交反馈','验证提交反馈','POST','/api/v1/feedback','{}','{}',NULL,'json','[]',30,0,'["feedback", "P2"]',2,true,5,'2026-06-01 03:07:00','failed','2026-04-25 07:15:00','2026-05-31 22:35:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO api_test_cases(id,collection_id,project_id,user_id,environment_id,name,description,method,url,headers,params,body,body_type,assertions,timeout,retry_count,tags,priority,is_enabled,sort_order,last_run_at,last_status,created_at,updated_at)VALUES(122,23,4,7,13,'获取配置','验证获取配置','GET','/api/v1/config','{}','{}',NULL,'json','[]',30,0,'["config", "P2"]',2,true,6,'2026-05-25 04:59:00','failed','2026-02-05 16:13:00','2026-06-01 06:31:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO api_test_cases(id,collection_id,project_id,user_id,environment_id,name,description,method,url,headers,params,body,body_type,assertions,timeout,retry_count,tags,priority,is_enabled,sort_order,last_run_at,last_status,created_at,updated_at)VALUES(123,23,4,1,14,'用户登录','验证用户登录','POST','/api/v1/auth/login','{}','{}',NULL,'json','[]',30,0,'["auth", "P0"]',1,true,7,'2026-06-01 02:52:00','success','2026-02-18 22:17:00','2026-06-01 15:23:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO api_test_cases(id,collection_id,project_id,user_id,environment_id,name,description,method,url,headers,params,body,body_type,assertions,timeout,retry_count,tags,priority,is_enabled,sort_order,last_run_at,last_status,created_at,updated_at)VALUES(124,24,4,2,13,'更新资料','验证更新资料','PUT','/api/v1/users/me','{}','{}',NULL,'json','[]',30,0,'["user", "P1"]',2,true,0,'2026-05-23 06:58:00','running','2026-05-20 04:01:00','2026-05-29 10:35:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO api_test_cases(id,collection_id,project_id,user_id,environment_id,name,description,method,url,headers,params,body,body_type,assertions,timeout,retry_count,tags,priority,is_enabled,sort_order,last_run_at,last_status,created_at,updated_at)VALUES(125,24,4,6,13,'用户登录','验证用户登录','POST','/api/v1/auth/login','{}','{}',NULL,'json','[]',30,0,'["auth", "P0"]',1,true,1,'2026-05-20 04:38:00','success','2026-04-15 01:43:00','2026-05-30 05:58:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO api_test_cases(id,collection_id,project_id,user_id,environment_id,name,description,method,url,headers,params,body,body_type,assertions,timeout,retry_count,tags,priority,is_enabled,sort_order,last_run_at,last_status,created_at,updated_at)VALUES(126,24,4,7,14,'健康检查','验证健康检查','GET','/api/v1/health','{}','{}',NULL,'json','[]',30,0,'["health", "P0"]',2,true,2,'2026-05-17 20:04:00','success','2026-01-30 08:55:00','2026-05-30 21:52:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO api_test_cases(id,collection_id,project_id,user_id,environment_id,name,description,method,url,headers,params,body,body_type,assertions,timeout,retry_count,tags,priority,is_enabled,sort_order,last_run_at,last_status,created_at,updated_at)VALUES(127,24,4,6,14,'取消订单','验证取消订单','POST','/api/v1/orders/1001/cancel','{}','{}',NULL,'json','[]',30,0,'["order", "P1"]',2,true,3,'2026-05-25 13:09:00','success','2025-11-10 09:36:00','2026-05-30 18:26:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO api_test_cases(id,collection_id,project_id,user_id,environment_id,name,description,method,url,headers,params,body,body_type,assertions,timeout,retry_count,tags,priority,is_enabled,sort_order,last_run_at,last_status,created_at,updated_at)VALUES(128,24,4,6,15,'上传图片','验证上传图片','POST','/api/v1/upload','{}','{}',NULL,'json','[]',30,0,'["upload", "P1"]',1,true,4,'2026-05-22 21:43:00','running','2026-05-25 23:22:00','2026-06-01 09:03:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO api_test_cases(id,collection_id,project_id,user_id,environment_id,name,description,method,url,headers,params,body,body_type,assertions,timeout,retry_count,tags,priority,is_enabled,sort_order,last_run_at,last_status,created_at,updated_at)VALUES(129,25,4,2,13,'用户信息','验证用户信息','GET','/api/v1/users/me','{}','{}',NULL,'json','[]',30,0,'["user", "P0"]',3,true,0,'2026-05-26 01:26:00','success','2026-05-18 02:24:00','2026-05-29 22:01:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO api_test_cases(id,collection_id,project_id,user_id,environment_id,name,description,method,url,headers,params,body,body_type,assertions,timeout,retry_count,tags,priority,is_enabled,sort_order,last_run_at,last_status,created_at,updated_at)VALUES(130,25,4,2,14,'获取配置','验证获取配置','GET','/api/v1/config','{}','{}',NULL,'json','[]',30,0,'["config", "P2"]',2,true,1,'2026-05-22 10:16:00','success','2026-01-01 09:15:00','2026-05-30 15:24:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO api_test_cases(id,collection_id,project_id,user_id,environment_id,name,description,method,url,headers,params,body,body_type,assertions,timeout,retry_count,tags,priority,is_enabled,sort_order,last_run_at,last_status,created_at,updated_at)VALUES(131,25,4,2,14,'提交反馈','验证提交反馈','POST','/api/v1/feedback','{}','{}',NULL,'json','[]',30,0,'["feedback", "P2"]',1,true,2,'2026-05-17 16:41:00','failed','2026-01-27 08:55:00','2026-06-02 02:22:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO api_test_cases(id,collection_id,project_id,user_id,environment_id,name,description,method,url,headers,params,body,body_type,assertions,timeout,retry_count,tags,priority,is_enabled,sort_order,last_run_at,last_status,created_at,updated_at)VALUES(132,25,4,2,13,'标记已读','验证标记已读','PUT','/api/v1/messages/1001','{}','{}',NULL,'json','[]',30,0,'["message", "P2"]',2,true,3,'2026-06-01 23:02:00','success','2026-04-11 05:39:00','2026-05-31 23:57:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO api_test_cases(id,collection_id,project_id,user_id,environment_id,name,description,method,url,headers,params,body,body_type,assertions,timeout,retry_count,tags,priority,is_enabled,sort_order,last_run_at,last_status,created_at,updated_at)VALUES(133,25,4,1,14,'发起支付','验证发起支付','POST','/api/v1/payments','{}','{}',NULL,'json','[]',30,0,'["payment", "P0"]',2,true,4,'2026-05-29 06:06:00','success','2026-02-28 07:37:00','2026-05-29 15:54:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO api_test_cases(id,collection_id,project_id,user_id,environment_id,name,description,method,url,headers,params,body,body_type,assertions,timeout,retry_count,tags,priority,is_enabled,sort_order,last_run_at,last_status,created_at,updated_at)VALUES(134,26,4,6,15,'申请退款','验证申请退款','POST','/api/v1/refunds','{}','{}',NULL,'json','[]',30,0,'["payment", "P1"]',2,true,0,'2026-05-22 02:18:00','success','2025-11-05 04:36:00','2026-05-30 10:16:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO api_test_cases(id,collection_id,project_id,user_id,environment_id,name,description,method,url,headers,params,body,body_type,assertions,timeout,retry_count,tags,priority,is_enabled,sort_order,last_run_at,last_status,created_at,updated_at)VALUES(135,26,4,5,14,'消息列表','验证消息列表','GET','/api/v1/messages','{}','{}',NULL,'json','[]',30,0,'["message", "P1"]',2,true,1,'2026-06-01 11:24:00','success','2025-11-15 15:58:00','2026-05-31 14:40:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO api_test_cases(id,collection_id,project_id,user_id,environment_id,name,description,method,url,headers,params,body,body_type,assertions,timeout,retry_count,tags,priority,is_enabled,sort_order,last_run_at,last_status,created_at,updated_at)VALUES(136,26,4,7,14,'创建订单','验证创建订单','POST','/api/v1/orders','{}','{}',NULL,'json','[]',30,0,'["order", "P0"]',2,true,2,'2026-05-29 18:51:00','success','2025-11-23 07:45:00','2026-05-30 23:50:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO api_test_cases(id,collection_id,project_id,user_id,environment_id,name,description,method,url,headers,params,body,body_type,assertions,timeout,retry_count,tags,priority,is_enabled,sort_order,last_run_at,last_status,created_at,updated_at)VALUES(137,26,4,1,15,'订单详情','验证订单详情','GET','/api/v1/orders/1001','{}','{}',NULL,'json','[]',30,0,'["order", "P0"]',3,true,3,'2026-05-25 03:45:00','success','2026-05-14 22:44:00','2026-06-01 11:00:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO api_test_cases(id,collection_id,project_id,user_id,environment_id,name,description,method,url,headers,params,body,body_type,assertions,timeout,retry_count,tags,priority,is_enabled,sort_order,last_run_at,last_status,created_at,updated_at)VALUES(138,26,4,1,16,'推荐列表','验证推荐列表','GET','/api/v1/recommendations','{}','{}',NULL,'json','[]',30,0,'["recommendation", "P2"]',2,true,4,'2026-05-20 04:04:00','success','2026-01-25 21:38:00','2026-05-30 06:07:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO api_test_cases(id,collection_id,project_id,user_id,environment_id,name,description,method,url,headers,params,body,body_type,assertions,timeout,retry_count,tags,priority,is_enabled,sort_order,last_run_at,last_status,created_at,updated_at)VALUES(139,27,4,1,15,'领取券','验证领取券','POST','/api/v1/coupons/1001','{}','{}',NULL,'json','[]',30,0,'["marketing", "P1"]',2,true,0,'2026-05-25 06:56:00','success','2026-04-18 21:50:00','2026-06-01 16:03:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO api_test_cases(id,collection_id,project_id,user_id,environment_id,name,description,method,url,headers,params,body,body_type,assertions,timeout,retry_count,tags,priority,is_enabled,sort_order,last_run_at,last_status,created_at,updated_at)VALUES(140,27,4,1,15,'发起支付','验证发起支付','POST','/api/v1/payments','{}','{}',NULL,'json','[]',30,0,'["payment", "P0"]',2,true,1,'2026-05-17 11:59:00','success','2025-12-16 04:22:00','2026-05-30 04:57:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO api_test_cases(id,collection_id,project_id,user_id,environment_id,name,description,method,url,headers,params,body,body_type,assertions,timeout,retry_count,tags,priority,is_enabled,sort_order,last_run_at,last_status,created_at,updated_at)VALUES(141,27,4,1,15,'订单详情','验证订单详情','GET','/api/v1/orders/1001','{}','{}',NULL,'json','[]',30,0,'["order", "P0"]',2,true,2,'2026-05-26 20:16:00','success','2025-11-28 10:26:00','2026-05-30 12:42:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO api_test_cases(id,collection_id,project_id,user_id,environment_id,name,description,method,url,headers,params,body,body_type,assertions,timeout,retry_count,tags,priority,is_enabled,sort_order,last_run_at,last_status,created_at,updated_at)VALUES(142,27,4,5,14,'上传图片','验证上传图片','POST','/api/v1/upload','{}','{}',NULL,'json','[]',30,0,'["upload", "P1"]',2,true,3,'2026-05-20 15:25:00','success','2026-04-23 08:37:00','2026-06-01 20:55:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO api_test_cases(id,collection_id,project_id,user_id,environment_id,name,description,method,url,headers,params,body,body_type,assertions,timeout,retry_count,tags,priority,is_enabled,sort_order,last_run_at,last_status,created_at,updated_at)VALUES(143,27,4,5,16,'更新资料','验证更新资料','PUT','/api/v1/users/me','{}','{}',NULL,'json','[]',30,0,'["user", "P1"]',3,true,4,'2026-06-02 03:50:00','success','2026-03-19 07:30:00','2026-06-02 00:10:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO api_test_cases(id,collection_id,project_id,user_id,environment_id,name,description,method,url,headers,params,body,body_type,assertions,timeout,retry_count,tags,priority,is_enabled,sort_order,last_run_at,last_status,created_at,updated_at)VALUES(144,27,4,6,16,'搜索商品','验证搜索商品','GET','/api/v1/search','{}','{}',NULL,'json','[]',30,0,'["search", "P1"]',2,true,5,'2026-05-25 07:19:00','success','2026-02-22 04:37:00','2026-05-29 22:49:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO api_test_cases(id,collection_id,project_id,user_id,environment_id,name,description,method,url,headers,params,body,body_type,assertions,timeout,retry_count,tags,priority,is_enabled,sort_order,last_run_at,last_status,created_at,updated_at)VALUES(145,28,4,5,13,'用户信息','验证用户信息','GET','/api/v1/users/me','{}','{}',NULL,'json','[]',30,0,'["user", "P0"]',2,true,0,'2026-05-30 07:18:00','success','2025-11-06 16:34:00','2026-05-31 16:57:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO api_test_cases(id,collection_id,project_id,user_id,environment_id,name,description,method,url,headers,params,body,body_type,assertions,timeout,retry_count,tags,priority,is_enabled,sort_order,last_run_at,last_status,created_at,updated_at)VALUES(146,28,4,6,16,'支付状态','验证支付状态','GET','/api/v1/payments/1001','{}','{}',NULL,'json','[]',30,0,'["payment", "P1"]',3,true,1,NULL,'pending','2026-01-30 15:04:00','2026-05-31 18:41:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO api_test_cases(id,collection_id,project_id,user_id,environment_id,name,description,method,url,headers,params,body,body_type,assertions,timeout,retry_count,tags,priority,is_enabled,sort_order,last_run_at,last_status,created_at,updated_at)VALUES(147,28,4,1,16,'上传图片','验证上传图片','POST','/api/v1/upload','{}','{}',NULL,'json','[]',30,0,'["upload", "P1"]',2,true,2,'2026-05-31 17:24:00','running','2025-11-08 15:17:00','2026-06-01 06:12:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO api_test_cases(id,collection_id,project_id,user_id,environment_id,name,description,method,url,headers,params,body,body_type,assertions,timeout,retry_count,tags,priority,is_enabled,sort_order,last_run_at,last_status,created_at,updated_at)VALUES(148,28,4,6,14,'优惠券','验证优惠券','GET','/api/v1/coupons','{}','{}',NULL,'json','[]',30,0,'["marketing", "P1"]',1,true,3,NULL,'pending','2026-04-08 03:52:00','2026-06-01 20:55:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO api_test_cases(id,collection_id,project_id,user_id,environment_id,name,description,method,url,headers,params,body,body_type,assertions,timeout,retry_count,tags,priority,is_enabled,sort_order,last_run_at,last_status,created_at,updated_at)VALUES(149,28,4,6,14,'领取券','验证领取券','POST','/api/v1/coupons/1001','{}','{}',NULL,'json','[]',30,0,'["marketing", "P1"]',2,true,4,'2026-05-28 14:44:00','cancelled','2025-11-27 07:55:00','2026-05-29 16:35:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO api_test_cases(id,collection_id,project_id,user_id,environment_id,name,description,method,url,headers,params,body,body_type,assertions,timeout,retry_count,tags,priority,is_enabled,sort_order,last_run_at,last_status,created_at,updated_at)VALUES(150,28,4,7,15,'商品列表','验证商品列表','GET','/api/v1/products','{}','{}',NULL,'json','[]',30,0,'["product", "P0"]',3,true,5,'2026-05-19 09:10:00','running','2025-12-23 15:27:00','2026-05-30 06:34:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO api_test_cases(id,collection_id,project_id,user_id,environment_id,name,description,method,url,headers,params,body,body_type,assertions,timeout,retry_count,tags,priority,is_enabled,sort_order,last_run_at,last_status,created_at,updated_at)VALUES(151,29,4,7,13,'创建订单','验证创建订单','POST','/api/v1/orders','{}','{}',NULL,'json','[]',30,0,'["order", "P0"]',2,true,0,'2026-05-21 20:44:00','failed','2025-12-15 18:24:00','2026-05-30 08:49:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO api_test_cases(id,collection_id,project_id,user_id,environment_id,name,description,method,url,headers,params,body,body_type,assertions,timeout,retry_count,tags,priority,is_enabled,sort_order,last_run_at,last_status,created_at,updated_at)VALUES(152,29,4,5,16,'领取券','验证领取券','POST','/api/v1/coupons/1001','{}','{}',NULL,'json','[]',30,0,'["marketing", "P1"]',2,true,1,'2026-05-21 08:35:00','success','2025-12-07 02:57:00','2026-05-30 01:03:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO api_test_cases(id,collection_id,project_id,user_id,environment_id,name,description,method,url,headers,params,body,body_type,assertions,timeout,retry_count,tags,priority,is_enabled,sort_order,last_run_at,last_status,created_at,updated_at)VALUES(153,29,4,5,13,'商品列表','验证商品列表','GET','/api/v1/products','{}','{}',NULL,'json','[]',30,0,'["product", "P0"]',2,true,2,'2026-05-24 00:43:00','success','2025-12-04 12:54:00','2026-06-01 05:41:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO api_test_cases(id,collection_id,project_id,user_id,environment_id,name,description,method,url,headers,params,body,body_type,assertions,timeout,retry_count,tags,priority,is_enabled,sort_order,last_run_at,last_status,created_at,updated_at)VALUES(154,29,4,6,15,'优惠券','验证优惠券','GET','/api/v1/coupons','{}','{}',NULL,'json','[]',30,0,'["marketing", "P1"]',1,true,3,'2026-05-19 14:19:00','success','2026-04-13 19:47:00','2026-05-29 10:29:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO api_test_cases(id,collection_id,project_id,user_id,environment_id,name,description,method,url,headers,params,body,body_type,assertions,timeout,retry_count,tags,priority,is_enabled,sort_order,last_run_at,last_status,created_at,updated_at)VALUES(155,30,5,7,20,'标记已读','验证标记已读','PUT','/api/v1/messages/1001','{}','{}',NULL,'json','[]',30,0,'["message", "P2"]',1,true,0,'2026-06-02 04:48:00','success','2026-05-18 02:58:00','2026-05-30 08:02:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO api_test_cases(id,collection_id,project_id,user_id,environment_id,name,description,method,url,headers,params,body,body_type,assertions,timeout,retry_count,tags,priority,is_enabled,sort_order,last_run_at,last_status,created_at,updated_at)VALUES(156,30,5,5,18,'用户信息','验证用户信息','GET','/api/v1/users/me','{}','{}',NULL,'json','[]',30,0,'["user", "P0"]',3,true,1,'2026-05-18 17:35:00','success','2026-04-30 12:59:00','2026-05-31 22:29:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO api_test_cases(id,collection_id,project_id,user_id,environment_id,name,description,method,url,headers,params,body,body_type,assertions,timeout,retry_count,tags,priority,is_enabled,sort_order,last_run_at,last_status,created_at,updated_at)VALUES(157,30,5,7,20,'提交反馈','验证提交反馈','POST','/api/v1/feedback','{}','{}',NULL,'json','[]',30,0,'["feedback", "P2"]',2,true,2,'2026-05-17 15:25:00','success','2026-03-05 04:07:00','2026-05-30 10:07:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO api_test_cases(id,collection_id,project_id,user_id,environment_id,name,description,method,url,headers,params,body,body_type,assertions,timeout,retry_count,tags,priority,is_enabled,sort_order,last_run_at,last_status,created_at,updated_at)VALUES(158,30,5,1,19,'订单详情','验证订单详情','GET','/api/v1/orders/1001','{}','{}',NULL,'json','[]',30,0,'["order", "P0"]',2,true,3,'2026-06-01 04:06:00','success','2025-11-14 03:06:00','2026-05-31 13:46:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO api_test_cases(id,collection_id,project_id,user_id,environment_id,name,description,method,url,headers,params,body,body_type,assertions,timeout,retry_count,tags,priority,is_enabled,sort_order,last_run_at,last_status,created_at,updated_at)VALUES(159,30,5,2,19,'更新资料','验证更新资料','PUT','/api/v1/users/me','{}','{}',NULL,'json','[]',30,0,'["user", "P1"]',2,true,4,'2026-06-01 13:00:00','failed','2026-04-28 13:49:00','2026-06-02 02:44:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO api_test_cases(id,collection_id,project_id,user_id,environment_id,name,description,method,url,headers,params,body,body_type,assertions,timeout,retry_count,tags,priority,is_enabled,sort_order,last_run_at,last_status,created_at,updated_at)VALUES(160,30,5,7,19,'创建订单','验证创建订单','POST','/api/v1/orders','{}','{}',NULL,'json','[]',30,0,'["order", "P0"]',2,true,5,'2026-05-24 20:03:00','failed','2026-03-03 19:44:00','2026-05-31 19:41:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO api_test_cases(id,collection_id,project_id,user_id,environment_id,name,description,method,url,headers,params,body,body_type,assertions,timeout,retry_count,tags,priority,is_enabled,sort_order,last_run_at,last_status,created_at,updated_at)VALUES(161,30,5,7,20,'健康检查','验证健康检查','GET','/api/v1/health','{}','{}',NULL,'json','[]',30,0,'["health", "P0"]',2,true,6,'2026-06-01 17:18:00','success','2026-01-08 13:22:00','2026-05-31 00:17:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO api_test_cases(id,collection_id,project_id,user_id,environment_id,name,description,method,url,headers,params,body,body_type,assertions,timeout,retry_count,tags,priority,is_enabled,sort_order,last_run_at,last_status,created_at,updated_at)VALUES(162,31,5,5,19,'获取配置','验证获取配置','GET','/api/v1/config','{}','{}',NULL,'json','[]',30,0,'["config", "P2"]',3,true,0,'2026-05-24 13:15:00','running','2026-03-17 03:51:00','2026-06-01 08:09:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO api_test_cases(id,collection_id,project_id,user_id,environment_id,name,description,method,url,headers,params,body,body_type,assertions,timeout,retry_count,tags,priority,is_enabled,sort_order,last_run_at,last_status,created_at,updated_at)VALUES(163,31,5,7,20,'更新资料','验证更新资料','PUT','/api/v1/users/me','{}','{}',NULL,'json','[]',30,0,'["user", "P1"]',3,true,1,'2026-05-28 10:59:00','failed','2026-01-25 00:44:00','2026-05-29 21:36:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO api_test_cases(id,collection_id,project_id,user_id,environment_id,name,description,method,url,headers,params,body,body_type,assertions,timeout,retry_count,tags,priority,is_enabled,sort_order,last_run_at,last_status,created_at,updated_at)VALUES(164,31,5,1,18,'消息列表','验证消息列表','GET','/api/v1/messages','{}','{}',NULL,'json','[]',30,0,'["message", "P1"]',3,true,2,'2026-05-25 12:26:00','success','2025-11-12 18:02:00','2026-05-30 17:41:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO api_test_cases(id,collection_id,project_id,user_id,environment_id,name,description,method,url,headers,params,body,body_type,assertions,timeout,retry_count,tags,priority,is_enabled,sort_order,last_run_at,last_status,created_at,updated_at)VALUES(165,32,5,6,18,'优惠券','验证优惠券','GET','/api/v1/coupons','{}','{}',NULL,'json','[]',30,0,'["marketing", "P1"]',2,true,0,'2026-05-27 12:03:00','failed','2025-12-16 07:46:00','2026-05-31 02:13:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO api_test_cases(id,collection_id,project_id,user_id,environment_id,name,description,method,url,headers,params,body,body_type,assertions,timeout,retry_count,tags,priority,is_enabled,sort_order,last_run_at,last_status,created_at,updated_at)VALUES(166,32,5,5,20,'订单详情','验证订单详情','GET','/api/v1/orders/1001','{}','{}',NULL,'json','[]',30,0,'["order", "P0"]',2,true,1,'2026-05-22 22:44:00','failed','2026-03-17 19:06:00','2026-06-01 18:57:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO api_test_cases(id,collection_id,project_id,user_id,environment_id,name,description,method,url,headers,params,body,body_type,assertions,timeout,retry_count,tags,priority,is_enabled,sort_order,last_run_at,last_status,created_at,updated_at)VALUES(167,32,5,7,17,'申请退款','验证申请退款','POST','/api/v1/refunds','{}','{}',NULL,'json','[]',30,0,'["payment", "P1"]',3,true,2,'2026-05-26 17:53:00','success','2026-02-23 17:41:00','2026-05-30 08:05:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO api_test_cases(id,collection_id,project_id,user_id,environment_id,name,description,method,url,headers,params,body,body_type,assertions,timeout,retry_count,tags,priority,is_enabled,sort_order,last_run_at,last_status,created_at,updated_at)VALUES(168,32,5,2,18,'商品列表','验证商品列表','GET','/api/v1/products','{}','{}',NULL,'json','[]',30,0,'["product", "P0"]',2,true,3,'2026-05-22 20:24:00','cancelled','2026-04-25 23:05:00','2026-06-01 07:29:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO api_test_cases(id,collection_id,project_id,user_id,environment_id,name,description,method,url,headers,params,body,body_type,assertions,timeout,retry_count,tags,priority,is_enabled,sort_order,last_run_at,last_status,created_at,updated_at)VALUES(169,33,5,5,18,'订单详情','验证订单详情','GET','/api/v1/orders/1001','{}','{}',NULL,'json','[]',30,0,'["order", "P0"]',1,true,0,'2026-05-27 15:12:00','failed','2026-01-27 07:52:00','2026-05-29 13:33:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO api_test_cases(id,collection_id,project_id,user_id,environment_id,name,description,method,url,headers,params,body,body_type,assertions,timeout,retry_count,tags,priority,is_enabled,sort_order,last_run_at,last_status,created_at,updated_at)VALUES(170,33,5,6,20,'消息列表','验证消息列表','GET','/api/v1/messages','{}','{}',NULL,'json','[]',30,0,'["message", "P1"]',2,true,1,NULL,'pending','2026-05-31 08:26:00','2026-05-31 10:37:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO api_test_cases(id,collection_id,project_id,user_id,environment_id,name,description,method,url,headers,params,body,body_type,assertions,timeout,retry_count,tags,priority,is_enabled,sort_order,last_run_at,last_status,created_at,updated_at)VALUES(171,33,5,1,19,'用户信息','验证用户信息','GET','/api/v1/users/me','{}','{}',NULL,'json','[]',30,0,'["user", "P0"]',1,true,2,'2026-05-27 09:17:00','failed','2025-12-22 10:45:00','2026-05-31 11:04:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO api_test_cases(id,collection_id,project_id,user_id,environment_id,name,description,method,url,headers,params,body,body_type,assertions,timeout,retry_count,tags,priority,is_enabled,sort_order,last_run_at,last_status,created_at,updated_at)VALUES(172,33,5,5,19,'用户登录','验证用户登录','POST','/api/v1/auth/login','{}','{}',NULL,'json','[]',30,0,'["auth", "P0"]',2,true,3,'2026-05-20 17:23:00','success','2026-04-20 07:08:00','2026-06-02 00:42:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO api_test_cases(id,collection_id,project_id,user_id,environment_id,name,description,method,url,headers,params,body,body_type,assertions,timeout,retry_count,tags,priority,is_enabled,sort_order,last_run_at,last_status,created_at,updated_at)VALUES(173,33,5,6,19,'上传图片','验证上传图片','POST','/api/v1/upload','{}','{}',NULL,'json','[]',30,0,'["upload", "P1"]',2,true,4,'2026-05-28 23:03:00','success','2026-03-02 03:50:00','2026-05-30 09:46:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO api_test_cases(id,collection_id,project_id,user_id,environment_id,name,description,method,url,headers,params,body,body_type,assertions,timeout,retry_count,tags,priority,is_enabled,sort_order,last_run_at,last_status,created_at,updated_at)VALUES(174,34,5,2,17,'创建订单','验证创建订单','POST','/api/v1/orders','{}','{}',NULL,'json','[]',30,0,'["order", "P0"]',3,true,0,'2026-05-31 21:04:00','success','2026-03-27 16:21:00','2026-06-01 14:57:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO api_test_cases(id,collection_id,project_id,user_id,environment_id,name,description,method,url,headers,params,body,body_type,assertions,timeout,retry_count,tags,priority,is_enabled,sort_order,last_run_at,last_status,created_at,updated_at)VALUES(175,34,5,1,17,'取消订单','验证取消订单','POST','/api/v1/orders/1001/cancel','{}','{}',NULL,'json','[]',30,0,'["order", "P1"]',2,true,1,'2026-05-29 20:32:00','success','2026-04-30 16:44:00','2026-05-29 11:51:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO api_test_cases(id,collection_id,project_id,user_id,environment_id,name,description,method,url,headers,params,body,body_type,assertions,timeout,retry_count,tags,priority,is_enabled,sort_order,last_run_at,last_status,created_at,updated_at)VALUES(176,34,5,2,17,'用户登录','验证用户登录','POST','/api/v1/auth/login','{}','{}',NULL,'json','[]',30,0,'["auth", "P0"]',2,true,2,'2026-05-29 12:27:00','success','2025-12-23 14:16:00','2026-05-31 20:07:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO api_test_cases(id,collection_id,project_id,user_id,environment_id,name,description,method,url,headers,params,body,body_type,assertions,timeout,retry_count,tags,priority,is_enabled,sort_order,last_run_at,last_status,created_at,updated_at)VALUES(177,34,5,1,17,'提交反馈','验证提交反馈','POST','/api/v1/feedback','{}','{}',NULL,'json','[]',30,0,'["feedback", "P2"]',2,true,3,'2026-05-29 18:48:00','success','2026-04-11 01:07:00','2026-05-31 22:15:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO api_test_cases(id,collection_id,project_id,user_id,environment_id,name,description,method,url,headers,params,body,body_type,assertions,timeout,retry_count,tags,priority,is_enabled,sort_order,last_run_at,last_status,created_at,updated_at)VALUES(178,35,5,6,19,'申请退款','验证申请退款','POST','/api/v1/refunds','{}','{}',NULL,'json','[]',30,0,'["payment", "P1"]',1,true,0,'2026-06-01 12:55:00','success','2026-01-05 12:29:00','2026-06-01 07:11:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO api_test_cases(id,collection_id,project_id,user_id,environment_id,name,description,method,url,headers,params,body,body_type,assertions,timeout,retry_count,tags,priority,is_enabled,sort_order,last_run_at,last_status,created_at,updated_at)VALUES(179,35,5,7,17,'订单详情','验证订单详情','GET','/api/v1/orders/1001','{}','{}',NULL,'json','[]',30,0,'["order", "P0"]',1,true,1,'2026-05-30 01:19:00','failed','2026-02-05 00:44:00','2026-05-30 08:54:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO api_test_cases(id,collection_id,project_id,user_id,environment_id,name,description,method,url,headers,params,body,body_type,assertions,timeout,retry_count,tags,priority,is_enabled,sort_order,last_run_at,last_status,created_at,updated_at)VALUES(180,35,5,2,17,'用户信息','验证用户信息','GET','/api/v1/users/me','{}','{}',NULL,'json','[]',30,0,'["user", "P0"]',2,true,2,'2026-05-21 12:40:00','running','2025-11-24 06:54:00','2026-06-02 09:06:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO api_test_cases(id,collection_id,project_id,user_id,environment_id,name,description,method,url,headers,params,body,body_type,assertions,timeout,retry_count,tags,priority,is_enabled,sort_order,last_run_at,last_status,created_at,updated_at)VALUES(181,35,5,2,18,'获取配置','验证获取配置','GET','/api/v1/config','{}','{}',NULL,'json','[]',30,0,'["config", "P2"]',3,true,3,'2026-05-18 14:43:00','success','2026-05-08 22:08:00','2026-05-31 04:53:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO api_test_cases(id,collection_id,project_id,user_id,environment_id,name,description,method,url,headers,params,body,body_type,assertions,timeout,retry_count,tags,priority,is_enabled,sort_order,last_run_at,last_status,created_at,updated_at)VALUES(182,35,5,6,20,'取消订单','验证取消订单','POST','/api/v1/orders/1001/cancel','{}','{}',NULL,'json','[]',30,0,'["order", "P1"]',2,true,4,NULL,'pending','2026-02-22 11:06:00','2026-05-29 20:19:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO api_test_cases(id,collection_id,project_id,user_id,environment_id,name,description,method,url,headers,params,body,body_type,assertions,timeout,retry_count,tags,priority,is_enabled,sort_order,last_run_at,last_status,created_at,updated_at)VALUES(183,35,5,2,17,'标记已读','验证标记已读','PUT','/api/v1/messages/1001','{}','{}',NULL,'json','[]',30,0,'["message", "P2"]',2,true,5,'2026-06-01 04:54:00','success','2025-12-31 18:09:00','2026-05-30 04:21:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO api_test_cases(id,collection_id,project_id,user_id,environment_id,name,description,method,url,headers,params,body,body_type,assertions,timeout,retry_count,tags,priority,is_enabled,sort_order,last_run_at,last_status,created_at,updated_at)VALUES(184,36,6,6,24,'标记已读','验证标记已读','PUT','/api/v1/messages/1001','{}','{}',NULL,'json','[]',30,0,'["message", "P2"]',1,true,0,'2026-05-24 13:40:00','success','2025-12-02 12:27:00','2026-05-31 12:05:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO api_test_cases(id,collection_id,project_id,user_id,environment_id,name,description,method,url,headers,params,body,body_type,assertions,timeout,retry_count,tags,priority,is_enabled,sort_order,last_run_at,last_status,created_at,updated_at)VALUES(185,36,6,5,21,'用户登录','验证用户登录','POST','/api/v1/auth/login','{}','{}',NULL,'json','[]',30,0,'["auth", "P0"]',3,true,1,'2026-05-25 18:38:00','success','2025-12-09 13:36:00','2026-05-31 16:03:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO api_test_cases(id,collection_id,project_id,user_id,environment_id,name,description,method,url,headers,params,body,body_type,assertions,timeout,retry_count,tags,priority,is_enabled,sort_order,last_run_at,last_status,created_at,updated_at)VALUES(186,36,6,7,21,'创建订单','验证创建订单','POST','/api/v1/orders','{}','{}',NULL,'json','[]',30,0,'["order", "P0"]',2,true,2,'2026-05-27 17:06:00','success','2026-01-26 04:56:00','2026-05-29 23:45:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO api_test_cases(id,collection_id,project_id,user_id,environment_id,name,description,method,url,headers,params,body,body_type,assertions,timeout,retry_count,tags,priority,is_enabled,sort_order,last_run_at,last_status,created_at,updated_at)VALUES(187,36,6,5,23,'获取配置','验证获取配置','GET','/api/v1/config','{}','{}',NULL,'json','[]',30,0,'["config", "P2"]',2,true,3,'2026-05-25 16:19:00','success','2026-02-18 02:55:00','2026-05-29 19:09:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO api_test_cases(id,collection_id,project_id,user_id,environment_id,name,description,method,url,headers,params,body,body_type,assertions,timeout,retry_count,tags,priority,is_enabled,sort_order,last_run_at,last_status,created_at,updated_at)VALUES(188,36,6,7,24,'提交反馈','验证提交反馈','POST','/api/v1/feedback','{}','{}',NULL,'json','[]',30,0,'["feedback", "P2"]',1,true,4,'2026-05-17 19:40:00','success','2026-01-24 10:19:00','2026-06-02 06:35:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO api_test_cases(id,collection_id,project_id,user_id,environment_id,name,description,method,url,headers,params,body,body_type,assertions,timeout,retry_count,tags,priority,is_enabled,sort_order,last_run_at,last_status,created_at,updated_at)VALUES(189,36,6,6,21,'用户信息','验证用户信息','GET','/api/v1/users/me','{}','{}',NULL,'json','[]',30,0,'["user", "P0"]',2,true,5,'2026-06-02 07:10:00','success','2025-12-24 13:41:00','2026-05-31 13:18:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO api_test_cases(id,collection_id,project_id,user_id,environment_id,name,description,method,url,headers,params,body,body_type,assertions,timeout,retry_count,tags,priority,is_enabled,sort_order,last_run_at,last_status,created_at,updated_at)VALUES(190,37,6,7,24,'消息列表','验证消息列表','GET','/api/v1/messages','{}','{}',NULL,'json','[]',30,0,'["message", "P1"]',1,true,0,'2026-05-21 11:32:00','failed','2026-05-07 12:46:00','2026-06-01 23:38:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO api_test_cases(id,collection_id,project_id,user_id,environment_id,name,description,method,url,headers,params,body,body_type,assertions,timeout,retry_count,tags,priority,is_enabled,sort_order,last_run_at,last_status,created_at,updated_at)VALUES(191,37,6,5,23,'标记已读','验证标记已读','PUT','/api/v1/messages/1001','{}','{}',NULL,'json','[]',30,0,'["message", "P2"]',1,true,1,'2026-06-01 04:29:00','failed','2025-11-29 10:14:00','2026-05-30 06:44:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO api_test_cases(id,collection_id,project_id,user_id,environment_id,name,description,method,url,headers,params,body,body_type,assertions,timeout,retry_count,tags,priority,is_enabled,sort_order,last_run_at,last_status,created_at,updated_at)VALUES(192,37,6,7,22,'用户信息','验证用户信息','GET','/api/v1/users/me','{}','{}',NULL,'json','[]',30,0,'["user", "P0"]',1,true,2,'2026-05-21 03:31:00','success','2025-11-29 23:54:00','2026-05-30 08:01:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO api_test_cases(id,collection_id,project_id,user_id,environment_id,name,description,method,url,headers,params,body,body_type,assertions,timeout,retry_count,tags,priority,is_enabled,sort_order,last_run_at,last_status,created_at,updated_at)VALUES(193,37,6,7,21,'发起支付','验证发起支付','POST','/api/v1/payments','{}','{}',NULL,'json','[]',30,0,'["payment", "P0"]',2,true,3,'2026-05-18 19:18:00','failed','2026-01-23 05:29:00','2026-06-01 17:13:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO api_test_cases(id,collection_id,project_id,user_id,environment_id,name,description,method,url,headers,params,body,body_type,assertions,timeout,retry_count,tags,priority,is_enabled,sort_order,last_run_at,last_status,created_at,updated_at)VALUES(194,37,6,1,24,'上传图片','验证上传图片','POST','/api/v1/upload','{}','{}',NULL,'json','[]',30,0,'["upload", "P1"]',1,true,4,'2026-05-17 17:11:00','failed','2025-12-05 15:49:00','2026-06-01 06:36:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO api_test_cases(id,collection_id,project_id,user_id,environment_id,name,description,method,url,headers,params,body,body_type,assertions,timeout,retry_count,tags,priority,is_enabled,sort_order,last_run_at,last_status,created_at,updated_at)VALUES(195,37,6,7,23,'订单详情','验证订单详情','GET','/api/v1/orders/1001','{}','{}',NULL,'json','[]',30,0,'["order", "P0"]',3,true,5,'2026-05-20 20:22:00','success','2025-11-18 02:43:00','2026-05-29 23:42:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO api_test_cases(id,collection_id,project_id,user_id,environment_id,name,description,method,url,headers,params,body,body_type,assertions,timeout,retry_count,tags,priority,is_enabled,sort_order,last_run_at,last_status,created_at,updated_at)VALUES(196,38,6,7,23,'创建订单','验证创建订单','POST','/api/v1/orders','{}','{}',NULL,'json','[]',30,0,'["order", "P0"]',2,true,0,'2026-05-27 03:47:00','failed','2025-12-01 00:17:00','2026-05-30 12:52:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO api_test_cases(id,collection_id,project_id,user_id,environment_id,name,description,method,url,headers,params,body,body_type,assertions,timeout,retry_count,tags,priority,is_enabled,sort_order,last_run_at,last_status,created_at,updated_at)VALUES(197,38,6,2,23,'健康检查','验证健康检查','GET','/api/v1/health','{}','{}',NULL,'json','[]',30,0,'["health", "P0"]',2,true,1,'2026-05-21 16:30:00','failed','2026-01-05 12:15:00','2026-05-29 12:13:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO api_test_cases(id,collection_id,project_id,user_id,environment_id,name,description,method,url,headers,params,body,body_type,assertions,timeout,retry_count,tags,priority,is_enabled,sort_order,last_run_at,last_status,created_at,updated_at)VALUES(198,38,6,7,23,'推荐列表','验证推荐列表','GET','/api/v1/recommendations','{}','{}',NULL,'json','[]',30,0,'["recommendation", "P2"]',1,true,2,'2026-05-20 09:27:00','running','2026-05-25 21:51:00','2026-06-01 12:57:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO api_test_cases(id,collection_id,project_id,user_id,environment_id,name,description,method,url,headers,params,body,body_type,assertions,timeout,retry_count,tags,priority,is_enabled,sort_order,last_run_at,last_status,created_at,updated_at)VALUES(199,38,6,2,23,'提交反馈','验证提交反馈','POST','/api/v1/feedback','{}','{}',NULL,'json','[]',30,0,'["feedback", "P2"]',2,true,3,'2026-05-28 00:17:00','failed','2026-04-25 08:16:00','2026-05-31 03:12:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO api_test_cases(id,collection_id,project_id,user_id,environment_id,name,description,method,url,headers,params,body,body_type,assertions,timeout,retry_count,tags,priority,is_enabled,sort_order,last_run_at,last_status,created_at,updated_at)VALUES(200,38,6,7,21,'申请退款','验证申请退款','POST','/api/v1/refunds','{}','{}',NULL,'json','[]',30,0,'["payment", "P1"]',3,true,4,'2026-05-19 06:21:00','success','2025-11-23 16:05:00','2026-05-31 10:19:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO api_test_cases(id,collection_id,project_id,user_id,environment_id,name,description,method,url,headers,params,body,body_type,assertions,timeout,retry_count,tags,priority,is_enabled,sort_order,last_run_at,last_status,created_at,updated_at)VALUES(201,38,6,7,24,'优惠券','验证优惠券','GET','/api/v1/coupons','{}','{}',NULL,'json','[]',30,0,'["marketing", "P1"]',1,true,5,'2026-05-23 11:18:00','success','2026-02-23 21:34:00','2026-05-30 16:57:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO api_test_cases(id,collection_id,project_id,user_id,environment_id,name,description,method,url,headers,params,body,body_type,assertions,timeout,retry_count,tags,priority,is_enabled,sort_order,last_run_at,last_status,created_at,updated_at)VALUES(202,39,6,2,23,'支付状态','验证支付状态','GET','/api/v1/payments/1001','{}','{}',NULL,'json','[]',30,0,'["payment", "P1"]',2,true,0,'2026-05-26 10:48:00','failed','2026-02-07 04:17:00','2026-06-02 04:49:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO api_test_cases(id,collection_id,project_id,user_id,environment_id,name,description,method,url,headers,params,body,body_type,assertions,timeout,retry_count,tags,priority,is_enabled,sort_order,last_run_at,last_status,created_at,updated_at)VALUES(203,39,6,7,21,'取消订单','验证取消订单','POST','/api/v1/orders/1001/cancel','{}','{}',NULL,'json','[]',30,0,'["order", "P1"]',2,true,1,'2026-05-20 01:25:00','success','2026-04-29 04:23:00','2026-05-31 09:39:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO api_test_cases(id,collection_id,project_id,user_id,environment_id,name,description,method,url,headers,params,body,body_type,assertions,timeout,retry_count,tags,priority,is_enabled,sort_order,last_run_at,last_status,created_at,updated_at)VALUES(204,39,6,6,22,'上传图片','验证上传图片','POST','/api/v1/upload','{}','{}',NULL,'json','[]',30,0,'["upload", "P1"]',3,true,2,'2026-05-22 14:57:00','success','2025-12-25 12:41:00','2026-05-29 15:25:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO api_test_cases(id,collection_id,project_id,user_id,environment_id,name,description,method,url,headers,params,body,body_type,assertions,timeout,retry_count,tags,priority,is_enabled,sort_order,last_run_at,last_status,created_at,updated_at)VALUES(205,40,6,7,21,'更新资料','验证更新资料','PUT','/api/v1/users/me','{}','{}',NULL,'json','[]',30,0,'["user", "P1"]',2,true,0,'2026-05-27 20:26:00','failed','2026-02-18 07:38:00','2026-06-01 03:18:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO api_test_cases(id,collection_id,project_id,user_id,environment_id,name,description,method,url,headers,params,body,body_type,assertions,timeout,retry_count,tags,priority,is_enabled,sort_order,last_run_at,last_status,created_at,updated_at)VALUES(206,40,6,5,23,'消息列表','验证消息列表','GET','/api/v1/messages','{}','{}',NULL,'json','[]',30,0,'["message", "P1"]',2,true,1,'2026-05-26 14:27:00','success','2026-01-08 14:00:00','2026-06-01 12:38:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO api_test_cases(id,collection_id,project_id,user_id,environment_id,name,description,method,url,headers,params,body,body_type,assertions,timeout,retry_count,tags,priority,is_enabled,sort_order,last_run_at,last_status,created_at,updated_at)VALUES(207,40,6,6,22,'提交反馈','验证提交反馈','POST','/api/v1/feedback','{}','{}',NULL,'json','[]',30,0,'["feedback", "P2"]',2,true,2,'2026-05-26 08:17:00','running','2026-02-24 06:36:00','2026-05-30 16:14:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO api_test_cases(id,collection_id,project_id,user_id,environment_id,name,description,method,url,headers,params,body,body_type,assertions,timeout,retry_count,tags,priority,is_enabled,sort_order,last_run_at,last_status,created_at,updated_at)VALUES(208,40,6,5,21,'发起支付','验证发起支付','POST','/api/v1/payments','{}','{}',NULL,'json','[]',30,0,'["payment", "P0"]',2,true,3,'2026-05-21 17:09:00','running','2026-02-06 18:58:00','2026-05-30 13:48:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO api_test_cases(id,collection_id,project_id,user_id,environment_id,name,description,method,url,headers,params,body,body_type,assertions,timeout,retry_count,tags,priority,is_enabled,sort_order,last_run_at,last_status,created_at,updated_at)VALUES(209,40,6,5,21,'订单详情','验证订单详情','GET','/api/v1/orders/1001','{}','{}',NULL,'json','[]',30,0,'["order", "P0"]',1,true,4,NULL,'pending','2025-11-15 16:26:00','2026-06-01 13:56:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO api_test_cases(id,collection_id,project_id,user_id,environment_id,name,description,method,url,headers,params,body,body_type,assertions,timeout,retry_count,tags,priority,is_enabled,sort_order,last_run_at,last_status,created_at,updated_at)VALUES(210,41,6,7,24,'取消订单','验证取消订单','POST','/api/v1/orders/1001/cancel','{}','{}',NULL,'json','[]',30,0,'["order", "P1"]',1,true,0,'2026-05-30 10:17:00','success','2026-05-25 19:15:00','2026-05-31 08:55:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO api_test_cases(id,collection_id,project_id,user_id,environment_id,name,description,method,url,headers,params,body,body_type,assertions,timeout,retry_count,tags,priority,is_enabled,sort_order,last_run_at,last_status,created_at,updated_at)VALUES(211,41,6,1,21,'推荐列表','验证推荐列表','GET','/api/v1/recommendations','{}','{}',NULL,'json','[]',30,0,'["recommendation", "P2"]',2,true,1,'2026-05-24 16:56:00','success','2026-04-04 01:34:00','2026-05-29 19:20:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO api_test_cases(id,collection_id,project_id,user_id,environment_id,name,description,method,url,headers,params,body,body_type,assertions,timeout,retry_count,tags,priority,is_enabled,sort_order,last_run_at,last_status,created_at,updated_at)VALUES(212,41,6,6,24,'商品列表','验证商品列表','GET','/api/v1/products','{}','{}',NULL,'json','[]',30,0,'["product", "P0"]',2,true,2,'2026-05-20 12:53:00','success','2026-05-30 13:14:00','2026-06-01 10:23:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO api_test_cases(id,collection_id,project_id,user_id,environment_id,name,description,method,url,headers,params,body,body_type,assertions,timeout,retry_count,tags,priority,is_enabled,sort_order,last_run_at,last_status,created_at,updated_at)VALUES(213,41,6,1,21,'健康检查','验证健康检查','GET','/api/v1/health','{}','{}',NULL,'json','[]',30,0,'["health", "P0"]',3,true,3,'2026-05-30 00:10:00','success','2026-03-15 14:55:00','2026-05-30 19:36:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO api_test_cases(id,collection_id,project_id,user_id,environment_id,name,description,method,url,headers,params,body,body_type,assertions,timeout,retry_count,tags,priority,is_enabled,sort_order,last_run_at,last_status,created_at,updated_at)VALUES(214,42,6,6,23,'用户登录','验证用户登录','POST','/api/v1/auth/login','{}','{}',NULL,'json','[]',30,0,'["auth", "P0"]',1,true,0,NULL,'pending','2026-03-16 12:04:00','2026-05-31 09:25:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO api_test_cases(id,collection_id,project_id,user_id,environment_id,name,description,method,url,headers,params,body,body_type,assertions,timeout,retry_count,tags,priority,is_enabled,sort_order,last_run_at,last_status,created_at,updated_at)VALUES(215,42,6,7,22,'获取配置','验证获取配置','GET','/api/v1/config','{}','{}',NULL,'json','[]',30,0,'["config", "P2"]',2,true,1,'2026-06-01 15:22:00','success','2026-01-14 16:55:00','2026-05-31 03:13:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO api_test_cases(id,collection_id,project_id,user_id,environment_id,name,description,method,url,headers,params,body,body_type,assertions,timeout,retry_count,tags,priority,is_enabled,sort_order,last_run_at,last_status,created_at,updated_at)VALUES(216,42,6,5,22,'订单详情','验证订单详情','GET','/api/v1/orders/1001','{}','{}',NULL,'json','[]',30,0,'["order", "P0"]',1,true,2,'2026-05-29 04:49:00','success','2025-12-26 01:48:00','2026-06-02 04:18:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO api_test_cases(id,collection_id,project_id,user_id,environment_id,name,description,method,url,headers,params,body,body_type,assertions,timeout,retry_count,tags,priority,is_enabled,sort_order,last_run_at,last_status,created_at,updated_at)VALUES(217,42,6,7,21,'发起支付','验证发起支付','POST','/api/v1/payments','{}','{}',NULL,'json','[]',30,0,'["payment", "P0"]',1,true,3,'2026-05-18 13:25:00','running','2026-03-18 12:56:00','2026-05-31 06:48:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO api_test_cases(id,collection_id,project_id,user_id,environment_id,name,description,method,url,headers,params,body,body_type,assertions,timeout,retry_count,tags,priority,is_enabled,sort_order,last_run_at,last_status,created_at,updated_at)VALUES(218,42,6,7,24,'创建订单','验证创建订单','POST','/api/v1/orders','{}','{}',NULL,'json','[]',30,0,'["order", "P0"]',2,true,4,NULL,'pending','2026-04-29 12:19:00','2026-06-01 06:42:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO api_test_cases(id,collection_id,project_id,user_id,environment_id,name,description,method,url,headers,params,body,body_type,assertions,timeout,retry_count,tags,priority,is_enabled,sort_order,last_run_at,last_status,created_at,updated_at)VALUES(219,42,6,7,21,'标记已读','验证标记已读','PUT','/api/v1/messages/1001','{}','{}',NULL,'json','[]',30,0,'["message", "P2"]',2,true,5,'2026-05-22 18:32:00','running','2025-12-25 12:41:00','2026-05-31 15:24:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO api_test_cases(id,collection_id,project_id,user_id,environment_id,name,description,method,url,headers,params,body,body_type,assertions,timeout,retry_count,tags,priority,is_enabled,sort_order,last_run_at,last_status,created_at,updated_at)VALUES(220,43,6,2,22,'消息列表','验证消息列表','GET','/api/v1/messages','{}','{}',NULL,'json','[]',30,0,'["message", "P1"]',2,true,0,'2026-05-20 01:07:00','failed','2026-04-27 12:14:00','2026-05-30 18:31:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO api_test_cases(id,collection_id,project_id,user_id,environment_id,name,description,method,url,headers,params,body,body_type,assertions,timeout,retry_count,tags,priority,is_enabled,sort_order,last_run_at,last_status,created_at,updated_at)VALUES(221,43,6,6,23,'推荐列表','验证推荐列表','GET','/api/v1/recommendations','{}','{}',NULL,'json','[]',30,0,'["recommendation", "P2"]',1,true,1,'2026-05-17 16:54:00','failed','2025-12-17 14:55:00','2026-05-31 05:03:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO api_test_cases(id,collection_id,project_id,user_id,environment_id,name,description,method,url,headers,params,body,body_type,assertions,timeout,retry_count,tags,priority,is_enabled,sort_order,last_run_at,last_status,created_at,updated_at)VALUES(222,43,6,7,22,'订单详情','验证订单详情','GET','/api/v1/orders/1001','{}','{}',NULL,'json','[]',30,0,'["order", "P0"]',1,true,2,'2026-05-30 10:56:00','success','2026-01-22 13:59:00','2026-05-29 15:47:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO api_test_cases(id,collection_id,project_id,user_id,environment_id,name,description,method,url,headers,params,body,body_type,assertions,timeout,retry_count,tags,priority,is_enabled,sort_order,last_run_at,last_status,created_at,updated_at)VALUES(223,43,6,1,23,'用户登录','验证用户登录','POST','/api/v1/auth/login','{}','{}',NULL,'json','[]',30,0,'["auth", "P0"]',1,true,3,'2026-05-17 13:11:00','success','2026-02-27 21:46:00','2026-05-31 05:31:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO api_test_cases(id,collection_id,project_id,user_id,environment_id,name,description,method,url,headers,params,body,body_type,assertions,timeout,retry_count,tags,priority,is_enabled,sort_order,last_run_at,last_status,created_at,updated_at)VALUES(224,43,6,7,21,'健康检查','验证健康检查','GET','/api/v1/health','{}','{}',NULL,'json','[]',30,0,'["health", "P0"]',2,true,4,'2026-06-01 12:45:00','success','2025-12-08 04:12:00','2026-05-31 19:50:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO api_test_cases(id,collection_id,project_id,user_id,environment_id,name,description,method,url,headers,params,body,body_type,assertions,timeout,retry_count,tags,priority,is_enabled,sort_order,last_run_at,last_status,created_at,updated_at)VALUES(225,44,7,5,25,'领取券','验证领取券','POST','/api/v1/coupons/1001','{}','{}',NULL,'json','[]',30,0,'["marketing", "P1"]',2,true,0,'2026-05-18 02:56:00','success','2026-02-27 02:58:00','2026-05-31 17:02:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO api_test_cases(id,collection_id,project_id,user_id,environment_id,name,description,method,url,headers,params,body,body_type,assertions,timeout,retry_count,tags,priority,is_enabled,sort_order,last_run_at,last_status,created_at,updated_at)VALUES(226,44,7,5,28,'健康检查','验证健康检查','GET','/api/v1/health','{}','{}',NULL,'json','[]',30,0,'["health", "P0"]',3,true,1,'2026-05-19 08:58:00','success','2026-03-11 06:15:00','2026-05-30 10:44:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO api_test_cases(id,collection_id,project_id,user_id,environment_id,name,description,method,url,headers,params,body,body_type,assertions,timeout,retry_count,tags,priority,is_enabled,sort_order,last_run_at,last_status,created_at,updated_at)VALUES(227,44,7,7,26,'创建订单','验证创建订单','POST','/api/v1/orders','{}','{}',NULL,'json','[]',30,0,'["order", "P0"]',3,true,2,'2026-05-20 22:23:00','success','2026-05-12 17:44:00','2026-05-30 02:27:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO api_test_cases(id,collection_id,project_id,user_id,environment_id,name,description,method,url,headers,params,body,body_type,assertions,timeout,retry_count,tags,priority,is_enabled,sort_order,last_run_at,last_status,created_at,updated_at)VALUES(228,44,7,6,27,'获取配置','验证获取配置','GET','/api/v1/config','{}','{}',NULL,'json','[]',30,0,'["config", "P2"]',2,true,3,'2026-05-21 18:10:00','failed','2025-12-29 09:28:00','2026-05-31 19:50:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO api_test_cases(id,collection_id,project_id,user_id,environment_id,name,description,method,url,headers,params,body,body_type,assertions,timeout,retry_count,tags,priority,is_enabled,sort_order,last_run_at,last_status,created_at,updated_at)VALUES(229,45,7,2,26,'更新资料','验证更新资料','PUT','/api/v1/users/me','{}','{}',NULL,'json','[]',30,0,'["user", "P1"]',2,true,0,'2026-05-29 12:46:00','success','2025-11-05 23:14:00','2026-06-01 18:17:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO api_test_cases(id,collection_id,project_id,user_id,environment_id,name,description,method,url,headers,params,body,body_type,assertions,timeout,retry_count,tags,priority,is_enabled,sort_order,last_run_at,last_status,created_at,updated_at)VALUES(230,45,7,6,28,'提交反馈','验证提交反馈','POST','/api/v1/feedback','{}','{}',NULL,'json','[]',30,0,'["feedback", "P2"]',2,true,1,'2026-05-27 13:07:00','success','2026-05-27 02:58:00','2026-05-31 15:23:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO api_test_cases(id,collection_id,project_id,user_id,environment_id,name,description,method,url,headers,params,body,body_type,assertions,timeout,retry_count,tags,priority,is_enabled,sort_order,last_run_at,last_status,created_at,updated_at)VALUES(231,45,7,2,26,'支付状态','验证支付状态','GET','/api/v1/payments/1001','{}','{}',NULL,'json','[]',30,0,'["payment", "P1"]',1,true,2,'2026-05-31 15:51:00','success','2026-04-20 01:01:00','2026-05-31 17:35:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO api_test_cases(id,collection_id,project_id,user_id,environment_id,name,description,method,url,headers,params,body,body_type,assertions,timeout,retry_count,tags,priority,is_enabled,sort_order,last_run_at,last_status,created_at,updated_at)VALUES(232,45,7,7,25,'取消订单','验证取消订单','POST','/api/v1/orders/1001/cancel','{}','{}',NULL,'json','[]',30,0,'["order", "P1"]',2,true,3,'2026-05-24 07:47:00','running','2025-12-27 18:05:00','2026-05-30 04:46:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO api_test_cases(id,collection_id,project_id,user_id,environment_id,name,description,method,url,headers,params,body,body_type,assertions,timeout,retry_count,tags,priority,is_enabled,sort_order,last_run_at,last_status,created_at,updated_at)VALUES(233,46,7,5,28,'健康检查','验证健康检查','GET','/api/v1/health','{}','{}',NULL,'json','[]',30,0,'["health", "P0"]',2,true,0,'2026-05-31 02:36:00','success','2026-04-29 06:59:00','2026-05-31 17:05:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO api_test_cases(id,collection_id,project_id,user_id,environment_id,name,description,method,url,headers,params,body,body_type,assertions,timeout,retry_count,tags,priority,is_enabled,sort_order,last_run_at,last_status,created_at,updated_at)VALUES(234,46,7,7,28,'创建订单','验证创建订单','POST','/api/v1/orders','{}','{}',NULL,'json','[]',30,0,'["order", "P0"]',2,true,1,'2026-05-30 04:30:00','failed','2025-12-30 08:04:00','2026-06-02 07:30:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO api_test_cases(id,collection_id,project_id,user_id,environment_id,name,description,method,url,headers,params,body,body_type,assertions,timeout,retry_count,tags,priority,is_enabled,sort_order,last_run_at,last_status,created_at,updated_at)VALUES(235,46,7,2,25,'订单详情','验证订单详情','GET','/api/v1/orders/1001','{}','{}',NULL,'json','[]',30,0,'["order", "P0"]',2,true,2,'2026-05-19 17:34:00','running','2026-05-20 11:27:00','2026-05-30 02:09:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO api_test_cases(id,collection_id,project_id,user_id,environment_id,name,description,method,url,headers,params,body,body_type,assertions,timeout,retry_count,tags,priority,is_enabled,sort_order,last_run_at,last_status,created_at,updated_at)VALUES(236,46,7,6,28,'提交反馈','验证提交反馈','POST','/api/v1/feedback','{}','{}',NULL,'json','[]',30,0,'["feedback", "P2"]',2,true,3,'2026-05-29 20:52:00','success','2026-01-30 02:02:00','2026-06-02 00:22:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO api_test_cases(id,collection_id,project_id,user_id,environment_id,name,description,method,url,headers,params,body,body_type,assertions,timeout,retry_count,tags,priority,is_enabled,sort_order,last_run_at,last_status,created_at,updated_at)VALUES(237,46,7,7,28,'支付状态','验证支付状态','GET','/api/v1/payments/1001','{}','{}',NULL,'json','[]',30,0,'["payment", "P1"]',1,true,4,'2026-06-01 11:13:00','success','2026-01-04 17:53:00','2026-06-01 21:19:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO api_test_cases(id,collection_id,project_id,user_id,environment_id,name,description,method,url,headers,params,body,body_type,assertions,timeout,retry_count,tags,priority,is_enabled,sort_order,last_run_at,last_status,created_at,updated_at)VALUES(238,46,7,2,27,'更新资料','验证更新资料','PUT','/api/v1/users/me','{}','{}',NULL,'json','[]',30,0,'["user", "P1"]',3,true,5,'2026-05-30 05:33:00','success','2026-01-03 01:44:00','2026-05-29 15:37:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO api_test_cases(id,collection_id,project_id,user_id,environment_id,name,description,method,url,headers,params,body,body_type,assertions,timeout,retry_count,tags,priority,is_enabled,sort_order,last_run_at,last_status,created_at,updated_at)VALUES(239,47,7,7,28,'支付状态','验证支付状态','GET','/api/v1/payments/1001','{}','{}',NULL,'json','[]',30,0,'["payment", "P1"]',3,true,0,'2026-05-23 15:38:00','success','2026-02-19 10:52:00','2026-06-01 10:46:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO api_test_cases(id,collection_id,project_id,user_id,environment_id,name,description,method,url,headers,params,body,body_type,assertions,timeout,retry_count,tags,priority,is_enabled,sort_order,last_run_at,last_status,created_at,updated_at)VALUES(240,47,7,6,26,'搜索商品','验证搜索商品','GET','/api/v1/search','{}','{}',NULL,'json','[]',30,0,'["search", "P1"]',2,true,1,'2026-05-20 23:09:00','success','2025-12-25 11:17:00','2026-06-02 04:36:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO api_test_cases(id,collection_id,project_id,user_id,environment_id,name,description,method,url,headers,params,body,body_type,assertions,timeout,retry_count,tags,priority,is_enabled,sort_order,last_run_at,last_status,created_at,updated_at)VALUES(241,47,7,1,25,'取消订单','验证取消订单','POST','/api/v1/orders/1001/cancel','{}','{}',NULL,'json','[]',30,0,'["order", "P1"]',1,true,2,'2026-05-17 14:33:00','failed','2026-05-16 01:46:00','2026-05-31 07:22:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO api_test_cases(id,collection_id,project_id,user_id,environment_id,name,description,method,url,headers,params,body,body_type,assertions,timeout,retry_count,tags,priority,is_enabled,sort_order,last_run_at,last_status,created_at,updated_at)VALUES(242,47,7,1,28,'推荐列表','验证推荐列表','GET','/api/v1/recommendations','{}','{}',NULL,'json','[]',30,0,'["recommendation", "P2"]',2,true,3,NULL,'pending','2025-12-25 13:27:00','2026-05-30 11:22:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO api_test_cases(id,collection_id,project_id,user_id,environment_id,name,description,method,url,headers,params,body,body_type,assertions,timeout,retry_count,tags,priority,is_enabled,sort_order,last_run_at,last_status,created_at,updated_at)VALUES(243,47,7,1,26,'获取配置','验证获取配置','GET','/api/v1/config','{}','{}',NULL,'json','[]',30,0,'["config", "P2"]',3,true,4,'2026-05-19 09:48:00','success','2025-11-07 17:42:00','2026-06-01 08:10:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO api_test_cases(id,collection_id,project_id,user_id,environment_id,name,description,method,url,headers,params,body,body_type,assertions,timeout,retry_count,tags,priority,is_enabled,sort_order,last_run_at,last_status,created_at,updated_at)VALUES(244,47,7,7,26,'更新资料','验证更新资料','PUT','/api/v1/users/me','{}','{}',NULL,'json','[]',30,0,'["user", "P1"]',3,true,5,'2026-05-31 22:45:00','success','2026-06-01 04:55:00','2026-05-30 21:38:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO api_test_cases(id,collection_id,project_id,user_id,environment_id,name,description,method,url,headers,params,body,body_type,assertions,timeout,retry_count,tags,priority,is_enabled,sort_order,last_run_at,last_status,created_at,updated_at)VALUES(245,47,7,6,28,'订单详情','验证订单详情','GET','/api/v1/orders/1001','{}','{}',NULL,'json','[]',30,0,'["order", "P0"]',1,true,6,'2026-06-01 10:15:00','success','2026-05-08 16:42:00','2026-05-30 22:08:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO api_test_cases(id,collection_id,project_id,user_id,environment_id,name,description,method,url,headers,params,body,body_type,assertions,timeout,retry_count,tags,priority,is_enabled,sort_order,last_run_at,last_status,created_at,updated_at)VALUES(246,48,7,5,26,'发起支付','验证发起支付','POST','/api/v1/payments','{}','{}',NULL,'json','[]',30,0,'["payment", "P0"]',2,true,0,'2026-05-29 16:56:00','success','2026-03-17 23:53:00','2026-05-30 16:08:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO api_test_cases(id,collection_id,project_id,user_id,environment_id,name,description,method,url,headers,params,body,body_type,assertions,timeout,retry_count,tags,priority,is_enabled,sort_order,last_run_at,last_status,created_at,updated_at)VALUES(247,48,7,7,27,'取消订单','验证取消订单','POST','/api/v1/orders/1001/cancel','{}','{}',NULL,'json','[]',30,0,'["order", "P1"]',1,true,1,'2026-05-20 15:30:00','failed','2025-11-19 23:11:00','2026-05-29 12:31:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO api_test_cases(id,collection_id,project_id,user_id,environment_id,name,description,method,url,headers,params,body,body_type,assertions,timeout,retry_count,tags,priority,is_enabled,sort_order,last_run_at,last_status,created_at,updated_at)VALUES(248,48,7,7,25,'上传图片','验证上传图片','POST','/api/v1/upload','{}','{}',NULL,'json','[]',30,0,'["upload", "P1"]',3,true,2,'2026-05-25 07:36:00','success','2025-11-12 02:17:00','2026-05-31 23:34:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO api_test_cases(id,collection_id,project_id,user_id,environment_id,name,description,method,url,headers,params,body,body_type,assertions,timeout,retry_count,tags,priority,is_enabled,sort_order,last_run_at,last_status,created_at,updated_at)VALUES(249,48,7,5,25,'搜索商品','验证搜索商品','GET','/api/v1/search','{}','{}',NULL,'json','[]',30,0,'["search", "P1"]',1,true,3,'2026-05-25 02:42:00','failed','2026-02-18 12:13:00','2026-05-31 07:25:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO api_test_cases(id,collection_id,project_id,user_id,environment_id,name,description,method,url,headers,params,body,body_type,assertions,timeout,retry_count,tags,priority,is_enabled,sort_order,last_run_at,last_status,created_at,updated_at)VALUES(250,48,7,2,28,'用户登录','验证用户登录','POST','/api/v1/auth/login','{}','{}',NULL,'json','[]',30,0,'["auth", "P0"]',1,true,4,'2026-05-26 15:43:00','success','2025-11-21 12:01:00','2026-05-31 18:13:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO api_test_cases(id,collection_id,project_id,user_id,environment_id,name,description,method,url,headers,params,body,body_type,assertions,timeout,retry_count,tags,priority,is_enabled,sort_order,last_run_at,last_status,created_at,updated_at)VALUES(251,49,7,2,26,'发起支付','验证发起支付','POST','/api/v1/payments','{}','{}',NULL,'json','[]',30,0,'["payment", "P0"]',1,true,0,'2026-05-22 05:11:00','failed','2026-05-02 07:17:00','2026-05-29 15:00:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO api_test_cases(id,collection_id,project_id,user_id,environment_id,name,description,method,url,headers,params,body,body_type,assertions,timeout,retry_count,tags,priority,is_enabled,sort_order,last_run_at,last_status,created_at,updated_at)VALUES(252,49,7,7,25,'健康检查','验证健康检查','GET','/api/v1/health','{}','{}',NULL,'json','[]',30,0,'["health", "P0"]',2,true,1,'2026-05-21 14:40:00','failed','2026-01-05 01:29:00','2026-05-31 17:43:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO api_test_cases(id,collection_id,project_id,user_id,environment_id,name,description,method,url,headers,params,body,body_type,assertions,timeout,retry_count,tags,priority,is_enabled,sort_order,last_run_at,last_status,created_at,updated_at)VALUES(253,49,7,6,26,'支付状态','验证支付状态','GET','/api/v1/payments/1001','{}','{}',NULL,'json','[]',30,0,'["payment", "P1"]',2,true,2,'2026-05-29 08:27:00','failed','2026-01-29 16:58:00','2026-05-30 21:05:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO api_test_cases(id,collection_id,project_id,user_id,environment_id,name,description,method,url,headers,params,body,body_type,assertions,timeout,retry_count,tags,priority,is_enabled,sort_order,last_run_at,last_status,created_at,updated_at)VALUES(254,49,7,2,28,'取消订单','验证取消订单','POST','/api/v1/orders/1001/cancel','{}','{}',NULL,'json','[]',30,0,'["order", "P1"]',1,true,3,'2026-05-18 23:16:00','cancelled','2026-05-28 12:47:00','2026-05-29 15:54:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO api_test_cases(id,collection_id,project_id,user_id,environment_id,name,description,method,url,headers,params,body,body_type,assertions,timeout,retry_count,tags,priority,is_enabled,sort_order,last_run_at,last_status,created_at,updated_at)VALUES(255,50,8,5,32,'标记已读','验证标记已读','PUT','/api/v1/messages/1001','{}','{}',NULL,'json','[]',30,0,'["message", "P2"]',2,true,0,NULL,'pending','2026-02-28 04:29:00','2026-05-30 03:34:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO api_test_cases(id,collection_id,project_id,user_id,environment_id,name,description,method,url,headers,params,body,body_type,assertions,timeout,retry_count,tags,priority,is_enabled,sort_order,last_run_at,last_status,created_at,updated_at)VALUES(256,50,8,5,31,'支付状态','验证支付状态','GET','/api/v1/payments/1001','{}','{}',NULL,'json','[]',30,0,'["payment", "P1"]',2,true,1,'2026-05-24 19:49:00','running','2026-04-28 15:17:00','2026-06-01 06:14:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO api_test_cases(id,collection_id,project_id,user_id,environment_id,name,description,method,url,headers,params,body,body_type,assertions,timeout,retry_count,tags,priority,is_enabled,sort_order,last_run_at,last_status,created_at,updated_at)VALUES(257,50,8,5,30,'订单详情','验证订单详情','GET','/api/v1/orders/1001','{}','{}',NULL,'json','[]',30,0,'["order", "P0"]',3,true,2,'2026-05-21 03:51:00','success','2026-04-23 18:09:00','2026-06-02 04:34:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO api_test_cases(id,collection_id,project_id,user_id,environment_id,name,description,method,url,headers,params,body,body_type,assertions,timeout,retry_count,tags,priority,is_enabled,sort_order,last_run_at,last_status,created_at,updated_at)VALUES(258,50,8,6,30,'领取券','验证领取券','POST','/api/v1/coupons/1001','{}','{}',NULL,'json','[]',30,0,'["marketing", "P1"]',2,true,3,'2026-05-22 18:41:00','cancelled','2026-01-08 15:57:00','2026-05-30 06:16:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO api_test_cases(id,collection_id,project_id,user_id,environment_id,name,description,method,url,headers,params,body,body_type,assertions,timeout,retry_count,tags,priority,is_enabled,sort_order,last_run_at,last_status,created_at,updated_at)VALUES(259,50,8,2,29,'发起支付','验证发起支付','POST','/api/v1/payments','{}','{}',NULL,'json','[]',30,0,'["payment", "P0"]',3,true,4,'2026-05-24 18:07:00','success','2026-05-07 19:13:00','2026-05-31 01:37:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO api_test_cases(id,collection_id,project_id,user_id,environment_id,name,description,method,url,headers,params,body,body_type,assertions,timeout,retry_count,tags,priority,is_enabled,sort_order,last_run_at,last_status,created_at,updated_at)VALUES(260,51,8,6,29,'优惠券','验证优惠券','GET','/api/v1/coupons','{}','{}',NULL,'json','[]',30,0,'["marketing", "P1"]',3,true,0,'2026-05-26 15:24:00','success','2025-12-16 16:49:00','2026-05-30 22:40:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO api_test_cases(id,collection_id,project_id,user_id,environment_id,name,description,method,url,headers,params,body,body_type,assertions,timeout,retry_count,tags,priority,is_enabled,sort_order,last_run_at,last_status,created_at,updated_at)VALUES(261,51,8,7,32,'健康检查','验证健康检查','GET','/api/v1/health','{}','{}',NULL,'json','[]',30,0,'["health", "P0"]',2,true,1,'2026-05-19 07:36:00','failed','2026-03-19 19:20:00','2026-06-01 04:20:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO api_test_cases(id,collection_id,project_id,user_id,environment_id,name,description,method,url,headers,params,body,body_type,assertions,timeout,retry_count,tags,priority,is_enabled,sort_order,last_run_at,last_status,created_at,updated_at)VALUES(262,51,8,5,32,'支付状态','验证支付状态','GET','/api/v1/payments/1001','{}','{}',NULL,'json','[]',30,0,'["payment", "P1"]',1,true,2,'2026-05-21 07:55:00','success','2026-03-06 02:40:00','2026-05-30 13:42:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO api_test_cases(id,collection_id,project_id,user_id,environment_id,name,description,method,url,headers,params,body,body_type,assertions,timeout,retry_count,tags,priority,is_enabled,sort_order,last_run_at,last_status,created_at,updated_at)VALUES(263,51,8,5,32,'标记已读','验证标记已读','PUT','/api/v1/messages/1001','{}','{}',NULL,'json','[]',30,0,'["message", "P2"]',2,true,3,'2026-05-18 22:13:00','success','2026-01-18 19:34:00','2026-06-01 04:06:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO api_test_cases(id,collection_id,project_id,user_id,environment_id,name,description,method,url,headers,params,body,body_type,assertions,timeout,retry_count,tags,priority,is_enabled,sort_order,last_run_at,last_status,created_at,updated_at)VALUES(264,51,8,1,30,'用户登录','验证用户登录','POST','/api/v1/auth/login','{}','{}',NULL,'json','[]',30,0,'["auth", "P0"]',3,true,4,'2026-05-24 10:16:00','failed','2026-05-12 03:50:00','2026-05-30 06:54:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO api_test_cases(id,collection_id,project_id,user_id,environment_id,name,description,method,url,headers,params,body,body_type,assertions,timeout,retry_count,tags,priority,is_enabled,sort_order,last_run_at,last_status,created_at,updated_at)VALUES(265,52,8,1,32,'获取配置','验证获取配置','GET','/api/v1/config','{}','{}',NULL,'json','[]',30,0,'["config", "P2"]',2,true,0,'2026-05-31 06:44:00','success','2026-04-23 07:19:00','2026-05-30 00:46:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO api_test_cases(id,collection_id,project_id,user_id,environment_id,name,description,method,url,headers,params,body,body_type,assertions,timeout,retry_count,tags,priority,is_enabled,sort_order,last_run_at,last_status,created_at,updated_at)VALUES(266,52,8,2,31,'优惠券','验证优惠券','GET','/api/v1/coupons','{}','{}',NULL,'json','[]',30,0,'["marketing", "P1"]',1,true,1,'2026-05-29 05:27:00','success','2026-05-25 08:18:00','2026-05-30 23:05:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO api_test_cases(id,collection_id,project_id,user_id,environment_id,name,description,method,url,headers,params,body,body_type,assertions,timeout,retry_count,tags,priority,is_enabled,sort_order,last_run_at,last_status,created_at,updated_at)VALUES(267,52,8,6,32,'用户信息','验证用户信息','GET','/api/v1/users/me','{}','{}',NULL,'json','[]',30,0,'["user", "P0"]',1,true,2,'2026-05-24 16:32:00','cancelled','2025-12-04 16:49:00','2026-05-29 13:13:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO api_test_cases(id,collection_id,project_id,user_id,environment_id,name,description,method,url,headers,params,body,body_type,assertions,timeout,retry_count,tags,priority,is_enabled,sort_order,last_run_at,last_status,created_at,updated_at)VALUES(268,53,8,1,32,'领取券','验证领取券','POST','/api/v1/coupons/1001','{}','{}',NULL,'json','[]',30,0,'["marketing", "P1"]',2,true,0,'2026-05-20 01:51:00','success','2026-05-30 09:27:00','2026-05-31 22:42:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO api_test_cases(id,collection_id,project_id,user_id,environment_id,name,description,method,url,headers,params,body,body_type,assertions,timeout,retry_count,tags,priority,is_enabled,sort_order,last_run_at,last_status,created_at,updated_at)VALUES(269,53,8,6,29,'推荐列表','验证推荐列表','GET','/api/v1/recommendations','{}','{}',NULL,'json','[]',30,0,'["recommendation", "P2"]',1,true,1,'2026-05-17 18:41:00','failed','2025-11-16 20:09:00','2026-05-30 14:46:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO api_test_cases(id,collection_id,project_id,user_id,environment_id,name,description,method,url,headers,params,body,body_type,assertions,timeout,retry_count,tags,priority,is_enabled,sort_order,last_run_at,last_status,created_at,updated_at)VALUES(270,53,8,1,31,'提交反馈','验证提交反馈','POST','/api/v1/feedback','{}','{}',NULL,'json','[]',30,0,'["feedback", "P2"]',1,true,2,'2026-05-19 21:45:00','success','2025-11-29 10:19:00','2026-05-29 21:46:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO api_test_cases(id,collection_id,project_id,user_id,environment_id,name,description,method,url,headers,params,body,body_type,assertions,timeout,retry_count,tags,priority,is_enabled,sort_order,last_run_at,last_status,created_at,updated_at)VALUES(271,53,8,5,29,'申请退款','验证申请退款','POST','/api/v1/refunds','{}','{}',NULL,'json','[]',30,0,'["payment", "P1"]',2,true,3,'2026-05-25 17:12:00','success','2025-11-06 11:17:00','2026-05-31 00:19:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO api_test_cases(id,collection_id,project_id,user_id,environment_id,name,description,method,url,headers,params,body,body_type,assertions,timeout,retry_count,tags,priority,is_enabled,sort_order,last_run_at,last_status,created_at,updated_at)VALUES(272,53,8,7,31,'标记已读','验证标记已读','PUT','/api/v1/messages/1001','{}','{}',NULL,'json','[]',30,0,'["message", "P2"]',2,true,4,'2026-05-31 04:52:00','success','2026-05-03 13:31:00','2026-05-30 01:16:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO api_test_cases(id,collection_id,project_id,user_id,environment_id,name,description,method,url,headers,params,body,body_type,assertions,timeout,retry_count,tags,priority,is_enabled,sort_order,last_run_at,last_status,created_at,updated_at)VALUES(273,53,8,7,32,'发起支付','验证发起支付','POST','/api/v1/payments','{}','{}',NULL,'json','[]',30,0,'["payment", "P0"]',2,true,5,'2026-06-02 05:57:00','success','2026-05-27 04:54:00','2026-05-31 01:52:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO api_test_cases(id,collection_id,project_id,user_id,environment_id,name,description,method,url,headers,params,body,body_type,assertions,timeout,retry_count,tags,priority,is_enabled,sort_order,last_run_at,last_status,created_at,updated_at)VALUES(274,53,8,6,29,'支付状态','验证支付状态','GET','/api/v1/payments/1001','{}','{}',NULL,'json','[]',30,0,'["payment", "P1"]',1,true,6,'2026-05-29 09:29:00','success','2026-03-05 20:41:00','2026-05-29 22:31:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO api_test_cases(id,collection_id,project_id,user_id,environment_id,name,description,method,url,headers,params,body,body_type,assertions,timeout,retry_count,tags,priority,is_enabled,sort_order,last_run_at,last_status,created_at,updated_at)VALUES(275,53,8,1,31,'商品列表','验证商品列表','GET','/api/v1/products','{}','{}',NULL,'json','[]',30,0,'["product", "P0"]',2,true,7,'2026-05-29 08:43:00','success','2026-05-13 16:30:00','2026-06-01 03:03:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO api_test_cases(id,collection_id,project_id,user_id,environment_id,name,description,method,url,headers,params,body,body_type,assertions,timeout,retry_count,tags,priority,is_enabled,sort_order,last_run_at,last_status,created_at,updated_at)VALUES(276,54,8,6,30,'搜索商品','验证搜索商品','GET','/api/v1/search','{}','{}',NULL,'json','[]',30,0,'["search", "P1"]',3,true,0,'2026-06-01 03:31:00','failed','2025-11-16 06:27:00','2026-05-31 18:36:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO api_test_cases(id,collection_id,project_id,user_id,environment_id,name,description,method,url,headers,params,body,body_type,assertions,timeout,retry_count,tags,priority,is_enabled,sort_order,last_run_at,last_status,created_at,updated_at)VALUES(277,54,8,5,31,'用户登录','验证用户登录','POST','/api/v1/auth/login','{}','{}',NULL,'json','[]',30,0,'["auth", "P0"]',2,true,1,'2026-05-31 10:01:00','success','2026-01-19 06:44:00','2026-05-29 13:41:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO api_test_cases(id,collection_id,project_id,user_id,environment_id,name,description,method,url,headers,params,body,body_type,assertions,timeout,retry_count,tags,priority,is_enabled,sort_order,last_run_at,last_status,created_at,updated_at)VALUES(278,54,8,2,31,'商品列表','验证商品列表','GET','/api/v1/products','{}','{}',NULL,'json','[]',30,0,'["product", "P0"]',3,true,2,'2026-05-27 06:45:00','running','2026-02-10 00:00:00','2026-06-01 01:23:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO api_test_cases(id,collection_id,project_id,user_id,environment_id,name,description,method,url,headers,params,body,body_type,assertions,timeout,retry_count,tags,priority,is_enabled,sort_order,last_run_at,last_status,created_at,updated_at)VALUES(279,54,8,1,32,'发起支付','验证发起支付','POST','/api/v1/payments','{}','{}',NULL,'json','[]',30,0,'["payment", "P0"]',3,true,3,'2026-06-02 08:23:00','failed','2026-01-30 11:22:00','2026-05-31 22:11:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO api_test_cases(id,collection_id,project_id,user_id,environment_id,name,description,method,url,headers,params,body,body_type,assertions,timeout,retry_count,tags,priority,is_enabled,sort_order,last_run_at,last_status,created_at,updated_at)VALUES(280,54,8,1,30,'健康检查','验证健康检查','GET','/api/v1/health','{}','{}',NULL,'json','[]',30,0,'["health", "P0"]',2,true,4,'2026-05-30 12:21:00','success','2025-11-18 13:57:00','2026-06-01 22:19:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO api_test_cases(id,collection_id,project_id,user_id,environment_id,name,description,method,url,headers,params,body,body_type,assertions,timeout,retry_count,tags,priority,is_enabled,sort_order,last_run_at,last_status,created_at,updated_at)VALUES(281,55,8,2,31,'优惠券','验证优惠券','GET','/api/v1/coupons','{}','{}',NULL,'json','[]',30,0,'["marketing", "P1"]',1,true,0,'2026-05-21 19:14:00','cancelled','2026-05-26 11:36:00','2026-05-30 10:52:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO api_test_cases(id,collection_id,project_id,user_id,environment_id,name,description,method,url,headers,params,body,body_type,assertions,timeout,retry_count,tags,priority,is_enabled,sort_order,last_run_at,last_status,created_at,updated_at)VALUES(282,55,8,5,29,'商品列表','验证商品列表','GET','/api/v1/products','{}','{}',NULL,'json','[]',30,0,'["product", "P0"]',2,true,1,'2026-05-18 16:42:00','success','2025-12-04 18:48:00','2026-05-31 16:38:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO api_test_cases(id,collection_id,project_id,user_id,environment_id,name,description,method,url,headers,params,body,body_type,assertions,timeout,retry_count,tags,priority,is_enabled,sort_order,last_run_at,last_status,created_at,updated_at)VALUES(283,55,8,5,32,'创建订单','验证创建订单','POST','/api/v1/orders','{}','{}',NULL,'json','[]',30,0,'["order", "P0"]',1,true,2,'2026-05-28 07:27:00','success','2026-02-06 00:08:00','2026-05-30 16:37:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO api_test_cases(id,collection_id,project_id,user_id,environment_id,name,description,method,url,headers,params,body,body_type,assertions,timeout,retry_count,tags,priority,is_enabled,sort_order,last_run_at,last_status,created_at,updated_at)VALUES(284,55,8,6,29,'获取配置','验证获取配置','GET','/api/v1/config','{}','{}',NULL,'json','[]',30,0,'["config", "P2"]',1,true,3,'2026-05-20 10:49:00','failed','2025-12-24 22:11:00','2026-05-31 23:14:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO api_test_cases(id,collection_id,project_id,user_id,environment_id,name,description,method,url,headers,params,body,body_type,assertions,timeout,retry_count,tags,priority,is_enabled,sort_order,last_run_at,last_status,created_at,updated_at)VALUES(285,56,8,7,32,'优惠券','验证优惠券','GET','/api/v1/coupons','{}','{}',NULL,'json','[]',30,0,'["marketing", "P1"]',2,true,0,'2026-05-28 14:42:00','failed','2026-02-16 13:40:00','2026-06-02 06:27:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO api_test_cases(id,collection_id,project_id,user_id,environment_id,name,description,method,url,headers,params,body,body_type,assertions,timeout,retry_count,tags,priority,is_enabled,sort_order,last_run_at,last_status,created_at,updated_at)VALUES(286,56,8,1,29,'搜索商品','验证搜索商品','GET','/api/v1/search','{}','{}',NULL,'json','[]',30,0,'["search", "P1"]',1,true,1,'2026-05-29 04:05:00','failed','2026-04-11 06:29:00','2026-06-01 06:58:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO api_test_cases(id,collection_id,project_id,user_id,environment_id,name,description,method,url,headers,params,body,body_type,assertions,timeout,retry_count,tags,priority,is_enabled,sort_order,last_run_at,last_status,created_at,updated_at)VALUES(287,56,8,7,32,'取消订单','验证取消订单','POST','/api/v1/orders/1001/cancel','{}','{}',NULL,'json','[]',30,0,'["order", "P1"]',1,true,2,'2026-05-25 08:37:00','failed','2025-12-27 11:56:00','2026-06-02 03:19:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO api_test_cases(id,collection_id,project_id,user_id,environment_id,name,description,method,url,headers,params,body,body_type,assertions,timeout,retry_count,tags,priority,is_enabled,sort_order,last_run_at,last_status,created_at,updated_at)VALUES(288,57,9,5,33,'更新资料','验证更新资料','PUT','/api/v1/users/me','{}','{}',NULL,'json','[]',30,0,'["user", "P1"]',3,true,0,'2026-05-24 17:58:00','failed','2026-05-14 00:56:00','2026-05-31 17:54:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO api_test_cases(id,collection_id,project_id,user_id,environment_id,name,description,method,url,headers,params,body,body_type,assertions,timeout,retry_count,tags,priority,is_enabled,sort_order,last_run_at,last_status,created_at,updated_at)VALUES(289,57,9,1,34,'上传图片','验证上传图片','POST','/api/v1/upload','{}','{}',NULL,'json','[]',30,0,'["upload", "P1"]',3,true,1,'2026-05-27 03:27:00','success','2026-03-29 15:20:00','2026-05-31 16:13:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO api_test_cases(id,collection_id,project_id,user_id,environment_id,name,description,method,url,headers,params,body,body_type,assertions,timeout,retry_count,tags,priority,is_enabled,sort_order,last_run_at,last_status,created_at,updated_at)VALUES(290,57,9,7,36,'用户信息','验证用户信息','GET','/api/v1/users/me','{}','{}',NULL,'json','[]',30,0,'["user", "P0"]',3,true,2,'2026-05-21 12:31:00','failed','2025-12-12 20:04:00','2026-06-02 04:10:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO api_test_cases(id,collection_id,project_id,user_id,environment_id,name,description,method,url,headers,params,body,body_type,assertions,timeout,retry_count,tags,priority,is_enabled,sort_order,last_run_at,last_status,created_at,updated_at)VALUES(291,57,9,2,36,'标记已读','验证标记已读','PUT','/api/v1/messages/1001','{}','{}',NULL,'json','[]',30,0,'["message", "P2"]',2,true,3,'2026-05-27 16:22:00','success','2026-03-02 23:25:00','2026-05-30 22:34:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO api_test_cases(id,collection_id,project_id,user_id,environment_id,name,description,method,url,headers,params,body,body_type,assertions,timeout,retry_count,tags,priority,is_enabled,sort_order,last_run_at,last_status,created_at,updated_at)VALUES(292,57,9,6,35,'推荐列表','验证推荐列表','GET','/api/v1/recommendations','{}','{}',NULL,'json','[]',30,0,'["recommendation", "P2"]',2,true,4,'2026-05-26 21:11:00','success','2025-11-23 01:37:00','2026-05-29 19:35:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO api_test_cases(id,collection_id,project_id,user_id,environment_id,name,description,method,url,headers,params,body,body_type,assertions,timeout,retry_count,tags,priority,is_enabled,sort_order,last_run_at,last_status,created_at,updated_at)VALUES(293,57,9,1,33,'获取配置','验证获取配置','GET','/api/v1/config','{}','{}',NULL,'json','[]',30,0,'["config", "P2"]',2,true,5,'2026-06-01 17:52:00','cancelled','2026-05-31 00:46:00','2026-05-31 23:59:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO api_test_cases(id,collection_id,project_id,user_id,environment_id,name,description,method,url,headers,params,body,body_type,assertions,timeout,retry_count,tags,priority,is_enabled,sort_order,last_run_at,last_status,created_at,updated_at)VALUES(294,58,9,2,34,'支付状态','验证支付状态','GET','/api/v1/payments/1001','{}','{}',NULL,'json','[]',30,0,'["payment", "P1"]',2,true,0,'2026-05-26 02:44:00','success','2026-05-08 15:35:00','2026-05-31 10:56:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO api_test_cases(id,collection_id,project_id,user_id,environment_id,name,description,method,url,headers,params,body,body_type,assertions,timeout,retry_count,tags,priority,is_enabled,sort_order,last_run_at,last_status,created_at,updated_at)VALUES(295,58,9,5,36,'优惠券','验证优惠券','GET','/api/v1/coupons','{}','{}',NULL,'json','[]',30,0,'["marketing", "P1"]',2,true,1,'2026-05-29 14:19:00','success','2026-05-22 10:09:00','2026-05-30 07:11:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO api_test_cases(id,collection_id,project_id,user_id,environment_id,name,description,method,url,headers,params,body,body_type,assertions,timeout,retry_count,tags,priority,is_enabled,sort_order,last_run_at,last_status,created_at,updated_at)VALUES(296,58,9,1,35,'提交反馈','验证提交反馈','POST','/api/v1/feedback','{}','{}',NULL,'json','[]',30,0,'["feedback", "P2"]',1,true,2,'2026-05-19 20:01:00','success','2025-11-16 02:13:00','2026-06-01 13:11:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO api_test_cases(id,collection_id,project_id,user_id,environment_id,name,description,method,url,headers,params,body,body_type,assertions,timeout,retry_count,tags,priority,is_enabled,sort_order,last_run_at,last_status,created_at,updated_at)VALUES(297,58,9,6,33,'创建订单','验证创建订单','POST','/api/v1/orders','{}','{}',NULL,'json','[]',30,0,'["order", "P0"]',2,true,3,'2026-05-31 23:26:00','success','2026-04-23 23:28:00','2026-06-01 05:57:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO api_test_cases(id,collection_id,project_id,user_id,environment_id,name,description,method,url,headers,params,body,body_type,assertions,timeout,retry_count,tags,priority,is_enabled,sort_order,last_run_at,last_status,created_at,updated_at)VALUES(298,58,9,6,36,'商品列表','验证商品列表','GET','/api/v1/products','{}','{}',NULL,'json','[]',30,0,'["product", "P0"]',2,true,4,'2026-05-31 02:33:00','failed','2025-11-11 21:51:00','2026-05-31 23:55:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO api_test_cases(id,collection_id,project_id,user_id,environment_id,name,description,method,url,headers,params,body,body_type,assertions,timeout,retry_count,tags,priority,is_enabled,sort_order,last_run_at,last_status,created_at,updated_at)VALUES(299,58,9,6,33,'用户登录','验证用户登录','POST','/api/v1/auth/login','{}','{}',NULL,'json','[]',30,0,'["auth", "P0"]',2,true,5,'2026-05-25 07:35:00','success','2026-02-09 11:52:00','2026-05-31 18:25:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO api_test_cases(id,collection_id,project_id,user_id,environment_id,name,description,method,url,headers,params,body,body_type,assertions,timeout,retry_count,tags,priority,is_enabled,sort_order,last_run_at,last_status,created_at,updated_at)VALUES(300,58,9,2,36,'发起支付','验证发起支付','POST','/api/v1/payments','{}','{}',NULL,'json','[]',30,0,'["payment", "P0"]',3,true,6,'2026-05-26 16:21:00','success','2026-01-18 02:45:00','2026-06-02 01:11:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO api_test_cases(id,collection_id,project_id,user_id,environment_id,name,description,method,url,headers,params,body,body_type,assertions,timeout,retry_count,tags,priority,is_enabled,sort_order,last_run_at,last_status,created_at,updated_at)VALUES(301,58,9,6,35,'订单详情','验证订单详情','GET','/api/v1/orders/1001','{}','{}',NULL,'json','[]',30,0,'["order", "P0"]',2,true,7,'2026-05-31 06:18:00','failed','2026-02-12 22:38:00','2026-05-31 23:38:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO api_test_cases(id,collection_id,project_id,user_id,environment_id,name,description,method,url,headers,params,body,body_type,assertions,timeout,retry_count,tags,priority,is_enabled,sort_order,last_run_at,last_status,created_at,updated_at)VALUES(302,59,9,6,33,'用户登录','验证用户登录','POST','/api/v1/auth/login','{}','{}',NULL,'json','[]',30,0,'["auth", "P0"]',1,true,0,NULL,'pending','2026-04-10 12:37:00','2026-05-31 10:06:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO api_test_cases(id,collection_id,project_id,user_id,environment_id,name,description,method,url,headers,params,body,body_type,assertions,timeout,retry_count,tags,priority,is_enabled,sort_order,last_run_at,last_status,created_at,updated_at)VALUES(303,59,9,1,33,'申请退款','验证申请退款','POST','/api/v1/refunds','{}','{}',NULL,'json','[]',30,0,'["payment", "P1"]',1,true,1,'2026-05-25 14:01:00','failed','2025-11-04 01:00:00','2026-05-30 11:09:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO api_test_cases(id,collection_id,project_id,user_id,environment_id,name,description,method,url,headers,params,body,body_type,assertions,timeout,retry_count,tags,priority,is_enabled,sort_order,last_run_at,last_status,created_at,updated_at)VALUES(304,59,9,1,35,'订单详情','验证订单详情','GET','/api/v1/orders/1001','{}','{}',NULL,'json','[]',30,0,'["order", "P0"]',3,true,2,'2026-06-01 23:47:00','success','2026-01-15 03:47:00','2026-05-30 16:30:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO api_test_cases(id,collection_id,project_id,user_id,environment_id,name,description,method,url,headers,params,body,body_type,assertions,timeout,retry_count,tags,priority,is_enabled,sort_order,last_run_at,last_status,created_at,updated_at)VALUES(305,59,9,7,34,'标记已读','验证标记已读','PUT','/api/v1/messages/1001','{}','{}',NULL,'json','[]',30,0,'["message", "P2"]',3,true,3,'2026-06-01 21:23:00','failed','2026-01-18 08:44:00','2026-06-01 08:42:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO api_test_cases(id,collection_id,project_id,user_id,environment_id,name,description,method,url,headers,params,body,body_type,assertions,timeout,retry_count,tags,priority,is_enabled,sort_order,last_run_at,last_status,created_at,updated_at)VALUES(306,59,9,2,35,'上传图片','验证上传图片','POST','/api/v1/upload','{}','{}',NULL,'json','[]',30,0,'["upload", "P1"]',3,true,4,'2026-06-02 07:36:00','success','2026-03-23 12:06:00','2026-05-31 06:59:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO api_test_cases(id,collection_id,project_id,user_id,environment_id,name,description,method,url,headers,params,body,body_type,assertions,timeout,retry_count,tags,priority,is_enabled,sort_order,last_run_at,last_status,created_at,updated_at)VALUES(307,59,9,5,36,'领取券','验证领取券','POST','/api/v1/coupons/1001','{}','{}',NULL,'json','[]',30,0,'["marketing", "P1"]',1,true,5,'2026-05-20 17:15:00','success','2026-03-12 18:05:00','2026-06-02 04:48:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO api_test_cases(id,collection_id,project_id,user_id,environment_id,name,description,method,url,headers,params,body,body_type,assertions,timeout,retry_count,tags,priority,is_enabled,sort_order,last_run_at,last_status,created_at,updated_at)VALUES(308,59,9,7,36,'更新资料','验证更新资料','PUT','/api/v1/users/me','{}','{}',NULL,'json','[]',30,0,'["user", "P1"]',2,true,6,'2026-06-02 08:45:00','success','2026-03-14 23:29:00','2026-05-29 10:50:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO api_test_cases(id,collection_id,project_id,user_id,environment_id,name,description,method,url,headers,params,body,body_type,assertions,timeout,retry_count,tags,priority,is_enabled,sort_order,last_run_at,last_status,created_at,updated_at)VALUES(309,60,9,5,34,'标记已读','验证标记已读','PUT','/api/v1/messages/1001','{}','{}',NULL,'json','[]',30,0,'["message", "P2"]',2,true,0,'2026-05-25 08:20:00','cancelled','2026-02-22 09:25:00','2026-05-31 02:51:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO api_test_cases(id,collection_id,project_id,user_id,environment_id,name,description,method,url,headers,params,body,body_type,assertions,timeout,retry_count,tags,priority,is_enabled,sort_order,last_run_at,last_status,created_at,updated_at)VALUES(310,60,9,5,36,'健康检查','验证健康检查','GET','/api/v1/health','{}','{}',NULL,'json','[]',30,0,'["health", "P0"]',2,true,1,'2026-05-30 10:36:00','failed','2025-12-09 14:05:00','2026-05-31 20:45:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO api_test_cases(id,collection_id,project_id,user_id,environment_id,name,description,method,url,headers,params,body,body_type,assertions,timeout,retry_count,tags,priority,is_enabled,sort_order,last_run_at,last_status,created_at,updated_at)VALUES(311,60,9,7,34,'领取券','验证领取券','POST','/api/v1/coupons/1001','{}','{}',NULL,'json','[]',30,0,'["marketing", "P1"]',2,true,2,'2026-05-23 14:39:00','success','2026-01-14 05:47:00','2026-05-31 15:26:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO api_test_cases(id,collection_id,project_id,user_id,environment_id,name,description,method,url,headers,params,body,body_type,assertions,timeout,retry_count,tags,priority,is_enabled,sort_order,last_run_at,last_status,created_at,updated_at)VALUES(312,61,9,7,34,'取消订单','验证取消订单','POST','/api/v1/orders/1001/cancel','{}','{}',NULL,'json','[]',30,0,'["order", "P1"]',1,true,0,'2026-05-30 04:40:00','success','2025-11-27 09:12:00','2026-05-30 20:34:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO api_test_cases(id,collection_id,project_id,user_id,environment_id,name,description,method,url,headers,params,body,body_type,assertions,timeout,retry_count,tags,priority,is_enabled,sort_order,last_run_at,last_status,created_at,updated_at)VALUES(313,61,9,5,36,'创建订单','验证创建订单','POST','/api/v1/orders','{}','{}',NULL,'json','[]',30,0,'["order", "P0"]',1,true,1,'2026-05-25 05:11:00','failed','2026-05-05 05:49:00','2026-06-01 14:21:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO api_test_cases(id,collection_id,project_id,user_id,environment_id,name,description,method,url,headers,params,body,body_type,assertions,timeout,retry_count,tags,priority,is_enabled,sort_order,last_run_at,last_status,created_at,updated_at)VALUES(314,61,9,5,34,'申请退款','验证申请退款','POST','/api/v1/refunds','{}','{}',NULL,'json','[]',30,0,'["payment", "P1"]',2,true,2,'2026-05-25 12:59:00','success','2026-05-11 11:11:00','2026-05-30 05:28:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO api_test_cases(id,collection_id,project_id,user_id,environment_id,name,description,method,url,headers,params,body,body_type,assertions,timeout,retry_count,tags,priority,is_enabled,sort_order,last_run_at,last_status,created_at,updated_at)VALUES(315,61,9,7,36,'提交反馈','验证提交反馈','POST','/api/v1/feedback','{}','{}',NULL,'json','[]',30,0,'["feedback", "P2"]',2,true,3,'2026-05-22 04:06:00','failed','2026-01-26 18:52:00','2026-06-01 03:46:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO api_test_cases(id,collection_id,project_id,user_id,environment_id,name,description,method,url,headers,params,body,body_type,assertions,timeout,retry_count,tags,priority,is_enabled,sort_order,last_run_at,last_status,created_at,updated_at)VALUES(316,61,9,1,36,'领取券','验证领取券','POST','/api/v1/coupons/1001','{}','{}',NULL,'json','[]',30,0,'["marketing", "P1"]',1,true,4,'2026-06-02 01:34:00','failed','2025-11-22 12:48:00','2026-06-01 07:49:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO api_test_cases(id,collection_id,project_id,user_id,environment_id,name,description,method,url,headers,params,body,body_type,assertions,timeout,retry_count,tags,priority,is_enabled,sort_order,last_run_at,last_status,created_at,updated_at)VALUES(317,61,9,6,36,'健康检查','验证健康检查','GET','/api/v1/health','{}','{}',NULL,'json','[]',30,0,'["health", "P0"]',2,true,5,'2026-05-19 02:33:00','failed','2025-11-15 08:22:00','2026-05-29 10:40:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO api_test_cases(id,collection_id,project_id,user_id,environment_id,name,description,method,url,headers,params,body,body_type,assertions,timeout,retry_count,tags,priority,is_enabled,sort_order,last_run_at,last_status,created_at,updated_at)VALUES(318,61,9,6,33,'搜索商品','验证搜索商品','GET','/api/v1/search','{}','{}',NULL,'json','[]',30,0,'["search", "P1"]',1,true,6,'2026-05-18 19:08:00','success','2026-03-30 17:26:00','2026-05-29 10:58:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO api_test_cases(id,collection_id,project_id,user_id,environment_id,name,description,method,url,headers,params,body,body_type,assertions,timeout,retry_count,tags,priority,is_enabled,sort_order,last_run_at,last_status,created_at,updated_at)VALUES(319,61,9,7,36,'更新资料','验证更新资料','PUT','/api/v1/users/me','{}','{}',NULL,'json','[]',30,0,'["user", "P1"]',2,true,7,'2026-06-01 03:42:00','success','2026-02-20 00:11:00','2026-05-30 19:50:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO api_test_cases(id,collection_id,project_id,user_id,environment_id,name,description,method,url,headers,params,body,body_type,assertions,timeout,retry_count,tags,priority,is_enabled,sort_order,last_run_at,last_status,created_at,updated_at)VALUES(320,62,9,6,33,'申请退款','验证申请退款','POST','/api/v1/refunds','{}','{}',NULL,'json','[]',30,0,'["payment", "P1"]',2,true,0,'2026-05-30 04:11:00','failed','2025-12-04 16:52:00','2026-05-29 20:40:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO api_test_cases(id,collection_id,project_id,user_id,environment_id,name,description,method,url,headers,params,body,body_type,assertions,timeout,retry_count,tags,priority,is_enabled,sort_order,last_run_at,last_status,created_at,updated_at)VALUES(321,62,9,6,33,'用户信息','验证用户信息','GET','/api/v1/users/me','{}','{}',NULL,'json','[]',30,0,'["user", "P0"]',2,true,1,'2026-05-26 19:55:00','success','2026-03-10 11:19:00','2026-05-31 11:14:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO api_test_cases(id,collection_id,project_id,user_id,environment_id,name,description,method,url,headers,params,body,body_type,assertions,timeout,retry_count,tags,priority,is_enabled,sort_order,last_run_at,last_status,created_at,updated_at)VALUES(322,62,9,1,33,'提交反馈','验证提交反馈','POST','/api/v1/feedback','{}','{}',NULL,'json','[]',30,0,'["feedback", "P2"]',1,true,2,'2026-05-18 13:37:00','success','2026-01-17 11:36:00','2026-05-31 21:25:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO api_test_cases(id,collection_id,project_id,user_id,environment_id,name,description,method,url,headers,params,body,body_type,assertions,timeout,retry_count,tags,priority,is_enabled,sort_order,last_run_at,last_status,created_at,updated_at)VALUES(323,62,9,6,33,'创建订单','验证创建订单','POST','/api/v1/orders','{}','{}',NULL,'json','[]',30,0,'["order", "P0"]',3,true,3,'2026-05-22 15:05:00','failed','2026-04-24 04:05:00','2026-06-01 04:11:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO api_test_cases(id,collection_id,project_id,user_id,environment_id,name,description,method,url,headers,params,body,body_type,assertions,timeout,retry_count,tags,priority,is_enabled,sort_order,last_run_at,last_status,created_at,updated_at)VALUES(324,62,9,1,36,'上传图片','验证上传图片','POST','/api/v1/upload','{}','{}',NULL,'json','[]',30,0,'["upload", "P1"]',1,true,4,'2026-05-19 00:20:00','success','2026-05-02 05:48:00','2026-06-01 14:12:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO api_test_cases(id,collection_id,project_id,user_id,environment_id,name,description,method,url,headers,params,body,body_type,assertions,timeout,retry_count,tags,priority,is_enabled,sort_order,last_run_at,last_status,created_at,updated_at)VALUES(325,62,9,5,33,'推荐列表','验证推荐列表','GET','/api/v1/recommendations','{}','{}',NULL,'json','[]',30,0,'["recommendation", "P2"]',1,true,5,'2026-05-17 16:09:00','success','2025-12-27 18:45:00','2026-05-31 15:18:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO api_test_cases(id,collection_id,project_id,user_id,environment_id,name,description,method,url,headers,params,body,body_type,assertions,timeout,retry_count,tags,priority,is_enabled,sort_order,last_run_at,last_status,created_at,updated_at)VALUES(326,63,9,7,35,'上传图片','验证上传图片','POST','/api/v1/upload','{}','{}',NULL,'json','[]',30,0,'["upload", "P1"]',1,true,0,'2026-05-27 08:49:00','success','2026-05-17 13:38:00','2026-06-02 05:06:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO api_test_cases(id,collection_id,project_id,user_id,environment_id,name,description,method,url,headers,params,body,body_type,assertions,timeout,retry_count,tags,priority,is_enabled,sort_order,last_run_at,last_status,created_at,updated_at)VALUES(327,63,9,1,35,'推荐列表','验证推荐列表','GET','/api/v1/recommendations','{}','{}',NULL,'json','[]',30,0,'["recommendation", "P2"]',2,true,1,'2026-05-31 08:54:00','success','2026-04-17 04:17:00','2026-05-30 14:18:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO api_test_cases(id,collection_id,project_id,user_id,environment_id,name,description,method,url,headers,params,body,body_type,assertions,timeout,retry_count,tags,priority,is_enabled,sort_order,last_run_at,last_status,created_at,updated_at)VALUES(328,63,9,7,34,'健康检查','验证健康检查','GET','/api/v1/health','{}','{}',NULL,'json','[]',30,0,'["health", "P0"]',3,true,2,NULL,'pending','2026-01-03 22:01:00','2026-06-02 07:11:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO api_test_cases(id,collection_id,project_id,user_id,environment_id,name,description,method,url,headers,params,body,body_type,assertions,timeout,retry_count,tags,priority,is_enabled,sort_order,last_run_at,last_status,created_at,updated_at)VALUES(329,63,9,5,35,'更新资料','验证更新资料','PUT','/api/v1/users/me','{}','{}',NULL,'json','[]',30,0,'["user", "P1"]',2,true,3,'2026-05-21 07:12:00','success','2026-01-12 07:42:00','2026-05-30 05:53:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO api_test_cases(id,collection_id,project_id,user_id,environment_id,name,description,method,url,headers,params,body,body_type,assertions,timeout,retry_count,tags,priority,is_enabled,sort_order,last_run_at,last_status,created_at,updated_at)VALUES(330,63,9,5,35,'用户登录','验证用户登录','POST','/api/v1/auth/login','{}','{}',NULL,'json','[]',30,0,'["auth", "P0"]',2,true,4,'2026-05-26 11:47:00','success','2026-05-18 06:24:00','2026-06-01 18:14:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO api_test_cases(id,collection_id,project_id,user_id,environment_id,name,description,method,url,headers,params,body,body_type,assertions,timeout,retry_count,tags,priority,is_enabled,sort_order,last_run_at,last_status,created_at,updated_at)VALUES(331,63,9,7,35,'商品列表','验证商品列表','GET','/api/v1/products','{}','{}',NULL,'json','[]',30,0,'["product", "P0"]',2,true,5,'2026-05-23 01:27:00','success','2025-12-23 22:01:00','2026-05-31 14:24:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO api_test_cases(id,collection_id,project_id,user_id,environment_id,name,description,method,url,headers,params,body,body_type,assertions,timeout,retry_count,tags,priority,is_enabled,sort_order,last_run_at,last_status,created_at,updated_at)VALUES(332,64,10,5,38,'提交反馈','验证提交反馈','POST','/api/v1/feedback','{}','{}',NULL,'json','[]',30,0,'["feedback", "P2"]',1,true,0,'2026-06-01 19:20:00','success','2025-11-25 03:09:00','2026-05-29 20:58:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO api_test_cases(id,collection_id,project_id,user_id,environment_id,name,description,method,url,headers,params,body,body_type,assertions,timeout,retry_count,tags,priority,is_enabled,sort_order,last_run_at,last_status,created_at,updated_at)VALUES(333,64,10,5,39,'获取配置','验证获取配置','GET','/api/v1/config','{}','{}',NULL,'json','[]',30,0,'["config", "P2"]',1,true,1,'2026-05-27 09:20:00','success','2025-12-07 00:44:00','2026-06-02 00:41:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO api_test_cases(id,collection_id,project_id,user_id,environment_id,name,description,method,url,headers,params,body,body_type,assertions,timeout,retry_count,tags,priority,is_enabled,sort_order,last_run_at,last_status,created_at,updated_at)VALUES(334,64,10,7,39,'领取券','验证领取券','POST','/api/v1/coupons/1001','{}','{}',NULL,'json','[]',30,0,'["marketing", "P1"]',2,true,2,'2026-05-29 12:39:00','failed','2026-02-19 10:24:00','2026-06-02 04:48:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO api_test_cases(id,collection_id,project_id,user_id,environment_id,name,description,method,url,headers,params,body,body_type,assertions,timeout,retry_count,tags,priority,is_enabled,sort_order,last_run_at,last_status,created_at,updated_at)VALUES(335,64,10,5,39,'订单详情','验证订单详情','GET','/api/v1/orders/1001','{}','{}',NULL,'json','[]',30,0,'["order", "P0"]',2,true,3,NULL,'pending','2026-01-31 08:19:00','2026-05-31 18:51:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO api_test_cases(id,collection_id,project_id,user_id,environment_id,name,description,method,url,headers,params,body,body_type,assertions,timeout,retry_count,tags,priority,is_enabled,sort_order,last_run_at,last_status,created_at,updated_at)VALUES(336,64,10,6,39,'发起支付','验证发起支付','POST','/api/v1/payments','{}','{}',NULL,'json','[]',30,0,'["payment", "P0"]',2,true,4,'2026-05-19 10:57:00','success','2026-03-16 15:14:00','2026-05-30 16:26:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO api_test_cases(id,collection_id,project_id,user_id,environment_id,name,description,method,url,headers,params,body,body_type,assertions,timeout,retry_count,tags,priority,is_enabled,sort_order,last_run_at,last_status,created_at,updated_at)VALUES(337,64,10,1,38,'标记已读','验证标记已读','PUT','/api/v1/messages/1001','{}','{}',NULL,'json','[]',30,0,'["message", "P2"]',1,true,5,'2026-05-22 22:56:00','success','2026-03-22 09:39:00','2026-05-29 13:26:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO api_test_cases(id,collection_id,project_id,user_id,environment_id,name,description,method,url,headers,params,body,body_type,assertions,timeout,retry_count,tags,priority,is_enabled,sort_order,last_run_at,last_status,created_at,updated_at)VALUES(338,65,10,5,39,'领取券','验证领取券','POST','/api/v1/coupons/1001','{}','{}',NULL,'json','[]',30,0,'["marketing", "P1"]',2,true,0,'2026-05-24 20:55:00','failed','2026-04-01 22:32:00','2026-05-31 03:27:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO api_test_cases(id,collection_id,project_id,user_id,environment_id,name,description,method,url,headers,params,body,body_type,assertions,timeout,retry_count,tags,priority,is_enabled,sort_order,last_run_at,last_status,created_at,updated_at)VALUES(339,65,10,5,38,'搜索商品','验证搜索商品','GET','/api/v1/search','{}','{}',NULL,'json','[]',30,0,'["search", "P1"]',1,true,1,'2026-06-01 03:02:00','success','2026-02-07 17:59:00','2026-05-29 17:51:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO api_test_cases(id,collection_id,project_id,user_id,environment_id,name,description,method,url,headers,params,body,body_type,assertions,timeout,retry_count,tags,priority,is_enabled,sort_order,last_run_at,last_status,created_at,updated_at)VALUES(340,65,10,2,39,'订单详情','验证订单详情','GET','/api/v1/orders/1001','{}','{}',NULL,'json','[]',30,0,'["order", "P0"]',3,true,2,NULL,'pending','2026-01-18 00:11:00','2026-05-31 05:11:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO api_test_cases(id,collection_id,project_id,user_id,environment_id,name,description,method,url,headers,params,body,body_type,assertions,timeout,retry_count,tags,priority,is_enabled,sort_order,last_run_at,last_status,created_at,updated_at)VALUES(341,65,10,1,38,'商品列表','验证商品列表','GET','/api/v1/products','{}','{}',NULL,'json','[]',30,0,'["product", "P0"]',3,true,3,'2026-05-31 19:36:00','success','2026-01-19 07:00:00','2026-05-31 08:17:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO api_test_cases(id,collection_id,project_id,user_id,environment_id,name,description,method,url,headers,params,body,body_type,assertions,timeout,retry_count,tags,priority,is_enabled,sort_order,last_run_at,last_status,created_at,updated_at)VALUES(342,66,10,5,37,'更新资料','验证更新资料','PUT','/api/v1/users/me','{}','{}',NULL,'json','[]',30,0,'["user", "P1"]',1,true,0,'2026-05-23 13:03:00','success','2026-03-11 03:48:00','2026-05-31 01:26:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO api_test_cases(id,collection_id,project_id,user_id,environment_id,name,description,method,url,headers,params,body,body_type,assertions,timeout,retry_count,tags,priority,is_enabled,sort_order,last_run_at,last_status,created_at,updated_at)VALUES(343,66,10,5,40,'消息列表','验证消息列表','GET','/api/v1/messages','{}','{}',NULL,'json','[]',30,0,'["message", "P1"]',2,true,1,'2026-05-25 05:50:00','failed','2026-05-03 09:21:00','2026-06-02 03:26:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO api_test_cases(id,collection_id,project_id,user_id,environment_id,name,description,method,url,headers,params,body,body_type,assertions,timeout,retry_count,tags,priority,is_enabled,sort_order,last_run_at,last_status,created_at,updated_at)VALUES(344,66,10,5,39,'上传图片','验证上传图片','POST','/api/v1/upload','{}','{}',NULL,'json','[]',30,0,'["upload", "P1"]',1,true,2,'2026-05-23 15:45:00','success','2026-05-14 00:21:00','2026-05-30 16:32:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO api_test_cases(id,collection_id,project_id,user_id,environment_id,name,description,method,url,headers,params,body,body_type,assertions,timeout,retry_count,tags,priority,is_enabled,sort_order,last_run_at,last_status,created_at,updated_at)VALUES(345,66,10,1,38,'用户信息','验证用户信息','GET','/api/v1/users/me','{}','{}',NULL,'json','[]',30,0,'["user", "P0"]',1,true,3,'2026-06-01 06:36:00','success','2026-05-09 20:35:00','2026-05-31 11:22:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO api_test_cases(id,collection_id,project_id,user_id,environment_id,name,description,method,url,headers,params,body,body_type,assertions,timeout,retry_count,tags,priority,is_enabled,sort_order,last_run_at,last_status,created_at,updated_at)VALUES(346,66,10,7,40,'商品列表','验证商品列表','GET','/api/v1/products','{}','{}',NULL,'json','[]',30,0,'["product", "P0"]',1,true,4,'2026-05-23 23:08:00','success','2025-11-30 12:09:00','2026-06-01 19:24:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO api_test_cases(id,collection_id,project_id,user_id,environment_id,name,description,method,url,headers,params,body,body_type,assertions,timeout,retry_count,tags,priority,is_enabled,sort_order,last_run_at,last_status,created_at,updated_at)VALUES(347,66,10,2,37,'支付状态','验证支付状态','GET','/api/v1/payments/1001','{}','{}',NULL,'json','[]',30,0,'["payment", "P1"]',2,true,5,'2026-05-19 06:31:00','failed','2025-12-07 13:15:00','2026-05-29 18:46:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO api_test_cases(id,collection_id,project_id,user_id,environment_id,name,description,method,url,headers,params,body,body_type,assertions,timeout,retry_count,tags,priority,is_enabled,sort_order,last_run_at,last_status,created_at,updated_at)VALUES(348,66,10,2,38,'搜索商品','验证搜索商品','GET','/api/v1/search','{}','{}',NULL,'json','[]',30,0,'["search", "P1"]',1,true,6,'2026-05-24 22:35:00','running','2025-12-03 12:39:00','2026-05-30 19:29:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO api_test_cases(id,collection_id,project_id,user_id,environment_id,name,description,method,url,headers,params,body,body_type,assertions,timeout,retry_count,tags,priority,is_enabled,sort_order,last_run_at,last_status,created_at,updated_at)VALUES(349,67,10,5,40,'更新资料','验证更新资料','PUT','/api/v1/users/me','{}','{}',NULL,'json','[]',30,0,'["user", "P1"]',2,true,0,'2026-05-28 00:11:00','success','2025-12-28 15:52:00','2026-06-01 21:08:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO api_test_cases(id,collection_id,project_id,user_id,environment_id,name,description,method,url,headers,params,body,body_type,assertions,timeout,retry_count,tags,priority,is_enabled,sort_order,last_run_at,last_status,created_at,updated_at)VALUES(350,67,10,1,39,'获取配置','验证获取配置','GET','/api/v1/config','{}','{}',NULL,'json','[]',30,0,'["config", "P2"]',2,true,1,'2026-05-31 00:26:00','success','2026-02-18 15:34:00','2026-05-31 14:45:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO api_test_cases(id,collection_id,project_id,user_id,environment_id,name,description,method,url,headers,params,body,body_type,assertions,timeout,retry_count,tags,priority,is_enabled,sort_order,last_run_at,last_status,created_at,updated_at)VALUES(351,67,10,7,38,'商品列表','验证商品列表','GET','/api/v1/products','{}','{}',NULL,'json','[]',30,0,'["product", "P0"]',1,true,2,'2026-05-21 07:39:00','cancelled','2025-11-04 11:23:00','2026-05-29 20:24:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO api_test_cases(id,collection_id,project_id,user_id,environment_id,name,description,method,url,headers,params,body,body_type,assertions,timeout,retry_count,tags,priority,is_enabled,sort_order,last_run_at,last_status,created_at,updated_at)VALUES(352,68,10,1,40,'优惠券','验证优惠券','GET','/api/v1/coupons','{}','{}',NULL,'json','[]',30,0,'["marketing", "P1"]',2,true,0,'2026-05-29 19:49:00','success','2026-02-18 07:22:00','2026-06-01 12:08:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO api_test_cases(id,collection_id,project_id,user_id,environment_id,name,description,method,url,headers,params,body,body_type,assertions,timeout,retry_count,tags,priority,is_enabled,sort_order,last_run_at,last_status,created_at,updated_at)VALUES(353,68,10,7,40,'发起支付','验证发起支付','POST','/api/v1/payments','{}','{}',NULL,'json','[]',30,0,'["payment", "P0"]',1,true,1,'2026-06-01 07:47:00','success','2026-01-03 13:09:00','2026-06-02 05:18:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO api_test_cases(id,collection_id,project_id,user_id,environment_id,name,description,method,url,headers,params,body,body_type,assertions,timeout,retry_count,tags,priority,is_enabled,sort_order,last_run_at,last_status,created_at,updated_at)VALUES(354,68,10,2,40,'订单详情','验证订单详情','GET','/api/v1/orders/1001','{}','{}',NULL,'json','[]',30,0,'["order", "P0"]',2,true,2,'2026-05-20 14:24:00','success','2026-04-12 03:17:00','2026-05-31 00:24:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO api_test_cases(id,collection_id,project_id,user_id,environment_id,name,description,method,url,headers,params,body,body_type,assertions,timeout,retry_count,tags,priority,is_enabled,sort_order,last_run_at,last_status,created_at,updated_at)VALUES(355,68,10,5,40,'更新资料','验证更新资料','PUT','/api/v1/users/me','{}','{}',NULL,'json','[]',30,0,'["user", "P1"]',1,true,3,'2026-05-22 07:23:00','failed','2025-12-26 17:35:00','2026-06-01 00:57:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO api_test_cases(id,collection_id,project_id,user_id,environment_id,name,description,method,url,headers,params,body,body_type,assertions,timeout,retry_count,tags,priority,is_enabled,sort_order,last_run_at,last_status,created_at,updated_at)VALUES(356,68,10,5,37,'获取配置','验证获取配置','GET','/api/v1/config','{}','{}',NULL,'json','[]',30,0,'["config", "P2"]',2,true,4,'2026-05-22 06:05:00','success','2026-05-25 02:33:00','2026-05-29 13:40:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO api_test_cases(id,collection_id,project_id,user_id,environment_id,name,description,method,url,headers,params,body,body_type,assertions,timeout,retry_count,tags,priority,is_enabled,sort_order,last_run_at,last_status,created_at,updated_at)VALUES(357,69,10,2,38,'搜索商品','验证搜索商品','GET','/api/v1/search','{}','{}',NULL,'json','[]',30,0,'["search", "P1"]',2,true,0,'2026-05-21 20:51:00','success','2025-12-12 05:52:00','2026-06-02 07:19:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO api_test_cases(id,collection_id,project_id,user_id,environment_id,name,description,method,url,headers,params,body,body_type,assertions,timeout,retry_count,tags,priority,is_enabled,sort_order,last_run_at,last_status,created_at,updated_at)VALUES(358,69,10,1,38,'健康检查','验证健康检查','GET','/api/v1/health','{}','{}',NULL,'json','[]',30,0,'["health", "P0"]',1,true,1,'2026-05-17 12:33:00','failed','2026-05-11 05:19:00','2026-05-29 19:03:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO api_test_cases(id,collection_id,project_id,user_id,environment_id,name,description,method,url,headers,params,body,body_type,assertions,timeout,retry_count,tags,priority,is_enabled,sort_order,last_run_at,last_status,created_at,updated_at)VALUES(359,69,10,7,40,'领取券','验证领取券','POST','/api/v1/coupons/1001','{}','{}',NULL,'json','[]',30,0,'["marketing", "P1"]',2,true,2,'2026-05-18 17:33:00','success','2025-11-03 19:36:00','2026-05-31 02:49:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO api_test_cases(id,collection_id,project_id,user_id,environment_id,name,description,method,url,headers,params,body,body_type,assertions,timeout,retry_count,tags,priority,is_enabled,sort_order,last_run_at,last_status,created_at,updated_at)VALUES(360,69,10,6,37,'推荐列表','验证推荐列表','GET','/api/v1/recommendations','{}','{}',NULL,'json','[]',30,0,'["recommendation", "P2"]',2,true,3,'2026-05-25 11:28:00','success','2026-02-15 16:24:00','2026-05-31 08:58:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO api_test_cases(id,collection_id,project_id,user_id,environment_id,name,description,method,url,headers,params,body,body_type,assertions,timeout,retry_count,tags,priority,is_enabled,sort_order,last_run_at,last_status,created_at,updated_at)VALUES(361,69,10,7,40,'取消订单','验证取消订单','POST','/api/v1/orders/1001/cancel','{}','{}',NULL,'json','[]',30,0,'["order", "P1"]',3,true,4,'2026-05-29 15:30:00','failed','2026-05-12 05:14:00','2026-05-30 19:27:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO api_test_cases(id,collection_id,project_id,user_id,environment_id,name,description,method,url,headers,params,body,body_type,assertions,timeout,retry_count,tags,priority,is_enabled,sort_order,last_run_at,last_status,created_at,updated_at)VALUES(362,69,10,1,37,'消息列表','验证消息列表','GET','/api/v1/messages','{}','{}',NULL,'json','[]',30,0,'["message", "P1"]',2,true,5,'2026-05-30 12:20:00','success','2025-11-08 15:41:00','2026-06-01 23:26:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO api_test_cases(id,collection_id,project_id,user_id,environment_id,name,description,method,url,headers,params,body,body_type,assertions,timeout,retry_count,tags,priority,is_enabled,sort_order,last_run_at,last_status,created_at,updated_at)VALUES(363,69,10,1,40,'更新资料','验证更新资料','PUT','/api/v1/users/me','{}','{}',NULL,'json','[]',30,0,'["user", "P1"]',2,true,6,'2026-05-17 15:14:00','success','2026-02-13 22:09:00','2026-05-31 00:50:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO api_test_cases(id,collection_id,project_id,user_id,environment_id,name,description,method,url,headers,params,body,body_type,assertions,timeout,retry_count,tags,priority,is_enabled,sort_order,last_run_at,last_status,created_at,updated_at)VALUES(364,69,10,1,39,'发起支付','验证发起支付','POST','/api/v1/payments','{}','{}',NULL,'json','[]',30,0,'["payment", "P0"]',2,true,7,'2026-05-25 08:20:00','failed','2026-01-04 04:24:00','2026-06-01 12:42:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO api_test_cases(id,collection_id,project_id,user_id,environment_id,name,description,method,url,headers,params,body,body_type,assertions,timeout,retry_count,tags,priority,is_enabled,sort_order,last_run_at,last_status,created_at,updated_at)VALUES(365,70,10,5,39,'健康检查','验证健康检查','GET','/api/v1/health','{}','{}',NULL,'json','[]',30,0,'["health", "P0"]',2,true,0,'2026-05-25 01:06:00','success','2026-05-28 10:53:00','2026-05-31 15:13:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO api_test_cases(id,collection_id,project_id,user_id,environment_id,name,description,method,url,headers,params,body,body_type,assertions,timeout,retry_count,tags,priority,is_enabled,sort_order,last_run_at,last_status,created_at,updated_at)VALUES(366,70,10,2,40,'用户登录','验证用户登录','POST','/api/v1/auth/login','{}','{}',NULL,'json','[]',30,0,'["auth", "P0"]',3,true,1,'2026-05-28 01:10:00','success','2026-04-01 18:49:00','2026-06-01 23:55:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO api_test_cases(id,collection_id,project_id,user_id,environment_id,name,description,method,url,headers,params,body,body_type,assertions,timeout,retry_count,tags,priority,is_enabled,sort_order,last_run_at,last_status,created_at,updated_at)VALUES(367,70,10,2,38,'申请退款','验证申请退款','POST','/api/v1/refunds','{}','{}',NULL,'json','[]',30,0,'["payment", "P1"]',3,true,2,'2026-05-19 21:45:00','failed','2026-02-08 10:20:00','2026-06-01 03:24:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO api_test_cases(id,collection_id,project_id,user_id,environment_id,name,description,method,url,headers,params,body,body_type,assertions,timeout,retry_count,tags,priority,is_enabled,sort_order,last_run_at,last_status,created_at,updated_at)VALUES(368,70,10,5,37,'获取配置','验证获取配置','GET','/api/v1/config','{}','{}',NULL,'json','[]',30,0,'["config", "P2"]',2,true,3,'2026-05-30 08:50:00','success','2026-02-18 18:41:00','2026-05-29 10:12:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO api_test_cases(id,collection_id,project_id,user_id,environment_id,name,description,method,url,headers,params,body,body_type,assertions,timeout,retry_count,tags,priority,is_enabled,sort_order,last_run_at,last_status,created_at,updated_at)VALUES(369,70,10,7,38,'更新资料','验证更新资料','PUT','/api/v1/users/me','{}','{}',NULL,'json','[]',30,0,'["user", "P1"]',1,true,4,'2026-05-20 18:44:00','success','2026-01-16 21:00:00','2026-05-30 19:36:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO api_test_cases(id,collection_id,project_id,user_id,environment_id,name,description,method,url,headers,params,body,body_type,assertions,timeout,retry_count,tags,priority,is_enabled,sort_order,last_run_at,last_status,created_at,updated_at)VALUES(370,70,10,5,37,'提交反馈','验证提交反馈','POST','/api/v1/feedback','{}','{}',NULL,'json','[]',30,0,'["feedback", "P2"]',3,true,5,'2026-05-21 20:21:00','success','2026-03-23 23:43:00','2026-05-31 06:44:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO api_test_cases(id,collection_id,project_id,user_id,environment_id,name,description,method,url,headers,params,body,body_type,assertions,timeout,retry_count,tags,priority,is_enabled,sort_order,last_run_at,last_status,created_at,updated_at)VALUES(371,70,10,7,40,'支付状态','验证支付状态','GET','/api/v1/payments/1001','{}','{}',NULL,'json','[]',30,0,'["payment", "P1"]',2,true,6,'2026-05-25 10:17:00','success','2025-11-16 03:27:00','2026-05-30 12:16:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO api_test_cases(id,collection_id,project_id,user_id,environment_id,name,description,method,url,headers,params,body,body_type,assertions,timeout,retry_count,tags,priority,is_enabled,sort_order,last_run_at,last_status,created_at,updated_at)VALUES(372,70,10,2,39,'用户信息','验证用户信息','GET','/api/v1/users/me','{}','{}',NULL,'json','[]',30,0,'["user", "P0"]',2,true,7,'2026-06-02 08:00:00','success','2026-05-06 17:54:00','2026-05-29 22:46:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO api_test_cases(id,collection_id,project_id,user_id,environment_id,name,description,method,url,headers,params,body,body_type,assertions,timeout,retry_count,tags,priority,is_enabled,sort_order,last_run_at,last_status,created_at,updated_at)VALUES(373,71,11,7,42,'申请退款','验证申请退款','POST','/api/v1/refunds','{}','{}',NULL,'json','[]',30,0,'["payment", "P1"]',3,true,0,NULL,'pending','2026-04-30 11:53:00','2026-06-01 14:52:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO api_test_cases(id,collection_id,project_id,user_id,environment_id,name,description,method,url,headers,params,body,body_type,assertions,timeout,retry_count,tags,priority,is_enabled,sort_order,last_run_at,last_status,created_at,updated_at)VALUES(374,71,11,6,42,'支付状态','验证支付状态','GET','/api/v1/payments/1001','{}','{}',NULL,'json','[]',30,0,'["payment", "P1"]',2,true,1,'2026-05-28 01:42:00','running','2025-12-14 07:20:00','2026-05-30 01:11:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO api_test_cases(id,collection_id,project_id,user_id,environment_id,name,description,method,url,headers,params,body,body_type,assertions,timeout,retry_count,tags,priority,is_enabled,sort_order,last_run_at,last_status,created_at,updated_at)VALUES(375,71,11,6,43,'取消订单','验证取消订单','POST','/api/v1/orders/1001/cancel','{}','{}',NULL,'json','[]',30,0,'["order", "P1"]',1,true,2,'2026-05-31 01:11:00','success','2026-02-23 21:39:00','2026-06-02 01:08:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO api_test_cases(id,collection_id,project_id,user_id,environment_id,name,description,method,url,headers,params,body,body_type,assertions,timeout,retry_count,tags,priority,is_enabled,sort_order,last_run_at,last_status,created_at,updated_at)VALUES(376,71,11,5,42,'用户信息','验证用户信息','GET','/api/v1/users/me','{}','{}',NULL,'json','[]',30,0,'["user", "P0"]',2,true,3,'2026-05-18 03:21:00','success','2026-04-16 13:29:00','2026-06-02 05:26:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO api_test_cases(id,collection_id,project_id,user_id,environment_id,name,description,method,url,headers,params,body,body_type,assertions,timeout,retry_count,tags,priority,is_enabled,sort_order,last_run_at,last_status,created_at,updated_at)VALUES(377,71,11,6,42,'用户登录','验证用户登录','POST','/api/v1/auth/login','{}','{}',NULL,'json','[]',30,0,'["auth", "P0"]',2,true,4,'2026-05-29 19:15:00','success','2026-05-06 08:56:00','2026-06-01 15:14:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO api_test_cases(id,collection_id,project_id,user_id,environment_id,name,description,method,url,headers,params,body,body_type,assertions,timeout,retry_count,tags,priority,is_enabled,sort_order,last_run_at,last_status,created_at,updated_at)VALUES(378,71,11,5,44,'健康检查','验证健康检查','GET','/api/v1/health','{}','{}',NULL,'json','[]',30,0,'["health", "P0"]',3,true,5,'2026-05-18 05:19:00','success','2026-06-01 08:18:00','2026-05-30 01:51:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO api_test_cases(id,collection_id,project_id,user_id,environment_id,name,description,method,url,headers,params,body,body_type,assertions,timeout,retry_count,tags,priority,is_enabled,sort_order,last_run_at,last_status,created_at,updated_at)VALUES(379,71,11,5,44,'提交反馈','验证提交反馈','POST','/api/v1/feedback','{}','{}',NULL,'json','[]',30,0,'["feedback", "P2"]',2,true,6,'2026-05-17 18:33:00','success','2025-11-27 07:26:00','2026-06-01 09:36:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO api_test_cases(id,collection_id,project_id,user_id,environment_id,name,description,method,url,headers,params,body,body_type,assertions,timeout,retry_count,tags,priority,is_enabled,sort_order,last_run_at,last_status,created_at,updated_at)VALUES(380,71,11,6,41,'获取配置','验证获取配置','GET','/api/v1/config','{}','{}',NULL,'json','[]',30,0,'["config", "P2"]',2,true,7,'2026-05-21 23:17:00','success','2026-02-19 08:20:00','2026-06-01 22:26:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO api_test_cases(id,collection_id,project_id,user_id,environment_id,name,description,method,url,headers,params,body,body_type,assertions,timeout,retry_count,tags,priority,is_enabled,sort_order,last_run_at,last_status,created_at,updated_at)VALUES(381,72,11,7,41,'更新资料','验证更新资料','PUT','/api/v1/users/me','{}','{}',NULL,'json','[]',30,0,'["user", "P1"]',3,true,0,NULL,'pending','2026-04-14 00:16:00','2026-05-30 06:20:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO api_test_cases(id,collection_id,project_id,user_id,environment_id,name,description,method,url,headers,params,body,body_type,assertions,timeout,retry_count,tags,priority,is_enabled,sort_order,last_run_at,last_status,created_at,updated_at)VALUES(382,72,11,5,44,'上传图片','验证上传图片','POST','/api/v1/upload','{}','{}',NULL,'json','[]',30,0,'["upload", "P1"]',1,true,1,'2026-05-18 10:48:00','success','2026-05-23 03:59:00','2026-05-31 18:36:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO api_test_cases(id,collection_id,project_id,user_id,environment_id,name,description,method,url,headers,params,body,body_type,assertions,timeout,retry_count,tags,priority,is_enabled,sort_order,last_run_at,last_status,created_at,updated_at)VALUES(383,72,11,1,43,'申请退款','验证申请退款','POST','/api/v1/refunds','{}','{}',NULL,'json','[]',30,0,'["payment", "P1"]',2,true,2,'2026-05-19 09:58:00','success','2026-05-17 23:10:00','2026-06-01 21:53:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO api_test_cases(id,collection_id,project_id,user_id,environment_id,name,description,method,url,headers,params,body,body_type,assertions,timeout,retry_count,tags,priority,is_enabled,sort_order,last_run_at,last_status,created_at,updated_at)VALUES(384,72,11,2,44,'取消订单','验证取消订单','POST','/api/v1/orders/1001/cancel','{}','{}',NULL,'json','[]',30,0,'["order", "P1"]',2,true,3,NULL,'pending','2026-04-23 10:23:00','2026-06-01 07:58:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO api_test_cases(id,collection_id,project_id,user_id,environment_id,name,description,method,url,headers,params,body,body_type,assertions,timeout,retry_count,tags,priority,is_enabled,sort_order,last_run_at,last_status,created_at,updated_at)VALUES(385,72,11,2,44,'订单详情','验证订单详情','GET','/api/v1/orders/1001','{}','{}',NULL,'json','[]',30,0,'["order", "P0"]',1,true,4,'2026-05-17 14:58:00','failed','2025-12-03 13:52:00','2026-06-02 04:20:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO api_test_cases(id,collection_id,project_id,user_id,environment_id,name,description,method,url,headers,params,body,body_type,assertions,timeout,retry_count,tags,priority,is_enabled,sort_order,last_run_at,last_status,created_at,updated_at)VALUES(386,73,11,7,42,'申请退款','验证申请退款','POST','/api/v1/refunds','{}','{}',NULL,'json','[]',30,0,'["payment", "P1"]',2,true,0,'2026-05-31 06:53:00','failed','2025-12-30 14:46:00','2026-06-02 03:33:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO api_test_cases(id,collection_id,project_id,user_id,environment_id,name,description,method,url,headers,params,body,body_type,assertions,timeout,retry_count,tags,priority,is_enabled,sort_order,last_run_at,last_status,created_at,updated_at)VALUES(387,73,11,5,44,'商品列表','验证商品列表','GET','/api/v1/products','{}','{}',NULL,'json','[]',30,0,'["product", "P0"]',1,true,1,'2026-05-28 23:07:00','success','2025-11-18 08:23:00','2026-05-31 23:56:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO api_test_cases(id,collection_id,project_id,user_id,environment_id,name,description,method,url,headers,params,body,body_type,assertions,timeout,retry_count,tags,priority,is_enabled,sort_order,last_run_at,last_status,created_at,updated_at)VALUES(388,73,11,1,43,'上传图片','验证上传图片','POST','/api/v1/upload','{}','{}',NULL,'json','[]',30,0,'["upload", "P1"]',2,true,2,'2026-05-20 04:16:00','success','2026-01-11 04:32:00','2026-05-31 15:58:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO api_test_cases(id,collection_id,project_id,user_id,environment_id,name,description,method,url,headers,params,body,body_type,assertions,timeout,retry_count,tags,priority,is_enabled,sort_order,last_run_at,last_status,created_at,updated_at)VALUES(389,74,11,6,41,'商品列表','验证商品列表','GET','/api/v1/products','{}','{}',NULL,'json','[]',30,0,'["product", "P0"]',3,true,0,'2026-05-28 07:15:00','success','2026-01-01 00:34:00','2026-05-29 11:52:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO api_test_cases(id,collection_id,project_id,user_id,environment_id,name,description,method,url,headers,params,body,body_type,assertions,timeout,retry_count,tags,priority,is_enabled,sort_order,last_run_at,last_status,created_at,updated_at)VALUES(390,74,11,2,42,'搜索商品','验证搜索商品','GET','/api/v1/search','{}','{}',NULL,'json','[]',30,0,'["search", "P1"]',1,true,1,'2026-05-18 20:45:00','success','2025-12-26 11:58:00','2026-05-31 11:29:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO api_test_cases(id,collection_id,project_id,user_id,environment_id,name,description,method,url,headers,params,body,body_type,assertions,timeout,retry_count,tags,priority,is_enabled,sort_order,last_run_at,last_status,created_at,updated_at)VALUES(391,74,11,7,41,'订单详情','验证订单详情','GET','/api/v1/orders/1001','{}','{}',NULL,'json','[]',30,0,'["order", "P0"]',1,true,2,'2026-05-23 22:34:00','success','2026-01-10 02:48:00','2026-06-01 17:54:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO api_test_cases(id,collection_id,project_id,user_id,environment_id,name,description,method,url,headers,params,body,body_type,assertions,timeout,retry_count,tags,priority,is_enabled,sort_order,last_run_at,last_status,created_at,updated_at)VALUES(392,74,11,7,43,'用户登录','验证用户登录','POST','/api/v1/auth/login','{}','{}',NULL,'json','[]',30,0,'["auth", "P0"]',3,true,3,'2026-05-25 19:11:00','running','2025-12-15 03:43:00','2026-06-02 03:53:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO api_test_cases(id,collection_id,project_id,user_id,environment_id,name,description,method,url,headers,params,body,body_type,assertions,timeout,retry_count,tags,priority,is_enabled,sort_order,last_run_at,last_status,created_at,updated_at)VALUES(393,75,11,1,41,'获取配置','验证获取配置','GET','/api/v1/config','{}','{}',NULL,'json','[]',30,0,'["config", "P2"]',2,true,0,'2026-05-24 03:33:00','success','2026-03-07 14:09:00','2026-05-30 08:54:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO api_test_cases(id,collection_id,project_id,user_id,environment_id,name,description,method,url,headers,params,body,body_type,assertions,timeout,retry_count,tags,priority,is_enabled,sort_order,last_run_at,last_status,created_at,updated_at)VALUES(394,75,11,1,42,'健康检查','验证健康检查','GET','/api/v1/health','{}','{}',NULL,'json','[]',30,0,'["health", "P0"]',1,true,1,'2026-06-01 18:28:00','success','2026-05-14 02:14:00','2026-05-29 15:23:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO api_test_cases(id,collection_id,project_id,user_id,environment_id,name,description,method,url,headers,params,body,body_type,assertions,timeout,retry_count,tags,priority,is_enabled,sort_order,last_run_at,last_status,created_at,updated_at)VALUES(395,75,11,5,44,'订单详情','验证订单详情','GET','/api/v1/orders/1001','{}','{}',NULL,'json','[]',30,0,'["order", "P0"]',1,true,2,'2026-05-23 02:11:00','success','2026-03-10 02:54:00','2026-05-31 10:34:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO api_test_cases(id,collection_id,project_id,user_id,environment_id,name,description,method,url,headers,params,body,body_type,assertions,timeout,retry_count,tags,priority,is_enabled,sort_order,last_run_at,last_status,created_at,updated_at)VALUES(396,75,11,2,44,'优惠券','验证优惠券','GET','/api/v1/coupons','{}','{}',NULL,'json','[]',30,0,'["marketing", "P1"]',2,true,3,'2026-05-30 18:23:00','running','2026-05-18 20:51:00','2026-05-31 14:31:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO api_test_cases(id,collection_id,project_id,user_id,environment_id,name,description,method,url,headers,params,body,body_type,assertions,timeout,retry_count,tags,priority,is_enabled,sort_order,last_run_at,last_status,created_at,updated_at)VALUES(397,76,11,2,43,'搜索商品','验证搜索商品','GET','/api/v1/search','{}','{}',NULL,'json','[]',30,0,'["search", "P1"]',1,true,0,'2026-05-26 23:52:00','cancelled','2025-12-05 15:57:00','2026-05-31 05:53:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO api_test_cases(id,collection_id,project_id,user_id,environment_id,name,description,method,url,headers,params,body,body_type,assertions,timeout,retry_count,tags,priority,is_enabled,sort_order,last_run_at,last_status,created_at,updated_at)VALUES(398,76,11,6,44,'标记已读','验证标记已读','PUT','/api/v1/messages/1001','{}','{}',NULL,'json','[]',30,0,'["message", "P2"]',2,true,1,'2026-05-23 02:04:00','success','2025-12-29 04:10:00','2026-05-31 15:25:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO api_test_cases(id,collection_id,project_id,user_id,environment_id,name,description,method,url,headers,params,body,body_type,assertions,timeout,retry_count,tags,priority,is_enabled,sort_order,last_run_at,last_status,created_at,updated_at)VALUES(399,76,11,2,41,'创建订单','验证创建订单','POST','/api/v1/orders','{}','{}',NULL,'json','[]',30,0,'["order", "P0"]',2,true,2,'2026-05-18 03:23:00','success','2026-02-03 02:00:00','2026-05-29 10:05:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO api_test_cases(id,collection_id,project_id,user_id,environment_id,name,description,method,url,headers,params,body,body_type,assertions,timeout,retry_count,tags,priority,is_enabled,sort_order,last_run_at,last_status,created_at,updated_at)VALUES(400,76,11,2,42,'上传图片','验证上传图片','POST','/api/v1/upload','{}','{}',NULL,'json','[]',30,0,'["upload", "P1"]',2,true,3,'2026-05-25 15:51:00','success','2026-05-30 20:58:00','2026-06-01 18:14:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO api_test_cases(id,collection_id,project_id,user_id,environment_id,name,description,method,url,headers,params,body,body_type,assertions,timeout,retry_count,tags,priority,is_enabled,sort_order,last_run_at,last_status,created_at,updated_at)VALUES(401,77,11,1,44,'用户信息','验证用户信息','GET','/api/v1/users/me','{}','{}',NULL,'json','[]',30,0,'["user", "P0"]',1,true,0,'2026-05-30 16:12:00','success','2025-12-05 10:34:00','2026-06-01 05:38:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO api_test_cases(id,collection_id,project_id,user_id,environment_id,name,description,method,url,headers,params,body,body_type,assertions,timeout,retry_count,tags,priority,is_enabled,sort_order,last_run_at,last_status,created_at,updated_at)VALUES(402,77,11,5,42,'推荐列表','验证推荐列表','GET','/api/v1/recommendations','{}','{}',NULL,'json','[]',30,0,'["recommendation", "P2"]',3,true,1,'2026-05-31 09:30:00','success','2026-03-15 04:15:00','2026-05-29 15:13:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO api_test_cases(id,collection_id,project_id,user_id,environment_id,name,description,method,url,headers,params,body,body_type,assertions,timeout,retry_count,tags,priority,is_enabled,sort_order,last_run_at,last_status,created_at,updated_at)VALUES(403,77,11,7,41,'提交反馈','验证提交反馈','POST','/api/v1/feedback','{}','{}',NULL,'json','[]',30,0,'["feedback", "P2"]',3,true,2,'2026-05-19 05:05:00','cancelled','2026-02-18 04:10:00','2026-05-30 13:31:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO api_test_cases(id,collection_id,project_id,user_id,environment_id,name,description,method,url,headers,params,body,body_type,assertions,timeout,retry_count,tags,priority,is_enabled,sort_order,last_run_at,last_status,created_at,updated_at)VALUES(404,77,11,1,41,'搜索商品','验证搜索商品','GET','/api/v1/search','{}','{}',NULL,'json','[]',30,0,'["search", "P1"]',2,true,3,'2026-05-22 17:58:00','success','2026-02-12 01:16:00','2026-05-31 12:55:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO api_test_cases(id,collection_id,project_id,user_id,environment_id,name,description,method,url,headers,params,body,body_type,assertions,timeout,retry_count,tags,priority,is_enabled,sort_order,last_run_at,last_status,created_at,updated_at)VALUES(405,77,11,7,43,'获取配置','验证获取配置','GET','/api/v1/config','{}','{}',NULL,'json','[]',30,0,'["config", "P2"]',3,true,4,'2026-05-31 17:02:00','failed','2026-02-28 08:53:00','2026-05-29 22:31:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO api_test_cases(id,collection_id,project_id,user_id,environment_id,name,description,method,url,headers,params,body,body_type,assertions,timeout,retry_count,tags,priority,is_enabled,sort_order,last_run_at,last_status,created_at,updated_at)VALUES(406,77,11,7,41,'优惠券','验证优惠券','GET','/api/v1/coupons','{}','{}',NULL,'json','[]',30,0,'["marketing", "P1"]',3,true,5,'2026-05-27 13:25:00','success','2026-05-14 16:15:00','2026-06-01 05:39:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO api_test_cases(id,collection_id,project_id,user_id,environment_id,name,description,method,url,headers,params,body,body_type,assertions,timeout,retry_count,tags,priority,is_enabled,sort_order,last_run_at,last_status,created_at,updated_at)VALUES(407,77,11,2,41,'上传图片','验证上传图片','POST','/api/v1/upload','{}','{}',NULL,'json','[]',30,0,'["upload", "P1"]',1,true,6,'2026-05-26 10:12:00','success','2026-03-10 22:03:00','2026-05-30 17:17:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO api_test_cases(id,collection_id,project_id,user_id,environment_id,name,description,method,url,headers,params,body,body_type,assertions,timeout,retry_count,tags,priority,is_enabled,sort_order,last_run_at,last_status,created_at,updated_at)VALUES(408,78,12,6,45,'支付状态','验证支付状态','GET','/api/v1/payments/1001','{}','{}',NULL,'json','[]',30,0,'["payment", "P1"]',2,true,0,'2026-05-23 19:21:00','success','2025-11-08 12:16:00','2026-06-02 03:03:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO api_test_cases(id,collection_id,project_id,user_id,environment_id,name,description,method,url,headers,params,body,body_type,assertions,timeout,retry_count,tags,priority,is_enabled,sort_order,last_run_at,last_status,created_at,updated_at)VALUES(409,78,12,6,45,'用户信息','验证用户信息','GET','/api/v1/users/me','{}','{}',NULL,'json','[]',30,0,'["user", "P0"]',1,true,1,'2026-05-28 00:56:00','success','2026-04-20 01:53:00','2026-05-31 18:51:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO api_test_cases(id,collection_id,project_id,user_id,environment_id,name,description,method,url,headers,params,body,body_type,assertions,timeout,retry_count,tags,priority,is_enabled,sort_order,last_run_at,last_status,created_at,updated_at)VALUES(410,78,12,2,45,'更新资料','验证更新资料','PUT','/api/v1/users/me','{}','{}',NULL,'json','[]',30,0,'["user", "P1"]',2,true,2,'2026-05-28 18:38:00','success','2026-02-07 10:19:00','2026-06-02 00:48:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO api_test_cases(id,collection_id,project_id,user_id,environment_id,name,description,method,url,headers,params,body,body_type,assertions,timeout,retry_count,tags,priority,is_enabled,sort_order,last_run_at,last_status,created_at,updated_at)VALUES(411,78,12,1,45,'标记已读','验证标记已读','PUT','/api/v1/messages/1001','{}','{}',NULL,'json','[]',30,0,'["message", "P2"]',2,true,3,'2026-05-25 17:19:00','running','2026-02-15 15:39:00','2026-05-30 18:23:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO api_test_cases(id,collection_id,project_id,user_id,environment_id,name,description,method,url,headers,params,body,body_type,assertions,timeout,retry_count,tags,priority,is_enabled,sort_order,last_run_at,last_status,created_at,updated_at)VALUES(412,78,12,7,48,'提交反馈','验证提交反馈','POST','/api/v1/feedback','{}','{}',NULL,'json','[]',30,0,'["feedback", "P2"]',2,true,4,'2026-05-29 00:50:00','success','2026-04-03 18:37:00','2026-05-31 08:51:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO api_test_cases(id,collection_id,project_id,user_id,environment_id,name,description,method,url,headers,params,body,body_type,assertions,timeout,retry_count,tags,priority,is_enabled,sort_order,last_run_at,last_status,created_at,updated_at)VALUES(413,78,12,5,47,'发起支付','验证发起支付','POST','/api/v1/payments','{}','{}',NULL,'json','[]',30,0,'["payment", "P0"]',1,true,5,'2026-05-27 14:01:00','success','2025-11-30 16:42:00','2026-06-01 04:07:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO api_test_cases(id,collection_id,project_id,user_id,environment_id,name,description,method,url,headers,params,body,body_type,assertions,timeout,retry_count,tags,priority,is_enabled,sort_order,last_run_at,last_status,created_at,updated_at)VALUES(414,79,12,6,47,'创建订单','验证创建订单','POST','/api/v1/orders','{}','{}',NULL,'json','[]',30,0,'["order", "P0"]',1,true,0,'2026-05-26 16:15:00','success','2025-12-12 23:38:00','2026-05-31 22:32:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO api_test_cases(id,collection_id,project_id,user_id,environment_id,name,description,method,url,headers,params,body,body_type,assertions,timeout,retry_count,tags,priority,is_enabled,sort_order,last_run_at,last_status,created_at,updated_at)VALUES(415,79,12,7,46,'订单详情','验证订单详情','GET','/api/v1/orders/1001','{}','{}',NULL,'json','[]',30,0,'["order", "P0"]',2,true,1,'2026-05-30 09:35:00','success','2025-11-17 05:31:00','2026-05-31 06:00:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO api_test_cases(id,collection_id,project_id,user_id,environment_id,name,description,method,url,headers,params,body,body_type,assertions,timeout,retry_count,tags,priority,is_enabled,sort_order,last_run_at,last_status,created_at,updated_at)VALUES(416,79,12,7,47,'发起支付','验证发起支付','POST','/api/v1/payments','{}','{}',NULL,'json','[]',30,0,'["payment", "P0"]',2,true,2,'2026-05-23 18:03:00','success','2025-11-19 15:18:00','2026-05-31 15:14:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO api_test_cases(id,collection_id,project_id,user_id,environment_id,name,description,method,url,headers,params,body,body_type,assertions,timeout,retry_count,tags,priority,is_enabled,sort_order,last_run_at,last_status,created_at,updated_at)VALUES(417,79,12,6,47,'商品列表','验证商品列表','GET','/api/v1/products','{}','{}',NULL,'json','[]',30,0,'["product", "P0"]',3,true,3,'2026-05-18 08:52:00','failed','2026-01-11 06:41:00','2026-06-01 21:21:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO api_test_cases(id,collection_id,project_id,user_id,environment_id,name,description,method,url,headers,params,body,body_type,assertions,timeout,retry_count,tags,priority,is_enabled,sort_order,last_run_at,last_status,created_at,updated_at)VALUES(418,79,12,2,48,'用户信息','验证用户信息','GET','/api/v1/users/me','{}','{}',NULL,'json','[]',30,0,'["user", "P0"]',3,true,4,'2026-05-23 08:22:00','success','2026-04-12 15:27:00','2026-06-01 01:48:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO api_test_cases(id,collection_id,project_id,user_id,environment_id,name,description,method,url,headers,params,body,body_type,assertions,timeout,retry_count,tags,priority,is_enabled,sort_order,last_run_at,last_status,created_at,updated_at)VALUES(419,79,12,1,45,'领取券','验证领取券','POST','/api/v1/coupons/1001','{}','{}',NULL,'json','[]',30,0,'["marketing", "P1"]',1,true,5,'2026-05-18 12:18:00','success','2026-01-20 21:48:00','2026-05-29 23:22:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO api_test_cases(id,collection_id,project_id,user_id,environment_id,name,description,method,url,headers,params,body,body_type,assertions,timeout,retry_count,tags,priority,is_enabled,sort_order,last_run_at,last_status,created_at,updated_at)VALUES(420,79,12,7,45,'申请退款','验证申请退款','POST','/api/v1/refunds','{}','{}',NULL,'json','[]',30,0,'["payment", "P1"]',3,true,6,'2026-05-21 21:51:00','running','2026-02-11 22:36:00','2026-05-31 09:42:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO api_test_cases(id,collection_id,project_id,user_id,environment_id,name,description,method,url,headers,params,body,body_type,assertions,timeout,retry_count,tags,priority,is_enabled,sort_order,last_run_at,last_status,created_at,updated_at)VALUES(421,79,12,5,47,'更新资料','验证更新资料','PUT','/api/v1/users/me','{}','{}',NULL,'json','[]',30,0,'["user", "P1"]',1,true,7,'2026-05-18 16:55:00','success','2025-11-26 19:13:00','2026-05-29 19:42:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO api_test_cases(id,collection_id,project_id,user_id,environment_id,name,description,method,url,headers,params,body,body_type,assertions,timeout,retry_count,tags,priority,is_enabled,sort_order,last_run_at,last_status,created_at,updated_at)VALUES(422,80,12,2,46,'推荐列表','验证推荐列表','GET','/api/v1/recommendations','{}','{}',NULL,'json','[]',30,0,'["recommendation", "P2"]',2,true,0,'2026-05-23 07:01:00','success','2025-11-19 21:55:00','2026-06-01 20:20:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO api_test_cases(id,collection_id,project_id,user_id,environment_id,name,description,method,url,headers,params,body,body_type,assertions,timeout,retry_count,tags,priority,is_enabled,sort_order,last_run_at,last_status,created_at,updated_at)VALUES(423,80,12,5,48,'健康检查','验证健康检查','GET','/api/v1/health','{}','{}',NULL,'json','[]',30,0,'["health", "P0"]',1,true,1,'2026-05-18 11:24:00','success','2026-04-11 04:07:00','2026-05-30 00:25:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO api_test_cases(id,collection_id,project_id,user_id,environment_id,name,description,method,url,headers,params,body,body_type,assertions,timeout,retry_count,tags,priority,is_enabled,sort_order,last_run_at,last_status,created_at,updated_at)VALUES(424,80,12,6,45,'创建订单','验证创建订单','POST','/api/v1/orders','{}','{}',NULL,'json','[]',30,0,'["order", "P0"]',2,true,2,'2026-05-23 15:41:00','failed','2026-01-08 10:31:00','2026-06-01 09:10:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO api_test_cases(id,collection_id,project_id,user_id,environment_id,name,description,method,url,headers,params,body,body_type,assertions,timeout,retry_count,tags,priority,is_enabled,sort_order,last_run_at,last_status,created_at,updated_at)VALUES(425,80,12,1,46,'更新资料','验证更新资料','PUT','/api/v1/users/me','{}','{}',NULL,'json','[]',30,0,'["user", "P1"]',3,true,3,'2026-05-18 06:19:00','success','2026-03-19 20:49:00','2026-05-29 11:19:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO api_test_cases(id,collection_id,project_id,user_id,environment_id,name,description,method,url,headers,params,body,body_type,assertions,timeout,retry_count,tags,priority,is_enabled,sort_order,last_run_at,last_status,created_at,updated_at)VALUES(426,81,12,1,47,'用户登录','验证用户登录','POST','/api/v1/auth/login','{}','{}',NULL,'json','[]',30,0,'["auth", "P0"]',3,true,0,'2026-05-20 01:20:00','success','2026-01-30 11:08:00','2026-06-01 22:28:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO api_test_cases(id,collection_id,project_id,user_id,environment_id,name,description,method,url,headers,params,body,body_type,assertions,timeout,retry_count,tags,priority,is_enabled,sort_order,last_run_at,last_status,created_at,updated_at)VALUES(427,81,12,7,45,'商品列表','验证商品列表','GET','/api/v1/products','{}','{}',NULL,'json','[]',30,0,'["product", "P0"]',1,true,1,'2026-05-27 15:57:00','failed','2026-03-11 19:04:00','2026-05-31 22:50:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO api_test_cases(id,collection_id,project_id,user_id,environment_id,name,description,method,url,headers,params,body,body_type,assertions,timeout,retry_count,tags,priority,is_enabled,sort_order,last_run_at,last_status,created_at,updated_at)VALUES(428,81,12,1,47,'支付状态','验证支付状态','GET','/api/v1/payments/1001','{}','{}',NULL,'json','[]',30,0,'["payment", "P1"]',2,true,2,'2026-05-22 08:42:00','success','2026-01-16 13:01:00','2026-06-01 17:48:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO api_test_cases(id,collection_id,project_id,user_id,environment_id,name,description,method,url,headers,params,body,body_type,assertions,timeout,retry_count,tags,priority,is_enabled,sort_order,last_run_at,last_status,created_at,updated_at)VALUES(429,81,12,2,45,'获取配置','验证获取配置','GET','/api/v1/config','{}','{}',NULL,'json','[]',30,0,'["config", "P2"]',2,true,3,'2026-05-27 16:40:00','success','2025-12-08 00:43:00','2026-05-31 06:26:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO api_test_cases(id,collection_id,project_id,user_id,environment_id,name,description,method,url,headers,params,body,body_type,assertions,timeout,retry_count,tags,priority,is_enabled,sort_order,last_run_at,last_status,created_at,updated_at)VALUES(430,82,12,6,48,'标记已读','验证标记已读','PUT','/api/v1/messages/1001','{}','{}',NULL,'json','[]',30,0,'["message", "P2"]',1,true,0,'2026-05-28 06:47:00','success','2026-01-24 02:07:00','2026-05-31 16:21:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO api_test_cases(id,collection_id,project_id,user_id,environment_id,name,description,method,url,headers,params,body,body_type,assertions,timeout,retry_count,tags,priority,is_enabled,sort_order,last_run_at,last_status,created_at,updated_at)VALUES(431,82,12,7,45,'创建订单','验证创建订单','POST','/api/v1/orders','{}','{}',NULL,'json','[]',30,0,'["order", "P0"]',1,true,1,'2026-05-31 06:08:00','success','2026-05-27 18:38:00','2026-05-30 11:37:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO api_test_cases(id,collection_id,project_id,user_id,environment_id,name,description,method,url,headers,params,body,body_type,assertions,timeout,retry_count,tags,priority,is_enabled,sort_order,last_run_at,last_status,created_at,updated_at)VALUES(432,82,12,2,48,'用户登录','验证用户登录','POST','/api/v1/auth/login','{}','{}',NULL,'json','[]',30,0,'["auth", "P0"]',2,true,2,'2026-05-23 04:15:00','running','2026-05-24 10:08:00','2026-06-02 02:52:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO api_test_cases(id,collection_id,project_id,user_id,environment_id,name,description,method,url,headers,params,body,body_type,assertions,timeout,retry_count,tags,priority,is_enabled,sort_order,last_run_at,last_status,created_at,updated_at)VALUES(433,82,12,2,46,'领取券','验证领取券','POST','/api/v1/coupons/1001','{}','{}',NULL,'json','[]',30,0,'["marketing", "P1"]',2,true,3,'2026-05-27 05:55:00','success','2025-12-07 06:56:00','2026-06-01 18:12:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO api_test_cases(id,collection_id,project_id,user_id,environment_id,name,description,method,url,headers,params,body,body_type,assertions,timeout,retry_count,tags,priority,is_enabled,sort_order,last_run_at,last_status,created_at,updated_at)VALUES(434,82,12,6,45,'申请退款','验证申请退款','POST','/api/v1/refunds','{}','{}',NULL,'json','[]',30,0,'["payment", "P1"]',2,true,4,'2026-05-31 12:28:00','success','2026-05-16 18:53:00','2026-05-31 08:56:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO api_test_cases(id,collection_id,project_id,user_id,environment_id,name,description,method,url,headers,params,body,body_type,assertions,timeout,retry_count,tags,priority,is_enabled,sort_order,last_run_at,last_status,created_at,updated_at)VALUES(435,82,12,5,45,'订单详情','验证订单详情','GET','/api/v1/orders/1001','{}','{}',NULL,'json','[]',30,0,'["order", "P0"]',2,true,5,'2026-05-29 14:47:00','failed','2026-04-11 04:18:00','2026-05-31 09:55:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO api_test_cases(id,collection_id,project_id,user_id,environment_id,name,description,method,url,headers,params,body,body_type,assertions,timeout,retry_count,tags,priority,is_enabled,sort_order,last_run_at,last_status,created_at,updated_at)VALUES(436,82,12,2,47,'搜索商品','验证搜索商品','GET','/api/v1/search','{}','{}',NULL,'json','[]',30,0,'["search", "P1"]',2,true,6,NULL,'pending','2026-03-03 04:06:00','2026-05-31 17:24:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO api_test_cases(id,collection_id,project_id,user_id,environment_id,name,description,method,url,headers,params,body,body_type,assertions,timeout,retry_count,tags,priority,is_enabled,sort_order,last_run_at,last_status,created_at,updated_at)VALUES(437,83,12,7,46,'商品列表','验证商品列表','GET','/api/v1/products','{}','{}',NULL,'json','[]',30,0,'["product", "P0"]',2,true,0,'2026-05-24 04:03:00','failed','2026-05-30 10:54:00','2026-05-31 17:06:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO api_test_cases(id,collection_id,project_id,user_id,environment_id,name,description,method,url,headers,params,body,body_type,assertions,timeout,retry_count,tags,priority,is_enabled,sort_order,last_run_at,last_status,created_at,updated_at)VALUES(438,83,12,6,47,'领取券','验证领取券','POST','/api/v1/coupons/1001','{}','{}',NULL,'json','[]',30,0,'["marketing", "P1"]',1,true,1,'2026-05-27 19:17:00','failed','2026-04-15 22:36:00','2026-05-30 03:28:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO api_test_cases(id,collection_id,project_id,user_id,environment_id,name,description,method,url,headers,params,body,body_type,assertions,timeout,retry_count,tags,priority,is_enabled,sort_order,last_run_at,last_status,created_at,updated_at)VALUES(439,83,12,2,48,'用户登录','验证用户登录','POST','/api/v1/auth/login','{}','{}',NULL,'json','[]',30,0,'["auth", "P0"]',1,true,2,'2026-05-23 06:31:00','success','2026-01-19 05:29:00','2026-05-30 11:42:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO api_test_cases(id,collection_id,project_id,user_id,environment_id,name,description,method,url,headers,params,body,body_type,assertions,timeout,retry_count,tags,priority,is_enabled,sort_order,last_run_at,last_status,created_at,updated_at)VALUES(440,84,12,6,47,'用户信息','验证用户信息','GET','/api/v1/users/me','{}','{}',NULL,'json','[]',30,0,'["user", "P0"]',2,true,0,'2026-05-19 02:25:00','failed','2026-03-18 20:48:00','2026-06-01 18:17:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO api_test_cases(id,collection_id,project_id,user_id,environment_id,name,description,method,url,headers,params,body,body_type,assertions,timeout,retry_count,tags,priority,is_enabled,sort_order,last_run_at,last_status,created_at,updated_at)VALUES(441,84,12,5,46,'更新资料','验证更新资料','PUT','/api/v1/users/me','{}','{}',NULL,'json','[]',30,0,'["user", "P1"]',2,true,1,'2026-05-17 12:54:00','success','2026-02-08 17:18:00','2026-06-02 06:51:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO api_test_cases(id,collection_id,project_id,user_id,environment_id,name,description,method,url,headers,params,body,body_type,assertions,timeout,retry_count,tags,priority,is_enabled,sort_order,last_run_at,last_status,created_at,updated_at)VALUES(442,84,12,6,48,'消息列表','验证消息列表','GET','/api/v1/messages','{}','{}',NULL,'json','[]',30,0,'["message", "P1"]',1,true,2,'2026-05-29 10:01:00','failed','2026-05-15 22:48:00','2026-05-31 03:22:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO api_test_cases(id,collection_id,project_id,user_id,environment_id,name,description,method,url,headers,params,body,body_type,assertions,timeout,retry_count,tags,priority,is_enabled,sort_order,last_run_at,last_status,created_at,updated_at)VALUES(443,84,12,6,45,'获取配置','验证获取配置','GET','/api/v1/config','{}','{}',NULL,'json','[]',30,0,'["config", "P2"]',2,true,3,'2026-05-19 10:29:00','success','2025-11-17 11:11:00','2026-05-30 13:35:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO api_test_cases(id,collection_id,project_id,user_id,environment_id,name,description,method,url,headers,params,body,body_type,assertions,timeout,retry_count,tags,priority,is_enabled,sort_order,last_run_at,last_status,created_at,updated_at)VALUES(444,84,12,5,48,'商品列表','验证商品列表','GET','/api/v1/products','{}','{}',NULL,'json','[]',30,0,'["product", "P0"]',2,true,4,'2026-05-20 18:28:00','failed','2026-04-24 19:54:00','2026-06-02 01:29:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO api_test_cases(id,collection_id,project_id,user_id,environment_id,name,description,method,url,headers,params,body,body_type,assertions,timeout,retry_count,tags,priority,is_enabled,sort_order,last_run_at,last_status,created_at,updated_at)VALUES(445,84,12,6,46,'取消订单','验证取消订单','POST','/api/v1/orders/1001/cancel','{}','{}',NULL,'json','[]',30,0,'["order", "P1"]',3,true,5,'2026-05-29 09:54:00','success','2026-05-19 07:29:00','2026-06-02 04:36:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO api_test_cases(id,collection_id,project_id,user_id,environment_id,name,description,method,url,headers,params,body,body_type,assertions,timeout,retry_count,tags,priority,is_enabled,sort_order,last_run_at,last_status,created_at,updated_at)VALUES(446,84,12,7,47,'创建订单','验证创建订单','POST','/api/v1/orders','{}','{}',NULL,'json','[]',30,0,'["order", "P0"]',2,true,6,'2026-05-30 07:18:00','success','2025-11-16 18:10:00','2026-05-30 03:42:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO api_test_cases(id,collection_id,project_id,user_id,environment_id,name,description,method,url,headers,params,body,body_type,assertions,timeout,retry_count,tags,priority,is_enabled,sort_order,last_run_at,last_status,created_at,updated_at)VALUES(447,85,12,7,45,'获取配置','验证获取配置','GET','/api/v1/config','{}','{}',NULL,'json','[]',30,0,'["config", "P2"]',1,true,0,NULL,'pending','2026-02-11 06:36:00','2026-05-29 23:06:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO api_test_cases(id,collection_id,project_id,user_id,environment_id,name,description,method,url,headers,params,body,body_type,assertions,timeout,retry_count,tags,priority,is_enabled,sort_order,last_run_at,last_status,created_at,updated_at)VALUES(448,85,12,6,48,'健康检查','验证健康检查','GET','/api/v1/health','{}','{}',NULL,'json','[]',30,0,'["health", "P0"]',3,true,1,'2026-06-01 04:25:00','success','2025-11-14 00:04:00','2026-05-31 18:33:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO api_test_cases(id,collection_id,project_id,user_id,environment_id,name,description,method,url,headers,params,body,body_type,assertions,timeout,retry_count,tags,priority,is_enabled,sort_order,last_run_at,last_status,created_at,updated_at)VALUES(449,85,12,2,47,'提交反馈','验证提交反馈','POST','/api/v1/feedback','{}','{}',NULL,'json','[]',30,0,'["feedback", "P2"]',3,true,2,'2026-05-18 06:24:00','failed','2026-01-26 12:25:00','2026-05-29 18:25:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO api_test_cases(id,collection_id,project_id,user_id,environment_id,name,description,method,url,headers,params,body,body_type,assertions,timeout,retry_count,tags,priority,is_enabled,sort_order,last_run_at,last_status,created_at,updated_at)VALUES(450,85,12,2,45,'支付状态','验证支付状态','GET','/api/v1/payments/1001','{}','{}',NULL,'json','[]',30,0,'["payment", "P1"]',2,true,3,'2026-05-17 15:36:00','success','2025-12-09 22:11:00','2026-05-30 23:57:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO api_test_cases(id,collection_id,project_id,user_id,environment_id,name,description,method,url,headers,params,body,body_type,assertions,timeout,retry_count,tags,priority,is_enabled,sort_order,last_run_at,last_status,created_at,updated_at)VALUES(451,85,12,1,45,'消息列表','验证消息列表','GET','/api/v1/messages','{}','{}',NULL,'json','[]',30,0,'["message", "P1"]',3,true,4,'2026-05-21 22:09:00','success','2026-01-03 09:12:00','2026-05-30 21:54:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO api_test_cases(id,collection_id,project_id,user_id,environment_id,name,description,method,url,headers,params,body,body_type,assertions,timeout,retry_count,tags,priority,is_enabled,sort_order,last_run_at,last_status,created_at,updated_at)VALUES(452,85,12,6,47,'搜索商品','验证搜索商品','GET','/api/v1/search','{}','{}',NULL,'json','[]',30,0,'["search", "P1"]',3,true,5,'2026-05-19 22:57:00','cancelled','2026-03-31 02:45:00','2026-05-30 15:55:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO api_test_cases(id,collection_id,project_id,user_id,environment_id,name,description,method,url,headers,params,body,body_type,assertions,timeout,retry_count,tags,priority,is_enabled,sort_order,last_run_at,last_status,created_at,updated_at)VALUES(453,85,12,1,47,'推荐列表','验证推荐列表','GET','/api/v1/recommendations','{}','{}',NULL,'json','[]',30,0,'["recommendation", "P2"]',2,true,6,'2026-05-28 09:26:00','success','2026-05-22 19:18:00','2026-05-29 15:28:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO api_test_cases(id,collection_id,project_id,user_id,environment_id,name,description,method,url,headers,params,body,body_type,assertions,timeout,retry_count,tags,priority,is_enabled,sort_order,last_run_at,last_status,created_at,updated_at)VALUES(454,85,12,6,47,'优惠券','验证优惠券','GET','/api/v1/coupons','{}','{}',NULL,'json','[]',30,0,'["marketing", "P1"]',2,true,7,'2026-05-17 15:59:00','success','2026-02-24 15:36:00','2026-05-30 15:54:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO api_test_cases(id,collection_id,project_id,user_id,environment_id,name,description,method,url,headers,params,body,body_type,assertions,timeout,retry_count,tags,priority,is_enabled,sort_order,last_run_at,last_status,created_at,updated_at)VALUES(455,86,13,7,51,'商品列表','验证商品列表','GET','/api/v1/products','{}','{}',NULL,'json','[]',30,0,'["product", "P0"]',3,true,0,'2026-05-20 03:29:00','success','2025-11-12 07:07:00','2026-06-01 00:44:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO api_test_cases(id,collection_id,project_id,user_id,environment_id,name,description,method,url,headers,params,body,body_type,assertions,timeout,retry_count,tags,priority,is_enabled,sort_order,last_run_at,last_status,created_at,updated_at)VALUES(456,86,13,1,51,'取消订单','验证取消订单','POST','/api/v1/orders/1001/cancel','{}','{}',NULL,'json','[]',30,0,'["order", "P1"]',3,true,1,'2026-05-21 02:21:00','cancelled','2026-05-08 11:06:00','2026-06-01 15:39:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO api_test_cases(id,collection_id,project_id,user_id,environment_id,name,description,method,url,headers,params,body,body_type,assertions,timeout,retry_count,tags,priority,is_enabled,sort_order,last_run_at,last_status,created_at,updated_at)VALUES(457,86,13,5,49,'消息列表','验证消息列表','GET','/api/v1/messages','{}','{}',NULL,'json','[]',30,0,'["message", "P1"]',2,true,2,'2026-05-17 20:47:00','success','2025-11-10 07:19:00','2026-05-30 17:09:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO api_test_cases(id,collection_id,project_id,user_id,environment_id,name,description,method,url,headers,params,body,body_type,assertions,timeout,retry_count,tags,priority,is_enabled,sort_order,last_run_at,last_status,created_at,updated_at)VALUES(458,86,13,5,52,'获取配置','验证获取配置','GET','/api/v1/config','{}','{}',NULL,'json','[]',30,0,'["config", "P2"]',2,true,3,'2026-05-23 03:34:00','failed','2026-03-28 14:28:00','2026-05-29 12:12:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO api_test_cases(id,collection_id,project_id,user_id,environment_id,name,description,method,url,headers,params,body,body_type,assertions,timeout,retry_count,tags,priority,is_enabled,sort_order,last_run_at,last_status,created_at,updated_at)VALUES(459,86,13,7,50,'优惠券','验证优惠券','GET','/api/v1/coupons','{}','{}',NULL,'json','[]',30,0,'["marketing", "P1"]',1,true,4,'2026-05-27 15:29:00','running','2025-12-13 10:31:00','2026-05-30 13:26:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO api_test_cases(id,collection_id,project_id,user_id,environment_id,name,description,method,url,headers,params,body,body_type,assertions,timeout,retry_count,tags,priority,is_enabled,sort_order,last_run_at,last_status,created_at,updated_at)VALUES(460,86,13,7,52,'更新资料','验证更新资料','PUT','/api/v1/users/me','{}','{}',NULL,'json','[]',30,0,'["user", "P1"]',3,true,5,NULL,'pending','2025-12-23 08:27:00','2026-05-31 22:31:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO api_test_cases(id,collection_id,project_id,user_id,environment_id,name,description,method,url,headers,params,body,body_type,assertions,timeout,retry_count,tags,priority,is_enabled,sort_order,last_run_at,last_status,created_at,updated_at)VALUES(461,87,13,6,51,'发起支付','验证发起支付','POST','/api/v1/payments','{}','{}',NULL,'json','[]',30,0,'["payment", "P0"]',2,true,0,'2026-05-30 13:47:00','running','2026-03-25 00:19:00','2026-06-01 01:17:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO api_test_cases(id,collection_id,project_id,user_id,environment_id,name,description,method,url,headers,params,body,body_type,assertions,timeout,retry_count,tags,priority,is_enabled,sort_order,last_run_at,last_status,created_at,updated_at)VALUES(462,87,13,7,50,'创建订单','验证创建订单','POST','/api/v1/orders','{}','{}',NULL,'json','[]',30,0,'["order", "P0"]',1,true,1,'2026-05-30 05:48:00','success','2026-03-31 00:31:00','2026-05-29 16:33:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO api_test_cases(id,collection_id,project_id,user_id,environment_id,name,description,method,url,headers,params,body,body_type,assertions,timeout,retry_count,tags,priority,is_enabled,sort_order,last_run_at,last_status,created_at,updated_at)VALUES(463,87,13,6,49,'申请退款','验证申请退款','POST','/api/v1/refunds','{}','{}',NULL,'json','[]',30,0,'["payment", "P1"]',2,true,2,'2026-05-25 05:59:00','success','2025-11-11 01:18:00','2026-05-31 13:06:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO api_test_cases(id,collection_id,project_id,user_id,environment_id,name,description,method,url,headers,params,body,body_type,assertions,timeout,retry_count,tags,priority,is_enabled,sort_order,last_run_at,last_status,created_at,updated_at)VALUES(464,87,13,1,52,'推荐列表','验证推荐列表','GET','/api/v1/recommendations','{}','{}',NULL,'json','[]',30,0,'["recommendation", "P2"]',2,true,3,'2026-06-01 07:40:00','failed','2026-03-17 07:03:00','2026-05-29 22:18:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO api_test_cases(id,collection_id,project_id,user_id,environment_id,name,description,method,url,headers,params,body,body_type,assertions,timeout,retry_count,tags,priority,is_enabled,sort_order,last_run_at,last_status,created_at,updated_at)VALUES(465,88,13,1,51,'更新资料','验证更新资料','PUT','/api/v1/users/me','{}','{}',NULL,'json','[]',30,0,'["user", "P1"]',1,true,0,'2026-05-31 02:22:00','success','2025-11-15 23:39:00','2026-05-29 10:13:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO api_test_cases(id,collection_id,project_id,user_id,environment_id,name,description,method,url,headers,params,body,body_type,assertions,timeout,retry_count,tags,priority,is_enabled,sort_order,last_run_at,last_status,created_at,updated_at)VALUES(466,88,13,2,52,'搜索商品','验证搜索商品','GET','/api/v1/search','{}','{}',NULL,'json','[]',30,0,'["search", "P1"]',2,true,1,'2026-05-30 04:47:00','success','2026-02-08 20:44:00','2026-06-01 18:26:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO api_test_cases(id,collection_id,project_id,user_id,environment_id,name,description,method,url,headers,params,body,body_type,assertions,timeout,retry_count,tags,priority,is_enabled,sort_order,last_run_at,last_status,created_at,updated_at)VALUES(467,88,13,5,49,'创建订单','验证创建订单','POST','/api/v1/orders','{}','{}',NULL,'json','[]',30,0,'["order", "P0"]',1,true,2,'2026-05-19 18:17:00','success','2026-03-22 05:37:00','2026-05-29 11:37:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO api_test_cases(id,collection_id,project_id,user_id,environment_id,name,description,method,url,headers,params,body,body_type,assertions,timeout,retry_count,tags,priority,is_enabled,sort_order,last_run_at,last_status,created_at,updated_at)VALUES(468,88,13,5,49,'发起支付','验证发起支付','POST','/api/v1/payments','{}','{}',NULL,'json','[]',30,0,'["payment", "P0"]',1,true,3,'2026-05-31 10:18:00','success','2025-12-06 12:45:00','2026-05-30 16:36:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO api_test_cases(id,collection_id,project_id,user_id,environment_id,name,description,method,url,headers,params,body,body_type,assertions,timeout,retry_count,tags,priority,is_enabled,sort_order,last_run_at,last_status,created_at,updated_at)VALUES(469,88,13,5,51,'商品列表','验证商品列表','GET','/api/v1/products','{}','{}',NULL,'json','[]',30,0,'["product", "P0"]',1,true,4,'2026-05-29 16:05:00','running','2026-02-07 22:00:00','2026-05-30 01:41:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO api_test_cases(id,collection_id,project_id,user_id,environment_id,name,description,method,url,headers,params,body,body_type,assertions,timeout,retry_count,tags,priority,is_enabled,sort_order,last_run_at,last_status,created_at,updated_at)VALUES(470,88,13,1,50,'申请退款','验证申请退款','POST','/api/v1/refunds','{}','{}',NULL,'json','[]',30,0,'["payment", "P1"]',2,true,5,'2026-05-27 19:20:00','success','2025-11-05 13:34:00','2026-06-02 01:05:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO api_test_cases(id,collection_id,project_id,user_id,environment_id,name,description,method,url,headers,params,body,body_type,assertions,timeout,retry_count,tags,priority,is_enabled,sort_order,last_run_at,last_status,created_at,updated_at)VALUES(471,88,13,1,52,'标记已读','验证标记已读','PUT','/api/v1/messages/1001','{}','{}',NULL,'json','[]',30,0,'["message", "P2"]',2,true,6,'2026-05-19 23:15:00','success','2025-11-04 06:08:00','2026-05-31 11:44:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO api_test_cases(id,collection_id,project_id,user_id,environment_id,name,description,method,url,headers,params,body,body_type,assertions,timeout,retry_count,tags,priority,is_enabled,sort_order,last_run_at,last_status,created_at,updated_at)VALUES(472,88,13,7,49,'支付状态','验证支付状态','GET','/api/v1/payments/1001','{}','{}',NULL,'json','[]',30,0,'["payment", "P1"]',1,true,7,'2026-05-22 19:16:00','success','2025-11-18 08:19:00','2026-05-31 13:32:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO api_test_cases(id,collection_id,project_id,user_id,environment_id,name,description,method,url,headers,params,body,body_type,assertions,timeout,retry_count,tags,priority,is_enabled,sort_order,last_run_at,last_status,created_at,updated_at)VALUES(473,89,13,1,50,'创建订单','验证创建订单','POST','/api/v1/orders','{}','{}',NULL,'json','[]',30,0,'["order", "P0"]',2,true,0,'2026-05-28 14:17:00','success','2025-11-10 23:32:00','2026-05-29 10:52:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO api_test_cases(id,collection_id,project_id,user_id,environment_id,name,description,method,url,headers,params,body,body_type,assertions,timeout,retry_count,tags,priority,is_enabled,sort_order,last_run_at,last_status,created_at,updated_at)VALUES(474,89,13,5,50,'用户登录','验证用户登录','POST','/api/v1/auth/login','{}','{}',NULL,'json','[]',30,0,'["auth", "P0"]',1,true,1,'2026-05-23 00:48:00','failed','2026-02-14 22:49:00','2026-05-29 21:07:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO api_test_cases(id,collection_id,project_id,user_id,environment_id,name,description,method,url,headers,params,body,body_type,assertions,timeout,retry_count,tags,priority,is_enabled,sort_order,last_run_at,last_status,created_at,updated_at)VALUES(475,89,13,7,50,'搜索商品','验证搜索商品','GET','/api/v1/search','{}','{}',NULL,'json','[]',30,0,'["search", "P1"]',2,true,2,'2026-06-01 16:19:00','success','2025-12-23 02:02:00','2026-06-01 19:48:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO api_test_cases(id,collection_id,project_id,user_id,environment_id,name,description,method,url,headers,params,body,body_type,assertions,timeout,retry_count,tags,priority,is_enabled,sort_order,last_run_at,last_status,created_at,updated_at)VALUES(476,89,13,5,50,'取消订单','验证取消订单','POST','/api/v1/orders/1001/cancel','{}','{}',NULL,'json','[]',30,0,'["order", "P1"]',1,true,3,'2026-05-19 14:44:00','success','2026-05-09 22:50:00','2026-06-02 09:15:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO api_test_cases(id,collection_id,project_id,user_id,environment_id,name,description,method,url,headers,params,body,body_type,assertions,timeout,retry_count,tags,priority,is_enabled,sort_order,last_run_at,last_status,created_at,updated_at)VALUES(477,89,13,7,52,'申请退款','验证申请退款','POST','/api/v1/refunds','{}','{}',NULL,'json','[]',30,0,'["payment", "P1"]',1,true,4,'2026-05-18 12:29:00','failed','2026-04-04 11:47:00','2026-06-01 01:42:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO api_test_cases(id,collection_id,project_id,user_id,environment_id,name,description,method,url,headers,params,body,body_type,assertions,timeout,retry_count,tags,priority,is_enabled,sort_order,last_run_at,last_status,created_at,updated_at)VALUES(478,89,13,6,52,'订单详情','验证订单详情','GET','/api/v1/orders/1001','{}','{}',NULL,'json','[]',30,0,'["order", "P0"]',2,true,5,'2026-05-26 14:47:00','success','2025-11-26 12:48:00','2026-05-30 04:34:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO api_test_cases(id,collection_id,project_id,user_id,environment_id,name,description,method,url,headers,params,body,body_type,assertions,timeout,retry_count,tags,priority,is_enabled,sort_order,last_run_at,last_status,created_at,updated_at)VALUES(479,89,13,2,49,'获取配置','验证获取配置','GET','/api/v1/config','{}','{}',NULL,'json','[]',30,0,'["config", "P2"]',2,true,6,'2026-05-25 02:21:00','success','2026-03-29 22:23:00','2026-05-30 08:00:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO api_test_cases(id,collection_id,project_id,user_id,environment_id,name,description,method,url,headers,params,body,body_type,assertions,timeout,retry_count,tags,priority,is_enabled,sort_order,last_run_at,last_status,created_at,updated_at)VALUES(480,89,13,6,50,'用户信息','验证用户信息','GET','/api/v1/users/me','{}','{}',NULL,'json','[]',30,0,'["user", "P0"]',3,true,7,'2026-05-20 12:47:00','running','2026-02-22 11:33:00','2026-05-31 07:54:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO api_test_cases(id,collection_id,project_id,user_id,environment_id,name,description,method,url,headers,params,body,body_type,assertions,timeout,retry_count,tags,priority,is_enabled,sort_order,last_run_at,last_status,created_at,updated_at)VALUES(481,90,13,7,49,'用户信息','验证用户信息','GET','/api/v1/users/me','{}','{}',NULL,'json','[]',30,0,'["user", "P0"]',3,true,0,'2026-05-21 00:35:00','success','2026-02-27 05:03:00','2026-06-01 15:49:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO api_test_cases(id,collection_id,project_id,user_id,environment_id,name,description,method,url,headers,params,body,body_type,assertions,timeout,retry_count,tags,priority,is_enabled,sort_order,last_run_at,last_status,created_at,updated_at)VALUES(482,90,13,5,50,'健康检查','验证健康检查','GET','/api/v1/health','{}','{}',NULL,'json','[]',30,0,'["health", "P0"]',1,true,1,'2026-05-22 19:52:00','success','2026-03-11 11:27:00','2026-05-30 05:44:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO api_test_cases(id,collection_id,project_id,user_id,environment_id,name,description,method,url,headers,params,body,body_type,assertions,timeout,retry_count,tags,priority,is_enabled,sort_order,last_run_at,last_status,created_at,updated_at)VALUES(483,90,13,1,51,'消息列表','验证消息列表','GET','/api/v1/messages','{}','{}',NULL,'json','[]',30,0,'["message", "P1"]',2,true,2,'2026-05-28 18:05:00','success','2025-11-21 22:01:00','2026-05-30 00:03:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO api_test_cases(id,collection_id,project_id,user_id,environment_id,name,description,method,url,headers,params,body,body_type,assertions,timeout,retry_count,tags,priority,is_enabled,sort_order,last_run_at,last_status,created_at,updated_at)VALUES(484,90,13,5,51,'发起支付','验证发起支付','POST','/api/v1/payments','{}','{}',NULL,'json','[]',30,0,'["payment", "P0"]',3,true,3,'2026-05-20 04:40:00','success','2026-01-27 05:25:00','2026-05-30 08:48:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO api_test_cases(id,collection_id,project_id,user_id,environment_id,name,description,method,url,headers,params,body,body_type,assertions,timeout,retry_count,tags,priority,is_enabled,sort_order,last_run_at,last_status,created_at,updated_at)VALUES(485,90,13,2,49,'获取配置','验证获取配置','GET','/api/v1/config','{}','{}',NULL,'json','[]',30,0,'["config", "P2"]',1,true,4,'2026-05-31 18:44:00','success','2025-12-02 19:33:00','2026-06-01 18:58:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO api_test_cases(id,collection_id,project_id,user_id,environment_id,name,description,method,url,headers,params,body,body_type,assertions,timeout,retry_count,tags,priority,is_enabled,sort_order,last_run_at,last_status,created_at,updated_at)VALUES(486,90,13,6,51,'上传图片','验证上传图片','POST','/api/v1/upload','{}','{}',NULL,'json','[]',30,0,'["upload", "P1"]',1,true,5,'2026-05-17 19:29:00','cancelled','2025-11-29 05:53:00','2026-05-31 07:47:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO api_test_cases(id,collection_id,project_id,user_id,environment_id,name,description,method,url,headers,params,body,body_type,assertions,timeout,retry_count,tags,priority,is_enabled,sort_order,last_run_at,last_status,created_at,updated_at)VALUES(487,90,13,5,50,'订单详情','验证订单详情','GET','/api/v1/orders/1001','{}','{}',NULL,'json','[]',30,0,'["order", "P0"]',3,true,6,'2026-05-24 15:03:00','failed','2026-01-03 03:23:00','2026-06-01 17:11:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO api_test_cases(id,collection_id,project_id,user_id,environment_id,name,description,method,url,headers,params,body,body_type,assertions,timeout,retry_count,tags,priority,is_enabled,sort_order,last_run_at,last_status,created_at,updated_at)VALUES(488,91,13,5,49,'订单详情','验证订单详情','GET','/api/v1/orders/1001','{}','{}',NULL,'json','[]',30,0,'["order", "P0"]',2,true,0,'2026-05-29 21:37:00','success','2026-05-04 23:51:00','2026-06-02 07:31:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO api_test_cases(id,collection_id,project_id,user_id,environment_id,name,description,method,url,headers,params,body,body_type,assertions,timeout,retry_count,tags,priority,is_enabled,sort_order,last_run_at,last_status,created_at,updated_at)VALUES(489,91,13,6,52,'推荐列表','验证推荐列表','GET','/api/v1/recommendations','{}','{}',NULL,'json','[]',30,0,'["recommendation", "P2"]',1,true,1,'2026-05-24 14:18:00','success','2026-03-09 08:19:00','2026-05-29 23:14:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO api_test_cases(id,collection_id,project_id,user_id,environment_id,name,description,method,url,headers,params,body,body_type,assertions,timeout,retry_count,tags,priority,is_enabled,sort_order,last_run_at,last_status,created_at,updated_at)VALUES(490,91,13,7,50,'更新资料','验证更新资料','PUT','/api/v1/users/me','{}','{}',NULL,'json','[]',30,0,'["user", "P1"]',2,true,2,'2026-05-31 13:42:00','success','2025-11-09 08:13:00','2026-06-01 16:22:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO api_test_cases(id,collection_id,project_id,user_id,environment_id,name,description,method,url,headers,params,body,body_type,assertions,timeout,retry_count,tags,priority,is_enabled,sort_order,last_run_at,last_status,created_at,updated_at)VALUES(491,91,13,6,49,'发起支付','验证发起支付','POST','/api/v1/payments','{}','{}',NULL,'json','[]',30,0,'["payment", "P0"]',2,true,3,'2026-05-28 02:11:00','success','2026-05-10 09:06:00','2026-06-01 04:36:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO api_test_cases(id,collection_id,project_id,user_id,environment_id,name,description,method,url,headers,params,body,body_type,assertions,timeout,retry_count,tags,priority,is_enabled,sort_order,last_run_at,last_status,created_at,updated_at)VALUES(492,91,13,6,51,'获取配置','验证获取配置','GET','/api/v1/config','{}','{}',NULL,'json','[]',30,0,'["config", "P2"]',2,true,4,'2026-05-29 06:41:00','success','2025-11-07 20:13:00','2026-05-30 12:22:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO api_test_cases(id,collection_id,project_id,user_id,environment_id,name,description,method,url,headers,params,body,body_type,assertions,timeout,retry_count,tags,priority,is_enabled,sort_order,last_run_at,last_status,created_at,updated_at)VALUES(493,91,13,2,51,'消息列表','验证消息列表','GET','/api/v1/messages','{}','{}',NULL,'json','[]',30,0,'["message", "P1"]',2,true,5,'2026-05-21 17:48:00','failed','2026-02-06 21:30:00','2026-05-30 15:22:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO api_test_cases(id,collection_id,project_id,user_id,environment_id,name,description,method,url,headers,params,body,body_type,assertions,timeout,retry_count,tags,priority,is_enabled,sort_order,last_run_at,last_status,created_at,updated_at)VALUES(494,91,13,6,49,'用户信息','验证用户信息','GET','/api/v1/users/me','{}','{}',NULL,'json','[]',30,0,'["user", "P0"]',2,true,6,'2026-05-21 14:49:00','failed','2025-12-21 20:55:00','2026-06-01 17:39:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO api_test_cases(id,collection_id,project_id,user_id,environment_id,name,description,method,url,headers,params,body,body_type,assertions,timeout,retry_count,tags,priority,is_enabled,sort_order,last_run_at,last_status,created_at,updated_at)VALUES(495,92,14,6,56,'发起支付','验证发起支付','POST','/api/v1/payments','{}','{}',NULL,'json','[]',30,0,'["payment", "P0"]',1,true,0,'2026-05-18 00:51:00','success','2025-12-08 00:07:00','2026-05-31 17:33:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO api_test_cases(id,collection_id,project_id,user_id,environment_id,name,description,method,url,headers,params,body,body_type,assertions,timeout,retry_count,tags,priority,is_enabled,sort_order,last_run_at,last_status,created_at,updated_at)VALUES(496,92,14,5,53,'创建订单','验证创建订单','POST','/api/v1/orders','{}','{}',NULL,'json','[]',30,0,'["order", "P0"]',2,true,1,'2026-05-31 17:54:00','success','2026-02-12 20:54:00','2026-05-29 12:14:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO api_test_cases(id,collection_id,project_id,user_id,environment_id,name,description,method,url,headers,params,body,body_type,assertions,timeout,retry_count,tags,priority,is_enabled,sort_order,last_run_at,last_status,created_at,updated_at)VALUES(497,92,14,7,55,'获取配置','验证获取配置','GET','/api/v1/config','{}','{}',NULL,'json','[]',30,0,'["config", "P2"]',1,true,2,'2026-05-30 17:59:00','success','2025-11-23 12:31:00','2026-06-01 04:07:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO api_test_cases(id,collection_id,project_id,user_id,environment_id,name,description,method,url,headers,params,body,body_type,assertions,timeout,retry_count,tags,priority,is_enabled,sort_order,last_run_at,last_status,created_at,updated_at)VALUES(498,92,14,6,53,'提交反馈','验证提交反馈','POST','/api/v1/feedback','{}','{}',NULL,'json','[]',30,0,'["feedback", "P2"]',3,true,3,'2026-05-23 23:23:00','success','2026-02-04 12:32:00','2026-05-30 23:02:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO api_test_cases(id,collection_id,project_id,user_id,environment_id,name,description,method,url,headers,params,body,body_type,assertions,timeout,retry_count,tags,priority,is_enabled,sort_order,last_run_at,last_status,created_at,updated_at)VALUES(499,92,14,2,54,'更新资料','验证更新资料','PUT','/api/v1/users/me','{}','{}',NULL,'json','[]',30,0,'["user", "P1"]',2,true,4,'2026-05-24 12:54:00','success','2026-01-16 10:00:00','2026-05-30 07:00:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO api_test_cases(id,collection_id,project_id,user_id,environment_id,name,description,method,url,headers,params,body,body_type,assertions,timeout,retry_count,tags,priority,is_enabled,sort_order,last_run_at,last_status,created_at,updated_at)VALUES(500,92,14,2,56,'领取券','验证领取券','POST','/api/v1/coupons/1001','{}','{}',NULL,'json','[]',30,0,'["marketing", "P1"]',2,true,5,'2026-05-20 12:13:00','success','2025-11-27 18:41:00','2026-05-30 11:17:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO api_test_cases(id,collection_id,project_id,user_id,environment_id,name,description,method,url,headers,params,body,body_type,assertions,timeout,retry_count,tags,priority,is_enabled,sort_order,last_run_at,last_status,created_at,updated_at)VALUES(501,93,14,1,54,'搜索商品','验证搜索商品','GET','/api/v1/search','{}','{}',NULL,'json','[]',30,0,'["search", "P1"]',1,true,0,'2026-05-26 18:19:00','running','2025-12-17 02:33:00','2026-06-01 07:41:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO api_test_cases(id,collection_id,project_id,user_id,environment_id,name,description,method,url,headers,params,body,body_type,assertions,timeout,retry_count,tags,priority,is_enabled,sort_order,last_run_at,last_status,created_at,updated_at)VALUES(502,93,14,6,54,'申请退款','验证申请退款','POST','/api/v1/refunds','{}','{}',NULL,'json','[]',30,0,'["payment", "P1"]',1,true,1,'2026-06-02 06:50:00','success','2025-11-23 11:32:00','2026-05-29 18:59:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO api_test_cases(id,collection_id,project_id,user_id,environment_id,name,description,method,url,headers,params,body,body_type,assertions,timeout,retry_count,tags,priority,is_enabled,sort_order,last_run_at,last_status,created_at,updated_at)VALUES(503,93,14,6,54,'更新资料','验证更新资料','PUT','/api/v1/users/me','{}','{}',NULL,'json','[]',30,0,'["user", "P1"]',1,true,2,'2026-05-21 08:39:00','success','2026-05-05 13:06:00','2026-05-29 20:06:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO api_test_cases(id,collection_id,project_id,user_id,environment_id,name,description,method,url,headers,params,body,body_type,assertions,timeout,retry_count,tags,priority,is_enabled,sort_order,last_run_at,last_status,created_at,updated_at)VALUES(504,93,14,6,55,'创建订单','验证创建订单','POST','/api/v1/orders','{}','{}',NULL,'json','[]',30,0,'["order", "P0"]',2,true,3,'2026-05-20 18:28:00','success','2025-11-27 14:01:00','2026-05-30 02:15:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO api_test_cases(id,collection_id,project_id,user_id,environment_id,name,description,method,url,headers,params,body,body_type,assertions,timeout,retry_count,tags,priority,is_enabled,sort_order,last_run_at,last_status,created_at,updated_at)VALUES(505,93,14,1,53,'提交反馈','验证提交反馈','POST','/api/v1/feedback','{}','{}',NULL,'json','[]',30,0,'["feedback", "P2"]',2,true,4,'2026-05-22 16:56:00','success','2025-12-17 20:04:00','2026-05-30 06:29:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO api_test_cases(id,collection_id,project_id,user_id,environment_id,name,description,method,url,headers,params,body,body_type,assertions,timeout,retry_count,tags,priority,is_enabled,sort_order,last_run_at,last_status,created_at,updated_at)VALUES(506,93,14,7,55,'用户登录','验证用户登录','POST','/api/v1/auth/login','{}','{}',NULL,'json','[]',30,0,'["auth", "P0"]',2,true,5,'2026-05-20 09:50:00','success','2025-11-28 03:30:00','2026-05-30 19:46:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO api_test_cases(id,collection_id,project_id,user_id,environment_id,name,description,method,url,headers,params,body,body_type,assertions,timeout,retry_count,tags,priority,is_enabled,sort_order,last_run_at,last_status,created_at,updated_at)VALUES(507,93,14,7,54,'商品列表','验证商品列表','GET','/api/v1/products','{}','{}',NULL,'json','[]',30,0,'["product", "P0"]',3,true,6,'2026-05-22 14:06:00','success','2025-12-14 19:52:00','2026-05-30 10:15:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO api_test_cases(id,collection_id,project_id,user_id,environment_id,name,description,method,url,headers,params,body,body_type,assertions,timeout,retry_count,tags,priority,is_enabled,sort_order,last_run_at,last_status,created_at,updated_at)VALUES(508,93,14,6,56,'用户信息','验证用户信息','GET','/api/v1/users/me','{}','{}',NULL,'json','[]',30,0,'["user", "P0"]',1,true,7,'2026-05-21 18:09:00','failed','2025-12-24 03:42:00','2026-06-01 12:30:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO api_test_cases(id,collection_id,project_id,user_id,environment_id,name,description,method,url,headers,params,body,body_type,assertions,timeout,retry_count,tags,priority,is_enabled,sort_order,last_run_at,last_status,created_at,updated_at)VALUES(509,94,14,1,56,'订单详情','验证订单详情','GET','/api/v1/orders/1001','{}','{}',NULL,'json','[]',30,0,'["order", "P0"]',2,true,0,NULL,'pending','2026-03-16 02:47:00','2026-06-02 09:38:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO api_test_cases(id,collection_id,project_id,user_id,environment_id,name,description,method,url,headers,params,body,body_type,assertions,timeout,retry_count,tags,priority,is_enabled,sort_order,last_run_at,last_status,created_at,updated_at)VALUES(510,94,14,5,55,'取消订单','验证取消订单','POST','/api/v1/orders/1001/cancel','{}','{}',NULL,'json','[]',30,0,'["order", "P1"]',1,true,1,'2026-05-27 17:58:00','failed','2026-03-06 20:53:00','2026-06-01 06:25:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO api_test_cases(id,collection_id,project_id,user_id,environment_id,name,description,method,url,headers,params,body,body_type,assertions,timeout,retry_count,tags,priority,is_enabled,sort_order,last_run_at,last_status,created_at,updated_at)VALUES(511,94,14,2,56,'健康检查','验证健康检查','GET','/api/v1/health','{}','{}',NULL,'json','[]',30,0,'["health", "P0"]',1,true,2,'2026-05-22 22:11:00','success','2025-11-15 16:43:00','2026-05-31 11:05:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO api_test_cases(id,collection_id,project_id,user_id,environment_id,name,description,method,url,headers,params,body,body_type,assertions,timeout,retry_count,tags,priority,is_enabled,sort_order,last_run_at,last_status,created_at,updated_at)VALUES(512,94,14,7,53,'获取配置','验证获取配置','GET','/api/v1/config','{}','{}',NULL,'json','[]',30,0,'["config", "P2"]',1,true,3,'2026-05-18 19:07:00','failed','2026-05-04 14:21:00','2026-06-01 16:58:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO api_test_cases(id,collection_id,project_id,user_id,environment_id,name,description,method,url,headers,params,body,body_type,assertions,timeout,retry_count,tags,priority,is_enabled,sort_order,last_run_at,last_status,created_at,updated_at)VALUES(513,95,14,5,56,'商品列表','验证商品列表','GET','/api/v1/products','{}','{}',NULL,'json','[]',30,0,'["product", "P0"]',1,true,0,'2026-05-17 10:05:00','failed','2026-04-22 13:37:00','2026-05-31 05:53:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO api_test_cases(id,collection_id,project_id,user_id,environment_id,name,description,method,url,headers,params,body,body_type,assertions,timeout,retry_count,tags,priority,is_enabled,sort_order,last_run_at,last_status,created_at,updated_at)VALUES(514,95,14,2,56,'订单详情','验证订单详情','GET','/api/v1/orders/1001','{}','{}',NULL,'json','[]',30,0,'["order", "P0"]',1,true,1,NULL,'pending','2026-03-30 18:39:00','2026-05-30 17:50:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO api_test_cases(id,collection_id,project_id,user_id,environment_id,name,description,method,url,headers,params,body,body_type,assertions,timeout,retry_count,tags,priority,is_enabled,sort_order,last_run_at,last_status,created_at,updated_at)VALUES(515,95,14,1,55,'健康检查','验证健康检查','GET','/api/v1/health','{}','{}',NULL,'json','[]',30,0,'["health", "P0"]',3,true,2,'2026-05-19 22:20:00','success','2026-03-31 05:12:00','2026-05-30 02:52:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO api_test_cases(id,collection_id,project_id,user_id,environment_id,name,description,method,url,headers,params,body,body_type,assertions,timeout,retry_count,tags,priority,is_enabled,sort_order,last_run_at,last_status,created_at,updated_at)VALUES(516,95,14,6,56,'取消订单','验证取消订单','POST','/api/v1/orders/1001/cancel','{}','{}',NULL,'json','[]',30,0,'["order", "P1"]',3,true,3,'2026-05-18 17:10:00','running','2026-03-01 09:32:00','2026-06-01 09:15:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO api_test_cases(id,collection_id,project_id,user_id,environment_id,name,description,method,url,headers,params,body,body_type,assertions,timeout,retry_count,tags,priority,is_enabled,sort_order,last_run_at,last_status,created_at,updated_at)VALUES(517,95,14,7,53,'标记已读','验证标记已读','PUT','/api/v1/messages/1001','{}','{}',NULL,'json','[]',30,0,'["message", "P2"]',1,true,4,'2026-05-22 21:11:00','success','2026-02-10 08:35:00','2026-06-01 12:01:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO api_test_cases(id,collection_id,project_id,user_id,environment_id,name,description,method,url,headers,params,body,body_type,assertions,timeout,retry_count,tags,priority,is_enabled,sort_order,last_run_at,last_status,created_at,updated_at)VALUES(518,95,14,2,53,'更新资料','验证更新资料','PUT','/api/v1/users/me','{}','{}',NULL,'json','[]',30,0,'["user", "P1"]',3,true,5,'2026-05-23 20:35:00','cancelled','2025-12-03 16:05:00','2026-05-30 10:13:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO api_test_cases(id,collection_id,project_id,user_id,environment_id,name,description,method,url,headers,params,body,body_type,assertions,timeout,retry_count,tags,priority,is_enabled,sort_order,last_run_at,last_status,created_at,updated_at)VALUES(519,95,14,5,55,'获取配置','验证获取配置','GET','/api/v1/config','{}','{}',NULL,'json','[]',30,0,'["config", "P2"]',1,true,6,'2026-05-24 17:21:00','success','2025-12-03 21:32:00','2026-05-31 16:21:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO api_test_cases(id,collection_id,project_id,user_id,environment_id,name,description,method,url,headers,params,body,body_type,assertions,timeout,retry_count,tags,priority,is_enabled,sort_order,last_run_at,last_status,created_at,updated_at)VALUES(520,96,14,7,55,'上传图片','验证上传图片','POST','/api/v1/upload','{}','{}',NULL,'json','[]',30,0,'["upload", "P1"]',2,true,0,'2026-05-28 17:26:00','success','2026-04-08 07:28:00','2026-05-30 17:39:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO api_test_cases(id,collection_id,project_id,user_id,environment_id,name,description,method,url,headers,params,body,body_type,assertions,timeout,retry_count,tags,priority,is_enabled,sort_order,last_run_at,last_status,created_at,updated_at)VALUES(521,96,14,2,53,'标记已读','验证标记已读','PUT','/api/v1/messages/1001','{}','{}',NULL,'json','[]',30,0,'["message", "P2"]',2,true,1,'2026-05-25 02:07:00','success','2025-11-27 20:28:00','2026-06-01 10:57:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO api_test_cases(id,collection_id,project_id,user_id,environment_id,name,description,method,url,headers,params,body,body_type,assertions,timeout,retry_count,tags,priority,is_enabled,sort_order,last_run_at,last_status,created_at,updated_at)VALUES(522,96,14,5,55,'搜索商品','验证搜索商品','GET','/api/v1/search','{}','{}',NULL,'json','[]',30,0,'["search", "P1"]',3,true,2,'2026-05-22 06:57:00','success','2026-04-30 19:41:00','2026-06-01 19:39:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO api_test_cases(id,collection_id,project_id,user_id,environment_id,name,description,method,url,headers,params,body,body_type,assertions,timeout,retry_count,tags,priority,is_enabled,sort_order,last_run_at,last_status,created_at,updated_at)VALUES(523,96,14,2,54,'取消订单','验证取消订单','POST','/api/v1/orders/1001/cancel','{}','{}',NULL,'json','[]',30,0,'["order", "P1"]',3,true,3,'2026-05-23 12:10:00','success','2026-01-05 12:52:00','2026-05-29 17:13:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO api_test_cases(id,collection_id,project_id,user_id,environment_id,name,description,method,url,headers,params,body,body_type,assertions,timeout,retry_count,tags,priority,is_enabled,sort_order,last_run_at,last_status,created_at,updated_at)VALUES(524,96,14,2,53,'申请退款','验证申请退款','POST','/api/v1/refunds','{}','{}',NULL,'json','[]',30,0,'["payment", "P1"]',1,true,4,'2026-05-26 22:31:00','success','2026-04-24 11:33:00','2026-05-30 07:55:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO api_test_cases(id,collection_id,project_id,user_id,environment_id,name,description,method,url,headers,params,body,body_type,assertions,timeout,retry_count,tags,priority,is_enabled,sort_order,last_run_at,last_status,created_at,updated_at)VALUES(525,96,14,1,56,'用户信息','验证用户信息','GET','/api/v1/users/me','{}','{}',NULL,'json','[]',30,0,'["user", "P0"]',1,true,5,'2026-05-18 03:32:00','running','2026-02-26 12:27:00','2026-05-29 15:25:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO api_test_cases(id,collection_id,project_id,user_id,environment_id,name,description,method,url,headers,params,body,body_type,assertions,timeout,retry_count,tags,priority,is_enabled,sort_order,last_run_at,last_status,created_at,updated_at)VALUES(526,96,14,7,56,'用户登录','验证用户登录','POST','/api/v1/auth/login','{}','{}',NULL,'json','[]',30,0,'["auth", "P0"]',2,true,6,'2026-05-17 13:33:00','running','2025-12-06 18:14:00','2026-05-30 04:51:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO api_test_cases(id,collection_id,project_id,user_id,environment_id,name,description,method,url,headers,params,body,body_type,assertions,timeout,retry_count,tags,priority,is_enabled,sort_order,last_run_at,last_status,created_at,updated_at)VALUES(527,97,14,6,56,'创建订单','验证创建订单','POST','/api/v1/orders','{}','{}',NULL,'json','[]',30,0,'["order", "P0"]',1,true,0,'2026-05-27 16:37:00','success','2025-12-28 20:53:00','2026-06-01 22:24:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO api_test_cases(id,collection_id,project_id,user_id,environment_id,name,description,method,url,headers,params,body,body_type,assertions,timeout,retry_count,tags,priority,is_enabled,sort_order,last_run_at,last_status,created_at,updated_at)VALUES(528,97,14,5,53,'获取配置','验证获取配置','GET','/api/v1/config','{}','{}',NULL,'json','[]',30,0,'["config", "P2"]',2,true,1,'2026-05-29 22:41:00','success','2026-03-16 00:29:00','2026-06-02 05:51:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO api_test_cases(id,collection_id,project_id,user_id,environment_id,name,description,method,url,headers,params,body,body_type,assertions,timeout,retry_count,tags,priority,is_enabled,sort_order,last_run_at,last_status,created_at,updated_at)VALUES(529,97,14,7,56,'上传图片','验证上传图片','POST','/api/v1/upload','{}','{}',NULL,'json','[]',30,0,'["upload", "P1"]',1,true,2,'2026-05-24 00:47:00','success','2025-11-03 10:29:00','2026-06-02 06:25:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO api_test_cases(id,collection_id,project_id,user_id,environment_id,name,description,method,url,headers,params,body,body_type,assertions,timeout,retry_count,tags,priority,is_enabled,sort_order,last_run_at,last_status,created_at,updated_at)VALUES(530,97,14,5,53,'健康检查','验证健康检查','GET','/api/v1/health','{}','{}',NULL,'json','[]',30,0,'["health", "P0"]',2,true,3,'2026-05-19 18:24:00','running','2026-01-07 19:03:00','2026-05-30 21:30:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO api_test_cases(id,collection_id,project_id,user_id,environment_id,name,description,method,url,headers,params,body,body_type,assertions,timeout,retry_count,tags,priority,is_enabled,sort_order,last_run_at,last_status,created_at,updated_at)VALUES(531,97,14,7,54,'商品列表','验证商品列表','GET','/api/v1/products','{}','{}',NULL,'json','[]',30,0,'["product", "P0"]',2,true,4,'2026-05-18 19:18:00','failed','2026-04-23 10:40:00','2026-06-01 14:18:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO api_test_cases(id,collection_id,project_id,user_id,environment_id,name,description,method,url,headers,params,body,body_type,assertions,timeout,retry_count,tags,priority,is_enabled,sort_order,last_run_at,last_status,created_at,updated_at)VALUES(532,97,14,7,56,'标记已读','验证标记已读','PUT','/api/v1/messages/1001','{}','{}',NULL,'json','[]',30,0,'["message", "P2"]',1,true,5,'2026-05-20 23:26:00','success','2025-12-11 19:13:00','2026-05-30 13:55:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO api_test_cases(id,collection_id,project_id,user_id,environment_id,name,description,method,url,headers,params,body,body_type,assertions,timeout,retry_count,tags,priority,is_enabled,sort_order,last_run_at,last_status,created_at,updated_at)VALUES(533,97,14,2,53,'领取券','验证领取券','POST','/api/v1/coupons/1001','{}','{}',NULL,'json','[]',30,0,'["marketing", "P1"]',1,true,6,'2026-05-23 16:19:00','success','2025-12-18 16:55:00','2026-05-31 14:26:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO api_test_cases(id,collection_id,project_id,user_id,environment_id,name,description,method,url,headers,params,body,body_type,assertions,timeout,retry_count,tags,priority,is_enabled,sort_order,last_run_at,last_status,created_at,updated_at)VALUES(534,98,14,1,54,'用户信息','验证用户信息','GET','/api/v1/users/me','{}','{}',NULL,'json','[]',30,0,'["user", "P0"]',2,true,0,NULL,'pending','2025-11-12 03:45:00','2026-05-30 07:09:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO api_test_cases(id,collection_id,project_id,user_id,environment_id,name,description,method,url,headers,params,body,body_type,assertions,timeout,retry_count,tags,priority,is_enabled,sort_order,last_run_at,last_status,created_at,updated_at)VALUES(535,98,14,7,55,'领取券','验证领取券','POST','/api/v1/coupons/1001','{}','{}',NULL,'json','[]',30,0,'["marketing", "P1"]',1,true,1,'2026-05-31 18:05:00','success','2026-03-05 20:49:00','2026-05-30 09:05:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO api_test_cases(id,collection_id,project_id,user_id,environment_id,name,description,method,url,headers,params,body,body_type,assertions,timeout,retry_count,tags,priority,is_enabled,sort_order,last_run_at,last_status,created_at,updated_at)VALUES(536,98,14,7,55,'提交反馈','验证提交反馈','POST','/api/v1/feedback','{}','{}',NULL,'json','[]',30,0,'["feedback", "P2"]',2,true,2,'2026-05-31 06:54:00','success','2026-04-19 00:51:00','2026-06-01 01:11:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO api_test_cases(id,collection_id,project_id,user_id,environment_id,name,description,method,url,headers,params,body,body_type,assertions,timeout,retry_count,tags,priority,is_enabled,sort_order,last_run_at,last_status,created_at,updated_at)VALUES(537,98,14,1,54,'取消订单','验证取消订单','POST','/api/v1/orders/1001/cancel','{}','{}',NULL,'json','[]',30,0,'["order", "P1"]',1,true,3,'2026-05-19 12:50:00','success','2025-12-25 23:49:00','2026-06-01 11:57:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO api_test_cases(id,collection_id,project_id,user_id,environment_id,name,description,method,url,headers,params,body,body_type,assertions,timeout,retry_count,tags,priority,is_enabled,sort_order,last_run_at,last_status,created_at,updated_at)VALUES(538,98,14,5,56,'获取配置','验证获取配置','GET','/api/v1/config','{}','{}',NULL,'json','[]',30,0,'["config", "P2"]',2,true,4,'2026-05-28 20:03:00','success','2026-03-26 21:08:00','2026-06-02 08:48:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO api_test_cases(id,collection_id,project_id,user_id,environment_id,name,description,method,url,headers,params,body,body_type,assertions,timeout,retry_count,tags,priority,is_enabled,sort_order,last_run_at,last_status,created_at,updated_at)VALUES(539,98,14,2,54,'支付状态','验证支付状态','GET','/api/v1/payments/1001','{}','{}',NULL,'json','[]',30,0,'["payment", "P1"]',1,true,5,'2026-05-21 06:43:00','success','2026-03-11 19:25:00','2026-05-30 07:30:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO api_test_cases(id,collection_id,project_id,user_id,environment_id,name,description,method,url,headers,params,body,body_type,assertions,timeout,retry_count,tags,priority,is_enabled,sort_order,last_run_at,last_status,created_at,updated_at)VALUES(540,98,14,1,56,'用户登录','验证用户登录','POST','/api/v1/auth/login','{}','{}',NULL,'json','[]',30,0,'["auth", "P0"]',2,true,6,'2026-06-02 01:25:00','success','2025-12-11 06:45:00','2026-06-01 00:24:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO api_test_cases(id,collection_id,project_id,user_id,environment_id,name,description,method,url,headers,params,body,body_type,assertions,timeout,retry_count,tags,priority,is_enabled,sort_order,last_run_at,last_status,created_at,updated_at)VALUES(541,99,15,7,58,'上传图片','验证上传图片','POST','/api/v1/upload','{}','{}',NULL,'json','[]',30,0,'["upload", "P1"]',1,true,0,'2026-05-19 16:32:00','failed','2026-05-31 19:07:00','2026-05-30 13:50:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO api_test_cases(id,collection_id,project_id,user_id,environment_id,name,description,method,url,headers,params,body,body_type,assertions,timeout,retry_count,tags,priority,is_enabled,sort_order,last_run_at,last_status,created_at,updated_at)VALUES(542,99,15,1,57,'更新资料','验证更新资料','PUT','/api/v1/users/me','{}','{}',NULL,'json','[]',30,0,'["user", "P1"]',2,true,1,NULL,'pending','2026-03-23 14:44:00','2026-05-29 22:07:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO api_test_cases(id,collection_id,project_id,user_id,environment_id,name,description,method,url,headers,params,body,body_type,assertions,timeout,retry_count,tags,priority,is_enabled,sort_order,last_run_at,last_status,created_at,updated_at)VALUES(543,99,15,2,59,'提交反馈','验证提交反馈','POST','/api/v1/feedback','{}','{}',NULL,'json','[]',30,0,'["feedback", "P2"]',2,true,2,'2026-05-31 00:55:00','success','2025-12-05 06:07:00','2026-05-31 10:25:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO api_test_cases(id,collection_id,project_id,user_id,environment_id,name,description,method,url,headers,params,body,body_type,assertions,timeout,retry_count,tags,priority,is_enabled,sort_order,last_run_at,last_status,created_at,updated_at)VALUES(544,99,15,5,60,'取消订单','验证取消订单','POST','/api/v1/orders/1001/cancel','{}','{}',NULL,'json','[]',30,0,'["order", "P1"]',3,true,3,'2026-05-22 12:39:00','success','2026-03-26 11:32:00','2026-05-31 02:18:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO api_test_cases(id,collection_id,project_id,user_id,environment_id,name,description,method,url,headers,params,body,body_type,assertions,timeout,retry_count,tags,priority,is_enabled,sort_order,last_run_at,last_status,created_at,updated_at)VALUES(545,99,15,5,59,'创建订单','验证创建订单','POST','/api/v1/orders','{}','{}',NULL,'json','[]',30,0,'["order", "P0"]',3,true,4,'2026-05-23 09:02:00','success','2026-04-27 13:01:00','2026-06-01 14:30:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO api_test_cases(id,collection_id,project_id,user_id,environment_id,name,description,method,url,headers,params,body,body_type,assertions,timeout,retry_count,tags,priority,is_enabled,sort_order,last_run_at,last_status,created_at,updated_at)VALUES(546,99,15,1,57,'订单详情','验证订单详情','GET','/api/v1/orders/1001','{}','{}',NULL,'json','[]',30,0,'["order", "P0"]',3,true,5,'2026-05-19 16:03:00','failed','2025-12-02 18:12:00','2026-05-29 16:55:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO api_test_cases(id,collection_id,project_id,user_id,environment_id,name,description,method,url,headers,params,body,body_type,assertions,timeout,retry_count,tags,priority,is_enabled,sort_order,last_run_at,last_status,created_at,updated_at)VALUES(547,100,15,7,59,'更新资料','验证更新资料','PUT','/api/v1/users/me','{}','{}',NULL,'json','[]',30,0,'["user", "P1"]',2,true,0,'2026-06-02 06:31:00','success','2026-04-12 20:00:00','2026-05-31 10:59:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO api_test_cases(id,collection_id,project_id,user_id,environment_id,name,description,method,url,headers,params,body,body_type,assertions,timeout,retry_count,tags,priority,is_enabled,sort_order,last_run_at,last_status,created_at,updated_at)VALUES(548,100,15,5,59,'优惠券','验证优惠券','GET','/api/v1/coupons','{}','{}',NULL,'json','[]',30,0,'["marketing", "P1"]',1,true,1,'2026-05-23 11:46:00','success','2026-01-25 22:58:00','2026-05-30 18:03:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO api_test_cases(id,collection_id,project_id,user_id,environment_id,name,description,method,url,headers,params,body,body_type,assertions,timeout,retry_count,tags,priority,is_enabled,sort_order,last_run_at,last_status,created_at,updated_at)VALUES(549,100,15,7,58,'用户登录','验证用户登录','POST','/api/v1/auth/login','{}','{}',NULL,'json','[]',30,0,'["auth", "P0"]',2,true,2,'2026-05-21 06:05:00','success','2026-01-06 17:29:00','2026-05-31 16:48:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO api_test_cases(id,collection_id,project_id,user_id,environment_id,name,description,method,url,headers,params,body,body_type,assertions,timeout,retry_count,tags,priority,is_enabled,sort_order,last_run_at,last_status,created_at,updated_at)VALUES(550,100,15,7,58,'上传图片','验证上传图片','POST','/api/v1/upload','{}','{}',NULL,'json','[]',30,0,'["upload", "P1"]',1,true,3,'2026-05-28 10:56:00','success','2026-03-26 15:06:00','2026-05-31 17:14:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO api_test_cases(id,collection_id,project_id,user_id,environment_id,name,description,method,url,headers,params,body,body_type,assertions,timeout,retry_count,tags,priority,is_enabled,sort_order,last_run_at,last_status,created_at,updated_at)VALUES(551,100,15,5,58,'商品列表','验证商品列表','GET','/api/v1/products','{}','{}',NULL,'json','[]',30,0,'["product", "P0"]',2,true,4,'2026-06-01 11:17:00','failed','2025-12-26 01:17:00','2026-05-30 09:33:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO api_test_cases(id,collection_id,project_id,user_id,environment_id,name,description,method,url,headers,params,body,body_type,assertions,timeout,retry_count,tags,priority,is_enabled,sort_order,last_run_at,last_status,created_at,updated_at)VALUES(552,100,15,1,59,'订单详情','验证订单详情','GET','/api/v1/orders/1001','{}','{}',NULL,'json','[]',30,0,'["order", "P0"]',3,true,5,'2026-05-20 01:53:00','success','2026-01-19 19:29:00','2026-05-30 17:12:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO api_test_cases(id,collection_id,project_id,user_id,environment_id,name,description,method,url,headers,params,body,body_type,assertions,timeout,retry_count,tags,priority,is_enabled,sort_order,last_run_at,last_status,created_at,updated_at)VALUES(553,100,15,1,58,'推荐列表','验证推荐列表','GET','/api/v1/recommendations','{}','{}',NULL,'json','[]',30,0,'["recommendation", "P2"]',2,true,6,'2026-05-19 16:32:00','success','2026-05-30 21:48:00','2026-05-31 07:04:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO api_test_cases(id,collection_id,project_id,user_id,environment_id,name,description,method,url,headers,params,body,body_type,assertions,timeout,retry_count,tags,priority,is_enabled,sort_order,last_run_at,last_status,created_at,updated_at)VALUES(554,100,15,7,57,'取消订单','验证取消订单','POST','/api/v1/orders/1001/cancel','{}','{}',NULL,'json','[]',30,0,'["order", "P1"]',1,true,7,'2026-05-25 11:33:00','cancelled','2026-03-30 03:50:00','2026-05-31 00:56:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO api_test_cases(id,collection_id,project_id,user_id,environment_id,name,description,method,url,headers,params,body,body_type,assertions,timeout,retry_count,tags,priority,is_enabled,sort_order,last_run_at,last_status,created_at,updated_at)VALUES(555,101,15,5,59,'商品列表','验证商品列表','GET','/api/v1/products','{}','{}',NULL,'json','[]',30,0,'["product", "P0"]',1,true,0,'2026-05-18 02:39:00','success','2026-03-07 17:10:00','2026-06-01 07:11:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO api_test_cases(id,collection_id,project_id,user_id,environment_id,name,description,method,url,headers,params,body,body_type,assertions,timeout,retry_count,tags,priority,is_enabled,sort_order,last_run_at,last_status,created_at,updated_at)VALUES(556,101,15,7,60,'用户登录','验证用户登录','POST','/api/v1/auth/login','{}','{}',NULL,'json','[]',30,0,'["auth", "P0"]',1,true,1,'2026-05-18 15:53:00','failed','2026-05-17 08:36:00','2026-05-30 11:56:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO api_test_cases(id,collection_id,project_id,user_id,environment_id,name,description,method,url,headers,params,body,body_type,assertions,timeout,retry_count,tags,priority,is_enabled,sort_order,last_run_at,last_status,created_at,updated_at)VALUES(557,101,15,2,57,'获取配置','验证获取配置','GET','/api/v1/config','{}','{}',NULL,'json','[]',30,0,'["config", "P2"]',2,true,2,'2026-05-19 08:41:00','running','2025-12-22 20:56:00','2026-06-01 12:57:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO api_test_cases(id,collection_id,project_id,user_id,environment_id,name,description,method,url,headers,params,body,body_type,assertions,timeout,retry_count,tags,priority,is_enabled,sort_order,last_run_at,last_status,created_at,updated_at)VALUES(558,101,15,7,57,'推荐列表','验证推荐列表','GET','/api/v1/recommendations','{}','{}',NULL,'json','[]',30,0,'["recommendation", "P2"]',2,true,3,'2026-05-20 21:54:00','success','2025-11-20 20:46:00','2026-06-01 19:36:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO api_test_cases(id,collection_id,project_id,user_id,environment_id,name,description,method,url,headers,params,body,body_type,assertions,timeout,retry_count,tags,priority,is_enabled,sort_order,last_run_at,last_status,created_at,updated_at)VALUES(559,101,15,6,60,'领取券','验证领取券','POST','/api/v1/coupons/1001','{}','{}',NULL,'json','[]',30,0,'["marketing", "P1"]',3,true,4,'2026-05-29 23:19:00','running','2025-11-13 09:31:00','2026-05-30 15:48:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO api_test_cases(id,collection_id,project_id,user_id,environment_id,name,description,method,url,headers,params,body,body_type,assertions,timeout,retry_count,tags,priority,is_enabled,sort_order,last_run_at,last_status,created_at,updated_at)VALUES(560,101,15,1,57,'申请退款','验证申请退款','POST','/api/v1/refunds','{}','{}',NULL,'json','[]',30,0,'["payment", "P1"]',1,true,5,'2026-05-30 15:10:00','success','2026-01-06 05:20:00','2026-05-30 22:34:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO api_test_cases(id,collection_id,project_id,user_id,environment_id,name,description,method,url,headers,params,body,body_type,assertions,timeout,retry_count,tags,priority,is_enabled,sort_order,last_run_at,last_status,created_at,updated_at)VALUES(561,101,15,6,60,'搜索商品','验证搜索商品','GET','/api/v1/search','{}','{}',NULL,'json','[]',30,0,'["search", "P1"]',1,true,6,'2026-05-29 08:57:00','success','2026-03-13 15:33:00','2026-05-31 00:23:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO api_test_cases(id,collection_id,project_id,user_id,environment_id,name,description,method,url,headers,params,body,body_type,assertions,timeout,retry_count,tags,priority,is_enabled,sort_order,last_run_at,last_status,created_at,updated_at)VALUES(562,101,15,7,58,'消息列表','验证消息列表','GET','/api/v1/messages','{}','{}',NULL,'json','[]',30,0,'["message", "P1"]',2,true,7,'2026-05-23 14:39:00','success','2026-02-27 09:27:00','2026-06-01 08:45:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO api_test_cases(id,collection_id,project_id,user_id,environment_id,name,description,method,url,headers,params,body,body_type,assertions,timeout,retry_count,tags,priority,is_enabled,sort_order,last_run_at,last_status,created_at,updated_at)VALUES(563,102,15,2,57,'优惠券','验证优惠券','GET','/api/v1/coupons','{}','{}',NULL,'json','[]',30,0,'["marketing", "P1"]',2,true,0,'2026-05-17 11:16:00','success','2025-12-29 11:39:00','2026-05-30 14:41:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO api_test_cases(id,collection_id,project_id,user_id,environment_id,name,description,method,url,headers,params,body,body_type,assertions,timeout,retry_count,tags,priority,is_enabled,sort_order,last_run_at,last_status,created_at,updated_at)VALUES(564,102,15,6,59,'用户信息','验证用户信息','GET','/api/v1/users/me','{}','{}',NULL,'json','[]',30,0,'["user", "P0"]',1,true,1,'2026-05-19 08:29:00','success','2026-05-31 13:46:00','2026-05-31 19:21:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO api_test_cases(id,collection_id,project_id,user_id,environment_id,name,description,method,url,headers,params,body,body_type,assertions,timeout,retry_count,tags,priority,is_enabled,sort_order,last_run_at,last_status,created_at,updated_at)VALUES(565,102,15,2,58,'推荐列表','验证推荐列表','GET','/api/v1/recommendations','{}','{}',NULL,'json','[]',30,0,'["recommendation", "P2"]',1,true,2,'2026-05-22 10:36:00','success','2026-02-19 04:08:00','2026-06-01 23:00:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO api_test_cases(id,collection_id,project_id,user_id,environment_id,name,description,method,url,headers,params,body,body_type,assertions,timeout,retry_count,tags,priority,is_enabled,sort_order,last_run_at,last_status,created_at,updated_at)VALUES(566,102,15,1,59,'标记已读','验证标记已读','PUT','/api/v1/messages/1001','{}','{}',NULL,'json','[]',30,0,'["message", "P2"]',2,true,3,'2026-05-30 05:42:00','success','2026-04-12 13:23:00','2026-05-31 08:59:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO api_test_cases(id,collection_id,project_id,user_id,environment_id,name,description,method,url,headers,params,body,body_type,assertions,timeout,retry_count,tags,priority,is_enabled,sort_order,last_run_at,last_status,created_at,updated_at)VALUES(567,102,15,2,58,'取消订单','验证取消订单','POST','/api/v1/orders/1001/cancel','{}','{}',NULL,'json','[]',30,0,'["order", "P1"]',1,true,4,'2026-05-26 01:14:00','success','2026-03-06 16:45:00','2026-06-01 03:59:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO api_test_cases(id,collection_id,project_id,user_id,environment_id,name,description,method,url,headers,params,body,body_type,assertions,timeout,retry_count,tags,priority,is_enabled,sort_order,last_run_at,last_status,created_at,updated_at)VALUES(568,102,15,2,59,'商品列表','验证商品列表','GET','/api/v1/products','{}','{}',NULL,'json','[]',30,0,'["product", "P0"]',2,true,5,'2026-06-01 12:52:00','running','2025-12-16 06:39:00','2026-06-01 00:31:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO api_test_cases(id,collection_id,project_id,user_id,environment_id,name,description,method,url,headers,params,body,body_type,assertions,timeout,retry_count,tags,priority,is_enabled,sort_order,last_run_at,last_status,created_at,updated_at)VALUES(569,102,15,2,59,'消息列表','验证消息列表','GET','/api/v1/messages','{}','{}',NULL,'json','[]',30,0,'["message", "P1"]',2,true,6,'2026-05-27 17:09:00','failed','2026-02-09 11:56:00','2026-06-02 05:04:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO api_test_cases(id,collection_id,project_id,user_id,environment_id,name,description,method,url,headers,params,body,body_type,assertions,timeout,retry_count,tags,priority,is_enabled,sort_order,last_run_at,last_status,created_at,updated_at)VALUES(570,103,15,5,59,'取消订单','验证取消订单','POST','/api/v1/orders/1001/cancel','{}','{}',NULL,'json','[]',30,0,'["order", "P1"]',2,true,0,'2026-05-26 08:12:00','success','2026-01-02 03:06:00','2026-05-31 05:40:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO api_test_cases(id,collection_id,project_id,user_id,environment_id,name,description,method,url,headers,params,body,body_type,assertions,timeout,retry_count,tags,priority,is_enabled,sort_order,last_run_at,last_status,created_at,updated_at)VALUES(571,103,15,2,57,'健康检查','验证健康检查','GET','/api/v1/health','{}','{}',NULL,'json','[]',30,0,'["health", "P0"]',2,true,1,'2026-05-25 05:06:00','success','2026-01-02 18:47:00','2026-06-01 18:10:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO api_test_cases(id,collection_id,project_id,user_id,environment_id,name,description,method,url,headers,params,body,body_type,assertions,timeout,retry_count,tags,priority,is_enabled,sort_order,last_run_at,last_status,created_at,updated_at)VALUES(572,103,15,7,57,'优惠券','验证优惠券','GET','/api/v1/coupons','{}','{}',NULL,'json','[]',30,0,'["marketing", "P1"]',2,true,2,'2026-05-20 13:12:00','success','2026-02-25 18:27:00','2026-05-30 04:40:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO api_test_cases(id,collection_id,project_id,user_id,environment_id,name,description,method,url,headers,params,body,body_type,assertions,timeout,retry_count,tags,priority,is_enabled,sort_order,last_run_at,last_status,created_at,updated_at)VALUES(573,103,15,5,60,'搜索商品','验证搜索商品','GET','/api/v1/search','{}','{}',NULL,'json','[]',30,0,'["search", "P1"]',2,true,3,'2026-05-17 18:43:00','failed','2026-02-18 13:02:00','2026-06-02 03:46:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO api_test_cases(id,collection_id,project_id,user_id,environment_id,name,description,method,url,headers,params,body,body_type,assertions,timeout,retry_count,tags,priority,is_enabled,sort_order,last_run_at,last_status,created_at,updated_at)VALUES(574,104,15,5,60,'上传图片','验证上传图片','POST','/api/v1/upload','{}','{}',NULL,'json','[]',30,0,'["upload", "P1"]',2,true,0,'2026-05-27 22:44:00','running','2026-05-11 05:12:00','2026-06-02 00:32:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO api_test_cases(id,collection_id,project_id,user_id,environment_id,name,description,method,url,headers,params,body,body_type,assertions,timeout,retry_count,tags,priority,is_enabled,sort_order,last_run_at,last_status,created_at,updated_at)VALUES(575,104,15,7,59,'发起支付','验证发起支付','POST','/api/v1/payments','{}','{}',NULL,'json','[]',30,0,'["payment", "P0"]',2,true,1,'2026-05-31 19:28:00','success','2026-03-06 20:32:00','2026-05-29 20:34:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO api_test_cases(id,collection_id,project_id,user_id,environment_id,name,description,method,url,headers,params,body,body_type,assertions,timeout,retry_count,tags,priority,is_enabled,sort_order,last_run_at,last_status,created_at,updated_at)VALUES(576,104,15,5,60,'搜索商品','验证搜索商品','GET','/api/v1/search','{}','{}',NULL,'json','[]',30,0,'["search", "P1"]',2,true,2,'2026-05-21 09:49:00','success','2026-04-03 01:19:00','2026-06-01 22:03:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO api_test_cases(id,collection_id,project_id,user_id,environment_id,name,description,method,url,headers,params,body,body_type,assertions,timeout,retry_count,tags,priority,is_enabled,sort_order,last_run_at,last_status,created_at,updated_at)VALUES(577,104,15,1,59,'取消订单','验证取消订单','POST','/api/v1/orders/1001/cancel','{}','{}',NULL,'json','[]',30,0,'["order", "P1"]',1,true,3,'2026-05-31 01:01:00','failed','2026-05-07 06:56:00','2026-05-31 08:26:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO api_test_cases(id,collection_id,project_id,user_id,environment_id,name,description,method,url,headers,params,body,body_type,assertions,timeout,retry_count,tags,priority,is_enabled,sort_order,last_run_at,last_status,created_at,updated_at)VALUES(578,105,16,5,63,'消息列表','验证消息列表','GET','/api/v1/messages','{}','{}',NULL,'json','[]',30,0,'["message", "P1"]',2,true,0,'2026-05-28 11:13:00','success','2026-03-27 09:11:00','2026-05-31 00:08:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO api_test_cases(id,collection_id,project_id,user_id,environment_id,name,description,method,url,headers,params,body,body_type,assertions,timeout,retry_count,tags,priority,is_enabled,sort_order,last_run_at,last_status,created_at,updated_at)VALUES(579,105,16,5,64,'取消订单','验证取消订单','POST','/api/v1/orders/1001/cancel','{}','{}',NULL,'json','[]',30,0,'["order", "P1"]',2,true,1,NULL,'pending','2025-11-19 14:00:00','2026-05-29 13:28:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO api_test_cases(id,collection_id,project_id,user_id,environment_id,name,description,method,url,headers,params,body,body_type,assertions,timeout,retry_count,tags,priority,is_enabled,sort_order,last_run_at,last_status,created_at,updated_at)VALUES(580,105,16,2,64,'健康检查','验证健康检查','GET','/api/v1/health','{}','{}',NULL,'json','[]',30,0,'["health", "P0"]',2,true,2,'2026-05-26 18:46:00','success','2026-01-01 16:12:00','2026-05-29 10:08:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO api_test_cases(id,collection_id,project_id,user_id,environment_id,name,description,method,url,headers,params,body,body_type,assertions,timeout,retry_count,tags,priority,is_enabled,sort_order,last_run_at,last_status,created_at,updated_at)VALUES(581,105,16,6,63,'支付状态','验证支付状态','GET','/api/v1/payments/1001','{}','{}',NULL,'json','[]',30,0,'["payment", "P1"]',3,true,3,'2026-05-23 03:33:00','failed','2026-02-15 03:32:00','2026-05-29 16:59:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO api_test_cases(id,collection_id,project_id,user_id,environment_id,name,description,method,url,headers,params,body,body_type,assertions,timeout,retry_count,tags,priority,is_enabled,sort_order,last_run_at,last_status,created_at,updated_at)VALUES(582,106,16,6,63,'创建订单','验证创建订单','POST','/api/v1/orders','{}','{}',NULL,'json','[]',30,0,'["order", "P0"]',2,true,0,'2026-05-19 20:17:00','success','2025-11-17 11:26:00','2026-05-30 23:23:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO api_test_cases(id,collection_id,project_id,user_id,environment_id,name,description,method,url,headers,params,body,body_type,assertions,timeout,retry_count,tags,priority,is_enabled,sort_order,last_run_at,last_status,created_at,updated_at)VALUES(583,106,16,1,61,'领取券','验证领取券','POST','/api/v1/coupons/1001','{}','{}',NULL,'json','[]',30,0,'["marketing", "P1"]',1,true,1,NULL,'pending','2026-03-08 15:20:00','2026-05-29 21:47:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO api_test_cases(id,collection_id,project_id,user_id,environment_id,name,description,method,url,headers,params,body,body_type,assertions,timeout,retry_count,tags,priority,is_enabled,sort_order,last_run_at,last_status,created_at,updated_at)VALUES(584,106,16,6,61,'健康检查','验证健康检查','GET','/api/v1/health','{}','{}',NULL,'json','[]',30,0,'["health", "P0"]',2,true,2,'2026-05-26 18:54:00','success','2026-01-06 19:20:00','2026-05-31 07:50:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO api_test_cases(id,collection_id,project_id,user_id,environment_id,name,description,method,url,headers,params,body,body_type,assertions,timeout,retry_count,tags,priority,is_enabled,sort_order,last_run_at,last_status,created_at,updated_at)VALUES(585,106,16,1,62,'申请退款','验证申请退款','POST','/api/v1/refunds','{}','{}',NULL,'json','[]',30,0,'["payment", "P1"]',1,true,3,'2026-05-18 09:49:00','success','2026-05-14 21:42:00','2026-06-01 02:42:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO api_test_cases(id,collection_id,project_id,user_id,environment_id,name,description,method,url,headers,params,body,body_type,assertions,timeout,retry_count,tags,priority,is_enabled,sort_order,last_run_at,last_status,created_at,updated_at)VALUES(586,106,16,7,61,'用户登录','验证用户登录','POST','/api/v1/auth/login','{}','{}',NULL,'json','[]',30,0,'["auth", "P0"]',1,true,4,'2026-05-21 18:00:00','success','2026-03-09 20:35:00','2026-06-01 06:52:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO api_test_cases(id,collection_id,project_id,user_id,environment_id,name,description,method,url,headers,params,body,body_type,assertions,timeout,retry_count,tags,priority,is_enabled,sort_order,last_run_at,last_status,created_at,updated_at)VALUES(587,107,16,2,63,'推荐列表','验证推荐列表','GET','/api/v1/recommendations','{}','{}',NULL,'json','[]',30,0,'["recommendation", "P2"]',2,true,0,'2026-05-18 04:22:00','success','2026-03-13 15:48:00','2026-05-30 01:48:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO api_test_cases(id,collection_id,project_id,user_id,environment_id,name,description,method,url,headers,params,body,body_type,assertions,timeout,retry_count,tags,priority,is_enabled,sort_order,last_run_at,last_status,created_at,updated_at)VALUES(588,107,16,1,62,'获取配置','验证获取配置','GET','/api/v1/config','{}','{}',NULL,'json','[]',30,0,'["config", "P2"]',1,true,1,'2026-05-20 14:09:00','success','2026-01-17 23:02:00','2026-05-29 19:31:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO api_test_cases(id,collection_id,project_id,user_id,environment_id,name,description,method,url,headers,params,body,body_type,assertions,timeout,retry_count,tags,priority,is_enabled,sort_order,last_run_at,last_status,created_at,updated_at)VALUES(589,107,16,7,61,'更新资料','验证更新资料','PUT','/api/v1/users/me','{}','{}',NULL,'json','[]',30,0,'["user", "P1"]',2,true,2,'2026-05-23 13:04:00','failed','2026-03-04 11:07:00','2026-05-30 21:21:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO api_test_cases(id,collection_id,project_id,user_id,environment_id,name,description,method,url,headers,params,body,body_type,assertions,timeout,retry_count,tags,priority,is_enabled,sort_order,last_run_at,last_status,created_at,updated_at)VALUES(590,107,16,2,64,'搜索商品','验证搜索商品','GET','/api/v1/search','{}','{}',NULL,'json','[]',30,0,'["search", "P1"]',3,true,3,'2026-05-19 19:36:00','success','2026-04-15 11:24:00','2026-06-01 21:16:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO api_test_cases(id,collection_id,project_id,user_id,environment_id,name,description,method,url,headers,params,body,body_type,assertions,timeout,retry_count,tags,priority,is_enabled,sort_order,last_run_at,last_status,created_at,updated_at)VALUES(591,107,16,1,62,'取消订单','验证取消订单','POST','/api/v1/orders/1001/cancel','{}','{}',NULL,'json','[]',30,0,'["order", "P1"]',3,true,4,'2026-05-28 01:04:00','running','2026-01-15 00:18:00','2026-06-01 11:14:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO api_test_cases(id,collection_id,project_id,user_id,environment_id,name,description,method,url,headers,params,body,body_type,assertions,timeout,retry_count,tags,priority,is_enabled,sort_order,last_run_at,last_status,created_at,updated_at)VALUES(592,107,16,2,64,'优惠券','验证优惠券','GET','/api/v1/coupons','{}','{}',NULL,'json','[]',30,0,'["marketing", "P1"]',1,true,5,'2026-05-29 22:56:00','success','2026-01-22 23:34:00','2026-05-30 04:44:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO api_test_cases(id,collection_id,project_id,user_id,environment_id,name,description,method,url,headers,params,body,body_type,assertions,timeout,retry_count,tags,priority,is_enabled,sort_order,last_run_at,last_status,created_at,updated_at)VALUES(593,107,16,2,61,'健康检查','验证健康检查','GET','/api/v1/health','{}','{}',NULL,'json','[]',30,0,'["health", "P0"]',3,true,6,'2026-05-30 13:16:00','success','2025-11-21 19:36:00','2026-05-30 10:35:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO api_test_cases(id,collection_id,project_id,user_id,environment_id,name,description,method,url,headers,params,body,body_type,assertions,timeout,retry_count,tags,priority,is_enabled,sort_order,last_run_at,last_status,created_at,updated_at)VALUES(594,108,16,1,62,'搜索商品','验证搜索商品','GET','/api/v1/search','{}','{}',NULL,'json','[]',30,0,'["search", "P1"]',1,true,0,'2026-05-18 18:31:00','success','2026-05-10 16:18:00','2026-05-31 11:32:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO api_test_cases(id,collection_id,project_id,user_id,environment_id,name,description,method,url,headers,params,body,body_type,assertions,timeout,retry_count,tags,priority,is_enabled,sort_order,last_run_at,last_status,created_at,updated_at)VALUES(595,108,16,2,64,'用户信息','验证用户信息','GET','/api/v1/users/me','{}','{}',NULL,'json','[]',30,0,'["user", "P0"]',1,true,1,'2026-05-28 04:07:00','failed','2025-12-28 06:49:00','2026-05-31 06:26:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO api_test_cases(id,collection_id,project_id,user_id,environment_id,name,description,method,url,headers,params,body,body_type,assertions,timeout,retry_count,tags,priority,is_enabled,sort_order,last_run_at,last_status,created_at,updated_at)VALUES(596,108,16,6,62,'用户登录','验证用户登录','POST','/api/v1/auth/login','{}','{}',NULL,'json','[]',30,0,'["auth", "P0"]',1,true,2,'2026-06-01 12:43:00','success','2026-02-08 22:49:00','2026-05-31 11:58:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO api_test_cases(id,collection_id,project_id,user_id,environment_id,name,description,method,url,headers,params,body,body_type,assertions,timeout,retry_count,tags,priority,is_enabled,sort_order,last_run_at,last_status,created_at,updated_at)VALUES(597,108,16,7,62,'支付状态','验证支付状态','GET','/api/v1/payments/1001','{}','{}',NULL,'json','[]',30,0,'["payment", "P1"]',2,true,3,'2026-05-31 13:09:00','success','2025-12-18 12:15:00','2026-06-01 21:16:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO api_test_cases(id,collection_id,project_id,user_id,environment_id,name,description,method,url,headers,params,body,body_type,assertions,timeout,retry_count,tags,priority,is_enabled,sort_order,last_run_at,last_status,created_at,updated_at)VALUES(598,109,16,2,62,'上传图片','验证上传图片','POST','/api/v1/upload','{}','{}',NULL,'json','[]',30,0,'["upload", "P1"]',1,true,0,'2026-05-26 03:55:00','success','2026-02-14 10:00:00','2026-05-31 03:17:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO api_test_cases(id,collection_id,project_id,user_id,environment_id,name,description,method,url,headers,params,body,body_type,assertions,timeout,retry_count,tags,priority,is_enabled,sort_order,last_run_at,last_status,created_at,updated_at)VALUES(599,109,16,1,62,'用户信息','验证用户信息','GET','/api/v1/users/me','{}','{}',NULL,'json','[]',30,0,'["user", "P0"]',1,true,1,NULL,'pending','2025-11-08 12:50:00','2026-06-01 08:34:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO api_test_cases(id,collection_id,project_id,user_id,environment_id,name,description,method,url,headers,params,body,body_type,assertions,timeout,retry_count,tags,priority,is_enabled,sort_order,last_run_at,last_status,created_at,updated_at)VALUES(600,109,16,7,61,'用户登录','验证用户登录','POST','/api/v1/auth/login','{}','{}',NULL,'json','[]',30,0,'["auth", "P0"]',1,true,2,'2026-05-22 16:20:00','failed','2025-12-24 03:01:00','2026-05-29 20:53:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO api_test_cases(id,collection_id,project_id,user_id,environment_id,name,description,method,url,headers,params,body,body_type,assertions,timeout,retry_count,tags,priority,is_enabled,sort_order,last_run_at,last_status,created_at,updated_at)VALUES(601,109,16,2,62,'领取券','验证领取券','POST','/api/v1/coupons/1001','{}','{}',NULL,'json','[]',30,0,'["marketing", "P1"]',2,true,3,'2026-05-23 05:00:00','success','2025-12-16 00:00:00','2026-05-30 03:31:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO api_test_cases(id,collection_id,project_id,user_id,environment_id,name,description,method,url,headers,params,body,body_type,assertions,timeout,retry_count,tags,priority,is_enabled,sort_order,last_run_at,last_status,created_at,updated_at)VALUES(602,109,16,2,61,'搜索商品','验证搜索商品','GET','/api/v1/search','{}','{}',NULL,'json','[]',30,0,'["search", "P1"]',2,true,4,'2026-05-24 13:21:00','failed','2026-05-21 07:04:00','2026-05-31 20:41:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO api_test_cases(id,collection_id,project_id,user_id,environment_id,name,description,method,url,headers,params,body,body_type,assertions,timeout,retry_count,tags,priority,is_enabled,sort_order,last_run_at,last_status,created_at,updated_at)VALUES(603,110,16,5,64,'获取配置','验证获取配置','GET','/api/v1/config','{}','{}',NULL,'json','[]',30,0,'["config", "P2"]',3,true,0,'2026-05-28 23:49:00','failed','2025-11-18 11:40:00','2026-05-30 07:39:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO api_test_cases(id,collection_id,project_id,user_id,environment_id,name,description,method,url,headers,params,body,body_type,assertions,timeout,retry_count,tags,priority,is_enabled,sort_order,last_run_at,last_status,created_at,updated_at)VALUES(604,110,16,1,64,'商品列表','验证商品列表','GET','/api/v1/products','{}','{}',NULL,'json','[]',30,0,'["product", "P0"]',3,true,1,'2026-05-25 17:23:00','success','2026-05-29 02:59:00','2026-06-02 00:45:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO api_test_cases(id,collection_id,project_id,user_id,environment_id,name,description,method,url,headers,params,body,body_type,assertions,timeout,retry_count,tags,priority,is_enabled,sort_order,last_run_at,last_status,created_at,updated_at)VALUES(605,110,16,6,62,'优惠券','验证优惠券','GET','/api/v1/coupons','{}','{}',NULL,'json','[]',30,0,'["marketing", "P1"]',2,true,2,'2026-06-01 05:37:00','success','2026-03-18 03:51:00','2026-05-30 03:19:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO api_test_cases(id,collection_id,project_id,user_id,environment_id,name,description,method,url,headers,params,body,body_type,assertions,timeout,retry_count,tags,priority,is_enabled,sort_order,last_run_at,last_status,created_at,updated_at)VALUES(606,110,16,1,62,'订单详情','验证订单详情','GET','/api/v1/orders/1001','{}','{}',NULL,'json','[]',30,0,'["order", "P0"]',2,true,3,NULL,'pending','2026-02-07 10:04:00','2026-05-31 05:43:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO api_test_cases(id,collection_id,project_id,user_id,environment_id,name,description,method,url,headers,params,body,body_type,assertions,timeout,retry_count,tags,priority,is_enabled,sort_order,last_run_at,last_status,created_at,updated_at)VALUES(607,110,16,5,61,'支付状态','验证支付状态','GET','/api/v1/payments/1001','{}','{}',NULL,'json','[]',30,0,'["payment", "P1"]',2,true,4,'2026-05-19 13:08:00','success','2025-11-21 09:46:00','2026-05-30 23:45:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO api_test_cases(id,collection_id,project_id,user_id,environment_id,name,description,method,url,headers,params,body,body_type,assertions,timeout,retry_count,tags,priority,is_enabled,sort_order,last_run_at,last_status,created_at,updated_at)VALUES(608,110,16,2,61,'用户信息','验证用户信息','GET','/api/v1/users/me','{}','{}',NULL,'json','[]',30,0,'["user", "P0"]',3,true,5,'2026-05-25 12:16:00','running','2026-04-05 14:05:00','2026-05-29 17:40:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO api_test_cases(id,collection_id,project_id,user_id,environment_id,name,description,method,url,headers,params,body,body_type,assertions,timeout,retry_count,tags,priority,is_enabled,sort_order,last_run_at,last_status,created_at,updated_at)VALUES(609,110,16,2,64,'申请退款','验证申请退款','POST','/api/v1/refunds','{}','{}',NULL,'json','[]',30,0,'["payment", "P1"]',1,true,6,'2026-05-30 18:56:00','success','2026-05-18 13:51:00','2026-06-01 05:55:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO api_test_cases(id,collection_id,project_id,user_id,environment_id,name,description,method,url,headers,params,body,body_type,assertions,timeout,retry_count,tags,priority,is_enabled,sort_order,last_run_at,last_status,created_at,updated_at)VALUES(610,111,16,7,61,'领取券','验证领取券','POST','/api/v1/coupons/1001','{}','{}',NULL,'json','[]',30,0,'["marketing", "P1"]',3,true,0,'2026-05-19 00:50:00','success','2026-04-12 02:33:00','2026-05-31 14:45:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO api_test_cases(id,collection_id,project_id,user_id,environment_id,name,description,method,url,headers,params,body,body_type,assertions,timeout,retry_count,tags,priority,is_enabled,sort_order,last_run_at,last_status,created_at,updated_at)VALUES(611,111,16,5,63,'优惠券','验证优惠券','GET','/api/v1/coupons','{}','{}',NULL,'json','[]',30,0,'["marketing", "P1"]',2,true,1,'2026-05-27 01:05:00','success','2026-05-11 22:35:00','2026-05-30 04:30:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO api_test_cases(id,collection_id,project_id,user_id,environment_id,name,description,method,url,headers,params,body,body_type,assertions,timeout,retry_count,tags,priority,is_enabled,sort_order,last_run_at,last_status,created_at,updated_at)VALUES(612,111,16,6,64,'取消订单','验证取消订单','POST','/api/v1/orders/1001/cancel','{}','{}',NULL,'json','[]',30,0,'["order", "P1"]',2,true,2,'2026-05-20 05:08:00','success','2026-05-26 21:33:00','2026-06-02 00:22:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO api_test_cases(id,collection_id,project_id,user_id,environment_id,name,description,method,url,headers,params,body,body_type,assertions,timeout,retry_count,tags,priority,is_enabled,sort_order,last_run_at,last_status,created_at,updated_at)VALUES(613,111,16,7,62,'发起支付','验证发起支付','POST','/api/v1/payments','{}','{}',NULL,'json','[]',30,0,'["payment", "P0"]',2,true,3,'2026-05-28 01:36:00','success','2026-03-14 19:42:00','2026-05-29 16:22:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO api_test_cases(id,collection_id,project_id,user_id,environment_id,name,description,method,url,headers,params,body,body_type,assertions,timeout,retry_count,tags,priority,is_enabled,sort_order,last_run_at,last_status,created_at,updated_at)VALUES(614,112,16,2,61,'更新资料','验证更新资料','PUT','/api/v1/users/me','{}','{}',NULL,'json','[]',30,0,'["user", "P1"]',2,true,0,'2026-05-21 18:35:00','success','2026-02-19 10:37:00','2026-05-29 18:41:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO api_test_cases(id,collection_id,project_id,user_id,environment_id,name,description,method,url,headers,params,body,body_type,assertions,timeout,retry_count,tags,priority,is_enabled,sort_order,last_run_at,last_status,created_at,updated_at)VALUES(615,112,16,7,61,'消息列表','验证消息列表','GET','/api/v1/messages','{}','{}',NULL,'json','[]',30,0,'["message", "P1"]',2,true,1,'2026-06-01 06:36:00','success','2026-04-21 03:12:00','2026-05-30 01:11:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO api_test_cases(id,collection_id,project_id,user_id,environment_id,name,description,method,url,headers,params,body,body_type,assertions,timeout,retry_count,tags,priority,is_enabled,sort_order,last_run_at,last_status,created_at,updated_at)VALUES(616,112,16,5,64,'创建订单','验证创建订单','POST','/api/v1/orders','{}','{}',NULL,'json','[]',30,0,'["order", "P0"]',3,true,2,'2026-05-21 11:57:00','success','2026-02-22 20:13:00','2026-06-01 02:30:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO api_test_cases(id,collection_id,project_id,user_id,environment_id,name,description,method,url,headers,params,body,body_type,assertions,timeout,retry_count,tags,priority,is_enabled,sort_order,last_run_at,last_status,created_at,updated_at)VALUES(617,112,16,1,63,'获取配置','验证获取配置','GET','/api/v1/config','{}','{}',NULL,'json','[]',30,0,'["config", "P2"]',3,true,3,'2026-06-01 11:18:00','success','2026-04-25 01:22:00','2026-05-29 12:51:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO api_test_cases(id,collection_id,project_id,user_id,environment_id,name,description,method,url,headers,params,body,body_type,assertions,timeout,retry_count,tags,priority,is_enabled,sort_order,last_run_at,last_status,created_at,updated_at)VALUES(618,112,16,5,62,'取消订单','验证取消订单','POST','/api/v1/orders/1001/cancel','{}','{}',NULL,'json','[]',30,0,'["order", "P1"]',1,true,4,'2026-05-28 09:53:00','success','2025-12-18 11:02:00','2026-05-29 21:15:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO api_test_cases(id,collection_id,project_id,user_id,environment_id,name,description,method,url,headers,params,body,body_type,assertions,timeout,retry_count,tags,priority,is_enabled,sort_order,last_run_at,last_status,created_at,updated_at)VALUES(619,112,16,7,61,'健康检查','验证健康检查','GET','/api/v1/health','{}','{}',NULL,'json','[]',30,0,'["health", "P0"]',2,true,5,'2026-05-26 20:50:00','success','2026-03-28 11:41:00','2026-05-29 15:41:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO web_test_collections(id,project_id,user_id,name,description,sort_order,created_at,updated_at)VALUES(1,1,1,'冒烟测试集','核心冒烟',0,'2026-05-04 13:24:00','2026-05-31 05:43:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO web_test_scripts(id,project_id,collection_id,user_id,name,description,script_content,script_type,target_url,browser,headless,timeout,step_count,status,last_status,last_run_at,last_run_duration,tags,is_enabled,sort_order,created_at,updated_at)VALUES(1,1,1,1,'表单验证','注册校验','from playwright.sync_api import Page','playwright','https://example.com/register','chromium',true,30000,9,'success','success','2026-05-30 19:00:00',16.1,'["regression", "P1"]',true,0,'2026-01-17 20:19:00','2026-05-30 10:33:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO web_test_scripts(id,project_id,collection_id,user_id,name,description,script_content,script_type,target_url,browser,headless,timeout,step_count,status,last_status,last_run_at,last_run_duration,tags,is_enabled,sort_order,created_at,updated_at)VALUES(2,1,1,1,'响应式布局','多设备','from playwright.sync_api import Page','playwright','https://example.com','chromium',true,30000,10,'success','success','2026-05-28 04:15:00',20.4,'["visual", "P2"]',true,1,'2026-04-15 17:53:00','2026-05-29 15:08:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO web_test_scripts(id,project_id,collection_id,user_id,name,description,script_content,script_type,target_url,browser,headless,timeout,step_count,status,last_status,last_run_at,last_run_duration,tags,is_enabled,sort_order,created_at,updated_at)VALUES(3,1,1,1,'购物车','验证购物车','from playwright.sync_api import Page','playwright','https://example.com/cart','chromium',true,30000,6,'success','success','2026-05-30 08:13:00',26.0,'["regression", "P1"]',true,2,'2026-03-26 20:32:00','2026-06-01 13:50:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO web_test_collections(id,project_id,user_id,name,description,sort_order,created_at,updated_at)VALUES(2,5,1,'冒烟测试集','核心冒烟',0,'2026-05-30 08:43:00','2026-06-01 12:23:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO web_test_scripts(id,project_id,collection_id,user_id,name,description,script_content,script_type,target_url,browser,headless,timeout,step_count,status,last_status,last_run_at,last_run_duration,tags,is_enabled,sort_order,created_at,updated_at)VALUES(4,5,2,1,'商品搜索','验证搜索','from playwright.sync_api import Page','playwright','https://example.com/products','chromium',true,30000,7,'success','success','2026-06-01 21:22:00',64.8,'["smoke", "P0"]',true,0,'2026-01-27 18:12:00','2026-05-30 14:33:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO web_test_scripts(id,project_id,collection_id,user_id,name,description,script_content,script_type,target_url,browser,headless,timeout,step_count,status,last_status,last_run_at,last_run_duration,tags,is_enabled,sort_order,created_at,updated_at)VALUES(5,5,2,1,'文件上传','头像上传','from playwright.sync_api import Page','playwright','https://example.com/profile','chromium',true,30000,8,'success','success','2026-05-22 23:40:00',98.9,'["regression", "P2"]',true,1,'2025-12-12 21:36:00','2026-06-01 22:05:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO web_test_collections(id,project_id,user_id,name,description,sort_order,created_at,updated_at)VALUES(3,5,1,'回归测试集','版本回归',1,'2026-05-31 19:05:00','2026-05-29 10:07:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO web_test_scripts(id,project_id,collection_id,user_id,name,description,script_content,script_type,target_url,browser,headless,timeout,step_count,status,last_status,last_run_at,last_run_duration,tags,is_enabled,sort_order,created_at,updated_at)VALUES(6,5,3,1,'用户登录流程','验证登录','from playwright.sync_api import Page','playwright','https://example.com/login','chromium',true,30000,8,'running','running','2026-05-28 11:12:00',98.7,'["smoke", "P0"]',true,0,'2026-02-05 14:17:00','2026-05-29 17:34:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO web_test_scripts(id,project_id,collection_id,user_id,name,description,script_content,script_type,target_url,browser,headless,timeout,step_count,status,last_status,last_run_at,last_run_duration,tags,is_enabled,sort_order,created_at,updated_at)VALUES(7,5,3,1,'后台用户列表','后台管理','from playwright.sync_api import Page','playwright','https://admin.example.com/users','chromium',true,30000,8,'failed','failed','2026-06-01 13:08:00',42.1,'["regression", "P1"]',true,1,'2026-05-20 10:40:00','2026-05-30 02:22:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO web_test_scripts(id,project_id,collection_id,user_id,name,description,script_content,script_type,target_url,browser,headless,timeout,step_count,status,last_status,last_run_at,last_run_duration,tags,is_enabled,sort_order,created_at,updated_at)VALUES(8,5,3,1,'文件上传','头像上传','from playwright.sync_api import Page','playwright','https://example.com/profile','chromium',true,30000,10,'success','success','2026-05-24 07:38:00',54.2,'["regression", "P2"]',true,2,'2025-12-14 11:03:00','2026-06-01 10:36:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO web_test_collections(id,project_id,user_id,name,description,sort_order,created_at,updated_at)VALUES(4,8,7,'冒烟测试集','核心冒烟',0,'2026-05-24 05:29:00','2026-06-02 00:07:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO web_test_scripts(id,project_id,collection_id,user_id,name,description,script_content,script_type,target_url,browser,headless,timeout,step_count,status,last_status,last_run_at,last_run_duration,tags,is_enabled,sort_order,created_at,updated_at)VALUES(9,8,4,7,'购物车','验证购物车','from playwright.sync_api import Page','playwright','https://example.com/cart','chromium',true,30000,9,'success','success','2026-05-30 12:16:00',15.3,'["regression", "P1"]',true,0,'2026-05-25 04:01:00','2026-05-30 21:11:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO web_test_scripts(id,project_id,collection_id,user_id,name,description,script_content,script_type,target_url,browser,headless,timeout,step_count,status,last_status,last_run_at,last_run_duration,tags,is_enabled,sort_order,created_at,updated_at)VALUES(10,8,4,7,'订单支付','端到端支付','from playwright.sync_api import Page','playwright','https://example.com/checkout','chromium',true,30000,4,'success','success','2026-05-28 12:30:00',114.4,'["smoke", "P0"]',true,1,'2025-12-13 05:01:00','2026-05-30 07:10:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO web_test_scripts(id,project_id,collection_id,user_id,name,description,script_content,script_type,target_url,browser,headless,timeout,step_count,status,last_status,last_run_at,last_run_duration,tags,is_enabled,sort_order,created_at,updated_at)VALUES(11,8,4,7,'用户登录流程','验证登录','from playwright.sync_api import Page','playwright','https://example.com/login','chromium',true,30000,4,'failed','failed','2026-05-29 15:11:00',111.2,'["smoke", "P0"]',true,2,'2025-12-18 23:36:00','2026-05-29 13:19:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO web_test_scripts(id,project_id,collection_id,user_id,name,description,script_content,script_type,target_url,browser,headless,timeout,step_count,status,last_status,last_run_at,last_run_duration,tags,is_enabled,sort_order,created_at,updated_at)VALUES(12,8,4,7,'表单验证','注册校验','from playwright.sync_api import Page','playwright','https://example.com/register','chromium',true,30000,7,'failed','failed','2026-05-27 02:46:00',34.8,'["regression", "P1"]',true,3,'2026-05-10 06:55:00','2026-05-30 10:23:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO web_test_scripts(id,project_id,collection_id,user_id,name,description,script_content,script_type,target_url,browser,headless,timeout,step_count,status,last_status,last_run_at,last_run_duration,tags,is_enabled,sort_order,created_at,updated_at)VALUES(13,8,4,7,'商品搜索','验证搜索','from playwright.sync_api import Page','playwright','https://example.com/products','chromium',true,30000,4,'pending','pending',NULL,NULL,'["smoke", "P0"]',true,4,'2026-01-05 22:52:00','2026-05-30 21:24:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO web_test_collections(id,project_id,user_id,name,description,sort_order,created_at,updated_at)VALUES(5,8,5,'回归测试集','版本回归',1,'2026-05-16 15:26:00','2026-05-31 21:33:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO web_test_scripts(id,project_id,collection_id,user_id,name,description,script_content,script_type,target_url,browser,headless,timeout,step_count,status,last_status,last_run_at,last_run_duration,tags,is_enabled,sort_order,created_at,updated_at)VALUES(14,8,5,5,'响应式布局','多设备','from playwright.sync_api import Page','playwright','https://example.com','chromium',true,30000,3,'success','success','2026-05-23 15:46:00',17.3,'["visual", "P2"]',true,0,'2026-01-14 19:40:00','2026-06-01 00:07:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO web_test_scripts(id,project_id,collection_id,user_id,name,description,script_content,script_type,target_url,browser,headless,timeout,step_count,status,last_status,last_run_at,last_run_duration,tags,is_enabled,sort_order,created_at,updated_at)VALUES(15,8,5,5,'表单验证','注册校验','from playwright.sync_api import Page','playwright','https://example.com/register','chromium',true,30000,5,'success','success','2026-05-22 19:51:00',74.2,'["regression", "P1"]',true,1,'2025-12-12 11:58:00','2026-05-31 00:28:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO web_test_scripts(id,project_id,collection_id,user_id,name,description,script_content,script_type,target_url,browser,headless,timeout,step_count,status,last_status,last_run_at,last_run_duration,tags,is_enabled,sort_order,created_at,updated_at)VALUES(16,8,5,5,'文件上传','头像上传','from playwright.sync_api import Page','playwright','https://example.com/profile','chromium',true,30000,10,'cancelled','cancelled','2026-06-01 01:06:00',86.3,'["regression", "P2"]',true,2,'2025-12-22 03:29:00','2026-05-30 11:36:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO web_test_scripts(id,project_id,collection_id,user_id,name,description,script_content,script_type,target_url,browser,headless,timeout,step_count,status,last_status,last_run_at,last_run_duration,tags,is_enabled,sort_order,created_at,updated_at)VALUES(17,8,5,5,'商品搜索','验证搜索','from playwright.sync_api import Page','playwright','https://example.com/products','chromium',true,30000,6,'success','success','2026-05-28 05:08:00',87.4,'["smoke", "P0"]',true,3,'2025-12-03 10:57:00','2026-05-31 18:14:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO web_test_collections(id,project_id,user_id,name,description,sort_order,created_at,updated_at)VALUES(6,8,2,'UI兼容性','多浏览器',2,'2026-05-26 16:35:00','2026-05-30 20:17:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO web_test_scripts(id,project_id,collection_id,user_id,name,description,script_content,script_type,target_url,browser,headless,timeout,step_count,status,last_status,last_run_at,last_run_duration,tags,is_enabled,sort_order,created_at,updated_at)VALUES(18,8,6,2,'响应式布局','多设备','from playwright.sync_api import Page','playwright','https://example.com','chromium',true,30000,11,'success','success','2026-05-29 00:16:00',111.2,'["visual", "P2"]',true,0,'2026-02-21 06:52:00','2026-05-30 15:05:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO web_test_scripts(id,project_id,collection_id,user_id,name,description,script_content,script_type,target_url,browser,headless,timeout,step_count,status,last_status,last_run_at,last_run_duration,tags,is_enabled,sort_order,created_at,updated_at)VALUES(19,8,6,2,'表单验证','注册校验','from playwright.sync_api import Page','playwright','https://example.com/register','chromium',true,30000,5,'failed','failed','2026-05-28 19:19:00',23.8,'["regression", "P1"]',true,1,'2026-02-07 11:30:00','2026-05-31 05:47:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO web_test_scripts(id,project_id,collection_id,user_id,name,description,script_content,script_type,target_url,browser,headless,timeout,step_count,status,last_status,last_run_at,last_run_duration,tags,is_enabled,sort_order,created_at,updated_at)VALUES(20,8,6,2,'订单支付','端到端支付','from playwright.sync_api import Page','playwright','https://example.com/checkout','chromium',true,30000,12,'success','success','2026-05-29 10:19:00',6.1,'["smoke", "P0"]',true,2,'2026-05-05 12:10:00','2026-05-31 21:33:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO web_test_scripts(id,project_id,collection_id,user_id,name,description,script_content,script_type,target_url,browser,headless,timeout,step_count,status,last_status,last_run_at,last_run_duration,tags,is_enabled,sort_order,created_at,updated_at)VALUES(21,8,6,2,'文件上传','头像上传','from playwright.sync_api import Page','playwright','https://example.com/profile','chromium',true,30000,10,'failed','failed','2026-05-31 08:54:00',45.9,'["regression", "P2"]',true,3,'2026-04-17 08:53:00','2026-05-30 15:33:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO web_test_scripts(id,project_id,collection_id,user_id,name,description,script_content,script_type,target_url,browser,headless,timeout,step_count,status,last_status,last_run_at,last_run_duration,tags,is_enabled,sort_order,created_at,updated_at)VALUES(22,8,6,2,'用户登录流程','验证登录','from playwright.sync_api import Page','playwright','https://example.com/login','chromium',true,30000,9,'pending','pending',NULL,NULL,'["smoke", "P0"]',true,4,'2026-03-31 08:53:00','2026-05-31 21:29:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO web_test_collections(id,project_id,user_id,name,description,sort_order,created_at,updated_at)VALUES(7,9,2,'冒烟测试集','核心冒烟',0,'2025-12-15 10:36:00','2026-06-01 19:05:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO web_test_scripts(id,project_id,collection_id,user_id,name,description,script_content,script_type,target_url,browser,headless,timeout,step_count,status,last_status,last_run_at,last_run_duration,tags,is_enabled,sort_order,created_at,updated_at)VALUES(23,9,7,2,'后台用户列表','后台管理','from playwright.sync_api import Page','playwright','https://admin.example.com/users','chromium',true,30000,11,'success','success','2026-06-01 07:53:00',61.3,'["regression", "P1"]',true,0,'2026-04-05 09:23:00','2026-05-30 01:16:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO web_test_scripts(id,project_id,collection_id,user_id,name,description,script_content,script_type,target_url,browser,headless,timeout,step_count,status,last_status,last_run_at,last_run_duration,tags,is_enabled,sort_order,created_at,updated_at)VALUES(24,9,7,2,'响应式布局','多设备','from playwright.sync_api import Page','playwright','https://example.com','chromium',true,30000,9,'failed','failed','2026-05-24 04:36:00',60.7,'["visual", "P2"]',true,1,'2026-03-16 15:52:00','2026-06-01 23:56:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO web_test_scripts(id,project_id,collection_id,user_id,name,description,script_content,script_type,target_url,browser,headless,timeout,step_count,status,last_status,last_run_at,last_run_duration,tags,is_enabled,sort_order,created_at,updated_at)VALUES(25,9,7,2,'表单验证','注册校验','from playwright.sync_api import Page','playwright','https://example.com/register','chromium',true,30000,3,'failed','failed','2026-05-25 04:35:00',98.5,'["regression", "P1"]',true,2,'2026-02-20 16:08:00','2026-05-30 07:27:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO web_test_scripts(id,project_id,collection_id,user_id,name,description,script_content,script_type,target_url,browser,headless,timeout,step_count,status,last_status,last_run_at,last_run_duration,tags,is_enabled,sort_order,created_at,updated_at)VALUES(26,9,7,2,'订单支付','端到端支付','from playwright.sync_api import Page','playwright','https://example.com/checkout','chromium',true,30000,4,'failed','failed','2026-05-24 11:08:00',95.9,'["smoke", "P0"]',true,3,'2026-04-08 12:03:00','2026-06-02 04:05:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO web_test_scripts(id,project_id,collection_id,user_id,name,description,script_content,script_type,target_url,browser,headless,timeout,step_count,status,last_status,last_run_at,last_run_duration,tags,is_enabled,sort_order,created_at,updated_at)VALUES(27,9,7,2,'购物车','验证购物车','from playwright.sync_api import Page','playwright','https://example.com/cart','chromium',true,30000,8,'success','success','2026-05-31 09:25:00',56.4,'["regression", "P1"]',true,4,'2026-05-01 08:52:00','2026-05-31 13:50:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO web_test_collections(id,project_id,user_id,name,description,sort_order,created_at,updated_at)VALUES(8,11,1,'回归测试集','版本回归',1,'2026-03-30 00:58:00','2026-05-30 12:26:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO web_test_scripts(id,project_id,collection_id,user_id,name,description,script_content,script_type,target_url,browser,headless,timeout,step_count,status,last_status,last_run_at,last_run_duration,tags,is_enabled,sort_order,created_at,updated_at)VALUES(28,11,8,1,'购物车','验证购物车','from playwright.sync_api import Page','playwright','https://example.com/cart','chromium',true,30000,3,'success','success','2026-05-25 03:16:00',16.4,'["regression", "P1"]',true,0,'2026-04-02 08:48:00','2026-06-01 00:06:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO web_test_scripts(id,project_id,collection_id,user_id,name,description,script_content,script_type,target_url,browser,headless,timeout,step_count,status,last_status,last_run_at,last_run_duration,tags,is_enabled,sort_order,created_at,updated_at)VALUES(29,11,8,1,'后台用户列表','后台管理','from playwright.sync_api import Page','playwright','https://admin.example.com/users','chromium',true,30000,8,'failed','failed','2026-05-30 14:25:00',29.8,'["regression", "P1"]',true,1,'2026-03-22 05:14:00','2026-05-30 07:25:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO web_test_scripts(id,project_id,collection_id,user_id,name,description,script_content,script_type,target_url,browser,headless,timeout,step_count,status,last_status,last_run_at,last_run_duration,tags,is_enabled,sort_order,created_at,updated_at)VALUES(30,11,8,1,'订单支付','端到端支付','from playwright.sync_api import Page','playwright','https://example.com/checkout','chromium',true,30000,10,'success','success','2026-05-26 13:03:00',23.8,'["smoke", "P0"]',true,2,'2026-05-11 01:17:00','2026-05-29 11:51:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO web_test_scripts(id,project_id,collection_id,user_id,name,description,script_content,script_type,target_url,browser,headless,timeout,step_count,status,last_status,last_run_at,last_run_duration,tags,is_enabled,sort_order,created_at,updated_at)VALUES(31,11,8,1,'文件上传','头像上传','from playwright.sync_api import Page','playwright','https://example.com/profile','chromium',true,30000,6,'success','success','2026-05-31 13:14:00',36.0,'["regression", "P2"]',true,3,'2026-02-25 15:18:00','2026-05-31 20:08:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO web_test_scripts(id,project_id,collection_id,user_id,name,description,script_content,script_type,target_url,browser,headless,timeout,step_count,status,last_status,last_run_at,last_run_duration,tags,is_enabled,sort_order,created_at,updated_at)VALUES(32,11,8,1,'表单验证','注册校验','from playwright.sync_api import Page','playwright','https://example.com/register','chromium',true,30000,6,'success','success','2026-05-26 21:59:00',115.9,'["regression", "P1"]',true,4,'2026-05-13 01:53:00','2026-06-01 12:25:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO web_test_collections(id,project_id,user_id,name,description,sort_order,created_at,updated_at)VALUES(9,11,5,'UI兼容性','多浏览器',2,'2025-12-20 07:37:00','2026-05-31 01:51:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO web_test_scripts(id,project_id,collection_id,user_id,name,description,script_content,script_type,target_url,browser,headless,timeout,step_count,status,last_status,last_run_at,last_run_duration,tags,is_enabled,sort_order,created_at,updated_at)VALUES(33,11,9,5,'后台用户列表','后台管理','from playwright.sync_api import Page','playwright','https://admin.example.com/users','chromium',true,30000,4,'success','success','2026-05-29 21:54:00',95.0,'["regression", "P1"]',true,0,'2026-04-17 17:14:00','2026-05-30 15:08:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO web_test_scripts(id,project_id,collection_id,user_id,name,description,script_content,script_type,target_url,browser,headless,timeout,step_count,status,last_status,last_run_at,last_run_duration,tags,is_enabled,sort_order,created_at,updated_at)VALUES(34,11,9,5,'用户登录流程','验证登录','from playwright.sync_api import Page','playwright','https://example.com/login','chromium',true,30000,7,'failed','failed','2026-05-31 17:38:00',85.6,'["smoke", "P0"]',true,1,'2026-01-11 01:22:00','2026-06-02 08:50:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO web_test_scripts(id,project_id,collection_id,user_id,name,description,script_content,script_type,target_url,browser,headless,timeout,step_count,status,last_status,last_run_at,last_run_duration,tags,is_enabled,sort_order,created_at,updated_at)VALUES(35,11,9,5,'表单验证','注册校验','from playwright.sync_api import Page','playwright','https://example.com/register','chromium',true,30000,11,'success','success','2026-05-27 04:38:00',97.7,'["regression", "P1"]',true,2,'2026-01-10 14:04:00','2026-05-29 18:23:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO web_test_collections(id,project_id,user_id,name,description,sort_order,created_at,updated_at)VALUES(10,14,5,'UI兼容性','多浏览器',2,'2026-05-18 10:20:00','2026-05-30 11:11:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO web_test_scripts(id,project_id,collection_id,user_id,name,description,script_content,script_type,target_url,browser,headless,timeout,step_count,status,last_status,last_run_at,last_run_duration,tags,is_enabled,sort_order,created_at,updated_at)VALUES(36,14,10,5,'表单验证','注册校验','from playwright.sync_api import Page','playwright','https://example.com/register','chromium',true,30000,9,'success','success','2026-05-27 19:28:00',38.0,'["regression", "P1"]',true,0,'2026-01-18 11:04:00','2026-06-01 00:20:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO web_test_scripts(id,project_id,collection_id,user_id,name,description,script_content,script_type,target_url,browser,headless,timeout,step_count,status,last_status,last_run_at,last_run_duration,tags,is_enabled,sort_order,created_at,updated_at)VALUES(37,14,10,5,'响应式布局','多设备','from playwright.sync_api import Page','playwright','https://example.com','chromium',true,30000,4,'running','running','2026-05-28 20:11:00',41.0,'["visual", "P2"]',true,1,'2025-12-21 07:56:00','2026-06-01 07:50:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO web_test_scripts(id,project_id,collection_id,user_id,name,description,script_content,script_type,target_url,browser,headless,timeout,step_count,status,last_status,last_run_at,last_run_duration,tags,is_enabled,sort_order,created_at,updated_at)VALUES(38,14,10,5,'订单支付','端到端支付','from playwright.sync_api import Page','playwright','https://example.com/checkout','chromium',true,30000,10,'success','success','2026-05-31 10:42:00',68.7,'["smoke", "P0"]',true,2,'2026-05-29 20:17:00','2026-05-31 18:29:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO web_test_collections(id,project_id,user_id,name,description,sort_order,created_at,updated_at)VALUES(11,15,7,'冒烟测试集','核心冒烟',0,'2025-12-05 06:35:00','2026-06-01 14:48:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO web_test_scripts(id,project_id,collection_id,user_id,name,description,script_content,script_type,target_url,browser,headless,timeout,step_count,status,last_status,last_run_at,last_run_duration,tags,is_enabled,sort_order,created_at,updated_at)VALUES(39,15,11,7,'表单验证','注册校验','from playwright.sync_api import Page','playwright','https://example.com/register','chromium',true,30000,11,'success','success','2026-05-28 02:13:00',81.0,'["regression", "P1"]',true,0,'2025-12-07 14:58:00','2026-05-30 04:17:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO web_test_scripts(id,project_id,collection_id,user_id,name,description,script_content,script_type,target_url,browser,headless,timeout,step_count,status,last_status,last_run_at,last_run_duration,tags,is_enabled,sort_order,created_at,updated_at)VALUES(40,15,11,7,'响应式布局','多设备','from playwright.sync_api import Page','playwright','https://example.com','chromium',true,30000,11,'pending','pending',NULL,NULL,'["visual", "P2"]',true,1,'2026-04-05 04:56:00','2026-05-31 05:28:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO web_test_collections(id,project_id,user_id,name,description,sort_order,created_at,updated_at)VALUES(12,15,1,'回归测试集','版本回归',1,'2026-02-12 18:36:00','2026-05-31 22:53:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO web_test_scripts(id,project_id,collection_id,user_id,name,description,script_content,script_type,target_url,browser,headless,timeout,step_count,status,last_status,last_run_at,last_run_duration,tags,is_enabled,sort_order,created_at,updated_at)VALUES(41,15,12,1,'订单支付','端到端支付','from playwright.sync_api import Page','playwright','https://example.com/checkout','chromium',true,30000,12,'success','success','2026-05-26 00:44:00',29.5,'["smoke", "P0"]',true,0,'2026-02-21 03:01:00','2026-05-30 13:28:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO web_test_scripts(id,project_id,collection_id,user_id,name,description,script_content,script_type,target_url,browser,headless,timeout,step_count,status,last_status,last_run_at,last_run_duration,tags,is_enabled,sort_order,created_at,updated_at)VALUES(42,15,12,1,'表单验证','注册校验','from playwright.sync_api import Page','playwright','https://example.com/register','chromium',true,30000,10,'failed','failed','2026-06-01 19:03:00',76.0,'["regression", "P1"]',true,1,'2026-05-17 23:00:00','2026-05-29 23:41:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO web_test_scripts(id,project_id,collection_id,user_id,name,description,script_content,script_type,target_url,browser,headless,timeout,step_count,status,last_status,last_run_at,last_run_duration,tags,is_enabled,sort_order,created_at,updated_at)VALUES(43,15,12,1,'后台用户列表','后台管理','from playwright.sync_api import Page','playwright','https://admin.example.com/users','chromium',true,30000,9,'success','success','2026-06-01 22:04:00',88.1,'["regression", "P1"]',true,2,'2026-03-03 09:54:00','2026-05-29 18:48:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO web_test_scripts(id,project_id,collection_id,user_id,name,description,script_content,script_type,target_url,browser,headless,timeout,step_count,status,last_status,last_run_at,last_run_duration,tags,is_enabled,sort_order,created_at,updated_at)VALUES(44,15,12,1,'用户登录流程','验证登录','from playwright.sync_api import Page','playwright','https://example.com/login','chromium',true,30000,10,'success','success','2026-05-25 05:34:00',19.2,'["smoke", "P0"]',true,3,'2026-05-31 05:11:00','2026-05-31 02:30:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO web_test_collections(id,project_id,user_id,name,description,sort_order,created_at,updated_at)VALUES(13,15,5,'UI兼容性','多浏览器',2,'2026-02-27 20:03:00','2026-05-31 16:09:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO web_test_scripts(id,project_id,collection_id,user_id,name,description,script_content,script_type,target_url,browser,headless,timeout,step_count,status,last_status,last_run_at,last_run_duration,tags,is_enabled,sort_order,created_at,updated_at)VALUES(45,15,13,5,'商品搜索','验证搜索','from playwright.sync_api import Page','playwright','https://example.com/products','chromium',true,30000,6,'success','success','2026-05-27 10:33:00',5.7,'["smoke", "P0"]',true,0,'2026-05-04 03:42:00','2026-06-02 05:35:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO web_test_scripts(id,project_id,collection_id,user_id,name,description,script_content,script_type,target_url,browser,headless,timeout,step_count,status,last_status,last_run_at,last_run_duration,tags,is_enabled,sort_order,created_at,updated_at)VALUES(46,15,13,5,'订单支付','端到端支付','from playwright.sync_api import Page','playwright','https://example.com/checkout','chromium',true,30000,10,'success','success','2026-05-28 08:50:00',81.6,'["smoke", "P0"]',true,1,'2025-12-13 01:53:00','2026-05-29 18:25:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO web_test_scripts(id,project_id,collection_id,user_id,name,description,script_content,script_type,target_url,browser,headless,timeout,step_count,status,last_status,last_run_at,last_run_duration,tags,is_enabled,sort_order,created_at,updated_at)VALUES(47,15,13,5,'响应式布局','多设备','from playwright.sync_api import Page','playwright','https://example.com','chromium',true,30000,9,'success','success','2026-05-22 11:52:00',42.4,'["visual", "P2"]',true,2,'2026-01-23 10:01:00','2026-05-30 05:53:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO web_test_scripts(id,project_id,collection_id,user_id,name,description,script_content,script_type,target_url,browser,headless,timeout,step_count,status,last_status,last_run_at,last_run_duration,tags,is_enabled,sort_order,created_at,updated_at)VALUES(48,15,13,5,'表单验证','注册校验','from playwright.sync_api import Page','playwright','https://example.com/register','chromium',true,30000,3,'pending','pending',NULL,NULL,'["regression", "P1"]',true,3,'2026-04-30 05:38:00','2026-06-01 12:45:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO perf_test_scenarios(id,project_id,user_id,name,description,target_url,method,headers,script_content,user_count,spawn_rate,duration,status,last_run_at,avg_response_time,max_response_time,min_response_time,throughput,error_rate,tags,is_enabled,created_at,updated_at)VALUES(1,1,6,'搜索压测','全文搜索','https://example.com/api/v1/search','GET','{}','from locust import HttpUser',100,10,180,'pending',NULL,158.9,1017.2,64.3,533.1,0.76,'["performance"]',true,'2026-01-22 04:45:00','2026-05-31 06:05:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO perf_test_scenarios(id,project_id,user_id,name,description,target_url,method,headers,script_content,user_count,spawn_rate,duration,status,last_run_at,avg_response_time,max_response_time,min_response_time,throughput,error_rate,tags,is_enabled,created_at,updated_at)VALUES(2,1,5,'首页并发','大量用户访问','https://example.com/','GET','{}','from locust import HttpUser',100,10,300,'completed','2026-05-16 14:49:00',339.8,2040.2,98.4,1576.3,0.52,'["performance"]',true,'2026-04-13 15:20:00','2026-05-28 05:46:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO perf_test_scenarios(id,project_id,user_id,name,description,target_url,method,headers,script_content,user_count,spawn_rate,duration,status,last_run_at,avg_response_time,max_response_time,min_response_time,throughput,error_rate,tags,is_enabled,created_at,updated_at)VALUES(3,3,6,'登录压测','登录高并发','https://example.com/api/v1/auth/login','POST','{}','from locust import HttpUser',200,20,180,'completed','2026-05-13 02:46:00',315.9,1148.8,38.0,844.2,1.53,'["performance"]',true,'2026-03-06 20:30:00','2026-06-01 17:33:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO perf_test_scenarios(id,project_id,user_id,name,description,target_url,method,headers,script_content,user_count,spawn_rate,duration,status,last_run_at,avg_response_time,max_response_time,min_response_time,throughput,error_rate,tags,is_enabled,created_at,updated_at)VALUES(4,3,1,'搜索压测','全文搜索','https://example.com/api/v1/search','GET','{}','from locust import HttpUser',100,10,180,'completed','2026-06-01 04:58:00',72.8,403.7,34.7,1437.6,1.23,'["performance"]',true,'2026-06-01 08:18:00','2026-05-27 23:47:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO perf_test_scenarios(id,project_id,user_id,name,description,target_url,method,headers,script_content,user_count,spawn_rate,duration,status,last_run_at,avg_response_time,max_response_time,min_response_time,throughput,error_rate,tags,is_enabled,created_at,updated_at)VALUES(5,6,6,'登录压测','登录高并发','https://example.com/api/v1/auth/login','POST','{}','from locust import HttpUser',200,20,180,'completed','2026-05-28 23:37:00',180.5,682.4,66.3,1381.8,3.85,'["performance"]',true,'2026-02-28 10:11:00','2026-05-28 17:22:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO perf_test_scenarios(id,project_id,user_id,name,description,target_url,method,headers,script_content,user_count,spawn_rate,duration,status,last_run_at,avg_response_time,max_response_time,min_response_time,throughput,error_rate,tags,is_enabled,created_at,updated_at)VALUES(6,6,5,'商品查询','缓存性能','https://example.com/api/v1/products','GET','{}','from locust import HttpUser',150,15,300,'completed','2026-05-14 06:58:00',332.1,1484.6,84.2,1780.0,0.65,'["performance"]',true,'2026-01-01 13:08:00','2026-06-01 03:15:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO perf_test_scenarios(id,project_id,user_id,name,description,target_url,method,headers,script_content,user_count,spawn_rate,duration,status,last_run_at,avg_response_time,max_response_time,min_response_time,throughput,error_rate,tags,is_enabled,created_at,updated_at)VALUES(7,7,7,'首页并发','大量用户访问','https://example.com/','GET','{}','from locust import HttpUser',100,10,300,'failed','2026-06-01 05:48:00',184.6,1491.1,91.5,443.9,3.6,'["performance"]',true,'2026-02-13 16:15:00','2026-05-30 16:38:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO perf_test_scenarios(id,project_id,user_id,name,description,target_url,method,headers,script_content,user_count,spawn_rate,duration,status,last_run_at,avg_response_time,max_response_time,min_response_time,throughput,error_rate,tags,is_enabled,created_at,updated_at)VALUES(8,8,1,'首页并发','大量用户访问','https://example.com/','GET','{}','from locust import HttpUser',100,10,300,'pending',NULL,221.1,2104.7,66.7,92.7,3.0,'["performance"]',true,'2025-12-05 05:42:00','2026-06-01 15:57:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO perf_test_scenarios(id,project_id,user_id,name,description,target_url,method,headers,script_content,user_count,spawn_rate,duration,status,last_run_at,avg_response_time,max_response_time,min_response_time,throughput,error_rate,tags,is_enabled,created_at,updated_at)VALUES(9,8,2,'下单全流程','完整业务','https://example.com/api/v1/orders','POST','{}','from locust import HttpUser',50,5,600,'pending',NULL,257.6,1732.9,78.7,196.2,2.19,'["performance"]',true,'2026-01-21 21:25:00','2026-05-29 21:22:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO perf_test_scenarios(id,project_id,user_id,name,description,target_url,method,headers,script_content,user_count,spawn_rate,duration,status,last_run_at,avg_response_time,max_response_time,min_response_time,throughput,error_rate,tags,is_enabled,created_at,updated_at)VALUES(10,13,2,'下单全流程','完整业务','https://example.com/api/v1/orders','POST','{}','from locust import HttpUser',50,5,600,'completed','2026-05-31 13:51:00',360.0,2471.4,60.6,138.9,1.19,'["performance"]',true,'2026-03-22 05:43:00','2026-06-01 13:45:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO perf_test_scenarios(id,project_id,user_id,name,description,target_url,method,headers,script_content,user_count,spawn_rate,duration,status,last_run_at,avg_response_time,max_response_time,min_response_time,throughput,error_rate,tags,is_enabled,created_at,updated_at)VALUES(11,13,2,'商品查询','缓存性能','https://example.com/api/v1/products','GET','{}','from locust import HttpUser',150,15,300,'failed','2026-05-16 01:14:00',75.8,571.6,26.8,1945.8,1.62,'["performance"]',true,'2026-04-27 20:03:00','2026-05-29 00:40:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO perf_test_scenarios(id,project_id,user_id,name,description,target_url,method,headers,script_content,user_count,spawn_rate,duration,status,last_run_at,avg_response_time,max_response_time,min_response_time,throughput,error_rate,tags,is_enabled,created_at,updated_at)VALUES(12,13,1,'登录压测','登录高并发','https://example.com/api/v1/auth/login','POST','{}','from locust import HttpUser',200,20,180,'completed','2026-05-15 12:05:00',415.5,1884.3,202.0,394.6,4.86,'["performance"]',true,'2026-01-03 06:14:00','2026-05-27 11:36:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO perf_test_scenarios(id,project_id,user_id,name,description,target_url,method,headers,script_content,user_count,spawn_rate,duration,status,last_run_at,avg_response_time,max_response_time,min_response_time,throughput,error_rate,tags,is_enabled,created_at,updated_at)VALUES(13,14,6,'搜索压测','全文搜索','https://example.com/api/v1/search','GET','{}','from locust import HttpUser',100,10,180,'completed','2026-05-19 02:14:00',175.6,777.5,61.8,1723.5,1.98,'["performance"]',true,'2026-02-09 22:51:00','2026-05-30 07:29:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO perf_test_scenarios(id,project_id,user_id,name,description,target_url,method,headers,script_content,user_count,spawn_rate,duration,status,last_run_at,avg_response_time,max_response_time,min_response_time,throughput,error_rate,tags,is_enabled,created_at,updated_at)VALUES(14,14,2,'登录压测','登录高并发','https://example.com/api/v1/auth/login','POST','{}','from locust import HttpUser',200,20,180,'pending',NULL,108.8,983.2,19.1,1006.5,3.65,'["performance"]',true,'2025-12-18 00:59:00','2026-05-31 04:04:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO perf_test_scenarios(id,project_id,user_id,name,description,target_url,method,headers,script_content,user_count,spawn_rate,duration,status,last_run_at,avg_response_time,max_response_time,min_response_time,throughput,error_rate,tags,is_enabled,created_at,updated_at)VALUES(15,16,1,'登录压测','登录高并发','https://example.com/api/v1/auth/login','POST','{}','from locust import HttpUser',200,20,180,'pending',NULL,137.7,1289.4,67.2,245.5,2.63,'["performance"]',true,'2026-05-28 14:54:00','2026-05-29 21:59:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO perf_test_scenarios(id,project_id,user_id,name,description,target_url,method,headers,script_content,user_count,spawn_rate,duration,status,last_run_at,avg_response_time,max_response_time,min_response_time,throughput,error_rate,tags,is_enabled,created_at,updated_at)VALUES(16,16,1,'首页并发','大量用户访问','https://example.com/','GET','{}','from locust import HttpUser',100,10,300,'completed','2026-05-28 13:22:00',386.5,2903.1,45.4,534.3,0.42,'["performance"]',true,'2026-05-29 09:10:00','2026-06-01 16:13:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO perf_test_scenarios(id,project_id,user_id,name,description,target_url,method,headers,script_content,user_count,spawn_rate,duration,status,last_run_at,avg_response_time,max_response_time,min_response_time,throughput,error_rate,tags,is_enabled,created_at,updated_at)VALUES(17,16,5,'下单全流程','完整业务','https://example.com/api/v1/orders','POST','{}','from locust import HttpUser',50,5,600,'completed','2026-05-22 18:51:00',117.1,745.1,38.1,916.4,0.82,'["performance"]',true,'2026-03-31 08:26:00','2026-05-28 01:20:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO performance_test_results(id,scenario_id,project_id,user_count,spawn_rate,duration,target_url,status,started_at,finished_at,total_requests,total_failures,error_rate,rps,avg_response_time,min_response_time,max_response_time,p50_response_time,p75_response_time,p95_response_time,p99_response_time,created_at,updated_at)VALUES(1,1,1,67,1,363,'https://example.com/api','completed','2026-05-27 08:54:00','2026-05-27 09:00:03',34524,1530,4.43,1275.1,15.5,4.6,77.5,10.8,20.2,38.8,62.0,'2026-05-27 08:54:00','2026-05-27 09:00:03')ON CONFLICT(id)DO NOTHING;

INSERT INTO performance_metric_samples(test_result_id,timestamp,elapsed_seconds,rps,active_users,avg_response_time,min_response_time,max_response_time,p95_response_time,p99_response_time,request_count,failure_count,error_rate)VALUES(1,'2026-05-27 08:54:00',0,1066.0,3,13.3,4.6,46.5,31.0,62.0,4315,191,1.97);

INSERT INTO performance_metric_samples(test_result_id,timestamp,elapsed_seconds,rps,active_users,avg_response_time,min_response_time,max_response_time,p95_response_time,p99_response_time,request_count,failure_count,error_rate)VALUES(1,'2026-05-27 08:54:01',1,1065.4,6,14.8,4.6,46.5,31.0,62.0,8631,382,2.65);

INSERT INTO performance_metric_samples(test_result_id,timestamp,elapsed_seconds,rps,active_users,avg_response_time,min_response_time,max_response_time,p95_response_time,p99_response_time,request_count,failure_count,error_rate)VALUES(1,'2026-05-27 08:54:02',2,1522.0,9,15.4,4.6,46.5,31.0,62.0,12946,573,2.97);

INSERT INTO performance_metric_samples(test_result_id,timestamp,elapsed_seconds,rps,active_users,avg_response_time,min_response_time,max_response_time,p95_response_time,p99_response_time,request_count,failure_count,error_rate)VALUES(1,'2026-05-27 08:54:03',3,1064.3,12,14.6,4.6,46.5,31.0,62.0,17262,765,1.85);

INSERT INTO performance_metric_samples(test_result_id,timestamp,elapsed_seconds,rps,active_users,avg_response_time,min_response_time,max_response_time,p95_response_time,p99_response_time,request_count,failure_count,error_rate)VALUES(1,'2026-05-27 08:54:04',4,983.1,15,18.0,4.6,46.5,31.0,62.0,21577,956,1.81);

INSERT INTO performance_metric_samples(test_result_id,timestamp,elapsed_seconds,rps,active_users,avg_response_time,min_response_time,max_response_time,p95_response_time,p99_response_time,request_count,failure_count,error_rate)VALUES(1,'2026-05-27 08:54:05',5,1028.8,18,14.5,4.6,46.5,31.0,62.0,25893,1147,0.54);

INSERT INTO performance_metric_samples(test_result_id,timestamp,elapsed_seconds,rps,active_users,avg_response_time,min_response_time,max_response_time,p95_response_time,p99_response_time,request_count,failure_count,error_rate)VALUES(1,'2026-05-27 08:54:06',6,1217.9,21,16.7,4.6,46.5,31.0,62.0,30208,1338,1.87);

INSERT INTO performance_metric_samples(test_result_id,timestamp,elapsed_seconds,rps,active_users,avg_response_time,min_response_time,max_response_time,p95_response_time,p99_response_time,request_count,failure_count,error_rate)VALUES(1,'2026-05-27 08:54:07',7,1112.1,24,14.1,4.6,46.5,31.0,62.0,34524,1530,1.5);

INSERT INTO performance_test_results(id,scenario_id,project_id,user_count,spawn_rate,duration,target_url,status,started_at,finished_at,total_requests,total_failures,error_rate,rps,avg_response_time,min_response_time,max_response_time,p50_response_time,p75_response_time,p95_response_time,p99_response_time,created_at,updated_at)VALUES(2,1,1,124,16,138,'https://example.com/api','completed','2026-02-27 01:09:00','2026-02-27 01:11:18',10741,417,3.88,482.4,71.9,21.6,359.5,50.3,93.5,179.8,287.6,'2026-02-27 01:09:00','2026-02-27 01:11:18')ON CONFLICT(id)DO NOTHING;

INSERT INTO performance_metric_samples(test_result_id,timestamp,elapsed_seconds,rps,active_users,avg_response_time,min_response_time,max_response_time,p95_response_time,p99_response_time,request_count,failure_count,error_rate)VALUES(2,'2026-02-27 01:09:00',0,573.5,3,74.1,21.6,215.7,143.8,287.6,1342,52,2.88);

INSERT INTO performance_metric_samples(test_result_id,timestamp,elapsed_seconds,rps,active_users,avg_response_time,min_response_time,max_response_time,p95_response_time,p99_response_time,request_count,failure_count,error_rate)VALUES(2,'2026-02-27 01:09:01',1,418.3,6,66.8,21.6,215.7,143.8,287.6,2685,104,0.38);

INSERT INTO performance_metric_samples(test_result_id,timestamp,elapsed_seconds,rps,active_users,avg_response_time,min_response_time,max_response_time,p95_response_time,p99_response_time,request_count,failure_count,error_rate)VALUES(2,'2026-02-27 01:09:02',2,559.8,9,66.7,21.6,215.7,143.8,287.6,4027,156,1.27);

INSERT INTO performance_metric_samples(test_result_id,timestamp,elapsed_seconds,rps,active_users,avg_response_time,min_response_time,max_response_time,p95_response_time,p99_response_time,request_count,failure_count,error_rate)VALUES(2,'2026-02-27 01:09:03',3,538.4,12,74.8,21.6,215.7,143.8,287.6,5370,208,1.91);

INSERT INTO performance_metric_samples(test_result_id,timestamp,elapsed_seconds,rps,active_users,avg_response_time,min_response_time,max_response_time,p95_response_time,p99_response_time,request_count,failure_count,error_rate)VALUES(2,'2026-02-27 01:09:04',4,377.7,15,84.0,21.6,215.7,143.8,287.6,6713,260,1.15);

INSERT INTO performance_metric_samples(test_result_id,timestamp,elapsed_seconds,rps,active_users,avg_response_time,min_response_time,max_response_time,p95_response_time,p99_response_time,request_count,failure_count,error_rate)VALUES(2,'2026-02-27 01:09:05',5,496.7,18,72.9,21.6,215.7,143.8,287.6,8055,312,1.6);

INSERT INTO performance_metric_samples(test_result_id,timestamp,elapsed_seconds,rps,active_users,avg_response_time,min_response_time,max_response_time,p95_response_time,p99_response_time,request_count,failure_count,error_rate)VALUES(2,'2026-02-27 01:09:06',6,575.4,21,59.9,21.6,215.7,143.8,287.6,9398,364,2.14);

INSERT INTO performance_metric_samples(test_result_id,timestamp,elapsed_seconds,rps,active_users,avg_response_time,min_response_time,max_response_time,p95_response_time,p99_response_time,request_count,failure_count,error_rate)VALUES(2,'2026-02-27 01:09:07',7,490.2,24,77.5,21.6,215.7,143.8,287.6,10741,417,2.24);

INSERT INTO performance_test_results(id,scenario_id,project_id,user_count,spawn_rate,duration,target_url,status,started_at,finished_at,total_requests,total_failures,error_rate,rps,avg_response_time,min_response_time,max_response_time,p50_response_time,p75_response_time,p95_response_time,p99_response_time,created_at,updated_at)VALUES(3,1,1,38,2,62,'https://example.com/api','completed','2026-05-10 02:37:00','2026-05-10 02:38:02',2124,38,1.79,1448.1,66.4,19.9,332.0,46.5,86.3,166.0,265.6,'2026-05-10 02:37:00','2026-05-10 02:38:02')ON CONFLICT(id)DO NOTHING;

INSERT INTO performance_metric_samples(test_result_id,timestamp,elapsed_seconds,rps,active_users,avg_response_time,min_response_time,max_response_time,p95_response_time,p99_response_time,request_count,failure_count,error_rate)VALUES(3,'2026-05-10 02:37:00',0,1805.5,3,75.7,19.9,199.2,132.8,265.6,265,4,2.6);

INSERT INTO performance_metric_samples(test_result_id,timestamp,elapsed_seconds,rps,active_users,avg_response_time,min_response_time,max_response_time,p95_response_time,p99_response_time,request_count,failure_count,error_rate)VALUES(3,'2026-05-10 02:37:01',1,1725.3,6,65.3,19.9,199.2,132.8,265.6,531,9,2.51);

INSERT INTO performance_metric_samples(test_result_id,timestamp,elapsed_seconds,rps,active_users,avg_response_time,min_response_time,max_response_time,p95_response_time,p99_response_time,request_count,failure_count,error_rate)VALUES(3,'2026-05-10 02:37:02',2,1492.8,9,59.6,19.9,199.2,132.8,265.6,796,14,2.48);

INSERT INTO performance_metric_samples(test_result_id,timestamp,elapsed_seconds,rps,active_users,avg_response_time,min_response_time,max_response_time,p95_response_time,p99_response_time,request_count,failure_count,error_rate)VALUES(3,'2026-05-10 02:37:03',3,1062.2,12,56.2,19.9,199.2,132.8,265.6,1062,19,2.09);

INSERT INTO performance_metric_samples(test_result_id,timestamp,elapsed_seconds,rps,active_users,avg_response_time,min_response_time,max_response_time,p95_response_time,p99_response_time,request_count,failure_count,error_rate)VALUES(3,'2026-05-10 02:37:04',4,1138.0,15,53.8,19.9,199.2,132.8,265.6,1327,23,2.89);

INSERT INTO performance_metric_samples(test_result_id,timestamp,elapsed_seconds,rps,active_users,avg_response_time,min_response_time,max_response_time,p95_response_time,p99_response_time,request_count,failure_count,error_rate)VALUES(3,'2026-05-10 02:37:05',5,1336.6,18,55.9,19.9,199.2,132.8,265.6,1593,28,1.74);

INSERT INTO performance_metric_samples(test_result_id,timestamp,elapsed_seconds,rps,active_users,avg_response_time,min_response_time,max_response_time,p95_response_time,p99_response_time,request_count,failure_count,error_rate)VALUES(3,'2026-05-10 02:37:06',6,1428.0,21,76.2,19.9,199.2,132.8,265.6,1858,33,0.09);

INSERT INTO performance_metric_samples(test_result_id,timestamp,elapsed_seconds,rps,active_users,avg_response_time,min_response_time,max_response_time,p95_response_time,p99_response_time,request_count,failure_count,error_rate)VALUES(3,'2026-05-10 02:37:07',7,1331.0,21,59.6,19.9,199.2,132.8,265.6,2124,38,0.04);

INSERT INTO performance_test_results(id,scenario_id,project_id,user_count,spawn_rate,duration,target_url,status,started_at,finished_at,total_requests,total_failures,error_rate,rps,avg_response_time,min_response_time,max_response_time,p50_response_time,p75_response_time,p95_response_time,p99_response_time,created_at,updated_at)VALUES(4,2,1,187,1,203,'https://example.com/api','completed','2026-04-24 04:30:00','2026-04-24 04:33:23',31814,654,2.06,1045.1,315.8,94.7,1579.0,221.1,410.5,789.5,1263.2,'2026-04-24 04:30:00','2026-04-24 04:33:23')ON CONFLICT(id)DO NOTHING;

INSERT INTO performance_metric_samples(test_result_id,timestamp,elapsed_seconds,rps,active_users,avg_response_time,min_response_time,max_response_time,p95_response_time,p99_response_time,request_count,failure_count,error_rate)VALUES(4,'2026-04-24 04:30:00',0,911.4,3,260.2,94.7,947.4,631.6,1263.2,3976,81,1.93);

INSERT INTO performance_metric_samples(test_result_id,timestamp,elapsed_seconds,rps,active_users,avg_response_time,min_response_time,max_response_time,p95_response_time,p99_response_time,request_count,failure_count,error_rate)VALUES(4,'2026-04-24 04:30:01',1,1110.4,6,316.2,94.7,947.4,631.6,1263.2,7953,163,0.03);

INSERT INTO performance_metric_samples(test_result_id,timestamp,elapsed_seconds,rps,active_users,avg_response_time,min_response_time,max_response_time,p95_response_time,p99_response_time,request_count,failure_count,error_rate)VALUES(4,'2026-04-24 04:30:02',2,1253.7,9,372.4,94.7,947.4,631.6,1263.2,11930,245,1.36);

INSERT INTO performance_metric_samples(test_result_id,timestamp,elapsed_seconds,rps,active_users,avg_response_time,min_response_time,max_response_time,p95_response_time,p99_response_time,request_count,failure_count,error_rate)VALUES(4,'2026-04-24 04:30:03',3,1177.7,12,368.7,94.7,947.4,631.6,1263.2,15907,327,1.51);

INSERT INTO performance_metric_samples(test_result_id,timestamp,elapsed_seconds,rps,active_users,avg_response_time,min_response_time,max_response_time,p95_response_time,p99_response_time,request_count,failure_count,error_rate)VALUES(4,'2026-04-24 04:30:04',4,1176.4,15,370.3,94.7,947.4,631.6,1263.2,19883,408,0.82);

INSERT INTO performance_metric_samples(test_result_id,timestamp,elapsed_seconds,rps,active_users,avg_response_time,min_response_time,max_response_time,p95_response_time,p99_response_time,request_count,failure_count,error_rate)VALUES(4,'2026-04-24 04:30:05',5,789.2,18,376.2,94.7,947.4,631.6,1263.2,23860,490,0.38);

INSERT INTO performance_metric_samples(test_result_id,timestamp,elapsed_seconds,rps,active_users,avg_response_time,min_response_time,max_response_time,p95_response_time,p99_response_time,request_count,failure_count,error_rate)VALUES(4,'2026-04-24 04:30:06',6,864.4,21,259.7,94.7,947.4,631.6,1263.2,27837,572,1.18);

INSERT INTO performance_metric_samples(test_result_id,timestamp,elapsed_seconds,rps,active_users,avg_response_time,min_response_time,max_response_time,p95_response_time,p99_response_time,request_count,failure_count,error_rate)VALUES(4,'2026-04-24 04:30:07',7,1247.3,24,329.1,94.7,947.4,631.6,1263.2,31814,654,0.23);

INSERT INTO performance_test_results(id,scenario_id,project_id,user_count,spawn_rate,duration,target_url,status,started_at,finished_at,total_requests,total_failures,error_rate,rps,avg_response_time,min_response_time,max_response_time,p50_response_time,p75_response_time,p95_response_time,p99_response_time,created_at,updated_at)VALUES(5,2,1,79,4,474,'https://example.com/api','failed','2026-02-01 18:40:00','2026-02-01 18:47:54',11801,32,0.27,1145.9,178.3,53.5,891.5,124.8,231.8,445.8,713.2,'2026-02-01 18:40:00','2026-02-01 18:47:54')ON CONFLICT(id)DO NOTHING;

INSERT INTO performance_metric_samples(test_result_id,timestamp,elapsed_seconds,rps,active_users,avg_response_time,min_response_time,max_response_time,p95_response_time,p99_response_time,request_count,failure_count,error_rate)VALUES(5,'2026-02-01 18:40:00',0,873.9,3,185.7,53.5,534.9,356.6,713.2,1475,4,2.54);

INSERT INTO performance_metric_samples(test_result_id,timestamp,elapsed_seconds,rps,active_users,avg_response_time,min_response_time,max_response_time,p95_response_time,p99_response_time,request_count,failure_count,error_rate)VALUES(5,'2026-02-01 18:40:01',1,821.4,6,154.2,53.5,534.9,356.6,713.2,2950,8,0.32);

INSERT INTO performance_metric_samples(test_result_id,timestamp,elapsed_seconds,rps,active_users,avg_response_time,min_response_time,max_response_time,p95_response_time,p99_response_time,request_count,failure_count,error_rate)VALUES(5,'2026-02-01 18:40:02',2,947.8,3,196.6,53.5,534.9,356.6,713.2,4425,12,0.93);

INSERT INTO performance_metric_samples(test_result_id,timestamp,elapsed_seconds,rps,active_users,avg_response_time,min_response_time,max_response_time,p95_response_time,p99_response_time,request_count,failure_count,error_rate)VALUES(5,'2026-02-01 18:40:03',3,1181.4,12,208.9,53.5,534.9,356.6,713.2,5900,16,0.72);

INSERT INTO performance_metric_samples(test_result_id,timestamp,elapsed_seconds,rps,active_users,avg_response_time,min_response_time,max_response_time,p95_response_time,p99_response_time,request_count,failure_count,error_rate)VALUES(5,'2026-02-01 18:40:04',4,860.6,15,182.9,53.5,534.9,356.6,713.2,7375,20,1.69);

INSERT INTO performance_metric_samples(test_result_id,timestamp,elapsed_seconds,rps,active_users,avg_response_time,min_response_time,max_response_time,p95_response_time,p99_response_time,request_count,failure_count,error_rate)VALUES(5,'2026-02-01 18:40:05',5,1345.4,12,146.1,53.5,534.9,356.6,713.2,8850,24,0.28);

INSERT INTO performance_metric_samples(test_result_id,timestamp,elapsed_seconds,rps,active_users,avg_response_time,min_response_time,max_response_time,p95_response_time,p99_response_time,request_count,failure_count,error_rate)VALUES(5,'2026-02-01 18:40:06',6,1014.3,21,196.2,53.5,534.9,356.6,713.2,10325,28,2.88);

INSERT INTO performance_metric_samples(test_result_id,timestamp,elapsed_seconds,rps,active_users,avg_response_time,min_response_time,max_response_time,p95_response_time,p99_response_time,request_count,failure_count,error_rate)VALUES(5,'2026-02-01 18:40:07',7,1146.0,24,196.3,53.5,534.9,356.6,713.2,11801,32,2.18);

INSERT INTO performance_test_results(id,scenario_id,project_id,user_count,spawn_rate,duration,target_url,status,started_at,finished_at,total_requests,total_failures,error_rate,rps,avg_response_time,min_response_time,max_response_time,p50_response_time,p75_response_time,p95_response_time,p99_response_time,created_at,updated_at)VALUES(6,2,1,48,1,159,'https://example.com/api','completed','2026-04-28 11:17:00','2026-04-28 11:19:39',27691,1241,4.48,1535.6,208.3,62.5,1041.5,145.8,270.8,520.8,833.2,'2026-04-28 11:17:00','2026-04-28 11:19:39')ON CONFLICT(id)DO NOTHING;

INSERT INTO performance_metric_samples(test_result_id,timestamp,elapsed_seconds,rps,active_users,avg_response_time,min_response_time,max_response_time,p95_response_time,p99_response_time,request_count,failure_count,error_rate)VALUES(6,'2026-04-28 11:17:00',0,1615.9,3,206.4,62.5,624.9,416.6,833.2,3461,155,2.61);

INSERT INTO performance_metric_samples(test_result_id,timestamp,elapsed_seconds,rps,active_users,avg_response_time,min_response_time,max_response_time,p95_response_time,p99_response_time,request_count,failure_count,error_rate)VALUES(6,'2026-04-28 11:17:01',1,1109.4,6,179.3,62.5,624.9,416.6,833.2,6922,310,1.39);

INSERT INTO performance_metric_samples(test_result_id,timestamp,elapsed_seconds,rps,active_users,avg_response_time,min_response_time,max_response_time,p95_response_time,p99_response_time,request_count,failure_count,error_rate)VALUES(6,'2026-04-28 11:17:02',2,1890.5,9,246.0,62.5,624.9,416.6,833.2,10384,465,0.69);

INSERT INTO performance_metric_samples(test_result_id,timestamp,elapsed_seconds,rps,active_users,avg_response_time,min_response_time,max_response_time,p95_response_time,p99_response_time,request_count,failure_count,error_rate)VALUES(6,'2026-04-28 11:17:03',3,1273.6,12,221.1,62.5,624.9,416.6,833.2,13845,620,2.31);

INSERT INTO performance_metric_samples(test_result_id,timestamp,elapsed_seconds,rps,active_users,avg_response_time,min_response_time,max_response_time,p95_response_time,p99_response_time,request_count,failure_count,error_rate)VALUES(6,'2026-04-28 11:17:04',4,1223.3,15,209.7,62.5,624.9,416.6,833.2,17306,775,2.19);

INSERT INTO performance_metric_samples(test_result_id,timestamp,elapsed_seconds,rps,active_users,avg_response_time,min_response_time,max_response_time,p95_response_time,p99_response_time,request_count,failure_count,error_rate)VALUES(6,'2026-04-28 11:17:05',5,1675.1,18,195.1,62.5,624.9,416.6,833.2,20768,930,2.36);

INSERT INTO performance_metric_samples(test_result_id,timestamp,elapsed_seconds,rps,active_users,avg_response_time,min_response_time,max_response_time,p95_response_time,p99_response_time,request_count,failure_count,error_rate)VALUES(6,'2026-04-28 11:17:06',6,1387.3,21,218.6,62.5,624.9,416.6,833.2,24229,1085,2.82);

INSERT INTO performance_metric_samples(test_result_id,timestamp,elapsed_seconds,rps,active_users,avg_response_time,min_response_time,max_response_time,p95_response_time,p99_response_time,request_count,failure_count,error_rate)VALUES(6,'2026-04-28 11:17:07',7,1111.8,24,231.1,62.5,624.9,416.6,833.2,27691,1241,1.16);

INSERT INTO performance_test_results(id,scenario_id,project_id,user_count,spawn_rate,duration,target_url,status,started_at,finished_at,total_requests,total_failures,error_rate,rps,avg_response_time,min_response_time,max_response_time,p50_response_time,p75_response_time,p95_response_time,p99_response_time,created_at,updated_at)VALUES(7,2,1,46,10,136,'https://example.com/api','completed','2026-04-08 14:22:00','2026-04-08 14:24:16',38152,1197,3.14,1517.7,324.8,97.4,1624.0,227.4,422.2,812.0,1299.2,'2026-04-08 14:22:00','2026-04-08 14:24:16')ON CONFLICT(id)DO NOTHING;

INSERT INTO performance_metric_samples(test_result_id,timestamp,elapsed_seconds,rps,active_users,avg_response_time,min_response_time,max_response_time,p95_response_time,p99_response_time,request_count,failure_count,error_rate)VALUES(7,'2026-04-08 14:22:00',0,1560.6,3,324.7,97.4,974.4,649.6,1299.2,4769,149,1.36);

INSERT INTO performance_metric_samples(test_result_id,timestamp,elapsed_seconds,rps,active_users,avg_response_time,min_response_time,max_response_time,p95_response_time,p99_response_time,request_count,failure_count,error_rate)VALUES(7,'2026-04-08 14:22:01',1,1216.9,6,280.8,97.4,974.4,649.6,1299.2,9538,299,0.84);

INSERT INTO performance_metric_samples(test_result_id,timestamp,elapsed_seconds,rps,active_users,avg_response_time,min_response_time,max_response_time,p95_response_time,p99_response_time,request_count,failure_count,error_rate)VALUES(7,'2026-04-08 14:22:02',2,1393.2,9,269.1,97.4,974.4,649.6,1299.2,14307,448,2.13);

INSERT INTO performance_metric_samples(test_result_id,timestamp,elapsed_seconds,rps,active_users,avg_response_time,min_response_time,max_response_time,p95_response_time,p99_response_time,request_count,failure_count,error_rate)VALUES(7,'2026-04-08 14:22:03',3,1482.0,12,387.0,97.4,974.4,649.6,1299.2,19076,598,2.29);

INSERT INTO performance_metric_samples(test_result_id,timestamp,elapsed_seconds,rps,active_users,avg_response_time,min_response_time,max_response_time,p95_response_time,p99_response_time,request_count,failure_count,error_rate)VALUES(7,'2026-04-08 14:22:04',4,1464.9,15,381.9,97.4,974.4,649.6,1299.2,23845,748,2.92);

INSERT INTO performance_metric_samples(test_result_id,timestamp,elapsed_seconds,rps,active_users,avg_response_time,min_response_time,max_response_time,p95_response_time,p99_response_time,request_count,failure_count,error_rate)VALUES(7,'2026-04-08 14:22:05',5,1507.0,18,371.4,97.4,974.4,649.6,1299.2,28614,897,1.2);

INSERT INTO performance_metric_samples(test_result_id,timestamp,elapsed_seconds,rps,active_users,avg_response_time,min_response_time,max_response_time,p95_response_time,p99_response_time,request_count,failure_count,error_rate)VALUES(7,'2026-04-08 14:22:06',6,1842.8,21,276.6,97.4,974.4,649.6,1299.2,33383,1047,1.1);

INSERT INTO performance_metric_samples(test_result_id,timestamp,elapsed_seconds,rps,active_users,avg_response_time,min_response_time,max_response_time,p95_response_time,p99_response_time,request_count,failure_count,error_rate)VALUES(7,'2026-04-08 14:22:07',7,1831.7,24,308.4,97.4,974.4,649.6,1299.2,38152,1197,2.05);

INSERT INTO performance_test_results(id,scenario_id,project_id,user_count,spawn_rate,duration,target_url,status,started_at,finished_at,total_requests,total_failures,error_rate,rps,avg_response_time,min_response_time,max_response_time,p50_response_time,p75_response_time,p95_response_time,p99_response_time,created_at,updated_at)VALUES(8,2,1,49,4,103,'https://example.com/api','completed','2026-01-22 19:44:00','2026-01-22 19:45:43',49564,1959,3.95,2114.2,230.9,69.3,1154.5,161.6,300.2,577.2,923.6,'2026-01-22 19:44:00','2026-01-22 19:45:43')ON CONFLICT(id)DO NOTHING;

INSERT INTO performance_metric_samples(test_result_id,timestamp,elapsed_seconds,rps,active_users,avg_response_time,min_response_time,max_response_time,p95_response_time,p99_response_time,request_count,failure_count,error_rate)VALUES(8,'2026-01-22 19:44:00',0,1848.6,3,237.4,69.3,692.7,461.8,923.6,6195,244,2.56);

INSERT INTO performance_metric_samples(test_result_id,timestamp,elapsed_seconds,rps,active_users,avg_response_time,min_response_time,max_response_time,p95_response_time,p99_response_time,request_count,failure_count,error_rate)VALUES(8,'2026-01-22 19:44:01',1,1762.9,6,246.5,69.3,692.7,461.8,923.6,12391,489,1.05);

INSERT INTO performance_metric_samples(test_result_id,timestamp,elapsed_seconds,rps,active_users,avg_response_time,min_response_time,max_response_time,p95_response_time,p99_response_time,request_count,failure_count,error_rate)VALUES(8,'2026-01-22 19:44:02',2,2074.2,9,267.9,69.3,692.7,461.8,923.6,18586,734,1.39);

INSERT INTO performance_metric_samples(test_result_id,timestamp,elapsed_seconds,rps,active_users,avg_response_time,min_response_time,max_response_time,p95_response_time,p99_response_time,request_count,failure_count,error_rate)VALUES(8,'2026-01-22 19:44:03',3,1588.8,12,194.7,69.3,692.7,461.8,923.6,24782,979,2.88);

INSERT INTO performance_metric_samples(test_result_id,timestamp,elapsed_seconds,rps,active_users,avg_response_time,min_response_time,max_response_time,p95_response_time,p99_response_time,request_count,failure_count,error_rate)VALUES(8,'2026-01-22 19:44:04',4,1983.5,15,203.1,69.3,692.7,461.8,923.6,30977,1224,0.99);

INSERT INTO performance_metric_samples(test_result_id,timestamp,elapsed_seconds,rps,active_users,avg_response_time,min_response_time,max_response_time,p95_response_time,p99_response_time,request_count,failure_count,error_rate)VALUES(8,'2026-01-22 19:44:05',5,1882.4,18,229.6,69.3,692.7,461.8,923.6,37173,1469,2.11);

INSERT INTO performance_metric_samples(test_result_id,timestamp,elapsed_seconds,rps,active_users,avg_response_time,min_response_time,max_response_time,p95_response_time,p99_response_time,request_count,failure_count,error_rate)VALUES(8,'2026-01-22 19:44:06',6,2084.0,21,226.7,69.3,692.7,461.8,923.6,43368,1714,1.64);

INSERT INTO performance_metric_samples(test_result_id,timestamp,elapsed_seconds,rps,active_users,avg_response_time,min_response_time,max_response_time,p95_response_time,p99_response_time,request_count,failure_count,error_rate)VALUES(8,'2026-01-22 19:44:07',7,2683.2,24,243.9,69.3,692.7,461.8,923.6,49564,1959,0.96);

INSERT INTO performance_test_results(id,scenario_id,project_id,user_count,spawn_rate,duration,target_url,status,started_at,finished_at,total_requests,total_failures,error_rate,rps,avg_response_time,min_response_time,max_response_time,p50_response_time,p75_response_time,p95_response_time,p99_response_time,created_at,updated_at)VALUES(9,2,1,64,1,449,'https://example.com/api','completed','2026-05-23 14:11:00','2026-05-23 14:18:29',24690,974,3.94,2936.8,97.2,29.2,486.0,68.0,126.4,243.0,388.8,'2026-05-23 14:11:00','2026-05-23 14:18:29')ON CONFLICT(id)DO NOTHING;

INSERT INTO performance_metric_samples(test_result_id,timestamp,elapsed_seconds,rps,active_users,avg_response_time,min_response_time,max_response_time,p95_response_time,p99_response_time,request_count,failure_count,error_rate)VALUES(9,'2026-05-23 14:11:00',0,3734.4,3,94.2,29.2,291.6,194.4,388.8,3086,121,0.76);

INSERT INTO performance_metric_samples(test_result_id,timestamp,elapsed_seconds,rps,active_users,avg_response_time,min_response_time,max_response_time,p95_response_time,p99_response_time,request_count,failure_count,error_rate)VALUES(9,'2026-05-23 14:11:01',1,2366.1,6,80.5,29.2,291.6,194.4,388.8,6172,243,1.22);

INSERT INTO performance_metric_samples(test_result_id,timestamp,elapsed_seconds,rps,active_users,avg_response_time,min_response_time,max_response_time,p95_response_time,p99_response_time,request_count,failure_count,error_rate)VALUES(9,'2026-05-23 14:11:02',2,2581.5,9,95.3,29.2,291.6,194.4,388.8,9258,365,1.26);

INSERT INTO performance_metric_samples(test_result_id,timestamp,elapsed_seconds,rps,active_users,avg_response_time,min_response_time,max_response_time,p95_response_time,p99_response_time,request_count,failure_count,error_rate)VALUES(9,'2026-05-23 14:11:03',3,2433.0,12,84.9,29.2,291.6,194.4,388.8,12345,487,0.16);

INSERT INTO performance_metric_samples(test_result_id,timestamp,elapsed_seconds,rps,active_users,avg_response_time,min_response_time,max_response_time,p95_response_time,p99_response_time,request_count,failure_count,error_rate)VALUES(9,'2026-05-23 14:11:04',4,3632.7,15,91.1,29.2,291.6,194.4,388.8,15431,608,2.26);

INSERT INTO performance_metric_samples(test_result_id,timestamp,elapsed_seconds,rps,active_users,avg_response_time,min_response_time,max_response_time,p95_response_time,p99_response_time,request_count,failure_count,error_rate)VALUES(9,'2026-05-23 14:11:05',5,2345.7,18,114.4,29.2,291.6,194.4,388.8,18517,730,1.44);

INSERT INTO performance_metric_samples(test_result_id,timestamp,elapsed_seconds,rps,active_users,avg_response_time,min_response_time,max_response_time,p95_response_time,p99_response_time,request_count,failure_count,error_rate)VALUES(9,'2026-05-23 14:11:06',6,2999.4,21,115.3,29.2,291.6,194.4,388.8,21603,852,1.31);

INSERT INTO performance_metric_samples(test_result_id,timestamp,elapsed_seconds,rps,active_users,avg_response_time,min_response_time,max_response_time,p95_response_time,p99_response_time,request_count,failure_count,error_rate)VALUES(9,'2026-05-23 14:11:07',7,3663.8,24,92.9,29.2,291.6,194.4,388.8,24690,974,0.03);

INSERT INTO performance_test_results(id,scenario_id,project_id,user_count,spawn_rate,duration,target_url,status,started_at,finished_at,total_requests,total_failures,error_rate,rps,avg_response_time,min_response_time,max_response_time,p50_response_time,p75_response_time,p95_response_time,p99_response_time,created_at,updated_at)VALUES(10,3,3,198,11,208,'https://example.com/api','completed','2026-05-12 10:18:00','2026-05-12 10:21:28',44520,2195,4.93,2820.0,301.0,90.3,1505.0,210.7,391.3,752.5,1204.0,'2026-05-12 10:18:00','2026-05-12 10:21:28')ON CONFLICT(id)DO NOTHING;

INSERT INTO performance_metric_samples(test_result_id,timestamp,elapsed_seconds,rps,active_users,avg_response_time,min_response_time,max_response_time,p95_response_time,p99_response_time,request_count,failure_count,error_rate)VALUES(10,'2026-05-12 10:18:00',0,1998.0,3,353.2,90.3,903.0,602.0,1204.0,5565,274,1.5);

INSERT INTO performance_metric_samples(test_result_id,timestamp,elapsed_seconds,rps,active_users,avg_response_time,min_response_time,max_response_time,p95_response_time,p99_response_time,request_count,failure_count,error_rate)VALUES(10,'2026-05-12 10:18:01',1,2509.4,6,289.7,90.3,903.0,602.0,1204.0,11130,548,1.56);

INSERT INTO performance_metric_samples(test_result_id,timestamp,elapsed_seconds,rps,active_users,avg_response_time,min_response_time,max_response_time,p95_response_time,p99_response_time,request_count,failure_count,error_rate)VALUES(10,'2026-05-12 10:18:02',2,1980.2,9,354.4,90.3,903.0,602.0,1204.0,16695,823,2.57);

INSERT INTO performance_metric_samples(test_result_id,timestamp,elapsed_seconds,rps,active_users,avg_response_time,min_response_time,max_response_time,p95_response_time,p99_response_time,request_count,failure_count,error_rate)VALUES(10,'2026-05-12 10:18:03',3,3047.2,12,357.5,90.3,903.0,602.0,1204.0,22260,1097,0.29);

INSERT INTO performance_metric_samples(test_result_id,timestamp,elapsed_seconds,rps,active_users,avg_response_time,min_response_time,max_response_time,p95_response_time,p99_response_time,request_count,failure_count,error_rate)VALUES(10,'2026-05-12 10:18:04',4,2343.9,15,291.4,90.3,903.0,602.0,1204.0,27825,1371,1.64);

INSERT INTO performance_metric_samples(test_result_id,timestamp,elapsed_seconds,rps,active_users,avg_response_time,min_response_time,max_response_time,p95_response_time,p99_response_time,request_count,failure_count,error_rate)VALUES(10,'2026-05-12 10:18:05',5,2255.0,18,266.8,90.3,903.0,602.0,1204.0,33390,1646,0.63);

INSERT INTO performance_metric_samples(test_result_id,timestamp,elapsed_seconds,rps,active_users,avg_response_time,min_response_time,max_response_time,p95_response_time,p99_response_time,request_count,failure_count,error_rate)VALUES(10,'2026-05-12 10:18:06',6,2297.4,21,310.3,90.3,903.0,602.0,1204.0,38955,1920,0.04);

INSERT INTO performance_metric_samples(test_result_id,timestamp,elapsed_seconds,rps,active_users,avg_response_time,min_response_time,max_response_time,p95_response_time,p99_response_time,request_count,failure_count,error_rate)VALUES(10,'2026-05-12 10:18:07',7,3350.9,5,277.2,90.3,903.0,602.0,1204.0,44520,2195,0.92);

INSERT INTO performance_test_results(id,scenario_id,project_id,user_count,spawn_rate,duration,target_url,status,started_at,finished_at,total_requests,total_failures,error_rate,rps,avg_response_time,min_response_time,max_response_time,p50_response_time,p75_response_time,p95_response_time,p99_response_time,created_at,updated_at)VALUES(11,3,3,95,4,526,'https://example.com/api','failed','2026-04-30 11:29:00','2026-04-30 11:37:46',27895,490,1.76,2493.1,179.0,53.7,895.0,125.3,232.7,447.5,716.0,'2026-04-30 11:29:00','2026-04-30 11:37:46')ON CONFLICT(id)DO NOTHING;

INSERT INTO performance_metric_samples(test_result_id,timestamp,elapsed_seconds,rps,active_users,avg_response_time,min_response_time,max_response_time,p95_response_time,p99_response_time,request_count,failure_count,error_rate)VALUES(11,'2026-04-30 11:29:00',0,3130.9,3,173.9,53.7,537.0,358.0,716.0,3486,61,0.53);

INSERT INTO performance_metric_samples(test_result_id,timestamp,elapsed_seconds,rps,active_users,avg_response_time,min_response_time,max_response_time,p95_response_time,p99_response_time,request_count,failure_count,error_rate)VALUES(11,'2026-04-30 11:29:01',1,2635.0,6,174.4,53.7,537.0,358.0,716.0,6973,122,0.86);

INSERT INTO performance_metric_samples(test_result_id,timestamp,elapsed_seconds,rps,active_users,avg_response_time,min_response_time,max_response_time,p95_response_time,p99_response_time,request_count,failure_count,error_rate)VALUES(11,'2026-04-30 11:29:02',2,2731.8,9,174.5,53.7,537.0,358.0,716.0,10460,183,0.85);

INSERT INTO performance_metric_samples(test_result_id,timestamp,elapsed_seconds,rps,active_users,avg_response_time,min_response_time,max_response_time,p95_response_time,p99_response_time,request_count,failure_count,error_rate)VALUES(11,'2026-04-30 11:29:03',3,2673.2,12,214.5,53.7,537.0,358.0,716.0,13947,245,2.42);

INSERT INTO performance_metric_samples(test_result_id,timestamp,elapsed_seconds,rps,active_users,avg_response_time,min_response_time,max_response_time,p95_response_time,p99_response_time,request_count,failure_count,error_rate)VALUES(11,'2026-04-30 11:29:04',4,1900.5,15,144.4,53.7,537.0,358.0,716.0,17434,306,2.8);

INSERT INTO performance_metric_samples(test_result_id,timestamp,elapsed_seconds,rps,active_users,avg_response_time,min_response_time,max_response_time,p95_response_time,p99_response_time,request_count,failure_count,error_rate)VALUES(11,'2026-04-30 11:29:05',5,1900.3,18,197.0,53.7,537.0,358.0,716.0,20921,367,2.78);

INSERT INTO performance_metric_samples(test_result_id,timestamp,elapsed_seconds,rps,active_users,avg_response_time,min_response_time,max_response_time,p95_response_time,p99_response_time,request_count,failure_count,error_rate)VALUES(11,'2026-04-30 11:29:06',6,1894.3,21,179.2,53.7,537.0,358.0,716.0,24408,428,2.42);

INSERT INTO performance_metric_samples(test_result_id,timestamp,elapsed_seconds,rps,active_users,avg_response_time,min_response_time,max_response_time,p95_response_time,p99_response_time,request_count,failure_count,error_rate)VALUES(11,'2026-04-30 11:29:07',7,2744.0,24,158.4,53.7,537.0,358.0,716.0,27895,490,2.33);

INSERT INTO performance_test_results(id,scenario_id,project_id,user_count,spawn_rate,duration,target_url,status,started_at,finished_at,total_requests,total_failures,error_rate,rps,avg_response_time,min_response_time,max_response_time,p50_response_time,p75_response_time,p95_response_time,p99_response_time,created_at,updated_at)VALUES(12,3,3,175,13,260,'https://example.com/api','failed','2026-01-10 21:53:00','2026-01-10 21:57:20',9155,160,1.75,2391.6,193.6,58.1,968.0,135.5,251.7,484.0,774.4,'2026-01-10 21:53:00','2026-01-10 21:57:20')ON CONFLICT(id)DO NOTHING;

INSERT INTO performance_metric_samples(test_result_id,timestamp,elapsed_seconds,rps,active_users,avg_response_time,min_response_time,max_response_time,p95_response_time,p99_response_time,request_count,failure_count,error_rate)VALUES(12,'2026-01-10 21:53:00',0,1685.0,3,215.5,58.1,580.8,387.2,774.4,1144,20,1.52);

INSERT INTO performance_metric_samples(test_result_id,timestamp,elapsed_seconds,rps,active_users,avg_response_time,min_response_time,max_response_time,p95_response_time,p99_response_time,request_count,failure_count,error_rate)VALUES(12,'2026-01-10 21:53:01',1,2058.1,6,175.4,58.1,580.8,387.2,774.4,2288,40,2.52);

INSERT INTO performance_metric_samples(test_result_id,timestamp,elapsed_seconds,rps,active_users,avg_response_time,min_response_time,max_response_time,p95_response_time,p99_response_time,request_count,failure_count,error_rate)VALUES(12,'2026-01-10 21:53:02',2,2815.1,9,207.0,58.1,580.8,387.2,774.4,3433,60,0.01);

INSERT INTO performance_metric_samples(test_result_id,timestamp,elapsed_seconds,rps,active_users,avg_response_time,min_response_time,max_response_time,p95_response_time,p99_response_time,request_count,failure_count,error_rate)VALUES(12,'2026-01-10 21:53:03',3,2978.6,9,156.1,58.1,580.8,387.2,774.4,4577,80,0.46);

INSERT INTO performance_metric_samples(test_result_id,timestamp,elapsed_seconds,rps,active_users,avg_response_time,min_response_time,max_response_time,p95_response_time,p99_response_time,request_count,failure_count,error_rate)VALUES(12,'2026-01-10 21:53:04',4,2211.4,15,218.4,58.1,580.8,387.2,774.4,5721,100,1.8);

INSERT INTO performance_metric_samples(test_result_id,timestamp,elapsed_seconds,rps,active_users,avg_response_time,min_response_time,max_response_time,p95_response_time,p99_response_time,request_count,failure_count,error_rate)VALUES(12,'2026-01-10 21:53:05',5,2155.0,18,231.8,58.1,580.8,387.2,774.4,6866,120,0.73);

INSERT INTO performance_metric_samples(test_result_id,timestamp,elapsed_seconds,rps,active_users,avg_response_time,min_response_time,max_response_time,p95_response_time,p99_response_time,request_count,failure_count,error_rate)VALUES(12,'2026-01-10 21:53:06',6,3071.0,21,202.6,58.1,580.8,387.2,774.4,8010,140,1.18);

INSERT INTO performance_metric_samples(test_result_id,timestamp,elapsed_seconds,rps,active_users,avg_response_time,min_response_time,max_response_time,p95_response_time,p99_response_time,request_count,failure_count,error_rate)VALUES(12,'2026-01-10 21:53:07',7,1748.1,24,188.1,58.1,580.8,387.2,774.4,9155,160,2.82);

INSERT INTO performance_test_results(id,scenario_id,project_id,user_count,spawn_rate,duration,target_url,status,started_at,finished_at,total_requests,total_failures,error_rate,rps,avg_response_time,min_response_time,max_response_time,p50_response_time,p75_response_time,p95_response_time,p99_response_time,created_at,updated_at)VALUES(13,3,3,42,17,472,'https://example.com/api','completed','2026-02-21 10:49:00','2026-02-21 10:56:52',34900,276,0.79,731.4,288.4,86.5,1442.0,201.9,374.9,721.0,1153.6,'2026-02-21 10:49:00','2026-02-21 10:56:52')ON CONFLICT(id)DO NOTHING;

INSERT INTO performance_metric_samples(test_result_id,timestamp,elapsed_seconds,rps,active_users,avg_response_time,min_response_time,max_response_time,p95_response_time,p99_response_time,request_count,failure_count,error_rate)VALUES(13,'2026-02-21 10:49:00',0,563.9,3,321.2,86.5,865.2,576.8,1153.6,4362,34,2.53);

INSERT INTO performance_metric_samples(test_result_id,timestamp,elapsed_seconds,rps,active_users,avg_response_time,min_response_time,max_response_time,p95_response_time,p99_response_time,request_count,failure_count,error_rate)VALUES(13,'2026-02-21 10:49:01',1,787.3,6,327.3,86.5,865.2,576.8,1153.6,8725,69,0.48);

INSERT INTO performance_metric_samples(test_result_id,timestamp,elapsed_seconds,rps,active_users,avg_response_time,min_response_time,max_response_time,p95_response_time,p99_response_time,request_count,failure_count,error_rate)VALUES(13,'2026-02-21 10:49:02',2,653.5,9,241.5,86.5,865.2,576.8,1153.6,13087,103,1.31);

INSERT INTO performance_metric_samples(test_result_id,timestamp,elapsed_seconds,rps,active_users,avg_response_time,min_response_time,max_response_time,p95_response_time,p99_response_time,request_count,failure_count,error_rate)VALUES(13,'2026-02-21 10:49:03',3,788.0,12,248.4,86.5,865.2,576.8,1153.6,17450,138,1.85);

INSERT INTO performance_metric_samples(test_result_id,timestamp,elapsed_seconds,rps,active_users,avg_response_time,min_response_time,max_response_time,p95_response_time,p99_response_time,request_count,failure_count,error_rate)VALUES(13,'2026-02-21 10:49:04',4,750.6,15,296.7,86.5,865.2,576.8,1153.6,21812,172,0.08);

INSERT INTO performance_metric_samples(test_result_id,timestamp,elapsed_seconds,rps,active_users,avg_response_time,min_response_time,max_response_time,p95_response_time,p99_response_time,request_count,failure_count,error_rate)VALUES(13,'2026-02-21 10:49:05',5,834.2,18,303.9,86.5,865.2,576.8,1153.6,26175,207,2.33);

INSERT INTO performance_metric_samples(test_result_id,timestamp,elapsed_seconds,rps,active_users,avg_response_time,min_response_time,max_response_time,p95_response_time,p99_response_time,request_count,failure_count,error_rate)VALUES(13,'2026-02-21 10:49:06',6,593.8,21,334.3,86.5,865.2,576.8,1153.6,30537,241,0.89);

INSERT INTO performance_metric_samples(test_result_id,timestamp,elapsed_seconds,rps,active_users,avg_response_time,min_response_time,max_response_time,p95_response_time,p99_response_time,request_count,failure_count,error_rate)VALUES(13,'2026-02-21 10:49:07',7,746.9,24,314.5,86.5,865.2,576.8,1153.6,34900,276,2.42);

INSERT INTO performance_test_results(id,scenario_id,project_id,user_count,spawn_rate,duration,target_url,status,started_at,finished_at,total_requests,total_failures,error_rate,rps,avg_response_time,min_response_time,max_response_time,p50_response_time,p75_response_time,p95_response_time,p99_response_time,created_at,updated_at)VALUES(14,4,3,36,4,341,'https://example.com/api','completed','2026-03-26 12:57:00','2026-03-26 13:02:41',10422,326,3.13,1933.2,238.1,71.4,1190.5,166.7,309.5,595.2,952.4,'2026-03-26 12:57:00','2026-03-26 13:02:41')ON CONFLICT(id)DO NOTHING;

INSERT INTO performance_metric_samples(test_result_id,timestamp,elapsed_seconds,rps,active_users,avg_response_time,min_response_time,max_response_time,p95_response_time,p99_response_time,request_count,failure_count,error_rate)VALUES(14,'2026-03-26 12:57:00',0,1885.8,3,202.2,71.4,714.3,476.2,952.4,1302,40,0.43);

INSERT INTO performance_metric_samples(test_result_id,timestamp,elapsed_seconds,rps,active_users,avg_response_time,min_response_time,max_response_time,p95_response_time,p99_response_time,request_count,failure_count,error_rate)VALUES(14,'2026-03-26 12:57:01',1,1657.1,6,199.3,71.4,714.3,476.2,952.4,2605,81,1.48);

INSERT INTO performance_metric_samples(test_result_id,timestamp,elapsed_seconds,rps,active_users,avg_response_time,min_response_time,max_response_time,p95_response_time,p99_response_time,request_count,failure_count,error_rate)VALUES(14,'2026-03-26 12:57:02',2,1772.4,9,227.7,71.4,714.3,476.2,952.4,3908,122,1.47);

INSERT INTO performance_metric_samples(test_result_id,timestamp,elapsed_seconds,rps,active_users,avg_response_time,min_response_time,max_response_time,p95_response_time,p99_response_time,request_count,failure_count,error_rate)VALUES(14,'2026-03-26 12:57:03',3,1378.7,12,236.8,71.4,714.3,476.2,952.4,5211,163,1.88);

INSERT INTO performance_metric_samples(test_result_id,timestamp,elapsed_seconds,rps,active_users,avg_response_time,min_response_time,max_response_time,p95_response_time,p99_response_time,request_count,failure_count,error_rate)VALUES(14,'2026-03-26 12:57:04',4,1597.2,15,226.2,71.4,714.3,476.2,952.4,6513,203,0.94);

INSERT INTO performance_metric_samples(test_result_id,timestamp,elapsed_seconds,rps,active_users,avg_response_time,min_response_time,max_response_time,p95_response_time,p99_response_time,request_count,failure_count,error_rate)VALUES(14,'2026-03-26 12:57:05',5,2406.8,18,207.6,71.4,714.3,476.2,952.4,7816,244,0.03);

INSERT INTO performance_metric_samples(test_result_id,timestamp,elapsed_seconds,rps,active_users,avg_response_time,min_response_time,max_response_time,p95_response_time,p99_response_time,request_count,failure_count,error_rate)VALUES(14,'2026-03-26 12:57:06',6,1560.5,21,250.6,71.4,714.3,476.2,952.4,9119,285,2.56);

INSERT INTO performance_metric_samples(test_result_id,timestamp,elapsed_seconds,rps,active_users,avg_response_time,min_response_time,max_response_time,p95_response_time,p99_response_time,request_count,failure_count,error_rate)VALUES(14,'2026-03-26 12:57:07',7,1489.2,24,285.1,71.4,714.3,476.2,952.4,10422,326,1.45);

INSERT INTO performance_test_results(id,scenario_id,project_id,user_count,spawn_rate,duration,target_url,status,started_at,finished_at,total_requests,total_failures,error_rate,rps,avg_response_time,min_response_time,max_response_time,p50_response_time,p75_response_time,p95_response_time,p99_response_time,created_at,updated_at)VALUES(15,4,3,141,5,594,'https://example.com/api','completed','2026-01-13 09:50:00','2026-01-13 09:59:54',8968,86,0.96,137.2,23.9,7.2,119.5,16.7,31.1,59.8,95.6,'2026-01-13 09:50:00','2026-01-13 09:59:54')ON CONFLICT(id)DO NOTHING;

INSERT INTO performance_metric_samples(test_result_id,timestamp,elapsed_seconds,rps,active_users,avg_response_time,min_response_time,max_response_time,p95_response_time,p99_response_time,request_count,failure_count,error_rate)VALUES(15,'2026-01-13 09:50:00',0,113.8,3,20.2,7.2,71.7,47.8,95.6,1121,10,0.65);

INSERT INTO performance_metric_samples(test_result_id,timestamp,elapsed_seconds,rps,active_users,avg_response_time,min_response_time,max_response_time,p95_response_time,p99_response_time,request_count,failure_count,error_rate)VALUES(15,'2026-01-13 09:50:01',1,123.0,6,19.9,7.2,71.7,47.8,95.6,2242,21,2.07);

INSERT INTO performance_metric_samples(test_result_id,timestamp,elapsed_seconds,rps,active_users,avg_response_time,min_response_time,max_response_time,p95_response_time,p99_response_time,request_count,failure_count,error_rate)VALUES(15,'2026-01-13 09:50:02',2,106.5,9,23.7,7.2,71.7,47.8,95.6,3363,32,2.86);

INSERT INTO performance_metric_samples(test_result_id,timestamp,elapsed_seconds,rps,active_users,avg_response_time,min_response_time,max_response_time,p95_response_time,p99_response_time,request_count,failure_count,error_rate)VALUES(15,'2026-01-13 09:50:03',3,124.7,12,25.4,7.2,71.7,47.8,95.6,4484,43,1.4);

INSERT INTO performance_metric_samples(test_result_id,timestamp,elapsed_seconds,rps,active_users,avg_response_time,min_response_time,max_response_time,p95_response_time,p99_response_time,request_count,failure_count,error_rate)VALUES(15,'2026-01-13 09:50:04',4,162.6,15,24.0,7.2,71.7,47.8,95.6,5605,53,1.2);

INSERT INTO performance_metric_samples(test_result_id,timestamp,elapsed_seconds,rps,active_users,avg_response_time,min_response_time,max_response_time,p95_response_time,p99_response_time,request_count,failure_count,error_rate)VALUES(15,'2026-01-13 09:50:05',5,111.9,18,21.0,7.2,71.7,47.8,95.6,6726,64,2.54);

INSERT INTO performance_metric_samples(test_result_id,timestamp,elapsed_seconds,rps,active_users,avg_response_time,min_response_time,max_response_time,p95_response_time,p99_response_time,request_count,failure_count,error_rate)VALUES(15,'2026-01-13 09:50:06',6,155.1,21,20.1,7.2,71.7,47.8,95.6,7847,75,2.38);

INSERT INTO performance_metric_samples(test_result_id,timestamp,elapsed_seconds,rps,active_users,avg_response_time,min_response_time,max_response_time,p95_response_time,p99_response_time,request_count,failure_count,error_rate)VALUES(15,'2026-01-13 09:50:07',7,144.4,24,26.7,7.2,71.7,47.8,95.6,8968,86,2.86);

INSERT INTO performance_test_results(id,scenario_id,project_id,user_count,spawn_rate,duration,target_url,status,started_at,finished_at,total_requests,total_failures,error_rate,rps,avg_response_time,min_response_time,max_response_time,p50_response_time,p75_response_time,p95_response_time,p99_response_time,created_at,updated_at)VALUES(16,4,3,165,13,516,'https://example.com/api','failed','2026-01-27 20:04:00','2026-01-27 20:12:36',40081,1497,3.73,2456.9,254.8,76.4,1274.0,178.4,331.2,637.0,1019.2,'2026-01-27 20:04:00','2026-01-27 20:12:36')ON CONFLICT(id)DO NOTHING;

INSERT INTO performance_metric_samples(test_result_id,timestamp,elapsed_seconds,rps,active_users,avg_response_time,min_response_time,max_response_time,p95_response_time,p99_response_time,request_count,failure_count,error_rate)VALUES(16,'2026-01-27 20:04:00',0,2352.7,3,239.8,76.4,764.4,509.6,1019.2,5010,187,2.69);

INSERT INTO performance_metric_samples(test_result_id,timestamp,elapsed_seconds,rps,active_users,avg_response_time,min_response_time,max_response_time,p95_response_time,p99_response_time,request_count,failure_count,error_rate)VALUES(16,'2026-01-27 20:04:01',1,2927.7,6,220.9,76.4,764.4,509.6,1019.2,10020,374,0.1);

INSERT INTO performance_metric_samples(test_result_id,timestamp,elapsed_seconds,rps,active_users,avg_response_time,min_response_time,max_response_time,p95_response_time,p99_response_time,request_count,failure_count,error_rate)VALUES(16,'2026-01-27 20:04:02',2,2473.6,9,245.6,76.4,764.4,509.6,1019.2,15030,561,1.81);

INSERT INTO performance_metric_samples(test_result_id,timestamp,elapsed_seconds,rps,active_users,avg_response_time,min_response_time,max_response_time,p95_response_time,p99_response_time,request_count,failure_count,error_rate)VALUES(16,'2026-01-27 20:04:03',3,3013.0,12,239.7,76.4,764.4,509.6,1019.2,20040,748,0.09);

INSERT INTO performance_metric_samples(test_result_id,timestamp,elapsed_seconds,rps,active_users,avg_response_time,min_response_time,max_response_time,p95_response_time,p99_response_time,request_count,failure_count,error_rate)VALUES(16,'2026-01-27 20:04:04',4,1985.0,15,247.6,76.4,764.4,509.6,1019.2,25050,935,0.56);

INSERT INTO performance_metric_samples(test_result_id,timestamp,elapsed_seconds,rps,active_users,avg_response_time,min_response_time,max_response_time,p95_response_time,p99_response_time,request_count,failure_count,error_rate)VALUES(16,'2026-01-27 20:04:05',5,2081.5,18,270.8,76.4,764.4,509.6,1019.2,30060,1122,1.12);

INSERT INTO performance_metric_samples(test_result_id,timestamp,elapsed_seconds,rps,active_users,avg_response_time,min_response_time,max_response_time,p95_response_time,p99_response_time,request_count,failure_count,error_rate)VALUES(16,'2026-01-27 20:04:06',6,2868.9,21,204.8,76.4,764.4,509.6,1019.2,35070,1309,2.06);

INSERT INTO performance_metric_samples(test_result_id,timestamp,elapsed_seconds,rps,active_users,avg_response_time,min_response_time,max_response_time,p95_response_time,p99_response_time,request_count,failure_count,error_rate)VALUES(16,'2026-01-27 20:04:07',7,2776.5,24,251.3,76.4,764.4,509.6,1019.2,40081,1497,2.39);

INSERT INTO performance_test_results(id,scenario_id,project_id,user_count,spawn_rate,duration,target_url,status,started_at,finished_at,total_requests,total_failures,error_rate,rps,avg_response_time,min_response_time,max_response_time,p50_response_time,p75_response_time,p95_response_time,p99_response_time,created_at,updated_at)VALUES(17,4,3,193,20,454,'https://example.com/api','completed','2026-04-02 16:56:00','2026-04-02 17:03:34',40439,429,1.06,691.5,231.0,69.3,1155.0,161.7,300.3,577.5,924.0,'2026-04-02 16:56:00','2026-04-02 17:03:34')ON CONFLICT(id)DO NOTHING;

INSERT INTO performance_metric_samples(test_result_id,timestamp,elapsed_seconds,rps,active_users,avg_response_time,min_response_time,max_response_time,p95_response_time,p99_response_time,request_count,failure_count,error_rate)VALUES(17,'2026-04-02 16:56:00',0,876.7,3,191.7,69.3,693.0,462.0,924.0,5054,53,2.68);

INSERT INTO performance_metric_samples(test_result_id,timestamp,elapsed_seconds,rps,active_users,avg_response_time,min_response_time,max_response_time,p95_response_time,p99_response_time,request_count,failure_count,error_rate)VALUES(17,'2026-04-02 16:56:01',1,659.0,6,225.0,69.3,693.0,462.0,924.0,10109,107,2.44);

INSERT INTO performance_metric_samples(test_result_id,timestamp,elapsed_seconds,rps,active_users,avg_response_time,min_response_time,max_response_time,p95_response_time,p99_response_time,request_count,failure_count,error_rate)VALUES(17,'2026-04-02 16:56:02',2,566.3,9,259.0,69.3,693.0,462.0,924.0,15164,160,1.5);

INSERT INTO performance_metric_samples(test_result_id,timestamp,elapsed_seconds,rps,active_users,avg_response_time,min_response_time,max_response_time,p95_response_time,p99_response_time,request_count,failure_count,error_rate)VALUES(17,'2026-04-02 16:56:03',3,894.9,12,195.8,69.3,693.0,462.0,924.0,20219,214,1.36);

INSERT INTO performance_metric_samples(test_result_id,timestamp,elapsed_seconds,rps,active_users,avg_response_time,min_response_time,max_response_time,p95_response_time,p99_response_time,request_count,failure_count,error_rate)VALUES(17,'2026-04-02 16:56:04',4,733.6,15,220.2,69.3,693.0,462.0,924.0,25274,268,1.73);

INSERT INTO performance_metric_samples(test_result_id,timestamp,elapsed_seconds,rps,active_users,avg_response_time,min_response_time,max_response_time,p95_response_time,p99_response_time,request_count,failure_count,error_rate)VALUES(17,'2026-04-02 16:56:05',5,602.3,18,257.2,69.3,693.0,462.0,924.0,30329,321,1.73);

INSERT INTO performance_metric_samples(test_result_id,timestamp,elapsed_seconds,rps,active_users,avg_response_time,min_response_time,max_response_time,p95_response_time,p99_response_time,request_count,failure_count,error_rate)VALUES(17,'2026-04-02 16:56:06',6,486.0,21,211.1,69.3,693.0,462.0,924.0,35384,375,2.52);

INSERT INTO performance_metric_samples(test_result_id,timestamp,elapsed_seconds,rps,active_users,avg_response_time,min_response_time,max_response_time,p95_response_time,p99_response_time,request_count,failure_count,error_rate)VALUES(17,'2026-04-02 16:56:07',7,651.2,24,269.6,69.3,693.0,462.0,924.0,40439,429,0.12);

INSERT INTO performance_test_results(id,scenario_id,project_id,user_count,spawn_rate,duration,target_url,status,started_at,finished_at,total_requests,total_failures,error_rate,rps,avg_response_time,min_response_time,max_response_time,p50_response_time,p75_response_time,p95_response_time,p99_response_time,created_at,updated_at)VALUES(18,4,3,30,18,157,'https://example.com/api','failed','2026-05-28 07:30:00','2026-05-28 07:32:37',48399,728,1.5,985.7,148.1,44.4,740.5,103.7,192.5,370.2,592.4,'2026-05-28 07:30:00','2026-05-28 07:32:37')ON CONFLICT(id)DO NOTHING;

INSERT INTO performance_metric_samples(test_result_id,timestamp,elapsed_seconds,rps,active_users,avg_response_time,min_response_time,max_response_time,p95_response_time,p99_response_time,request_count,failure_count,error_rate)VALUES(18,'2026-05-28 07:30:00',0,1148.1,3,154.8,44.4,444.3,296.2,592.4,6049,91,1.18);

INSERT INTO performance_metric_samples(test_result_id,timestamp,elapsed_seconds,rps,active_users,avg_response_time,min_response_time,max_response_time,p95_response_time,p99_response_time,request_count,failure_count,error_rate)VALUES(18,'2026-05-28 07:30:01',1,1101.9,6,147.7,44.4,444.3,296.2,592.4,12099,182,1.92);

INSERT INTO performance_metric_samples(test_result_id,timestamp,elapsed_seconds,rps,active_users,avg_response_time,min_response_time,max_response_time,p95_response_time,p99_response_time,request_count,failure_count,error_rate)VALUES(18,'2026-05-28 07:30:02',2,1228.5,9,174.0,44.4,444.3,296.2,592.4,18149,273,0.31);

INSERT INTO performance_metric_samples(test_result_id,timestamp,elapsed_seconds,rps,active_users,avg_response_time,min_response_time,max_response_time,p95_response_time,p99_response_time,request_count,failure_count,error_rate)VALUES(18,'2026-05-28 07:30:03',3,822.5,3,126.7,44.4,444.3,296.2,592.4,24199,364,2.98);

INSERT INTO performance_metric_samples(test_result_id,timestamp,elapsed_seconds,rps,active_users,avg_response_time,min_response_time,max_response_time,p95_response_time,p99_response_time,request_count,failure_count,error_rate)VALUES(18,'2026-05-28 07:30:04',4,1199.4,15,144.3,44.4,444.3,296.2,592.4,30249,455,0.51);

INSERT INTO performance_metric_samples(test_result_id,timestamp,elapsed_seconds,rps,active_users,avg_response_time,min_response_time,max_response_time,p95_response_time,p99_response_time,request_count,failure_count,error_rate)VALUES(18,'2026-05-28 07:30:05',5,803.0,18,166.8,44.4,444.3,296.2,592.4,36299,546,1.61);

INSERT INTO performance_metric_samples(test_result_id,timestamp,elapsed_seconds,rps,active_users,avg_response_time,min_response_time,max_response_time,p95_response_time,p99_response_time,request_count,failure_count,error_rate)VALUES(18,'2026-05-28 07:30:06',6,692.9,21,169.9,44.4,444.3,296.2,592.4,42349,637,0.78);

INSERT INTO performance_metric_samples(test_result_id,timestamp,elapsed_seconds,rps,active_users,avg_response_time,min_response_time,max_response_time,p95_response_time,p99_response_time,request_count,failure_count,error_rate)VALUES(18,'2026-05-28 07:30:07',7,1154.2,24,121.3,44.4,444.3,296.2,592.4,48399,728,0.91);

INSERT INTO performance_test_results(id,scenario_id,project_id,user_count,spawn_rate,duration,target_url,status,started_at,finished_at,total_requests,total_failures,error_rate,rps,avg_response_time,min_response_time,max_response_time,p50_response_time,p75_response_time,p95_response_time,p99_response_time,created_at,updated_at)VALUES(19,4,3,42,11,448,'https://example.com/api','completed','2026-03-25 23:16:00','2026-03-25 23:23:28',46787,398,0.85,456.4,192.4,57.7,962.0,134.7,250.1,481.0,769.6,'2026-03-25 23:16:00','2026-03-25 23:23:28')ON CONFLICT(id)DO NOTHING;

INSERT INTO performance_metric_samples(test_result_id,timestamp,elapsed_seconds,rps,active_users,avg_response_time,min_response_time,max_response_time,p95_response_time,p99_response_time,request_count,failure_count,error_rate)VALUES(19,'2026-03-25 23:16:00',0,555.5,3,198.9,57.7,577.2,384.8,769.6,5848,49,2.55);

INSERT INTO performance_metric_samples(test_result_id,timestamp,elapsed_seconds,rps,active_users,avg_response_time,min_response_time,max_response_time,p95_response_time,p99_response_time,request_count,failure_count,error_rate)VALUES(19,'2026-03-25 23:16:01',1,564.7,6,188.3,57.7,577.2,384.8,769.6,11696,99,0.37);

INSERT INTO performance_metric_samples(test_result_id,timestamp,elapsed_seconds,rps,active_users,avg_response_time,min_response_time,max_response_time,p95_response_time,p99_response_time,request_count,failure_count,error_rate)VALUES(19,'2026-03-25 23:16:02',2,464.0,9,190.7,57.7,577.2,384.8,769.6,17545,149,1.47);

INSERT INTO performance_metric_samples(test_result_id,timestamp,elapsed_seconds,rps,active_users,avg_response_time,min_response_time,max_response_time,p95_response_time,p99_response_time,request_count,failure_count,error_rate)VALUES(19,'2026-03-25 23:16:03',3,396.3,12,210.2,57.7,577.2,384.8,769.6,23393,199,0.68);

INSERT INTO performance_metric_samples(test_result_id,timestamp,elapsed_seconds,rps,active_users,avg_response_time,min_response_time,max_response_time,p95_response_time,p99_response_time,request_count,failure_count,error_rate)VALUES(19,'2026-03-25 23:16:04',4,391.7,15,208.7,57.7,577.2,384.8,769.6,29241,248,1.06);

INSERT INTO performance_metric_samples(test_result_id,timestamp,elapsed_seconds,rps,active_users,avg_response_time,min_response_time,max_response_time,p95_response_time,p99_response_time,request_count,failure_count,error_rate)VALUES(19,'2026-03-25 23:16:05',5,548.3,18,204.7,57.7,577.2,384.8,769.6,35090,298,2.21);

INSERT INTO performance_metric_samples(test_result_id,timestamp,elapsed_seconds,rps,active_users,avg_response_time,min_response_time,max_response_time,p95_response_time,p99_response_time,request_count,failure_count,error_rate)VALUES(19,'2026-03-25 23:16:06',6,375.9,20,159.7,57.7,577.2,384.8,769.6,40938,348,1.48);

INSERT INTO performance_metric_samples(test_result_id,timestamp,elapsed_seconds,rps,active_users,avg_response_time,min_response_time,max_response_time,p95_response_time,p99_response_time,request_count,failure_count,error_rate)VALUES(19,'2026-03-25 23:16:07',7,377.7,24,170.6,57.7,577.2,384.8,769.6,46787,398,2.46);

INSERT INTO performance_test_results(id,scenario_id,project_id,user_count,spawn_rate,duration,target_url,status,started_at,finished_at,total_requests,total_failures,error_rate,rps,avg_response_time,min_response_time,max_response_time,p50_response_time,p75_response_time,p95_response_time,p99_response_time,created_at,updated_at)VALUES(20,5,6,37,5,273,'https://example.com/api','completed','2026-01-28 06:39:00','2026-01-28 06:43:33',21435,759,3.54,1983.1,341.4,102.4,1707.0,239.0,443.8,853.5,1365.6,'2026-01-28 06:39:00','2026-01-28 06:43:33')ON CONFLICT(id)DO NOTHING;

INSERT INTO performance_metric_samples(test_result_id,timestamp,elapsed_seconds,rps,active_users,avg_response_time,min_response_time,max_response_time,p95_response_time,p99_response_time,request_count,failure_count,error_rate)VALUES(20,'2026-01-28 06:39:00',0,1648.5,3,325.8,102.4,1024.2,682.8,1365.6,2679,94,1.36);

INSERT INTO performance_metric_samples(test_result_id,timestamp,elapsed_seconds,rps,active_users,avg_response_time,min_response_time,max_response_time,p95_response_time,p99_response_time,request_count,failure_count,error_rate)VALUES(20,'2026-01-28 06:39:01',1,2126.5,6,379.6,102.4,1024.2,682.8,1365.6,5358,189,0.56);

INSERT INTO performance_metric_samples(test_result_id,timestamp,elapsed_seconds,rps,active_users,avg_response_time,min_response_time,max_response_time,p95_response_time,p99_response_time,request_count,failure_count,error_rate)VALUES(20,'2026-01-28 06:39:02',2,1718.8,9,366.8,102.4,1024.2,682.8,1365.6,8038,284,2.85);

INSERT INTO performance_metric_samples(test_result_id,timestamp,elapsed_seconds,rps,active_users,avg_response_time,min_response_time,max_response_time,p95_response_time,p99_response_time,request_count,failure_count,error_rate)VALUES(20,'2026-01-28 06:39:03',3,2075.0,12,293.2,102.4,1024.2,682.8,1365.6,10717,379,2.63);

INSERT INTO performance_metric_samples(test_result_id,timestamp,elapsed_seconds,rps,active_users,avg_response_time,min_response_time,max_response_time,p95_response_time,p99_response_time,request_count,failure_count,error_rate)VALUES(20,'2026-01-28 06:39:04',4,2274.6,15,275.4,102.4,1024.2,682.8,1365.6,13396,474,1.38);

INSERT INTO performance_metric_samples(test_result_id,timestamp,elapsed_seconds,rps,active_users,avg_response_time,min_response_time,max_response_time,p95_response_time,p99_response_time,request_count,failure_count,error_rate)VALUES(20,'2026-01-28 06:39:05',5,1705.6,18,363.5,102.4,1024.2,682.8,1365.6,16076,569,1.36);

INSERT INTO performance_metric_samples(test_result_id,timestamp,elapsed_seconds,rps,active_users,avg_response_time,min_response_time,max_response_time,p95_response_time,p99_response_time,request_count,failure_count,error_rate)VALUES(20,'2026-01-28 06:39:06',6,1704.2,21,284.6,102.4,1024.2,682.8,1365.6,18755,664,1.29);

INSERT INTO performance_metric_samples(test_result_id,timestamp,elapsed_seconds,rps,active_users,avg_response_time,min_response_time,max_response_time,p95_response_time,p99_response_time,request_count,failure_count,error_rate)VALUES(20,'2026-01-28 06:39:07',7,1567.4,24,332.0,102.4,1024.2,682.8,1365.6,21435,759,1.0);

INSERT INTO performance_test_results(id,scenario_id,project_id,user_count,spawn_rate,duration,target_url,status,started_at,finished_at,total_requests,total_failures,error_rate,rps,avg_response_time,min_response_time,max_response_time,p50_response_time,p75_response_time,p95_response_time,p99_response_time,created_at,updated_at)VALUES(21,5,6,58,13,160,'https://example.com/api','completed','2026-02-09 01:37:00','2026-02-09 01:39:40',43508,832,1.91,2787.7,89.7,26.9,448.5,62.8,116.6,224.2,358.8,'2026-02-09 01:37:00','2026-02-09 01:39:40')ON CONFLICT(id)DO NOTHING;

INSERT INTO performance_metric_samples(test_result_id,timestamp,elapsed_seconds,rps,active_users,avg_response_time,min_response_time,max_response_time,p95_response_time,p99_response_time,request_count,failure_count,error_rate)VALUES(21,'2026-02-09 01:37:00',0,2246.9,3,90.8,26.9,269.1,179.4,358.8,5438,104,1.48);

INSERT INTO performance_metric_samples(test_result_id,timestamp,elapsed_seconds,rps,active_users,avg_response_time,min_response_time,max_response_time,p95_response_time,p99_response_time,request_count,failure_count,error_rate)VALUES(21,'2026-02-09 01:37:01',1,2676.6,6,73.5,26.9,269.1,179.4,358.8,10877,208,0.75);

INSERT INTO performance_metric_samples(test_result_id,timestamp,elapsed_seconds,rps,active_users,avg_response_time,min_response_time,max_response_time,p95_response_time,p99_response_time,request_count,failure_count,error_rate)VALUES(21,'2026-02-09 01:37:02',2,2137.2,9,73.7,26.9,269.1,179.4,358.8,16315,312,0.11);

INSERT INTO performance_metric_samples(test_result_id,timestamp,elapsed_seconds,rps,active_users,avg_response_time,min_response_time,max_response_time,p95_response_time,p99_response_time,request_count,failure_count,error_rate)VALUES(21,'2026-02-09 01:37:03',3,2396.6,12,90.9,26.9,269.1,179.4,358.8,21754,416,0.83);

INSERT INTO performance_metric_samples(test_result_id,timestamp,elapsed_seconds,rps,active_users,avg_response_time,min_response_time,max_response_time,p95_response_time,p99_response_time,request_count,failure_count,error_rate)VALUES(21,'2026-02-09 01:37:04',4,3427.6,15,97.4,26.9,269.1,179.4,358.8,27192,520,1.18);

INSERT INTO performance_metric_samples(test_result_id,timestamp,elapsed_seconds,rps,active_users,avg_response_time,min_response_time,max_response_time,p95_response_time,p99_response_time,request_count,failure_count,error_rate)VALUES(21,'2026-02-09 01:37:05',5,2120.8,18,101.3,26.9,269.1,179.4,358.8,32631,624,2.08);

INSERT INTO performance_metric_samples(test_result_id,timestamp,elapsed_seconds,rps,active_users,avg_response_time,min_response_time,max_response_time,p95_response_time,p99_response_time,request_count,failure_count,error_rate)VALUES(21,'2026-02-09 01:37:06',6,2779.6,21,100.0,26.9,269.1,179.4,358.8,38069,728,1.04);

INSERT INTO performance_metric_samples(test_result_id,timestamp,elapsed_seconds,rps,active_users,avg_response_time,min_response_time,max_response_time,p95_response_time,p99_response_time,request_count,failure_count,error_rate)VALUES(21,'2026-02-09 01:37:07',7,2433.1,24,82.1,26.9,269.1,179.4,358.8,43508,832,0.01);

INSERT INTO performance_test_results(id,scenario_id,project_id,user_count,spawn_rate,duration,target_url,status,started_at,finished_at,total_requests,total_failures,error_rate,rps,avg_response_time,min_response_time,max_response_time,p50_response_time,p75_response_time,p95_response_time,p99_response_time,created_at,updated_at)VALUES(22,5,6,57,11,548,'https://example.com/api','completed','2026-04-14 17:02:00','2026-04-14 17:11:08',46084,549,1.19,979.6,41.7,12.5,208.5,29.2,54.2,104.2,166.8,'2026-04-14 17:02:00','2026-04-14 17:11:08')ON CONFLICT(id)DO NOTHING;

INSERT INTO performance_metric_samples(test_result_id,timestamp,elapsed_seconds,rps,active_users,avg_response_time,min_response_time,max_response_time,p95_response_time,p99_response_time,request_count,failure_count,error_rate)VALUES(22,'2026-04-14 17:02:00',0,1214.6,3,49.4,12.5,125.1,83.4,166.8,5760,68,2.0);

INSERT INTO performance_metric_samples(test_result_id,timestamp,elapsed_seconds,rps,active_users,avg_response_time,min_response_time,max_response_time,p95_response_time,p99_response_time,request_count,failure_count,error_rate)VALUES(22,'2026-04-14 17:02:01',1,937.2,6,36.3,12.5,125.1,83.4,166.8,11521,137,0.79);

INSERT INTO performance_metric_samples(test_result_id,timestamp,elapsed_seconds,rps,active_users,avg_response_time,min_response_time,max_response_time,p95_response_time,p99_response_time,request_count,failure_count,error_rate)VALUES(22,'2026-04-14 17:02:02',2,731.0,9,46.0,12.5,125.1,83.4,166.8,17281,205,0.03);

INSERT INTO performance_metric_samples(test_result_id,timestamp,elapsed_seconds,rps,active_users,avg_response_time,min_response_time,max_response_time,p95_response_time,p99_response_time,request_count,failure_count,error_rate)VALUES(22,'2026-04-14 17:02:03',3,892.7,12,43.1,12.5,125.1,83.4,166.8,23042,274,1.46);

INSERT INTO performance_metric_samples(test_result_id,timestamp,elapsed_seconds,rps,active_users,avg_response_time,min_response_time,max_response_time,p95_response_time,p99_response_time,request_count,failure_count,error_rate)VALUES(22,'2026-04-14 17:02:04',4,831.2,15,34.1,12.5,125.1,83.4,166.8,28802,343,0.05);

INSERT INTO performance_metric_samples(test_result_id,timestamp,elapsed_seconds,rps,active_users,avg_response_time,min_response_time,max_response_time,p95_response_time,p99_response_time,request_count,failure_count,error_rate)VALUES(22,'2026-04-14 17:02:05',5,1085.4,18,47.3,12.5,125.1,83.4,166.8,34563,411,1.58);

INSERT INTO performance_metric_samples(test_result_id,timestamp,elapsed_seconds,rps,active_users,avg_response_time,min_response_time,max_response_time,p95_response_time,p99_response_time,request_count,failure_count,error_rate)VALUES(22,'2026-04-14 17:02:06',6,784.1,21,46.3,12.5,125.1,83.4,166.8,40323,480,0.3);

INSERT INTO performance_metric_samples(test_result_id,timestamp,elapsed_seconds,rps,active_users,avg_response_time,min_response_time,max_response_time,p95_response_time,p99_response_time,request_count,failure_count,error_rate)VALUES(22,'2026-04-14 17:02:07',7,1158.2,24,40.9,12.5,125.1,83.4,166.8,46084,549,2.2);

INSERT INTO performance_test_results(id,scenario_id,project_id,user_count,spawn_rate,duration,target_url,status,started_at,finished_at,total_requests,total_failures,error_rate,rps,avg_response_time,min_response_time,max_response_time,p50_response_time,p75_response_time,p95_response_time,p99_response_time,created_at,updated_at)VALUES(23,5,6,95,17,558,'https://example.com/api','completed','2026-01-13 01:18:00','2026-01-13 01:27:18',24874,570,2.29,2491.9,130.9,39.3,654.5,91.6,170.2,327.2,523.6,'2026-01-13 01:18:00','2026-01-13 01:27:18')ON CONFLICT(id)DO NOTHING;

INSERT INTO performance_metric_samples(test_result_id,timestamp,elapsed_seconds,rps,active_users,avg_response_time,min_response_time,max_response_time,p95_response_time,p99_response_time,request_count,failure_count,error_rate)VALUES(23,'2026-01-13 01:18:00',0,2902.4,3,130.1,39.3,392.7,261.8,523.6,3109,71,0.81);

INSERT INTO performance_metric_samples(test_result_id,timestamp,elapsed_seconds,rps,active_users,avg_response_time,min_response_time,max_response_time,p95_response_time,p99_response_time,request_count,failure_count,error_rate)VALUES(23,'2026-01-13 01:18:01',1,2520.8,6,105.8,39.3,392.7,261.8,523.6,6218,142,2.94);

INSERT INTO performance_metric_samples(test_result_id,timestamp,elapsed_seconds,rps,active_users,avg_response_time,min_response_time,max_response_time,p95_response_time,p99_response_time,request_count,failure_count,error_rate)VALUES(23,'2026-01-13 01:18:02',2,3024.6,9,156.8,39.3,392.7,261.8,523.6,9327,213,1.07);

INSERT INTO performance_metric_samples(test_result_id,timestamp,elapsed_seconds,rps,active_users,avg_response_time,min_response_time,max_response_time,p95_response_time,p99_response_time,request_count,failure_count,error_rate)VALUES(23,'2026-01-13 01:18:03',3,1790.5,12,143.5,39.3,392.7,261.8,523.6,12437,285,2.92);

INSERT INTO performance_metric_samples(test_result_id,timestamp,elapsed_seconds,rps,active_users,avg_response_time,min_response_time,max_response_time,p95_response_time,p99_response_time,request_count,failure_count,error_rate)VALUES(23,'2026-01-13 01:18:04',4,2281.7,15,109.4,39.3,392.7,261.8,523.6,15546,356,2.76);

INSERT INTO performance_metric_samples(test_result_id,timestamp,elapsed_seconds,rps,active_users,avg_response_time,min_response_time,max_response_time,p95_response_time,p99_response_time,request_count,failure_count,error_rate)VALUES(23,'2026-01-13 01:18:05',5,2309.2,18,155.3,39.3,392.7,261.8,523.6,18655,427,2.63);

INSERT INTO performance_metric_samples(test_result_id,timestamp,elapsed_seconds,rps,active_users,avg_response_time,min_response_time,max_response_time,p95_response_time,p99_response_time,request_count,failure_count,error_rate)VALUES(23,'2026-01-13 01:18:06',6,2759.2,21,156.4,39.3,392.7,261.8,523.6,21764,498,2.63);

INSERT INTO performance_metric_samples(test_result_id,timestamp,elapsed_seconds,rps,active_users,avg_response_time,min_response_time,max_response_time,p95_response_time,p99_response_time,request_count,failure_count,error_rate)VALUES(23,'2026-01-13 01:18:07',7,2005.9,24,123.0,39.3,392.7,261.8,523.6,24874,570,0.99);

INSERT INTO performance_test_results(id,scenario_id,project_id,user_count,spawn_rate,duration,target_url,status,started_at,finished_at,total_requests,total_failures,error_rate,rps,avg_response_time,min_response_time,max_response_time,p50_response_time,p75_response_time,p95_response_time,p99_response_time,created_at,updated_at)VALUES(24,6,6,98,10,102,'https://example.com/api','completed','2026-03-23 00:48:00','2026-03-23 00:49:42',41132,252,0.61,2396.2,233.2,70.0,1166.0,163.2,303.2,583.0,932.8,'2026-03-23 00:48:00','2026-03-23 00:49:42')ON CONFLICT(id)DO NOTHING;

INSERT INTO performance_metric_samples(test_result_id,timestamp,elapsed_seconds,rps,active_users,avg_response_time,min_response_time,max_response_time,p95_response_time,p99_response_time,request_count,failure_count,error_rate)VALUES(24,'2026-03-23 00:48:00',0,1835.8,3,233.1,70.0,699.6,466.4,932.8,5141,31,2.06);

INSERT INTO performance_metric_samples(test_result_id,timestamp,elapsed_seconds,rps,active_users,avg_response_time,min_response_time,max_response_time,p95_response_time,p99_response_time,request_count,failure_count,error_rate)VALUES(24,'2026-03-23 00:48:01',1,2347.8,6,235.4,70.0,699.6,466.4,932.8,10283,63,0.87);

INSERT INTO performance_metric_samples(test_result_id,timestamp,elapsed_seconds,rps,active_users,avg_response_time,min_response_time,max_response_time,p95_response_time,p99_response_time,request_count,failure_count,error_rate)VALUES(24,'2026-03-23 00:48:02',2,2479.8,9,214.9,70.0,699.6,466.4,932.8,15424,94,0.86);

INSERT INTO performance_metric_samples(test_result_id,timestamp,elapsed_seconds,rps,active_users,avg_response_time,min_response_time,max_response_time,p95_response_time,p99_response_time,request_count,failure_count,error_rate)VALUES(24,'2026-03-23 00:48:03',3,2827.2,4,228.9,70.0,699.6,466.4,932.8,20566,126,0.65);

INSERT INTO performance_metric_samples(test_result_id,timestamp,elapsed_seconds,rps,active_users,avg_response_time,min_response_time,max_response_time,p95_response_time,p99_response_time,request_count,failure_count,error_rate)VALUES(24,'2026-03-23 00:48:04',4,2864.1,15,191.5,70.0,699.6,466.4,932.8,25707,157,0.92);

INSERT INTO performance_metric_samples(test_result_id,timestamp,elapsed_seconds,rps,active_users,avg_response_time,min_response_time,max_response_time,p95_response_time,p99_response_time,request_count,failure_count,error_rate)VALUES(24,'2026-03-23 00:48:05',5,2296.0,18,264.4,70.0,699.6,466.4,932.8,30849,189,0.15);

INSERT INTO performance_metric_samples(test_result_id,timestamp,elapsed_seconds,rps,active_users,avg_response_time,min_response_time,max_response_time,p95_response_time,p99_response_time,request_count,failure_count,error_rate)VALUES(24,'2026-03-23 00:48:06',6,1875.3,21,259.8,70.0,699.6,466.4,932.8,35990,220,1.51);

INSERT INTO performance_metric_samples(test_result_id,timestamp,elapsed_seconds,rps,active_users,avg_response_time,min_response_time,max_response_time,p95_response_time,p99_response_time,request_count,failure_count,error_rate)VALUES(24,'2026-03-23 00:48:07',7,3055.4,24,201.0,70.0,699.6,466.4,932.8,41132,252,0.26);

INSERT INTO performance_test_results(id,scenario_id,project_id,user_count,spawn_rate,duration,target_url,status,started_at,finished_at,total_requests,total_failures,error_rate,rps,avg_response_time,min_response_time,max_response_time,p50_response_time,p75_response_time,p95_response_time,p99_response_time,created_at,updated_at)VALUES(25,6,6,100,8,261,'https://example.com/api','failed','2026-03-24 05:14:00','2026-03-24 05:18:21',39353,1806,4.59,907.9,27.4,8.2,137.0,19.2,35.6,68.5,109.6,'2026-03-24 05:14:00','2026-03-24 05:18:21')ON CONFLICT(id)DO NOTHING;

INSERT INTO performance_metric_samples(test_result_id,timestamp,elapsed_seconds,rps,active_users,avg_response_time,min_response_time,max_response_time,p95_response_time,p99_response_time,request_count,failure_count,error_rate)VALUES(25,'2026-03-24 05:14:00',0,1077.7,3,26.2,8.2,82.2,54.8,109.6,4919,225,1.2);

INSERT INTO performance_metric_samples(test_result_id,timestamp,elapsed_seconds,rps,active_users,avg_response_time,min_response_time,max_response_time,p95_response_time,p99_response_time,request_count,failure_count,error_rate)VALUES(25,'2026-03-24 05:14:01',1,1128.1,6,32.0,8.2,82.2,54.8,109.6,9838,451,1.79);

INSERT INTO performance_metric_samples(test_result_id,timestamp,elapsed_seconds,rps,active_users,avg_response_time,min_response_time,max_response_time,p95_response_time,p99_response_time,request_count,failure_count,error_rate)VALUES(25,'2026-03-24 05:14:02',2,729.9,9,29.4,8.2,82.2,54.8,109.6,14757,677,0.97);

INSERT INTO performance_metric_samples(test_result_id,timestamp,elapsed_seconds,rps,active_users,avg_response_time,min_response_time,max_response_time,p95_response_time,p99_response_time,request_count,failure_count,error_rate)VALUES(25,'2026-03-24 05:14:03',3,950.5,12,30.3,8.2,82.2,54.8,109.6,19676,903,0.75);

INSERT INTO performance_metric_samples(test_result_id,timestamp,elapsed_seconds,rps,active_users,avg_response_time,min_response_time,max_response_time,p95_response_time,p99_response_time,request_count,failure_count,error_rate)VALUES(25,'2026-03-24 05:14:04',4,862.3,15,25.2,8.2,82.2,54.8,109.6,24595,1128,0.26);

INSERT INTO performance_metric_samples(test_result_id,timestamp,elapsed_seconds,rps,active_users,avg_response_time,min_response_time,max_response_time,p95_response_time,p99_response_time,request_count,failure_count,error_rate)VALUES(25,'2026-03-24 05:14:05',5,944.2,18,27.0,8.2,82.2,54.8,109.6,29514,1354,0.55);

INSERT INTO performance_metric_samples(test_result_id,timestamp,elapsed_seconds,rps,active_users,avg_response_time,min_response_time,max_response_time,p95_response_time,p99_response_time,request_count,failure_count,error_rate)VALUES(25,'2026-03-24 05:14:06',6,1061.7,21,23.0,8.2,82.2,54.8,109.6,34433,1580,1.58);

INSERT INTO performance_metric_samples(test_result_id,timestamp,elapsed_seconds,rps,active_users,avg_response_time,min_response_time,max_response_time,p95_response_time,p99_response_time,request_count,failure_count,error_rate)VALUES(25,'2026-03-24 05:14:07',7,1013.7,24,32.2,8.2,82.2,54.8,109.6,39353,1806,2.14);

INSERT INTO performance_test_results(id,scenario_id,project_id,user_count,spawn_rate,duration,target_url,status,started_at,finished_at,total_requests,total_failures,error_rate,rps,avg_response_time,min_response_time,max_response_time,p50_response_time,p75_response_time,p95_response_time,p99_response_time,created_at,updated_at)VALUES(26,6,6,117,3,537,'https://example.com/api','failed','2026-02-01 22:33:00','2026-02-01 22:41:57',27886,643,2.31,2742.0,25.2,7.6,126.0,17.6,32.8,63.0,100.8,'2026-02-01 22:33:00','2026-02-01 22:41:57')ON CONFLICT(id)DO NOTHING;

INSERT INTO performance_metric_samples(test_result_id,timestamp,elapsed_seconds,rps,active_users,avg_response_time,min_response_time,max_response_time,p95_response_time,p99_response_time,request_count,failure_count,error_rate)VALUES(26,'2026-02-01 22:33:00',0,3162.9,3,29.3,7.6,75.6,50.4,100.8,3485,80,2.36);

INSERT INTO performance_metric_samples(test_result_id,timestamp,elapsed_seconds,rps,active_users,avg_response_time,min_response_time,max_response_time,p95_response_time,p99_response_time,request_count,failure_count,error_rate)VALUES(26,'2026-02-01 22:33:01',1,2874.1,6,21.4,7.6,75.6,50.4,100.8,6971,160,1.63);

INSERT INTO performance_metric_samples(test_result_id,timestamp,elapsed_seconds,rps,active_users,avg_response_time,min_response_time,max_response_time,p95_response_time,p99_response_time,request_count,failure_count,error_rate)VALUES(26,'2026-02-01 22:33:02',2,2849.9,9,20.7,7.6,75.6,50.4,100.8,10457,241,2.54);

INSERT INTO performance_metric_samples(test_result_id,timestamp,elapsed_seconds,rps,active_users,avg_response_time,min_response_time,max_response_time,p95_response_time,p99_response_time,request_count,failure_count,error_rate)VALUES(26,'2026-02-01 22:33:03',3,2126.6,12,20.2,7.6,75.6,50.4,100.8,13943,321,2.42);

INSERT INTO performance_metric_samples(test_result_id,timestamp,elapsed_seconds,rps,active_users,avg_response_time,min_response_time,max_response_time,p95_response_time,p99_response_time,request_count,failure_count,error_rate)VALUES(26,'2026-02-01 22:33:04',4,3358.8,15,28.6,7.6,75.6,50.4,100.8,17428,401,0.25);

INSERT INTO performance_metric_samples(test_result_id,timestamp,elapsed_seconds,rps,active_users,avg_response_time,min_response_time,max_response_time,p95_response_time,p99_response_time,request_count,failure_count,error_rate)VALUES(26,'2026-02-01 22:33:05',5,2363.9,18,21.2,7.6,75.6,50.4,100.8,20914,482,1.78);

INSERT INTO performance_metric_samples(test_result_id,timestamp,elapsed_seconds,rps,active_users,avg_response_time,min_response_time,max_response_time,p95_response_time,p99_response_time,request_count,failure_count,error_rate)VALUES(26,'2026-02-01 22:33:06',6,3271.7,21,25.0,7.6,75.6,50.4,100.8,24400,562,0.99);

INSERT INTO performance_metric_samples(test_result_id,timestamp,elapsed_seconds,rps,active_users,avg_response_time,min_response_time,max_response_time,p95_response_time,p99_response_time,request_count,failure_count,error_rate)VALUES(26,'2026-02-01 22:33:07',7,2019.5,24,26.1,7.6,75.6,50.4,100.8,27886,643,1.53);

INSERT INTO performance_test_results(id,scenario_id,project_id,user_count,spawn_rate,duration,target_url,status,started_at,finished_at,total_requests,total_failures,error_rate,rps,avg_response_time,min_response_time,max_response_time,p50_response_time,p75_response_time,p95_response_time,p99_response_time,created_at,updated_at)VALUES(27,6,6,182,5,588,'https://example.com/api','completed','2026-05-18 11:47:00','2026-05-18 11:56:48',37834,1400,3.7,1511.1,101.1,30.3,505.5,70.8,131.4,252.8,404.4,'2026-05-18 11:47:00','2026-05-18 11:56:48')ON CONFLICT(id)DO NOTHING;

INSERT INTO performance_metric_samples(test_result_id,timestamp,elapsed_seconds,rps,active_users,avg_response_time,min_response_time,max_response_time,p95_response_time,p99_response_time,request_count,failure_count,error_rate)VALUES(27,'2026-05-18 11:47:00',0,1330.6,3,110.0,30.3,303.3,202.2,404.4,4729,175,2.81);

INSERT INTO performance_metric_samples(test_result_id,timestamp,elapsed_seconds,rps,active_users,avg_response_time,min_response_time,max_response_time,p95_response_time,p99_response_time,request_count,failure_count,error_rate)VALUES(27,'2026-05-18 11:47:01',1,1788.2,6,108.7,30.3,303.3,202.2,404.4,9458,350,0.34);

INSERT INTO performance_metric_samples(test_result_id,timestamp,elapsed_seconds,rps,active_users,avg_response_time,min_response_time,max_response_time,p95_response_time,p99_response_time,request_count,failure_count,error_rate)VALUES(27,'2026-05-18 11:47:02',2,1057.8,9,116.5,30.3,303.3,202.2,404.4,14187,525,1.56);

INSERT INTO performance_metric_samples(test_result_id,timestamp,elapsed_seconds,rps,active_users,avg_response_time,min_response_time,max_response_time,p95_response_time,p99_response_time,request_count,failure_count,error_rate)VALUES(27,'2026-05-18 11:47:03',3,1281.9,12,100.0,30.3,303.3,202.2,404.4,18917,700,2.5);

INSERT INTO performance_metric_samples(test_result_id,timestamp,elapsed_seconds,rps,active_users,avg_response_time,min_response_time,max_response_time,p95_response_time,p99_response_time,request_count,failure_count,error_rate)VALUES(27,'2026-05-18 11:47:04',4,1460.2,15,118.3,30.3,303.3,202.2,404.4,23646,875,0.9);

INSERT INTO performance_metric_samples(test_result_id,timestamp,elapsed_seconds,rps,active_users,avg_response_time,min_response_time,max_response_time,p95_response_time,p99_response_time,request_count,failure_count,error_rate)VALUES(27,'2026-05-18 11:47:05',5,1496.3,18,114.1,30.3,303.3,202.2,404.4,28375,1050,2.53);

INSERT INTO performance_metric_samples(test_result_id,timestamp,elapsed_seconds,rps,active_users,avg_response_time,min_response_time,max_response_time,p95_response_time,p99_response_time,request_count,failure_count,error_rate)VALUES(27,'2026-05-18 11:47:06',6,1553.5,21,108.4,30.3,303.3,202.2,404.4,33104,1225,2.58);

INSERT INTO performance_metric_samples(test_result_id,timestamp,elapsed_seconds,rps,active_users,avg_response_time,min_response_time,max_response_time,p95_response_time,p99_response_time,request_count,failure_count,error_rate)VALUES(27,'2026-05-18 11:47:07',7,1617.3,24,86.8,30.3,303.3,202.2,404.4,37834,1400,0.06);

INSERT INTO performance_test_results(id,scenario_id,project_id,user_count,spawn_rate,duration,target_url,status,started_at,finished_at,total_requests,total_failures,error_rate,rps,avg_response_time,min_response_time,max_response_time,p50_response_time,p75_response_time,p95_response_time,p99_response_time,created_at,updated_at)VALUES(28,6,6,84,10,306,'https://example.com/api','completed','2026-04-25 10:18:00','2026-04-25 10:23:06',34522,1280,3.71,1662.7,198.3,59.5,991.5,138.8,257.8,495.8,793.2,'2026-04-25 10:18:00','2026-04-25 10:23:06')ON CONFLICT(id)DO NOTHING;

INSERT INTO performance_metric_samples(test_result_id,timestamp,elapsed_seconds,rps,active_users,avg_response_time,min_response_time,max_response_time,p95_response_time,p99_response_time,request_count,failure_count,error_rate)VALUES(28,'2026-04-25 10:18:00',0,1829.8,3,197.7,59.5,594.9,396.6,793.2,4315,160,2.0);

INSERT INTO performance_metric_samples(test_result_id,timestamp,elapsed_seconds,rps,active_users,avg_response_time,min_response_time,max_response_time,p95_response_time,p99_response_time,request_count,failure_count,error_rate)VALUES(28,'2026-04-25 10:18:01',1,1554.1,6,222.1,59.5,594.9,396.6,793.2,8630,320,1.39);

INSERT INTO performance_metric_samples(test_result_id,timestamp,elapsed_seconds,rps,active_users,avg_response_time,min_response_time,max_response_time,p95_response_time,p99_response_time,request_count,failure_count,error_rate)VALUES(28,'2026-04-25 10:18:02',2,1975.4,9,160.9,59.5,594.9,396.6,793.2,12945,480,1.37);

INSERT INTO performance_metric_samples(test_result_id,timestamp,elapsed_seconds,rps,active_users,avg_response_time,min_response_time,max_response_time,p95_response_time,p99_response_time,request_count,failure_count,error_rate)VALUES(28,'2026-04-25 10:18:03',3,1726.8,3,204.7,59.5,594.9,396.6,793.2,17261,640,0.1);

INSERT INTO performance_metric_samples(test_result_id,timestamp,elapsed_seconds,rps,active_users,avg_response_time,min_response_time,max_response_time,p95_response_time,p99_response_time,request_count,failure_count,error_rate)VALUES(28,'2026-04-25 10:18:04',4,1812.8,15,207.8,59.5,594.9,396.6,793.2,21576,800,0.13);

INSERT INTO performance_metric_samples(test_result_id,timestamp,elapsed_seconds,rps,active_users,avg_response_time,min_response_time,max_response_time,p95_response_time,p99_response_time,request_count,failure_count,error_rate)VALUES(28,'2026-04-25 10:18:05',5,2068.8,18,195.8,59.5,594.9,396.6,793.2,25891,960,2.17);

INSERT INTO performance_metric_samples(test_result_id,timestamp,elapsed_seconds,rps,active_users,avg_response_time,min_response_time,max_response_time,p95_response_time,p99_response_time,request_count,failure_count,error_rate)VALUES(28,'2026-04-25 10:18:06',6,1440.1,21,187.0,59.5,594.9,396.6,793.2,30206,1120,2.57);

INSERT INTO performance_metric_samples(test_result_id,timestamp,elapsed_seconds,rps,active_users,avg_response_time,min_response_time,max_response_time,p95_response_time,p99_response_time,request_count,failure_count,error_rate)VALUES(28,'2026-04-25 10:18:07',7,1665.9,24,230.2,59.5,594.9,396.6,793.2,34522,1280,1.58);

INSERT INTO performance_test_results(id,scenario_id,project_id,user_count,spawn_rate,duration,target_url,status,started_at,finished_at,total_requests,total_failures,error_rate,rps,avg_response_time,min_response_time,max_response_time,p50_response_time,p75_response_time,p95_response_time,p99_response_time,created_at,updated_at)VALUES(29,6,6,45,9,215,'https://example.com/api','completed','2026-01-21 07:49:00','2026-01-21 07:52:35',43987,1581,3.59,1050.9,290.3,87.1,1451.5,203.2,377.4,725.8,1161.2,'2026-01-21 07:49:00','2026-01-21 07:52:35')ON CONFLICT(id)DO NOTHING;

INSERT INTO performance_metric_samples(test_result_id,timestamp,elapsed_seconds,rps,active_users,avg_response_time,min_response_time,max_response_time,p95_response_time,p99_response_time,request_count,failure_count,error_rate)VALUES(29,'2026-01-21 07:49:00',0,1230.6,3,267.4,87.1,870.9,580.6,1161.2,5498,197,1.18);

INSERT INTO performance_metric_samples(test_result_id,timestamp,elapsed_seconds,rps,active_users,avg_response_time,min_response_time,max_response_time,p95_response_time,p99_response_time,request_count,failure_count,error_rate)VALUES(29,'2026-01-21 07:49:01',1,1313.3,6,288.4,87.1,870.9,580.6,1161.2,10996,395,2.89);

INSERT INTO performance_metric_samples(test_result_id,timestamp,elapsed_seconds,rps,active_users,avg_response_time,min_response_time,max_response_time,p95_response_time,p99_response_time,request_count,failure_count,error_rate)VALUES(29,'2026-01-21 07:49:02',2,1117.6,9,299.1,87.1,870.9,580.6,1161.2,16495,592,2.78);

INSERT INTO performance_metric_samples(test_result_id,timestamp,elapsed_seconds,rps,active_users,avg_response_time,min_response_time,max_response_time,p95_response_time,p99_response_time,request_count,failure_count,error_rate)VALUES(29,'2026-01-21 07:49:03',3,1224.5,12,262.3,87.1,870.9,580.6,1161.2,21993,790,2.09);

INSERT INTO performance_metric_samples(test_result_id,timestamp,elapsed_seconds,rps,active_users,avg_response_time,min_response_time,max_response_time,p95_response_time,p99_response_time,request_count,failure_count,error_rate)VALUES(29,'2026-01-21 07:49:04',4,1106.9,15,272.7,87.1,870.9,580.6,1161.2,27491,988,1.85);

INSERT INTO performance_metric_samples(test_result_id,timestamp,elapsed_seconds,rps,active_users,avg_response_time,min_response_time,max_response_time,p95_response_time,p99_response_time,request_count,failure_count,error_rate)VALUES(29,'2026-01-21 07:49:05',5,990.2,12,235.7,87.1,870.9,580.6,1161.2,32990,1185,2.2);

INSERT INTO performance_metric_samples(test_result_id,timestamp,elapsed_seconds,rps,active_users,avg_response_time,min_response_time,max_response_time,p95_response_time,p99_response_time,request_count,failure_count,error_rate)VALUES(29,'2026-01-21 07:49:06',6,881.7,21,244.6,87.1,870.9,580.6,1161.2,38488,1383,2.8);

INSERT INTO performance_metric_samples(test_result_id,timestamp,elapsed_seconds,rps,active_users,avg_response_time,min_response_time,max_response_time,p95_response_time,p99_response_time,request_count,failure_count,error_rate)VALUES(29,'2026-01-21 07:49:07',7,1036.0,24,259.1,87.1,870.9,580.6,1161.2,43987,1581,2.32);

INSERT INTO performance_test_results(id,scenario_id,project_id,user_count,spawn_rate,duration,target_url,status,started_at,finished_at,total_requests,total_failures,error_rate,rps,avg_response_time,min_response_time,max_response_time,p50_response_time,p75_response_time,p95_response_time,p99_response_time,created_at,updated_at)VALUES(30,7,7,28,15,453,'https://example.com/api','failed','2026-05-06 04:14:00','2026-05-06 04:21:33',5218,16,0.31,788.9,29.4,8.8,147.0,20.6,38.2,73.5,117.6,'2026-05-06 04:14:00','2026-05-06 04:21:33')ON CONFLICT(id)DO NOTHING;

INSERT INTO performance_metric_samples(test_result_id,timestamp,elapsed_seconds,rps,active_users,avg_response_time,min_response_time,max_response_time,p95_response_time,p99_response_time,request_count,failure_count,error_rate)VALUES(30,'2026-05-06 04:14:00',0,913.6,3,30.9,8.8,88.2,58.8,117.6,652,2,0.09);

INSERT INTO performance_metric_samples(test_result_id,timestamp,elapsed_seconds,rps,active_users,avg_response_time,min_response_time,max_response_time,p95_response_time,p99_response_time,request_count,failure_count,error_rate)VALUES(30,'2026-05-06 04:14:01',1,634.6,6,31.7,8.8,88.2,58.8,117.6,1304,4,1.13);

INSERT INTO performance_metric_samples(test_result_id,timestamp,elapsed_seconds,rps,active_users,avg_response_time,min_response_time,max_response_time,p95_response_time,p99_response_time,request_count,failure_count,error_rate)VALUES(30,'2026-05-06 04:14:02',2,1020.3,9,30.1,8.8,88.2,58.8,117.6,1956,6,0.59);

INSERT INTO performance_metric_samples(test_result_id,timestamp,elapsed_seconds,rps,active_users,avg_response_time,min_response_time,max_response_time,p95_response_time,p99_response_time,request_count,failure_count,error_rate)VALUES(30,'2026-05-06 04:14:03',3,784.7,12,26.9,8.8,88.2,58.8,117.6,2609,8,0.6);

INSERT INTO performance_metric_samples(test_result_id,timestamp,elapsed_seconds,rps,active_users,avg_response_time,min_response_time,max_response_time,p95_response_time,p99_response_time,request_count,failure_count,error_rate)VALUES(30,'2026-05-06 04:14:04',4,629.0,15,33.0,8.8,88.2,58.8,117.6,3261,10,0.58);

INSERT INTO performance_metric_samples(test_result_id,timestamp,elapsed_seconds,rps,active_users,avg_response_time,min_response_time,max_response_time,p95_response_time,p99_response_time,request_count,failure_count,error_rate)VALUES(30,'2026-05-06 04:14:05',5,827.8,18,34.8,8.8,88.2,58.8,117.6,3913,12,0.29);

INSERT INTO performance_metric_samples(test_result_id,timestamp,elapsed_seconds,rps,active_users,avg_response_time,min_response_time,max_response_time,p95_response_time,p99_response_time,request_count,failure_count,error_rate)VALUES(30,'2026-05-06 04:14:06',6,568.0,21,34.0,8.8,88.2,58.8,117.6,4565,14,1.08);

INSERT INTO performance_metric_samples(test_result_id,timestamp,elapsed_seconds,rps,active_users,avg_response_time,min_response_time,max_response_time,p95_response_time,p99_response_time,request_count,failure_count,error_rate)VALUES(30,'2026-05-06 04:14:07',7,745.4,24,33.7,8.8,88.2,58.8,117.6,5218,16,1.02);

INSERT INTO performance_test_results(id,scenario_id,project_id,user_count,spawn_rate,duration,target_url,status,started_at,finished_at,total_requests,total_failures,error_rate,rps,avg_response_time,min_response_time,max_response_time,p50_response_time,p75_response_time,p95_response_time,p99_response_time,created_at,updated_at)VALUES(31,7,7,45,3,272,'https://example.com/api','failed','2026-01-16 18:48:00','2026-01-16 18:52:32',33823,595,1.76,1874.5,230.1,69.0,1150.5,161.1,299.1,575.2,920.4,'2026-01-16 18:48:00','2026-01-16 18:52:32')ON CONFLICT(id)DO NOTHING;

INSERT INTO performance_metric_samples(test_result_id,timestamp,elapsed_seconds,rps,active_users,avg_response_time,min_response_time,max_response_time,p95_response_time,p99_response_time,request_count,failure_count,error_rate)VALUES(31,'2026-01-16 18:48:00',0,1805.8,3,218.7,69.0,690.3,460.2,920.4,4227,74,0.21);

INSERT INTO performance_metric_samples(test_result_id,timestamp,elapsed_seconds,rps,active_users,avg_response_time,min_response_time,max_response_time,p95_response_time,p99_response_time,request_count,failure_count,error_rate)VALUES(31,'2026-01-16 18:48:01',1,1400.0,6,211.5,69.0,690.3,460.2,920.4,8455,148,0.35);

INSERT INTO performance_metric_samples(test_result_id,timestamp,elapsed_seconds,rps,active_users,avg_response_time,min_response_time,max_response_time,p95_response_time,p99_response_time,request_count,failure_count,error_rate)VALUES(31,'2026-01-16 18:48:02',2,1571.5,9,233.8,69.0,690.3,460.2,920.4,12683,223,0.07);

INSERT INTO performance_metric_samples(test_result_id,timestamp,elapsed_seconds,rps,active_users,avg_response_time,min_response_time,max_response_time,p95_response_time,p99_response_time,request_count,failure_count,error_rate)VALUES(31,'2026-01-16 18:48:03',3,2235.9,12,269.0,69.0,690.3,460.2,920.4,16911,297,0.75);

INSERT INTO performance_metric_samples(test_result_id,timestamp,elapsed_seconds,rps,active_users,avg_response_time,min_response_time,max_response_time,p95_response_time,p99_response_time,request_count,failure_count,error_rate)VALUES(31,'2026-01-16 18:48:04',4,2103.1,15,264.4,69.0,690.3,460.2,920.4,21139,371,0.47);

INSERT INTO performance_metric_samples(test_result_id,timestamp,elapsed_seconds,rps,active_users,avg_response_time,min_response_time,max_response_time,p95_response_time,p99_response_time,request_count,failure_count,error_rate)VALUES(31,'2026-01-16 18:48:05',5,1636.1,18,237.0,69.0,690.3,460.2,920.4,25367,446,2.56);

INSERT INTO performance_metric_samples(test_result_id,timestamp,elapsed_seconds,rps,active_users,avg_response_time,min_response_time,max_response_time,p95_response_time,p99_response_time,request_count,failure_count,error_rate)VALUES(31,'2026-01-16 18:48:06',6,2360.2,21,212.8,69.0,690.3,460.2,920.4,29595,520,1.86);

INSERT INTO performance_metric_samples(test_result_id,timestamp,elapsed_seconds,rps,active_users,avg_response_time,min_response_time,max_response_time,p95_response_time,p99_response_time,request_count,failure_count,error_rate)VALUES(31,'2026-01-16 18:48:07',7,1926.2,24,237.7,69.0,690.3,460.2,920.4,33823,595,2.81);

INSERT INTO performance_test_results(id,scenario_id,project_id,user_count,spawn_rate,duration,target_url,status,started_at,finished_at,total_requests,total_failures,error_rate,rps,avg_response_time,min_response_time,max_response_time,p50_response_time,p75_response_time,p95_response_time,p99_response_time,created_at,updated_at)VALUES(32,7,7,45,7,93,'https://example.com/api','completed','2026-03-25 13:59:00','2026-03-25 14:00:33',28617,373,1.3,1036.9,309.4,92.8,1547.0,216.6,402.2,773.5,1237.6,'2026-03-25 13:59:00','2026-03-25 14:00:33')ON CONFLICT(id)DO NOTHING;

INSERT INTO performance_metric_samples(test_result_id,timestamp,elapsed_seconds,rps,active_users,avg_response_time,min_response_time,max_response_time,p95_response_time,p99_response_time,request_count,failure_count,error_rate)VALUES(32,'2026-03-25 13:59:00',0,1066.2,3,288.3,92.8,928.2,618.8,1237.6,3577,46,2.27);

INSERT INTO performance_metric_samples(test_result_id,timestamp,elapsed_seconds,rps,active_users,avg_response_time,min_response_time,max_response_time,p95_response_time,p99_response_time,request_count,failure_count,error_rate)VALUES(32,'2026-03-25 13:59:01',1,1293.4,6,276.7,92.8,928.2,618.8,1237.6,7154,93,0.22);

INSERT INTO performance_metric_samples(test_result_id,timestamp,elapsed_seconds,rps,active_users,avg_response_time,min_response_time,max_response_time,p95_response_time,p99_response_time,request_count,failure_count,error_rate)VALUES(32,'2026-03-25 13:59:02',2,1315.6,9,334.5,92.8,928.2,618.8,1237.6,10731,139,2.3);

INSERT INTO performance_metric_samples(test_result_id,timestamp,elapsed_seconds,rps,active_users,avg_response_time,min_response_time,max_response_time,p95_response_time,p99_response_time,request_count,failure_count,error_rate)VALUES(32,'2026-03-25 13:59:03',3,747.8,12,365.1,92.8,928.2,618.8,1237.6,14308,186,1.79);

INSERT INTO performance_metric_samples(test_result_id,timestamp,elapsed_seconds,rps,active_users,avg_response_time,min_response_time,max_response_time,p95_response_time,p99_response_time,request_count,failure_count,error_rate)VALUES(32,'2026-03-25 13:59:04',4,1106.8,15,357.4,92.8,928.2,618.8,1237.6,17885,233,1.44);

INSERT INTO performance_metric_samples(test_result_id,timestamp,elapsed_seconds,rps,active_users,avg_response_time,min_response_time,max_response_time,p95_response_time,p99_response_time,request_count,failure_count,error_rate)VALUES(32,'2026-03-25 13:59:05',5,806.4,18,252.7,92.8,928.2,618.8,1237.6,21462,279,0.11);

INSERT INTO performance_metric_samples(test_result_id,timestamp,elapsed_seconds,rps,active_users,avg_response_time,min_response_time,max_response_time,p95_response_time,p99_response_time,request_count,failure_count,error_rate)VALUES(32,'2026-03-25 13:59:06',6,1041.6,21,290.9,92.8,928.2,618.8,1237.6,25039,326,1.43);

INSERT INTO performance_metric_samples(test_result_id,timestamp,elapsed_seconds,rps,active_users,avg_response_time,min_response_time,max_response_time,p95_response_time,p99_response_time,request_count,failure_count,error_rate)VALUES(32,'2026-03-25 13:59:07',7,1212.1,24,250.2,92.8,928.2,618.8,1237.6,28617,373,0.17);

INSERT INTO performance_test_results(id,scenario_id,project_id,user_count,spawn_rate,duration,target_url,status,started_at,finished_at,total_requests,total_failures,error_rate,rps,avg_response_time,min_response_time,max_response_time,p50_response_time,p75_response_time,p95_response_time,p99_response_time,created_at,updated_at)VALUES(33,7,7,42,14,448,'https://example.com/api','completed','2026-04-11 16:22:00','2026-04-11 16:29:28',37208,897,2.41,1192.0,160.2,48.1,801.0,112.1,208.3,400.5,640.8,'2026-04-11 16:22:00','2026-04-11 16:29:28')ON CONFLICT(id)DO NOTHING;

INSERT INTO performance_metric_samples(test_result_id,timestamp,elapsed_seconds,rps,active_users,avg_response_time,min_response_time,max_response_time,p95_response_time,p99_response_time,request_count,failure_count,error_rate)VALUES(33,'2026-04-11 16:22:00',0,1336.0,3,137.0,48.1,480.6,320.4,640.8,4651,112,1.31);

INSERT INTO performance_metric_samples(test_result_id,timestamp,elapsed_seconds,rps,active_users,avg_response_time,min_response_time,max_response_time,p95_response_time,p99_response_time,request_count,failure_count,error_rate)VALUES(33,'2026-04-11 16:22:01',1,1476.0,6,150.7,48.1,480.6,320.4,640.8,9302,224,1.03);

INSERT INTO performance_metric_samples(test_result_id,timestamp,elapsed_seconds,rps,active_users,avg_response_time,min_response_time,max_response_time,p95_response_time,p99_response_time,request_count,failure_count,error_rate)VALUES(33,'2026-04-11 16:22:02',2,1491.0,9,143.0,48.1,480.6,320.4,640.8,13953,336,1.77);

INSERT INTO performance_metric_samples(test_result_id,timestamp,elapsed_seconds,rps,active_users,avg_response_time,min_response_time,max_response_time,p95_response_time,p99_response_time,request_count,failure_count,error_rate)VALUES(33,'2026-04-11 16:22:03',3,996.8,12,176.4,48.1,480.6,320.4,640.8,18604,448,2.42);

INSERT INTO performance_metric_samples(test_result_id,timestamp,elapsed_seconds,rps,active_users,avg_response_time,min_response_time,max_response_time,p95_response_time,p99_response_time,request_count,failure_count,error_rate)VALUES(33,'2026-04-11 16:22:04',4,1217.9,12,191.7,48.1,480.6,320.4,640.8,23255,560,0.04);

INSERT INTO performance_metric_samples(test_result_id,timestamp,elapsed_seconds,rps,active_users,avg_response_time,min_response_time,max_response_time,p95_response_time,p99_response_time,request_count,failure_count,error_rate)VALUES(33,'2026-04-11 16:22:05',5,1349.2,15,133.1,48.1,480.6,320.4,640.8,27906,672,0.38);

INSERT INTO performance_metric_samples(test_result_id,timestamp,elapsed_seconds,rps,active_users,avg_response_time,min_response_time,max_response_time,p95_response_time,p99_response_time,request_count,failure_count,error_rate)VALUES(33,'2026-04-11 16:22:06',6,963.6,12,148.3,48.1,480.6,320.4,640.8,32557,784,1.81);

INSERT INTO performance_metric_samples(test_result_id,timestamp,elapsed_seconds,rps,active_users,avg_response_time,min_response_time,max_response_time,p95_response_time,p99_response_time,request_count,failure_count,error_rate)VALUES(33,'2026-04-11 16:22:07',7,1471.2,24,136.5,48.1,480.6,320.4,640.8,37208,897,1.19);

INSERT INTO performance_test_results(id,scenario_id,project_id,user_count,spawn_rate,duration,target_url,status,started_at,finished_at,total_requests,total_failures,error_rate,rps,avg_response_time,min_response_time,max_response_time,p50_response_time,p75_response_time,p95_response_time,p99_response_time,created_at,updated_at)VALUES(34,8,8,66,15,270,'https://example.com/api','failed','2026-05-13 07:44:00','2026-05-13 07:48:30',47219,1735,3.67,1103.0,367.3,110.2,1836.5,257.1,477.5,918.2,1469.2,'2026-05-13 07:44:00','2026-05-13 07:48:30')ON CONFLICT(id)DO NOTHING;

INSERT INTO performance_metric_samples(test_result_id,timestamp,elapsed_seconds,rps,active_users,avg_response_time,min_response_time,max_response_time,p95_response_time,p99_response_time,request_count,failure_count,error_rate)VALUES(34,'2026-05-13 07:44:00',0,1244.1,3,408.5,110.2,1101.9,734.6,1469.2,5902,216,0.88);

INSERT INTO performance_metric_samples(test_result_id,timestamp,elapsed_seconds,rps,active_users,avg_response_time,min_response_time,max_response_time,p95_response_time,p99_response_time,request_count,failure_count,error_rate)VALUES(34,'2026-05-13 07:44:01',1,1204.7,6,425.0,110.2,1101.9,734.6,1469.2,11804,433,0.96);

INSERT INTO performance_metric_samples(test_result_id,timestamp,elapsed_seconds,rps,active_users,avg_response_time,min_response_time,max_response_time,p95_response_time,p99_response_time,request_count,failure_count,error_rate)VALUES(34,'2026-05-13 07:44:02',2,1130.4,9,301.8,110.2,1101.9,734.6,1469.2,17707,650,2.7);

INSERT INTO performance_metric_samples(test_result_id,timestamp,elapsed_seconds,rps,active_users,avg_response_time,min_response_time,max_response_time,p95_response_time,p99_response_time,request_count,failure_count,error_rate)VALUES(34,'2026-05-13 07:44:03',3,1239.0,12,365.3,110.2,1101.9,734.6,1469.2,23609,867,0.24);

INSERT INTO performance_metric_samples(test_result_id,timestamp,elapsed_seconds,rps,active_users,avg_response_time,min_response_time,max_response_time,p95_response_time,p99_response_time,request_count,failure_count,error_rate)VALUES(34,'2026-05-13 07:44:04',4,1375.7,15,327.7,110.2,1101.9,734.6,1469.2,29511,1084,2.23);

INSERT INTO performance_metric_samples(test_result_id,timestamp,elapsed_seconds,rps,active_users,avg_response_time,min_response_time,max_response_time,p95_response_time,p99_response_time,request_count,failure_count,error_rate)VALUES(34,'2026-05-13 07:44:05',5,911.6,18,400.3,110.2,1101.9,734.6,1469.2,35414,1301,2.36);

INSERT INTO performance_metric_samples(test_result_id,timestamp,elapsed_seconds,rps,active_users,avg_response_time,min_response_time,max_response_time,p95_response_time,p99_response_time,request_count,failure_count,error_rate)VALUES(34,'2026-05-13 07:44:06',6,795.8,21,396.4,110.2,1101.9,734.6,1469.2,41316,1518,1.95);

INSERT INTO performance_metric_samples(test_result_id,timestamp,elapsed_seconds,rps,active_users,avg_response_time,min_response_time,max_response_time,p95_response_time,p99_response_time,request_count,failure_count,error_rate)VALUES(34,'2026-05-13 07:44:07',7,1072.4,24,297.0,110.2,1101.9,734.6,1469.2,47219,1735,2.51);

INSERT INTO performance_test_results(id,scenario_id,project_id,user_count,spawn_rate,duration,target_url,status,started_at,finished_at,total_requests,total_failures,error_rate,rps,avg_response_time,min_response_time,max_response_time,p50_response_time,p75_response_time,p95_response_time,p99_response_time,created_at,updated_at)VALUES(35,8,8,14,13,453,'https://example.com/api','completed','2026-03-24 01:23:00','2026-03-24 01:30:33',6537,19,0.29,2571.0,162.8,48.8,814.0,114.0,211.6,407.0,651.2,'2026-03-24 01:23:00','2026-03-24 01:30:33')ON CONFLICT(id)DO NOTHING;

INSERT INTO performance_metric_samples(test_result_id,timestamp,elapsed_seconds,rps,active_users,avg_response_time,min_response_time,max_response_time,p95_response_time,p99_response_time,request_count,failure_count,error_rate)VALUES(35,'2026-03-24 01:23:00',0,2393.1,3,144.9,48.8,488.4,325.6,651.2,817,2,1.14);

INSERT INTO performance_metric_samples(test_result_id,timestamp,elapsed_seconds,rps,active_users,avg_response_time,min_response_time,max_response_time,p95_response_time,p99_response_time,request_count,failure_count,error_rate)VALUES(35,'2026-03-24 01:23:01',1,2817.7,6,133.6,48.8,488.4,325.6,651.2,1634,4,0.92);

INSERT INTO performance_metric_samples(test_result_id,timestamp,elapsed_seconds,rps,active_users,avg_response_time,min_response_time,max_response_time,p95_response_time,p99_response_time,request_count,failure_count,error_rate)VALUES(35,'2026-03-24 01:23:02',2,2635.1,9,191.3,48.8,488.4,325.6,651.2,2451,7,2.73);

INSERT INTO performance_metric_samples(test_result_id,timestamp,elapsed_seconds,rps,active_users,avg_response_time,min_response_time,max_response_time,p95_response_time,p99_response_time,request_count,failure_count,error_rate)VALUES(35,'2026-03-24 01:23:03',3,2963.6,12,190.3,48.8,488.4,325.6,651.2,3268,9,2.72);

INSERT INTO performance_metric_samples(test_result_id,timestamp,elapsed_seconds,rps,active_users,avg_response_time,min_response_time,max_response_time,p95_response_time,p99_response_time,request_count,failure_count,error_rate)VALUES(35,'2026-03-24 01:23:04',4,3049.6,15,144.3,48.8,488.4,325.6,651.2,4085,11,0.08);

INSERT INTO performance_metric_samples(test_result_id,timestamp,elapsed_seconds,rps,active_users,avg_response_time,min_response_time,max_response_time,p95_response_time,p99_response_time,request_count,failure_count,error_rate)VALUES(35,'2026-03-24 01:23:05',5,2919.3,18,158.5,48.8,488.4,325.6,651.2,4902,14,1.28);

INSERT INTO performance_metric_samples(test_result_id,timestamp,elapsed_seconds,rps,active_users,avg_response_time,min_response_time,max_response_time,p95_response_time,p99_response_time,request_count,failure_count,error_rate)VALUES(35,'2026-03-24 01:23:06',6,2924.6,21,179.2,48.8,488.4,325.6,651.2,5719,16,2.42);

INSERT INTO performance_metric_samples(test_result_id,timestamp,elapsed_seconds,rps,active_users,avg_response_time,min_response_time,max_response_time,p95_response_time,p99_response_time,request_count,failure_count,error_rate)VALUES(35,'2026-03-24 01:23:07',7,2653.2,24,191.0,48.8,488.4,325.6,651.2,6537,19,0.86);

INSERT INTO performance_test_results(id,scenario_id,project_id,user_count,spawn_rate,duration,target_url,status,started_at,finished_at,total_requests,total_failures,error_rate,rps,avg_response_time,min_response_time,max_response_time,p50_response_time,p75_response_time,p95_response_time,p99_response_time,created_at,updated_at)VALUES(36,8,8,70,5,591,'https://example.com/api','completed','2026-01-15 19:33:00','2026-01-15 19:42:51',11652,559,4.8,1428.6,397.2,119.2,1986.0,278.0,516.4,993.0,1588.8,'2026-01-15 19:33:00','2026-01-15 19:42:51')ON CONFLICT(id)DO NOTHING;

INSERT INTO performance_metric_samples(test_result_id,timestamp,elapsed_seconds,rps,active_users,avg_response_time,min_response_time,max_response_time,p95_response_time,p99_response_time,request_count,failure_count,error_rate)VALUES(36,'2026-01-15 19:33:00',0,1778.1,3,444.8,119.2,1191.6,794.4,1588.8,1456,69,2.85);

INSERT INTO performance_metric_samples(test_result_id,timestamp,elapsed_seconds,rps,active_users,avg_response_time,min_response_time,max_response_time,p95_response_time,p99_response_time,request_count,failure_count,error_rate)VALUES(36,'2026-01-15 19:33:01',1,1073.3,6,440.3,119.2,1191.6,794.4,1588.8,2913,139,0.89);

INSERT INTO performance_metric_samples(test_result_id,timestamp,elapsed_seconds,rps,active_users,avg_response_time,min_response_time,max_response_time,p95_response_time,p99_response_time,request_count,failure_count,error_rate)VALUES(36,'2026-01-15 19:33:02',2,1489.5,9,415.6,119.2,1191.6,794.4,1588.8,4369,209,1.09);

INSERT INTO performance_metric_samples(test_result_id,timestamp,elapsed_seconds,rps,active_users,avg_response_time,min_response_time,max_response_time,p95_response_time,p99_response_time,request_count,failure_count,error_rate)VALUES(36,'2026-01-15 19:33:03',3,1565.1,12,446.5,119.2,1191.6,794.4,1588.8,5826,279,1.82);

INSERT INTO performance_metric_samples(test_result_id,timestamp,elapsed_seconds,rps,active_users,avg_response_time,min_response_time,max_response_time,p95_response_time,p99_response_time,request_count,failure_count,error_rate)VALUES(36,'2026-01-15 19:33:04',4,1106.6,15,422.7,119.2,1191.6,794.4,1588.8,7282,349,2.51);

INSERT INTO performance_metric_samples(test_result_id,timestamp,elapsed_seconds,rps,active_users,avg_response_time,min_response_time,max_response_time,p95_response_time,p99_response_time,request_count,failure_count,error_rate)VALUES(36,'2026-01-15 19:33:05',5,1726.5,18,391.3,119.2,1191.6,794.4,1588.8,8739,419,1.32);

INSERT INTO performance_metric_samples(test_result_id,timestamp,elapsed_seconds,rps,active_users,avg_response_time,min_response_time,max_response_time,p95_response_time,p99_response_time,request_count,failure_count,error_rate)VALUES(36,'2026-01-15 19:33:06',6,1399.8,21,394.1,119.2,1191.6,794.4,1588.8,10195,489,2.53);

INSERT INTO performance_metric_samples(test_result_id,timestamp,elapsed_seconds,rps,active_users,avg_response_time,min_response_time,max_response_time,p95_response_time,p99_response_time,request_count,failure_count,error_rate)VALUES(36,'2026-01-15 19:33:07',7,1186.7,15,409.8,119.2,1191.6,794.4,1588.8,11652,559,0.24);

INSERT INTO performance_test_results(id,scenario_id,project_id,user_count,spawn_rate,duration,target_url,status,started_at,finished_at,total_requests,total_failures,error_rate,rps,avg_response_time,min_response_time,max_response_time,p50_response_time,p75_response_time,p95_response_time,p99_response_time,created_at,updated_at)VALUES(37,9,8,47,20,324,'https://example.com/api','completed','2026-05-15 19:49:00','2026-05-15 19:54:24',18009,782,4.34,425.3,257.7,77.3,1288.5,180.4,335.0,644.2,1030.8,'2026-05-15 19:49:00','2026-05-15 19:54:24')ON CONFLICT(id)DO NOTHING;

INSERT INTO performance_metric_samples(test_result_id,timestamp,elapsed_seconds,rps,active_users,avg_response_time,min_response_time,max_response_time,p95_response_time,p99_response_time,request_count,failure_count,error_rate)VALUES(37,'2026-05-15 19:49:00',0,465.1,3,218.0,77.3,773.1,515.4,1030.8,2251,97,0.12);

INSERT INTO performance_metric_samples(test_result_id,timestamp,elapsed_seconds,rps,active_users,avg_response_time,min_response_time,max_response_time,p95_response_time,p99_response_time,request_count,failure_count,error_rate)VALUES(37,'2026-05-15 19:49:01',1,472.4,6,265.9,77.3,773.1,515.4,1030.8,4502,195,0.13);

INSERT INTO performance_metric_samples(test_result_id,timestamp,elapsed_seconds,rps,active_users,avg_response_time,min_response_time,max_response_time,p95_response_time,p99_response_time,request_count,failure_count,error_rate)VALUES(37,'2026-05-15 19:49:02',2,480.8,9,304.3,77.3,773.1,515.4,1030.8,6753,293,2.98);

INSERT INTO performance_metric_samples(test_result_id,timestamp,elapsed_seconds,rps,active_users,avg_response_time,min_response_time,max_response_time,p95_response_time,p99_response_time,request_count,failure_count,error_rate)VALUES(37,'2026-05-15 19:49:03',3,546.6,5,276.1,77.3,773.1,515.4,1030.8,9004,391,2.57);

INSERT INTO performance_metric_samples(test_result_id,timestamp,elapsed_seconds,rps,active_users,avg_response_time,min_response_time,max_response_time,p95_response_time,p99_response_time,request_count,failure_count,error_rate)VALUES(37,'2026-05-15 19:49:04',4,387.9,15,210.8,77.3,773.1,515.4,1030.8,11255,488,0.7);

INSERT INTO performance_metric_samples(test_result_id,timestamp,elapsed_seconds,rps,active_users,avg_response_time,min_response_time,max_response_time,p95_response_time,p99_response_time,request_count,failure_count,error_rate)VALUES(37,'2026-05-15 19:49:05',5,325.6,18,251.9,77.3,773.1,515.4,1030.8,13506,586,1.53);

INSERT INTO performance_metric_samples(test_result_id,timestamp,elapsed_seconds,rps,active_users,avg_response_time,min_response_time,max_response_time,p95_response_time,p99_response_time,request_count,failure_count,error_rate)VALUES(37,'2026-05-15 19:49:06',6,358.2,21,265.0,77.3,773.1,515.4,1030.8,15757,684,2.49);

INSERT INTO performance_metric_samples(test_result_id,timestamp,elapsed_seconds,rps,active_users,avg_response_time,min_response_time,max_response_time,p95_response_time,p99_response_time,request_count,failure_count,error_rate)VALUES(37,'2026-05-15 19:49:07',7,471.5,19,272.3,77.3,773.1,515.4,1030.8,18009,782,2.63);

INSERT INTO performance_test_results(id,scenario_id,project_id,user_count,spawn_rate,duration,target_url,status,started_at,finished_at,total_requests,total_failures,error_rate,rps,avg_response_time,min_response_time,max_response_time,p50_response_time,p75_response_time,p95_response_time,p99_response_time,created_at,updated_at)VALUES(38,9,8,85,20,428,'https://example.com/api','completed','2026-04-26 09:40:00','2026-04-26 09:47:08',27747,1244,4.48,1155.4,377.9,113.4,1889.5,264.5,491.3,944.8,1511.6,'2026-04-26 09:40:00','2026-04-26 09:47:08')ON CONFLICT(id)DO NOTHING;

INSERT INTO performance_metric_samples(test_result_id,timestamp,elapsed_seconds,rps,active_users,avg_response_time,min_response_time,max_response_time,p95_response_time,p99_response_time,request_count,failure_count,error_rate)VALUES(38,'2026-04-26 09:40:00',0,830.4,3,309.1,113.4,1133.7,755.8,1511.6,3468,155,2.79);

INSERT INTO performance_metric_samples(test_result_id,timestamp,elapsed_seconds,rps,active_users,avg_response_time,min_response_time,max_response_time,p95_response_time,p99_response_time,request_count,failure_count,error_rate)VALUES(38,'2026-04-26 09:40:01',1,1440.9,6,318.4,113.4,1133.7,755.8,1511.6,6936,311,0.63);

INSERT INTO performance_metric_samples(test_result_id,timestamp,elapsed_seconds,rps,active_users,avg_response_time,min_response_time,max_response_time,p95_response_time,p99_response_time,request_count,failure_count,error_rate)VALUES(38,'2026-04-26 09:40:02',2,1025.8,9,420.4,113.4,1133.7,755.8,1511.6,10405,466,1.52);

INSERT INTO performance_metric_samples(test_result_id,timestamp,elapsed_seconds,rps,active_users,avg_response_time,min_response_time,max_response_time,p95_response_time,p99_response_time,request_count,failure_count,error_rate)VALUES(38,'2026-04-26 09:40:03',3,1211.9,12,444.4,113.4,1133.7,755.8,1511.6,13873,622,1.14);

INSERT INTO performance_metric_samples(test_result_id,timestamp,elapsed_seconds,rps,active_users,avg_response_time,min_response_time,max_response_time,p95_response_time,p99_response_time,request_count,failure_count,error_rate)VALUES(38,'2026-04-26 09:40:04',4,1212.7,15,412.1,113.4,1133.7,755.8,1511.6,17341,777,1.14);

INSERT INTO performance_metric_samples(test_result_id,timestamp,elapsed_seconds,rps,active_users,avg_response_time,min_response_time,max_response_time,p95_response_time,p99_response_time,request_count,failure_count,error_rate)VALUES(38,'2026-04-26 09:40:05',5,1500.5,18,446.7,113.4,1133.7,755.8,1511.6,20810,933,2.88);

INSERT INTO performance_metric_samples(test_result_id,timestamp,elapsed_seconds,rps,active_users,avg_response_time,min_response_time,max_response_time,p95_response_time,p99_response_time,request_count,failure_count,error_rate)VALUES(38,'2026-04-26 09:40:06',6,1496.7,21,378.4,113.4,1133.7,755.8,1511.6,24278,1088,1.72);

INSERT INTO performance_metric_samples(test_result_id,timestamp,elapsed_seconds,rps,active_users,avg_response_time,min_response_time,max_response_time,p95_response_time,p99_response_time,request_count,failure_count,error_rate)VALUES(38,'2026-04-26 09:40:07',7,1188.8,24,383.8,113.4,1133.7,755.8,1511.6,27747,1244,0.36);

INSERT INTO performance_test_results(id,scenario_id,project_id,user_count,spawn_rate,duration,target_url,status,started_at,finished_at,total_requests,total_failures,error_rate,rps,avg_response_time,min_response_time,max_response_time,p50_response_time,p75_response_time,p95_response_time,p99_response_time,created_at,updated_at)VALUES(39,9,8,72,11,543,'https://example.com/api','failed','2026-01-17 08:22:00','2026-01-17 08:31:03',21770,293,1.35,2516.2,127.8,38.3,639.0,89.5,166.1,319.5,511.2,'2026-01-17 08:22:00','2026-01-17 08:31:03')ON CONFLICT(id)DO NOTHING;

INSERT INTO performance_metric_samples(test_result_id,timestamp,elapsed_seconds,rps,active_users,avg_response_time,min_response_time,max_response_time,p95_response_time,p99_response_time,request_count,failure_count,error_rate)VALUES(39,'2026-01-17 08:22:00',0,2128.3,3,152.2,38.3,383.4,255.6,511.2,2721,36,0.69);

INSERT INTO performance_metric_samples(test_result_id,timestamp,elapsed_seconds,rps,active_users,avg_response_time,min_response_time,max_response_time,p95_response_time,p99_response_time,request_count,failure_count,error_rate)VALUES(39,'2026-01-17 08:22:01',1,2236.6,6,137.7,38.3,383.4,255.6,511.2,5442,73,1.34);

INSERT INTO performance_metric_samples(test_result_id,timestamp,elapsed_seconds,rps,active_users,avg_response_time,min_response_time,max_response_time,p95_response_time,p99_response_time,request_count,failure_count,error_rate)VALUES(39,'2026-01-17 08:22:02',2,3207.1,9,120.7,38.3,383.4,255.6,511.2,8163,109,1.06);

INSERT INTO performance_metric_samples(test_result_id,timestamp,elapsed_seconds,rps,active_users,avg_response_time,min_response_time,max_response_time,p95_response_time,p99_response_time,request_count,failure_count,error_rate)VALUES(39,'2026-01-17 08:22:03',3,2524.7,12,135.6,38.3,383.4,255.6,511.2,10885,146,1.82);

INSERT INTO performance_metric_samples(test_result_id,timestamp,elapsed_seconds,rps,active_users,avg_response_time,min_response_time,max_response_time,p95_response_time,p99_response_time,request_count,failure_count,error_rate)VALUES(39,'2026-01-17 08:22:04',4,2439.2,15,114.0,38.3,383.4,255.6,511.2,13606,183,2.48);

INSERT INTO performance_metric_samples(test_result_id,timestamp,elapsed_seconds,rps,active_users,avg_response_time,min_response_time,max_response_time,p95_response_time,p99_response_time,request_count,failure_count,error_rate)VALUES(39,'2026-01-17 08:22:05',5,3251.0,18,114.8,38.3,383.4,255.6,511.2,16327,219,2.73);

INSERT INTO performance_metric_samples(test_result_id,timestamp,elapsed_seconds,rps,active_users,avg_response_time,min_response_time,max_response_time,p95_response_time,p99_response_time,request_count,failure_count,error_rate)VALUES(39,'2026-01-17 08:22:06',6,2779.0,21,109.3,38.3,383.4,255.6,511.2,19048,256,0.78);

INSERT INTO performance_metric_samples(test_result_id,timestamp,elapsed_seconds,rps,active_users,avg_response_time,min_response_time,max_response_time,p95_response_time,p99_response_time,request_count,failure_count,error_rate)VALUES(39,'2026-01-17 08:22:07',7,2194.5,24,108.3,38.3,383.4,255.6,511.2,21770,293,1.23);

INSERT INTO performance_test_results(id,scenario_id,project_id,user_count,spawn_rate,duration,target_url,status,started_at,finished_at,total_requests,total_failures,error_rate,rps,avg_response_time,min_response_time,max_response_time,p50_response_time,p75_response_time,p95_response_time,p99_response_time,created_at,updated_at)VALUES(40,9,8,77,18,566,'https://example.com/api','completed','2026-01-23 05:24:00','2026-01-23 05:33:26',12790,560,4.38,95.8,61.5,18.4,307.5,43.0,80.0,153.8,246.0,'2026-01-23 05:24:00','2026-01-23 05:33:26')ON CONFLICT(id)DO NOTHING;

INSERT INTO performance_metric_samples(test_result_id,timestamp,elapsed_seconds,rps,active_users,avg_response_time,min_response_time,max_response_time,p95_response_time,p99_response_time,request_count,failure_count,error_rate)VALUES(40,'2026-01-23 05:24:00',0,108.0,3,67.5,18.4,184.5,123.0,246.0,1598,70,0.38);

INSERT INTO performance_metric_samples(test_result_id,timestamp,elapsed_seconds,rps,active_users,avg_response_time,min_response_time,max_response_time,p95_response_time,p99_response_time,request_count,failure_count,error_rate)VALUES(40,'2026-01-23 05:24:01',1,69.0,6,49.8,18.4,184.5,123.0,246.0,3197,140,0.5);

INSERT INTO performance_metric_samples(test_result_id,timestamp,elapsed_seconds,rps,active_users,avg_response_time,min_response_time,max_response_time,p95_response_time,p99_response_time,request_count,failure_count,error_rate)VALUES(40,'2026-01-23 05:24:02',2,71.3,9,70.5,18.4,184.5,123.0,246.0,4796,210,2.76);

INSERT INTO performance_metric_samples(test_result_id,timestamp,elapsed_seconds,rps,active_users,avg_response_time,min_response_time,max_response_time,p95_response_time,p99_response_time,request_count,failure_count,error_rate)VALUES(40,'2026-01-23 05:24:03',3,119.0,12,52.3,18.4,184.5,123.0,246.0,6395,280,2.09);

INSERT INTO performance_metric_samples(test_result_id,timestamp,elapsed_seconds,rps,active_users,avg_response_time,min_response_time,max_response_time,p95_response_time,p99_response_time,request_count,failure_count,error_rate)VALUES(40,'2026-01-23 05:24:04',4,80.9,15,52.1,18.4,184.5,123.0,246.0,7993,350,2.69);

INSERT INTO performance_metric_samples(test_result_id,timestamp,elapsed_seconds,rps,active_users,avg_response_time,min_response_time,max_response_time,p95_response_time,p99_response_time,request_count,failure_count,error_rate)VALUES(40,'2026-01-23 05:24:05',5,118.7,18,64.2,18.4,184.5,123.0,246.0,9592,420,0.32);

INSERT INTO performance_metric_samples(test_result_id,timestamp,elapsed_seconds,rps,active_users,avg_response_time,min_response_time,max_response_time,p95_response_time,p99_response_time,request_count,failure_count,error_rate)VALUES(40,'2026-01-23 05:24:06',6,108.6,19,67.4,18.4,184.5,123.0,246.0,11191,490,1.06);

INSERT INTO performance_metric_samples(test_result_id,timestamp,elapsed_seconds,rps,active_users,avg_response_time,min_response_time,max_response_time,p95_response_time,p99_response_time,request_count,failure_count,error_rate)VALUES(40,'2026-01-23 05:24:07',7,92.9,24,64.7,18.4,184.5,123.0,246.0,12790,560,2.22);

INSERT INTO performance_test_results(id,scenario_id,project_id,user_count,spawn_rate,duration,target_url,status,started_at,finished_at,total_requests,total_failures,error_rate,rps,avg_response_time,min_response_time,max_response_time,p50_response_time,p75_response_time,p95_response_time,p99_response_time,created_at,updated_at)VALUES(41,9,8,140,3,548,'https://example.com/api','completed','2026-02-10 00:12:00','2026-02-10 00:21:08',49066,450,0.92,2309.6,367.8,110.3,1839.0,257.5,478.1,919.5,1471.2,'2026-02-10 00:12:00','2026-02-10 00:21:08')ON CONFLICT(id)DO NOTHING;

INSERT INTO performance_metric_samples(test_result_id,timestamp,elapsed_seconds,rps,active_users,avg_response_time,min_response_time,max_response_time,p95_response_time,p99_response_time,request_count,failure_count,error_rate)VALUES(41,'2026-02-10 00:12:00',0,1827.7,2,381.6,110.3,1103.4,735.6,1471.2,6133,56,1.11);

INSERT INTO performance_metric_samples(test_result_id,timestamp,elapsed_seconds,rps,active_users,avg_response_time,min_response_time,max_response_time,p95_response_time,p99_response_time,request_count,failure_count,error_rate)VALUES(41,'2026-02-10 00:12:01',1,2516.6,6,341.4,110.3,1103.4,735.6,1471.2,12266,112,0.53);

INSERT INTO performance_metric_samples(test_result_id,timestamp,elapsed_seconds,rps,active_users,avg_response_time,min_response_time,max_response_time,p95_response_time,p99_response_time,request_count,failure_count,error_rate)VALUES(41,'2026-02-10 00:12:02',2,2618.0,9,433.2,110.3,1103.4,735.6,1471.2,18399,168,0.29);

INSERT INTO performance_metric_samples(test_result_id,timestamp,elapsed_seconds,rps,active_users,avg_response_time,min_response_time,max_response_time,p95_response_time,p99_response_time,request_count,failure_count,error_rate)VALUES(41,'2026-02-10 00:12:03',3,2028.8,12,301.3,110.3,1103.4,735.6,1471.2,24533,225,1.55);

INSERT INTO performance_metric_samples(test_result_id,timestamp,elapsed_seconds,rps,active_users,avg_response_time,min_response_time,max_response_time,p95_response_time,p99_response_time,request_count,failure_count,error_rate)VALUES(41,'2026-02-10 00:12:04',4,2344.5,15,418.4,110.3,1103.4,735.6,1471.2,30666,281,1.28);

INSERT INTO performance_metric_samples(test_result_id,timestamp,elapsed_seconds,rps,active_users,avg_response_time,min_response_time,max_response_time,p95_response_time,p99_response_time,request_count,failure_count,error_rate)VALUES(41,'2026-02-10 00:12:05',5,2064.0,18,405.7,110.3,1103.4,735.6,1471.2,36799,337,2.86);

INSERT INTO performance_metric_samples(test_result_id,timestamp,elapsed_seconds,rps,active_users,avg_response_time,min_response_time,max_response_time,p95_response_time,p99_response_time,request_count,failure_count,error_rate)VALUES(41,'2026-02-10 00:12:06',6,1674.8,21,424.1,110.3,1103.4,735.6,1471.2,42932,393,2.19);

INSERT INTO performance_metric_samples(test_result_id,timestamp,elapsed_seconds,rps,active_users,avg_response_time,min_response_time,max_response_time,p95_response_time,p99_response_time,request_count,failure_count,error_rate)VALUES(41,'2026-02-10 00:12:07',7,2213.3,24,378.9,110.3,1103.4,735.6,1471.2,49066,450,1.85);

INSERT INTO performance_test_results(id,scenario_id,project_id,user_count,spawn_rate,duration,target_url,status,started_at,finished_at,total_requests,total_failures,error_rate,rps,avg_response_time,min_response_time,max_response_time,p50_response_time,p75_response_time,p95_response_time,p99_response_time,created_at,updated_at)VALUES(42,10,13,76,20,181,'https://example.com/api','completed','2026-03-05 00:50:00','2026-03-05 00:53:01',18946,460,2.43,709.7,80.2,24.1,401.0,56.1,104.3,200.5,320.8,'2026-03-05 00:50:00','2026-03-05 00:53:01')ON CONFLICT(id)DO NOTHING;

INSERT INTO performance_metric_samples(test_result_id,timestamp,elapsed_seconds,rps,active_users,avg_response_time,min_response_time,max_response_time,p95_response_time,p99_response_time,request_count,failure_count,error_rate)VALUES(42,'2026-03-05 00:50:00',0,817.6,3,85.5,24.1,240.6,160.4,320.8,2368,57,0.42);

INSERT INTO performance_metric_samples(test_result_id,timestamp,elapsed_seconds,rps,active_users,avg_response_time,min_response_time,max_response_time,p95_response_time,p99_response_time,request_count,failure_count,error_rate)VALUES(42,'2026-03-05 00:50:01',1,584.9,6,88.4,24.1,240.6,160.4,320.8,4736,115,0.08);

INSERT INTO performance_metric_samples(test_result_id,timestamp,elapsed_seconds,rps,active_users,avg_response_time,min_response_time,max_response_time,p95_response_time,p99_response_time,request_count,failure_count,error_rate)VALUES(42,'2026-03-05 00:50:02',2,881.1,9,81.4,24.1,240.6,160.4,320.8,7104,172,0.59);

INSERT INTO performance_metric_samples(test_result_id,timestamp,elapsed_seconds,rps,active_users,avg_response_time,min_response_time,max_response_time,p95_response_time,p99_response_time,request_count,failure_count,error_rate)VALUES(42,'2026-03-05 00:50:03',3,704.7,7,76.0,24.1,240.6,160.4,320.8,9473,230,0.85);

INSERT INTO performance_metric_samples(test_result_id,timestamp,elapsed_seconds,rps,active_users,avg_response_time,min_response_time,max_response_time,p95_response_time,p99_response_time,request_count,failure_count,error_rate)VALUES(42,'2026-03-05 00:50:04',4,900.4,15,87.6,24.1,240.6,160.4,320.8,11841,287,1.56);

INSERT INTO performance_metric_samples(test_result_id,timestamp,elapsed_seconds,rps,active_users,avg_response_time,min_response_time,max_response_time,p95_response_time,p99_response_time,request_count,failure_count,error_rate)VALUES(42,'2026-03-05 00:50:05',5,850.7,18,93.6,24.1,240.6,160.4,320.8,14209,345,2.15);

INSERT INTO performance_metric_samples(test_result_id,timestamp,elapsed_seconds,rps,active_users,avg_response_time,min_response_time,max_response_time,p95_response_time,p99_response_time,request_count,failure_count,error_rate)VALUES(42,'2026-03-05 00:50:06',6,888.2,21,78.4,24.1,240.6,160.4,320.8,16577,402,1.3);

INSERT INTO performance_metric_samples(test_result_id,timestamp,elapsed_seconds,rps,active_users,avg_response_time,min_response_time,max_response_time,p95_response_time,p99_response_time,request_count,failure_count,error_rate)VALUES(42,'2026-03-05 00:50:07',7,608.8,24,96.0,24.1,240.6,160.4,320.8,18946,460,2.19);

INSERT INTO performance_test_results(id,scenario_id,project_id,user_count,spawn_rate,duration,target_url,status,started_at,finished_at,total_requests,total_failures,error_rate,rps,avg_response_time,min_response_time,max_response_time,p50_response_time,p75_response_time,p95_response_time,p99_response_time,created_at,updated_at)VALUES(43,10,13,126,17,140,'https://example.com/api','completed','2026-05-02 22:09:00','2026-05-02 22:11:20',48668,180,0.37,512.3,144.1,43.2,720.5,100.9,187.3,360.2,576.4,'2026-05-02 22:09:00','2026-05-02 22:11:20')ON CONFLICT(id)DO NOTHING;

INSERT INTO performance_metric_samples(test_result_id,timestamp,elapsed_seconds,rps,active_users,avg_response_time,min_response_time,max_response_time,p95_response_time,p99_response_time,request_count,failure_count,error_rate)VALUES(43,'2026-05-02 22:09:00',0,565.2,3,156.0,43.2,432.3,288.2,576.4,6083,22,0.94);

INSERT INTO performance_metric_samples(test_result_id,timestamp,elapsed_seconds,rps,active_users,avg_response_time,min_response_time,max_response_time,p95_response_time,p99_response_time,request_count,failure_count,error_rate)VALUES(43,'2026-05-02 22:09:01',1,642.9,6,121.1,43.2,432.3,288.2,576.4,12167,45,2.12);

INSERT INTO performance_metric_samples(test_result_id,timestamp,elapsed_seconds,rps,active_users,avg_response_time,min_response_time,max_response_time,p95_response_time,p99_response_time,request_count,failure_count,error_rate)VALUES(43,'2026-05-02 22:09:02',2,518.8,9,163.8,43.2,432.3,288.2,576.4,18250,67,1.98);

INSERT INTO performance_metric_samples(test_result_id,timestamp,elapsed_seconds,rps,active_users,avg_response_time,min_response_time,max_response_time,p95_response_time,p99_response_time,request_count,failure_count,error_rate)VALUES(43,'2026-05-02 22:09:03',3,628.4,10,170.0,43.2,432.3,288.2,576.4,24334,90,1.88);

INSERT INTO performance_metric_samples(test_result_id,timestamp,elapsed_seconds,rps,active_users,avg_response_time,min_response_time,max_response_time,p95_response_time,p99_response_time,request_count,failure_count,error_rate)VALUES(43,'2026-05-02 22:09:04',4,434.2,15,137.0,43.2,432.3,288.2,576.4,30417,112,2.83);

INSERT INTO performance_metric_samples(test_result_id,timestamp,elapsed_seconds,rps,active_users,avg_response_time,min_response_time,max_response_time,p95_response_time,p99_response_time,request_count,failure_count,error_rate)VALUES(43,'2026-05-02 22:09:05',5,565.6,18,142.4,43.2,432.3,288.2,576.4,36501,135,1.45);

INSERT INTO performance_metric_samples(test_result_id,timestamp,elapsed_seconds,rps,active_users,avg_response_time,min_response_time,max_response_time,p95_response_time,p99_response_time,request_count,failure_count,error_rate)VALUES(43,'2026-05-02 22:09:06',6,416.1,21,131.6,43.2,432.3,288.2,576.4,42584,157,0.6);

INSERT INTO performance_metric_samples(test_result_id,timestamp,elapsed_seconds,rps,active_users,avg_response_time,min_response_time,max_response_time,p95_response_time,p99_response_time,request_count,failure_count,error_rate)VALUES(43,'2026-05-02 22:09:07',7,627.8,24,164.7,43.2,432.3,288.2,576.4,48668,180,2.25);

INSERT INTO performance_test_results(id,scenario_id,project_id,user_count,spawn_rate,duration,target_url,status,started_at,finished_at,total_requests,total_failures,error_rate,rps,avg_response_time,min_response_time,max_response_time,p50_response_time,p75_response_time,p95_response_time,p99_response_time,created_at,updated_at)VALUES(44,10,13,107,19,562,'https://example.com/api','completed','2026-05-31 20:56:00','2026-05-31 21:05:22',47529,423,0.89,1283.6,116.3,34.9,581.5,81.4,151.2,290.8,465.2,'2026-05-31 20:56:00','2026-05-31 21:05:22')ON CONFLICT(id)DO NOTHING;

INSERT INTO performance_metric_samples(test_result_id,timestamp,elapsed_seconds,rps,active_users,avg_response_time,min_response_time,max_response_time,p95_response_time,p99_response_time,request_count,failure_count,error_rate)VALUES(44,'2026-05-31 20:56:00',0,1079.3,3,115.6,34.9,348.9,232.6,465.2,5941,52,1.97);

INSERT INTO performance_metric_samples(test_result_id,timestamp,elapsed_seconds,rps,active_users,avg_response_time,min_response_time,max_response_time,p95_response_time,p99_response_time,request_count,failure_count,error_rate)VALUES(44,'2026-05-31 20:56:01',1,1037.2,6,132.1,34.9,348.9,232.6,465.2,11882,105,2.63);

INSERT INTO performance_metric_samples(test_result_id,timestamp,elapsed_seconds,rps,active_users,avg_response_time,min_response_time,max_response_time,p95_response_time,p99_response_time,request_count,failure_count,error_rate)VALUES(44,'2026-05-31 20:56:02',2,1413.0,9,130.1,34.9,348.9,232.6,465.2,17823,158,1.18);

INSERT INTO performance_metric_samples(test_result_id,timestamp,elapsed_seconds,rps,active_users,avg_response_time,min_response_time,max_response_time,p95_response_time,p99_response_time,request_count,failure_count,error_rate)VALUES(44,'2026-05-31 20:56:03',3,1173.6,12,106.8,34.9,348.9,232.6,465.2,23764,211,0.66);

INSERT INTO performance_metric_samples(test_result_id,timestamp,elapsed_seconds,rps,active_users,avg_response_time,min_response_time,max_response_time,p95_response_time,p99_response_time,request_count,failure_count,error_rate)VALUES(44,'2026-05-31 20:56:04',4,1640.1,15,128.6,34.9,348.9,232.6,465.2,29705,264,1.26);

INSERT INTO performance_metric_samples(test_result_id,timestamp,elapsed_seconds,rps,active_users,avg_response_time,min_response_time,max_response_time,p95_response_time,p99_response_time,request_count,failure_count,error_rate)VALUES(44,'2026-05-31 20:56:05',5,1242.9,18,123.9,34.9,348.9,232.6,465.2,35646,317,0.35);

INSERT INTO performance_metric_samples(test_result_id,timestamp,elapsed_seconds,rps,active_users,avg_response_time,min_response_time,max_response_time,p95_response_time,p99_response_time,request_count,failure_count,error_rate)VALUES(44,'2026-05-31 20:56:06',6,1256.4,21,123.8,34.9,348.9,232.6,465.2,41587,370,1.04);

INSERT INTO performance_metric_samples(test_result_id,timestamp,elapsed_seconds,rps,active_users,avg_response_time,min_response_time,max_response_time,p95_response_time,p99_response_time,request_count,failure_count,error_rate)VALUES(44,'2026-05-31 20:56:07',7,1205.1,24,129.0,34.9,348.9,232.6,465.2,47529,423,1.45);

INSERT INTO performance_test_results(id,scenario_id,project_id,user_count,spawn_rate,duration,target_url,status,started_at,finished_at,total_requests,total_failures,error_rate,rps,avg_response_time,min_response_time,max_response_time,p50_response_time,p75_response_time,p95_response_time,p99_response_time,created_at,updated_at)VALUES(45,11,13,25,18,89,'https://example.com/api','completed','2026-02-15 12:45:00','2026-02-15 12:46:29',18558,470,2.53,2674.9,316.4,94.9,1582.0,221.5,411.3,791.0,1265.6,'2026-02-15 12:45:00','2026-02-15 12:46:29')ON CONFLICT(id)DO NOTHING;

INSERT INTO performance_metric_samples(test_result_id,timestamp,elapsed_seconds,rps,active_users,avg_response_time,min_response_time,max_response_time,p95_response_time,p99_response_time,request_count,failure_count,error_rate)VALUES(45,'2026-02-15 12:45:00',0,3111.1,3,338.5,94.9,949.2,632.8,1265.6,2319,58,1.23);

INSERT INTO performance_metric_samples(test_result_id,timestamp,elapsed_seconds,rps,active_users,avg_response_time,min_response_time,max_response_time,p95_response_time,p99_response_time,request_count,failure_count,error_rate)VALUES(45,'2026-02-15 12:45:01',1,3170.9,6,303.6,94.9,949.2,632.8,1265.6,4639,117,2.74);

INSERT INTO performance_metric_samples(test_result_id,timestamp,elapsed_seconds,rps,active_users,avg_response_time,min_response_time,max_response_time,p95_response_time,p99_response_time,request_count,failure_count,error_rate)VALUES(45,'2026-02-15 12:45:02',2,2303.1,9,280.8,94.9,949.2,632.8,1265.6,6959,176,1.91);

INSERT INTO performance_metric_samples(test_result_id,timestamp,elapsed_seconds,rps,active_users,avg_response_time,min_response_time,max_response_time,p95_response_time,p99_response_time,request_count,failure_count,error_rate)VALUES(45,'2026-02-15 12:45:03',3,1945.7,12,305.0,94.9,949.2,632.8,1265.6,9279,235,1.72);

INSERT INTO performance_metric_samples(test_result_id,timestamp,elapsed_seconds,rps,active_users,avg_response_time,min_response_time,max_response_time,p95_response_time,p99_response_time,request_count,failure_count,error_rate)VALUES(45,'2026-02-15 12:45:04',4,2139.7,15,351.8,94.9,949.2,632.8,1265.6,11598,293,0.33);

INSERT INTO performance_metric_samples(test_result_id,timestamp,elapsed_seconds,rps,active_users,avg_response_time,min_response_time,max_response_time,p95_response_time,p99_response_time,request_count,failure_count,error_rate)VALUES(45,'2026-02-15 12:45:05',5,3426.4,18,294.8,94.9,949.2,632.8,1265.6,13918,352,1.81);

INSERT INTO performance_metric_samples(test_result_id,timestamp,elapsed_seconds,rps,active_users,avg_response_time,min_response_time,max_response_time,p95_response_time,p99_response_time,request_count,failure_count,error_rate)VALUES(45,'2026-02-15 12:45:06',6,1904.4,21,255.8,94.9,949.2,632.8,1265.6,16238,411,1.14);

INSERT INTO performance_metric_samples(test_result_id,timestamp,elapsed_seconds,rps,active_users,avg_response_time,min_response_time,max_response_time,p95_response_time,p99_response_time,request_count,failure_count,error_rate)VALUES(45,'2026-02-15 12:45:07',7,3125.0,24,368.6,94.9,949.2,632.8,1265.6,18558,470,2.3);

INSERT INTO performance_test_results(id,scenario_id,project_id,user_count,spawn_rate,duration,target_url,status,started_at,finished_at,total_requests,total_failures,error_rate,rps,avg_response_time,min_response_time,max_response_time,p50_response_time,p75_response_time,p95_response_time,p99_response_time,created_at,updated_at)VALUES(46,11,13,111,8,110,'https://example.com/api','completed','2026-01-11 07:19:00','2026-01-11 07:20:50',24730,662,2.68,2956.4,337.7,101.3,1688.5,236.4,439.0,844.2,1350.8,'2026-01-11 07:19:00','2026-01-11 07:20:50')ON CONFLICT(id)DO NOTHING;

INSERT INTO performance_metric_samples(test_result_id,timestamp,elapsed_seconds,rps,active_users,avg_response_time,min_response_time,max_response_time,p95_response_time,p99_response_time,request_count,failure_count,error_rate)VALUES(46,'2026-01-11 07:19:00',0,2584.2,3,393.2,101.3,1013.1,675.4,1350.8,3091,82,0.99);

INSERT INTO performance_metric_samples(test_result_id,timestamp,elapsed_seconds,rps,active_users,avg_response_time,min_response_time,max_response_time,p95_response_time,p99_response_time,request_count,failure_count,error_rate)VALUES(46,'2026-01-11 07:19:01',1,2451.9,6,303.8,101.3,1013.1,675.4,1350.8,6182,165,0.04);

INSERT INTO performance_metric_samples(test_result_id,timestamp,elapsed_seconds,rps,active_users,avg_response_time,min_response_time,max_response_time,p95_response_time,p99_response_time,request_count,failure_count,error_rate)VALUES(46,'2026-01-11 07:19:02',2,3569.2,9,397.2,101.3,1013.1,675.4,1350.8,9273,248,0.31);

INSERT INTO performance_metric_samples(test_result_id,timestamp,elapsed_seconds,rps,active_users,avg_response_time,min_response_time,max_response_time,p95_response_time,p99_response_time,request_count,failure_count,error_rate)VALUES(46,'2026-01-11 07:19:03',3,2775.4,12,275.9,101.3,1013.1,675.4,1350.8,12365,331,0.85);

INSERT INTO performance_metric_samples(test_result_id,timestamp,elapsed_seconds,rps,active_users,avg_response_time,min_response_time,max_response_time,p95_response_time,p99_response_time,request_count,failure_count,error_rate)VALUES(46,'2026-01-11 07:19:04',4,2112.5,15,374.5,101.3,1013.1,675.4,1350.8,15456,413,0.74);

INSERT INTO performance_metric_samples(test_result_id,timestamp,elapsed_seconds,rps,active_users,avg_response_time,min_response_time,max_response_time,p95_response_time,p99_response_time,request_count,failure_count,error_rate)VALUES(46,'2026-01-11 07:19:05',5,2552.8,18,380.0,101.3,1013.1,675.4,1350.8,18547,496,1.13);

INSERT INTO performance_metric_samples(test_result_id,timestamp,elapsed_seconds,rps,active_users,avg_response_time,min_response_time,max_response_time,p95_response_time,p99_response_time,request_count,failure_count,error_rate)VALUES(46,'2026-01-11 07:19:06',6,2780.3,21,388.6,101.3,1013.1,675.4,1350.8,21638,579,2.59);

INSERT INTO performance_metric_samples(test_result_id,timestamp,elapsed_seconds,rps,active_users,avg_response_time,min_response_time,max_response_time,p95_response_time,p99_response_time,request_count,failure_count,error_rate)VALUES(46,'2026-01-11 07:19:07',7,2205.2,24,367.7,101.3,1013.1,675.4,1350.8,24730,662,2.29);

INSERT INTO performance_test_results(id,scenario_id,project_id,user_count,spawn_rate,duration,target_url,status,started_at,finished_at,total_requests,total_failures,error_rate,rps,avg_response_time,min_response_time,max_response_time,p50_response_time,p75_response_time,p95_response_time,p99_response_time,created_at,updated_at)VALUES(47,11,13,89,11,215,'https://example.com/api','completed','2026-02-15 10:00:00','2026-02-15 10:03:35',49226,1447,2.94,1203.8,335.1,100.5,1675.5,234.6,435.6,837.8,1340.4,'2026-02-15 10:00:00','2026-02-15 10:03:35')ON CONFLICT(id)DO NOTHING;

INSERT INTO performance_metric_samples(test_result_id,timestamp,elapsed_seconds,rps,active_users,avg_response_time,min_response_time,max_response_time,p95_response_time,p99_response_time,request_count,failure_count,error_rate)VALUES(47,'2026-02-15 10:00:00',0,1149.7,3,271.2,100.5,1005.3,670.2,1340.4,6153,180,0.82);

INSERT INTO performance_metric_samples(test_result_id,timestamp,elapsed_seconds,rps,active_users,avg_response_time,min_response_time,max_response_time,p95_response_time,p99_response_time,request_count,failure_count,error_rate)VALUES(47,'2026-02-15 10:00:01',1,989.0,6,398.0,100.5,1005.3,670.2,1340.4,12306,361,1.73);

INSERT INTO performance_metric_samples(test_result_id,timestamp,elapsed_seconds,rps,active_users,avg_response_time,min_response_time,max_response_time,p95_response_time,p99_response_time,request_count,failure_count,error_rate)VALUES(47,'2026-02-15 10:00:02',2,1114.7,9,280.6,100.5,1005.3,670.2,1340.4,18459,542,2.9);

INSERT INTO performance_metric_samples(test_result_id,timestamp,elapsed_seconds,rps,active_users,avg_response_time,min_response_time,max_response_time,p95_response_time,p99_response_time,request_count,failure_count,error_rate)VALUES(47,'2026-02-15 10:00:03',3,1247.9,12,306.2,100.5,1005.3,670.2,1340.4,24613,723,2.11);

INSERT INTO performance_metric_samples(test_result_id,timestamp,elapsed_seconds,rps,active_users,avg_response_time,min_response_time,max_response_time,p95_response_time,p99_response_time,request_count,failure_count,error_rate)VALUES(47,'2026-02-15 10:00:04',4,1208.6,15,270.4,100.5,1005.3,670.2,1340.4,30766,904,1.49);

INSERT INTO performance_metric_samples(test_result_id,timestamp,elapsed_seconds,rps,active_users,avg_response_time,min_response_time,max_response_time,p95_response_time,p99_response_time,request_count,failure_count,error_rate)VALUES(47,'2026-02-15 10:00:05',5,1127.0,18,370.3,100.5,1005.3,670.2,1340.4,36919,1085,2.14);

INSERT INTO performance_metric_samples(test_result_id,timestamp,elapsed_seconds,rps,active_users,avg_response_time,min_response_time,max_response_time,p95_response_time,p99_response_time,request_count,failure_count,error_rate)VALUES(47,'2026-02-15 10:00:06',6,1169.3,21,398.8,100.5,1005.3,670.2,1340.4,43072,1266,1.19);

INSERT INTO performance_metric_samples(test_result_id,timestamp,elapsed_seconds,rps,active_users,avg_response_time,min_response_time,max_response_time,p95_response_time,p99_response_time,request_count,failure_count,error_rate)VALUES(47,'2026-02-15 10:00:07',7,1010.3,24,332.0,100.5,1005.3,670.2,1340.4,49226,1447,0.33);

INSERT INTO performance_test_results(id,scenario_id,project_id,user_count,spawn_rate,duration,target_url,status,started_at,finished_at,total_requests,total_failures,error_rate,rps,avg_response_time,min_response_time,max_response_time,p50_response_time,p75_response_time,p95_response_time,p99_response_time,created_at,updated_at)VALUES(48,11,13,73,3,145,'https://example.com/api','completed','2026-03-13 23:51:00','2026-03-13 23:53:25',37758,319,0.84,2601.2,203.6,61.1,1018.0,142.5,264.7,509.0,814.4,'2026-03-13 23:51:00','2026-03-13 23:53:25')ON CONFLICT(id)DO NOTHING;

INSERT INTO performance_metric_samples(test_result_id,timestamp,elapsed_seconds,rps,active_users,avg_response_time,min_response_time,max_response_time,p95_response_time,p99_response_time,request_count,failure_count,error_rate)VALUES(48,'2026-03-13 23:51:00',0,2041.4,3,231.1,61.1,610.8,407.2,814.4,4719,39,1.57);

INSERT INTO performance_metric_samples(test_result_id,timestamp,elapsed_seconds,rps,active_users,avg_response_time,min_response_time,max_response_time,p95_response_time,p99_response_time,request_count,failure_count,error_rate)VALUES(48,'2026-03-13 23:51:01',1,3131.3,6,181.8,61.1,610.8,407.2,814.4,9439,79,2.3);

INSERT INTO performance_metric_samples(test_result_id,timestamp,elapsed_seconds,rps,active_users,avg_response_time,min_response_time,max_response_time,p95_response_time,p99_response_time,request_count,failure_count,error_rate)VALUES(48,'2026-03-13 23:51:02',2,2214.2,9,223.2,61.1,610.8,407.2,814.4,14159,119,2.5);

INSERT INTO performance_metric_samples(test_result_id,timestamp,elapsed_seconds,rps,active_users,avg_response_time,min_response_time,max_response_time,p95_response_time,p99_response_time,request_count,failure_count,error_rate)VALUES(48,'2026-03-13 23:51:03',3,1877.8,12,208.9,61.1,610.8,407.2,814.4,18879,159,1.22);

INSERT INTO performance_metric_samples(test_result_id,timestamp,elapsed_seconds,rps,active_users,avg_response_time,min_response_time,max_response_time,p95_response_time,p99_response_time,request_count,failure_count,error_rate)VALUES(48,'2026-03-13 23:51:04',4,1829.5,15,179.9,61.1,610.8,407.2,814.4,23598,199,1.69);

INSERT INTO performance_metric_samples(test_result_id,timestamp,elapsed_seconds,rps,active_users,avg_response_time,min_response_time,max_response_time,p95_response_time,p99_response_time,request_count,failure_count,error_rate)VALUES(48,'2026-03-13 23:51:05',5,2583.6,18,188.4,61.1,610.8,407.2,814.4,28318,239,1.96);

INSERT INTO performance_metric_samples(test_result_id,timestamp,elapsed_seconds,rps,active_users,avg_response_time,min_response_time,max_response_time,p95_response_time,p99_response_time,request_count,failure_count,error_rate)VALUES(48,'2026-03-13 23:51:06',6,2323.1,21,202.2,61.1,610.8,407.2,814.4,33038,279,1.66);

INSERT INTO performance_metric_samples(test_result_id,timestamp,elapsed_seconds,rps,active_users,avg_response_time,min_response_time,max_response_time,p95_response_time,p99_response_time,request_count,failure_count,error_rate)VALUES(48,'2026-03-13 23:51:07',7,2975.3,24,169.5,61.1,610.8,407.2,814.4,37758,319,0.32);

INSERT INTO performance_test_results(id,scenario_id,project_id,user_count,spawn_rate,duration,target_url,status,started_at,finished_at,total_requests,total_failures,error_rate,rps,avg_response_time,min_response_time,max_response_time,p50_response_time,p75_response_time,p95_response_time,p99_response_time,created_at,updated_at)VALUES(49,11,13,39,2,73,'https://example.com/api','completed','2026-05-12 21:52:00','2026-05-12 21:53:13',35074,1312,3.74,540.3,183.5,55.0,917.5,128.4,238.6,458.8,734.0,'2026-05-12 21:52:00','2026-05-12 21:53:13')ON CONFLICT(id)DO NOTHING;

INSERT INTO performance_metric_samples(test_result_id,timestamp,elapsed_seconds,rps,active_users,avg_response_time,min_response_time,max_response_time,p95_response_time,p99_response_time,request_count,failure_count,error_rate)VALUES(49,'2026-05-12 21:52:00',0,665.3,3,159.3,55.0,550.5,367.0,734.0,4384,164,2.41);

INSERT INTO performance_metric_samples(test_result_id,timestamp,elapsed_seconds,rps,active_users,avg_response_time,min_response_time,max_response_time,p95_response_time,p99_response_time,request_count,failure_count,error_rate)VALUES(49,'2026-05-12 21:52:01',1,536.1,6,211.0,55.0,550.5,367.0,734.0,8768,328,1.25);

INSERT INTO performance_metric_samples(test_result_id,timestamp,elapsed_seconds,rps,active_users,avg_response_time,min_response_time,max_response_time,p95_response_time,p99_response_time,request_count,failure_count,error_rate)VALUES(49,'2026-05-12 21:52:02',2,381.2,9,178.8,55.0,550.5,367.0,734.0,13152,492,0.88);

INSERT INTO performance_metric_samples(test_result_id,timestamp,elapsed_seconds,rps,active_users,avg_response_time,min_response_time,max_response_time,p95_response_time,p99_response_time,request_count,failure_count,error_rate)VALUES(49,'2026-05-12 21:52:03',3,677.1,12,166.7,55.0,550.5,367.0,734.0,17537,656,0.97);

INSERT INTO performance_metric_samples(test_result_id,timestamp,elapsed_seconds,rps,active_users,avg_response_time,min_response_time,max_response_time,p95_response_time,p99_response_time,request_count,failure_count,error_rate)VALUES(49,'2026-05-12 21:52:04',4,666.6,15,194.5,55.0,550.5,367.0,734.0,21921,820,0.42);

INSERT INTO performance_metric_samples(test_result_id,timestamp,elapsed_seconds,rps,active_users,avg_response_time,min_response_time,max_response_time,p95_response_time,p99_response_time,request_count,failure_count,error_rate)VALUES(49,'2026-05-12 21:52:05',5,547.8,18,205.7,55.0,550.5,367.0,734.0,26305,984,2.86);

INSERT INTO performance_metric_samples(test_result_id,timestamp,elapsed_seconds,rps,active_users,avg_response_time,min_response_time,max_response_time,p95_response_time,p99_response_time,request_count,failure_count,error_rate)VALUES(49,'2026-05-12 21:52:06',6,498.6,21,165.2,55.0,550.5,367.0,734.0,30689,1148,1.39);

INSERT INTO performance_metric_samples(test_result_id,timestamp,elapsed_seconds,rps,active_users,avg_response_time,min_response_time,max_response_time,p95_response_time,p99_response_time,request_count,failure_count,error_rate)VALUES(49,'2026-05-12 21:52:07',7,681.7,24,199.7,55.0,550.5,367.0,734.0,35074,1312,2.56);

INSERT INTO performance_test_results(id,scenario_id,project_id,user_count,spawn_rate,duration,target_url,status,started_at,finished_at,total_requests,total_failures,error_rate,rps,avg_response_time,min_response_time,max_response_time,p50_response_time,p75_response_time,p95_response_time,p99_response_time,created_at,updated_at)VALUES(50,11,13,11,10,545,'https://example.com/api','completed','2026-04-28 04:27:00','2026-04-28 04:36:05',21820,454,2.08,493.5,40.8,12.2,204.0,28.6,53.0,102.0,163.2,'2026-04-28 04:27:00','2026-04-28 04:36:05')ON CONFLICT(id)DO NOTHING;

INSERT INTO performance_metric_samples(test_result_id,timestamp,elapsed_seconds,rps,active_users,avg_response_time,min_response_time,max_response_time,p95_response_time,p99_response_time,request_count,failure_count,error_rate)VALUES(50,'2026-04-28 04:27:00',0,553.2,3,44.0,12.2,122.4,81.6,163.2,2727,56,1.61);

INSERT INTO performance_metric_samples(test_result_id,timestamp,elapsed_seconds,rps,active_users,avg_response_time,min_response_time,max_response_time,p95_response_time,p99_response_time,request_count,failure_count,error_rate)VALUES(50,'2026-04-28 04:27:01',1,443.5,6,42.8,12.2,122.4,81.6,163.2,5455,113,1.78);

INSERT INTO performance_metric_samples(test_result_id,timestamp,elapsed_seconds,rps,active_users,avg_response_time,min_response_time,max_response_time,p95_response_time,p99_response_time,request_count,failure_count,error_rate)VALUES(50,'2026-04-28 04:27:02',2,365.2,9,41.8,12.2,122.4,81.6,163.2,8182,170,0.68);

INSERT INTO performance_metric_samples(test_result_id,timestamp,elapsed_seconds,rps,active_users,avg_response_time,min_response_time,max_response_time,p95_response_time,p99_response_time,request_count,failure_count,error_rate)VALUES(50,'2026-04-28 04:27:03',3,531.6,12,37.1,12.2,122.4,81.6,163.2,10910,227,2.46);

INSERT INTO performance_metric_samples(test_result_id,timestamp,elapsed_seconds,rps,active_users,avg_response_time,min_response_time,max_response_time,p95_response_time,p99_response_time,request_count,failure_count,error_rate)VALUES(50,'2026-04-28 04:27:04',4,602.5,15,44.5,12.2,122.4,81.6,163.2,13637,283,1.1);

INSERT INTO performance_metric_samples(test_result_id,timestamp,elapsed_seconds,rps,active_users,avg_response_time,min_response_time,max_response_time,p95_response_time,p99_response_time,request_count,failure_count,error_rate)VALUES(50,'2026-04-28 04:27:05',5,572.6,18,41.8,12.2,122.4,81.6,163.2,16365,340,1.92);

INSERT INTO performance_metric_samples(test_result_id,timestamp,elapsed_seconds,rps,active_users,avg_response_time,min_response_time,max_response_time,p95_response_time,p99_response_time,request_count,failure_count,error_rate)VALUES(50,'2026-04-28 04:27:06',6,405.4,21,35.1,12.2,122.4,81.6,163.2,19092,397,2.19);

INSERT INTO performance_metric_samples(test_result_id,timestamp,elapsed_seconds,rps,active_users,avg_response_time,min_response_time,max_response_time,p95_response_time,p99_response_time,request_count,failure_count,error_rate)VALUES(50,'2026-04-28 04:27:07',7,428.4,24,41.8,12.2,122.4,81.6,163.2,21820,454,0.38);

INSERT INTO performance_test_results(id,scenario_id,project_id,user_count,spawn_rate,duration,target_url,status,started_at,finished_at,total_requests,total_failures,error_rate,rps,avg_response_time,min_response_time,max_response_time,p50_response_time,p75_response_time,p95_response_time,p99_response_time,created_at,updated_at)VALUES(51,12,13,33,20,343,'https://example.com/api','failed','2026-03-08 15:11:00','2026-03-08 15:16:43',14717,123,0.84,2360.9,395.8,118.7,1979.0,277.1,514.5,989.5,1583.2,'2026-03-08 15:11:00','2026-03-08 15:16:43')ON CONFLICT(id)DO NOTHING;

INSERT INTO performance_metric_samples(test_result_id,timestamp,elapsed_seconds,rps,active_users,avg_response_time,min_response_time,max_response_time,p95_response_time,p99_response_time,request_count,failure_count,error_rate)VALUES(51,'2026-03-08 15:11:00',0,1860.1,3,391.9,118.7,1187.4,791.6,1583.2,1839,15,0.0);

INSERT INTO performance_metric_samples(test_result_id,timestamp,elapsed_seconds,rps,active_users,avg_response_time,min_response_time,max_response_time,p95_response_time,p99_response_time,request_count,failure_count,error_rate)VALUES(51,'2026-03-08 15:11:01',1,1762.8,6,338.3,118.7,1187.4,791.6,1583.2,3679,30,2.42);

INSERT INTO performance_metric_samples(test_result_id,timestamp,elapsed_seconds,rps,active_users,avg_response_time,min_response_time,max_response_time,p95_response_time,p99_response_time,request_count,failure_count,error_rate)VALUES(51,'2026-03-08 15:11:02',2,2255.2,9,368.4,118.7,1187.4,791.6,1583.2,5518,46,1.5);

INSERT INTO performance_metric_samples(test_result_id,timestamp,elapsed_seconds,rps,active_users,avg_response_time,min_response_time,max_response_time,p95_response_time,p99_response_time,request_count,failure_count,error_rate)VALUES(51,'2026-03-08 15:11:03',3,1818.8,12,378.9,118.7,1187.4,791.6,1583.2,7358,61,2.32);

INSERT INTO performance_metric_samples(test_result_id,timestamp,elapsed_seconds,rps,active_users,avg_response_time,min_response_time,max_response_time,p95_response_time,p99_response_time,request_count,failure_count,error_rate)VALUES(51,'2026-03-08 15:11:04',4,2653.1,15,366.0,118.7,1187.4,791.6,1583.2,9198,76,1.57);

INSERT INTO performance_metric_samples(test_result_id,timestamp,elapsed_seconds,rps,active_users,avg_response_time,min_response_time,max_response_time,p95_response_time,p99_response_time,request_count,failure_count,error_rate)VALUES(51,'2026-03-08 15:11:05',5,2404.4,18,450.0,118.7,1187.4,791.6,1583.2,11037,92,2.87);

INSERT INTO performance_metric_samples(test_result_id,timestamp,elapsed_seconds,rps,active_users,avg_response_time,min_response_time,max_response_time,p95_response_time,p99_response_time,request_count,failure_count,error_rate)VALUES(51,'2026-03-08 15:11:06',6,2992.0,21,429.3,118.7,1187.4,791.6,1583.2,12877,107,2.52);

INSERT INTO performance_metric_samples(test_result_id,timestamp,elapsed_seconds,rps,active_users,avg_response_time,min_response_time,max_response_time,p95_response_time,p99_response_time,request_count,failure_count,error_rate)VALUES(51,'2026-03-08 15:11:07',7,2446.6,24,426.7,118.7,1187.4,791.6,1583.2,14717,123,0.75);

INSERT INTO performance_test_results(id,scenario_id,project_id,user_count,spawn_rate,duration,target_url,status,started_at,finished_at,total_requests,total_failures,error_rate,rps,avg_response_time,min_response_time,max_response_time,p50_response_time,p75_response_time,p95_response_time,p99_response_time,created_at,updated_at)VALUES(52,12,13,181,12,505,'https://example.com/api','completed','2026-05-01 16:03:00','2026-05-01 16:11:25',12666,16,0.13,1128.8,194.4,58.3,972.0,136.1,252.7,486.0,777.6,'2026-05-01 16:03:00','2026-05-01 16:11:25')ON CONFLICT(id)DO NOTHING;

INSERT INTO performance_metric_samples(test_result_id,timestamp,elapsed_seconds,rps,active_users,avg_response_time,min_response_time,max_response_time,p95_response_time,p99_response_time,request_count,failure_count,error_rate)VALUES(52,'2026-05-01 16:03:00',0,1283.6,3,203.5,58.3,583.2,388.8,777.6,1583,2,2.63);

INSERT INTO performance_metric_samples(test_result_id,timestamp,elapsed_seconds,rps,active_users,avg_response_time,min_response_time,max_response_time,p95_response_time,p99_response_time,request_count,failure_count,error_rate)VALUES(52,'2026-05-01 16:03:01',1,1413.7,6,185.3,58.3,583.2,388.8,777.6,3166,4,0.54);

INSERT INTO performance_metric_samples(test_result_id,timestamp,elapsed_seconds,rps,active_users,avg_response_time,min_response_time,max_response_time,p95_response_time,p99_response_time,request_count,failure_count,error_rate)VALUES(52,'2026-05-01 16:03:02',2,1296.5,3,170.7,58.3,583.2,388.8,777.6,4749,6,1.08);

INSERT INTO performance_metric_samples(test_result_id,timestamp,elapsed_seconds,rps,active_users,avg_response_time,min_response_time,max_response_time,p95_response_time,p99_response_time,request_count,failure_count,error_rate)VALUES(52,'2026-05-01 16:03:03',3,922.2,12,179.7,58.3,583.2,388.8,777.6,6333,8,0.28);

INSERT INTO performance_metric_samples(test_result_id,timestamp,elapsed_seconds,rps,active_users,avg_response_time,min_response_time,max_response_time,p95_response_time,p99_response_time,request_count,failure_count,error_rate)VALUES(52,'2026-05-01 16:03:04',4,1040.0,15,194.6,58.3,583.2,388.8,777.6,7916,10,0.04);

INSERT INTO performance_metric_samples(test_result_id,timestamp,elapsed_seconds,rps,active_users,avg_response_time,min_response_time,max_response_time,p95_response_time,p99_response_time,request_count,failure_count,error_rate)VALUES(52,'2026-05-01 16:03:05',5,975.1,18,176.9,58.3,583.2,388.8,777.6,9499,12,1.44);

INSERT INTO performance_metric_samples(test_result_id,timestamp,elapsed_seconds,rps,active_users,avg_response_time,min_response_time,max_response_time,p95_response_time,p99_response_time,request_count,failure_count,error_rate)VALUES(52,'2026-05-01 16:03:06',6,819.9,21,210.3,58.3,583.2,388.8,777.6,11082,14,0.82);

INSERT INTO performance_metric_samples(test_result_id,timestamp,elapsed_seconds,rps,active_users,avg_response_time,min_response_time,max_response_time,p95_response_time,p99_response_time,request_count,failure_count,error_rate)VALUES(52,'2026-05-01 16:03:07',7,828.9,24,219.5,58.3,583.2,388.8,777.6,12666,16,2.59);

INSERT INTO performance_test_results(id,scenario_id,project_id,user_count,spawn_rate,duration,target_url,status,started_at,finished_at,total_requests,total_failures,error_rate,rps,avg_response_time,min_response_time,max_response_time,p50_response_time,p75_response_time,p95_response_time,p99_response_time,created_at,updated_at)VALUES(53,12,13,36,2,525,'https://example.com/api','failed','2026-01-31 14:20:00','2026-01-31 14:28:45',12388,293,2.37,2631.1,304.0,91.2,1520.0,212.8,395.2,760.0,1216.0,'2026-01-31 14:20:00','2026-01-31 14:28:45')ON CONFLICT(id)DO NOTHING;

INSERT INTO performance_metric_samples(test_result_id,timestamp,elapsed_seconds,rps,active_users,avg_response_time,min_response_time,max_response_time,p95_response_time,p99_response_time,request_count,failure_count,error_rate)VALUES(53,'2026-01-31 14:20:00',0,2425.1,3,351.9,91.2,912.0,608.0,1216.0,1548,36,0.46);

INSERT INTO performance_metric_samples(test_result_id,timestamp,elapsed_seconds,rps,active_users,avg_response_time,min_response_time,max_response_time,p95_response_time,p99_response_time,request_count,failure_count,error_rate)VALUES(53,'2026-01-31 14:20:01',1,3004.0,6,253.3,91.2,912.0,608.0,1216.0,3097,73,2.5);

INSERT INTO performance_metric_samples(test_result_id,timestamp,elapsed_seconds,rps,active_users,avg_response_time,min_response_time,max_response_time,p95_response_time,p99_response_time,request_count,failure_count,error_rate)VALUES(53,'2026-01-31 14:20:02',2,2030.3,9,320.7,91.2,912.0,608.0,1216.0,4645,109,0.19);

INSERT INTO performance_metric_samples(test_result_id,timestamp,elapsed_seconds,rps,active_users,avg_response_time,min_response_time,max_response_time,p95_response_time,p99_response_time,request_count,failure_count,error_rate)VALUES(53,'2026-01-31 14:20:03',3,1995.7,12,276.9,91.2,912.0,608.0,1216.0,6194,146,2.56);

INSERT INTO performance_metric_samples(test_result_id,timestamp,elapsed_seconds,rps,active_users,avg_response_time,min_response_time,max_response_time,p95_response_time,p99_response_time,request_count,failure_count,error_rate)VALUES(53,'2026-01-31 14:20:04',4,2876.0,15,245.2,91.2,912.0,608.0,1216.0,7742,183,2.51);

INSERT INTO performance_metric_samples(test_result_id,timestamp,elapsed_seconds,rps,active_users,avg_response_time,min_response_time,max_response_time,p95_response_time,p99_response_time,request_count,failure_count,error_rate)VALUES(53,'2026-01-31 14:20:05',5,3180.8,18,352.4,91.2,912.0,608.0,1216.0,9291,219,0.51);

INSERT INTO performance_metric_samples(test_result_id,timestamp,elapsed_seconds,rps,active_users,avg_response_time,min_response_time,max_response_time,p95_response_time,p99_response_time,request_count,failure_count,error_rate)VALUES(53,'2026-01-31 14:20:06',6,3398.8,21,358.0,91.2,912.0,608.0,1216.0,10839,256,1.55);

INSERT INTO performance_metric_samples(test_result_id,timestamp,elapsed_seconds,rps,active_users,avg_response_time,min_response_time,max_response_time,p95_response_time,p99_response_time,request_count,failure_count,error_rate)VALUES(53,'2026-01-31 14:20:07',7,3326.6,24,293.8,91.2,912.0,608.0,1216.0,12388,293,2.0);

INSERT INTO performance_test_results(id,scenario_id,project_id,user_count,spawn_rate,duration,target_url,status,started_at,finished_at,total_requests,total_failures,error_rate,rps,avg_response_time,min_response_time,max_response_time,p50_response_time,p75_response_time,p95_response_time,p99_response_time,created_at,updated_at)VALUES(54,12,13,165,7,573,'https://example.com/api','completed','2026-05-17 07:48:00','2026-05-17 07:57:33',48772,650,1.33,559.1,32.1,9.6,160.5,22.5,41.7,80.2,128.4,'2026-05-17 07:48:00','2026-05-17 07:57:33')ON CONFLICT(id)DO NOTHING;

INSERT INTO performance_metric_samples(test_result_id,timestamp,elapsed_seconds,rps,active_users,avg_response_time,min_response_time,max_response_time,p95_response_time,p99_response_time,request_count,failure_count,error_rate)VALUES(54,'2026-05-17 07:48:00',0,622.4,3,27.9,9.6,96.3,64.2,128.4,6096,81,2.24);

INSERT INTO performance_metric_samples(test_result_id,timestamp,elapsed_seconds,rps,active_users,avg_response_time,min_response_time,max_response_time,p95_response_time,p99_response_time,request_count,failure_count,error_rate)VALUES(54,'2026-05-17 07:48:01',1,672.4,1,29.7,9.6,96.3,64.2,128.4,12193,162,1.68);

INSERT INTO performance_metric_samples(test_result_id,timestamp,elapsed_seconds,rps,active_users,avg_response_time,min_response_time,max_response_time,p95_response_time,p99_response_time,request_count,failure_count,error_rate)VALUES(54,'2026-05-17 07:48:02',2,430.9,9,33.0,9.6,96.3,64.2,128.4,18289,243,2.09);

INSERT INTO performance_metric_samples(test_result_id,timestamp,elapsed_seconds,rps,active_users,avg_response_time,min_response_time,max_response_time,p95_response_time,p99_response_time,request_count,failure_count,error_rate)VALUES(54,'2026-05-17 07:48:03',3,581.3,12,26.8,9.6,96.3,64.2,128.4,24386,325,2.75);

INSERT INTO performance_metric_samples(test_result_id,timestamp,elapsed_seconds,rps,active_users,avg_response_time,min_response_time,max_response_time,p95_response_time,p99_response_time,request_count,failure_count,error_rate)VALUES(54,'2026-05-17 07:48:04',4,452.6,15,28.1,9.6,96.3,64.2,128.4,30482,406,1.77);

INSERT INTO performance_metric_samples(test_result_id,timestamp,elapsed_seconds,rps,active_users,avg_response_time,min_response_time,max_response_time,p95_response_time,p99_response_time,request_count,failure_count,error_rate)VALUES(54,'2026-05-17 07:48:05',5,715.3,18,27.9,9.6,96.3,64.2,128.4,36579,487,0.03);

INSERT INTO performance_metric_samples(test_result_id,timestamp,elapsed_seconds,rps,active_users,avg_response_time,min_response_time,max_response_time,p95_response_time,p99_response_time,request_count,failure_count,error_rate)VALUES(54,'2026-05-17 07:48:06',6,605.4,21,26.7,9.6,96.3,64.2,128.4,42675,568,2.17);

INSERT INTO performance_metric_samples(test_result_id,timestamp,elapsed_seconds,rps,active_users,avg_response_time,min_response_time,max_response_time,p95_response_time,p99_response_time,request_count,failure_count,error_rate)VALUES(54,'2026-05-17 07:48:07',7,474.1,24,33.9,9.6,96.3,64.2,128.4,48772,650,2.7);

INSERT INTO performance_test_results(id,scenario_id,project_id,user_count,spawn_rate,duration,target_url,status,started_at,finished_at,total_requests,total_failures,error_rate,rps,avg_response_time,min_response_time,max_response_time,p50_response_time,p75_response_time,p95_response_time,p99_response_time,created_at,updated_at)VALUES(55,12,13,154,11,195,'https://example.com/api','completed','2026-04-13 10:12:00','2026-04-13 10:15:15',4495,85,1.89,896.9,122.4,36.7,612.0,85.7,159.1,306.0,489.6,'2026-04-13 10:12:00','2026-04-13 10:15:15')ON CONFLICT(id)DO NOTHING;

INSERT INTO performance_metric_samples(test_result_id,timestamp,elapsed_seconds,rps,active_users,avg_response_time,min_response_time,max_response_time,p95_response_time,p99_response_time,request_count,failure_count,error_rate)VALUES(55,'2026-04-13 10:12:00',0,850.6,3,111.3,36.7,367.2,244.8,489.6,561,10,0.6);

INSERT INTO performance_metric_samples(test_result_id,timestamp,elapsed_seconds,rps,active_users,avg_response_time,min_response_time,max_response_time,p95_response_time,p99_response_time,request_count,failure_count,error_rate)VALUES(55,'2026-04-13 10:12:01',1,1154.8,6,132.1,36.7,367.2,244.8,489.6,1123,21,0.79);

INSERT INTO performance_metric_samples(test_result_id,timestamp,elapsed_seconds,rps,active_users,avg_response_time,min_response_time,max_response_time,p95_response_time,p99_response_time,request_count,failure_count,error_rate)VALUES(55,'2026-04-13 10:12:02',2,891.5,9,115.7,36.7,367.2,244.8,489.6,1685,31,2.32);

INSERT INTO performance_metric_samples(test_result_id,timestamp,elapsed_seconds,rps,active_users,avg_response_time,min_response_time,max_response_time,p95_response_time,p99_response_time,request_count,failure_count,error_rate)VALUES(55,'2026-04-13 10:12:03',3,909.3,12,131.6,36.7,367.2,244.8,489.6,2247,42,0.51);

INSERT INTO performance_metric_samples(test_result_id,timestamp,elapsed_seconds,rps,active_users,avg_response_time,min_response_time,max_response_time,p95_response_time,p99_response_time,request_count,failure_count,error_rate)VALUES(55,'2026-04-13 10:12:04',4,1138.9,15,116.8,36.7,367.2,244.8,489.6,2809,53,1.61);

INSERT INTO performance_metric_samples(test_result_id,timestamp,elapsed_seconds,rps,active_users,avg_response_time,min_response_time,max_response_time,p95_response_time,p99_response_time,request_count,failure_count,error_rate)VALUES(55,'2026-04-13 10:12:05',5,741.2,18,119.2,36.7,367.2,244.8,489.6,3371,63,1.94);

INSERT INTO performance_metric_samples(test_result_id,timestamp,elapsed_seconds,rps,active_users,avg_response_time,min_response_time,max_response_time,p95_response_time,p99_response_time,request_count,failure_count,error_rate)VALUES(55,'2026-04-13 10:12:06',6,994.9,21,108.1,36.7,367.2,244.8,489.6,3933,74,2.1);

INSERT INTO performance_metric_samples(test_result_id,timestamp,elapsed_seconds,rps,active_users,avg_response_time,min_response_time,max_response_time,p95_response_time,p99_response_time,request_count,failure_count,error_rate)VALUES(55,'2026-04-13 10:12:07',7,898.9,24,136.8,36.7,367.2,244.8,489.6,4495,85,0.27);

INSERT INTO performance_test_results(id,scenario_id,project_id,user_count,spawn_rate,duration,target_url,status,started_at,finished_at,total_requests,total_failures,error_rate,rps,avg_response_time,min_response_time,max_response_time,p50_response_time,p75_response_time,p95_response_time,p99_response_time,created_at,updated_at)VALUES(56,12,13,131,5,538,'https://example.com/api','completed','2026-04-09 01:47:00','2026-04-09 01:55:58',3060,141,4.61,1575.2,258.0,77.4,1290.0,180.6,335.4,645.0,1032.0,'2026-04-09 01:47:00','2026-04-09 01:55:58')ON CONFLICT(id)DO NOTHING;

INSERT INTO performance_metric_samples(test_result_id,timestamp,elapsed_seconds,rps,active_users,avg_response_time,min_response_time,max_response_time,p95_response_time,p99_response_time,request_count,failure_count,error_rate)VALUES(56,'2026-04-09 01:47:00',0,1544.2,3,244.8,77.4,774.0,516.0,1032.0,382,17,1.13);

INSERT INTO performance_metric_samples(test_result_id,timestamp,elapsed_seconds,rps,active_users,avg_response_time,min_response_time,max_response_time,p95_response_time,p99_response_time,request_count,failure_count,error_rate)VALUES(56,'2026-04-09 01:47:01',1,1658.7,6,239.7,77.4,774.0,516.0,1032.0,765,35,0.31);

INSERT INTO performance_metric_samples(test_result_id,timestamp,elapsed_seconds,rps,active_users,avg_response_time,min_response_time,max_response_time,p95_response_time,p99_response_time,request_count,failure_count,error_rate)VALUES(56,'2026-04-09 01:47:02',2,1441.8,3,222.8,77.4,774.0,516.0,1032.0,1147,52,1.43);

INSERT INTO performance_metric_samples(test_result_id,timestamp,elapsed_seconds,rps,active_users,avg_response_time,min_response_time,max_response_time,p95_response_time,p99_response_time,request_count,failure_count,error_rate)VALUES(56,'2026-04-09 01:47:03',3,1420.8,12,225.7,77.4,774.0,516.0,1032.0,1530,70,1.07);

INSERT INTO performance_metric_samples(test_result_id,timestamp,elapsed_seconds,rps,active_users,avg_response_time,min_response_time,max_response_time,p95_response_time,p99_response_time,request_count,failure_count,error_rate)VALUES(56,'2026-04-09 01:47:04',4,1256.5,15,225.6,77.4,774.0,516.0,1032.0,1912,88,0.07);

INSERT INTO performance_metric_samples(test_result_id,timestamp,elapsed_seconds,rps,active_users,avg_response_time,min_response_time,max_response_time,p95_response_time,p99_response_time,request_count,failure_count,error_rate)VALUES(56,'2026-04-09 01:47:05',5,1867.5,18,267.7,77.4,774.0,516.0,1032.0,2295,105,2.08);

INSERT INTO performance_metric_samples(test_result_id,timestamp,elapsed_seconds,rps,active_users,avg_response_time,min_response_time,max_response_time,p95_response_time,p99_response_time,request_count,failure_count,error_rate)VALUES(56,'2026-04-09 01:47:06',6,1793.5,21,292.5,77.4,774.0,516.0,1032.0,2677,123,0.76);

INSERT INTO performance_metric_samples(test_result_id,timestamp,elapsed_seconds,rps,active_users,avg_response_time,min_response_time,max_response_time,p95_response_time,p99_response_time,request_count,failure_count,error_rate)VALUES(56,'2026-04-09 01:47:07',7,1455.4,24,256.2,77.4,774.0,516.0,1032.0,3060,141,1.2);

INSERT INTO performance_test_results(id,scenario_id,project_id,user_count,spawn_rate,duration,target_url,status,started_at,finished_at,total_requests,total_failures,error_rate,rps,avg_response_time,min_response_time,max_response_time,p50_response_time,p75_response_time,p95_response_time,p99_response_time,created_at,updated_at)VALUES(57,13,14,141,6,491,'https://example.com/api','failed','2026-04-02 17:54:00','2026-04-02 18:02:11',18652,889,4.77,1232.2,26.0,7.8,130.0,18.2,33.8,65.0,104.0,'2026-04-02 17:54:00','2026-04-02 18:02:11')ON CONFLICT(id)DO NOTHING;

INSERT INTO performance_metric_samples(test_result_id,timestamp,elapsed_seconds,rps,active_users,avg_response_time,min_response_time,max_response_time,p95_response_time,p99_response_time,request_count,failure_count,error_rate)VALUES(57,'2026-04-02 17:54:00',0,1544.5,3,30.8,7.8,78.0,52.0,104.0,2331,111,2.83);

INSERT INTO performance_metric_samples(test_result_id,timestamp,elapsed_seconds,rps,active_users,avg_response_time,min_response_time,max_response_time,p95_response_time,p99_response_time,request_count,failure_count,error_rate)VALUES(57,'2026-04-02 17:54:01',1,1009.3,6,28.6,7.8,78.0,52.0,104.0,4663,222,0.39);

INSERT INTO performance_metric_samples(test_result_id,timestamp,elapsed_seconds,rps,active_users,avg_response_time,min_response_time,max_response_time,p95_response_time,p99_response_time,request_count,failure_count,error_rate)VALUES(57,'2026-04-02 17:54:02',2,1108.8,9,30.9,7.8,78.0,52.0,104.0,6994,333,0.93);

INSERT INTO performance_metric_samples(test_result_id,timestamp,elapsed_seconds,rps,active_users,avg_response_time,min_response_time,max_response_time,p95_response_time,p99_response_time,request_count,failure_count,error_rate)VALUES(57,'2026-04-02 17:54:03',3,1428.7,12,25.6,7.8,78.0,52.0,104.0,9326,444,0.5);

INSERT INTO performance_metric_samples(test_result_id,timestamp,elapsed_seconds,rps,active_users,avg_response_time,min_response_time,max_response_time,p95_response_time,p99_response_time,request_count,failure_count,error_rate)VALUES(57,'2026-04-02 17:54:04',4,863.2,15,22.9,7.8,78.0,52.0,104.0,11657,555,0.52);

INSERT INTO performance_metric_samples(test_result_id,timestamp,elapsed_seconds,rps,active_users,avg_response_time,min_response_time,max_response_time,p95_response_time,p99_response_time,request_count,failure_count,error_rate)VALUES(57,'2026-04-02 17:54:05',5,1089.9,18,23.3,7.8,78.0,52.0,104.0,13989,666,0.61);

INSERT INTO performance_metric_samples(test_result_id,timestamp,elapsed_seconds,rps,active_users,avg_response_time,min_response_time,max_response_time,p95_response_time,p99_response_time,request_count,failure_count,error_rate)VALUES(57,'2026-04-02 17:54:06',6,929.2,21,22.4,7.8,78.0,52.0,104.0,16320,777,1.67);

INSERT INTO performance_metric_samples(test_result_id,timestamp,elapsed_seconds,rps,active_users,avg_response_time,min_response_time,max_response_time,p95_response_time,p99_response_time,request_count,failure_count,error_rate)VALUES(57,'2026-04-02 17:54:07',7,1436.0,2,25.8,7.8,78.0,52.0,104.0,18652,889,1.03);

INSERT INTO performance_test_results(id,scenario_id,project_id,user_count,spawn_rate,duration,target_url,status,started_at,finished_at,total_requests,total_failures,error_rate,rps,avg_response_time,min_response_time,max_response_time,p50_response_time,p75_response_time,p95_response_time,p99_response_time,created_at,updated_at)VALUES(58,13,14,34,13,463,'https://example.com/api','completed','2026-01-31 16:17:00','2026-01-31 16:24:43',31953,1067,3.34,2502.5,286.9,86.1,1434.5,200.8,373.0,717.2,1147.6,'2026-01-31 16:17:00','2026-01-31 16:24:43')ON CONFLICT(id)DO NOTHING;

INSERT INTO performance_metric_samples(test_result_id,timestamp,elapsed_seconds,rps,active_users,avg_response_time,min_response_time,max_response_time,p95_response_time,p99_response_time,request_count,failure_count,error_rate)VALUES(58,'2026-01-31 16:17:00',0,1944.7,3,336.9,86.1,860.7,573.8,1147.6,3994,133,1.2);

INSERT INTO performance_metric_samples(test_result_id,timestamp,elapsed_seconds,rps,active_users,avg_response_time,min_response_time,max_response_time,p95_response_time,p99_response_time,request_count,failure_count,error_rate)VALUES(58,'2026-01-31 16:17:01',1,2242.9,6,323.6,86.1,860.7,573.8,1147.6,7988,266,2.19);

INSERT INTO performance_metric_samples(test_result_id,timestamp,elapsed_seconds,rps,active_users,avg_response_time,min_response_time,max_response_time,p95_response_time,p99_response_time,request_count,failure_count,error_rate)VALUES(58,'2026-01-31 16:17:02',2,2389.3,9,290.8,86.1,860.7,573.8,1147.6,11982,400,1.04);

INSERT INTO performance_metric_samples(test_result_id,timestamp,elapsed_seconds,rps,active_users,avg_response_time,min_response_time,max_response_time,p95_response_time,p99_response_time,request_count,failure_count,error_rate)VALUES(58,'2026-01-31 16:17:03',3,2757.6,12,232.6,86.1,860.7,573.8,1147.6,15976,533,2.66);

INSERT INTO performance_metric_samples(test_result_id,timestamp,elapsed_seconds,rps,active_users,avg_response_time,min_response_time,max_response_time,p95_response_time,p99_response_time,request_count,failure_count,error_rate)VALUES(58,'2026-01-31 16:17:04',4,2019.3,15,271.9,86.1,860.7,573.8,1147.6,19970,666,1.02);

INSERT INTO performance_metric_samples(test_result_id,timestamp,elapsed_seconds,rps,active_users,avg_response_time,min_response_time,max_response_time,p95_response_time,p99_response_time,request_count,failure_count,error_rate)VALUES(58,'2026-01-31 16:17:05',5,2987.8,18,298.3,86.1,860.7,573.8,1147.6,23964,800,1.19);

INSERT INTO performance_metric_samples(test_result_id,timestamp,elapsed_seconds,rps,active_users,avg_response_time,min_response_time,max_response_time,p95_response_time,p99_response_time,request_count,failure_count,error_rate)VALUES(58,'2026-01-31 16:17:06',6,1867.8,21,245.4,86.1,860.7,573.8,1147.6,27958,933,0.56);

INSERT INTO performance_metric_samples(test_result_id,timestamp,elapsed_seconds,rps,active_users,avg_response_time,min_response_time,max_response_time,p95_response_time,p99_response_time,request_count,failure_count,error_rate)VALUES(58,'2026-01-31 16:17:07',7,2068.9,24,240.2,86.1,860.7,573.8,1147.6,31953,1067,1.15);

INSERT INTO performance_test_results(id,scenario_id,project_id,user_count,spawn_rate,duration,target_url,status,started_at,finished_at,total_requests,total_failures,error_rate,rps,avg_response_time,min_response_time,max_response_time,p50_response_time,p75_response_time,p95_response_time,p99_response_time,created_at,updated_at)VALUES(59,13,14,117,6,351,'https://example.com/api','completed','2026-04-15 20:51:00','2026-04-15 20:56:51',26350,889,3.37,1467.9,115.5,34.6,577.5,80.8,150.2,288.8,462.0,'2026-04-15 20:51:00','2026-04-15 20:56:51')ON CONFLICT(id)DO NOTHING;

INSERT INTO performance_metric_samples(test_result_id,timestamp,elapsed_seconds,rps,active_users,avg_response_time,min_response_time,max_response_time,p95_response_time,p99_response_time,request_count,failure_count,error_rate)VALUES(59,'2026-04-15 20:51:00',0,1171.6,3,116.3,34.6,346.5,231.0,462.0,3293,111,0.32);

INSERT INTO performance_metric_samples(test_result_id,timestamp,elapsed_seconds,rps,active_users,avg_response_time,min_response_time,max_response_time,p95_response_time,p99_response_time,request_count,failure_count,error_rate)VALUES(59,'2026-04-15 20:51:01',1,1737.6,6,124.1,34.6,346.5,231.0,462.0,6587,222,0.3);

INSERT INTO performance_metric_samples(test_result_id,timestamp,elapsed_seconds,rps,active_users,avg_response_time,min_response_time,max_response_time,p95_response_time,p99_response_time,request_count,failure_count,error_rate)VALUES(59,'2026-04-15 20:51:02',2,1787.1,4,99.8,34.6,346.5,231.0,462.0,9881,333,0.39);

INSERT INTO performance_metric_samples(test_result_id,timestamp,elapsed_seconds,rps,active_users,avg_response_time,min_response_time,max_response_time,p95_response_time,p99_response_time,request_count,failure_count,error_rate)VALUES(59,'2026-04-15 20:51:03',3,1474.0,12,113.4,34.6,346.5,231.0,462.0,13175,444,1.46);

INSERT INTO performance_metric_samples(test_result_id,timestamp,elapsed_seconds,rps,active_users,avg_response_time,min_response_time,max_response_time,p95_response_time,p99_response_time,request_count,failure_count,error_rate)VALUES(59,'2026-04-15 20:51:04',4,1873.0,15,111.9,34.6,346.5,231.0,462.0,16468,555,0.16);

INSERT INTO performance_metric_samples(test_result_id,timestamp,elapsed_seconds,rps,active_users,avg_response_time,min_response_time,max_response_time,p95_response_time,p99_response_time,request_count,failure_count,error_rate)VALUES(59,'2026-04-15 20:51:05',5,1401.8,18,121.7,34.6,346.5,231.0,462.0,19762,666,1.81);

INSERT INTO performance_metric_samples(test_result_id,timestamp,elapsed_seconds,rps,active_users,avg_response_time,min_response_time,max_response_time,p95_response_time,p99_response_time,request_count,failure_count,error_rate)VALUES(59,'2026-04-15 20:51:06',6,1734.3,21,115.6,34.6,346.5,231.0,462.0,23056,777,2.34);

INSERT INTO performance_metric_samples(test_result_id,timestamp,elapsed_seconds,rps,active_users,avg_response_time,min_response_time,max_response_time,p95_response_time,p99_response_time,request_count,failure_count,error_rate)VALUES(59,'2026-04-15 20:51:07',7,1654.6,24,137.3,34.6,346.5,231.0,462.0,26350,889,0.34);

INSERT INTO performance_test_results(id,scenario_id,project_id,user_count,spawn_rate,duration,target_url,status,started_at,finished_at,total_requests,total_failures,error_rate,rps,avg_response_time,min_response_time,max_response_time,p50_response_time,p75_response_time,p95_response_time,p99_response_time,created_at,updated_at)VALUES(60,14,14,76,7,452,'https://example.com/api','completed','2026-02-12 16:12:00','2026-02-12 16:19:32',10855,3,0.03,2847.2,287.4,86.2,1437.0,201.2,373.6,718.5,1149.6,'2026-02-12 16:12:00','2026-02-12 16:19:32')ON CONFLICT(id)DO NOTHING;

INSERT INTO performance_metric_samples(test_result_id,timestamp,elapsed_seconds,rps,active_users,avg_response_time,min_response_time,max_response_time,p95_response_time,p99_response_time,request_count,failure_count,error_rate)VALUES(60,'2026-02-12 16:12:00',0,2872.6,3,313.6,86.2,862.2,574.8,1149.6,1356,0,1.36);

INSERT INTO performance_metric_samples(test_result_id,timestamp,elapsed_seconds,rps,active_users,avg_response_time,min_response_time,max_response_time,p95_response_time,p99_response_time,request_count,failure_count,error_rate)VALUES(60,'2026-02-12 16:12:01',1,2076.0,6,234.5,86.2,862.2,574.8,1149.6,2713,0,2.6);

INSERT INTO performance_metric_samples(test_result_id,timestamp,elapsed_seconds,rps,active_users,avg_response_time,min_response_time,max_response_time,p95_response_time,p99_response_time,request_count,failure_count,error_rate)VALUES(60,'2026-02-12 16:12:02',2,2779.3,9,332.1,86.2,862.2,574.8,1149.6,4070,1,2.06);

INSERT INTO performance_metric_samples(test_result_id,timestamp,elapsed_seconds,rps,active_users,avg_response_time,min_response_time,max_response_time,p95_response_time,p99_response_time,request_count,failure_count,error_rate)VALUES(60,'2026-02-12 16:12:03',3,2424.1,12,307.5,86.2,862.2,574.8,1149.6,5427,1,2.3);

INSERT INTO performance_metric_samples(test_result_id,timestamp,elapsed_seconds,rps,active_users,avg_response_time,min_response_time,max_response_time,p95_response_time,p99_response_time,request_count,failure_count,error_rate)VALUES(60,'2026-02-12 16:12:04',4,2033.2,15,250.5,86.2,862.2,574.8,1149.6,6784,1,1.07);

INSERT INTO performance_metric_samples(test_result_id,timestamp,elapsed_seconds,rps,active_users,avg_response_time,min_response_time,max_response_time,p95_response_time,p99_response_time,request_count,failure_count,error_rate)VALUES(60,'2026-02-12 16:12:05',5,2023.0,18,264.1,86.2,862.2,574.8,1149.6,8141,2,0.11);

INSERT INTO performance_metric_samples(test_result_id,timestamp,elapsed_seconds,rps,active_users,avg_response_time,min_response_time,max_response_time,p95_response_time,p99_response_time,request_count,failure_count,error_rate)VALUES(60,'2026-02-12 16:12:06',6,2183.8,21,234.1,86.2,862.2,574.8,1149.6,9498,2,2.22);

INSERT INTO performance_metric_samples(test_result_id,timestamp,elapsed_seconds,rps,active_users,avg_response_time,min_response_time,max_response_time,p95_response_time,p99_response_time,request_count,failure_count,error_rate)VALUES(60,'2026-02-12 16:12:07',7,2417.8,22,291.4,86.2,862.2,574.8,1149.6,10855,3,0.38);

INSERT INTO performance_test_results(id,scenario_id,project_id,user_count,spawn_rate,duration,target_url,status,started_at,finished_at,total_requests,total_failures,error_rate,rps,avg_response_time,min_response_time,max_response_time,p50_response_time,p75_response_time,p95_response_time,p99_response_time,created_at,updated_at)VALUES(61,14,14,197,17,501,'https://example.com/api','completed','2026-04-24 13:29:00','2026-04-24 13:37:21',23635,1148,4.86,2082.5,109.0,32.7,545.0,76.3,141.7,272.5,436.0,'2026-04-24 13:29:00','2026-04-24 13:37:21')ON CONFLICT(id)DO NOTHING;

INSERT INTO performance_metric_samples(test_result_id,timestamp,elapsed_seconds,rps,active_users,avg_response_time,min_response_time,max_response_time,p95_response_time,p99_response_time,request_count,failure_count,error_rate)VALUES(61,'2026-04-24 13:29:00',0,2168.8,3,90.5,32.7,327.0,218.0,436.0,2954,143,1.12);

INSERT INTO performance_metric_samples(test_result_id,timestamp,elapsed_seconds,rps,active_users,avg_response_time,min_response_time,max_response_time,p95_response_time,p99_response_time,request_count,failure_count,error_rate)VALUES(61,'2026-04-24 13:29:01',1,1641.1,6,115.0,32.7,327.0,218.0,436.0,5908,287,2.65);

INSERT INTO performance_metric_samples(test_result_id,timestamp,elapsed_seconds,rps,active_users,avg_response_time,min_response_time,max_response_time,p95_response_time,p99_response_time,request_count,failure_count,error_rate)VALUES(61,'2026-04-24 13:29:02',2,1935.0,9,90.6,32.7,327.0,218.0,436.0,8863,430,2.78);

INSERT INTO performance_metric_samples(test_result_id,timestamp,elapsed_seconds,rps,active_users,avg_response_time,min_response_time,max_response_time,p95_response_time,p99_response_time,request_count,failure_count,error_rate)VALUES(61,'2026-04-24 13:29:03',3,2394.0,12,104.7,32.7,327.0,218.0,436.0,11817,574,0.55);

INSERT INTO performance_metric_samples(test_result_id,timestamp,elapsed_seconds,rps,active_users,avg_response_time,min_response_time,max_response_time,p95_response_time,p99_response_time,request_count,failure_count,error_rate)VALUES(61,'2026-04-24 13:29:04',4,2390.8,15,115.7,32.7,327.0,218.0,436.0,14771,717,2.65);

INSERT INTO performance_metric_samples(test_result_id,timestamp,elapsed_seconds,rps,active_users,avg_response_time,min_response_time,max_response_time,p95_response_time,p99_response_time,request_count,failure_count,error_rate)VALUES(61,'2026-04-24 13:29:05',5,2503.4,18,129.3,32.7,327.0,218.0,436.0,17726,861,2.38);

INSERT INTO performance_metric_samples(test_result_id,timestamp,elapsed_seconds,rps,active_users,avg_response_time,min_response_time,max_response_time,p95_response_time,p99_response_time,request_count,failure_count,error_rate)VALUES(61,'2026-04-24 13:29:06',6,2171.1,21,114.0,32.7,327.0,218.0,436.0,20680,1004,1.62);

INSERT INTO performance_metric_samples(test_result_id,timestamp,elapsed_seconds,rps,active_users,avg_response_time,min_response_time,max_response_time,p95_response_time,p99_response_time,request_count,failure_count,error_rate)VALUES(61,'2026-04-24 13:29:07',7,2449.5,24,122.0,32.7,327.0,218.0,436.0,23635,1148,1.12);

INSERT INTO performance_test_results(id,scenario_id,project_id,user_count,spawn_rate,duration,target_url,status,started_at,finished_at,total_requests,total_failures,error_rate,rps,avg_response_time,min_response_time,max_response_time,p50_response_time,p75_response_time,p95_response_time,p99_response_time,created_at,updated_at)VALUES(62,14,14,21,20,507,'https://example.com/api','completed','2026-01-31 03:12:00','2026-01-31 03:20:27',49946,1720,3.44,597.9,208.1,62.4,1040.5,145.7,270.5,520.2,832.4,'2026-01-31 03:12:00','2026-01-31 03:20:27')ON CONFLICT(id)DO NOTHING;

INSERT INTO performance_metric_samples(test_result_id,timestamp,elapsed_seconds,rps,active_users,avg_response_time,min_response_time,max_response_time,p95_response_time,p99_response_time,request_count,failure_count,error_rate)VALUES(62,'2026-01-31 03:12:00',0,561.5,3,222.9,62.4,624.3,416.2,832.4,6243,215,0.82);

INSERT INTO performance_metric_samples(test_result_id,timestamp,elapsed_seconds,rps,active_users,avg_response_time,min_response_time,max_response_time,p95_response_time,p99_response_time,request_count,failure_count,error_rate)VALUES(62,'2026-01-31 03:12:01',1,564.6,5,231.6,62.4,624.3,416.2,832.4,12486,430,1.97);

INSERT INTO performance_metric_samples(test_result_id,timestamp,elapsed_seconds,rps,active_users,avg_response_time,min_response_time,max_response_time,p95_response_time,p99_response_time,request_count,failure_count,error_rate)VALUES(62,'2026-01-31 03:12:02',2,517.1,9,216.3,62.4,624.3,416.2,832.4,18729,645,2.93);

INSERT INTO performance_metric_samples(test_result_id,timestamp,elapsed_seconds,rps,active_users,avg_response_time,min_response_time,max_response_time,p95_response_time,p99_response_time,request_count,failure_count,error_rate)VALUES(62,'2026-01-31 03:12:03',3,532.7,12,185.2,62.4,624.3,416.2,832.4,24973,860,2.13);

INSERT INTO performance_metric_samples(test_result_id,timestamp,elapsed_seconds,rps,active_users,avg_response_time,min_response_time,max_response_time,p95_response_time,p99_response_time,request_count,failure_count,error_rate)VALUES(62,'2026-01-31 03:12:04',4,497.8,15,190.4,62.4,624.3,416.2,832.4,31216,1075,2.14);

INSERT INTO performance_metric_samples(test_result_id,timestamp,elapsed_seconds,rps,active_users,avg_response_time,min_response_time,max_response_time,p95_response_time,p99_response_time,request_count,failure_count,error_rate)VALUES(62,'2026-01-31 03:12:05',5,715.2,18,201.5,62.4,624.3,416.2,832.4,37459,1290,1.79);

INSERT INTO performance_metric_samples(test_result_id,timestamp,elapsed_seconds,rps,active_users,avg_response_time,min_response_time,max_response_time,p95_response_time,p99_response_time,request_count,failure_count,error_rate)VALUES(62,'2026-01-31 03:12:06',6,612.8,21,243.9,62.4,624.3,416.2,832.4,43702,1505,0.04);

INSERT INTO performance_metric_samples(test_result_id,timestamp,elapsed_seconds,rps,active_users,avg_response_time,min_response_time,max_response_time,p95_response_time,p99_response_time,request_count,failure_count,error_rate)VALUES(62,'2026-01-31 03:12:07',7,540.7,24,235.0,62.4,624.3,416.2,832.4,49946,1720,0.46);

INSERT INTO performance_test_results(id,scenario_id,project_id,user_count,spawn_rate,duration,target_url,status,started_at,finished_at,total_requests,total_failures,error_rate,rps,avg_response_time,min_response_time,max_response_time,p50_response_time,p75_response_time,p95_response_time,p99_response_time,created_at,updated_at)VALUES(63,14,14,30,16,234,'https://example.com/api','failed','2026-01-25 03:26:00','2026-01-25 03:29:54',17757,357,2.01,1999.1,235.0,70.5,1175.0,164.5,305.5,587.5,940.0,'2026-01-25 03:26:00','2026-01-25 03:29:54')ON CONFLICT(id)DO NOTHING;

INSERT INTO performance_metric_samples(test_result_id,timestamp,elapsed_seconds,rps,active_users,avg_response_time,min_response_time,max_response_time,p95_response_time,p99_response_time,request_count,failure_count,error_rate)VALUES(63,'2026-01-25 03:26:00',0,2072.7,3,195.8,70.5,705.0,470.0,940.0,2219,44,2.24);

INSERT INTO performance_metric_samples(test_result_id,timestamp,elapsed_seconds,rps,active_users,avg_response_time,min_response_time,max_response_time,p95_response_time,p99_response_time,request_count,failure_count,error_rate)VALUES(63,'2026-01-25 03:26:01',1,2034.6,6,215.4,70.5,705.0,470.0,940.0,4439,89,0.95);

INSERT INTO performance_metric_samples(test_result_id,timestamp,elapsed_seconds,rps,active_users,avg_response_time,min_response_time,max_response_time,p95_response_time,p99_response_time,request_count,failure_count,error_rate)VALUES(63,'2026-01-25 03:26:02',2,2208.4,8,202.7,70.5,705.0,470.0,940.0,6658,133,1.75);

INSERT INTO performance_metric_samples(test_result_id,timestamp,elapsed_seconds,rps,active_users,avg_response_time,min_response_time,max_response_time,p95_response_time,p99_response_time,request_count,failure_count,error_rate)VALUES(63,'2026-01-25 03:26:03',3,2148.2,12,228.6,70.5,705.0,470.0,940.0,8878,178,2.99);

INSERT INTO performance_metric_samples(test_result_id,timestamp,elapsed_seconds,rps,active_users,avg_response_time,min_response_time,max_response_time,p95_response_time,p99_response_time,request_count,failure_count,error_rate)VALUES(63,'2026-01-25 03:26:04',4,1427.4,15,240.3,70.5,705.0,470.0,940.0,11098,223,1.47);

INSERT INTO performance_metric_samples(test_result_id,timestamp,elapsed_seconds,rps,active_users,avg_response_time,min_response_time,max_response_time,p95_response_time,p99_response_time,request_count,failure_count,error_rate)VALUES(63,'2026-01-25 03:26:05',5,1680.9,18,200.4,70.5,705.0,470.0,940.0,13317,267,1.82);

INSERT INTO performance_metric_samples(test_result_id,timestamp,elapsed_seconds,rps,active_users,avg_response_time,min_response_time,max_response_time,p95_response_time,p99_response_time,request_count,failure_count,error_rate)VALUES(63,'2026-01-25 03:26:06',6,2418.5,21,225.2,70.5,705.0,470.0,940.0,15537,312,0.63);

INSERT INTO performance_metric_samples(test_result_id,timestamp,elapsed_seconds,rps,active_users,avg_response_time,min_response_time,max_response_time,p95_response_time,p99_response_time,request_count,failure_count,error_rate)VALUES(63,'2026-01-25 03:26:07',7,1532.1,24,204.8,70.5,705.0,470.0,940.0,17757,357,0.48);

INSERT INTO performance_test_results(id,scenario_id,project_id,user_count,spawn_rate,duration,target_url,status,started_at,finished_at,total_requests,total_failures,error_rate,rps,avg_response_time,min_response_time,max_response_time,p50_response_time,p75_response_time,p95_response_time,p99_response_time,created_at,updated_at)VALUES(64,15,16,180,11,282,'https://example.com/api','failed','2026-01-11 20:38:00','2026-01-11 20:42:42',40272,561,1.39,2323.0,257.7,77.3,1288.5,180.4,335.0,644.2,1030.8,'2026-01-11 20:38:00','2026-01-11 20:42:42')ON CONFLICT(id)DO NOTHING;

INSERT INTO performance_metric_samples(test_result_id,timestamp,elapsed_seconds,rps,active_users,avg_response_time,min_response_time,max_response_time,p95_response_time,p99_response_time,request_count,failure_count,error_rate)VALUES(64,'2026-01-11 20:38:00',0,2326.2,3,246.6,77.3,773.1,515.4,1030.8,5034,70,2.58);

INSERT INTO performance_metric_samples(test_result_id,timestamp,elapsed_seconds,rps,active_users,avg_response_time,min_response_time,max_response_time,p95_response_time,p99_response_time,request_count,failure_count,error_rate)VALUES(64,'2026-01-11 20:38:01',1,2315.8,6,235.7,77.3,773.1,515.4,1030.8,10068,140,2.77);

INSERT INTO performance_metric_samples(test_result_id,timestamp,elapsed_seconds,rps,active_users,avg_response_time,min_response_time,max_response_time,p95_response_time,p99_response_time,request_count,failure_count,error_rate)VALUES(64,'2026-01-11 20:38:02',2,1844.9,9,247.4,77.3,773.1,515.4,1030.8,15102,210,0.01);

INSERT INTO performance_metric_samples(test_result_id,timestamp,elapsed_seconds,rps,active_users,avg_response_time,min_response_time,max_response_time,p95_response_time,p99_response_time,request_count,failure_count,error_rate)VALUES(64,'2026-01-11 20:38:03',3,2782.8,12,254.0,77.3,773.1,515.4,1030.8,20136,280,0.52);

INSERT INTO performance_metric_samples(test_result_id,timestamp,elapsed_seconds,rps,active_users,avg_response_time,min_response_time,max_response_time,p95_response_time,p99_response_time,request_count,failure_count,error_rate)VALUES(64,'2026-01-11 20:38:04',4,2890.7,15,266.0,77.3,773.1,515.4,1030.8,25170,350,1.25);

INSERT INTO performance_metric_samples(test_result_id,timestamp,elapsed_seconds,rps,active_users,avg_response_time,min_response_time,max_response_time,p95_response_time,p99_response_time,request_count,failure_count,error_rate)VALUES(64,'2026-01-11 20:38:05',5,2209.1,18,271.8,77.3,773.1,515.4,1030.8,30204,420,1.86);

INSERT INTO performance_metric_samples(test_result_id,timestamp,elapsed_seconds,rps,active_users,avg_response_time,min_response_time,max_response_time,p95_response_time,p99_response_time,request_count,failure_count,error_rate)VALUES(64,'2026-01-11 20:38:06',6,1819.2,21,258.0,77.3,773.1,515.4,1030.8,35238,490,0.24);

INSERT INTO performance_metric_samples(test_result_id,timestamp,elapsed_seconds,rps,active_users,avg_response_time,min_response_time,max_response_time,p95_response_time,p99_response_time,request_count,failure_count,error_rate)VALUES(64,'2026-01-11 20:38:07',7,2421.4,24,303.6,77.3,773.1,515.4,1030.8,40272,561,0.98);

INSERT INTO performance_test_results(id,scenario_id,project_id,user_count,spawn_rate,duration,target_url,status,started_at,finished_at,total_requests,total_failures,error_rate,rps,avg_response_time,min_response_time,max_response_time,p50_response_time,p75_response_time,p95_response_time,p99_response_time,created_at,updated_at)VALUES(65,15,16,109,18,543,'https://example.com/api','completed','2026-03-30 04:24:00','2026-03-30 04:33:03',25267,28,0.11,1824.0,319.1,95.7,1595.5,223.4,414.8,797.8,1276.4,'2026-03-30 04:24:00','2026-03-30 04:33:03')ON CONFLICT(id)DO NOTHING;

INSERT INTO performance_metric_samples(test_result_id,timestamp,elapsed_seconds,rps,active_users,avg_response_time,min_response_time,max_response_time,p95_response_time,p99_response_time,request_count,failure_count,error_rate)VALUES(65,'2026-03-30 04:24:00',0,1836.4,3,363.8,95.7,957.3,638.2,1276.4,3158,3,0.48);

INSERT INTO performance_metric_samples(test_result_id,timestamp,elapsed_seconds,rps,active_users,avg_response_time,min_response_time,max_response_time,p95_response_time,p99_response_time,request_count,failure_count,error_rate)VALUES(65,'2026-03-30 04:24:01',1,1680.7,6,277.6,95.7,957.3,638.2,1276.4,6316,7,2.81);

INSERT INTO performance_metric_samples(test_result_id,timestamp,elapsed_seconds,rps,active_users,avg_response_time,min_response_time,max_response_time,p95_response_time,p99_response_time,request_count,failure_count,error_rate)VALUES(65,'2026-03-30 04:24:02',2,2285.2,9,272.2,95.7,957.3,638.2,1276.4,9475,10,0.19);

INSERT INTO performance_metric_samples(test_result_id,timestamp,elapsed_seconds,rps,active_users,avg_response_time,min_response_time,max_response_time,p95_response_time,p99_response_time,request_count,failure_count,error_rate)VALUES(65,'2026-03-30 04:24:03',3,1310.6,12,314.1,95.7,957.3,638.2,1276.4,12633,14,0.74);

INSERT INTO performance_metric_samples(test_result_id,timestamp,elapsed_seconds,rps,active_users,avg_response_time,min_response_time,max_response_time,p95_response_time,p99_response_time,request_count,failure_count,error_rate)VALUES(65,'2026-03-30 04:24:04',4,1937.0,15,357.0,95.7,957.3,638.2,1276.4,15791,17,2.92);

INSERT INTO performance_metric_samples(test_result_id,timestamp,elapsed_seconds,rps,active_users,avg_response_time,min_response_time,max_response_time,p95_response_time,p99_response_time,request_count,failure_count,error_rate)VALUES(65,'2026-03-30 04:24:05',5,1824.2,18,357.9,95.7,957.3,638.2,1276.4,18950,21,2.51);

INSERT INTO performance_metric_samples(test_result_id,timestamp,elapsed_seconds,rps,active_users,avg_response_time,min_response_time,max_response_time,p95_response_time,p99_response_time,request_count,failure_count,error_rate)VALUES(65,'2026-03-30 04:24:06',6,2231.2,21,286.5,95.7,957.3,638.2,1276.4,22108,24,2.17);

INSERT INTO performance_metric_samples(test_result_id,timestamp,elapsed_seconds,rps,active_users,avg_response_time,min_response_time,max_response_time,p95_response_time,p99_response_time,request_count,failure_count,error_rate)VALUES(65,'2026-03-30 04:24:07',7,1353.2,24,259.4,95.7,957.3,638.2,1276.4,25267,28,2.03);

INSERT INTO performance_test_results(id,scenario_id,project_id,user_count,spawn_rate,duration,target_url,status,started_at,finished_at,total_requests,total_failures,error_rate,rps,avg_response_time,min_response_time,max_response_time,p50_response_time,p75_response_time,p95_response_time,p99_response_time,created_at,updated_at)VALUES(66,15,16,193,20,454,'https://example.com/api','completed','2026-01-18 18:05:00','2026-01-18 18:12:34',28334,1356,4.79,2655.9,221.9,66.6,1109.5,155.3,288.5,554.8,887.6,'2026-01-18 18:05:00','2026-01-18 18:12:34')ON CONFLICT(id)DO NOTHING;

INSERT INTO performance_metric_samples(test_result_id,timestamp,elapsed_seconds,rps,active_users,avg_response_time,min_response_time,max_response_time,p95_response_time,p99_response_time,request_count,failure_count,error_rate)VALUES(66,'2026-01-18 18:05:00',0,2890.3,3,241.0,66.6,665.7,443.8,887.6,3541,169,1.32);

INSERT INTO performance_metric_samples(test_result_id,timestamp,elapsed_seconds,rps,active_users,avg_response_time,min_response_time,max_response_time,p95_response_time,p99_response_time,request_count,failure_count,error_rate)VALUES(66,'2026-01-18 18:05:01',1,3178.2,6,203.5,66.6,665.7,443.8,887.6,7083,339,1.2);

INSERT INTO performance_metric_samples(test_result_id,timestamp,elapsed_seconds,rps,active_users,avg_response_time,min_response_time,max_response_time,p95_response_time,p99_response_time,request_count,failure_count,error_rate)VALUES(66,'2026-01-18 18:05:02',2,3169.5,9,181.1,66.6,665.7,443.8,887.6,10625,508,1.2);

INSERT INTO performance_metric_samples(test_result_id,timestamp,elapsed_seconds,rps,active_users,avg_response_time,min_response_time,max_response_time,p95_response_time,p99_response_time,request_count,failure_count,error_rate)VALUES(66,'2026-01-18 18:05:03',3,3337.0,12,235.2,66.6,665.7,443.8,887.6,14167,678,1.29);

INSERT INTO performance_metric_samples(test_result_id,timestamp,elapsed_seconds,rps,active_users,avg_response_time,min_response_time,max_response_time,p95_response_time,p99_response_time,request_count,failure_count,error_rate)VALUES(66,'2026-01-18 18:05:04',4,2056.8,15,252.7,66.6,665.7,443.8,887.6,17708,847,2.27);

INSERT INTO performance_metric_samples(test_result_id,timestamp,elapsed_seconds,rps,active_users,avg_response_time,min_response_time,max_response_time,p95_response_time,p99_response_time,request_count,failure_count,error_rate)VALUES(66,'2026-01-18 18:05:05',5,2783.1,18,241.6,66.6,665.7,443.8,887.6,21250,1017,1.1);

INSERT INTO performance_metric_samples(test_result_id,timestamp,elapsed_seconds,rps,active_users,avg_response_time,min_response_time,max_response_time,p95_response_time,p99_response_time,request_count,failure_count,error_rate)VALUES(66,'2026-01-18 18:05:06',6,2905.3,21,258.6,66.6,665.7,443.8,887.6,24792,1186,2.39);

INSERT INTO performance_metric_samples(test_result_id,timestamp,elapsed_seconds,rps,active_users,avg_response_time,min_response_time,max_response_time,p95_response_time,p99_response_time,request_count,failure_count,error_rate)VALUES(66,'2026-01-18 18:05:07',7,2193.9,24,206.8,66.6,665.7,443.8,887.6,28334,1356,2.08);

INSERT INTO performance_test_results(id,scenario_id,project_id,user_count,spawn_rate,duration,target_url,status,started_at,finished_at,total_requests,total_failures,error_rate,rps,avg_response_time,min_response_time,max_response_time,p50_response_time,p75_response_time,p95_response_time,p99_response_time,created_at,updated_at)VALUES(67,15,16,189,9,310,'https://example.com/api','completed','2026-02-03 11:29:00','2026-02-03 11:34:10',23442,346,1.48,1361.8,318.1,95.4,1590.5,222.7,413.5,795.2,1272.4,'2026-02-03 11:29:00','2026-02-03 11:34:10')ON CONFLICT(id)DO NOTHING;

INSERT INTO performance_metric_samples(test_result_id,timestamp,elapsed_seconds,rps,active_users,avg_response_time,min_response_time,max_response_time,p95_response_time,p99_response_time,request_count,failure_count,error_rate)VALUES(67,'2026-02-03 11:29:00',0,1417.6,3,259.0,95.4,954.3,636.2,1272.4,2930,43,0.42);

INSERT INTO performance_metric_samples(test_result_id,timestamp,elapsed_seconds,rps,active_users,avg_response_time,min_response_time,max_response_time,p95_response_time,p99_response_time,request_count,failure_count,error_rate)VALUES(67,'2026-02-03 11:29:01',1,1379.6,6,282.6,95.4,954.3,636.2,1272.4,5860,86,1.11);

INSERT INTO performance_metric_samples(test_result_id,timestamp,elapsed_seconds,rps,active_users,avg_response_time,min_response_time,max_response_time,p95_response_time,p99_response_time,request_count,failure_count,error_rate)VALUES(67,'2026-02-03 11:29:02',2,1249.6,9,293.5,95.4,954.3,636.2,1272.4,8790,129,2.15);

INSERT INTO performance_metric_samples(test_result_id,timestamp,elapsed_seconds,rps,active_users,avg_response_time,min_response_time,max_response_time,p95_response_time,p99_response_time,request_count,failure_count,error_rate)VALUES(67,'2026-02-03 11:29:03',3,1417.1,12,315.0,95.4,954.3,636.2,1272.4,11721,173,1.32);

INSERT INTO performance_metric_samples(test_result_id,timestamp,elapsed_seconds,rps,active_users,avg_response_time,min_response_time,max_response_time,p95_response_time,p99_response_time,request_count,failure_count,error_rate)VALUES(67,'2026-02-03 11:29:04',4,1194.2,15,356.9,95.4,954.3,636.2,1272.4,14651,216,0.39);

INSERT INTO performance_metric_samples(test_result_id,timestamp,elapsed_seconds,rps,active_users,avg_response_time,min_response_time,max_response_time,p95_response_time,p99_response_time,request_count,failure_count,error_rate)VALUES(67,'2026-02-03 11:29:05',5,1449.6,18,287.2,95.4,954.3,636.2,1272.4,17581,259,0.68);

INSERT INTO performance_metric_samples(test_result_id,timestamp,elapsed_seconds,rps,active_users,avg_response_time,min_response_time,max_response_time,p95_response_time,p99_response_time,request_count,failure_count,error_rate)VALUES(67,'2026-02-03 11:29:06',6,1648.5,21,293.0,95.4,954.3,636.2,1272.4,20511,302,1.75);

INSERT INTO performance_metric_samples(test_result_id,timestamp,elapsed_seconds,rps,active_users,avg_response_time,min_response_time,max_response_time,p95_response_time,p99_response_time,request_count,failure_count,error_rate)VALUES(67,'2026-02-03 11:29:07',7,1165.2,24,319.2,95.4,954.3,636.2,1272.4,23442,346,2.61);

INSERT INTO performance_test_results(id,scenario_id,project_id,user_count,spawn_rate,duration,target_url,status,started_at,finished_at,total_requests,total_failures,error_rate,rps,avg_response_time,min_response_time,max_response_time,p50_response_time,p75_response_time,p95_response_time,p99_response_time,created_at,updated_at)VALUES(68,15,16,105,13,234,'https://example.com/api','completed','2026-01-19 21:30:00','2026-01-19 21:33:54',43195,336,0.78,2565.2,136.0,40.8,680.0,95.2,176.8,340.0,544.0,'2026-01-19 21:30:00','2026-01-19 21:33:54')ON CONFLICT(id)DO NOTHING;

INSERT INTO performance_metric_samples(test_result_id,timestamp,elapsed_seconds,rps,active_users,avg_response_time,min_response_time,max_response_time,p95_response_time,p99_response_time,request_count,failure_count,error_rate)VALUES(68,'2026-01-19 21:30:00',0,3127.6,3,144.1,40.8,408.0,272.0,544.0,5399,42,2.61);

INSERT INTO performance_metric_samples(test_result_id,timestamp,elapsed_seconds,rps,active_users,avg_response_time,min_response_time,max_response_time,p95_response_time,p99_response_time,request_count,failure_count,error_rate)VALUES(68,'2026-01-19 21:30:01',1,2537.6,6,157.6,40.8,408.0,272.0,544.0,10798,84,0.04);

INSERT INTO performance_metric_samples(test_result_id,timestamp,elapsed_seconds,rps,active_users,avg_response_time,min_response_time,max_response_time,p95_response_time,p99_response_time,request_count,failure_count,error_rate)VALUES(68,'2026-01-19 21:30:02',2,3253.1,9,121.0,40.8,408.0,272.0,544.0,16198,126,0.62);

INSERT INTO performance_metric_samples(test_result_id,timestamp,elapsed_seconds,rps,active_users,avg_response_time,min_response_time,max_response_time,p95_response_time,p99_response_time,request_count,failure_count,error_rate)VALUES(68,'2026-01-19 21:30:03',3,2026.6,12,151.1,40.8,408.0,272.0,544.0,21597,168,2.37);

INSERT INTO performance_metric_samples(test_result_id,timestamp,elapsed_seconds,rps,active_users,avg_response_time,min_response_time,max_response_time,p95_response_time,p99_response_time,request_count,failure_count,error_rate)VALUES(68,'2026-01-19 21:30:04',4,2796.1,15,135.9,40.8,408.0,272.0,544.0,26996,210,1.71);

INSERT INTO performance_metric_samples(test_result_id,timestamp,elapsed_seconds,rps,active_users,avg_response_time,min_response_time,max_response_time,p95_response_time,p99_response_time,request_count,failure_count,error_rate)VALUES(68,'2026-01-19 21:30:05',5,2778.6,4,154.5,40.8,408.0,272.0,544.0,32396,252,2.54);

INSERT INTO performance_metric_samples(test_result_id,timestamp,elapsed_seconds,rps,active_users,avg_response_time,min_response_time,max_response_time,p95_response_time,p99_response_time,request_count,failure_count,error_rate)VALUES(68,'2026-01-19 21:30:06',6,3000.9,21,157.7,40.8,408.0,272.0,544.0,37795,294,2.22);

INSERT INTO performance_metric_samples(test_result_id,timestamp,elapsed_seconds,rps,active_users,avg_response_time,min_response_time,max_response_time,p95_response_time,p99_response_time,request_count,failure_count,error_rate)VALUES(68,'2026-01-19 21:30:07',7,2355.2,9,130.5,40.8,408.0,272.0,544.0,43195,336,0.3);

INSERT INTO performance_test_results(id,scenario_id,project_id,user_count,spawn_rate,duration,target_url,status,started_at,finished_at,total_requests,total_failures,error_rate,rps,avg_response_time,min_response_time,max_response_time,p50_response_time,p75_response_time,p95_response_time,p99_response_time,created_at,updated_at)VALUES(69,15,16,199,6,337,'https://example.com/api','completed','2026-03-08 17:56:00','2026-03-08 18:01:37',4668,104,2.23,1592.7,109.2,32.8,546.0,76.4,142.0,273.0,436.8,'2026-03-08 17:56:00','2026-03-08 18:01:37')ON CONFLICT(id)DO NOTHING;

INSERT INTO performance_metric_samples(test_result_id,timestamp,elapsed_seconds,rps,active_users,avg_response_time,min_response_time,max_response_time,p95_response_time,p99_response_time,request_count,failure_count,error_rate)VALUES(69,'2026-03-08 17:56:00',0,1774.0,3,124.8,32.8,327.6,218.4,436.8,583,13,0.69);

INSERT INTO performance_metric_samples(test_result_id,timestamp,elapsed_seconds,rps,active_users,avg_response_time,min_response_time,max_response_time,p95_response_time,p99_response_time,request_count,failure_count,error_rate)VALUES(69,'2026-03-08 17:56:01',1,1800.4,6,89.1,32.8,327.6,218.4,436.8,1167,26,1.83);

INSERT INTO performance_metric_samples(test_result_id,timestamp,elapsed_seconds,rps,active_users,avg_response_time,min_response_time,max_response_time,p95_response_time,p99_response_time,request_count,failure_count,error_rate)VALUES(69,'2026-03-08 17:56:02',2,1642.4,9,119.8,32.8,327.6,218.4,436.8,1750,39,2.2);

INSERT INTO performance_metric_samples(test_result_id,timestamp,elapsed_seconds,rps,active_users,avg_response_time,min_response_time,max_response_time,p95_response_time,p99_response_time,request_count,failure_count,error_rate)VALUES(69,'2026-03-08 17:56:03',3,1991.6,12,110.2,32.8,327.6,218.4,436.8,2334,52,0.18);

INSERT INTO performance_metric_samples(test_result_id,timestamp,elapsed_seconds,rps,active_users,avg_response_time,min_response_time,max_response_time,p95_response_time,p99_response_time,request_count,failure_count,error_rate)VALUES(69,'2026-03-08 17:56:04',4,1332.4,15,120.6,32.8,327.6,218.4,436.8,2917,65,1.43);

INSERT INTO performance_metric_samples(test_result_id,timestamp,elapsed_seconds,rps,active_users,avg_response_time,min_response_time,max_response_time,p95_response_time,p99_response_time,request_count,failure_count,error_rate)VALUES(69,'2026-03-08 17:56:05',5,1208.8,14,101.3,32.8,327.6,218.4,436.8,3501,78,1.9);

INSERT INTO performance_metric_samples(test_result_id,timestamp,elapsed_seconds,rps,active_users,avg_response_time,min_response_time,max_response_time,p95_response_time,p99_response_time,request_count,failure_count,error_rate)VALUES(69,'2026-03-08 17:56:06',6,1302.6,21,106.7,32.8,327.6,218.4,436.8,4084,91,1.43);

INSERT INTO performance_metric_samples(test_result_id,timestamp,elapsed_seconds,rps,active_users,avg_response_time,min_response_time,max_response_time,p95_response_time,p99_response_time,request_count,failure_count,error_rate)VALUES(69,'2026-03-08 17:56:07',7,1210.3,24,96.8,32.8,327.6,218.4,436.8,4668,104,1.46);

INSERT INTO performance_test_results(id,scenario_id,project_id,user_count,spawn_rate,duration,target_url,status,started_at,finished_at,total_requests,total_failures,error_rate,rps,avg_response_time,min_response_time,max_response_time,p50_response_time,p75_response_time,p95_response_time,p99_response_time,created_at,updated_at)VALUES(70,16,16,126,1,174,'https://example.com/api','failed','2026-01-03 20:05:00','2026-01-03 20:07:54',43115,419,0.97,2427.0,251.5,75.5,1257.5,176.0,326.9,628.8,1006.0,'2026-01-03 20:05:00','2026-01-03 20:07:54')ON CONFLICT(id)DO NOTHING;

INSERT INTO performance_metric_samples(test_result_id,timestamp,elapsed_seconds,rps,active_users,avg_response_time,min_response_time,max_response_time,p95_response_time,p99_response_time,request_count,failure_count,error_rate)VALUES(70,'2026-01-03 20:05:00',0,2065.5,3,261.7,75.5,754.5,503.0,1006.0,5389,52,1.48);

INSERT INTO performance_metric_samples(test_result_id,timestamp,elapsed_seconds,rps,active_users,avg_response_time,min_response_time,max_response_time,p95_response_time,p99_response_time,request_count,failure_count,error_rate)VALUES(70,'2026-01-03 20:05:01',1,1956.0,6,249.8,75.5,754.5,503.0,1006.0,10778,104,0.85);

INSERT INTO performance_metric_samples(test_result_id,timestamp,elapsed_seconds,rps,active_users,avg_response_time,min_response_time,max_response_time,p95_response_time,p99_response_time,request_count,failure_count,error_rate)VALUES(70,'2026-01-03 20:05:02',2,2638.6,9,288.4,75.5,754.5,503.0,1006.0,16168,157,0.75);

INSERT INTO performance_metric_samples(test_result_id,timestamp,elapsed_seconds,rps,active_users,avg_response_time,min_response_time,max_response_time,p95_response_time,p99_response_time,request_count,failure_count,error_rate)VALUES(70,'2026-01-03 20:05:03',3,2099.8,12,251.8,75.5,754.5,503.0,1006.0,21557,209,1.88);

INSERT INTO performance_metric_samples(test_result_id,timestamp,elapsed_seconds,rps,active_users,avg_response_time,min_response_time,max_response_time,p95_response_time,p99_response_time,request_count,failure_count,error_rate)VALUES(70,'2026-01-03 20:05:04',4,1861.2,15,296.3,75.5,754.5,503.0,1006.0,26946,261,1.46);

INSERT INTO performance_metric_samples(test_result_id,timestamp,elapsed_seconds,rps,active_users,avg_response_time,min_response_time,max_response_time,p95_response_time,p99_response_time,request_count,failure_count,error_rate)VALUES(70,'2026-01-03 20:05:05',5,2163.7,18,248.5,75.5,754.5,503.0,1006.0,32336,314,0.49);

INSERT INTO performance_metric_samples(test_result_id,timestamp,elapsed_seconds,rps,active_users,avg_response_time,min_response_time,max_response_time,p95_response_time,p99_response_time,request_count,failure_count,error_rate)VALUES(70,'2026-01-03 20:05:06',6,1794.4,21,268.9,75.5,754.5,503.0,1006.0,37725,366,0.28);

INSERT INTO performance_metric_samples(test_result_id,timestamp,elapsed_seconds,rps,active_users,avg_response_time,min_response_time,max_response_time,p95_response_time,p99_response_time,request_count,failure_count,error_rate)VALUES(70,'2026-01-03 20:05:07',7,2954.2,24,265.4,75.5,754.5,503.0,1006.0,43115,419,1.62);

INSERT INTO performance_test_results(id,scenario_id,project_id,user_count,spawn_rate,duration,target_url,status,started_at,finished_at,total_requests,total_failures,error_rate,rps,avg_response_time,min_response_time,max_response_time,p50_response_time,p75_response_time,p95_response_time,p99_response_time,created_at,updated_at)VALUES(71,16,16,130,4,171,'https://example.com/api','completed','2026-04-16 03:11:00','2026-04-16 03:13:51',14973,229,1.53,950.9,310.1,93.0,1550.5,217.1,403.1,775.2,1240.4,'2026-04-16 03:11:00','2026-04-16 03:13:51')ON CONFLICT(id)DO NOTHING;

INSERT INTO performance_metric_samples(test_result_id,timestamp,elapsed_seconds,rps,active_users,avg_response_time,min_response_time,max_response_time,p95_response_time,p99_response_time,request_count,failure_count,error_rate)VALUES(71,'2026-04-16 03:11:00',0,1056.3,3,274.2,93.0,930.3,620.2,1240.4,1871,28,2.02);

INSERT INTO performance_metric_samples(test_result_id,timestamp,elapsed_seconds,rps,active_users,avg_response_time,min_response_time,max_response_time,p95_response_time,p99_response_time,request_count,failure_count,error_rate)VALUES(71,'2026-04-16 03:11:01',1,850.4,6,343.1,93.0,930.3,620.2,1240.4,3743,57,2.36);

INSERT INTO performance_metric_samples(test_result_id,timestamp,elapsed_seconds,rps,active_users,avg_response_time,min_response_time,max_response_time,p95_response_time,p99_response_time,request_count,failure_count,error_rate)VALUES(71,'2026-04-16 03:11:02',2,1151.9,9,330.3,93.0,930.3,620.2,1240.4,5614,85,0.98);

INSERT INTO performance_metric_samples(test_result_id,timestamp,elapsed_seconds,rps,active_users,avg_response_time,min_response_time,max_response_time,p95_response_time,p99_response_time,request_count,failure_count,error_rate)VALUES(71,'2026-04-16 03:11:03',3,960.3,12,329.1,93.0,930.3,620.2,1240.4,7486,114,2.37);

INSERT INTO performance_metric_samples(test_result_id,timestamp,elapsed_seconds,rps,active_users,avg_response_time,min_response_time,max_response_time,p95_response_time,p99_response_time,request_count,failure_count,error_rate)VALUES(71,'2026-04-16 03:11:04',4,1110.5,15,276.5,93.0,930.3,620.2,1240.4,9358,143,0.79);

INSERT INTO performance_metric_samples(test_result_id,timestamp,elapsed_seconds,rps,active_users,avg_response_time,min_response_time,max_response_time,p95_response_time,p99_response_time,request_count,failure_count,error_rate)VALUES(71,'2026-04-16 03:11:05',5,1198.7,18,294.1,93.0,930.3,620.2,1240.4,11229,171,0.92);

INSERT INTO performance_metric_samples(test_result_id,timestamp,elapsed_seconds,rps,active_users,avg_response_time,min_response_time,max_response_time,p95_response_time,p99_response_time,request_count,failure_count,error_rate)VALUES(71,'2026-04-16 03:11:06',6,1080.2,21,287.2,93.0,930.3,620.2,1240.4,13101,200,0.92);

INSERT INTO performance_metric_samples(test_result_id,timestamp,elapsed_seconds,rps,active_users,avg_response_time,min_response_time,max_response_time,p95_response_time,p99_response_time,request_count,failure_count,error_rate)VALUES(71,'2026-04-16 03:11:07',7,987.0,24,299.8,93.0,930.3,620.2,1240.4,14973,229,2.29);

INSERT INTO performance_test_results(id,scenario_id,project_id,user_count,spawn_rate,duration,target_url,status,started_at,finished_at,total_requests,total_failures,error_rate,rps,avg_response_time,min_response_time,max_response_time,p50_response_time,p75_response_time,p95_response_time,p99_response_time,created_at,updated_at)VALUES(72,16,16,63,9,422,'https://example.com/api','completed','2026-02-18 08:34:00','2026-02-18 08:41:02',30942,1186,3.83,107.5,286.2,85.9,1431.0,200.3,372.1,715.5,1144.8,'2026-02-18 08:34:00','2026-02-18 08:41:02')ON CONFLICT(id)DO NOTHING;

INSERT INTO performance_metric_samples(test_result_id,timestamp,elapsed_seconds,rps,active_users,avg_response_time,min_response_time,max_response_time,p95_response_time,p99_response_time,request_count,failure_count,error_rate)VALUES(72,'2026-02-18 08:34:00',0,94.3,3,231.7,85.9,858.6,572.4,1144.8,3867,148,1.28);

INSERT INTO performance_metric_samples(test_result_id,timestamp,elapsed_seconds,rps,active_users,avg_response_time,min_response_time,max_response_time,p95_response_time,p99_response_time,request_count,failure_count,error_rate)VALUES(72,'2026-02-18 08:34:01',1,99.9,6,293.1,85.9,858.6,572.4,1144.8,7735,296,0.6);

INSERT INTO performance_metric_samples(test_result_id,timestamp,elapsed_seconds,rps,active_users,avg_response_time,min_response_time,max_response_time,p95_response_time,p99_response_time,request_count,failure_count,error_rate)VALUES(72,'2026-02-18 08:34:02',2,89.1,9,279.3,85.9,858.6,572.4,1144.8,11603,444,0.82);

INSERT INTO performance_metric_samples(test_result_id,timestamp,elapsed_seconds,rps,active_users,avg_response_time,min_response_time,max_response_time,p95_response_time,p99_response_time,request_count,failure_count,error_rate)VALUES(72,'2026-02-18 08:34:03',3,80.1,12,266.2,85.9,858.6,572.4,1144.8,15471,593,1.44);

INSERT INTO performance_metric_samples(test_result_id,timestamp,elapsed_seconds,rps,active_users,avg_response_time,min_response_time,max_response_time,p95_response_time,p99_response_time,request_count,failure_count,error_rate)VALUES(72,'2026-02-18 08:34:04',4,121.8,15,338.0,85.9,858.6,572.4,1144.8,19338,741,2.84);

INSERT INTO performance_metric_samples(test_result_id,timestamp,elapsed_seconds,rps,active_users,avg_response_time,min_response_time,max_response_time,p95_response_time,p99_response_time,request_count,failure_count,error_rate)VALUES(72,'2026-02-18 08:34:05',5,125.6,18,307.7,85.9,858.6,572.4,1144.8,23206,889,2.73);

INSERT INTO performance_metric_samples(test_result_id,timestamp,elapsed_seconds,rps,active_users,avg_response_time,min_response_time,max_response_time,p95_response_time,p99_response_time,request_count,failure_count,error_rate)VALUES(72,'2026-02-18 08:34:06',6,106.7,21,341.9,85.9,858.6,572.4,1144.8,27074,1037,1.76);

INSERT INTO performance_metric_samples(test_result_id,timestamp,elapsed_seconds,rps,active_users,avg_response_time,min_response_time,max_response_time,p95_response_time,p99_response_time,request_count,failure_count,error_rate)VALUES(72,'2026-02-18 08:34:07',7,79.1,15,302.2,85.9,858.6,572.4,1144.8,30942,1186,0.83);

INSERT INTO performance_test_results(id,scenario_id,project_id,user_count,spawn_rate,duration,target_url,status,started_at,finished_at,total_requests,total_failures,error_rate,rps,avg_response_time,min_response_time,max_response_time,p50_response_time,p75_response_time,p95_response_time,p99_response_time,created_at,updated_at)VALUES(73,17,16,48,5,543,'https://example.com/api','completed','2026-02-09 00:53:00','2026-02-09 01:02:03',5848,94,1.61,2337.0,174.3,52.3,871.5,122.0,226.6,435.8,697.2,'2026-02-09 00:53:00','2026-02-09 01:02:03')ON CONFLICT(id)DO NOTHING;

INSERT INTO performance_metric_samples(test_result_id,timestamp,elapsed_seconds,rps,active_users,avg_response_time,min_response_time,max_response_time,p95_response_time,p99_response_time,request_count,failure_count,error_rate)VALUES(73,'2026-02-09 00:53:00',0,2462.9,3,153.4,52.3,522.9,348.6,697.2,731,11,0.26);

INSERT INTO performance_metric_samples(test_result_id,timestamp,elapsed_seconds,rps,active_users,avg_response_time,min_response_time,max_response_time,p95_response_time,p99_response_time,request_count,failure_count,error_rate)VALUES(73,'2026-02-09 00:53:01',1,1979.8,6,177.5,52.3,522.9,348.6,697.2,1462,23,1.98);

INSERT INTO performance_metric_samples(test_result_id,timestamp,elapsed_seconds,rps,active_users,avg_response_time,min_response_time,max_response_time,p95_response_time,p99_response_time,request_count,failure_count,error_rate)VALUES(73,'2026-02-09 00:53:02',2,2416.5,9,187.5,52.3,522.9,348.6,697.2,2193,35,0.42);

INSERT INTO performance_metric_samples(test_result_id,timestamp,elapsed_seconds,rps,active_users,avg_response_time,min_response_time,max_response_time,p95_response_time,p99_response_time,request_count,failure_count,error_rate)VALUES(73,'2026-02-09 00:53:03',3,2715.5,12,189.0,52.3,522.9,348.6,697.2,2924,47,0.94);

INSERT INTO performance_metric_samples(test_result_id,timestamp,elapsed_seconds,rps,active_users,avg_response_time,min_response_time,max_response_time,p95_response_time,p99_response_time,request_count,failure_count,error_rate)VALUES(73,'2026-02-09 00:53:04',4,2832.6,15,170.5,52.3,522.9,348.6,697.2,3655,58,2.65);

INSERT INTO performance_metric_samples(test_result_id,timestamp,elapsed_seconds,rps,active_users,avg_response_time,min_response_time,max_response_time,p95_response_time,p99_response_time,request_count,failure_count,error_rate)VALUES(73,'2026-02-09 00:53:05',5,1894.1,18,155.3,52.3,522.9,348.6,697.2,4386,70,1.09);

INSERT INTO performance_metric_samples(test_result_id,timestamp,elapsed_seconds,rps,active_users,avg_response_time,min_response_time,max_response_time,p95_response_time,p99_response_time,request_count,failure_count,error_rate)VALUES(73,'2026-02-09 00:53:06',6,1914.9,21,157.5,52.3,522.9,348.6,697.2,5117,82,1.81);

INSERT INTO performance_metric_samples(test_result_id,timestamp,elapsed_seconds,rps,active_users,avg_response_time,min_response_time,max_response_time,p95_response_time,p99_response_time,request_count,failure_count,error_rate)VALUES(73,'2026-02-09 00:53:07',7,2943.7,24,147.7,52.3,522.9,348.6,697.2,5848,94,1.23);

INSERT INTO performance_test_results(id,scenario_id,project_id,user_count,spawn_rate,duration,target_url,status,started_at,finished_at,total_requests,total_failures,error_rate,rps,avg_response_time,min_response_time,max_response_time,p50_response_time,p75_response_time,p95_response_time,p99_response_time,created_at,updated_at)VALUES(74,17,16,139,11,109,'https://example.com/api','completed','2026-02-19 18:09:00','2026-02-19 18:10:49',34571,645,1.87,1718.9,398.3,119.5,1991.5,278.8,517.8,995.8,1593.2,'2026-02-19 18:09:00','2026-02-19 18:10:49')ON CONFLICT(id)DO NOTHING;

INSERT INTO performance_metric_samples(test_result_id,timestamp,elapsed_seconds,rps,active_users,avg_response_time,min_response_time,max_response_time,p95_response_time,p99_response_time,request_count,failure_count,error_rate)VALUES(74,'2026-02-19 18:09:00',0,2018.1,3,363.7,119.5,1194.9,796.6,1593.2,4321,80,1.0);

INSERT INTO performance_metric_samples(test_result_id,timestamp,elapsed_seconds,rps,active_users,avg_response_time,min_response_time,max_response_time,p95_response_time,p99_response_time,request_count,failure_count,error_rate)VALUES(74,'2026-02-19 18:09:01',1,1272.4,6,408.7,119.5,1194.9,796.6,1593.2,8642,161,2.92);

INSERT INTO performance_metric_samples(test_result_id,timestamp,elapsed_seconds,rps,active_users,avg_response_time,min_response_time,max_response_time,p95_response_time,p99_response_time,request_count,failure_count,error_rate)VALUES(74,'2026-02-19 18:09:02',2,2008.3,9,343.8,119.5,1194.9,796.6,1593.2,12964,241,1.54);

INSERT INTO performance_metric_samples(test_result_id,timestamp,elapsed_seconds,rps,active_users,avg_response_time,min_response_time,max_response_time,p95_response_time,p99_response_time,request_count,failure_count,error_rate)VALUES(74,'2026-02-19 18:09:03',3,2081.4,12,465.6,119.5,1194.9,796.6,1593.2,17285,322,1.83);

INSERT INTO performance_metric_samples(test_result_id,timestamp,elapsed_seconds,rps,active_users,avg_response_time,min_response_time,max_response_time,p95_response_time,p99_response_time,request_count,failure_count,error_rate)VALUES(74,'2026-02-19 18:09:04',4,2227.3,15,330.3,119.5,1194.9,796.6,1593.2,21606,403,2.05);

INSERT INTO performance_metric_samples(test_result_id,timestamp,elapsed_seconds,rps,active_users,avg_response_time,min_response_time,max_response_time,p95_response_time,p99_response_time,request_count,failure_count,error_rate)VALUES(74,'2026-02-19 18:09:05',5,2046.6,18,390.5,119.5,1194.9,796.6,1593.2,25928,483,2.64);

INSERT INTO performance_metric_samples(test_result_id,timestamp,elapsed_seconds,rps,active_users,avg_response_time,min_response_time,max_response_time,p95_response_time,p99_response_time,request_count,failure_count,error_rate)VALUES(74,'2026-02-19 18:09:06',6,1965.3,21,371.3,119.5,1194.9,796.6,1593.2,30249,564,0.55);

INSERT INTO performance_metric_samples(test_result_id,timestamp,elapsed_seconds,rps,active_users,avg_response_time,min_response_time,max_response_time,p95_response_time,p99_response_time,request_count,failure_count,error_rate)VALUES(74,'2026-02-19 18:09:07',7,1796.5,24,402.7,119.5,1194.9,796.6,1593.2,34571,645,2.08);

INSERT INTO performance_test_results(id,scenario_id,project_id,user_count,spawn_rate,duration,target_url,status,started_at,finished_at,total_requests,total_failures,error_rate,rps,avg_response_time,min_response_time,max_response_time,p50_response_time,p75_response_time,p95_response_time,p99_response_time,created_at,updated_at)VALUES(75,17,16,119,5,360,'https://example.com/api','completed','2026-02-11 09:35:00','2026-02-11 09:41:00',41874,1734,4.14,105.7,101.7,30.5,508.5,71.2,132.2,254.2,406.8,'2026-02-11 09:35:00','2026-02-11 09:41:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO performance_metric_samples(test_result_id,timestamp,elapsed_seconds,rps,active_users,avg_response_time,min_response_time,max_response_time,p95_response_time,p99_response_time,request_count,failure_count,error_rate)VALUES(75,'2026-02-11 09:35:00',0,90.4,3,105.1,30.5,305.1,203.4,406.8,5234,216,2.3);

INSERT INTO performance_metric_samples(test_result_id,timestamp,elapsed_seconds,rps,active_users,avg_response_time,min_response_time,max_response_time,p95_response_time,p99_response_time,request_count,failure_count,error_rate)VALUES(75,'2026-02-11 09:35:01',1,107.8,6,108.4,30.5,305.1,203.4,406.8,10468,433,2.31);

INSERT INTO performance_metric_samples(test_result_id,timestamp,elapsed_seconds,rps,active_users,avg_response_time,min_response_time,max_response_time,p95_response_time,p99_response_time,request_count,failure_count,error_rate)VALUES(75,'2026-02-11 09:35:02',2,110.4,9,117.7,30.5,305.1,203.4,406.8,15702,650,2.14);

INSERT INTO performance_metric_samples(test_result_id,timestamp,elapsed_seconds,rps,active_users,avg_response_time,min_response_time,max_response_time,p95_response_time,p99_response_time,request_count,failure_count,error_rate)VALUES(75,'2026-02-11 09:35:03',3,110.6,12,112.8,30.5,305.1,203.4,406.8,20937,867,0.62);

INSERT INTO performance_metric_samples(test_result_id,timestamp,elapsed_seconds,rps,active_users,avg_response_time,min_response_time,max_response_time,p95_response_time,p99_response_time,request_count,failure_count,error_rate)VALUES(75,'2026-02-11 09:35:04',4,85.5,7,103.1,30.5,305.1,203.4,406.8,26171,1083,2.83);

INSERT INTO performance_metric_samples(test_result_id,timestamp,elapsed_seconds,rps,active_users,avg_response_time,min_response_time,max_response_time,p95_response_time,p99_response_time,request_count,failure_count,error_rate)VALUES(75,'2026-02-11 09:35:05',5,76.5,18,103.3,30.5,305.1,203.4,406.8,31405,1300,2.86);

INSERT INTO performance_metric_samples(test_result_id,timestamp,elapsed_seconds,rps,active_users,avg_response_time,min_response_time,max_response_time,p95_response_time,p99_response_time,request_count,failure_count,error_rate)VALUES(75,'2026-02-11 09:35:06',6,94.8,21,119.1,30.5,305.1,203.4,406.8,36639,1517,1.97);

INSERT INTO performance_metric_samples(test_result_id,timestamp,elapsed_seconds,rps,active_users,avg_response_time,min_response_time,max_response_time,p95_response_time,p99_response_time,request_count,failure_count,error_rate)VALUES(75,'2026-02-11 09:35:07',7,86.8,24,98.6,30.5,305.1,203.4,406.8,41874,1734,0.81);

INSERT INTO performance_test_results(id,scenario_id,project_id,user_count,spawn_rate,duration,target_url,status,started_at,finished_at,total_requests,total_failures,error_rate,rps,avg_response_time,min_response_time,max_response_time,p50_response_time,p75_response_time,p95_response_time,p99_response_time,created_at,updated_at)VALUES(76,17,16,200,7,200,'https://example.com/api','failed','2026-04-06 22:59:00','2026-04-06 23:02:20',9068,378,4.17,1156.6,185.9,55.8,929.5,130.1,241.7,464.8,743.6,'2026-04-06 22:59:00','2026-04-06 23:02:20')ON CONFLICT(id)DO NOTHING;

INSERT INTO performance_metric_samples(test_result_id,timestamp,elapsed_seconds,rps,active_users,avg_response_time,min_response_time,max_response_time,p95_response_time,p99_response_time,request_count,failure_count,error_rate)VALUES(76,'2026-04-06 22:59:00',0,1073.6,3,181.3,55.8,557.7,371.8,743.6,1133,47,0.6);

INSERT INTO performance_metric_samples(test_result_id,timestamp,elapsed_seconds,rps,active_users,avg_response_time,min_response_time,max_response_time,p95_response_time,p99_response_time,request_count,failure_count,error_rate)VALUES(76,'2026-04-06 22:59:01',1,1344.7,6,209.3,55.8,557.7,371.8,743.6,2267,94,0.28);

INSERT INTO performance_metric_samples(test_result_id,timestamp,elapsed_seconds,rps,active_users,avg_response_time,min_response_time,max_response_time,p95_response_time,p99_response_time,request_count,failure_count,error_rate)VALUES(76,'2026-04-06 22:59:02',2,931.1,9,202.6,55.8,557.7,371.8,743.6,3400,141,0.37);

INSERT INTO performance_metric_samples(test_result_id,timestamp,elapsed_seconds,rps,active_users,avg_response_time,min_response_time,max_response_time,p95_response_time,p99_response_time,request_count,failure_count,error_rate)VALUES(76,'2026-04-06 22:59:03',3,1334.7,12,218.7,55.8,557.7,371.8,743.6,4534,189,2.22);

INSERT INTO performance_metric_samples(test_result_id,timestamp,elapsed_seconds,rps,active_users,avg_response_time,min_response_time,max_response_time,p95_response_time,p99_response_time,request_count,failure_count,error_rate)VALUES(76,'2026-04-06 22:59:04',4,1058.3,15,179.6,55.8,557.7,371.8,743.6,5667,236,0.63);

INSERT INTO performance_metric_samples(test_result_id,timestamp,elapsed_seconds,rps,active_users,avg_response_time,min_response_time,max_response_time,p95_response_time,p99_response_time,request_count,failure_count,error_rate)VALUES(76,'2026-04-06 22:59:05',5,872.6,18,175.5,55.8,557.7,371.8,743.6,6801,283,0.77);

INSERT INTO performance_metric_samples(test_result_id,timestamp,elapsed_seconds,rps,active_users,avg_response_time,min_response_time,max_response_time,p95_response_time,p99_response_time,request_count,failure_count,error_rate)VALUES(76,'2026-04-06 22:59:06',6,887.3,21,149.9,55.8,557.7,371.8,743.6,7934,330,1.14);

INSERT INTO performance_metric_samples(test_result_id,timestamp,elapsed_seconds,rps,active_users,avg_response_time,min_response_time,max_response_time,p95_response_time,p99_response_time,request_count,failure_count,error_rate)VALUES(76,'2026-04-06 22:59:07',7,1101.1,24,175.1,55.8,557.7,371.8,743.6,9068,378,2.84);

INSERT INTO performance_test_results(id,scenario_id,project_id,user_count,spawn_rate,duration,target_url,status,started_at,finished_at,total_requests,total_failures,error_rate,rps,avg_response_time,min_response_time,max_response_time,p50_response_time,p75_response_time,p95_response_time,p99_response_time,created_at,updated_at)VALUES(77,17,16,130,1,367,'https://example.com/api','completed','2026-05-15 20:06:00','2026-05-15 20:12:07',46954,198,0.42,1948.6,165.0,49.5,825.0,115.5,214.5,412.5,660.0,'2026-05-15 20:06:00','2026-05-15 20:12:07')ON CONFLICT(id)DO NOTHING;

INSERT INTO performance_metric_samples(test_result_id,timestamp,elapsed_seconds,rps,active_users,avg_response_time,min_response_time,max_response_time,p95_response_time,p99_response_time,request_count,failure_count,error_rate)VALUES(77,'2026-05-15 20:06:00',0,2476.3,3,180.2,49.5,495.0,330.0,660.0,5869,24,2.69);

INSERT INTO performance_metric_samples(test_result_id,timestamp,elapsed_seconds,rps,active_users,avg_response_time,min_response_time,max_response_time,p95_response_time,p99_response_time,request_count,failure_count,error_rate)VALUES(77,'2026-05-15 20:06:01',1,1417.1,6,143.7,49.5,495.0,330.0,660.0,11738,49,0.03);

INSERT INTO performance_metric_samples(test_result_id,timestamp,elapsed_seconds,rps,active_users,avg_response_time,min_response_time,max_response_time,p95_response_time,p99_response_time,request_count,failure_count,error_rate)VALUES(77,'2026-05-15 20:06:02',2,1970.4,9,177.9,49.5,495.0,330.0,660.0,17607,74,2.29);

INSERT INTO performance_metric_samples(test_result_id,timestamp,elapsed_seconds,rps,active_users,avg_response_time,min_response_time,max_response_time,p95_response_time,p99_response_time,request_count,failure_count,error_rate)VALUES(77,'2026-05-15 20:06:03',3,1435.6,12,189.2,49.5,495.0,330.0,660.0,23477,99,1.98);

INSERT INTO performance_metric_samples(test_result_id,timestamp,elapsed_seconds,rps,active_users,avg_response_time,min_response_time,max_response_time,p95_response_time,p99_response_time,request_count,failure_count,error_rate)VALUES(77,'2026-05-15 20:06:04',4,1798.6,15,186.3,49.5,495.0,330.0,660.0,29346,123,1.26);

INSERT INTO performance_metric_samples(test_result_id,timestamp,elapsed_seconds,rps,active_users,avg_response_time,min_response_time,max_response_time,p95_response_time,p99_response_time,request_count,failure_count,error_rate)VALUES(77,'2026-05-15 20:06:05',5,1568.2,18,195.7,49.5,495.0,330.0,660.0,35215,148,2.23);

INSERT INTO performance_metric_samples(test_result_id,timestamp,elapsed_seconds,rps,active_users,avg_response_time,min_response_time,max_response_time,p95_response_time,p99_response_time,request_count,failure_count,error_rate)VALUES(77,'2026-05-15 20:06:06',6,2311.4,21,156.1,49.5,495.0,330.0,660.0,41084,173,2.77);

INSERT INTO performance_metric_samples(test_result_id,timestamp,elapsed_seconds,rps,active_users,avg_response_time,min_response_time,max_response_time,p95_response_time,p99_response_time,request_count,failure_count,error_rate)VALUES(77,'2026-05-15 20:06:07',7,2283.6,8,164.8,49.5,495.0,330.0,660.0,46954,198,0.92);

INSERT INTO test_runs(id,project_id,test_type,test_object_name,status,total_cases,passed,failed,skipped,error,duration,started_at,finished_at,environment_name,triggered_by,triggered_user_id,created_at)VALUES(5,1,'api','性能压测','running',38,33,5,0,0,205.6,'2026-02-01 08:13:00',NULL,'开发环境','schedule',6,'2026-02-01 08:13:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO test_runs(id,project_id,test_type,test_object_name,status,total_cases,passed,failed,skipped,error,duration,started_at,finished_at,environment_name,triggered_by,triggered_user_id,created_at)VALUES(6,1,'web','UI自动化','failed',97,83,14,1,0,18.8,'2026-04-05 07:34:00','2026-04-05 07:34:18','测试环境','manual',1,'2026-04-05 07:34:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO test_runs(id,project_id,test_type,test_object_name,status,total_cases,passed,failed,skipped,error,duration,started_at,finished_at,environment_name,triggered_by,triggered_user_id,created_at)VALUES(7,1,'web','冒烟测试','running',73,60,13,0,1,291.0,'2026-03-28 05:40:00',NULL,'预发布','ci',7,'2026-03-28 05:40:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO test_runs(id,project_id,test_type,test_object_name,status,total_cases,passed,failed,skipped,error,duration,started_at,finished_at,environment_name,triggered_by,triggered_user_id,created_at)VALUES(8,1,'web','UI自动化','success',78,59,19,1,2,86.6,'2026-04-26 02:18:00','2026-04-26 02:19:26','预发布','manual',1,'2026-04-26 02:18:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO test_runs(id,project_id,test_type,test_object_name,status,total_cases,passed,failed,skipped,error,duration,started_at,finished_at,environment_name,triggered_by,triggered_user_id,created_at)VALUES(9,1,'api','性能压测','running',18,13,5,2,0,440.7,'2026-03-15 23:15:00',NULL,'预发布','trigger',7,'2026-03-15 23:15:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO test_runs(id,project_id,test_type,test_object_name,status,total_cases,passed,failed,skipped,error,duration,started_at,finished_at,environment_name,triggered_by,triggered_user_id,created_at)VALUES(10,1,'web','冒烟测试','cancelled',39,36,3,1,1,259.0,'2025-12-14 05:23:00','2025-12-14 05:27:19','预发布','manual',6,'2025-12-14 05:23:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO test_runs(id,project_id,test_type,test_object_name,status,total_cases,passed,failed,skipped,error,duration,started_at,finished_at,environment_name,triggered_by,triggered_user_id,created_at)VALUES(11,1,'api','回归测试','cancelled',6,4,2,0,0,105.5,'2026-03-11 09:24:00','2026-03-11 09:25:45','测试环境','trigger',6,'2026-03-11 09:24:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO test_runs(id,project_id,test_type,test_object_name,status,total_cases,passed,failed,skipped,error,duration,started_at,finished_at,environment_name,triggered_by,triggered_user_id,created_at)VALUES(12,1,'performance','接口自动化','running',78,64,14,1,1,376.6,'2026-01-12 19:53:00',NULL,'测试环境','ci',7,'2026-01-12 19:53:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO test_runs(id,project_id,test_type,test_object_name,status,total_cases,passed,failed,skipped,error,duration,started_at,finished_at,environment_name,triggered_by,triggered_user_id,created_at)VALUES(13,1,'api','冒烟测试','success',67,62,5,3,2,66.9,'2026-03-05 17:44:00','2026-03-05 17:45:06','测试环境','manual',5,'2026-03-05 17:44:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO test_runs(id,project_id,test_type,test_object_name,status,total_cases,passed,failed,skipped,error,duration,started_at,finished_at,environment_name,triggered_by,triggered_user_id,created_at)VALUES(14,1,'web','UI自动化','success',34,33,1,0,0,334.8,'2026-03-18 05:05:00','2026-03-18 05:10:34','测试环境','ci',5,'2026-03-18 05:05:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO test_runs(id,project_id,test_type,test_object_name,status,total_cases,passed,failed,skipped,error,duration,started_at,finished_at,environment_name,triggered_by,triggered_user_id,created_at)VALUES(15,1,'web','接口自动化','cancelled',15,14,1,1,1,493.8,'2026-01-22 03:51:00','2026-01-22 03:59:13','开发环境','schedule',1,'2026-01-22 03:51:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO test_runs(id,project_id,test_type,test_object_name,status,total_cases,passed,failed,skipped,error,duration,started_at,finished_at,environment_name,triggered_by,triggered_user_id,created_at)VALUES(16,1,'web','冒烟测试','success',24,20,4,0,2,224.0,'2026-04-03 11:27:00','2026-04-03 11:30:44','开发环境','schedule',5,'2026-04-03 11:27:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO test_runs(id,project_id,test_type,test_object_name,status,total_cases,passed,failed,skipped,error,duration,started_at,finished_at,environment_name,triggered_by,triggered_user_id,created_at)VALUES(17,1,'performance','UI自动化','success',86,82,4,1,2,99.7,'2025-12-26 20:06:00','2025-12-26 20:07:39','开发环境','schedule',5,'2025-12-26 20:06:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO test_runs(id,project_id,test_type,test_object_name,status,total_cases,passed,failed,skipped,error,duration,started_at,finished_at,environment_name,triggered_by,triggered_user_id,created_at)VALUES(18,1,'api','接口自动化','success',71,70,1,3,1,199.9,'2026-03-17 09:56:00','2026-03-17 09:59:19','预发布','ci',7,'2026-03-17 09:56:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO test_runs(id,project_id,test_type,test_object_name,status,total_cases,passed,failed,skipped,error,duration,started_at,finished_at,environment_name,triggered_by,triggered_user_id,created_at)VALUES(19,1,'api','回归测试','pending',83,72,11,0,0,455.6,'2026-04-27 05:30:00',NULL,'测试环境','schedule',2,'2026-04-27 05:30:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO test_runs(id,project_id,test_type,test_object_name,status,total_cases,passed,failed,skipped,error,duration,started_at,finished_at,environment_name,triggered_by,triggered_user_id,created_at)VALUES(20,1,'performance','性能压测','success',80,60,20,2,0,143.5,'2026-03-23 05:03:00','2026-03-23 05:05:23','预发布','trigger',1,'2026-03-23 05:03:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO test_runs(id,project_id,test_type,test_object_name,status,total_cases,passed,failed,skipped,error,duration,started_at,finished_at,environment_name,triggered_by,triggered_user_id,created_at)VALUES(21,1,'performance','回归测试','success',61,45,16,2,1,16.4,'2026-05-01 17:41:00','2026-05-01 17:41:16','测试环境','manual',7,'2026-05-01 17:41:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO test_runs(id,project_id,test_type,test_object_name,status,total_cases,passed,failed,skipped,error,duration,started_at,finished_at,environment_name,triggered_by,triggered_user_id,created_at)VALUES(22,1,'performance','UI自动化','success',20,17,3,3,0,51.5,'2026-03-06 01:58:00','2026-03-06 01:58:51','开发环境','trigger',5,'2026-03-06 01:58:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO test_runs(id,project_id,test_type,test_object_name,status,total_cases,passed,failed,skipped,error,duration,started_at,finished_at,environment_name,triggered_by,triggered_user_id,created_at)VALUES(23,2,'web','UI自动化','success',95,86,9,3,1,142.5,'2026-05-06 07:14:00','2026-05-06 07:16:22','预发布','ci',2,'2026-05-06 07:14:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO test_runs(id,project_id,test_type,test_object_name,status,total_cases,passed,failed,skipped,error,duration,started_at,finished_at,environment_name,triggered_by,triggered_user_id,created_at)VALUES(24,2,'performance','接口自动化','pending',58,41,17,0,1,507.0,'2026-03-23 01:20:00',NULL,'预发布','ci',6,'2026-03-23 01:20:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO test_runs(id,project_id,test_type,test_object_name,status,total_cases,passed,failed,skipped,error,duration,started_at,finished_at,environment_name,triggered_by,triggered_user_id,created_at)VALUES(25,2,'api','UI自动化','success',17,15,2,3,0,355.6,'2026-04-05 15:33:00','2026-04-05 15:38:55','预发布','ci',1,'2026-04-05 15:33:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO test_runs(id,project_id,test_type,test_object_name,status,total_cases,passed,failed,skipped,error,duration,started_at,finished_at,environment_name,triggered_by,triggered_user_id,created_at)VALUES(26,2,'web','接口自动化','success',77,62,15,3,0,365.0,'2025-12-31 13:54:00','2025-12-31 14:00:05','开发环境','manual',1,'2025-12-31 13:54:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO test_runs(id,project_id,test_type,test_object_name,status,total_cases,passed,failed,skipped,error,duration,started_at,finished_at,environment_name,triggered_by,triggered_user_id,created_at)VALUES(27,2,'web','性能压测','failed',82,67,15,3,2,449.1,'2026-03-04 13:10:00','2026-03-04 13:17:29','预发布','trigger',6,'2026-03-04 13:10:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO test_runs(id,project_id,test_type,test_object_name,status,total_cases,passed,failed,skipped,error,duration,started_at,finished_at,environment_name,triggered_by,triggered_user_id,created_at)VALUES(28,2,'api','接口自动化','pending',85,78,7,3,2,545.8,'2026-04-06 15:49:00',NULL,'开发环境','manual',5,'2026-04-06 15:49:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO test_runs(id,project_id,test_type,test_object_name,status,total_cases,passed,failed,skipped,error,duration,started_at,finished_at,environment_name,triggered_by,triggered_user_id,created_at)VALUES(29,2,'web','接口自动化','failed',98,82,16,2,1,492.8,'2026-03-04 22:45:00','2026-03-04 22:53:12','开发环境','ci',6,'2026-03-04 22:45:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO test_runs(id,project_id,test_type,test_object_name,status,total_cases,passed,failed,skipped,error,duration,started_at,finished_at,environment_name,triggered_by,triggered_user_id,created_at)VALUES(30,2,'web','UI自动化','failed',86,66,20,1,0,339.5,'2026-01-11 13:40:00','2026-01-11 13:45:39','开发环境','trigger',5,'2026-01-11 13:40:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO test_runs(id,project_id,test_type,test_object_name,status,total_cases,passed,failed,skipped,error,duration,started_at,finished_at,environment_name,triggered_by,triggered_user_id,created_at)VALUES(31,2,'api','UI自动化','success',83,71,12,1,1,498.9,'2026-05-06 10:55:00','2026-05-06 11:03:18','预发布','trigger',5,'2026-05-06 10:55:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO test_runs(id,project_id,test_type,test_object_name,status,total_cases,passed,failed,skipped,error,duration,started_at,finished_at,environment_name,triggered_by,triggered_user_id,created_at)VALUES(32,2,'performance','冒烟测试','success',53,40,13,3,1,208.8,'2026-02-08 22:12:00','2026-02-08 22:15:28','测试环境','schedule',2,'2026-02-08 22:12:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO test_runs(id,project_id,test_type,test_object_name,status,total_cases,passed,failed,skipped,error,duration,started_at,finished_at,environment_name,triggered_by,triggered_user_id,created_at)VALUES(33,2,'api','冒烟测试','success',44,42,2,2,2,327.6,'2026-02-19 14:16:00','2026-02-19 14:21:27','开发环境','manual',2,'2026-02-19 14:16:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO test_runs(id,project_id,test_type,test_object_name,status,total_cases,passed,failed,skipped,error,duration,started_at,finished_at,environment_name,triggered_by,triggered_user_id,created_at)VALUES(34,2,'performance','接口自动化','success',89,73,16,2,0,432.4,'2026-01-15 22:35:00','2026-01-15 22:42:12','开发环境','schedule',6,'2026-01-15 22:35:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO test_runs(id,project_id,test_type,test_object_name,status,total_cases,passed,failed,skipped,error,duration,started_at,finished_at,environment_name,triggered_by,triggered_user_id,created_at)VALUES(35,2,'web','回归测试','success',15,11,4,1,1,497.4,'2026-03-30 16:51:00','2026-03-30 16:59:17','测试环境','ci',1,'2026-03-30 16:51:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO test_runs(id,project_id,test_type,test_object_name,status,total_cases,passed,failed,skipped,error,duration,started_at,finished_at,environment_name,triggered_by,triggered_user_id,created_at)VALUES(36,2,'performance','UI自动化','cancelled',36,34,2,3,2,488.8,'2026-04-25 09:42:00','2026-04-25 09:50:08','预发布','schedule',1,'2026-04-25 09:42:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO test_runs(id,project_id,test_type,test_object_name,status,total_cases,passed,failed,skipped,error,duration,started_at,finished_at,environment_name,triggered_by,triggered_user_id,created_at)VALUES(37,3,'web','接口自动化','success',77,58,19,1,2,352.7,'2025-12-22 15:04:00','2025-12-22 15:09:52','预发布','trigger',5,'2025-12-22 15:04:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO test_runs(id,project_id,test_type,test_object_name,status,total_cases,passed,failed,skipped,error,duration,started_at,finished_at,environment_name,triggered_by,triggered_user_id,created_at)VALUES(38,3,'api','性能压测','success',51,49,2,1,1,328.8,'2026-05-12 11:52:00','2026-05-12 11:57:28','预发布','ci',2,'2026-05-12 11:52:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO test_runs(id,project_id,test_type,test_object_name,status,total_cases,passed,failed,skipped,error,duration,started_at,finished_at,environment_name,triggered_by,triggered_user_id,created_at)VALUES(39,3,'api','UI自动化','success',69,62,7,2,0,486.3,'2025-12-29 02:14:00','2025-12-29 02:22:06','开发环境','ci',7,'2025-12-29 02:14:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO test_runs(id,project_id,test_type,test_object_name,status,total_cases,passed,failed,skipped,error,duration,started_at,finished_at,environment_name,triggered_by,triggered_user_id,created_at)VALUES(40,3,'api','冒烟测试','success',11,9,2,3,1,358.7,'2026-05-16 04:59:00','2026-05-16 05:04:58','预发布','trigger',7,'2026-05-16 04:59:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO test_runs(id,project_id,test_type,test_object_name,status,total_cases,passed,failed,skipped,error,duration,started_at,finished_at,environment_name,triggered_by,triggered_user_id,created_at)VALUES(41,3,'api','UI自动化','success',95,70,25,2,0,573.3,'2026-03-22 15:44:00','2026-03-22 15:53:33','测试环境','manual',7,'2026-03-22 15:44:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO test_runs(id,project_id,test_type,test_object_name,status,total_cases,passed,failed,skipped,error,duration,started_at,finished_at,environment_name,triggered_by,triggered_user_id,created_at)VALUES(42,3,'performance','性能压测','failed',22,21,1,1,2,276.7,'2026-01-14 11:17:00','2026-01-14 11:21:36','开发环境','ci',5,'2026-01-14 11:17:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO test_runs(id,project_id,test_type,test_object_name,status,total_cases,passed,failed,skipped,error,duration,started_at,finished_at,environment_name,triggered_by,triggered_user_id,created_at)VALUES(43,3,'web','冒烟测试','pending',23,21,2,2,0,582.8,'2026-05-18 11:12:00',NULL,'开发环境','ci',7,'2026-05-18 11:12:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO test_runs(id,project_id,test_type,test_object_name,status,total_cases,passed,failed,skipped,error,duration,started_at,finished_at,environment_name,triggered_by,triggered_user_id,created_at)VALUES(44,3,'web','冒烟测试','success',57,52,5,1,0,588.1,'2026-04-17 04:59:00','2026-04-17 05:08:48','测试环境','trigger',1,'2026-04-17 04:59:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO test_runs(id,project_id,test_type,test_object_name,status,total_cases,passed,failed,skipped,error,duration,started_at,finished_at,environment_name,triggered_by,triggered_user_id,created_at)VALUES(45,3,'api','接口自动化','pending',78,71,7,3,1,235.0,'2026-01-31 05:06:00',NULL,'开发环境','ci',2,'2026-01-31 05:06:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO test_runs(id,project_id,test_type,test_object_name,status,total_cases,passed,failed,skipped,error,duration,started_at,finished_at,environment_name,triggered_by,triggered_user_id,created_at)VALUES(46,3,'api','UI自动化','success',60,57,3,3,0,118.9,'2026-02-19 03:46:00','2026-02-19 03:47:58','测试环境','ci',1,'2026-02-19 03:46:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO test_runs(id,project_id,test_type,test_object_name,status,total_cases,passed,failed,skipped,error,duration,started_at,finished_at,environment_name,triggered_by,triggered_user_id,created_at)VALUES(47,3,'api','冒烟测试','success',7,6,1,0,2,44.9,'2026-02-26 06:50:00','2026-02-26 06:50:44','开发环境','manual',7,'2026-02-26 06:50:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO test_runs(id,project_id,test_type,test_object_name,status,total_cases,passed,failed,skipped,error,duration,started_at,finished_at,environment_name,triggered_by,triggered_user_id,created_at)VALUES(48,3,'api','回归测试','success',8,7,1,2,0,573.9,'2026-04-13 13:21:00','2026-04-13 13:30:33','预发布','trigger',2,'2026-04-13 13:21:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO test_runs(id,project_id,test_type,test_object_name,status,total_cases,passed,failed,skipped,error,duration,started_at,finished_at,environment_name,triggered_by,triggered_user_id,created_at)VALUES(49,3,'api','UI自动化','success',92,89,3,2,2,114.4,'2026-02-08 11:06:00','2026-02-08 11:07:54','开发环境','schedule',7,'2026-02-08 11:06:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO test_runs(id,project_id,test_type,test_object_name,status,total_cases,passed,failed,skipped,error,duration,started_at,finished_at,environment_name,triggered_by,triggered_user_id,created_at)VALUES(50,3,'api','回归测试','success',73,70,3,0,1,561.7,'2026-05-04 22:17:00','2026-05-04 22:26:21','预发布','schedule',7,'2026-05-04 22:17:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO test_runs(id,project_id,test_type,test_object_name,status,total_cases,passed,failed,skipped,error,duration,started_at,finished_at,environment_name,triggered_by,triggered_user_id,created_at)VALUES(51,3,'api','性能压测','success',82,61,21,2,1,557.9,'2026-01-11 21:10:00','2026-01-11 21:19:17','预发布','trigger',1,'2026-01-11 21:10:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO test_runs(id,project_id,test_type,test_object_name,status,total_cases,passed,failed,skipped,error,duration,started_at,finished_at,environment_name,triggered_by,triggered_user_id,created_at)VALUES(52,4,'api','性能压测','success',23,17,6,3,0,478.5,'2026-05-21 22:57:00','2026-05-21 23:04:58','开发环境','trigger',7,'2026-05-21 22:57:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO test_runs(id,project_id,test_type,test_object_name,status,total_cases,passed,failed,skipped,error,duration,started_at,finished_at,environment_name,triggered_by,triggered_user_id,created_at)VALUES(53,4,'api','UI自动化','failed',46,44,2,3,2,389.5,'2026-03-20 23:52:00','2026-03-20 23:58:29','测试环境','trigger',2,'2026-03-20 23:52:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO test_runs(id,project_id,test_type,test_object_name,status,total_cases,passed,failed,skipped,error,duration,started_at,finished_at,environment_name,triggered_by,triggered_user_id,created_at)VALUES(54,4,'web','冒烟测试','success',15,12,3,3,0,199.7,'2026-01-28 14:36:00','2026-01-28 14:39:19','测试环境','ci',6,'2026-01-28 14:36:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO test_runs(id,project_id,test_type,test_object_name,status,total_cases,passed,failed,skipped,error,duration,started_at,finished_at,environment_name,triggered_by,triggered_user_id,created_at)VALUES(55,4,'web','冒烟测试','failed',29,28,1,2,2,451.2,'2026-01-05 16:49:00','2026-01-05 16:56:31','预发布','ci',1,'2026-01-05 16:49:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO test_runs(id,project_id,test_type,test_object_name,status,total_cases,passed,failed,skipped,error,duration,started_at,finished_at,environment_name,triggered_by,triggered_user_id,created_at)VALUES(56,4,'api','冒烟测试','pending',54,40,14,0,2,525.5,'2026-01-21 17:06:00',NULL,'测试环境','schedule',7,'2026-01-21 17:06:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO test_runs(id,project_id,test_type,test_object_name,status,total_cases,passed,failed,skipped,error,duration,started_at,finished_at,environment_name,triggered_by,triggered_user_id,created_at)VALUES(57,4,'api','回归测试','success',28,27,1,2,0,431.3,'2026-01-26 03:24:00','2026-01-26 03:31:11','测试环境','manual',1,'2026-01-26 03:24:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO test_runs(id,project_id,test_type,test_object_name,status,total_cases,passed,failed,skipped,error,duration,started_at,finished_at,environment_name,triggered_by,triggered_user_id,created_at)VALUES(58,4,'performance','冒烟测试','success',42,29,13,1,2,490.0,'2026-03-09 04:36:00','2026-03-09 04:44:10','测试环境','schedule',5,'2026-03-09 04:36:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO test_runs(id,project_id,test_type,test_object_name,status,total_cases,passed,failed,skipped,error,duration,started_at,finished_at,environment_name,triggered_by,triggered_user_id,created_at)VALUES(59,4,'api','冒烟测试','success',36,31,5,2,1,411.4,'2025-12-23 00:47:00','2025-12-23 00:53:51','预发布','ci',6,'2025-12-23 00:47:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO test_runs(id,project_id,test_type,test_object_name,status,total_cases,passed,failed,skipped,error,duration,started_at,finished_at,environment_name,triggered_by,triggered_user_id,created_at)VALUES(60,4,'web','UI自动化','failed',53,41,12,1,1,159.5,'2026-05-29 13:16:00','2026-05-29 13:18:39','预发布','trigger',1,'2026-05-29 13:16:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO test_runs(id,project_id,test_type,test_object_name,status,total_cases,passed,failed,skipped,error,duration,started_at,finished_at,environment_name,triggered_by,triggered_user_id,created_at)VALUES(61,5,'performance','接口自动化','failed',14,12,2,0,0,542.3,'2026-01-27 07:49:00','2026-01-27 07:58:02','预发布','ci',2,'2026-01-27 07:49:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO test_runs(id,project_id,test_type,test_object_name,status,total_cases,passed,failed,skipped,error,duration,started_at,finished_at,environment_name,triggered_by,triggered_user_id,created_at)VALUES(62,5,'performance','冒烟测试','failed',93,76,17,2,1,514.7,'2026-03-27 06:12:00','2026-03-27 06:20:34','开发环境','manual',6,'2026-03-27 06:12:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO test_runs(id,project_id,test_type,test_object_name,status,total_cases,passed,failed,skipped,error,duration,started_at,finished_at,environment_name,triggered_by,triggered_user_id,created_at)VALUES(63,5,'web','冒烟测试','failed',30,22,8,0,1,292.5,'2026-05-04 02:58:00','2026-05-04 03:02:52','开发环境','trigger',2,'2026-05-04 02:58:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO test_runs(id,project_id,test_type,test_object_name,status,total_cases,passed,failed,skipped,error,duration,started_at,finished_at,environment_name,triggered_by,triggered_user_id,created_at)VALUES(64,5,'api','接口自动化','success',52,43,9,1,1,362.2,'2026-05-21 12:01:00','2026-05-21 12:07:02','预发布','schedule',2,'2026-05-21 12:01:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO test_runs(id,project_id,test_type,test_object_name,status,total_cases,passed,failed,skipped,error,duration,started_at,finished_at,environment_name,triggered_by,triggered_user_id,created_at)VALUES(65,5,'api','接口自动化','success',24,19,5,2,0,216.6,'2026-04-10 13:57:00','2026-04-10 14:00:36','开发环境','trigger',6,'2026-04-10 13:57:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO test_runs(id,project_id,test_type,test_object_name,status,total_cases,passed,failed,skipped,error,duration,started_at,finished_at,environment_name,triggered_by,triggered_user_id,created_at)VALUES(66,5,'web','接口自动化','success',28,24,4,2,2,435.5,'2026-05-25 19:56:00','2026-05-25 20:03:15','预发布','schedule',7,'2026-05-25 19:56:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO test_runs(id,project_id,test_type,test_object_name,status,total_cases,passed,failed,skipped,error,duration,started_at,finished_at,environment_name,triggered_by,triggered_user_id,created_at)VALUES(67,5,'web','回归测试','success',75,74,1,0,0,414.0,'2026-02-16 17:26:00','2026-02-16 17:32:54','预发布','manual',7,'2026-02-16 17:26:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO test_runs(id,project_id,test_type,test_object_name,status,total_cases,passed,failed,skipped,error,duration,started_at,finished_at,environment_name,triggered_by,triggered_user_id,created_at)VALUES(68,5,'performance','冒烟测试','pending',52,36,16,0,2,147.9,'2026-02-24 09:24:00',NULL,'预发布','manual',6,'2026-02-24 09:24:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO test_runs(id,project_id,test_type,test_object_name,status,total_cases,passed,failed,skipped,error,duration,started_at,finished_at,environment_name,triggered_by,triggered_user_id,created_at)VALUES(69,5,'api','性能压测','failed',9,7,2,0,0,392.8,'2026-01-30 15:19:00','2026-01-30 15:25:32','预发布','trigger',5,'2026-01-30 15:19:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO test_runs(id,project_id,test_type,test_object_name,status,total_cases,passed,failed,skipped,error,duration,started_at,finished_at,environment_name,triggered_by,triggered_user_id,created_at)VALUES(70,5,'web','接口自动化','success',100,77,23,3,2,157.5,'2025-12-20 19:30:00','2025-12-20 19:32:37','预发布','schedule',6,'2025-12-20 19:30:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO test_runs(id,project_id,test_type,test_object_name,status,total_cases,passed,failed,skipped,error,duration,started_at,finished_at,environment_name,triggered_by,triggered_user_id,created_at)VALUES(71,6,'api','冒烟测试','success',98,73,25,3,1,530.3,'2026-02-26 10:59:00','2026-02-26 11:07:50','开发环境','trigger',5,'2026-02-26 10:59:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO test_runs(id,project_id,test_type,test_object_name,status,total_cases,passed,failed,skipped,error,duration,started_at,finished_at,environment_name,triggered_by,triggered_user_id,created_at)VALUES(72,6,'web','UI自动化','success',74,70,4,3,0,505.7,'2026-03-03 03:35:00','2026-03-03 03:43:25','测试环境','trigger',6,'2026-03-03 03:35:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO test_runs(id,project_id,test_type,test_object_name,status,total_cases,passed,failed,skipped,error,duration,started_at,finished_at,environment_name,triggered_by,triggered_user_id,created_at)VALUES(73,6,'web','回归测试','pending',64,51,13,2,2,245.3,'2026-01-17 03:45:00',NULL,'预发布','schedule',2,'2026-01-17 03:45:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO test_runs(id,project_id,test_type,test_object_name,status,total_cases,passed,failed,skipped,error,duration,started_at,finished_at,environment_name,triggered_by,triggered_user_id,created_at)VALUES(74,6,'performance','回归测试','failed',84,67,17,3,2,518.8,'2026-02-16 22:19:00','2026-02-16 22:27:38','测试环境','ci',2,'2026-02-16 22:19:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO test_runs(id,project_id,test_type,test_object_name,status,total_cases,passed,failed,skipped,error,duration,started_at,finished_at,environment_name,triggered_by,triggered_user_id,created_at)VALUES(75,6,'web','UI自动化','success',88,73,15,3,0,127.7,'2026-03-06 16:04:00','2026-03-06 16:06:07','预发布','schedule',6,'2026-03-06 16:04:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO test_runs(id,project_id,test_type,test_object_name,status,total_cases,passed,failed,skipped,error,duration,started_at,finished_at,environment_name,triggered_by,triggered_user_id,created_at)VALUES(76,6,'api','回归测试','pending',8,7,1,3,2,403.5,'2026-03-23 10:17:00',NULL,'预发布','schedule',6,'2026-03-23 10:17:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO test_runs(id,project_id,test_type,test_object_name,status,total_cases,passed,failed,skipped,error,duration,started_at,finished_at,environment_name,triggered_by,triggered_user_id,created_at)VALUES(77,6,'api','冒烟测试','success',64,49,15,1,1,196.6,'2025-12-26 17:13:00','2025-12-26 17:16:16','开发环境','manual',1,'2025-12-26 17:13:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO test_runs(id,project_id,test_type,test_object_name,status,total_cases,passed,failed,skipped,error,duration,started_at,finished_at,environment_name,triggered_by,triggered_user_id,created_at)VALUES(78,6,'api','冒烟测试','success',11,8,3,0,1,559.6,'2026-03-02 03:13:00','2026-03-02 03:22:19','测试环境','schedule',2,'2026-03-02 03:13:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO test_runs(id,project_id,test_type,test_object_name,status,total_cases,passed,failed,skipped,error,duration,started_at,finished_at,environment_name,triggered_by,triggered_user_id,created_at)VALUES(79,6,'api','回归测试','success',45,39,6,3,1,209.8,'2026-04-18 00:41:00','2026-04-18 00:44:29','开发环境','manual',7,'2026-04-18 00:41:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO test_runs(id,project_id,test_type,test_object_name,status,total_cases,passed,failed,skipped,error,duration,started_at,finished_at,environment_name,triggered_by,triggered_user_id,created_at)VALUES(80,6,'api','回归测试','success',73,71,2,3,0,341.4,'2025-12-22 18:16:00','2025-12-22 18:21:41','开发环境','ci',2,'2025-12-22 18:16:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO test_runs(id,project_id,test_type,test_object_name,status,total_cases,passed,failed,skipped,error,duration,started_at,finished_at,environment_name,triggered_by,triggered_user_id,created_at)VALUES(81,6,'web','性能压测','success',10,7,3,3,1,233.8,'2026-04-19 09:23:00','2026-04-19 09:26:53','预发布','ci',6,'2026-04-19 09:23:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO test_runs(id,project_id,test_type,test_object_name,status,total_cases,passed,failed,skipped,error,duration,started_at,finished_at,environment_name,triggered_by,triggered_user_id,created_at)VALUES(82,7,'web','UI自动化','running',67,65,2,2,1,592.8,'2026-02-27 07:49:00',NULL,'测试环境','schedule',7,'2026-02-27 07:49:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO test_runs(id,project_id,test_type,test_object_name,status,total_cases,passed,failed,skipped,error,duration,started_at,finished_at,environment_name,triggered_by,triggered_user_id,created_at)VALUES(83,7,'api','性能压测','success',90,68,22,2,1,429.7,'2026-05-10 22:22:00','2026-05-10 22:29:09','预发布','trigger',1,'2026-05-10 22:22:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO test_runs(id,project_id,test_type,test_object_name,status,total_cases,passed,failed,skipped,error,duration,started_at,finished_at,environment_name,triggered_by,triggered_user_id,created_at)VALUES(84,7,'web','回归测试','cancelled',51,48,3,1,2,175.3,'2026-01-19 09:29:00','2026-01-19 09:31:55','开发环境','ci',2,'2026-01-19 09:29:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO test_runs(id,project_id,test_type,test_object_name,status,total_cases,passed,failed,skipped,error,duration,started_at,finished_at,environment_name,triggered_by,triggered_user_id,created_at)VALUES(85,7,'performance','冒烟测试','success',62,61,1,2,0,171.0,'2025-12-14 19:18:00','2025-12-14 19:20:51','预发布','manual',5,'2025-12-14 19:18:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO test_runs(id,project_id,test_type,test_object_name,status,total_cases,passed,failed,skipped,error,duration,started_at,finished_at,environment_name,triggered_by,triggered_user_id,created_at)VALUES(86,7,'api','UI自动化','running',84,59,25,0,1,234.6,'2026-01-31 21:36:00',NULL,'预发布','manual',5,'2026-01-31 21:36:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO test_runs(id,project_id,test_type,test_object_name,status,total_cases,passed,failed,skipped,error,duration,started_at,finished_at,environment_name,triggered_by,triggered_user_id,created_at)VALUES(87,7,'api','UI自动化','success',70,66,4,3,1,427.3,'2026-04-28 22:14:00','2026-04-28 22:21:07','开发环境','ci',7,'2026-04-28 22:14:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO test_runs(id,project_id,test_type,test_object_name,status,total_cases,passed,failed,skipped,error,duration,started_at,finished_at,environment_name,triggered_by,triggered_user_id,created_at)VALUES(88,7,'api','冒烟测试','success',62,60,2,0,2,548.9,'2026-01-22 06:59:00','2026-01-22 07:08:08','开发环境','schedule',1,'2026-01-22 06:59:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO test_runs(id,project_id,test_type,test_object_name,status,total_cases,passed,failed,skipped,error,duration,started_at,finished_at,environment_name,triggered_by,triggered_user_id,created_at)VALUES(89,7,'api','回归测试','success',24,20,4,1,0,519.6,'2026-05-29 11:00:00','2026-05-29 11:08:39','开发环境','ci',7,'2026-05-29 11:00:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO test_runs(id,project_id,test_type,test_object_name,status,total_cases,passed,failed,skipped,error,duration,started_at,finished_at,environment_name,triggered_by,triggered_user_id,created_at)VALUES(90,7,'web','冒烟测试','success',63,56,7,2,2,72.4,'2026-05-01 08:15:00','2026-05-01 08:16:12','预发布','schedule',2,'2026-05-01 08:15:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO test_runs(id,project_id,test_type,test_object_name,status,total_cases,passed,failed,skipped,error,duration,started_at,finished_at,environment_name,triggered_by,triggered_user_id,created_at)VALUES(91,7,'api','UI自动化','success',16,11,5,1,0,39.5,'2026-05-11 21:40:00','2026-05-11 21:40:39','开发环境','schedule',6,'2026-05-11 21:40:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO test_runs(id,project_id,test_type,test_object_name,status,total_cases,passed,failed,skipped,error,duration,started_at,finished_at,environment_name,triggered_by,triggered_user_id,created_at)VALUES(92,8,'performance','性能压测','success',41,37,4,0,1,119.1,'2026-05-31 07:49:00','2026-05-31 07:50:59','开发环境','schedule',5,'2026-05-31 07:49:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO test_runs(id,project_id,test_type,test_object_name,status,total_cases,passed,failed,skipped,error,duration,started_at,finished_at,environment_name,triggered_by,triggered_user_id,created_at)VALUES(93,8,'web','性能压测','cancelled',94,69,25,0,0,120.4,'2026-03-11 02:50:00','2026-03-11 02:52:00','测试环境','trigger',7,'2026-03-11 02:50:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO test_runs(id,project_id,test_type,test_object_name,status,total_cases,passed,failed,skipped,error,duration,started_at,finished_at,environment_name,triggered_by,triggered_user_id,created_at)VALUES(94,8,'web','冒烟测试','success',41,31,10,2,1,443.9,'2026-01-17 09:19:00','2026-01-17 09:26:23','开发环境','ci',5,'2026-01-17 09:19:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO test_runs(id,project_id,test_type,test_object_name,status,total_cases,passed,failed,skipped,error,duration,started_at,finished_at,environment_name,triggered_by,triggered_user_id,created_at)VALUES(95,8,'api','冒烟测试','success',49,47,2,0,2,455.8,'2026-02-11 07:17:00','2026-02-11 07:24:35','预发布','trigger',1,'2026-02-11 07:17:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO test_runs(id,project_id,test_type,test_object_name,status,total_cases,passed,failed,skipped,error,duration,started_at,finished_at,environment_name,triggered_by,triggered_user_id,created_at)VALUES(96,8,'api','接口自动化','success',51,46,5,0,2,164.8,'2026-03-11 19:38:00','2026-03-11 19:40:44','测试环境','trigger',5,'2026-03-11 19:38:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO test_runs(id,project_id,test_type,test_object_name,status,total_cases,passed,failed,skipped,error,duration,started_at,finished_at,environment_name,triggered_by,triggered_user_id,created_at)VALUES(97,8,'web','UI自动化','success',100,75,25,1,0,417.6,'2026-02-16 19:04:00','2026-02-16 19:10:57','测试环境','trigger',5,'2026-02-16 19:04:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO test_runs(id,project_id,test_type,test_object_name,status,total_cases,passed,failed,skipped,error,duration,started_at,finished_at,environment_name,triggered_by,triggered_user_id,created_at)VALUES(98,8,'web','冒烟测试','success',23,21,2,3,1,570.3,'2026-04-26 23:36:00','2026-04-26 23:45:30','测试环境','schedule',6,'2026-04-26 23:36:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO test_runs(id,project_id,test_type,test_object_name,status,total_cases,passed,failed,skipped,error,duration,started_at,finished_at,environment_name,triggered_by,triggered_user_id,created_at)VALUES(99,8,'web','接口自动化','failed',89,86,3,1,2,568.2,'2026-04-07 06:59:00','2026-04-07 07:08:28','开发环境','trigger',6,'2026-04-07 06:59:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO test_runs(id,project_id,test_type,test_object_name,status,total_cases,passed,failed,skipped,error,duration,started_at,finished_at,environment_name,triggered_by,triggered_user_id,created_at)VALUES(100,8,'api','回归测试','success',68,55,13,2,2,173.8,'2026-04-13 18:22:00','2026-04-13 18:24:53','测试环境','trigger',6,'2026-04-13 18:22:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO test_runs(id,project_id,test_type,test_object_name,status,total_cases,passed,failed,skipped,error,duration,started_at,finished_at,environment_name,triggered_by,triggered_user_id,created_at)VALUES(101,8,'web','UI自动化','pending',12,9,3,0,0,572.2,'2026-01-29 14:42:00',NULL,'预发布','schedule',2,'2026-01-29 14:42:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO test_runs(id,project_id,test_type,test_object_name,status,total_cases,passed,failed,skipped,error,duration,started_at,finished_at,environment_name,triggered_by,triggered_user_id,created_at)VALUES(102,8,'api','性能压测','success',6,5,1,1,1,382.0,'2025-12-07 14:33:00','2025-12-07 14:39:22','开发环境','manual',7,'2025-12-07 14:33:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO test_runs(id,project_id,test_type,test_object_name,status,total_cases,passed,failed,skipped,error,duration,started_at,finished_at,environment_name,triggered_by,triggered_user_id,created_at)VALUES(103,8,'api','回归测试','success',52,48,4,1,1,343.5,'2026-01-31 07:59:00','2026-01-31 08:04:43','测试环境','trigger',5,'2026-01-31 07:59:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO test_runs(id,project_id,test_type,test_object_name,status,total_cases,passed,failed,skipped,error,duration,started_at,finished_at,environment_name,triggered_by,triggered_user_id,created_at)VALUES(104,8,'api','回归测试','pending',93,71,22,2,2,550.3,'2026-01-31 01:25:00',NULL,'测试环境','ci',7,'2026-01-31 01:25:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO test_runs(id,project_id,test_type,test_object_name,status,total_cases,passed,failed,skipped,error,duration,started_at,finished_at,environment_name,triggered_by,triggered_user_id,created_at)VALUES(105,8,'api','性能压测','pending',85,74,11,1,2,359.8,'2026-04-02 02:29:00',NULL,'测试环境','trigger',1,'2026-04-02 02:29:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO test_runs(id,project_id,test_type,test_object_name,status,total_cases,passed,failed,skipped,error,duration,started_at,finished_at,environment_name,triggered_by,triggered_user_id,created_at)VALUES(106,8,'api','回归测试','success',23,20,3,0,2,299.7,'2025-12-28 10:43:00','2025-12-28 10:47:59','测试环境','manual',6,'2025-12-28 10:43:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO test_runs(id,project_id,test_type,test_object_name,status,total_cases,passed,failed,skipped,error,duration,started_at,finished_at,environment_name,triggered_by,triggered_user_id,created_at)VALUES(107,8,'api','性能压测','failed',51,48,3,0,1,155.5,'2025-12-21 09:40:00','2025-12-21 09:42:35','测试环境','ci',7,'2025-12-21 09:40:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO test_runs(id,project_id,test_type,test_object_name,status,total_cases,passed,failed,skipped,error,duration,started_at,finished_at,environment_name,triggered_by,triggered_user_id,created_at)VALUES(108,8,'api','冒烟测试','failed',45,38,7,2,2,531.1,'2026-04-10 13:48:00','2026-04-10 13:56:51','预发布','manual',5,'2026-04-10 13:48:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO test_runs(id,project_id,test_type,test_object_name,status,total_cases,passed,failed,skipped,error,duration,started_at,finished_at,environment_name,triggered_by,triggered_user_id,created_at)VALUES(109,9,'api','冒烟测试','success',69,54,15,3,1,423.4,'2026-05-30 00:44:00','2026-05-30 00:51:03','测试环境','schedule',2,'2026-05-30 00:44:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO test_runs(id,project_id,test_type,test_object_name,status,total_cases,passed,failed,skipped,error,duration,started_at,finished_at,environment_name,triggered_by,triggered_user_id,created_at)VALUES(110,9,'api','接口自动化','failed',58,41,17,3,0,273.5,'2026-02-23 16:50:00','2026-02-23 16:54:33','开发环境','trigger',5,'2026-02-23 16:50:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO test_runs(id,project_id,test_type,test_object_name,status,total_cases,passed,failed,skipped,error,duration,started_at,finished_at,environment_name,triggered_by,triggered_user_id,created_at)VALUES(111,9,'web','UI自动化','success',95,83,12,2,0,356.0,'2026-03-11 09:53:00','2026-03-11 09:58:56','预发布','manual',5,'2026-03-11 09:53:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO test_runs(id,project_id,test_type,test_object_name,status,total_cases,passed,failed,skipped,error,duration,started_at,finished_at,environment_name,triggered_by,triggered_user_id,created_at)VALUES(112,9,'api','接口自动化','success',97,78,19,0,2,266.2,'2026-03-10 21:49:00','2026-03-10 21:53:26','开发环境','ci',7,'2026-03-10 21:49:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO test_runs(id,project_id,test_type,test_object_name,status,total_cases,passed,failed,skipped,error,duration,started_at,finished_at,environment_name,triggered_by,triggered_user_id,created_at)VALUES(113,9,'api','冒烟测试','success',77,54,23,0,2,433.2,'2026-04-28 18:56:00','2026-04-28 19:03:13','开发环境','manual',2,'2026-04-28 18:56:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO test_runs(id,project_id,test_type,test_object_name,status,total_cases,passed,failed,skipped,error,duration,started_at,finished_at,environment_name,triggered_by,triggered_user_id,created_at)VALUES(114,9,'web','性能压测','success',96,73,23,2,1,209.5,'2026-02-15 23:12:00','2026-02-15 23:15:29','测试环境','manual',6,'2026-02-15 23:12:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO test_runs(id,project_id,test_type,test_object_name,status,total_cases,passed,failed,skipped,error,duration,started_at,finished_at,environment_name,triggered_by,triggered_user_id,created_at)VALUES(115,9,'api','回归测试','success',87,81,6,1,2,495.5,'2026-04-08 19:50:00','2026-04-08 19:58:15','开发环境','manual',5,'2026-04-08 19:50:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO test_runs(id,project_id,test_type,test_object_name,status,total_cases,passed,failed,skipped,error,duration,started_at,finished_at,environment_name,triggered_by,triggered_user_id,created_at)VALUES(116,9,'api','接口自动化','success',76,53,23,1,1,35.0,'2026-04-06 02:51:00','2026-04-06 02:51:35','测试环境','schedule',7,'2026-04-06 02:51:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO test_runs(id,project_id,test_type,test_object_name,status,total_cases,passed,failed,skipped,error,duration,started_at,finished_at,environment_name,triggered_by,triggered_user_id,created_at)VALUES(117,9,'web','性能压测','failed',90,73,17,2,1,23.9,'2025-12-04 20:25:00','2025-12-04 20:25:23','开发环境','manual',1,'2025-12-04 20:25:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO test_runs(id,project_id,test_type,test_object_name,status,total_cases,passed,failed,skipped,error,duration,started_at,finished_at,environment_name,triggered_by,triggered_user_id,created_at)VALUES(118,9,'api','回归测试','success',79,66,13,2,2,57.6,'2026-02-26 17:03:00','2026-02-26 17:03:57','开发环境','schedule',6,'2026-02-26 17:03:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO test_runs(id,project_id,test_type,test_object_name,status,total_cases,passed,failed,skipped,error,duration,started_at,finished_at,environment_name,triggered_by,triggered_user_id,created_at)VALUES(119,9,'web','接口自动化','success',85,78,7,2,1,338.2,'2026-01-21 21:50:00','2026-01-21 21:55:38','测试环境','schedule',7,'2026-01-21 21:50:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO test_runs(id,project_id,test_type,test_object_name,status,total_cases,passed,failed,skipped,error,duration,started_at,finished_at,environment_name,triggered_by,triggered_user_id,created_at)VALUES(120,9,'api','冒烟测试','success',38,31,7,2,1,27.0,'2025-12-28 13:18:00','2025-12-28 13:18:27','开发环境','trigger',2,'2025-12-28 13:18:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO test_runs(id,project_id,test_type,test_object_name,status,total_cases,passed,failed,skipped,error,duration,started_at,finished_at,environment_name,triggered_by,triggered_user_id,created_at)VALUES(121,9,'api','接口自动化','success',18,16,2,1,0,458.3,'2026-03-16 11:17:00','2026-03-16 11:24:38','测试环境','schedule',7,'2026-03-16 11:17:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO test_runs(id,project_id,test_type,test_object_name,status,total_cases,passed,failed,skipped,error,duration,started_at,finished_at,environment_name,triggered_by,triggered_user_id,created_at)VALUES(122,9,'web','UI自动化','success',85,65,20,2,0,311.5,'2026-03-14 09:47:00','2026-03-14 09:52:11','开发环境','schedule',5,'2026-03-14 09:47:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO test_runs(id,project_id,test_type,test_object_name,status,total_cases,passed,failed,skipped,error,duration,started_at,finished_at,environment_name,triggered_by,triggered_user_id,created_at)VALUES(123,9,'performance','性能压测','success',46,38,8,3,2,454.8,'2026-01-26 18:25:00','2026-01-26 18:32:34','开发环境','ci',2,'2026-01-26 18:25:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO test_runs(id,project_id,test_type,test_object_name,status,total_cases,passed,failed,skipped,error,duration,started_at,finished_at,environment_name,triggered_by,triggered_user_id,created_at)VALUES(124,9,'api','接口自动化','running',8,7,1,0,1,558.8,'2026-03-15 19:36:00',NULL,'开发环境','schedule',1,'2026-03-15 19:36:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO test_runs(id,project_id,test_type,test_object_name,status,total_cases,passed,failed,skipped,error,duration,started_at,finished_at,environment_name,triggered_by,triggered_user_id,created_at)VALUES(125,9,'api','回归测试','success',59,54,5,2,0,175.2,'2025-12-16 09:41:00','2025-12-16 09:43:55','测试环境','manual',1,'2025-12-16 09:41:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO test_runs(id,project_id,test_type,test_object_name,status,total_cases,passed,failed,skipped,error,duration,started_at,finished_at,environment_name,triggered_by,triggered_user_id,created_at)VALUES(126,9,'api','性能压测','success',31,22,9,0,1,113.0,'2026-05-04 07:14:00','2026-05-04 07:15:53','预发布','schedule',6,'2026-05-04 07:14:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO test_runs(id,project_id,test_type,test_object_name,status,total_cases,passed,failed,skipped,error,duration,started_at,finished_at,environment_name,triggered_by,triggered_user_id,created_at)VALUES(127,9,'api','UI自动化','success',94,81,13,0,2,418.2,'2026-04-07 07:35:00','2026-04-07 07:41:58','开发环境','trigger',1,'2026-04-07 07:35:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO test_runs(id,project_id,test_type,test_object_name,status,total_cases,passed,failed,skipped,error,duration,started_at,finished_at,environment_name,triggered_by,triggered_user_id,created_at)VALUES(128,10,'web','冒烟测试','success',6,5,1,0,2,47.2,'2026-03-21 11:42:00','2026-03-21 11:42:47','测试环境','trigger',2,'2026-03-21 11:42:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO test_runs(id,project_id,test_type,test_object_name,status,total_cases,passed,failed,skipped,error,duration,started_at,finished_at,environment_name,triggered_by,triggered_user_id,created_at)VALUES(129,10,'performance','UI自动化','success',29,22,7,3,0,597.5,'2026-05-20 15:07:00','2026-05-20 15:16:57','预发布','trigger',7,'2026-05-20 15:07:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO test_runs(id,project_id,test_type,test_object_name,status,total_cases,passed,failed,skipped,error,duration,started_at,finished_at,environment_name,triggered_by,triggered_user_id,created_at)VALUES(130,10,'api','接口自动化','failed',100,71,29,2,0,362.8,'2026-02-04 18:26:00','2026-02-04 18:32:02','预发布','schedule',5,'2026-02-04 18:26:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO test_runs(id,project_id,test_type,test_object_name,status,total_cases,passed,failed,skipped,error,duration,started_at,finished_at,environment_name,triggered_by,triggered_user_id,created_at)VALUES(131,10,'performance','UI自动化','success',23,18,5,2,1,112.6,'2026-02-18 22:31:00','2026-02-18 22:32:52','开发环境','ci',5,'2026-02-18 22:31:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO test_runs(id,project_id,test_type,test_object_name,status,total_cases,passed,failed,skipped,error,duration,started_at,finished_at,environment_name,triggered_by,triggered_user_id,created_at)VALUES(132,10,'performance','性能压测','success',51,50,1,0,2,159.4,'2026-04-26 23:01:00','2026-04-26 23:03:39','测试环境','ci',6,'2026-04-26 23:01:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO test_runs(id,project_id,test_type,test_object_name,status,total_cases,passed,failed,skipped,error,duration,started_at,finished_at,environment_name,triggered_by,triggered_user_id,created_at)VALUES(133,10,'performance','UI自动化','success',10,8,2,1,2,211.6,'2025-12-21 10:50:00','2025-12-21 10:53:31','预发布','schedule',2,'2025-12-21 10:50:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO test_runs(id,project_id,test_type,test_object_name,status,total_cases,passed,failed,skipped,error,duration,started_at,finished_at,environment_name,triggered_by,triggered_user_id,created_at)VALUES(134,10,'api','接口自动化','failed',19,18,1,0,2,71.3,'2026-05-31 01:01:00','2026-05-31 01:02:11','预发布','schedule',2,'2026-05-31 01:01:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO test_runs(id,project_id,test_type,test_object_name,status,total_cases,passed,failed,skipped,error,duration,started_at,finished_at,environment_name,triggered_by,triggered_user_id,created_at)VALUES(135,10,'web','接口自动化','success',98,93,5,2,2,562.8,'2026-01-18 12:08:00','2026-01-18 12:17:22','预发布','trigger',2,'2026-01-18 12:08:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO test_runs(id,project_id,test_type,test_object_name,status,total_cases,passed,failed,skipped,error,duration,started_at,finished_at,environment_name,triggered_by,triggered_user_id,created_at)VALUES(136,10,'performance','冒烟测试','success',18,13,5,3,0,502.3,'2026-04-13 12:00:00','2026-04-13 12:08:22','开发环境','manual',6,'2026-04-13 12:00:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO test_runs(id,project_id,test_type,test_object_name,status,total_cases,passed,failed,skipped,error,duration,started_at,finished_at,environment_name,triggered_by,triggered_user_id,created_at)VALUES(137,10,'performance','冒烟测试','pending',35,32,3,2,0,329.8,'2026-05-08 03:59:00',NULL,'测试环境','manual',1,'2026-05-08 03:59:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO test_runs(id,project_id,test_type,test_object_name,status,total_cases,passed,failed,skipped,error,duration,started_at,finished_at,environment_name,triggered_by,triggered_user_id,created_at)VALUES(138,10,'api','性能压测','success',92,66,26,2,1,571.1,'2026-02-12 22:18:00','2026-02-12 22:27:31','预发布','trigger',1,'2026-02-12 22:18:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO test_runs(id,project_id,test_type,test_object_name,status,total_cases,passed,failed,skipped,error,duration,started_at,finished_at,environment_name,triggered_by,triggered_user_id,created_at)VALUES(139,10,'api','UI自动化','success',52,39,13,3,2,357.9,'2026-01-29 13:21:00','2026-01-29 13:26:57','开发环境','manual',6,'2026-01-29 13:21:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO test_runs(id,project_id,test_type,test_object_name,status,total_cases,passed,failed,skipped,error,duration,started_at,finished_at,environment_name,triggered_by,triggered_user_id,created_at)VALUES(140,10,'api','UI自动化','success',37,33,4,3,2,464.2,'2026-02-12 11:23:00','2026-02-12 11:30:44','开发环境','ci',6,'2026-02-12 11:23:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO test_runs(id,project_id,test_type,test_object_name,status,total_cases,passed,failed,skipped,error,duration,started_at,finished_at,environment_name,triggered_by,triggered_user_id,created_at)VALUES(141,10,'api','性能压测','pending',16,13,3,0,0,154.8,'2025-12-22 06:31:00',NULL,'开发环境','trigger',5,'2025-12-22 06:31:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO test_runs(id,project_id,test_type,test_object_name,status,total_cases,passed,failed,skipped,error,duration,started_at,finished_at,environment_name,triggered_by,triggered_user_id,created_at)VALUES(142,11,'api','冒烟测试','success',75,69,6,3,0,372.1,'2026-05-08 09:17:00','2026-05-08 09:23:12','预发布','schedule',7,'2026-05-08 09:17:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO test_runs(id,project_id,test_type,test_object_name,status,total_cases,passed,failed,skipped,error,duration,started_at,finished_at,environment_name,triggered_by,triggered_user_id,created_at)VALUES(143,11,'web','冒烟测试','success',69,52,17,2,2,343.4,'2026-01-14 13:14:00','2026-01-14 13:19:43','预发布','manual',5,'2026-01-14 13:14:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO test_runs(id,project_id,test_type,test_object_name,status,total_cases,passed,failed,skipped,error,duration,started_at,finished_at,environment_name,triggered_by,triggered_user_id,created_at)VALUES(144,11,'performance','回归测试','success',27,26,1,2,0,33.5,'2025-12-29 23:33:00','2025-12-29 23:33:33','开发环境','manual',2,'2025-12-29 23:33:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO test_runs(id,project_id,test_type,test_object_name,status,total_cases,passed,failed,skipped,error,duration,started_at,finished_at,environment_name,triggered_by,triggered_user_id,created_at)VALUES(145,11,'web','UI自动化','success',5,4,1,1,1,35.9,'2026-04-16 02:39:00','2026-04-16 02:39:35','预发布','trigger',2,'2026-04-16 02:39:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO test_runs(id,project_id,test_type,test_object_name,status,total_cases,passed,failed,skipped,error,duration,started_at,finished_at,environment_name,triggered_by,triggered_user_id,created_at)VALUES(146,11,'performance','UI自动化','pending',19,13,6,1,0,446.8,'2025-12-28 15:59:00',NULL,'测试环境','trigger',6,'2025-12-28 15:59:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO test_runs(id,project_id,test_type,test_object_name,status,total_cases,passed,failed,skipped,error,duration,started_at,finished_at,environment_name,triggered_by,triggered_user_id,created_at)VALUES(147,11,'api','冒烟测试','failed',93,75,18,0,1,289.5,'2026-03-21 20:25:00','2026-03-21 20:29:49','开发环境','trigger',1,'2026-03-21 20:25:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO test_runs(id,project_id,test_type,test_object_name,status,total_cases,passed,failed,skipped,error,duration,started_at,finished_at,environment_name,triggered_by,triggered_user_id,created_at)VALUES(148,11,'api','回归测试','running',90,72,18,3,2,552.4,'2026-04-27 06:59:00',NULL,'预发布','schedule',1,'2026-04-27 06:59:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO test_runs(id,project_id,test_type,test_object_name,status,total_cases,passed,failed,skipped,error,duration,started_at,finished_at,environment_name,triggered_by,triggered_user_id,created_at)VALUES(149,11,'performance','冒烟测试','success',89,88,1,2,2,165.2,'2026-05-14 12:49:00','2026-05-14 12:51:45','预发布','trigger',1,'2026-05-14 12:49:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO test_runs(id,project_id,test_type,test_object_name,status,total_cases,passed,failed,skipped,error,duration,started_at,finished_at,environment_name,triggered_by,triggered_user_id,created_at)VALUES(150,11,'api','冒烟测试','success',43,31,12,3,0,229.4,'2026-01-22 09:53:00','2026-01-22 09:56:49','预发布','ci',7,'2026-01-22 09:53:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO test_runs(id,project_id,test_type,test_object_name,status,total_cases,passed,failed,skipped,error,duration,started_at,finished_at,environment_name,triggered_by,triggered_user_id,created_at)VALUES(151,11,'api','冒烟测试','running',22,17,5,1,1,482.7,'2026-04-13 12:30:00',NULL,'开发环境','trigger',6,'2026-04-13 12:30:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO test_runs(id,project_id,test_type,test_object_name,status,total_cases,passed,failed,skipped,error,duration,started_at,finished_at,environment_name,triggered_by,triggered_user_id,created_at)VALUES(152,11,'api','冒烟测试','success',86,76,10,0,0,403.6,'2026-01-22 05:05:00','2026-01-22 05:11:43','预发布','manual',6,'2026-01-22 05:05:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO test_runs(id,project_id,test_type,test_object_name,status,total_cases,passed,failed,skipped,error,duration,started_at,finished_at,environment_name,triggered_by,triggered_user_id,created_at)VALUES(153,11,'web','UI自动化','success',85,78,7,2,0,498.5,'2026-02-17 08:12:00','2026-02-17 08:20:18','测试环境','trigger',1,'2026-02-17 08:12:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO test_runs(id,project_id,test_type,test_object_name,status,total_cases,passed,failed,skipped,error,duration,started_at,finished_at,environment_name,triggered_by,triggered_user_id,created_at)VALUES(154,11,'api','性能压测','success',97,94,3,3,1,367.8,'2026-04-04 10:02:00','2026-04-04 10:08:07','预发布','schedule',6,'2026-04-04 10:02:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO test_runs(id,project_id,test_type,test_object_name,status,total_cases,passed,failed,skipped,error,duration,started_at,finished_at,environment_name,triggered_by,triggered_user_id,created_at)VALUES(155,11,'web','冒烟测试','success',86,64,22,2,1,466.1,'2026-02-10 14:59:00','2026-02-10 15:06:46','预发布','trigger',1,'2026-02-10 14:59:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO test_runs(id,project_id,test_type,test_object_name,status,total_cases,passed,failed,skipped,error,duration,started_at,finished_at,environment_name,triggered_by,triggered_user_id,created_at)VALUES(156,11,'performance','性能压测','running',23,21,2,0,1,173.7,'2026-03-21 19:19:00',NULL,'预发布','ci',5,'2026-03-21 19:19:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO test_runs(id,project_id,test_type,test_object_name,status,total_cases,passed,failed,skipped,error,duration,started_at,finished_at,environment_name,triggered_by,triggered_user_id,created_at)VALUES(157,12,'api','冒烟测试','running',65,55,10,3,2,357.8,'2026-01-08 12:22:00',NULL,'测试环境','schedule',6,'2026-01-08 12:22:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO test_runs(id,project_id,test_type,test_object_name,status,total_cases,passed,failed,skipped,error,duration,started_at,finished_at,environment_name,triggered_by,triggered_user_id,created_at)VALUES(158,12,'performance','回归测试','success',48,41,7,0,1,381.2,'2026-03-24 00:22:00','2026-03-24 00:28:21','测试环境','schedule',5,'2026-03-24 00:22:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO test_runs(id,project_id,test_type,test_object_name,status,total_cases,passed,failed,skipped,error,duration,started_at,finished_at,environment_name,triggered_by,triggered_user_id,created_at)VALUES(159,12,'web','回归测试','success',44,33,11,2,2,408.9,'2026-03-22 01:22:00','2026-03-22 01:28:48','预发布','trigger',2,'2026-03-22 01:22:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO test_runs(id,project_id,test_type,test_object_name,status,total_cases,passed,failed,skipped,error,duration,started_at,finished_at,environment_name,triggered_by,triggered_user_id,created_at)VALUES(160,12,'performance','回归测试','success',92,83,9,2,0,480.8,'2026-01-03 17:49:00','2026-01-03 17:57:00','预发布','manual',5,'2026-01-03 17:49:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO test_runs(id,project_id,test_type,test_object_name,status,total_cases,passed,failed,skipped,error,duration,started_at,finished_at,environment_name,triggered_by,triggered_user_id,created_at)VALUES(161,12,'api','UI自动化','success',86,81,5,1,2,487.7,'2026-02-26 02:35:00','2026-02-26 02:43:07','预发布','trigger',5,'2026-02-26 02:35:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO test_runs(id,project_id,test_type,test_object_name,status,total_cases,passed,failed,skipped,error,duration,started_at,finished_at,environment_name,triggered_by,triggered_user_id,created_at)VALUES(162,12,'web','UI自动化','success',37,32,5,2,0,580.2,'2026-01-11 22:00:00','2026-01-11 22:09:40','测试环境','manual',2,'2026-01-11 22:00:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO test_runs(id,project_id,test_type,test_object_name,status,total_cases,passed,failed,skipped,error,duration,started_at,finished_at,environment_name,triggered_by,triggered_user_id,created_at)VALUES(163,12,'web','冒烟测试','pending',75,65,10,2,2,344.8,'2026-04-12 01:57:00',NULL,'预发布','trigger',6,'2026-04-12 01:57:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO test_runs(id,project_id,test_type,test_object_name,status,total_cases,passed,failed,skipped,error,duration,started_at,finished_at,environment_name,triggered_by,triggered_user_id,created_at)VALUES(164,12,'web','性能压测','success',45,33,12,1,0,223.2,'2026-05-19 08:06:00','2026-05-19 08:09:43','开发环境','manual',5,'2026-05-19 08:06:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO test_runs(id,project_id,test_type,test_object_name,status,total_cases,passed,failed,skipped,error,duration,started_at,finished_at,environment_name,triggered_by,triggered_user_id,created_at)VALUES(165,12,'web','性能压测','success',17,16,1,3,0,33.6,'2025-12-13 15:57:00','2025-12-13 15:57:33','测试环境','manual',1,'2025-12-13 15:57:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO test_runs(id,project_id,test_type,test_object_name,status,total_cases,passed,failed,skipped,error,duration,started_at,finished_at,environment_name,triggered_by,triggered_user_id,created_at)VALUES(166,12,'performance','性能压测','success',60,46,14,1,2,366.2,'2026-03-24 16:38:00','2026-03-24 16:44:06','开发环境','schedule',2,'2026-03-24 16:38:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO test_runs(id,project_id,test_type,test_object_name,status,total_cases,passed,failed,skipped,error,duration,started_at,finished_at,environment_name,triggered_by,triggered_user_id,created_at)VALUES(167,12,'web','冒烟测试','success',33,24,9,3,0,329.6,'2026-05-28 04:55:00','2026-05-28 05:00:29','开发环境','ci',6,'2026-05-28 04:55:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO test_runs(id,project_id,test_type,test_object_name,status,total_cases,passed,failed,skipped,error,duration,started_at,finished_at,environment_name,triggered_by,triggered_user_id,created_at)VALUES(168,12,'api','性能压测','failed',33,25,8,1,0,551.4,'2026-03-22 07:00:00','2026-03-22 07:09:11','测试环境','schedule',5,'2026-03-22 07:00:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO test_runs(id,project_id,test_type,test_object_name,status,total_cases,passed,failed,skipped,error,duration,started_at,finished_at,environment_name,triggered_by,triggered_user_id,created_at)VALUES(169,12,'web','冒烟测试','failed',62,47,15,0,0,251.0,'2026-02-07 19:51:00','2026-02-07 19:55:11','测试环境','trigger',7,'2026-02-07 19:51:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO test_runs(id,project_id,test_type,test_object_name,status,total_cases,passed,failed,skipped,error,duration,started_at,finished_at,environment_name,triggered_by,triggered_user_id,created_at)VALUES(170,13,'api','接口自动化','success',91,77,14,2,1,22.2,'2026-01-22 14:36:00','2026-01-22 14:36:22','开发环境','trigger',7,'2026-01-22 14:36:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO test_runs(id,project_id,test_type,test_object_name,status,total_cases,passed,failed,skipped,error,duration,started_at,finished_at,environment_name,triggered_by,triggered_user_id,created_at)VALUES(171,13,'api','回归测试','failed',81,77,4,3,0,475.0,'2026-04-09 03:40:00','2026-04-09 03:47:55','测试环境','ci',6,'2026-04-09 03:40:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO test_runs(id,project_id,test_type,test_object_name,status,total_cases,passed,failed,skipped,error,duration,started_at,finished_at,environment_name,triggered_by,triggered_user_id,created_at)VALUES(172,13,'performance','冒烟测试','success',34,27,7,3,0,415.0,'2026-01-08 02:19:00','2026-01-08 02:25:55','预发布','manual',6,'2026-01-08 02:19:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO test_runs(id,project_id,test_type,test_object_name,status,total_cases,passed,failed,skipped,error,duration,started_at,finished_at,environment_name,triggered_by,triggered_user_id,created_at)VALUES(173,13,'web','接口自动化','success',51,41,10,3,1,437.3,'2026-02-13 07:33:00','2026-02-13 07:40:17','开发环境','ci',5,'2026-02-13 07:33:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO test_runs(id,project_id,test_type,test_object_name,status,total_cases,passed,failed,skipped,error,duration,started_at,finished_at,environment_name,triggered_by,triggered_user_id,created_at)VALUES(174,13,'api','接口自动化','running',38,32,6,1,0,513.7,'2025-12-17 17:22:00',NULL,'测试环境','schedule',1,'2025-12-17 17:22:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO test_runs(id,project_id,test_type,test_object_name,status,total_cases,passed,failed,skipped,error,duration,started_at,finished_at,environment_name,triggered_by,triggered_user_id,created_at)VALUES(175,13,'api','UI自动化','failed',16,14,2,1,0,373.1,'2026-01-11 08:44:00','2026-01-11 08:50:13','测试环境','manual',7,'2026-01-11 08:44:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO test_runs(id,project_id,test_type,test_object_name,status,total_cases,passed,failed,skipped,error,duration,started_at,finished_at,environment_name,triggered_by,triggered_user_id,created_at)VALUES(176,13,'api','冒烟测试','success',60,47,13,1,0,251.6,'2026-04-19 17:56:00','2026-04-19 18:00:11','预发布','schedule',1,'2026-04-19 17:56:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO test_runs(id,project_id,test_type,test_object_name,status,total_cases,passed,failed,skipped,error,duration,started_at,finished_at,environment_name,triggered_by,triggered_user_id,created_at)VALUES(177,13,'web','冒烟测试','failed',99,74,25,3,1,538.0,'2026-04-02 09:09:00','2026-04-02 09:17:58','预发布','schedule',7,'2026-04-02 09:09:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO test_runs(id,project_id,test_type,test_object_name,status,total_cases,passed,failed,skipped,error,duration,started_at,finished_at,environment_name,triggered_by,triggered_user_id,created_at)VALUES(178,13,'api','性能压测','failed',39,36,3,1,2,83.2,'2026-02-02 16:12:00','2026-02-02 16:13:23','开发环境','ci',2,'2026-02-02 16:12:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO test_runs(id,project_id,test_type,test_object_name,status,total_cases,passed,failed,skipped,error,duration,started_at,finished_at,environment_name,triggered_by,triggered_user_id,created_at)VALUES(179,13,'api','回归测试','success',6,4,2,1,1,312.8,'2026-05-26 17:28:00','2026-05-26 17:33:12','开发环境','manual',6,'2026-05-26 17:28:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO test_runs(id,project_id,test_type,test_object_name,status,total_cases,passed,failed,skipped,error,duration,started_at,finished_at,environment_name,triggered_by,triggered_user_id,created_at)VALUES(180,13,'api','回归测试','success',21,16,5,2,2,472.1,'2026-02-03 02:31:00','2026-02-03 02:38:52','预发布','schedule',1,'2026-02-03 02:31:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO test_runs(id,project_id,test_type,test_object_name,status,total_cases,passed,failed,skipped,error,duration,started_at,finished_at,environment_name,triggered_by,triggered_user_id,created_at)VALUES(181,13,'api','性能压测','success',10,7,3,3,0,10.3,'2026-02-03 17:09:00','2026-02-03 17:09:10','预发布','trigger',6,'2026-02-03 17:09:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO test_runs(id,project_id,test_type,test_object_name,status,total_cases,passed,failed,skipped,error,duration,started_at,finished_at,environment_name,triggered_by,triggered_user_id,created_at)VALUES(182,13,'performance','UI自动化','success',72,60,12,2,2,350.7,'2026-02-18 01:27:00','2026-02-18 01:32:50','预发布','trigger',2,'2026-02-18 01:27:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO test_runs(id,project_id,test_type,test_object_name,status,total_cases,passed,failed,skipped,error,duration,started_at,finished_at,environment_name,triggered_by,triggered_user_id,created_at)VALUES(183,13,'api','接口自动化','failed',31,22,9,2,1,78.2,'2026-02-15 21:36:00','2026-02-15 21:37:18','开发环境','ci',5,'2026-02-15 21:36:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO test_runs(id,project_id,test_type,test_object_name,status,total_cases,passed,failed,skipped,error,duration,started_at,finished_at,environment_name,triggered_by,triggered_user_id,created_at)VALUES(184,13,'web','回归测试','success',7,5,2,1,1,520.5,'2026-04-26 13:10:00','2026-04-26 13:18:40','开发环境','ci',6,'2026-04-26 13:10:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO test_runs(id,project_id,test_type,test_object_name,status,total_cases,passed,failed,skipped,error,duration,started_at,finished_at,environment_name,triggered_by,triggered_user_id,created_at)VALUES(185,13,'api','回归测试','running',61,47,14,3,1,430.6,'2026-02-26 03:31:00',NULL,'开发环境','schedule',6,'2026-02-26 03:31:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO test_runs(id,project_id,test_type,test_object_name,status,total_cases,passed,failed,skipped,error,duration,started_at,finished_at,environment_name,triggered_by,triggered_user_id,created_at)VALUES(186,14,'performance','性能压测','pending',42,34,8,2,1,546.5,'2025-12-15 20:56:00',NULL,'预发布','ci',5,'2025-12-15 20:56:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO test_runs(id,project_id,test_type,test_object_name,status,total_cases,passed,failed,skipped,error,duration,started_at,finished_at,environment_name,triggered_by,triggered_user_id,created_at)VALUES(187,14,'web','性能压测','success',66,47,19,2,0,193.1,'2026-01-23 05:00:00','2026-01-23 05:03:13','预发布','manual',2,'2026-01-23 05:00:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO test_runs(id,project_id,test_type,test_object_name,status,total_cases,passed,failed,skipped,error,duration,started_at,finished_at,environment_name,triggered_by,triggered_user_id,created_at)VALUES(188,14,'api','接口自动化','success',70,53,17,2,0,274.5,'2026-03-07 14:31:00','2026-03-07 14:35:34','测试环境','ci',7,'2026-03-07 14:31:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO test_runs(id,project_id,test_type,test_object_name,status,total_cases,passed,failed,skipped,error,duration,started_at,finished_at,environment_name,triggered_by,triggered_user_id,created_at)VALUES(189,14,'api','接口自动化','success',71,62,9,3,1,265.7,'2026-01-21 08:18:00','2026-01-21 08:22:25','测试环境','manual',2,'2026-01-21 08:18:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO test_runs(id,project_id,test_type,test_object_name,status,total_cases,passed,failed,skipped,error,duration,started_at,finished_at,environment_name,triggered_by,triggered_user_id,created_at)VALUES(190,14,'performance','回归测试','failed',98,89,9,2,0,93.9,'2026-04-12 07:21:00','2026-04-12 07:22:33','测试环境','trigger',5,'2026-04-12 07:21:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO test_runs(id,project_id,test_type,test_object_name,status,total_cases,passed,failed,skipped,error,duration,started_at,finished_at,environment_name,triggered_by,triggered_user_id,created_at)VALUES(191,14,'api','冒烟测试','success',6,5,1,1,1,345.9,'2026-02-15 05:33:00','2026-02-15 05:38:45','开发环境','ci',2,'2026-02-15 05:33:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO test_runs(id,project_id,test_type,test_object_name,status,total_cases,passed,failed,skipped,error,duration,started_at,finished_at,environment_name,triggered_by,triggered_user_id,created_at)VALUES(192,14,'api','UI自动化','running',38,34,4,0,0,286.3,'2026-04-19 12:29:00',NULL,'预发布','manual',1,'2026-04-19 12:29:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO test_runs(id,project_id,test_type,test_object_name,status,total_cases,passed,failed,skipped,error,duration,started_at,finished_at,environment_name,triggered_by,triggered_user_id,created_at)VALUES(193,14,'api','性能压测','success',52,49,3,2,2,339.6,'2026-03-08 13:18:00','2026-03-08 13:23:39','开发环境','ci',7,'2026-03-08 13:18:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO test_runs(id,project_id,test_type,test_object_name,status,total_cases,passed,failed,skipped,error,duration,started_at,finished_at,environment_name,triggered_by,triggered_user_id,created_at)VALUES(194,14,'web','UI自动化','failed',81,75,6,1,0,490.8,'2026-02-09 18:43:00','2026-02-09 18:51:10','测试环境','ci',7,'2026-02-09 18:43:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO test_runs(id,project_id,test_type,test_object_name,status,total_cases,passed,failed,skipped,error,duration,started_at,finished_at,environment_name,triggered_by,triggered_user_id,created_at)VALUES(195,14,'performance','回归测试','cancelled',11,10,1,2,1,72.8,'2026-04-24 16:46:00','2026-04-24 16:47:12','测试环境','schedule',2,'2026-04-24 16:46:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO test_runs(id,project_id,test_type,test_object_name,status,total_cases,passed,failed,skipped,error,duration,started_at,finished_at,environment_name,triggered_by,triggered_user_id,created_at)VALUES(196,15,'performance','冒烟测试','success',51,42,9,3,1,344.3,'2026-03-17 07:45:00','2026-03-17 07:50:44','测试环境','schedule',7,'2026-03-17 07:45:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO test_runs(id,project_id,test_type,test_object_name,status,total_cases,passed,failed,skipped,error,duration,started_at,finished_at,environment_name,triggered_by,triggered_user_id,created_at)VALUES(197,15,'api','UI自动化','pending',12,9,3,3,0,254.4,'2026-05-24 23:37:00',NULL,'开发环境','manual',5,'2026-05-24 23:37:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO test_runs(id,project_id,test_type,test_object_name,status,total_cases,passed,failed,skipped,error,duration,started_at,finished_at,environment_name,triggered_by,triggered_user_id,created_at)VALUES(198,15,'web','性能压测','pending',55,48,7,3,1,511.2,'2026-03-20 02:21:00',NULL,'开发环境','schedule',5,'2026-03-20 02:21:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO test_runs(id,project_id,test_type,test_object_name,status,total_cases,passed,failed,skipped,error,duration,started_at,finished_at,environment_name,triggered_by,triggered_user_id,created_at)VALUES(199,15,'api','冒烟测试','success',15,10,5,0,2,15.0,'2026-01-13 20:29:00','2026-01-13 20:29:15','开发环境','manual',2,'2026-01-13 20:29:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO test_runs(id,project_id,test_type,test_object_name,status,total_cases,passed,failed,skipped,error,duration,started_at,finished_at,environment_name,triggered_by,triggered_user_id,created_at)VALUES(200,15,'web','接口自动化','success',22,17,5,2,2,414.5,'2025-12-03 22:18:00','2025-12-03 22:24:54','开发环境','manual',1,'2025-12-03 22:18:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO test_runs(id,project_id,test_type,test_object_name,status,total_cases,passed,failed,skipped,error,duration,started_at,finished_at,environment_name,triggered_by,triggered_user_id,created_at)VALUES(201,15,'api','接口自动化','success',79,57,22,0,2,10.1,'2026-04-13 04:03:00','2026-04-13 04:03:10','开发环境','trigger',6,'2026-04-13 04:03:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO test_runs(id,project_id,test_type,test_object_name,status,total_cases,passed,failed,skipped,error,duration,started_at,finished_at,environment_name,triggered_by,triggered_user_id,created_at)VALUES(202,15,'web','回归测试','success',72,51,21,2,0,48.3,'2025-12-28 01:50:00','2025-12-28 01:50:48','预发布','manual',6,'2025-12-28 01:50:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO test_runs(id,project_id,test_type,test_object_name,status,total_cases,passed,failed,skipped,error,duration,started_at,finished_at,environment_name,triggered_by,triggered_user_id,created_at)VALUES(203,15,'performance','UI自动化','success',55,52,3,1,2,288.9,'2026-02-05 22:28:00','2026-02-05 22:32:48','预发布','ci',5,'2026-02-05 22:28:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO test_runs(id,project_id,test_type,test_object_name,status,total_cases,passed,failed,skipped,error,duration,started_at,finished_at,environment_name,triggered_by,triggered_user_id,created_at)VALUES(204,15,'web','冒烟测试','failed',35,32,3,2,2,202.7,'2026-03-31 19:51:00','2026-03-31 19:54:22','开发环境','schedule',1,'2026-03-31 19:51:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO test_runs(id,project_id,test_type,test_object_name,status,total_cases,passed,failed,skipped,error,duration,started_at,finished_at,environment_name,triggered_by,triggered_user_id,created_at)VALUES(205,16,'api','UI自动化','success',62,45,17,0,1,464.5,'2025-12-06 23:23:00','2025-12-06 23:30:44','测试环境','schedule',6,'2025-12-06 23:23:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO test_runs(id,project_id,test_type,test_object_name,status,total_cases,passed,failed,skipped,error,duration,started_at,finished_at,environment_name,triggered_by,triggered_user_id,created_at)VALUES(206,16,'api','回归测试','pending',90,88,2,2,2,133.8,'2026-01-30 13:58:00',NULL,'测试环境','ci',2,'2026-01-30 13:58:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO test_runs(id,project_id,test_type,test_object_name,status,total_cases,passed,failed,skipped,error,duration,started_at,finished_at,environment_name,triggered_by,triggered_user_id,created_at)VALUES(207,16,'api','回归测试','success',9,8,1,2,1,120.1,'2026-01-24 19:18:00','2026-01-24 19:20:00','测试环境','trigger',5,'2026-01-24 19:18:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO test_runs(id,project_id,test_type,test_object_name,status,total_cases,passed,failed,skipped,error,duration,started_at,finished_at,environment_name,triggered_by,triggered_user_id,created_at)VALUES(208,16,'api','冒烟测试','failed',95,78,17,2,2,522.2,'2026-04-15 09:05:00','2026-04-15 09:13:42','测试环境','schedule',5,'2026-04-15 09:05:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO test_runs(id,project_id,test_type,test_object_name,status,total_cases,passed,failed,skipped,error,duration,started_at,finished_at,environment_name,triggered_by,triggered_user_id,created_at)VALUES(209,16,'web','冒烟测试','running',47,34,13,1,0,312.5,'2026-01-26 01:02:00',NULL,'测试环境','schedule',2,'2026-01-26 01:02:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO test_runs(id,project_id,test_type,test_object_name,status,total_cases,passed,failed,skipped,error,duration,started_at,finished_at,environment_name,triggered_by,triggered_user_id,created_at)VALUES(210,16,'api','性能压测','success',96,77,19,2,1,11.6,'2026-01-28 17:48:00','2026-01-28 17:48:11','测试环境','schedule',2,'2026-01-28 17:48:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO test_runs(id,project_id,test_type,test_object_name,status,total_cases,passed,failed,skipped,error,duration,started_at,finished_at,environment_name,triggered_by,triggered_user_id,created_at)VALUES(211,16,'api','冒烟测试','success',72,71,1,1,1,464.1,'2026-05-21 19:14:00','2026-05-21 19:21:44','测试环境','ci',7,'2026-05-21 19:14:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO test_runs(id,project_id,test_type,test_object_name,status,total_cases,passed,failed,skipped,error,duration,started_at,finished_at,environment_name,triggered_by,triggered_user_id,created_at)VALUES(212,16,'api','回归测试','success',57,49,8,0,1,499.4,'2026-02-14 19:02:00','2026-02-14 19:10:19','预发布','schedule',5,'2026-02-14 19:02:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO test_runs(id,project_id,test_type,test_object_name,status,total_cases,passed,failed,skipped,error,duration,started_at,finished_at,environment_name,triggered_by,triggered_user_id,created_at)VALUES(213,16,'web','冒烟测试','success',88,84,4,1,2,543.6,'2026-03-27 21:44:00','2026-03-27 21:53:03','开发环境','manual',7,'2026-03-27 21:44:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO test_runs(id,project_id,test_type,test_object_name,status,total_cases,passed,failed,skipped,error,duration,started_at,finished_at,environment_name,triggered_by,triggered_user_id,created_at)VALUES(214,16,'api','接口自动化','pending',62,47,15,0,1,38.2,'2026-05-13 01:26:00',NULL,'预发布','trigger',1,'2026-05-13 01:26:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO test_runs(id,project_id,test_type,test_object_name,status,total_cases,passed,failed,skipped,error,duration,started_at,finished_at,environment_name,triggered_by,triggered_user_id,created_at)VALUES(215,16,'web','接口自动化','failed',68,67,1,1,2,400.2,'2026-03-20 06:06:00','2026-03-20 06:12:40','预发布','schedule',6,'2026-03-20 06:06:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO test_runs(id,project_id,test_type,test_object_name,status,total_cases,passed,failed,skipped,error,duration,started_at,finished_at,environment_name,triggered_by,triggered_user_id,created_at)VALUES(216,16,'api','接口自动化','success',30,21,9,3,0,204.0,'2026-03-30 18:59:00','2026-03-30 19:02:24','预发布','manual',2,'2026-03-30 18:59:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO test_runs(id,project_id,test_type,test_object_name,status,total_cases,passed,failed,skipped,error,duration,started_at,finished_at,environment_name,triggered_by,triggered_user_id,created_at)VALUES(217,16,'api','性能压测','failed',90,69,21,1,1,130.4,'2026-04-20 22:54:00','2026-04-20 22:56:10','预发布','ci',5,'2026-04-20 22:54:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO test_runs(id,project_id,test_type,test_object_name,status,total_cases,passed,failed,skipped,error,duration,started_at,finished_at,environment_name,triggered_by,triggered_user_id,created_at)VALUES(218,16,'performance','性能压测','success',24,23,1,0,0,48.9,'2026-03-24 04:53:00','2026-03-24 04:53:48','开发环境','trigger',5,'2026-03-24 04:53:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO test_runs(id,project_id,test_type,test_object_name,status,total_cases,passed,failed,skipped,error,duration,started_at,finished_at,environment_name,triggered_by,triggered_user_id,created_at)VALUES(219,16,'web','接口自动化','success',20,16,4,2,0,220.2,'2026-05-08 22:49:00','2026-05-08 22:52:40','预发布','trigger',2,'2026-05-08 22:49:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO test_runs(id,project_id,test_type,test_object_name,status,total_cases,passed,failed,skipped,error,duration,started_at,finished_at,environment_name,triggered_by,triggered_user_id,created_at)VALUES(220,16,'performance','接口自动化','success',84,79,5,0,0,105.8,'2026-03-06 04:27:00','2026-03-06 04:28:45','预发布','schedule',6,'2026-03-06 04:27:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO test_runs(id,project_id,test_type,test_object_name,status,total_cases,passed,failed,skipped,error,duration,started_at,finished_at,environment_name,triggered_by,triggered_user_id,created_at)VALUES(221,16,'api','UI自动化','success',54,50,4,3,0,486.3,'2026-02-18 03:50:00','2026-02-18 03:58:06','预发布','schedule',7,'2026-02-18 03:50:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO test_reports(id,test_run_id,project_id,test_type,title,summary,status,created_at,updated_at)VALUES(1,5,1,'performance','PERFORMANCE报告-2026-05-09','{"total": 39, "passed": 92, "pass_rate": 99.0}','generated','2026-01-25 16:11:00','2026-05-31 21:40:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO test_reports(id,test_run_id,project_id,test_type,title,summary,status,created_at,updated_at)VALUES(2,6,1,'performance','PERFORMANCE报告-2026-05-22','{"total": 15, "passed": 12, "pass_rate": 91.8}','generated','2026-05-31 15:38:00','2026-06-01 12:01:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO test_reports(id,test_run_id,project_id,test_type,title,summary,status,created_at,updated_at)VALUES(3,7,1,'web','WEB报告-2026-05-12','{"total": 10, "passed": 48, "pass_rate": 97.9}','generated','2026-05-11 05:07:00','2026-06-01 14:27:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO test_reports(id,test_run_id,project_id,test_type,title,summary,status,created_at,updated_at)VALUES(4,8,1,'performance','PERFORMANCE报告-2026-05-09','{"total": 27, "passed": 68, "pass_rate": 92.4}','generated','2026-01-10 10:12:00','2026-06-01 06:21:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO test_reports(id,test_run_id,project_id,test_type,title,summary,status,created_at,updated_at)VALUES(5,9,1,'api','API报告-2026-05-07','{"total": 41, "passed": 47, "pass_rate": 93.1}','generated','2026-02-13 00:58:00','2026-06-02 08:41:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO test_reports(id,test_run_id,project_id,test_type,title,summary,status,created_at,updated_at)VALUES(6,10,1,'performance','PERFORMANCE报告-2026-05-03','{"total": 43, "passed": 56, "pass_rate": 100.0}','generated','2026-03-21 23:06:00','2026-06-01 07:27:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO test_reports(id,test_run_id,project_id,test_type,title,summary,status,created_at,updated_at)VALUES(7,23,2,'web','WEB报告-2026-05-30','{"total": 48, "passed": 60, "pass_rate": 85.3}','generated','2026-03-20 23:49:00','2026-05-31 07:05:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO test_reports(id,test_run_id,project_id,test_type,title,summary,status,created_at,updated_at)VALUES(8,24,2,'api','API报告-2026-05-03','{"total": 86, "passed": 20, "pass_rate": 90.4}','generated','2026-05-08 01:11:00','2026-05-31 23:04:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO test_reports(id,test_run_id,project_id,test_type,title,summary,status,created_at,updated_at)VALUES(9,25,2,'api','API报告-2026-05-27','{"total": 84, "passed": 18, "pass_rate": 88.5}','generated','2026-03-23 00:07:00','2026-05-30 16:02:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO test_reports(id,test_run_id,project_id,test_type,title,summary,status,created_at,updated_at)VALUES(10,26,2,'api','API报告-2026-05-07','{"total": 83, "passed": 77, "pass_rate": 89.5}','generated','2026-01-10 12:41:00','2026-06-01 21:12:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO test_reports(id,test_run_id,project_id,test_type,title,summary,status,created_at,updated_at)VALUES(11,27,2,'api','API报告-2026-05-23','{"total": 94, "passed": 50, "pass_rate": 89.0}','generated','2026-05-19 05:56:00','2026-06-01 16:00:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO test_reports(id,test_run_id,project_id,test_type,title,summary,status,created_at,updated_at)VALUES(12,28,2,'api','API报告-2026-05-04','{"total": 70, "passed": 54, "pass_rate": 91.1}','generated','2026-05-05 01:50:00','2026-05-30 16:03:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO test_reports(id,test_run_id,project_id,test_type,title,summary,status,created_at,updated_at)VALUES(13,37,3,'api','API报告-2026-05-30','{"total": 33, "passed": 91, "pass_rate": 98.8}','generated','2026-05-05 13:09:00','2026-06-01 18:47:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO test_reports(id,test_run_id,project_id,test_type,title,summary,status,created_at,updated_at)VALUES(14,38,3,'performance','PERFORMANCE报告-2026-05-11','{"total": 97, "passed": 73, "pass_rate": 88.6}','generated','2026-02-17 09:17:00','2026-05-31 01:24:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO test_reports(id,test_run_id,project_id,test_type,title,summary,status,created_at,updated_at)VALUES(15,39,3,'performance','PERFORMANCE报告-2026-05-09','{"total": 80, "passed": 38, "pass_rate": 85.9}','generated','2026-04-07 14:18:00','2026-06-01 03:08:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO test_reports(id,test_run_id,project_id,test_type,title,summary,status,created_at,updated_at)VALUES(16,40,3,'performance','PERFORMANCE报告-2026-05-23','{"total": 61, "passed": 83, "pass_rate": 91.2}','generated','2026-01-04 00:43:00','2026-06-01 14:06:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO test_reports(id,test_run_id,project_id,test_type,title,summary,status,created_at,updated_at)VALUES(17,41,3,'api','API报告-2026-05-10','{"total": 92, "passed": 85, "pass_rate": 92.5}','generated','2026-05-02 21:23:00','2026-06-01 10:44:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO test_reports(id,test_run_id,project_id,test_type,title,summary,status,created_at,updated_at)VALUES(18,42,3,'performance','PERFORMANCE报告-2026-05-28','{"total": 92, "passed": 82, "pass_rate": 86.8}','generated','2026-03-30 05:15:00','2026-06-02 02:45:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO test_reports(id,test_run_id,project_id,test_type,title,summary,status,created_at,updated_at)VALUES(19,52,4,'performance','PERFORMANCE报告-2026-05-31','{"total": 97, "passed": 58, "pass_rate": 87.0}','generated','2026-04-07 01:53:00','2026-05-31 09:19:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO test_reports(id,test_run_id,project_id,test_type,title,summary,status,created_at,updated_at)VALUES(20,53,4,'api','API报告-2026-05-11','{"total": 99, "passed": 9, "pass_rate": 91.2}','generated','2026-03-06 03:32:00','2026-06-02 05:14:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO test_reports(id,test_run_id,project_id,test_type,title,summary,status,created_at,updated_at)VALUES(21,54,4,'performance','PERFORMANCE报告-2026-05-08','{"total": 57, "passed": 49, "pass_rate": 99.7}','generated','2026-02-24 12:27:00','2026-05-31 01:32:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO test_reports(id,test_run_id,project_id,test_type,title,summary,status,created_at,updated_at)VALUES(22,55,4,'performance','PERFORMANCE报告-2026-05-26','{"total": 36, "passed": 57, "pass_rate": 90.3}','generated','2026-03-30 18:29:00','2026-05-31 20:57:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO test_reports(id,test_run_id,project_id,test_type,title,summary,status,created_at,updated_at)VALUES(23,56,4,'web','WEB报告-2026-06-01','{"total": 30, "passed": 15, "pass_rate": 96.7}','generated','2026-05-16 10:31:00','2026-05-31 00:47:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO test_reports(id,test_run_id,project_id,test_type,title,summary,status,created_at,updated_at)VALUES(24,57,4,'web','WEB报告-2026-05-30','{"total": 46, "passed": 43, "pass_rate": 87.7}','generated','2026-05-28 18:10:00','2026-05-31 07:23:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO test_reports(id,test_run_id,project_id,test_type,title,summary,status,created_at,updated_at)VALUES(25,61,5,'web','WEB报告-2026-05-22','{"total": 38, "passed": 65, "pass_rate": 88.0}','generated','2026-03-22 18:36:00','2026-06-01 04:30:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO test_reports(id,test_run_id,project_id,test_type,title,summary,status,created_at,updated_at)VALUES(26,62,5,'api','API报告-2026-05-19','{"total": 40, "passed": 90, "pass_rate": 92.3}','generated','2026-04-05 16:28:00','2026-05-31 05:53:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO test_reports(id,test_run_id,project_id,test_type,title,summary,status,created_at,updated_at)VALUES(27,63,5,'web','WEB报告-2026-05-09','{"total": 42, "passed": 20, "pass_rate": 89.1}','generated','2026-01-20 00:13:00','2026-06-01 09:56:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO test_reports(id,test_run_id,project_id,test_type,title,summary,status,created_at,updated_at)VALUES(28,64,5,'performance','PERFORMANCE报告-2026-05-03','{"total": 46, "passed": 40, "pass_rate": 97.1}','generated','2026-01-09 14:24:00','2026-05-31 04:20:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO test_reports(id,test_run_id,project_id,test_type,title,summary,status,created_at,updated_at)VALUES(29,65,5,'web','WEB报告-2026-05-17','{"total": 12, "passed": 49, "pass_rate": 96.5}','generated','2026-01-10 20:24:00','2026-06-01 09:30:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO test_reports(id,test_run_id,project_id,test_type,title,summary,status,created_at,updated_at)VALUES(30,66,5,'api','API报告-2026-05-28','{"total": 49, "passed": 62, "pass_rate": 88.8}','generated','2026-03-23 15:48:00','2026-05-30 21:18:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO test_reports(id,test_run_id,project_id,test_type,title,summary,status,created_at,updated_at)VALUES(31,71,6,'performance','PERFORMANCE报告-2026-05-14','{"total": 22, "passed": 56, "pass_rate": 92.1}','generated','2026-04-12 02:40:00','2026-06-01 23:38:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO test_reports(id,test_run_id,project_id,test_type,title,summary,status,created_at,updated_at)VALUES(32,72,6,'web','WEB报告-2026-05-09','{"total": 52, "passed": 71, "pass_rate": 88.4}','generated','2026-01-09 09:16:00','2026-06-02 06:24:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO test_reports(id,test_run_id,project_id,test_type,title,summary,status,created_at,updated_at)VALUES(33,73,6,'api','API报告-2026-05-25','{"total": 15, "passed": 34, "pass_rate": 92.0}','generated','2026-01-15 10:56:00','2026-06-01 12:25:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO test_reports(id,test_run_id,project_id,test_type,title,summary,status,created_at,updated_at)VALUES(34,74,6,'web','WEB报告-2026-05-11','{"total": 37, "passed": 35, "pass_rate": 90.6}','generated','2026-05-23 02:00:00','2026-05-30 20:53:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO test_reports(id,test_run_id,project_id,test_type,title,summary,status,created_at,updated_at)VALUES(35,75,6,'web','WEB报告-2026-05-12','{"total": 67, "passed": 34, "pass_rate": 86.4}','generated','2026-04-01 14:53:00','2026-06-02 01:10:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO test_reports(id,test_run_id,project_id,test_type,title,summary,status,created_at,updated_at)VALUES(36,76,6,'performance','PERFORMANCE报告-2026-05-15','{"total": 40, "passed": 13, "pass_rate": 92.1}','generated','2026-03-22 16:50:00','2026-05-30 11:14:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO test_reports(id,test_run_id,project_id,test_type,title,summary,status,created_at,updated_at)VALUES(37,82,7,'api','API报告-2026-05-03','{"total": 37, "passed": 60, "pass_rate": 98.3}','generated','2026-05-07 07:28:00','2026-05-31 02:01:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO test_reports(id,test_run_id,project_id,test_type,title,summary,status,created_at,updated_at)VALUES(38,83,7,'performance','PERFORMANCE报告-2026-05-25','{"total": 99, "passed": 52, "pass_rate": 99.0}','generated','2026-02-05 16:16:00','2026-06-02 09:13:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO test_reports(id,test_run_id,project_id,test_type,title,summary,status,created_at,updated_at)VALUES(39,84,7,'api','API报告-2026-05-12','{"total": 95, "passed": 43, "pass_rate": 87.9}','generated','2026-04-22 02:13:00','2026-06-01 10:49:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO test_reports(id,test_run_id,project_id,test_type,title,summary,status,created_at,updated_at)VALUES(40,85,7,'api','API报告-2026-05-07','{"total": 26, "passed": 45, "pass_rate": 91.9}','generated','2026-02-06 02:21:00','2026-06-02 08:53:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO test_reports(id,test_run_id,project_id,test_type,title,summary,status,created_at,updated_at)VALUES(41,86,7,'performance','PERFORMANCE报告-2026-05-03','{"total": 56, "passed": 88, "pass_rate": 96.3}','generated','2026-03-16 12:33:00','2026-06-01 11:56:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO test_reports(id,test_run_id,project_id,test_type,title,summary,status,created_at,updated_at)VALUES(42,87,7,'api','API报告-2026-05-17','{"total": 31, "passed": 55, "pass_rate": 85.5}','generated','2026-04-17 12:07:00','2026-06-01 06:55:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO test_reports(id,test_run_id,project_id,test_type,title,summary,status,created_at,updated_at)VALUES(43,92,8,'api','API报告-2026-05-27','{"total": 63, "passed": 21, "pass_rate": 91.5}','generated','2026-04-20 01:15:00','2026-05-30 11:25:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO test_reports(id,test_run_id,project_id,test_type,title,summary,status,created_at,updated_at)VALUES(44,93,8,'performance','PERFORMANCE报告-2026-05-16','{"total": 84, "passed": 50, "pass_rate": 98.3}','generated','2026-04-21 14:26:00','2026-05-30 15:47:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO test_reports(id,test_run_id,project_id,test_type,title,summary,status,created_at,updated_at)VALUES(45,94,8,'web','WEB报告-2026-05-20','{"total": 66, "passed": 43, "pass_rate": 89.7}','generated','2026-04-07 10:09:00','2026-06-02 03:35:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO test_reports(id,test_run_id,project_id,test_type,title,summary,status,created_at,updated_at)VALUES(46,95,8,'web','WEB报告-2026-05-20','{"total": 21, "passed": 82, "pass_rate": 86.7}','generated','2026-04-30 08:46:00','2026-05-30 11:26:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO test_reports(id,test_run_id,project_id,test_type,title,summary,status,created_at,updated_at)VALUES(47,96,8,'api','API报告-2026-05-15','{"total": 93, "passed": 82, "pass_rate": 95.7}','generated','2026-04-28 08:27:00','2026-06-01 16:04:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO test_reports(id,test_run_id,project_id,test_type,title,summary,status,created_at,updated_at)VALUES(48,97,8,'api','API报告-2026-05-08','{"total": 16, "passed": 73, "pass_rate": 97.9}','generated','2026-01-13 07:45:00','2026-05-30 16:55:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO test_reports(id,test_run_id,project_id,test_type,title,summary,status,created_at,updated_at)VALUES(49,109,9,'web','WEB报告-2026-05-16','{"total": 43, "passed": 41, "pass_rate": 90.0}','generated','2026-04-28 04:58:00','2026-05-31 18:06:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO test_reports(id,test_run_id,project_id,test_type,title,summary,status,created_at,updated_at)VALUES(50,110,9,'api','API报告-2026-05-29','{"total": 91, "passed": 19, "pass_rate": 92.8}','generated','2026-02-08 07:33:00','2026-05-30 13:26:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO test_reports(id,test_run_id,project_id,test_type,title,summary,status,created_at,updated_at)VALUES(51,111,9,'api','API报告-2026-05-09','{"total": 31, "passed": 95, "pass_rate": 89.1}','generated','2026-03-07 09:58:00','2026-06-02 09:11:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO test_reports(id,test_run_id,project_id,test_type,title,summary,status,created_at,updated_at)VALUES(52,112,9,'performance','PERFORMANCE报告-2026-05-11','{"total": 13, "passed": 18, "pass_rate": 89.8}','generated','2026-01-03 07:55:00','2026-05-31 03:30:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO test_reports(id,test_run_id,project_id,test_type,title,summary,status,created_at,updated_at)VALUES(53,113,9,'api','API报告-2026-05-18','{"total": 57, "passed": 15, "pass_rate": 96.8}','generated','2026-05-25 10:51:00','2026-05-31 23:36:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO test_reports(id,test_run_id,project_id,test_type,title,summary,status,created_at,updated_at)VALUES(54,114,9,'performance','PERFORMANCE报告-2026-05-29','{"total": 47, "passed": 45, "pass_rate": 88.9}','generated','2026-05-10 16:08:00','2026-06-01 14:18:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO test_reports(id,test_run_id,project_id,test_type,title,summary,status,created_at,updated_at)VALUES(55,128,10,'performance','PERFORMANCE报告-2026-05-15','{"total": 72, "passed": 74, "pass_rate": 98.7}','generated','2026-05-13 05:49:00','2026-05-31 17:21:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO test_reports(id,test_run_id,project_id,test_type,title,summary,status,created_at,updated_at)VALUES(56,129,10,'api','API报告-2026-05-22','{"total": 15, "passed": 72, "pass_rate": 91.5}','generated','2026-05-26 08:22:00','2026-06-02 09:18:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO test_reports(id,test_run_id,project_id,test_type,title,summary,status,created_at,updated_at)VALUES(57,130,10,'web','WEB报告-2026-05-05','{"total": 54, "passed": 89, "pass_rate": 90.1}','generated','2026-02-28 10:27:00','2026-05-31 17:51:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO test_reports(id,test_run_id,project_id,test_type,title,summary,status,created_at,updated_at)VALUES(58,131,10,'web','WEB报告-2026-05-20','{"total": 40, "passed": 60, "pass_rate": 87.2}','generated','2026-03-24 17:46:00','2026-05-31 22:18:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO test_reports(id,test_run_id,project_id,test_type,title,summary,status,created_at,updated_at)VALUES(59,132,10,'api','API报告-2026-05-22','{"total": 31, "passed": 81, "pass_rate": 90.6}','generated','2026-05-21 16:15:00','2026-06-01 13:30:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO test_reports(id,test_run_id,project_id,test_type,title,summary,status,created_at,updated_at)VALUES(60,133,10,'api','API报告-2026-05-20','{"total": 62, "passed": 85, "pass_rate": 97.8}','generated','2026-01-09 19:21:00','2026-06-01 09:11:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO test_reports(id,test_run_id,project_id,test_type,title,summary,status,created_at,updated_at)VALUES(61,142,11,'performance','PERFORMANCE报告-2026-05-08','{"total": 77, "passed": 31, "pass_rate": 86.9}','generated','2026-05-17 01:09:00','2026-06-02 06:05:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO test_reports(id,test_run_id,project_id,test_type,title,summary,status,created_at,updated_at)VALUES(62,143,11,'web','WEB报告-2026-05-24','{"total": 81, "passed": 75, "pass_rate": 96.1}','generated','2026-03-26 13:14:00','2026-05-31 13:49:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO test_reports(id,test_run_id,project_id,test_type,title,summary,status,created_at,updated_at)VALUES(63,144,11,'performance','PERFORMANCE报告-2026-05-02','{"total": 41, "passed": 74, "pass_rate": 87.9}','generated','2026-04-13 17:19:00','2026-06-01 21:43:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO test_reports(id,test_run_id,project_id,test_type,title,summary,status,created_at,updated_at)VALUES(64,145,11,'api','API报告-2026-05-28','{"total": 28, "passed": 59, "pass_rate": 94.3}','generated','2026-03-17 10:50:00','2026-05-30 15:19:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO test_reports(id,test_run_id,project_id,test_type,title,summary,status,created_at,updated_at)VALUES(65,146,11,'performance','PERFORMANCE报告-2026-05-11','{"total": 62, "passed": 46, "pass_rate": 87.4}','generated','2026-03-30 20:12:00','2026-05-31 05:37:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO test_reports(id,test_run_id,project_id,test_type,title,summary,status,created_at,updated_at)VALUES(66,147,11,'performance','PERFORMANCE报告-2026-05-09','{"total": 37, "passed": 21, "pass_rate": 89.6}','generated','2026-03-29 07:31:00','2026-06-01 21:42:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO test_reports(id,test_run_id,project_id,test_type,title,summary,status,created_at,updated_at)VALUES(67,157,12,'performance','PERFORMANCE报告-2026-05-21','{"total": 57, "passed": 45, "pass_rate": 98.0}','generated','2026-05-22 04:35:00','2026-06-01 10:17:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO test_reports(id,test_run_id,project_id,test_type,title,summary,status,created_at,updated_at)VALUES(68,158,12,'web','WEB报告-2026-05-22','{"total": 33, "passed": 45, "pass_rate": 87.9}','generated','2026-05-26 12:55:00','2026-05-31 21:41:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO test_reports(id,test_run_id,project_id,test_type,title,summary,status,created_at,updated_at)VALUES(69,159,12,'web','WEB报告-2026-05-08','{"total": 47, "passed": 73, "pass_rate": 93.6}','generated','2026-01-16 17:02:00','2026-06-02 02:14:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO test_reports(id,test_run_id,project_id,test_type,title,summary,status,created_at,updated_at)VALUES(70,160,12,'api','API报告-2026-05-22','{"total": 99, "passed": 72, "pass_rate": 92.8}','generated','2026-03-22 23:14:00','2026-06-01 19:21:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO test_reports(id,test_run_id,project_id,test_type,title,summary,status,created_at,updated_at)VALUES(71,161,12,'performance','PERFORMANCE报告-2026-05-31','{"total": 53, "passed": 12, "pass_rate": 89.3}','generated','2026-05-18 00:45:00','2026-06-02 03:47:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO test_reports(id,test_run_id,project_id,test_type,title,summary,status,created_at,updated_at)VALUES(72,162,12,'web','WEB报告-2026-05-26','{"total": 85, "passed": 48, "pass_rate": 98.3}','generated','2026-04-30 21:14:00','2026-06-02 05:09:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO test_reports(id,test_run_id,project_id,test_type,title,summary,status,created_at,updated_at)VALUES(73,170,13,'api','API报告-2026-05-31','{"total": 86, "passed": 66, "pass_rate": 92.9}','generated','2026-04-30 16:57:00','2026-05-31 03:45:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO test_reports(id,test_run_id,project_id,test_type,title,summary,status,created_at,updated_at)VALUES(74,171,13,'performance','PERFORMANCE报告-2026-05-30','{"total": 35, "passed": 71, "pass_rate": 88.3}','generated','2026-02-17 13:40:00','2026-06-02 08:04:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO test_reports(id,test_run_id,project_id,test_type,title,summary,status,created_at,updated_at)VALUES(75,172,13,'web','WEB报告-2026-05-06','{"total": 19, "passed": 18, "pass_rate": 98.8}','generated','2026-01-22 18:12:00','2026-05-31 21:54:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO test_reports(id,test_run_id,project_id,test_type,title,summary,status,created_at,updated_at)VALUES(76,173,13,'web','WEB报告-2026-05-02','{"total": 62, "passed": 78, "pass_rate": 95.8}','generated','2026-01-18 10:00:00','2026-06-02 03:08:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO test_reports(id,test_run_id,project_id,test_type,title,summary,status,created_at,updated_at)VALUES(77,174,13,'api','API报告-2026-05-08','{"total": 23, "passed": 50, "pass_rate": 96.7}','generated','2026-05-03 16:52:00','2026-05-30 17:01:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO test_reports(id,test_run_id,project_id,test_type,title,summary,status,created_at,updated_at)VALUES(78,175,13,'api','API报告-2026-05-25','{"total": 52, "passed": 68, "pass_rate": 94.6}','generated','2026-01-25 01:14:00','2026-05-31 14:53:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO test_reports(id,test_run_id,project_id,test_type,title,summary,status,created_at,updated_at)VALUES(79,186,14,'performance','PERFORMANCE报告-2026-05-03','{"total": 10, "passed": 87, "pass_rate": 95.2}','generated','2026-02-20 22:21:00','2026-06-01 05:04:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO test_reports(id,test_run_id,project_id,test_type,title,summary,status,created_at,updated_at)VALUES(80,187,14,'api','API报告-2026-05-31','{"total": 19, "passed": 23, "pass_rate": 98.1}','generated','2026-01-05 00:54:00','2026-05-31 00:46:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO test_reports(id,test_run_id,project_id,test_type,title,summary,status,created_at,updated_at)VALUES(81,188,14,'api','API报告-2026-05-20','{"total": 53, "passed": 11, "pass_rate": 93.8}','generated','2026-02-17 03:50:00','2026-05-31 04:47:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO test_reports(id,test_run_id,project_id,test_type,title,summary,status,created_at,updated_at)VALUES(82,189,14,'performance','PERFORMANCE报告-2026-05-13','{"total": 19, "passed": 38, "pass_rate": 91.8}','generated','2026-03-07 23:34:00','2026-06-02 07:44:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO test_reports(id,test_run_id,project_id,test_type,title,summary,status,created_at,updated_at)VALUES(83,190,14,'api','API报告-2026-05-10','{"total": 47, "passed": 24, "pass_rate": 92.8}','generated','2026-02-16 10:58:00','2026-05-31 13:59:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO test_reports(id,test_run_id,project_id,test_type,title,summary,status,created_at,updated_at)VALUES(84,191,14,'web','WEB报告-2026-05-25','{"total": 60, "passed": 62, "pass_rate": 91.5}','generated','2026-05-20 17:16:00','2026-06-02 06:13:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO test_reports(id,test_run_id,project_id,test_type,title,summary,status,created_at,updated_at)VALUES(85,196,15,'api','API报告-2026-05-20','{"total": 34, "passed": 15, "pass_rate": 92.8}','generated','2026-04-09 22:36:00','2026-05-31 14:55:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO test_reports(id,test_run_id,project_id,test_type,title,summary,status,created_at,updated_at)VALUES(86,197,15,'api','API报告-2026-05-21','{"total": 68, "passed": 17, "pass_rate": 89.8}','generated','2026-04-08 06:49:00','2026-06-02 01:03:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO test_reports(id,test_run_id,project_id,test_type,title,summary,status,created_at,updated_at)VALUES(87,198,15,'web','WEB报告-2026-05-22','{"total": 65, "passed": 73, "pass_rate": 93.3}','generated','2026-02-09 15:54:00','2026-05-31 13:06:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO test_reports(id,test_run_id,project_id,test_type,title,summary,status,created_at,updated_at)VALUES(88,199,15,'web','WEB报告-2026-05-19','{"total": 28, "passed": 87, "pass_rate": 88.2}','generated','2026-01-18 01:42:00','2026-05-31 08:53:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO test_reports(id,test_run_id,project_id,test_type,title,summary,status,created_at,updated_at)VALUES(89,200,15,'api','API报告-2026-05-23','{"total": 77, "passed": 65, "pass_rate": 96.7}','generated','2026-03-06 00:45:00','2026-05-31 12:02:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO test_reports(id,test_run_id,project_id,test_type,title,summary,status,created_at,updated_at)VALUES(90,201,15,'performance','PERFORMANCE报告-2026-05-09','{"total": 62, "passed": 13, "pass_rate": 88.2}','generated','2026-02-25 14:14:00','2026-06-02 08:54:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO test_reports(id,test_run_id,project_id,test_type,title,summary,status,created_at,updated_at)VALUES(91,205,16,'performance','PERFORMANCE报告-2026-05-21','{"total": 98, "passed": 10, "pass_rate": 94.1}','generated','2026-05-19 17:37:00','2026-05-30 15:15:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO test_reports(id,test_run_id,project_id,test_type,title,summary,status,created_at,updated_at)VALUES(92,206,16,'api','API报告-2026-05-08','{"total": 83, "passed": 31, "pass_rate": 99.0}','generated','2026-02-06 01:23:00','2026-06-01 21:12:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO test_reports(id,test_run_id,project_id,test_type,title,summary,status,created_at,updated_at)VALUES(93,207,16,'performance','PERFORMANCE报告-2026-05-10','{"total": 90, "passed": 61, "pass_rate": 96.5}','generated','2026-01-05 21:05:00','2026-05-31 00:07:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO test_reports(id,test_run_id,project_id,test_type,title,summary,status,created_at,updated_at)VALUES(94,208,16,'performance','PERFORMANCE报告-2026-05-12','{"total": 86, "passed": 94, "pass_rate": 95.2}','generated','2026-02-05 07:04:00','2026-05-31 00:51:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO test_reports(id,test_run_id,project_id,test_type,title,summary,status,created_at,updated_at)VALUES(95,209,16,'performance','PERFORMANCE报告-2026-05-07','{"total": 59, "passed": 89, "pass_rate": 99.3}','generated','2026-03-30 05:39:00','2026-05-31 06:42:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO test_reports(id,test_run_id,project_id,test_type,title,summary,status,created_at,updated_at)VALUES(96,210,16,'api','API报告-2026-05-08','{"total": 49, "passed": 80, "pass_rate": 94.3}','generated','2026-04-13 04:04:00','2026-06-02 06:49:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO test_documents(id,project_id,title,content,category,version,created_by,updated_by,tags,is_published,created_at,updated_at)VALUES(1,1,'用户中心用例','用户中心测试用例','test_case','2.9',6,6,'["用例", "用户"]',true,' 2026-02-16 14:16:00','2026-06-01 16:30:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO test_documents(id,project_id,title,content,category,version,created_by,updated_by,tags,is_published,created_at,updated_at)VALUES(2,1,'Q3测试计划','Q3测试计划','test_plan','2.1',2,2,'["计划", "Q3"]',false,' 2025-11-17 20:03:00','2026-06-01 13:32:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO test_documents(id,project_id,title,content,category,version,created_by,updated_by,tags,is_published,created_at,updated_at)VALUES(3,2,'订单测试方案','订单模块方案','test_plan','3.3',5,5,'["方案"]',true,' 2026-03-09 12:18:00','2026-05-28 22:19:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO test_documents(id,project_id,title,content,category,version,created_by,updated_by,tags,is_published,created_at,updated_at)VALUES(4,2,'Q3测试计划','Q3测试计划','test_plan','3.2',2,2,'["计划", "Q3"]',true,' 2025-10-30 00:08:00','2026-06-01 22:34:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO test_documents(id,project_id,title,content,category,version,created_by,updated_by,tags,is_published,created_at,updated_at)VALUES(5,3,'API接口测试规范','API测试规范文档','test_plan','1.8',5,5,'["规范", "API"]',true,' 2026-02-17 15:12:00','2026-05-30 16:17:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO test_documents(id,project_id,title,content,category,version,created_by,updated_by,tags,is_published,created_at,updated_at)VALUES(6,3,'Q3测试计划','Q3测试计划','test_plan','2.4',2,2,'["计划", "Q3"]',true,' 2025-11-12 16:36:00','2026-05-28 21:38:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO test_documents(id,project_id,title,content,category,version,created_by,updated_by,tags,is_published,created_at,updated_at)VALUES(7,3,'自动化说明','自动化测试说明','other','3.1',6,6,'["文档"]',true,' 2026-05-28 16:30:00','2026-05-30 06:17:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO test_documents(id,project_id,title,content,category,version,created_by,updated_by,tags,is_published,created_at,updated_at)VALUES(8,3,'性能测试报告','性能测试报告','test_report','1.8',2,2,'["报告", "性能"]',true,' 2026-01-05 23:01:00','2026-06-02 01:07:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO test_documents(id,project_id,title,content,category,version,created_by,updated_by,tags,is_published,created_at,updated_at)VALUES(9,4,'安全检查清单','安全测试检查','test_case','3.2',6,6,'["安全"]',true,' 2026-01-02 00:06:00','2026-05-29 01:20:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO test_documents(id,project_id,title,content,category,version,created_by,updated_by,tags,is_published,created_at,updated_at)VALUES(10,4,'用户中心用例','用户中心测试用例','test_case','1.2',1,1,'["用例", "用户"]',false,' 2025-11-21 03:00:00','2026-06-01 12:06:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO test_documents(id,project_id,title,content,category,version,created_by,updated_by,tags,is_published,created_at,updated_at)VALUES(11,5,'性能测试报告','性能测试报告','test_report','1.1',1,1,'["报告", "性能"]',false,' 2026-01-24 03:56:00','2026-06-01 12:48:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO test_documents(id,project_id,title,content,category,version,created_by,updated_by,tags,is_published,created_at,updated_at)VALUES(12,5,'自动化说明','自动化测试说明','other','2.0',7,7,'["文档"]',true,' 2026-05-15 21:27:00','2026-06-01 14:19:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO test_documents(id,project_id,title,content,category,version,created_by,updated_by,tags,is_published,created_at,updated_at)VALUES(13,5,'安全检查清单','安全测试检查','test_case','1.4',5,5,'["安全"]',true,' 2025-10-24 10:40:00','2026-06-01 19:34:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO test_documents(id,project_id,title,content,category,version,created_by,updated_by,tags,is_published,created_at,updated_at)VALUES(14,5,'订单测试方案','订单模块方案','test_plan','3.8',2,2,'["方案"]',true,' 2025-10-20 15:32:00','2026-05-27 20:20:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO test_documents(id,project_id,title,content,category,version,created_by,updated_by,tags,is_published,created_at,updated_at)VALUES(15,6,'API接口测试规范','API测试规范文档','test_plan','1.4',5,5,'["规范", "API"]',true,' 2026-05-27 18:32:00','2026-05-29 14:42:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO test_documents(id,project_id,title,content,category,version,created_by,updated_by,tags,is_published,created_at,updated_at)VALUES(16,6,'订单测试方案','订单模块方案','test_plan','1.0',6,6,'["方案"]',false,' 2025-10-18 05:14:00','2026-05-29 20:18:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO test_documents(id,project_id,title,content,category,version,created_by,updated_by,tags,is_published,created_at,updated_at)VALUES(17,7,'自动化说明','自动化测试说明','other','1.8',5,5,'["文档"]',true,' 2025-11-22 18:14:00','2026-05-27 18:01:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO test_documents(id,project_id,title,content,category,version,created_by,updated_by,tags,is_published,created_at,updated_at)VALUES(18,7,'Q3测试计划','Q3测试计划','test_plan','1.2',6,6,'["计划", "Q3"]',true,' 2025-11-17 01:59:00','2026-05-29 17:17:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO test_documents(id,project_id,title,content,category,version,created_by,updated_by,tags,is_published,created_at,updated_at)VALUES(19,8,'用户中心用例','用户中心测试用例','test_case','2.3',2,2,'["用例", "用户"]',true,' 2025-10-05 05:01:00','2026-05-30 22:15:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO test_documents(id,project_id,title,content,category,version,created_by,updated_by,tags,is_published,created_at,updated_at)VALUES(20,8,'API接口测试规范','API测试规范文档','test_plan','1.5',2,2,'["规范", "API"]',false,' 2026-05-04 19:26:00','2026-06-01 20:00:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO test_documents(id,project_id,title,content,category,version,created_by,updated_by,tags,is_published,created_at,updated_at)VALUES(21,8,'Q3测试计划','Q3测试计划','test_plan','1.1',2,2,'["计划", "Q3"]',true,' 2025-12-29 05:00:00','2026-05-30 06:46:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO test_documents(id,project_id,title,content,category,version,created_by,updated_by,tags,is_published,created_at,updated_at)VALUES(22,8,'自动化说明','自动化测试说明','other','1.8',6,6,'["文档"]',true,' 2026-04-28 19:29:00','2026-05-28 15:38:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO test_documents(id,project_id,title,content,category,version,created_by,updated_by,tags,is_published,created_at,updated_at)VALUES(23,9,'API接口测试规范','API测试规范文档','test_plan','1.8',6,6,'["规范", "API"]',true,' 2026-03-15 01:23:00','2026-06-01 10:50:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO test_documents(id,project_id,title,content,category,version,created_by,updated_by,tags,is_published,created_at,updated_at)VALUES(24,9,'Q3测试计划','Q3测试计划','test_plan','2.0',7,7,'["计划", "Q3"]',true,' 2025-10-22 21:42:00','2026-05-29 08:08:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO test_documents(id,project_id,title,content,category,version,created_by,updated_by,tags,is_published,created_at,updated_at)VALUES(25,9,'订单测试方案','订单模块方案','test_plan','2.4',1,1,'["方案"]',true,' 2026-05-19 02:32:00','2026-05-31 12:44:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO test_documents(id,project_id,title,content,category,version,created_by,updated_by,tags,is_published,created_at,updated_at)VALUES(26,10,'性能测试报告','性能测试报告','test_report','1.2',7,7,'["报告", "性能"]',false,' 2025-11-23 18:18:00','2026-05-29 04:02:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO test_documents(id,project_id,title,content,category,version,created_by,updated_by,tags,is_published,created_at,updated_at)VALUES(27,10,'安全检查清单','安全测试检查','test_case','1.0',2,2,'["安全"]',true,' 2025-12-20 07:04:00','2026-05-29 15:26:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO test_documents(id,project_id,title,content,category,version,created_by,updated_by,tags,is_published,created_at,updated_at)VALUES(28,11,'API接口测试规范','API测试规范文档','test_plan','2.8',2,2,'["规范", "API"]',false,' 2026-04-18 15:26:00','2026-05-30 10:07:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO test_documents(id,project_id,title,content,category,version,created_by,updated_by,tags,is_published,created_at,updated_at)VALUES(29,11,'订单测试方案','订单模块方案','test_plan','3.9',6,6,'["方案"]',false,' 2026-04-02 20:05:00','2026-05-31 16:45:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO test_documents(id,project_id,title,content,category,version,created_by,updated_by,tags,is_published,created_at,updated_at)VALUES(30,12,'安全检查清单','安全测试检查','test_case','3.5',2,2,'["安全"]',false,' 2026-05-24 23:46:00','2026-05-28 19:13:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO test_documents(id,project_id,title,content,category,version,created_by,updated_by,tags,is_published,created_at,updated_at)VALUES(31,12,'自动化说明','自动化测试说明','other','2.9',1,1,'["文档"]',false,' 2026-02-17 12:01:00','2026-06-01 19:30:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO test_documents(id,project_id,title,content,category,version,created_by,updated_by,tags,is_published,created_at,updated_at)VALUES(32,13,'API接口测试规范','API测试规范文档','test_plan','3.2',6,6,'["规范", "API"]',true,' 2026-02-28 09:36:00','2026-05-29 05:55:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO test_documents(id,project_id,title,content,category,version,created_by,updated_by,tags,is_published,created_at,updated_at)VALUES(33,13,'性能测试报告','性能测试报告','test_report','1.3',2,2,'["报告", "性能"]',true,' 2026-03-09 12:50:00','2026-06-01 21:17:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO test_documents(id,project_id,title,content,category,version,created_by,updated_by,tags,is_published,created_at,updated_at)VALUES(34,13,'订单测试方案','订单模块方案','test_plan','1.5',5,5,'["方案"]',false,' 2025-10-05 06:17:00','2026-05-30 21:24:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO test_documents(id,project_id,title,content,category,version,created_by,updated_by,tags,is_published,created_at,updated_at)VALUES(35,13,'Q3测试计划','Q3测试计划','test_plan','3.1',2,2,'["计划", "Q3"]',true,' 2026-05-13 15:52:00','2026-05-30 15:35:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO test_documents(id,project_id,title,content,category,version,created_by,updated_by,tags,is_published,created_at,updated_at)VALUES(36,14,'安全检查清单','安全测试检查','test_case','3.8',7,7,'["安全"]',true,' 2026-04-01 20:21:00','2026-05-28 16:42:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO test_documents(id,project_id,title,content,category,version,created_by,updated_by,tags,is_published,created_at,updated_at)VALUES(37,14,'自动化说明','自动化测试说明','other','1.2',7,7,'["文档"]',true,' 2025-10-16 08:06:00','2026-05-31 08:22:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO test_documents(id,project_id,title,content,category,version,created_by,updated_by,tags,is_published,created_at,updated_at)VALUES(38,14,'API接口测试规范','API测试规范文档','test_plan','3.8',2,2,'["规范", "API"]',false,' 2025-11-28 14:15:00','2026-05-28 01:28:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO test_documents(id,project_id,title,content,category,version,created_by,updated_by,tags,is_published,created_at,updated_at)VALUES(39,15,'订单测试方案','订单模块方案','test_plan','2.9',7,7,'["方案"]',true,' 2025-12-18 07:42:00','2026-05-30 19:20:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO test_documents(id,project_id,title,content,category,version,created_by,updated_by,tags,is_published,created_at,updated_at)VALUES(40,15,'Q3测试计划','Q3测试计划','test_plan','3.7',7,7,'["计划", "Q3"]',true,' 2025-12-05 13:32:00','2026-06-01 22:01:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO test_documents(id,project_id,title,content,category,version,created_by,updated_by,tags,is_published,created_at,updated_at)VALUES(41,15,'用户中心用例','用户中心测试用例','test_case','1.8',2,2,'["用例", "用户"]',false,' 2026-02-06 21:30:00','2026-05-31 16:11:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO test_documents(id,project_id,title,content,category,version,created_by,updated_by,tags,is_published,created_at,updated_at)VALUES(42,16,'Q3测试计划','Q3测试计划','test_plan','2.1',5,5,'["计划", "Q3"]',true,' 2025-11-28 13:18:00','2026-05-29 18:21:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO test_documents(id,project_id,title,content,category,version,created_by,updated_by,tags,is_published,created_at,updated_at)VALUES(43,16,'API接口测试规范','API测试规范文档','test_plan','2.6',7,7,'["规范", "API"]',true,' 2025-10-24 14:24:00','2026-05-29 17:29:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO test_documents(id,project_id,title,content,category,version,created_by,updated_by,tags,is_published,created_at,updated_at)VALUES(44,16,'自动化说明','自动化测试说明','other','1.5',2,2,'["文档"]',true,' 2026-01-25 10:58:00','2026-05-27 16:40:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO test_documents(id,project_id,title,content,category,version,created_by,updated_by,tags,is_published,created_at,updated_at)VALUES(45,16,'性能测试报告','性能测试报告','test_report','1.6',7,7,'["报告", "性能"]',true,' 2025-12-08 13:10:00','2026-05-31 22:57:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO quality_gates(id,project_id,name,description,is_active,min_pass_rate,max_p95_response_time,max_visual_diff_percentage,created_by,created_at,updated_at)VALUES(1,1,'冒烟门禁','核心冒烟',true,95.0,500,5.0,1,'2025-12-13 22:12:00','2026-05-29 21:14:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO quality_gates(id,project_id,name,description,is_active,min_pass_rate,max_p95_response_time,max_visual_diff_percentage,created_by,created_at,updated_at)VALUES(2,1,'回归门禁','全量回归',true,90.0,1000,10.0,5,'2026-02-04 15:58:00','2026-06-01 12:53:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO quality_gates(id,project_id,name,description,is_active,min_pass_rate,max_p95_response_time,max_visual_diff_percentage,created_by,created_at,updated_at)VALUES(3,2,'冒烟门禁','核心冒烟',true,95.0,500,5.0,1,'2026-03-05 22:43:00','2026-05-31 04:01:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO quality_gates(id,project_id,name,description,is_active,min_pass_rate,max_p95_response_time,max_visual_diff_percentage,created_by,created_at,updated_at)VALUES(4,2,'回归门禁','全量回归',true,90.0,1000,10.0,2,'2025-12-31 21:48:00','2026-05-31 22:08:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO quality_gates(id,project_id,name,description,is_active,min_pass_rate,max_p95_response_time,max_visual_diff_percentage,created_by,created_at,updated_at)VALUES(5,2,'性能门禁','P95响应',true,85.0,2000,NULL,2,'2026-04-14 13:45:00','2026-05-28 05:17:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO quality_gates(id,project_id,name,description,is_active,min_pass_rate,max_p95_response_time,max_visual_diff_percentage,created_by,created_at,updated_at)VALUES(6,3,'冒烟门禁','核心冒烟',true,95.0,500,5.0,5,'2026-03-24 21:07:00','2026-06-01 03:26:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO quality_gates(id,project_id,name,description,is_active,min_pass_rate,max_p95_response_time,max_visual_diff_percentage,created_by,created_at,updated_at)VALUES(7,3,'回归门禁','全量回归',true,90.0,1000,10.0,5,'2026-05-05 23:35:00','2026-06-01 01:55:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO quality_gates(id,project_id,name,description,is_active,min_pass_rate,max_p95_response_time,max_visual_diff_percentage,created_by,created_at,updated_at)VALUES(8,3,'性能门禁','P95响应',true,85.0,2000,NULL,2,'2026-04-14 16:12:00','2026-05-30 10:01:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO quality_gates(id,project_id,name,description,is_active,min_pass_rate,max_p95_response_time,max_visual_diff_percentage,created_by,created_at,updated_at)VALUES(9,4,'冒烟门禁','核心冒烟',true,95.0,500,5.0,2,'2026-02-22 04:24:00','2026-05-31 21:23:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO quality_gates(id,project_id,name,description,is_active,min_pass_rate,max_p95_response_time,max_visual_diff_percentage,created_by,created_at,updated_at)VALUES(10,4,'回归门禁','全量回归',true,90.0,1000,10.0,5,'2026-04-05 23:27:00','2026-05-28 12:37:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO quality_gates(id,project_id,name,description,is_active,min_pass_rate,max_p95_response_time,max_visual_diff_percentage,created_by,created_at,updated_at)VALUES(11,5,'冒烟门禁','核心冒烟',true,95.0,500,5.0,5,'2026-05-04 16:15:00','2026-05-29 22:37:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO quality_gates(id,project_id,name,description,is_active,min_pass_rate,max_p95_response_time,max_visual_diff_percentage,created_by,created_at,updated_at)VALUES(12,5,'性能门禁','P95响应',true,85.0,2000,NULL,5,'2026-03-25 21:06:00','2026-05-28 23:59:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO quality_gates(id,project_id,name,description,is_active,min_pass_rate,max_p95_response_time,max_visual_diff_percentage,created_by,created_at,updated_at)VALUES(13,6,'冒烟门禁','核心冒烟',true,95.0,500,5.0,2,'2025-12-09 00:08:00','2026-05-31 03:00:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO quality_gates(id,project_id,name,description,is_active,min_pass_rate,max_p95_response_time,max_visual_diff_percentage,created_by,created_at,updated_at)VALUES(14,6,'性能门禁','P95响应',true,85.0,2000,NULL,1,'2025-12-10 17:08:00','2026-05-29 07:01:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO quality_gates(id,project_id,name,description,is_active,min_pass_rate,max_p95_response_time,max_visual_diff_percentage,created_by,created_at,updated_at)VALUES(15,7,'冒烟门禁','核心冒烟',true,95.0,500,5.0,2,'2025-12-29 18:50:00','2026-06-02 03:27:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO quality_gates(id,project_id,name,description,is_active,min_pass_rate,max_p95_response_time,max_visual_diff_percentage,created_by,created_at,updated_at)VALUES(16,7,'回归门禁','全量回归',true,90.0,1000,10.0,2,'2026-01-04 02:43:00','2026-06-02 07:07:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO quality_gates(id,project_id,name,description,is_active,min_pass_rate,max_p95_response_time,max_visual_diff_percentage,created_by,created_at,updated_at)VALUES(17,7,'性能门禁','P95响应',true,85.0,2000,NULL,2,'2026-03-15 07:40:00','2026-05-30 19:54:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO quality_gates(id,project_id,name,description,is_active,min_pass_rate,max_p95_response_time,max_visual_diff_percentage,created_by,created_at,updated_at)VALUES(18,8,'冒烟门禁','核心冒烟',true,95.0,500,5.0,2,'2026-04-11 06:47:00','2026-05-28 04:37:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO quality_gates(id,project_id,name,description,is_active,min_pass_rate,max_p95_response_time,max_visual_diff_percentage,created_by,created_at,updated_at)VALUES(19,8,'回归门禁','全量回归',true,90.0,1000,10.0,1,'2026-02-13 18:14:00','2026-05-29 06:45:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO quality_gates(id,project_id,name,description,is_active,min_pass_rate,max_p95_response_time,max_visual_diff_percentage,created_by,created_at,updated_at)VALUES(20,8,'性能门禁','P95响应',true,85.0,2000,NULL,2,'2026-03-12 08:59:00','2026-05-29 01:06:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO quality_gates(id,project_id,name,description,is_active,min_pass_rate,max_p95_response_time,max_visual_diff_percentage,created_by,created_at,updated_at)VALUES(21,9,'回归门禁','全量回归',true,90.0,1000,10.0,1,'2026-03-21 07:58:00','2026-05-31 04:31:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO quality_gates(id,project_id,name,description,is_active,min_pass_rate,max_p95_response_time,max_visual_diff_percentage,created_by,created_at,updated_at)VALUES(22,9,'性能门禁','P95响应',true,85.0,2000,NULL,5,'2026-04-30 11:23:00','2026-05-28 18:25:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO quality_gates(id,project_id,name,description,is_active,min_pass_rate,max_p95_response_time,max_visual_diff_percentage,created_by,created_at,updated_at)VALUES(23,10,'回归门禁','全量回归',true,90.0,1000,10.0,1,'2026-01-30 09:43:00','2026-05-31 05:45:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO quality_gates(id,project_id,name,description,is_active,min_pass_rate,max_p95_response_time,max_visual_diff_percentage,created_by,created_at,updated_at)VALUES(24,10,'性能门禁','P95响应',true,85.0,2000,NULL,5,'2026-01-09 22:35:00','2026-06-01 05:01:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO quality_gates(id,project_id,name,description,is_active,min_pass_rate,max_p95_response_time,max_visual_diff_percentage,created_by,created_at,updated_at)VALUES(25,11,'冒烟门禁','核心冒烟',true,95.0,500,5.0,2,'2026-02-15 08:40:00','2026-05-28 17:34:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO quality_gates(id,project_id,name,description,is_active,min_pass_rate,max_p95_response_time,max_visual_diff_percentage,created_by,created_at,updated_at)VALUES(26,11,'回归门禁','全量回归',true,90.0,1000,10.0,2,'2026-01-14 19:43:00','2026-05-31 04:52:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO quality_gates(id,project_id,name,description,is_active,min_pass_rate,max_p95_response_time,max_visual_diff_percentage,created_by,created_at,updated_at)VALUES(27,11,'性能门禁','P95响应',true,85.0,2000,NULL,2,'2026-01-21 23:13:00','2026-05-28 01:26:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO quality_gates(id,project_id,name,description,is_active,min_pass_rate,max_p95_response_time,max_visual_diff_percentage,created_by,created_at,updated_at)VALUES(28,12,'冒烟门禁','核心冒烟',true,95.0,500,5.0,5,'2026-01-01 20:37:00','2026-05-30 11:07:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO quality_gates(id,project_id,name,description,is_active,min_pass_rate,max_p95_response_time,max_visual_diff_percentage,created_by,created_at,updated_at)VALUES(29,12,'回归门禁','全量回归',true,90.0,1000,10.0,1,'2026-01-24 05:41:00','2026-05-29 06:55:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO quality_gates(id,project_id,name,description,is_active,min_pass_rate,max_p95_response_time,max_visual_diff_percentage,created_by,created_at,updated_at)VALUES(30,12,'性能门禁','P95响应',true,85.0,2000,NULL,2,'2026-03-08 09:52:00','2026-06-02 08:58:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO quality_gates(id,project_id,name,description,is_active,min_pass_rate,max_p95_response_time,max_visual_diff_percentage,created_by,created_at,updated_at)VALUES(31,13,'回归门禁','全量回归',true,90.0,1000,10.0,5,'2026-04-03 15:19:00','2026-06-01 07:45:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO quality_gates(id,project_id,name,description,is_active,min_pass_rate,max_p95_response_time,max_visual_diff_percentage,created_by,created_at,updated_at)VALUES(32,14,'冒烟门禁','核心冒烟',true,95.0,500,5.0,1,'2026-03-09 23:56:00','2026-06-01 09:40:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO quality_gates(id,project_id,name,description,is_active,min_pass_rate,max_p95_response_time,max_visual_diff_percentage,created_by,created_at,updated_at)VALUES(33,14,'回归门禁','全量回归',true,90.0,1000,10.0,1,'2026-01-19 03:20:00','2026-05-27 20:25:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO quality_gates(id,project_id,name,description,is_active,min_pass_rate,max_p95_response_time,max_visual_diff_percentage,created_by,created_at,updated_at)VALUES(34,14,'性能门禁','P95响应',true,85.0,2000,NULL,5,'2026-05-07 00:41:00','2026-05-30 17:27:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO quality_gates(id,project_id,name,description,is_active,min_pass_rate,max_p95_response_time,max_visual_diff_percentage,created_by,created_at,updated_at)VALUES(35,15,'冒烟门禁','核心冒烟',true,95.0,500,5.0,2,'2026-01-01 14:15:00','2026-05-30 05:29:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO quality_gates(id,project_id,name,description,is_active,min_pass_rate,max_p95_response_time,max_visual_diff_percentage,created_by,created_at,updated_at)VALUES(36,15,'回归门禁','全量回归',true,90.0,1000,10.0,5,'2026-04-05 20:32:00','2026-05-27 19:14:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO quality_gates(id,project_id,name,description,is_active,min_pass_rate,max_p95_response_time,max_visual_diff_percentage,created_by,created_at,updated_at)VALUES(37,15,'性能门禁','P95响应',true,85.0,2000,NULL,5,'2026-02-16 05:13:00','2026-06-02 05:37:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO quality_gates(id,project_id,name,description,is_active,min_pass_rate,max_p95_response_time,max_visual_diff_percentage,created_by,created_at,updated_at)VALUES(38,16,'冒烟门禁','核心冒烟',true,95.0,500,5.0,5,'2026-04-19 22:42:00','2026-06-01 07:27:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO quality_gates(id,project_id,name,description,is_active,min_pass_rate,max_p95_response_time,max_visual_diff_percentage,created_by,created_at,updated_at)VALUES(39,16,'回归门禁','全量回归',true,90.0,1000,10.0,1,'2026-01-13 06:13:00','2026-06-01 03:07:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO quality_gate_evaluations(id,quality_gate_id,test_run_id,passed,evaluation_details,created_at)VALUES(1,1,5,true,'{"pass_rate": 92.1, "met": true}','2026-02-08 14:00:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO quality_gate_evaluations(id,quality_gate_id,test_run_id,passed,evaluation_details,created_at)VALUES(2,1,6,true,'{"pass_rate": 92.5, "met": true}','2026-05-24 21:13:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO quality_gate_evaluations(id,quality_gate_id,test_run_id,passed,evaluation_details,created_at)VALUES(3,1,7,true,'{"pass_rate": 97.7, "met": true}','2026-03-27 02:34:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO quality_gate_evaluations(id,quality_gate_id,test_run_id,passed,evaluation_details,created_at)VALUES(4,1,8,true,'{"pass_rate": 89.8, "met": true}','2026-05-05 11:25:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO quality_gate_evaluations(id,quality_gate_id,test_run_id,passed,evaluation_details,created_at)VALUES(5,1,9,true,'{"pass_rate": 86.9, "met": true}','2026-03-25 04:11:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO quality_gate_evaluations(id,quality_gate_id,test_run_id,passed,evaluation_details,created_at)VALUES(6,2,5,true,'{"pass_rate": 88.1, "met": true}','2026-03-03 07:18:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO quality_gate_evaluations(id,quality_gate_id,test_run_id,passed,evaluation_details,created_at)VALUES(7,2,6,true,'{"pass_rate": 83.5, "met": true}','2026-05-08 22:30:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO quality_gate_evaluations(id,quality_gate_id,test_run_id,passed,evaluation_details,created_at)VALUES(8,2,7,true,'{"pass_rate": 86.4, "met": true}','2026-02-25 22:25:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO quality_gate_evaluations(id,quality_gate_id,test_run_id,passed,evaluation_details,created_at)VALUES(9,2,8,true,'{"pass_rate": 89.7, "met": true}','2026-04-14 05:05:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO quality_gate_evaluations(id,quality_gate_id,test_run_id,passed,evaluation_details,created_at)VALUES(10,2,9,false,'{"pass_rate": 98.8, "met": false}','2026-04-21 05:21:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO quality_gate_evaluations(id,quality_gate_id,test_run_id,passed,evaluation_details,created_at)VALUES(11,3,23,true,'{"pass_rate": 90.2, "met": true}','2026-02-21 12:13:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO quality_gate_evaluations(id,quality_gate_id,test_run_id,passed,evaluation_details,created_at)VALUES(12,3,24,true,'{"pass_rate": 87.6, "met": true}','2026-03-08 16:45:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO quality_gate_evaluations(id,quality_gate_id,test_run_id,passed,evaluation_details,created_at)VALUES(13,3,25,true,'{"pass_rate": 87.8, "met": true}','2026-03-23 04:15:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO quality_gate_evaluations(id,quality_gate_id,test_run_id,passed,evaluation_details,created_at)VALUES(14,3,26,true,'{"pass_rate": 99.2, "met": true}','2026-03-10 18:49:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO quality_gate_evaluations(id,quality_gate_id,test_run_id,passed,evaluation_details,created_at)VALUES(15,3,27,true,'{"pass_rate": 89.1, "met": true}','2026-05-05 03:32:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO quality_gate_evaluations(id,quality_gate_id,test_run_id,passed,evaluation_details,created_at)VALUES(16,4,23,true,'{"pass_rate": 98.5, "met": true}','2026-03-09 15:49:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO quality_gate_evaluations(id,quality_gate_id,test_run_id,passed,evaluation_details,created_at)VALUES(17,4,24,true,'{"pass_rate": 86.5, "met": true}','2026-05-10 05:24:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO quality_gate_evaluations(id,quality_gate_id,test_run_id,passed,evaluation_details,created_at)VALUES(18,4,25,false,'{"pass_rate": 98.2, "met": false}','2026-05-04 10:34:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO quality_gate_evaluations(id,quality_gate_id,test_run_id,passed,evaluation_details,created_at)VALUES(19,4,26,true,'{"pass_rate": 99.1, "met": true}','2026-02-27 20:09:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO quality_gate_evaluations(id,quality_gate_id,test_run_id,passed,evaluation_details,created_at)VALUES(20,4,27,true,'{"pass_rate": 93.1, "met": true}','2026-03-19 07:20:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO quality_gate_evaluations(id,quality_gate_id,test_run_id,passed,evaluation_details,created_at)VALUES(21,5,23,true,'{"pass_rate": 84.7, "met": true}','2026-03-23 05:45:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO quality_gate_evaluations(id,quality_gate_id,test_run_id,passed,evaluation_details,created_at)VALUES(22,5,24,true,'{"pass_rate": 86.5, "met": true}','2026-04-15 11:45:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO quality_gate_evaluations(id,quality_gate_id,test_run_id,passed,evaluation_details,created_at)VALUES(23,5,25,false,'{"pass_rate": 97.1, "met": false}','2026-03-24 03:40:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO quality_gate_evaluations(id,quality_gate_id,test_run_id,passed,evaluation_details,created_at)VALUES(24,5,26,false,'{"pass_rate": 98.8, "met": false}','2026-04-27 20:53:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO quality_gate_evaluations(id,quality_gate_id,test_run_id,passed,evaluation_details,created_at)VALUES(25,5,27,true,'{"pass_rate": 94.5, "met": true}','2026-04-02 10:13:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO quality_gate_evaluations(id,quality_gate_id,test_run_id,passed,evaluation_details,created_at)VALUES(26,6,37,true,'{"pass_rate": 84.4, "met": true}','2026-02-17 21:42:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO quality_gate_evaluations(id,quality_gate_id,test_run_id,passed,evaluation_details,created_at)VALUES(27,6,38,true,'{"pass_rate": 98.8, "met": true}','2026-03-19 23:44:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO quality_gate_evaluations(id,quality_gate_id,test_run_id,passed,evaluation_details,created_at)VALUES(28,6,39,true,'{"pass_rate": 91.6, "met": true}','2026-02-21 18:21:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO quality_gate_evaluations(id,quality_gate_id,test_run_id,passed,evaluation_details,created_at)VALUES(29,6,40,true,'{"pass_rate": 83.6, "met": true}','2026-04-04 14:08:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO quality_gate_evaluations(id,quality_gate_id,test_run_id,passed,evaluation_details,created_at)VALUES(30,6,41,false,'{"pass_rate": 88.8, "met": false}','2026-05-08 15:49:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO quality_gate_evaluations(id,quality_gate_id,test_run_id,passed,evaluation_details,created_at)VALUES(31,7,37,true,'{"pass_rate": 81.4, "met": true}','2026-05-24 23:45:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO quality_gate_evaluations(id,quality_gate_id,test_run_id,passed,evaluation_details,created_at)VALUES(32,7,38,false,'{"pass_rate": 89.4, "met": false}','2026-03-25 18:14:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO quality_gate_evaluations(id,quality_gate_id,test_run_id,passed,evaluation_details,created_at)VALUES(33,7,39,true,'{"pass_rate": 84.3, "met": true}','2026-03-02 23:52:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO quality_gate_evaluations(id,quality_gate_id,test_run_id,passed,evaluation_details,created_at)VALUES(34,7,40,false,'{"pass_rate": 99.0, "met": false}','2026-02-03 17:45:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO quality_gate_evaluations(id,quality_gate_id,test_run_id,passed,evaluation_details,created_at)VALUES(35,7,41,true,'{"pass_rate": 83.0, "met": true}','2026-02-17 12:12:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO quality_gate_evaluations(id,quality_gate_id,test_run_id,passed,evaluation_details,created_at)VALUES(36,8,37,true,'{"pass_rate": 82.7, "met": true}','2026-04-15 21:14:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO quality_gate_evaluations(id,quality_gate_id,test_run_id,passed,evaluation_details,created_at)VALUES(37,8,38,true,'{"pass_rate": 91.0, "met": true}','2026-05-10 08:04:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO quality_gate_evaluations(id,quality_gate_id,test_run_id,passed,evaluation_details,created_at)VALUES(38,8,39,true,'{"pass_rate": 85.3, "met": true}','2026-03-22 18:22:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO quality_gate_evaluations(id,quality_gate_id,test_run_id,passed,evaluation_details,created_at)VALUES(39,8,40,true,'{"pass_rate": 90.4, "met": true}','2026-03-28 15:32:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO quality_gate_evaluations(id,quality_gate_id,test_run_id,passed,evaluation_details,created_at)VALUES(40,8,41,true,'{"pass_rate": 93.7, "met": true}','2026-03-04 10:14:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO quality_gate_evaluations(id,quality_gate_id,test_run_id,passed,evaluation_details,created_at)VALUES(41,9,52,true,'{"pass_rate": 93.3, "met": true}','2026-04-17 04:45:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO quality_gate_evaluations(id,quality_gate_id,test_run_id,passed,evaluation_details,created_at)VALUES(42,9,53,false,'{"pass_rate": 87.9, "met": false}','2026-05-25 08:48:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO quality_gate_evaluations(id,quality_gate_id,test_run_id,passed,evaluation_details,created_at)VALUES(43,9,54,true,'{"pass_rate": 85.6, "met": true}','2026-04-24 02:01:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO quality_gate_evaluations(id,quality_gate_id,test_run_id,passed,evaluation_details,created_at)VALUES(44,9,55,true,'{"pass_rate": 92.9, "met": true}','2026-02-16 15:06:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO quality_gate_evaluations(id,quality_gate_id,test_run_id,passed,evaluation_details,created_at)VALUES(45,9,56,false,'{"pass_rate": 86.4, "met": false}','2026-04-04 07:38:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO quality_gate_evaluations(id,quality_gate_id,test_run_id,passed,evaluation_details,created_at)VALUES(46,10,52,true,'{"pass_rate": 99.1, "met": true}','2026-02-09 10:24:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO quality_gate_evaluations(id,quality_gate_id,test_run_id,passed,evaluation_details,created_at)VALUES(47,10,53,true,'{"pass_rate": 80.5, "met": true}','2026-05-12 13:24:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO quality_gate_evaluations(id,quality_gate_id,test_run_id,passed,evaluation_details,created_at)VALUES(48,10,54,true,'{"pass_rate": 95.6, "met": true}','2026-02-27 15:13:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO quality_gate_evaluations(id,quality_gate_id,test_run_id,passed,evaluation_details,created_at)VALUES(49,10,55,true,'{"pass_rate": 93.3, "met": true}','2026-05-21 00:48:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO quality_gate_evaluations(id,quality_gate_id,test_run_id,passed,evaluation_details,created_at)VALUES(50,10,56,true,'{"pass_rate": 85.5, "met": true}','2026-02-09 10:28:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO quality_gate_evaluations(id,quality_gate_id,test_run_id,passed,evaluation_details,created_at)VALUES(51,11,61,true,'{"pass_rate": 81.1, "met": true}','2026-02-16 03:02:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO quality_gate_evaluations(id,quality_gate_id,test_run_id,passed,evaluation_details,created_at)VALUES(52,11,62,true,'{"pass_rate": 91.5, "met": true}','2026-04-02 07:47:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO quality_gate_evaluations(id,quality_gate_id,test_run_id,passed,evaluation_details,created_at)VALUES(53,11,63,false,'{"pass_rate": 90.0, "met": false}','2026-03-16 06:51:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO quality_gate_evaluations(id,quality_gate_id,test_run_id,passed,evaluation_details,created_at)VALUES(54,11,64,true,'{"pass_rate": 81.0, "met": true}','2026-05-12 10:51:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO quality_gate_evaluations(id,quality_gate_id,test_run_id,passed,evaluation_details,created_at)VALUES(55,11,65,true,'{"pass_rate": 84.1, "met": true}','2026-05-16 12:01:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO quality_gate_evaluations(id,quality_gate_id,test_run_id,passed,evaluation_details,created_at)VALUES(56,12,61,true,'{"pass_rate": 88.2, "met": true}','2026-02-24 12:52:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO quality_gate_evaluations(id,quality_gate_id,test_run_id,passed,evaluation_details,created_at)VALUES(57,12,62,true,'{"pass_rate": 82.3, "met": true}','2026-02-22 10:17:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO quality_gate_evaluations(id,quality_gate_id,test_run_id,passed,evaluation_details,created_at)VALUES(58,12,63,true,'{"pass_rate": 82.3, "met": true}','2026-04-13 21:54:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO quality_gate_evaluations(id,quality_gate_id,test_run_id,passed,evaluation_details,created_at)VALUES(59,12,64,true,'{"pass_rate": 98.3, "met": true}','2026-05-27 06:21:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO quality_gate_evaluations(id,quality_gate_id,test_run_id,passed,evaluation_details,created_at)VALUES(60,12,65,true,'{"pass_rate": 88.9, "met": true}','2026-02-28 23:18:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO quality_gate_evaluations(id,quality_gate_id,test_run_id,passed,evaluation_details,created_at)VALUES(61,13,71,false,'{"pass_rate": 95.2, "met": false}','2026-02-02 02:48:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO quality_gate_evaluations(id,quality_gate_id,test_run_id,passed,evaluation_details,created_at)VALUES(62,13,72,false,'{"pass_rate": 94.9, "met": false}','2026-05-05 08:42:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO quality_gate_evaluations(id,quality_gate_id,test_run_id,passed,evaluation_details,created_at)VALUES(63,13,73,false,'{"pass_rate": 83.8, "met": false}','2026-04-13 23:47:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO quality_gate_evaluations(id,quality_gate_id,test_run_id,passed,evaluation_details,created_at)VALUES(64,13,74,false,'{"pass_rate": 80.3, "met": false}','2026-05-09 19:19:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO quality_gate_evaluations(id,quality_gate_id,test_run_id,passed,evaluation_details,created_at)VALUES(65,13,75,true,'{"pass_rate": 95.5, "met": true}','2026-05-19 05:12:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO quality_gate_evaluations(id,quality_gate_id,test_run_id,passed,evaluation_details,created_at)VALUES(66,14,71,true,'{"pass_rate": 83.5, "met": true}','2026-05-21 00:59:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO quality_gate_evaluations(id,quality_gate_id,test_run_id,passed,evaluation_details,created_at)VALUES(67,14,72,false,'{"pass_rate": 93.7, "met": false}','2026-03-12 17:52:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO quality_gate_evaluations(id,quality_gate_id,test_run_id,passed,evaluation_details,created_at)VALUES(68,14,73,true,'{"pass_rate": 97.2, "met": true}','2026-03-19 12:40:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO quality_gate_evaluations(id,quality_gate_id,test_run_id,passed,evaluation_details,created_at)VALUES(69,14,74,true,'{"pass_rate": 83.0, "met": true}','2026-04-25 21:52:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO quality_gate_evaluations(id,quality_gate_id,test_run_id,passed,evaluation_details,created_at)VALUES(70,14,75,true,'{"pass_rate": 96.8, "met": true}','2026-03-18 03:16:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO quality_gate_evaluations(id,quality_gate_id,test_run_id,passed,evaluation_details,created_at)VALUES(71,15,82,true,'{"pass_rate": 99.9, "met": true}','2026-04-17 10:36:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO quality_gate_evaluations(id,quality_gate_id,test_run_id,passed,evaluation_details,created_at)VALUES(72,15,83,true,'{"pass_rate": 96.2, "met": true}','2026-02-26 14:00:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO quality_gate_evaluations(id,quality_gate_id,test_run_id,passed,evaluation_details,created_at)VALUES(73,15,84,true,'{"pass_rate": 94.3, "met": true}','2026-03-20 14:38:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO quality_gate_evaluations(id,quality_gate_id,test_run_id,passed,evaluation_details,created_at)VALUES(74,15,85,true,'{"pass_rate": 95.6, "met": true}','2026-03-18 18:08:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO quality_gate_evaluations(id,quality_gate_id,test_run_id,passed,evaluation_details,created_at)VALUES(75,15,86,true,'{"pass_rate": 95.5, "met": true}','2026-05-02 19:53:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO quality_gate_evaluations(id,quality_gate_id,test_run_id,passed,evaluation_details,created_at)VALUES(76,16,82,true,'{"pass_rate": 85.5, "met": true}','2026-04-07 22:25:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO quality_gate_evaluations(id,quality_gate_id,test_run_id,passed,evaluation_details,created_at)VALUES(77,16,83,true,'{"pass_rate": 90.8, "met": true}','2026-04-13 00:12:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO quality_gate_evaluations(id,quality_gate_id,test_run_id,passed,evaluation_details,created_at)VALUES(78,16,84,true,'{"pass_rate": 84.2, "met": true}','2026-05-29 01:56:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO quality_gate_evaluations(id,quality_gate_id,test_run_id,passed,evaluation_details,created_at)VALUES(79,16,85,true,'{"pass_rate": 80.5, "met": true}','2026-04-01 08:33:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO quality_gate_evaluations(id,quality_gate_id,test_run_id,passed,evaluation_details,created_at)VALUES(80,16,86,true,'{"pass_rate": 87.2, "met": true}','2026-05-11 18:46:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO quality_gate_evaluations(id,quality_gate_id,test_run_id,passed,evaluation_details,created_at)VALUES(81,17,82,false,'{"pass_rate": 89.9, "met": false}','2026-05-25 04:22:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO quality_gate_evaluations(id,quality_gate_id,test_run_id,passed,evaluation_details,created_at)VALUES(82,17,83,false,'{"pass_rate": 81.2, "met": false}','2026-02-28 10:55:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO quality_gate_evaluations(id,quality_gate_id,test_run_id,passed,evaluation_details,created_at)VALUES(83,17,84,true,'{"pass_rate": 88.5, "met": true}','2026-03-18 09:34:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO quality_gate_evaluations(id,quality_gate_id,test_run_id,passed,evaluation_details,created_at)VALUES(84,17,85,true,'{"pass_rate": 82.6, "met": true}','2026-02-11 00:27:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO quality_gate_evaluations(id,quality_gate_id,test_run_id,passed,evaluation_details,created_at)VALUES(85,17,86,true,'{"pass_rate": 86.8, "met": true}','2026-04-29 04:08:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO quality_gate_evaluations(id,quality_gate_id,test_run_id,passed,evaluation_details,created_at)VALUES(86,18,92,true,'{"pass_rate": 84.4, "met": true}','2026-03-03 00:58:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO quality_gate_evaluations(id,quality_gate_id,test_run_id,passed,evaluation_details,created_at)VALUES(87,18,93,true,'{"pass_rate": 81.2, "met": true}','2026-05-29 14:37:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO quality_gate_evaluations(id,quality_gate_id,test_run_id,passed,evaluation_details,created_at)VALUES(88,18,94,true,'{"pass_rate": 99.1, "met": true}','2026-03-20 13:32:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO quality_gate_evaluations(id,quality_gate_id,test_run_id,passed,evaluation_details,created_at)VALUES(89,18,95,true,'{"pass_rate": 88.5, "met": true}','2026-02-21 00:21:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO quality_gate_evaluations(id,quality_gate_id,test_run_id,passed,evaluation_details,created_at)VALUES(90,18,96,true,'{"pass_rate": 87.4, "met": true}','2026-03-17 12:11:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO quality_gate_evaluations(id,quality_gate_id,test_run_id,passed,evaluation_details,created_at)VALUES(91,19,92,true,'{"pass_rate": 87.4, "met": true}','2026-04-08 04:45:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO quality_gate_evaluations(id,quality_gate_id,test_run_id,passed,evaluation_details,created_at)VALUES(92,19,93,true,'{"pass_rate": 89.6, "met": true}','2026-05-19 05:07:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO quality_gate_evaluations(id,quality_gate_id,test_run_id,passed,evaluation_details,created_at)VALUES(93,19,94,true,'{"pass_rate": 89.2, "met": true}','2026-06-01 06:58:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO quality_gate_evaluations(id,quality_gate_id,test_run_id,passed,evaluation_details,created_at)VALUES(94,19,95,false,'{"pass_rate": 81.2, "met": false}','2026-05-16 17:53:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO quality_gate_evaluations(id,quality_gate_id,test_run_id,passed,evaluation_details,created_at)VALUES(95,19,96,true,'{"pass_rate": 84.1, "met": true}','2026-02-17 10:10:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO quality_gate_evaluations(id,quality_gate_id,test_run_id,passed,evaluation_details,created_at)VALUES(96,20,92,true,'{"pass_rate": 91.1, "met": true}','2026-05-19 19:35:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO quality_gate_evaluations(id,quality_gate_id,test_run_id,passed,evaluation_details,created_at)VALUES(97,20,93,true,'{"pass_rate": 95.3, "met": true}','2026-05-20 18:50:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO quality_gate_evaluations(id,quality_gate_id,test_run_id,passed,evaluation_details,created_at)VALUES(98,20,94,true,'{"pass_rate": 90.3, "met": true}','2026-03-24 09:27:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO quality_gate_evaluations(id,quality_gate_id,test_run_id,passed,evaluation_details,created_at)VALUES(99,20,95,true,'{"pass_rate": 96.2, "met": true}','2026-03-07 22:32:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO quality_gate_evaluations(id,quality_gate_id,test_run_id,passed,evaluation_details,created_at)VALUES(100,20,96,true,'{"pass_rate": 83.0, "met": true}','2026-05-28 10:54:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO quality_gate_evaluations(id,quality_gate_id,test_run_id,passed,evaluation_details,created_at)VALUES(101,21,109,true,'{"pass_rate": 94.1, "met": true}','2026-04-03 07:48:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO quality_gate_evaluations(id,quality_gate_id,test_run_id,passed,evaluation_details,created_at)VALUES(102,21,110,false,'{"pass_rate": 80.8, "met": false}','2026-04-05 06:45:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO quality_gate_evaluations(id,quality_gate_id,test_run_id,passed,evaluation_details,created_at)VALUES(103,21,111,true,'{"pass_rate": 89.2, "met": true}','2026-05-02 23:55:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO quality_gate_evaluations(id,quality_gate_id,test_run_id,passed,evaluation_details,created_at)VALUES(104,21,112,true,'{"pass_rate": 96.3, "met": true}','2026-04-25 22:27:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO quality_gate_evaluations(id,quality_gate_id,test_run_id,passed,evaluation_details,created_at)VALUES(105,21,113,true,'{"pass_rate": 89.8, "met": true}','2026-05-06 21:49:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO quality_gate_evaluations(id,quality_gate_id,test_run_id,passed,evaluation_details,created_at)VALUES(106,22,109,true,'{"pass_rate": 94.1, "met": true}','2026-05-29 09:24:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO quality_gate_evaluations(id,quality_gate_id,test_run_id,passed,evaluation_details,created_at)VALUES(107,22,110,true,'{"pass_rate": 83.6, "met": true}','2026-03-24 17:17:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO quality_gate_evaluations(id,quality_gate_id,test_run_id,passed,evaluation_details,created_at)VALUES(108,22,111,true,'{"pass_rate": 88.9, "met": true}','2026-03-02 20:22:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO quality_gate_evaluations(id,quality_gate_id,test_run_id,passed,evaluation_details,created_at)VALUES(109,22,112,true,'{"pass_rate": 89.9, "met": true}','2026-05-06 06:25:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO quality_gate_evaluations(id,quality_gate_id,test_run_id,passed,evaluation_details,created_at)VALUES(110,22,113,true,'{"pass_rate": 86.7, "met": true}','2026-03-08 03:22:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO quality_gate_evaluations(id,quality_gate_id,test_run_id,passed,evaluation_details,created_at)VALUES(111,23,128,true,'{"pass_rate": 83.1, "met": true}','2026-02-17 19:01:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO quality_gate_evaluations(id,quality_gate_id,test_run_id,passed,evaluation_details,created_at)VALUES(112,23,129,true,'{"pass_rate": 96.8, "met": true}','2026-02-07 21:33:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO quality_gate_evaluations(id,quality_gate_id,test_run_id,passed,evaluation_details,created_at)VALUES(113,23,130,true,'{"pass_rate": 81.6, "met": true}','2026-03-19 07:27:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO quality_gate_evaluations(id,quality_gate_id,test_run_id,passed,evaluation_details,created_at)VALUES(114,23,131,true,'{"pass_rate": 96.6, "met": true}','2026-03-03 18:59:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO quality_gate_evaluations(id,quality_gate_id,test_run_id,passed,evaluation_details,created_at)VALUES(115,23,132,true,'{"pass_rate": 81.2, "met": true}','2026-04-27 21:34:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO quality_gate_evaluations(id,quality_gate_id,test_run_id,passed,evaluation_details,created_at)VALUES(116,24,128,true,'{"pass_rate": 82.0, "met": true}','2026-04-19 13:23:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO quality_gate_evaluations(id,quality_gate_id,test_run_id,passed,evaluation_details,created_at)VALUES(117,24,129,true,'{"pass_rate": 95.1, "met": true}','2026-02-20 06:57:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO quality_gate_evaluations(id,quality_gate_id,test_run_id,passed,evaluation_details,created_at)VALUES(118,24,130,true,'{"pass_rate": 91.8, "met": true}','2026-03-07 19:53:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO quality_gate_evaluations(id,quality_gate_id,test_run_id,passed,evaluation_details,created_at)VALUES(119,24,131,true,'{"pass_rate": 80.7, "met": true}','2026-02-25 13:44:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO quality_gate_evaluations(id,quality_gate_id,test_run_id,passed,evaluation_details,created_at)VALUES(120,24,132,false,'{"pass_rate": 84.7, "met": false}','2026-02-22 16:56:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO quality_gate_evaluations(id,quality_gate_id,test_run_id,passed,evaluation_details,created_at)VALUES(121,25,142,false,'{"pass_rate": 95.1, "met": false}','2026-02-11 11:20:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO quality_gate_evaluations(id,quality_gate_id,test_run_id,passed,evaluation_details,created_at)VALUES(122,25,143,true,'{"pass_rate": 91.5, "met": true}','2026-04-22 02:18:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO quality_gate_evaluations(id,quality_gate_id,test_run_id,passed,evaluation_details,created_at)VALUES(123,25,144,true,'{"pass_rate": 86.3, "met": true}','2026-05-10 08:44:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO quality_gate_evaluations(id,quality_gate_id,test_run_id,passed,evaluation_details,created_at)VALUES(124,25,145,false,'{"pass_rate": 92.2, "met": false}','2026-05-27 15:41:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO quality_gate_evaluations(id,quality_gate_id,test_run_id,passed,evaluation_details,created_at)VALUES(125,25,146,false,'{"pass_rate": 96.4, "met": false}','2026-02-02 21:10:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO quality_gate_evaluations(id,quality_gate_id,test_run_id,passed,evaluation_details,created_at)VALUES(126,26,142,false,'{"pass_rate": 90.6, "met": false}','2026-03-29 13:46:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO quality_gate_evaluations(id,quality_gate_id,test_run_id,passed,evaluation_details,created_at)VALUES(127,26,143,true,'{"pass_rate": 84.0, "met": true}','2026-03-17 19:17:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO quality_gate_evaluations(id,quality_gate_id,test_run_id,passed,evaluation_details,created_at)VALUES(128,26,144,true,'{"pass_rate": 96.3, "met": true}','2026-04-13 14:25:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO quality_gate_evaluations(id,quality_gate_id,test_run_id,passed,evaluation_details,created_at)VALUES(129,26,145,true,'{"pass_rate": 82.0, "met": true}','2026-02-04 21:54:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO quality_gate_evaluations(id,quality_gate_id,test_run_id,passed,evaluation_details,created_at)VALUES(130,26,146,true,'{"pass_rate": 84.3, "met": true}','2026-04-26 08:29:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO quality_gate_evaluations(id,quality_gate_id,test_run_id,passed,evaluation_details,created_at)VALUES(131,27,142,true,'{"pass_rate": 91.4, "met": true}','2026-05-01 02:07:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO quality_gate_evaluations(id,quality_gate_id,test_run_id,passed,evaluation_details,created_at)VALUES(132,27,143,true,'{"pass_rate": 95.2, "met": true}','2026-04-07 04:47:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO quality_gate_evaluations(id,quality_gate_id,test_run_id,passed,evaluation_details,created_at)VALUES(133,27,144,false,'{"pass_rate": 93.4, "met": false}','2026-03-17 00:23:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO quality_gate_evaluations(id,quality_gate_id,test_run_id,passed,evaluation_details,created_at)VALUES(134,27,145,false,'{"pass_rate": 98.2, "met": false}','2026-03-14 19:09:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO quality_gate_evaluations(id,quality_gate_id,test_run_id,passed,evaluation_details,created_at)VALUES(135,27,146,true,'{"pass_rate": 81.3, "met": true}','2026-02-16 01:50:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO quality_gate_evaluations(id,quality_gate_id,test_run_id,passed,evaluation_details,created_at)VALUES(136,28,157,true,'{"pass_rate": 97.0, "met": true}','2026-03-09 05:59:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO quality_gate_evaluations(id,quality_gate_id,test_run_id,passed,evaluation_details,created_at)VALUES(137,28,158,true,'{"pass_rate": 89.3, "met": true}','2026-03-27 19:08:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO quality_gate_evaluations(id,quality_gate_id,test_run_id,passed,evaluation_details,created_at)VALUES(138,28,159,false,'{"pass_rate": 96.9, "met": false}','2026-05-19 07:34:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO quality_gate_evaluations(id,quality_gate_id,test_run_id,passed,evaluation_details,created_at)VALUES(139,28,160,true,'{"pass_rate": 96.8, "met": true}','2026-03-08 12:18:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO quality_gate_evaluations(id,quality_gate_id,test_run_id,passed,evaluation_details,created_at)VALUES(140,28,161,true,'{"pass_rate": 92.6, "met": true}','2026-03-08 13:44:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO quality_gate_evaluations(id,quality_gate_id,test_run_id,passed,evaluation_details,created_at)VALUES(141,29,157,true,'{"pass_rate": 97.0, "met": true}','2026-02-05 16:09:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO quality_gate_evaluations(id,quality_gate_id,test_run_id,passed,evaluation_details,created_at)VALUES(142,29,158,true,'{"pass_rate": 84.7, "met": true}','2026-03-05 11:12:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO quality_gate_evaluations(id,quality_gate_id,test_run_id,passed,evaluation_details,created_at)VALUES(143,29,159,false,'{"pass_rate": 91.4, "met": false}','2026-03-16 17:04:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO quality_gate_evaluations(id,quality_gate_id,test_run_id,passed,evaluation_details,created_at)VALUES(144,29,160,false,'{"pass_rate": 89.0, "met": false}','2026-05-14 06:55:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO quality_gate_evaluations(id,quality_gate_id,test_run_id,passed,evaluation_details,created_at)VALUES(145,29,161,true,'{"pass_rate": 99.3, "met": true}','2026-02-27 16:28:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO quality_gate_evaluations(id,quality_gate_id,test_run_id,passed,evaluation_details,created_at)VALUES(146,30,157,false,'{"pass_rate": 99.3, "met": false}','2026-02-02 12:28:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO quality_gate_evaluations(id,quality_gate_id,test_run_id,passed,evaluation_details,created_at)VALUES(147,30,158,true,'{"pass_rate": 96.3, "met": true}','2026-02-13 07:26:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO quality_gate_evaluations(id,quality_gate_id,test_run_id,passed,evaluation_details,created_at)VALUES(148,30,159,true,'{"pass_rate": 97.9, "met": true}','2026-04-23 16:52:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO quality_gate_evaluations(id,quality_gate_id,test_run_id,passed,evaluation_details,created_at)VALUES(149,30,160,true,'{"pass_rate": 95.2, "met": true}','2026-04-04 22:27:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO quality_gate_evaluations(id,quality_gate_id,test_run_id,passed,evaluation_details,created_at)VALUES(150,30,161,false,'{"pass_rate": 94.7, "met": false}','2026-05-02 15:32:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO quality_gate_evaluations(id,quality_gate_id,test_run_id,passed,evaluation_details,created_at)VALUES(151,31,170,false,'{"pass_rate": 87.5, "met": false}','2026-02-02 09:26:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO quality_gate_evaluations(id,quality_gate_id,test_run_id,passed,evaluation_details,created_at)VALUES(152,31,171,true,'{"pass_rate": 81.2, "met": true}','2026-05-29 01:26:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO quality_gate_evaluations(id,quality_gate_id,test_run_id,passed,evaluation_details,created_at)VALUES(153,31,172,true,'{"pass_rate": 88.4, "met": true}','2026-04-21 18:18:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO quality_gate_evaluations(id,quality_gate_id,test_run_id,passed,evaluation_details,created_at)VALUES(154,31,173,true,'{"pass_rate": 96.6, "met": true}','2026-05-09 03:36:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO quality_gate_evaluations(id,quality_gate_id,test_run_id,passed,evaluation_details,created_at)VALUES(155,31,174,false,'{"pass_rate": 81.7, "met": false}','2026-03-16 21:55:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO quality_gate_evaluations(id,quality_gate_id,test_run_id,passed,evaluation_details,created_at)VALUES(156,32,186,true,'{"pass_rate": 98.7, "met": true}','2026-03-27 18:17:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO quality_gate_evaluations(id,quality_gate_id,test_run_id,passed,evaluation_details,created_at)VALUES(157,32,187,false,'{"pass_rate": 85.4, "met": false}','2026-05-10 14:18:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO quality_gate_evaluations(id,quality_gate_id,test_run_id,passed,evaluation_details,created_at)VALUES(158,32,188,true,'{"pass_rate": 91.2, "met": true}','2026-03-29 05:31:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO quality_gate_evaluations(id,quality_gate_id,test_run_id,passed,evaluation_details,created_at)VALUES(159,32,189,true,'{"pass_rate": 91.6, "met": true}','2026-03-07 18:18:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO quality_gate_evaluations(id,quality_gate_id,test_run_id,passed,evaluation_details,created_at)VALUES(160,32,190,true,'{"pass_rate": 85.3, "met": true}','2026-03-17 22:46:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO quality_gate_evaluations(id,quality_gate_id,test_run_id,passed,evaluation_details,created_at)VALUES(161,33,186,true,'{"pass_rate": 85.2, "met": true}','2026-02-20 07:10:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO quality_gate_evaluations(id,quality_gate_id,test_run_id,passed,evaluation_details,created_at)VALUES(162,33,187,false,'{"pass_rate": 88.5, "met": false}','2026-04-16 20:58:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO quality_gate_evaluations(id,quality_gate_id,test_run_id,passed,evaluation_details,created_at)VALUES(163,33,188,true,'{"pass_rate": 98.0, "met": true}','2026-03-11 02:49:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO quality_gate_evaluations(id,quality_gate_id,test_run_id,passed,evaluation_details,created_at)VALUES(164,33,189,true,'{"pass_rate": 85.7, "met": true}','2026-02-06 11:25:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO quality_gate_evaluations(id,quality_gate_id,test_run_id,passed,evaluation_details,created_at)VALUES(165,33,190,false,'{"pass_rate": 84.5, "met": false}','2026-02-28 21:38:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO quality_gate_evaluations(id,quality_gate_id,test_run_id,passed,evaluation_details,created_at)VALUES(166,34,186,true,'{"pass_rate": 95.6, "met": true}','2026-04-03 15:09:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO quality_gate_evaluations(id,quality_gate_id,test_run_id,passed,evaluation_details,created_at)VALUES(167,34,187,true,'{"pass_rate": 83.6, "met": true}','2026-03-12 08:04:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO quality_gate_evaluations(id,quality_gate_id,test_run_id,passed,evaluation_details,created_at)VALUES(168,34,188,false,'{"pass_rate": 98.5, "met": false}','2026-03-03 13:42:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO quality_gate_evaluations(id,quality_gate_id,test_run_id,passed,evaluation_details,created_at)VALUES(169,34,189,false,'{"pass_rate": 87.5, "met": false}','2026-03-24 02:14:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO quality_gate_evaluations(id,quality_gate_id,test_run_id,passed,evaluation_details,created_at)VALUES(170,34,190,true,'{"pass_rate": 98.7, "met": true}','2026-04-08 09:43:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO quality_gate_evaluations(id,quality_gate_id,test_run_id,passed,evaluation_details,created_at)VALUES(171,35,196,true,'{"pass_rate": 90.2, "met": true}','2026-05-13 07:32:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO quality_gate_evaluations(id,quality_gate_id,test_run_id,passed,evaluation_details,created_at)VALUES(172,35,197,true,'{"pass_rate": 83.1, "met": true}','2026-04-19 06:36:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO quality_gate_evaluations(id,quality_gate_id,test_run_id,passed,evaluation_details,created_at)VALUES(173,35,198,true,'{"pass_rate": 83.2, "met": true}','2026-02-01 22:23:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO quality_gate_evaluations(id,quality_gate_id,test_run_id,passed,evaluation_details,created_at)VALUES(174,35,199,true,'{"pass_rate": 96.5, "met": true}','2026-04-10 01:26:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO quality_gate_evaluations(id,quality_gate_id,test_run_id,passed,evaluation_details,created_at)VALUES(175,35,200,false,'{"pass_rate": 82.5, "met": false}','2026-03-28 15:10:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO quality_gate_evaluations(id,quality_gate_id,test_run_id,passed,evaluation_details,created_at)VALUES(176,36,196,true,'{"pass_rate": 85.3, "met": true}','2026-04-10 16:16:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO quality_gate_evaluations(id,quality_gate_id,test_run_id,passed,evaluation_details,created_at)VALUES(177,36,197,false,'{"pass_rate": 84.6, "met": false}','2026-05-26 20:52:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO quality_gate_evaluations(id,quality_gate_id,test_run_id,passed,evaluation_details,created_at)VALUES(178,36,198,true,'{"pass_rate": 87.9, "met": true}','2026-05-12 17:32:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO quality_gate_evaluations(id,quality_gate_id,test_run_id,passed,evaluation_details,created_at)VALUES(179,36,199,false,'{"pass_rate": 91.5, "met": false}','2026-04-08 09:21:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO quality_gate_evaluations(id,quality_gate_id,test_run_id,passed,evaluation_details,created_at)VALUES(180,36,200,true,'{"pass_rate": 81.8, "met": true}','2026-05-23 03:07:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO quality_gate_evaluations(id,quality_gate_id,test_run_id,passed,evaluation_details,created_at)VALUES(181,37,196,true,'{"pass_rate": 91.7, "met": true}','2026-02-24 10:45:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO quality_gate_evaluations(id,quality_gate_id,test_run_id,passed,evaluation_details,created_at)VALUES(182,37,197,true,'{"pass_rate": 93.2, "met": true}','2026-03-16 13:08:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO quality_gate_evaluations(id,quality_gate_id,test_run_id,passed,evaluation_details,created_at)VALUES(183,37,198,true,'{"pass_rate": 100.0, "met": true}','2026-02-10 03:15:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO quality_gate_evaluations(id,quality_gate_id,test_run_id,passed,evaluation_details,created_at)VALUES(184,37,199,true,'{"pass_rate": 82.2, "met": true}','2026-05-04 18:14:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO quality_gate_evaluations(id,quality_gate_id,test_run_id,passed,evaluation_details,created_at)VALUES(185,37,200,true,'{"pass_rate": 97.9, "met": true}','2026-04-19 04:45:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO quality_gate_evaluations(id,quality_gate_id,test_run_id,passed,evaluation_details,created_at)VALUES(186,38,205,true,'{"pass_rate": 98.4, "met": true}','2026-04-20 16:28:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO quality_gate_evaluations(id,quality_gate_id,test_run_id,passed,evaluation_details,created_at)VALUES(187,38,206,true,'{"pass_rate": 88.0, "met": true}','2026-02-21 11:59:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO quality_gate_evaluations(id,quality_gate_id,test_run_id,passed,evaluation_details,created_at)VALUES(188,38,207,true,'{"pass_rate": 87.2, "met": true}','2026-04-27 00:29:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO quality_gate_evaluations(id,quality_gate_id,test_run_id,passed,evaluation_details,created_at)VALUES(189,38,208,true,'{"pass_rate": 85.2, "met": true}','2026-03-15 06:33:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO quality_gate_evaluations(id,quality_gate_id,test_run_id,passed,evaluation_details,created_at)VALUES(190,38,209,true,'{"pass_rate": 93.0, "met": true}','2026-02-10 03:16:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO quality_gate_evaluations(id,quality_gate_id,test_run_id,passed,evaluation_details,created_at)VALUES(191,39,205,true,'{"pass_rate": 85.5, "met": true}','2026-02-20 15:34:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO quality_gate_evaluations(id,quality_gate_id,test_run_id,passed,evaluation_details,created_at)VALUES(192,39,206,true,'{"pass_rate": 96.9, "met": true}','2026-04-01 10:30:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO quality_gate_evaluations(id,quality_gate_id,test_run_id,passed,evaluation_details,created_at)VALUES(193,39,207,true,'{"pass_rate": 95.4, "met": true}','2026-05-15 11:44:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO quality_gate_evaluations(id,quality_gate_id,test_run_id,passed,evaluation_details,created_at)VALUES(194,39,208,false,'{"pass_rate": 90.8, "met": false}','2026-02-24 16:20:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO quality_gate_evaluations(id,quality_gate_id,test_run_id,passed,evaluation_details,created_at)VALUES(195,39,209,true,'{"pass_rate": 90.9, "met": true}','2026-02-04 11:00:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO trigger_rules(id,project_id,name,description,is_active,trigger_event,target_branches,test_types,target_type,created_by,created_at,updated_at)VALUES(1,1,'Push冒烟','自动Push冒烟',true,'push','["main", "develop"]','["api"]','api_collection',2,'2026-01-11 05:54:00','2026-05-31 07:32:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO trigger_rules(id,project_id,name,description,is_active,trigger_event,target_branches,test_types,target_type,created_by,created_at,updated_at)VALUES(2,1,'Release全量','自动Release全量',true,'tag','[]','["api", "web", "perf"]','web_collection',1,'2026-04-04 23:21:00','2026-05-31 21:20:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO trigger_rules(id,project_id,name,description,is_active,trigger_event,target_branches,test_types,target_type,created_by,created_at,updated_at)VALUES(3,2,'Push冒烟','自动Push冒烟',true,'push','["main", "develop"]','["api"]','api_collection',2,'2026-01-12 20:21:00','2026-05-31 11:23:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO trigger_rules(id,project_id,name,description,is_active,trigger_event,target_branches,test_types,target_type,created_by,created_at,updated_at)VALUES(4,2,'PR回归','自动PR回归',true,'pull_request','["main"]','["api", "web"]','api_collection',5,'2026-01-11 19:41:00','2026-05-29 15:41:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO trigger_rules(id,project_id,name,description,is_active,trigger_event,target_branches,test_types,target_type,created_by,created_at,updated_at)VALUES(5,2,'Release全量','自动Release全量',true,'tag','[]','["api", "web", "perf"]','web_collection',1,'2026-03-09 23:23:00','2026-05-30 23:09:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO trigger_rules(id,project_id,name,description,is_active,trigger_event,target_branches,test_types,target_type,created_by,created_at,updated_at)VALUES(6,3,'Push冒烟','自动Push冒烟',true,'push','["main", "develop"]','["api"]','api_collection',1,'2026-04-30 14:52:00','2026-06-01 08:06:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO trigger_rules(id,project_id,name,description,is_active,trigger_event,target_branches,test_types,target_type,created_by,created_at,updated_at)VALUES(7,3,'PR回归','自动PR回归',true,'pull_request','["main"]','["api", "web"]','api_collection',2,'2026-03-01 02:16:00','2026-05-29 11:58:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO trigger_rules(id,project_id,name,description,is_active,trigger_event,target_branches,test_types,target_type,created_by,created_at,updated_at)VALUES(8,3,'Release全量','自动Release全量',true,'tag','[]','["api", "web", "perf"]','web_collection',1,'2026-01-31 07:33:00','2026-06-02 02:07:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO trigger_rules(id,project_id,name,description,is_active,trigger_event,target_branches,test_types,target_type,created_by,created_at,updated_at)VALUES(9,4,'Push冒烟','自动Push冒烟',true,'push','["main", "develop"]','["api"]','api_collection',5,'2026-02-20 03:34:00','2026-05-31 02:34:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO trigger_rules(id,project_id,name,description,is_active,trigger_event,target_branches,test_types,target_type,created_by,created_at,updated_at)VALUES(10,4,'PR回归','自动PR回归',true,'pull_request','["main"]','["api", "web"]','api_collection',5,'2026-04-30 06:28:00','2026-05-30 23:37:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO trigger_rules(id,project_id,name,description,is_active,trigger_event,target_branches,test_types,target_type,created_by,created_at,updated_at)VALUES(11,4,'Release全量','自动Release全量',true,'tag','[]','["api", "web", "perf"]','web_collection',2,'2026-01-28 09:57:00','2026-06-01 14:19:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO trigger_rules(id,project_id,name,description,is_active,trigger_event,target_branches,test_types,target_type,created_by,created_at,updated_at)VALUES(12,5,'Push冒烟','自动Push冒烟',true,'push','["main", "develop"]','["api"]','api_collection',2,'2026-04-28 00:27:00','2026-05-31 04:57:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO trigger_rules(id,project_id,name,description,is_active,trigger_event,target_branches,test_types,target_type,created_by,created_at,updated_at)VALUES(13,5,'Release全量','自动Release全量',true,'tag','[]','["api", "web", "perf"]','web_collection',2,'2026-03-22 10:05:00','2026-05-29 20:29:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO trigger_rules(id,project_id,name,description,is_active,trigger_event,target_branches,test_types,target_type,created_by,created_at,updated_at)VALUES(14,6,'Push冒烟','自动Push冒烟',true,'push','["main", "develop"]','["api"]','api_collection',2,'2026-02-10 01:50:00','2026-06-02 00:40:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO trigger_rules(id,project_id,name,description,is_active,trigger_event,target_branches,test_types,target_type,created_by,created_at,updated_at)VALUES(15,6,'PR回归','自动PR回归',true,'pull_request','["main"]','["api", "web"]','api_collection',2,'2026-01-26 19:39:00','2026-06-01 15:32:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO trigger_rules(id,project_id,name,description,is_active,trigger_event,target_branches,test_types,target_type,created_by,created_at,updated_at)VALUES(16,6,'Release全量','自动Release全量',true,'tag','[]','["api", "web", "perf"]','web_collection',2,'2026-03-12 02:48:00','2026-06-01 20:52:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO trigger_rules(id,project_id,name,description,is_active,trigger_event,target_branches,test_types,target_type,created_by,created_at,updated_at)VALUES(17,7,'PR回归','自动PR回归',true,'pull_request','["main"]','["api", "web"]','api_collection',2,'2026-02-17 21:10:00','2026-05-31 13:49:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO trigger_rules(id,project_id,name,description,is_active,trigger_event,target_branches,test_types,target_type,created_by,created_at,updated_at)VALUES(18,7,'Release全量','自动Release全量',true,'tag','[]','["api", "web", "perf"]','web_collection',2,'2026-03-19 08:54:00','2026-05-29 13:39:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO trigger_rules(id,project_id,name,description,is_active,trigger_event,target_branches,test_types,target_type,created_by,created_at,updated_at)VALUES(19,8,'Push冒烟','自动Push冒烟',true,'push','["main", "develop"]','["api"]','api_collection',2,'2026-04-04 09:00:00','2026-05-30 04:06:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO trigger_rules(id,project_id,name,description,is_active,trigger_event,target_branches,test_types,target_type,created_by,created_at,updated_at)VALUES(20,9,'PR回归','自动PR回归',true,'pull_request','["main"]','["api", "web"]','api_collection',2,'2026-02-11 18:16:00','2026-05-30 00:35:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO trigger_rules(id,project_id,name,description,is_active,trigger_event,target_branches,test_types,target_type,created_by,created_at,updated_at)VALUES(21,10,'Push冒烟','自动Push冒烟',true,'push','["main", "develop"]','["api"]','api_collection',1,'2026-02-22 09:54:00','2026-06-02 04:43:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO trigger_rules(id,project_id,name,description,is_active,trigger_event,target_branches,test_types,target_type,created_by,created_at,updated_at)VALUES(22,10,'PR回归','自动PR回归',true,'pull_request','["main"]','["api", "web"]','api_collection',1,'2026-05-08 22:02:00','2026-05-30 16:09:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO trigger_rules(id,project_id,name,description,is_active,trigger_event,target_branches,test_types,target_type,created_by,created_at,updated_at)VALUES(23,10,'Release全量','自动Release全量',true,'tag','[]','["api", "web", "perf"]','web_collection',2,'2026-05-17 09:12:00','2026-06-02 06:30:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO trigger_rules(id,project_id,name,description,is_active,trigger_event,target_branches,test_types,target_type,created_by,created_at,updated_at)VALUES(24,11,'Push冒烟','自动Push冒烟',true,'push','["main", "develop"]','["api"]','api_collection',2,'2026-01-28 11:29:00','2026-06-01 03:05:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO trigger_rules(id,project_id,name,description,is_active,trigger_event,target_branches,test_types,target_type,created_by,created_at,updated_at)VALUES(25,11,'Release全量','自动Release全量',true,'tag','[]','["api", "web", "perf"]','web_collection',2,'2026-02-08 09:01:00','2026-05-30 19:52:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO trigger_rules(id,project_id,name,description,is_active,trigger_event,target_branches,test_types,target_type,created_by,created_at,updated_at)VALUES(26,12,'Push冒烟','自动Push冒烟',true,'push','["main", "develop"]','["api"]','api_collection',2,'2026-03-26 04:20:00','2026-05-30 07:51:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO trigger_rules(id,project_id,name,description,is_active,trigger_event,target_branches,test_types,target_type,created_by,created_at,updated_at)VALUES(27,12,'PR回归','自动PR回归',true,'pull_request','["main"]','["api", "web"]','api_collection',1,'2026-05-19 03:27:00','2026-05-31 02:13:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO trigger_rules(id,project_id,name,description,is_active,trigger_event,target_branches,test_types,target_type,created_by,created_at,updated_at)VALUES(28,12,'Release全量','自动Release全量',true,'tag','[]','["api", "web", "perf"]','web_collection',2,'2026-03-06 02:33:00','2026-05-30 11:23:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO trigger_rules(id,project_id,name,description,is_active,trigger_event,target_branches,test_types,target_type,created_by,created_at,updated_at)VALUES(29,13,'Push冒烟','自动Push冒烟',true,'push','["main", "develop"]','["api"]','api_collection',5,'2026-05-19 19:25:00','2026-05-30 13:50:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO trigger_rules(id,project_id,name,description,is_active,trigger_event,target_branches,test_types,target_type,created_by,created_at,updated_at)VALUES(30,13,'PR回归','自动PR回归',true,'pull_request','["main"]','["api", "web"]','api_collection',2,'2026-01-21 04:41:00','2026-06-01 06:18:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO trigger_rules(id,project_id,name,description,is_active,trigger_event,target_branches,test_types,target_type,created_by,created_at,updated_at)VALUES(31,13,'Release全量','自动Release全量',true,'tag','[]','["api", "web", "perf"]','web_collection',1,'2026-01-23 23:04:00','2026-05-30 22:09:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO trigger_rules(id,project_id,name,description,is_active,trigger_event,target_branches,test_types,target_type,created_by,created_at,updated_at)VALUES(32,14,'Push冒烟','自动Push冒烟',true,'push','["main", "develop"]','["api"]','api_collection',2,'2026-05-20 08:17:00','2026-05-30 01:41:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO trigger_rules(id,project_id,name,description,is_active,trigger_event,target_branches,test_types,target_type,created_by,created_at,updated_at)VALUES(33,14,'PR回归','自动PR回归',true,'pull_request','["main"]','["api", "web"]','api_collection',2,'2026-02-01 23:13:00','2026-06-01 03:06:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO trigger_rules(id,project_id,name,description,is_active,trigger_event,target_branches,test_types,target_type,created_by,created_at,updated_at)VALUES(34,14,'Release全量','自动Release全量',true,'tag','[]','["api", "web", "perf"]','web_collection',1,'2026-04-27 03:51:00','2026-05-30 00:11:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO trigger_rules(id,project_id,name,description,is_active,trigger_event,target_branches,test_types,target_type,created_by,created_at,updated_at)VALUES(35,15,'Push冒烟','自动Push冒烟',true,'push','["main", "develop"]','["api"]','api_collection',5,'2026-01-26 12:21:00','2026-06-01 19:32:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO trigger_rules(id,project_id,name,description,is_active,trigger_event,target_branches,test_types,target_type,created_by,created_at,updated_at)VALUES(36,15,'PR回归','自动PR回归',true,'pull_request','["main"]','["api", "web"]','api_collection',2,'2026-04-10 02:18:00','2026-05-30 13:19:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO trigger_rules(id,project_id,name,description,is_active,trigger_event,target_branches,test_types,target_type,created_by,created_at,updated_at)VALUES(37,15,'Release全量','自动Release全量',true,'tag','[]','["api", "web", "perf"]','web_collection',1,'2026-01-27 04:59:00','2026-05-31 16:26:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO trigger_rules(id,project_id,name,description,is_active,trigger_event,target_branches,test_types,target_type,created_by,created_at,updated_at)VALUES(38,16,'Push冒烟','自动Push冒烟',true,'push','["main", "develop"]','["api"]','api_collection',1,'2026-05-13 18:38:00','2026-06-01 13:26:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO trigger_rules(id,project_id,name,description,is_active,trigger_event,target_branches,test_types,target_type,created_by,created_at,updated_at)VALUES(39,16,'Release全量','自动Release全量',true,'tag','[]','["api", "web", "perf"]','web_collection',5,'2026-02-22 02:08:00','2026-06-02 01:39:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO scheduled_tasks(id,project_id,name,cron_expression,target_type,target_id,is_active,notify_webhook,notify_events,created_at,updated_at)VALUES(1,1,'每日冒烟','0 9 * * *','api_collection',2,true,'https://oapi.dingtalk.com/robot/send?access_token=xxx','all','2026-02-22 14:10:00','2026-05-31 23:14:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO scheduled_tasks(id,project_id,name,cron_expression,target_type,target_id,is_active,notify_webhook,notify_events,created_at,updated_at)VALUES(2,1,'每周回归','0 2 * * 1','api_collection',7,true,'https://oapi.dingtalk.com/robot/send?access_token=xxx','all','2026-03-24 14:03:00','2026-05-31 23:06:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO scheduled_tasks(id,project_id,name,cron_expression,target_type,target_id,is_active,notify_webhook,notify_events,created_at,updated_at)VALUES(3,1,'周末全量','0 1 * * 6','web_collection',1,true,NULL,'all','2025-12-20 10:54:00','2026-06-01 11:05:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO scheduled_tasks(id,project_id,name,cron_expression,target_type,target_id,is_active,notify_webhook,notify_events,created_at,updated_at)VALUES(4,2,'每日冒烟','0 9 * * *','api_collection',11,true,NULL,'all','2026-03-19 17:03:00','2026-06-01 20:38:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO scheduled_tasks(id,project_id,name,cron_expression,target_type,target_id,is_active,notify_webhook,notify_events,created_at,updated_at)VALUES(5,2,'每周回归','0 2 * * 1','api_collection',10,true,'https://open.feishu.cn/open-apis/bot/v2/hook/xxx','all','2026-03-27 12:37:00','2026-05-31 01:33:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO scheduled_tasks(id,project_id,name,cron_expression,target_type,target_id,is_active,notify_webhook,notify_events,created_at,updated_at)VALUES(6,2,'周末全量','0 1 * * 6','web_collection',14,true,NULL,'all','2026-02-28 11:56:00','2026-05-29 14:21:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO scheduled_tasks(id,project_id,name,cron_expression,target_type,target_id,is_active,notify_webhook,notify_events,created_at,updated_at)VALUES(7,3,'每周回归','0 2 * * 1','api_collection',19,true,'https://oapi.dingtalk.com/robot/send?access_token=xxx','all','2026-05-28 13:17:00','2026-05-31 02:19:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO scheduled_tasks(id,project_id,name,cron_expression,target_type,target_id,is_active,notify_webhook,notify_events,created_at,updated_at)VALUES(8,3,'性能巡检','0 3 * * *','perf_scenario',16,true,NULL,'all','2026-02-04 17:28:00','2026-05-30 16:13:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO scheduled_tasks(id,project_id,name,cron_expression,target_type,target_id,is_active,notify_webhook,notify_events,created_at,updated_at)VALUES(9,3,'周末全量','0 1 * * 6','web_collection',19,true,NULL,'all','2026-01-03 20:23:00','2026-05-31 11:22:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO scheduled_tasks(id,project_id,name,cron_expression,target_type,target_id,is_active,notify_webhook,notify_events,created_at,updated_at)VALUES(10,4,'每周回归','0 2 * * 1','api_collection',27,true,'https://open.feishu.cn/open-apis/bot/v2/hook/xxx','all','2026-01-03 11:52:00','2026-05-30 06:43:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO scheduled_tasks(id,project_id,name,cron_expression,target_type,target_id,is_active,notify_webhook,notify_events,created_at,updated_at)VALUES(11,4,'性能巡检','0 3 * * *','perf_scenario',24,true,'https://open.feishu.cn/open-apis/bot/v2/hook/xxx','all','2026-02-25 02:58:00','2026-06-01 10:22:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO scheduled_tasks(id,project_id,name,cron_expression,target_type,target_id,is_active,notify_webhook,notify_events,created_at,updated_at)VALUES(12,4,'周末全量','0 1 * * 6','web_collection',28,true,NULL,'all','2026-03-29 04:43:00','2026-06-01 03:07:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO scheduled_tasks(id,project_id,name,cron_expression,target_type,target_id,is_active,notify_webhook,notify_events,created_at,updated_at)VALUES(13,5,'每日冒烟','0 9 * * *','api_collection',31,true,NULL,'all','2026-02-06 04:27:00','2026-06-01 02:24:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO scheduled_tasks(id,project_id,name,cron_expression,target_type,target_id,is_active,notify_webhook,notify_events,created_at,updated_at)VALUES(14,5,'每周回归','0 2 * * 1','api_collection',31,true,'https://oapi.dingtalk.com/robot/send?access_token=xxx','all','2025-12-17 12:25:00','2026-05-30 09:35:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO scheduled_tasks(id,project_id,name,cron_expression,target_type,target_id,is_active,notify_webhook,notify_events,created_at,updated_at)VALUES(15,5,'性能巡检','0 3 * * *','perf_scenario',31,true,NULL,'all','2026-04-09 04:27:00','2026-06-01 11:24:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO scheduled_tasks(id,project_id,name,cron_expression,target_type,target_id,is_active,notify_webhook,notify_events,created_at,updated_at)VALUES(16,5,'周末全量','0 1 * * 6','web_collection',31,true,'https://oapi.dingtalk.com/robot/send?access_token=xxx','all','2026-04-25 06:58:00','2026-06-02 09:49:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO scheduled_tasks(id,project_id,name,cron_expression,target_type,target_id,is_active,notify_webhook,notify_events,created_at,updated_at)VALUES(17,6,'每周回归','0 2 * * 1','api_collection',36,true,'https://oapi.dingtalk.com/robot/send?access_token=xxx','all','2025-12-05 17:36:00','2026-05-29 20:36:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO scheduled_tasks(id,project_id,name,cron_expression,target_type,target_id,is_active,notify_webhook,notify_events,created_at,updated_at)VALUES(18,6,'周末全量','0 1 * * 6','web_collection',43,true,NULL,'all','2026-02-23 07:00:00','2026-06-02 00:48:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO scheduled_tasks(id,project_id,name,cron_expression,target_type,target_id,is_active,notify_webhook,notify_events,created_at,updated_at)VALUES(19,7,'每日冒烟','0 9 * * *','api_collection',44,true,'https://open.feishu.cn/open-apis/bot/v2/hook/xxx','all','2026-05-16 10:45:00','2026-05-30 23:19:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO scheduled_tasks(id,project_id,name,cron_expression,target_type,target_id,is_active,notify_webhook,notify_events,created_at,updated_at)VALUES(20,7,'性能巡检','0 3 * * *','perf_scenario',48,true,NULL,'all','2026-05-19 18:43:00','2026-05-29 16:19:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO scheduled_tasks(id,project_id,name,cron_expression,target_type,target_id,is_active,notify_webhook,notify_events,created_at,updated_at)VALUES(21,8,'每日冒烟','0 9 * * *','api_collection',53,true,NULL,'all','2026-03-12 12:10:00','2026-06-02 09:00:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO scheduled_tasks(id,project_id,name,cron_expression,target_type,target_id,is_active,notify_webhook,notify_events,created_at,updated_at)VALUES(22,8,'性能巡检','0 3 * * *','perf_scenario',50,true,'https://open.feishu.cn/open-apis/bot/v2/hook/xxx','all','2026-02-18 05:00:00','2026-05-31 01:39:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO scheduled_tasks(id,project_id,name,cron_expression,target_type,target_id,is_active,notify_webhook,notify_events,created_at,updated_at)VALUES(23,8,'周末全量','0 1 * * 6','web_collection',54,true,'https://open.feishu.cn/open-apis/bot/v2/hook/xxx','all','2026-02-09 07:39:00','2026-06-01 11:58:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO scheduled_tasks(id,project_id,name,cron_expression,target_type,target_id,is_active,notify_webhook,notify_events,created_at,updated_at)VALUES(24,9,'每日冒烟','0 9 * * *','api_collection',62,true,'https://open.feishu.cn/open-apis/bot/v2/hook/xxx','all','2026-02-13 01:55:00','2026-06-02 09:03:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO scheduled_tasks(id,project_id,name,cron_expression,target_type,target_id,is_active,notify_webhook,notify_events,created_at,updated_at)VALUES(25,9,'每周回归','0 2 * * 1','api_collection',59,true,'https://open.feishu.cn/open-apis/bot/v2/hook/xxx','all','2026-05-09 11:55:00','2026-06-01 01:00:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO scheduled_tasks(id,project_id,name,cron_expression,target_type,target_id,is_active,notify_webhook,notify_events,created_at,updated_at)VALUES(26,9,'性能巡检','0 3 * * *','perf_scenario',61,true,'https://open.feishu.cn/open-apis/bot/v2/hook/xxx','all','2026-05-06 21:21:00','2026-05-30 14:30:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO scheduled_tasks(id,project_id,name,cron_expression,target_type,target_id,is_active,notify_webhook,notify_events,created_at,updated_at)VALUES(27,10,'每日冒烟','0 9 * * *','api_collection',66,true,NULL,'all','2026-04-12 20:34:00','2026-06-01 00:25:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO scheduled_tasks(id,project_id,name,cron_expression,target_type,target_id,is_active,notify_webhook,notify_events,created_at,updated_at)VALUES(28,10,'性能巡检','0 3 * * *','perf_scenario',68,true,NULL,'all','2025-12-23 21:50:00','2026-05-29 14:31:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO scheduled_tasks(id,project_id,name,cron_expression,target_type,target_id,is_active,notify_webhook,notify_events,created_at,updated_at)VALUES(29,10,'周末全量','0 1 * * 6','web_collection',68,true,'https://oapi.dingtalk.com/robot/send?access_token=xxx','all','2026-01-13 20:25:00','2026-06-01 18:27:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO scheduled_tasks(id,project_id,name,cron_expression,target_type,target_id,is_active,notify_webhook,notify_events,created_at,updated_at)VALUES(30,11,'每日冒烟','0 9 * * *','api_collection',76,true,NULL,'all','2026-01-27 14:56:00','2026-05-31 09:37:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO scheduled_tasks(id,project_id,name,cron_expression,target_type,target_id,is_active,notify_webhook,notify_events,created_at,updated_at)VALUES(31,11,'每周回归','0 2 * * 1','api_collection',74,true,'https://oapi.dingtalk.com/robot/send?access_token=xxx','all','2026-02-28 19:06:00','2026-06-01 15:31:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO scheduled_tasks(id,project_id,name,cron_expression,target_type,target_id,is_active,notify_webhook,notify_events,created_at,updated_at)VALUES(32,11,'性能巡检','0 3 * * *','perf_scenario',71,true,NULL,'all','2025-12-31 02:52:00','2026-06-02 07:52:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO scheduled_tasks(id,project_id,name,cron_expression,target_type,target_id,is_active,notify_webhook,notify_events,created_at,updated_at)VALUES(33,11,'周末全量','0 1 * * 6','web_collection',76,true,'https://open.feishu.cn/open-apis/bot/v2/hook/xxx','all','2026-02-04 13:27:00','2026-05-31 22:00:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO scheduled_tasks(id,project_id,name,cron_expression,target_type,target_id,is_active,notify_webhook,notify_events,created_at,updated_at)VALUES(34,12,'每日冒烟','0 9 * * *','api_collection',79,true,NULL,'all','2026-05-30 15:37:00','2026-06-01 07:10:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO scheduled_tasks(id,project_id,name,cron_expression,target_type,target_id,is_active,notify_webhook,notify_events,created_at,updated_at)VALUES(35,12,'每周回归','0 2 * * 1','api_collection',83,true,NULL,'all','2026-03-13 06:31:00','2026-05-29 19:42:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO scheduled_tasks(id,project_id,name,cron_expression,target_type,target_id,is_active,notify_webhook,notify_events,created_at,updated_at)VALUES(36,12,'性能巡检','0 3 * * *','perf_scenario',80,true,'https://open.feishu.cn/open-apis/bot/v2/hook/xxx','all','2026-03-17 21:22:00','2026-06-01 07:54:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO scheduled_tasks(id,project_id,name,cron_expression,target_type,target_id,is_active,notify_webhook,notify_events,created_at,updated_at)VALUES(37,12,'周末全量','0 1 * * 6','web_collection',80,true,'https://open.feishu.cn/open-apis/bot/v2/hook/xxx','all','2026-05-08 14:15:00','2026-05-30 05:33:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO scheduled_tasks(id,project_id,name,cron_expression,target_type,target_id,is_active,notify_webhook,notify_events,created_at,updated_at)VALUES(38,13,'性能巡检','0 3 * * *','perf_scenario',89,true,'https://open.feishu.cn/open-apis/bot/v2/hook/xxx','all','2026-01-20 15:56:00','2026-05-30 08:09:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO scheduled_tasks(id,project_id,name,cron_expression,target_type,target_id,is_active,notify_webhook,notify_events,created_at,updated_at)VALUES(39,13,'周末全量','0 1 * * 6','web_collection',88,true,NULL,'all','2026-02-28 01:02:00','2026-06-01 06:08:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO scheduled_tasks(id,project_id,name,cron_expression,target_type,target_id,is_active,notify_webhook,notify_events,created_at,updated_at)VALUES(40,14,'每日冒烟','0 9 * * *','api_collection',97,true,'https://open.feishu.cn/open-apis/bot/v2/hook/xxx','all','2026-02-25 18:07:00','2026-06-01 23:33:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO scheduled_tasks(id,project_id,name,cron_expression,target_type,target_id,is_active,notify_webhook,notify_events,created_at,updated_at)VALUES(41,14,'每周回归','0 2 * * 1','api_collection',93,true,'https://oapi.dingtalk.com/robot/send?access_token=xxx','all','2026-01-05 05:52:00','2026-05-30 18:07:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO scheduled_tasks(id,project_id,name,cron_expression,target_type,target_id,is_active,notify_webhook,notify_events,created_at,updated_at)VALUES(42,14,'周末全量','0 1 * * 6','web_collection',97,true,'https://oapi.dingtalk.com/robot/send?access_token=xxx','all','2026-05-15 13:35:00','2026-05-31 11:03:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO scheduled_tasks(id,project_id,name,cron_expression,target_type,target_id,is_active,notify_webhook,notify_events,created_at,updated_at)VALUES(43,15,'每日冒烟','0 9 * * *','api_collection',101,true,'https://oapi.dingtalk.com/robot/send?access_token=xxx','all','2026-02-04 04:47:00','2026-06-01 01:06:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO scheduled_tasks(id,project_id,name,cron_expression,target_type,target_id,is_active,notify_webhook,notify_events,created_at,updated_at)VALUES(44,15,'每周回归','0 2 * * 1','api_collection',100,true,NULL,'all','2026-04-20 16:21:00','2026-05-30 10:04:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO scheduled_tasks(id,project_id,name,cron_expression,target_type,target_id,is_active,notify_webhook,notify_events,created_at,updated_at)VALUES(45,15,'性能巡检','0 3 * * *','perf_scenario',99,true,'https://oapi.dingtalk.com/robot/send?access_token=xxx','all','2026-05-09 18:27:00','2026-06-01 04:16:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO scheduled_tasks(id,project_id,name,cron_expression,target_type,target_id,is_active,notify_webhook,notify_events,created_at,updated_at)VALUES(46,16,'每日冒烟','0 9 * * *','api_collection',106,true,'https://oapi.dingtalk.com/robot/send?access_token=xxx','all','2026-02-14 07:36:00','2026-05-31 09:30:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO scheduled_tasks(id,project_id,name,cron_expression,target_type,target_id,is_active,notify_webhook,notify_events,created_at,updated_at)VALUES(47,16,'性能巡检','0 3 * * *','perf_scenario',105,true,'https://oapi.dingtalk.com/robot/send?access_token=xxx','all','2026-05-02 15:37:00','2026-06-01 14:49:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO scheduled_tasks(id,project_id,name,cron_expression,target_type,target_id,is_active,notify_webhook,notify_events,created_at,updated_at)VALUES(48,16,'周末全量','0 1 * * 6','web_collection',106,true,NULL,'all','2026-05-09 23:49:00','2026-05-30 07:13:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO api_tokens(id,user_id,name,token_hash,permissions,expires_at,is_active,last_used_at,created_at)VALUES(1,1,'CI/CD Token','c53106c54daeb547434fc9802716f855fc50bcf9f3f2ed2f183969598efb33ce','["read", "write"]','2027-06-01 00:00:00',true,'2026-05-31 19:57:00','2026-01-07 05:48:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO api_tokens(id,user_id,name,token_hash,permissions,expires_at,is_active,last_used_at,created_at)VALUES(2,1,'调试Token','c08af5523d4342a17bee3a41f176e48d94159d6d93a98d144f0f9a490029ef31','["read", "write"]','2027-06-01 00:00:00',true,'2026-05-30 13:00:00','2026-05-30 18:44:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO api_tokens(id,user_id,name,token_hash,permissions,expires_at,is_active,last_used_at,created_at)VALUES(3,2,'CI/CD Token','6d609f41dd0bfff5abb8732879f257b8bb542b8a7677ad1c4d5c552b62d7e525','["read", "write"]','2027-06-01 00:00:00',true,'2026-05-30 16:15:00','2026-03-09 11:42:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO api_tokens(id,user_id,name,token_hash,permissions,expires_at,is_active,last_used_at,created_at)VALUES(4,2,'调试Token','6f04409dcfc20c547be1365d86d744a3d7847017e3b2946eb00d1e034b6a67b8','["read", "write"]','2027-06-01 00:00:00',true,'2026-05-29 20:23:00','2026-01-09 15:47:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO api_tokens(id,user_id,name,token_hash,permissions,expires_at,is_active,last_used_at,created_at)VALUES(5,5,'CI/CD Token','4f1a9f27bdc792411837875dab0ab1b1c12f13ee307fa4e786f9763f9b041274','["read", "write"]','2027-06-01 00:00:00',true,'2026-05-31 05:22:00','2026-03-28 01:30:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO api_tokens(id,user_id,name,token_hash,permissions,expires_at,is_active,last_used_at,created_at)VALUES(6,5,'监控Token','51efe6456461c3a4f089e821564b4dbddc68fd81e090df4792d857bc40ce42b3','["read"]','2027-06-01 00:00:00',true,'2026-06-01 14:10:00','2026-01-21 05:30:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO api_tokens(id,user_id,name,token_hash,permissions,expires_at,is_active,last_used_at,created_at)VALUES(7,6,'监控Token','56c1f193ccb74389de6273ff873aaa421fe7ef589cc7d854553475e022bd5e26','["read"]','2027-06-01 00:00:00',true,'2026-06-02 08:44:00','2026-03-08 08:51:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO api_tokens(id,user_id,name,token_hash,permissions,expires_at,is_active,last_used_at,created_at)VALUES(8,7,'CI/CD Token','65bdb971ad64617ddd1da637d4b5b3814599b3e74877eff342a10fba7e40f564','["read", "write"]','2027-06-01 00:00:00',true,'2026-05-31 12:49:00','2026-05-14 19:03:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO api_tokens(id,user_id,name,token_hash,permissions,expires_at,is_active,last_used_at,created_at)VALUES(9,7,'调试Token','7c1d43c0119e7310ff445ef11899847ea3901950051be5670679ae05da919da0','["read", "write"]','2027-06-01 00:00:00',true,'2026-05-30 01:27:00','2026-03-31 23:05:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO prompt_versions(id,feature,name,version,is_active,system_prompt,temperature,model_name,total_invocations,success_count,failure_count,avg_latency_ms,avg_tokens,avg_cost,traffic_weight,created_by,created_at,updated_at)VALUES(1,'copilot','AI助手v1',1,false,'你是专业测试助手',0.3,'gpt-4o',911,841,70,1729.0,1728.0,0.0029,0.13,1,'2026-04-12 15:25:00','2026-05-31 11:44:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO prompt_versions(id,feature,name,version,is_active,system_prompt,temperature,model_name,total_invocations,success_count,failure_count,avg_latency_ms,avg_tokens,avg_cost,traffic_weight,created_by,created_at,updated_at)VALUES(2,'script_gen','脚本生成v1',1,false,'生成Playwright脚本',0.2,'gpt-4o',1956,1811,145,1866.0,695.0,0.0402,0.11,1,'2025-11-08 13:06:00','2026-05-30 21:02:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO prompt_versions(id,feature,name,version,is_active,system_prompt,temperature,model_name,total_invocations,success_count,failure_count,avg_latency_ms,avg_tokens,avg_cost,traffic_weight,created_by,created_at,updated_at)VALUES(3,'script_gen','脚本生成v2',2,true,'生成Playwright脚本',0.3,'gpt-4o',332,307,25,739.0,2486.0,0.0464,1.0,1,'2025-12-03 08:35:00','2026-05-30 19:21:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO prompt_versions(id,feature,name,version,is_active,system_prompt,temperature,model_name,total_invocations,success_count,failure_count,avg_latency_ms,avg_tokens,avg_cost,traffic_weight,created_by,created_at,updated_at)VALUES(4,'swagger_gen','用例生成v1',1,false,'根据OpenAPI生成',0.7,'gpt-4o',771,663,108,1218.0,1781.0,0.0367,0.0,1,'2026-05-23 16:01:00','2026-05-30 23:54:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO prompt_versions(id,feature,name,version,is_active,system_prompt,temperature,model_name,total_invocations,success_count,failure_count,avg_latency_ms,avg_tokens,avg_cost,traffic_weight,created_by,created_at,updated_at)VALUES(5,'swagger_gen','用例生成v2',2,true,'根据OpenAPI生成',0.5,'gpt-4o',137,125,12,3788.0,2065.0,0.0304,1.0,1,'2025-10-17 02:54:00','2026-06-02 06:31:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO prompt_versions(id,feature,name,version,is_active,system_prompt,temperature,model_name,total_invocations,success_count,failure_count,avg_latency_ms,avg_tokens,avg_cost,traffic_weight,created_by,created_at,updated_at)VALUES(6,'dedup','用例去重v1',1,false,'语义相似度分析',0.5,'gpt-4o',1977,1787,190,3590.0,599.0,0.0405,0.21,1,'2026-02-07 12:36:00','2026-06-01 12:16:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO prompt_versions(id,feature,name,version,is_active,system_prompt,temperature,model_name,total_invocations,success_count,failure_count,avg_latency_ms,avg_tokens,avg_cost,traffic_weight,created_by,created_at,updated_at)VALUES(7,'dedup','用例去重v2',2,true,'语义相似度分析',0.1,'gpt-4o',412,359,53,3727.0,1239.0,0.0125,1.0,1,'2025-11-04 01:16:00','2026-06-01 12:49:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO prompt_versions(id,feature,name,version,is_active,system_prompt,temperature,model_name,total_invocations,success_count,failure_count,avg_latency_ms,avg_tokens,avg_cost,traffic_weight,created_by,created_at,updated_at)VALUES(8,'dedup','用例去重v3',3,false,'语义相似度分析',0.5,'gpt-4o',51,49,2,1320.0,2723.0,0.0395,0.27,1,'2026-03-02 09:00:00','2026-05-31 20:12:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO prompt_versions(id,feature,name,version,is_active,system_prompt,temperature,model_name,total_invocations,success_count,failure_count,avg_latency_ms,avg_tokens,avg_cost,traffic_weight,created_by,created_at,updated_at)VALUES(9,'review','代码审查v1',1,false,'审查代码质量',0.3,'gpt-4o',1932,1655,277,2018.0,2616.0,0.0466,0.27,1,'2026-03-04 13:17:00','2026-05-27 15:44:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO prompt_versions(id,feature,name,version,is_active,system_prompt,temperature,model_name,total_invocations,success_count,failure_count,avg_latency_ms,avg_tokens,avg_cost,traffic_weight,created_by,created_at,updated_at)VALUES(10,'review','代码审查v2',2,true,'审查代码质量',0.5,'gpt-4o',951,892,59,644.0,991.0,0.0478,1.0,1,'2026-01-26 06:12:00','2026-05-29 11:48:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO prompt_versions(id,feature,name,version,is_active,system_prompt,temperature,model_name,total_invocations,success_count,failure_count,avg_latency_ms,avg_tokens,avg_cost,traffic_weight,created_by,created_at,updated_at)VALUES(11,'review','代码审查v3',3,false,'审查代码质量',0.5,'gpt-4o',1779,1544,235,723.0,1191.0,0.0374,0.2,1,'2025-12-19 09:02:00','2026-05-31 12:12:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO ai_invocation_logs(user_id,feature,model_name,prompt,response,success,error_message,error_type,latency_ms,prompt_tokens,completion_tokens,total_tokens,cost_estimate,created_at)VALUES(2,'copilot','gpt-4o','生成copilot测试用例','好的已生成',true,NULL,NULL,2558,2875,1323,4198,0.1259,'2026-04-07 00:11:00');

INSERT INTO ai_invocation_logs(user_id,feature,model_name,prompt,response,success,error_message,error_type,latency_ms,prompt_tokens,completion_tokens,total_tokens,cost_estimate,created_at)VALUES(1,'script_gen','gpt-4o','生成script_gen测试用例','NULL',false,'timeout','timeout',3052,616,1970,2586,0.0776,'2026-05-24 03:33:00');

INSERT INTO ai_invocation_logs(user_id,feature,model_name,prompt,response,success,error_message,error_type,latency_ms,prompt_tokens,completion_tokens,total_tokens,cost_estimate,created_at)VALUES(1,'review','claude-3-opus','生成review测试用例','NULL',false,'timeout','timeout',4646,1328,1333,2661,0.0798,'2025-12-26 06:46:00');

INSERT INTO ai_invocation_logs(user_id,feature,model_name,prompt,response,success,error_message,error_type,latency_ms,prompt_tokens,completion_tokens,total_tokens,cost_estimate,created_at)VALUES(8,'review','gpt-4o-mini','生成review测试用例','好的已生成',true,NULL,NULL,3142,1517,1606,3123,0.0937,'2026-03-30 22:17:00');

INSERT INTO ai_invocation_logs(user_id,feature,model_name,prompt,response,success,error_message,error_type,latency_ms,prompt_tokens,completion_tokens,total_tokens,cost_estimate,created_at)VALUES(8,'script_gen','gpt-4o','生成script_gen测试用例','好的已生成',true,NULL,NULL,778,236,171,407,0.0122,'2026-02-16 18:24:00');

INSERT INTO ai_invocation_logs(user_id,feature,model_name,prompt,response,success,error_message,error_type,latency_ms,prompt_tokens,completion_tokens,total_tokens,cost_estimate,created_at)VALUES(1,'copilot','claude-3-sonnet','生成copilot测试用例','好的已生成',true,NULL,NULL,7924,3843,1911,5754,0.1726,'2026-01-12 08:56:00');

INSERT INTO ai_invocation_logs(user_id,feature,model_name,prompt,response,success,error_message,error_type,latency_ms,prompt_tokens,completion_tokens,total_tokens,cost_estimate,created_at)VALUES(9,'dedup','claude-3-sonnet','生成dedup测试用例','好的已生成',true,NULL,NULL,6575,2948,1883,4831,0.1449,'2026-03-31 18:28:00');

INSERT INTO ai_invocation_logs(user_id,feature,model_name,prompt,response,success,error_message,error_type,latency_ms,prompt_tokens,completion_tokens,total_tokens,cost_estimate,created_at)VALUES(7,'script_gen','gpt-4o-mini','生成script_gen测试用例','好的已生成',true,NULL,NULL,4871,3574,641,4215,0.1265,'2026-03-14 15:16:00');

INSERT INTO ai_invocation_logs(user_id,feature,model_name,prompt,response,success,error_message,error_type,latency_ms,prompt_tokens,completion_tokens,total_tokens,cost_estimate,created_at)VALUES(8,'script_gen','gpt-4o','生成script_gen测试用例','NULL',false,'timeout','timeout',4220,1977,822,2799,0.084,'2026-04-21 23:40:00');

INSERT INTO ai_invocation_logs(user_id,feature,model_name,prompt,response,success,error_message,error_type,latency_ms,prompt_tokens,completion_tokens,total_tokens,cost_estimate,created_at)VALUES(1,'script_gen','gpt-4o-mini','生成script_gen测试用例','好的已生成',true,NULL,NULL,6986,145,199,344,0.0103,'2026-01-26 03:36:00');

INSERT INTO ai_invocation_logs(user_id,feature,model_name,prompt,response,success,error_message,error_type,latency_ms,prompt_tokens,completion_tokens,total_tokens,cost_estimate,created_at)VALUES(8,'swagger_gen','gpt-4o-mini','生成swagger_gen测试用例','好的已生成',true,NULL,NULL,1704,1270,266,1536,0.0461,'2026-02-03 16:44:00');

INSERT INTO ai_invocation_logs(user_id,feature,model_name,prompt,response,success,error_message,error_type,latency_ms,prompt_tokens,completion_tokens,total_tokens,cost_estimate,created_at)VALUES(5,'review','gpt-4o','生成review测试用例','好的已生成',true,NULL,NULL,5618,3979,1222,5201,0.156,'2025-12-04 05:46:00');

INSERT INTO ai_invocation_logs(user_id,feature,model_name,prompt,response,success,error_message,error_type,latency_ms,prompt_tokens,completion_tokens,total_tokens,cost_estimate,created_at)VALUES(6,'swagger_gen','claude-3-opus','生成swagger_gen测试用例','好的已生成',true,NULL,NULL,771,162,1559,1721,0.0516,'2026-05-23 15:58:00');

INSERT INTO ai_invocation_logs(user_id,feature,model_name,prompt,response,success,error_message,error_type,latency_ms,prompt_tokens,completion_tokens,total_tokens,cost_estimate,created_at)VALUES(9,'copilot','claude-3-opus','生成copilot测试用例','好的已生成',true,NULL,NULL,5419,3230,1157,4387,0.1316,'2026-01-09 20:28:00');

INSERT INTO ai_invocation_logs(user_id,feature,model_name,prompt,response,success,error_message,error_type,latency_ms,prompt_tokens,completion_tokens,total_tokens,cost_estimate,created_at)VALUES(7,'script_gen','gpt-4o','生成script_gen测试用例','好的已生成',true,NULL,NULL,7596,577,231,808,0.0242,'2026-02-22 21:32:00');

INSERT INTO ai_invocation_logs(user_id,feature,model_name,prompt,response,success,error_message,error_type,latency_ms,prompt_tokens,completion_tokens,total_tokens,cost_estimate,created_at)VALUES(6,'script_gen','gpt-4o','生成script_gen测试用例','好的已生成',true,NULL,NULL,5756,1470,1941,3411,0.1023,'2026-02-04 23:12:00');

INSERT INTO ai_invocation_logs(user_id,feature,model_name,prompt,response,success,error_message,error_type,latency_ms,prompt_tokens,completion_tokens,total_tokens,cost_estimate,created_at)VALUES(10,'swagger_gen','gpt-4o-mini','生成swagger_gen测试用例','好的已生成',true,NULL,NULL,5061,3118,1265,4383,0.1315,'2026-02-13 00:50:00');

INSERT INTO ai_invocation_logs(user_id,feature,model_name,prompt,response,success,error_message,error_type,latency_ms,prompt_tokens,completion_tokens,total_tokens,cost_estimate,created_at)VALUES(9,'copilot','gpt-4o-mini','生成copilot测试用例','好的已生成',true,NULL,NULL,2168,1816,1424,3240,0.0972,'2026-04-17 09:04:00');

INSERT INTO ai_invocation_logs(user_id,feature,model_name,prompt,response,success,error_message,error_type,latency_ms,prompt_tokens,completion_tokens,total_tokens,cost_estimate,created_at)VALUES(5,'dedup','claude-3-opus','生成dedup测试用例','好的已生成',true,NULL,NULL,1728,418,573,991,0.0297,'2026-02-02 19:04:00');

INSERT INTO ai_invocation_logs(user_id,feature,model_name,prompt,response,success,error_message,error_type,latency_ms,prompt_tokens,completion_tokens,total_tokens,cost_estimate,created_at)VALUES(1,'review','gpt-4o-mini','生成review测试用例','NULL',false,'timeout','timeout',3844,569,236,805,0.0242,'2026-03-05 04:46:00');

INSERT INTO ai_invocation_logs(user_id,feature,model_name,prompt,response,success,error_message,error_type,latency_ms,prompt_tokens,completion_tokens,total_tokens,cost_estimate,created_at)VALUES(1,'script_gen','gpt-4o-mini','生成script_gen测试用例','好的已生成',true,NULL,NULL,1578,505,1375,1880,0.0564,'2025-12-27 10:18:00');

INSERT INTO ai_invocation_logs(user_id,feature,model_name,prompt,response,success,error_message,error_type,latency_ms,prompt_tokens,completion_tokens,total_tokens,cost_estimate,created_at)VALUES(5,'copilot','claude-3-opus','生成copilot测试用例','好的已生成',true,NULL,NULL,4496,3318,304,3622,0.1087,'2026-01-18 15:02:00');

INSERT INTO ai_invocation_logs(user_id,feature,model_name,prompt,response,success,error_message,error_type,latency_ms,prompt_tokens,completion_tokens,total_tokens,cost_estimate,created_at)VALUES(10,'copilot','claude-3-opus','生成copilot测试用例','好的已生成',true,NULL,NULL,3753,535,1632,2167,0.065,'2026-05-03 17:33:00');

INSERT INTO ai_invocation_logs(user_id,feature,model_name,prompt,response,success,error_message,error_type,latency_ms,prompt_tokens,completion_tokens,total_tokens,cost_estimate,created_at)VALUES(6,'review','claude-3-opus','生成review测试用例','好的已生成',true,NULL,NULL,4710,434,1545,1979,0.0594,'2026-01-01 23:24:00');

INSERT INTO ai_invocation_logs(user_id,feature,model_name,prompt,response,success,error_message,error_type,latency_ms,prompt_tokens,completion_tokens,total_tokens,cost_estimate,created_at)VALUES(10,'dedup','gpt-4o-mini','生成dedup测试用例','好的已生成',true,NULL,NULL,971,1663,1188,2851,0.0855,'2026-01-20 08:15:00');

INSERT INTO ai_invocation_logs(user_id,feature,model_name,prompt,response,success,error_message,error_type,latency_ms,prompt_tokens,completion_tokens,total_tokens,cost_estimate,created_at)VALUES(1,'swagger_gen','gpt-4o-mini','生成swagger_gen测试用例','好的已生成',true,NULL,NULL,6471,3410,1482,4892,0.1468,'2025-12-29 03:56:00');

INSERT INTO ai_invocation_logs(user_id,feature,model_name,prompt,response,success,error_message,error_type,latency_ms,prompt_tokens,completion_tokens,total_tokens,cost_estimate,created_at)VALUES(9,'review','gpt-4o-mini','生成review测试用例','好的已生成',true,NULL,NULL,4966,2064,1891,3955,0.1187,'2026-04-17 17:43:00');

INSERT INTO ai_invocation_logs(user_id,feature,model_name,prompt,response,success,error_message,error_type,latency_ms,prompt_tokens,completion_tokens,total_tokens,cost_estimate,created_at)VALUES(8,'swagger_gen','gpt-4o','生成swagger_gen测试用例','好的已生成',true,NULL,NULL,4409,665,394,1059,0.0318,'2026-01-30 05:00:00');

INSERT INTO ai_invocation_logs(user_id,feature,model_name,prompt,response,success,error_message,error_type,latency_ms,prompt_tokens,completion_tokens,total_tokens,cost_estimate,created_at)VALUES(1,'script_gen','gpt-4o-mini','生成script_gen测试用例','好的已生成',true,NULL,NULL,4596,622,1330,1952,0.0586,'2026-04-04 05:18:00');

INSERT INTO ai_invocation_logs(user_id,feature,model_name,prompt,response,success,error_message,error_type,latency_ms,prompt_tokens,completion_tokens,total_tokens,cost_estimate,created_at)VALUES(5,'copilot','claude-3-opus','生成copilot测试用例','好的已生成',true,NULL,NULL,2483,2095,620,2715,0.0815,'2025-12-16 03:14:00');

INSERT INTO ai_invocation_logs(user_id,feature,model_name,prompt,response,success,error_message,error_type,latency_ms,prompt_tokens,completion_tokens,total_tokens,cost_estimate,created_at)VALUES(5,'review','gpt-4o','生成review测试用例','NULL',false,'timeout','timeout',3148,2464,1283,3747,0.1124,'2026-04-11 12:00:00');

INSERT INTO ai_invocation_logs(user_id,feature,model_name,prompt,response,success,error_message,error_type,latency_ms,prompt_tokens,completion_tokens,total_tokens,cost_estimate,created_at)VALUES(5,'copilot','gpt-4o-mini','生成copilot测试用例','NULL',false,'timeout','timeout',1902,307,617,924,0.0277,'2025-12-05 05:46:00');

INSERT INTO ai_invocation_logs(user_id,feature,model_name,prompt,response,success,error_message,error_type,latency_ms,prompt_tokens,completion_tokens,total_tokens,cost_estimate,created_at)VALUES(5,'script_gen','claude-3-sonnet','生成script_gen测试用例','好的已生成',true,NULL,NULL,7167,3910,310,4220,0.1266,'2025-12-05 06:45:00');

INSERT INTO ai_invocation_logs(user_id,feature,model_name,prompt,response,success,error_message,error_type,latency_ms,prompt_tokens,completion_tokens,total_tokens,cost_estimate,created_at)VALUES(8,'script_gen','gpt-4o','生成script_gen测试用例','好的已生成',true,NULL,NULL,6420,635,1080,1715,0.0515,'2026-05-08 20:39:00');

INSERT INTO ai_invocation_logs(user_id,feature,model_name,prompt,response,success,error_message,error_type,latency_ms,prompt_tokens,completion_tokens,total_tokens,cost_estimate,created_at)VALUES(1,'dedup','claude-3-opus','生成dedup测试用例','好的已生成',true,NULL,NULL,223,2894,1739,4633,0.139,'2026-05-17 22:15:00');

INSERT INTO ai_invocation_logs(user_id,feature,model_name,prompt,response,success,error_message,error_type,latency_ms,prompt_tokens,completion_tokens,total_tokens,cost_estimate,created_at)VALUES(6,'dedup','claude-3-sonnet','生成dedup测试用例','好的已生成',true,NULL,NULL,3459,3799,1247,5046,0.1514,'2026-05-07 14:26:00');

INSERT INTO ai_invocation_logs(user_id,feature,model_name,prompt,response,success,error_message,error_type,latency_ms,prompt_tokens,completion_tokens,total_tokens,cost_estimate,created_at)VALUES(6,'script_gen','gpt-4o','生成script_gen测试用例','好的已生成',true,NULL,NULL,5539,763,1275,2038,0.0611,'2026-05-09 20:17:00');

INSERT INTO ai_invocation_logs(user_id,feature,model_name,prompt,response,success,error_message,error_type,latency_ms,prompt_tokens,completion_tokens,total_tokens,cost_estimate,created_at)VALUES(2,'dedup','claude-3-opus','生成dedup测试用例','好的已生成',true,NULL,NULL,5181,267,1812,2079,0.0624,'2026-04-21 15:13:00');

INSERT INTO ai_invocation_logs(user_id,feature,model_name,prompt,response,success,error_message,error_type,latency_ms,prompt_tokens,completion_tokens,total_tokens,cost_estimate,created_at)VALUES(6,'copilot','gpt-4o','生成copilot测试用例','好的已生成',true,NULL,NULL,7098,3138,1158,4296,0.1289,'2026-03-23 07:21:00');

INSERT INTO ai_invocation_logs(user_id,feature,model_name,prompt,response,success,error_message,error_type,latency_ms,prompt_tokens,completion_tokens,total_tokens,cost_estimate,created_at)VALUES(9,'dedup','gpt-4o-mini','生成dedup测试用例','好的已生成',true,NULL,NULL,864,3382,1828,5210,0.1563,'2026-04-11 06:34:00');

INSERT INTO ai_invocation_logs(user_id,feature,model_name,prompt,response,success,error_message,error_type,latency_ms,prompt_tokens,completion_tokens,total_tokens,cost_estimate,created_at)VALUES(10,'copilot','gpt-4o','生成copilot测试用例','好的已生成',true,NULL,NULL,4764,3724,804,4528,0.1358,'2026-02-14 21:31:00');

INSERT INTO ai_invocation_logs(user_id,feature,model_name,prompt,response,success,error_message,error_type,latency_ms,prompt_tokens,completion_tokens,total_tokens,cost_estimate,created_at)VALUES(1,'dedup','gpt-4o-mini','生成dedup测试用例','好的已生成',true,NULL,NULL,7817,726,222,948,0.0284,'2026-01-05 17:09:00');

INSERT INTO ai_invocation_logs(user_id,feature,model_name,prompt,response,success,error_message,error_type,latency_ms,prompt_tokens,completion_tokens,total_tokens,cost_estimate,created_at)VALUES(9,'swagger_gen','claude-3-opus','生成swagger_gen测试用例','NULL',false,'timeout','timeout',4961,1275,1644,2919,0.0876,'2026-03-28 00:19:00');

INSERT INTO ai_invocation_logs(user_id,feature,model_name,prompt,response,success,error_message,error_type,latency_ms,prompt_tokens,completion_tokens,total_tokens,cost_estimate,created_at)VALUES(1,'dedup','claude-3-sonnet','生成dedup测试用例','好的已生成',true,NULL,NULL,1808,2905,677,3582,0.1075,'2025-12-29 03:15:00');

INSERT INTO ai_invocation_logs(user_id,feature,model_name,prompt,response,success,error_message,error_type,latency_ms,prompt_tokens,completion_tokens,total_tokens,cost_estimate,created_at)VALUES(6,'review','claude-3-sonnet','生成review测试用例','好的已生成',true,NULL,NULL,2676,2751,1288,4039,0.1212,'2026-02-25 04:31:00');

INSERT INTO ai_invocation_logs(user_id,feature,model_name,prompt,response,success,error_message,error_type,latency_ms,prompt_tokens,completion_tokens,total_tokens,cost_estimate,created_at)VALUES(6,'script_gen','gpt-4o-mini','生成script_gen测试用例','好的已生成',true,NULL,NULL,3754,3712,1758,5470,0.1641,'2026-05-02 07:42:00');

INSERT INTO ai_invocation_logs(user_id,feature,model_name,prompt,response,success,error_message,error_type,latency_ms,prompt_tokens,completion_tokens,total_tokens,cost_estimate,created_at)VALUES(5,'swagger_gen','gpt-4o-mini','生成swagger_gen测试用例','好的已生成',true,NULL,NULL,5651,662,1933,2595,0.0779,'2026-03-05 13:25:00');

INSERT INTO ai_invocation_logs(user_id,feature,model_name,prompt,response,success,error_message,error_type,latency_ms,prompt_tokens,completion_tokens,total_tokens,cost_estimate,created_at)VALUES(8,'swagger_gen','gpt-4o-mini','生成swagger_gen测试用例','好的已生成',true,NULL,NULL,4416,3582,1101,4683,0.1405,'2025-12-21 08:26:00');

INSERT INTO ai_invocation_logs(user_id,feature,model_name,prompt,response,success,error_message,error_type,latency_ms,prompt_tokens,completion_tokens,total_tokens,cost_estimate,created_at)VALUES(10,'review','gpt-4o','生成review测试用例','好的已生成',true,NULL,NULL,7821,1769,352,2121,0.0636,'2025-12-20 02:14:00');

INSERT INTO ai_invocation_logs(user_id,feature,model_name,prompt,response,success,error_message,error_type,latency_ms,prompt_tokens,completion_tokens,total_tokens,cost_estimate,created_at)VALUES(7,'copilot','claude-3-sonnet','生成copilot测试用例','好的已生成',true,NULL,NULL,1846,2392,743,3135,0.0941,'2026-04-01 05:14:00');

INSERT INTO ai_invocation_logs(user_id,feature,model_name,prompt,response,success,error_message,error_type,latency_ms,prompt_tokens,completion_tokens,total_tokens,cost_estimate,created_at)VALUES(7,'dedup','gpt-4o-mini','生成dedup测试用例','好的已生成',true,NULL,NULL,5661,335,796,1131,0.0339,'2026-01-16 02:46:00');

INSERT INTO ai_invocation_logs(user_id,feature,model_name,prompt,response,success,error_message,error_type,latency_ms,prompt_tokens,completion_tokens,total_tokens,cost_estimate,created_at)VALUES(6,'swagger_gen','gpt-4o-mini','生成swagger_gen测试用例','好的已生成',true,NULL,NULL,484,3413,1462,4875,0.1462,'2026-04-01 07:55:00');

INSERT INTO ai_invocation_logs(user_id,feature,model_name,prompt,response,success,error_message,error_type,latency_ms,prompt_tokens,completion_tokens,total_tokens,cost_estimate,created_at)VALUES(8,'review','claude-3-sonnet','生成review测试用例','好的已生成',true,NULL,NULL,3262,3044,596,3640,0.1092,'2026-02-26 19:11:00');

INSERT INTO ai_invocation_logs(user_id,feature,model_name,prompt,response,success,error_message,error_type,latency_ms,prompt_tokens,completion_tokens,total_tokens,cost_estimate,created_at)VALUES(9,'review','claude-3-opus','生成review测试用例','好的已生成',true,NULL,NULL,6721,1957,872,2829,0.0849,'2026-01-01 11:03:00');

INSERT INTO ai_invocation_logs(user_id,feature,model_name,prompt,response,success,error_message,error_type,latency_ms,prompt_tokens,completion_tokens,total_tokens,cost_estimate,created_at)VALUES(7,'swagger_gen','gpt-4o-mini','生成swagger_gen测试用例','好的已生成',true,NULL,NULL,2165,1888,809,2697,0.0809,'2026-01-07 18:06:00');

INSERT INTO ai_invocation_logs(user_id,feature,model_name,prompt,response,success,error_message,error_type,latency_ms,prompt_tokens,completion_tokens,total_tokens,cost_estimate,created_at)VALUES(7,'dedup','claude-3-sonnet','生成dedup测试用例','好的已生成',true,NULL,NULL,5071,3282,1079,4361,0.1308,'2026-02-24 07:33:00');

INSERT INTO ai_invocation_logs(user_id,feature,model_name,prompt,response,success,error_message,error_type,latency_ms,prompt_tokens,completion_tokens,total_tokens,cost_estimate,created_at)VALUES(6,'swagger_gen','gpt-4o-mini','生成swagger_gen测试用例','NULL',false,'timeout','timeout',3011,1269,807,2076,0.0623,'2026-05-26 16:16:00');

INSERT INTO ai_invocation_logs(user_id,feature,model_name,prompt,response,success,error_message,error_type,latency_ms,prompt_tokens,completion_tokens,total_tokens,cost_estimate,created_at)VALUES(1,'review','claude-3-opus','生成review测试用例','好的已生成',true,NULL,NULL,7874,2632,1928,4560,0.1368,'2026-03-14 17:55:00');

INSERT INTO ai_invocation_logs(user_id,feature,model_name,prompt,response,success,error_message,error_type,latency_ms,prompt_tokens,completion_tokens,total_tokens,cost_estimate,created_at)VALUES(8,'script_gen','claude-3-sonnet','生成script_gen测试用例','好的已生成',true,NULL,NULL,2846,3321,1975,5296,0.1589,'2026-02-25 15:36:00');

INSERT INTO ai_invocation_logs(user_id,feature,model_name,prompt,response,success,error_message,error_type,latency_ms,prompt_tokens,completion_tokens,total_tokens,cost_estimate,created_at)VALUES(9,'swagger_gen','claude-3-sonnet','生成swagger_gen测试用例','好的已生成',true,NULL,NULL,7191,3879,540,4419,0.1326,'2026-05-28 19:05:00');

INSERT INTO ai_invocation_logs(user_id,feature,model_name,prompt,response,success,error_message,error_type,latency_ms,prompt_tokens,completion_tokens,total_tokens,cost_estimate,created_at)VALUES(7,'script_gen','gpt-4o-mini','生成script_gen测试用例','好的已生成',true,NULL,NULL,6076,2510,293,2803,0.0841,'2026-03-25 04:36:00');

INSERT INTO ai_invocation_logs(user_id,feature,model_name,prompt,response,success,error_message,error_type,latency_ms,prompt_tokens,completion_tokens,total_tokens,cost_estimate,created_at)VALUES(2,'swagger_gen','gpt-4o','生成swagger_gen测试用例','好的已生成',true,NULL,NULL,2369,2765,1165,3930,0.1179,'2026-01-03 03:45:00');

INSERT INTO ai_invocation_logs(user_id,feature,model_name,prompt,response,success,error_message,error_type,latency_ms,prompt_tokens,completion_tokens,total_tokens,cost_estimate,created_at)VALUES(5,'dedup','gpt-4o','生成dedup测试用例','好的已生成',true,NULL,NULL,2794,3729,682,4411,0.1323,'2026-04-07 11:09:00');

INSERT INTO ai_invocation_logs(user_id,feature,model_name,prompt,response,success,error_message,error_type,latency_ms,prompt_tokens,completion_tokens,total_tokens,cost_estimate,created_at)VALUES(1,'dedup','claude-3-sonnet','生成dedup测试用例','好的已生成',true,NULL,NULL,6510,1975,512,2487,0.0746,'2026-05-05 12:03:00');

INSERT INTO ai_invocation_logs(user_id,feature,model_name,prompt,response,success,error_message,error_type,latency_ms,prompt_tokens,completion_tokens,total_tokens,cost_estimate,created_at)VALUES(1,'copilot','gpt-4o','生成copilot测试用例','好的已生成',true,NULL,NULL,4548,3466,779,4245,0.1273,'2026-04-20 05:01:00');

INSERT INTO ai_invocation_logs(user_id,feature,model_name,prompt,response,success,error_message,error_type,latency_ms,prompt_tokens,completion_tokens,total_tokens,cost_estimate,created_at)VALUES(2,'copilot','claude-3-opus','生成copilot测试用例','好的已生成',true,NULL,NULL,3858,478,1926,2404,0.0721,'2026-01-10 01:40:00');

INSERT INTO ai_invocation_logs(user_id,feature,model_name,prompt,response,success,error_message,error_type,latency_ms,prompt_tokens,completion_tokens,total_tokens,cost_estimate,created_at)VALUES(5,'script_gen','claude-3-opus','生成script_gen测试用例','好的已生成',true,NULL,NULL,5589,1244,1563,2807,0.0842,'2026-04-16 20:04:00');

INSERT INTO ai_invocation_logs(user_id,feature,model_name,prompt,response,success,error_message,error_type,latency_ms,prompt_tokens,completion_tokens,total_tokens,cost_estimate,created_at)VALUES(10,'swagger_gen','claude-3-opus','生成swagger_gen测试用例','好的已生成',true,NULL,NULL,5528,3746,1440,5186,0.1556,'2026-01-25 08:53:00');

INSERT INTO ai_invocation_logs(user_id,feature,model_name,prompt,response,success,error_message,error_type,latency_ms,prompt_tokens,completion_tokens,total_tokens,cost_estimate,created_at)VALUES(10,'script_gen','gpt-4o-mini','生成script_gen测试用例','好的已生成',true,NULL,NULL,7849,3441,1435,4876,0.1463,'2026-05-25 11:27:00');

INSERT INTO ai_invocation_logs(user_id,feature,model_name,prompt,response,success,error_message,error_type,latency_ms,prompt_tokens,completion_tokens,total_tokens,cost_estimate,created_at)VALUES(9,'swagger_gen','gpt-4o-mini','生成swagger_gen测试用例','好的已生成',true,NULL,NULL,3843,1995,977,2972,0.0892,'2026-04-28 15:33:00');

INSERT INTO ai_invocation_logs(user_id,feature,model_name,prompt,response,success,error_message,error_type,latency_ms,prompt_tokens,completion_tokens,total_tokens,cost_estimate,created_at)VALUES(9,'swagger_gen','claude-3-sonnet','生成swagger_gen测试用例','好的已生成',true,NULL,NULL,4034,113,278,391,0.0117,'2026-03-22 08:19:00');

INSERT INTO ai_invocation_logs(user_id,feature,model_name,prompt,response,success,error_message,error_type,latency_ms,prompt_tokens,completion_tokens,total_tokens,cost_estimate,created_at)VALUES(1,'swagger_gen','gpt-4o-mini','生成swagger_gen测试用例','好的已生成',true,NULL,NULL,7838,2299,178,2477,0.0743,'2026-05-25 22:40:00');

INSERT INTO ai_invocation_logs(user_id,feature,model_name,prompt,response,success,error_message,error_type,latency_ms,prompt_tokens,completion_tokens,total_tokens,cost_estimate,created_at)VALUES(1,'copilot','gpt-4o','生成copilot测试用例','好的已生成',true,NULL,NULL,4163,3607,1447,5054,0.1516,'2026-04-16 10:52:00');

INSERT INTO ai_invocation_logs(user_id,feature,model_name,prompt,response,success,error_message,error_type,latency_ms,prompt_tokens,completion_tokens,total_tokens,cost_estimate,created_at)VALUES(2,'swagger_gen','gpt-4o-mini','生成swagger_gen测试用例','好的已生成',true,NULL,NULL,5627,3568,1986,5554,0.1666,'2026-04-13 06:33:00');

INSERT INTO ai_invocation_logs(user_id,feature,model_name,prompt,response,success,error_message,error_type,latency_ms,prompt_tokens,completion_tokens,total_tokens,cost_estimate,created_at)VALUES(1,'review','claude-3-opus','生成review测试用例','好的已生成',true,NULL,NULL,4899,2935,1671,4606,0.1382,'2026-05-01 03:12:00');

INSERT INTO ai_invocation_logs(user_id,feature,model_name,prompt,response,success,error_message,error_type,latency_ms,prompt_tokens,completion_tokens,total_tokens,cost_estimate,created_at)VALUES(9,'review','gpt-4o','生成review测试用例','好的已生成',true,NULL,NULL,1547,3820,121,3941,0.1182,'2026-04-12 06:48:00');

INSERT INTO ai_invocation_logs(user_id,feature,model_name,prompt,response,success,error_message,error_type,latency_ms,prompt_tokens,completion_tokens,total_tokens,cost_estimate,created_at)VALUES(9,'review','claude-3-opus','生成review测试用例','好的已生成',true,NULL,NULL,1462,2222,1638,3860,0.1158,'2026-02-21 04:02:00');

INSERT INTO ai_invocation_logs(user_id,feature,model_name,prompt,response,success,error_message,error_type,latency_ms,prompt_tokens,completion_tokens,total_tokens,cost_estimate,created_at)VALUES(1,'review','gpt-4o-mini','生成review测试用例','好的已生成',true,NULL,NULL,5370,3605,1042,4647,0.1394,'2026-03-29 22:52:00');

INSERT INTO ai_invocation_logs(user_id,feature,model_name,prompt,response,success,error_message,error_type,latency_ms,prompt_tokens,completion_tokens,total_tokens,cost_estimate,created_at)VALUES(8,'review','claude-3-opus','生成review测试用例','好的已生成',true,NULL,NULL,7243,2800,1448,4248,0.1274,'2026-04-08 02:51:00');

INSERT INTO ai_invocation_logs(user_id,feature,model_name,prompt,response,success,error_message,error_type,latency_ms,prompt_tokens,completion_tokens,total_tokens,cost_estimate,created_at)VALUES(5,'script_gen','claude-3-sonnet','生成script_gen测试用例','好的已生成',true,NULL,NULL,5245,878,1880,2758,0.0827,'2026-01-18 14:22:00');

INSERT INTO ai_invocation_logs(user_id,feature,model_name,prompt,response,success,error_message,error_type,latency_ms,prompt_tokens,completion_tokens,total_tokens,cost_estimate,created_at)VALUES(5,'copilot','claude-3-opus','生成copilot测试用例','好的已生成',true,NULL,NULL,4080,2931,1470,4401,0.132,'2026-04-05 22:46:00');

INSERT INTO ai_invocation_logs(user_id,feature,model_name,prompt,response,success,error_message,error_type,latency_ms,prompt_tokens,completion_tokens,total_tokens,cost_estimate,created_at)VALUES(5,'script_gen','claude-3-sonnet','生成script_gen测试用例','好的已生成',true,NULL,NULL,4355,1533,121,1654,0.0496,'2026-01-31 21:55:00');

INSERT INTO ai_invocation_logs(user_id,feature,model_name,prompt,response,success,error_message,error_type,latency_ms,prompt_tokens,completion_tokens,total_tokens,cost_estimate,created_at)VALUES(1,'review','claude-3-sonnet','生成review测试用例','NULL',false,'timeout','timeout',1735,1693,1293,2986,0.0896,'2026-01-25 06:12:00');

INSERT INTO ai_invocation_logs(user_id,feature,model_name,prompt,response,success,error_message,error_type,latency_ms,prompt_tokens,completion_tokens,total_tokens,cost_estimate,created_at)VALUES(5,'script_gen','claude-3-sonnet','生成script_gen测试用例','NULL',false,'timeout','timeout',315,2112,305,2417,0.0725,'2026-04-22 21:54:00');

INSERT INTO ai_invocation_logs(user_id,feature,model_name,prompt,response,success,error_message,error_type,latency_ms,prompt_tokens,completion_tokens,total_tokens,cost_estimate,created_at)VALUES(8,'review','gpt-4o-mini','生成review测试用例','好的已生成',true,NULL,NULL,4773,2876,1197,4073,0.1222,'2025-12-22 04:15:00');

INSERT INTO ai_invocation_logs(user_id,feature,model_name,prompt,response,success,error_message,error_type,latency_ms,prompt_tokens,completion_tokens,total_tokens,cost_estimate,created_at)VALUES(2,'dedup','claude-3-sonnet','生成dedup测试用例','好的已生成',true,NULL,NULL,6442,1173,1143,2316,0.0695,'2026-03-26 21:30:00');

INSERT INTO ai_invocation_logs(user_id,feature,model_name,prompt,response,success,error_message,error_type,latency_ms,prompt_tokens,completion_tokens,total_tokens,cost_estimate,created_at)VALUES(6,'swagger_gen','claude-3-sonnet','生成swagger_gen测试用例','好的已生成',true,NULL,NULL,1273,694,479,1173,0.0352,'2026-04-06 11:51:00');

INSERT INTO ai_invocation_logs(user_id,feature,model_name,prompt,response,success,error_message,error_type,latency_ms,prompt_tokens,completion_tokens,total_tokens,cost_estimate,created_at)VALUES(5,'script_gen','gpt-4o','生成script_gen测试用例','好的已生成',true,NULL,NULL,6379,2588,648,3236,0.0971,'2026-03-29 05:38:00');

INSERT INTO ai_invocation_logs(user_id,feature,model_name,prompt,response,success,error_message,error_type,latency_ms,prompt_tokens,completion_tokens,total_tokens,cost_estimate,created_at)VALUES(5,'script_gen','gpt-4o-mini','生成script_gen测试用例','好的已生成',true,NULL,NULL,3097,1758,167,1925,0.0578,'2026-02-25 04:08:00');

INSERT INTO ai_invocation_logs(user_id,feature,model_name,prompt,response,success,error_message,error_type,latency_ms,prompt_tokens,completion_tokens,total_tokens,cost_estimate,created_at)VALUES(8,'script_gen','claude-3-opus','生成script_gen测试用例','好的已生成',true,NULL,NULL,7574,1695,546,2241,0.0672,'2025-12-20 10:30:00');

INSERT INTO ai_invocation_logs(user_id,feature,model_name,prompt,response,success,error_message,error_type,latency_ms,prompt_tokens,completion_tokens,total_tokens,cost_estimate,created_at)VALUES(6,'copilot','gpt-4o','生成copilot测试用例','好的已生成',true,NULL,NULL,2424,1725,1450,3175,0.0953,'2026-01-27 01:54:00');

INSERT INTO ai_invocation_logs(user_id,feature,model_name,prompt,response,success,error_message,error_type,latency_ms,prompt_tokens,completion_tokens,total_tokens,cost_estimate,created_at)VALUES(6,'copilot','claude-3-sonnet','生成copilot测试用例','好的已生成',true,NULL,NULL,2076,3609,1194,4803,0.1441,'2026-03-15 06:19:00');

INSERT INTO ai_invocation_logs(user_id,feature,model_name,prompt,response,success,error_message,error_type,latency_ms,prompt_tokens,completion_tokens,total_tokens,cost_estimate,created_at)VALUES(8,'script_gen','gpt-4o','生成script_gen测试用例','好的已生成',true,NULL,NULL,787,1000,1636,2636,0.0791,'2026-02-23 04:35:00');

INSERT INTO ai_invocation_logs(user_id,feature,model_name,prompt,response,success,error_message,error_type,latency_ms,prompt_tokens,completion_tokens,total_tokens,cost_estimate,created_at)VALUES(1,'review','claude-3-opus','生成review测试用例','好的已生成',true,NULL,NULL,2077,2438,1746,4184,0.1255,'2026-01-30 12:37:00');

INSERT INTO ai_invocation_logs(user_id,feature,model_name,prompt,response,success,error_message,error_type,latency_ms,prompt_tokens,completion_tokens,total_tokens,cost_estimate,created_at)VALUES(9,'copilot','claude-3-opus','生成copilot测试用例','好的已生成',true,NULL,NULL,6677,2050,142,2192,0.0658,'2026-02-28 23:44:00');

INSERT INTO ai_invocation_logs(user_id,feature,model_name,prompt,response,success,error_message,error_type,latency_ms,prompt_tokens,completion_tokens,total_tokens,cost_estimate,created_at)VALUES(2,'script_gen','gpt-4o','生成script_gen测试用例','好的已生成',true,NULL,NULL,3707,3050,598,3648,0.1094,'2026-05-14 07:24:00');

INSERT INTO ai_invocation_logs(user_id,feature,model_name,prompt,response,success,error_message,error_type,latency_ms,prompt_tokens,completion_tokens,total_tokens,cost_estimate,created_at)VALUES(8,'swagger_gen','claude-3-sonnet','生成swagger_gen测试用例','好的已生成',true,NULL,NULL,4865,3922,1423,5345,0.1603,'2026-05-08 15:14:00');

INSERT INTO ai_invocation_logs(user_id,feature,model_name,prompt,response,success,error_message,error_type,latency_ms,prompt_tokens,completion_tokens,total_tokens,cost_estimate,created_at)VALUES(9,'review','gpt-4o-mini','生成review测试用例','好的已生成',true,NULL,NULL,3893,2341,1067,3408,0.1022,'2026-03-02 04:57:00');

INSERT INTO ai_invocation_logs(user_id,feature,model_name,prompt,response,success,error_message,error_type,latency_ms,prompt_tokens,completion_tokens,total_tokens,cost_estimate,created_at)VALUES(10,'copilot','gpt-4o-mini','生成copilot测试用例','NULL',false,'timeout','timeout',1582,1880,374,2254,0.0676,'2025-12-13 09:56:00');

INSERT INTO ai_invocation_logs(user_id,feature,model_name,prompt,response,success,error_message,error_type,latency_ms,prompt_tokens,completion_tokens,total_tokens,cost_estimate,created_at)VALUES(10,'copilot','gpt-4o-mini','生成copilot测试用例','好的已生成',true,NULL,NULL,935,713,679,1392,0.0418,'2026-05-14 03:24:00');

INSERT INTO ai_invocation_logs(user_id,feature,model_name,prompt,response,success,error_message,error_type,latency_ms,prompt_tokens,completion_tokens,total_tokens,cost_estimate,created_at)VALUES(6,'dedup','claude-3-sonnet','生成dedup测试用例','好的已生成',true,NULL,NULL,4841,2751,979,3730,0.1119,'2026-02-18 08:24:00');

INSERT INTO ai_invocation_logs(user_id,feature,model_name,prompt,response,success,error_message,error_type,latency_ms,prompt_tokens,completion_tokens,total_tokens,cost_estimate,created_at)VALUES(10,'script_gen','gpt-4o','生成script_gen测试用例','好的已生成',true,NULL,NULL,4218,3758,1040,4798,0.1439,'2026-04-03 07:09:00');

INSERT INTO ai_invocation_logs(user_id,feature,model_name,prompt,response,success,error_message,error_type,latency_ms,prompt_tokens,completion_tokens,total_tokens,cost_estimate,created_at)VALUES(5,'script_gen','claude-3-sonnet','生成script_gen测试用例','好的已生成',true,NULL,NULL,5729,3231,107,3338,0.1001,'2026-02-03 23:16:00');

INSERT INTO ai_invocation_logs(user_id,feature,model_name,prompt,response,success,error_message,error_type,latency_ms,prompt_tokens,completion_tokens,total_tokens,cost_estimate,created_at)VALUES(10,'review','claude-3-sonnet','生成review测试用例','好的已生成',true,NULL,NULL,7086,2710,1966,4676,0.1403,'2026-04-08 13:17:00');

INSERT INTO ai_invocation_logs(user_id,feature,model_name,prompt,response,success,error_message,error_type,latency_ms,prompt_tokens,completion_tokens,total_tokens,cost_estimate,created_at)VALUES(7,'script_gen','gpt-4o','生成script_gen测试用例','好的已生成',true,NULL,NULL,5360,3253,832,4085,0.1226,'2026-03-09 00:48:00');

INSERT INTO ai_invocation_logs(user_id,feature,model_name,prompt,response,success,error_message,error_type,latency_ms,prompt_tokens,completion_tokens,total_tokens,cost_estimate,created_at)VALUES(1,'review','claude-3-opus','生成review测试用例','好的已生成',true,NULL,NULL,1221,692,143,835,0.025,'2026-04-22 06:23:00');

INSERT INTO ai_invocation_logs(user_id,feature,model_name,prompt,response,success,error_message,error_type,latency_ms,prompt_tokens,completion_tokens,total_tokens,cost_estimate,created_at)VALUES(2,'swagger_gen','gpt-4o','生成swagger_gen测试用例','好的已生成',true,NULL,NULL,4183,3407,824,4231,0.1269,'2026-03-24 00:24:00');

INSERT INTO ai_invocation_logs(user_id,feature,model_name,prompt,response,success,error_message,error_type,latency_ms,prompt_tokens,completion_tokens,total_tokens,cost_estimate,created_at)VALUES(10,'swagger_gen','claude-3-sonnet','生成swagger_gen测试用例','NULL',false,'timeout','timeout',609,104,337,441,0.0132,'2026-02-13 16:31:00');

INSERT INTO ai_invocation_logs(user_id,feature,model_name,prompt,response,success,error_message,error_type,latency_ms,prompt_tokens,completion_tokens,total_tokens,cost_estimate,created_at)VALUES(9,'swagger_gen','claude-3-opus','生成swagger_gen测试用例','好的已生成',true,NULL,NULL,6446,1882,1066,2948,0.0884,'2026-02-19 00:24:00');

INSERT INTO ai_invocation_logs(user_id,feature,model_name,prompt,response,success,error_message,error_type,latency_ms,prompt_tokens,completion_tokens,total_tokens,cost_estimate,created_at)VALUES(10,'review','claude-3-sonnet','生成review测试用例','好的已生成',true,NULL,NULL,7448,3954,232,4186,0.1256,'2026-02-14 03:36:00');

INSERT INTO ai_invocation_logs(user_id,feature,model_name,prompt,response,success,error_message,error_type,latency_ms,prompt_tokens,completion_tokens,total_tokens,cost_estimate,created_at)VALUES(8,'dedup','gpt-4o','生成dedup测试用例','好的已生成',true,NULL,NULL,2908,235,97,332,0.01,'2026-02-17 02:38:00');

INSERT INTO ai_invocation_logs(user_id,feature,model_name,prompt,response,success,error_message,error_type,latency_ms,prompt_tokens,completion_tokens,total_tokens,cost_estimate,created_at)VALUES(8,'script_gen','claude-3-sonnet','生成script_gen测试用例','好的已生成',true,NULL,NULL,5023,3127,840,3967,0.119,'2026-03-23 15:33:00');

INSERT INTO ai_invocation_logs(user_id,feature,model_name,prompt,response,success,error_message,error_type,latency_ms,prompt_tokens,completion_tokens,total_tokens,cost_estimate,created_at)VALUES(5,'dedup','claude-3-sonnet','生成dedup测试用例','NULL',false,'timeout','timeout',7431,2700,1208,3908,0.1172,'2025-12-16 22:52:00');

INSERT INTO ai_invocation_logs(user_id,feature,model_name,prompt,response,success,error_message,error_type,latency_ms,prompt_tokens,completion_tokens,total_tokens,cost_estimate,created_at)VALUES(9,'script_gen','claude-3-opus','生成script_gen测试用例','好的已生成',true,NULL,NULL,5891,1619,1265,2884,0.0865,'2026-02-01 11:00:00');

INSERT INTO ai_invocation_logs(user_id,feature,model_name,prompt,response,success,error_message,error_type,latency_ms,prompt_tokens,completion_tokens,total_tokens,cost_estimate,created_at)VALUES(5,'swagger_gen','claude-3-opus','生成swagger_gen测试用例','好的已生成',true,NULL,NULL,4533,759,997,1756,0.0527,'2026-02-15 12:47:00');

INSERT INTO ai_invocation_logs(user_id,feature,model_name,prompt,response,success,error_message,error_type,latency_ms,prompt_tokens,completion_tokens,total_tokens,cost_estimate,created_at)VALUES(9,'swagger_gen','gpt-4o-mini','生成swagger_gen测试用例','好的已生成',true,NULL,NULL,7190,1386,1307,2693,0.0808,'2026-03-18 17:21:00');

INSERT INTO ai_invocation_logs(user_id,feature,model_name,prompt,response,success,error_message,error_type,latency_ms,prompt_tokens,completion_tokens,total_tokens,cost_estimate,created_at)VALUES(8,'review','claude-3-sonnet','生成review测试用例','好的已生成',true,NULL,NULL,2507,1795,1396,3191,0.0957,'2026-02-10 02:41:00');

INSERT INTO ai_invocation_logs(user_id,feature,model_name,prompt,response,success,error_message,error_type,latency_ms,prompt_tokens,completion_tokens,total_tokens,cost_estimate,created_at)VALUES(8,'swagger_gen','claude-3-opus','生成swagger_gen测试用例','好的已生成',true,NULL,NULL,2718,3004,577,3581,0.1074,'2026-05-14 00:21:00');

INSERT INTO ai_invocation_logs(user_id,feature,model_name,prompt,response,success,error_message,error_type,latency_ms,prompt_tokens,completion_tokens,total_tokens,cost_estimate,created_at)VALUES(2,'dedup','gpt-4o-mini','生成dedup测试用例','好的已生成',true,NULL,NULL,2186,3515,1495,5010,0.1503,'2026-03-27 01:23:00');

INSERT INTO ai_invocation_logs(user_id,feature,model_name,prompt,response,success,error_message,error_type,latency_ms,prompt_tokens,completion_tokens,total_tokens,cost_estimate,created_at)VALUES(10,'swagger_gen','gpt-4o-mini','生成swagger_gen测试用例','好的已生成',true,NULL,NULL,2408,3692,889,4581,0.1374,'2026-03-26 09:27:00');

INSERT INTO ai_invocation_logs(user_id,feature,model_name,prompt,response,success,error_message,error_type,latency_ms,prompt_tokens,completion_tokens,total_tokens,cost_estimate,created_at)VALUES(5,'script_gen','gpt-4o-mini','生成script_gen测试用例','NULL',false,'timeout','timeout',2888,2150,910,3060,0.0918,'2026-04-29 14:14:00');

INSERT INTO ai_invocation_logs(user_id,feature,model_name,prompt,response,success,error_message,error_type,latency_ms,prompt_tokens,completion_tokens,total_tokens,cost_estimate,created_at)VALUES(10,'script_gen','claude-3-opus','生成script_gen测试用例','好的已生成',true,NULL,NULL,1491,524,66,590,0.0177,'2026-01-05 19:52:00');

INSERT INTO ai_invocation_logs(user_id,feature,model_name,prompt,response,success,error_message,error_type,latency_ms,prompt_tokens,completion_tokens,total_tokens,cost_estimate,created_at)VALUES(1,'script_gen','gpt-4o','生成script_gen测试用例','好的已生成',true,NULL,NULL,6439,277,1030,1307,0.0392,'2026-03-10 00:03:00');

INSERT INTO ai_invocation_logs(user_id,feature,model_name,prompt,response,success,error_message,error_type,latency_ms,prompt_tokens,completion_tokens,total_tokens,cost_estimate,created_at)VALUES(8,'script_gen','claude-3-opus','生成script_gen测试用例','好的已生成',true,NULL,NULL,6625,1790,808,2598,0.0779,'2026-03-06 18:09:00');

INSERT INTO ai_invocation_logs(user_id,feature,model_name,prompt,response,success,error_message,error_type,latency_ms,prompt_tokens,completion_tokens,total_tokens,cost_estimate,created_at)VALUES(5,'script_gen','gpt-4o','生成script_gen测试用例','好的已生成',true,NULL,NULL,551,1336,619,1955,0.0587,'2026-01-06 20:06:00');

INSERT INTO ai_invocation_logs(user_id,feature,model_name,prompt,response,success,error_message,error_type,latency_ms,prompt_tokens,completion_tokens,total_tokens,cost_estimate,created_at)VALUES(7,'dedup','gpt-4o','生成dedup测试用例','好的已生成',true,NULL,NULL,5204,1015,1210,2225,0.0668,'2026-05-19 09:51:00');

INSERT INTO ai_invocation_logs(user_id,feature,model_name,prompt,response,success,error_message,error_type,latency_ms,prompt_tokens,completion_tokens,total_tokens,cost_estimate,created_at)VALUES(8,'copilot','gpt-4o-mini','生成copilot测试用例','好的已生成',true,NULL,NULL,1871,3105,1819,4924,0.1477,'2026-02-02 23:06:00');

INSERT INTO ai_invocation_logs(user_id,feature,model_name,prompt,response,success,error_message,error_type,latency_ms,prompt_tokens,completion_tokens,total_tokens,cost_estimate,created_at)VALUES(9,'swagger_gen','claude-3-sonnet','生成swagger_gen测试用例','好的已生成',true,NULL,NULL,4970,1481,1336,2817,0.0845,'2025-12-09 19:00:00');

INSERT INTO ai_invocation_logs(user_id,feature,model_name,prompt,response,success,error_message,error_type,latency_ms,prompt_tokens,completion_tokens,total_tokens,cost_estimate,created_at)VALUES(9,'copilot','gpt-4o-mini','生成copilot测试用例','好的已生成',true,NULL,NULL,2338,2991,788,3779,0.1134,'2026-01-11 00:48:00');

INSERT INTO ai_invocation_logs(user_id,feature,model_name,prompt,response,success,error_message,error_type,latency_ms,prompt_tokens,completion_tokens,total_tokens,cost_estimate,created_at)VALUES(7,'swagger_gen','claude-3-sonnet','生成swagger_gen测试用例','好的已生成',true,NULL,NULL,893,396,506,902,0.0271,'2026-01-13 16:37:00');

INSERT INTO ai_invocation_logs(user_id,feature,model_name,prompt,response,success,error_message,error_type,latency_ms,prompt_tokens,completion_tokens,total_tokens,cost_estimate,created_at)VALUES(1,'script_gen','claude-3-opus','生成script_gen测试用例','好的已生成',true,NULL,NULL,1760,3494,884,4378,0.1313,'2026-04-21 12:13:00');

INSERT INTO ai_invocation_logs(user_id,feature,model_name,prompt,response,success,error_message,error_type,latency_ms,prompt_tokens,completion_tokens,total_tokens,cost_estimate,created_at)VALUES(5,'copilot','gpt-4o-mini','生成copilot测试用例','好的已生成',true,NULL,NULL,3947,1299,425,1724,0.0517,'2026-03-25 20:47:00');

INSERT INTO ai_invocation_logs(user_id,feature,model_name,prompt,response,success,error_message,error_type,latency_ms,prompt_tokens,completion_tokens,total_tokens,cost_estimate,created_at)VALUES(2,'copilot','claude-3-opus','生成copilot测试用例','好的已生成',true,NULL,NULL,3892,3025,1236,4261,0.1278,'2026-02-14 17:13:00');

INSERT INTO ai_invocation_logs(user_id,feature,model_name,prompt,response,success,error_message,error_type,latency_ms,prompt_tokens,completion_tokens,total_tokens,cost_estimate,created_at)VALUES(9,'review','gpt-4o','生成review测试用例','NULL',false,'timeout','timeout',6683,3792,1994,5786,0.1736,'2025-12-16 23:15:00');

INSERT INTO ai_invocation_logs(user_id,feature,model_name,prompt,response,success,error_message,error_type,latency_ms,prompt_tokens,completion_tokens,total_tokens,cost_estimate,created_at)VALUES(5,'review','claude-3-opus','生成review测试用例','好的已生成',true,NULL,NULL,4972,305,363,668,0.02,'2025-12-16 07:19:00');

INSERT INTO ai_invocation_logs(user_id,feature,model_name,prompt,response,success,error_message,error_type,latency_ms,prompt_tokens,completion_tokens,total_tokens,cost_estimate,created_at)VALUES(10,'dedup','claude-3-opus','生成dedup测试用例','NULL',false,'timeout','timeout',2358,871,126,997,0.0299,'2026-03-16 03:07:00');

INSERT INTO ai_invocation_logs(user_id,feature,model_name,prompt,response,success,error_message,error_type,latency_ms,prompt_tokens,completion_tokens,total_tokens,cost_estimate,created_at)VALUES(8,'copilot','gpt-4o-mini','生成copilot测试用例','好的已生成',true,NULL,NULL,6703,3341,1759,5100,0.153,'2026-02-28 08:50:00');

INSERT INTO ai_invocation_logs(user_id,feature,model_name,prompt,response,success,error_message,error_type,latency_ms,prompt_tokens,completion_tokens,total_tokens,cost_estimate,created_at)VALUES(5,'review','claude-3-opus','生成review测试用例','好的已生成',true,NULL,NULL,2971,842,968,1810,0.0543,'2026-03-06 10:05:00');

INSERT INTO ai_invocation_logs(user_id,feature,model_name,prompt,response,success,error_message,error_type,latency_ms,prompt_tokens,completion_tokens,total_tokens,cost_estimate,created_at)VALUES(5,'script_gen','gpt-4o-mini','生成script_gen测试用例','好的已生成',true,NULL,NULL,1455,2654,1674,4328,0.1298,'2026-04-03 09:52:00');

INSERT INTO ai_invocation_logs(user_id,feature,model_name,prompt,response,success,error_message,error_type,latency_ms,prompt_tokens,completion_tokens,total_tokens,cost_estimate,created_at)VALUES(1,'script_gen','claude-3-opus','生成script_gen测试用例','好的已生成',true,NULL,NULL,1083,982,468,1450,0.0435,'2026-05-30 02:59:00');

INSERT INTO ai_invocation_logs(user_id,feature,model_name,prompt,response,success,error_message,error_type,latency_ms,prompt_tokens,completion_tokens,total_tokens,cost_estimate,created_at)VALUES(6,'script_gen','claude-3-opus','生成script_gen测试用例','好的已生成',true,NULL,NULL,3812,377,1553,1930,0.0579,'2025-12-06 06:18:00');

INSERT INTO ai_invocation_logs(user_id,feature,model_name,prompt,response,success,error_message,error_type,latency_ms,prompt_tokens,completion_tokens,total_tokens,cost_estimate,created_at)VALUES(9,'dedup','claude-3-opus','生成dedup测试用例','好的已生成',true,NULL,NULL,287,1892,1802,3694,0.1108,'2026-02-12 05:11:00');

INSERT INTO ai_invocation_logs(user_id,feature,model_name,prompt,response,success,error_message,error_type,latency_ms,prompt_tokens,completion_tokens,total_tokens,cost_estimate,created_at)VALUES(10,'review','claude-3-opus','生成review测试用例','好的已生成',true,NULL,NULL,2782,1120,1890,3010,0.0903,'2026-05-18 04:43:00');

INSERT INTO ai_invocation_logs(user_id,feature,model_name,prompt,response,success,error_message,error_type,latency_ms,prompt_tokens,completion_tokens,total_tokens,cost_estimate,created_at)VALUES(8,'script_gen','gpt-4o','生成script_gen测试用例','NULL',false,'timeout','timeout',7601,808,1914,2722,0.0817,'2026-04-02 10:23:00');

INSERT INTO ai_invocation_logs(user_id,feature,model_name,prompt,response,success,error_message,error_type,latency_ms,prompt_tokens,completion_tokens,total_tokens,cost_estimate,created_at)VALUES(7,'dedup','gpt-4o-mini','生成dedup测试用例','好的已生成',true,NULL,NULL,1975,1209,1517,2726,0.0818,'2026-04-29 08:52:00');

INSERT INTO ai_invocation_logs(user_id,feature,model_name,prompt,response,success,error_message,error_type,latency_ms,prompt_tokens,completion_tokens,total_tokens,cost_estimate,created_at)VALUES(7,'dedup','gpt-4o','生成dedup测试用例','好的已生成',true,NULL,NULL,6749,2481,1707,4188,0.1256,'2026-05-28 07:31:00');

INSERT INTO ai_invocation_logs(user_id,feature,model_name,prompt,response,success,error_message,error_type,latency_ms,prompt_tokens,completion_tokens,total_tokens,cost_estimate,created_at)VALUES(5,'script_gen','gpt-4o-mini','生成script_gen测试用例','好的已生成',true,NULL,NULL,7417,1629,169,1798,0.0539,'2026-02-08 10:34:00');

INSERT INTO ai_invocation_logs(user_id,feature,model_name,prompt,response,success,error_message,error_type,latency_ms,prompt_tokens,completion_tokens,total_tokens,cost_estimate,created_at)VALUES(7,'review','claude-3-sonnet','生成review测试用例','好的已生成',true,NULL,NULL,1032,3506,1928,5434,0.163,'2026-01-30 13:20:00');

INSERT INTO ai_invocation_logs(user_id,feature,model_name,prompt,response,success,error_message,error_type,latency_ms,prompt_tokens,completion_tokens,total_tokens,cost_estimate,created_at)VALUES(10,'swagger_gen','claude-3-opus','生成swagger_gen测试用例','好的已生成',true,NULL,NULL,5297,3322,1754,5076,0.1523,'2025-12-30 04:01:00');

INSERT INTO ai_invocation_logs(user_id,feature,model_name,prompt,response,success,error_message,error_type,latency_ms,prompt_tokens,completion_tokens,total_tokens,cost_estimate,created_at)VALUES(7,'copilot','claude-3-sonnet','生成copilot测试用例','好的已生成',true,NULL,NULL,4636,1031,1149,2180,0.0654,'2026-02-09 05:10:00');

INSERT INTO performance_alert_rules(id,name,description,scenario_id,p95_threshold,error_rate_threshold,relative_p95_degradation,notify_webhook,enabled,last_triggered_at,trigger_count,created_at,updated_at)VALUES(1,'P95告警','监控性能',1,1000,NULL,NULL,'https://oapi.dingtalk.com/robot/send?access_token=xxx',true,'2026-05-22 17:05:00',4,'2026-05-16 04:51:00','2026-05-30 14:58:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO performance_alert_rules(id,name,description,scenario_id,p95_threshold,error_rate_threshold,relative_p95_degradation,notify_webhook,enabled,last_triggered_at,trigger_count,created_at,updated_at)VALUES(2,'错误率告警','监控性能',1,NULL,5.0,NULL,'https://oapi.dingtalk.com/robot/send?access_token=xxx',true,'2026-05-20 21:12:00',10,'2026-01-16 00:15:00','2026-05-30 17:14:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO performance_alert_rules(id,name,description,scenario_id,p95_threshold,error_rate_threshold,relative_p95_degradation,notify_webhook,enabled,last_triggered_at,trigger_count,created_at,updated_at)VALUES(3,'劣化告警','监控性能',1,NULL,NULL,30,'https://oapi.dingtalk.com/robot/send?access_token=xxx',true,'2026-05-18 02:20:00',7,'2026-04-13 19:24:00','2026-06-02 04:54:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO performance_alert_rules(id,name,description,scenario_id,p95_threshold,error_rate_threshold,relative_p95_degradation,notify_webhook,enabled,last_triggered_at,trigger_count,created_at,updated_at)VALUES(4,'P95告警','监控性能',3,1000,NULL,NULL,'https://oapi.dingtalk.com/robot/send?access_token=xxx',true,'2026-05-25 11:38:00',1,'2026-01-10 20:09:00','2026-06-01 12:02:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO performance_alert_rules(id,name,description,scenario_id,p95_threshold,error_rate_threshold,relative_p95_degradation,notify_webhook,enabled,last_triggered_at,trigger_count,created_at,updated_at)VALUES(5,'错误率告警','监控性能',3,NULL,5.0,NULL,'https://oapi.dingtalk.com/robot/send?access_token=xxx',true,'2026-05-19 08:05:00',2,'2026-01-28 00:16:00','2026-06-01 13:01:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO performance_alert_rules(id,name,description,scenario_id,p95_threshold,error_rate_threshold,relative_p95_degradation,notify_webhook,enabled,last_triggered_at,trigger_count,created_at,updated_at)VALUES(6,'劣化告警','监控性能',4,NULL,NULL,30,'https://oapi.dingtalk.com/robot/send?access_token=xxx',true,'2026-05-22 04:22:00',8,'2026-03-11 10:04:00','2026-06-01 18:54:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO performance_alert_rules(id,name,description,scenario_id,p95_threshold,error_rate_threshold,relative_p95_degradation,notify_webhook,enabled,last_triggered_at,trigger_count,created_at,updated_at)VALUES(7,'劣化告警','监控性能',9,NULL,NULL,30,'https://oapi.dingtalk.com/robot/send?access_token=xxx',true,'2026-05-27 03:13:00',12,'2026-05-31 11:26:00','2026-06-01 03:42:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO performance_alert_rules(id,name,description,scenario_id,p95_threshold,error_rate_threshold,relative_p95_degradation,notify_webhook,enabled,last_triggered_at,trigger_count,created_at,updated_at)VALUES(8,'劣化告警','监控性能',10,NULL,NULL,30,'https://oapi.dingtalk.com/robot/send?access_token=xxx',true,NULL,0,'2026-03-14 17:07:00','2026-05-29 17:22:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO performance_alert_rules(id,name,description,scenario_id,p95_threshold,error_rate_threshold,relative_p95_degradation,notify_webhook,enabled,last_triggered_at,trigger_count,created_at,updated_at)VALUES(9,'P95告警','监控性能',11,1000,NULL,NULL,'https://oapi.dingtalk.com/robot/send?access_token=xxx',true,'2026-06-02 01:31:00',10,'2026-05-27 05:00:00','2026-05-30 14:17:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO performance_alert_rules(id,name,description,scenario_id,p95_threshold,error_rate_threshold,relative_p95_degradation,notify_webhook,enabled,last_triggered_at,trigger_count,created_at,updated_at)VALUES(10,'劣化告警','监控性能',11,NULL,NULL,30,'https://oapi.dingtalk.com/robot/send?access_token=xxx',true,'2026-05-30 14:11:00',11,'2026-03-13 03:10:00','2026-05-29 18:44:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO performance_alert_rules(id,name,description,scenario_id,p95_threshold,error_rate_threshold,relative_p95_degradation,notify_webhook,enabled,last_triggered_at,trigger_count,created_at,updated_at)VALUES(11,'P95告警','监控性能',12,1000,NULL,NULL,'https://oapi.dingtalk.com/robot/send?access_token=xxx',true,'2026-05-20 20:20:00',5,'2026-04-09 04:04:00','2026-05-30 20:46:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO performance_alert_rules(id,name,description,scenario_id,p95_threshold,error_rate_threshold,relative_p95_degradation,notify_webhook,enabled,last_triggered_at,trigger_count,created_at,updated_at)VALUES(12,'P95告警','监控性能',14,1000,NULL,NULL,'https://oapi.dingtalk.com/robot/send?access_token=xxx',true,'2026-06-01 20:55:00',4,'2026-02-18 22:26:00','2026-06-02 05:09:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO performance_alert_rules(id,name,description,scenario_id,p95_threshold,error_rate_threshold,relative_p95_degradation,notify_webhook,enabled,last_triggered_at,trigger_count,created_at,updated_at)VALUES(13,'错误率告警','监控性能',14,NULL,5.0,NULL,'https://oapi.dingtalk.com/robot/send?access_token=xxx',true,NULL,0,'2026-02-26 15:14:00','2026-06-01 05:23:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO performance_alert_rules(id,name,description,scenario_id,p95_threshold,error_rate_threshold,relative_p95_degradation,notify_webhook,enabled,last_triggered_at,trigger_count,created_at,updated_at)VALUES(14,'错误率告警','监控性能',15,NULL,5.0,NULL,'https://oapi.dingtalk.com/robot/send?access_token=xxx',true,'2026-05-27 08:51:00',13,'2026-03-11 23:12:00','2026-05-30 02:33:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO performance_alert_rules(id,name,description,scenario_id,p95_threshold,error_rate_threshold,relative_p95_degradation,notify_webhook,enabled,last_triggered_at,trigger_count,created_at,updated_at)VALUES(15,'P95告警','监控性能',16,1000,NULL,NULL,'https://oapi.dingtalk.com/robot/send?access_token=xxx',true,'2026-05-12 20:49:00',4,'2026-03-17 12:12:00','2026-06-01 08:33:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO performance_alert_rules(id,name,description,scenario_id,p95_threshold,error_rate_threshold,relative_p95_degradation,notify_webhook,enabled,last_triggered_at,trigger_count,created_at,updated_at)VALUES(16,'错误率告警','监控性能',17,NULL,5.0,NULL,'https://oapi.dingtalk.com/robot/send?access_token=xxx',true,'2026-05-30 03:47:00',10,'2026-05-05 02:19:00','2026-06-02 08:43:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO performance_alert_rules(id,name,description,scenario_id,p95_threshold,error_rate_threshold,relative_p95_degradation,notify_webhook,enabled,last_triggered_at,trigger_count,created_at,updated_at)VALUES(17,'劣化告警','监控性能',17,NULL,NULL,30,'https://oapi.dingtalk.com/robot/send?access_token=xxx',true,'2026-05-28 07:08:00',7,'2026-05-11 04:06:00','2026-06-01 06:07:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO performance_alert_logs(rule_id,result_id,alert_type,metric_name,threshold_value,actual_value,message,notification_sent,created_at)VALUES(10,66,'absolute','p95_response_time',1586.0,2275.8,'告警:p95_response_time=2275.8>1586.0',true,'2026-02-08 06:15:00');

INSERT INTO performance_alert_logs(rule_id,result_id,alert_type,metric_name,threshold_value,actual_value,message,notification_sent,created_at)VALUES(14,69,'absolute','error_rate',1122.8,2114.0,'告警:error_rate=2114.0>1122.8',true,'2026-04-11 00:03:00');

INSERT INTO performance_alert_logs(rule_id,result_id,alert_type,metric_name,threshold_value,actual_value,message,notification_sent,created_at)VALUES(17,42,'absolute','p95_response_time',297.6,483.5,'告警:p95_response_time=483.5>297.6',true,'2026-03-25 08:36:00');

INSERT INTO performance_alert_logs(rule_id,result_id,alert_type,metric_name,threshold_value,actual_value,message,notification_sent,created_at)VALUES(1,6,'absolute','error_rate',1978.8,3512.5,'告警:error_rate=3512.5>1978.8',true,'2026-05-09 15:01:00');

INSERT INTO performance_alert_logs(rule_id,result_id,alert_type,metric_name,threshold_value,actual_value,message,notification_sent,created_at)VALUES(17,62,'absolute','rps',1839.6,2847.8,'告警:rps=2847.8>1839.6',true,'2026-04-21 17:40:00');

INSERT INTO performance_alert_logs(rule_id,result_id,alert_type,metric_name,threshold_value,actual_value,message,notification_sent,created_at)VALUES(10,52,'absolute','rps',1923.5,3220.0,'告警:rps=3220.0>1923.5',true,'2026-02-21 10:53:00');

INSERT INTO performance_alert_logs(rule_id,result_id,alert_type,metric_name,threshold_value,actual_value,message,notification_sent,created_at)VALUES(10,24,'absolute','rps',927.2,1127.8,'告警:rps=1127.8>927.2',true,'2026-05-13 11:01:00');

INSERT INTO performance_alert_logs(rule_id,result_id,alert_type,metric_name,threshold_value,actual_value,message,notification_sent,created_at)VALUES(7,24,'absolute','error_rate',1636.5,2063.9,'告警:error_rate=2063.9>1636.5',false,'2026-03-05 07:58:00');

INSERT INTO performance_alert_logs(rule_id,result_id,alert_type,metric_name,threshold_value,actual_value,message,notification_sent,created_at)VALUES(7,15,'absolute','error_rate',409.9,544.2,'告警:error_rate=544.2>409.9',true,'2026-03-30 17:02:00');

INSERT INTO performance_alert_logs(rule_id,result_id,alert_type,metric_name,threshold_value,actual_value,message,notification_sent,created_at)VALUES(4,12,'absolute','rps',1567.7,2712.1,'告警:rps=2712.1>1567.7',true,'2026-03-14 19:51:00');

INSERT INTO performance_alert_logs(rule_id,result_id,alert_type,metric_name,threshold_value,actual_value,message,notification_sent,created_at)VALUES(9,74,'absolute','error_rate',1217.4,1990.0,'告警:error_rate=1990.0>1217.4',true,'2026-05-19 13:50:00');

INSERT INTO performance_alert_logs(rule_id,result_id,alert_type,metric_name,threshold_value,actual_value,message,notification_sent,created_at)VALUES(1,8,'absolute','rps',1426.8,1711.9,'告警:rps=1711.9>1426.8',true,'2026-04-06 20:34:00');

INSERT INTO performance_alert_logs(rule_id,result_id,alert_type,metric_name,threshold_value,actual_value,message,notification_sent,created_at)VALUES(1,8,'absolute','p95_response_time',1501.3,2658.2,'告警:p95_response_time=2658.2>1501.3',false,'2026-02-02 03:13:00');

INSERT INTO performance_alert_logs(rule_id,result_id,alert_type,metric_name,threshold_value,actual_value,message,notification_sent,created_at)VALUES(13,25,'absolute','p95_response_time',1124.6,1432.8,'告警:p95_response_time=1432.8>1124.6',true,'2026-05-31 23:20:00');

INSERT INTO performance_alert_logs(rule_id,result_id,alert_type,metric_name,threshold_value,actual_value,message,notification_sent,created_at)VALUES(8,68,'absolute','p95_response_time',720.6,909.0,'告警:p95_response_time=909.0>720.6',true,'2026-03-22 12:00:00');

INSERT INTO performance_alert_logs(rule_id,result_id,alert_type,metric_name,threshold_value,actual_value,message,notification_sent,created_at)VALUES(14,22,'absolute','error_rate',1151.0,1433.7,'告警:error_rate=1433.7>1151.0',true,'2026-03-20 14:57:00');

INSERT INTO performance_alert_logs(rule_id,result_id,alert_type,metric_name,threshold_value,actual_value,message,notification_sent,created_at)VALUES(14,21,'absolute','p95_response_time',957.1,1512.8,'告警:p95_response_time=1512.8>957.1',true,'2026-02-24 20:01:00');

INSERT INTO performance_alert_logs(rule_id,result_id,alert_type,metric_name,threshold_value,actual_value,message,notification_sent,created_at)VALUES(7,65,'absolute','p95_response_time',1729.8,2178.8,'告警:p95_response_time=2178.8>1729.8',true,'2026-04-12 12:10:00');

INSERT INTO performance_alert_logs(rule_id,result_id,alert_type,metric_name,threshold_value,actual_value,message,notification_sent,created_at)VALUES(3,65,'absolute','p95_response_time',507.5,779.2,'告警:p95_response_time=779.2>507.5',true,'2026-05-17 13:26:00');

INSERT INTO performance_alert_logs(rule_id,result_id,alert_type,metric_name,threshold_value,actual_value,message,notification_sent,created_at)VALUES(8,56,'absolute','error_rate',436.4,658.7,'告警:error_rate=658.7>436.4',true,'2026-02-22 07:00:00');

INSERT INTO performance_alert_logs(rule_id,result_id,alert_type,metric_name,threshold_value,actual_value,message,notification_sent,created_at)VALUES(6,26,'absolute','p95_response_time',460.8,782.2,'告警:p95_response_time=782.2>460.8',true,'2026-03-01 14:51:00');

INSERT INTO performance_alert_logs(rule_id,result_id,alert_type,metric_name,threshold_value,actual_value,message,notification_sent,created_at)VALUES(8,45,'absolute','p95_response_time',1378.8,2570.4,'告警:p95_response_time=2570.4>1378.8',true,'2026-04-02 10:22:00');

INSERT INTO performance_alert_logs(rule_id,result_id,alert_type,metric_name,threshold_value,actual_value,message,notification_sent,created_at)VALUES(11,3,'absolute','rps',1726.7,2720.4,'告警:rps=2720.4>1726.7',true,'2026-02-06 18:29:00');

INSERT INTO performance_alert_logs(rule_id,result_id,alert_type,metric_name,threshold_value,actual_value,message,notification_sent,created_at)VALUES(12,75,'absolute','error_rate',280.4,319.4,'告警:error_rate=319.4>280.4',true,'2026-03-11 16:27:00');

INSERT INTO performance_alert_logs(rule_id,result_id,alert_type,metric_name,threshold_value,actual_value,message,notification_sent,created_at)VALUES(8,10,'absolute','p95_response_time',1727.0,3163.7,'告警:p95_response_time=3163.7>1727.0',true,'2026-04-02 14:32:00');

INSERT INTO performance_alert_logs(rule_id,result_id,alert_type,metric_name,threshold_value,actual_value,message,notification_sent,created_at)VALUES(4,46,'absolute','error_rate',321.9,620.1,'告警:error_rate=620.1>321.9',true,'2026-04-08 15:06:00');

INSERT INTO performance_alert_logs(rule_id,result_id,alert_type,metric_name,threshold_value,actual_value,message,notification_sent,created_at)VALUES(10,45,'absolute','rps',1322.2,2098.2,'告警:rps=2098.2>1322.2',true,'2026-05-09 10:17:00');

INSERT INTO performance_alert_logs(rule_id,result_id,alert_type,metric_name,threshold_value,actual_value,message,notification_sent,created_at)VALUES(5,51,'absolute','p95_response_time',1982.3,3646.9,'告警:p95_response_time=3646.9>1982.3',true,'2026-03-03 21:26:00');

INSERT INTO performance_alert_logs(rule_id,result_id,alert_type,metric_name,threshold_value,actual_value,message,notification_sent,created_at)VALUES(12,74,'absolute','error_rate',1551.1,2560.0,'告警:error_rate=2560.0>1551.1',true,'2026-05-14 23:32:00');

INSERT INTO performance_alert_logs(rule_id,result_id,alert_type,metric_name,threshold_value,actual_value,message,notification_sent,created_at)VALUES(6,44,'absolute','p95_response_time',685.3,1066.7,'告警:p95_response_time=1066.7>685.3',true,'2026-03-16 01:18:00');

INSERT INTO performance_alert_logs(rule_id,result_id,alert_type,metric_name,threshold_value,actual_value,message,notification_sent,created_at)VALUES(15,39,'absolute','error_rate',1293.7,1433.6,'告警:error_rate=1433.6>1293.7',true,'2026-03-18 14:59:00');

INSERT INTO performance_alert_logs(rule_id,result_id,alert_type,metric_name,threshold_value,actual_value,message,notification_sent,created_at)VALUES(14,55,'absolute','error_rate',609.4,931.0,'告警:error_rate=931.0>609.4',true,'2026-04-24 07:12:00');

INSERT INTO performance_alert_logs(rule_id,result_id,alert_type,metric_name,threshold_value,actual_value,message,notification_sent,created_at)VALUES(1,72,'absolute','error_rate',1190.8,1734.7,'告警:error_rate=1734.7>1190.8',false,'2026-02-20 14:31:00');

INSERT INTO performance_alert_logs(rule_id,result_id,alert_type,metric_name,threshold_value,actual_value,message,notification_sent,created_at)VALUES(12,74,'absolute','error_rate',1403.4,2172.8,'告警:error_rate=2172.8>1403.4',true,'2026-04-27 07:28:00');

INSERT INTO performance_alert_logs(rule_id,result_id,alert_type,metric_name,threshold_value,actual_value,message,notification_sent,created_at)VALUES(10,15,'absolute','p95_response_time',1625.2,2960.8,'告警:p95_response_time=2960.8>1625.2',true,'2026-05-01 00:07:00');

INSERT INTO visual_baselines(id,test_case_id,test_type,project_id,step_index,step_name,baseline_image_path,viewport_width,viewport_height,status,version,approved_by,approved_at,created_at,updated_at)VALUES(1,27,'web',2,0,'步骤1','/baselines/p2/s0.png',1920,1080,'active',4,1,'2026-03-18 16:09:00','2026-01-16 06:36:00','2026-05-30 15:26:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO visual_baselines(id,test_case_id,test_type,project_id,step_index,step_name,baseline_image_path,viewport_width,viewport_height,status,version,approved_by,approved_at,created_at,updated_at)VALUES(2,4,'web',2,1,'步骤2','/baselines/p2/s1.png',1920,1080,'active',3,1,'2026-04-25 00:00:00','2025-12-29 04:18:00','2026-05-30 09:40:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO visual_baselines(id,test_case_id,test_type,project_id,step_index,step_name,baseline_image_path,viewport_width,viewport_height,status,version,approved_by,approved_at,created_at,updated_at)VALUES(3,22,'web',2,2,'步骤3','/baselines/p2/s2.png',1920,1080,'active',1,1,'2026-05-28 04:35:00','2026-04-26 19:58:00','2026-05-29 21:42:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO visual_baselines(id,test_case_id,test_type,project_id,step_index,step_name,baseline_image_path,viewport_width,viewport_height,status,version,approved_by,approved_at,created_at,updated_at)VALUES(4,71,'web',2,3,'步骤4','/baselines/p2/s3.png',1920,1080,'active',5,1,'2026-05-25 09:07:00','2026-01-13 04:43:00','2026-05-30 22:27:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO visual_baselines(id,test_case_id,test_type,project_id,step_index,step_name,baseline_image_path,viewport_width,viewport_height,status,version,approved_by,approved_at,created_at,updated_at)VALUES(5,86,'web',5,0,'步骤1','/baselines/p5/s0.png',1920,1080,'active',1,1,'2026-04-19 18:41:00','2025-12-12 16:25:00','2026-05-31 14:22:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO visual_baselines(id,test_case_id,test_type,project_id,step_index,step_name,baseline_image_path,viewport_width,viewport_height,status,version,approved_by,approved_at,created_at,updated_at)VALUES(6,95,'web',5,1,'步骤2','/baselines/p5/s1.png',1920,1080,'active',4,1,'2026-04-28 10:54:00','2026-01-10 22:34:00','2026-06-01 09:51:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO visual_baselines(id,test_case_id,test_type,project_id,step_index,step_name,baseline_image_path,viewport_width,viewport_height,status,version,approved_by,approved_at,created_at,updated_at)VALUES(7,58,'web',5,2,'步骤3','/baselines/p5/s2.png',1920,1080,'active',3,1,'2026-05-31 09:00:00','2026-04-08 08:17:00','2026-05-30 10:36:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO visual_baselines(id,test_case_id,test_type,project_id,step_index,step_name,baseline_image_path,viewport_width,viewport_height,status,version,approved_by,approved_at,created_at,updated_at)VALUES(8,14,'web',6,0,'步骤1','/baselines/p6/s0.png',1920,1080,'active',5,1,'2026-03-16 22:19:00','2026-04-10 09:02:00','2026-05-30 21:42:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO visual_baselines(id,test_case_id,test_type,project_id,step_index,step_name,baseline_image_path,viewport_width,viewport_height,status,version,approved_by,approved_at,created_at,updated_at)VALUES(9,13,'web',6,1,'步骤2','/baselines/p6/s1.png',1920,1080,'active',5,1,'2026-04-28 15:48:00','2026-02-08 16:18:00','2026-05-30 20:32:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO visual_baselines(id,test_case_id,test_type,project_id,step_index,step_name,baseline_image_path,viewport_width,viewport_height,status,version,approved_by,approved_at,created_at,updated_at)VALUES(10,73,'web',6,2,'步骤3','/baselines/p6/s2.png',1920,1080,'active',1,1,'2026-03-28 18:02:00','2026-05-27 13:53:00','2026-05-30 04:34:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO visual_baselines(id,test_case_id,test_type,project_id,step_index,step_name,baseline_image_path,viewport_width,viewport_height,status,version,approved_by,approved_at,created_at,updated_at)VALUES(11,83,'web',6,3,'步骤4','/baselines/p6/s3.png',1920,1080,'active',1,1,'2026-05-29 06:20:00','2026-04-09 20:37:00','2026-06-02 08:46:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO visual_baselines(id,test_case_id,test_type,project_id,step_index,step_name,baseline_image_path,viewport_width,viewport_height,status,version,approved_by,approved_at,created_at,updated_at)VALUES(12,35,'web',6,4,'步骤5','/baselines/p6/s4.png',1920,1080,'active',3,1,'2026-04-24 01:52:00','2025-12-29 14:58:00','2026-05-29 18:43:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO visual_baselines(id,test_case_id,test_type,project_id,step_index,step_name,baseline_image_path,viewport_width,viewport_height,status,version,approved_by,approved_at,created_at,updated_at)VALUES(13,72,'web',7,0,'步骤1','/baselines/p7/s0.png',1920,1080,'active',4,1,'2026-04-15 04:41:00','2026-05-22 21:51:00','2026-06-01 06:40:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO visual_baselines(id,test_case_id,test_type,project_id,step_index,step_name,baseline_image_path,viewport_width,viewport_height,status,version,approved_by,approved_at,created_at,updated_at)VALUES(14,45,'web',7,1,'步骤2','/baselines/p7/s1.png',1920,1080,'active',5,1,'2026-03-16 20:05:00','2026-01-30 05:40:00','2026-05-30 04:49:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO visual_baselines(id,test_case_id,test_type,project_id,step_index,step_name,baseline_image_path,viewport_width,viewport_height,status,version,approved_by,approved_at,created_at,updated_at)VALUES(15,24,'web',7,2,'步骤3','/baselines/p7/s2.png',1920,1080,'active',1,1,'2026-03-16 09:39:00','2026-04-02 03:01:00','2026-05-30 19:10:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO visual_baselines(id,test_case_id,test_type,project_id,step_index,step_name,baseline_image_path,viewport_width,viewport_height,status,version,approved_by,approved_at,created_at,updated_at)VALUES(16,4,'web',7,3,'步骤4','/baselines/p7/s3.png',1920,1080,'active',3,1,'2026-03-30 00:30:00','2026-02-22 00:26:00','2026-05-30 12:10:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO visual_baselines(id,test_case_id,test_type,project_id,step_index,step_name,baseline_image_path,viewport_width,viewport_height,status,version,approved_by,approved_at,created_at,updated_at)VALUES(17,42,'web',7,4,'步骤5','/baselines/p7/s4.png',1920,1080,'active',3,1,'2026-03-17 02:22:00','2026-02-09 23:50:00','2026-06-02 02:26:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO visual_baselines(id,test_case_id,test_type,project_id,step_index,step_name,baseline_image_path,viewport_width,viewport_height,status,version,approved_by,approved_at,created_at,updated_at)VALUES(18,37,'web',10,0,'步骤1','/baselines/p10/s0.png',1920,1080,'active',3,1,'2026-04-18 03:54:00','2026-04-19 11:07:00','2026-06-02 09:13:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO visual_baselines(id,test_case_id,test_type,project_id,step_index,step_name,baseline_image_path,viewport_width,viewport_height,status,version,approved_by,approved_at,created_at,updated_at)VALUES(19,32,'web',10,1,'步骤2','/baselines/p10/s1.png',1920,1080,'active',4,1,'2026-05-15 12:49:00','2026-05-09 07:01:00','2026-05-30 02:01:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO visual_baselines(id,test_case_id,test_type,project_id,step_index,step_name,baseline_image_path,viewport_width,viewport_height,status,version,approved_by,approved_at,created_at,updated_at)VALUES(20,100,'web',10,2,'步骤3','/baselines/p10/s2.png',1920,1080,'active',2,1,'2026-03-11 19:29:00','2026-04-21 20:11:00','2026-05-30 16:19:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO visual_baselines(id,test_case_id,test_type,project_id,step_index,step_name,baseline_image_path,viewport_width,viewport_height,status,version,approved_by,approved_at,created_at,updated_at)VALUES(21,80,'web',11,0,'步骤1','/baselines/p11/s0.png',1920,1080,'active',3,1,'2026-03-21 23:15:00','2025-12-10 23:25:00','2026-05-31 04:49:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO visual_baselines(id,test_case_id,test_type,project_id,step_index,step_name,baseline_image_path,viewport_width,viewport_height,status,version,approved_by,approved_at,created_at,updated_at)VALUES(22,75,'web',11,1,'步骤2','/baselines/p11/s1.png',1920,1080,'active',3,1,'2026-05-10 12:07:00','2026-03-05 05:15:00','2026-05-31 06:35:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO visual_baselines(id,test_case_id,test_type,project_id,step_index,step_name,baseline_image_path,viewport_width,viewport_height,status,version,approved_by,approved_at,created_at,updated_at)VALUES(23,15,'web',11,2,'步骤3','/baselines/p11/s2.png',1920,1080,'active',5,1,'2026-04-20 18:37:00','2025-12-26 07:32:00','2026-06-02 08:39:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO visual_baselines(id,test_case_id,test_type,project_id,step_index,step_name,baseline_image_path,viewport_width,viewport_height,status,version,approved_by,approved_at,created_at,updated_at)VALUES(24,47,'web',12,0,'步骤1','/baselines/p12/s0.png',1920,1080,'active',3,1,'2026-03-17 07:44:00','2026-02-06 19:41:00','2026-05-30 18:46:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO visual_baselines(id,test_case_id,test_type,project_id,step_index,step_name,baseline_image_path,viewport_width,viewport_height,status,version,approved_by,approved_at,created_at,updated_at)VALUES(25,98,'web',12,1,'步骤2','/baselines/p12/s1.png',1920,1080,'active',3,1,'2026-03-12 03:38:00','2026-04-26 00:32:00','2026-05-31 06:07:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO visual_baselines(id,test_case_id,test_type,project_id,step_index,step_name,baseline_image_path,viewport_width,viewport_height,status,version,approved_by,approved_at,created_at,updated_at)VALUES(26,16,'web',13,0,'步骤1','/baselines/p13/s0.png',1920,1080,'active',3,1,'2026-03-19 00:16:00','2026-01-05 19:48:00','2026-05-31 00:06:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO visual_baselines(id,test_case_id,test_type,project_id,step_index,step_name,baseline_image_path,viewport_width,viewport_height,status,version,approved_by,approved_at,created_at,updated_at)VALUES(27,78,'web',13,1,'步骤2','/baselines/p13/s1.png',1920,1080,'active',2,1,'2026-05-27 23:46:00','2026-01-26 17:26:00','2026-06-02 02:48:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO visual_baselines(id,test_case_id,test_type,project_id,step_index,step_name,baseline_image_path,viewport_width,viewport_height,status,version,approved_by,approved_at,created_at,updated_at)VALUES(28,16,'web',13,2,'步骤3','/baselines/p13/s2.png',1920,1080,'active',5,1,'2026-05-04 20:55:00','2026-05-14 11:48:00','2026-05-31 13:27:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO visual_baselines(id,test_case_id,test_type,project_id,step_index,step_name,baseline_image_path,viewport_width,viewport_height,status,version,approved_by,approved_at,created_at,updated_at)VALUES(29,77,'web',13,3,'步骤4','/baselines/p13/s3.png',1920,1080,'active',2,1,'2026-04-08 08:28:00','2026-01-30 17:26:00','2026-05-31 16:56:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO visual_baselines(id,test_case_id,test_type,project_id,step_index,step_name,baseline_image_path,viewport_width,viewport_height,status,version,approved_by,approved_at,created_at,updated_at)VALUES(30,46,'web',13,4,'步骤5','/baselines/p13/s4.png',1920,1080,'active',2,1,'2026-03-31 16:30:00','2026-04-12 09:42:00','2026-05-30 04:40:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO visual_baselines(id,test_case_id,test_type,project_id,step_index,step_name,baseline_image_path,viewport_width,viewport_height,status,version,approved_by,approved_at,created_at,updated_at)VALUES(31,24,'web',14,0,'步骤1','/baselines/p14/s0.png',1920,1080,'active',1,1,'2026-04-05 11:41:00','2026-02-16 23:07:00','2026-05-31 23:14:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO visual_baselines(id,test_case_id,test_type,project_id,step_index,step_name,baseline_image_path,viewport_width,viewport_height,status,version,approved_by,approved_at,created_at,updated_at)VALUES(32,29,'web',14,1,'步骤2','/baselines/p14/s1.png',1920,1080,'active',4,1,'2026-03-28 08:54:00','2026-01-20 15:05:00','2026-06-01 22:33:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO visual_baselines(id,test_case_id,test_type,project_id,step_index,step_name,baseline_image_path,viewport_width,viewport_height,status,version,approved_by,approved_at,created_at,updated_at)VALUES(33,88,'web',14,2,'步骤3','/baselines/p14/s2.png',1920,1080,'active',4,1,'2026-05-08 00:43:00','2026-02-23 18:55:00','2026-05-29 19:13:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO visual_baselines(id,test_case_id,test_type,project_id,step_index,step_name,baseline_image_path,viewport_width,viewport_height,status,version,approved_by,approved_at,created_at,updated_at)VALUES(34,49,'web',14,3,'步骤4','/baselines/p14/s3.png',1920,1080,'active',2,1,'2026-03-17 21:23:00','2026-05-16 00:46:00','2026-05-31 21:52:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO visual_baselines(id,test_case_id,test_type,project_id,step_index,step_name,baseline_image_path,viewport_width,viewport_height,status,version,approved_by,approved_at,created_at,updated_at)VALUES(35,49,'web',15,0,'步骤1','/baselines/p15/s0.png',1920,1080,'active',4,1,'2026-04-28 23:57:00','2025-12-26 15:24:00','2026-06-01 11:58:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO visual_baselines(id,test_case_id,test_type,project_id,step_index,step_name,baseline_image_path,viewport_width,viewport_height,status,version,approved_by,approved_at,created_at,updated_at)VALUES(36,15,'web',15,1,'步骤2','/baselines/p15/s1.png',1920,1080,'active',1,1,'2026-03-24 14:25:00','2026-03-05 18:46:00','2026-06-01 16:03:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO visual_baselines(id,test_case_id,test_type,project_id,step_index,step_name,baseline_image_path,viewport_width,viewport_height,status,version,approved_by,approved_at,created_at,updated_at)VALUES(37,30,'web',15,2,'步骤3','/baselines/p15/s2.png',1920,1080,'active',3,1,'2026-05-12 06:15:00','2026-05-10 16:22:00','2026-05-29 12:27:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO visual_baselines(id,test_case_id,test_type,project_id,step_index,step_name,baseline_image_path,viewport_width,viewport_height,status,version,approved_by,approved_at,created_at,updated_at)VALUES(38,38,'web',15,3,'步骤4','/baselines/p15/s3.png',1920,1080,'active',3,1,'2026-05-10 13:42:00','2026-02-22 01:13:00','2026-05-30 14:12:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO visual_baselines(id,test_case_id,test_type,project_id,step_index,step_name,baseline_image_path,viewport_width,viewport_height,status,version,approved_by,approved_at,created_at,updated_at)VALUES(39,75,'web',16,0,'步骤1','/baselines/p16/s0.png',1920,1080,'active',3,1,'2026-04-06 04:25:00','2026-02-26 18:39:00','2026-05-30 17:52:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO visual_baselines(id,test_case_id,test_type,project_id,step_index,step_name,baseline_image_path,viewport_width,viewport_height,status,version,approved_by,approved_at,created_at,updated_at)VALUES(40,67,'web',16,1,'步骤2','/baselines/p16/s1.png',1920,1080,'active',1,1,'2026-03-18 08:49:00','2026-04-26 07:32:00','2026-05-29 10:26:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO visual_baselines(id,test_case_id,test_type,project_id,step_index,step_name,baseline_image_path,viewport_width,viewport_height,status,version,approved_by,approved_at,created_at,updated_at)VALUES(41,78,'web',16,2,'步骤3','/baselines/p16/s2.png',1920,1080,'active',1,1,'2026-05-15 00:27:00','2026-01-14 03:20:00','2026-05-30 07:31:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO visual_baselines(id,test_case_id,test_type,project_id,step_index,step_name,baseline_image_path,viewport_width,viewport_height,status,version,approved_by,approved_at,created_at,updated_at)VALUES(42,2,'web',16,3,'步骤4','/baselines/p16/s3.png',1920,1080,'active',3,1,'2026-03-18 17:41:00','2026-03-25 23:09:00','2026-06-02 01:10:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO visual_baselines(id,test_case_id,test_type,project_id,step_index,step_name,baseline_image_path,viewport_width,viewport_height,status,version,approved_by,approved_at,created_at,updated_at)VALUES(43,27,'web',16,4,'步骤5','/baselines/p16/s4.png',1920,1080,'active',4,1,'2026-03-30 04:27:00','2026-02-20 17:54:00','2026-06-02 04:14:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO visual_diffs(test_run_id,baseline_id,test_case_id,test_type,step_index,step_name,current_image_path,diff_image_path,diff_percentage,diff_pixel_count,total_pixel_count,similarity_score,viewport_width,viewport_height,threshold,status,created_at,updated_at)VALUES(12,14,68,'web',4,'页面截图','/runs/cur.png','/runs/diff.png',3.26,5698,2073600,0.967,1920,1080,5.0,'visual_pass','2026-02-24 20:06:00','2026-05-31 06:11:00');

INSERT INTO visual_diffs(test_run_id,baseline_id,test_case_id,test_type,step_index,step_name,current_image_path,diff_image_path,diff_percentage,diff_pixel_count,total_pixel_count,similarity_score,viewport_width,viewport_height,threshold,status,created_at,updated_at)VALUES(67,40,63,'web',4,'页面截图','/runs/cur.png','/runs/diff.png',1.23,1407,2073600,0.988,1920,1080,5.0,'visual_pass','2026-04-26 23:24:00','2026-06-02 09:13:00');

INSERT INTO visual_diffs(test_run_id,baseline_id,test_case_id,test_type,step_index,step_name,current_image_path,diff_image_path,diff_percentage,diff_pixel_count,total_pixel_count,similarity_score,viewport_width,viewport_height,threshold,status,created_at,updated_at)VALUES(218,7,57,'web',3,'页面截图','/runs/cur.png','/runs/diff.png',11.92,9555,2073600,0.881,1920,1080,5.0,'visual_fail','2026-05-25 22:40:00','2026-06-01 16:05:00');

INSERT INTO visual_diffs(test_run_id,baseline_id,test_case_id,test_type,step_index,step_name,current_image_path,diff_image_path,diff_percentage,diff_pixel_count,total_pixel_count,similarity_score,viewport_width,viewport_height,threshold,status,created_at,updated_at)VALUES(154,14,29,'web',2,'页面截图','/runs/cur.png','/runs/diff.png',6.38,1565,2073600,0.936,1920,1080,5.0,'approved','2026-03-12 12:40:00','2026-05-30 17:26:00');

INSERT INTO visual_diffs(test_run_id,baseline_id,test_case_id,test_type,step_index,step_name,current_image_path,diff_image_path,diff_percentage,diff_pixel_count,total_pixel_count,similarity_score,viewport_width,viewport_height,threshold,status,created_at,updated_at)VALUES(196,1,99,'web',2,'页面截图','/runs/cur.png','/runs/diff.png',11.26,3297,2073600,0.887,1920,1080,5.0,'approved','2026-05-15 12:35:00','2026-06-01 10:13:00');

INSERT INTO visual_diffs(test_run_id,baseline_id,test_case_id,test_type,step_index,step_name,current_image_path,diff_image_path,diff_percentage,diff_pixel_count,total_pixel_count,similarity_score,viewport_width,viewport_height,threshold,status,created_at,updated_at)VALUES(152,16,75,'web',0,'页面截图','/runs/cur.png','/runs/diff.png',1.82,270,2073600,0.982,1920,1080,5.0,'visual_pass','2026-04-30 16:52:00','2026-05-30 18:41:00');

INSERT INTO visual_diffs(test_run_id,baseline_id,test_case_id,test_type,step_index,step_name,current_image_path,diff_image_path,diff_percentage,diff_pixel_count,total_pixel_count,similarity_score,viewport_width,viewport_height,threshold,status,created_at,updated_at)VALUES(85,23,16,'web',1,'页面截图','/runs/cur.png','/runs/diff.png',2.02,7089,2073600,0.98,1920,1080,5.0,'visual_pass','2026-05-26 15:57:00','2026-05-30 17:40:00');

INSERT INTO visual_diffs(test_run_id,baseline_id,test_case_id,test_type,step_index,step_name,current_image_path,diff_image_path,diff_percentage,diff_pixel_count,total_pixel_count,similarity_score,viewport_width,viewport_height,threshold,status,created_at,updated_at)VALUES(133,8,6,'web',2,'页面截图','/runs/cur.png','/runs/diff.png',12.4,5469,2073600,0.876,1920,1080,5.0,'visual_fail','2026-05-25 05:41:00','2026-06-01 11:31:00');

INSERT INTO visual_diffs(test_run_id,baseline_id,test_case_id,test_type,step_index,step_name,current_image_path,diff_image_path,diff_percentage,diff_pixel_count,total_pixel_count,similarity_score,viewport_width,viewport_height,threshold,status,created_at,updated_at)VALUES(22,22,90,'web',4,'页面截图','/runs/cur.png','/runs/diff.png',3.1,8229,2073600,0.969,1920,1080,5.0,'visual_pass','2026-05-05 21:12:00','2026-06-01 05:02:00');

INSERT INTO visual_diffs(test_run_id,baseline_id,test_case_id,test_type,step_index,step_name,current_image_path,diff_image_path,diff_percentage,diff_pixel_count,total_pixel_count,similarity_score,viewport_width,viewport_height,threshold,status,created_at,updated_at)VALUES(181,23,66,'web',4,'页面截图','/runs/cur.png','/runs/diff.png',6.6,6669,2073600,0.934,1920,1080,5.0,'visual_fail','2026-03-21 02:47:00','2026-06-01 02:09:00');

INSERT INTO visual_diffs(test_run_id,baseline_id,test_case_id,test_type,step_index,step_name,current_image_path,diff_image_path,diff_percentage,diff_pixel_count,total_pixel_count,similarity_score,viewport_width,viewport_height,threshold,status,created_at,updated_at)VALUES(165,22,70,'web',2,'页面截图','/runs/cur.png','/runs/diff.png',9.28,7148,2073600,0.907,1920,1080,5.0,'visual_fail','2026-05-20 22:20:00','2026-05-31 19:18:00');

INSERT INTO visual_diffs(test_run_id,baseline_id,test_case_id,test_type,step_index,step_name,current_image_path,diff_image_path,diff_percentage,diff_pixel_count,total_pixel_count,similarity_score,viewport_width,viewport_height,threshold,status,created_at,updated_at)VALUES(171,22,50,'web',3,'页面截图','/runs/cur.png','/runs/diff.png',3.69,4022,2073600,0.963,1920,1080,5.0,'visual_pass','2026-03-18 18:24:00','2026-06-01 22:38:00');

INSERT INTO visual_diffs(test_run_id,baseline_id,test_case_id,test_type,step_index,step_name,current_image_path,diff_image_path,diff_percentage,diff_pixel_count,total_pixel_count,similarity_score,viewport_width,viewport_height,threshold,status,created_at,updated_at)VALUES(30,25,38,'web',1,'页面截图','/runs/cur.png','/runs/diff.png',11.85,6537,2073600,0.881,1920,1080,5.0,'visual_fail','2026-03-06 14:58:00','2026-05-31 05:07:00');

INSERT INTO visual_diffs(test_run_id,baseline_id,test_case_id,test_type,step_index,step_name,current_image_path,diff_image_path,diff_percentage,diff_pixel_count,total_pixel_count,similarity_score,viewport_width,viewport_height,threshold,status,created_at,updated_at)VALUES(125,32,24,'web',3,'页面截图','/runs/cur.png','/runs/diff.png',7.62,561,2073600,0.924,1920,1080,5.0,'visual_fail','2026-02-12 04:26:00','2026-05-30 20:11:00');

INSERT INTO visual_diffs(test_run_id,baseline_id,test_case_id,test_type,step_index,step_name,current_image_path,diff_image_path,diff_percentage,diff_pixel_count,total_pixel_count,similarity_score,viewport_width,viewport_height,threshold,status,created_at,updated_at)VALUES(6,22,32,'web',2,'页面截图','/runs/cur.png','/runs/diff.png',9.75,3001,2073600,0.902,1920,1080,5.0,'approved','2026-03-27 07:36:00','2026-06-01 01:56:00');

INSERT INTO visual_diffs(test_run_id,baseline_id,test_case_id,test_type,step_index,step_name,current_image_path,diff_image_path,diff_percentage,diff_pixel_count,total_pixel_count,similarity_score,viewport_width,viewport_height,threshold,status,created_at,updated_at)VALUES(24,3,14,'web',4,'页面截图','/runs/cur.png','/runs/diff.png',12.26,7666,2073600,0.877,1920,1080,5.0,'approved','2026-04-20 13:03:00','2026-06-01 23:26:00');

INSERT INTO visual_diffs(test_run_id,baseline_id,test_case_id,test_type,step_index,step_name,current_image_path,diff_image_path,diff_percentage,diff_pixel_count,total_pixel_count,similarity_score,viewport_width,viewport_height,threshold,status,created_at,updated_at)VALUES(109,17,6,'web',2,'页面截图','/runs/cur.png','/runs/diff.png',13.08,2138,2073600,0.869,1920,1080,5.0,'approved','2026-05-28 03:18:00','2026-05-30 17:00:00');

INSERT INTO visual_diffs(test_run_id,baseline_id,test_case_id,test_type,step_index,step_name,current_image_path,diff_image_path,diff_percentage,diff_pixel_count,total_pixel_count,similarity_score,viewport_width,viewport_height,threshold,status,created_at,updated_at)VALUES(59,1,34,'web',1,'页面截图','/runs/cur.png','/runs/diff.png',2.03,8072,2073600,0.98,1920,1080,5.0,'visual_pass','2026-04-09 03:33:00','2026-06-01 17:05:00');

INSERT INTO visual_diffs(test_run_id,baseline_id,test_case_id,test_type,step_index,step_name,current_image_path,diff_image_path,diff_percentage,diff_pixel_count,total_pixel_count,similarity_score,viewport_width,viewport_height,threshold,status,created_at,updated_at)VALUES(167,17,87,'web',2,'页面截图','/runs/cur.png','/runs/diff.png',1.54,7526,2073600,0.985,1920,1080,5.0,'visual_pass','2026-05-17 17:12:00','2026-05-31 02:23:00');

INSERT INTO visual_diffs(test_run_id,baseline_id,test_case_id,test_type,step_index,step_name,current_image_path,diff_image_path,diff_percentage,diff_pixel_count,total_pixel_count,similarity_score,viewport_width,viewport_height,threshold,status,created_at,updated_at)VALUES(59,2,74,'web',3,'页面截图','/runs/cur.png','/runs/diff.png',4.75,9522,2073600,0.953,1920,1080,5.0,'visual_pass','2026-02-19 08:34:00','2026-05-31 21:44:00');

INSERT INTO audit_logs(user_id,organization_id,action,resource_type,resource_id,changes,ip_address,user_agent,created_at)VALUES(1,5,'create','project',12,'{}','172.16.0.10','Mozilla/5.0 Mac Safari/605','2025-09-13 19:12:00');

INSERT INTO audit_logs(user_id,organization_id,action,resource_type,resource_id,changes,ip_address,user_agent,created_at)VALUES(7,3,'create','test_run',49,'{}','192.168.1.100','Mozilla/5.0 iPhone Mobile','2026-01-30 23:26:00');

INSERT INTO audit_logs(user_id,organization_id,action,resource_type,resource_id,changes,ip_address,user_agent,created_at)VALUES(10,1,'create','project',32,'{}','10.0.0.51','Mozilla/5.0 Mac Safari/605','2026-02-21 09:19:00');

INSERT INTO audit_logs(user_id,organization_id,action,resource_type,resource_id,changes,ip_address,user_agent,created_at)VALUES(9,1,'export','report',36,'{}','192.168.1.100','Mozilla/5.0 Mac Safari/605','2026-01-13 10:11:00');

INSERT INTO audit_logs(user_id,organization_id,action,resource_type,resource_id,changes,ip_address,user_agent,created_at)VALUES(1,2,'update','project',20,'{}','172.16.0.10','Mozilla/5.0 iPhone Mobile','2025-09-07 07:28:00');

INSERT INTO audit_logs(user_id,organization_id,action,resource_type,resource_id,changes,ip_address,user_agent,created_at)VALUES(10,4,'update','project',36,'{}','10.0.0.51','Mozilla/5.0 iPhone Mobile','2025-11-29 17:46:00');

INSERT INTO audit_logs(user_id,organization_id,action,resource_type,resource_id,changes,ip_address,user_agent,created_at)VALUES(6,3,'update','project',26,'{}','10.0.0.51','Mozilla/5.0 Mac Safari/605','2026-05-25 01:54:00');

INSERT INTO audit_logs(user_id,organization_id,action,resource_type,resource_id,changes,ip_address,user_agent,created_at)VALUES(6,1,'login','user',39,'{}','172.16.0.10','Mozilla/5.0 Windows Chrome/120','2025-12-05 03:28:00');

INSERT INTO audit_logs(user_id,organization_id,action,resource_type,resource_id,changes,ip_address,user_agent,created_at)VALUES(9,5,'login','user',12,'{}','192.168.1.101','Mozilla/5.0 Mac Safari/605','2026-03-24 22:44:00');

INSERT INTO audit_logs(user_id,organization_id,action,resource_type,resource_id,changes,ip_address,user_agent,created_at)VALUES(5,1,'login','user',17,'{}','223.5.5.5','Mozilla/5.0 Windows Chrome/120','2026-02-02 07:21:00');

INSERT INTO audit_logs(user_id,organization_id,action,resource_type,resource_id,changes,ip_address,user_agent,created_at)VALUES(1,4,'create','test_run',29,'{}','192.168.1.101','Mozilla/5.0 Windows Chrome/120','2026-01-15 01:56:00');

INSERT INTO audit_logs(user_id,organization_id,action,resource_type,resource_id,changes,ip_address,user_agent,created_at)VALUES(1,4,'login','user',46,'{}','223.5.5.5','Mozilla/5.0 iPhone Mobile','2026-01-13 06:24:00');

INSERT INTO audit_logs(user_id,organization_id,action,resource_type,resource_id,changes,ip_address,user_agent,created_at)VALUES(6,3,'create','project',18,'{}','192.168.1.101','Mozilla/5.0 iPhone Mobile','2026-04-24 08:21:00');

INSERT INTO audit_logs(user_id,organization_id,action,resource_type,resource_id,changes,ip_address,user_agent,created_at)VALUES(10,2,'create','test_case',7,'{}','192.168.1.101','Mozilla/5.0 Mac Safari/605','2025-08-26 19:59:00');

INSERT INTO audit_logs(user_id,organization_id,action,resource_type,resource_id,changes,ip_address,user_agent,created_at)VALUES(10,4,'create','project',48,'{}','10.0.0.50','Mozilla/5.0 iPhone Mobile','2025-11-05 03:49:00');

INSERT INTO audit_logs(user_id,organization_id,action,resource_type,resource_id,changes,ip_address,user_agent,created_at)VALUES(5,4,'create','test_run',6,'{}','10.0.0.50','Mozilla/5.0 Windows Chrome/120','2026-02-27 01:00:00');

INSERT INTO audit_logs(user_id,organization_id,action,resource_type,resource_id,changes,ip_address,user_agent,created_at)VALUES(7,4,'update','project',12,'{}','192.168.1.100','Mozilla/5.0 Windows Chrome/120','2025-08-31 14:57:00');

INSERT INTO audit_logs(user_id,organization_id,action,resource_type,resource_id,changes,ip_address,user_agent,created_at)VALUES(1,4,'update','project',20,'{}','172.16.0.10','Mozilla/5.0 Mac Safari/605','2026-04-11 11:36:00');

INSERT INTO audit_logs(user_id,organization_id,action,resource_type,resource_id,changes,ip_address,user_agent,created_at)VALUES(6,1,'login','user',31,'{}','192.168.1.101','Mozilla/5.0 iPhone Mobile','2025-11-08 19:16:00');

INSERT INTO audit_logs(user_id,organization_id,action,resource_type,resource_id,changes,ip_address,user_agent,created_at)VALUES(5,1,'login','user',10,'{}','192.168.1.100','Mozilla/5.0 iPhone Mobile','2025-12-12 02:35:00');

INSERT INTO audit_logs(user_id,organization_id,action,resource_type,resource_id,changes,ip_address,user_agent,created_at)VALUES(9,5,'create','project',5,'{}','10.0.0.50','Mozilla/5.0 Windows Chrome/120','2025-11-03 16:23:00');

INSERT INTO audit_logs(user_id,organization_id,action,resource_type,resource_id,changes,ip_address,user_agent,created_at)VALUES(1,4,'login','user',22,'{}','10.0.0.51','Mozilla/5.0 iPhone Mobile','2025-12-23 09:57:00');

INSERT INTO audit_logs(user_id,organization_id,action,resource_type,resource_id,changes,ip_address,user_agent,created_at)VALUES(2,2,'create','organization',16,'{}','10.0.0.50','Mozilla/5.0 iPhone Mobile','2026-05-26 09:09:00');

INSERT INTO audit_logs(user_id,organization_id,action,resource_type,resource_id,changes,ip_address,user_agent,created_at)VALUES(10,4,'update','project',40,'{}','192.168.1.100','Mozilla/5.0 Windows Chrome/120','2026-05-14 13:32:00');

INSERT INTO audit_logs(user_id,organization_id,action,resource_type,resource_id,changes,ip_address,user_agent,created_at)VALUES(5,1,'create','project',6,'{}','192.168.1.101','Mozilla/5.0 iPhone Mobile','2025-11-18 15:58:00');

INSERT INTO audit_logs(user_id,organization_id,action,resource_type,resource_id,changes,ip_address,user_agent,created_at)VALUES(10,4,'logout','user',42,'{}','10.0.0.51','Mozilla/5.0 Windows Chrome/120','2026-02-26 06:59:00');

INSERT INTO audit_logs(user_id,organization_id,action,resource_type,resource_id,changes,ip_address,user_agent,created_at)VALUES(7,3,'create','test_run',46,'{}','223.5.5.5','Mozilla/5.0 Mac Safari/605','2026-04-04 18:53:00');

INSERT INTO audit_logs(user_id,organization_id,action,resource_type,resource_id,changes,ip_address,user_agent,created_at)VALUES(5,4,'export','report',5,'{}','192.168.1.100','Mozilla/5.0 Mac Safari/605','2026-01-21 00:45:00');

INSERT INTO audit_logs(user_id,organization_id,action,resource_type,resource_id,changes,ip_address,user_agent,created_at)VALUES(9,2,'login','user',10,'{}','10.0.0.50','Mozilla/5.0 Mac Safari/605','2026-03-26 04:37:00');

INSERT INTO audit_logs(user_id,organization_id,action,resource_type,resource_id,changes,ip_address,user_agent,created_at)VALUES(5,4,'logout','user',42,'{}','192.168.1.100','Mozilla/5.0 Windows Chrome/120','2025-12-08 04:47:00');

INSERT INTO audit_logs(user_id,organization_id,action,resource_type,resource_id,changes,ip_address,user_agent,created_at)VALUES(7,1,'logout','user',10,'{}','172.16.0.10','Mozilla/5.0 Mac Safari/605','2025-12-26 10:08:00');

INSERT INTO audit_logs(user_id,organization_id,action,resource_type,resource_id,changes,ip_address,user_agent,created_at)VALUES(10,4,'create','organization',12,'{}','172.16.0.10','Mozilla/5.0 Windows Chrome/120','2026-02-14 12:49:00');

INSERT INTO audit_logs(user_id,organization_id,action,resource_type,resource_id,changes,ip_address,user_agent,created_at)VALUES(9,1,'create','test_run',21,'{}','192.168.1.101','Mozilla/5.0 Windows Chrome/120','2025-10-03 20:55:00');

INSERT INTO audit_logs(user_id,organization_id,action,resource_type,resource_id,changes,ip_address,user_agent,created_at)VALUES(10,5,'create','test_case',47,'{}','192.168.1.100','Mozilla/5.0 iPhone Mobile','2026-03-25 01:38:00');

INSERT INTO audit_logs(user_id,organization_id,action,resource_type,resource_id,changes,ip_address,user_agent,created_at)VALUES(8,1,'export','report',23,'{}','10.0.0.51','Mozilla/5.0 Windows Chrome/120','2026-03-26 06:54:00');

INSERT INTO audit_logs(user_id,organization_id,action,resource_type,resource_id,changes,ip_address,user_agent,created_at)VALUES(2,5,'create','test_run',35,'{}','192.168.1.100','Mozilla/5.0 Windows Chrome/120','2025-10-23 16:04:00');

INSERT INTO audit_logs(user_id,organization_id,action,resource_type,resource_id,changes,ip_address,user_agent,created_at)VALUES(9,5,'create','test_case',47,'{}','172.16.0.10','Mozilla/5.0 Mac Safari/605','2026-01-21 18:25:00');

INSERT INTO audit_logs(user_id,organization_id,action,resource_type,resource_id,changes,ip_address,user_agent,created_at)VALUES(9,4,'export','report',44,'{}','192.168.1.101','Mozilla/5.0 Windows Chrome/120','2025-10-06 21:57:00');

INSERT INTO audit_logs(user_id,organization_id,action,resource_type,resource_id,changes,ip_address,user_agent,created_at)VALUES(1,3,'export','report',34,'{}','10.0.0.50','Mozilla/5.0 Mac Safari/605','2026-01-20 09:28:00');

INSERT INTO audit_logs(user_id,organization_id,action,resource_type,resource_id,changes,ip_address,user_agent,created_at)VALUES(6,5,'create','organization',43,'{}','192.168.1.100','Mozilla/5.0 iPhone Mobile','2026-04-05 15:58:00');

INSERT INTO audit_logs(user_id,organization_id,action,resource_type,resource_id,changes,ip_address,user_agent,created_at)VALUES(10,5,'create','test_case',40,'{}','192.168.1.101','Mozilla/5.0 Windows Chrome/120','2025-10-21 00:58:00');

INSERT INTO audit_logs(user_id,organization_id,action,resource_type,resource_id,changes,ip_address,user_agent,created_at)VALUES(1,5,'create','environment',37,'{}','192.168.1.101','Mozilla/5.0 Mac Safari/605','2026-03-28 03:10:00');

INSERT INTO audit_logs(user_id,organization_id,action,resource_type,resource_id,changes,ip_address,user_agent,created_at)VALUES(8,5,'update','project',18,'{}','10.0.0.50','Mozilla/5.0 iPhone Mobile','2025-10-21 01:32:00');

INSERT INTO audit_logs(user_id,organization_id,action,resource_type,resource_id,changes,ip_address,user_agent,created_at)VALUES(1,1,'export','report',11,'{}','192.168.1.101','Mozilla/5.0 iPhone Mobile','2025-09-03 20:40:00');

INSERT INTO audit_logs(user_id,organization_id,action,resource_type,resource_id,changes,ip_address,user_agent,created_at)VALUES(7,2,'create','environment',12,'{}','223.5.5.5','Mozilla/5.0 Windows Chrome/120','2026-03-07 07:50:00');

INSERT INTO audit_logs(user_id,organization_id,action,resource_type,resource_id,changes,ip_address,user_agent,created_at)VALUES(6,2,'create','organization',44,'{}','192.168.1.100','Mozilla/5.0 Mac Safari/605','2025-12-15 09:04:00');

INSERT INTO audit_logs(user_id,organization_id,action,resource_type,resource_id,changes,ip_address,user_agent,created_at)VALUES(6,1,'update','project',1,'{}','192.168.1.100','Mozilla/5.0 Windows Chrome/120','2025-08-24 17:36:00');

INSERT INTO audit_logs(user_id,organization_id,action,resource_type,resource_id,changes,ip_address,user_agent,created_at)VALUES(6,4,'create','test_case',48,'{}','10.0.0.51','Mozilla/5.0 Windows Chrome/120','2026-04-05 15:00:00');

INSERT INTO audit_logs(user_id,organization_id,action,resource_type,resource_id,changes,ip_address,user_agent,created_at)VALUES(1,5,'export','report',34,'{}','172.16.0.10','Mozilla/5.0 Windows Chrome/120','2026-03-31 01:53:00');

INSERT INTO audit_logs(user_id,organization_id,action,resource_type,resource_id,changes,ip_address,user_agent,created_at)VALUES(9,5,'login','user',2,'{}','192.168.1.100','Mozilla/5.0 Mac Safari/605','2025-08-14 10:20:00');

INSERT INTO audit_logs(user_id,organization_id,action,resource_type,resource_id,changes,ip_address,user_agent,created_at)VALUES(5,4,'update','project',9,'{}','192.168.1.101','Mozilla/5.0 Mac Safari/605','2025-08-07 12:26:00');

INSERT INTO audit_logs(user_id,organization_id,action,resource_type,resource_id,changes,ip_address,user_agent,created_at)VALUES(10,1,'login','user',25,'{}','172.16.0.10','Mozilla/5.0 iPhone Mobile','2025-12-11 00:26:00');

INSERT INTO audit_logs(user_id,organization_id,action,resource_type,resource_id,changes,ip_address,user_agent,created_at)VALUES(2,4,'export','report',28,'{}','10.0.0.50','Mozilla/5.0 Mac Safari/605','2026-01-27 08:57:00');

INSERT INTO audit_logs(user_id,organization_id,action,resource_type,resource_id,changes,ip_address,user_agent,created_at)VALUES(1,2,'export','report',18,'{}','192.168.1.101','Mozilla/5.0 Mac Safari/605','2026-04-02 06:14:00');

INSERT INTO audit_logs(user_id,organization_id,action,resource_type,resource_id,changes,ip_address,user_agent,created_at)VALUES(6,1,'create','organization',6,'{}','172.16.0.10','Mozilla/5.0 Windows Chrome/120','2025-12-21 07:18:00');

INSERT INTO audit_logs(user_id,organization_id,action,resource_type,resource_id,changes,ip_address,user_agent,created_at)VALUES(8,5,'create','test_case',22,'{}','192.168.1.101','Mozilla/5.0 iPhone Mobile','2025-12-25 05:59:00');

INSERT INTO audit_logs(user_id,organization_id,action,resource_type,resource_id,changes,ip_address,user_agent,created_at)VALUES(6,1,'create','test_case',43,'{}','192.168.1.100','Mozilla/5.0 Mac Safari/605','2026-02-16 23:12:00');

INSERT INTO audit_logs(user_id,organization_id,action,resource_type,resource_id,changes,ip_address,user_agent,created_at)VALUES(6,4,'create','test_case',27,'{}','192.168.1.100','Mozilla/5.0 Mac Safari/605','2025-12-18 21:24:00');

INSERT INTO audit_logs(user_id,organization_id,action,resource_type,resource_id,changes,ip_address,user_agent,created_at)VALUES(7,3,'create','test_case',38,'{}','10.0.0.51','Mozilla/5.0 Mac Safari/605','2025-10-18 05:15:00');

INSERT INTO audit_logs(user_id,organization_id,action,resource_type,resource_id,changes,ip_address,user_agent,created_at)VALUES(1,5,'logout','user',4,'{}','192.168.1.101','Mozilla/5.0 Mac Safari/605','2026-05-24 05:15:00');

INSERT INTO audit_logs(user_id,organization_id,action,resource_type,resource_id,changes,ip_address,user_agent,created_at)VALUES(2,2,'export','report',10,'{}','223.5.5.5','Mozilla/5.0 Windows Chrome/120','2025-09-11 19:22:00');

INSERT INTO audit_logs(user_id,organization_id,action,resource_type,resource_id,changes,ip_address,user_agent,created_at)VALUES(7,4,'login','user',10,'{}','192.168.1.101','Mozilla/5.0 Windows Chrome/120','2025-09-02 22:28:00');

INSERT INTO audit_logs(user_id,organization_id,action,resource_type,resource_id,changes,ip_address,user_agent,created_at)VALUES(2,3,'create','organization',17,'{}','192.168.1.101','Mozilla/5.0 Mac Safari/605','2026-02-04 22:20:00');

INSERT INTO audit_logs(user_id,organization_id,action,resource_type,resource_id,changes,ip_address,user_agent,created_at)VALUES(6,2,'create','environment',20,'{}','192.168.1.101','Mozilla/5.0 Mac Safari/605','2025-10-12 10:00:00');

INSERT INTO audit_logs(user_id,organization_id,action,resource_type,resource_id,changes,ip_address,user_agent,created_at)VALUES(7,5,'logout','user',11,'{}','192.168.1.100','Mozilla/5.0 iPhone Mobile','2026-03-21 16:16:00');

INSERT INTO audit_logs(user_id,organization_id,action,resource_type,resource_id,changes,ip_address,user_agent,created_at)VALUES(8,1,'logout','user',36,'{}','223.5.5.5','Mozilla/5.0 Mac Safari/605','2026-04-26 13:49:00');

INSERT INTO audit_logs(user_id,organization_id,action,resource_type,resource_id,changes,ip_address,user_agent,created_at)VALUES(8,1,'create','test_run',37,'{}','10.0.0.50','Mozilla/5.0 iPhone Mobile','2025-11-10 06:04:00');

INSERT INTO audit_logs(user_id,organization_id,action,resource_type,resource_id,changes,ip_address,user_agent,created_at)VALUES(1,5,'login','user',30,'{}','192.168.1.101','Mozilla/5.0 Windows Chrome/120','2026-05-04 01:33:00');

INSERT INTO audit_logs(user_id,organization_id,action,resource_type,resource_id,changes,ip_address,user_agent,created_at)VALUES(9,1,'login','user',4,'{}','192.168.1.101','Mozilla/5.0 iPhone Mobile','2026-01-27 17:51:00');

INSERT INTO audit_logs(user_id,organization_id,action,resource_type,resource_id,changes,ip_address,user_agent,created_at)VALUES(10,1,'logout','user',2,'{}','223.5.5.5','Mozilla/5.0 iPhone Mobile','2026-03-04 03:03:00');

INSERT INTO audit_logs(user_id,organization_id,action,resource_type,resource_id,changes,ip_address,user_agent,created_at)VALUES(5,3,'create','environment',5,'{}','192.168.1.100','Mozilla/5.0 Windows Chrome/120','2026-05-16 13:03:00');

INSERT INTO audit_logs(user_id,organization_id,action,resource_type,resource_id,changes,ip_address,user_agent,created_at)VALUES(7,3,'export','report',46,'{}','192.168.1.100','Mozilla/5.0 Mac Safari/605','2025-10-24 20:12:00');

INSERT INTO audit_logs(user_id,organization_id,action,resource_type,resource_id,changes,ip_address,user_agent,created_at)VALUES(8,3,'update','project',50,'{}','10.0.0.50','Mozilla/5.0 Mac Safari/605','2026-05-09 00:19:00');

INSERT INTO audit_logs(user_id,organization_id,action,resource_type,resource_id,changes,ip_address,user_agent,created_at)VALUES(5,4,'create','project',29,'{}','192.168.1.101','Mozilla/5.0 iPhone Mobile','2025-12-29 21:08:00');

INSERT INTO audit_logs(user_id,organization_id,action,resource_type,resource_id,changes,ip_address,user_agent,created_at)VALUES(1,1,'logout','user',40,'{}','10.0.0.50','Mozilla/5.0 Windows Chrome/120','2026-05-28 22:29:00');

INSERT INTO audit_logs(user_id,organization_id,action,resource_type,resource_id,changes,ip_address,user_agent,created_at)VALUES(6,2,'create','test_case',32,'{}','10.0.0.50','Mozilla/5.0 Windows Chrome/120','2025-12-03 16:34:00');

INSERT INTO audit_logs(user_id,organization_id,action,resource_type,resource_id,changes,ip_address,user_agent,created_at)VALUES(2,5,'create','organization',27,'{}','192.168.1.101','Mozilla/5.0 Windows Chrome/120','2025-12-21 06:13:00');

INSERT INTO audit_logs(user_id,organization_id,action,resource_type,resource_id,changes,ip_address,user_agent,created_at)VALUES(5,2,'create','organization',43,'{}','10.0.0.51','Mozilla/5.0 Mac Safari/605','2026-05-30 17:35:00');

INSERT INTO audit_logs(user_id,organization_id,action,resource_type,resource_id,changes,ip_address,user_agent,created_at)VALUES(9,4,'create','environment',23,'{}','192.168.1.101','Mozilla/5.0 Windows Chrome/120','2026-01-11 07:01:00');

INSERT INTO audit_logs(user_id,organization_id,action,resource_type,resource_id,changes,ip_address,user_agent,created_at)VALUES(10,4,'create','environment',35,'{}','172.16.0.10','Mozilla/5.0 Mac Safari/605','2026-01-01 18:31:00');

INSERT INTO audit_logs(user_id,organization_id,action,resource_type,resource_id,changes,ip_address,user_agent,created_at)VALUES(2,1,'create','project',38,'{}','223.5.5.5','Mozilla/5.0 Windows Chrome/120','2025-11-28 09:58:00');

INSERT INTO audit_logs(user_id,organization_id,action,resource_type,resource_id,changes,ip_address,user_agent,created_at)VALUES(9,3,'logout','user',33,'{}','172.16.0.10','Mozilla/5.0 iPhone Mobile','2025-09-27 00:51:00');

INSERT INTO audit_logs(user_id,organization_id,action,resource_type,resource_id,changes,ip_address,user_agent,created_at)VALUES(5,3,'update','project',21,'{}','192.168.1.101','Mozilla/5.0 Mac Safari/605','2026-05-05 00:14:00');

INSERT INTO audit_logs(user_id,organization_id,action,resource_type,resource_id,changes,ip_address,user_agent,created_at)VALUES(9,2,'create','environment',36,'{}','192.168.1.100','Mozilla/5.0 Windows Chrome/120','2026-04-17 23:10:00');

INSERT INTO audit_logs(user_id,organization_id,action,resource_type,resource_id,changes,ip_address,user_agent,created_at)VALUES(9,3,'create','test_case',39,'{}','192.168.1.101','Mozilla/5.0 Mac Safari/605','2026-01-20 15:10:00');

INSERT INTO audit_logs(user_id,organization_id,action,resource_type,resource_id,changes,ip_address,user_agent,created_at)VALUES(5,3,'login','user',26,'{}','10.0.0.50','Mozilla/5.0 iPhone Mobile','2026-04-17 06:54:00');

INSERT INTO audit_logs(user_id,organization_id,action,resource_type,resource_id,changes,ip_address,user_agent,created_at)VALUES(10,5,'update','project',35,'{}','192.168.1.100','Mozilla/5.0 iPhone Mobile','2026-03-17 19:45:00');

INSERT INTO audit_logs(user_id,organization_id,action,resource_type,resource_id,changes,ip_address,user_agent,created_at)VALUES(1,3,'create','environment',15,'{}','192.168.1.101','Mozilla/5.0 Mac Safari/605','2026-01-04 17:05:00');

INSERT INTO audit_logs(user_id,organization_id,action,resource_type,resource_id,changes,ip_address,user_agent,created_at)VALUES(5,5,'logout','user',34,'{}','10.0.0.50','Mozilla/5.0 iPhone Mobile','2025-10-29 16:59:00');

INSERT INTO audit_logs(user_id,organization_id,action,resource_type,resource_id,changes,ip_address,user_agent,created_at)VALUES(9,1,'create','environment',17,'{}','10.0.0.50','Mozilla/5.0 Windows Chrome/120','2026-04-11 08:49:00');

INSERT INTO audit_logs(user_id,organization_id,action,resource_type,resource_id,changes,ip_address,user_agent,created_at)VALUES(2,3,'create','project',24,'{}','192.168.1.101','Mozilla/5.0 iPhone Mobile','2026-01-10 07:09:00');

INSERT INTO audit_logs(user_id,organization_id,action,resource_type,resource_id,changes,ip_address,user_agent,created_at)VALUES(5,1,'update','project',2,'{}','223.5.5.5','Mozilla/5.0 Mac Safari/605','2026-05-06 00:21:00');

INSERT INTO audit_logs(user_id,organization_id,action,resource_type,resource_id,changes,ip_address,user_agent,created_at)VALUES(9,4,'login','user',16,'{}','192.168.1.101','Mozilla/5.0 Windows Chrome/120','2025-09-15 21:57:00');

INSERT INTO audit_logs(user_id,organization_id,action,resource_type,resource_id,changes,ip_address,user_agent,created_at)VALUES(1,1,'update','project',11,'{}','223.5.5.5','Mozilla/5.0 Windows Chrome/120','2026-04-08 14:32:00');

INSERT INTO audit_logs(user_id,organization_id,action,resource_type,resource_id,changes,ip_address,user_agent,created_at)VALUES(1,3,'logout','user',6,'{}','192.168.1.100','Mozilla/5.0 Windows Chrome/120','2026-02-14 00:02:00');

INSERT INTO audit_logs(user_id,organization_id,action,resource_type,resource_id,changes,ip_address,user_agent,created_at)VALUES(10,1,'logout','user',16,'{}','223.5.5.5','Mozilla/5.0 Mac Safari/605','2026-04-11 15:08:00');

INSERT INTO audit_logs(user_id,organization_id,action,resource_type,resource_id,changes,ip_address,user_agent,created_at)VALUES(10,1,'export','report',27,'{}','223.5.5.5','Mozilla/5.0 Windows Chrome/120','2025-11-15 05:12:00');

INSERT INTO audit_logs(user_id,organization_id,action,resource_type,resource_id,changes,ip_address,user_agent,created_at)VALUES(8,5,'login','user',47,'{}','10.0.0.50','Mozilla/5.0 Windows Chrome/120','2025-08-07 13:42:00');

INSERT INTO audit_logs(user_id,organization_id,action,resource_type,resource_id,changes,ip_address,user_agent,created_at)VALUES(10,3,'export','report',22,'{}','192.168.1.100','Mozilla/5.0 iPhone Mobile','2026-04-01 07:47:00');

INSERT INTO audit_logs(user_id,organization_id,action,resource_type,resource_id,changes,ip_address,user_agent,created_at)VALUES(10,3,'create','test_run',15,'{}','172.16.0.10','Mozilla/5.0 Windows Chrome/120','2026-04-01 09:30:00');

INSERT INTO audit_logs(user_id,organization_id,action,resource_type,resource_id,changes,ip_address,user_agent,created_at)VALUES(5,4,'export','report',34,'{}','172.16.0.10','Mozilla/5.0 iPhone Mobile','2026-05-30 18:52:00');

INSERT INTO audit_logs(user_id,organization_id,action,resource_type,resource_id,changes,ip_address,user_agent,created_at)VALUES(10,2,'login','user',46,'{}','10.0.0.51','Mozilla/5.0 Windows Chrome/120','2025-11-01 06:33:00');

INSERT INTO audit_logs(user_id,organization_id,action,resource_type,resource_id,changes,ip_address,user_agent,created_at)VALUES(1,5,'export','report',45,'{}','192.168.1.100','Mozilla/5.0 iPhone Mobile','2025-10-04 05:52:00');

INSERT INTO audit_logs(user_id,organization_id,action,resource_type,resource_id,changes,ip_address,user_agent,created_at)VALUES(6,4,'create','environment',17,'{}','10.0.0.51','Mozilla/5.0 Windows Chrome/120','2025-08-31 03:29:00');

INSERT INTO audit_logs(user_id,organization_id,action,resource_type,resource_id,changes,ip_address,user_agent,created_at)VALUES(8,4,'update','project',3,'{}','10.0.0.51','Mozilla/5.0 iPhone Mobile','2026-04-08 09:49:00');

INSERT INTO audit_logs(user_id,organization_id,action,resource_type,resource_id,changes,ip_address,user_agent,created_at)VALUES(7,5,'export','report',1,'{}','10.0.0.50','Mozilla/5.0 Mac Safari/605','2025-10-05 17:58:00');

INSERT INTO audit_logs(user_id,organization_id,action,resource_type,resource_id,changes,ip_address,user_agent,created_at)VALUES(1,3,'create','project',42,'{}','223.5.5.5','Mozilla/5.0 Mac Safari/605','2026-02-22 05:47:00');

INSERT INTO audit_logs(user_id,organization_id,action,resource_type,resource_id,changes,ip_address,user_agent,created_at)VALUES(9,1,'create','project',11,'{}','10.0.0.51','Mozilla/5.0 iPhone Mobile','2026-05-12 21:22:00');

INSERT INTO audit_logs(user_id,organization_id,action,resource_type,resource_id,changes,ip_address,user_agent,created_at)VALUES(9,4,'export','report',23,'{}','10.0.0.50','Mozilla/5.0 Mac Safari/605','2025-10-03 09:36:00');

INSERT INTO audit_logs(user_id,organization_id,action,resource_type,resource_id,changes,ip_address,user_agent,created_at)VALUES(10,4,'create','test_run',5,'{}','172.16.0.10','Mozilla/5.0 iPhone Mobile','2026-04-02 02:24:00');

INSERT INTO audit_logs(user_id,organization_id,action,resource_type,resource_id,changes,ip_address,user_agent,created_at)VALUES(8,3,'create','project',6,'{}','192.168.1.100','Mozilla/5.0 iPhone Mobile','2026-04-02 20:03:00');

INSERT INTO audit_logs(user_id,organization_id,action,resource_type,resource_id,changes,ip_address,user_agent,created_at)VALUES(7,1,'create','project',25,'{}','192.168.1.100','Mozilla/5.0 Mac Safari/605','2026-05-28 03:48:00');

INSERT INTO audit_logs(user_id,organization_id,action,resource_type,resource_id,changes,ip_address,user_agent,created_at)VALUES(8,5,'login','user',42,'{}','10.0.0.50','Mozilla/5.0 Windows Chrome/120','2026-01-08 03:16:00');

INSERT INTO audit_logs(user_id,organization_id,action,resource_type,resource_id,changes,ip_address,user_agent,created_at)VALUES(2,5,'export','report',15,'{}','192.168.1.101','Mozilla/5.0 Mac Safari/605','2025-08-28 00:28:00');

INSERT INTO audit_logs(user_id,organization_id,action,resource_type,resource_id,changes,ip_address,user_agent,created_at)VALUES(2,1,'update','project',2,'{}','10.0.0.50','Mozilla/5.0 Windows Chrome/120','2025-10-26 14:09:00');

INSERT INTO audit_logs(user_id,organization_id,action,resource_type,resource_id,changes,ip_address,user_agent,created_at)VALUES(2,2,'login','user',21,'{}','192.168.1.100','Mozilla/5.0 Windows Chrome/120','2026-04-10 22:02:00');

INSERT INTO audit_logs(user_id,organization_id,action,resource_type,resource_id,changes,ip_address,user_agent,created_at)VALUES(2,3,'create','environment',31,'{}','223.5.5.5','Mozilla/5.0 iPhone Mobile','2025-11-14 11:42:00');

INSERT INTO audit_logs(user_id,organization_id,action,resource_type,resource_id,changes,ip_address,user_agent,created_at)VALUES(9,5,'update','project',15,'{}','10.0.0.50','Mozilla/5.0 Windows Chrome/120','2025-12-24 16:55:00');

INSERT INTO audit_logs(user_id,organization_id,action,resource_type,resource_id,changes,ip_address,user_agent,created_at)VALUES(2,1,'login','user',21,'{}','192.168.1.100','Mozilla/5.0 Mac Safari/605','2025-09-18 20:44:00');

INSERT INTO audit_logs(user_id,organization_id,action,resource_type,resource_id,changes,ip_address,user_agent,created_at)VALUES(5,5,'create','organization',33,'{}','10.0.0.51','Mozilla/5.0 Windows Chrome/120','2025-12-19 18:45:00');

INSERT INTO audit_logs(user_id,organization_id,action,resource_type,resource_id,changes,ip_address,user_agent,created_at)VALUES(8,1,'create','test_run',48,'{}','192.168.1.101','Mozilla/5.0 iPhone Mobile','2026-04-22 19:02:00');

INSERT INTO audit_logs(user_id,organization_id,action,resource_type,resource_id,changes,ip_address,user_agent,created_at)VALUES(10,2,'create','test_run',7,'{}','192.168.1.101','Mozilla/5.0 iPhone Mobile','2025-11-22 15:29:00');

INSERT INTO audit_logs(user_id,organization_id,action,resource_type,resource_id,changes,ip_address,user_agent,created_at)VALUES(2,3,'create','test_run',24,'{}','192.168.1.101','Mozilla/5.0 Mac Safari/605','2026-05-08 12:09:00');

INSERT INTO audit_logs(user_id,organization_id,action,resource_type,resource_id,changes,ip_address,user_agent,created_at)VALUES(10,4,'create','project',15,'{}','192.168.1.100','Mozilla/5.0 Windows Chrome/120','2026-01-01 00:33:00');

INSERT INTO audit_logs(user_id,organization_id,action,resource_type,resource_id,changes,ip_address,user_agent,created_at)VALUES(8,4,'create','test_case',28,'{}','10.0.0.51','Mozilla/5.0 Windows Chrome/120','2026-05-13 22:56:00');

INSERT INTO audit_logs(user_id,organization_id,action,resource_type,resource_id,changes,ip_address,user_agent,created_at)VALUES(10,4,'logout','user',2,'{}','192.168.1.101','Mozilla/5.0 Windows Chrome/120','2025-09-17 19:53:00');

INSERT INTO audit_logs(user_id,organization_id,action,resource_type,resource_id,changes,ip_address,user_agent,created_at)VALUES(8,4,'create','environment',17,'{}','172.16.0.10','Mozilla/5.0 iPhone Mobile','2026-02-03 18:18:00');

INSERT INTO audit_logs(user_id,organization_id,action,resource_type,resource_id,changes,ip_address,user_agent,created_at)VALUES(1,4,'update','project',7,'{}','10.0.0.50','Mozilla/5.0 Mac Safari/605','2026-02-04 17:59:00');

INSERT INTO audit_logs(user_id,organization_id,action,resource_type,resource_id,changes,ip_address,user_agent,created_at)VALUES(5,1,'create','organization',19,'{}','10.0.0.50','Mozilla/5.0 iPhone Mobile','2025-12-16 11:31:00');

INSERT INTO audit_logs(user_id,organization_id,action,resource_type,resource_id,changes,ip_address,user_agent,created_at)VALUES(5,2,'create','environment',4,'{}','172.16.0.10','Mozilla/5.0 Windows Chrome/120','2025-12-13 01:11:00');

INSERT INTO audit_logs(user_id,organization_id,action,resource_type,resource_id,changes,ip_address,user_agent,created_at)VALUES(9,2,'export','report',26,'{}','10.0.0.51','Mozilla/5.0 Windows Chrome/120','2025-08-20 17:07:00');

INSERT INTO audit_logs(user_id,organization_id,action,resource_type,resource_id,changes,ip_address,user_agent,created_at)VALUES(7,4,'login','user',29,'{}','10.0.0.51','Mozilla/5.0 Mac Safari/605','2026-03-24 09:32:00');

INSERT INTO audit_logs(user_id,organization_id,action,resource_type,resource_id,changes,ip_address,user_agent,created_at)VALUES(9,4,'update','project',10,'{}','192.168.1.100','Mozilla/5.0 iPhone Mobile','2026-02-15 23:47:00');

INSERT INTO audit_logs(user_id,organization_id,action,resource_type,resource_id,changes,ip_address,user_agent,created_at)VALUES(9,2,'create','organization',27,'{}','10.0.0.50','Mozilla/5.0 iPhone Mobile','2026-03-29 03:03:00');

INSERT INTO audit_logs(user_id,organization_id,action,resource_type,resource_id,changes,ip_address,user_agent,created_at)VALUES(9,5,'export','report',31,'{}','192.168.1.100','Mozilla/5.0 Mac Safari/605','2026-05-17 01:27:00');

INSERT INTO audit_logs(user_id,organization_id,action,resource_type,resource_id,changes,ip_address,user_agent,created_at)VALUES(9,1,'update','project',12,'{}','223.5.5.5','Mozilla/5.0 Mac Safari/605','2025-11-24 02:44:00');

INSERT INTO audit_logs(user_id,organization_id,action,resource_type,resource_id,changes,ip_address,user_agent,created_at)VALUES(1,5,'create','test_run',2,'{}','172.16.0.10','Mozilla/5.0 Windows Chrome/120','2025-10-02 03:24:00');

INSERT INTO audit_logs(user_id,organization_id,action,resource_type,resource_id,changes,ip_address,user_agent,created_at)VALUES(9,5,'logout','user',21,'{}','10.0.0.51','Mozilla/5.0 Mac Safari/605','2026-01-21 09:40:00');

INSERT INTO audit_logs(user_id,organization_id,action,resource_type,resource_id,changes,ip_address,user_agent,created_at)VALUES(6,4,'create','test_run',27,'{}','192.168.1.100','Mozilla/5.0 iPhone Mobile','2025-10-01 17:22:00');

INSERT INTO audit_logs(user_id,organization_id,action,resource_type,resource_id,changes,ip_address,user_agent,created_at)VALUES(10,3,'create','organization',46,'{}','10.0.0.50','Mozilla/5.0 Mac Safari/605','2026-03-11 20:06:00');

INSERT INTO audit_logs(user_id,organization_id,action,resource_type,resource_id,changes,ip_address,user_agent,created_at)VALUES(2,5,'login','user',16,'{}','10.0.0.50','Mozilla/5.0 Windows Chrome/120','2026-02-28 18:47:00');

INSERT INTO audit_logs(user_id,organization_id,action,resource_type,resource_id,changes,ip_address,user_agent,created_at)VALUES(9,2,'create','project',30,'{}','192.168.1.101','Mozilla/5.0 Windows Chrome/120','2026-03-03 04:19:00');

INSERT INTO audit_logs(user_id,organization_id,action,resource_type,resource_id,changes,ip_address,user_agent,created_at)VALUES(5,1,'create','organization',7,'{}','192.168.1.100','Mozilla/5.0 Mac Safari/605','2025-11-23 13:04:00');

INSERT INTO audit_logs(user_id,organization_id,action,resource_type,resource_id,changes,ip_address,user_agent,created_at)VALUES(10,1,'create','environment',39,'{}','10.0.0.51','Mozilla/5.0 Windows Chrome/120','2025-10-28 04:57:00');

INSERT INTO audit_logs(user_id,organization_id,action,resource_type,resource_id,changes,ip_address,user_agent,created_at)VALUES(7,5,'create','project',40,'{}','10.0.0.50','Mozilla/5.0 Windows Chrome/120','2026-01-05 01:07:00');

INSERT INTO audit_logs(user_id,organization_id,action,resource_type,resource_id,changes,ip_address,user_agent,created_at)VALUES(9,1,'export','report',15,'{}','10.0.0.50','Mozilla/5.0 Windows Chrome/120','2026-04-08 20:23:00');

INSERT INTO audit_logs(user_id,organization_id,action,resource_type,resource_id,changes,ip_address,user_agent,created_at)VALUES(1,2,'update','project',38,'{}','192.168.1.101','Mozilla/5.0 Windows Chrome/120','2026-02-28 10:34:00');

INSERT INTO audit_logs(user_id,organization_id,action,resource_type,resource_id,changes,ip_address,user_agent,created_at)VALUES(1,2,'logout','user',18,'{}','223.5.5.5','Mozilla/5.0 Mac Safari/605','2026-01-14 18:07:00');

INSERT INTO audit_logs(user_id,organization_id,action,resource_type,resource_id,changes,ip_address,user_agent,created_at)VALUES(2,5,'login','user',28,'{}','192.168.1.100','Mozilla/5.0 Windows Chrome/120','2025-10-13 19:04:00');

INSERT INTO audit_logs(user_id,organization_id,action,resource_type,resource_id,changes,ip_address,user_agent,created_at)VALUES(1,4,'update','project',6,'{}','192.168.1.101','Mozilla/5.0 Mac Safari/605','2026-05-11 23:17:00');

INSERT INTO audit_logs(user_id,organization_id,action,resource_type,resource_id,changes,ip_address,user_agent,created_at)VALUES(1,5,'login','user',19,'{}','192.168.1.101','Mozilla/5.0 Windows Chrome/120','2026-02-26 20:07:00');

INSERT INTO audit_logs(user_id,organization_id,action,resource_type,resource_id,changes,ip_address,user_agent,created_at)VALUES(10,3,'create','project',17,'{}','10.0.0.51','Mozilla/5.0 iPhone Mobile','2026-02-07 06:05:00');

INSERT INTO audit_logs(user_id,organization_id,action,resource_type,resource_id,changes,ip_address,user_agent,created_at)VALUES(10,3,'create','project',37,'{}','10.0.0.51','Mozilla/5.0 Mac Safari/605','2026-01-28 17:00:00');

INSERT INTO audit_logs(user_id,organization_id,action,resource_type,resource_id,changes,ip_address,user_agent,created_at)VALUES(6,4,'login','user',48,'{}','10.0.0.50','Mozilla/5.0 Mac Safari/605','2026-05-01 04:04:00');

INSERT INTO audit_logs(user_id,organization_id,action,resource_type,resource_id,changes,ip_address,user_agent,created_at)VALUES(8,1,'export','report',21,'{}','223.5.5.5','Mozilla/5.0 iPhone Mobile','2026-02-08 10:22:00');

INSERT INTO audit_logs(user_id,organization_id,action,resource_type,resource_id,changes,ip_address,user_agent,created_at)VALUES(6,2,'create','project',30,'{}','10.0.0.51','Mozilla/5.0 Windows Chrome/120','2025-08-29 07:50:00');

INSERT INTO audit_logs(user_id,organization_id,action,resource_type,resource_id,changes,ip_address,user_agent,created_at)VALUES(2,3,'create','environment',15,'{}','223.5.5.5','Mozilla/5.0 Windows Chrome/120','2025-12-30 15:08:00');

INSERT INTO audit_logs(user_id,organization_id,action,resource_type,resource_id,changes,ip_address,user_agent,created_at)VALUES(9,4,'login','user',9,'{}','223.5.5.5','Mozilla/5.0 Mac Safari/605','2025-10-12 21:19:00');

INSERT INTO audit_logs(user_id,organization_id,action,resource_type,resource_id,changes,ip_address,user_agent,created_at)VALUES(8,2,'create','project',30,'{}','172.16.0.10','Mozilla/5.0 iPhone Mobile','2025-12-27 22:47:00');

INSERT INTO audit_logs(user_id,organization_id,action,resource_type,resource_id,changes,ip_address,user_agent,created_at)VALUES(10,5,'create','test_case',40,'{}','10.0.0.50','Mozilla/5.0 Windows Chrome/120','2025-10-12 11:00:00');

INSERT INTO audit_logs(user_id,organization_id,action,resource_type,resource_id,changes,ip_address,user_agent,created_at)VALUES(9,4,'create','test_case',1,'{}','223.5.5.5','Mozilla/5.0 Mac Safari/605','2025-11-26 20:06:00');

INSERT INTO audit_logs(user_id,organization_id,action,resource_type,resource_id,changes,ip_address,user_agent,created_at)VALUES(1,5,'create','project',3,'{}','192.168.1.100','Mozilla/5.0 iPhone Mobile','2026-04-09 15:07:00');

INSERT INTO audit_logs(user_id,organization_id,action,resource_type,resource_id,changes,ip_address,user_agent,created_at)VALUES(5,2,'login','user',11,'{}','192.168.1.100','Mozilla/5.0 Mac Safari/605','2025-12-30 02:21:00');

INSERT INTO audit_logs(user_id,organization_id,action,resource_type,resource_id,changes,ip_address,user_agent,created_at)VALUES(1,5,'create','test_case',17,'{}','172.16.0.10','Mozilla/5.0 Windows Chrome/120','2025-08-06 02:49:00');

INSERT INTO audit_logs(user_id,organization_id,action,resource_type,resource_id,changes,ip_address,user_agent,created_at)VALUES(5,2,'create','test_run',13,'{}','192.168.1.101','Mozilla/5.0 Windows Chrome/120','2026-05-29 04:45:00');

INSERT INTO audit_logs(user_id,organization_id,action,resource_type,resource_id,changes,ip_address,user_agent,created_at)VALUES(8,2,'logout','user',3,'{}','10.0.0.50','Mozilla/5.0 iPhone Mobile','2025-12-13 22:06:00');

INSERT INTO audit_logs(user_id,organization_id,action,resource_type,resource_id,changes,ip_address,user_agent,created_at)VALUES(1,2,'logout','user',40,'{}','10.0.0.50','Mozilla/5.0 Mac Safari/605','2025-12-14 11:17:00');

INSERT INTO audit_logs(user_id,organization_id,action,resource_type,resource_id,changes,ip_address,user_agent,created_at)VALUES(1,5,'update','project',26,'{}','172.16.0.10','Mozilla/5.0 iPhone Mobile','2025-08-19 00:16:00');

INSERT INTO audit_logs(user_id,organization_id,action,resource_type,resource_id,changes,ip_address,user_agent,created_at)VALUES(6,2,'update','project',49,'{}','192.168.1.101','Mozilla/5.0 Windows Chrome/120','2026-01-02 02:35:00');

INSERT INTO audit_logs(user_id,organization_id,action,resource_type,resource_id,changes,ip_address,user_agent,created_at)VALUES(5,1,'create','environment',9,'{}','172.16.0.10','Mozilla/5.0 Windows Chrome/120','2025-12-05 15:13:00');

INSERT INTO audit_logs(user_id,organization_id,action,resource_type,resource_id,changes,ip_address,user_agent,created_at)VALUES(6,3,'logout','user',9,'{}','10.0.0.50','Mozilla/5.0 Windows Chrome/120','2026-03-10 15:57:00');

INSERT INTO audit_logs(user_id,organization_id,action,resource_type,resource_id,changes,ip_address,user_agent,created_at)VALUES(10,5,'create','test_run',49,'{}','10.0.0.51','Mozilla/5.0 Mac Safari/605','2026-03-25 08:53:00');

INSERT INTO audit_logs(user_id,organization_id,action,resource_type,resource_id,changes,ip_address,user_agent,created_at)VALUES(5,4,'update','project',32,'{}','192.168.1.101','Mozilla/5.0 Windows Chrome/120','2025-09-27 19:41:00');

INSERT INTO audit_logs(user_id,organization_id,action,resource_type,resource_id,changes,ip_address,user_agent,created_at)VALUES(8,1,'create','test_case',11,'{}','192.168.1.100','Mozilla/5.0 Mac Safari/605','2026-02-27 14:11:00');

INSERT INTO audit_logs(user_id,organization_id,action,resource_type,resource_id,changes,ip_address,user_agent,created_at)VALUES(7,2,'logout','user',37,'{}','10.0.0.51','Mozilla/5.0 Mac Safari/605','2026-04-11 15:52:00');

INSERT INTO audit_logs(user_id,organization_id,action,resource_type,resource_id,changes,ip_address,user_agent,created_at)VALUES(5,1,'create','environment',29,'{}','223.5.5.5','Mozilla/5.0 Windows Chrome/120','2026-04-10 18:37:00');

INSERT INTO audit_logs(user_id,organization_id,action,resource_type,resource_id,changes,ip_address,user_agent,created_at)VALUES(6,4,'create','environment',9,'{}','10.0.0.50','Mozilla/5.0 Mac Safari/605','2025-12-20 05:18:00');

INSERT INTO audit_logs(user_id,organization_id,action,resource_type,resource_id,changes,ip_address,user_agent,created_at)VALUES(9,1,'create','test_case',25,'{}','192.168.1.101','Mozilla/5.0 iPhone Mobile','2026-05-18 14:33:00');

INSERT INTO audit_logs(user_id,organization_id,action,resource_type,resource_id,changes,ip_address,user_agent,created_at)VALUES(2,2,'create','organization',50,'{}','192.168.1.100','Mozilla/5.0 Windows Chrome/120','2025-08-12 15:50:00');

INSERT INTO audit_logs(user_id,organization_id,action,resource_type,resource_id,changes,ip_address,user_agent,created_at)VALUES(7,3,'create','test_run',9,'{}','192.168.1.100','Mozilla/5.0 Windows Chrome/120','2026-03-07 11:54:00');

INSERT INTO audit_logs(user_id,organization_id,action,resource_type,resource_id,changes,ip_address,user_agent,created_at)VALUES(2,2,'create','test_run',45,'{}','10.0.0.50','Mozilla/5.0 Mac Safari/605','2026-05-26 23:54:00');

INSERT INTO audit_logs(user_id,organization_id,action,resource_type,resource_id,changes,ip_address,user_agent,created_at)VALUES(7,2,'update','project',47,'{}','192.168.1.100','Mozilla/5.0 iPhone Mobile','2026-04-09 00:45:00');

INSERT INTO audit_logs(user_id,organization_id,action,resource_type,resource_id,changes,ip_address,user_agent,created_at)VALUES(1,4,'export','report',29,'{}','172.16.0.10','Mozilla/5.0 Mac Safari/605','2026-03-22 01:31:00');

INSERT INTO audit_logs(user_id,organization_id,action,resource_type,resource_id,changes,ip_address,user_agent,created_at)VALUES(5,3,'create','test_run',45,'{}','192.168.1.101','Mozilla/5.0 Windows Chrome/120','2026-04-14 17:26:00');

INSERT INTO audit_logs(user_id,organization_id,action,resource_type,resource_id,changes,ip_address,user_agent,created_at)VALUES(6,3,'create','test_case',41,'{}','223.5.5.5','Mozilla/5.0 iPhone Mobile','2026-04-05 15:49:00');

INSERT INTO audit_logs(user_id,organization_id,action,resource_type,resource_id,changes,ip_address,user_agent,created_at)VALUES(1,5,'create','test_case',50,'{}','10.0.0.51','Mozilla/5.0 Mac Safari/605','2026-05-10 20:29:00');

INSERT INTO audit_logs(user_id,organization_id,action,resource_type,resource_id,changes,ip_address,user_agent,created_at)VALUES(9,2,'update','project',14,'{}','192.168.1.101','Mozilla/5.0 iPhone Mobile','2025-08-19 20:38:00');

INSERT INTO audit_logs(user_id,organization_id,action,resource_type,resource_id,changes,ip_address,user_agent,created_at)VALUES(2,1,'create','test_run',40,'{}','192.168.1.101','Mozilla/5.0 Mac Safari/605','2025-10-04 11:26:00');

INSERT INTO audit_logs(user_id,organization_id,action,resource_type,resource_id,changes,ip_address,user_agent,created_at)VALUES(7,1,'create','environment',18,'{}','172.16.0.10','Mozilla/5.0 Mac Safari/605','2025-09-16 22:13:00');

INSERT INTO audit_logs(user_id,organization_id,action,resource_type,resource_id,changes,ip_address,user_agent,created_at)VALUES(6,3,'export','report',11,'{}','223.5.5.5','Mozilla/5.0 Mac Safari/605','2025-09-30 05:35:00');

INSERT INTO audit_logs(user_id,organization_id,action,resource_type,resource_id,changes,ip_address,user_agent,created_at)VALUES(5,5,'login','user',48,'{}','10.0.0.50','Mozilla/5.0 Mac Safari/605','2025-09-28 05:18:00');

INSERT INTO audit_logs(user_id,organization_id,action,resource_type,resource_id,changes,ip_address,user_agent,created_at)VALUES(5,2,'create','test_run',20,'{}','223.5.5.5','Mozilla/5.0 Mac Safari/605','2025-11-22 07:10:00');

INSERT INTO audit_logs(user_id,organization_id,action,resource_type,resource_id,changes,ip_address,user_agent,created_at)VALUES(9,2,'create','project',36,'{}','192.168.1.101','Mozilla/5.0 Windows Chrome/120','2025-12-04 09:12:00');

INSERT INTO audit_logs(user_id,organization_id,action,resource_type,resource_id,changes,ip_address,user_agent,created_at)VALUES(2,3,'export','report',12,'{}','223.5.5.5','Mozilla/5.0 iPhone Mobile','2025-11-06 04:12:00');

INSERT INTO audit_logs(user_id,organization_id,action,resource_type,resource_id,changes,ip_address,user_agent,created_at)VALUES(7,5,'create','organization',12,'{}','10.0.0.51','Mozilla/5.0 Windows Chrome/120','2026-01-24 04:19:00');

INSERT INTO audit_logs(user_id,organization_id,action,resource_type,resource_id,changes,ip_address,user_agent,created_at)VALUES(1,2,'logout','user',11,'{}','192.168.1.101','Mozilla/5.0 Mac Safari/605','2026-04-18 00:24:00');

INSERT INTO audit_logs(user_id,organization_id,action,resource_type,resource_id,changes,ip_address,user_agent,created_at)VALUES(5,5,'login','user',1,'{}','223.5.5.5','Mozilla/5.0 iPhone Mobile','2025-10-30 21:50:00');

INSERT INTO audit_logs(user_id,organization_id,action,resource_type,resource_id,changes,ip_address,user_agent,created_at)VALUES(10,4,'login','user',9,'{}','10.0.0.51','Mozilla/5.0 Windows Chrome/120','2026-01-17 23:08:00');

INSERT INTO audit_logs(user_id,organization_id,action,resource_type,resource_id,changes,ip_address,user_agent,created_at)VALUES(1,2,'create','test_run',28,'{}','192.168.1.101','Mozilla/5.0 Windows Chrome/120','2025-09-30 00:19:00');

INSERT INTO audit_logs(user_id,organization_id,action,resource_type,resource_id,changes,ip_address,user_agent,created_at)VALUES(1,2,'login','user',46,'{}','172.16.0.10','Mozilla/5.0 Windows Chrome/120','2026-05-06 10:12:00');

INSERT INTO github_integrations(id,user_id,repo_owner,repo_name,webhook_secret,is_active,created_at,updated_at)VALUES(1,1,'1','fullscope-backend','whsec_188502',true,'2026-01-05 02:45:00','2026-05-31 03:26:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO github_integrations(id,user_id,repo_owner,repo_name,webhook_secret,is_active,created_at,updated_at)VALUES(2,1,'2','fullscope-frontend','whsec_749264',true,'2026-04-17 05:50:00','2026-05-30 19:55:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO github_integrations(id,user_id,repo_owner,repo_name,webhook_secret,is_active,created_at,updated_at)VALUES(3,2,'3','user-center','whsec_191062',true,'2026-01-01 02:36:00','2026-06-01 11:58:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO webhook_tokens(id,project_id,name,token,is_active,created_at)VALUES(1,1,'Webhook-1','wh_c4ca4238a0b92382',true,'2026-02-14 09:01:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO webhook_tokens(id,project_id,name,token,is_active,created_at)VALUES(2,2,'Webhook-2','wh_c81e728d9d4c2f63',true,'2026-01-17 05:31:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO webhook_tokens(id,project_id,name,token,is_active,created_at)VALUES(3,3,'Webhook-3','wh_eccbc87e4b5ce2fe',true,'2026-01-27 12:58:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO webhook_tokens(id,project_id,name,token,is_active,created_at)VALUES(4,4,'Webhook-4','wh_a87ff679a2f3e71d',true,'2026-03-10 21:43:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO webhook_tokens(id,project_id,name,token,is_active,created_at)VALUES(5,5,'Webhook-5','wh_e4da3b7fbbce2345',true,'2026-02-19 06:01:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO webhook_tokens(id,project_id,name,token,is_active,created_at)VALUES(6,6,'Webhook-6','wh_1679091c5a880faf',true,'2025-12-07 10:34:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO webhook_tokens(id,project_id,name,token,is_active,created_at)VALUES(7,7,'Webhook-7','wh_8f14e45fceea167a',true,'2026-05-17 18:33:00')ON CONFLICT(id)DO NOTHING;

INSERT INTO webhook_tokens(id,project_id,name,token,is_active,created_at)VALUES(8,8,'Webhook-8','wh_c9f0f895fb98ab91',true,'2026-04-28 21:42:00')ON CONFLICT(id)DO NOTHING;

SELECT setval('users_id_seq',55);

SELECT setval('organizations_id_seq',10);

SELECT setval('organization_members_id_seq',200);

SELECT setval('projects_id_seq',20);

SELECT setval('environments_id_seq',70);

SELECT setval('api_test_collections_id_seq',150);

SELECT setval('api_test_cases_id_seq',1000);

SELECT setval('web_test_collections_id_seq',50);

SELECT setval('web_test_scripts_id_seq',200);

SELECT setval('perf_test_scenarios_id_seq',30);

SELECT setval('performance_test_results_id_seq',200);

SELECT setval('test_runs_id_seq',500);

SELECT setval('test_reports_id_seq',200);

SELECT setval('test_documents_id_seq',80);

SELECT setval('quality_gates_id_seq',30);

SELECT setval('quality_gate_evaluations_id_seq',300);

SELECT setval('trigger_rules_id_seq',30);

SELECT setval('scheduled_tasks_id_seq',30);

SELECT setval('api_tokens_id_seq',20);

SELECT setval('prompt_versions_id_seq',30);

SELECT setval('ai_invocation_logs_id_seq',300);

SELECT setval('performance_alert_rules_id_seq',50);

SELECT setval('performance_alert_logs_id_seq',60);

SELECT setval('visual_baselines_id_seq',50);

SELECT setval('visual_diffs_id_seq',40);

SELECT setval('audit_logs_id_seq',400);

SELECT setval('github_integrations_id_seq',10);

SELECT setval('webhook_tokens_id_seq',10);

