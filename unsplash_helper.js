/**
 * unsplash_helper.js
 *
 * Strategy:
 *  1. On boot, load unsplash_resolved_cards.json (built by resolve_images.js).
 *  2. `applyUnsplashImages(dataset)` maps each card to its resolved Unsplash photo.
 *  3. If a card is not yet in the cache, fall back to board-specific curated photo IDs
 *     (one unique fallback pool per board, not just 16 generic categories).
 *  4. `initializeUnsplashImages(dataset)` wires everything together and kicks off
 *     a background re-resolver for any still-missing cards.
 */

const https = require('https');
const fs    = require('fs');
const path  = require('path');

// ─── Board-specific curated fallback photo pools ──────────────────────────────
// Each key matches `card.boardName` from the dataset.
const BOARD_FALLBACKS = {
        '1595959183075-c1d09e7c991a','1549298916-b41d501d3772',
    ],
    'Plum + Gray': [
        '1548624313-0396c75e4b1a','1576158113928-4c240eaaf360',
        '1507679799987-c73779587ccf','1599643478518-878f73fbf50b',
        '1516762681021-a53b45c20b85','1617627143724-4a2122ab69e4',
        '1603403212352-79ad83860ef7','1585487000160-6e6503c6a79e',
    ],
};

// ─── Cache & Helpers ─────────────────────────────────────────────────────────
const cacheFilePath = path.join(__dirname, 'unsplash_resolved_cards.json');
let cardCache = {};

function loadCacheFromDisk() {
    try {
        if (fs.existsSync(cacheFilePath)) {
            cardCache = JSON.parse(fs.readFileSync(cacheFilePath, 'utf8'));
            console.log(`[Unsplash] Loaded ${Object.keys(cardCache).length} pre-resolved card images.`);
        }
    } catch (e) {
        console.warn('[Unsplash] Could not load cache:', e.message);
        cardCache = {};
    }
}

