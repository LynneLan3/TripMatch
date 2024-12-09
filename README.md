# TripMatch 问卷系统

一个基于Flask和MySQL的在线问卷调查系统，支持用户答题和数据收集功能。

## 功能特点

- 问卷列表展示
- 实时答题进度
- 自动保存答案
- 问卷难度分级
- 用户答题记录

## 技术栈

- 后端：Python Flask
- 前端：HTML5, CSS3, jQuery
- 数据库：MySQL
- 部署：支持本地开发环境

## 快速开始

### 1. 环境要求

- Python 3.8+
- MySQL 8.0+
- 现代浏览器（Chrome, Firefox, Safari等）

### 2. 安装依赖

```bash
pip install -r requirements.txt
```

### 3. 配置环境变量

创建 `.env` 文件并配置以下变量：

```
DB_HOST=localhost
DB_PORT=3306
DB_NAME=tripmatch
DB_USER=your_username
DB_PASSWORD=your_password
```

### 4. 初始化数据库

使用 `docs/DATABASE.md` 中的数据库设计创建所需的表结构。

### 5. 运行服务

```bash
python app.py
```

服务将在 http://localhost:8081 启动

## API 接口

### 问卷相关

#### 获取问卷列表
- URL: `/questionnaires`
- 方法: `GET`
- 响应: 返回所有问卷信息

#### 获取问卷详情
- URL: `/questionnaire/<id>`
- 方法: `GET`
- 响应: 返回指定问卷的详细信息和问题列表

### 答题相关

#### 保存答案
- URL: `/save_answers`
- 方法: `POST`
- 请求体: 包含用户ID、问卷ID和答案列表

## 项目文档

- [产品需求文档](docs/PRD.md)
- [项目维护文档](docs/MAINTENANCE.md)
- [数据库设计文档](docs/DATABASE.md)

## 开发团队

- 后端开发：[LynneLan3](https://github.com/LynneLan3)

## 版本历史

- v1.0.0 (2024-12-09)
  - 初始版本发布
  - 实现基础问卷功能
  - 完成用户答题系统

## 许可证

MIT License
