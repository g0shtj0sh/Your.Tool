import re
import os
import sys
from Config.Util import *
from Config.Config import *
from Config.Translates import *

current_language = LANGUAGE

def tr(key):
    return translations[current_language].get(key, key)


def load_common_passwords(file_path):
    if not os.path.exists(file_path):
        print(f"{tr('Error')} {tr('File')} {file_path} {tr('NotExist')}")
        return []
    
    with open(file_path, 'r', encoding='utf-8', errors='ignore') as file:
        return [line.strip() for line in file]


def load_dictionary(file_path):
    if not os.path.exists(file_path):
        print(f"{tr('Error')} {tr('File')} {file_path} {tr('NotExist')}")
        return []
    
    with open(file_path, 'r', encoding='utf-8', errors='ignore') as file:
        return [line.strip() for line in file]


def has_repetitive_or_sequential_patterns(password):
    return re.search(r'(.)\1{2,}', password) or re.search(r'012|123|234|345|456|567|678|789|890', password)


def has_sequential_characters(password):
    sequences = [
        'abcdefghijklmnopqrstuvwxyz',
        'ABCDEFGHIJKLMNOPQRSTUVWXYZ',
        '0123456789',
        'qwertyuiop',
        'asdfghjkl',
        'zxcvbnm',
        'QWERTYUIOP',
        'ASDFGHJKL',
        'ZXCVBNM'
    ]
    for seq in sequences:
        if any(seq[i:i+3] in password for i in range(len(seq)-2)):
            return True
    return False


def evaluate_password_strength(password, common_passwords, dictionary_words):
    score = 0
    feedback = []
    
    # Length check
    if len(password) < 8:
        feedback.append("Password is too short")
        score -= 20
    elif len(password) >= 12:
        feedback.append("Good length")
        score += 20
    elif len(password) >= 16:
        feedback.append("Excellent length")
        score += 30
    
    # Complexity checks
    if re.search(r'[A-Z]', password):
        score += 10
    else:
        feedback.append("Missing uppercase letters")
    
    if re.search(r'[a-z]', password):
        score += 10
    else:
        feedback.append("Missing lowercase letters")
    
    if re.search(r'[0-9]', password):
        score += 10
    else:
        feedback.append("Missing numbers")
    
    if re.search(r'[^A-Za-z0-9]', password):
        score += 20
    else:
        feedback.append("Missing special characters")
    
    # Check for common passwords
    if password.lower() in [p.lower() for p in common_passwords]:
        feedback.append("This is a common password")
        score -= 40
    
    # Check if it's a dictionary word
    if password.lower() in [w.lower() for w in dictionary_words]:
        feedback.append("This is a dictionary word")
        score -= 20
    
    # Check for sequences and repeats
    if re.search(r'(abc|bcd|cde|def|efg|fgh|ghi|hij|ijk|jkl|klm|lmn|mno|nop|opq|pqr|qrs|rst|stu|tuv|uvw|vwx|wxy|xyz|012|123|234|345|456|567|678|789|890)', password.lower()):
        feedback.append("Contains sequential characters")
        score -= 15
    
    if re.search(r'(.)\1{2,}', password):
        feedback.append("Contains repeated characters")
        score -= 15
    
    # Normalize score
    score = max(0, min(100, score))
    
    # Determine strength based on score
    if score < 40:
        strength = f"{color.RED}Weak{color.RESET}"
        color_code = color.RED
    elif score < 70:
        strength = f"{color.YELLOW}Moderate{color.RESET}"
        color_code = color.YELLOW
    else:
        strength = f"{color.GREEN}Strong{color.RESET}"
        color_code = color.GREEN
    
    return strength, color_code, score

def estimate_brute_force_time(password):
    charset_size = 0
    
    if re.search(r'[a-z]', password):
        charset_size += 26
    if re.search(r'[A-Z]', password):
        charset_size += 26
    if re.search(r'[0-9]', password):
        charset_size += 10
    if re.search(r'[^A-Za-z0-9]', password):
        charset_size += 33  # Common special characters
    
    if charset_size == 0:
        charset_size = 26  # Default to lowercase if no character set detected
    
    # Estimated attempts per second for different scenarios
    attempts_per_second = {
        'online': 10,
        'offline_slow': 10000,
        'offline_fast': 1e9,
        'cluster': 1e12
    }
    
    length = len(password)
    combinations = charset_size ** length
    
    times = {}
    for scenario, attempts in attempts_per_second.items():
        seconds = combinations / attempts
        
        # Convert to appropriate time units
        if seconds < 60:
            times[scenario] = f"{seconds:.2f} seconds"
        elif seconds < 3600:
            times[scenario] = f"{seconds/60:.2f} minutes"
        elif seconds < 86400:
            times[scenario] = f"{seconds/3600:.2f} hours"
        elif seconds < 31536000:
            times[scenario] = f"{seconds/86400:.2f} days"
        elif seconds < 315360000:
            times[scenario] = f"{seconds/31536000:.2f} years"
        else:
            times[scenario] = f"{seconds:.2e} seconds"
    
    return times

def display_progress_bar(percentage, length=50):
    filled_length = int(length * percentage / 100)
    bar = '█' * filled_length + '▒' * (length - filled_length)
    
    # Color code based on percentage
    if percentage < 30:
        color_code = '\033[91m'  # Red
    elif percentage < 70:
        color_code = '\033[93m'  # Yellow
    else:
        color_code = '\033[92m'  # Green
        
    reset_code = '\033[0m'
    return f"{color_code}{bar} {percentage:.1f}%{reset_code}"

def main():
    # Chemins par défaut des fichiers txt
    default_common_passwords_file = '2-Input/Passwords/common_passwords.txt'
    default_dictionary_file = '2-Input/Passwords/dictionary.txt'
    

    common_passwords_file = sys.argv[1] if len(sys.argv) > 1 else default_common_passwords_file
    dictionary_file = sys.argv[2] if len(sys.argv) > 2 else default_dictionary_file
    

    common_passwords = load_common_passwords(common_passwords_file)
    dictionary_words = load_dictionary(dictionary_file)
    
    password = input(f"\n{BEFORE + current_time_hour() + AFTER} {INPUT} {tr('PassEvaluate')} -> {reset}")
    
    strength, color, score_percentage = evaluate_password_strength(password, common_passwords, dictionary_words)
    time_to_crack = estimate_brute_force_time(password)
    
    print(f"\n{tr('PassStrength')}: {strength}")
    print(display_progress_bar(score_percentage))
    print(f"\n{BEFORE + current_time_hour() + AFTER} {WAIT} {tr('TimeCrackPass')}: {reset}\n")
    for unit, time in time_to_crack.items():
        print(f"{BEFORE + current_time_hour() + AFTER}{primary}{unit.capitalize()}: {secondary}{time:.2e}\n")

    input(f"{BEFORE + current_time_hour() + AFTER} {INFO} Press to continue -> " + reset)
    Reset()

if __name__ == "__main__":
    main()

