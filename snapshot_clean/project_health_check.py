#!/usr/bin/env python3
"""
Webapp Project Health Check Script
Scans and reports the status of a webapp project in the current directory
"""

import os
import sys
import json
import subprocess
import socket
import requests
import platform
import getpass
import pwd
import grp
import stat
from datetime import datetime
from urllib.parse import urlparse
import re
import tempfile
from pathlib import Path
import mimetypes


def run_command(cmd):
    """Execute a shell command and return its output"""
    try:
        result = subprocess.run(
            cmd, shell=True, capture_output=True, text=True, timeout=30
        )
        return result.stdout.strip(), result.stderr.strip(), result.returncode
    except subprocess.TimeoutExpired:
        return "", "Command timed out", -1
    except Exception as e:
        return "", str(e), -1


def run_command_simple(cmd):
    """Execute a shell command and return its output without return code"""
    try:
        result = subprocess.run(
            cmd, shell=True, capture_output=True, text=True, timeout=30
        )
        return result.stdout.strip(), result.stderr.strip()
    except subprocess.TimeoutExpired:
        return "", "Command timed out"
    except Exception as e:
        return "", str(e)


def get_basic_context():
    """Collect basic system context information"""
    context = {}
    
    # Current working directory
    context['cwd'] = os.getcwd()
    
    # Username and hostname
    context['username'] = getpass.getuser()
    context['hostname'] = socket.gethostname()
    
    # Git information
    try:
        git_branch, _, _ = run_command("git branch --show-current")
        git_remote, _, _ = run_command("git remote get-url origin")
        git_commit, _, _ = run_command("git log -1 --format='%H|%s|%an|%ad'")
        
        if git_commit and '|' in git_commit:
            commit_hash, commit_msg, commit_author, commit_date = git_commit.split('|', 3)
            context['git'] = {
                'branch': git_branch,
                'remote_origin_url': git_remote,
                'latest_commit': {
                    'hash': commit_hash,
                    'message': commit_msg,
                    'author': commit_author,
                    'date': commit_date
                }
            }
    except:
        context['git'] = None
    
    # Node versions
    node_version, _, _ = run_command("node -v")
    npm_version, _, _ = run_command("npm -v")
    npx_version, _, _ = run_command("npx -v")
    
    context['node'] = {
        'node_version': node_version,
        'npm_version': npm_version,
        'npx_version': npx_version
    }
    
    # Python versions
    python_version, _, _ = run_command("python3 --version")
    pip_list, _, _ = run_command("pip3 freeze")
    
    context['python'] = {
        'python_version': python_version,
        'pip_list': pip_list
    }
    
    # OS information
    context['os'] = {
        'name': platform.system(),
        'distro': run_command("cat /etc/os-release")[0] if os.path.exists("/etc/os-release") else "N/A",
        'kernel': platform.uname().release,
        'architecture': platform.machine()
    }
    
    return context


def scan_file_system():
    """Scan the file system and return a tree structure"""
    project_root = Path.cwd()
    important_files = set([
        'package.json', 'package-lock.json', 'yarn.lock', 'pnpm-lock.yaml',
        'vite.config.js', 'vite.config.ts', 'webpack.config.js', 'next.config.js',
        'nuxt.config.js', 'angular.json', 'astro.config.js', 'pubspec.yaml',
        'manifest.json', 'service-worker.js', 'sw.js', 'src', 'public', 'dist',
        'build', 'static', 'offline.html', 'manifest.webmanifest'
    ])
    
    files_content = {}
    tree = {}
    
    def build_tree(path, current_tree, depth=0):
        if depth > 4:  # Max depth 4
            return
        for item in path.iterdir():
            if item.is_dir():
                current_tree[item.name] = {}
                build_tree(item, current_tree[item.name], depth + 1)
            else:
                current_tree[item.name] = item.stat().st_size  # Store size for files
                if item.name in important_files:
                    try:
                        with open(item, 'r', encoding='utf-8', errors='ignore') as f:
                            content = f.read(2000)  # First 2000 characters
                            files_content[str(item.relative_to(project_root))] = content
                    except:
                        pass  # Skip files that can't be read
    
    build_tree(project_root, tree)
    
    # Also look for specific top-level files/directories
    top_level_files = []
    for item in project_root.iterdir():
        if item.name in important_files:
            top_level_files.append(item.name)
    
    return {
        'tree': tree,
        'top_level_important_files': top_level_files,
        'files_content': files_content
    }


