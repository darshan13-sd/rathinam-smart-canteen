import urllib.request
import os

images_map = {
    # Authentic Food Replacements
    "static/images/foods/curd_rice.jpg": "https://images.unsplash.com/photo-1589301760014-d929f3979dbc?w=600&auto=format&fit=crop&q=80",
    "static/images/foods/sambar_rice.jpg": "https://images.unsplash.com/photo-1610192244261-3f33de3f55e4?w=600&auto=format&fit=crop&q=80",
    "static/images/foods/kothu_parotta.jpg": "https://images.unsplash.com/photo-1606471191009-63994c53433b?w=600&auto=format&fit=crop&q=80",

    # Zed Coffee Juice Menu Images
    "static/images/foods/orange_juice.jpg": "https://images.unsplash.com/photo-1613478223719-2ab802602423?w=600&auto=format&fit=crop&q=80",
    "static/images/foods/watermelon_juice.jpg": "https://images.unsplash.com/photo-1589733955941-5eeaf752f6dd?w=600&auto=format&fit=crop&q=80",
    "static/images/foods/muskmelon_juice.jpg": "https://images.unsplash.com/photo-1596461404969-9ae70f2830c1?w=600&auto=format&fit=crop&q=80",
    "static/images/foods/lime_juice.jpg": "https://images.unsplash.com/photo-1513558161293-cdaf765ed2fd?w=600&auto=format&fit=crop&q=80",
    "static/images/foods/mango_juice.jpg": "https://images.unsplash.com/photo-1546173159-315724a31696?w=600&auto=format&fit=crop&q=80",
    "static/images/foods/papaya_juice.jpg": "https://images.unsplash.com/photo-1622597467836-f3285f2131b7?w=600&auto=format&fit=crop&q=80",
    "static/images/foods/pomegranate_juice.jpg": "https://images.unsplash.com/photo-1541832676-9b763b0239ab?w=600&auto=format&fit=crop&q=80",
    "static/images/foods/apple_juice.jpg": "https://images.unsplash.com/photo-1560806887-1e4cd0b6cbd6?w=600&auto=format&fit=crop&q=80",

    # Zed Coffee Juice Canteen Photo
    "static/images/canteen_juice.jpg": "https://images.unsplash.com/photo-1501339847302-ac426a4a7cbb?w=800&auto=format&fit=crop&q=80",
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

print("Updated realistic food and Zed Coffee Juice photos successfully!")
