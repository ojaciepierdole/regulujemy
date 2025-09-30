# DANE DOSTĘPOWE - REGULUJEMY.PL
## Środowisko developerskie

### 1. Payload CMS
- **URL**: http://localhost:3456/admin
- **Pierwsze logowanie**: Musisz utworzyć konto administratora
- **API URL**: http://localhost:3456/api
- **GraphQL Playground**: http://localhost:3456/api/graphql-playground

### 2. MinIO (Object Storage / S3)
- **Console URL**: http://localhost:9001
- **API URL**: http://localhost:9000
- **Login**: `minio`
- **Hasło**: `minio123`
- **Bucket**: `uploads`
- **Access Key ID**: `minio`
- **Secret Access Key**: `minio123`

### 3. MongoDB
- **Connection String**: `mongodb://admin:admin123@localhost:27017/regulujemy-cms?authSource=admin`
- **Host**: localhost
- **Port**: 27017
- **Database**: `regulujemy-cms`
- **Username**: `admin`
- **Password**: `admin123`
- **Auth Database**: `admin`

### 4. Zmienne środowiskowe (.env)
```env
PAYLOAD_SECRET=supersecret-change-this-in-production
NODE_ENV=development
PORT=3456
DATABASE_URI=mongodb://localhost:27017/regulujemy-cms
S3_ENDPOINT=http://localhost:9000
S3_ACCESS_KEY_ID=minio
S3_SECRET_ACCESS_KEY=minio123
S3_BUCKET=uploads
S3_REGION=us-east-1
PAYLOAD_PUBLIC_SERVER_URL=http://localhost:3456
PAYLOAD_PUBLIC_SITE_URL=http://localhost:3000
```

### 5. Docker Services
- **MongoDB**: port 27017
- **MinIO**: ports 9000 (API), 9001 (Console)
- **Payload CMS**: port 3456

### 6. Komendy Docker
```bash
# Start wszystkich serwisów
docker-compose up -d

# Stop wszystkich serwisów
docker-compose down

# Restart konkretnego serwisu
docker-compose restart payload

# Sprawdzenie logów
docker-compose logs -f payload
docker-compose logs -f mongo
docker-compose logs -f minio

# Status kontenerów
docker-compose ps
```

### 7. Ścieżki w projekcie
- **Projekt CMS**: `/Users/tomek/Development/regulujemy/payload-app`
- **Konfiguracje**: `/Users/tomek/Documents/Kamyki/Regulujemy.pl/_config`
- **Oryginalna zawartość**: `/Users/tomek/Documents/Kamyki/Regulujemy.pl`

### 8. Domyślne dane testowe
Po utworzeniu konta administratora w Payload CMS:
- Email: (twój email)
- Hasło: (wybierz silne hasło)

### 9. Bezpieczeństwo - DO ZMIANY W PRODUKCJI!
- [ ] Zmień `PAYLOAD_SECRET` na losowy ciąg znaków
- [ ] Zmień hasła MongoDB
- [ ] Zmień dane dostępowe MinIO
- [ ] Skonfiguruj HTTPS
- [ ] Ustaw właściwe CORS origins
- [ ] Włącz rate limiting
- [ ] Skonfiguruj backupy

### 10. Troubleshooting
Jeśli Payload nie działa:
1. Sprawdź logi: `docker-compose logs -f payload`
2. Zrestartuj kontenery: `docker-compose restart`
3. Przebuduj obrazy: `docker-compose build --no-cache`
4. Sprawdź czy porty są wolne: `lsof -i :3456`

---
**UWAGA**: To są dane dostępowe dla środowiska developerskiego.
NIE UŻYWAJ tych danych w produkcji!
