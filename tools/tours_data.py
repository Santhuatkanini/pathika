"""Tour content for the Pathika website.

Source of truth: the itinerary PDFs under `itineraries/`. Fixed departure dates
from those PDFs are deliberately omitted — batches are published separately.

Photos: drop your own files into `pathika/assets/images/tours/` and they are
picked up automatically on the next build (see `photo()` and `_resolve_photos()`
at the bottom of this file). Anything you have not supplied keeps the ViTour
stock image, so the site never ends up with broken images.
"""

from pathlib import Path

PHOTO_DIR = Path(__file__).resolve().parent.parent / "pathika" / "assets" / "images" / "tours"
PHOTO_EXTS = (".jpg", ".jpeg", ".png", ".webp")


def photo(name: str, fallback: str) -> str:
    for ext in PHOTO_EXTS:
        if (PHOTO_DIR / f"{name}{ext}").is_file():
            return f"./assets/images/tours/{name}{ext}"
    return fallback


CONTACT = {
    "email": "pathikabackpacking@gmail.com",
    "phone_display": "+91 87623 15962",
    "phone_intl": "918762315962",
    "instagram": "_pathika_",
    "upi": "8762315962@ybl",
}

PICKUP_POINTS = [
    "Vijaynagar Metro Station",
    "Majestic Metro Station",
    "Rajajinagar / Yeshwanthpur Metro Station",
    "Goraguntepalya (KLE Dental College)",
]

PICKUP_NOTES = [
    "Please select your preferred pickup point from the drop-down list while booking.",
    "Any change in pickup locations or timings will be updated on WhatsApp 24 hours before the start of the trip.",
    "Drop-off points are the same as the pickup points.",
]

TREK_THINGS_TO_CARRY = [
    "Small and comfortable backpack to carry your essentials during the trek.",
    "Water bottles &ndash; 2 (1 litre each).",
    "Trekking shoes, sandals.",
    "4 pairs of clothes that dry quickly.",
    "Unwrapped energy bars and dry fruits in a separate box (plastic packaging is not allowed).",
    "Personal medication, if any.",
    "Cap.",
    "Clothes to keep you warm during travel.",
    "Toiletries.",
    "Power banks.",
    "An empty lunch box to carry lunch during the trek.",
    "Rain coat, umbrella.",
    "Polythene covers to carry your wet clothes.",
    "Extra cash for meals not included in the itinerary.",
    "ID card (a photocopy or a photo on your phone will do). This is mandatory.",
    "Your favourite dance moves and your best smile, determination and zeal.",
]

DAY_TREK_THINGS_TO_CARRY = [
    "Small and comfortable backpack to carry your essentials during the trek.",
    "Water bottles &ndash; 2 (1 litre each).",
    "Trekking shoes, sandals.",
    "Unwrapped energy bars and dry fruits in a separate box (plastic packaging is not allowed).",
    "Personal medication, if any.",
    "Cap.",
    "Clothes to keep you warm during travel.",
    "Power banks.",
    "An empty lunch box to carry lunch during the trek.",
    "Extra cash for meals not included in the itinerary.",
    "ID card (a photocopy or a photo on your phone will do). This is mandatory.",
    "Your favourite dance moves and your best smile, determination and zeal.",
]

WATER_THINGS_TO_CARRY = [
    "Small and comfortable backpack to carry your essentials for the water activities.",
    "Water bottles &ndash; 2 (1 litre each).",
    "Sandals.",
    "4 pairs of clothes that dry quickly.",
    "Unwrapped energy bars and dry fruits in a separate box (plastic packaging is not allowed).",
    "Personal medication, if any.",
    "Cap.",
    "Clothes to keep you warm during travel.",
    "Toiletries.",
    "Power banks.",
    "An empty lunch box.",
    "Rain coat, umbrella.",
    "Polythene covers to carry your wet clothes.",
    "Extra cash for meals not included in the itinerary.",
    "ID card (a photocopy or a photo on your phone will do). This is mandatory.",
    "Your favourite dance moves and your best smile, determination and zeal.",
]

SCUBA_THINGS_TO_CARRY = [
    "Small and comfortable backpack to carry your essentials during the dive.",
    "Water bottles &ndash; 2 (1 litre each).",
    "Sandals.",
    "5 pairs of clothes that dry quickly.",
    "Unwrapped energy bars and dry fruits in a separate box (plastic packaging is not allowed).",
    "Personal medication, if any.",
    "Cap.",
    "Clothes to keep you warm during travel.",
    "Toiletries.",
    "Power banks.",
    "An empty lunch box.",
    "Rain coat, umbrella.",
    "Polythene covers to carry your wet clothes.",
    "Extra cash for meals not included in the itinerary.",
    "ID card (a photocopy or a photo on your phone will do). This is mandatory.",
    "Your favourite dance moves and your best smile, determination and zeal.",
]

TREK_PAYMENT_POLICY = [
    "50% of the total amount is to be paid as advance at least 35 days before the desired trek date, as confirmation of registration, along with your Name, Aadhar No., Age, Gender and Phone No. (in the same format on WhatsApp).",
    "100% of the payment is to be made at least 2 days before the trip.",
]

DAY_TREK_PAYMENT_POLICY = [
    "50% of the total amount is to be paid as advance at least 15 days before the desired trek date, as confirmation of registration, along with your Name, Aadhar No., Age, Gender and Phone No. (in the same format on WhatsApp).",
    "100% of the payment is to be made at least 2 days before the trip.",
]

BACKPACKING_PAYMENT_POLICY = [
    "50% of the package cost is to be paid as advance, as confirmation of registration, along with your booked flight / train tickets.",
    "The remaining 100% of the payment is to be completed before the balance-payment date shared for your batch.",
    "Your registration is considered confirmed only after the 50% advance payment is made.",
    "Payments can be made by UPI to " + CONTACT["upi"] + ".",
]

TREK_CANCELLATION_POLICY = [
    "Cancel before 15 days &ndash; 75% of the paid amount is refunded.",
    "Cancel before 10 days &ndash; 30% of the paid amount is refunded.",
    "Cancel between 3 and 6 days &ndash; 10% of the amount is refunded.",
    "Cancel between 0 and 3 days &ndash; no refund.",
]

TREK_CANCELLATION_NOTE = (
    "For all of the above you can transfer your ticket to someone else so that you do not lose "
    "your money. Transfer to a future date is possible only if you cancel 15 days before the trek "
    "date and not any time after that, provided slots are still available in the portal."
)

FOREST_FEE_NOTE = (
    "The specified registration fee of Rs 500 for this trek, payable to the forest department, "
    "cannot be refunded once paid."
)

BACKPACKING_CANCELLATION_POLICY = [
    "Cancel before 45 days &ndash; 90% of the paid amount is refunded.",
    "Cancel between 15 and 30 days &ndash; 50% of the amount is refunded.",
    "Cancel between 0 and 15 days &ndash; no refund.",
]

BACKPACKING_CANCELLATION_NOTE = (
    "For all of the above you can transfer your ticket to someone else so that you do not lose "
    "your money. Transfer to a future date is possible only if you cancel between 15 and 30 days "
    "before the trip date, and not later."
)

TERMS = [
    "If you want the trip to be a memorable experience, you need to co-operate with your trip captain.",
    "Do not create any nuisance on the way by throwing any kind of plastic waste.",
    "Sometimes the local authorities might restrict entry to places mentioned in the itinerary. Under such circumstances Pathika will not be responsible, and we will try to make alternate arrangements.",
    "You will be responsible for your belongings.",
    "On-time arrival at the destination might be delayed due to heavy rains, road damage, traffic, road blocks or any other unavoidable circumstances.",
    "Do not expect any luxury in the accommodation.",
    "We cannot promise hot water facilities or a campfire, as these depend on weather conditions.",
    "If you are under 18, you need to send a consent letter signed by your parents.",
    "Any kind of medical or accidental insurance is not included.",
    "Do not expect the same view as depicted in pictures on Instagram and WhatsApp. The views depend on the weather.",
    "Be careful while clicking pictures. Do not risk your life.",
    "Do not get into the sea, water streams or falls without the trip captain's permission.",
    "Please stay with the group. Do not deviate from the path or separate yourself from the group.",
    "The arrival of the jeep may be delayed due to unforeseen conditions. Please be ready to wait patiently.",
    "If there are not enough participants in a batch, the batch will be cancelled and the amount refunded.",
    "If any participant wishes to wander separately or leave the group for any reason, they must formally discontinue the trip with an official message or written letter to the organiser. From that point onward they are considered to have exited the trip, and the organisers are not responsible for their safety, well-being or any incidents that may occur.",
    "Participants join at their own risk. Pathika will not be held liable for any injuries, accidents, loss or damage during the trip.",
    "Participants are requested to respect the ethnicity, culture and environment of the place of visit, and fellow travellers.",
    "Any behaviour deemed disrespectful, harmful or illegal may result in immediate expulsion from the trip without any refund.",
    "Littering, damage, malpractice or any illegal activity that harms the ecosystem is strictly prohibited.",
    "The organisers reserve the right to modify or cancel the trip in case of unforeseen circumstances such as weather conditions, natural disasters or any other factors beyond their control. Participants will be notified of significant changes as and when they occur.",
    "Participants must be in good physical and mental health and have the necessary fitness level. It is recommended to consult a medical professional before participating, especially if you have pre-existing medical conditions.",
    "It is the participant's responsibility to inform us of any pre-existing medical conditions, allergies or physical limitations that may affect their ability to participate.",
    "Pathika reserves the right to take photographs during the trip and use them for promotional purposes.",
    "In the event you fall ill or suffer an accident during the trip, all hospital expenses, doctor fees, repatriation expenses, evacuation from road or mountain, and any other charges incurred as a direct or indirect result are your responsibility.",
    "Active, adventure travel requires a degree of personal risk. By booking with us you accept that you are aware of the personal risks, dangers and challenges that might arise, and you release Pathika from all claims arising from them.",
]

