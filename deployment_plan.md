# خطة نشر موقع Code Aura

## مقدمة

تهدف هذه الوثيقة إلى توفير خطة شاملة لنشر موقع Code Aura على بيئة الإنتاج. تتضمن الخطة إعداد البنية التحتية، تكوين الخوادم، نشر التطبيق، وإعداد المراقبة والصيانة.

## متطلبات البنية التحتية

### الخوادم

سنستخدم خوادم AWS EC2 لاستضافة الموقع:

1. **خادم الواجهة الأمامية**:
   - نوع الخادم: t3.small (2 vCPU، 2 GB RAM)
   - نظام التشغيل: Ubuntu 22.04 LTS
   - التخزين: 20 GB SSD

2. **خادم الباك إند**:
   - نوع الخادم: t3.medium (2 vCPU، 4 GB RAM)
   - نظام التشغيل: Ubuntu 22.04 LTS
   - التخزين: 30 GB SSD

3. **خادم قاعدة البيانات**:
   - نوع الخادم: t3.medium (2 vCPU، 4 GB RAM)
   - نظام التشغيل: Ubuntu 22.04 LTS
   - التخزين: 50 GB SSD

### خدمات إضافية

1. **AWS RDS** (اختياري): يمكن استخدام خدمة RDS لإدارة قاعدة البيانات بدلاً من تشغيلها على خادم منفصل.
2. **AWS S3**: لتخزين الملفات الثابتة والصور.
3. **AWS CloudFront**: لتوزيع المحتوى (CDN).
4. **AWS Route 53**: لإدارة DNS.
5. **AWS Certificate Manager**: لإدارة شهادات SSL.

## إعداد البنية التحتية

### 1. إنشاء شبكة VPC

```bash
# إنشاء VPC
aws ec2 create-vpc --cidr-block 10.0.0.0/16 --tag-specifications 'ResourceType=vpc,Tags=[{Key=Name,Value=CodeAuraVPC}]'

# إنشاء الشبكات الفرعية
aws ec2 create-subnet --vpc-id vpc-id --cidr-block 10.0.1.0/24 --availability-zone us-east-1a --tag-specifications 'ResourceType=subnet,Tags=[{Key=Name,Value=PublicSubnet1}]'
aws ec2 create-subnet --vpc-id vpc-id --cidr-block 10.0.2.0/24 --availability-zone us-east-1b --tag-specifications 'ResourceType=subnet,Tags=[{Key=Name,Value=PublicSubnet2}]'
aws ec2 create-subnet --vpc-id vpc-id --cidr-block 10.0.3.0/24 --availability-zone us-east-1a --tag-specifications 'ResourceType=subnet,Tags=[{Key=Name,Value=PrivateSubnet1}]'
aws ec2 create-subnet --vpc-id vpc-id --cidr-block 10.0.4.0/24 --availability-zone us-east-1b --tag-specifications 'ResourceType=subnet,Tags=[{Key=Name,Value=PrivateSubnet2}]'

# إنشاء بوابة إنترنت
aws ec2 create-internet-gateway --tag-specifications 'ResourceType=internet-gateway,Tags=[{Key=Name,Value=CodeAuraIGW}]'
aws ec2 attach-internet-gateway --internet-gateway-id igw-id --vpc-id vpc-id

# إنشاء جدول التوجيه
aws ec2 create-route-table --vpc-id vpc-id --tag-specifications 'ResourceType=route-table,Tags=[{Key=Name,Value=PublicRouteTable}]'
aws ec2 create-route --route-table-id rtb-id --destination-cidr-block 0.0.0.0/0 --gateway-id igw-id
aws ec2 associate-route-table --route-table-id rtb-id --subnet-id subnet-public1-id
aws ec2 associate-route-table --route-table-id rtb-id --subnet-id subnet-public2-id
```

### 2. إنشاء مجموعات الأمان

