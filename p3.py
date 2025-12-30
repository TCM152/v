import subprocess
import sys
import site

# Add user site-packages to path (for Cloud Shell)
user_site = site.getusersitepackages()
if user_site not in sys.path:
    sys.path.insert(0, user_site)
    print(f"[+] Added {user_site} to PATH")

# Auto-install dependencies
def install_dependencies():
    """Auto-install required packages"""
    required_packages = ['seleniumbase']
    
    for package in required_packages:
        try:
            __import__(package)
            print(f"[✓] {package} already installed")
        except ImportError:
            print(f"[!] Installing {package}...")
            try:
                # Install with --user flag for Cloud Shell
                subprocess.check_call([sys.executable, "-m", "pip", "install", package, "--user", "--quiet"])
                print(f"[✓] {package} installed successfully")
                
                # Reload sys.path after installation
                import importlib
                importlib.invalidate_caches()
                
            except subprocess.CalledProcessError as e:
                print(f"[✗] Failed to install {package}: {e}")
                sys.exit(1)

# Install dependencies first
install_dependencies()

# Now import the packages
from seleniumbase import SB
import time
import platform
import random
import secrets
import string

TARGET_URL = "https://sfl.gl/fnKT"
MAX_STEPS = 25
WAIT_TIME = 12



def log(msg):
    print(f"[*] {msg}")
    sys.stdout.flush()

