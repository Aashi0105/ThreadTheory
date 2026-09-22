/**
 * ThreadTheory Inspiration Dataset
 * ARCHITECTURE: Each board has its OWN dedicated set of cards.
 * Cards are NOT shared across boards. Each board is a unique Pinterest board.
 *
 * Board Types:
 *  1. aesthetics    — Fashion Aesthetics (15 boards × 5 cards = 75)
 *  2. movements     — Style Movements    (5 boards  × 5 cards = 25)
 *  3. occasions     — Occasions          (10 boards × 6 cards = 60)
 *  4. colorStories  — Color Stories      (15 boards × 6 cards = 90)
 *  5. combos        — Color Combinations (15 boards × 5 cards = 75)
 * Total: 325 cards
 */

// ─── Shared image references ──────────────────────────────────────────────
const IMG = {
    minimalist:   '/assets/inspiration/insp_minimalist.png',
    capsule:      '/assets/inspiration/insp_capsule_wardrobe.png',
    clean:        '/assets/inspiration/insp_clean_girl.png',
    y2k:          '/assets/inspiration/insp_y2k.png',
    barbie:       '/assets/inspiration/insp_barbiecore.png',
    bratz:        '/assets/inspiration/insp_bratz_fashion.png',
    dark_acad:    '/assets/inspiration/insp_dark_academia.png',
    old_money:    '/assets/inspiration/insp_old_money.png',
    coastal:      '/assets/inspiration/insp_coastal_grandmother.png',
    cottage:      '/assets/inspiration/insp_cottagecore.png',
    street:       '/assets/inspiration/insp_streetwear.png',
    office:       '/assets/inspiration/insp_office_siren.png',
    winter:       '/assets/inspiration/insp_winter_outfits.png',
    coquette:     '/assets/inspiration/insp_coquette.png',
    ballet:       '/assets/inspiration/insp_ballet_core.png',
    summer:       '/assets/inspiration/insp_summer_outfits.png',
    concerts:     '/assets/inspiration/insp_concerts.png',
    white_soir:   '/assets/inspiration/insp_white_soir.png',
    black_night:  '/assets/inspiration/insp_black_night.png',
    europe_trip:  '/assets/inspiration/insp_europe_trip.png',
    graduation:   '/assets/inspiration/insp_graduation.png',
    birthday:     '/assets/inspiration/insp_birthday.png',
    date_night:   '/assets/inspiration/insp_date_night.png',
    instagram:    '/assets/inspiration/insp_instagram.png',
    cafe_date:    '/assets/inspiration/insp_cafe_date.png',
    college:      '/assets/inspiration/insp_college.png',
};

