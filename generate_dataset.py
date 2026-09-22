import os
import json

# Image paths mapping
images = {
    "minimalist": "/assets/inspiration/insp_minimalist.png",
    "capsule": "/assets/inspiration/insp_capsule_wardrobe.png",
    "clean": "/assets/inspiration/insp_clean_girl.png",
    "y2k": "/assets/inspiration/insp_y2k.png",
    "barbie": "/assets/inspiration/insp_barbiecore.png",
    "bratz": "/assets/inspiration/insp_bratz_fashion.png",
    "dark_academia": "/assets/inspiration/insp_dark_academia.png",
    "old_money": "/assets/inspiration/insp_old_money.png",
    "coastal": "/assets/inspiration/insp_coastal_grandmother.png",
    "cottagecore": "/assets/inspiration/insp_cottagecore.png",
    "streetwear": "/assets/inspiration/insp_streetwear.png",
    "office": "/assets/inspiration/insp_office_siren.png",
    "winter": "/assets/inspiration/insp_winter_outfits.png",
    "coquette": "/assets/inspiration/insp_coquette.png",
    "ballet": "/assets/inspiration/insp_ballet_core.png",
    "summer": "/assets/inspiration/insp_summer_outfits.png"
}

# 1. Aesthetics (15 boards, 4 cards each = 60 cards)
aesthetics_raw = {
    "Minimalism / Quiet Luxury": [
        {"title": "Double-Breasted Cream Coat", "image": images["minimalist"], "notes": "A cream coat layered over matching cream knit trousers for an understated quiet luxury feel.", "colors": ["#FFFDD0", "#EAE6DF", "#CCCCCC", "#1A1817"]},
        {"title": "Tailored Pleated Trousers", "image": images["minimalist"], "notes": "Sleek beige high-waisted tailored pants paired with a tucked-in white silk button-down.", "colors": ["#D2B48C", "#FFFFFF", "#E1D9D1", "#1A1817"]},
        {"title": "Cashmere Mockneck Sweater", "image": images["capsule"], "notes": "Grey cashmere mockneck knit paired with structured slate trousers and leather loafers.", "colors": ["#808080", "#2B2B2B", "#FFFFFF", "#CCCCCC"]},
        {"title": "Silk Wrap Midi Skirt", "image": images["minimalist"], "notes": "A sand-toned silk wrap skirt styled with a simple white ribbed crewneck top.", "colors": ["#E1D9D1", "#FFFFFF", "#C2B280", "#1A1817"]}
    ],
    "Y2K": [
        {"title": "Low-Rise Denim & Baby Tee", "image": images["y2k"], "notes": "Low-rise baggy cargo jeans paired with a baby pink graphic crop tee and metallic hair clips.", "colors": ["#FFC0CB", "#4B6F96", "#CCCCCC", "#FFFFFF"]},
        {"title": "Metallic Silver Crop Puffer", "image": images["y2k"], "notes": "Silver foil cropped puffer jacket worn with dark wash low-rise jeans and chunky sneakers.", "colors": ["#C0C0C0", "#1A1A1A", "#FFFFFF", "#FF0000"]},
        {"title": "Rhinestone Velour Track Jacket", "image": images["barbie"], "notes": "Y2K velour track jacket in hot pink with rhinestone detailing and a chunky silver zip.", "colors": ["#FF1493", "#FF69B4", "#CCCCCC", "#FFFFFF"]},
        {"title": "Pleated Denim Micro Skirt", "image": images["bratz"], "notes": "A pleated blue denim micro skirt styled with a red crop tank top and pink chunky sandals.", "colors": ["#FF0000", "#FFC0CB", "#4B6F96", "#0D0D0D"]}
    ],
    "Dark Academia": [
        {"title": "Tweed Blazer & Pleated Skirt", "image": images["dark_academia"], "notes": "Chocolate brown herringbone tweed blazer combined with a black pleated wool skirt.", "colors": ["#5C4033", "#0D0D0D", "#FFFDD0", "#8B5A2B"]},
        {"title": "Herringbone Oversized Coat", "image": images["dark_academia"], "notes": "Oversized grey herringbone wool coat layered over a black ribbed mockneck.", "colors": ["#808080", "#0D0D0D", "#FFFFFF", "#CCCCCC"]},
        {"title": "Ribbed Corduroy Blazer", "image": images["dark_academia"], "notes": "Plum velvet corduroy blazer styled with a charcoal grey turtleneck sweater.", "colors": ["#3A0033", "#808080", "#1A1A1A", "#FFFFFF"]},
        {"title": "Scholarly Wool Cable Vest", "image": images["dark_academia"], "notes": "Earthy brown cable vest layered over a white cotton button-down and trousers.", "colors": ["#5C4033", "#FFFFFF", "#F5F5DC", "#2B2B2B"]}
    ],
    "Cottagecore": [
        {"title": "Gingham Puffed Sleeve Dress", "image": images["cottagecore"], "notes": "Sage green and cream gingham maxi dress styled with a woven straw hat.", "colors": ["#8FBC8F", "#FFFDD0", "#8B5A2B", "#FFFFFF"]},
        {"title": "Linen Ruffled Sundress", "image": images["cottagecore"], "notes": "A simple cream linen sundress featuring ruffled shoulder straps and a tiered skirt.", "colors": ["#FFFDD0", "#EAE6DF", "#C2B280", "#FFFFFF"]},
        {"title": "Crochet Floral Knit Vest", "image": images["cottagecore"], "notes": "A hand-crocheted cream vest decorated with pastel embroidered flowers over a white dress.", "colors": ["#FFFDD0", "#FFC0CB", "#8FBC8F", "#FFFFFF"]},
        {"title": "Swiss Dot Prairie Blouse", "image": images["cottagecore"], "notes": "Ivory Swiss dot cotton blouse styled with a sage green tiered linen maxi skirt.", "colors": ["#FFFFFF", "#8FBC8F", "#FFFDD0", "#D2B48C"]}
    ],
    "Streetwear": [
        {"title": "Oversized Utility Cargo Hoodie", "image": images["streetwear"], "notes": "Oversized black graphic hoodie paired with black nylon utility cargo pants.", "colors": ["#0D0D0D", "#CCCCCC", "#555555", "#FFFFFF"]},
        {"title": "Nylon Graphic Windbreaker", "image": images["streetwear"], "notes": "Color-blocked olive and black windbreaker jacket paired with loose utility joggers.", "colors": ["#556B2F", "#0D0D0D", "#1F1F1F", "#CCCCCC"]},
        {"title": "Baggy Denim & Varsity Jacket", "image": images["streetwear"], "notes": "Oversized black varsity jacket styled with light-wash baggy denim jeans.", "colors": ["#0D0D0D", "#4B6F96", "#CCCCCC", "#FFFFFF"]},
        {"title": "Chunky Sneakers Utility Style", "image": images["streetwear"], "notes": "Black cargo track pants paired with an oversized white graphic tee and chunky trainers.", "colors": ["#0D0D0D", "#FFFFFF", "#808080", "#1F1F1F"]}
    ],
    "Gorpcore": [
        {"title": "Technical Ripstop Shell Jacket", "image": images["streetwear"], "notes": "Waterproof olive green shell jacket featuring taped seams and utility zippers.", "colors": ["#556B2F", "#0D0D0D", "#CCCCCC", "#1F1F1F"]},
        {"title": "Waterproof Fleece-Lined Parka", "image": images["streetwear"], "notes": "Heavy navy blue technical parka shell worn over hiking utility trail pants.", "colors": ["#0B1D3A", "#D2B48C", "#111111", "#CCCCCC"]},
        {"title": "Nylon Utility Trail Pants", "image": images["streetwear"], "notes": "Tan ripstop utility pants styled with a tactical quick-release belt and shell jacket.", "colors": ["#D2B48C", "#0B1D3A", "#0D0D0D", "#CCCCCC"]},
        {"title": "Hiking Trail Shell Vest", "image": images["streetwear"], "notes": "Sage green technical cargo vest layered over a black dry-fit long-sleeve tee.", "colors": ["#8FBC8F", "#0D0D0D", "#EAE6DF", "#1F1F1F"]}
    ],
    "Grunge": [
        {"title": "Oversized Checked Flannel Shirt", "image": images["dark_academia"], "notes": "Burgundy and cream checked flannel shirt styled open over a distressed band tee.", "colors": ["#800020", "#FFFDD0", "#0D0D0D", "#808080"]},
        {"title": "Distressed Knit & Slip Skirt", "image": images["winter"], "notes": "Oversized ripped burgundy sweater paired with a black silk slip midi skirt.", "colors": ["#800020", "#0D0D0D", "#FFFDD0", "#4A4A4A"]},
        {"title": "Chunky Combat Boots Grunge Fit", "image": images["winter"], "notes": "Heavily distressed dark grey jeans paired with chunky black leather combat boots.", "colors": ["#808080", "#0D0D0D", "#CCCCCC", "#1F1F1F"]},
        {"title": "Faded Band Tee & Leather Jacket", "image": images["office"], "notes": "A black leather moto jacket thrown over a faded charcoal band tee and distressed jeans.", "colors": ["#0D0D0D", "#808080", "#CCCCCC", "#1F1F1F"]}
    ],
    "Coquette / Balletcore": [
        {"title": "Pink Ribbon Cardigan & Bows", "image": images["coquette"], "notes": "Light pink cardigan styled with small red satin bows down the front button placket.", "colors": ["#FFC0CB", "#FF0000", "#FFF0F5", "#FDF2F8"]},
        {"title": "Ballet Wrap Top & Tulle Skirt", "image": images["coquette"], "notes": "Ribbed pale pink wrap top worn with a white tulle skirt and satin hair ribbons.", "colors": ["#FFC0CB", "#FFFFFF", "#FFFDD0", "#FFF0F5"]},
        {"title": "Satin Slip Dress & Pearl Choker", "image": images["coquette"], "notes": "Soft pink satin midi slip dress styled with a delicate red ribbon choker.", "colors": ["#FFC0CB", "#FF0000", "#FFF0F5", "#FFFFFF"]},
        {"title": "Ruffled Pastel Knit Camisole", "image": images["coquette"], "notes": "Lavender knit camisole with white ruffle trim details and matching hair ribbons.", "colors": ["#E6E6FA", "#FFFDD0", "#D4AF37", "#9370DB"]}
    ],
    "Old Money / Preppy": [
        {"title": "Navy Crest Blazer & Chinos", "image": images["old_money"], "notes": "Double-breasted navy crest blazer styled with tan tailored wool chinos.", "colors": ["#0B1D3A", "#D2B48C", "#D4AF37", "#FFFFFF"]},
        {"title": "Cable-Knit Tennis Polo Vest", "image": images["old_money"], "notes": "White cable-knit tennis vest with navy piping layered over a white polo shirt.", "colors": ["#FFFFFF", "#0B1D3A", "#D2B48C", "#CCCCCC"]},
        {"title": "Tailored Double-Breasted Trench", "image": images["old_money"], "notes": "Camel hair double-breasted trench coat paired with white linen trousers.", "colors": ["#C2B280", "#FFFFFF", "#EAE6DF", "#8B5A2B"]},
        {"title": "Oxford Button-Down & Pleated Skirt", "image": images["old_money"], "notes": "Crisp light blue Oxford button-down tucked into a beige pleated tennis skirt.", "colors": ["#ADD8E6", "#C2B280", "#FFFFFF", "#5C4033"]}
    ],
    "Eclectic Grandpa": [
        {"title": "Chunky Knit Patterned Cardigan", "image": images["coastal"], "notes": "Vintage patterned brown knit cardigan worn over a light blue denim button-down.", "colors": ["#5C4033", "#ADD8E6", "#FFFDD0", "#D4AF37"]},
        {"title": "Corduroy Blazer & Argyle Vest", "image": images["coastal"], "notes": "Tan corduroy blazer layered over a mustard yellow argyle vest and brown pants.", "colors": ["#C2B280", "#FFD700", "#5C4033", "#F0F0F0"]},
        {"title": "Oversized Wool Grandpa Vest", "image": images["coastal"], "notes": "Patterned brown wool vest styled with a blue Oxford shirt and green pants.", "colors": ["#5C4033", "#F5F5DC", "#ADD8E6", "#2E8B57"]},
        {"title": "Academic Loafers Corduroy Trousers", "image": images["coastal"], "notes": "Chocolate brown ribbed cardigan paired with beige corduroys and suede penny loafers.", "colors": ["#5C4033", "#F5F5DC", "#8B5A2B", "#C2B280"]}
    ],
    "Cyberpunk / Techwear": [
        {"title": "Tactical Asymmetric Buckled Jacket", "image": images["streetwear"], "notes": "All-black asymmetrical tactical windbreaker featuring industrial silver strap buckles.", "colors": ["#0D0D0D", "#CCCCCC", "#1F1F1F", "#808080"]},
        {"title": "Harness Strap Cargo Trousers", "image": images["streetwear"], "notes": "All-black utility cargo pants with adjustable harness straps and tactical metal buckles.", "colors": ["#0D0D0D", "#CCCCCC", "#1A1A1A", "#808080"]},
        {"title": "Reflective Waterproof Shell", "image": images["streetwear"], "notes": "Grey reflective technical shell jacket paired with black utility ripstop cargos.", "colors": ["#808080", "#0D0D0D", "#CCCCCC", "#1F1F1F"]},
        {"title": "Industrial Silver Zipper Vest", "image": images["streetwear"], "notes": "Black technical vest loaded with multi-pockets and heavy-duty silver zippers.", "colors": ["#0D0D0D", "#CCCCCC", "#1F1F1F", "#FFFFFF"]}
    ],
    "Boho Chic": [
        {"title": "Fringe Suede Outerwear Jacket", "image": images["cottagecore"], "notes": "A fringe camel suede jacket layered over an ivory crochet crop top and flared jeans.", "colors": ["#C2B280", "#FFFDD0", "#8B5A2B", "#40E0D0"]},
        {"title": "Crochet Tiered Maxi Sundress", "image": images["cottagecore"], "notes": "Ivory crochet knit maxi dress layered over a camel bodysuit with turquoise jewelry.", "colors": ["#FFFDD0", "#C2B280", "#FFD700", "#FFFFFF"]},
        {"title": "Embroidered Cotton Tunic Top", "image": images["cottagecore"], "notes": "Warm ivory embroidered linen tunic paired with camel suede boots and fringe bag.", "colors": ["#FFFDD0", "#C2B280", "#8B5A2B", "#F5F5DC"]},
        {"title": "Boho Suede Fringe Shoulder Fit", "image": images["cottagecore"], "notes": "Tiered floral print maxi dress styled with a fringe suede shoulder vest and belt.", "colors": ["#8B5A2B", "#FFFDD0", "#C2B280", "#40E0D0"]}
    ],
    "Whimsigoth": [
        {"title": "Deep Velvet Lace Slip Dress", "image": images["dark_academia"], "notes": "A deep plum velvet slip dress with black lace trim, styled with platforms.", "colors": ["#3A0033", "#000000", "#808080", "#800020"]},
        {"title": "Celestial Embroidered Velvet Skirt", "image": images["dark_academia"], "notes": "Deep plum velvet maxi skirt styled with a black lace top and celestial gold pins.", "colors": ["#3A0033", "#000000", "#D4AF37", "#808080"]},
        {"title": "Sheer Bell Sleeve Lace Top", "image": images["dark_academia"], "notes": "Burgundy velvet bodice with dramatic sheer bell sleeves, styled with cream pants.", "colors": ["#800020", "#FFFDD0", "#3A0033", "#1A1A1A"]},
        {"title": "Plum Velvet Kimono Duster", "image": images["dark_academia"], "notes": "A flowing plum velvet kimono duster layered over an all-black ribbed base set.", "colors": ["#3A0033", "#0D0D0D", "#808080", "#800020"]}
    ],
    "Indie Sleaze": [
        {"title": "Shiny Silver Sequin Tank Top", "image": images["y2k"], "notes": "Metallic silver sequined tank top paired with distressed black skinny pants.", "colors": ["#1A1A1A", "#C0C0C0", "#F0F0F0", "#0D0D0D"]},
        {"title": "Metallic Leather Skinny Pants", "image": images["y2k"], "notes": "High-shine black leather skinny trousers styled with a distressed charcoal graphic tee.", "colors": ["#808080", "#CCCCCC", "#0D0D0D", "#FFFFFF"]},
        {"title": "Graphic Band Tee & Faux Fur Coat", "image": images["y2k"], "notes": "Vintage black faux fur coat worn over a graphic band tee and glitter boots.", "colors": ["#0D0D0D", "#CCCCCC", "#1F1F1F", "#FFFFFF"]},
        {"title": "Distressed Leather Moto Vest", "image": images["y2k"], "notes": "Black distressed leather motorcycle vest layered over a shiny silver chainmail tank.", "colors": ["#0D0D0D", "#CCCCCC", "#FFFFFF", "#1F1F1F"]}
    ],
    "Clean Girl": [
        {"title": "White Ribbed Knit Lounge Set", "image": images["clean"], "notes": "Crisp white ribbed knit crewneck sweater with matching clean white lounge pants.", "colors": ["#FFFFFF", "#EAE6DF", "#CCCCCC", "#4E3629"]},
        {"title": "Sleek Bun Linen Button-Down", "image": images["clean"], "notes": "Clean girl oversized white linen button-down styled with simple gold hoop earrings.", "colors": ["#FFFFFF", "#EAE6DF", "#D4AF37", "#1A1817"]},
        {"title": "Tailored Beige Trench Coat", "image": images["clean"], "notes": "Tailored camel trench coat styled over an ivory activewear jumpsuit and sneakers.", "colors": ["#C2B280", "#FFFDD0", "#FFFFFF", "#5C4033"]},
        {"title": "Activewear Jumpsuit & Gold Hoops", "image": images["clean"], "notes": "Slate grey zip activewear jumpsuit paired with gold jewelry and a sleek bun.", "colors": ["#808080", "#D4AF37", "#FFFFFF", "#1A1817"]}
    ]
}

