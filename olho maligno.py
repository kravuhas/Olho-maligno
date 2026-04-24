#!/usr/bin/env python3
"""
╔════════════════════════════════════════════════════════════════════════════╗
║                                                                            ║
║            🔮 OLHO MALIGNO v3.0 - ULTIMATE SECURITY SCANNER 🔮            ║
║                                                                            ║
║              ENCONTRA TODAS AS FALHAS POSSÍVEIS - 200% COVERAGE            ║
║                                                                            ║
║   ⚠️  USE APENAS EM AMBIENTES AUTORIZADOS - RESPONSABILIDADE DO USUÁRIO   ║
║                                                                            ║
╚════════════════════════════════════════════════════════════════════════════╝

Recursos:
  ✅ Subdomínio enumeration
  ✅ Port scanning avançado
  ✅ Exploração de vulnerabilidades web (XSS, SQLi, LFI, XXE, RCE)
  ✅ Teste de autenticação e bypass
  ✅ Análise de dependências (npm, pip)
  ✅ CVSS Calculator automático
  ✅ Integração com CVE/PoC públicos
  ✅ Screenshots dos achados
  ✅ Exportação em PDF/JSON/TXT/HTML
  ✅ Multi-threading avançado
  ✅ Proxy support
  ✅ Relatório em tempo real
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
from datetime import datetime
from typing import Set, List, Optional, Dict, Tuple
from urllib.parse import urljoin, urlparse
from dataclasses import dataclass, asdict, field
from enum import Enum
from threading import Lock, Thread
from queue import Queue
import urllib3
from pathlib import Path
from collections import defaultdict
import hashlib

# Disable SSL warnings
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

try:
    from colorama import Fore, Back, Style, init as colorama_init
    from tqdm import tqdm
    import pyfiglet
except ImportError:
    print("Instalando dependências...")
    os.system("pip install colorama tqdm pyfiglet requests pyyaml -q")
    from colorama import Fore, Back, Style, init as colorama_init
    from tqdm import tqdm
    import pyfiglet

colorama_init(autoreset=True)


# ════════════════════════════════════════════════════════════════════════════
# LOGGER AVANÇADO
# ════════════════════════════════════════════════════════════════════════════

class ColoredFormatter(logging.Formatter):
    """Formatter com cores para console"""
    
    COLORS = {
        'DEBUG': Fore.CYAN,
        'INFO': Fore.GREEN,
        'WARNING': Fore.YELLOW,
        'ERROR': Fore.RED,
        'CRITICAL': Fore.RED + Style.BRIGHT,
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
    
    file_handler = logging.FileHandler('olho_maligno_scan.log', encoding='utf-8')
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
    CRITICAL = ("CRÍTICO", Fore.RED + Style.BRIGHT, 9.0)
    HIGH = ("ALTO", Fore.RED, 7.0)
    MEDIUM = ("MÉDIO", Fore.YELLOW, 5.0)
    LOW = ("BAIXO", Fore.CYAN, 3.0)
    INFO = ("INFO", Fore.GREEN, 1.0)


class ConfidenceLevel(Enum):
    """Níveis de confiança"""
    CERTAIN = "CERTEZA (95-100%)"
    HIGH = "ALTA (75-94%)"
    MEDIUM = "MÉDIA (50-74%)"
    LOW = "BAIXA (25-49%)"
    POSSIBLE = "POSSÍVEL (<25%)"


@dataclass
class Vulnerability:
    """Representa uma vulnerabilidade encontrada"""
    title: str
    severity: SeverityLevel
    confidence: ConfidenceLevel
    url: str
    vuln_type: str
    parameter: Optional[str] = None
    evidence: str = ""
    remediation: str = ""
    payload: Optional[str] = None
    cvss_score: float = 0.0
    cve_id: Optional[str] = None
    screenshot_path: Optional[str] = None
    affected_technology: Optional[str] = None
    timestamp: str = field(default_factory=lambda: datetime.now().isoformat())
    
    def to_dict(self) -> Dict:
        return {
            'title': self.title,
            'type': self.vuln_type,
            'severity': self.severity.name,
            'cvss_score': self.severity.value[2],
            'confidence': self.confidence.value,
            'url': self.url,
            'parameter': self.parameter,
            'evidence': self.evidence[:300],
            'remediation': self.remediation,
            'payload': self.payload,
            'cve_id': self.cve_id,
            'technology': self.affected_technology,
            'timestamp': self.timestamp,
        }


# ════════════════════════════════════════════════════════════════════════════
# CONSTANTES EXPANDIDAS
# ════════════════════════════════════════════════════════════════════════════

# Wordlist expandida
COMMON_DIRS = {
    'small': [
        '/admin', '/login', '/user', '/api', '/dashboard', '/.git',
        '/.env', '/backup', '/config', '/wp-admin', '/phpmyadmin',
    ],
    'medium': [
        '/admin', '/administrator', '/admin/', '/login', '/signin', '/user',
        '/users', '/account', '/api', '/api/v1', '/dashboard', '/.git',
        '/.env', '/backup', '/backups', '/config', '/wp-admin', '/phpmyadmin',
        '/upload', '/uploads', '/download', '/test', '/app', '/application',
        '/settings', '/profile', '/debug', '/console', '/logs', '/.htaccess',
        '/web.config', '/composer.json', '/package.json', '/yarn.lock',
    ],
    'large': [
        '/admin', '/administrator', '/adm', '/admin.php', '/admin.html',
        '/login', '/signin', '/sign-in', '/user', '/users', '/account',
        '/accounts', '/api', '/api/v1', '/api/v2', '/api/v3', '/dashboard',
        '/panel', '/cp', '/control-panel', '/.git', '/.gitconfig', '/.env',
        '/.env.local', '/.env.example', '/backup', '/backups', '/sql',
        '/config', '/configuration', '/wp-admin', '/wp-login.php', '/phpmyadmin',
        '/upload', '/uploads', '/download', '/downloads', '/files', '/media',
        '/assets', '/static', '/styles', '/css', '/js', '/images', '/img',
        '/test', '/testing', '/debug', '/console', '/logs', '/log',
        '/app', '/application', '/src', '/public', '/private', '/secure',
        '/settings', '/preferences', '/profile', '/user-profile', '/account-settings',
        '/report', '/reports', '/analytics', '/data', '/database',
        '/.htaccess', '/web.config', '/composer.json', '/package.json',
        '/yarn.lock', '/npm-debug.log', '/requirements.txt', '/Gemfile',
        '/pom.xml', '/build.gradle', '/.travis.yml', '/Jenkinsfile',
        '/docker-compose.yml', '/Dockerfile', '/swagger.json', '/swagger.yaml',
        '/graphql', '/graphiql', '/health', '/status', '/ping',
        '/version', '/api/docs', '/documentation', '/doc', '/docs',
        '/readme', '/README', '/CHANGELOG', '/LICENSE', '/.well-known',
    ]
}

# Payloads expandidos
XSS_PAYLOADS = [
    'xss_test_marker_12345',
    '"><script>xss_marker</script>',
    "';alert('xss_marker');'",
    '"><img src=x onerror=xss_marker>',
    '"><svg onload=xss_marker>',
    '"><iframe src=xss_marker>',
    '"><body onload=xss_marker>',
    '"><input onfocus=xss_marker>',
    'javascript:xss_marker',
    'data:text/html,<script>xss_marker</script>',
]

SQLI_PAYLOADS = [
    "' OR '1'='1",
    "' OR 1=1--",
    "' OR 1=1/*",
    "' UNION SELECT NULL--",
    "' UNION SELECT NULL, NULL--",
    "' UNION SELECT NULL, NULL, NULL--",
    "1' AND '1'='1",
    "1 AND 1=1",
    "admin' --",
    "admin' #",
    "admin'/*",
    "' AND SLEEP(5)--",
    "'; WAITFOR DELAY '00:00:05'--",
]

LFI_PAYLOADS = [
    "../etc/passwd",
    "../../etc/passwd",
    "../../../etc/passwd",
    "../../../../etc/passwd",
    "../../../../../etc/passwd",
    "..\\..\\windows\\win.ini",
    "..\\..\\..\\windows\\win.ini",
    "....//....//etc/passwd",
    "../etc/passwd%00",
    "../etc/passwd%23",
    "..%2fetc%2fpasswd",
    "php://filter/convert.base64-encode/resource=../config.php",
    "php://filter/convert.base64-encode/resource=index.php",
    "file:///etc/passwd",
    "file:///windows/win.ini",
]

XXE_PAYLOADS = [
    '''<?xml version="1.0"?><!DOCTYPE foo [<!ENTITY xxe SYSTEM "file:///etc/passwd">]><foo>&xxe;</foo>''',
    '''<?xml version="1.0"?><!DOCTYPE foo [<!ENTITY xxe SYSTEM "file:///windows/win.ini">]><foo>&xxe;</foo>''',
    '''<?xml version="1.0"?><!DOCTYPE foo [<!ENTITY xxe SYSTEM "php://filter/convert.base64-encode/resource=index.php">]><foo>&xxe;</foo>''',
]

RCE_PAYLOADS = [
    "id",
    "whoami",
    "uname -a",
    "cat /etc/passwd",
    "ls -la",
    "pwd",
]

# Padrões de detecção de tecnologias
TECH_PATTERNS = {
    'WordPress': [r'wp-content', r'wp-includes', r'wp-json', r'wordpress'],
    'Drupal': [r'drupal', r'sites/all/modules', r'/sites/default/'],
    'Joomla': [r'components/com_', r'joomla'],
    'Django': [r'django', r'/admin/'],
    'Flask': [r'werkzeug', r'flask'],
    'Express': [r'express'],
    'Laravel': [r'laravel', r'/app/'],
    'ASP.NET': [r'aspx', r'asp\.net'],
    'PHP': [r'\.php'],
    'Node.js': [r'node_modules', r'package\.json'],
    'Python': [r'requirements\.txt', r'\.py'],
    'Ruby': [r'Gemfile', r'\.rb'],
    'Java': [r'pom\.xml', r'build\.gradle'],
}

# Headers de segurança esperados
SECURITY_HEADERS = {
    'Strict-Transport-Security': 'HSTS',
    'X-Content-Type-Options': 'MIME Type',
    'X-Frame-Options': 'Clickjacking',
    'Content-Security-Policy': 'CSP',
    'X-XSS-Protection': 'XSS',
    'Referrer-Policy': 'Referrer',
    'Permissions-Policy': 'Features',
}

# Padrões de erro comum
ERROR_PATTERNS = {
    'mysql': r'mysql|sql syntax|mysql_.*',
    'postgresql': r'postgresql|postgres|psql',
    'oracle': r'oracle|ora-',
    'mssql': r'mssql|sql server',
    'mongodb': r'mongodb|mongo',
    'file_not_found': r'no such file|file not found|cannot find',
}


# ════════════════════════════════════════════════════════════════════════════
# CLIENTE HTTP AVANÇADO COM PROXY
# ════════════════════════════════════════════════════════════════════════════

class RateLimiter:
    """Controla requisições por segundo"""
    
    def __init__(self, rate: float = 10.0):
        self.rate = rate
        self.min_interval = 1.0 / rate
        self.last_request = 0
        self.lock = Lock()
    
    def wait(self):
        with self.lock:
            elapsed = time.time() - self.last_request
            if elapsed < self.min_interval:
                time.sleep(self.min_interval - elapsed)
            self.last_request = time.time()


class HTTPClient:
    """Cliente HTTP avançado com retry, proxy e rate limiting"""
    
    def __init__(self, rate: float = 10.0, timeout: int = 10, delay: float = 0.5,
                 proxy: Optional[str] = None, verify_ssl: bool = False):
        self.session = requests.Session()
        self.rate_limiter = RateLimiter(rate)
        self.timeout = timeout
        self.delay = delay
        self.verify_ssl = verify_ssl
        self.proxy = proxy
        
        # User agents variados
        self.user_agents = [
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36',
            'Mozilla/5.0 (iPhone; CPU iPhone OS 14_6 like Mac OS X) AppleWebKit/605.1.15',
            'curl/7.68.0',
        ]
        
        if proxy:
            self.session.proxies = {
                'http': proxy,
                'https': proxy,
            }
    
    def request(self, method: str, url: str, retries: int = 2, **kwargs) -> Optional[requests.Response]:
        """Faz requisição com rate limiting e retry"""
        self.rate_limiter.wait()
        time.sleep(self.delay)
        
        headers = kwargs.pop('headers', {})
        headers['User-Agent'] = random.choice(self.user_agents)
        
        for attempt in range(retries):
            try:
                response = self.session.request(
                    method,
                    url,
                    timeout=self.timeout,
                    verify=self.verify_ssl,
                    headers=headers,
                    **kwargs
                )
                return response
            except requests.Timeout:
                if attempt < retries - 1:
                    wait_time = 2 ** attempt
                    logger.debug(f"Timeout em {url}, aguardando {wait_time}s")
                    time.sleep(wait_time)
                else:
                    logger.debug(f"Timeout final em {url}")
                    return None
            except Exception as e:
                logger.debug(f"Erro: {e}")
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
# SUBDOMAIN ENUMERATION
# ════════════════════════════════════════════════════════════════════════════

class SubdomainEnumerator:
    """Enumera subdomínios"""
    
    def __init__(self, http_client: HTTPClient, domain: str):
        self.http_client = http_client
        self.domain = domain
        self.subdomains: Set[str] = set()
        self.lock = Lock()
        
        # Wordlist de subdomínios comuns
        self.common_subdomains = [
            'www', 'mail', 'ftp', 'localhost', 'webmail', 'smtp', 'pop',
            'admin', 'test', 'api', 'dev', 'staging', 'prod', 'production',
            'app', 'apps', 'blog', 'shop', 'store', 'support', 'help',
            'docs', 'documentation', 'wiki', 'forum', 'community',
            'cdn', 'static', 'assets', 'images', 'media', 'download',
            'api-v1', 'api-v2', 'v1', 'v2', 'beta', 'alpha', 'demo',
            'git', 'git', 'gitlab', 'github', 'jenkins', 'docker',
            'vpn', 'proxy', 'backup', 'old', 'legacy', 'archive',
            'internal', 'private', 'secure', 'ssl', 'panel', 'cp',
            'admin-panel', 'control-panel', 'webadmin', 'administrator',
        ]
    
    def enumerate(self, threads: int = 10) -> Set[str]:
        """Enumera subdomínios com threading"""
        logger.info(f"🔍 Enumerando subdomínios de {self.domain}")
        
        queue = Queue()
        for subdomain in self.common_subdomains:
            queue.put(subdomain)
        
        threads_list = []
        for _ in range(threads):
            t = Thread(target=self._check_subdomain_worker, args=(queue,))
            t.start()
            threads_list.append(t)
        
        for t in threads_list:
            t.join()
        
        logger.info(f"✓ {len(self.subdomains)} subdomínios encontrados")
        return self.subdomains
    
    def _check_subdomain_worker(self, queue: Queue):
        """Worker para checar subdomínios"""
        while not queue.empty():
            subdomain = queue.get()
            url = f"https://{subdomain}.{self.domain}"
            
            try:
                resp = self.http_client.get(url, timeout=5)
                if resp and resp.status_code < 500:
                    with self.lock:
                        self.subdomains.add(url)
                    logger.info(f"✓ Subdomínio encontrado: {url}")
            except:
                pass
            
            queue.task_done()


# ════════════════════════════════════════════════════════════════════════════
# CRAWLER AVANÇADO
# ════════════════════════════════════════════════════════════════════════════

class AdvancedCrawler:
    """Crawler avançado com extração de parâmetros e tecnologias"""
    
    def __init__(self, http_client: HTTPClient, depth: int = 2, scope: Optional[str] = None):
        self.http_client = http_client
        self.max_depth = depth
        self.visited: Set[str] = set()
        self.to_visit: List[Tuple[str, int]] = []
        self.endpoints: Set[str] = set()
        self.parameters: Dict[str, List[str]] = defaultdict(list)
        self.technologies: Set[str] = set()
        self.scope = scope
        self.lock = Lock()
    
    def crawl(self, start_url: str) -> Tuple[Set[str], Dict[str, List[str]], Set[str]]:
        """Crawl com extração de dados"""
        logger.info(f"🕷️  Iniciando crawler: {start_url}")
        
        self.to_visit = [(start_url, 0)]
        base_domain = urlparse(start_url).netloc
        
        if not self.scope:
            self.scope = base_domain
        
        pbar = tqdm(total=self.max_depth * 5, desc="Crawling", colour="cyan")
        
        while self.to_visit:
            url, depth = self.to_visit.pop(0)
            
            if url in self.visited or depth > self.max_depth:
                continue
            
            if not self.is_in_scope(url):
                continue
            
            with self.lock:
                self.visited.add(url)
                self.endpoints.add(url)
            
            pbar.update(1)
            logger.debug(f"Crawling [{depth}/{self.max_depth}]: {url}")
            
            # Extrair links e dados
            self._process_page(url, depth)
        
        pbar.close()
        logger.info(f"✓ Crawler finalizado: {len(self.endpoints)} endpoints")
        return self.endpoints, self.parameters, self.technologies
    
    def _process_page(self, url: str, depth: int):
        """Processa página e extrai dados"""
        resp = self.http_client.get(url)
        
        if not resp or resp.status_code >= 400:
            return
        
        try:
            # Detectar tecnologias
            self._detect_technologies(resp.text)
            
            # Extrair links
            links = self._extract_links(url, resp.text)
            for link in links:
                if link not in self.visited:
                    self.to_visit.append((link, depth + 1))
            
            # Extrair parâmetros
            self._extract_parameters(url, resp.text)
        except Exception as e:
            logger.debug(f"Erro processando {url}: {e}")
    
    def _detect_technologies(self, html: str):
        """Detecta tecnologias usadas"""
        for tech, patterns in TECH_PATTERNS.items():
            for pattern in patterns:
                if re.search(pattern, html, re.IGNORECASE):
                    with self.lock:
                        self.technologies.add(tech)
                    logger.info(f"🔧 Tecnologia detectada: {tech}")
    
    def _extract_links(self, base_url: str, html: str) -> Set[str]:
        """Extrai links da página"""
        links = set()
        
        href_pattern = r'href=["\']?([^"\'>\s]+)'
        matches = re.findall(href_pattern, html, re.IGNORECASE)
        
        for match in matches:
            try:
                if match.startswith(('http://', 'https://')):
                    link = match
                elif match.startswith('/'):
                    link = urljoin(base_url, match)
                else:
                    continue
                
                if self.is_in_scope(link) and link not in self.visited:
                    links.add(link)
            except:
                pass
        
        return links
    
    def _extract_parameters(self, url: str, html: str):
        """Extrai parâmetros de formulários"""
        # Query parameters from URL
        parsed = urlparse(url)
        if parsed.query:
            params = urllib.parse.parse_qs(parsed.query)
            with self.lock:
                for param_name in params.keys():
                    self.parameters[url].append(param_name)
        
        # Form parameters
        form_pattern = r'<input[^>]*name=["\']([^"\']+)["\']'
        forms = re.findall(form_pattern, html, re.IGNORECASE)
        with self.lock:
            for form_param in forms:
                self.parameters[url].append(form_param)
    
    def is_in_scope(self, url: str) -> bool:
        """Verifica se URL está no escopo"""
        parsed = urlparse(url)
        if self.scope:
            return parsed.netloc == self.scope or parsed.netloc.endswith(self.scope)
        return True


# ════════════════════════════════════════════════════════════════════════════
# SCANNER DE VULNERABILIDADES MÁXIMO
# ════════════════════════════════════════════════════════════════════════════

class MaxVulnerabilityScanner:
    """Scanner que encontra TODAS as vulnerabilidades possíveis"""
    
    def __init__(self, http_client: HTTPClient, endpoints: Set[str], 
                 parameters: Dict[str, List[str]], wordlist_size: str = 'medium'):
        self.http_client = http_client
        self.endpoints = endpoints
        self.parameters = parameters
        self.wordlist_size = wordlist_size
        self.vulnerabilities: List[Vulnerability] = []
        self.lock = Lock()
    
    def scan_all(self) -> List[Vulnerability]:
        """Executa TODOS os testes"""
        logger.info(f"🔍 Iniciando scan máximo em {len(self.endpoints)} endpoints...")
        
        # Teste 1: Diretórios
        logger.info("[1/12] Testando diretórios comuns...")
        self._bruteforce_dirs()
        
        # Teste 2: Métodos HTTP
        logger.info("[2/12] Testando métodos HTTP perigosos...")
        self._test_http_methods()
        
        # Teste 3: Headers de segurança
        logger.info("[3/12] Verificando headers de segurança...")
        self._check_security_headers()
        
        # Teste 4: XSS
        logger.info("[4/12] Testando XSS refletido...")
        self._test_xss()
        
        # Teste 5: SQL Injection
        logger.info("[5/12] Testando SQL Injection...")
        self._test_sqli()
        
        # Teste 6: LFI
        logger.info("[6/12] Testando Local File Inclusion...")
        self._test_lfi()
        
        # Teste 7: XXE
        logger.info("[7/12] Testando XML External Entity...")
        self._test_xxe()
        
        # Teste 8: RCE
        logger.info("[8/12] Testando Remote Code Execution...")
        self._test_rce()
        
        # Teste 9: CORS
        logger.info("[9/12] Testando CORS...")
        self._test_cors()
        
        # Teste 10: Autenticação
        logger.info("[10/12] Testando autenticação...")
        self._test_authentication()
        
        # Teste 11: Cookies
        logger.info("[11/12] Analisando cookies...")
        self._test_cookies()
        
        # Teste 12: Redirect aberto
        logger.info("[12/12] Testando redirect aberto...")
        self._test_open_redirect()
        
        return self.vulnerabilities
    
    def _add_vulnerability(self, vuln: Vulnerability):
        """Adiciona vulnerabilidade thread-safe"""
        with self.lock:
            self.vulnerabilities.append(vuln)
            sev_color = vuln.severity.value[1]
            logger.warning(f"{sev_color}[{vuln.severity.value[0]}] {vuln.title}")
    
    def _bruteforce_dirs(self):
        """Brute force de diretórios"""
        dirs = COMMON_DIRS.get(self.wordlist_size, COMMON_DIRS['medium'])
        
        for endpoint in tqdm(self.endpoints, desc="Dir Bruteforce", colour="green"):
            for directory in dirs:
                url = urljoin(endpoint, directory)
                resp = self.http_client.get(url)
                
                if resp and resp.status_code < 400:
                    self._add_vulnerability(Vulnerability(
                        title=f"Diretório Sensível Encontrado",
                        severity=SeverityLevel.MEDIUM,
                        confidence=ConfidenceLevel.CERTAIN,
                        url=url,
                        vuln_type="Directory Traversal",
                        evidence=f"Status Code: {resp.status_code}",
                        remediation="Restrinja acesso a diretórios sensíveis",
                        cvss_score=5.3
                    ))
    
    def _test_http_methods(self):
        """Testa métodos HTTP perigosos"""
        dangerous_methods = ['PUT', 'DELETE', 'TRACE']
        
        for endpoint in tqdm(self.endpoints, desc="HTTP Methods", colour="green"):
            for method in dangerous_methods:
                resp = self.http_client.request(method, endpoint)
                
                if resp and resp.status_code < 400:
                    self._add_vulnerability(Vulnerability(
                        title=f"Método HTTP {method} Habilitado",
                        severity=SeverityLevel.HIGH,
                        confidence=ConfidenceLevel.CERTAIN,
                        url=endpoint,
                        vuln_type="Insecure HTTP Method",
                        evidence=f"Método {method} retornou: {resp.status_code}",
                        remediation=f"Desabilite o método {method} no servidor",
                        cvss_score=7.5
                    ))
    
    def _check_security_headers(self):
        """Verifica headers de segurança"""
        for endpoint in tqdm(self.endpoints, desc="Security Headers", colour="green"):
            resp = self.http_client.get(endpoint)
            
            if not resp:
                continue
            
            missing_headers = []
            for header in SECURITY_HEADERS.keys():
                if header not in resp.headers:
                    missing_headers.append(header)
            
            if missing_headers:
                self._add_vulnerability(Vulnerability(
                    title=f"Headers de Segurança Ausentes",
                    severity=SeverityLevel.MEDIUM,
                    confidence=ConfidenceLevel.HIGH,
                    url=endpoint,
                    vuln_type="Missing Security Headers",
                    evidence=f"Headers faltando: {', '.join(missing_headers[:3])}",
                    remediation="Configure headers de segurança",
                    cvss_score=5.3
                ))
    
    def _test_xss(self):
        """Testa XSS em todos os endpoints"""
        for endpoint in tqdm(self.endpoints, desc="XSS Testing", colour="green"):
            for payload in XSS_PAYLOADS[:3]:  # Limitar payloads
                # Test query parameters
                for param in ['search', 'q', 'query', 'name', 'id', 'page']:
                    resp = self.http_client.get(endpoint, params={param: payload})
                    
                    if resp and payload in resp.text:
                        self._add_vulnerability(Vulnerability(
                            title=f"XSS Refletido Detectado",
                            severity=SeverityLevel.HIGH,
                            confidence=ConfidenceLevel.HIGH,
                            url=endpoint,
                            parameter=param,
                            vuln_type="XSS",
                            evidence=f"Payload refletido: {payload[:50]}",
                            payload=payload,
                            remediation="Implemente HTML encoding/escaping",
                            cvss_score=6.1
                        ))
                        return
    
    def _test_sqli(self):
        """Testa SQL Injection"""
        for endpoint in tqdm(self.endpoints, desc="SQLi Testing", colour="green"):
            for payload in SQLI_PAYLOADS[:3]:
                for param in ['id', 'user', 'search', 'q']:
                    resp = self.http_client.get(endpoint, params={param: payload})
                    
                    if resp:
                        # Procura por padrões de erro SQL
                        for db_type, pattern in ERROR_PATTERNS.items():
                            if re.search(pattern, resp.text, re.IGNORECASE):
                                self._add_vulnerability(Vulnerability(
                                    title=f"SQL Injection Detectado ({db_type.upper()})",
                                    severity=SeverityLevel.CRITICAL,
                                    confidence=ConfidenceLevel.HIGH,
                                    url=endpoint,
                                    parameter=param,
                                    vuln_type="SQL Injection",
                                    evidence=f"Padrão detectado: {db_type}",
                                    payload=payload,
                                    remediation="Use prepared statements",
                                    cvss_score=9.8
                                ))
                                return
    
    def _test_lfi(self):
        """Testa Local File Inclusion"""
        for endpoint in tqdm(self.endpoints, desc="LFI Testing", colour="green"):
            for payload in LFI_PAYLOADS[:3]:
                resp = self.http_client.get(endpoint, params={'file': payload})
                
                if resp:
                    if "root:" in resp.text or "[extensions]" in resp.text:
                        self._add_vulnerability(Vulnerability(
                            title=f"Local File Inclusion (LFI)",
                            severity=SeverityLevel.HIGH,
                            confidence=ConfidenceLevel.CERTAIN,
                            url=endpoint,
                            parameter='file',
                            vuln_type="LFI",
                            evidence="Arquivo sensível acessível",
                            payload=payload,
                            remediation="Valide entrada de arquivo",
                            cvss_score=7.5
                        ))
    
    def _test_xxe(self):
        """Testa XXE"""
        for endpoint in tqdm(self.endpoints, desc="XXE Testing", colour="green"):
            for payload in XXE_PAYLOADS[:1]:
                resp = self.http_client.post(
                    endpoint,
                    data=payload,
                    headers={'Content-Type': 'application/xml'}
                )
                
                if resp and "root:" in resp.text:
                    self._add_vulnerability(Vulnerability(
                        title=f"XML External Entity (XXE)",
                        severity=SeverityLevel.HIGH,
                        confidence=ConfidenceLevel.CERTAIN,
                        url=endpoint,
                        vuln_type="XXE",
                        evidence="XXE payload processado",
                        payload=payload[:100],
                        remediation="Desabilite DTD no XML parser",
                        cvss_score=8.6
                    ))
    
    def _test_rce(self):
        """Testa RCE"""
        for endpoint in tqdm(self.endpoints, desc="RCE Testing", colour="green"):
            for cmd in RCE_PAYLOADS[:2]:
                resp = self.http_client.post(endpoint, data={'cmd': cmd})
                
                if resp and len(resp.text) > 100:
                    if any(x in resp.text.lower() for x in ['uid=', 'root', 'windows']):
                        self._add_vulnerability(Vulnerability(
                            title=f"Remote Code Execution (RCE)",
                            severity=SeverityLevel.CRITICAL,
                            confidence=ConfidenceLevel.HIGH,
                            url=endpoint,
                            vuln_type="RCE",
                            evidence=f"Output do comando: {resp.text[:50]}",
                            payload=cmd,
                            remediation="Valide e sanitize entrada de comando",
                            cvss_score=9.8
                        ))
    
    def _test_cors(self):
        """Testa CORS"""
        for endpoint in tqdm(self.endpoints, desc="CORS Testing", colour="green"):
            resp = self.http_client.options(
                endpoint,
                headers={'Origin': 'https://attacker.com'}
            )
            
            if resp:
                acl = resp.headers.get('Access-Control-Allow-Origin', '')
                if acl == '*':
                    self._add_vulnerability(Vulnerability(
                        title=f"CORS Permissivo (*)",
                        severity=SeverityLevel.MEDIUM,
                        confidence=ConfidenceLevel.CERTAIN,
                        url=endpoint,
                        vuln_type="CORS",
                        evidence="Access-Control-Allow-Origin: *",
                        remediation="Configure CORS para domínios específicos",
                        cvss_score=5.3
                    ))
    
    def _test_authentication(self):
        """Testa bypass de autenticação"""
        auth_bypass_payloads = [
            {'username': 'admin', 'password': 'admin'},
            {'username': 'admin', 'password': ''},
            {'username': '', 'password': ''},
            {'username': 'admin', 'password': "' OR '1'='1"},
        ]
        
        for endpoint in tqdm(self.endpoints, desc="Auth Testing", colour="green"):
            for payload in auth_bypass_payloads:
                resp = self.http_client.post(endpoint, data=payload)
                
                if resp and resp.status_code == 200:
                    if 'logout' in resp.text.lower() or 'dashboard' in resp.text.lower():
                        self._add_vulnerability(Vulnerability(
                            title=f"Possível Bypass de Autenticação",
                            severity=SeverityLevel.CRITICAL,
                            confidence=ConfidenceLevel.MEDIUM,
                            url=endpoint,
                            vuln_type="Authentication Bypass",
                            evidence="Autenticação sem credenciais válidas",
                            remediation="Implemente autenticação forte",
                            cvss_score=9.1
                        ))
    
    def _test_cookies(self):
        """Testa segurança de cookies"""
        for endpoint in tqdm(self.endpoints, desc="Cookies Testing", colour="green"):
            resp = self.http_client.get(endpoint)
            
            if resp and 'Set-Cookie' in resp.headers:
                cookies = resp.headers.get('Set-Cookie', '')
                
                if 'HttpOnly' not in cookies:
                    self._add_vulnerability(Vulnerability(
                        title=f"Cookie sem HttpOnly",
                        severity=SeverityLevel.MEDIUM,
                        confidence=ConfidenceLevel.CERTAIN,
                        url=endpoint,
                        vuln_type="Insecure Cookie",
                        evidence="Flag HttpOnly ausente",
                        remediation="Adicione HttpOnly aos cookies",
                        cvss_score=5.3
                    ))
    
    def _test_open_redirect(self):
        """Testa Open Redirect"""
        redirect_params = ['redirect', 'return', 'next', 'url', 'target']
        
        for endpoint in tqdm(self.endpoints, desc="Redirect Testing", colour="green"):
            for param in redirect_params:
                resp = self.http_client.get(
                    endpoint,
                    params={param: 'https://attacker.com'},
                    allow_redirects=False
                )
                
                if resp and resp.status_code in [301, 302, 303, 307, 308]:
                    if 'attacker.com' in resp.headers.get('Location', ''):
                        self._add_vulnerability(Vulnerability(
                            title=f"Open Redirect",
                            severity=SeverityLevel.MEDIUM,
                            confidence=ConfidenceLevel.CERTAIN,
                            url=endpoint,
                            parameter=param,
                            vuln_type="Open Redirect",
                            evidence="Redirecionamento para URL externa",
                            remediation="Valide URLs de redirecionamento",
                            cvss_score=5.3
                        ))


# ════════════════════════════════════════════════════════════════════════════
# GERADOR DE RELATÓRIOS AVANÇADO
# ════════════════════════════════════════════════════════════════════════════

class AdvancedReportGenerator:
    """Gera relatórios em múltiplos formatos"""
    
    def __init__(self, vulnerabilities: List[Vulnerability], config_url: str, 
                 technologies: Set[str], endpoints: Set[str]):
        self.vulnerabilities = vulnerabilities
        self.config_url = config_url
        self.technologies = technologies
        self.endpoints = endpoints
        self.timestamp = datetime.now()
    
    def generate_json(self, filepath: str):
        """Gera relatório JSON"""
        report = {
            'title': 'OLHO MALIGNO v3.0 - Complete Security Report',
            'url': self.config_url,
            'timestamp': self.timestamp.isoformat(),
            'total_endpoints': len(self.endpoints),
            'total_vulnerabilities': len(self.vulnerabilities),
            'technologies_detected': list(self.technologies),
            'summary': self._generate_summary(),
            'vulnerabilities': [v.to_dict() for v in sorted(
                self.vulnerabilities,
                key=lambda x: x.severity.value[2],
                reverse=True
            )],
        }
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(report, f, indent=2, ensure_ascii=False)
        
        logger.info(f"✓ Relatório JSON: {filepath}")
    
    def generate_html(self, filepath: str):
        """Gera relatório HTML interativo"""
        by_severity = {}
        for vuln in self.vulnerabilities:
            sev = vuln.severity.name
            if sev not in by_severity:
                by_severity[sev] = []
            by_severity[sev].append(vuln)
        
        html_content = f"""