// ─── 1. AESTHETICS ────────────────────────────────────────────────────────
const aestheticsBoards = {
    'Minimalism / Quiet Luxury': [
        { title: 'Double-Breasted Cream Coat',       img: IMG.minimalist, notes: 'Cream coat layered over matching cream knit trousers — understated quiet luxury at its finest.',             colors: ['#FFFDD0','#EAE6DF','#CCCCCC','#1A1817'] },
        { title: 'Tailored Pleated Trousers Look',   img: IMG.minimalist, notes: 'Sleek beige high-waisted tailored pants with tucked white silk button-down.',                                colors: ['#D2B48C','#FFFFFF','#E1D9D1','#1A1817'] },
        { title: 'Cashmere Mockneck Layering',       img: IMG.capsule,    notes: 'Grey cashmere mockneck knit paired with structured slate trousers and leather loafers.',                    colors: ['#808080','#2B2B2B','#FFFFFF','#CCCCCC'] },
        { title: 'Silk Wrap Midi Skirt Outfit',      img: IMG.minimalist, notes: 'Sand-toned silk wrap skirt with a simple white ribbed crewneck top and minimalist mules.',                  colors: ['#E1D9D1','#FFFFFF','#C2B280','#1A1817'] },
        { title: 'Monochrome Beige Power Suit',      img: IMG.capsule,    notes: 'Perfectly tailored single-button beige blazer over matching wide-leg trousers.',                            colors: ['#C2B280','#FFFDD0','#EAE6DF','#1A1817'] },
    ],
    'Y2K': [
        { title: 'Low-Rise Denim & Baby Tee',        img: IMG.y2k,    notes: 'Low-rise baggy cargo jeans paired with a baby pink graphic crop tee and metallic hair clips.',        colors: ['#FFC0CB','#4B6F96','#CCCCCC','#FFFFFF'] },
        { title: 'Metallic Silver Crop Puffer',      img: IMG.y2k,    notes: 'Silver foil cropped puffer jacket with dark wash low-rise jeans and chunky sneakers.',               colors: ['#C0C0C0','#1A1A1A','#FFFFFF','#FF0000'] },
        { title: 'Rhinestone Velour Track Set',      img: IMG.barbie, notes: 'Y2K velour tracksuit in hot pink with rhinestone detailing and a chunky silver zip.',               colors: ['#FF1493','#FF69B4','#CCCCCC','#FFFFFF'] },
        { title: 'Pleated Denim Micro Skirt Fit',    img: IMG.bratz,  notes: 'Pleated blue denim micro skirt with a red crop tank top and pink chunky platform sandals.',        colors: ['#FF0000','#FFC0CB','#4B6F96','#0D0D0D'] },
        { title: 'Butterfly Clips & Slip Dress',     img: IMG.barbie, notes: 'Baby blue satin slip dress accessorised with butterfly clips and platform flip-flops.',             colors: ['#ADD8E6','#FFC0CB','#FFFFFF','#C0C0C0'] },
    ],
    'Dark Academia': [
        { title: 'Tweed Blazer & Pleated Skirt',     img: IMG.dark_acad, notes: 'Chocolate brown herringbone blazer combined with a black pleated wool skirt and oxford shoes.',      colors: ['#5C4033','#0D0D0D','#FFFDD0','#8B5A2B'] },
        { title: 'Herringbone Oversized Coat',       img: IMG.dark_acad, notes: 'Oversized grey herringbone wool coat layered over a black ribbed mockneck and cord pants.',        colors: ['#808080','#0D0D0D','#FFFFFF','#CCCCCC'] },
        { title: 'Plum Corduroy Blazer Set',         img: IMG.dark_acad, notes: 'Plum velvet corduroy blazer styled with a charcoal grey turtleneck sweater and loafers.',         colors: ['#3A0033','#808080','#1A1A1A','#FFFFFF'] },
        { title: 'Scholarly Cable Knit Vest',        img: IMG.dark_acad, notes: 'Earthy brown cable vest over a white cotton button-down and tailored trousers.',                  colors: ['#5C4033','#FFFFFF','#F5F5DC','#2B2B2B'] },
        { title: 'Collegiate Wool Scarf Layering',   img: IMG.dark_acad, notes: 'Rich burgundy plaid scarf wrapped over a grey herringbone blazer and dark jeans.',               colors: ['#800020','#808080','#F5F5DC','#0D0D0D'] },
    ],
    'Cottagecore': [
        { title: 'Gingham Puffed Sleeve Maxi',       img: IMG.cottage, notes: 'Sage green and cream gingham maxi dress styled with a woven straw hat and leather sandals.',       colors: ['#8FBC8F','#FFFDD0','#8B5A2B','#FFFFFF'] },
        { title: 'Linen Ruffled Sundress',           img: IMG.cottage, notes: 'Simple cream linen sundress featuring ruffled shoulder straps and a tiered skirt hem.',            colors: ['#FFFDD0','#EAE6DF','#C2B280','#FFFFFF'] },
        { title: 'Crochet Floral Knit Vest Outfit',  img: IMG.cottage, notes: 'Hand-crocheted cream vest with pastel embroidered flowers over a white smock dress.',             colors: ['#FFFDD0','#FFC0CB','#8FBC8F','#FFFFFF'] },
        { title: 'Swiss Dot Prairie Blouse Set',     img: IMG.cottage, notes: 'Ivory Swiss dot cotton blouse styled with a sage green tiered linen maxi skirt.',                 colors: ['#FFFFFF','#8FBC8F','#FFFDD0','#D2B48C'] },
        { title: 'Wildflower Embroidered Dress',     img: IMG.cottage, notes: 'Soft cotton dress with delicate hand-embroidered wildflower details at the cuffs and collar.',     colors: ['#FFFDD0','#FFC0CB','#8FBC8F','#E8D5B7'] },
    ],
    'Streetwear': [
        { title: 'Oversized Utility Cargo Hoodie',   img: IMG.street, notes: 'Oversized black graphic hoodie paired with black nylon utility cargo pants and Air Max.',          colors: ['#0D0D0D','#CCCCCC','#555555','#FFFFFF'] },
        { title: 'Nylon Graphic Windbreaker Fit',    img: IMG.street, notes: 'Color-blocked olive and black windbreaker with loose utility joggers and box-toe sneakers.',        colors: ['#556B2F','#0D0D0D','#1F1F1F','#CCCCCC'] },
        { title: 'Baggy Denim & Varsity Jacket',     img: IMG.street, notes: 'Oversized black varsity jacket styled with light-wash baggy denim jeans and chained wallet.',      colors: ['#0D0D0D','#4B6F96','#CCCCCC','#FFFFFF'] },
        { title: 'Chunky Sneakers Utility Fit',      img: IMG.street, notes: 'Black cargo track pants with oversized white graphic tee and chunky foam-sole trainers.',          colors: ['#0D0D0D','#FFFFFF','#808080','#1F1F1F'] },
        { title: 'Puffer Vest & Cargo Pants Look',   img: IMG.street, notes: 'Black quilted puffer vest layered over grey long-sleeve, with khaki utility cargos.',             colors: ['#0D0D0D','#808080','#D2B48C','#FFFFFF'] },
    ],
    'Gorpcore': [
        { title: 'Technical Ripstop Shell Jacket',   img: IMG.street, notes: 'Waterproof olive green shell jacket with taped seams, utility zippers, and trail pants.',          colors: ['#556B2F','#0D0D0D','#CCCCCC','#1F1F1F'] },
        { title: 'Fleece-Lined Navy Parka',          img: IMG.street, notes: 'Heavy navy blue technical parka shell worn over hiking utility trail pants and lug boots.',         colors: ['#0B1D3A','#D2B48C','#111111','#CCCCCC'] },
        { title: 'Nylon Utility Trail Pants Set',    img: IMG.street, notes: 'Tan ripstop utility pants styled with a tactical quick-release belt and shell jacket.',            colors: ['#D2B48C','#0B1D3A','#0D0D0D','#CCCCCC'] },
        { title: 'Hiking Trail Shell Vest Fit',      img: IMG.street, notes: 'Sage green technical cargo vest layered over a black dry-fit long-sleeve tee and boots.',          colors: ['#8FBC8F','#0D0D0D','#EAE6DF','#1F1F1F'] },
        { title: 'All-Weather Adventure Fleece',     img: IMG.winter, notes: 'Heavyweight olive fleece zip-up over a thermal base layer and waterproof gaiter pants.',           colors: ['#556B2F','#CCCCCC','#D2B48C','#111111'] },
    ],
    'Grunge': [
        { title: 'Oversized Checked Flannel Shirt',  img: IMG.dark_acad, notes: 'Burgundy and cream checked flannel shirt styled open over a distressed band tee.',             colors: ['#800020','#FFFDD0','#0D0D0D','#808080'] },
        { title: 'Distressed Knit & Silk Slip Skirt',img: IMG.winter,    notes: 'Oversized ripped burgundy sweater paired with a black silk slip midi skirt.',                  colors: ['#800020','#0D0D0D','#FFFDD0','#4A4A4A'] },
        { title: 'Chunky Combat Boots Grunge Fit',   img: IMG.winter,    notes: 'Distressed dark grey jeans paired with chunky black leather combat boots and band tee.',       colors: ['#808080','#0D0D0D','#CCCCCC','#1F1F1F'] },
        { title: 'Leather Jacket & Faded Band Tee',  img: IMG.office,    notes: 'Black leather moto jacket thrown over a faded charcoal band tee and distressed skinnies.',    colors: ['#0D0D0D','#808080','#CCCCCC','#1F1F1F'] },
        { title: 'Plaid Mini Skirt & Platform Boots',img: IMG.dark_acad, notes: 'Black and red plaid micro skirt with a black tube top and chunky platform ankle boots.',       colors: ['#800020','#0D0D0D','#CCCCCC','#808080'] },
    ],
    'Coquette / Balletcore': [
        { title: 'Pink Ribbon Cardigan & Bows',      img: IMG.coquette, notes: 'Light pink cardigan styled with small red satin bows down the front button placket.',           colors: ['#FFC0CB','#FF0000','#FFF0F5','#FDF2F8'] },
        { title: 'Ballet Wrap Top & Tulle Skirt',    img: IMG.ballet,   notes: 'Ribbed pale pink wrap top worn with a white tulle skirt and satin hair ribbons.',               colors: ['#FFC0CB','#FFFFFF','#FFFDD0','#FFF0F5'] },
        { title: 'Satin Slip Dress & Pearl Choker',  img: IMG.coquette, notes: 'Soft pink satin midi slip dress styled with a delicate red ribbon choker and gold hoops.',      colors: ['#FFC0CB','#FF0000','#FFF0F5','#FFFFFF'] },
        { title: 'Ruffled Pastel Knit Camisole',     img: IMG.coquette, notes: 'Lavender knit camisole with white ruffle trim details and matching lavender hair ribbons.',      colors: ['#E6E6FA','#FFFDD0','#D4AF37','#9370DB'] },
        { title: 'Ballerina Pink Mini Dress Look',   img: IMG.ballet,   notes: 'Dusty pink wrap mini dress with bow embellishments, styled with ballet-toe flats.',             colors: ['#FFC0CB','#FFFFFF','#E6E6FA','#FFF0F5'] },
    ],
    'Old Money / Preppy': [
        { title: 'Navy Crest Blazer & Chinos',       img: IMG.old_money, notes: 'Double-breasted navy crest blazer styled with tan tailored wool chinos and loafers.',          colors: ['#0B1D3A','#D2B48C','#D4AF37','#FFFFFF'] },
        { title: 'Cable-Knit Tennis Polo Vest',      img: IMG.old_money, notes: 'White cable-knit tennis vest with navy piping layered over a white polo shirt.',               colors: ['#FFFFFF','#0B1D3A','#D2B48C','#CCCCCC'] },
        { title: 'Camel Double-Breasted Trench',     img: IMG.old_money, notes: 'Camel hair double-breasted trench coat paired with white linen trousers and loafers.',          colors: ['#C2B280','#FFFFFF','#EAE6DF','#8B5A2B'] },
        { title: 'Oxford Button-Down & Pleated Skirt',img: IMG.old_money,notes: 'Crisp light blue Oxford button-down tucked into a beige pleated tennis skirt.',               colors: ['#ADD8E6','#C2B280','#FFFFFF','#5C4033'] },
        { title: 'Equestrian-Inspired Riding Coat',  img: IMG.old_money, notes: 'Dark brown equestrian-cut blazer with gold buttons over ivory turtleneck and jodhpurs.',       colors: ['#5C4033','#FFFDD0','#D4AF37','#0B1D3A'] },
    ],
    'Eclectic Grandpa': [
        { title: 'Chunky Patterned Cardigan Fit',    img: IMG.coastal, notes: 'Vintage patterned brown knit cardigan worn over a light blue denim button-down.',               colors: ['#5C4033','#ADD8E6','#FFFDD0','#D4AF37'] },
        { title: 'Corduroy Blazer & Argyle Vest',    img: IMG.coastal, notes: 'Tan corduroy blazer layered over a mustard yellow argyle vest and brown cord pants.',           colors: ['#C2B280','#FFD700','#5C4033','#F0F0F0'] },
        { title: 'Oversized Wool Grandpa Vest',      img: IMG.coastal, notes: 'Patterned brown wool vest styled with a blue Oxford shirt and wide-leg green trousers.',        colors: ['#5C4033','#F5F5DC','#ADD8E6','#2E8B57'] },
        { title: 'Academic Loafers & Corduroys',     img: IMG.coastal, notes: 'Chocolate brown ribbed cardigan paired with beige corduroys and suede penny loafers.',          colors: ['#5C4033','#F5F5DC','#8B5A2B','#C2B280'] },
        { title: 'Mismatched Plaid & Stripe Layering',img: IMG.coastal, notes: 'Intentionally mismatched plaid flannel and stripe oxford layered together with chinos.',        colors: ['#5C4033','#ADD8E6','#FFD700','#FFFDD0'] },
    ],
    'Cyberpunk / Techwear': [
        { title: 'Tactical Asymmetric Buckled Jacket',img: IMG.street, notes: 'All-black asymmetrical tactical windbreaker featuring industrial silver strap buckles.',         colors: ['#0D0D0D','#CCCCCC','#1F1F1F','#808080'] },
        { title: 'Harness Strap Cargo Trousers',     img: IMG.street, notes: 'All-black utility cargo pants with adjustable harness straps and tactical metal buckles.',        colors: ['#0D0D0D','#CCCCCC','#1A1A1A','#808080'] },
        { title: 'Reflective Waterproof Shell',      img: IMG.street, notes: 'Grey reflective technical shell jacket paired with black utility ripstop cargos.',                colors: ['#808080','#0D0D0D','#CCCCCC','#1F1F1F'] },
        { title: 'Industrial Silver Zipper Vest',    img: IMG.street, notes: 'Black technical vest loaded with multi-pockets and heavy-duty silver zippers.',                   colors: ['#0D0D0D','#CCCCCC','#1F1F1F','#FFFFFF'] },
        { title: 'RGB-Trimmed Tech Mesh Layer',      img: IMG.dark_acad, notes: 'Semi-sheer black mesh top over tactical base layer, with neon blue reflective seams.',        colors: ['#0D0D0D','#1F1F1F','#4169E1','#CCCCCC'] },
    ],
    'Boho Chic': [
        { title: 'Fringe Suede Outerwear Jacket',    img: IMG.cottage, notes: 'Camel suede jacket with fringe trim layered over an ivory crochet crop top and flared jeans.',  colors: ['#C2B280','#FFFDD0','#8B5A2B','#40E0D0'] },
        { title: 'Crochet Tiered Maxi Sundress',     img: IMG.cottage, notes: 'Ivory crochet knit maxi dress layered over a camel bodysuit with turquoise bead jewelry.',      colors: ['#FFFDD0','#C2B280','#FFD700','#FFFFFF'] },
        { title: 'Embroidered Cotton Tunic Top',     img: IMG.cottage, notes: 'Warm ivory embroidered linen tunic paired with camel suede boots and a fringe boho bag.',       colors: ['#FFFDD0','#C2B280','#8B5A2B','#F5F5DC'] },
        { title: 'Boho Suede Fringe Shoulder Fit',   img: IMG.cottage, notes: 'Tiered floral print maxi dress styled with a fringe suede shoulder vest and woven belt.',       colors: ['#8B5A2B','#FFFDD0','#C2B280','#40E0D0'] },
        { title: 'Paisley Wrap Skirt & Crop Set',    img: IMG.summer,  notes: 'Paisley-print wrap skirt with macramé crop top and layered wooden bead necklaces.',             colors: ['#C2B280','#8FBC8F','#FFD700','#FFFDD0'] },
    ],
    'Whimsigoth': [
        { title: 'Deep Velvet Lace Slip Dress',      img: IMG.dark_acad, notes: 'Deep plum velvet slip dress with black lace trim, styled with chunky platform boots.',        colors: ['#3A0033','#000000','#808080','#800020'] },
        { title: 'Celestial Embroidered Velvet Skirt',img: IMG.dark_acad,notes: 'Deep plum velvet maxi skirt styled with a black lace top and gold celestial pins.',           colors: ['#3A0033','#000000','#D4AF37','#808080'] },
        { title: 'Sheer Bell Sleeve Lace Top',       img: IMG.dark_acad, notes: 'Burgundy velvet bodice with dramatic sheer bell sleeves, styled with cream trousers.',         colors: ['#800020','#FFFDD0','#3A0033','#1A1A1A'] },
        { title: 'Plum Velvet Kimono Duster',        img: IMG.dark_acad, notes: 'Flowing plum velvet kimono duster layered over an all-black ribbed base layer set.',          colors: ['#3A0033','#0D0D0D','#808080','#800020'] },
        { title: 'Moon Phase Corset Layering Look',  img: IMG.coquette,  notes: 'Black lace corset layered over a sheer chiffon blouse with silver crescent moon rings.',      colors: ['#0D0D0D','#CCCCCC','#3A0033','#800020'] },
    ],
    'Indie Sleaze': [
        { title: 'Shiny Silver Sequin Tank Top',     img: IMG.y2k,  notes: 'Metallic silver sequined tank top paired with distressed black skinny jeans and platforms.',      colors: ['#1A1A1A','#C0C0C0','#F0F0F0','#0D0D0D'] },
        { title: 'Metallic Leather Skinny Pants',    img: IMG.y2k,  notes: 'High-shine black leather skinny trousers styled with a distressed charcoal graphic tee.',         colors: ['#808080','#CCCCCC','#0D0D0D','#FFFFFF'] },
        { title: 'Graphic Band Tee & Faux Fur Coat', img: IMG.y2k,  notes: 'Vintage black faux fur coat worn over a graphic band tee and glitter platform boots.',            colors: ['#0D0D0D','#CCCCCC','#1F1F1F','#FFFFFF'] },
        { title: 'Distressed Leather Moto Vest',     img: IMG.y2k,  notes: 'Black distressed leather motorcycle vest over a shiny silver chainmail tank top.',                colors: ['#0D0D0D','#CCCCCC','#FFFFFF','#1F1F1F'] },
        { title: 'Smudged Liner & Slip Dress Grunge',img: IMG.dark_acad, notes: 'Black silk slip dress worn over a shredded fishnet bodysuit with chunky ring stack.',         colors: ['#0D0D0D','#808080','#FFFFFF','#3A0033'] },
    ],
    'Clean Girl': [
        { title: 'White Ribbed Knit Lounge Set',     img: IMG.clean, notes: 'Crisp white ribbed knit crewneck sweater with matching clean white wide-leg lounge pants.',       colors: ['#FFFFFF','#EAE6DF','#CCCCCC','#4E3629'] },
        { title: 'Sleek Bun Linen Button-Down',      img: IMG.clean, notes: 'Clean girl oversized white linen button-down styled with simple gold hoop earrings and bun.',    colors: ['#FFFFFF','#EAE6DF','#D4AF37','#1A1817'] },
        { title: 'Tailored Beige Trench Coat Look',  img: IMG.clean, notes: 'Tailored camel trench coat styled over an ivory activewear jumpsuit and white sneakers.',         colors: ['#C2B280','#FFFDD0','#FFFFFF','#5C4033'] },
        { title: 'Activewear Jumpsuit & Gold Hoops', img: IMG.clean, notes: 'Slate grey zip activewear jumpsuit paired with gold jewelry and a sleek pulled-back bun.',       colors: ['#808080','#D4AF37','#FFFFFF','#1A1817'] },
        { title: 'Glazed Skin Matching Set',         img: IMG.clean, notes: 'Sage green matching ribbed crewneck and shorts set with SPF-dewy skin and minimal jewellery.',   colors: ['#8FBC8F','#FFFFFF','#FFFDD0','#D4AF37'] },
    ],
};