const GARMENT_RULES = [
    {
        name: 'knit vest',
        detect: (tokens, text) => (tokens.includes('vest') && tokens.includes('knit')) || text.includes('knit vest') || text.includes('knitted vest'),
        validate: (photoText) => {
            const hasVest = ['vest', 'waistcoat', 'gilet'].some(w => photoText.includes(w));
            const hasKnit = ['knit', 'knitted', 'cable', 'knitwear', 'crochet', 'wool'].some(w => photoText.includes(w));
            return hasVest && hasKnit;
        }
    },
    {
        name: 'trench coat',
        detect: (tokens, text) => (tokens.includes('trench') && tokens.includes('coat')) || text.includes('trench coat'),
        validate: (photoText) => {
            const hasTrench = photoText.includes('trench');
            const hasCoat = ['coat', 'overcoat', 'jacket', 'outerwear'].some(w => photoText.includes(w));
            return hasTrench && hasCoat;
        }
    },
    {
        name: 'cargo pants',
        detect: (tokens, text) => (tokens.includes('cargo') && (tokens.includes('pants') || tokens.includes('trousers') || tokens.includes('jeans'))),
        validate: (photoText) => {
            const hasCargo = ['cargo', 'cargos', 'utility', 'tactical'].some(w => photoText.includes(w));
            const hasPants = ['pants', 'trousers', 'jeans', 'slacks', 'tracksuit', 'joggers'].some(w => photoText.includes(w));
            return hasCargo && hasPants;
        }
    },
    {
        name: 'ballet flats',
        detect: (tokens, text) => tokens.includes('flats') || tokens.includes('flat') || tokens.includes('ballerina') || text.includes('ballet flats'),
        validate: (photoText) => {
            const hasFlat = ['flat', 'flats', 'ballerina', 'ballet'].some(w => photoText.includes(w));
            const hasShoes = ['shoes', 'footwear', 'pumps', 'slippers'].some(w => photoText.includes(w));
            return hasFlat && hasShoes;
        }
    },
    {
        name: 'combat boots',
        detect: (tokens, text) => tokens.includes('boots') && tokens.includes('combat'),
        validate: (photoText) => {
            const hasCombat = ['combat', 'tactical', 'military', 'lug', 'leather'].some(w => photoText.includes(w));
            const hasBoots = ['boots', 'boot', 'footwear'].some(w => photoText.includes(w));
            return hasCombat && hasBoots;
        }
    },
    {
        name: 'slip dress',
        detect: (tokens, text) => tokens.includes('slip') && tokens.includes('dress'),
        validate: (photoText) => {
            const hasSlip = ['slip', 'silk', 'satin'].some(w => photoText.includes(w));
            const hasDress = ['dress', 'gown', 'sundress'].some(w => photoText.includes(w));
            return hasSlip && hasDress;
        }
    },
    {
        name: 'vest',
        detect: (tokens) => tokens.includes('vest'),
        validate: (photoText) => ['vest', 'waistcoat', 'gilet'].some(w => photoText.includes(w))
    },
    {
        name: 'cardigan',
        detect: (tokens) => tokens.includes('cardigan'),
        validate: (photoText) => ['cardigan', 'knitwear', 'sweater', 'knitted'].some(w => photoText.includes(w))
    },
    {
        name: 'hoodie',
        detect: (tokens) => tokens.includes('hoodie'),
        validate: (photoText) => ['hoodie', 'hooded', 'sweatshirt'].some(w => photoText.includes(w))
    },
    {
        name: 'loafers',
        detect: (tokens) => tokens.includes('loafers') || tokens.includes('loafer'),
        validate: (photoText) => ['loafers', 'loafer', 'shoes', 'footwear', 'oxford', 'oxfords', 'derby'].some(w => photoText.includes(w))
    },
    {
        name: 'dress',
        detect: (tokens) => tokens.includes('dress') || tokens.includes('sundress') || tokens.includes('gown'),
        validate: (photoText) => ['dress', 'gown', 'sundress', 'slip', 'jumpsuit'].some(w => photoText.includes(w))
    },
    {
        name: 'skirt',
        detect: (tokens) => tokens.includes('skirt'),
        validate: (photoText) => ['skirt', 'midi', 'mini', 'maxi', 'tulle'].some(w => photoText.includes(w))
    },
    {
        name: 'boots',
        detect: (tokens) => tokens.includes('boots') || tokens.includes('boot'),
        validate: (photoText) => ['boots', 'boot', 'footwear'].some(w => photoText.includes(w))
    },
    {
        name: 'sneakers',
        detect: (tokens) => tokens.includes('sneakers') || tokens.includes('sneaker') || tokens.includes('trainers'),
        validate: (photoText) => ['sneakers', 'sneaker', 'trainers', 'shoes', 'footwear'].some(w => photoText.includes(w))
    },
    {
        name: 'blazer',
        detect: (tokens) => tokens.includes('blazer'),
        validate: (photoText) => ['blazer', 'suit', 'jacket', 'tailored'].some(w => photoText.includes(w))
    },
    {
        name: 'trousers',
        detect: (tokens) => ['trousers', 'pants', 'chinos', 'jeans', 'corduroys', 'slacks', 'cargos', 'cargo', 'joggers'].some(w => tokens.includes(w)),
        validate: (photoText) => ['trousers', 'pants', 'chinos', 'jeans', 'denim', 'cargos', 'cargo', 'slacks', 'corduroys', 'joggers'].some(w => photoText.includes(w))
    },
    {
        name: 'coat',
        detect: (tokens) => ['coat', 'overcoat', 'parka', 'duster'].some(w => tokens.includes(w)),
        validate: (photoText) => ['coat', 'trench', 'overcoat', 'parka', 'duster', 'jacket', 'outerwear'].some(w => photoText.includes(w))
    },
    {
        name: 'jacket',
        detect: (tokens) => ['jacket', 'windbreaker', 'fleece'].some(w => tokens.includes(w)),
        validate: (photoText) => ['jacket', 'outerwear', 'windbreaker', 'bomber', 'fleece', 'parka', 'coat'].some(w => photoText.includes(w))
    },
    {
        name: 'shirt',
        detect: (tokens) => ['shirt', 'button-down', 'oxford', 'blouse'].some(w => tokens.includes(w)),
        validate: (photoText) => ['shirt', 'button-down', 'oxford', 'blouse', 'tunic', 'top'].some(w => photoText.includes(w))
    },
    {
        name: 'top',
        detect: (tokens) => ['top', 'tee', 'tank', 'camisole', 'corset', 'bustier', 'tunic'].some(w => tokens.includes(w)),
        validate: (photoText) => ['top', 'shirt', 'blouse', 'tee', 'tank', 'camisole', 'corset', 'bustier', 'tunic'].some(w => photoText.includes(w))
    },
];

