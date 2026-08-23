import os

# Generates clean, colorful SVG food illustrations for all menu dishes and canteens
food_svgs = {
    "chicken_biryani.jpg": '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 400 300" width="100%" height="100%">
  <defs>
    <linearGradient id="bg" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#ea580c"/>
      <stop offset="100%" stop-color="#9a3412"/>
    </linearGradient>
    <radialGradient id="rice" cx="50%" cy="50%" r="50%">
      <stop offset="0%" stop-color="#fef08a"/>
      <stop offset="60%" stop-color="#f59e0b"/>
      <stop offset="100%" stop-color="#d97706"/>
    </radialGradient>
  </defs>
  <rect width="400" height="300" fill="url(#bg)"/>
  <!-- Bowl -->
  <ellipse cx="200" cy="180" rx="140" ry="80" fill="#1e293b"/>
  <ellipse cx="200" cy="165" rx="130" ry="70" fill="#334155"/>
  <ellipse cx="200" cy="155" rx="120" ry="60" fill="url(#rice)"/>
  <!-- Spices & Chicken pieces -->
  <ellipse cx="170" cy="140" rx="35" ry="25" fill="#78350f" transform="rotate(-15 170 140)"/>
  <ellipse cx="235" cy="150" rx="40" ry="28" fill="#991b1b" transform="rotate(10 235 150)"/>
  <circle cx="150" cy="165" r="7" fill="#15803d"/>
  <circle cx="210" cy="130" r="6" fill="#16a34a"/>
  <circle cx="250" cy="165" r="8" fill="#15803d"/>
  <ellipse cx="195" cy="160" rx="18" ry="12" fill="#fff" stroke="#f59e0b" stroke-width="2"/>
  <circle cx="195" cy="160" r="6" fill="#fbbf24"/>
  <!-- Tag -->
  <rect x="20" y="20" width="160" height="36" rx="18" fill="rgba(0,0,0,0.6)"/>
  <text x="100" y="44" fill="#fde047" font-family="system-ui, sans-serif" font-weight="bold" font-size="16" text-anchor="middle">🍗 Dum Biryani</text>
</svg>''',

    "thokku_biryani.jpg": '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 400 300" width="100%" height="100%">
  <rect width="400" height="300" fill="#881337"/>
  <ellipse cx="200" cy="180" rx="140" ry="80" fill="#18181b"/>
  <ellipse cx="200" cy="165" rx="130" ry="70" fill="#27272a"/>
  <ellipse cx="200" cy="155" rx="120" ry="60" fill="#d97706"/>
  <!-- Rich spicy Thokku gravy layer -->
  <ellipse cx="200" cy="150" rx="80" ry="40" fill="#991b1b" opacity="0.9"/>
  <ellipse cx="180" cy="140" rx="35" ry="22" fill="#450a0a"/>
  <circle cx="220" cy="145" r="7" fill="#16a34a"/>
  <circle cx="170" cy="160" r="6" fill="#15803d"/>
  <rect x="20" y="20" width="170" height="36" rx="18" fill="rgba(0,0,0,0.6)"/>
  <text x="105" y="44" fill="#fca5a5" font-family="system-ui, sans-serif" font-weight="bold" font-size="16" text-anchor="middle">🌶️ Thokku Biryani</text>
</svg>''',

    "chili_biryani.jpg": '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 400 300" width="100%" height="100%">
  <rect width="400" height="300" fill="#7f1d1d"/>
  <ellipse cx="200" cy="180" rx="140" ry="80" fill="#18181b"/>
  <ellipse cx="200" cy="165" rx="130" ry="70" fill="#b91c1c"/>
  <ellipse cx="200" cy="155" rx="120" ry="60" fill="#d97706"/>
  <!-- Crispy chili chicken bites -->
  <circle cx="160" cy="145" r="18" fill="#dc2626"/>
  <circle cx="200" cy="135" r="16" fill="#b91c1c"/>
  <circle cx="240" cy="150" r="18" fill="#dc2626"/>
  <circle cx="190" cy="165" r="15" fill="#991b1b"/>
  <rect x="20" y="20" width="160" height="36" rx="18" fill="rgba(0,0,0,0.6)"/>
  <text x="100" y="44" fill="#fecaca" font-family="system-ui, sans-serif" font-weight="bold" font-size="16" text-anchor="middle">🔥 Chili Biryani</text>
</svg>''',

    "veg_biryani.jpg": '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 400 300" width="100%" height="100%">
  <rect width="400" height="300" fill="#065f46"/>
  <ellipse cx="200" cy="180" rx="140" ry="80" fill="#1e293b"/>
  <ellipse cx="200" cy="165" rx="130" ry="70" fill="#334155"/>
  <ellipse cx="200" cy="155" rx="120" ry="60" fill="#fef08a"/>
  <!-- Paneer, peas, carrots -->
  <rect x="150" y="130" width="22" height="22" rx="4" fill="#f8fafc" stroke="#f59e0b"/>
  <rect x="220" y="145" width="20" height="20" rx="4" fill="#f8fafc" stroke="#f59e0b"/>
  <circle cx="185" cy="160" r="8" fill="#16a34a"/>
  <circle cx="210" cy="135" r="7" fill="#15803d"/>
  <circle cx="250" cy="140" r="8" fill="#ea580c"/>
  <circle cx="170" cy="140" r="7" fill="#ea580c"/>
  <rect x="20" y="20" width="160" height="36" rx="18" fill="rgba(0,0,0,0.6)"/>
  <text x="100" y="44" fill="#86efac" font-family="system-ui, sans-serif" font-weight="bold" font-size="16" text-anchor="middle">🌿 Veg Biryani</text>
</svg>''',

    "chicken_rice.jpg": '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 400 300" width="100%" height="100%">
  <rect width="400" height="300" fill="#b45309"/>
  <ellipse cx="200" cy="180" rx="140" ry="80" fill="#18181b"/>
  <ellipse cx="200" cy="160" rx="125" ry="65" fill="#fed7aa"/>
  <!-- Fried chicken cubes & veggies -->
  <ellipse cx="160" cy="145" rx="20" ry="14" fill="#9a3412"/>
  <ellipse cx="230" cy="140" rx="22" ry="15" fill="#9a3412"/>
  <ellipse cx="195" cy="165" rx="18" ry="12" fill="#78350f"/>
  <rect x="175" y="140" width="15" height="6" rx="2" fill="#16a34a"/>
  <rect x="215" y="160" width="14" height="5" rx="2" fill="#ea580c"/>
  <rect x="20" y="20" width="160" height="36" rx="18" fill="rgba(0,0,0,0.6)"/>
  <text x="100" y="44" fill="#ffedd5" font-family="system-ui, sans-serif" font-weight="bold" font-size="16" text-anchor="middle">🍲 Chicken Rice</text>
</svg>''',

    "chicken_noodles.jpg": '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 400 300" width="100%" height="100%">
  <rect width="400" height="300" fill="#c2410c"/>
  <ellipse cx="200" cy="180" rx="140" ry="80" fill="#0f172a"/>
  <ellipse cx="200" cy="160" rx="125" ry="65" fill="#fef08a"/>
  <!-- Noodles strands -->
  <path d="M 120 160 Q 150 130 190 160 T 250 140 T 280 165" stroke="#ca8a04" stroke-width="6" fill="none"/>
  <path d="M 130 145 Q 170 120 210 150 T 270 135" stroke="#eab308" stroke-width="5" fill="none"/>
  <path d="M 140 170 Q 180 140 220 165 T 260 155" stroke="#ca8a04" stroke-width="5" fill="none"/>
  <!-- Chicken shreds & capsicum -->
  <rect x="165" y="140" width="22" height="10" rx="3" fill="#831843"/>
  <rect x="220" y="150" width="20" height="9" rx="3" fill="#831843"/>
  <rect x="190" y="130" width="15" height="5" rx="2" fill="#16a34a"/>
  <rect x="20" y="20" width="170" height="36" rx="18" fill="rgba(0,0,0,0.6)"/>
  <text x="105" y="44" fill="#fef08a" font-family="system-ui, sans-serif" font-weight="bold" font-size="16" text-anchor="middle">🍜 Chicken Noodles</text>
</svg>''',

    "egg_rice.jpg": '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 400 300" width="100%" height="100%">
  <rect width="400" height="300" fill="#ca8a04"/>
  <ellipse cx="200" cy="180" rx="140" ry="80" fill="#18181b"/>
  <ellipse cx="200" cy="160" rx="125" ry="65" fill="#fef9c3"/>
  <!-- Scrambled eggs & greens -->
  <ellipse cx="160" cy="145" rx="25" ry="16" fill="#facc15"/>
  <ellipse cx="225" cy="140" rx="28" ry="17" fill="#facc15"/>
  <ellipse cx="195" cy="165" rx="22" ry="14" fill="#eab308"/>
  <circle cx="180" cy="140" r="5" fill="#16a34a"/>
  <circle cx="210" cy="155" r="5" fill="#16a34a"/>
  <rect x="20" y="20" width="150" height="36" rx="18" fill="rgba(0,0,0,0.6)"/>
  <text x="95" y="44" fill="#fef08a" font-family="system-ui, sans-serif" font-weight="bold" font-size="16" text-anchor="middle">🍳 Egg Rice</text>
</svg>''',

    "egg_noodles.jpg": '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 400 300" width="100%" height="100%">
  <rect width="400" height="300" fill="#d97706"/>
  <ellipse cx="200" cy="180" rx="140" ry="80" fill="#1e293b"/>
  <ellipse cx="200" cy="160" rx="125" ry="65" fill="#fef08a"/>
  <path d="M 120 155 Q 160 125 200 155 T 260 145" stroke="#ca8a04" stroke-width="5" fill="none"/>
  <ellipse cx="175" cy="145" rx="20" ry="14" fill="#facc15"/>
  <ellipse cx="225" cy="150" rx="22" ry="15" fill="#facc15"/>
  <rect x="20" y="20" width="160" height="36" rx="18" fill="rgba(0,0,0,0.6)"/>
  <text x="100" y="44" fill="#fef9c3" font-family="system-ui, sans-serif" font-weight="bold" font-size="16" text-anchor="middle">🍜 Egg Noodles</text>
</svg>''',

    "kothu_parotta.jpg": '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 400 300" width="100%" height="100%">
  <rect width="400" height="300" fill="#7c2d12"/>
  <ellipse cx="200" cy="180" rx="140" ry="80" fill="#18181b"/>
  <ellipse cx="200" cy="160" rx="125" ry="65" fill="#d97706"/>
  <!-- Shredded parotta pieces, salna & egg -->
  <polygon points="150,140 170,130 165,155" fill="#fed7aa"/>
  <polygon points="210,145 235,135 225,160" fill="#fed7aa"/>
  <polygon points="180,160 200,150 195,170" fill="#fde68a"/>
  <circle cx="190" cy="140" r="15" fill="#b45309" opacity="0.8"/>
  <circle cx="160" cy="160" r="6" fill="#16a34a"/>
  <rect x="20" y="20" width="170" height="36" rx="18" fill="rgba(0,0,0,0.6)"/>
  <text x="105" y="44" fill="#fed7aa" font-family="system-ui, sans-serif" font-weight="bold" font-size="16" text-anchor="middle">🥘 Kothu Parotta</text>
</svg>''',

    "curd_rice.jpg": '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 400 300" width="100%" height="100%">
  <rect width="400" height="300" fill="#0284c7"/>
  <ellipse cx="200" cy="180" rx="140" ry="80" fill="#1e293b"/>
  <ellipse cx="200" cy="160" rx="125" ry="65" fill="#f8fafc"/>
  <!-- Pomegranate, mustard, coriander, chili -->
  <circle cx="170" cy="145" r="5" fill="#dc2626"/>
  <circle cx="185" cy="155" r="5" fill="#dc2626"/>
  <circle cx="220" cy="140" r="5" fill="#dc2626"/>
  <circle cx="235" cy="155" r="5" fill="#dc2626"/>
  <circle cx="195" cy="145" r="3" fill="#18181b"/>
  <circle cx="210" cy="160" r="3" fill="#18181b"/>
  <rect x="190" y="135" width="14" height="4" rx="1" fill="#16a34a"/>
  <rect x="20" y="20" width="150" height="36" rx="18" fill="rgba(0,0,0,0.6)"/>
  <text x="95" y="44" fill="#e0f2fe" font-family="system-ui, sans-serif" font-weight="bold" font-size="16" text-anchor="middle">🥣 Curd Rice</text>
</svg>''',

    "sambar_rice.jpg": '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 400 300" width="100%" height="100%">
  <rect width="400" height="300" fill="#c2410c"/>
  <ellipse cx="200" cy="180" rx="140" ry="80" fill="#1e293b"/>
  <ellipse cx="200" cy="160" rx="125" ry="65" fill="#f97316"/>
  <!-- Ghee drizzle & curry leaves & appalam -->
  <circle cx="200" cy="155" r="22" fill="#fef08a" opacity="0.8"/>
  <circle cx="240" cy="140" r="25" fill="#fed7aa" stroke="#ca8a04" stroke-width="2"/>
  <circle cx="160" cy="150" r="6" fill="#15803d"/>
  <circle cx="180" cy="165" r="5" fill="#15803d"/>
  <rect x="20" y="20" width="160" height="36" rx="18" fill="rgba(0,0,0,0.6)"/>
  <text x="100" y="44" fill="#ffedd5" font-family="system-ui, sans-serif" font-weight="bold" font-size="16" text-anchor="middle">🍲 Sambar Rice</text>
</svg>''',

    "tomato_rice.jpg": '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 400 300" width="100%" height="100%">
  <rect width="400" height="300" fill="#b91c1c"/>
  <ellipse cx="200" cy="180" rx="140" ry="80" fill="#18181b"/>
  <ellipse cx="200" cy="160" rx="125" ry="65" fill="#ef4444"/>
  <circle cx="170" cy="145" r="8" fill="#fef08a"/>
  <circle cx="225" cy="150" r="8" fill="#fef08a"/>
  <circle cx="195" cy="160" r="5" fill="#16a34a"/>
  <rect x="20" y="20" width="160" height="36" rx="18" fill="rgba(0,0,0,0.6)"/>
  <text x="100" y="44" fill="#fee2e2" font-family="system-ui, sans-serif" font-weight="bold" font-size="16" text-anchor="middle">🍅 Tomato Rice</text>
</svg>''',

    "lime_juice.jpg": '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 400 300" width="100%" height="100%">
  <rect width="400" height="300" fill="#65a30d"/>
  <!-- Glass -->
  <polygon points="160,80 240,80 225,230 175,230" fill="#bef264" opacity="0.85" stroke="#f7fee7" stroke-width="3"/>
  <ellipse cx="200" cy="80" rx="40" ry="12" fill="#d9f99d"/>
  <!-- Straw -->
  <line x1="220" y1="40" x2="190" y2="200" stroke="#f43f5e" stroke-width="8" stroke-linecap="round"/>
  <!-- Lemon slice & mint -->
  <circle cx="160" cy="80" r="22" fill="#facc15" stroke="#65a30d" stroke-width="4"/>
  <circle cx="190" cy="110" r="7" fill="#15803d"/>
  <rect x="20" y="20" width="160" height="36" rx="18" fill="rgba(0,0,0,0.6)"/>
  <text x="100" y="44" fill="#f7fee7" font-family="system-ui, sans-serif" font-weight="bold" font-size="16" text-anchor="middle">🍋 Lime Juice</text>
</svg>''',

    "orange_juice.jpg": '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 400 300" width="100%" height="100%">
  <rect width="400" height="300" fill="#ea580c"/>
  <polygon points="160,80 240,80 225,230 175,230" fill="#fb923c" opacity="0.9" stroke="#fff7ed" stroke-width="3"/>
  <ellipse cx="200" cy="80" rx="40" ry="12" fill="#fdba74"/>
  <line x1="220" y1="40" x2="190" y2="200" stroke="#0284c7" stroke-width="8" stroke-linecap="round"/>
  <circle cx="160" cy="80" r="24" fill="#ea580c" stroke="#fed7aa" stroke-width="4"/>
  <rect x="20" y="20" width="160" height="36" rx="18" fill="rgba(0,0,0,0.6)"/>
  <text x="100" y="44" fill="#fff7ed" font-family="system-ui, sans-serif" font-weight="bold" font-size="16" text-anchor="middle">🍊 Orange Juice</text>
</svg>''',

    "watermelon_juice.jpg": '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 400 300" width="100%" height="100%">
  <rect width="400" height="300" fill="#be123c"/>
  <polygon points="160,80 240,80 225,230 175,230" fill="#f43f5e" opacity="0.9" stroke="#fff1f2" stroke-width="3"/>
  <ellipse cx="200" cy="80" rx="40" ry="12" fill="#fda4af"/>
  <line x1="220" y1="40" x2="190" y2="200" stroke="#16a34a" stroke-width="8" stroke-linecap="round"/>
  <circle cx="190" cy="130" r="4" fill="#18181b"/>
  <circle cx="205" cy="160" r="4" fill="#18181b"/>
  <circle cx="185" cy="180" r="4" fill="#18181b"/>
  <rect x="20" y="20" width="180" height="36" rx="18" fill="rgba(0,0,0,0.6)"/>
  <text x="110" y="44" fill="#ffe4e6" font-family="system-ui, sans-serif" font-weight="bold" font-size="16" text-anchor="middle">🍉 Watermelon Cooler</text>
</svg>''',

    "chocolate_shake.jpg": '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 400 300" width="100%" height="100%">
  <rect width="400" height="300" fill="#451a03"/>
  <polygon points="160,80 240,80 225,230 175,230" fill="#78350f" opacity="0.9" stroke="#fef3c7" stroke-width="3"/>
  <ellipse cx="200" cy="80" rx="40" ry="12" fill="#92400e"/>
  <ellipse cx="200" cy="75" rx="35" ry="18" fill="#fffbeb"/>
  <line x1="220" y1="35" x2="190" y2="190" stroke="#b45309" stroke-width="8" stroke-linecap="round"/>
  <rect x="20" y="20" width="180" height="36" rx="18" fill="rgba(0,0,0,0.6)"/>
  <text x="110" y="44" fill="#fde68a" font-family="system-ui, sans-serif" font-weight="bold" font-size="16" text-anchor="middle">🍫 Chocolate Shake</text>
</svg>''',

    "cold_coffee.jpg": '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 400 300" width="100%" height="100%">
  <rect width="400" height="300" fill="#3b1d0c"/>
  <polygon points="160,80 240,80 225,230 175,230" fill="#a16207" opacity="0.9" stroke="#fefce8" stroke-width="3"/>
  <ellipse cx="200" cy="80" rx="40" ry="12" fill="#ca8a04"/>
  <ellipse cx="200" cy="74" rx="35" ry="16" fill="#fef9c3"/>
  <line x1="220" y1="35" x2="190" y2="190" stroke="#64748b" stroke-width="8" stroke-linecap="round"/>
  <rect x="20" y="20" width="160" height="36" rx="18" fill="rgba(0,0,0,0.6)"/>
  <text x="100" y="44" fill="#fef08a" font-family="system-ui, sans-serif" font-weight="bold" font-size="16" text-anchor="middle">☕ Cold Coffee</text>
</svg>''',
}

canteen_svgs = {
    "canteen_chatstop.jpg": '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 600 350" width="100%" height="100%">
  <defs>
    <linearGradient id="g1" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#ea580c"/>
      <stop offset="100%" stop-color="#7c2d12"/>
    </linearGradient>
  </defs>
  <rect width="600" height="350" fill="url(#g1)"/>
  <text x="300" y="140" fill="#fff" font-family="system-ui, sans-serif" font-weight="900" font-size="42" text-anchor="middle">CHAT STOP</text>
  <text x="300" y="185" fill="#fde047" font-family="system-ui, sans-serif" font-weight="600" font-size="20" text-anchor="middle">Biryani • Fried Rice • Noodles • Fast Bites</text>
  <rect x="210" y="220" width="180" height="40" rx="20" fill="rgba(0,0,0,0.4)"/>
  <text x="300" y="246" fill="#fff" font-family="system-ui, sans-serif" font-weight="bold" font-size="16" text-anchor="middle">Near Main Block</text>
</svg>''',

    "canteen_zcafe.jpg": '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 600 350" width="100%" height="100%">
  <defs>
    <linearGradient id="g2" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#0284c7"/>
      <stop offset="100%" stop-color="#1e1b4b"/>
    </linearGradient>
  </defs>
  <rect width="600" height="350" fill="url(#g2)"/>
  <text x="300" y="140" fill="#fff" font-family="system-ui, sans-serif" font-weight="900" font-size="42" text-anchor="middle">Z-CAFE</text>
  <text x="300" y="185" fill="#38bdf8" font-family="system-ui, sans-serif" font-weight="600" font-size="20" text-anchor="middle">Trendy Student Cafe • Express Orders</text>
  <rect x="190" y="220" width="220" height="40" rx="20" fill="rgba(0,0,0,0.4)"/>
  <text x="300" y="246" fill="#fff" font-family="system-ui, sans-serif" font-weight="bold" font-size="16" text-anchor="middle">Opp. Engineering Block 2</text>
</svg>''',

    "canteen_seyon.jpg": '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 600 350" width="100%" height="100%">
  <defs>
    <linearGradient id="g3" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#16a34a"/>
      <stop offset="100%" stop-color="#064e3b"/>
    </linearGradient>
  </defs>
  <rect width="600" height="350" fill="url(#g3)"/>
  <text x="300" y="140" fill="#fff" font-family="system-ui, sans-serif" font-weight="900" font-size="42" text-anchor="middle">SEYON</text>
  <text x="300" y="185" fill="#86efac" font-family="system-ui, sans-serif" font-weight="600" font-size="20" text-anchor="middle">Authentic South Indian Meals • Express Parcel</text>
  <rect x="180" y="220" width="240" height="40" rx="20" fill="rgba(0,0,0,0.4)"/>
  <text x="300" y="246" fill="#fff" font-family="system-ui, sans-serif" font-weight="bold" font-size="16" text-anchor="middle">Architecture Campus Desk</text>
</svg>''',

    "canteen_cct.jpg": '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 600 350" width="100%" height="100%">
  <defs>
    <linearGradient id="g4" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#9333ea"/>
      <stop offset="100%" stop-color="#4c1d95"/>
    </linearGradient>
  </defs>
  <rect width="600" height="350" fill="url(#g4)"/>
  <text x="300" y="140" fill="#fff" font-family="system-ui, sans-serif" font-weight="900" font-size="42" text-anchor="middle">CCT (Central Campus Treat)</text>
  <text x="300" y="185" fill="#d8b4fe" font-family="system-ui, sans-serif" font-weight="600" font-size="20" text-anchor="middle">King Biryani • Kothu Parotta • Hot Meals</text>
  <rect x="200" y="220" width="200" height="40" rx="20" fill="rgba(0,0,0,0.4)"/>
  <text x="300" y="246" fill="#fff" font-family="system-ui, sans-serif" font-weight="bold" font-size="16" text-anchor="middle">Central Food Court</text>
</svg>''',

    "canteen_juice.jpg": '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 600 350" width="100%" height="100%">
  <defs>
    <linearGradient id="g5" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#059669"/>
      <stop offset="100%" stop-color="#0f766e"/>
    </linearGradient>
  </defs>
  <rect width="600" height="350" fill="url(#g5)"/>
  <text x="300" y="140" fill="#fff" font-family="system-ui, sans-serif" font-weight="900" font-size="38" text-anchor="middle">JUICE &amp; SNACKS HUB</text>
  <text x="300" y="185" fill="#a7f3d0" font-family="system-ui, sans-serif" font-weight="600" font-size="20" text-anchor="middle">Fresh Fruit Coolers • Thick Shakes • Snacks</text>
  <rect x="210" y="220" width="180" height="40" rx="20" fill="rgba(0,0,0,0.4)"/>
  <text x="300" y="246" fill="#fff" font-family="system-ui, sans-serif" font-weight="bold" font-size="16" text-anchor="middle">Sports Pathway</text>
</svg>''',
}

os.makedirs("static/images/foods", exist_ok=True)

for fname, svg_code in food_svgs.items():
    with open(os.path.join("static/images/foods", fname), "w", encoding="utf-8") as f:
        f.write(svg_code)

for fname, svg_code in canteen_svgs.items():
    with open(os.path.join("static/images", fname), "w", encoding="utf-8") as f:
        f.write(svg_code)

print("Generated all food and canteen visual assets successfully!")
