# Kimlik Doğrulama Sistemi

SQLite veritabanı kullanan, komut satırı tabanlı kullanıcı kayıt ve giriş sistemi.

## Gereksinimler

- Python 3.6+
- pytest (sadece testler için)

## Kurulum

```bash
# Repoyu klonlayın
git clone https://github.com/taco-ay/kimlik-dogrulama.git
cd kimlik-dogrulama

# Test bağımlılığını yükleyin
pip install pytest
```

## Çalıştırma

```bash
python3 registration.py
```

Uygulama başladığında kayıtlı kullanıcıları listeler, ardından bir menü sunar:

```
1. Giriş yap
2. Kayıt ol
```

### Kayıt Olma

Seçenek `2` ile yeni hesap oluşturabilirsiniz. Kullanıcı adı, e-posta ve şifre girmeniz istenir.

### Giriş Yapma

Seçenek `1` ile mevcut hesabınıza giriş yapabilirsiniz. Kullanıcı adı ve şifre doğrulanır.

## Testleri Çalıştırma

```bash
pytest test_registration.py -v
```

## Proje Yapısı

```
kimlik-dogrulama/
├── registration.py       # Ana uygulama (veritabanı, kayıt, giriş mantığı)
├── test_registration.py  # Pytest test suite
└── users.db              # SQLite veritabanı (uygulama ilk çalıştığında oluşur)
```

## Özellikler

- Yeni kullanıcı kaydı (kullanıcı adı, e-posta, şifre)
- Kullanıcı adı ve şifre ile kimlik doğrulama
- Kayıtlı kullanıcıları listeleme
- Tekrar eden kullanıcı adı engelleme
- SQLite ile kalıcı veri saklama
