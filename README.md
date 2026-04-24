<!-- BANNER / GIF -->

<p align="center">
  <img src="https://media1.tenor.com/m/ykMmQPdP-7sAAAAC/wrench-watch-dogs-2.gif" width="500px"/>
</p>

<h1 align="center">🔮 OLHO MALIGNO</h1>
<p align="center">
  <b>Ethical Security Scanner</b><br>
  <i>Hack the system. Secure the future.</i>
</p>

---

## 🚀 Funcionalidades

* 🕷️ Web Crawler automático
* 🔍 Scanner de vulnerabilidades:

  * XSS
  * SQL Injection
  * LFI
  * XXE
  * CORS misconfig
  * Headers ausentes
* 📊 Classificação por severidade
* 📁 Relatórios em:

  * JSON
  * TXT
  * HTML
* ⚡ Rate limiting
* 🔒 Safe Mode (não destrutivo)

---

## 📦 Instalação

```bash
git clone https://github.com/seu-user/olho-maligno.git
cd olho-maligno
pip install -r requirements.txt
```

ou:

```bash
pip install requests colorama tqdm pyfiglet pyyaml
```

---

## 🧠 Uso

### ▶️ Básico

```bash
python olho_maligno.py -u https://exemplo.com
```

---

### ⚙️ Avançado

```bash
python olho_maligno.py -u https://exemplo.com --depth 2 --delay 1 --rate 5 --format html
```

---

### 🔒 Seguro (recomendado)

```bash
python olho_maligno.py -u https://exemplo.com --scope exemplo.com --delay 2 --rate 2 --format html
```

---

## 🧩 Parâmetros

| Parâmetro | Descrição     |
| --------- | ------------- |
| -u        | URL alvo      |
| --depth   | Profundidade  |
| --delay   | Delay         |
| --rate    | Req/s         |
| --timeout | Timeout       |
| --format  | json/txt/html |
| --output  | Nome saída    |
| --scope   | Domínio       |
| --config  | YAML          |
| --no-safe | Desativa safe |

---

## 📊 Relatórios

```
scan_report_YYYYMMDD_HHMMSS.json
scan_report_YYYYMMDD_HHMMSS.txt
scan_report_YYYYMMDD_HHMMSS.html
```

---

## 🧪 Bug Bounty Example

```bash
python olho_maligno.py -u https://target.com --scope target.com --depth 2 --rate 3 --format html
```

---

## ⚠️ Aviso Legal

> Use apenas com autorização.

* ✔️ Pentest autorizado
* ✔️ Bug bounty
* ✔️ Labs

🚫 Nada ilegal.

---

## 👨‍💻 Autor

Felipe
💻 Cybersecurity | Pentest | Red Team

---

## ⭐ Contribuição

PRs são bem-vindos!

---

## 🧠 Roadmap

* [ ] Multithreading
* [ ] Subdomain scanner
* [ ] Integração bug bounty
* [ ] Dashboard web

---

<p align="center">
  <img src="https://capsule-render.vercel.app/api?type=waving&color=0:00ff00,100:003300&height=100&section=footer"/>
</p>
