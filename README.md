# Flask API Ödevi

Bu proje, bir Flask uygulamasının Dockerize edilmesi ve JWT ile güvenli hale getirilmesini içermektedir.

## Özellikler
* **Açık Endpoint:** `/ortalama` (Token gerektirmez)
* **Kilitli Endpoint:** `/ozel-veri` (JWT gerektirir)
* **Veritabanı:** JSON tabanlı veri simülasyonu içermektedir.

## Sistem Akışı (Mermaid.js)
```mermaid
sequenceDiagram
    participant Kullanıcı
    participant API
    participant Veritabanı

    Kullanıcı->>API: /login (admin/123)
    API-->>Kullanıcı: JWT Token Dönüşü
    
    Note over Kullanıcı, API: Token ile Yetkili İstek
    
    Kullanıcı->>API: /ozel-veri (Header: Authorization)
    API->>Veritabanı: Veri Sorgula
    Veritabanı-->>API: JSON Verisi
    API-->>Kullanıcı: 200 OK (Gizli Veri)
