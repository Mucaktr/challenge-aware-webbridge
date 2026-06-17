# Challenge Aware WebBridge

Turn browser verification interruptions into calm, recoverable workflows.

Tarayici dogrulama kesintilerini sakin ve toparlanabilir is akislarina donusturun.

## English

### Overview

Challenge Aware WebBridge is a publishable Codex wrapper repository for a Codex skill built around Kimi WebBridge sessions. It helps an agent detect browser verification interstitials, pause cleanly for user handoff, preserve session state, and resume the original task once the challenge page clears.

This repository is intentionally designed for safe, human-in-the-loop browsing workflows. It is not an anti-bot bypass package.

### Why this exists

Browser automation regularly stalls on pages such as:

- Cloudflare Turnstile screens
- "Checking your browser" interstitials
- "Verify you are human" checkpoints
- localized challenge pages such as `Bir dakika lutfen`

In many real workflows, the right move is not to force the page. The right move is to recognize the challenge, keep browser state intact, let the user complete the check, and continue smoothly.

### What this repository includes

- A Codex skill folder ready to install
- Helper scripts for Kimi WebBridge daemon requests
- Detection logic for verification pages
- A polling helper that waits for challenge clearance
- Reference guidance for safe handoff and user messaging
- GitHub-ready documentation and licensing

### What it does

- Detects likely verification pages from URL, title, visible text, and accessibility content
- Standardizes Kimi WebBridge daemon calls with a Windows-safe UTF-8 request helper
- Waits for challenge clearance without losing browser session state
- Gives agents clean, user-friendly handoff language
- Resumes the original browsing task once the page becomes usable again

### What it does not do

- It does not claim to solve CAPTCHAs
- It does not bypass Cloudflare or other anti-bot systems
- It does not replay tokens or fabricate challenge responses
- It does not present itself as an evasion or stealth tool

### Suggested GitHub description

> A Codex skill for Kimi WebBridge that detects browser verification pages, hands off safely to the user, and resumes the workflow once the challenge clears.

### Suggested short pitch

> Turn verification interruptions into graceful browser handoffs instead of broken automation.

### Suggested release blurb

> Challenge Aware WebBridge gives Codex a calm, reusable playbook for challenge pages: detect the interstitial, hand off cleanly to the user, preserve the session, and resume the task when the page clears.

### Suggested GitHub topics

`codex` `agent-skill` `browser-automation` `kimi-webbridge` `human-in-the-loop` `challenge-detection`

### Repository layout

```text
challenge-aware-webbridge/
|-- .gitignore
|-- LICENSE
|-- README.md
`-- challenge-aware-webbridge/
    |-- LICENSE.txt
    |-- SKILL.md
    |-- agents/
    |   `-- openai.yaml
    |-- references/
    |   |-- challenge-patterns.md
    |   `-- user-messaging.md
    `-- scripts/
        |-- detect_verification_page.py
        |-- wait_for_clearance.py
        `-- webbridge_request.py
```

### Install

Copy the `challenge-aware-webbridge/` folder into your Codex skills directory.

Typical location:

```text
$CODEX_HOME/skills
```

If `CODEX_HOME` is not set, use:

```text
~/.codex/skills
```

Restart Codex after installation so the new skill is picked up.

### Example prompts

- `Use $challenge-aware-webbridge to detect whether this site is stuck on a browser verification page and wait for me to clear it.`
- `Use $challenge-aware-webbridge to keep this Kimi WebBridge session alive while I complete the manual browser check.`
- `Use $challenge-aware-webbridge to classify this page, hand off if needed, and resume once the site is accessible.`

### Script quick start

Send a daemon request:

```bash
python challenge-aware-webbridge/scripts/webbridge_request.py \
  --session demo-task \
  --action snapshot \
  --args-json '{}'
```

Probe the current page:

```bash
python challenge-aware-webbridge/scripts/detect_verification_page.py \
  --session demo-task \
  --pretty
```

Wait until the challenge clears:

```bash
python challenge-aware-webbridge/scripts/wait_for_clearance.py \
  --session demo-task \
  --timeout-sec 120 \
  --pretty