class FingerprintRandomizer:
    def __init__(self):
        self.user_agents = [
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:122.0) Gecko/20100101 Firefox/122.0",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:121.0) Gecko/20100101 Firefox/121.0",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36 Edg/120.0.0.0"
        ]
        
        self.timezones = [
            "America/New_York", "America/Chicago", "America/Los_Angeles", "America/Denver",
            "Europe/London", "Europe/Paris", "Europe/Berlin", "Europe/Madrid",
            "Asia/Tokyo", "Asia/Shanghai", "Asia/Dubai", "Asia/Singapore",
            "Australia/Sydney", "Pacific/Auckland", "America/Toronto", "America/Mexico_City"
        ]
        
        self.languages = [
            ["en-US", "en"], ["en-GB", "en"], ["es-ES", "es"], ["fr-FR", "fr"],
            ["de-DE", "de"], ["it-IT", "it"], ["pt-BR", "pt"], ["ja-JP", "ja"],
            ["zh-CN", "zh"], ["ko-KR", "ko"], ["ru-RU", "ru"], ["ar-SA", "ar"]
        ]
        
        self.webgl_vendors = [
            "Google Inc. (NVIDIA)", "Google Inc. (Intel)", "Google Inc. (AMD)",
            "Google Inc. (NVIDIA Corporation)", "Google Inc. (Intel(R) HD Graphics)",
            "Google Inc. (AMD Radeon)", "Mozilla (NVIDIA)", "Mozilla (Intel)"
        ]
        
        self.webgl_renderers = [
            "ANGLE (NVIDIA GeForce RTX 3060 Direct3D11 vs_5_0 ps_5_0)",
            "ANGLE (Intel(R) UHD Graphics 630 Direct3D11 vs_5_0 ps_5_0)",
            "ANGLE (AMD Radeon RX 6700 XT Direct3D11 vs_5_0 ps_5_0)",
            "ANGLE (NVIDIA GeForce GTX 1660 Ti Direct3D11 vs_5_0 ps_5_0)",
            "ANGLE (Intel(R) Iris(R) Xe Graphics Direct3D11 vs_5_0 ps_5_0)",
            "ANGLE (AMD Radeon RX 5700 Direct3D11 vs_5_0 ps_5_0)"
        ]
        
        self.screen_resolutions = [
            (1920, 1080), (2560, 1440), (1366, 768), (1440, 900),
            (1600, 900), (1680, 1050), (3840, 2160), (2560, 1080)
        ]
        
        self.generate_fingerprint()
    
    def generate_fingerprint(self):
        """Generate random fingerprint data"""
        self.user_agent = random.choice(self.user_agents)
        self.timezone = random.choice(self.timezones)
        self.language = random.choice(self.languages)
        self.webgl_vendor = random.choice(self.webgl_vendors)
        self.webgl_renderer = random.choice(self.webgl_renderers)
        self.screen_width, self.screen_height = random.choice(self.screen_resolutions)
        self.color_depth = random.choice([24, 32])
        self.hardware_concurrency = random.choice([2, 4, 6, 8, 12, 16])
        self.device_memory = random.choice([4, 8, 16, 32])
        self.canvas_noise = ''.join(random.choices(string.hexdigits, k=16))
        
        log(f"Fingerprint: UA={self.user_agent[:50]}...")
        log(f"Timezone: {self.timezone}, Lang: {self.language[0]}")
        log(f"WebGL: {self.webgl_vendor} / {self.webgl_renderer[:40]}...")
        log(f"Screen: {self.screen_width}x{self.screen_height}, Cores: {self.hardware_concurrency}")
    
    def get_injection_script(self):
        """Generate JavaScript to inject fingerprint"""
        return f"""
        (function() {{
            // Override User Agent
            Object.defineProperty(navigator, 'userAgent', {{
                get: () => '{self.user_agent}'
            }});
            
            // Override Language
            Object.defineProperty(navigator, 'language', {{
                get: () => '{self.language[0]}'
            }});
            Object.defineProperty(navigator, 'languages', {{
                get: () => {self.language}
            }});
            
            // Override Timezone
            const originalDateTimeFormat = Intl.DateTimeFormat;
            Intl.DateTimeFormat = function(...args) {{
                const instance = new originalDateTimeFormat(...args);
                const originalResolvedOptions = instance.resolvedOptions;
                instance.resolvedOptions = function() {{
                    const options = originalResolvedOptions.call(this);
                    options.timeZone = '{self.timezone}';
                    return options;
                }};
                return instance;
            }};
            
            // Override WebGL
            const getParameter = WebGLRenderingContext.prototype.getParameter;
            WebGLRenderingContext.prototype.getParameter = function(parameter) {{
                if (parameter === 37445) return '{self.webgl_vendor}';
                if (parameter === 37446) return '{self.webgl_renderer}';
                return getParameter.call(this, parameter);
            }};
            
            const getParameter2 = WebGL2RenderingContext.prototype.getParameter;
            WebGL2RenderingContext.prototype.getParameter = function(parameter) {{
                if (parameter === 37445) return '{self.webgl_vendor}';
                if (parameter === 37446) return '{self.webgl_renderer}';
                return getParameter2.call(this, parameter);
            }};
            
            // Override Canvas
            const originalToDataURL = HTMLCanvasElement.prototype.toDataURL;
            HTMLCanvasElement.prototype.toDataURL = function(type) {{
                const dataURL = originalToDataURL.apply(this, arguments);
                return dataURL + '{self.canvas_noise}';
            }};
            
            const originalToBlob = HTMLCanvasElement.prototype.toBlob;
            HTMLCanvasElement.prototype.toBlob = function(callback, type, quality) {{
                originalToBlob.call(this, function(blob) {{
                    callback(new Blob([blob, '{self.canvas_noise}'], {{type: blob.type}}));
                }}, type, quality);
            }};
            
            // Override Screen
            Object.defineProperty(screen, 'width', {{
                get: () => {self.screen_width}
            }});
            Object.defineProperty(screen, 'height', {{
                get: () => {self.screen_height}
            }});
            Object.defineProperty(screen, 'availWidth', {{
                get: () => {self.screen_width}
            }});
            Object.defineProperty(screen, 'availHeight', {{
                get: () => {self.screen_height - 40}
            }});
            Object.defineProperty(screen, 'colorDepth', {{
                get: () => {self.color_depth}
            }});
            Object.defineProperty(screen, 'pixelDepth', {{
                get: () => {self.color_depth}
            }});
            
            // Override Hardware
            Object.defineProperty(navigator, 'hardwareConcurrency', {{
                get: () => {self.hardware_concurrency}
            }});
            Object.defineProperty(navigator, 'deviceMemory', {{
                get: () => {self.device_memory}
            }});
            
            // Override Platform
            Object.defineProperty(navigator, 'platform', {{
                get: () => 'Win32'
            }});
            
            console.log('[Fingerprint] Injected successfully');
        }})();
        """