# 2. Style Movements (5 boards, 5 cards each = 25 cards)
movements_raw = {
    "Avant-Garde / Darkwear": [
        {"title": "Draped Black Wool Silhouette", "image": images["minimalist"], "notes": "Asymmetric black wool draped coat combined with black wide-leg pleated trousers.", "colors": ["#111111", "#CCCCCC", "#1F1F1F", "#FFFFFF"]},
        {"title": "Asymmetrical Pleated Trench", "image": images["minimalist"], "notes": "A structural deconstructed black trench coat featuring an asymmetric pleated hem.", "colors": ["#0D0D0D", "#1F1F1F", "#808080", "#FFFFFF"]},
        {"title": "Architectural Layered Poncho", "image": images["minimalist"], "notes": "Layered heavy black wool poncho styled with raw silver rings and black combat boots.", "colors": ["#0D0D0D", "#CCCCCC", "#1A1A1A", "#808080"]},
        {"title": "Deconstructed Cowl-Neck Coat", "image": images["minimalist"], "notes": "Heavy charcoal cowl-neck deconstructed coat featuring asymmetric zipper detailing.", "colors": ["#555555", "#0D0D0D", "#CCCCCC", "#1F1F1F"]},
        {"title": "Avant-Garde Oversized Dark Vest", "image": images["minimalist"], "notes": "Oversized black cotton vest styled with draped asymmetric layers and raw hem pants.", "colors": ["#0D0D0D", "#1F1F1F", "#CCCCCC", "#808080"]}
    ],
    "Matrixcore / Neo-Noir": [
        {"title": "Patent Leather Long Trench Coat", "image": images["office"], "notes": "Shiny black leather trench coat styled over a grey knit and burgundy trousers.", "colors": ["#0D0D0D", "#808080", "#800020", "#1F1F1F"]},
        {"title": "Matrix Neo-Noir High Neck Top", "image": images["office"], "notes": "High-neck black ribbed bodysuit paired with a long leather duster and micro shades.", "colors": ["#0D0D0D", "#1F1F1F", "#CCCCCC", "#808080"]},
        {"title": "Sleek All-Black Utility Blazer", "image": images["office"], "notes": "Tailored black leather blazer styled with slim black trousers and high-shine boots.", "colors": ["#0D0D0D", "#1F1F1F", "#1A1A1A", "#FFFFFF"]},
        {"title": "Neo-Noir Leather Ankle Boots Styling", "image": images["office"], "notes": "High-waisted black vinyl trousers styled with a mock-neck and square-toe leather boots.", "colors": ["#0D0D0D", "#111111", "#CCCCCC", "#808080"]},
        {"title": "High-Shine Asymmetrical Dress", "image": images["office"], "notes": "Asymmetrical black satin midi dress styled under a structured leather blazer.", "colors": ["#0D0D0D", "#1A1A1A", "#CCCCCC", "#FFFFFF"]}
    ],
    "Corporate Minimalist": [
        {"title": "Structured Grey Tailored Suit", "image": images["office"], "notes": "Tailored grey blazer paired with structured grey trousers and a burgundy bag.", "colors": ["#808080", "#800020", "#FFFFFF", "#2B2B2B"]},
        {"title": "Corporate Minimalist Silk Tee", "image": images["office"], "notes": "Off-white silk tee tucked into structured navy blue high-waisted work trousers.", "colors": ["#FFFFFF", "#0B1D3A", "#EAE6DF", "#CCCCCC"]},
        {"title": "Slim Fit Double-Breasted Blazer", "image": images["office"], "notes": "Sleek charcoal grey double-breasted suit blazer worn over a crisp white shirt.", "colors": ["#555555", "#FFFFFF", "#0D0D0D", "#CCCCCC"]},
        {"title": "Tailored Pencil Skirt & Loafers", "image": images["office"], "notes": "Structured navy wool pencil skirt styled with a tailored grey cotton shirt and loafers.", "colors": ["#0B1D3A", "#808080", "#FFFFFF", "#1A1817"]},
        {"title": "Neutral Clean Linen Trousers", "image": images["office"], "notes": "Tailored grey linen trousers paired with a minimal mock-neck cream knit vest.", "colors": ["#808080", "#FFFDD0", "#EAE6DF", "#1A1817"]}
    ],
    "Oatmeal / Vanilla Girl": [
        {"title": "Cream Cable Cashmere Set", "image": images["capsule"], "notes": "Oatmeal-colored ribbed cashmere knit pants paired with a cream crewneck sweater.", "colors": ["#FFFDD0", "#E1D9D1", "#E6E6FA", "#C2B280"]},
        {"title": "Teddy Fleece Soft Lounge Coat", "image": images["capsule"], "notes": "Fluffy cream teddy-fleece coat layered over oatmeal ribbed knit lounge trousers.", "colors": ["#FFFDD0", "#C2B280", "#EAE6DF", "#FFFFFF"]},
        {"title": "Ribbed Oatmeal Knit Loungewear", "image": images["capsule"], "notes": "Oatmeal knit lounge set styled with a soft vanilla silk hair scrunchie.", "colors": ["#E1D9D1", "#FFFDD0", "#EAE6DF", "#8B5A2B"]},
        {"title": "Vanilla Bean Cozy Scarf Layering", "image": images["capsule"], "notes": "Oversized chunky knit vanilla-colored wool scarf paired with a beige trench coat.", "colors": ["#FFFDD0", "#C2B280", "#EAE6DF", "#8B5A2B"]},
        {"title": "Oatmeal Cropped Knit Sweater", "image": images["capsule"], "notes": "Ribbed oatmeal cropped sweater paired with off-white linen wide-leg trousers.", "colors": ["#E1D9D1", "#FFFFFF", "#FFFDD0", "#CCCCCC"]}
    ],
    "Dopamine Monochrome": [
        {"title": "Hot Pink Double-Breasted Suit", "image": images["barbie"], "notes": "Vibrant hot pink matching trousers and double-breasted suit blazer.", "colors": ["#FF1493", "#FF69B4", "#FFFFFF", "#FF0000"]},
        {"title": "Vibrant Royal Blue Trench Look", "image": images["barbie"], "notes": "Royal blue monochrome trench coat styled over matching blue trousers and white sneakers.", "colors": ["#4169E1", "#FFFFFF", "#CCCCCC", "#1A1A1A"]},
        {"title": "Saturated Red Monochrome Knit", "image": images["barbie"], "notes": "Bright red oversized cable-knit sweater paired with red denim jeans and boots.", "colors": ["#FF0000", "#0D0D0D", "#CCCCCC", "#FFFFFF"]},
        {"title": "Dopamine Yellow Utility Coord", "image": images["barbie"], "notes": "Sunny yellow utility vest paired with matching yellow cargo utility pants.", "colors": ["#FFD700", "#FFFFFF", "#CCCCCC", "#1A1A1A"]},
        {"title": "Monochrome Forest Green Overcoat", "image": images["barbie"], "notes": "Rich forest green wool overcoat worn over a matching emerald green rib sweater.", "colors": ["#2E8B57", "#FFFDD0", "#CCCCCC", "#1F1F1F"]}
    ]
}

