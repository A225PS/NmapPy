# تمت كتابه وتعريب الكود بواسطه محمد الصياد
# الإصدار: Autonomous Execution Edition 3.0
# تاريخ التعديل: 25 شوّال 1447

import nmap
import os
import sys
import json
import datetime
from google import genai
from colorama import Fore, init

init(autoreset=True)

# --- الإعدادات المركزية ---
DEFAULT_MODEL = "gemini"
GEMINI_API_KEY = "YOUR_API_HERE"
GEMINI_MODEL = "gemini-3-flash-preview"
RESULTS_DIR = "results"

def root_checker():
    if os.geteuid() != 0:
        print(Fore.RED + "[-] خطأ: يجب تشغيل الأداة بصلاحيات sudo للتنفيذ المباشر.")
        sys.exit(1)

def import_ai_config():
    config_path = os.path.join("sources", "ai_config.txt")
    if not os.path.exists(config_path):
        return "Role: Autonomous Cyber Executor. Protocol: Absolute Mode. Execute via Python-Nmap."
    with open(config_path, "r", encoding="utf-8") as f:
        return f.read()

def call_ai(prompt_input):
    try:
        client = genai.Client(api_key=GEMINI_API_KEY)
        response = client.models.generate_content(
            model=GEMINI_MODEL,
            contents=f"{import_ai_config()}\n\nUser Request: {prompt_input}"
        )
        return response.text.strip()
    except Exception as e:
        print(Fore.RED + f"[-] فشل محرك الذكاء الاصطناعي: {e}")
        return None

def execute_and_report(target, user_input):
    """المحرك التنفيذي: يحلل، ينفذ، ويؤرشف فوراً"""
    start_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    # 1. الحصول على "أمر التنفيذ" فقط من الـ AI
    decision = call_ai(f"Target: {target} | Task: {user_input} | Output ONLY the command starting with 'EXEC:'")
    
    if decision and "EXEC:" in decision:
        raw_cmd = decision.split("EXEC:")[1].split("\n")[0].strip()
        # تنظيف الأوامر لاستخدامها في المكتبة
        clean_args = raw_cmd.replace("nmap", "").replace(target, "").strip()
        
        print(Fore.MAGENTA + f"🚀 جاري التنفيذ الذاتي: nmap {clean_args} {target}")
        
        try:
            nm = nmap.PortScanner()
            nm.scan(target, arguments=clean_args)
            
            # 2. إرسال النتائج الخام للـ AI لصياغة التقرير الحرفي
            tech_data = nm[target] if target in nm.all_hosts() else {"error": "Target unreachable"}
            print(Fore.BLUE + "[*] جاري تحليل مخرجات النظام وتوليد التقرير الشامل...")
            
            final_report = call_ai(f"Generate a LITERAL and COMPREHENSIVE report for this scan data: {tech_data}. Start with the date {start_time}.")
            
            # 3. العرض والأرشفة القسرية
            print("\n" + Fore.GREEN + "="*60)
            print(final_report)
            print(Fore.GREEN + "="*60)
            
            # حفظ الملف
            if not os.path.exists(RESULTS_DIR): os.makedirs(RESULTS_DIR)
            filename = f"{RESULTS_DIR}/Report_{target}_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
            with open(filename, "w", encoding="utf-8") as f:
                f.write(f"--- AUTONOMOUS EXECUTION LOG ---\nTarget: {target}\nDate: {start_time}\nIntent: {user_input}\nCommand: nmap {clean_args}\n")
                f.write("="*50 + "\n" + final_report)
            
            print(Fore.YELLOW + f"✅ تم التنفيذ والأرشفة حرفياً في: {filename}")
            
        except Exception as e:
            print(Fore.RED + f"❌ خطأ أثناء التنفيذ البرمجي: {e}")

def main():
    root_checker()
    print(Fore.GREEN + "--- SNmapPy: Autonomous Executor v4.0 ---")
    target = input(Fore.YELLOW + "أدخل الهدف: ").strip()
    
    if target:
        while True:
            u_input = input(Fore.WHITE + "\nماذا تريد تنفيذه الآن؟ (أو 'exit'): ").strip()
            if u_input.lower() in ['exit', 'quit', 'خروج']: break
            execute_and_report(target, u_input)

if __name__ == "__main__":
    main()
