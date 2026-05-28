import os
import sys
import time
import threading
import subprocess
import shutil



def clear():
    os.system("cls" if os.name == "nt" else "clear")


def width():
    return shutil.get_terminal_size((100, 30)).columns


def center(text, w=None):
    w = w or width()
    return text.center(w)


def cprint(text, color="", w=None):
    COLORS = {
        "red": "\033[91m",
        "green": "\033[92m",
        "yellow": "\033[93m",
        "blue": "\033[94m",
        "cyan": "\033[96m",
        "white": "\033[97m",
        "dim": "\033[2m",
        "bold": "\033[1m",
        "reset": "\033[0m",
    }

    prefix = COLORS.get(color, "")
    reset = COLORS["reset"] if color else ""

    print(prefix + center(text, w) + reset)


def hline(char="─", color="dim"):
    w = max(72, min(width(), 100))
    cprint(char * w, color)


# ============================================================================
# ASCII BANNERS
# ============================================================================

BANNER_SECLAB = r"""
 $$$$$$\  $$$$$$$$\  $$$$$$\  $$\        $$$$$$\  $$$$$$$\
$$  __$$\ $$  _____|$$  __$$\ $$ |      $$  __$$\ $$  __$$\
$$ /  \__|$$ |      $$ /  \__|$$ |      $$ /  $$ |$$ |  $$ |
\$$$$$$\  $$$$$\    $$ |      $$ |      $$$$$$$$ |$$$$$$$\ |
 \____$$\ $$  __|   $$ |      $$ |      $$  __$$ |$$  __$$\
$$\   $$ |$$ |      $$ |  $$\ $$ |      $$ |  $$ |$$ |  $$ |
\$$$$$$  |$$$$$$$$\ \$$$$$$  |$$$$$$$$\ $$ |  $$ |$$$$$$$  |
 \______/ \________| \______/ \________|\__|  \__|\_______/
"""

BANNER_PIRATE = r"""
                      .-.
                     (o.o)
                      |=|
                     __|__
                     //.=|=.\\
                     // .=|=. \\
                     \\ .=|=. //
                     \\(_=_)//
                     (:| |:)
                     || ||
                     () ()
                     || ||
                     || ||
                    ==' '==

              ☠  DEAD MEN'S BYTES  ☠
             ~ Hack the seas safely ~
"""

BANNERS = [BANNER_SECLAB, BANNER_PIRATE]



_banner_idx = 0
_banner_lock = threading.Lock()
_stop_animate = threading.Event()


def banner_cycle():
    global _banner_idx

    while not _stop_animate.is_set():
        time.sleep(5)

        with _banner_lock:
            _banner_idx = (_banner_idx + 1) % len(BANNERS)


def current_banner():
    with _banner_lock:
        return BANNERS[_banner_idx]


def typewrite(text, delay=0.025, color="cyan"):
    COLORS = {
        "cyan": "\033[96m",
        "green": "\033[92m",
        "dim": "\033[2m",
        "reset": "\033[0m",
    }

    prefix = COLORS.get(color, "")
    reset = COLORS["reset"]

    for ch in text:
        sys.stdout.write(prefix + ch + reset)
        sys.stdout.flush()
        time.sleep(delay)

    print()


def boot_sequence():
    clear()

    lines = [
        "[ SECLAB ] Initialising...",
        "[ OK ] Loading Cryptography Modules",
        "[ OK ] Loading Honeypot Module",
        "[ OK ] Loading Password Toolkit",
        "[ OK ] Loading Phishing Demo",
        "[ OK ] Loading SQL Injection Demo",
        "[ >> ] All modules armed. Welcome operator.",
    ]

    for line in lines:

        if "OK" in line:
            color = "green"

        elif ">>" in line:
            color = "cyan"

        else:
            color = "dim"

        typewrite("  " + line, color=color)

        time.sleep(0.1)

    time.sleep(0.5)



MENU = [
    ("1", "Cryptography", "cryptography"),
    ("2", "Honeypot Module", "honeypot"),
    ("3", "Password Tools", "passwords"),
    ("4", "Phishing Demo", "phishing"),
    ("5", "SQL Injection Demo", "sql"),
    ("0", "Exit", "exit"),
]