function extractGarmentKeywords(title) {
    const titleLower = title.toLowerCase();
    const titleTokens = titleLower.replace(/[^a-z0-9\s]/g, ' ').split(/\s+/);
    const keywords = [];

    const mappings = {
        'blazer': 'blazer suit jacket',
        'loafers': 'loafers shoes',
        'loafer': 'loafers shoes',
        'corduroys': 'corduroy pants',
        'corduroy': 'corduroy pants',
        'cargo': 'cargo pants',
        'cargos': 'cargo pants',
        'hoodie': 'oversized hoodie',
        'vest': 'knit vest',
        'trench': 'trench coat',
        'cardigan': 'cardigan sweater',
        'dress': 'dress fashion',
        'sundress': 'dress fashion',
        'skirt': 'skirt fashion',
        'boots': 'boots footwear',
        'boot': 'boots footwear',
        'sneakers': 'sneakers footwear',
        'sneaker': 'sneakers footwear',
        'coat': 'coat jacket',
        'jacket': 'jacket coat',
        'sweater': 'sweater knitwear',
        'pants': 'pants trousers',
        'trousers': 'trousers pants',
        'jeans': 'jeans denim',
    };

    for (const key of Object.keys(mappings)) {
        if (titleTokens.includes(key)) {
            keywords.push(mappings[key]);
        }
    }
    
    if (keywords.length === 0) return '';
    const words = [];
    const seen = new Set();
    keywords.join(' ').split(/\s+/).forEach(w => {
        if (w && !seen.has(w)) {
            seen.add(w);
            words.push(w);
        }
    });
    return words.join(' ');
}

function getQueries(card) {
    const title = card.title;
    const aes = card.aesthetic || card.styleMovement || '';
    const col = card.colorStory || card.colorCombination || '';
    const occ = card.occasion || '';
    const notes = card.notes ? card.notes.split(/[.—]/)[0] : '';
    
    const garmentKeywords = extractGarmentKeywords(title);

    const attempts = [];
    let q1 = title;
    if (garmentKeywords) {
        if (title.toLowerCase().includes('shell jacket')) {
            q1 = `${title} technical shell jacket outdoor fashion`;
        } else {
            q1 = `${title} ${garmentKeywords} fashion outfit`;
        }
    } else {
        q1 = `${title} fashion outfit`;
    }
    attempts.push({ label: 'Attempt 1 (Title + Garments)', query: q1 });
    if (notes) {
        attempts.push({ label: 'Attempt 2 (Title + Notes)', query: `${title} ${notes}` });
    }
    if (aes) {
        attempts.push({ label: 'Attempt 3 (Title + Aesthetic)', query: `${title} ${aes}` });
    }
    if (occ) {
        attempts.push({ label: 'Attempt 4 (Title + Occasion)', query: `${title} ${occ}` });
    }
    return attempts;
}

function cleanQuery(queryStr) {
    if (!queryStr) return '';
    let clean = queryStr.toLowerCase().replace(/[&+/\-]/g, ' ');
    const words = [];
    const seen = new Set();
    clean.split(/\s+/).forEach(w => {
        if (w && !seen.has(w) && w !== 'look' && w !== 'fit' && w !== 'style' && w !== 'board' && w !== 'combo') {
            seen.add(w);
            words.push(w);
        }
    });
    return words.join(' ');
}

function validatePhoto(photo, card) {
    if (!photo) return false;
    
    const photoText = [
        photo.description || '',
        photo.alt_description || '',
        (photo.tags || []).map(t => t.title || '').join(' '),
        (photo.tags_preview || []).map(t => t.title || '').join(' ')
    ].join(' ').toLowerCase();

    const fashionWords = ['fashion', 'apparel', 'clothing', 'outfit', 'wear', 'streetwear', 'style', 'model', 'person', 'human', 'woman', 'man', 'dressed', 'garment', 'look', 'fit', 'aesthetic', 'chic'];
    const hasFashion = fashionWords.some(w => photoText.includes(w));
    if (!hasFashion) {
        return false;
    }

    const rejectWords = ['landscape', 'architecture', 'building', 'food', 'dish', 'recipe', 'interior', 'scenery', 'furniture'];
    const hasReject = rejectWords.some(w => photoText.includes(w));
    if (hasReject) {
        const isModel = ['person', 'human', 'woman', 'man', 'model', 'portrait'].some(w => photoText.includes(w));
        if (!isModel) {
            return false;
        }
    }

    const titleLower = card.title.toLowerCase();
    const notesLower = (card.notes || '').toLowerCase();
    const combinedText = titleLower + ' ' + notesLower;
    const textTokens = combinedText.replace(/[^a-z0-9\s]/g, ' ').split(/\s+/);
    
    let rulesApplied = 0;
    let rulesPassed = 0;
    
    for (const rule of GARMENT_RULES) {
        if (rule.detect(textTokens, combinedText)) {
            rulesApplied++;
            if (rule.validate(photoText)) {
                rulesPassed++;
            }
        }
    }
    
    if (rulesApplied > 0 && rulesPassed === 0) {
        return false;
    }

    if (textTokens.includes('vest') && !textTokens.includes('dress') && !textTokens.includes('skirt')) {
        if (photoText.includes('dress') || photoText.includes('gown') || photoText.includes('skirt')) {
            if (!photoText.includes('vest') && !photoText.includes('waistcoat') && !photoText.includes('gilet')) {
                return false;
            }
        }
    }

    if (['pants', 'trousers', 'jeans', 'corduroys', 'cargo', 'chinos', 'slacks', 'shorts'].some(w => textTokens.includes(w))) {
        const isFaceOnly = ['face', 'makeup', 'lips', 'headshot', 'portrait close up'].some(w => photoText.includes(w));
        const hasPants = ['pants', 'trousers', 'jeans', 'denim', 'cargos', 'cargo', 'slacks', 'corduroys', 'legs', 'footwear', 'shoes', 'boots'].some(w => photoText.includes(w));
        if (isFaceOnly && !hasPants) {
            return false;
        }
    }

    return true;
}

