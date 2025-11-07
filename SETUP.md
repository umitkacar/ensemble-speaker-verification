# 🔧 Setup Guide - Hatch + Pre-commit

## ⚡ Quick Setup (2 dakika)

```bash
# 1. Hatch'i yükle
pip install hatch

# 2. Development ortamını oluştur
hatch shell

# 3. Pre-commit hooks'ları kur
pre-commit install

# 4. Test et (opsiyonel)
hatch run test

# ✅ Hazırsınız!
```

---

## 📦 **Hatch Kullanımı**

### Ortam Yönetimi

```bash
# Virtual environment'a gir
hatch shell

# Environment'tan çık
exit

# Tüm environment'ları listele
hatch env show

# Environment'ı temizle
hatch env prune
```

### Test & Kalite Kontrolleri

```bash
# Testleri çalıştır
hatch run test

# Coverage ile testler
hatch run test-cov
# Sonuç: htmlcov/index.html

# Kod formatla (Black)
hatch run format

# Format kontrolü
hatch run format-check

# Lint (Ruff)
hatch run lint

# Type check (MyPy)
hatch run type-check

# 🔥 HEPSİNİ ÇALIŞTIR
hatch run all
```

### Build & Publish

```bash
# Package oluştur (wheel + sdist)
hatch build

# Temizle
hatch clean

# PyPI'a yükle (hazır olunca)
hatch publish

# Test PyPI'a yükle (önce test için)
hatch publish -r test
```

### CLI'ı Çalıştır

```bash
# Hatch environment'ında
hatch run speech-verify --help
hatch run speech-verify verify audio1.wav audio2.wav

# Ya da environment'a girdikten sonra
hatch shell
speech-verify --help
```

---

## 🪝 **Pre-commit Kullanımı**

### Kurulum

```bash
# Pre-commit hooks'ları kur
pre-commit install

# Hooks'ları güncelle
pre-commit autoupdate
```

### Manuel Çalıştırma

```bash
# Tüm dosyalarda çalıştır
pre-commit run --all-files

# Sadece staged dosyalarda
pre-commit run

# Belirli bir hook'u çalıştır
pre-commit run black --all-files
pre-commit run ruff --all-files
pre-commit run mypy --all-files
```

### Kurulu Hooks

✅ **trailing-whitespace** - Satır sonlarındaki boşlukları temizle
✅ **end-of-file-fixer** - Dosya sonuna newline ekle
✅ **check-yaml** - YAML syntax kontrolü
✅ **check-toml** - TOML syntax kontrolü
✅ **check-json** - JSON syntax kontrolü
✅ **check-added-large-files** - Büyük dosya kontrolü (max 1MB)
✅ **black** - Python kod formatı
✅ **ruff** - Fast Python linter
✅ **mypy** - Static type checker
✅ **isort** - Import sıralama
✅ **pyupgrade** - Python syntax upgrade (py38+)
✅ **bandit** - Security checker
✅ **pydocstyle** - Docstring style checker

### Hook'ları Atla (Gerekirse)

```bash
# Tüm hooks'ları atla
git commit -m "message" --no-verify

# Belirli bir hook'u devre dışı bırak (geçici)
SKIP=mypy git commit -m "WIP: testing"
```

---

## 📝 **pyproject.toml Yapılandırması**

### Dependency Grupları

```bash
# Sadece core bağımlılıklar
pip install .

# Development bağımlılıkları
pip install ".[dev]"

# Visualization bağımlılıkları
pip install ".[viz]"

# Audio utilities
pip install ".[audio]"

# 🔥 HER ŞEY
pip install ".[all]"
```

### Editable Installation

```bash
# Geliştirme için (önerilen)
pip install -e ".[all]"

# Şimdi kodda değişiklik yaptığınızda
# yeniden install etmeye gerek yok!
```

---

## 🎯 **Tipik Workflow**

### İlk Kurulum

```bash
# 1. Repository'yi klonla
git clone https://github.com/umitkacar/Speech-Verification-Ensemble.git
cd Speech-Verification-Ensemble

# 2. Hatch kur ve environment oluştur
pip install hatch
hatch shell

# 3. Pre-commit hooks kur
pre-commit install

# 4. Test et
hatch run test
```

