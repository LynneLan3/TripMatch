# 问卷系统数据库设计文档

## 1. 数据库概述

### 1.1 数据库信息
- 数据库名：tripmatch
- 字符集：utf8mb4
- 排序规则：utf8mb4_unicode_ci

### 1.2 表清单
1. questionnaires（问卷表）
2. questions（问题表）
3. options（选项表）
4. questionnaire_questions（问卷-问题关联表）
5. user_answers（用户答案表）
6. users（用户表）

## 2. 表结构设计

### 2.1 questionnaires（问卷表）
| 字段名      | 类型         | 允许空 | 默认值 | 说明     |
|------------|-------------|--------|--------|----------|
| id         | bigint(20)  | NO     | NULL   | 主键     |
| title      | varchar(255)| NO     | NULL   | 问卷标题  |
| level      | varchar(20) | NO     | 'easy' | 难度等级  |
| description| text        | YES    | NULL   | 问卷描述  |

### 2.2 questions（问题表）
| 字段名    | 类型         | 允许空 | 默认值 | 说明     |
|----------|-------------|--------|--------|----------|
| id       | bigint(20)  | NO     | NULL   | 主键     |
| content  | text        | NO     | NULL   | 问题内容  |
| category | varchar(50) | YES    | NULL   | 问题类别  |

### 2.3 options（选项表）
| 字段名      | 类型         | 允许空 | 默认值 | 说明     |
|------------|-------------|--------|--------|----------|
| id         | bigint(20)  | NO     | NULL   | 主键     |
| question_id| bigint(20)  | NO     | NULL   | 问题ID   |
| content    | text        | NO     | NULL   | 选项内容  |

### 2.4 questionnaire_questions（问卷-问题关联表）
| 字段名          | 类型        | 允许空 | 默认值 | 说明     |
|----------------|------------|--------|--------|----------|
| id             | bigint(20) | NO     | NULL   | 主键     |
| questionnaire_id| bigint(20) | NO     | NULL   | 问卷ID   |
| question_id    | bigint(20) | NO     | NULL   | 问题ID   |

### 2.5 user_answers（用户答案表）
| 字段名          | 类型        | 允许空 | 默认值 | 说明     |
|----------------|------------|--------|--------|----------|
| id             | bigint(20) | NO     | NULL   | 主键     |
| user_id        | bigint(20) | NO     | NULL   | 用户ID   |
| questionnaire_id| bigint(20) | NO     | NULL   | 问卷ID   |
| question_id    | bigint(20) | NO     | NULL   | 问题ID   |
| option_id      | bigint(20) | NO     | NULL   | 选项ID   |
| created_at     | timestamp  | NO     | NOW()  | 创建时间  |

### 2.6 users（用户表）
| 字段名      | 类型         | 允许空 | 默认值 | 说明     |
|------------|-------------|--------|--------|----------|
| id         | bigint(20)  | NO     | NULL   | 主键     |
| username   | varchar(50) | NO     | NULL   | 用户名   |
| password   | varchar(255)| NO     | NULL   | 密码     |
| created_at | timestamp   | NO     | NOW()  | 创建时间  |

## 3. 索引设计

### 3.1 主键索引
- questionnaires.id
- questions.id
- options.id
- questionnaire_questions.id
- user_answers.id
- users.id

### 3.2 外键索引
- options.question_id -> questions.id
- questionnaire_questions.questionnaire_id -> questionnaires.id
- questionnaire_questions.question_id -> questions.id
- user_answers.user_id -> users.id
- user_answers.questionnaire_id -> questionnaires.id
- user_answers.question_id -> questions.id
- user_answers.option_id -> options.id

### 3.3 普通索引
- users.username（唯一索引）
- user_answers.created_at

## 4. 数据库维护

### 4.1 备份策略
- 每日全量备份
- 实时binlog备份
- 定期测试恢复

### 4.2 优化建议
1. 定期ANALYZE TABLE
2. 监控慢查询
3. 优化索引使用
4. 定期清理冗余数据

## 5. 示例查询

### 5.1 获取问卷及其问题
```sql
SELECT q.*, qq.question_id
FROM questionnaires q
JOIN questionnaire_questions qq ON q.id = qq.questionnaire_id
WHERE q.id = ?;
```

### 5.2 获取用户答题记录
```sql
SELECT ua.*, q.content as question_content, o.content as option_content
FROM user_answers ua
JOIN questions q ON ua.question_id = q.id
JOIN options o ON ua.option_id = o.id
WHERE ua.user_id = ? AND ua.questionnaire_id = ?;
```

## 6. 安全考虑

### 6.1 权限控制
- 创建只读用户用于查询
- 限制数据库远程访问
- 定期更新数据库密码

### 6.2 数据安全
- 敏感数据加密存储
- 定期安全审计
- 监控异常访问