def parse_package_json():
    """Parse package.json if it exists"""
    pkg_json_path = Path("package.json")
    if pkg_json_path.exists():
        try:
            with open(pkg_json_path, 'r', encoding='utf-8') as f:
                content = json.load(f)
                return {
                    'scripts': content.get('scripts', {}),
                    'dependencies': content.get('dependencies', {}),
                    'devDependencies': content.get('devDependencies', {})
                }
        except:
            pass
    return None


def detect_framework(package_json_data):
    """Detect the framework from package.json and config files"""
    detection = {
        'framework': 'Unknown',
        'confidence': 'low',
        'reason': 'No detection method matched'
    }
    
    if package_json_data:
        scripts = package_json_data.get('scripts', {})
        dependencies = package_json_data.get('dependencies', {})
        dev_dependencies = package_json_data.get('devDependencies', {})
        
        # Combine all dependencies
        all_deps = {**dependencies, **dev_dependencies}
        
        # Check for dev scripts
        dev_scripts = ' '.join(scripts.values())
        
        # Detect frameworks based on dependencies and scripts
        if 'vite' in all_deps or 'vite' in dev_scripts or any('vite' in script for script in scripts.values()):
            detection.update({
                'framework': 'Vite',
                'confidence': 'high',
                'reason': 'vite dependency found in package.json'
            })
        elif 'next' in all_deps:
            detection.update({
                'framework': 'Next.js',
                'confidence': 'high',
                'reason': 'next dependency found in package.json'
            })
        elif 'create-react-app' in all_deps or '@react-scripts' in dev_dependencies:
            detection.update({
                'framework': 'Create-React-App',
                'confidence': 'high',
                'reason': 'create-react-app or react-scripts dependency found'
            })
        elif 'nuxt' in all_deps:
            detection.update({
                'framework': 'Nuxt',
                'confidence': 'high',
                'reason': 'nuxt dependency found in package.json'
            })
        elif '@angular/core' in all_deps:
            detection.update({
                'framework': 'Angular',
                'confidence': 'high',
                'reason': '@angular/core dependency found in package.json'
            })
        elif 'svelte' in all_deps and 'rollup' in all_deps:
            detection.update({
                'framework': 'SvelteKit',
                'confidence': 'medium',
                'reason': 'svelte and rollup dependencies found'
            })
        elif 'astro' in all_deps:
            detection.update({
                'framework': 'Astro',
                'confidence': 'high',
                'reason': 'astro dependency found in package.json'
            })
        elif 'parcel' in all_deps or 'parcel' in dev_scripts:
            detection.update({
                'framework': 'Parcel',
                'confidence': 'medium',
                'reason': 'parcel dependency or script found'
            })
        elif 'flutter' in dev_scripts.lower():
            detection.update({
                'framework': 'Flutter Web',
                'confidence': 'medium',
                'reason': 'flutter command found in scripts'
            })
        elif not all_deps and 'start' in scripts:
            detection.update({
                'framework': 'Plain Static Site',
                'confidence': 'medium',
                'reason': 'no framework dependencies, but start script exists'
            })
    
    # Check config files
    config_files = [
        ('vite.config.js', 'Vite', 'high', 'vite config file found'),
        ('vite.config.ts', 'Vite', 'high', 'vite config file found'),
        ('webpack.config.js', 'Webpack', 'high', 'webpack config file found'),
        ('next.config.js', 'Next.js', 'high', 'next config file found'),
        ('nuxt.config.js', 'Nuxt', 'high', 'nuxt config file found'),
        ('angular.json', 'Angular', 'high', 'angular config file found'),
        ('astro.config.js', 'Astro', 'high', 'astro config file found'),
    ]
    
    for file_name, framework, conf, reason in config_files:
        if Path(file_name).exists():
            detection.update({
                'framework': framework,
                'confidence': conf,
                'reason': reason
            })
            break  # Use the first match
    
    return detection