class SafelinkBypass:
    def __init__(self, sb):
        self.sb = sb
        self.anchor = None
        self.processed = set()
        self.fingerprint = FingerprintRandomizer()

    def is_valid_session(self):
        try:
            self.sb.driver.current_window_handle
            return True
        except:
            return False

    def set_anchor(self):
        try:
            self.anchor = self.sb.driver.current_window_handle
            self.processed.add(self.anchor)
            log(f"Anchor: {self.anchor[:8]}...")
        except Exception as e:
            log(f"Warning: Could not set anchor - {e}")

    def back_to_anchor(self):
        if not self.is_valid_session():
            return
        try:
            if self.anchor and self.sb.driver.current_window_handle != self.anchor:
                self.sb.driver.switch_to.window(self.anchor)
        except:
            try:
                handles = self.sb.driver.window_handles
                if handles:
                    for h in handles:
                        try:
                            self.sb.driver.switch_to.window(h)
                            if "sfl.gl" in self.sb.get_current_url():
                                self.anchor = h
                                return
                        except:
                            continue
            except:
                pass

    def handle_popups(self):
        if not self.is_valid_session():
            return
        try:
            current = self.sb.driver.window_handles
            new_tabs = [h for h in current if h not in self.processed]
            if new_tabs:
                log(f"Detected {len(new_tabs)} popup(s)")
                for h in new_tabs:
                    try:
                        self.sb.driver.switch_to.window(h)
                        time.sleep(2)
                        self.processed.add(h)
                    except:
                        continue
                self.back_to_anchor()
            
            if self.anchor and self.sb.driver.current_window_handle != self.anchor:
                self.back_to_anchor()
        except:
            self.back_to_anchor()

    def remove_overlays(self):
        if not self.is_valid_session():
            return
        try:
            if self.anchor and self.sb.driver.current_window_handle != self.anchor:
                return
        except:
            return
            
        js = """
        try {
            document.querySelectorAll('ins, iframe[id^="aswift"], div[class*="overlay"], div[class*="popup"]').forEach(el => el.remove());
            document.querySelectorAll('body > div').forEach(el => {
                const s = window.getComputedStyle(el);
                if (el.innerText && el.innerText.includes("OPEN LINK")) return;
                if ((parseInt(s.zIndex) > 50 || s.position === 'fixed') && el.offsetHeight > window.innerHeight * 0.5) {
                    el.remove();
                }
            });
            document.body.style.overflow = 'auto';
        } catch(e) {}
        """
        try:
            self.sb.execute_script(js)
        except:
            pass

    def inject_fingerprint(self):
        """Inject fingerprint randomization script"""
        if not self.is_valid_session():
            return
        try:
            script = self.fingerprint.get_injection_script()
            self.sb.execute_script(script)
            log("Fingerprint injected")
        except Exception as e:
            log(f"Warning: Could not inject fingerprint - {e}")
    
    def cleanup_browser_data(self):
        """Clean up all browser data for anonymity"""
        if not self.is_valid_session():
            return
        try:
            log("Cleaning up browser data...")
            
            # Clear cookies
            self.sb.driver.delete_all_cookies()
            
            # Clear storage via JavaScript
            cleanup_script = """
            try {
                // Clear localStorage
                localStorage.clear();
                
                // Clear sessionStorage
                sessionStorage.clear();
                
                // Clear IndexedDB
                if (window.indexedDB && window.indexedDB.databases) {
                    window.indexedDB.databases().then(dbs => {
                        dbs.forEach(db => window.indexedDB.deleteDatabase(db.name));
                    });
                }
                
                console.log('[Cleanup] Browser data cleared');
            } catch(e) {
                console.error('[Cleanup] Error:', e);
            }
            """
            self.sb.execute_script(cleanup_script)
            log("Cleanup complete")
        except Exception as e:
            log(f"Warning: Cleanup error - {e}")
    
    def find_button(self):
        if not self.is_valid_session():
            return None
        try:
            if self.sb.is_element_visible("//span[contains(text(), 'OPEN LINK')]"):
                return "//span[contains(text(), 'OPEN LINK')]/.."
            if self.sb.is_element_visible("button:contains('OPEN LINK')"):
                return "button:contains('OPEN LINK')"
            if self.sb.is_element_visible("button.bg-[#1A56DB]"):
                return "button.bg-[#1A56DB]"
        except:
            pass
        return None

    def run(self):
        log(f"Starting on {TARGET_URL}")
        
        try:
            self.sb.uc_open_with_reconnect(TARGET_URL, reconnect_time=6)
        except Exception as e:
            log(f"Error opening URL: {e}")
            return
            
        self.set_anchor()
        self.inject_fingerprint()
        
        try:
            if "Just a moment" in self.sb.get_title():
                self.sb.uc_gui_click_captcha()
                time.sleep(5)
                self.set_anchor()
                self.inject_fingerprint()
        except:
            pass

        for step in range(1, MAX_STEPS):
            if not self.is_valid_session():
                log("Session lost, stopping")
                break
                
            log(f"Step {step}")
            self.handle_popups()
            
            try:
                current_url = self.sb.get_current_url()
                if "youtube.com" in current_url:
                    log(f"SUCCESS: {current_url}")
                    try:
                        with open("real_link.txt", "w") as f:
                            f.write(current_url)
                    except:
                        pass
                    self.cleanup_browser_data()
                    return
            except:
                pass

            self.remove_overlays()
            time.sleep(0.5)

            selector = self.find_button()
            
            if selector:
                log(f"Found: {selector[:30]}...")
                try:
                    self.remove_overlays()
                    if self.sb.is_element_visible(selector):
                        self.sb.click(selector)
                        log(f"Clicked 1/2")
                        time.sleep(2)
                        self.handle_popups()
                        
                        try:
                            el_text = self.sb.get_text(selector).lower() if self.sb.is_element_visible(selector) else "link"
                        except:
                            el_text = "link"
                            
                        if "link" in el_text or "open" in el_text:
                            log(f"Double tap mode")
                            time.sleep(5)
                            self.back_to_anchor()
                            self.remove_overlays()
                            
                            if not self.sb.is_element_visible(selector):
                                selector = self.find_button()
                            
                            if selector and self.sb.click_if_visible(selector):
                                log(f"Clicked 2/2")
                        
                        time.sleep(WAIT_TIME)
                except Exception as e:
                    log(f"Error clicking: {str(e)[:50]}")
            else:
                log("No selector, trying fallback")
                targets = ["//span[contains(text(), 'OPEN LINK')]/..", "a:contains('Open')", "a:contains('Link')"]
                for t in targets:
                    try:
                        if self.sb.click_if_visible(t):
                            log(f"Fallback clicked")
                            time.sleep(WAIT_TIME)
                            break
                    except:
                        continue
        
        # Cleanup at the end
        self.cleanup_browser_data()

def main():
    config = {
        "uc": True,
        "incognito": True,
        "headless": False,
        "chromium_arg": "--disable-gpu,--no-sandbox,--disable-dev-shm-usage"
    }
    
    log("Running on Windows VPS (GUI mode)")
    
    try:
        with SB(**config) as sb:
            bot = SafelinkBypass(sb)
            bot.run()
    except KeyboardInterrupt:
        log("Stopped by user")
    except Exception as e:
        log(f"Fatal error: {e}")

if __name__ == "__main__":
    main()