### Günlük Geliştirme

```bash
# 1. Branch oluştur
git checkout -b feature/my-feature

# 2. Hatch environment'a gir
hatch shell

# 3. Kod yaz...

# 4. Testleri çalıştır
hatch run test

# 5. Kod kalitesini kontrol et
hatch run all

# 6. Commit (pre-commit otomatik çalışır)
git add .
git commit -m "feat: add awesome feature"

# 7. Push
git push origin feature/my-feature
```

### Hızlı Kontroller

```bash
# Quick check pipeline
hatch run format    # 1. Format kodu
hatch run lint      # 2. Lint kontrol
hatch run type-check # 3. Type check
hatch run test      # 4. Testleri çalıştır

# Ya da hepsini bir komutla
hatch run all
```

---

## 🔧 **Makefile Shortcuts**

Daha kolay kullanım için Makefile komutları:

```bash
make help           # Tüm komutları göster
make dev-install    # Development kurulumu
make test           # Testleri çalıştır
make test-cov       # Coverage ile testler
make lint           # Lint
make format         # Format
make all-checks     # Tüm kontroller
make clean          # Temizlik
make pre-commit     # Pre-commit tüm dosyalarda
```

---

## 🐛 **Troubleshooting**

### Hatch bulunamıyor

```bash
pip install --upgrade hatch
# veya
pipx install hatch
```

### Pre-commit çalışmıyor

```bash
# Yeniden kur
pre-commit uninstall
pre-commit install

# Cache temizle
pre-commit clean
```

### MyPy hataları

```bash
# Bazı kütüphaneler type stubs'ı olmayabilir
# pyproject.toml'da ignore_missing_imports = true ayarlandı
```

### Import hataları

```bash
# Editable mode'da kur
pip install -e .

# Ya da hatch environment'ı yeniden oluştur
hatch env prune
hatch shell
```

---

## 📊 **Hatch Environment Detayları**

### Default Environment

```toml
[tool.hatch.envs.default]
dependencies = [
    "pytest>=7.0.0",
    "pytest-cov>=4.0.0",
    "black>=23.0.0",
    "ruff>=0.1.0",
    "mypy>=1.0.0",
]
```

### Custom Scripts

```toml
[tool.hatch.envs.default.scripts]
test = "pytest {args:tests}"
test-cov = "pytest --cov --cov-report=html"
lint = "ruff check src tests"
format = "black src tests"
type-check = "mypy src"
all = ["format", "lint", "type-check", "test-cov"]
```

---

## 🎨 **Code Style Kuralları**

### Black

- Line length: 88
- Python 3.8+ target
- Otomatik formatting

### Ruff

- Fast Python linter
- pycodestyle, pyflakes, isort, bugbear, comprehensions
- Auto-fix özelliği

### MyPy

- Static type checking
- Python 3.8 compatibility
- Strict mode (kademeli)

### isort

- Import sıralama
- Black compatible
- Known first-party: speech_verification

---

## 🚀 **CI/CD Hazırlığı**

### GitHub Actions için

```yaml
# .github/workflows/test.yml
name: Tests

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-python@v4
        with:
          python-version: '3.11'
      - name: Install Hatch
        run: pip install hatch
      - name: Run tests
        run: hatch run test-cov
      - name: Run checks
        run: hatch run all
```

---

## 💡 **İpuçları**

1. **Her zaman hatch shell kullan** - Bağımlılıklar otomatik yönetilir
2. **Pre-commit'i aktif tut** - Commit öncesi otomatik kontrol
3. **make all-checks çalıştır** - Push öncesi son kontrol
4. **hatch run test-cov kullan** - Coverage raporu ile test et
5. **Editable install yap** - `pip install -e .` değişiklikler anında aktif

---

## 📚 **Daha Fazla Bilgi**

- [Hatch Docs](https://hatch.pypa.io/)
- [Pre-commit Docs](https://pre-commit.com/)
- [Black Docs](https://black.readthedocs.io/)
- [Ruff Docs](https://docs.astral.sh/ruff/)
- [MyPy Docs](https://mypy.readthedocs.io/)

---

**Happy Coding! 🎉**