// ─── Background resolver (runs after initial paint) ─────────────────────────
function fetchPhotosForQuery(query) {
    return new Promise(resolve => {
        const ACCESS_KEY = process.env.UNSPLASH_ACCESS_KEY;
        const useOfficial = !!ACCESS_KEY;
        const url = useOfficial 
            ? `https://api.unsplash.com/search/photos?query=${encodeURIComponent(query)}&per_page=6&orientation=portrait&client_id=${ACCESS_KEY}`
            : `https://unsplash.com/napi/search/photos?query=${encodeURIComponent(query)}&per_page=6&orientation=portrait`;
            
        const req = https.get(url, {
            headers: {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/120 Safari/537.36',
                'Accept': 'application/json',
            }
        }, res => {
            if (res.statusCode !== 200) return resolve([]);
            let body = '';
            res.on('data', c => body += c);
            res.on('end', () => {
                try {
                    const data = JSON.parse(body);
                    resolve(data.results || []);
                } catch { resolve([]); }
            });
        });
        req.on('error', () => resolve([]));
        req.setTimeout(4000, () => { req.destroy(); resolve([]); });
    });
}

async function resolveAllCards(dataset) {
    const queue = dataset.filter(c => !cardCache[c.title]);
    if (queue.length === 0) return;

    console.log(`[Unsplash] Background-resolving ${queue.length} cards…`);
    const usedIds = new Set(Object.values(cardCache));

    const BATCH = 4;
    for (let i = 0; i < queue.length; i += BATCH) {
        const batch = queue.slice(i, i + BATCH);
        await Promise.all(batch.map(async card => {
            const attempts = getQueries(card);
            let chosenPhoto = null;
            
            try {
                for (const attempt of attempts) {
                    const cleanedQ = cleanQuery(attempt.query);
                    if (!cleanedQ) continue;
                    
                    let photos = await fetchPhotosForQuery(cleanedQ);
                    
                    for (const photo of photos) {
                        if (!usedIds.has(photo.id) && validatePhoto(photo, card)) {
                            chosenPhoto = photo;
                            break;
                        }
                    }
                    if (chosenPhoto) break;
                    await sleep(150);
                }
                
                if (!chosenPhoto) {
                    const pool = BOARD_FALLBACKS[card.boardName] || BOARD_FALLBACKS['Minimalism / Quiet Luxury'];
                    const fallbackId = pool.find(id => !usedIds.has(id)) || pool[0];
                    chosenPhoto = { id: fallbackId };
                }

                if (chosenPhoto) {
                    cardCache[card.title] = chosenPhoto.id;
                    usedIds.add(chosenPhoto.id);
                }
            } catch { /* silently skip */ }
        }));
        try { fs.writeFileSync(cacheFilePath, JSON.stringify(cardCache, null, 2)); } catch {}
        await new Promise(r => setTimeout(r, 250));
    }
    console.log(`[Unsplash] Background resolution done. Cache: ${Object.keys(cardCache).length} cards.`);
}