const movementsBoards = {
    'Avant-Garde / Darkwear': [
        { title: 'Draped Black Wool Silhouette',      img: IMG.minimalist, notes: 'Asymmetric black wool draped coat combined with black wide-leg pleated trousers.',                colors: ['#111111','#CCCCCC','#1F1F1F','#FFFFFF'] },
        { title: 'Layered Distressed Hem Ensemble',   img: IMG.minimalist, notes: 'Deconstructed layers with distressed hems, raw seams, and dark charcoal textures.',               colors: ['#1A1A1A','#2B2B2B','#555555','#FFFFFF'] },
        { title: 'Oversized Asymmetric Long Coat',    img: IMG.minimalist, notes: 'Oversized black wool coat featuring asymmetric front wrap panels and structured shoulders.',      colors: ['#0D0D0D','#1F1F1F','#808080','#FFFFFF'] },
        { title: 'Monochrome Texture Play',           img: IMG.minimalist, notes: 'Play of varying black textures including heavy wool, sheer mesh, and coated cotton layers.',     colors: ['#0D0D0D','#2B2B2B','#CCCCCC','#808080'] },
        { title: 'Structured Darkwear Boots Look',     img: IMG.minimalist, notes: 'High-top structured darkwear boots paired with modular strap trousers and heavy jacket.',        colors: ['#0D0D0D','#1F1F1F','#CCCCCC','#808080'] },
    ],
    'Matrixcore / Neo-Noir': [
        { title: 'Patent Leather Long Trench Coat',   img: IMG.office,  notes: 'Shiny black leather trench coat styled over a grey knit and burgundy slim trousers.',              colors: ['#0D0D0D','#808080','#800020','#1F1F1F'] },
        { title: 'Neo Noir Tactical Harness',         img: IMG.office,  notes: 'Modular chest harness worn over a high-neck ribbed black top and technical trousers.',              colors: ['#0D0D0D','#1F1F1F','#CCCCCC','#808080'] },
        { title: 'Black Vinyl Utility Set',           img: IMG.office,  notes: 'Coated vinyl utility jacket and matching pants with high-shine surface styling.',                  colors: ['#0D0D0D','#1F1F1F','#1A1A1A','#FFFFFF'] },
        { title: 'Futuristic Monochrome Layering',    img: IMG.office,  notes: 'Floor-length technical trench coat layered with cyber shield shades and mock-neck top.',           colors: ['#0D0D0D','#111111','#CCCCCC','#808080'] },
        { title: 'Sharp Cyber Tailoring',             img: IMG.office,  notes: 'Structured black blazer with angular lapels, micro sunglasses, and high-shine boots.',             colors: ['#0D0D0D','#1A1A1A','#CCCCCC','#FFFFFF'] },
    ],
    'Corporate Minimalist': [
        { title: 'Structured Grey Tailored Suit',     img: IMG.office, notes: 'Tailored grey blazer with structured grey trousers and a burgundy leather tote.',                   colors: ['#808080','#800020','#FFFFFF','#2B2B2B'] },
        { title: 'Charcoal Wool Office Set',          img: IMG.office, notes: 'Sleek charcoal wool trousers paired with a minimal tucked silk button-down shirt.',                colors: ['#2B2B2B','#FFFFFF','#EAE6DF','#CCCCCC'] },
        { title: 'Slate Blazer & Pleated Trousers',   img: IMG.office, notes: 'Slate grey double-breasted blazer over crisp white shirt and tailored pleated slacks.',            colors: ['#555555','#FFFFFF','#0D0D0D','#CCCCCC'] },
        { title: 'Monochrome Business Capsule',       img: IMG.office, notes: 'Structured pencil skirt styled with a tailored grey cotton shirt and classic loafers.',             colors: ['#0B1D3A','#808080','#FFFFFF','#1A1817'] },
        { title: 'Tailored High-Neck Knitwear',       img: IMG.office, notes: 'Fine-knit mock-neck sweater tucked into high-waisted tailored wool trousers.',                     colors: ['#808080','#FFFDD0','#EAE6DF','#1A1817'] },
    ],
    'Oatmeal / Vanilla Girl': [
        { title: 'Cream Cable Cashmere Set',          img: IMG.capsule, notes: 'Oatmeal-colored ribbed cashmere knit pants paired with a cream crewneck sweater.',                colors: ['#FFFDD0','#E1D9D1','#E6E6FA','#C2B280'] },
        { title: 'Beige Wool Wrap Coat',              img: IMG.capsule, notes: 'Cozy beige wool wrap coat with tie belt, layered over off-white knitwear.',                       colors: ['#FFFDD0','#C2B280','#EAE6DF','#FFFFFF'] },
        { title: 'Soft Knit Lounge Ensemble',         img: IMG.capsule, notes: 'Ribbed knit wide-leg pants and matching long-sleeve top in warm oatmeal.',                       colors: ['#E1D9D1','#FFFDD0','#EAE6DF','#8B5A2B'] },
        { title: 'Vanilla Ribbed Cardigan Outfit',    img: IMG.capsule, notes: 'Chunky ribbed cardigan in vanilla cream, paired with cream linen pants and gold details.',      colors: ['#FFFDD0','#C2B280','#EAE6DF','#8B5A2B'] },
        { title: 'Cozy Neutral Layering',             img: IMG.capsule, notes: 'Tonal layering of beige knitwear, cream teddy coat, and light tan accessories.',                  colors: ['#E1D9D1','#FFFFFF','#FFFDD0','#CCCCCC'] },
    ],
    'Dopamine Monochrome': [
        { title: 'Hot Pink Double-Breasted Suit',     img: IMG.barbie, notes: 'Vibrant hot pink matching trousers and double-breasted suit blazer for maximum dopamine.',           colors: ['#FF1493','#FF69B4','#FFFFFF','#FF0000'] },
        { title: 'Royal Blue Power Dressing',         img: IMG.barbie, notes: 'Royal blue monochrome pantsuit with a matching blue trench coat for high impact.',                 colors: ['#4169E1','#FFFFFF','#CCCCCC','#1A1A1A'] },
        { title: 'Emerald Green Statement Look',      img: IMG.barbie, notes: 'Rich emerald green wool overcoat worn over a matching emerald green rib sweater and slacks.',       colors: ['#2E8B57','#FFFDD0','#CCCCCC','#1F1F1F'] },
        { title: 'Vibrant Yellow Monochrome Set',     img: IMG.barbie, notes: 'Sunny yellow utility vest paired with matching yellow cargo utility pants.',                         colors: ['#FFD700','#FFFFFF','#CCCCCC','#1A1A1A'] },
        { title: 'Bright Orange Textured Coat Look',  img: IMG.barbie, notes: 'Bright orange textured coat layered over a bright yellow crewneck knit and orange trousers.',       colors: ['#FF8C00','#FFD700','#FFFFFF','#1A1A1A'] },
    ],
};