# 3. Occasions (10 boards, 6 cards each = 60 cards)
occasions_raw = {
    "Concerts & Festivals": [
        {"title": "Festival Mesh Top & Cargo Pants", "image": images["y2k"], "notes": "Neon printed mesh top worn with low-rise cargo pants and metallic hair clips.", "colors": ["#FF1493", "#4B6F96", "#CCCCCC", "#FFFFFF"]},
        {"title": "Retro Graphic Tee & Denim Shorts", "image": images["y2k"], "notes": "Faded graphic tee tucked into ripped denim shorts with a pink studded belt.", "colors": ["#FFC0CB", "#4B6F96", "#FF0000", "#0D0D0D"]},
        {"title": "Fringe Suede Festival Vest", "image": images["cottagecore"], "notes": "Fringe camel suede vest over crochet top and high-waisted denim shorts.", "colors": ["#C2B280", "#FFFDD0", "#8B5A2B", "#40E0D0"]},
        {"title": "Silver Sequin Concert Skirt", "image": images["y2k"], "notes": "Metallic silver sequined mini skirt styled with an oversized black graphic band tee.", "colors": ["#C0C0C0", "#0D0D0D", "#FFFFFF", "#808080"]},
        {"title": "Neon Cargo Utility Concert Fit", "image": images["streetwear"], "notes": "Black nylon utility cargos paired with a neon pink mesh long-sleeve crop tee.", "colors": ["#FF1493", "#0D0D0D", "#1F1F1F", "#CCCCCC"]},
        {"title": "Distressed Knit & Combat Boots", "image": images["winter"], "notes": "Distressed red knit oversized sweater over cargo shorts and combat boots.", "colors": ["#FF0000", "#0D0D0D", "#808080", "#FFFFFF"]}
    ],
    "All White Soirées": [
        {"title": "White Linen Garden Party Suit", "image": images["summer"], "notes": "Crisp white linen blazer paired with matching wide-leg white linen trousers.", "colors": ["#FFFFFF", "#FFFDD0", "#EAE6DF", "#D4AF37"]},
        {"title": "Ethereal White Satin Maxi Dress", "image": images["summer"], "notes": "Elegant white satin maxi dress styled with gold droplet earrings and heels.", "colors": ["#FFFFFF", "#D4AF37", "#FFFDD0", "#EAE6DF"]},
        {"title": "White Crochet Lace Sundress", "image": images["summer"], "notes": "Delicate white crochet knit sundress styled with a woven straw tote bag.", "colors": ["#FFFFFF", "#8B5A2B", "#FFFDD0", "#EAE6DF"]},
        {"title": "All White Silk Halter & Slacks", "image": images["summer"], "notes": "White silk halter crop top paired with high-waisted white pleated trousers.", "colors": ["#FFFFFF", "#EAE6DF", "#CCCCCC", "#1A1817"]},
        {"title": "Ivory Linen Ruffled Jumpsuit", "image": images["summer"], "notes": "Warm ivory linen jumpsuit featuring ruffle straps and a relaxed wide-leg cut.", "colors": ["#FFFDD0", "#FFFFFF", "#EAE6DF", "#C2B280"]},
        {"title": "Pristine White Summer Blazer Set", "image": images["summer"], "notes": "Pristine white linen shorts paired with a matching structured linen blazer.", "colors": ["#FFFFFF", "#EAE6DF", "#C0C0C0", "#111111"]}
    ],
    "All Black Nights": [
        {"title": "All Black Leather Moto & Denim", "image": images["office"], "notes": "Black leather moto jacket layered over a black tee and washed black jeans.", "colors": ["#0D0D0D", "#1A1A1A", "#808080", "#CCCCCC"]},
        {"title": "Black Satin Backless Slip Dress", "image": images["office"], "notes": "Sleek backless mock-neck black midi dress paired with high black stilettos.", "colors": ["#0D0D0D", "#1F1F1F", "#D4AF37", "#FFFFFF"]},
        {"title": "Black Lace Bustier & Trousers", "image": images["office"], "notes": "Black lace trim corset bustier paired with black tailored suit trousers.", "colors": ["#0D0D0D", "#1F1F1F", "#FFFFFF", "#CCCCCC"]},
        {"title": "All Black Tailored Velvet Blazer", "image": images["office"], "notes": "Double-breasted black velvet blazer styled with black wide-leg silk pants.", "colors": ["#0D0D0D", "#1A1A1A", "#808080", "#FFFFFF"]},
        {"title": "Sheer Mesh Top & Black Leather Skirt", "image": images["office"], "notes": "Black sheer mesh long-sleeve top paired with a black leather mini skirt.", "colors": ["#0D0D0D", "#1F1F1F", "#CCCCCC", "#111111"]},
        {"title": "Black Asymmetric Draped Maxi Outfit", "image": images["office"], "notes": "Draped black asymmetric knit maxi dress paired with heavy platform boots.", "colors": ["#0D0D0D", "#1F1F1F", "#808080", "#FFFFFF"]}
    ],
    "Europe Trip Capsule Wardrobe": [
        {"title": "Europe Capsule Beige Trench Coat", "image": images["capsule"], "notes": "High-quality beige trench coat worn over a striped Breton tee and denim.", "colors": ["#C2B280", "#0B1D3A", "#FFFFFF", "#0D0D0D"]},
        {"title": "Striped Linen Button-Down & Shorts", "image": images["capsule"], "notes": "Light blue and white striped linen shirt paired with clean white shorts.", "colors": ["#ADD8E6", "#FFFFFF", "#CCCCCC", "#E1D9D1"]},
        {"title": "Cozy Travel Knit & Slip Dress", "image": images["capsule"], "notes": "Oatmeal knit pullover sweater layered over a silk midi slip dress.", "colors": ["#E1D9D1", "#FFFDD0", "#CCCCCC", "#8B5A2B"]},
        {"title": "Europe Capsule Walking Loafers Look", "image": images["capsule"], "notes": "Tailored camel trench styled with white linen pants and walk-friendly loafers.", "colors": ["#C2B280", "#FFFFFF", "#FFFDD0", "#5C4033"]},
        {"title": "White Cotton Dress & Straw Tote", "image": images["capsule"], "notes": "Breezy white cotton midi dress styled with a woven straw tote and leather slides.", "colors": ["#FFFFFF", "#8B5A2B", "#FFFDD0", "#D2B48C"]},
        {"title": "Travel Capsule Cashmere Wrap Knit", "image": images["capsule"], "notes": "Warm ivory cashmere wrap cardigan styled with beige wide-leg knit trousers.", "colors": ["#FFFDD0", "#C2B280", "#EAE6DF", "#FFFFFF"]}
    ],
    "Graduation Looks": [
        {"title": "Graduation Prep Tweed Crest Dress", "image": images["old_money"], "notes": "Classic navy structured tweed dress with white collar piping and pearl detail.", "colors": ["#0B1D3A", "#FFFFFF", "#D4AF37", "#CCCCCC"]},
        {"title": "Tailored Pastel Suit Coordination", "image": images["old_money"], "notes": "A pale pink tailored blazer paired with matching pink suit trousers.", "colors": ["#FFC0CB", "#FFFFFF", "#FFF0F5", "#CCCCCC"]},
        {"title": "White Lace Graduation Midi Dress", "image": images["old_money"], "notes": "Elegant white floral lace midi dress featuring scallop hem and block heels.", "colors": ["#FFFFFF", "#EAE6DF", "#CCCCCC", "#D4AF37"]},
        {"title": "Smart Navy Double-Breasted Blazer", "image": images["old_money"], "notes": "Navy blue crest blazer styled with white tailored linen trousers.", "colors": ["#0B1D3A", "#FFFFFF", "#D4AF37", "#D2B48C"]},
        {"title": "Elegantly Draped Silk Blouse & Slacks", "image": images["old_money"], "notes": "Cream silk cowl-neck blouse tucked into navy high-waisted trousers.", "colors": ["#FFFDD0", "#0B1D3A", "#FFFFFF", "#CCCCCC"]},
        {"title": "Polished Wrap Dress & Block Heels", "image": images["old_money"], "notes": "Tailored sage green wrap dress styled with low nude block heels.", "colors": ["#8FBC8F", "#D2B48C", "#FFFFFF", "#FFFDD0"]}
    ],
    "Birthday Milestone Looks": [
        {"title": "Birthday Dinner Glam", "image": images["summer"], "notes": "A show-stopping silk slip dress styled with gold drop earrings for birthday dinner.", "colors": ["#FFFFFF", "#FFFDD0", "#D4AF37", "#1A1817"]},
        {"title": "Rooftop Party Look", "image": images["barbie"], "notes": "A vibrant hot pink matching trouser and blazer set to command the rooftop party.", "colors": ["#FF1493", "#FF69B4", "#FFFFFF", "#FF0000"]},
        {"title": "Pink Birthday Dress", "image": images["coquette"], "notes": "Pale pink ruffle tulle party dress with red velvet shoulder bows.", "colors": ["#FFC0CB", "#FF0000", "#FFF0F5", "#FFFFFF"]},
        {"title": "Red Main Character Outfit", "image": images["barbie"], "notes": "Saturated red double-breasted blazer dress with statement silver hardware.", "colors": ["#FF0000", "#CCCCCC", "#0D0D0D", "#FFFFFF"]},
        {"title": "Black Club Night Look", "image": images["office"], "notes": "Asymmetric neck black midi dress paired with high-shine silver heels.", "colors": ["#0D0D0D", "#CCCCCC", "#1A1A1A", "#FFFFFF"]},
        {"title": "Birthday Brunch Outfit", "image": images["clean"], "notes": "White linen button-down paired with a pastel pink knit vest and gold hoops.", "colors": ["#FFFFFF", "#FFC0CB", "#D4AF37", "#1A1817"]}
    ],
    "High-End Date Nights": [
        {"title": "Date Night Silk Slip & Blazer", "image": images["old_money"], "notes": "Rich burgundy silk slip dress styled under a warm cream oversized blazer.", "colors": ["#800020", "#FFFDD0", "#D4AF37", "#1A1817"]},
        {"title": "Backless Satin Midi Dress Look", "image": images["office"], "notes": "Mock-neck backless black midi dress paired with beige leather slingbacks.", "colors": ["#0D0D0D", "#D2B48C", "#D4AF37", "#1F1F1F"]},
        {"title": "Tailored Velvet Tuxedo Blazer", "image": images["office"], "notes": "Deep navy velvet tuxedo blazer worn over a silk camisole and slim trousers.", "colors": ["#0B1D3A", "#FFFFFF", "#0D0D0D", "#CCCCCC"]},
        {"title": "Off-Shoulder Knit & Leather Skirt", "image": images["office"], "notes": "Cream off-shoulder ribbed knit top paired with a black leather midi skirt.", "colors": ["#FFFDD0", "#0D0D0D", "#8B5A2B", "#CCCCCC"]},
        {"title": "High-End Date Night Sheer Dress", "image": images["dark_academia"], "notes": "Deep burgundy velvet dress featuring sheer bell sleeves and cream heels.", "colors": ["#800020", "#FFFDD0", "#3A0033", "#1A1A1A"]},
        {"title": "Elevated Wool Coat & Slingbacks", "image": images["minimalist"], "notes": "Tailored camel wool coat styled over an all-black silk slip dress.", "colors": ["#C2B280", "#0D0D0D", "#D4AF37", "#FFFFFF"]}
    ],
    "Instagram Content Creation": [
        {"title": "Bratz Fashion Denim Midi Skirt", "image": images["bratz"], "notes": "Distressed denim midi skirt paired with a red crop top and pink sandals.", "colors": ["#FF0000", "#FFC0CB", "#4B6F96", "#0D0D0D"]},
        {"title": "Color Block Cropped Knit Cardigan", "image": images["coquette"], "notes": "Lavender crop cardigan styled with cream slip skirt and lavender ribbons.", "colors": ["#E6E6FA", "#FFFDD0", "#D4AF37", "#9370DB"]},
        {"title": "Asymmetric Wrap Top Content Look", "image": images["clean"], "notes": "Sleek asymmetry wrap top paired with white trousers and statement shades.", "colors": ["#111111", "#FFFFFF", "#CCCCCC", "#808080"]},
        {"title": "Bold Graphic Blazer & Chunky Boots", "image": images["streetwear"], "notes": "Oversized graphic blazer worn over biker shorts and chunky silver trainers.", "colors": ["#0D0D0D", "#808080", "#CCCCCC", "#FFFFFF"]},
        {"title": "Instagram Content Ribbon Bow Hair Set", "image": images["coquette"], "notes": "Pale pink wrap top paired with a cream slip skirt and green velvet bow.", "colors": ["#FFC0CB", "#FFFDD0", "#8FBC8F", "#FDF2F8"]},
        {"title": "Contrast Stitch Utility Cargo Jogger", "image": images["streetwear"], "notes": "Black cargos featuring white contrast stitching, paired with utility crop tee.", "colors": ["#0D0D0D", "#FFFFFF", "#CCCCCC", "#1A1A1A"]}
    ],
    "Cozy Cafe Dates": [
        {"title": "Cafe Dates Tweed Oversized Blazer", "image": images["dark_academia"], "notes": "Chocolate brown wool blazer worn over a cream knit and pleated trousers.", "colors": ["#5C4033", "#F5F5DC", "#2B2B2B", "#CCCCCC"]},
        {"title": "Chocolate Herringbone Wool Coat", "image": images["dark_academia"], "notes": "Chocolate brown herringbone coat paired with a cream turtleneck sweater.", "colors": ["#5C4033", "#F5F5DC", "#8B5A2B", "#FFFFFF"]},
        {"title": "Cable Knit Cozy Turtle Vest", "image": images["dark_academia"], "notes": "Cream knit cable vest over blue Oxford shirt, corduroy slacks.", "colors": ["#FFFDD0", "#ADD8E6", "#5C4033", "#D4AF37"]},
        {"title": "Cafe Dates Ribbed Cardigan & Skirt", "image": images["coquette"], "notes": "Lavender ribbed cardigan paired with a cream slip skirt and hair ribbons.", "colors": ["#E6E6FA", "#FFFDD0", "#D4AF37", "#9370DB"]},
        {"title": "Chunky Oatmeal Scarf Coffee Look", "image": images["capsule"], "notes": "Chunky oatmeal wool scarf layered over a beige trench coat and tan trousers.", "colors": ["#E1D9D1", "#C2B280", "#FFFDD0", "#8B5A2B"]},
        {"title": "Corduroy Pants Vintage Cozy Fit", "image": images["coastal"], "notes": "Vintage brown wool vest over blue shirt, corduroy trousers.", "colors": ["#5C4033", "#F5F5DC", "#ADD8E6", "#2E8B57"]}
    ],
    "College Daily Wear": [
        {"title": "Oversized College Crewneck Hoodie", "image": images["streetwear"], "notes": "Oversized black graphic hoodie paired with loose utility cargos and sneakers.", "colors": ["#0D0D0D", "#CCCCCC", "#555555", "#FFFFFF"]},
        {"title": "Baggy Denim Jeans Daily Wear", "image": images["streetwear"], "notes": "Grey graphic crewneck sweater paired with black biker shorts and silver sneakers.", "colors": ["#808080", "#0D0D0D", "#CCCCCC", "#FFFFFF"]},
        {"title": "Preppy Knit Polo & Pleated Skirt", "image": images["old_money"], "notes": "Navy cable-knit vest over white oxford shirt, pleated cargo shorts.", "colors": ["#0B1D3A", "#FFFFFF", "#D2B48C", "#CCCCCC"]},
        {"title": "College Cargo Pants Everyday Style", "image": images["streetwear"], "notes": "Olive green technical fleece jacket paired with tan ripstop utility cargos.", "colors": ["#8FBC8F", "#D2B48C", "#0B1D3A", "#F0F0F0"]},
        {"title": "Flannel Shirt Denim Jacket Layering", "image": images["dark_academia"], "notes": "Burgundy and cream flannel shirt styled open over a black graphic tee.", "colors": ["#800020", "#FFFDD0", "#0D0D0D", "#808080"]},
        {"title": "Casual Varsity Jacket & Sneakers", "image": images["streetwear"], "notes": "Varsity jacket in forest green and white styled with loose light-wash jeans.", "colors": ["#2E8B57", "#FFFFFF", "#4B6F96", "#1A1A1A"]}
    ]
}