```bash
# مجموعة أمان للواجهة الأمامية
aws ec2 create-security-group --group-name frontend-sg --description "Security group for frontend server" --vpc-id vpc-id
aws ec2 authorize-security-group-ingress --group-id sg-frontend-id --protocol tcp --port 80 --cidr 0.0.0.0/0
aws ec2 authorize-security-group-ingress --group-id sg-frontend-id --protocol tcp --port 443 --cidr 0.0.0.0/0
aws ec2 authorize-security-group-ingress --group-id sg-frontend-id --protocol tcp --port 22 --cidr your-ip/32

# مجموعة أمان للباك إند
aws ec2 create-security-group --group-name backend-sg --description "Security group for backend server" --vpc-id vpc-id
aws ec2 authorize-security-group-ingress --group-id sg-backend-id --protocol tcp --port 5000 --source-group sg-frontend-id
aws ec2 authorize-security-group-ingress --group-id sg-backend-id --protocol tcp --port 22 --cidr your-ip/32

# مجموعة أمان لقاعدة البيانات
aws ec2 create-security-group --group-name db-sg --description "Security group for database server" --vpc-id vpc-id
aws ec2 authorize-security-group-ingress --group-id sg-db-id --protocol tcp --port 5432 --source-group sg-backend-id
aws ec2 authorize-security-group-ingress --group-id sg-db-id --protocol tcp --port 22 --cidr your-ip/32
```

### 3. إنشاء الخوادم

```bash
# إنشاء خادم الواجهة الأمامية
aws ec2 run-instances --image-id ami-ubuntu-22.04 --count 1 --instance-type t3.small --key-name your-key --security-group-ids sg-frontend-id --subnet-id subnet-public1-id --tag-specifications 'ResourceType=instance,Tags=[{Key=Name,Value=CodeAuraFrontend}]'

# إنشاء خادم الباك إند
aws ec2 run-instances --image-id ami-ubuntu-22.04 --count 1 --instance-type t3.medium --key-name your-key --security-group-ids sg-backend-id --subnet-id subnet-private1-id --tag-specifications 'ResourceType=instance,Tags=[{Key=Name,Value=CodeAuraBackend}]'

# إنشاء خادم قاعدة البيانات
aws ec2 run-instances --image-id ami-ubuntu-22.04 --count 1 --instance-type t3.medium --key-name your-key --security-group-ids sg-db-id --subnet-id subnet-private2-id --tag-specifications 'ResourceType=instance,Tags=[{Key=Name,Value=CodeAuraDatabase}]'
```

### 4. تخصيص عناوين IP ثابتة

```bash
# تخصيص عنوان IP ثابت للواجهة الأمامية
aws ec2 allocate-address --domain vpc
aws ec2 associate-address --instance-id i-frontend-id --allocation-id eipalloc-id
```

### 5. إنشاء خدمة S3 لتخزين الملفات

```bash
# إنشاء دلو S3
aws s3 mb s3://code-aura-assets
aws s3api put-bucket-policy --bucket code-aura-assets --policy file://bucket-policy.json
```

## إعداد الخوادم

### 1. إعداد خادم قاعدة البيانات

```bash
# الاتصال بالخادم
ssh -i your-key.pem ubuntu@db-server-ip

# تثبيت PostgreSQL
sudo apt update
sudo apt install -y postgresql postgresql-contrib

# تكوين PostgreSQL
sudo -u postgres psql -c "CREATE USER code_aura WITH PASSWORD 'secure_password';"
sudo -u postgres psql -c "CREATE DATABASE code_aura_db OWNER code_aura;"
sudo -u postgres psql -c "GRANT ALL PRIVILEGES ON DATABASE code_aura_db TO code_aura;"

# تكوين PostgreSQL للسماح بالاتصالات من خادم الباك إند
sudo nano /etc/postgresql/14/main/postgresql.conf
# تعديل listen_addresses = '*'

sudo nano /etc/postgresql/14/main/pg_hba.conf
# إضافة: host code_aura_db code_aura backend-server-ip/32 md5

# إعادة تشغيل PostgreSQL
sudo systemctl restart postgresql
```

### 2. إعداد خادم الباك إند

```bash
# الاتصال بالخادم
ssh -i your-key.pem ubuntu@backend-server-ip

# تثبيت الحزم المطلوبة
sudo apt update
sudo apt install -y python3-pip python3-venv nginx certbot python3-certbot-nginx

# إنشاء مستخدم التطبيق
sudo useradd -m -s /bin/bash code_aura
sudo mkdir -p /var/www/code_aura
sudo chown code_aura:code_aura /var/www/code_aura

# تبديل إلى مستخدم التطبيق
sudo su - code_aura

# نسخ كود الباك إند
git clone https://github.com/your-repo/code-aura-backend.git /var/www/code_aura

# إعداد البيئة الافتراضية
cd /var/www/code_aura
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# إنشاء ملف .env
cat > .env << EOF
FLASK_APP=src/main.py
FLASK_ENV=production
DATABASE_URL=postgresql://code_aura:secure_password@db-server-ip:5432/code_aura_db
SECRET_KEY=your_secret_key
OPENAI_API_KEY=your_openai_api_key
GOOGLE_CLIENT_ID=your_google_client_id
GOOGLE_CLIENT_SECRET=your_google_client_secret
FACEBOOK_CLIENT_ID=your_facebook_client_id
FACEBOOK_CLIENT_SECRET=your_facebook_client_secret
GITHUB_CLIENT_ID=your_github_client_id
GITHUB_CLIENT_SECRET=your_github_client_secret
EOF

# إنشاء ملف خدمة systemd
exit  # الخروج من مستخدم التطبيق
sudo nano /etc/systemd/system/code_aura.service
```

