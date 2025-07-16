# 📚 UNNES Document Chat System - API Documentation

## 🌟 Overview

UNNES Document Chat System adalah platform berbasis AI yang memungkinkan mahasiswa dan staf UNNES untuk mengunggah dokumen dan berinteraksi dengan dokumen tersebut menggunakan teknologi RAG (Retrieval-Augmented Generation) yang berjalan secara lokal menggunakan Ollama.

**Base URL:** `http://localhost:8000`  
**API Version:** v1  
**API Prefix:** `/api/v1`

---

## 🔐 Authentication

Sistem menggunakan JWT Bearer Token untuk autentikasi. Token harus disertakan dalam header `Authorization` dengan format:

```
Authorization: Bearer <your_jwt_token>
```

### Roles
- **user**: Pengguna biasa (mahasiswa/staf)
- **admin**: Administrator sistem

---

## 📋 API Endpoints

### 🔑 Authentication Endpoints

#### 1. Login dengan Password
**POST** `/api/v1/auth/token`

**Description:** Login menggunakan username dan password

**Request Body (Form Data):**
```json
{
  "username": "string",
  "password": "string"
}
```

**Response:**
```json
{
  "access_token": "string",
  "token_type": "bearer",
  "role": "user|admin"
}
```

**Status Codes:**
- `200`: Login berhasil
- `401`: Kredensial tidak valid

---

#### 2. Login dengan Google
**POST** `/api/v1/auth/google`

**Description:** Login menggunakan Google OAuth

**Request Body:**
```json
{
  "credential": "string"
}
```

**Response:**
```json
{
  "access_token": "string",
  "token_type": "bearer",
  "role": "user|admin"
}
```

---

#### 3. Register
**POST** `/api/v1/auth/register`

**Description:** Registrasi pengguna baru

**Request Body:**
```json
{
  "username": "string",
  "email": "user@students.unnes.ac.id",
  "password": "string"
}
```

**Response:**
```json
{
  "message": "User registered successfully"
}
```

**Validation:**
- Email harus dari domain `@students.unnes.ac.id` atau `@mail.unnes.ac.id`

**Status Codes:**
- `201`: Registrasi berhasil
- `400`: Data tidak valid
- `409`: Username/email sudah ada

---

#### 4. Get User Profile
**GET** `/api/v1/auth/profile`

**Description:** Mendapatkan profil pengguna yang sedang login

**Headers:**
```
Authorization: Bearer <token>
```

**Response:**
```json
{
  "username": "string",
  "email": "string",
  "role": "user|admin"
}
```

---

### 📄 Document Management Endpoints

#### 1. Upload Documents
**POST** `/api/v1/documents/upload`

**Description:** Upload dokumen untuk diproses oleh sistem RAG

**Headers:**
```
Authorization: Bearer <token>
Content-Type: multipart/form-data
```

**Request Body (Form Data):**
```
files: File[] (multiple files)
```

**Supported Formats:** PDF, DOCX, DOC, TXT  
**Max Files:** 5 files per request

**Response:**
```json
{
  "uploaded_documents": [
    {
      "document_id": "uuid",
      "filename": "string"
    }
  ]
}
```

**Status Codes:**
- `200`: Upload berhasil
- `503`: Sistem RAG tidak siap
- `500`: Error saat memproses file

---

#### 2. Get User Documents
**GET** `/api/v1/documents/documents`

**Description:** Mendapatkan daftar dokumen milik pengguna

**Headers:**
```
Authorization: Bearer <token>
```

**Response:**
```json
{
  "documents": [
    {
      "id": "string",
      "filename": "string",
      "upload_date": "2024-01-01T00:00:00"
    }
  ]
}
```

---

#### 3. Delete Document
**DELETE** `/api/v1/documents/documents/{document_id}`

**Description:** Menghapus dokumen milik pengguna

**Headers:**
```
Authorization: Bearer <token>
```

**Path Parameters:**
- `document_id`: ID dokumen yang akan dihapus

**Status Codes:**
- `204`: Dokumen berhasil dihapus
- `404`: Dokumen tidak ditemukan

---

### 💬 Chat Endpoints

#### 1. Process Chat Message
**POST** `/api/v1/chat`

**Description:** Mengirim pesan chat dan mendapatkan respons dari sistem RAG

**Headers:**
```
Authorization: Bearer <token>
Content-Type: application/json
```

**Request Body:**
```json
{
  "session_id": "string",
  "message": "string",
  "document_ids": ["string"]
}
```

**Response:**
```json
{
  "response": "string"
}
```

**Notes:**
- `document_ids` dapat berupa array kosong untuk mencari di semua dokumen
- Jika diisi, sistem akan mencari hanya di dokumen yang ditentukan

---

#### 2. Get Chat History
**GET** `/api/v1/chat/history/{session_id}`

**Description:** Mendapatkan riwayat chat untuk session tertentu

**Headers:**
```
Authorization: Bearer <token>
```

**Path Parameters:**
- `session_id`: ID session chat

**Response:**
```json
[
  {
    "sender": "user|assistant",
    "content": "string",
    "timestamp": "2024-01-01T00:00:00"
  }
]
```

---

### 👑 Admin Endpoints

> **Note:** Semua endpoint admin memerlukan role `admin`