def detect_dev_server(framework_info, package_json_data):
    """Detect running dev server and its details"""
    server_info = {
        'running': False,
        'host': None,
        'port': None,
        'command': None,
        'suggested_start_command': None
    }
    
    # Check package.json scripts for dev commands
    if package_json_data:
        scripts = package_json_data.get('scripts', {})
        
        # Look for development scripts
        dev_script_names = ['dev', 'develop', 'start', 'serve', 'watch']
        for name in dev_script_names:
            if name in scripts:
                script_cmd = scripts[name]
                
                # Try to extract port from the script
                port_match = re.search(r'(?:--port|--port=|-p\s+)(\d+)', script_cmd)
                if port_match:
                    server_info['port'] = int(port_match.group(1))
                
                # For common frameworks with default ports
                if not server_info['port']:
                    framework = framework_info.get('framework', '').lower()
                    if framework == 'vite':
                        server_info['port'] = 5173
                    elif framework == 'create-react-app':
                        server_info['port'] = 3000
                    elif framework == 'next.js':
                        server_info['port'] = 3000
                    elif framework == 'nuxt':
                        server_info['port'] = 3000
                    elif framework == 'angular':
                        server_info['port'] = 4200
                    elif framework == 'sveltekit':
                        server_info['port'] = 5173
                    elif framework == 'astro':
                        server_info['port'] = 4321
                
                server_info['suggested_start_command'] = f"npm run {name}"
                break
    
    # Check for currently running servers
    ports_output, _, _ = run_command("ss -tulpn")
    if ports_output:
        # Look for node, python, or other server processes
        lines = ports_output.split('\n')
        for line in lines:
            if 'node' in line or 'python' in line:
                # Extract the port from the listening addresses
                match = re.search(r':(\d+)\s+.*LISTEN', line)
                if match:
                    port = int(match.group(1))
                    server_info['running'] = True
                    server_info['port'] = port
                    # Get the process command
                    pid_match = re.search(r'users:\(\("([^"]+)', line)
                    if pid_match:
                        server_info['command'] = pid_match.group(1)
                    break
    
    return server_info


def check_pwa():
    """Check for PWA-related files and configurations"""
    pwa_info = {
        'manifest': None,
        'service_workers': [],
        'meta_tags': [],
        'offline_page': None
    }
    
    # Check for manifest files
    manifest_paths = ['manifest.json', 'manifest.webmanifest']
    for manifest_path in manifest_paths:
        if Path(manifest_path).exists():
            try:
                with open(manifest_path, 'r', encoding='utf-8') as f:
                    manifest_data = json.load(f)
                    pwa_info['manifest'] = {
                        'name': manifest_data.get('name'),
                        'short_name': manifest_data.get('short_name'),
                        'start_url': manifest_data.get('start_url'),
                        'display': manifest_data.get('display'),
                        'icons': manifest_data.get('icons', []),
                        'background_color': manifest_data.get('background_color'),
                        'theme_color': manifest_data.get('theme_color')
                    }
            except:
                pass
    
    # Check for service worker registration in JS files
    for root, dirs, files in os.walk('.'):
        for file in files:
            if file.endswith('.js') or file.endswith('.html'):
                file_path = Path(root) / file
                try:
                    with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                        content = f.read()
                        
                        # Look for service worker registration
                        if 'navigator.serviceWorker.register' in content.lower() or 'service-worker.js' in content.lower() or 'sw.js' in content.lower():
                            # Find the specific registration lines
                            lines = content.split('\n')
                            for i, line in enumerate(lines):
                                if 'navigator.serviceWorker.register' in line.lower() or 'service-worker.js' in line.lower() or 'sw.js' in line.lower():
                                    context_lines = max(0, i-25), min(len(lines), i+25)
                                    snippet = '\n'.join(lines[context_lines[0]:context_lines[1]])
                                    pwa_info['service_workers'].append({
                                        'file': str(file_path),
                                        'registration_snippet': snippet
                                    })
                except:
                    pass  # Skip files that can't be read
    
    # Check for service worker files
    sw_files = ['service-worker.js', 'sw.js']
    for sw_file in sw_files:
        sw_path = Path(sw_file)
        if sw_path.exists():
            try:
                with open(sw_path, 'r', encoding='utf-8') as f:
                    content = f.read(2000)  # First 2000 chars
                    pwa_info[f'{sw_file}_content'] = content
            except:
                pass
    
    # Look for PWA meta tags in HTML files
    for root, dirs, files in os.walk('.'):
        for file in files:
            if file.endswith('.html'):
                file_path = Path(root) / file
                try:
                    with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                        content = f.read()
                        
                        # Look for PWA-related meta tags
                        meta_patterns = [
                            r'<meta[^>]*name="theme-color"[^>]*>',
                            r'<meta[^>]*name="apple-mobile-web-app-capable"[^>]*>',
                            r'<meta[^>]*name="viewport"[^>]*>',
                            r'<meta[^>]*property="og:image"[^>]*>'
                        ]
                        
                        for pattern in meta_patterns:
                            matches = re.findall(pattern, content, re.IGNORECASE)
                            pwa_info['meta_tags'].extend(matches)
                except:
                    pass  # Skip files that can't be read
    
    # Check for offline page
    offline_pages = ['offline.html', 'fallback.html', '404.html']
    for page in offline_pages:
        if Path(page).exists():
            pwa_info['offline_page'] = page
            break
    
    return pwa_info