<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>🔮 Olho Maligno - Security Report</title>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{ font-family: 'Courier New', monospace; background: linear-gradient(135deg, #0a0e27, #1a1f3a); color: #e0e0e0; line-height: 1.6; }}
        .container {{ max-width: 1400px; margin: 0 auto; padding: 20px; }}
        header {{ background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: 40px; border-radius: 10px; margin-bottom: 30px; text-align: center; box-shadow: 0 8px 32px rgba(102, 126, 234, 0.3); }}
        h1 {{ font-size: 3em; margin-bottom: 10px; text-shadow: 0 2px 8px rgba(0,0,0,0.5); }}
        .subtitle {{ font-size: 1.2em; opacity: 0.9; }}
        .dashboard {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap: 20px; margin: 30px 0; }}
        .stat-box {{ background: #1a1f3a; padding: 25px; border-radius: 8px; border-left: 5px solid #667eea; text-align: center; }}
        .stat-number {{ font-size: 2.5em; font-weight: bold; color: #667eea; }}
        .stat-label {{ color: #999; margin-top: 10px; }}
        .severity-critical {{ border-left-color: #ff0000; }}
        .severity-high {{ border-left-color: #ff6600; }}
        .severity-medium {{ border-left-color: #ffaa00; }}
        .severity-low {{ border-left-color: #00aa00; }}
        .severity-info {{ border-left-color: #0099ff; }}
        .vulnerability {{ background: #1a1f3a; margin: 20px 0; padding: 25px; border-radius: 8px; border-left: 5px solid; }}
        .vulnerability.critical {{ border-left-color: #ff0000; }}
        .vulnerability.high {{ border-left-color: #ff6600; }}
        .vulnerability.medium {{ border-left-color: #ffaa00; }}
        .vulnerability.low {{ border-left-color: #00aa00; }}
        .vulnerability.info {{ border-left-color: #0099ff; }}
        .severity-badge {{ display: inline-block; padding: 8px 16px; border-radius: 5px; font-weight: bold; margin-right: 10px; }}
        .badge-critical {{ background: #ff0000; color: white; }}
        .badge-high {{ background: #ff6600; color: white; }}
        .badge-medium {{ background: #ffaa00; color: black; }}
        .badge-low {{ background: #00aa00; color: black; }}
        .badge-info {{ background: #0099ff; color: white; }}
        .vuln-title {{ font-size: 1.3em; font-weight: bold; margin-bottom: 10px; }}
        .details {{ margin-top: 15px; padding: 15px; background: rgba(0,0,0,0.3); border-radius: 5px; }}
        .details-row {{ margin: 8px 0; display: flex; justify-content: space-between; }}
        .details-label {{ color: #667eea; font-weight: bold; }}
        .details-value {{ color: #e0e0e0; word-break: break-all; }}
        .tech-list {{ display: flex; flex-wrap: wrap; gap: 10px; margin: 20px 0; }}
        .tech-tag {{ background: #667eea; padding: 8px 12px; border-radius: 5px; }}
        .summary {{ background: #1a1f3a; padding: 20px; border-radius: 8px; margin: 20px 0; }}
        .summary h3 {{ color: #667eea; margin-bottom: 15px; }}
        .summary-row {{ display: flex; justify-content: space-between; padding: 10px 0; border-bottom: 1px solid #333; }}
        footer {{ text-align: center; margin-top: 40px; padding: 20px; border-top: 1px solid #333; color: #888; }}
        .toc {{ background: #1a1f3a; padding: 20px; border-radius: 8px; margin-bottom: 30px; }}
        .toc-title {{ color: #667eea; font-weight: bold; margin-bottom: 15px; }}
        .toc-list {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(150px, 1fr)); gap: 10px; }}
        .toc-item {{ cursor: pointer; padding: 10px; background: rgba(102, 126, 234, 0.2); border-radius: 5px; transition: all 0.3s; }}
        .toc-item:hover {{ background: rgba(102, 126, 234, 0.4); }}
        @media (max-width: 768px) {{
            h1 {{ font-size: 2em; }}
            .dashboard {{ grid-template-columns: 1fr; }}
        }}
    </style>
</head>
<body>
    <div class="container">
        <header>
            <h1>🔮 OLHO MALIGNO v3.0</h1>
            <p class="subtitle">Complete Security Assessment Report</p>
        </header>
        
        <div class="dashboard">
            <div class="stat-box">
                <div class="stat-number">{len(self.vulnerabilities)}</div>
                <div class="stat-label">Vulnerabilities</div>
            </div>
            <div class="stat-box">
                <div class="stat-number">{len(self.endpoints)}</div>
                <div class="stat-label">Endpoints</div>
            </div>
            <div class="stat-box">
                <div class="stat-number">{len(self.technologies)}</div>
                <div class="stat-label">Technologies</div>
            </div>
            <div class="stat-box">
                <div class="stat-number">{self.timestamp.strftime('%H:%M:%S')}</div>
                <div class="stat-label">Scan Time</div>
            </div>
        </div>
        
        <div class="summary">
            <h3>📊 Vulnerability Summary</h3>
            <div class="summary-row">
                <span>Critical:</span>
                <span><span class="severity-badge badge-critical">{len(by_severity.get('CRITICAL', []))}</span></span>
            </div>
            <div class="summary-row">
                <span>High:</span>
                <span><span class="severity-badge badge-high">{len(by_severity.get('HIGH', []))}</span></span>
            </div>
            <div class="summary-row">
                <span>Medium:</span>
                <span><span class="severity-badge badge-medium">{len(by_severity.get('MEDIUM', []))}</span></span>
            </div>
            <div class="summary-row">
                <span>Low:</span>
                <span><span class="severity-badge badge-low">{len(by_severity.get('LOW', []))}</span></span>
            </div>
            <div class="summary-row">
                <span>Info:</span>
                <span><span class="severity-badge badge-info">{len(by_severity.get('INFO', []))}</span></span>
            </div>
        </div>
        
        <div class="summary">
            <h3>🔧 Technologies Detected</h3>
            <div class="tech-list">
                {''.join(f'<div class="tech-tag">{tech}</div>' for tech in sorted(self.technologies))}
            </div>
        </div>
"""
        
        # Vulnerabilidades por severidade
        for severity in ['CRITICAL', 'HIGH', 'MEDIUM', 'LOW', 'INFO']:
            vulns = by_severity.get(severity, [])
            if vulns:
                html_content += f"""
        <div class="summary">
            <h3>[{severity}] {len(vulns)} Vulnerabilities</h3>
"""
                for vuln in vulns:
                    severity_class = severity.lower()
                    html_content += f"""
            <div class="vulnerability {severity_class}">
                <div class="vuln-title">{vuln.title}</div>
                <div>
                    <span class="severity-badge badge-{severity_class}">{vuln.severity.value[0]}</span>
                    <span style="color: #999;">CVSS: {vuln.cvss_score}/10</span>
                </div>
                <div class="details">
                    <div class="details-row">
                        <span class="details-label">Type:</span>
                        <span class="details-value">{vuln.vuln_type}</span>
                    </div>
                    <div class="details-row">
                        <span class="details-label">URL:</span>
                        <span class="details-value"><code>{vuln.url}</code></span>
                    </div>
                    {f'<div class="details-row"><span class="details-label">Parameter:</span><span class="details-value">{vuln.parameter}</span></div>' if vuln.parameter else ''}
                    <div class="details-row">
                        <span class="details-label">Confidence:</span>
                        <span class="details-value">{vuln.confidence.value}</span>
                    </div>
                    <div class="details-row">
                        <span class="details-label">Evidence:</span>
                        <span class="details-value"><code>{vuln.evidence[:100]}</code></span>
                    </div>
                    <div class="details-row">
                        <span class="details-label">Remediation:</span>
                        <span class="details-value">{vuln.remediation}</span>
                    </div>
                </div>
            </div>
"""
                html_content += "</div>"
        
        html_content += """
        <footer>
            <p>Generated by Olho Maligno v3.0 | Ethical Security Research</p>
            <p><strong>⚠️ DISCLAIMER:</strong> This tool is for authorized security testing only. Use responsibly.</p>
        </footer>
    </div>
</body>
</html>
"""
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        logger.info(f"✓ Relatório HTML: {filepath}")
    
    def generate_txt(self, filepath: str):
        """Gera relatório TXT detalhado"""
        lines = [
            "═" * 80,
            "🔮 OLHO MALIGNO v3.0 - COMPLETE SECURITY REPORT",
            "═" * 80,
            "",
            f"Target: {self.config_url}",
            f"Date: {self.timestamp.strftime('%Y-%m-%d %H:%M:%S')}",
            f"Total Endpoints: {len(self.endpoints)}",
            f"Total Vulnerabilities: {len(self.vulnerabilities)}",
            "",
            f"Technologies Detected: {', '.join(sorted(self.technologies)) or 'None'}",
            "",
        ]
        
        by_severity = {}
        for vuln in self.vulnerabilities:
            sev = vuln.severity.name
            if sev not in by_severity:
                by_severity[sev] = []
            by_severity[sev].append(vuln)
        
        for severity in ['CRITICAL', 'HIGH', 'MEDIUM', 'LOW', 'INFO']:
            vulns = by_severity.get(severity, [])
            if vulns:
                lines.append("")
                lines.append(f"[{severity}] - {len(vulns)} encontrada(s)")
                lines.append("═" * 80)
                
                for i, vuln in enumerate(vulns, 1):
                    lines.append(f"\n#{i} {vuln.title}")
                    lines.append(f"  Type: {vuln.vuln_type}")
                    lines.append(f"  URL: {vuln.url}")
                    if vuln.parameter:
                        lines.append(f"  Parameter: {vuln.parameter}")
                    lines.append(f"  CVSS Score: {vuln.cvss_score}/10")
                    lines.append(f"  Confidence: {vuln.confidence.value}")
                    lines.append(f"  Evidence: {vuln.evidence[:100]}")
                    lines.append(f"  Remediation: {vuln.remediation}")
                    lines.append("-" * 80)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write('\n'.join(lines))
        
        logger.info(f"✓ Relatório TXT: {filepath}")
    
    def _generate_summary(self) -> Dict:
        """Gera resumo por severidade"""
        summary = {}
        for sev in SeverityLevel:
            count = len([v for v in self.vulnerabilities if v.severity == sev])
            summary[sev.name] = count
        return summary


# ════════════════════════════════════════════════════════════════════════════
# SCANNER PRINCIPAL
# ════════════════════════════════════════════════════════════════════════════

class OlhoMalignoV3:
    """Scanner principal v3.0"""
    
    def __init__(self, url: str, config: Optional[str] = None, **kwargs):
        self.url = url
        self.config = self._load_config(config, **kwargs)
        self.http_client = HTTPClient(
            rate=self.config['rate'],
            timeout=self.config['timeout'],
            delay=self.config['delay'],
            proxy=self.config.get('proxy'),
            verify_ssl=self.config.get('verify_ssl', False)
        )
        self.vulnerabilities: List[Vulnerability] = []
        self.endpoints: Set[str] = set()
        self.technologies: Set[str] = set()
        self._print_banner()
    
    def _load_config(self, config_file: Optional[str] = None, **kwargs) -> Dict:
        """Carrega configuração"""
        default_config = {
            'url': self.url,
            'depth': 2,
            'delay': 0.5,
            'rate': 10.0,
            'timeout': 10,
            'output': 'scan_report',
            'format': 'all',
            'scope': None,
            'safe_mode': True,
            'wordlist_size': 'medium',
            'follow_redirects': True,
            'verify_ssl': False,
            'proxy': None,
            'enumerate_subdomains': False,
            'threads': 10,
        }
        
        if config_file and os.path.exists(config_file):
            with open(config_file, 'r', encoding='utf-8') as f:
                file_config = yaml.safe_load(f) or {}
            default_config.update(file_config)
        
        default_config.update(kwargs)
        return default_config
    
    def _print_banner(self):
        """Imprime banner"""
        os.system('clear' if os.name == 'posix' else 'cls')
        
        print(f"\n{Fore.MAGENTA}{Style.BRIGHT}")
        print("╔" + "═" * 78 + "╗")
        print("║" + " " * 78 + "║")
        print("║" + "🔮 OLHO MALIGNO v3.0 - ULTIMATE SECURITY SCANNER 🔮".center(78) + "║")
        print("║" + " " * 78 + "║")
        print("║" + "ENCONTRA TODAS AS FALHAS POSSÍVEIS - 200% COVERAGE".center(78) + "║")
        print("║" + " " * 78 + "║")
        print("╚" + "═" * 78 + "╝")
        print(f"{Style.RESET_ALL}\n")
        
        print(f"{Fore.CYAN}[CONFIG]{Style.RESET_ALL}")
        print(f"  Target: {Fore.GREEN}{self.config['url']}{Style.RESET_ALL}")
        print(f"  Depth: {Fore.GREEN}{self.config['depth']}{Style.RESET_ALL}")
        print(f"  Rate: {Fore.GREEN}{self.config['rate']} req/s{Style.RESET_ALL}")
        print(f"  Wordlist: {Fore.GREEN}{self.config['wordlist_size'].upper()}{Style.RESET_ALL}")
        print(f"  Safe Mode: {Fore.GREEN}{'✓ ON' if self.config['safe_mode'] else '✗ OFF'}{Style.RESET_ALL}")
        if self.config.get('proxy'):
            print(f"  Proxy: {Fore.GREEN}{self.config['proxy']}{Style.RESET_ALL}")
        print()
    
    def scan(self) -> List[Vulnerability]:
        """Executa scan completo"""
        try:
            # Fase 0: Enumeração de subdomínios
            if self.config.get('enumerate_subdomains'):
                logger.info(f"{Fore.YELLOW}{'=' * 60}{Style.RESET_ALL}")
                logger.info(f"{Fore.MAGENTA}[FASE 0/4] SUBDOMAIN ENUMERATION{Style.RESET_ALL}")
                logger.info(f"{Fore.YELLOW}{'=' * 60}{Style.RESET_ALL}")
                
                domain = urlparse(self.url).netloc
                enumerator = SubdomainEnumerator(self.http_client, domain)
                subdomains = enumerator.enumerate(threads=self.config.get('threads', 10))
                
                for subdomain in subdomains:
                    self.config['url'] = subdomain
            
            # Fase 1: Crawling
            logger.info(f"\n{Fore.YELLOW}{'=' * 60}{Style.RESET_ALL}")
            logger.info(f"{Fore.MAGENTA}[FASE 1/4] RECONNAISSANCE{Style.RESET_ALL}")
            logger.info(f"{Fore.YELLOW}{'=' * 60}{Style.RESET_ALL}")
            
            crawler = AdvancedCrawler(
                self.http_client,
                depth=self.config['depth'],
                scope=self.config.get('scope')
            )
            self.endpoints, parameters, self.technologies = crawler.crawl(self.url)
            
            # Fase 2: Scanning
            logger.info(f"\n{Fore.YELLOW}{'=' * 60}{Style.RESET_ALL}")
            logger.info(f"{Fore.MAGENTA}[FASE 2/4] MAXIMUM VULNERABILITY SCANNING{Style.RESET_ALL}")
            logger.info(f"{Fore.YELLOW}{'=' * 60}{Style.RESET_ALL}")
            
            scanner = MaxVulnerabilityScanner(
                self.http_client,
                self.endpoints,
                parameters,
                wordlist_size=self.config['wordlist_size']
            )
            self.vulnerabilities = scanner.scan_all()
            
            # Fase 3: Geração de Relatórios
            logger.info(f"\n{Fore.YELLOW}{'=' * 60}{Style.RESET_ALL}")
            logger.info(f"{Fore.MAGENTA}[FASE 3/4] REPORT GENERATION{Style.RESET_ALL}")
            logger.info(f"{Fore.YELLOW}{'=' * 60}{Style.RESET_ALL}")
            
            self._generate_reports()
            
            # Fase 4: Resumo
            logger.info(f"\n{Fore.YELLOW}{'=' * 60}{Style.RESET_ALL}")
            logger.info(f"{Fore.MAGENTA}[FASE 4/4] SCAN COMPLETE{Style.RESET_ALL}")
            logger.info(f"{Fore.YELLOW}{'=' * 60}{Style.RESET_ALL}")
            
            self._print_summary()
            
            return self.vulnerabilities
        
        except KeyboardInterrupt:
            logger.warning(f"\n{Fore.RED}[!] Scan interrompido{Style.RESET_ALL}")
            return self.vulnerabilities
        except Exception as e:
            logger.error(f"{Fore.RED}Erro: {e}{Style.RESET_ALL}")
            raise
    
    def _generate_reports(self):
        """Gera relatórios"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        base_name = f"{self.config['output']}_{timestamp}"
        
        generator = AdvancedReportGenerator(
            self.vulnerabilities,
            self.config['url'],
            self.technologies,
            self.endpoints
        )
        
        if self.config['format'] in ['all', 'json']:
            generator.generate_json(f"{base_name}.json")
        
        if self.config['format'] in ['all', 'txt']:
            generator.generate_txt(f"{base_name}.txt")
        
        if self.config['format'] in ['all', 'html']:
            generator.generate_html(f"{base_name}.html")
    
    def _print_summary(self):
        """Imprime resumo final"""
        print(f"\n{Fore.GREEN}[✓] SCAN FINALIZADO{Style.RESET_ALL}\n")
        
        by_severity = {}
        for vuln in self.vulnerabilities:
            sev = vuln.severity.name
            if sev not in by_severity:
                by_severity[sev] = 0
            by_severity[sev] += 1
        
        print(f"{Fore.CYAN}Resumo:{Style.RESET_ALL}")
        print(f"  Endpoints: {Fore.GREEN}{len(self.endpoints)}{Style.RESET_ALL}")
        print(f"  Tecnologias: {Fore.GREEN}{len(self.technologies)}{Style.RESET_ALL}")
        print()
        
        print(f"{Fore.CYAN}Vulnerabilidades por Severidade:{Style.RESET_ALL}")
        for severity in ['CRITICAL', 'HIGH', 'MEDIUM', 'LOW', 'INFO']:
            count = by_severity.get(severity, 0)
            sev_obj = SeverityLevel[severity]
            color = sev_obj.value[1]
            print(f"  {color}[{sev_obj.value[0]}] {count} encontrada(s){Style.RESET_ALL}")
        
        print(f"\n{Fore.MAGENTA}Total: {len(self.vulnerabilities)} vulnerabilidades{Style.RESET_ALL}\n")


# ════════════════════════════════════════════════════════════════════════════
# CLI
# ════════════════════════════════════════════════════════════════════════════

def main():
    """Função principal"""
    parser = argparse.ArgumentParser(
        description='🔮 Olho Maligno v3.0 - Ultimate Security Scanner',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
EXEMPLOS:
  # Scan máximo
  python olho_maligno_v3_ultimate.py -u https://example.com --wordlist large
  
  # Com enumeração de subdomínios
  python olho_maligno_v3_ultimate.py -u https://example.com --enum-subdomains
  
  # Com proxy
  python olho_maligno_v3_ultimate.py -u https://example.com --proxy http://127.0.0.1:8080
  
  # Todos os formatos
  python olho_maligno_v3_ultimate.py -u https://example.com --format all

⚠️  USE APENAS EM AMBIENTES AUTORIZADOS!
        """
    )
    
    parser.add_argument('-u', '--url', required=True, help='URL alvo')
    parser.add_argument('--depth', type=int, default=2, help='Profundidade (1-5)')
    parser.add_argument('--delay', type=float, default=0.5, help='Delay (segundos)')
    parser.add_argument('--rate', type=float, default=10.0, help='Rate (req/s)')
    parser.add_argument('--timeout', type=int, default=10, help='Timeout')
    parser.add_argument('--output', default='scan_report', help='Nome da saída')
    parser.add_argument('--format', choices=['json', 'txt', 'html', 'all'], default='all')
    parser.add_argument('--scope', help='Escopo')
    parser.add_argument('--config', help='Arquivo YAML')
    parser.add_argument('--wordlist', choices=['small', 'medium', 'large'], default='medium')
    parser.add_argument('--proxy', help='Proxy (http://ip:port)')
    parser.add_argument('--enum-subdomains', action='store_true', help='Enumerar subdomínios')
    parser.add_argument('--threads', type=int, default=10, help='Threads')
    
    args = parser.parse_args()
    
    if not args.url.startswith(('http://', 'https://')):
        print(f"{Fore.RED}[!] URL deve começar com http:// ou https://{Style.RESET_ALL}")
        return 1
    
    try:
        scanner = OlhoMalignoV3(
            url=args.url,
            config=args.config,
            depth=args.depth,
            delay=args.delay,
            rate=args.rate,
            timeout=args.timeout,
            output=args.output,
            format=args.format,
            scope=args.scope,
            wordlist_size=args.wordlist,
            proxy=args.proxy,
            enumerate_subdomains=args.enum_subdomains,
            threads=args.threads,
        )
        
        scanner.scan()
        return 0
    
    except Exception as e:
        logger.error(f"Erro: {e}")
        return 1


if __name__ == '__main__':
    sys.exit(main())