TREK_EXCLUSIONS = [
    "Meals marked as self-sponsored in the itinerary.",
    "Any kind of medical or accidental insurance.",
    "Personal expenses, water activities and anything not listed under inclusions.",
]

WHY_PATHIKA = [
    "We started with the motive: &lsquo;Just like that, we are on our way to everywhere to "
    "ENLIVE, ENRICH, INSPIRE your adventure.&rsquo;",
    "We live by it, allowing travellers their space &mdash; you are not sheep, and we are not shepherds.",
    "With over 7 years of experience in this domain, we take pride in ensuring an inclusive "
    "environment for every kind of traveller, be it solo, a group of friends, or a family "
    "travelling together.",
    "Safety and clean trails are our top priorities. With Pathika as your host you are not just a "
    "traveller, you are part of the family.",
]

CATEGORIES = [
    {
        "slug": "western-ghat-treks",
        "name": "Western Ghat Treks",
        "page": "tours-western-ghat-treks.html",
        "tagline": "Two-day weekend outings",
        "image": "./assets/images/travel-list/1.jpg",
        "blurb": "Shola forests, ridge walks and misty summits across Chikkamagaluru, "
                 "Shivamogga and the Goa border. Depart Bengaluru on Friday night, "
                 "back by Sunday night.",
    },
    {
        "slug": "coastal-treks",
        "name": "Coastal Treks",
        "page": "tours-coastal-treks.html",
        "tagline": "Beaches, backwaters and river rapids",
        "image": "./assets/images/travel-list/9.jpg",
        "blurb": "Beach-to-beach trails on the Karnataka coast, scuba diving off a coral "
                 "island, and white-water rafting on the Kali river.",
    },
    {
        "slug": "day-treks",
        "name": "Day Treks",
        "page": "tours-day-treks.html",
        "tagline": "Single-day hikes around Bengaluru",
        "image": "./assets/images/travel-list/12.jpg",
        "blurb": "Sunrise hikes on the monolithic hills and fort ranges within a few "
                 "hours of Bengaluru. Out and back in a single day.",
    },
    {
        "slug": "backpacking-tours",
        "name": "Backpacking Tours",
        "page": "tours-backpacking.html",
        "tagline": "Long-format domestic journeys",
        "image": "./assets/images/travel-list/13.jpg",
        "blurb": "Week-long, multi-city backpacking routes across India with air-conditioned "
                 "stays, local guides and all sightseeing covered.",
    },
]