def check_static_assets(pwa_manifest):
    """Check for static assets and icons"""
    assets_info = {
        'icons': []
    }
    
    if pwa_manifest and 'manifest' in pwa_manifest and pwa_manifest['manifest']:
        manifest_icons = pwa_manifest['manifest'].get('icons', [])
        for icon in manifest_icons:
            src = icon.get('src', '')
            if src:
                # Check if icon file exists in project
                icon_path = Path(src.lstrip('/'))
                if not icon_path.exists():
                    # Try common public directories
                    for pub_dir in ['public', 'static', 'assets', 'images']:
                        pub_path = Path(pub_dir) / src.lstrip('/')
                        if pub_path.exists():
                            icon_path = pub_path
                            break
                
                icon_exists = icon_path.exists()
                icon_info = {
                    'src': src,
                    'sizes': icon.get('sizes'),
                    'type': icon.get('type'),
                    'exists': icon_exists,
                    'path': str(icon_path) if icon_exists else None,
                    'size_bytes': icon_path.stat().st_size if icon_exists else None
                }
                
                # Try to get image dimensions if ImageMagick is available
                if icon_exists:
                    width, _, _ = run_command(f"identify -format '%%w:%%h' '{icon_path}'")
                    if width and ':' in width:
                        w, h = width.split(':')
                        try:
                            icon_info['width'] = int(w)
                            icon_info['height'] = int(h)
                        except ValueError:
                            pass  # Skip if can't parse dimensions
                
                assets_info['icons'].append(icon_info)
    
    return assets_info


def check_hot_reload():
    """Check for hot-reload/livereload capabilities"""
    reload_info = {
        'hot_reload_scripts': [],
        'watcher_files': []
    }
    
    # Check for common hot-reload patterns in the codebase
    hot_reload_patterns = [
        'livereload',
        'browser-sync',
        'vite dev',
        'webpack-dev-server',
        'react-refresh',
        'hmr',
        'HotModuleReplacementPlugin'
    ]
    
    for root, dirs, files in os.walk('.'):
        for file in files:
            if file.endswith(('.js', '.ts', '.jsx', '.tsx', '.json', '.html', '.config.js')):
                file_path = Path(root) / file
                try:
                    with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                        content = f.read().lower()
                        
                        # Check for hot reload patterns
                        for pattern in hot_reload_patterns:
                            if pattern.lower() in content:
                                reload_info['hot_reload_scripts'].append({
                                    'file': str(file_path),
                                    'pattern': pattern,
                                    'context': content[:500]  # First 500 chars as context
                                })
                                break  # Don't add same file multiple times
                        
                        # Check for WebSocket usage related to reload
                        if 'ws://' in content or 'websocket' in content:
                            reload_info['hot_reload_scripts'].append({
                                'file': str(file_path),
                                'pattern': 'websocket',
                                'context': content[:500]
                            })
                except:
                    pass  # Skip files that can't be read
    
    # Look for specific watcher files
    watcher_files = ['ws-reload-server.js', 'reload-server.js', 'file-watcher.js', 'watcher.py']
    for watcher_name in watcher_files:
        watcher_path = Path(watcher_name)
        if watcher_path.exists():
            try:
                with open(watcher_path, 'r', encoding='utf-8') as f:
                    content = f.read(2000)  # First 2000 chars
                    reload_info['watcher_files'].append({
                        'name': watcher_name,
                        'content': content
                    })
            except:
                pass  # Skip files that can't be read
    
    return reload_info