محتوى ملف خدمة systemd:

```ini
[Unit]
Description=Code Aura Backend
After=network.target

[Service]
User=code_aura
Group=code_aura
WorkingDirectory=/var/www/code_aura
Environment="PATH=/var/www/code_aura/venv/bin"
EnvironmentFile=/var/www/code_aura/.env
ExecStart=/var/www/code_aura/venv/bin/gunicorn --workers 4 --bind 0.0.0.0:5000 src.main:app

[Install]
WantedBy=multi-user.target
```

```bash
# تفعيل وتشغيل الخدمة
sudo systemctl enable code_aura
sudo systemctl start code_aura

# تكوين Nginx
sudo nano /etc/nginx/sites-available/code_aura
```

محتوى ملف تكوين Nginx:

```nginx
server {
    listen 80;
    server_name api.codeaura.com;

    location / {
        proxy_pass http://localhost:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

```bash
# تفعيل موقع Nginx
sudo ln -s /etc/nginx/sites-available/code_aura /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx

# إعداد شهادة SSL
sudo certbot --nginx -d api.codeaura.com
```

### 3. إعداد خادم الواجهة الأمامية

```bash
# الاتصال بالخادم
ssh -i your-key.pem ubuntu@frontend-server-ip

# تثبيت الحزم المطلوبة
sudo apt update
sudo apt install -y nginx certbot python3-certbot-nginx

# إنشاء مستخدم التطبيق
sudo useradd -m -s /bin/bash code_aura
sudo mkdir -p /var/www/code_aura
sudo chown code_aura:code_aura /var/www/code_aura