SUB_MENUS = {

    "cryptography": [

        ("1", "AES Encryption", "Cryptography/aes_demo.py"),
        ("2", "Base64 Encoder/Decoder", "Cryptography/base64_encoder_decoder.py"),
        ("3", "Caesar Cipher", "Cryptography/caesar_cipher.py"),
        ("4", "Digital Signature", "Cryptography/digital_signature_demo.py"),
        ("5", "File Hash Checker", "Cryptography/file_hash_checker.py"),
        ("6", "Hash Generator", "Cryptography/hash_generator.py"),
        ("7", "Hash Identifier", "Cryptography/hash_identifier.py"),
        ("8", "Hex Encoder/Decoder", "Cryptography/hex_encoder_decoder.py"),
        ("9", "RSA Demo", "Cryptography/rsa_demo.py"),
        ("10", "Secure File Encryptor", "Cryptography/secure_file_encryptor.py"),
        ("11", "Steganography", "Cryptography/Steganography.py"),
        ("12", "URL Encoder/Decoder", "Cryptography/url_encoder_decoder.py"),
        ("13", "Vigenere Cipher", "Cryptography/vigenere_cipher.py"),
        ("0", "Back", None),
    ],

    "honeypot": [
        ("1", "Run Honeypot", "Honeypot Module/honeypot.py"),
        ("0", "Back", None),
    ],

    "passwords": [
        ("1", "Attack Simulator", "passwords/attack_simulator.py"),
        ("2", "Common Password Detector", "passwords/commonpassworddetector.py"),
        ("3", "Password Generator", "passwords/generator.py"),
        ("4", "Entropy Calculator", "passwords/password_entropy_calculator.py"),
        ("5", "Strength Checker", "passwords/strength.py"),
        ("0", "Back", None),
    ],

    "phishing": [
        ("1", "Run Phishing Demo (Flask)", "Phishing demo/Phishing_demo.py"),
        ("0", "Back", None),
    ],

    "sql": [
        ("1", "Run SQL Injection Demo (Flask)", "Sql Injection Demo/sql_app.py"),
        ("0", "Back", None),
    ],
}

ICONS = {
    "cryptography": "🔐",
    "honeypot": "🍯",
    "passwords": "🔑",
    "phishing": "🎣",
    "sql": "🗄️",
    "exit": "🚪",
}


def render_header():

    clear()

    w = max(72, min(width(), 100))

    banner = current_banner()

    print("\033[96m")

    for line in banner.splitlines():
        print(line.center(w))

    print("\033[0m")

    hline("═", "cyan")

    cprint(
        "Security Education & Awareness Laboratory",
        "bold",
        w
    )

    cprint(
        "[ For Educational Purposes Only · Run Locally ]",
        "dim",
        w
    )

    hline("═", "cyan")

    print()



def render_main_menu():

    render_header()

    w = max(72, min(width(), 100))

    cprint("MAIN MENU", "yellow", w)

    print()

    for key, label, module in MENU:

        icon = ICONS.get(module, " ")

        line = f" [{key}]  {icon:<2}  {label:<30}"

        if key == "0":
            print("\033[91m" + center(line, w) + "\033[0m")

        else:
            print("\033[97m" + center(line, w) + "\033[0m")

    print()

    hline("─", "dim")


def render_sub_menu(module_key, title):

    render_header()

    w = max(72, min(width(), 100))

    cprint(
        f"{ICONS.get(module_key, '')}  {title.upper()}",
        "yellow",
        w
    )

    print()

    entries = SUB_MENUS.get(module_key, [])

    for key, label, _ in entries:

        if key == "0":

            line = f" [{key}]  ←  {label:<35}"

            print("\033[93m" + center(line, w) + "\033[0m")

        else:

            line = f" [{key:<2}]  {label:<40}"

            print("\033[97m" + center(line, w) + "\033[0m")

    print()

    hline("─", "dim")


def launch(script_path):

    abs_path = os.path.join(
        os.path.dirname(os.path.abspath(__file__)),
        script_path
    )

    if not os.path.exists(abs_path):

        print(f"\n\033[91m[!] Script not found:\033[0m {abs_path}")

        input("\nPress ENTER to continue...")

        return

    print(f"\n\033[96m[>>] Launching: {script_path}\033[0m\n")

    time.sleep(0.4)
    try:
        process = subprocess.Popen(
            [sys.executable, abs_path]
        )
        process.wait()
    except KeyboardInterrupt:
        print("\n\n[!] Stopping module...")
        process.terminate()
        try:
            process.wait(timeout=2)
        except:
            process.kill()
    print("\n\033[93m[<<] Module finished.\033[0m")

    input("\n\033[92mPress ENTER to return to menu...\033[0m")


def sub_menu_loop(module_key, title):

    entries = SUB_MENUS.get(module_key, [])

    lookup = {entry[0]: entry for entry in entries}

    while True:

        render_sub_menu(module_key, title)

        choice = input(
            "\n\033[92m[ SECLAB ] >> \033[0m"
        ).strip()

        if choice not in lookup:

            print("\033[91m\n[!] Invalid option.\033[0m")

            time.sleep(1)

            continue

        key, label, script = lookup[choice]

        if script is None:
            return

        launch(script)


def main():

    animation_thread = threading.Thread(
        target=banner_cycle,
        daemon=True
    )

    animation_thread.start()

    boot_sequence()

    menu_lookup = {entry[0]: entry for entry in MENU}

    while True:

        render_main_menu()

        choice = input(
            "\n\033[92m[ SECLAB ] >> \033[0m"
        ).strip()

        if choice not in menu_lookup:

            print("\033[91m\n[!] Invalid option. Try again.\033[0m")

            time.sleep(1)

            continue

        key, label, module = menu_lookup[choice]

        if module == "exit":

            clear()

            print("\n\033[96m")

            msg = "[ SECLAB ] Shutting down... Stay curious, stay ethical."

            print(msg.center(max(72, min(width(), 100))))

            print("\033[0m\n")

            _stop_animate.set()

            sys.exit(0)

        sub_menu_loop(module, label)


if __name__ == "__main__":

    try:
        main()

    except KeyboardInterrupt:

        clear()

        print("\n\033[93m[!] Interrupted. Goodbye.\033[0m\n")

        sys.exit(0)