def check_dev_helpers():
    """Check for development helpers and tools"""
    helpers_info = {
        'install_script': None,
        'run_script': None,
        'start_script': None,
        'docker_compose': None,
        'dockerfile': None,
        'device_frame': None,
        'ios_fixes_css': None,
        'ios_fixes_js': None
    }
    
    # Check for helper files
    helper_files = {
        'install.sh': 'install_script',
        'run.sh': 'run_script', 
        'start.sh': 'start_script',
        'docker-compose.yml': 'docker_compose',
        'Dockerfile': 'dockerfile',
        'device_frame.py': 'device_frame',
        'auto/ios-fixes.css': 'ios_fixes_css',
        'auto/ios-fixes.js': 'ios_fixes_js'
    }
    
    for file_name, key in helper_files.items():
        file_path = Path(file_name)
        if file_path.exists():
            try:
                if key in ['ios_fixes_css', 'ios_fixes_js', 'device_frame']:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        content = f.read(500)  # First 500 chars
                        helpers_info[key] = {
                            'path': str(file_path),
                            'content': content
                        }
                else:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        content = f.read(500)  # First 500 chars
                        helpers_info[key] = {
                            'path': str(file_path),
                            'content': content
                        }
            except:
                helpers_info[key] = {
                    'path': str(file_path),
                    'error': 'Could not read file'
                }
    
    return helpers_info


def get_network_info():
    """Get network information"""
    network_info = {
        'local_ips': [],
        'firewall_status': None,
        'active_ports': []
    }
    
    # Get local IPs
    try:
        hostname_ips, _, _ = run_command("hostname -I")
        if hostname_ips:
            network_info['local_ips'] = hostname_ips.split()
    except:
        pass
    
    # Check firewall status
    try:
        ufw_status, _, _ = run_command("ufw status")
        if ufw_status:
            network_info['firewall_status'] = ufw_status
    except:
        network_info['firewall_status'] = 'Command not available'
    
    # Get active ports
    try:
        ss_output, _, _ = run_command("ss -tulpn")
        if ss_output:
            lines = ss_output.split('\n')
            for line in lines:
                if 'LISTEN' in line:
                    network_info['active_ports'].append(line)
            
            # Save to log file
            with open('./logs/system_ports.log', 'w') as f:
                f.write(ss_output)
    except:
        network_info['active_ports'] = ['Could not retrieve port information']
    
    return network_info


def check_runtime(dev_server_info):
    """Perform runtime checks if a dev server is running"""
    runtime_info = {
        'local_check': None,
        'external_check': None
    }
    
    if dev_server_info.get('running') and dev_server_info.get('port'):
        port = dev_server_info['port']
        
        # Check local access
        try:
            local_url = f"http://127.0.0.1:{port}/"
            response = requests.get(local_url, timeout=5)
            runtime_info['local_check'] = {
                'url': local_url,
                'status_code': response.status_code,
                'content_type': response.headers.get('content-type'),
                'content_preview': response.text[:2000] if response.headers.get('content-type', '').startswith('text/') or 'json' in response.headers.get('content-type', '') else '<non-text content>'
            }
        except Exception as e:
            runtime_info['local_check'] = {
                'url': f"http://127.0.0.1:{port}/",
                'error': str(e)
            }
        
        # Check external access if we have a local IP
        network_info = get_network_info()
        if network_info.get('local_ips'):
            local_ip = None
            for ip in network_info['local_ips']:
                if not ip.startswith('127.'):  # Skip loopback
                    local_ip = ip
                    break
            
            if local_ip:
                try:
                    external_url = f"http://{local_ip}:{port}/"
                    response = requests.get(external_url, timeout=5)
                    runtime_info['external_check'] = {
                        'url': external_url,
                        'status_code': response.status_code,
                        'content_type': response.headers.get('content-type'),
                        'content_preview': response.text[:2000] if response.headers.get('content-type', '').startswith('text/') or 'json' in response.headers.get('content-type', '') else '<non-text content>'
                    }
                except Exception as e:
                    runtime_info['external_check'] = {
                        'url': f"http://{local_ip}:{port}/",
                        'error': str(e)
                    }
    
    return runtime_info