# Package tiers are (amount in INR, what the tier covers).
TOURS = [
    # ---------------------------------------------------------------- Western Ghats
    {
        "slug": "kodachadri",
        "name": "Kodachadri",
        "heading": "Kodachadri",
        "tagline": "Mystic",
        "category": "western-ghat-treks",
        "coords": (13.8608, 74.8747),
        "coords_label": "13.8608&deg; N, 74.8747&deg; E",
        "duration": "2 Days / 1 Night",
        "difficulty": "Moderate to Challenging",
        "distance": "~14 km &ndash; 16 km round trip",
        "location": "Hosanagara Taluk, Shivamogga District, Karnataka",
        "image": "./assets/images/travel-list/1.jpg",
        "gallery": ["./assets/images/destination/1.jpg", "./assets/images/destination/2.jpg",
                    "./assets/images/destination/3.jpg"],
        "intro": [
            "Kodachadri is a scenic mountain peak at 1,343 metres (4,406 ft) in the Western Ghats "
            "within the Shivamogga district of Karnataka. Declared a natural heritage site, it is "
            "famous for its dense tropical rainforests, the Kodachadri Hill trekking route via "
            "Hidlumane Falls, and the historic Sarvajna Peetha shrine.",
        ],
        "facts": [
            ("District / Region", "Hosanagara Taluk, Shivamogga District, Karnataka"),
            ("Starting Village", "Kattinahole"),
            ("Base Elevation (Kattinahole)", "~644 m (~2,113 ft) above sea level"),
            ("Peak Altitude (Sarvajna Peetha)", "~1,343 m (~4,406 ft) above sea level"),
            ("Total Round-Trip Distance", "~14 km &ndash; 16 km"),
            ("Difficulty Level", "Moderate to Challenging (moderate inclines, open rolling ridge trails)"),
        ],
        "itinerary": [
            ("Day 0", "Friday", ["Start from Bengaluru by 9 pm."]),
            ("Day 1", "Saturday", [
                "Reach the homestay by 6:30 am and freshen up in the allotted dorms.",
                "Assemble for breakfast by 7:30 am.",
                "Leave for the trek by 8:15 am.",
                "Reach the base of the trek by 9:30 am and start trekking.",
                "Trek for about 2 hours to reach the falls. Enjoy the view and click pictures, then trek back to the stay and have lunch.",
                "Take a jeep ride to the IB, trek 2 km and reach the peak by 3 pm.",
                "Start down from the peak by 3:30 pm and reach the base by 5:30 pm.",
                "Reach the homestay by 6:30 pm, freshen up and assemble for tea and snacks.",
                "Dance and play games around the campfire, then have dinner and head to bed.",
            ]),
            ("Day 2", "Sunday", [
                "Wake up, get ready and assemble for breakfast.",
                "Check out of the homestay by 9 am.",
                "Visit Devagange Pond and Nagara Fort.",
                "Self-sponsored lunch, then start for Kavaledurga.",
                "Visit Kavimane and then Kavishyla for sunset.",
                "Stop for a self-sponsored dinner at Shivamogga on the way back to Bengaluru.",
                "Reach Bengaluru by 4:30 am on Monday.",
            ]),
        ],
        "inclusions": [
            "To and fro transport in a non-AC private vehicle",
            "Dormitory stay accommodation",
            "Guide fee", "Forest fee", "Jeep ride", "Permissions", "Souvenir", "Refreshments",
            "2 breakfasts", "1 lunch", "1 dinner", "Basic first aid",
            "Bonfire (if weather permits)",
        ],
        "prices": [(4299, "with all inclusions"), (3299, "exclusive of transport"),
                   (2000, "exclusive of transport, stay and meals")],
        "price_note": "Additional discount of Rs 100 per head for repeaters, or if you are a group of 5 or more.",
        "own_transport": "Those coming by own transport, please reach the homestay by 6 am on Saturday. The location will be shared on WhatsApp.",
        "forest_fee": True,
    },
    {
        "slug": "bandajje",
        "name": "Bandajje Arbi",
        "heading": "Bandajje Arbi",
        "tagline": "Enchanting",
        "category": "western-ghat-treks",
        "coords": (13.1057, 75.4148),
        "coords_label": "13&deg;6'20.55&quot; N, 75&deg;24'53.44&quot; E",
        "duration": "2 Days / 1 Night",
        "difficulty": "Moderate to Challenging",
        "distance": "~14 km &ndash; 16 km round trip",
        "location": "Mudigere Taluk, Chikkamagaluru District, Karnataka",
        "image": "./assets/images/travel-list/2.jpg",
        "gallery": ["./assets/images/destination/des1.jpg", "./assets/images/destination/des2.jpg",
                    "./assets/images/destination/des3.jpg"],
        "intro": [
            "The Bandaje Arbi (Falls) trek via Sunkasale is one of the most scenic trail "
            "combinations in the Charmadi Ghat region of Karnataka's Western Ghats. Approaching "
            "the trail from Sunkasale lets trekkers experience the famous ridge-walk route "
            "starting from Rani Jhari View Point and passing through the ancient Ballalarayana "
            "Durga Fort.",
        ],
        "facts": [
            ("District / Region", "Mudigere Taluk, Chikkamagaluru District, Karnataka"),
            ("Starting Village", "Sunkasale (physical trail base at Durgadahalli / Rani Jhari parking area, ~8&ndash;10 km past Sunkasale)"),
            ("End Point / Waterfall", "Border between Chikkamagaluru and Dakshina Kannada districts"),
            ("Base Elevation (Sunkasale / Durgadahalli)", "~950 m (~3,117 ft) above sea level"),
            ("Peak Altitude (Ballalarayana Durga Fort)", "~1,500 m (~4,921 ft) above sea level"),
            ("Waterfall Edge Elevation (Bandaje Arbi)", "~1,020 m (~3,346 ft) above sea level"),
            ("Total Round-Trip Distance", "~14 km &ndash; 16 km"),
            ("Difficulty Level", "Moderate to Challenging (moderate inclines, open rolling ridge trails, followed by a steep descent to the waterfall's edge)"),
        ],
        "itinerary": [
            ("Day 0", "Friday", ["Start from Bengaluru by 9 pm."]),
            ("Day 1", "Saturday", [
                "Reach the homestay by 6:30 am and freshen up in the allotted dorms.",
                "Assemble for breakfast by 7:30 am.",
                "Leave for the trek by 8:15 am.",
                "Reach the base of the trek by jeep by 9 am and start the trek after ID verification and bag checks.",
                "Trek for about 3 hours to reach the peak. Enjoy the view, click pictures and have lunch.",
                "Start down from the peak by 1:30 pm and reach the base by 5 pm.",
                "Reach the homestay by 6 pm. Hot water will be provided for bathing.",
                "Freshen up and assemble for tea and snacks.",
                "Dance and play games around the campfire, and share your travel diaries.",
                "Dinner will be served at 9 pm, after which you can head to bed.",
            ]),
            ("Day 2", "Sunday", [
                "Wake up to the sounds of nature, freshen up and assemble for breakfast.",
                "Check out of the homestay by 10:30 am.",
                "Visit Kodige Falls and Kelaguru Tea Estate en route to Bengaluru.",
                "Visit Purna Chandra Tejasvi Pratishtana if time permits.",
                "Visit Belur Chennakeshava Temple.",
                "Stop for a self-sponsored lunch at Hassan on the way back.",
                "Stop for a self-sponsored tea or dinner break if running late due to traffic.",
                "Reach Bengaluru by 10:30 pm.",
            ]),
        ],
        "inclusions": [
            "To and fro transport in a non-AC private vehicle",
            "Dormitory stay accommodation",
            "Guide fee", "Forest fee", "Jeep ride", "Permissions", "Souvenir", "Refreshments",
            "2 breakfasts", "1 lunch", "1 dinner (veg / non-veg)", "Basic first aid",
            "Bonfire (if weather permits)",
        ],
        "prices": [(4299, "with all inclusions"), (3299, "exclusive of transport"),
                   (2000, "exclusive of transport, stay and meals")],
        "price_note": "Additional discount of Rs 100 per head for repeaters, or if you are a group of 5 or more.",
        "own_transport": "Those coming by own transport, please reach the homestay by 6 am on Saturday. The location will be shared on WhatsApp.",
        "forest_fee": True,
    },
    {
        "slug": "kudremukha",
        "name": "Kudremukha",
        "heading": "Kudremukha",
        "tagline": "Exhilarating",
        "category": "western-ghat-treks",
        "coords": (13.1294, 75.2683),
        "coords_label": "13.1294&deg; N, 75.2683&deg; E",
        "duration": "2 Days / 1 Night",
        "difficulty": "Moderate to Challenging",
        "distance": "~20 km &ndash; 22 km round trip",
        "location": "Mullodi, Mudigere Taluk, Chikkamagaluru District, Karnataka",
        "image": "./assets/images/travel-list/3.jpg",
        "gallery": ["./assets/images/tour/tour5.1.jpg", "./assets/images/tour/tour5.2.jpg",
                    "./assets/images/tour/tour5.3.jpg"],
        "intro": [
            "Nestled within Karnataka's Western Ghats, the Kudremukha trek is a scenic "
            "22-kilometre round trip through lush shola forests, babbling streams and rolling "
            "emerald hills. The trail culminates at a horse-face-shaped summit rising 1,894 metres "
            "above sea level, offering panoramic ridge views and continuous mountain winds.",
            "As part of a protected national park it stands out for its pristine ecosystem, "
            "requiring forest department permits and strict single-day timing limits.",
        ],
        "facts": [
            ("District / Region", "Mullodi, Mudigere Taluk, Chikkamagaluru District, Karnataka"),
            ("Starting Village", "Mullodi"),
            ("Base Elevation (Mullodi)", "~950 m (~3,110 ft) above sea level"),
            ("Peak Altitude", "~1,894 m (~6,214 ft) above sea level"),
            ("Total Round-Trip Distance", "~20 km &ndash; 22 km"),
            ("Difficulty Level", "Moderate to Challenging"),
        ],
        "itinerary": [
            ("Day 0", "Friday", ["Start from Bengaluru by 9 pm."]),
            ("Day 1", "Saturday", [
                "Reach the homestay by 6:30 am and freshen up in the allotted dorms.",
                "Assemble for breakfast by 7:30 am.",
                "Leave for the trek by 8:15 am.",
                "Trek for about 3 hours to reach the peak. Enjoy the view and click pictures.",
                "Start down from the peak by 1:30 pm and reach the base by 4:30 pm.",
                "Visit a secret waterfall before heading to the homestay.",
                "Reach the homestay by 6:30 pm, freshen up and assemble for tea and snacks.",
                "Dance and play games around the campfire, then have dinner and head to bed.",
            ]),
            ("Day 2", "Sunday", [
                "Wake up, get ready and assemble for breakfast.",
                "Check out of the homestay by 9 am.",
                "Visit Samse Tea Estate and Kalasa Hanging Bridge en route to Bengaluru.",
                "Visit Purna Chandra Tejasvi Pratishtana if time permits.",
                "Stop for a self-sponsored lunch on the way back.",
                "Stop for a self-sponsored tea or dinner break if running late due to traffic.",
                "Reach Bengaluru by 10:30 pm.",
            ]),
        ],
        "inclusions": [
            "To and fro transport in a non-AC private vehicle",
            "Dormitory stay accommodation",
            "Guide fee", "Forest fee", "Permissions", "Souvenir", "Refreshments",
            "2 breakfasts", "1 lunch", "1 dinner (veg / non-veg)", "Basic first aid",
            "Bonfire (if weather permits)",
        ],
        "prices": [(4349, "with all inclusions"), (3499, "exclusive of transport"),
                   (2100, "exclusive of transport, stay and meals")],
        "price_note": "Additional discount of Rs 100 per head for repeaters, or if you are a group of 5 or more.",
        "own_transport": "Those coming by own transport, please reach the homestay by 6 am on Saturday. The location will be shared on WhatsApp.",
        "forest_fee": True,
    },
    {
        "slug": "kurinjal",
        "name": "Kurinjal",
        "heading": "Kurinjal Peak",
        "tagline": "Canopied",
        "category": "western-ghat-treks",
        "coords": (13.2356, 75.2678),
        "coords_label": "13.2356&deg; N, 75.2678&deg; E",
        "duration": "2 Days / 1 Night",
        "difficulty": "Easy to Moderate",
        "distance": "~14 km &ndash; 16 km round trip",
        "location": "Kudremukha, Mudigere Taluk, Chikkamagaluru District, Karnataka",
        "image": "./assets/images/travel-list/4.jpg",
        "gallery": ["./assets/images/tour/tour5.4.jpg", "./assets/images/tour/tour5.5.jpg",
                    "./assets/images/tour/tour5.6.jpg"],
        "intro": [
            "Located deep within the Kudremukh National Park in Karnataka, the Kurinjal Peak trek "
            "is a serene trail through pristine shola forests and rolling grasslands. Ascending to "
            "an elevation of 1,159 metres, this moderate climb guides hikers past moss-covered "
            "trees, hidden streams and an abandoned radio tower structure near the summit.",
            "The trail provides a quieter alternative to the more crowded Kudremukh Peak while "
            "offering equally breathtaking panoramic views of the mist-laden Western Ghats. Its "
            "dense canopy keeps much of the path shaded, creating a cool, immersive escape for "
            "both novice and seasoned trekkers.",
        ],
        "facts": [
            ("District / Region", "Kudremukha, Mudigere Taluk, Chikkamagaluru District, Karnataka"),
            ("Base Elevation (Kudremukha)", "~815 m (~2,674 ft) above sea level"),
            ("Peak Altitude", "~1,159 m (~3,802 ft) above sea level"),
            ("Total Round-Trip Distance", "~14 km &ndash; 16 km"),
            ("Difficulty Level", "Easy to Moderate"),
        ],
        "itinerary": [
            ("Day 0", "Friday", ["Start from Bengaluru by 9 pm."]),
            ("Day 1", "Saturday", [
                "Reach the homestay by 6:30 am and freshen up in the allotted dorms.",
                "Assemble for breakfast by 7:30 am.",
                "Leave for the trek by 8:15 am.",
                "Trek for about 3 hours to reach the peak. Enjoy the view and click pictures.",
                "Start down from the peak by 1:30 pm and reach the base by 4:30 pm.",
                "Visit a secret waterfall before heading to the homestay.",
                "Reach the homestay by 6:30 pm, freshen up and assemble for tea and snacks.",
                "Dance and play games around the campfire, then have dinner and head to bed.",
            ]),
            ("Day 2", "Sunday", [
                "Wake up, get ready and assemble for breakfast.",
                "Check out of the homestay by 9 am.",
                "Visit Samse Tea Estate and Kalasa Hanging Bridge en route to Bengaluru.",
                "Visit Purna Chandra Tejasvi Pratishtana if time permits.",
                "Stop for a self-sponsored lunch on the way back.",
                "Stop for a self-sponsored tea or dinner break if running late due to traffic.",
                "Reach Bengaluru by 10:30 pm.",
            ]),
        ],
        "inclusions": [
            "To and fro transport in a non-AC private vehicle",
            "Dormitory stay accommodation",
            "Guide fee", "Forest fee", "Permissions", "Souvenir", "Refreshments",
            "2 breakfasts", "1 lunch", "1 dinner (veg / non-veg)", "Basic first aid",
            "Bonfire (if weather permits)",
        ],
        "prices": [(4299, "with all inclusions"), (3299, "exclusive of transport"),
                   (2000, "exclusive of transport, stay and meals")],
        "price_note": "Additional discount of Rs 100 per head for repeaters, or if you are a group of 5 or more.",
        "own_transport": "Those coming by own transport, please reach the homestay by 6 am on Saturday. The location will be shared on WhatsApp.",
        "forest_fee": True,
    },
    {
        "slug": "gangadikal",
        "name": "Gangadikal",
        "heading": "Gangadikal",
        "tagline": "Pristine",
        "category": "western-ghat-treks",
        "coords": (13.2488, 75.1835),
        "coords_label": "13.2488&deg; N, 75.1835&deg; E",
        "duration": "2 Days / 1 Night",
        "difficulty": "Moderate to Challenging",
        "distance": "~8 km &ndash; 10 km round trip",
        "location": "Mudigere Taluk, Chikkamagaluru District, Karnataka",
        "image": "./assets/images/travel-list/5.jpg",
        "gallery": ["./assets/images/tour/tour5.7.jpg", "./assets/images/tour/tour5.8.jpg",
                    "./assets/images/tour/tour5.9.jpg"],
        "intro": [
            "The Gangadikal trek is a scenic and less-crowded trail in the Kudremukh ranges of the "
            "Western Ghats within Chikkamagaluru, Karnataka. Rising to an altitude of about 1,465 "
            "metres (4,800 ft), the 8 to 10 km round-trip route features lush shola grasslands, "
            "ridge walks and panoramic views of the Lakya Dam backwaters.",
        ],
        "facts": [
            ("District / Region", "Mudigere Taluk, Chikkamagaluru District, Karnataka"),
            ("Starting Village", "Kudremukha (physical trail base ~20 km past Kudremukha)"),
            ("Base Elevation (Kudremukha)", "~815 m (~2,674 ft) above sea level"),
            ("Peak Altitude", "~1,465 m (~4,806 ft) above sea level"),
            ("Total Round-Trip Distance", "~8 km &ndash; 10 km"),
            ("Difficulty Level", "Moderate to Challenging"),
        ],
        "itinerary": [
            ("Day 0", "Friday", ["Start from Bengaluru by 9 pm."]),
            ("Day 1", "Saturday", [
                "Reach the homestay by 6:30 am and freshen up in the allotted dorms.",
                "Assemble for breakfast by 7:30 am.",
                "Leave for the trek by 8:15 am.",
                "Reach the base of the trek by jeep by 9:30 am and start the trek after ID verification and bag checks.",
                "Trek for about 3 hours to reach the peak. Enjoy the view, click pictures and have lunch.",
                "Start down from the peak by 1:30 pm and reach the base by 4:30 pm.",
                "Visit a secret waterfall before heading to the homestay.",
                "Reach the homestay by 6:30 pm. Hot water will be provided for bathing.",
                "Freshen up and assemble for tea and snacks.",
                "Dance and play games around the campfire, and share your travel diaries.",
                "Dinner will be served at 9 pm, after which you can head to bed.",
            ]),
            ("Day 2", "Sunday", [
                "Wake up early and hike to Bhaamikonda View Point, returning to the homestay by 9:30 am.",
                "Freshen up, get ready and assemble for breakfast.",
                "Check out of the homestay by 10:30 am.",
                "Visit Samse Tea Estate and Kalasa Hanging Bridge en route to Bengaluru.",
                "Visit Purna Chandra Tejasvi Pratishtana if time permits.",
                "Stop for a self-sponsored lunch on the way back.",
                "Visit Belur Chennakeshava Temple.",
                "Stop for a self-sponsored tea or dinner break if running late due to traffic.",
                "Reach Bengaluru by 10:30 pm.",
            ]),
        ],
        "inclusions": [
            "To and fro transport in a non-AC private vehicle",
            "Dormitory stay accommodation",
            "Guide fee", "Forest fee", "Permissions", "Souvenir", "Refreshments",
            "2 breakfasts", "1 lunch", "1 dinner (veg / non-veg)", "Basic first aid",
            "Bonfire (if weather permits)",
        ],
        "prices": [(4299, "with all inclusions"), (3299, "exclusive of transport"),
                   (2000, "exclusive of transport, stay and meals")],
        "price_note": "Additional discount of Rs 100 per head for repeaters, or if you are a group of 5 or more.",
        "own_transport": "Those coming by own transport, please reach the homestay by 6 am on Saturday. The location will be shared on WhatsApp.",
        "forest_fee": True,
    },
    {
        "slug": "merthi-gudda",
        "name": "Merthi Gudda",
        "heading": "Merthi Gudda",
        "tagline": "Misty",
        "category": "western-ghat-treks",
        "coords": (13.2928, 75.3747),
        "coords_label": "13.2928&deg; N, 75.3747&deg; E",
        "duration": "2 Days / 1 Night",
        "difficulty": "Easy to Moderate",
        "distance": "~8 km &ndash; 10 km round trip",
        "location": "Kalasa / Koppa Taluk, Chikkamagaluru District, Karnataka",
        "image": "./assets/images/travel-list/6.jpg",
        "gallery": ["./assets/images/tour/tour1.jpg", "./assets/images/tour/tour2.jpg",
                    "./assets/images/tour/tour3.jpg"],
        "intro": [
            "Merthi Gudda is a scenic, offbeat peak nestled in the Kudremukh region of the Western "
            "Ghats near Horanadu, Karnataka. Standing at roughly 5,500 feet, this 8 to 10 km "
            "round-trip trek features rolling green grasslands, open ridge walks and panoramic "
            "valley views.",
        ],
        "facts": [
            ("District / Region", "Kalasa / Koppa Taluk, Chikkamagaluru District, Karnataka"),
            ("Starting Village", "Horanadu (physical trail base ~8&ndash;10 km past Horanadu)"),
            ("Base Elevation", "~831 m (~2,726 ft) above sea level"),
            ("Peak Altitude", "~1,676 m (~5,499 ft) above sea level"),
            ("Total Round-Trip Distance", "~8 km &ndash; 10 km"),
            ("Difficulty Level", "Easy to Moderate"),
        ],
        "itinerary": [
            ("Day 0", "Friday", ["Start from Bengaluru by 9 pm."]),
            ("Day 1", "Saturday", [
                "Reach the homestay by 6:30 am and freshen up in the allotted dorms.",
                "Assemble for breakfast by 7:30 am.",
                "Leave for the trek by 8:15 am.",
                "Reach the base of the trek by 9:30 am and start the trek.",
                "Trek for about 3 hours to reach the peak. Enjoy the view and click pictures.",
                "Start down from the peak by 1:30 pm and reach the base by 3:30 pm.",
                "Reach the homestay by 6:30 pm, freshen up and assemble for tea and snacks.",
                "Dance and play games around the campfire, then have dinner and head to bed.",
            ]),
            ("Day 2", "Sunday", [
                "Wake up, get ready and assemble for breakfast.",
                "Check out of the homestay by 9 am.",
                "Visit Horanadu Temple, Kalasa Temple and Kalasa Hanging Bridge en route to Bengaluru.",
                "Visit Purna Chandra Tejasvi Pratishtana if time permits.",
                "Stop for a self-sponsored lunch on the way back.",
                "Visit Belur Chennakeshava Temple.",
                "Reach Bengaluru by 9:30 pm.",
            ]),
        ],
        "inclusions": [
            "To and fro transport in a non-AC private vehicle",
            "Dormitory stay accommodation",
            "Guide fee", "Forest fee", "Permissions", "Souvenir", "Refreshments",
            "2 breakfasts", "1 lunch", "1 dinner (veg / non-veg)", "Basic first aid",
            "Bonfire (if weather permits)",
        ],
        "prices": [(4299, "with all inclusions"), (3299, "exclusive of transport"),
                   (2000, "exclusive of transport, stay and meals")],
        "price_note": "Additional discount of Rs 100 per head for repeaters, or if you are a group of 5 or more.",
        "own_transport": "Those coming by own transport, please reach the homestay by 6 am on Saturday. The location will be shared on WhatsApp.",
        "forest_fee": True,
    },
    {
        "slug": "karushi-gudda",
        "name": "Karushi Gudda",
        "heading": "Karushi Gudda",
        "tagline": "Untouched",
        "category": "western-ghat-treks",
        "coords": (13.2721, 75.3422),
        "coords_label": "13.2721&deg; N, 75.3422&deg; E",
        "duration": "2 Days / 1 Night",
        "difficulty": "Easy to Moderate",
        "distance": "~8 km &ndash; 10 km round trip",
        "location": "Kalasa Taluk, Chikkamagaluru District, Karnataka",
        "image": "./assets/images/travel-list/7.jpg",
        "gallery": ["./assets/images/tour/tour4.jpg", "./assets/images/tour/tour5.jpg",
                    "./assets/images/tour/tour6.jpg"],
        "intro": [
            "The Karushi Gudda trek is a newly opened, scenic trail in the Western Ghats near "
            "Horanadu and Kalasa in Karnataka's Chikkamagaluru district. Spanning a moderate "
            "round trip, the hike features lush forests and rolling grasslands opening out to "
            "panoramic 360-degree views from the summit.",
        ],
        "facts": [
            ("District / Region", "Kalasa Taluk, Chikkamagaluru District, Karnataka"),
            ("Starting Village", "Horanadu (physical trail base ~8&ndash;10 km past Horanadu)"),
            ("Base Elevation", "~831 m (~2,726 ft) above sea level"),
            ("Peak Altitude", "~1,346 m (~4,450 ft) above sea level"),
            ("Total Round-Trip Distance", "~8 km &ndash; 10 km"),
            ("Difficulty Level", "Easy to Moderate"),
        ],
        "itinerary": [
            ("Day 0", "Friday", ["Start from Bengaluru by 9 pm."]),
            ("Day 1", "Saturday", [
                "Reach the homestay by 6:30 am and freshen up in the allotted dorms.",
                "Assemble for breakfast by 7:30 am.",
                "Leave for the trek by 8:15 am.",
                "Reach the base of the trek by 9:30 am and start the trek.",
                "Trek for about 3 hours to reach the peak. Enjoy the view and click pictures.",
                "Start down from the peak by 1:30 pm and reach the base by 3:30 pm.",
                "Reach the homestay by 6:30 pm, freshen up and assemble for tea and snacks.",
                "Dance and play games around the campfire, then have dinner and head to bed.",
            ]),
            ("Day 2", "Sunday", [
                "Wake up, get ready and assemble for breakfast.",
                "Check out of the homestay by 9 am.",
                "Visit Horanadu Temple, Kalasa Temple and Kalasa Hanging Bridge en route to Bengaluru.",
                "Visit Purna Chandra Tejasvi Pratishtana if time permits.",
                "Stop for a self-sponsored lunch on the way back.",
                "Visit Belur Chennakeshava Temple.",
                "Reach Bengaluru by 9:30 pm.",
            ]),
        ],
        "inclusions": [
            "To and fro transport in a non-AC private vehicle",
            "Dormitory stay accommodation",
            "Guide fee", "Forest fee", "Permissions", "Souvenir", "Refreshments",
            "2 breakfasts", "1 lunch", "1 dinner (veg / non-veg)", "Basic first aid",
            "Bonfire (if weather permits)",
        ],
        "prices": [(4299, "with all inclusions"), (3299, "exclusive of transport"),
                   (2000, "exclusive of transport, stay and meals")],
        "price_note": "Additional discount of Rs 100 per head for repeaters, or if you are a group of 5 or more.",
        "own_transport": "Those coming by own transport, please reach the homestay by 6 am on Saturday. The location will be shared on WhatsApp.",
        "forest_fee": True,
    },
    {
        "slug": "dudhsagar",
        "name": "Dudhsagar",
        "heading": "Dudhsagar Falls",
        "tagline": "Sea of Milk",
        "category": "western-ghat-treks",
        "coords": (15.3144, 74.3143),
        "coords_label": "15.3144&deg; N, 74.3143&deg; E",
        "duration": "3 Days / 2 Nights",
        "difficulty": "Easy to Moderate",
        "distance": "~14 km &ndash; 16 km round trip",
        "location": "Mandovi River, Goa &ndash; Karnataka border",
        "image": "./assets/images/travel-list/8.jpg",
        "gallery": ["./assets/images/tour/tour7.jpg", "./assets/images/tour/tour8.jpg",
                    "./assets/images/tour/tourh5.jpg"],
        "intro": [
            "Dudhsagar Falls is a spectacular four-tiered waterfall on the Mandovi River along the "
            "border of Goa and Karnataka. Translating to &lsquo;Sea of Milk&rsquo;, its name stems "
            "from the roaring white foam created as the water plunges down nearly 310 metres "
            "(1,017 ft).",
            "Surrounded by the lush green canopy of the Bhagwan Mahaveer Sanctuary in the Western "
            "Ghats, it is one of India's tallest and most iconic natural wonders. A railway bridge "
            "spans directly across the middle of the cascades, creating a world-famous view as "
            "trains pass right through the mist of the waterfalls.",
        ],
        "facts": [
            ("Region", "Bhagwan Mahaveer Sanctuary, Goa &ndash; Karnataka border"),
            ("River", "Mandovi"),
            ("Waterfall Height", "~310 m (~1,017 ft), four tiers"),
            ("Trail Start", "Kulem"),
            ("Total Round-Trip Distance", "~14 km &ndash; 16 km"),
            ("Difficulty Level", "Easy to Moderate"),
        ],
        "itinerary": [
            ("Day 0", "Friday", ["Start from Bengaluru by 7 pm."]),
            ("Day 1", "Saturday", [
                "Reach Kulem by 8 am and freshen up in the allotted dorms.",
                "Assemble for breakfast by 8:30 am.",
                "Leave for the trek by 9:15 am.",
                "Trek for about 3 hours to reach the waterfalls. Enjoy the view and click pictures.",
                "Start back from the falls by 1:30 pm and reach the base by 4:30 pm.",
                "Freshen up and assemble for evening refreshments.",
                "Reach the homestay at Dandeli by 8:30 pm, freshen up and assemble for dinner.",
                "Dance and play games around the campfire, then have dinner and head to bed.",
            ]),
            ("Day 2", "Sunday", [
                "Wake up, get ready and assemble for breakfast.",
                "Check out of the homestay by 9 am.",
                "Visit Magod Waterfalls.",
                "Stop for a self-sponsored lunch on the way back.",
                "Visit Sirsi Temple and Banavasi Temple.",
                "Stop for a self-sponsored tea or dinner break, then start for Bengaluru.",
            ]),
            ("Day 3", "Monday", ["Reach Bengaluru by 5 am."]),
        ],
        "inclusions": [
            "To and fro transport in a non-AC private vehicle",
            "Dormitory stay accommodation",
            "Guide fee", "Forest fee", "Permissions", "Souvenir", "Refreshments",
            "2 breakfasts", "1 lunch", "1 dinner (veg / non-veg)", "Basic first aid",
            "Bonfire (if weather permits)",
        ],
        "prices": [(5599, "with all inclusions"), (3999, "exclusive of transport"),
                   (2000, "exclusive of transport, stay and meals")],
        "price_note": "Additional discount of Rs 100 per head for repeaters, or if you are a group of 5 or more.",
        "own_transport": "Those coming by own transport, please reach the homestay by 6 am on Saturday. The location will be shared on WhatsApp.",
        "forest_fee": True,
    },
    # ------------------------------------------------------------------- Coastal
    {
        "slug": "gokarna",
        "name": "Gokarna",
        "heading": "Gokarna Beach Trek",
        "tagline": "Bohemian",
        "category": "coastal-treks",
        "coords": (14.5479, 74.3188),
        "coords_label": "14.5479&deg; N, 74.3188&deg; E",
        "duration": "3 Days / 2 Nights",
        "difficulty": "Easy to Moderate",
        "distance": "Belekan &rarr; Paradise &rarr; Half Moon &rarr; Om &rarr; Kudle",
        "location": "Gokarna, Uttara Kannada District, Karnataka",
        "image": "./assets/images/travel-list/9.jpg",
        "gallery": ["./assets/images/gallery/gallery.jpg", "./assets/images/gallery/gallery2.jpg",
                    "./assets/images/gallery/gallery3.jpg"],
        "intro": [
            "The Gokarna beach trek is a dream for travellers, with miles of golden sand beaches, "
            "jagged cliffs, outstanding sunset views, undiscovered coves and quaint temples. The "
            "long sandy stretches of Om Beach and Kudle Beach are a delight for every beach lover.",
            "We arrive at Gokarna main beach at the golden hour to soak in the beauty of the "
            "Arabian Sea and its seemingly infinite horizon. After freshening up we reach Belekan "
            "Beach, from where the trek begins. The route goes through Paradise Beach, also known "
            "as Full Moon Beach &mdash; reachable only by trekking or by boat, which makes it a "
            "trekker's paradise.",
            "Next comes Half Moon Beach, perfect whether you love standing at the edge of a cliff "
            "or chilling on a hammock. As we continue, the sun slowly reaches for the horizon. No "
            "matter how many beautiful sunsets you have witnessed, Om Beach has one truly worth "
            "craving. We finally end the trek at Kudle Beach.",
        ],
        "facts": [
            ("District / Region", "Gokarna, Uttara Kannada District, Karnataka"),
            ("Trek Start", "Belekan Beach"),
            ("Beaches Covered", "Paradise (Full Moon), Half Moon, Om and Kudle"),
            ("Terrain", "Sandy stretches, cliff paths and coastal forest"),
            ("Difficulty Level", "Easy to Moderate"),
        ],
        "itinerary": [
            ("Day 0", "Friday", ["Start from Bengaluru by 9 pm."]),
            ("Day 1", "Saturday", [
                "Reach the homestay by 7:30 am and freshen up in the allotted dorms.",
                "Assemble for breakfast by 8:30 am.",
                "Leave for the trek by 9:15 am.",
                "Reach the base of the trek at Belekan Beach by 10 am and start the trek.",
                "Trek for about an hour to reach Paradise Beach. Soak in the beauty of this serene beach and indulge in water activities at your own cost.",
                "Start for Half Moon Beach, a half-hour trek through cliffs and forests, and stop for lunch.",
                "The stretch from Half Moon to Om Beach is one of the best you will experience on the trek.",
                "Spend time at Om Beach hopping around the fancy beachside cafes and clicking pictures on the cliffs, then start for Kudle Beach.",
                "Enjoy the sunset from Kudle Beach, get into the sea and embrace the evening waves.",
                "Freshen up and assemble for dinner.",
                "Spend the later part of the evening along the beachside sharing travel diaries and playing games, then head to bed.",
            ]),
            ("Day 2", "Sunday", [
                "Wake up early, have breakfast and check out.",
                "Visit Gokarna Mahabaleshwara Temple and Koti Theertha.",
                "Visit Honnavara, experience a boat ride at Mavinkurva Islands, visit the Kandla forests and then the magnificent Jog Falls in the evening.",
                "Stop for self-sponsored lunch and dinner en route to Bengaluru.",
            ]),
            ("Day 3", "Monday", ["Reach Bengaluru by 5 am."]),
        ],
        "inclusions": [
            "To and fro transport in a non-AC private vehicle",
            "Dormitory stay accommodation",
            "Guide fee", "Forest fee", "Permissions", "Souvenir", "Refreshments",
            "2 breakfasts", "1 lunch", "1 dinner (veg / non-veg)", "Basic first aid",
            "Bonfire (if weather permits)",
        ],
        "prices": [(4399, "with all inclusions"), (3299, "exclusive of transport"),
                   (2000, "exclusive of transport, stay and meals")],
        "price_note": "Additional discount of Rs 100 per head for repeaters, or if you are a group of 5 or more.",
        "own_transport": "Those coming by own transport, please reach the homestay by 6 am on Saturday. The location will be shared on WhatsApp.",
        "forest_fee": True,
    },
    {
        "slug": "netrani",
        "name": "Netrani Island",
        "heading": "Netrani Island",
        "tagline": "Heart Shaped",
        "category": "coastal-treks",
        "coords": (14.0165, 74.3259),
        "coords_label": "14.0165&deg; N, 74.3259&deg; E",
        "duration": "3 Days / 2 Nights",
        "difficulty": "Easy (scuba diving &mdash; no experience required)",
        "distance": "~19 km (10 nautical miles) offshore from Murudeshwar",
        "location": "Arabian Sea, off Murudeshwar, Bhatkal Taluk, Karnataka",
        "image": "./assets/images/travel-list/10.jpg",
        "gallery": ["./assets/images/gallery/gallery4.jpg", "./assets/images/gallery/gallery5.jpg",
                    "./assets/images/gallery/gallery6.jpg"],
        "intro": [
            "Netrani is a small island in the Arabian Sea off the coast of Karnataka, situated "
            "approximately 10 nautical miles (19 km) from the temple town of Murudeshwar in "
            "Bhatkal Taluk.",
            "Netrani Island has several dive sites with visibility ranging from 15 to 20 metres "
            "(49.2 to 65.6 ft). There are healthy coral reefs with a huge variety of reef fish "
            "around the island. After initial resistance from local fishermen, diving is now "
            "actively promoted by Karnataka Tourism.",
            "Netrani is a coral island whose reefs teem with many varieties of butterfly fish, "
            "trigger fish, parrot fish, eel and shrimp.",
        ],
        "facts": [
            ("Region", "Arabian Sea, off Murudeshwar, Bhatkal Taluk, Karnataka"),
            ("Distance Offshore", "~10 nautical miles (~19 km) from Murudeshwar"),
            ("Dive Visibility", "15 &ndash; 20 m (49.2 &ndash; 65.6 ft)"),
            ("Marine Life", "Butterfly fish, trigger fish, parrot fish, eel and shrimp"),
            ("Activity", "Scuba diving, snorkelling and swimming"),
        ],
        "itinerary": [
            ("Day 0", "Friday", ["Start from Bengaluru by 9 pm."]),
            ("Day 1", "Saturday", [
                "Reach Murudeshwar by 8 am and freshen up in the allotted rooms.",
                "Report at the hotel lobby by 9:30 am.",
                "Walk to the dive club office and complete the registration. The briefing will be done on the boat.",
                "Enjoy the 1-hour boat ride in the Arabian Sea &mdash; if lucky, spot dolphins.",
                "Wait for your turn for the dive, and meanwhile spend time snorkelling and swimming in the sea.",
                "Finish the dive and reach Murudeshwar by 5:30 pm.",
                "Head back to the hotel for lunch, freshen up and visit the temple in the evening.",
                "Stay at Murudeshwar after dinner.",
            ]),
            ("Day 2", "Sunday", [
                "Have breakfast and check out by 9 am.",
                "Drive to Honnavara and take a boat ride in the backwaters of the Sharavathi.",
                "Take a walk along the mangrove forests.",
                "Self-sponsored lunch at Honnavara.",
                "Visit Bangara Kusuma Waterfalls en route to Jog Falls.",
                "Head to Jog Falls, witness the sunset and then drive to Shimoga.",
                "Stop for dinner and then start for Bengaluru.",
            ]),
            ("Day 3", "Monday", ["Reach Bengaluru by 6 am."]),
        ],
        "inclusions": [
            "To and fro transport in a non-AC private vehicle",
            "Dormitory stay accommodation",
            "Guide fee", "Forest fee", "Permissions", "Souvenir", "Refreshments",
            "2 breakfasts", "1 lunch", "1 dinner (veg / non-veg)", "Basic first aid",
            "Bonfire (if weather permits)",
        ],
        "prices": [(7599, "with all inclusions"), (5899, "exclusive of transport"),
                   (6299, "exclusive of scuba")],
        "price_note": "Additional discount of Rs 100 per head for repeaters, or if you are a group of 5 or more. "
                      "The higher prices are due to a hike in the scuba package price and in diesel prices.",
        "own_transport": "Those coming by own transport, please reach the stay by 8 am on Saturday. The location will be shared on WhatsApp.",
        "forest_fee": False,
        "things_to_carry": SCUBA_THINGS_TO_CARRY,
    },
    {
        "slug": "dandeli",
        "name": "Dandeli",
        "heading": "Dandeli",
        "tagline": "Untamed",
        "category": "coastal-treks",
        "coords": (15.2429, 74.6247),
        "coords_label": "15.2429&deg; N, 74.6247&deg; E",
        "duration": "3 Days / 2 Nights",
        "difficulty": "Easy (adventure water sports)",
        "distance": "Kali River, ~473 m altitude",
        "location": "Uttara Kannada District, Karnataka",
        "image": "./assets/images/travel-list/11.jpg",
        "gallery": ["./assets/images/gallery/gallery7.jpg", "./assets/images/gallery/gallery8.jpg",
                    "./assets/images/gallery/gallery9.jpg"],
        "intro": [
            "Dandeli is a picturesque town in the Uttara Kannada district of Karnataka, renowned "
            "for its dense Western Ghats rainforests, rich biodiversity and high-energy river "
            "sports. Situated along the banks of the Kali River, it serves as a major eco-tourism "
            "hub and adventure travel destination in South India.",
        ],
        "facts": [
            ("District / Region", "Uttara Kannada District, Karnataka"),
            ("Canopied Wilderness", "Evergreen forests, bamboo thickets and teak plantations of the Western Ghats"),
            ("The Kali River", "The lifeline of the region, flowing through rocky gorges and creating rapids suited for water sports"),
            ("Elevated Terrain", "~473 m altitude, with a tropical forest climate and misty mornings during monsoon and winter"),
            ("River Adventures", "White-water rafting, jacuzzis in natural rapids, kayaking and coracle rides on the Kali River"),
            ("Forest Exploration", "Jungle safaris, birdwatching trails and trekking routes through surrounding hills and caves such as the Ulavi Caves"),
        ],
        "itinerary": [
            ("Day 0", "Friday", ["Start from Bengaluru by 9 pm."]),
            ("Day 1", "Saturday", [
                "Reach the resort by 9:30 am and freshen up in the allotted dorms.",
                "Assemble for breakfast by 10 am.",
                "Leave for water activities by 10:45 am.",
                "Reach the adventure activities centre by 11:15 am.",
                "Start the activities and wait for your turn to get each one done.",
                "Assemble for lunch at a specified place, then resume the activities.",
                "Finish all the activities and start back for the resort.",
                "Freshen up and assemble for dinner around the campfire.",
                "Spend time playing games, dancing around the campfire and sharing experiences of the day, then head to bed.",
            ]),
            ("Day 2", "Sunday", [
                "Wake up to the sounds of nature and take a quick walk around the homestay in the jungle.",
                "Assemble for breakfast, check out and start for Yellapur.",
                "Visit Sahasralinga and the hanging bridge, spend time and click pictures.",
                "Visit Sirsi Marikamba Temple, have a self-sponsored lunch and start for Sagara.",
                "Visit Champaka Sarasi and start for Shimoga. Have a self-sponsored dinner.",
                "Start for Bengaluru.",
            ]),
            ("Day 3", "Monday", ["Reach Bengaluru by 5:30 am."]),
        ],
        "inclusions": [
            "To and fro transport in a non-AC private vehicle",
            "Dormitory stay accommodation",
            "Guide fee", "Souvenir",
            "Boating, kayaking, zorbing and river rafting",
            "Refreshments", "2 breakfasts", "1 lunch", "1 dinner (veg / non-veg)",
            "Basic first aid", "Bonfire (if weather permits)",
        ],
        "prices": [(5350, "with all inclusions"), (4159, "exclusive of transport"),
                   (2000, "exclusive of transport, stay and meals")],
        "price_note": "Additional discount of Rs 100 per head for repeaters, or if you are a group of 5 or more.",
        "own_transport": "Those coming by own transport, please reach the resort by 6 am on Saturday. The location will be shared on WhatsApp.",
        "forest_fee": False,
        "things_to_carry": WATER_THINGS_TO_CARRY,
    },
    # ------------------------------------------------------------------ Day treks
    {
        "slug": "chennarayanadurga",
        "name": "Chennarayana Durga",
        "heading": "Chennarayana Durga",
        "tagline": "Monolithic",
        "category": "day-treks",
        "coords": (13.5897, 77.2067),
        "coords_label": "13.5897&deg; N, 77.2067&deg; E",
        "duration": "1 Day",
        "difficulty": "Moderate",
        "distance": "~1.5 &ndash; 2 hours up, ~1 hour down",
        "location": "Tumakuru District, Karnataka",
        "image": "./assets/images/travel-list/12.jpg",
        "gallery": ["./assets/images/gallery/gallery10.jpg", "./assets/images/gallery/gallery11.jpg",
                    "./assets/images/gallery/gallery12.jpg"],
        "intro": [
            "The hike to Channarayana Durga Fort is a thrilling, offbeat trek in the Tumakuru "
            "district of Karnataka. Rising to an elevation of around 3,730 feet, this massive "
            "monolithic hill is crowned by a historic multi-tiered fort built by Channapa Gauda in "
            "the 17th century.",
        ],
        "facts": [
            ("District / Region", "Tumakuru District, Karnataka"),
            ("Elevation", "~3,730 ft above sea level"),
            ("Trail &amp; Terrain", "Primarily steep, bare rock faces (rocky monolith) with very little shade or vegetation on the incline"),
            ("Fort Structures", "Multiple gateways, stone guard walls, watchtowers, water reservoirs (kalyanis) and old stone ruins carved into the hillside"),
            ("Views &amp; Summit", "Panoramic views of the surrounding rural landscape, agricultural fields and neighbouring hillocks of the Tumakuru region"),
            ("Difficulty &amp; Duration", "Moderate &mdash; about 1.5 to 2 hours to reach the top and about 1 hour to descend"),
        ],
        "itinerary": [
            ("Day 1", "Sunday", [
                "Start from Vijaynagar Metro Station by 5:30 am.",
                "Pickup from Majestic (Shanthala Silks) by 6 am.",
                "Pickup from Yeshwanthpur (Govardhan Theatre) by 6:40 am and Goraguntepalya (KLE Dental College) by 6:50 am.",
                "Tea break at Nelamangala Toll.",
                "Reach the foothills of Chennarayana Durga by 8:30 am.",
                "Collect packed breakfast and start the trek.",
                "Stop at viewpoints and click pictures of the sunrise.",
                "Get to the peak by 10:30 am.",
                "Have breakfast, spend time clicking pictures and gazing at the bird's eye view of the hill ranges from Asia's biggest monolith.",
                "Start descending by 11:30 am and reach the base by 12:30 pm.",
                "Board the bus and stop for lunch en route.",
                "Visit Devarayandurga on the way back to Bengaluru.",
                "Reach Bengaluru by 5 pm.",
            ]),
        ],
        "inclusions": [
            "To and fro transport in a non-AC private vehicle",
            "Guide fee", "Forest fee", "Permissions", "Souvenir",
            "1 breakfast", "1 lunch",
        ],
        "prices": [(1000, "with all inclusions"), (500, "exclusive of transport"),
                   (600, "for kids above 6 years")],
        "price_note": "Absolutely free for kids below 6 years.",
        "own_transport": "Those coming by own transport, please reach the base by 8 am on Sunday. The location will be shared on WhatsApp.",
        "forest_fee": True,
        "things_to_carry": DAY_TREK_THINGS_TO_CARRY,
        "payment_policy": DAY_TREK_PAYMENT_POLICY,
        "exclusions": [
            "Meals other than the breakfast and lunch specified in the inclusions.",
            "Any kind of medical or accidental insurance.",
            "Personal expenses and anything not listed under inclusions.",
        ],
    },
    # --------------------------------------------------------------- Backpacking
    {
        "slug": "rajasthan",
        "name": "Rajasthan",
        "heading": "Rajasthan",
        "tagline": "Jaipur &middot; Bikaner &middot; Jaisalmer &middot; Jodhpur &middot; Udaipur",
        "category": "backpacking-tours",
        "coords": (26.9124, 75.7873),
        "coords_label": "26.9124&deg; N, 75.7873&deg; E (Jaipur)",
        "duration": "9 Days / 8 Nights",
        "difficulty": "Easy &mdash; sightseeing and road travel",
        "distance": "Jaipur &rarr; Bikaner &rarr; Sam &rarr; Jaisalmer &rarr; Jodhpur &rarr; Udaipur",
        "location": "Rajasthan, India",
        "image": "./assets/images/travel-list/13.jpg",
        "gallery": ["./assets/images/explore/el1.jpg", "./assets/images/explore/el2.jpg",
                    "./assets/images/explore/el3.jpg"],
        "intro": [
            "A nine-day loop through the forts, havelis, lakes and dunes of Rajasthan, covering "
            "Jaipur, Bikaner, Jaisalmer, Jodhpur and Udaipur. Air-conditioned stays, an exclusive "
            "AC tempo traveller, local guides and all entrance fees are taken care of &mdash; you "
            "just show up at Jaipur airport.",
        ],
        "facts": [
            ("Route", "Jaipur &rarr; Bikaner &rarr; Sam &rarr; Jaisalmer &rarr; Jodhpur &rarr; Udaipur"),
            ("Duration", "8 Nights / 9 Days"),
            ("Starts", "Jaipur Airport"),
            ("Ends", "Udaipur Airport"),
            ("Accommodation", "Air-conditioned hotels on double occupancy, plus one night in a desert camp"),
            ("Transport", "Exclusive AC tempo traveller for all sightseeing and transfers"),
        ],
        "itinerary": [
            ("Day 01", "Jaipur &mdash; Arrival &amp; New City Tour", [
                "You will be picked up from Jaipur airport and transferred to the hotel.",
                "After lunch we start the Jaipur outer city tour covering Statue Circle, the new Vidhana Sabha, the War Memorial, Albert Hall Museum, Birla Mandir and Patrika Gate.",
                "In the evening proceed to old Jaipur &mdash; explore the streets, shop, and try local snacks and handicrafts.",
                "Return to the hotel for an overnight stay at Jaipur.",
            ]),
            ("Day 02", "Jaipur &mdash; Pink City &amp; Amer Fort", [
                "After breakfast we start the Pink City tour of old Jaipur along with our guide.",
                "The full-day city tour covers Amber Fort, Sheesh Mahal, Jal Mahal, City Palace, Jantar Mantar, Hawa Mahal and the walled Pink City.",
                "In the evening we take in a stunning view of the Pink City from the hills of Nahargarh Fort, and a breathtaking sunset.",
                "Later we enjoy the sound and light show at Amber Fort.",
                "After dinner proceed to the hotel for an overnight stay at Jaipur.",
            ]),
            ("Day 03", "Jaipur &rarr; Bikaner", [
                "After breakfast transfer to Bikaner, 250 km (about a 5-hour drive).",
                "En route we visit Deshnok Rat Temple.",
                "Soon after check-in we start Bikaner sightseeing covering Lalgarh Palace &amp; Museum, Junagarh Fort and the Camel Breeding Farm.",
                "In the evening explore the snack and sweet stall streets of Bikaner.",
                "Overnight at Bikaner.",
            ]),
            ("Day 04", "Bikaner &rarr; Sam Sand Dunes", [
                "After breakfast transfer to Sam, 350 km (about a 6-hour drive).",
                "Return to the desert camp, enjoy the camel ride and witness the sunset from the deserts of Jaisalmer.",
                "Experience an Arabian-night-like stay at the desert camps alongside a bonfire, a musical night and folk performances.",
                "Overnight stay in tented accommodation.",
            ]),
            ("Day 05", "Sam &rarr; Jaisalmer", [
                "Have breakfast and check out.",
                "Transfer to Jaisalmer, 50 km (about a 1-hour drive).",
                "After check-in we leave for Jaisalmer Fort with our guide, and visit Nathmal Haveli, Patwon Ki Haveli and the Jain temples inside the fort.",
                "Visit Gadisar Lake and Vyas Chhatri.",
                "Overnight stay at Jaisalmer.",
            ]),
            ("Day 06", "Jaisalmer &rarr; Jodhpur", [
                "After breakfast check out from the hotel.",
                "Proceed to Jodhpur (280 km / 4&ndash;5 hours).",
                "Upon arrival check in at the hotel, then visit Mehrangarh Fort, Jaswant Thada, Umaid Bhawan Palace &amp; Museum, the Clock Tower and Jodhpur old city.",
                "Overnight at Jodhpur.",
            ]),
            ("Day 07", "Jodhpur &rarr; Udaipur via Kumbhalgarh", [
                "After breakfast check out from the hotel.",
                "Start for Udaipur, en route visiting Kumbhalgarh Fort and Palace.",
                "If time permits, visit Ranakpur Jain Temple.",
                "Reach Udaipur and go for a boat ride on Lake Pichola during sunset.",
                "Check in to the hotel and visit the local markets.",
                "Overnight stay at Udaipur.",
            ]),
            ("Day 08", "Udaipur &mdash; Full Day City Tour", [
                "After breakfast leave for the city tour.",
                "Visit City Palace, Jagdish Temple, Saheliyon Ki Bari, Pratap Smarak, Fateh Sagar Lake, Pratap Sagar Lake, Shilpgram and Sajjangarh.",
                "Overnight stay at Udaipur.",
            ]),
            ("Day 09", "Departure", [
                "After breakfast, leave for the airport.",
            ]),
        ],
        "inclusions": [
            "08 nights / 09 days of air-conditioned accommodation (double occupancy room)",
            "Daily breakfast and dinner",
            "All sightseeing and transfers by an exclusive AC tempo traveller",
            "Driver allowance, fuel, parking charges, toll taxes and interstate taxes",
            "Desert camp stay including camel ride, hi-tea, bonfire, cultural programmes and veg dinner",
            "All entrance fees",
            "Local guide service during Jaipur, Jaisalmer, Jodhpur and Udaipur sightseeing",
            "Complimentary packaged drinking water bottles in the vehicle",
            "Price is inclusive of GST",
        ],
        "exclusions": [
            "Meals and drinks other than those specified in the inclusions.",
            "Expenses of a personal nature such as portage, tips and laundry.",
            "Guide and driver tipping.",
            "Chokhi Dhani dinner and entrance charges.",
            "Light &amp; sound show and boat ride ticket charges.",
            "Any air, train or bus fare.",
            "Travel insurance.",
        ],
        "hotels": [
            ("Jaipur", "Hotel Royal GM Plaza (2N)"),
            ("Bikaner", "Hotel Marudhar Palace (1N)"),
            ("Jaisalmer", "Hotel Gorakh Haveli (1N)"),
            ("Sam", "Welcome Desert Camp (1N)"),
            ("Jodhpur", "Hotel Kissan Legacy (1N)"),
            ("Udaipur", "Hotel Royal Excellency (2N)"),
        ],
        "prices": [(30000, "excluding air fares, double sharing accommodation"),
                   (60000, "including air fares")],
        "price_note": "All hotels are subject to availability, otherwise similar stays will be provided.",
        "payment_policy": BACKPACKING_PAYMENT_POLICY,
        "cancellation_policy": BACKPACKING_CANCELLATION_POLICY,
        "cancellation_note": BACKPACKING_CANCELLATION_NOTE,
        "forest_fee": False,
        "things_to_carry": None,
        "pickup": False,
        "arrival": [
            "The tour starts at Jaipur airport, where you will be picked up and transferred to the hotel.",
            "The tour ends with a drop at Udaipur airport after breakfast on the final day.",
            "Air, train and bus fares are not included. Please book your tickets to match the batch dates shared at the time of booking, and send us a copy along with your advance payment.",
            "All sightseeing and transfers in between are covered by an exclusive AC tempo traveller.",
        ],
    },
    {
        "slug": "spiti",
        "name": "Spiti Valley",
        "heading": "Spiti Valley",
        "tagline": "Shimla &middot; Sangla &middot; Chitkul &middot; Tabo &middot; Kaza &middot; Kalpa",
        "category": "backpacking-tours",
        "coords": (32.2272, 78.0720),
        "coords_label": "32.2272&deg; N, 78.0720&deg; E (Kaza)",
        "duration": "8 Days / 7 Nights",
        "difficulty": "Moderate &mdash; high-altitude road travel",
        "distance": "Shimla &rarr; Sangla &rarr; Tabo &rarr; Kaza &rarr; Kalpa &rarr; Shimla",
        "location": "Himachal Pradesh, India",
        "image": "./assets/images/travel-list/14.jpg",
        "gallery": ["./assets/images/explore/el4.jpg", "./assets/images/explore/el5.jpg",
                    "./assets/images/explore/el6.jpg"],
        "intro": [
            "An eight-day circuit from Chandigarh into the cold desert of Spiti, climbing through "
            "Shimla, Kinnaur and the Sutlej gorge before crossing into the valley at Sumdo. Along "
            "the way you will see India's last village before Tibet, the world's highest post "
            "office, the world's highest motorable village and the iconic Key Monastery.",
        ],
        "facts": [
            ("Route", "Shimla &rarr; Sangla &rarr; Chitkul &rarr; Tabo &rarr; Kaza &rarr; Kalpa &rarr; Shimla"),
            ("Duration", "7 Nights / 8 Days"),
            ("Starts &amp; Ends", "Chandigarh Airport"),
            ("Accommodation", "Air-conditioned stays and homestays on double occupancy"),
            ("Transport", "Exclusive AC tempo traveller for all sightseeing and transfers"),
            ("Terrain", "High-altitude mountain roads, including one of the world's most challenging stretches"),
        ],
        "itinerary": [
            ("Day 01", "Chandigarh &rarr; Shimla", [
                "You will be picked up from Chandigarh airport.",
                "Stop for a self-sponsored lunch en route to Shimla.",
                "Transfer to Shimla and check in to the stay.",
                "Leave for Mall Road, visit Ridge Point and explore the local market and cuisines of Himachal.",
                "Get back to the stay by 9 pm. The briefing for the next day happens over dinner.",
            ]),
            ("Day 02", "Shimla &rarr; Sangla", [
                "After an early breakfast we start our journey towards Sangla in Kinnaur district.",
                "A 280 km drive along scenic Himalayan ranges and one of the world's deadliest roads.",
                "Stop for a self-sponsored lunch.",
                "After lunch stop at the Gateway of Kinnaur, then drive alongside the Sutlej river all the way to Sangla.",
                "Check in to the stay at Sangla, have dinner and head to bed after the briefing.",
            ]),
            ("Day 03", "Sangla &rarr; Chitkul &rarr; Tabo", [
                "After an early breakfast, start for Chitkul, India's last village before Tibet.",
                "Spend time enjoying the views from the banks of the River Baspa.",
                "Leave for Tabo, en route visiting Khab Sangam &mdash; the confluence of the Spiti and Sutlej rivers &mdash; Nako Lake and Monastery.",
                "Enter the Spiti Valley at Sumdo and reach Tabo by night.",
                "Check in to the stay, have dinner and head to bed.",
            ]),
            ("Day 04", "Tabo &rarr; Kaza", [
                "After breakfast, visit Tabo Monastery and the Tabo Caves.",
                "Check out from the stay and start for Kaza.",
                "En route visit Dhankar Monastery, and Dhankar Lake if time permits.",
                "Self-sponsored lunch at Dhankar.",
                "Reach Kaza by evening and check in to the stay.",
                "Leave for the Kaza market and explore local commodities, cafes and food.",
                "Get back to the stay, have dinner and head to bed.",
            ]),
            ("Day 05", "Kaza &mdash; Langza, Komic, Hikkim, Chicham &amp; Key", [
                "After breakfast, start for Langza &mdash; the fossil village, home to the world's highest Buddha statue.",
                "Visit Komic, the world's highest motorable village and home to the world's highest cafe, then Hikkim, the world's highest post office.",
                "Then on to Chicham, the world's highest suspension bridge. If lucky, spot snow leopards and ibex.",
                "Lastly, the iconic Key Monastery, before heading back to the stay.",
                "Self exploration in the market, dinner, and then to bed.",
            ]),
            ("Day 06", "Kaza &rarr; Kalpa", [
                "After breakfast, start for Kalpa.",
                "En route visit Gue Monastery. Stop for lunch at Nako.",
                "Reach Reckong Peo market by evening, explore the market and then head to the stay.",
                "Check in, have dinner and overnight stay at Kalpa.",
            ]),
            ("Day 07", "Kalpa &rarr; Shimla", [
                "After breakfast check out from the hotel.",
                "Visit Roghi suicide point, Kalpa Monastery and temple.",
                "Start for Shimla and reach by evening. Check in and overnight stay after dinner.",
            ]),
            ("Day 08", "Departure", [
                "After breakfast, leave for Chandigarh airport.",
            ]),
        ],
        "inclusions": [
            "07 nights / 08 days of air-conditioned accommodation (double occupancy room)",
            "Daily breakfast and dinner",
            "All sightseeing and transfers by an exclusive AC tempo traveller",
            "Driver allowance, fuel, parking charges, toll taxes and interstate taxes",
            "All entrance fees",
            "Farewell gift on departure",
            "Price is inclusive of GST",
        ],
        "exclusions": [
            "Meals and drinks other than those specified in the inclusions.",
            "Expenses of a personal nature such as portage, tips and laundry.",
            "Guide and driver tipping.",
            "Any air, train or bus fare.",
            "Travel insurance.",
        ],
        "hotels": [
            ("Shimla", "Traveller's Inn (2N)"),
            ("Sangla", "Negi Cottage (1N)"),
            ("Tabo", "Green Tara (1N)"),
            ("Kaza", "Dragon Homestay (2N)"),
            ("Kalpa", "Jahnvi Homestay (1N)"),
        ],
        "prices": [(25000, "excluding air fares, double sharing accommodation"),
                   (50000, "including air fares")],
        "price_note": "All hotels are subject to availability, otherwise similar stays will be provided.",
        "payment_policy": BACKPACKING_PAYMENT_POLICY,
        "cancellation_policy": BACKPACKING_CANCELLATION_POLICY,
        "cancellation_note": BACKPACKING_CANCELLATION_NOTE,
        "forest_fee": False,
        "things_to_carry": None,
        "pickup": False,
        "arrival": [
            "The tour starts and ends at Chandigarh airport.",
            "You will be picked up from Chandigarh airport on day one and dropped back there after breakfast on the final day.",
            "Air, train and bus fares are not included. Please book your tickets to match the batch dates shared at the time of booking, and send us a copy along with your advance payment.",
            "All sightseeing and transfers in between are covered by an exclusive AC tempo traveller.",
            "This is a high-altitude route. Please consult a medical professional before booking if you have any pre-existing condition.",
        ],
    },
]


