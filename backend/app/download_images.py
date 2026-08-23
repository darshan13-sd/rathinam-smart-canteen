import urllib.request
import os

images_map = {
    # Food Dishes
    "static/images/foods/chicken_biryani.jpg": "https://images.unsplash.com/photo-1563379091339-03b21ab4a4f8?w=600&auto=format&fit=crop&q=80",
    "static/images/foods/thokku_biryani.jpg": "https://images.unsplash.com/photo-1589302168068-964664d93dc0?w=600&auto=format&fit=crop&q=80",
    "static/images/foods/chili_biryani.jpg": "https://images.unsplash.com/photo-1633945274405-b6c8069047b0?w=600&auto=format&fit=crop&q=80",
    "static/images/foods/veg_biryani.jpg": "https://images.unsplash.com/photo-1645177628172-a94c1f96e6db?w=600&auto=format&fit=crop&q=80",
    "static/images/foods/chicken_rice.jpg": "https://images.unsplash.com/photo-1603133872878-684f208fb84b?w=600&auto=format&fit=crop&q=80",
    "static/images/foods/chicken_noodles.jpg": "https://images.unsplash.com/photo-1585032226651-759b368d7246?w=600&auto=format&fit=crop&q=80",
    "static/images/foods/egg_rice.jpg": "https://images.unsplash.com/photo-1512058564366-18510be2db19?w=600&auto=format&fit=crop&q=80",
    "static/images/foods/egg_noodles.jpg": "https://images.unsplash.com/photo-1569718212165-3a8278d5f624?w=600&auto=format&fit=crop&q=80",
    "static/images/foods/kothu_parotta.jpg": "https://images.unsplash.com/photo-1626777552726-4a6b54c97e46?w=600&auto=format&fit=crop&q=80",
    "static/images/foods/curd_rice.jpg": "https://images.unsplash.com/photo-1546833999-b9f581a1996d?w=600&auto=format&fit=crop&q=80",
    "static/images/foods/sambar_rice.jpg": "https://images.unsplash.com/photo-1626082927389-6cd097cdc6ec?w=600&auto=format&fit=crop&q=80",
    "static/images/foods/tomato_rice.jpg": "https://images.unsplash.com/photo-1596797038530-2c107229654b?w=600&auto=format&fit=crop&q=80",
    "static/images/foods/lime_juice.jpg": "https://images.unsplash.com/photo-1513558161293-cdaf765ed2fd?w=600&auto=format&fit=crop&q=80",
    "static/images/foods/orange_juice.jpg": "https://images.unsplash.com/photo-1613478223719-2ab802602423?w=600&auto=format&fit=crop&q=80",
    "static/images/foods/watermelon_juice.jpg": "https://images.unsplash.com/photo-1589733955941-5eeaf752f6dd?w=600&auto=format&fit=crop&q=80",
    "static/images/foods/chocolate_shake.jpg": "https://images.unsplash.com/photo-1572490122747-3968b75cc699?w=600&auto=format&fit=crop&q=80",
    "static/images/foods/cold_coffee.jpg": "https://images.unsplash.com/photo-1517701550927-30cf4ba1dba5?w=600&auto=format&fit=crop&q=80",

    # Canteen Outlets
    "static/images/canteen_chatstop.jpg": "https://images.unsplash.com/photo-1555396273-367ea4eb4db5?w=800&auto=format&fit=crop&q=80",
    "static/images/canteen_zcafe.jpg": "https://images.unsplash.com/photo-1554118811-1e0d58224f24?w=800&auto=format&fit=crop&q=80",
    "static/images/canteen_seyon.jpg": "https://images.unsplash.com/photo-1567620905732-2d1ec7ab7445?w=800&auto=format&fit=crop&q=80",
    "static/images/canteen_cct.jpg": "https://images.unsplash.com/photo-1517248135467-4c7edcad34c4?w=800&auto=format&fit=crop&q=80",
    "static/images/canteen_juice.jpg": "https://images.unsplash.com/photo-1551024709-8f23befc6f87?w=800&auto=format&fit=crop&q=80",
}

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}

for local_path, url in images_map.items():
    try:
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req, timeout=10) as response:
            data = response.read()
            with open(local_path, "wb") as f:
                f.write(data)
            print(f"Downloaded: {local_path} ({len(data)} bytes)")
    except Exception as e:
        print(f"Failed to download {local_path}: {e}")

print("All realistic food and canteen photo assets updated!")