```

### Publishing checklist

- Review the repo description above and tailor it to your audience
- Replace the copyright holder in `LICENSE` and `challenge-aware-webbridge/LICENSE.txt` if needed
- Push the repository as-is, or choose a different public GitHub slug if you want a stronger brand
- Add a release note using the short pitch if you want a stronger first impression

### Safety position

This project is intentionally scoped to safe verification-aware browsing workflows:

- detect
- hand off
- wait
- resume

It is not an anti-bot bypass package.

## Turkce

### Genel bakis

Challenge Aware WebBridge, Kimi WebBridge oturumlari icin hazirlanmis, yayinlanabilir bir Codex skill reposudur. Ajanin tarayici dogrulama ara sayfalarini algilamasina, kullaniciya kontrollu sekilde devretmesine, oturum durumunu korumasina ve dogrulama kalkinca ayni goreve devam etmesine yardim eder.

Bu repo bilincli olarak guvenli ve kullanici kontrollu tarayici akislari icin tasarlandi. Anti-bot engellerini asma paketi degildir.

### Neden var

Tarayici otomasyonu su tip sayfalarda sikca takilir:

- Cloudflare Turnstile ekranlari
- "Checking your browser" ara sayfalari
- "Verify you are human" dogrulama adimlari
- `Bir dakika lutfen` benzeri yerellesmis challenge ekranlari

Gercek dunyadaki pek cok akista dogru hareket sayfayi zorlamak degildir. Dogru hareket challenge'i taniyip tarayici durumunu korumak, kullanicinin kontrolden cikmadan dogrulamayi tamamlamasini beklemek ve sonra kaldigi yerden devam etmektir.

### Bu repo neler icerir

- Kuruluma hazir bir Codex skill klasoru
- Kimi WebBridge daemon istekleri icin yardimci betikler
- Dogrulama sayfasi tespiti mantigi
- Challenge kalkana kadar bekleyen bir polling yardimcisi
- Guvenli devretme ve kullanici mesajlari icin referans dokumanlar
- GitHub'a hazir dokumantasyon ve lisanslama

### Ne yapar

- URL, baslik, gorunen metin ve erisilebilirlik iceriginden muhtemel dogrulama sayfalarini algilar
- Windows guvenli UTF-8 istek yardimcisi ile Kimi WebBridge daemon cagri formatini standartlastirir
- Tarayici oturum durumunu kaybetmeden challenge kalkisini bekler
- Ajanlara temiz ve kullanici dostu devir mesajlari verir
- Sayfa tekrar kullanilabilir oldugunda asli goreve geri doner

### Ne yapmaz

- CAPTCHA cozdigunu iddia etmez
- Cloudflare veya diger anti-bot sistemlerini bypass etmez
- Token tekrar oynatma ya da sahte challenge cevabi uretmez
- Kendini kacak, stealth veya engel asma araci olarak konumlandirmaz

### Onerilen GitHub aciklamasi

> Kimi WebBridge icin, tarayici dogrulama sayfalarini algilayan, kullaniciya guvenli sekilde devreden ve challenge kalkinca gorevi surduren bir Codex skill'i.

### Onerilen kisa tanitim

> Dogrulama kesintilerini kirik otomasyon yerine kontrollu tarayici devrine cevirin.

### Onerilen release metni

> Challenge Aware WebBridge, Codex'e challenge sayfalari icin tekrar kullanilabilir bir is akisi kazandirir: ara sayfayi algila, kullaniciya temiz sekilde devret, oturumu koru ve sayfa acilinca goreve devam et.

### Kurulum

`challenge-aware-webbridge/` klasorunu Codex skill dizininize kopyalayin.

Tipik konum:

```text
$CODEX_HOME/skills
```

`CODEX_HOME` tanimli degilse:

```text
~/.codex/skills
```

Kurulumdan sonra Codex'i yeniden baslatin.

### Ornek komutlar

- `Use $challenge-aware-webbridge to detect whether this site is stuck on a browser verification page and wait for me to clear it.`
- `Use $challenge-aware-webbridge to keep this Kimi WebBridge session alive while I complete the manual browser check.`
- `Use $challenge-aware-webbridge to classify this page, hand off if needed, and resume once the site is accessible.`

### Yayinlama kontrol listesi

- README icindeki aciklamalari kendi hedef kitlenize gore son kez duzenleyin
- Gerekirse `LICENSE` ve `challenge-aware-webbridge/LICENSE.txt` icindeki telif adini guncelleyin
- Isterseniz herkese acik GitHub slug'ini daha markali bir adla degistirebilirsiniz
- Ilk release notunda kisa tanitim metnini kullanin

### Guvenlik durusu

Bu proje bilerek su akisa odaklanir:

- algila
- kullaniciya devret
- bekle
- devam et

Yani bu repo bir anti-bot asma paketi degildir.