// ─── 3. OCCASIONS ─────────────────────────────────────────────────────────
const occasionsBoards = {
    'Concerts & Festivals': [
        { title: 'Festival Mesh Top & Cargo Pants',   img: IMG.concerts,    notes: 'Neon printed mesh long-sleeve top styled with low-rise cargo pants, chunky belt, and mini shoulder bag.',            colors: ['#FF1493','#4B6F96','#CCCCCC','#0D0D0D'] },
        { title: 'Neon Crochet Festival Set',         img: IMG.concerts, notes: 'Vibrant neon green crochet halter crop top and matching mini skirt, finished with woven lace-up sandals.',          colors: ['#39FF14','#FFFFFF','#D2B48C','#FFFDD0'] },
        { title: 'Metallic Mini Skirt Concert Look',  img: IMG.concerts,    notes: 'High-shine metallic silver mini skirt paired with an oversized black graphic band tee and chunky platform boots.',                   colors: ['#C0C0C0','#0D0D0D','#FFFFFF','#808080'] },
        { title: 'Graphic Band Tee & Combat Boots',   img: IMG.concerts,  notes: 'Oversized charcoal graphic band tee styled as a dress with fishnet tights and heavy-duty black leather combat boots.',               colors: ['#0D0D0D','#808080','#FFFFFF','#1F1F1F'] },
        { title: 'Rhinestone Denim Festival Outfit',  img: IMG.concerts,  notes: 'Rhinestone-studded denim crop jacket worn over a white crop top, paired with matching rhinestone distressed jeans.',                  colors: ['#4B6F96','#FFFFFF','#CCCCCC','#FFC0CB'] },
    ],
    'All White Soirées': [
        { title: 'White Linen Garden Party Suit',     img: IMG.white_soir, notes: 'Crisp white structured linen blazer paired with matching wide-leg white linen trousers and gold details.',                    colors: ['#FFFFFF','#EAE6DF','#D4AF37','#C2B280'] },
        { title: 'White Satin Slip Dress',           img: IMG.white_soir, notes: 'Elegant white satin midi slip dress featuring a cowl neckline, styled with minimal strappy heels and gold jewelry.',             colors: ['#FFFFFF','#FFFDD0','#D4AF37','#EAE6DF'] },
        { title: 'Ivory Wide-Leg Resort Set',         img: IMG.white_soir, notes: 'Breezy ivory wide-leg linen trousers paired with a matching button-down resort shirt and straw accessories.',                        colors: ['#FFFDD0','#FFFFFF','#E1D9D1','#8B5A2B'] },
        { title: 'White Eyelet Midi Dress',           img: IMG.white_soir, notes: 'Delicate white cotton midi dress featuring all-over eyelet embroidery, puffed sleeves, and a tiered skirt.',                        colors: ['#FFFFFF','#FFFDD0','#8FBC8F','#D2B48C'] },
        { title: 'Crisp White Summer Co-Ord',         img: IMG.white_soir, notes: 'Two-piece white summer co-ord featuring a cropped linen tank top and high-waisted linen shorts.',                     colors: ['#FFFFFF','#EAE6DF','#CCCCCC','#8B5A2B'] },
    ],
    'All Black Nights': [
        { title: 'Black Leather Moto & Denim',        img: IMG.black_night, notes: 'Classic black leather motorcycle jacket worn over a simple black tee, paired with washed black denim.',                            colors: ['#0D0D0D','#1A1A1A','#808080','#FFFFFF'] },
        { title: 'Black Corset Evening Look',         img: IMG.black_night, notes: 'Structured black satin corset bustier styled with high-waisted black tailored trousers and a velvet clutch.',                        colors: ['#0D0D0D','#1F1F1F','#FFFFFF','#CCCCCC'] },
        { title: 'Monochrome Clubwear Set',           img: IMG.black_night,  notes: 'Edgy monochrome black matching set featuring a crop top with hardware cutouts and a matching cargo mini skirt.',                        colors: ['#0D0D0D','#111111','#FFFFFF','#808080'] },
        { title: 'Black Satin Slip & Boots',          img: IMG.black_night, notes: 'Sleek black satin midi slip dress styled with a lace-trimmed hem and chunky black leather knee-high boots.',                       colors: ['#0D0D0D','#1F1F1F','#FFFFFF','#FFC0CB'] },
        { title: 'Structured Noir Blazer Dress',      img: IMG.black_night, notes: 'Sophisticated structured double-breasted black blazer dress styled with sheer tights and pointed slingbacks.',                     colors: ['#0D0D0D','#1A1A1A','#CCCCCC','#FFFFFF'] },
    ],
    'Europe Trip Capsule Wardrobe': [
        { title: 'Beige Trench & Breton Stripe',      img: IMG.europe_trip, notes: 'Classic double-breasted beige trench coat layered over a navy Breton stripe top and straight-leg blue jeans.',            colors: ['#C2B280','#0B1D3A','#FFFFFF','#4B6F96'] },
        { title: 'White Linen Summer Sundress',       img: IMG.europe_trip, notes: 'Breezy white linen midi sundress styled with a woven straw tote bag and comfortable leather slide sandals.',               colors: ['#FFFFFF','#8B5A2B','#FFFDD0','#D2B48C'] },
        { title: 'Neutral Airport Travel Set',        img: IMG.europe_trip, notes: 'Cozy oatmeal-colored ribbed knit wide-leg pants and matching long-sleeve crewneck set for comfortable travel.',                    colors: ['#E1D9D1','#FFFDD0','#EAE6DF','#8B5A2B'] },
        { title: 'Camel Blazer & Straight Jeans',     img: IMG.europe_trip, notes: 'Tailored camel blazer layered over a white crewneck tee, styled with straight-leg blue denims and loafers.',          colors: ['#C2B280','#FFFFFF','#4B6F96','#5C4033'] },
        { title: 'Navy Coastal Vacation Outfit',      img: IMG.europe_trip, notes: 'Navy knit polo shirt styled with white tailored linen shorts, white leather sneakers, and gold hoop jewelry.',                    colors: ['#0B1D3A','#FFFFFF','#EAE6DF','#D4AF37'] },
    ],
    'Graduation Looks': [
        { title: 'Graduation Navy Tweed Dress',       img: IMG.graduation, notes: 'Smart navy structured tweed dress featuring white collar trim and vintage pearl buttons.',         colors: ['#0B1D3A','#FFFFFF','#D4AF37','#CCCCCC'] },
        { title: 'White Blazer Ceremony Outfit',      img: IMG.graduation, notes: 'Tailored white blazer worn over an ivory silk camisole and matching wide-leg pleated trousers.',           colors: ['#FFFFFF','#FFFDD0','#EAE6DF','#CCCCCC'] },
        { title: 'Classic Black Graduation Ensemble',  img: IMG.graduation, notes: 'Timeless black A-line midi dress styled with simple pearls and low block-heeled sandals.',             colors: ['#0D0D0D','#FFFFFF','#D4AF37','#CCCCCC'] },
        { title: 'Soft Pink Celebration Dress',       img: IMG.graduation, notes: 'Delicate pastel pink wrap dress featuring ruffle sleeve details, paired with elegant nude heels.',                           colors: ['#FFC0CB','#FFFFFF','#FFF0F5','#D2B48C'] },
        { title: 'Tailored Wide-Leg Graduation Set',   img: IMG.graduation,    notes: 'Polished sage green tailored blazer and matching high-waisted wide-leg trousers for a fresh celebratory look.',         colors: ['#8FBC8F','#FFFFFF','#EAE6DF','#D4AF37'] },
    ],
    'Birthday Milestone Looks': [
        { title: 'Hot Pink Birthday Statement Dress',  img: IMG.birthday,    notes: 'Vibrant hot pink double-breasted blazer dress featuring rhinestone statement buttons for maximum birthday impact.',              colors: ['#FF1493','#FF69B4','#FFFFFF','#C0C0C0'] },
        { title: 'Silver Party Mini Dress',           img: IMG.birthday,       notes: 'High-impact metallic silver sequin party mini dress styled with strappy silver heels and hoop earrings.',            colors: ['#C0C0C0','#FFFFFF','#0D0D0D','#808080'] },
        { title: 'Emerald Satin Celebration Look',     img: IMG.birthday,    notes: 'Emerald green satin wrap top and matching satin wide-leg trousers for an elegant birthday celebration.',                           colors: ['#2E8B57','#FFFFFF','#CCCCCC','#1F1F1F'] },
        { title: 'Red Birthday Glam Outfit',          img: IMG.birthday,    notes: 'Stunning bright red satin slip dress styled with a matching red blazer thrown over the shoulders.', colors: ['#FF0000','#0D0D0D','#FFFFFF','#CCCCCC'] },
        { title: 'White Luxe Birthday Set',           img: IMG.birthday,    notes: 'Luxe off-the-shoulder white knit top paired with a matching white silk midi skirt and gold statement jewelry.',              colors: ['#FFFFFF','#FFFDD0','#D4AF37','#EAE6DF'] },
    ],
    'High-End Date Nights': [
        { title: 'Black Silk Halter Slip Dress',      img: IMG.date_night,    notes: 'Sensual backless black silk halter midi slip dress styled with gold droplet earrings and strappy black heels.',                  colors: ['#0D0D0D','#D4AF37','#1F1F1F','#FFFFFF'] },
        { title: 'Burgundy Satin Evening Dress',      img: IMG.date_night, notes: 'Elegant deep burgundy satin evening dress styled under a structured black coat for candlelight dining.',                      colors: ['#800020','#0D0D0D','#D4AF37','#FFFFFF'] },
        { title: 'Cream Tailored Dinner Ensemble',     img: IMG.date_night,notes: 'Sophisticated cream tailored silk blouse tucked into high-waisted beige wool trousers with a tan leather belt.',                       colors: ['#FFFDD0','#C2B280','#8B5A2B','#FFFFFF'] },
        { title: 'Elegant Off-Shoulder Date Look',     img: IMG.date_night,   notes: 'Chic off-the-shoulder black ribbed knit top paired with a flowing burgundy midi skirt and knee-high boots.',                   colors: ['#0D0D0D','#800020','#FFFFFF','#1A1817'] },
        { title: 'Monochrome Luxury Dinner Fit',      img: IMG.date_night,notes: 'Understated monochrome ivory knit midi dress layered under an oversized matching ivory cashmere wrap coat.',               colors: ['#FFFFFF','#FFFDD0','#EAE6DF','#C2B280'] },
    ],
    'Instagram Content Creation': [
        { title: 'Neutral Influencer Street Style',   img: IMG.instagram,   notes: 'Tan nylon utility cargo pants paired with a white crop tee, cropped black puffer vest, and retro sunglasses.',                  colors: ['#D2B48C','#FFFFFF','#0D0D0D','#808080'] },
        { title: 'Coffee Run Content Creator Fit',    img: IMG.instagram,    notes: 'Cozy grey oversized sweatshirt paired with black biker shorts, thick white crew socks, and sporty sneakers.',             colors: ['#808080','#0D0D0D','#FFFFFF','#CCCCCC'] },
        { title: 'Beige Minimalist Content Outfit',   img: IMG.instagram,   notes: 'Oversized beige linen button-down shirt paired with off-white wide-leg knit trousers and a brown leather tote.',          colors: ['#C2B280','#FFFDD0','#8B5A2B','#FFFFFF'] },
        { title: 'Pinterest Girl Weekend Look',       img: IMG.instagram,  notes: 'Pale pink cropped cardigan styled with a cream satin midi slip skirt, gold hoops, and a messy bun.',              colors: ['#FFC0CB','#FFFDD0','#D4AF37','#FFFFFF'] },
        { title: 'Fashion Blogger City Look',         img: IMG.instagram,   notes: 'Black varsity jacket paired with a white tee, light-wash baggy boyfriend jeans, and chunky retro trainers.',                  colors: ['#0D0D0D','#FFFFFF','#4B6F96','#CCCCCC'] },
    ],
    'Cozy Cafe Dates': [
        { title: 'Cream Cable Cashmere Knitwear',     img: IMG.cafe_date,   notes: 'Heavyweight cream cable-knit cashmere sweater tucked into high-waisted warm oatmeal ribbed pants.',                      colors: ['#FFFDD0','#E1D9D1','#EAE6DF','#8B5A2B'] },
        { title: 'Brown Wool Coat & Loafers',         img: IMG.cafe_date, notes: 'Tailored chocolate brown wool coat layered over a cream turtleneck knit, finished with classic leather penny loafers.',           colors: ['#5C4033','#FFFDD0','#8B5A2B','#FFFFFF'] },
        { title: 'Oatmeal Knit Lounge Outfit',        img: IMG.cafe_date,   notes: 'Soft ribbed knit lounge set in oatmeal, styled with a cozy cream fleece cardigan and slide slippers.',                      colors: ['#E1D9D1','#FFFDD0','#EAE6DF','#8B5A2B'] },
        { title: 'Soft Cardigan Coffee Date Look',    img: IMG.cafe_date,  notes: 'Chunky pastel lavender cardigan worn open over a white cotton camisole and cream corduroy trousers.',              colors: ['#E6E6FA','#FFFFFF','#FFFDD0','#CCCCCC'] },
        { title: 'Neutral Sweater & Midi Skirt',      img: IMG.cafe_date,notes: 'Oversized beige knit sweater paired with a matching neutral silk wrap midi skirt and suede ankle boots.',               colors: ['#C2B280','#E1D9D1','#8B5A2B','#FFFFFF'] },
    ],
    'College Daily Wear': [
        { title: 'Relaxed Hoodie & Cargo Pants',      img: IMG.college,    notes: 'Oversized black graphic hoodie paired with olive green technical cargo utility pants and white canvas sneakers.',         colors: ['#0D0D0D','#556B2F','#FFFFFF','#CCCCCC'] },
        { title: 'Oversized Sweatshirt Campus Fit',   img: IMG.college,    notes: 'Oversized athletic grey college sweatshirt styled with loose blue denim jeans and a simple white tote bag.',           colors: ['#808080','#4B6F96','#FFFFFF','#CCCCCC'] },
        { title: 'Straight-Leg Denim Everyday Look',  img: IMG.college,    notes: 'Crisp white cotton button-down shirt layered under a grey crewneck sweater, paired with straight-leg blue jeans.',           colors: ['#FFFFFF','#808080','#4B6F96','#1A1817'] },
        { title: 'Varsity Knit & Sneakers',           img: IMG.college, notes: 'Navy blue cable-knit varsity vest worn over a white polo, styled with beige tailored chinos and retro trainers.',            colors: ['#0B1D3A','#FFFFFF','#D2B48C','#CCCCCC'] },
        { title: 'Casual Layered College Outfit',     img: IMG.college,   notes: 'Tonal olive green utility windbreaker worn over a black t-shirt, paired with casual loose charcoal joggers.',                  colors: ['#556B2F','#0D0D0D','#808080','#FFFFFF'] },
    ],
};

