#!/bin/bash

set -e

# 🎨 Banner
banner() {
    echo -e "\e[1;36m"
    echo "╔══════════════════════════════════════╗"
    echo "║ 🔐 By Sayyad — Env Setup ║"
    echo "╚══════════════════════════════════════╝"
    echo -e "\e[0m"
}
banner

# 🧠 دوال مساعدة
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

package_installed() {
    pip show "$1" >/dev/null 2>&1
}

fix_pip() {
    echo "🚑 Running pip fix from GitHub..."
    curl -sL https://raw.githubusercontent.com/Sayyad-N/fix-pip/main/fix_pip_problems.sh -o fix-pip.sh

    if grep -q "404: Not Found" fix-pip.sh || ! grep -q "#!/bin/bash" fix-pip.sh; then
        echo -e "\e[1;31m❌ Failed to download or verify fix-pip.sh. Check the GitHub link!\e[0m"
        rm -f fix-pip.sh
        exit 1
    fi

    chmod +x fix-pip.sh
    echo "5" | ./fix-pip.sh
    rm -f fix-pip.sh
}

# ✅ التحقق من Python و pip
echo "🔍 Checking for Python3..."
if ! command_exists python3; then
    echo -e "\e[1;31m❌ Python3 not found. Please install it manually.\e[0m"
    exit 1
fi

echo "🔍 Checking for pip..."
if ! command_exists pip; then
    echo "⚠️ pip not found. Installing..."
    curl -sS https://bootstrap.pypa.io/get-pip.py -o get-pip.py
    python3 get-pip.py || python get-pip.py
    rm -f get-pip.py
fi

echo -e "\e[1;32m✅ Python and pip are ready.\e[0m"

# 📦 الحزم المطلوبة
PY_PACKAGES=("python-nmap" "google-genai" "colorama" )

ALL_INSTALLED=true

echo -e "\n⬇️ Checking Python packages..."
for pkg in "${PY_PACKAGES[@]}"; do
    if package_installed "$pkg"; then
        echo -e "✅ $pkg is already installed."
    else
        echo -e "📦 Installing $pkg..."
        if ! pip install "$pkg"; then
            echo -e "\e[1;33m⚠️ Failed to install $pkg. Trying pip fix...\e[0m"
            fix_pip
            if ! pip install "$pkg"; then
                echo -e "\n❓ \e[1;31mFailed to install $pkg even after pip fix.\e[0m"
                read -p "Do you want to continue without it? (y/n): " choice
                if [[ "$choice" =~ ^[Nn]$ ]]; then
                    echo -e "\n🛑 Aborting as requested by user."
                    exit 1
                else
                    echo -e "⚠️ Continuing without $pkg."
                fi
            fi
        fi
        ALL_INSTALLED=false
    fi
done


# ✅ تقرير نهائي
if $ALL_INSTALLED; then
    echo -e "\n🎉 \e[1;32mEverything is already installed. You're good to go, باشا!\e[0m"
else
    echo -e "\n✅ \e[1;32mSetup completed with some installations or fixes. All set!\e[0m"
fi