# نسخ ملفات الواجهة الأمامية المبنية
# (يفترض أنك قمت ببناء الواجهة الأمامية محليًا)
scp -i your-key.pem -r ./code_aura_frontend/dist/* ubuntu@frontend-server-ip:/var/www/code_aura/

# تكوين Nginx
sudo nano /etc/nginx/sites-available/code_aura
```

محتوى ملف تكوين Nginx:

```nginx
server {
    listen 80;
    server_name codeaura.com www.codeaura.com;
    root /var/www/code_aura;
    index index.html;

    # تكوين Gzip
    gzip on;
    gzip_types text/plain text/css application/json application/javascript text/xml application/xml application/xml+rss text/javascript;
    gzip_comp_level 6;
    gzip_min_length 1000;

    # تكوين التخزين المؤقت
    location ~* \.(jpg|jpeg|png|gif|ico|css|js)$ {
        expires 1y;
        add_header Cache-Control "public, max-age=31536000, immutable";
    }

    location / {
        try_files $uri $uri/ /index.html;
    }
}
```

```bash
# تفعيل موقع Nginx
sudo ln -s /etc/nginx/sites-available/code_aura /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx

# إعداد شهادة SSL
sudo certbot --nginx -d codeaura.com -d www.codeaura.com
```

## إعداد DNS

سنستخدم AWS Route 53 لإدارة DNS:

1. إنشاء منطقة مستضافة:
```bash
aws route53 create-hosted-zone --name codeaura.com --caller-reference $(date +%s)
```

2. إضافة سجلات DNS:
```bash
# سجل A للنطاق الرئيسي
aws route53 change-resource-record-sets --hosted-zone-id your-hosted-zone-id --change-batch '{
  "Changes": [
    {
      "Action": "CREATE",
      "ResourceRecordSet": {
        "Name": "codeaura.com",
        "Type": "A",
        "TTL": 300,
        "ResourceRecords": [
          {
            "Value": "frontend-server-ip"
          }
        ]
      }
    }
  ]
}'

# سجل A للنطاق الفرعي www
aws route53 change-resource-record-sets --hosted-zone-id your-hosted-zone-id --change-batch '{
  "Changes": [
    {
      "Action": "CREATE",
      "ResourceRecordSet": {
        "Name": "www.codeaura.com",
        "Type": "A",
        "TTL": 300,
        "ResourceRecords": [
          {
            "Value": "frontend-server-ip"
          }
        ]
      }
    }
  ]
}'

# سجل A للنطاق الفرعي api
aws route53 change-resource-record-sets --hosted-zone-id your-hosted-zone-id --change-batch '{
  "Changes": [
    {
      "Action": "CREATE",
      "ResourceRecordSet": {
        "Name": "api.codeaura.com",
        "Type": "A",
        "TTL": 300,
        "ResourceRecords": [
          {
            "Value": "backend-server-ip"
          }
        ]
      }
    }
  ]
}'
```

## نشر التطبيق

### 1. نشر قاعدة البيانات

```bash
# الاتصال بخادم قاعدة البيانات
ssh -i your-key.pem ubuntu@db-server-ip

# تشغيل سكريبت تهيئة قاعدة البيانات
sudo -u postgres psql code_aura_db < /path/to/schema.sql

# تشغيل سكريبت تعبئة البيانات الأولية
sudo -u postgres psql code_aura_db < /path/to/seed_data.sql
```

### 2. نشر الباك إند

```bash
# الاتصال بخادم الباك إند
ssh -i your-key.pem ubuntu@backend-server-ip

# تحديث الكود
cd /var/www/code_aura
sudo -u code_aura git pull

# تحديث التبعيات
sudo -u code_aura bash -c "source venv/bin/activate && pip install -r requirements.txt"

# تشغيل ترحيلات قاعدة البيانات
sudo -u code_aura bash -c "source venv/bin/activate && flask db upgrade"

# إعادة تشغيل الخدمة
sudo systemctl restart code_aura
```

### 3. نشر الواجهة الأمامية

```bash
# بناء الواجهة الأمامية محليًا
cd code_aura_frontend
npm run build

# نسخ الملفات المبنية إلى الخادم
scp -i your-key.pem -r dist/* ubuntu@frontend-server-ip:/var/www/code_aura/
```

## إعداد المراقبة والصيانة

### 1. إعداد Prometheus و Grafana للمراقبة

```bash
# تثبيت Prometheus على خادم المراقبة
sudo apt update
sudo apt install -y prometheus

# تكوين Prometheus
sudo nano /etc/prometheus/prometheus.yml
```

محتوى ملف تكوين Prometheus:

```yaml
global:
  scrape_interval: 15s

scrape_configs:
  - job_name: 'code_aura_backend'
    static_configs:
      - targets: ['backend-server-ip:5000']
  
  - job_name: 'code_aura_frontend'
    static_configs:
      - targets: ['frontend-server-ip:80']
  
  - job_name: 'code_aura_database'
    static_configs:
      - targets: ['db-server-ip:9187']
```

```bash
# تثبيت Grafana
sudo apt install -y grafana

# تفعيل وتشغيل الخدمات
sudo systemctl enable prometheus
sudo systemctl start prometheus
sudo systemctl enable grafana-server
sudo systemctl start grafana-server
```

### 2. إعداد النسخ الاحتياطي التلقائي

```bash
# إنشاء سكريبت النسخ الاحتياطي
sudo nano /usr/local/bin/backup_database.sh
```

محتوى سكريبت النسخ الاحتياطي:

```bash
#!/bin/bash
BACKUP_DIR="/var/backups/code_aura"
TIMESTAMP=$(date +"%Y%m%d_%H%M%S")
BACKUP_FILE="$BACKUP_DIR/code_aura_db_$TIMESTAMP.sql"

# إنشاء دليل النسخ الاحتياطي إذا لم يكن موجودًا
mkdir -p $BACKUP_DIR

# إنشاء نسخة احتياطية من قاعدة البيانات
pg_dump -h db-server-ip -U code_aura -d code_aura_db -f $BACKUP_FILE

# ضغط ملف النسخة الاحتياطية
gzip $BACKUP_FILE

# نسخ النسخة الاحتياطية إلى S3
aws s3 cp $BACKUP_FILE.gz s3://code-aura-backups/

# الاحتفاظ بآخر 7 نسخ احتياطية فقط
find $BACKUP_DIR -name "code_aura_db_*.sql.gz" -type f -mtime +7 -delete
```

```bash
# جعل السكريبت قابل للتنفيذ
sudo chmod +x /usr/local/bin/backup_database.sh

# إضافة مهمة cron للنسخ الاحتياطي اليومي
echo "0 2 * * * /usr/local/bin/backup_database.sh" | sudo tee -a /etc/crontab
```

### 3. إعداد تحديثات الأمان التلقائية

```bash
# تثبيت unattended-upgrades
sudo apt install -y unattended-upgrades apt-listchanges

# تكوين unattended-upgrades
sudo nano /etc/apt/apt.conf.d/50unattended-upgrades
```

محتوى ملف تكوين unattended-upgrades:

```
Unattended-Upgrade::Allowed-Origins {
    "${distro_id}:${distro_codename}";
    "${distro_id}:${distro_codename}-security";
    "${distro_id}ESMApps:${distro_codename}-apps-security";
    "${distro_id}ESM:${distro_codename}-infra-security";
};

Unattended-Upgrade::Package-Blacklist {
};

Unattended-Upgrade::Automatic-Reboot "true";
Unattended-Upgrade::Automatic-Reboot-Time "02:00";
```

```bash
# تفعيل التحديثات التلقائية
sudo nano /etc/apt/apt.conf.d/20auto-upgrades
```

محتوى ملف تكوين auto-upgrades:

```
APT::Periodic::Update-Package-Lists "1";
APT::Periodic::Download-Upgradeable-Packages "1";
APT::Periodic::AutocleanInterval "7";
APT::Periodic::Unattended-Upgrade "1";
```

## قائمة التحقق قبل الإطلاق

قبل إطلاق الموقع رسميًا، يجب التحقق من النقاط التالية:

1. **اختبار الوظائف الأساسية**:
   - تسجيل المستخدمين وتسجيل الدخول
   - عرض وتصفح الدورات
   - إجراء الاختبارات
   - استخدام محرر الأكواد وأدوات الذكاء الاصطناعي
   - لوحة تحكم الأدمن

2. **اختبار الأمان**:
   - التحقق من تشفير HTTPS
   - التحقق من حماية نقاط نهاية API
   - التحقق من تشفير كلمات المرور

3. **اختبار الأداء**:
   - قياس وقت تحميل الصفحات
   - اختبار الموقع تحت الحمل

4. **اختبار التوافق**:
   - اختبار الموقع على متصفحات مختلفة
   - اختبار الموقع على أجهزة مختلفة

5. **التحقق من SEO**:
   - التحقق من الوسوم الوصفية
   - التحقق من خريطة الموقع
   - التحقق من البيانات المنظمة

6. **التحقق من المراقبة والنسخ الاحتياطي**:
   - التحقق من عمل أدوات المراقبة
   - التحقق من عمل النسخ الاحتياطي التلقائي

## خطة الإطلاق

1. **الإطلاق التجريبي (Soft Launch)**:
   - إطلاق الموقع لمجموعة محدودة من المستخدمين
   - جمع التعليقات وإصلاح المشاكل

2. **الإطلاق الكامل**:
   - فتح الموقع للجمهور
   - مراقبة الأداء والاستقرار

3. **ما بعد الإطلاق**:
   - جمع تعليقات المستخدمين
   - تحديث وتحسين الموقع بناءً على التعليقات

## خطة الطوارئ

في حالة حدوث مشاكل أثناء الإطلاق، يجب اتباع الخطوات التالية:

1. **مشاكل في الباك إند**:
   - التحقق من سجلات الخطأ
   - إعادة تشغيل خدمة الباك إند
   - استعادة النسخة الاحتياطية الأخيرة من قاعدة البيانات إذا لزم الأمر

2. **مشاكل في الواجهة الأمامية**:
   - التحقق من سجلات Nginx
   - إعادة نشر الإصدار السابق إذا لزم الأمر

3. **مشاكل في قاعدة البيانات**:
   - التحقق من سجلات PostgreSQL
   - استعادة النسخة الاحتياطية الأخيرة

4. **مشاكل في الأداء**:
   - زيادة موارد الخوادم
   - تفعيل التخزين المؤقت الإضافي

## الخلاصة

توفر خطة النشر هذه إطارًا شاملاً لنشر موقع Code Aura على بيئة الإنتاج. من خلال اتباع هذه الخطة، يمكننا ضمان إطلاق ناجح وسلس للموقع مع تقليل المخاطر والمشاكل المحتملة.

