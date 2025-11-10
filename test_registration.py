import pytest
import sqlite3
import os
from registration.registration import create_db, add_user, authenticate_user, display_users

@pytest.fixture(scope="module")
def setup_database():
    """Testlerden önce veri tabanını oluşturmak ve testlerden sonra temizlemek için kullanılan test düzeneği."""
    create_db()
    yield
    try:
        os.remove('users.db')
    except PermissionError:
        pass

@pytest.fixture
def connection():
    """Test sırasında veri tabanı bağlantısı oluşturur ve testten sonra bağlantıyı kapatır."""
    conn = sqlite3.connect('users.db')
    yield conn
    conn.close()


def test_create_db(setup_database, connection):
    """Veri tabanı ve 'users' tablosunun oluşturulmasını test eder."""
    cursor = connection.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='users';")
    table_exists = cursor.fetchone()
    assert table_exists, "'users' tablosu veri tabanında bulunmalıdır."

def test_add_new_user(setup_database, connection):
    """Yeni bir kullanıcının eklenmesini test eder."""
    add_user('testuser', 'testuser@example.com', 'password123')
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM users WHERE username='testuser';")
    user = cursor.fetchone()
    assert user, "Kullanıcı veri tabanına eklenmiş olmalıdır."

def test_successful_authentication(setup_database):
    """
    Başarılı kullanıcı doğrulamasını test etme.
    Kayıtlı bir kullanıcının doğru şifre ile başarılı doğrulamasını test eder.
    """
    # Test için temiz bir kullanıcı adı seçelim
    username = 'auth_success_user'
    password = 'secure_pass_123'
    
    # 1. Kullanıcıyı ekle
    add_user(username, 'success@example.com', password)
    
    # 2. Doğrulama yap
    is_authenticated = authenticate_user(username, password)
    
    # 3. Sonucu kontrol et
    assert is_authenticated is True, "Doğru kullanıcı adı ve şifre ile doğrulama BAŞARILI olmalıdır."

def test_add_existing_user(setup_database, connection):
    """
    Var olan bir kullanıcı adıyla kullanıcı eklemeye çalışmayı test etme.
    Aynı kullanıcı adıyla tekrar kayıt işleminin başarısız olduğunu test eder.
    """
    username = 'duplicate_test_user'
    
    # 1. Kullanıcıyı ilk kez ekle
    # add_user fonksiyonunun başarılı kayıt durumunda True döndürdüğünü varsayıyoruz.
    initial_add_success = add_user(username, 'first@example.com', 'pass1')
    

    # 2. Aynı kullanıcı adıyla tekrar eklemeye çalış
    # add_user fonksiyonunun tekrar kaydı reddedip False döndürmesini bekliyoruz.
    second_add_success = add_user(username, 'second@example.com', 'pass2')

    
    # 3. İkinci eklemenin başarısız olduğunu kontrol et
    assert second_add_success is False, "Var olan kullanıcı adıyla ikinci kayıt başarısız olmalıdır."
    





# İşte yazabileceğiniz bazı testler:
"""
Var olmayan bir kullanıcıyla doğrulama yapmayı test etme.
Yanlış şifreyle doğrulama yapmayı test etme.
Kullanıcı listesinin doğru şekilde görüntülenmesini test etme.
"""


def test_authentication_non_existent_user(setup_database):
    """
    Var olmayan bir kullanıcı adıyla doğrulama yapmayı test etme.
    Sistemde kayıtlı olmayan bir kullanıcı adının doğrulamasının başarısız olduğunu test eder.
    """
    # Kayıtlı olmayan bir kullanıcı adı seç
    username = 'non_existent_user_xyz'
    password = 'any_password'
    
    # Doğrulama yap
    is_authenticated = authenticate_user(username, password)
    
    # Sonucu kontrol et
    assert is_authenticated is False, "Var olmayan kullanıcı doğrulama BAŞARISIZ olmalıdır."

def test_authentication_wrong_password(setup_database):
    """
    Kayıtlı bir kullanıcının yanlış şifreyle doğrulamasını test etme.
    """
    username = 'wrong_pass_user'
    correct_password = 'correct_password_456'
    wrong_password = 'incorrect_password_789'
    
    # 1. Kullanıcıyı doğru şifreyle ekle
    add_user(username, 'wrongpass@example.com', correct_password)
    
    # 2. Yanlış şifreyle doğrulama yap
    is_authenticated = authenticate_user(username, wrong_password)
    
    # 3. Sonucu kontrol et
    assert is_authenticated is False, "Yanlış şifre ile doğrulama BAŞARISIZ olmalıdır."