# 4. Color Stories (15 boards, 6 cards each = 90 cards)
color_stories_raw = {
    "Black": [
        {"title": "Black Silk Halter Slip Dress", "image": images["office"], "notes": "A minimal black silk halter neck slip dress paired with black strappy heels.", "colors": ["#0D0D0D", "#1A1A1A", "#FFFFFF", "#CCCCCC"]},
        {"title": "Black Leather Biker Outerwear", "image": images["office"], "notes": "A black leather moto jacket thrown over a black rib knit crop top.", "colors": ["#0D0D0D", "#1F1F1F", "#CCCCCC", "#808080"]},
        {"title": "Black Structured Wool Overcoat", "image": images["office"], "notes": "Double-breasted black wool overcoat paired with black trousers and leather boots.", "colors": ["#0D0D0D", "#111111", "#808080", "#FFFFFF"]},
        {"title": "Black Ribbed Cashmere Turtleneck", "image": images["office"], "notes": "A cozy black ribbed cashmere turtleneck knit styled with black leather pants.", "colors": ["#0D0D0D", "#1F1F1F", "#808080", "#FFFFFF"]},
        {"title": "Black Asymmetric Pleated Skirt", "image": images["office"], "notes": "Deconstructed black pleated wool skirt styled with a draped black knit wrap.", "colors": ["#0D0D0D", "#1F1F1F", "#CCCCCC", "#808080"]},
        {"title": "Black Tailored Minimalist Suit", "image": images["office"], "notes": "Structured black suit blazer paired with matching wide-leg tailored trousers.", "colors": ["#0D0D0D", "#1A1A1A", "#FFFFFF", "#CCCCCC"]}
    ],
    "White": [
        {"title": "White Linen Summer Sundress", "image": images["summer"], "notes": "Crisp white linen sundress featuring puff sleeves and tiered skirt paneling.", "colors": ["#FFFFFF", "#FFFDD0", "#EAE6DF", "#8B5A2B"]},
        {"title": "White Ribbed Knit Wide Leg Set", "image": images["summer"], "notes": "Cozy white ribbed knit crewneck paired with matching white knit wide-leg pants.", "colors": ["#FFFFFF", "#EAE6DF", "#CCCCCC", "#E1D9D1"]},
        {"title": "White Tailored Crest Blazer", "image": images["summer"], "notes": "Structured white double-breasted blazer styled with white tailored linen shorts.", "colors": ["#FFFFFF", "#EAE6DF", "#C0C0C0", "#111111"]},
        {"title": "White Satin Halter Neck Top", "image": images["summer"], "notes": "Smooth white satin halter neck top tucked into white pleated trousers.", "colors": ["#FFFFFF", "#EAE6DF", "#CCCCCC", "#1A1817"]},
        {"title": "White Eyelet Cotton Maxi Skirt", "image": images["summer"], "notes": "White cotton eyelet maxi skirt paired with white crop knit tank top.", "colors": ["#FFFFFF", "#FFFDD0", "#EAE6DF", "#CCCCCC"]},
        {"title": "White Silk Slip Dress & Gold", "image": images["summer"], "notes": "White silk cowl-neck slip dress styled with gold droplet earrings.", "colors": ["#FFFFFF", "#FFFDD0", "#D4AF37", "#EAE6DF"]}
    ],
    "Cream / Ivory": [
        {"title": "Cream Cable Cashmere Knitwear", "image": images["capsule"], "notes": "Rich cream cable knit sweater layered over an ivory silk midi slip skirt.", "colors": ["#FFFDD0", "#E1D9D1", "#E6E6FA", "#C2B280"]},
        {"title": "Ivory Crochet Fringe Maxi Dress", "image": images["cottagecore"], "notes": "Ivory crochet knit maxi dress featuring fringe trim and a tiered skirt.", "colors": ["#FFFDD0", "#C2B280", "#FFD700", "#FFFFFF"]},
        {"title": "Cream Linen Wide Leg Trousers", "image": images["minimalist"], "notes": "Cream wide-leg linen pants styled with a neutral beige mock-neck top.", "colors": ["#FFFDD0", "#EAE6DF", "#C2B280", "#1A1817"]},
        {"title": "Ivory Tailored Double Trench", "image": images["minimalist"], "notes": "Ivory double-breasted trench coat layered over off-white tailored slacks.", "colors": ["#FFFDD0", "#EAE6DF", "#CCCCCC", "#1A1817"]},
        {"title": "Cream Gingham Puffed Sleeve Dress", "image": images["cottagecore"], "notes": "Romantic cream and sage green gingham dress with puffed sleeve details.", "colors": ["#FFFDD0", "#8FBC8F", "#FFFFFF", "#D2B48C"]},
        {"title": "Ivory Silk Wrap Midi Skirt", "image": images["minimalist"], "notes": "Ivory silk midi skirt paired with an off-white ribbed cashmere knit.", "colors": ["#FFFDD0", "#EAE6DF", "#CCCCCC", "#1A1817"]}
    ],
    "Beige / Tan": [
        {"title": "Beige Tailored Pleated Pants", "image": images["minimalist"], "notes": "Sleek beige high-waisted tailored pants styled with a minimal cream top.", "colors": ["#D2B48C", "#FFFDD0", "#E1D9D1", "#1A1817"]},
        {"title": "Tan Herringbone Wool Overcoat", "image": images["dark_academia"], "notes": "Tan herringbone wool coat layered over chocolate brown ribbed trousers.", "colors": ["#C2B280", "#5C4033", "#FFFFFF", "#CCCCCC"]},
        {"title": "Beige Knit Crewneck Cozy Sweater", "image": images["capsule"], "notes": "Cozy beige crewneck wool sweater paired with cream wide-leg linen pants.", "colors": ["#C2B280", "#FFFDD0", "#EAE6DF", "#8B5A2B"]},
        {"title": "Tan Suede Fringe Outer Jacket", "image": images["cottagecore"], "notes": "A fringe camel suede jacket styled over an ivory crochet knit top.", "colors": ["#C2B280", "#FFFDD0", "#8B5A2B", "#40E0D0"]},
        {"title": "Beige Corduroy Blazer Classic", "image": images["coastal"], "notes": "Classic tan corduroy blazer styled with a sky blue cotton polo shirt.", "colors": ["#C2B280", "#ADD8E6", "#5C4033", "#FFFDD0"]},
        {"title": "Tan Linen Button-Down Shirt", "image": images["capsule"], "notes": "Relaxed tan linen button-down shirt paired with off-white linen shorts.", "colors": ["#C2B280", "#FFFFFF", "#EAE6DF", "#8B5A2B"]}
    ],
    "Brown": [
        {"title": "Chocolate Brown Wool Trench", "image": images["dark_academia"], "notes": "Rich chocolate brown wool trench coat layered over an ivory mock-neck.", "colors": ["#5C4033", "#FFFDD0", "#8B5A2B", "#0D0D0D"]},
        {"title": "Brown Ribbed Knit Polo Sweater", "image": images["coastal"], "notes": "Chocolate brown ribbed polo sweater paired with beige pleated trousers.", "colors": ["#5C4033", "#F5F5DC", "#8B5A2B", "#C2B280"]},
        {"title": "Dark Brown Leather Moto Jacket", "image": images["dark_academia"], "notes": "Vintage dark brown leather moto jacket worn over a faded grey band tee.", "colors": ["#5C4033", "#808080", "#0D0D0D", "#CCCCCC"]},
        {"title": "Brown Corduroy Wide Leg Pants", "image": images["coastal"], "notes": "Earthy brown corduroy wide-leg pants styled with a cream cable vest.", "colors": ["#5C4033", "#FFFDD0", "#ADD8E6", "#2E8B57"]},
        {"title": "Chocolate Cashmere Turtleneck", "image": images["dark_academia"], "notes": "Cozy chocolate brown cashmere turtleneck sweater styled with grey slacks.", "colors": ["#5C4033", "#808080", "#FFFFFF", "#1A1A1A"]},
        {"title": "Brown Vintage Cable Knit Vest", "image": images["coastal"], "notes": "Vintage brown wool cable-knit vest layered over a blue denim shirt.", "colors": ["#5C4033", "#ADD8E6", "#FFFDD0", "#D4AF37"]}
    ],
    "Gray": [
        {"title": "Grey Tailored Double-Breasted Suit", "image": images["office"], "notes": "Sleek tailored grey suit blazer and matching grey trousers.", "colors": ["#808080", "#FFFFFF", "#1A1A1A", "#CCCCCC"]},
        {"title": "Charcoal Oversized Crewneck Knit", "image": images["streetwear"], "notes": "Oversized charcoal grey crewneck knit paired with black biker shorts.", "colors": ["#808080", "#0D0D0D", "#CCCCCC", "#FFFFFF"]},
        {"title": "Slate Grey Pleated Mini Skirt", "image": images["dark_academia"], "notes": "Charcoal grey checked wool pleated skirt paired with a black mock-neck.", "colors": ["#808080", "#0D0D0D", "#FFFDD0", "#CCCCCC"]},
        {"title": "Grey Cashmere Wrap Cardigan", "image": images["capsule"], "notes": "Slate grey cashmere wrap cardigan paired with off-white ribbed pants.", "colors": ["#808080", "#FFFFFF", "#EAE6DF", "#CCCCCC"]},
        {"title": "Charcoal Denim Distressed Jacket", "image": images["streetwear"], "notes": "Distressed charcoal denim jacket styled with black cargo pants and chains.", "colors": ["#808080", "#0D0D0D", "#CCCCCC", "#1F1F1F"]},
        {"title": "Grey Wool Trench Coat Tailoring", "image": images["office"], "notes": "Grey structured wool trench coat layered over a black silk camisole.", "colors": ["#808080", "#0D0D0D", "#FFFFFF", "#CCCCCC"]}
    ],
    "Navy": [
        {"title": "Navy Crest Double Blazer", "image": images["old_money"], "notes": "Double-breasted navy blazer featuring gold crest buttons and white linen.", "colors": ["#0B1D3A", "#FFFFFF", "#D4AF37", "#D2B48C"]},
        {"title": "Navy Cable-Knit Preppy Vest", "image": images["old_money"], "notes": "Navy blue cable-knit vest layered over a crisp white oxford shirt.", "colors": ["#0B1D3A", "#FFFFFF", "#D2B48C", "#CCCCCC"]},
        {"title": "Navy Tweed Pleated A-Line Dress", "image": images["old_money"], "notes": "Navy tweed pleated dress featuring pearl button embellishments.", "colors": ["#0B1D3A", "#FFFFFF", "#CCCCCC", "#FFF0F5"]},
        {"title": "Navy Silk Slip Dress Styling", "image": images["old_money"], "notes": "Luxe navy blue silk midi slip dress styled with a white linen wrap.", "colors": ["#0B1D3A", "#FFFFFF", "#CCCCCC", "#EAE6DF"]},
        {"title": "Navy Striped Sailor Linen Knit", "image": images["old_money"], "notes": "Navy and white striped knit crewneck sweater styled with white shorts.", "colors": ["#0B1D3A", "#FFFFFF", "#CCCCCC", "#E1D9D1"]},
        {"title": "Navy Ribbed Wool Turtleneck", "image": images["old_money"], "notes": "Deep navy ribbed wool turtleneck knit styled with camel wool trousers.", "colors": ["#0B1D3A", "#C2B280", "#5C4033", "#FFFFFF"]}
    ],
    "Olive / Sage": [
        {"title": "Sage Green Gingham Cotton Dress", "image": images["cottagecore"], "notes": "Calming sage green and cream gingham print puffed sleeve maxi dress.", "colors": ["#8FBC8F", "#FFFDD0", "#8B5A2B", "#FFFFFF"]},
        {"title": "Olive Technical Waterproof Shell", "image": images["streetwear"], "notes": "Water-resistant olive technical shell jacket paired with black utility ripstop.", "colors": ["#556B2F", "#0D0D0D", "#CCCCCC", "#1F1F1F"]},
        {"title": "Sage Knit Wrap Top Ballet Style", "image": images["coquette"], "notes": "Sage green wrap top paired with cream slip skirt and sage ribbon bow.", "colors": ["#8FBC8F", "#FFFDD0", "#FFC0CB", "#FFFFFF"]},
        {"title": "Olive Ripstop Utility Cargo Pants", "image": images["streetwear"], "notes": "Olive green ripstop utility cargos paired with a black graphic tee.", "colors": ["#556B2F", "#0D0D0D", "#808080", "#FFFFFF"]},
        {"title": "Sage Wool Overcoat Cozy Layering", "image": images["winter"], "notes": "Sage green technical fleece jacket paired with tan nylon utility trousers.", "colors": ["#8FBC8F", "#D2B48C", "#0B1D3A", "#F0F0F0"]},
        {"title": "Olive Satin Slip Midi Skirt", "image": images["office"], "notes": "Olive green satin midi slip skirt styled with a cream rib-knit top.", "colors": ["#556B2F", "#FFFDD0", "#CCCCCC", "#1A1A1A"]}
    ],
    "Burgundy": [
        {"title": "Burgundy Date Night", "image": images["old_money"], "notes": "A rich burgundy silk slip dress paired with a warm cream oversized blazer and gold drop earrings.", "colors": ["#800020", "#FFFDD0", "#D4AF37", "#1A1817"]},
        {"title": "Burgundy Monochrome Knitwear", "image": images["winter"], "notes": "Cosy burgundy chunky knit sweater paired with matching burgundy tailored trousers.", "colors": ["#800020", "#1A1817", "#808080", "#CCCCCC"]},
        {"title": "Burgundy Office Chic", "image": images["office"], "notes": "Burgundy tailored blazer paired with a charcoal grey knit and burgundy slacks.", "colors": ["#800020", "#808080", "#FFFFFF", "#1F1F1F"]},
        {"title": "Burgundy Streetwear", "image": images["streetwear"], "notes": "Burgundy graphic hoodie paired with faded black cargo pants and chunky sneakers.", "colors": ["#800020", "#0D0D0D", "#CCCCCC", "#FFFFFF"]},
        {"title": "Burgundy Winter Layering", "image": images["winter"], "notes": "Oversized burgundy wool coat paired with dark grey pants and oxfords.", "colors": ["#800020", "#808080", "#FFFFFF", "#0D0D0D"]},
        {"title": "Burgundy Old Money", "image": images["old_money"], "notes": "Elegant burgundy cable-knit crewneck sweater styled with white trousers.", "colors": ["#800020", "#FFFFFF", "#D2B48C", "#CCCCCC"]}
    ],
    "Light Blue": [
        {"title": "Light Blue Oxford Cotton Shirt", "image": images["clean"], "notes": "Oversized sky blue Oxford cotton shirt styled with camel wool pants.", "colors": ["#ADD8E6", "#C2B280", "#5C4033", "#FFFFFF"]},
        {"title": "Sky Blue Cashmere Knit Sweater", "image": images["capsule"], "notes": "Soft sky blue cashmere crewneck sweater paired with white linen pants.", "colors": ["#ADD8E6", "#FFFFFF", "#E1D9D1", "#CCCCCC"]},
        {"title": "Light Blue Striped Linen Set", "image": images["summer"], "notes": "Light blue and white striped linen shirt styled over clean white shorts.", "colors": ["#ADD8E6", "#FFFFFF", "#CCCCCC", "#EAE6DF"]},
        {"title": "Sky Blue Corduroy Grandpa Blazer", "image": images["coastal"], "notes": "Vintage sky blue Oxford shirt layered under a patterned brown vest.", "colors": ["#ADD8E6", "#5C4033", "#FFFDD0", "#D4AF37"]},
        {"title": "Light Blue Denim Midi Skirt", "image": images["bratz"], "notes": "Light blue distressed denim midi skirt styled with a red crop top.", "colors": ["#4B6F96", "#FF0000", "#FFC0CB", "#0D0D0D"]},
        {"title": "Sky Blue Silk Wrap Crop Top", "image": images["summer"], "notes": "Sky blue silk wrap crop top paired with clean white linen midi skirt.", "colors": ["#ADD8E6", "#FFFFFF", "#EAE6DF", "#CCCCCC"]}
    ],
    "Red": [
        {"title": "Vibrant Red Double-Breasted Blazer", "image": images["barbie"], "notes": "Vibrant red matching trouser and double-breasted suit blazer set.", "colors": ["#FF0000", "#FFFFFF", "#CCCCCC", "#1A1A1A"]},
        {"title": "Cherry Red Silk Backless Slip", "image": images["coquette"], "notes": "Cherry red satin slip dress styled with a red velvet ribbon choker.", "colors": ["#FF0000", "#FFC0CB", "#FFF0F5", "#FFFFFF"]},
        {"title": "Red Graphic Crop Tee & Denim", "image": images["bratz"], "notes": "Red crop top styled with distressed denim midi skirt and pink sandals.", "colors": ["#FF0000", "#FFC0CB", "#4B6F96", "#0D0D0D"]},
        {"title": "Red Cable-Knit Crewneck Sweater", "image": images["barbie"], "notes": "Bright red oversized cable-knit sweater paired with washed blue jeans.", "colors": ["#FF0000", "#4B6F96", "#CCCCCC", "#FFFFFF"]},
        {"title": "Vibrant Red Pleated Tennis Skirt", "image": images["barbie"], "notes": "Red pleated mini tennis skirt styled with a white polo and sneakers.", "colors": ["#FF0000", "#FFFFFF", "#CCCCCC", "#111111"]},
        {"title": "Red Leather Moto Cropped Jacket", "image": images["bratz"], "notes": "Cropped red leather moto jacket paired with black low-rise cargos.", "colors": ["#FF0000", "#0D0D0D", "#CCCCCC", "#FFFFFF"]}
    ],
    "Pink": [
        {"title": "Hot Pink Double Tailored Suit", "image": images["barbie"], "notes": "Vibrant hot pink double-breasted suit blazer paired with matching pants.", "colors": ["#FF1493", "#FF69B4", "#FFFFFF", "#FF0000"]},
        {"title": "Baby Pink Velour Zip Tracksuit", "image": images["barbie"], "notes": "Baby pink velour Y2K tracksuit featuring silver rhinestone details.", "colors": ["#FFC0CB", "#FF0000", "#F0F0F0", "#FFFFFF"]},
        {"title": "Soft Pink Cardigan Ribbon Bows", "image": images["coquette"], "notes": "Pale pink cardigan adorned with small red satin bows down the front.", "colors": ["#FFC0CB", "#FF0000", "#FFF0F5", "#FDF2F8"]},
        {"title": "Pale Pink Tulle Birthday Dress", "image": images["coquette"], "notes": "Light pink tulle party dress featuring red velvet shoulder ribbon bows.", "colors": ["#FFC0CB", "#FF0000", "#FFF0F5", "#FFFFFF"]},
        {"title": "Pink Ribbed Wrap Top Knitwear", "image": images["coquette"], "notes": "Pale pink ribbed wrap top paired with a cream linen midi slip skirt.", "colors": ["#FFC0CB", "#FFFDD0", "#8FBC8F", "#FDF2F8"]},
        {"title": "Blush Satin Slip Skirt Outfit", "image": images["coquette"], "notes": "Soft pink slip skirt paired with a pale pink knit crop top.", "colors": ["#FFC0CB", "#FFFDD0", "#FFFFFF", "#EAE6DF"]}
    ],
    "Yellow": [
        {"title": "Bright Mustard Wool Knit Vest", "image": images["coastal"], "notes": "Mustard yellow patterned knit vest layered over a blue Oxford shirt.", "colors": ["#FFD700", "#ADD8E6", "#5C4033", "#F0F0F0"]},
        {"title": "Yellow Linen Summer Resort Set", "image": images["summer"], "notes": "Sunny yellow linen button-down shirt paired with matching yellow shorts.", "colors": ["#FFD700", "#FFFFFF", "#EAE6DF", "#C2B280"]},
        {"title": "Mustard Yellow Cropped Utility Coat", "image": images["y2k"], "notes": "Mustard yellow crop utility jacket paired with Y2K low-rise wide jeans.", "colors": ["#FFD700", "#4B6F96", "#FFC0CB", "#0D0D0D"]},
        {"title": "Sunny Yellow Eyelet Maxi Dress", "image": images["cottagecore"], "notes": "Cheerful yellow cotton eyelet maxi dress styled with a straw bag.", "colors": ["#FFD700", "#FFFFFF", "#FFFDD0", "#D2B48C"]},
        {"title": "Yellow Corduroy Tailored Pants", "image": images["coastal"], "notes": "Yellow corduroy trousers styled with a cream cable-knit vest.", "colors": ["#FFD700", "#FFFDD0", "#5C4033", "#FFFFFF"]},
        {"title": "Yellow Suede Fringe Outerwear", "image": images["cottagecore"], "notes": "A fringe yellow suede jacket layered over an ivory crochet knit top.", "colors": ["#FFD700", "#FFFDD0", "#8B5A2B", "#40E0D0"]}
    ],
    "Royal Blue": [
        {"title": "Royal Blue Tailored Suit Blazer", "image": images["barbie"], "notes": "Tailored royal blue monochrome suit blazer paired with white sneakers.", "colors": ["#4169E1", "#FFFFFF", "#CCCCCC", "#1A1A1A"]},
        {"title": "Royal Blue Monochrome Knit Set", "image": images["barbie"], "notes": "Vibrant royal blue crewneck knit sweater paired with matching knit trousers.", "colors": ["#4169E1", "#FFFFFF", "#CCCCCC", "#1A1A1A"]},
        {"title": "Vibrant Blue Oversized Crewneck", "image": images["streetwear"], "notes": "Oversized royal blue graphic crewneck paired with black cargo pants.", "colors": ["#4169E1", "#0D0D0D", "#CCCCCC", "#FFFFFF"]},
        {"title": "Royal Blue Satin Midi Slip Dress", "image": images["barbie"], "notes": "Sleek royal blue satin slip dress paired with silver strappy heels.", "colors": ["#4169E1", "#CCCCCC", "#FFFFFF", "#111111"]},
        {"title": "Royal Blue Nylon Utility Shell", "image": images["streetwear"], "notes": "Royal blue windproof shell jacket paired with black utility trail cargo pants.", "colors": ["#4169E1", "#0D0D0D", "#CCCCCC", "#1F1F1F"]},
        {"title": "Royal Blue Pleated Trousers Style", "image": images["office"], "notes": "Tailored royal blue high-waisted slacks paired with a tucked white shirt.", "colors": ["#4169E1", "#FFFFFF", "#CCCCCC", "#EAE6DF"]}
    ],
    "Purple": [
        {"title": "Deep Plum Velvet Maxi Skirt", "image": images["dark_academia"], "notes": "A deep plum velvet maxi skirt combined with a black lace top.", "colors": ["#3A0033", "#000000", "#808080", "#800020"]},
        {"title": "Plum Cable-Knit Warm Vest", "image": images["dark_academia"], "notes": "Plum cable knit vest layered over a slate grey collared shirt.", "colors": ["#3A0033", "#808080", "#1A1A1A", "#FFFFFF"]},
        {"title": "Deep Purple Silk Slip Dress", "image": images["dark_academia"], "notes": "Rich plum velvet slip dress with black lace trim and platform heels.", "colors": ["#3A0033", "#000000", "#808080", "#800020"]},
        {"title": "Lavender Knit Cardigan & Ribbon", "image": images["coquette"], "notes": "Lavender knit cardigan paired with a cream slip skirt and lavender ribbons.", "colors": ["#E6E6FA", "#FFFDD0", "#D4AF37", "#9370DB"]},
        {"title": "Plum Velvet Sheer Bell Dress", "image": images["dark_academia"], "notes": "Burgundy velvet dress with dramatic sheer bell sleeves and cream heels.", "colors": ["#800020", "#FFFDD0", "#3A0033", "#1A1A1A"]},
        {"title": "Lavender Linen Summer Sundress", "image": images["summer"], "notes": "Soft lavender linen midi sundress styled with a woven straw hat.", "colors": ["#E6E6FA", "#FFFFFF", "#FFFDD0", "#D2B48C"]}
    ]
}