// ─── 4. COLOR STORIES ─────────────────────────────────────────────────────
const colorStoriesBoards = {
    'Black': [
        { title: 'Monochrome Noir Tailoring',         img: IMG.black_night, notes: 'Sleek double-breasted black wool coat layered over a black silk mockneck and tailored trousers.',  colors: ['#0D0D0D','#1F1F1F','#555555','#FFFFFF'] },
        { title: 'Black Leather Moto Ensemble',       img: IMG.black_night, notes: 'Distressed black leather moto jacket styled with a black tee, raw black denim, and combat boots.',     colors: ['#0D0D0D','#1A1A1A','#808080','#FFFFFF'] },
        { title: 'Minimal Black Turtleneck Fit',       img: IMG.black_night, notes: 'Cozy fine-knit black turtleneck sweater tucked neatly into high-waisted black wool trousers.',     colors: ['#0D0D0D','#2B2B2B','#CCCCCC','#FFFFFF'] },
        { title: 'Satin Evening Black Dress',         img: IMG.black_night, notes: 'Elegant backless black satin midi slip dress paired with minimal black strappy heels and clutch.',   colors: ['#0D0D0D','#111111','#FFFFFF','#CCCCCC'] },
        { title: 'All Black Streetwear Layering',     img: IMG.black_night, notes: 'Oversized black graphic hoodie layered with a utility nylon cargo vest and baggy utility pants.',   colors: ['#0D0D0D','#1F1F1F','#CCCCCC','#808080'] },
    ],
    'White': [
        { title: 'Crisp White Linen Co-Ord',         img: IMG.white_soir, notes: 'Two-piece matching set featuring a cropped white linen halter top and high-waisted linen trousers.', colors: ['#FFFFFF','#EAE6DF','#CCCCCC','#8B5A2B'] },
        { title: 'White Summer Resort Dress',         img: IMG.white_soir, notes: 'Breezy white linen sundress featuring puff sleeves, tiered skirt paneling, and straw accessories.', colors: ['#FFFFFF','#FFFDD0','#EAE6DF','#D2B48C'] },
        { title: 'White Tailored Power Suit',         img: IMG.white_soir, notes: 'Sharp double-breasted white suit blazer combined with matching white straight-leg pants.',        colors: ['#FFFFFF','#EAE6DF','#C0C0C0','#111111'] },
        { title: 'Minimal White Capsule Outfit',      img: IMG.white_soir, notes: 'Sleek white ribbed knit crewneck paired with matching ivory wide-leg lounge pants and gold hoops.',  colors: ['#FFFFFF','#FFFDD0','#EAE6DF','#D4AF37'] },
        { title: 'White Coastal Vacation Look',       img: IMG.white_soir, notes: 'White knit polo shirt styled with white tailored linen shorts, white leather sneakers, and sunglasses.', colors: ['#FFFFFF','#EAE6DF','#CCCCCC','#0B1D3A'] },
    ],
    'Cream / Ivory': [
        { title: 'Ivory Cashmere Lounge Set',         img: IMG.white_soir, notes: 'Heavyweight cream-colored cashmere knit sweater paired with matching wide-leg ivory knit pants.',     colors: ['#FFFDD0','#E1D9D1','#FFFFFF','#C2B280'] },
        { title: 'Cream Wool Winter Layers',          img: IMG.white_soir, notes: 'Cozy cream wool wrap coat with tie belt, layered over an off-white ribbed turtleneck knit.',       colors: ['#FFFDD0','#EAE6DF','#FFFFFF','#8B5A2B'] },
        { title: 'Soft Neutral Knit Ensemble',         img: IMG.white_soir, notes: 'Tonal layering of cream sweater knitwear, fluffy teddy-fleece vest, and light tan pants.',          colors: ['#E1D9D1','#FFFDD0','#FFFFFF','#CCCCCC'] },
        { title: 'Ivory Satin Slip Look',             img: IMG.white_soir, notes: 'Ivory silk midi wrap skirt paired with a dewy, off-the-shoulder ribbed cashmere cream sweater.',     colors: ['#FFFDD0','#EAE6DF','#CCCCCC','#1A1817'] },
        { title: 'Cream Minimalist Workwear',         img: IMG.white_soir, notes: 'Structured cream linen blazer styled over a cream tank top and tailored wide-leg trousers.',          colors: ['#FFFDD0','#EAE6DF','#C2B280','#1A1817'] },
    ],
    'Beige / Tan': [
        { title: 'Beige Trench & Straight Denim',     img: IMG.europe_trip, notes: 'Double-breasted beige trench coat layered over a white crewneck tee and straight-leg blue jeans.',   colors: ['#C2B280','#FFFFFF','#4B6F96','#5C4033'] },
        { title: 'Camel Wool Coat Styling',           img: IMG.europe_trip, notes: 'Camel hair wool overcoat layered over ivory mockneck knits, finished with suede ankle boots.',      colors: ['#C2B280','#FFFDD0','#8B5A2B','#FFFFFF'] },
        { title: 'Tan Tailored Wide-Leg Pants',       img: IMG.europe_trip, notes: 'High-waisted beige tailored pleated trousers styled with a minimal cream wrap blouse.',             colors: ['#D2B48C','#FFFDD0','#E1D9D1','#1A1A17'] },
        { title: 'European Capsule Wardrobe Fit',     img: IMG.europe_trip, notes: 'Tan linen button-down shirt paired with off-white high-waisted linen shorts and straw slide sandals.',colors: ['#C2B280','#FFFFFF','#EAE6DF','#8B5A2B'] },
        { title: 'Neutral Airport Travel Look',        img: IMG.europe_trip, notes: 'Cozy oatmeal-colored ribbed knit wide-leg pants and matching long-sleeve travel set.',              colors: ['#E1D9D1','#FFFDD0','#EAE6DF','#8B5A2B'] },
    ],
    'Brown': [
        { title: 'Chocolate Wool Coat Outfit',        img: IMG.cafe_date,  notes: 'Rich chocolate brown wool trench coat over an ivory mock-neck and charcoal tailored trousers.',       colors: ['#5C4033','#FFFDD0','#8B5A2B','#0D0D0D'] },
        { title: 'Espresso Knit Layering',            img: IMG.cafe_date,  notes: 'Chocolate brown ribbed polo sweater paired with beige pleated high-waisted wool trousers.',          colors: ['#5C4033','#F5F5DC','#8B5A2B','#C2B280'] },
        { title: 'Brown Monochrome Winter Look',      img: IMG.cafe_date,  notes: 'Earthy brown corduroy wide-leg pants styled with a brown vintage cable-knit sweater vest and boot.',  colors: ['#5C4033','#FFFDD0','#ADD8E6','#2E8B57'] },
        { title: 'Rich Mocha Tailored Suit',          img: IMG.cafe_date,  notes: 'Mocha brown single-button tailored blazer over matching brown wide-leg pants.',                      colors: ['#5C4033','#FFFFFF','#8B5A2B','#CCCCCC'] },
        { title: 'Coffee-Tone Weekend Outfit',        img: IMG.cafe_date,  notes: 'Patterned brown knit cardigan worn over a light blue denim shirt and cream straight chinos.',         colors: ['#5C4033','#ADD8E6','#FFFDD0','#D4AF37'] },
    ],
    'Gray': [
        { title: 'Charcoal Corporate Tailoring',      img: IMG.office,     notes: 'Tailored grey blazer paired with matching wide-leg grey trousers and a structured leather tote.',    colors: ['#808080','#FFFFFF','#1A1A1A','#CCCCCC'] },
        { title: 'Slate Knit & Trouser Combo',        img: IMG.office,     notes: 'Charcoal grey knit sweater styled with slate grey checked wool pleated trousers.',                    colors: ['#808080','#0D0D0D','#FFFDD0','#CCCCCC'] },
        { title: 'Monochrome Grey Capsule',           img: IMG.office,     notes: 'Slate grey cashmere wrap cardigan paired with off-white ribbed wide-leg pants and grey loafers.',     colors: ['#808080','#FFFFFF','#EAE6DF','#CCCCCC'] },
        { title: 'Grey Blazer Workwear Edit',         img: IMG.office,     notes: 'Grey structured wool trench coat layered over a black silk camisole and tailored grey trousers.',      colors: ['#808080','#0D0D0D','#FFFFFF','#CCCCCC'] },
        { title: 'Soft Heather Lounge Styling',       img: IMG.office,     notes: 'Oversized charcoal grey crewneck knit paired with matching heather grey joggers and trainers.',      colors: ['#808080','#0D0D0D','#CCCCCC','#FFFFFF'] },
    ],
    'Navy': [
        { title: 'Navy Double-Breasted Blazer',       img: IMG.old_money,  notes: 'Double-breasted navy blazer featuring gold crest buttons and white tailored linen trousers.',        colors: ['#0B1D3A','#FFFFFF','#D4AF37','#D2B48C'] },
        { title: 'Coastal Navy Summer Fit',           img: IMG.old_money,  notes: 'Navy and white striped knit crewneck sweater styled with white wide-leg linen shorts and sunglasses.', colors: ['#0B1D3A','#FFFFFF','#CCCCCC','#E1D9D1'] },
        { title: 'Navy Knit Minimalist Styling',      img: IMG.old_money,  notes: 'Navy blue cable-knit preppy vest styled over a white Oxford button-down shirt and beige chinos.',     colors: ['#0B1D3A','#FFFFFF','#D2B48C','#CCCCCC'] },
        { title: 'Classic Navy Workwear Look',        img: IMG.old_money,  notes: 'Navy tweed pleated A-line dress featuring pearl button details, styled with clean white pumps.',     colors: ['#0B1D3A','#FFFFFF','#CCCCCC','#FFF0F5'] },
        { title: 'Navy Luxury Capsule Outfit',        img: IMG.old_money,  notes: 'Navy blue silk midi slip dress styled with a white linen wrap-cardigan and gold accessories.',       colors: ['#0B1D3A','#FFFFFF','#CCCCCC','#EAE6DF'] },
    ],
    'Olive / Sage': [
        { title: 'Sage Linen Summer Outfit',         img: IMG.cottage,    notes: 'Calming sage green and cream gingham print puffed sleeve midi dress with straw accessories.',         colors: ['#8FBC8F','#FFFDD0','#8B5A2B','#FFFFFF'] },
        { title: 'Olive Utility Layering',            img: IMG.street,     notes: 'Water-resistant olive technical shell jacket paired with black utility ripstop cargo pants.',         colors: ['#556B2F','#0D0D0D','#CCCCCC','#1F1F1F'] },
        { title: 'Sage Cottagecore Styling',          img: IMG.cottage,    notes: 'Sage green wrap top paired with a cream slip skirt, sage ribbon bow, and woven ballet flats.',        colors: ['#8FBC8F','#FFFDD0','#FFC0CB','#FFFFFF'] },
        { title: 'Olive Cargo Streetwear Look',       img: IMG.street,     notes: 'Olive green ripstop utility cargos paired with a black graphic tee and chunky combat boots.',         colors: ['#556B2F','#0D0D0D','#808080','#FFFFFF'] },
        { title: 'Earth-Tone Weekend Capsule',        img: IMG.street,     notes: 'Sage green technical fleece jacket paired with tan nylon utility cargo pants and trail runners.',    colors: ['#8FBC8F','#D2B48C','#0B1D3A','#F0F0F0'] },
    ],
    'Burgundy': [
        { title: 'Burgundy Silk Evening Dress',       img: IMG.winter,     notes: 'Burgundy silk slip dress styled with a cream oversized wool blazer and gold drop earrings.',          colors: ['#800020','#FFFDD0','#D4AF37','#1A1817'] },
        { title: 'Burgundy Knit & Cream Trousers',    img: IMG.winter,     notes: 'Burgundy cable-knit crewneck sweater styled with cream linen trousers and leather loafers.',          colors: ['#800020','#FFFFFF','#D2B48C','#CCCCCC'] },
        { title: 'Burgundy Date Night Blazer',        img: IMG.winter,     notes: 'Burgundy tailored blazer paired with a charcoal grey knit sweater and burgundy tailored slacks.',    colors: ['#800020','#808080','#FFFFFF','#1F1F1F'] },
        { title: 'Burgundy Velvet Winter Styling',    img: IMG.winter,     notes: 'Oversized burgundy wool coat paired with dark grey pants and patent leather oxford shoes.',          colors: ['#800020','#808080','#FFFFFF','#0D0D0D'] },
        { title: 'Burgundy Monochrome Statement',     img: IMG.winter,     notes: 'Burgundy chunky knit sweater paired with matching burgundy tailored trousers and burgundy heels.',    colors: ['#800020','#1A1817','#808080','#CCCCCC'] },
    ],
    'Light Blue': [
        { title: 'Sky Blue Oxford Styling',           img: IMG.clean,      notes: 'Oversized sky blue Oxford cotton shirt styled with camel wide-leg wool pants and leather boots.',      colors: ['#ADD8E6','#C2B280','#5C4033','#FFFFFF'] },
        { title: 'Light Blue Resort Co-Ord',          img: IMG.summer,     notes: 'Light blue and white striped linen shirt styled over clean white tailored shorts and sandals.',       colors: ['#ADD8E6','#FFFFFF','#CCCCCC','#EAE6DF'] },
        { title: 'Soft Blue Denim Layering',          img: IMG.bratz,      notes: 'Light blue distressed denim midi skirt styled with a red crop top and chunky platform sandals.',     colors: ['#4B6F96','#FF0000','#FFC0CB','#0D0D0D'] },
        { title: 'Coastal Blue Summer Look',          img: IMG.summer,     notes: 'Sky blue silk wrap crop top paired with a clean white linen midi skirt and woven sandals.',          colors: ['#ADD8E6','#FFFFFF','#EAE6DF','#CCCCCC'] },
        { title: 'Light Blue Minimalist Fit',         img: IMG.clean,      notes: 'Soft sky blue cashmere crewneck sweater paired with clean white wide-leg linen pants.',              colors: ['#ADD8E6','#FFFFFF','#E1D9D1','#CCCCCC'] },
    ],
    'Red': [
        { title: 'Red Satin Celebration Dress',       img: IMG.barbie,     notes: 'Cherry red satin slip dress styled with a red velvet ribbon choker and red heels.',                  colors: ['#FF0000','#FFC0CB','#FFF0F5','#FFFFFF'] },
        { title: 'Scarlet Power Suit',                img: IMG.barbie,     notes: 'Vibrant scarlet red double-breasted suit blazer paired with matching red tailored trousers.',        colors: ['#FF0000','#FFFFFF','#CCCCCC','#1A1A1A'] },
        { title: 'Red Statement Evening Look',        img: IMG.barbie,     notes: 'Vibrant red pleated mini skirt styled with a white collared polo and white leather sneakers.',       colors: ['#FF0000','#FFFFFF','#CCCCCC','#111111'] },
        { title: 'Crimson Winter Layering',           img: IMG.barbie,     notes: 'Crimson red oversized cable-knit sweater paired with washed blue jeans and brown boots.',            colors: ['#FF0000','#4B6F96','#CCCCCC','#FFFFFF'] },
        { title: 'Monochrome Red Fashion Edit',       img: IMG.bratz,      notes: 'Cropped red leather moto jacket paired with red-accented cargo pants and high-top sneakers.',        colors: ['#FF0000','#0D0D0D','#CCCCCC','#FFFFFF'] },
    ],
    'Pink': [
        { title: 'Pink Coquette Cardigan Fit',        img: IMG.coquette,   notes: 'Pale pink cardigan adorned with small red satin bows down the front button placket.',                 colors: ['#FFC0CB','#FF0000','#FFF0F5','#FDF2F8'] },
        { title: 'Soft Blush Minimal Styling',        img: IMG.coquette,   notes: 'Blush pink silk slip skirt paired with a matching pale pink ribbed crop top and sandals.',            colors: ['#FFC0CB','#FFFDD0','#FFFFFF','#EAE6DF'] },
        { title: 'Hot Pink Fashion Statement',        img: IMG.barbie,     notes: 'Vibrant hot pink double-breasted suit blazer paired with matching hot pink tailored pants.',          colors: ['#FF1493','#FF69B4','#FFFFFF','#FF0000'] },
        { title: 'Rose-Tone Weekend Outfit',          img: IMG.coquette,   notes: 'Pale pink tulle party dress featuring red velvet shoulder ribbon bows and pink flats.',              colors: ['#FFC0CB','#FF0000','#FFF0F5','#FFFFFF'] },
        { title: 'Pink Monochrome Layering',          img: IMG.coquette,   notes: 'Pink ribbed wrap top paired with a cream linen midi slip skirt and pink hair ribbons.',               colors: ['#FFC0CB','#FFFDD0','#8FBC8F','#FDF2F8'] },
    ],
    'Yellow': [
        { title: 'Butter Yellow Summer Dress',        img: IMG.cottage,    notes: 'Cheerful butter yellow cotton eyelet maxi dress styled with a natural straw shoulder bag.',           colors: ['#FFD700','#FFFFFF','#FFFDD0','#D2B48C'] },
        { title: 'Mustard Knit Styling',              img: IMG.coastal,    notes: 'Bright mustard yellow patterned knit vest layered over a light blue Oxford button-down shirt.',      colors: ['#FFD700','#ADD8E6','#5C4033','#F0F0F0'] },
        { title: 'Sunshine Resort Outfit',            img: IMG.summer,     notes: 'Sunny yellow linen button-down shirt paired with matching yellow wide-leg utility shorts.',          colors: ['#FFD700','#FFFFFF','#EAE6DF','#C2B280'] },
        { title: 'Yellow Statement Streetwear',       img: IMG.y2k,        notes: 'Mustard yellow crop utility jacket paired with Y2K low-rise wide denim jeans and chain belt.',        colors: ['#FFD700','#4B6F96','#FFC0CB','#0D0D0D'] },
        { title: 'Golden Monochrome Fashion',         img: IMG.cottage,    notes: 'Golden suede fringe jacket layered over an ivory crochet knit top and yellow corduroy pants.',       colors: ['#FFD700','#FFFDD0','#8B5A2B','#40E0D0'] },
    ],
    'Royal Blue': [
        { title: 'Royal Blue Tailored Suit',          img: IMG.barbie,     notes: 'Tailored royal blue monochrome suit blazer paired with white crew socks and sneakers.',              colors: ['#4169E1','#FFFFFF','#CCCCCC','#1A1A1A'] },
        { title: 'Electric Blue Statement Look',      img: IMG.barbie,     notes: 'Royal blue monochrome pantsuit with a matching royal blue structured trench coat.',                  colors: ['#4169E1','#FFFFFF','#CCCCCC','#1A1A1A'] },
        { title: 'Blue Monochrome Power Outfit',      img: IMG.street,     notes: 'Oversized royal blue graphic crewneck sweatshirt paired with baggy blue windbreaker joggers.',        colors: ['#4169E1','#0D0D0D','#CCCCCC','#FFFFFF'] },
        { title: 'Sapphire Evening Styling',          img: IMG.barbie,     notes: 'Sleek royal blue satin slip dress paired with sapphire blue earrings and strappy heels.',            colors: ['#4169E1','#CCCCCC','#FFFFFF','#111111'] },
        { title: 'Royal Blue Editorial Fashion',      img: IMG.office,     notes: 'Tailored royal blue high-waisted trousers paired with a tucked white satin blouse.',                colors: ['#4169E1','#FFFFFF','#CCCCCC','#EAE6DF'] },
    ],
    'Purple': [
        { title: 'Lavender Ribbon Cardigan',          img: IMG.coquette,   notes: 'Lavender knit cardigan paired with a cream slip skirt and lavender satin ribbon bows.',               colors: ['#E6E6FA','#FFFDD0','#D4AF37','#9370DB'] },
        { title: 'Plum Velvet Evening Look',          img: IMG.dark_acad,  notes: 'Rich plum velvet slip dress with black lace trim and chunky black velvet platform heels.',            colors: ['#3A0033','#000000','#808080','#800020'] },
        { title: 'Purple Monochrome Styling',         img: IMG.dark_acad,  notes: 'Plum cable knit vest layered over a purple collared shirt and dark wash denim jeans.',                colors: ['#3A0033','#808080','#1A1A1A','#FFFFFF'] },
        { title: 'Lilac Spring Fashion Edit',         img: IMG.summer,     notes: 'Soft lilac/lavender linen midi sundress styled with a woven straw hat and pearl jewelry.',           colors: ['#E6E6FA','#FFFFFF','#FFFDD0','#D2B48C'] },
        { title: 'Deep Purple Winter Layers',         img: IMG.dark_acad,  notes: 'Burgundy velvet dress with dramatic sheer bell sleeves layered under a deep purple duster coat.',    colors: ['#800020','#FFFDD0','#3A0033','#1A1A1A'] },
    ],
};