// ─── Apply images to dataset ─────────────────────────────────────────────────
// Query-override map: short semantic queries for title → Unsplash source
const TITLE_QUERIES = {
    'Academic Loafers & Corduroys':          'corduroy academic loafers preppy',
    'Mismatched Plaid & Stripe Layering':    'plaid stripe layering fashion',
    'Tactical Asymmetric Buckled Jacket':    'techwear tactical dark outfit',
    'Harness Strap Cargo Trousers':          'techwear utility cargo trousers',
    'Reflective Waterproof Shell':           'technical shell jacket techwear',
    'Industrial Silver Zipper Vest':         'tactical vest zipper techwear',
    'RGB-Trimmed Tech Mesh Layer':           'cyberpunk mesh techwear dark',
    'Pink Ribbon Cardigan & Bows':           'pink cardigan bow coquette',
    'Ballet Wrap Top & Tulle Skirt':         'ballerina tulle skirt pink',
    'Satin Slip Dress & Pearl Choker':       'satin slip dress pearl pink',
    'Deep Velvet Lace Slip Dress':           'velvet lace slip dress dark goth',
    'Celestial Embroidered Velvet Skirt':    'velvet skirt celestial lace gothic',
    'Sheer Bell Sleeve Lace Top':            'velvet sheer bell sleeve goth',
    'Plum Velvet Kimono Duster':             'velvet kimono plum dark fashion',
    'Moon Phase Corset Layering Look':       'corset lace goth dark fashion',
    'Pink Birthday Dinner Look':             'pink silk slip dress birthday dinner',
    'Satin Birthday Mini Dress':             'satin pink birthday mini dress',
    'Pink Birthday Tulle Dress':             'pink tulle dress birthday party',
    'Red Birthday Dress':                    'red statement blazer dress birthday',
    'Black Birthday Club Outfit':            'black asymmetric dress silver heels',
    'Main Character Birthday Fit':           'hot pink suit birthday fashion',
};

function applyUnsplashImages(dataset) {
    const assignedIds = new Set();
    const boardPointers = {};
    let resolvedCount = 0;
    let fallbackCount = 0;

    dataset.forEach(card => {
        // 1. Use resolved cache first (semantically correct)
        const cachedId = cardCache[card.title];
        if (cachedId) {
            // Use sig to make URLs unique per card even when IDs repeat
            card.image = buildPhotoUrl(cachedId, card.id);
            assignedIds.add(cachedId);
            resolvedCount++;
            return;
        }

        // 2. Try board-specific curated pool (better than generic fallback)
        const pool = BOARD_FALLBACKS[card.boardName] || [];
        let chosen = null;
        const ptr = boardPointers[card.boardName] || 0;

        for (let i = 0; i < pool.length; i++) {
            const id = pool[(ptr + i) % pool.length];
            if (!assignedIds.has(id)) {
                chosen = id;
                boardPointers[card.boardName] = ptr + i + 1;
                break;
            }
        }
        if (!chosen && pool.length > 0) {
            chosen = pool[ptr % pool.length];
            boardPointers[card.boardName] = ptr + 1;
        }

        if (chosen) {
            card.image = buildPhotoUrl(chosen, card.id);
            assignedIds.add(chosen);
        } else {
            // 3. Last resort: Unsplash source URL with semantic query keyword
            const query = TITLE_QUERIES[card.title]
                || `${card.boardName || 'fashion'} outfit style`;
            card.image = buildSourceUrl(query, card.id);
        }
        fallbackCount++;
    });

    console.log(`[Unsplash] Images applied: ${resolvedCount} from cache, ${fallbackCount} from board fallbacks.`);
}

/** Photo ID URL — exact Unsplash photo */
function buildPhotoUrl(photoId, cardId) {
    return `https://images.unsplash.com/photo-${photoId}?auto=format&fit=crop&w=600&q=80&sig=${cardId}`;
}

/** Source URL — keyword-matched random Unsplash photo, no API key required */
function buildSourceUrl(query, cardId) {
    const encoded = encodeURIComponent(query.replace(/[&]/g, 'and'));
    return `https://source.unsplash.com/600x800/?${encoded}&sig=${cardId}`;
}

// ─── Public API ──────────────────────────────────────────────────────────────
function initializeUnsplashImages(dataset) {
    loadCacheFromDisk();
    applyUnsplashImages(dataset);
    // Background: try to resolve remaining cards without blocking the server
    resolveAllCards(dataset).then(() => {
        applyUnsplashImages(dataset);
    }).catch(err => {
        console.log('[Unsplash] Background resolver error:', err);
    });
}

module.exports = { initializeUnsplashImages, BOARD_FALLBACKS };