# --------------------------------------------------------------------------- photos

BANNER_FALLBACK = "./assets/images/page/breakcrumb.jpg"

GALLERY_TAB_FALLBACK = [
    "./assets/images/gallery/gallery.jpg",
    "./assets/images/gallery/gallery2.jpg",
    "./assets/images/gallery/gallery3.jpg",
    "./assets/images/gallery/gallery4.jpg",
    "./assets/images/gallery/gallery5.jpg",
    "./assets/images/gallery/gallery6.jpg",
]


def _resolve_photos() -> None:
    for cat in CATEGORIES:
        main = photo(cat["slug"], cat["image"])
        cat["image"] = main
        cat["banner"] = photo(f"{cat['slug']}-banner", _banner_default(main))

    for tour in TOURS:
        slug = tour["slug"]
        main = photo(slug, tour["image"])
        tour["image"] = main
        tour["banner"] = photo(f"{slug}-banner", _banner_default(main))
        tour["gallery"] = [photo(f"{slug}-{i}", src) for i, src in enumerate(tour["gallery"], start=1)]
        tour["gallery_tab"] = [photo(f"{slug}-{i}", src)
                               for i, src in enumerate(GALLERY_TAB_FALLBACK, start=1)]


def _banner_default(main: str) -> str:
    """Your own hero doubles as the banner; the stock card art is too small to stretch."""
    return main if main.startswith("./assets/images/tours/") else BANNER_FALLBACK


_resolve_photos()