// ─── 5. COLOR COMBINATIONS ────────────────────────────────────────────────
const combosBoards = {
    'Black + Beige': [
        { title: 'Black Blazer & Beige Wide-Leg Trousers', img: IMG.minimalist, notes: 'Structured black double-breasted blazer with beige wide-leg tailored trousers.', colors: ['#0D0D0D','#D2B48C','#FFFFFF','#CCCCCC'] },
        { title: 'Beige Trench & Black Boots', img: IMG.minimalist, notes: 'Classic beige double-breasted trench coat paired with structured black leather boots.', colors: ['#C2B280','#0D0D0D','#FFFFFF','#EAE6DF'] },
        { title: 'Black Knit & Beige Midi Skirt', img: IMG.minimalist, notes: 'Soft black crewneck knit sweater paired with a flowing beige satin midi skirt.', colors: ['#0D0D0D','#D2B48C','#EAE6DF','#FFFFFF'] },
        { title: 'Black Streetwear Cargo & Camel Jacket', img: IMG.street, notes: 'Black ripstop cargo trousers styled with a warm camel utility outerwear jacket.', colors: ['#0D0D0D','#C2B280','#CCCCCC','#1F1F1F'] },
        { title: 'Minimal Black & Sand Capsule', img: IMG.capsule, notes: 'Clean black mockneck top paired with high-waisted sand trousers for a minimal look.', colors: ['#0D0D0D','#E1D9D1','#FFFFFF','#CCCCCC'] }
    ],
    'Burgundy + Cream': [
        { title: 'Burgundy Silk Dress & Cream Blazer', img: IMG.old_money, notes: 'Elegant burgundy silk midi dress paired with an oversized cream blazer.', colors: ['#800020','#FFFDD0','#D4AF37','#FFFFFF'] },
        { title: 'Burgundy Knit & Cream Trousers', img: IMG.winter, notes: 'Burgundy cable-knit sweater styled with off-white cream tailored pants.', colors: ['#800020','#FFFDD0','#FFFFFF','#CCCCCC'] },
        { title: 'Cream Coat with Burgundy Accessories', img: IMG.winter, notes: 'Structured cream wool coat styled with a burgundy leather handbag and scarf.', colors: ['#FFFDD0','#800020','#D2B48C','#1A1817'] },
        { title: 'Burgundy Velvet Evening Styling', img: IMG.winter, notes: 'Deep burgundy velvet dress paired with cream strappy heels for evening glam.', colors: ['#800020','#FFFDD0','#CCCCCC','#0D0D0D'] },
        { title: 'Burgundy Date Night Ensemble', img: IMG.date_night, notes: 'Burgundy silk camisole tucked into cream wide-leg trousers for a date night.', colors: ['#800020','#FFFFFF','#D2B48C','#CCCCCC'] }
    ],
    'Chocolate Brown + Cream': [
        { title: 'Chocolate Trench & Cream Turtleneck', img: IMG.dark_acad, notes: 'Chocolate brown wool trench coat layered over a cream cashmere turtleneck.', colors: ['#5C4033','#F5F5DC','#FFFFFF','#8B5A2B'] },
        { title: 'Brown Knit & Cream Wide-Leg Pants', img: IMG.dark_acad, notes: 'Earthy brown patterned knit sweater styled with cream linen wide-leg pants.', colors: ['#5C4033','#F5F5DC','#C2B280','#FFFFFF'] },
        { title: 'Espresso Wool Coat Styling', img: IMG.cafe_date, notes: 'Espresso wool overcoat layered over an ivory crewneck knit and tan chinos.', colors: ['#5C4033','#FFFDD0','#D2B48C','#0D0D0D'] },
        { title: 'Cream Cashmere & Brown Boots', img: IMG.cafe_date, notes: 'Soft cream cashmere knitwear paired with chocolate brown leather riding boots.', colors: ['#FFFDD0','#5C4033','#8B5A2B','#FFFFFF'] },
        { title: 'Mocha Winter Layering', img: IMG.cafe_date, notes: 'Mocha brown blazer layered over a cream mockneck knit and brown trousers.', colors: ['#5C4033','#FFFDD0','#8B5A2B','#CCCCCC'] }
    ],
    'Navy + White': [
        { title: 'Navy Blazer & White Linen Polo', img: IMG.old_money, notes: 'Classic double-breasted navy blazer styled with a crisp white linen knit polo.', colors: ['#0B1D3A','#FFFFFF','#D4AF37','#D2B48C'] },
        { title: 'Coastal Navy Summer Styling', img: IMG.old_money, notes: 'Navy striped crewneck sweater styled with white linen summer shorts.', colors: ['#0B1D3A','#FFFFFF','#CCCCCC','#E1D9D1'] },
        { title: 'White Shirt & Navy Trousers', img: IMG.old_money, notes: 'White oxford button-down shirt paired with tailored navy blue wool trousers.', colors: ['#FFFFFF','#0B1D3A','#CCCCCC','#EAE6DF'] },
        { title: 'Yacht Club Capsule Wardrobe', img: IMG.old_money, notes: 'Navy knit polo paired with white tailored trousers and gold crest details.', colors: ['#0B1D3A','#FFFFFF','#D4AF37','#CCCCCC'] },
        { title: 'Navy Knit & White Denim', img: IMG.old_money, notes: 'Cozy navy blue cable-knit sweater styled with straight-leg white denim jeans.', colors: ['#0B1D3A','#FFFFFF','#EAE6DF','#CCCCCC'] }
    ],
    'Sage Green + Cream': [
        { title: 'Sage Linen Dress & Cream Cardigan', img: IMG.cottage, notes: 'Sage green gingham maxi linen dress paired with a soft cream knit cardigan.', colors: ['#8FBC8F','#FFFDD0','#8B5A2B','#FFFFFF'] },
        { title: 'Cream Knit with Sage Trousers', img: IMG.cottage, notes: 'Cream ribbed knit sweater paired with tailored sage green high-waisted trousers.', colors: ['#FFFDD0','#8FBC8F','#FFFFFF','#CCCCCC'] },
        { title: 'Cottagecore Sage Layering', img: IMG.cottage, notes: 'Sage wrap top paired with a cream slip skirt and delicate cottagecore details.', colors: ['#8FBC8F','#FFFDD0','#FFC0CB','#FFFFFF'] },
        { title: 'Sage Utility Jacket Styling', img: IMG.street, notes: 'Sage green utility jacket layered over a cream tee and beige cargo pants.', colors: ['#8FBC8F','#FFFDD0','#D2B48C','#1F1F1F'] },
        { title: 'Soft Green Spring Capsule', img: IMG.cottage, notes: 'Light sage knit vest layered over a cream blouse with cream straight trousers.', colors: ['#8FBC8F','#FFFDD0','#CCCCCC','#FFFFFF'] }
    ],
    'White + Light Blue': [
        { title: 'White Shirt & Sky Blue Trousers', img: IMG.clean, notes: 'Crisp white cotton shirt styled with sky blue wide-leg tailored trousers.', colors: ['#FFFFFF','#ADD8E6','#C2B280','#CCCCCC'] },
        { title: 'Coastal Vacation Styling', img: IMG.summer, notes: 'Light blue and white striped linen shirt styled over white linen shorts.', colors: ['#ADD8E6','#FFFFFF','#CCCCCC','#EAE6DF'] },
        { title: 'Blue Linen Resort Set', img: IMG.summer, notes: 'Sky blue linen button-down shirt paired with matching blue resort shorts.', colors: ['#ADD8E6','#FFFFFF','#EAE6DF','#CCCCCC'] },
        { title: 'White Summer Sundress', img: IMG.summer, notes: 'Breezy white summer sundress styled with sky blue satin hair ribbons.', colors: ['#FFFFFF','#ADD8E6','#FFFDD0','#CCCCCC'] },
        { title: 'Soft Blue Capsule Outfit', img: IMG.clean, notes: 'Soft sky blue cashmere sweater paired with clean white wide-leg trousers.', colors: ['#ADD8E6','#FFFFFF','#E1D9D1','#CCCCCC'] }
    ],
    'Brown + Sky Blue': [
        { title: 'Brown Blazer & Sky Blue Oxford', img: IMG.coastal, notes: 'Tailored brown wool blazer over a sky blue Oxford cotton button-down.', colors: ['#5C4033','#ADD8E6','#F5F5DC','#2E8B57'] },
        { title: 'Soft Blue Denim & Mocha Knit', img: IMG.coastal, notes: 'Light blue denim jeans styled with a cozy mocha brown ribbed knit sweater.', colors: ['#ADD8E6','#5C4033','#FFFDD0','#8B5A2B'] },
        { title: 'Autumn Weekend Styling', img: IMG.coastal, notes: 'Brown suede jacket layered over a sky blue shirt and beige chino trousers.', colors: ['#C2B280','#ADD8E6','#5C4033','#FFFDD0'] },
        { title: 'Brown Wool Layers & Blue Shirt', img: IMG.coastal, notes: 'Patterned brown wool vest styled with a sky blue button-down shirt.', colors: ['#5C4033','#ADD8E6','#FFFDD0','#D4AF37'] },
        { title: 'Vintage Inspired Layering', img: IMG.coastal, notes: 'Brown corduroy blazer styled with a sky blue knit polo shirt.', colors: ['#C2B280','#ADD8E6','#5C4033','#FFFDD0'] }
    ],
    'Gray + Burgundy': [
        { title: 'Burgundy Coat & Gray Trousers', img: IMG.winter, notes: 'Oversized burgundy wool coat paired with dark grey tailored trousers.', colors: ['#800020','#808080','#FFFFFF','#0D0D0D'] },
        { title: 'Corporate Burgundy Styling', img: IMG.office, notes: 'Tailored grey suit blazer paired with a deep burgundy silk blouse.', colors: ['#808080','#800020','#FFFFFF','#CCCCCC'] },
        { title: 'Gray Knit with Burgundy Skirt', img: IMG.office, notes: 'Charcoal grey knit sweater paired with a flowing burgundy midi skirt.', colors: ['#808080','#800020','#1A1A1A','#FFFFFF'] },
        { title: 'Winter Editorial Layering', img: IMG.winter, notes: 'Charcoal grey trench coat styled over a burgundy knit turtlneck dress.', colors: ['#555555','#800020','#FFFFFF','#CCCCCC'] },
        { title: 'Burgundy Office Capsule', img: IMG.office, notes: 'Grey blazer paired with a burgundy structured leather tote and slacks.', colors: ['#808080','#800020','#FFFFFF','#2B2B2B'] }
    ],
    'Red + Pink': [
        { title: 'Hot Pink Power Suit', img: IMG.barbie, notes: 'Vibrant hot pink double-breasted suit blazer with matching hot pink pants.', colors: ['#FF1493','#FF69B4','#FFFFFF','#FF0000'] },
        { title: 'Red Satin Celebration Dress', img: IMG.barbie, notes: 'Cherry red satin slip dress styled with a pink velvet ribbon choker.', colors: ['#FF0000','#FFC0CB','#FFF0F5','#FFFFFF'] },
        { title: 'Pink Monochrome Layering', img: IMG.coquette, notes: 'Pink ribbed wrap top paired with a pink linen midi slip skirt.', colors: ['#FFC0CB','#FFF0F5','#FFFFFF','#FDF2F8'] },
        { title: 'Valentine\'s Inspired Styling', img: IMG.coquette, notes: 'Red open cardigan paired with a blush pink satin midi slip skirt.', colors: ['#FF0000','#FFC0CB','#FFF0F5','#FFFFFF'] },
        { title: 'Statement Event Outfit', img: IMG.barbie, notes: 'Vibrant red blazer paired with a hot pink crewneck sweater and trousers.', colors: ['#FF0000','#FF1493','#FF69B4','#FFFFFF'] }
    ],
    'Black + Silver': [
        { title: 'Black Leather Moto Styling', img: IMG.street, notes: 'Black leather moto jacket styled with silver metal hardware and chains.', colors: ['#0D0D0D','#CCCCCC','#1F1F1F','#808080'] },
        { title: 'Silver Metallic Evening Look', img: IMG.y2k, notes: 'Sleek black tank top styled with silver metallic wide-leg trousers.', colors: ['#0D0D0D','#C0C0C0','#FFFFFF','#808080'] },
        { title: 'Concert Ready Monochrome Outfit', img: IMG.street, notes: 'Oversized black graphic hoodie with chunky silver statement necklaces.', colors: ['#0D0D0D','#CCCCCC','#555555','#FFFFFF'] },
        { title: 'Black Utility Fashion Edit', img: IMG.street, notes: 'Black cargos styled with a heavy silver metal-buckle utility belt.', colors: ['#0D0D0D','#CCCCCC','#1A1A1A','#808080'] },
        { title: 'Cyberpunk Party Styling', img: IMG.y2k, notes: 'Asymmetrical black technical top styled with silver jewelry and accents.', colors: ['#0D0D0D','#CCCCCC','#FFFFFF','#1F1F1F'] }
    ],
    'Ivory + Camel': [
        { title: 'Camel Wool Coat & Ivory Knit', img: IMG.minimalist, notes: 'Structured camel wool trench coat layered over an ivory cashmere sweater.', colors: ['#C2B280','#FFFDD0','#D2B48C','#FFFFFF'] },
        { title: 'Quiet Luxury Winter Styling', img: IMG.minimalist, notes: 'Camel hair coat paired with a warm ivory wrap midi skirt and boots.', colors: ['#C2B280','#FFFDD0','#D4AF37','#FFFFFF'] },
        { title: 'Ivory Tailored Trousers', img: IMG.minimalist, notes: 'High-waisted ivory tailored trousers styled with a camel knit vest.', colors: ['#FFFDD0','#C2B280','#EAE6DF','#8B5A2B'] },
        { title: 'European Travel Capsule', img: IMG.summer, notes: 'Camel wool blazer styled with an ivory linen button-down and trousers.', colors: ['#C2B280','#FFFDD0','#EAE6DF','#FFFFFF'] },
        { title: 'Neutral Luxe Layering', img: IMG.minimalist, notes: 'Ivory cashmere turtleneck sweater paired with tailored camel slacks.', colors: ['#FFFDD0','#C2B280','#FFFFFF','#CCCCCC'] }
    ],
    'Olive + Black': [
        { title: 'Olive Utility Jacket & Black Cargo', img: IMG.street, notes: 'Olive green utility cargo vest layered over an oversized black graphic tee.', colors: ['#556B2F','#0D0D0D','#CCCCCC','#1F1F1F'] },
        { title: 'Streetwear Tactical Styling', img: IMG.street, notes: 'Waterproof olive shell jacket paired with black utility cargo pants.', colors: ['#556B2F','#0D0D0D','#1A1A1A','#808080'] },
        { title: 'Gorpcore Layered Outfit', img: IMG.street, notes: 'Water-resistant olive shell jacket paired with black ripstop trail pants.', colors: ['#556B2F','#0D0D0D','#CCCCCC','#1F1F1F'] },
        { title: 'Black Knit & Olive Trousers', img: IMG.street, notes: 'Olive green cable-knit crewneck sweater styled with black slim-fit jeans.', colors: ['#556B2F','#0D0D0D','#CCCCCC','#FFFFFF'] },
        { title: 'Outdoor Capsule Wardrobe', img: IMG.street, notes: 'Olive green utility parka coat paired with black lace-up combat boots.', colors: ['#556B2F','#0D0D0D','#808080','#FFFFFF'] }
    ],
    'Navy + Tan': [
        { title: 'Navy Blazer & Tan Chinos', img: IMG.old_money, notes: 'Double-breasted navy crest blazer styled with tailored tan chinos.', colors: ['#0B1D3A','#D2B48C','#D4AF37','#FFFFFF'] },
        { title: 'Coastal Gentleman Styling', img: IMG.old_money, notes: 'Navy striped crewneck sweater styled with tan linen shorts and loafers.', colors: ['#0B1D3A','#D2B48C','#FFFFFF','#CCCCCC'] },
        { title: 'Travel Capsule Outfit', img: IMG.old_money, notes: 'Navy wool sweater paired with tan corduroy utility trousers.', colors: ['#0B1D3A','#D2B48C','#111111','#FFFDD0'] },
        { title: 'Navy Knit & Camel Coat', img: IMG.old_money, notes: 'Navy blue ribbed knit cardigan paired with a classic camel trench coat.', colors: ['#0B1D3A','#C2B280','#EAE6DF','#FFFFFF'] },
        { title: 'Old Money Inspired Layering', img: IMG.old_money, notes: 'Navy preppy sweater vest layered over a white shirt and tan trousers.', colors: ['#0B1D3A','#D2B48C','#FFFFFF','#CCCCCC'] }
    ],
    'Cream + Chocolate': [
        { title: 'Cream Cashmere & Chocolate Coat', img: IMG.capsule, notes: 'Cream cashmere crewneck sweater styled under a chocolate brown trench coat.', colors: ['#FFFDD0','#5C4033','#E1D9D1','#FFFFFF'] },
        { title: 'Winter Coffee-Tone Styling', img: IMG.clean, notes: 'Cream linen dress styled with rich chocolate brown suede loafers.', colors: ['#FFFDD0','#5C4033','#EAE6DF','#FFFFFF'] },
        { title: 'Cozy Knit Weekend Outfit', img: IMG.coastal, notes: 'Cream corduroy trousers paired with a chocolate brown patterned knit.', colors: ['#FFFDD0','#5C4033','#F5F5DC','#C2B280'] },
        { title: 'Neutral Layering Capsule', img: IMG.clean, notes: 'Cream crewneck sweater styled under a rich chocolate brown wool coat.', colors: ['#FFFDD0','#5C4033','#C2B280','#FFFFFF'] },
        { title: 'Rich Brown Luxe Styling', img: IMG.dark_acad, notes: 'Cream button-down shirt paired with a chocolate brown knit sweater vest.', colors: ['#FFFDD0','#5C4033','#8B5A2B','#FFFFFF'] }
    ],
    'Plum + Gray': [
        { title: 'Plum Velvet Evening Styling', img: IMG.dark_acad, notes: 'Deep plum velvet maxi skirt combined with grey platform ankle boots.', colors: ['#3A0033','#808080','#000000','#800020'] },
        { title: 'Gray Tailored Winter Outfit', img: IMG.dark_acad, notes: 'Plum cable-knit turtleneck sweater with a grey herringbone blazer.', colors: ['#3A0033','#808080','#FFFDD0','#1A1A1A'] },
        { title: 'Whimsigoth Editorial Layering', img: IMG.dark_acad, notes: 'Deep plum slip dress with a grey wool structured trench coat.', colors: ['#3A0033','#808080','#0D0D0D','#800020'] },
        { title: 'Purple Knit & Gray Trousers', img: IMG.dark_acad, notes: 'Plum cable-knit vest layered over a slate grey collared shirt.', colors: ['#3A0033','#808080','#1A1A1A','#FFFFFF'] },
        { title: 'Deep Winter Fashion Edit', img: IMG.dark_acad, notes: 'Plum velvet slip dress styled with a grey knit wrap cardigan.', colors: ['#3A0033','#808080','#FFFDD0','#0D0D0D'] }
    ]
};

