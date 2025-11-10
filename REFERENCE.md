# 🚀 Quick Reference Card

## ⚡ Hızlı Komutlar

```bash
# KURULUM
pip install hatch
hatch shell
pre-commit install

# TEST & KALİTE
hatch run all              # Hepsini çalıştır (önerilen!)
hatch run format           # Black formatla
hatch run lint             # Ruff lint
hatch run type-check       # MyPy type check
hatch run test             # Pytest test
hatch run test-cov         # Coverage ile test

# ALTERNATIF (Make)
make all-checks            # Tüm kontroller
make test-cov              # Coverage ile test
make format                # Format kodu
make clean                 # Temizlik

# PRE-COMMIT
pre-commit run --all-files # Tüm dosyalarda çalıştır
pre-commit autoupdate      # Hook'ları güncelle
git commit                 # Otomatik çalışır!

# BUILD & PUBLISH
hatch build                # Package oluştur
hatch publish              # PyPI'a yükle
```

## 🔧 Yapılandırılmış Araçlar

| Araç | Versiyon | Amaç | Komut |
|------|----------|------|-------|
| **Hatch** | Latest | Build system | `hatch run <script>` |
| **Black** | v23.12.1 | Code formatter | `hatch run format` |
| **Ruff** | v0.1.9 | Fast linter | `hatch run lint` |
| **MyPy** | v1.8.0 | Type checker | `hatch run type-check` |
| **pytest** | v7.0+ | Testing | `hatch run test` |
| **pytest-cov** | v4.0+ | Coverage | `hatch run test-cov` |
| **isort** | v5.13.2 | Import sorter | (pre-commit) |
| **pyupgrade** | v3.15.0 | Syntax upgrade | (pre-commit) |
| **Bandit** | v1.7.6 | Security | (pre-commit) |
| **pydocstyle** | v6.3.0 | Docstrings | (pre-commit) |

## 📋 Standartlar

- **Line Length**: 88 (Black)
- **Python Version**: 3.8+
- **Type Hints**: 100% coverage
- **Docstrings**: Google style
- **Import Style**: isort (Black compatible)
- **Coverage**: Branch coverage enabled

## 🎯 Workflow

```bash
# 1. Kod yaz
vim src/speech_verification/...

# 2. Format ve kontrol
hatch run format
hatch run lint
hatch run type-check

# 3. Test
hatch run test-cov

# 4. Commit (pre-commit otomatik!)
git add .
git commit -m "feat: awesome feature"

# 5. Push
git push
```

## 🪝 Pre-commit Hooks

15+ otomatik hook:
- ✅ Trailing whitespace
- ✅ EOF fixer
- ✅ YAML/TOML/JSON check
- ✅ Large files check
- ✅ Black formatting
- ✅ Ruff linting
- ✅ MyPy type check
- ✅ isort imports
- ✅ pyupgrade syntax
- ✅ Bandit security
- ✅ pydocstyle docs

## 📚 Dokümantasyon

- `SETUP.md` - Detaylı kurulum ve kullanım
- `QUICKSTART.md` - Hızlı başlangıç
- `CONTRIBUTING.md` - Developer kılavuzu
- `README.md` - Proje dokümantasyonu

## 💡 İpuçları

1. **`hatch run all`** her push öncesi çalıştır
2. **Pre-commit** her commit'te otomatik çalışır
3. **Coverage raporu**: `htmlcov/index.html`
4. **Editable install**: `pip install -e .`
5. **Hatch shell**: Bağımlılıkları otomatik yönetir

---

**v2.0.0** | Ultra-modern Python Package | 2024-2025 Standards