# 5. Color Combinations (15 boards, 5 cards each = 75 cards, with Black + Beige = 6 cards)
color_combinations_raw = {
    "Black + Beige": [
        {"title": "Black Blazer Beige Trousers", "image": images["minimalist"], "notes": "A structured black double-breasted blazer paired with beige wide-leg tailored trousers.", "colors": ["#0D0D0D", "#D2B48C", "#FFFFFF", "#CCCCCC"]},
        {"title": "Black Dress Camel Coat", "image": images["minimalist"], "notes": "A minimal black mock-neck midi dress layered under a classic camel hair trench coat.", "colors": ["#0D0D0D", "#C2B280", "#D4AF37", "#FFFFFF"]},
        {"title": "Black Hoodie Beige Cargo", "image": images["streetwear"], "notes": "Oversized black graphic hoodie paired with beige ripstop utility cargo pants.", "colors": ["#0D0D0D", "#D2B48C", "#CCCCCC", "#1F1F1F"]},
        {"title": "Black Knit Beige Skirt", "image": images["minimalist"], "notes": "Black ribbed knit mockneck sweater styled with a beige pleated midi skirt.", "colors": ["#0D0D0D", "#D2B48C", "#FFFFFF", "#E1D9D1"]},
        {"title": "Airport Capsule Outfit", "image": images["capsule"], "notes": "Beige fleece-lined utility trousers paired with a black crewneck knit and coat.", "colors": ["#D2B48C", "#0D0D0D", "#FFFFFF", "#CCCCCC"]},
        {"title": "Old Money Neutral Combo", "image": images["old_money"], "notes": "Double-breasted black crest blazer paired with beige tailored wool trousers.", "colors": ["#0D0D0D", "#D2B48C", "#D4AF37", "#FFFFFF"]}
    ],
    "Burgundy + Cream": [
        {"title": "Burgundy Dress Cream Blazer", "image": images["old_money"], "notes": "Burgundy silk slip dress styled with a cream oversized blazer.", "colors": ["#800020", "#FFFDD0", "#D4AF37", "#1A1817"]},
        {"title": "Burgundy Knit Cream Slip Skirt", "image": images["winter"], "notes": "Cozy burgundy chunky knit sweater paired with a cream slip midi skirt.", "colors": ["#800020", "#FFFDD0", "#EAE6DF", "#CCCCCC"]},
        {"title": "Burgundy Blazer Cream Trousers", "image": images["office"], "notes": "Burgundy tailored blazer paired with off-white tailored cream trousers.", "colors": ["#800020", "#FFFDD0", "#FFFFFF", "#1F1F1F"]},
        {"title": "Burgundy Coat Cream Turtleneck", "image": images["winter"], "notes": "Burgundy wool coat layered over a cozy cream cashmere turtleneck sweater.", "colors": ["#800020", "#FFFDD0", "#808080", "#0D0D0D"]},
        {"title": "Burgundy Slip Cream Trench Set", "image": images["old_money"], "notes": "Deep burgundy cable-knit crewneck sweater styled with cream linen slacks.", "colors": ["#800020", "#FFFDD0", "#C2B280", "#FFFFFF"]}
    ],
    "Chocolate Brown + Cream": [
        {"title": "Brown Trench Cream Turtleneck", "image": images["dark_academia"], "notes": "Chocolate brown wool trench coat layered over a cream turtleneck sweater.", "colors": ["#5C4033", "#F5F5DC", "#8B5A2B", "#FFFFFF"]},
        {"title": "Brown Vest Cream Oxford Shirt", "image": images["dark_academia"], "notes": "Earthy brown cable vest layered over a cream cotton button-down shirt.", "colors": ["#5C4033", "#F5F5DC", "#FFFFFF", "#2B2B2B"]},
        {"title": "Brown Cardigan Cream Trousers", "image": images["coastal"], "notes": "Chocolate brown cardigan paired with cream corduroy wide-leg pants.", "colors": ["#5C4033", "#F5F5DC", "#8B5A2B", "#C2B280"]},
        {"title": "Brown Turtleneck Cream Trousers", "image": images["dark_academia"], "notes": "Chocolate cashmere turtleneck sweater styled with cream tailored trousers.", "colors": ["#5C4033", "#FFFDD0", "#FFFFFF", "#1A1A1A"]},
        {"title": "Brown Corduroy Cream Knit Look", "image": images["coastal"], "notes": "Brown patterned knit cardigan worn over cream trousers and suede loafers.", "colors": ["#5C4033", "#FFFDD0", "#8B5A2B", "#C2B280"]}
    ],
    "Navy + White": [
        {"title": "Navy Blazer White Linen Polo", "image": images["old_money"], "notes": "Double-breasted navy blazer styled with a white linen knit polo shirt.", "colors": ["#0B1D3A", "#FFFFFF", "#D4AF37", "#D2B48C"]},
        {"title": "Navy Tweed Dress White Collar", "image": images["old_money"], "notes": "Navy tweed pleated A-line dress featuring white collar piping.", "colors": ["#0B1D3A", "#FFFFFF", "#CCCCCC", "#FFF0F5"]},
        {"title": "Navy Oxford Shirt White Shorts", "image": images["old_money"], "notes": "Oversized navy button-down shirt paired with white linen summer shorts.", "colors": ["#0B1D3A", "#FFFFFF", "#CCCCCC", "#E1D9D1"]},
        {"title": "Navy Cable Vest White Chinos", "image": images["old_money"], "notes": "Navy cable-knit preppy vest styled over a white oxford shirt and chinos.", "colors": ["#0B1D3A", "#FFFFFF", "#D2B48C", "#CCCCCC"]},
        {"title": "Navy Silk Slip White Linen Wrap", "image": images["old_money"], "notes": "Navy silk slip dress paired with a white linen wrap and gold accessories.", "colors": ["#0B1D3A", "#FFFFFF", "#CCCCCC", "#EAE6DF"]}
    ],
    "Sage Green + Cream": [
        {"title": "Sage Gingham Dress Cream Tote", "image": images["cottagecore"], "notes": "Sage green and cream gingham maxi dress styled with a cream woven tote bag.", "colors": ["#8FBC8F", "#FFFDD0", "#8B5A2B", "#FFFFFF"]},
        {"title": "Sage Halter Top Cream Trousers", "image": images["summer"], "notes": "Sage green halter crop top paired with cream linen wide-leg trousers.", "colors": ["#8FBC8F", "#FFFDD0", "#FFFFFF", "#D2B48C"]},
        {"title": "Sage Corset Blouse Cream Skirt", "image": images["cottagecore"], "notes": "Sage green embroidered floral corset belt styled over a cream linen skirt.", "colors": ["#8FBC8F", "#FFFDD0", "#FFFFFF", "#EAE6DF"]},
        {"title": "Sage Ribbon Wrap Cream Slip Set", "image": images["coquette"], "notes": "Sage green wrap top paired with a cream slip skirt and green ribbon bows.", "colors": ["#8FBC8F", "#FFFDD0", "#FFC0CB", "#FFFFFF"]},
        {"title": "Sage Cable Sweater Cream Trousers", "image": images["cottagecore"], "notes": "Sage green crop cable-knit sweater styled with cream linen trousers.", "colors": ["#8FBC8F", "#FFFDD0", "#CCCCCC", "#FFFFFF"]}
    ],
    "White + Light Blue": [
        {"title": "White Linen Shorts Blue Stripe Shirt", "image": images["summer"], "notes": "Light blue and white striped linen shirt styled over clean white shorts.", "colors": ["#ADD8E6", "#FFFFFF", "#CCCCCC", "#E1D9D1"]},
        {"title": "White Ribbed Set Blue Trench", "image": images["clean"], "notes": "White ribbed knit set paired with a light blue tailored trench coat.", "colors": ["#FFFFFF", "#ADD8E6", "#CCCCCC", "#EAE6DF"]},
        {"title": "White Tennis Skirt Blue Oxford", "image": images["old_money"], "notes": "Crisp white tennis skirt paired with a light blue Oxford cotton shirt.", "colors": ["#FFFFFF", "#ADD8E6", "#C2B280", "#CCCCCC"]},
        {"title": "White Denim Pants Blue Cashmere", "image": images["capsule"], "notes": "Clean white denim pants paired with a sky blue cashmere crewneck sweater.", "colors": ["#FFFFFF", "#ADD8E6", "#E1D9D1", "#CCCCCC"]},
        {"title": "White Silk Cami Blue Denim Outfit", "image": images["summer"], "notes": "White silk camisole top paired with light blue denim midi skirt.", "colors": ["#FFFFFF", "#ADD8E6", "#EAE6DF", "#CCCCCC"]}
    ],
    "Brown + Sky Blue": [
        {"title": "Brown Wool Vest Blue Oxford Shirt", "image": images["coastal"], "notes": "Patterned brown wool vest over a light blue Oxford shirt.", "colors": ["#5C4033", "#ADD8E6", "#F5F5DC", "#2E8B57"]},
        {"title": "Brown Pants Blue Cotton Shirt", "image": images["coastal"], "notes": "Chocolate brown corduroy trousers styled with a sky blue cotton shirt.", "colors": ["#5C4033", "#ADD8E6", "#FFFDD0", "#5C4033"]},
        {"title": "Brown Corduroy Blazer Blue Polo", "image": images["coastal"], "notes": "Tan corduroy blazer styled with a sky blue knit polo shirt.", "colors": ["#C2B280", "#ADD8E6", "#5C4033", "#FFFDD0"]},
        {"title": "Brown Suede Jacket Blue Denim Fit", "image": images["cottagecore"], "notes": "Camel suede fringe jacket over sky blue denim jeans.", "colors": ["#C2B280", "#ADD8E6", "#8B5A2B", "#FFFFFF"]},
        {"title": "Brown Knit Cardigan Blue Ribbons", "image": images["coastal"], "notes": "Patterned brown knit cardigan paired with sky blue ribbons and jeans.", "colors": ["#5C4033", "#ADD8E6", "#FFFDD0", "#D4AF37"]}
    ],
    "Gray + Burgundy": [
        {"title": "Grey Blazer Burgundy Leather Bag", "image": images["office"], "notes": "Tailored grey blazer paired with grey trousers and a burgundy leather bag.", "colors": ["#808080", "#800020", "#FFFFFF", "#2B2B2B"]},
        {"title": "Grey Trouser Burgundy Wool Coat", "image": images["winter"], "notes": "Oversized burgundy wool coat paired with dark grey tailored pants.", "colors": ["#800020", "#808080", "#FFFFFF", "#0D0D0D"]},
        {"title": "Grey Knit Sweater Burgundy Pants", "image": images["office"], "notes": "Charcoal grey knit sweater styled with burgundy tailored trousers.", "colors": ["#808080", "#800020", "#1A1A1A", "#FFFFFF"]},
        {"title": "Grey Suit Set Burgundy Silk Shirt", "image": images["office"], "notes": "Tailored grey suit blazer paired with a burgundy silk button-down shirt.", "colors": ["#808080", "#800020", "#FFFFFF", "#CCCCCC"]},
        {"title": "Charcoal Trench Burgundy Trousers", "image": images["office"], "notes": "Charcoal grey trench coat styled over burgundy high-waisted pants.", "colors": ["#555555", "#800020", "#FFFFFF", "#CCCCCC"]}
    ],
    "Red + Pink": [
        {"title": "Red Cargo Pants Pink Baby Tee", "image": images["y2k"], "notes": "Hot pink graphic baby tee paired with loose red utility cargo pants.", "colors": ["#FF1493", "#FF0000", "#CCCCCC", "#EFEFEF"]},
        {"title": "Red Cardigan Pink Satin Skirt", "image": images["coquette"], "notes": "Vibrant red cardigan paired with a blush pink satin midi slip skirt.", "colors": ["#FF0000", "#FFC0CB", "#FFF0F5", "#FFFFFF"]},
        {"title": "Red Party Dress Pink Outer Wrap", "image": images["coquette"], "notes": "Red tulle dress styled with pale pink velvet wrap ribbons.", "colors": ["#FF0000", "#FFC0CB", "#FFF0F5", "#FFFFFF"]},
        {"title": "Red Crop Top Pink Satin Sandals", "image": images["bratz"], "notes": "Red cropped tank top paired with denim skirt and pink platform sandals.", "colors": ["#FF0000", "#FFC0CB", "#4B6F96", "#0D0D0D"]},
        {"title": "Red Blazer Pink Tailored Coord", "image": images["barbie"], "notes": "Vibrant red blazer paired with a hot pink crewneck and pink trousers.", "colors": ["#FF0000", "#FF1493", "#FF69B4", "#FFFFFF"]}
    ],
    "Black + Silver": [
        {"title": "Black Hoodie Silver Chunky Chains", "image": images["streetwear"], "notes": "Oversized black graphic hoodie paired with chunky silver statement chains.", "colors": ["#0D0D0D", "#CCCCCC", "#555555", "#FFFFFF"]},
        {"title": "Black Windbreaker Silver Hardware", "image": images["streetwear"], "notes": "Asymmetrical black tactical windbreaker featuring industrial silver zip hardware.", "colors": ["#0D0D0D", "#CCCCCC", "#1F1F1F", "#808080"]},
        {"title": "Black Sequined Top Silver Pants", "image": images["y2k"], "notes": "A black graphic tank top styled with silver metallic skinny trousers.", "colors": ["#0D0D0D", "#C0C0C0", "#FFFFFF", "#808080"]},
        {"title": "Black Asymmetric Coat Silver Rings", "image": images["minimalist"], "notes": "Asymmetric black draped wool coat styled with raw industrial silver rings.", "colors": ["#111111", "#CCCCCC", "#1F1F1F", "#FFFFFF"]},
        {"title": "Black Cargo Pants Silver Buckle", "image": images["streetwear"], "notes": "Black cargos styled with a silver metal-buckle utility belt and boots.", "colors": ["#0D0D0D", "#CCCCCC", "#1A1A1A", "#808080"]}
    ],
    "Ivory + Camel": [
        {"title": "Ivory Crochet Top Camel Suede Coat", "image": images["cottagecore"], "notes": "Ivory crochet crop top styled under a fringe camel suede jacket.", "colors": ["#FFFDD0", "#C2B280", "#8B5A2B", "#FFFFFF"]},
        {"title": "Ivory Slip Dress Camel Hair Coat", "image": images["summer"], "notes": "Ivory silk slip dress styled with a camel hair coat and gold droplet earrings.", "colors": ["#FFFDD0", "#C2B280", "#D4AF37", "#FFFFFF"]},
        {"title": "Ivory Cashmere Set Camel Trench", "image": images["minimalist"], "notes": "Ivory cashmere sweater and slacks styled under a camel wool trench coat.", "colors": ["#FFFDD0", "#C2B280", "#D2B48C", "#FFFFFF"]},
        {"title": "Ivory Linen Pants Camel Knit Vest", "image": images["minimalist"], "notes": "Ivory wide-leg linen pants paired with camel knit vest and straw hat.", "colors": ["#FFFDD0", "#C2B280", "#EAE6DF", "#8B5A2B"]},
        {"title": "Ivory Cable Knit Camel Slacks Fit", "image": images["minimalist"], "notes": "Ivory cable-knit turtleneck sweater paired with camel tailored slacks.", "colors": ["#FFFDD0", "#C2B280", "#FFFFFF", "#CCCCCC"]}
    ],
    "Olive + Black": [
        {"title": "Olive windbreaker Black Ripstop", "image": images["streetwear"], "notes": "Waterproof olive tech jacket paired with black utility ripstop trousers.", "colors": ["#556B2F", "#0D0D0D", "#CCCCCC", "#1F1F1F"]},
        {"title": "Olive Cargo Vest Black Crop Tee", "image": images["streetwear"], "notes": "Tactical olive utility cargo vest over an oversized black graphic tee.", "colors": ["#556B2F", "#0D0D0D", "#CCCCCC", "#1F1F1F"]},
        {"title": "Olive Shell Jacket Black Cargos", "image": images["streetwear"], "notes": "Olive green technical shell jacket paired with black tactical cargo pants.", "colors": ["#556B2F", "#0D0D0D", "#1A1A1A", "#808080"]},
        {"title": "Olive Cable Sweater Black Jeans", "image": images["streetwear"], "notes": "Olive green cable-knit crewneck sweater styled with black jeans.", "colors": ["#556B2F", "#0D0D0D", "#CCCCCC", "#FFFFFF"]},
        {"title": "Olive Utility Coat Black Boots", "image": images["streetwear"], "notes": "Olive green utility parka coat paired with heavy black combat boots.", "colors": ["#556B2F", "#0D0D0D", "#808080", "#FFFFFF"]}
    ],
    "Navy + Tan": [
        {"title": "Navy Wool Sweater Tan Corduroy Pants", "image": images["winter"], "notes": "Thick navy blue wool sweater paired with tan corduroy utility trousers.", "colors": ["#0B1D3A", "#D2B48C", "#111111", "#FFFDD0"]},
        {"title": "Navy Shell Windbreaker Tan Cargos", "image": images["streetwear"], "notes": "Navy blue technical shell windbreaker paired with tan ripstop utility cargos.", "colors": ["#0B1D3A", "#D2B48C", "#0D0D0D", "#CCCCCC"]},
        {"title": "Navy Crest Blazer Tan Trousers", "image": images["old_money"], "notes": "Double-breasted navy crest blazer styled with tan tailored trousers.", "colors": ["#0B1D3A", "#D2B48C", "#D4AF37", "#FFFFFF"]},
        {"title": "Navy Tweed Vest Tan Utility Shorts", "image": images["old_money"], "notes": "Navy tweed vest layered over a white oxford shirt and tan shorts.", "colors": ["#0B1D3A", "#D2B48C", "#FFFFFF", "#CCCCCC"]},
        {"title": "Navy Draped Cardigan Tan Slacks", "image": images["old_money"], "notes": "Navy blue ribbed knit cardigan paired with tan tailored slacks.", "colors": ["#0B1D3A", "#D2B48C", "#EAE6DF", "#FFFFFF"]}
    ],
    "Cream + Chocolate": [
        {"title": "Cream Ribbed Cashmere Chocolate Pants", "image": images["capsule"], "notes": "Oatmeal and cream ribbed crewneck paired with chocolate cashmeres.", "colors": ["#FFFDD0", "#5C4033", "#E1D9D1", "#FFFFFF"]},
        {"title": "Cream Linen Dress Chocolate Loafers", "image": images["clean"], "notes": "Cream linen button-down dress styled with chocolate brown loafers.", "colors": ["#FFFDD0", "#5C4033", "#EAE6DF", "#FFFFFF"]},
        {"title": "Cream Crewneck Chocolate Trench Coat", "image": images["clean"], "notes": "Off-white crewneck sweater styled under chocolate brown wool trench coat.", "colors": ["#FFFDD0", "#5C4033", "#C2B280", "#FFFFFF"]},
        {"title": "Cream Buttondown Chocolate Knit Vest", "image": images["dark_academia"], "notes": "Cream cotton button-down shirt layered under chocolate brown knit vest.", "colors": ["#FFFDD0", "#5C4033", "#8B5A2B", "#FFFFFF"]},
        {"title": "Cream Corduroy Pants Chocolate Fleece", "image": images["coastal"], "notes": "Cream corduroy trousers paired with chocolate brown patterned fleece.", "colors": ["#FFFDD0", "#5C4033", "#F5F5DC", "#C2B280"]}
    ],
    "Plum + Gray": [
        {"title": "Plum Velvet Dress Grey Platform Boots", "image": images["dark_academia"], "notes": "Deep plum velvet maxi skirt combined with gray platform boots.", "colors": ["#3A0033", "#808080", "#000000", "#800020"]},
        {"title": "Plum Velvet Skirt Grey Knit Cardigan", "image": images["dark_academia"], "notes": "Plum velvet slip dress styled with a grey knit wrap cardigan.", "colors": ["#3A0033", "#808080", "#FFFDD0", "#0D0D0D"]},
        {"title": "Plum Vest Grey Slate Collared Shirt", "image": images["dark_academia"], "notes": "Plum cable knit vest layered over a slate grey collared shirt.", "colors": ["#3A0033", "#808080", "#1A1A1A", "#FFFFFF"]},
        {"title": "Plum Slip Dress Grey Wool Trench Coat", "image": images["dark_academia"], "notes": "Deep plum slip dress with black lace trim and grey wool trench coat.", "colors": ["#3A0033", "#808080", "#0D0D0D", "#800020"]},
        {"title": "Plum Cable Knit Grey Tweed Blazer", "image": images["dark_academia"], "notes": "Plum cable knit turtleneck sweater styled with grey tweed blazer.", "colors": ["#3A0033", "#808080", "#FFFDD0", "#1A1A1A"]}
    ]
}