def generate_console_snippet():
    """Generate a browser console snippet for device info"""
    return """
(() => {
  const info = {
    innerWidth: window.innerWidth,
    innerHeight: window.innerHeight,
    devicePixelRatio: window.devicePixelRatio,
    userAgent: navigator.userAgent,
    platform: navigator.platform,
    onLine: navigator.onLine,
    cookieEnabled: navigator.cookieEnabled,
    language: navigator.language,
    maxTouchPoints: navigator.maxTouchPoints
  };
  console.table ? console.table(info) : console.log(info);
  return info;
})()
""".strip()


def generate_report():
    """Generate the complete project health report"""
    print("Scanning project directory...")
    
    # Ensure logs directory exists
    os.makedirs('./logs', exist_ok=True)
    
    # Collect all information
    basic_context = get_basic_context()
    file_system_scan = scan_file_system()
    package_json_data = parse_package_json()
    framework_info = detect_framework(package_json_data)
    dev_server_info = detect_dev_server(framework_info, package_json_data)
    pwa_info = check_pwa()
    assets_info = check_static_assets(pwa_info)
    hot_reload_info = check_hot_reload()
    dev_helpers_info = check_dev_helpers()
    network_info = get_network_info()
    runtime_info = check_runtime(dev_server_info)
    console_snippet = generate_console_snippet()
    
    # Mask sensitive environment variables
    env_vars = dict(os.environ)
    masked_env_vars = {}
    sensitive_patterns = ['SECRET', 'KEY', 'TOKEN', 'PASSWORD', 'AWS_', 'GCP_', 'DB_']
    
    for key, value in env_vars.items():
        is_sensitive = any(pattern in key.upper() for pattern in sensitive_patterns)
        if is_sensitive:
            masked_env_vars[key] = '<REDACTED>'
        else:
            masked_env_vars[key] = value
    
    # Generate human summary
    framework = framework_info.get('framework', 'Unknown')
    confidence = framework_info.get('confidence', 'low')
    
    human_summary = f"""
• Project framework detected: {framework} (confidence: {confidence})
• Node version: {basic_context['node']['node_version']}
• Python version: {basic_context['python']['python_version']}
• Dev server: {'Running' if dev_server_info['running'] else 'Not running'}
• Manifest file: {'Found' if pwa_info['manifest'] else 'Not found'}
• Service worker: {'Found' if pwa_info['service_workers'] else 'Not found'}
• Hot reload: {'Enabled' if hot_reload_info['hot_reload_scripts'] else 'Not detected'}
    """.strip()
    
    # Generate actions recommended
    actions = []
    if not dev_server_info['running']:
        if dev_server_info['suggested_start_command']:
            actions.append(f"Start dev server: {dev_server_info['suggested_start_command']}")
        else:
            actions.append("Configure and start a dev server")
    
    if not pwa_info['manifest']:
        actions.append("Create manifest.json for PWA functionality")
    
    if not pwa_info['service_workers']:
        actions.append("Add service worker for offline functionality")
    
    if pwa_info['manifest'] and not pwa_info['offline_page']:
        actions.append("Add offline.html for offline fallback")
    
    # Create the full report
    report = {
        'timestamp': datetime.now().isoformat(),
        'human_summary': human_summary,
        'actions_recommended': actions,
        'metadata': basic_context,
        'system': {
            'os_info': basic_context['os'],
            'env_vars': masked_env_vars
        },
        'node': basic_context['node'],
        'python': basic_context['python'],
        'project_files': file_system_scan,
        'package_json': package_json_data,
        'framework_detection': framework_info,
        'dev_server': dev_server_info,
        'pwa_manifest': pwa_info,
        'service_workers': hot_reload_info,  # Service worker info is included in hot reload check
        'icons': assets_info,
        'watcher': hot_reload_info,
        'tools': dev_helpers_info,
        'network': network_info,
        'http_check': runtime_info,
        'console_snippet': console_snippet
    }
    
    # Save report to file
    with open('./logs/project_report.json', 'w') as f:
        json.dump(report, f, indent=2)
    
    return report


if __name__ == "__main__":
    try:
        report = generate_report()
        print(json.dumps(report, indent=2))
    except Exception as e:
        print(f"Error generating report: {str(e)}", file=sys.stderr)
        sys.exit(1)