#### 1. Get Admin Statistics
**GET** `/api/v1/admin/stats`

**Description:** Mendapatkan statistik sistem

**Headers:**
```
Authorization: Bearer <admin_token>
```

**Response:**
```json
{
  "total_users": 0,
  "total_documents": 0,
  "total_chats": 0
}
```

---

#### 2. Get All Users
**GET** `/api/v1/admin/users`

**Description:** Mendapatkan daftar semua pengguna

**Response:**
```json
[
  {
    "username": "string",
    "email": "string",
    "role": "user|admin",
    "created_at": "2024-01-01T00:00:00"
  }
]
```

---

#### 3. Delete User
**DELETE** `/api/v1/admin/users/{username}`

**Description:** Menghapus pengguna dan semua data terkait

**Path Parameters:**
- `username`: Username yang akan dihapus

**Status Codes:**
- `204`: Pengguna berhasil dihapus
- `400`: Tidak dapat menghapus akun sendiri
- `404`: Pengguna tidak ditemukan

**Notes:**
- Akan menghapus semua dokumen dan chat history pengguna
- Akan rebuild FAISS index

---

#### 4. Get All Documents (Admin)
**GET** `/api/v1/admin/documents`

**Description:** Mendapatkan daftar semua dokumen di sistem

**Response:**
```json
[
  {
    "id": "string",
    "username": "string",
    "filename": "string",
    "upload_date": "2024-01-01T00:00:00",
    "file_size": 0
  }
]
```

---

#### 5. Delete Document (Admin)
**DELETE** `/api/v1/admin/documents/{document_id}`

**Description:** Menghapus dokumen dari sistem (admin)

**Path Parameters:**
- `document_id`: ID dokumen yang akan dihapus

**Status Codes:**
- `204`: Dokumen berhasil dihapus
- `404`: Dokumen tidak ditemukan

---

#### 6. Get System Activity
**GET** `/api/v1/admin/activity`

**Description:** Mendapatkan aktivitas chat terbaru (50 terakhir)

**Response:**
```json
{
  "activity": [
    {
      "username": "string",
      "message": "string",
      "response": "string",
      "timestamp": "2024-01-01T00:00:00",
      "document_ids": "[\"id1\", \"id2\"]"
    }
  ]
}
```

---

### 🏥 System Health Endpoint

#### Health Check
**GET** `/health`

**Description:** Mengecek status kesehatan sistem

**Response:**
```json
{
  "status": "healthy|degraded",
  "database": "connected|disconnected",
  "llm_ollama": "connected|disconnected"
}
```

---

## 🔧 Error Handling

### Standard Error Response
```json
{
  "detail": "Error message"
}
```

### Common HTTP Status Codes
- `200`: Success
- `201`: Created
- `204`: No Content
- `400`: Bad Request
- `401`: Unauthorized
- `403`: Forbidden
- `404`: Not Found
- `409`: Conflict
- `500`: Internal Server Error
- `503`: Service Unavailable

---

## 📝 Usage Examples

### Example 1: Complete Authentication Flow

```bash
# 1. Register
curl -X POST "http://localhost:8000/api/v1/auth/register" \
  -H "Content-Type: application/json" \
  -d '{
    "username": "john_doe",
    "email": "john@students.unnes.ac.id",
    "password": "securepassword"
  }'

# 2. Login
curl -X POST "http://localhost:8000/api/v1/auth/token" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=john_doe&password=securepassword"

# Response:
# {
#   "access_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
#   "token_type": "bearer",
#   "role": "user"
# }
```

### Example 2: Upload and Chat with Documents

```bash
# 1. Upload document
curl -X POST "http://localhost:8000/api/v1/documents/upload" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -F "files=@document.pdf"

# 2. Send chat message
curl -X POST "http://localhost:8000/api/v1/chat" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "session_id": "session_123",
    "message": "Apa isi dari dokumen ini?",
    "document_ids": []
  }'
```

### Example 3: Admin Operations

```bash
# Get system statistics
curl -X GET "http://localhost:8000/api/v1/admin/stats" \
  -H "Authorization: Bearer ADMIN_TOKEN"

# Get all users
curl -X GET "http://localhost:8000/api/v1/admin/users" \
  -H "Authorization: Bearer ADMIN_TOKEN"
```

---

## 🔒 Security Considerations

1. **JWT Tokens**: Tokens memiliki expiration time
2. **Email Validation**: Hanya email domain UNNES yang diterima
3. **File Upload**: Validasi format file dan ukuran
4. **Role-based Access**: Admin endpoints hanya dapat diakses oleh admin
5. **Data Isolation**: User hanya dapat mengakses data milik sendiri

---

## 🚀 Getting Started

1. **Start the server:**
   ```bash
   uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
   ```

2. **Access API Documentation:**
   - Swagger UI: `http://localhost:8000/docs`
   - ReDoc: `http://localhost:8000/redoc`

3. **Access Web Interface:**
   - Main App: `http://localhost:8000/`

---

## 📞 Support

Untuk pertanyaan atau dukungan teknis, silakan hubungi tim pengembang UNNES Document Chat System.

---

**Last Updated:** 2024  
**Version:** 7.0.0  
**Framework:** FastAPI + LangChain + Ollama