// ─── Compile into flat array ───────────────────────────────────────────────
const curatedInspiration = [];
let idx = 1;

function push(card, type, boardName) {
    curatedInspiration.push({
        id: `insp_${idx++}`,
        title: card.title,
        image: card.img,
        pinterestUrl: `https://www.pinterest.com/search/pins/?q=${encodeURIComponent(card.title + " outfit")}`,
        aesthetic:        type === 'aesthetic'   ? boardName : '',
        styleMovement:    type === 'movement'    ? boardName : '',
        occasion:         type === 'occasion'    ? boardName : '',
        colorStory:       type === 'colorStory'  ? boardName : '',
        colorCombination: type === 'colorCombination' ? boardName : '',
        boardType:        type,
        boardName:        boardName,
        notes: card.notes,
        colors: card.colors,
    });
}

Object.entries(aestheticsBoards).forEach(([board, cards]) =>
    cards.forEach(c => push(c, 'aesthetic', board))
);
Object.entries(movementsBoards).forEach(([board, cards]) =>
    cards.forEach(c => push(c, 'movement', board))
);
Object.entries(occasionsBoards).forEach(([board, cards]) =>
    cards.forEach(c => push(c, 'occasion', board))
);
Object.entries(colorStoriesBoards).forEach(([board, cards]) =>
    cards.forEach(c => push(c, 'colorStory', board))
);
Object.entries(combosBoards).forEach(([board, cards]) =>
    cards.forEach(c => push(c, 'colorCombination', board))
);

module.exports = curatedInspiration;