# Compile dataset
curated_inspiration = []
card_idx = 1

# 1. Aesthetics
for aesthetic, cards_list in aesthetics_raw.items():
    for card in cards_list:
        curated_inspiration.append({
            "id": f"insp_{card_idx}",
            "title": card["title"],
            "image": card["image"],
            "pinterestUrl": f"https://www.pinterest.com/pin/{100000000 + card_idx}/",
            "aesthetic": aesthetic,
            "styleMovement": "",
            "occasion": "",
            "colorStory": "",
            "colorCombination": "",
            "notes": card["notes"],
            "colors": card["colors"]
        })
        card_idx += 1

# 2. Style Movements
for movement, cards_list in movements_raw.items():
    for card in cards_list:
        curated_inspiration.append({
            "id": f"insp_{card_idx}",
            "title": card["title"],
            "image": card["image"],
            "pinterestUrl": f"https://www.pinterest.com/pin/{100000000 + card_idx}/",
            "aesthetic": "",
            "styleMovement": movement,
            "occasion": "",
            "colorStory": "",
            "colorCombination": "",
            "notes": card["notes"],
            "colors": card["colors"]
        })
        card_idx += 1

# 3. Occasions
for occasion, cards_list in occasions_raw.items():
    for card in cards_list:
        curated_inspiration.append({
            "id": f"insp_{card_idx}",
            "title": card["title"],
            "image": card["image"],
            "pinterestUrl": f"https://www.pinterest.com/pin/{100000000 + card_idx}/",
            "aesthetic": "",
            "styleMovement": "",
            "occasion": occasion,
            "colorStory": "",
            "colorCombination": "",
            "notes": card["notes"],
            "colors": card["colors"]
        })
        card_idx += 1

