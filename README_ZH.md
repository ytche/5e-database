# 5e 数据库管理系统

## 项目概述

这是一个基于 Spring Boot 框架开发的 5e 数据库管理系统。项目采用现代化的 Java Web 开发技术栈，提供完整的数据管理功能。

## 功能特性

### 核心功能
- ✅ **用户管理**: 完整的用户注册、登录、权限控制
- ✅ **数据管理**: CRUD 操作，支持批量导入导出
- ✅ **API 接口**: 提供 RESTful API 供外部系统调用
- ✅ **数据验证**: 输入数据验证和业务逻辑校验
- ✅ **安全机制**: 基于 Spring Security 的安全防护

### 技术特性
-  **高性能**: 基于 Spring Boot 2.x，启动快速，响应迅速
- ️ **安全性**: 集成 Spring Security，提供身份验证和授权
-  **数据库**: 支持 MySQL/PostgreSQL，使用 JPA/Hibernate
-  **API 文档**: 集成 Swagger/OpenAPI 自动生成 API 文档
-  **测试覆盖**: 单元测试和集成测试

## 技术栈

### 后端技术
- **框架**: Spring Boot 2.x
- **安全**: Spring Security
- **数据访问**: Spring Data JPA + Hibernate
- **数据库**: MySQL 8.0 / PostgreSQL 13
- **构建工具**: Maven 3.6+
- **API 文档**: Swagger 2 / OpenAPI 3

### 前端技术（如果包含）
- **框架**: Vue.js 3 / React
- **构建工具**: Vite / Webpack
- **UI 组件**: Element Plus / Ant Design

## 快速开始

### 前置条件
- JDK 11 或更高版本
- Maven 3.6+
- MySQL 8.0+ 或 PostgreSQL 13+
- Git

### 安装步骤

1. **克隆项目**
   ```bash
   git clone https://github.com/yourusername/5e-database.git
   cd 5e-database
   ```

2. **配置数据库**
   ```bash
   # 创建数据库
   CREATE DATABASE five_edb;
   
   # 或者使用 Docker
   docker run --name mysql-5e -e MYSQL_ROOT_PASSWORD=password -p 3306:3306 -d mysql:8.0
   ```

3. **修改配置文件**
   ```properties
   # src/main/resources/application.properties
   spring.datasource.url=jdbc:mysql://localhost:3306/five_edb
   spring.datasource.username=root
   spring.datasource.password=password
   ```

4. **构建项目**
   ```bash
   mvn clean install
   ```

5. **运行应用**
   ```bash
   mvn spring-boot:run
   # 或
   java -jar target/5e-database-1.0.0.jar
   ```

## 项目结构
