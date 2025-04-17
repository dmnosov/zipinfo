# ZipInfo

**ZipInfo** — это проект для просмотра и анализа ZIP-архивов через веб-интерфейс и API.

## 🚀 Быстрый старт

### 1. Клонируйте репозиторий

```bash
git clone https://github.com/dmnosov/zipinfo.git
```

### 2. Перейдите в директорию проекта

```bash
cd zipinfo
```

### 3. Запустите проект с помощью Docker

```bash
docker compose up -d --build
```

---

## 📌 Основные ресурсы

- **API**: [http://localhost:8000/docs](http://localhost:8000/docs)
- **Веб-версия**: [http://localhost:3000](http://localhost:3000)

---

## 🔐 Данные для авторизации

- **Логин**: `test`  
- **Пароль**: `test`

---

## 💾 Дополнительные ресурсы

- **MinIO S3 (консоль)**: [http://localhost:9001](http://localhost:9001)  
  Логин: `user`  
  Пароль: `miniopass123`

- **Keycloak**: [http://localhost:8080](http://localhost:8080)  
  Логин: `admin`  
  Пароль: `admin`

---

## 📦 Возможности

- Загрузка ZIP-архивов
- Просмотр содержимого архива
- Работа через REST API и веб-интерфейс
- Хранение файлов через S3-совместимое хранилище
- Аутентификация через Keycloak

---

## 🛠️ Требования

- Docker
- Docker Compose