# 4. Color Stories
for story, cards_list in color_stories_raw.items():
    for card in cards_list:
        curated_inspiration.append({
            "id": f"insp_{card_idx}",
            "title": card["title"],
            "image": card["image"],
            "pinterestUrl": f"https://www.pinterest.com/pin/{100000000 + card_idx}/",
            "aesthetic": "",
            "styleMovement": "",
            "occasion": "",
            "colorStory": story,
            "colorCombination": "",
            "notes": card["notes"],
            "colors": card["colors"]
        })
        card_idx += 1

# 5. Color Combinations
for combo, cards_list in color_combinations_raw.items():
    for card in cards_list:
        curated_inspiration.append({
            "id": f"insp_{card_idx}",
            "title": card["title"],
            "image": card["image"],
            "pinterestUrl": f"https://www.pinterest.com/pin/{100000000 + card_idx}/",
            "aesthetic": "",
            "styleMovement": "",
            "occasion": "",
            "colorStory": "",
            "colorCombination": combo,
            "notes": card["notes"],
            "colors": card["colors"]
        })
        card_idx += 1

print(f"Generated {len(curated_inspiration)} cards.")

# Format as JavaScript array lines
js_lines = []
js_lines.append("const curatedInspiration = [")
for card in curated_inspiration:
    # Convert to single line JSON string representation
    card_str = json.dumps(card)
    js_lines.append(f"    {card_str},")
js_lines.append("];")

js_code = "\n".join(js_lines)

# Read server.js
server_path = os.path.join(os.path.dirname(__file__), 'server.js')
with open(server_path, "r", encoding="utf-8") as f:
    server_content = f.read()

# Find bounds of current curatedInspiration array
start_marker = "const curatedInspiration = ["
end_marker = "];\n\n// Board Profiles and Curated Recommendation System"
if end_marker not in server_content:
    end_marker = "];\n// Board Profiles and Curated Recommendation System"
if end_marker not in server_content:
    end_marker = "];\r\n\r\n// Board Profiles and Curated Recommendation System"

start_idx = server_content.find(start_marker)
if start_idx == -1:
    print("Could not find start marker!")
    exit(1)

end_idx = server_content.find(end_marker, start_idx)
if end_idx == -1:
    print("Could not find end marker!")
    exit(1)

# Include the closing bracket and newlines of the marker in replacement
replacement_end = end_idx + len("];")

# Do the replacement
new_content = server_content[:start_idx] + js_code + server_content[replacement_end:]

with open(server_path, "w", encoding="utf-8") as f:
    f.write(new_content)

print("Successfully replaced curatedInspiration in server.js!")
