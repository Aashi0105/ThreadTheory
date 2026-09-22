/**
 * pexels_helper.js
 * Backend search proxy, validator, and local caching system for Pexels API.
 */

const https = require('https');
const fs = require('fs');
const path = require('path');

const CACHE_FILE = path.join(__dirname, 'pexels_search_cache.json');

// Hard rejections list
const HARD_REJECTIONS = [
    'mannequin', 'dummy', 'display model', 'dress form', 'clothing rack', 
    'hanger', 'retail display', 'wardrobe rail', 'corkboard', 'design desk',
    'workspace', 'desk', 'laptop', 'computer', 'screen', 'sketch', 'drawing', 'moodboard',
    'interior', 'room', 'furniture', 'chair', 'table', 'sofa', 'couch', 'decor',
    'building', 'architecture', 'house', 'home', 'apartment', 'landscape',
    'mountain', 'nature', 'sea', 'ocean', 'sky', 'forest', 'lake', 'river',
    'tree', 'field', 'scenery', 'sunset', 'sunrise', 'food', 'recipe',
    'dish', 'plate', 'cooking', 'meal', 'fabric closeup', 'closeup', 'fabric'
];

/**
 * Extracts garment keywords from the card title for scoring.
 */
function extractGarmentKeywords(title) {
    const titleLower = title.toLowerCase();
    const keywords = [];

    const mappings = [
        { term: 'vest', matches: ['vest', 'waistcoat'] },
        { term: 'coat', matches: ['coat', 'overcoat', 'duster', 'parka'] },
        { term: 'trench', matches: ['trench', 'coat'] },
        { term: 'jacket', matches: ['jacket', 'puffer', 'windbreaker', 'bomber', 'moto'] },
        { term: 'blazer', matches: ['blazer', 'suit', 'jacket'] },
        { term: 'hoodie', matches: ['hoodie', 'sweatshirt', 'pullover'] },
        { term: 'cardigan', matches: ['cardigan', 'knitwear', 'sweater'] },
        { term: 'sweater', matches: ['sweater', 'knit', 'turtleneck', 'mockneck', 'pullover', 'cardigan'] },
        { term: 'knit', matches: ['knit', 'sweater', 'cardigan', 'crochet'] },
        { term: 'crochet', matches: ['crochet', 'knit'] },
        { term: 'skirt', matches: ['skirt', 'dress'] },
        { term: 'dress', matches: ['dress', 'sundress', 'gown', 'maxi', 'slip'] },
        { term: 'sundress', matches: ['dress', 'sundress'] },
        { term: 'slip', matches: ['slip', 'dress'] },
        { term: 'trousers', matches: ['trousers', 'pants', 'chinos', 'corduroy', 'jeans', 'slacks'] },
        { term: 'pants', matches: ['pants', 'trousers', 'chinos', 'corduroy', 'jeans', 'slacks', 'cargos', 'joggers', 'jumpsuit'] },
        { term: 'jeans', matches: ['jeans', 'denim', 'pants'] },
        { term: 'denim', matches: ['denim', 'jeans', 'jacket'] },
        { term: 'cargo', matches: ['cargo', 'cargos', 'pants', 'trousers', 'pocket'] },
        { term: 'blouse', matches: ['blouse', 'shirt', 'top'] },
        { term: 'shirt', matches: ['shirt', 'button-down', 'polo', 'top', 'blouse', 'flannel'] },
        { term: 'button-down', matches: ['shirt', 'button-down'] },
        { term: 'polo', matches: ['polo', 'shirt'] },
        { term: 'tee', matches: ['tee', 't-shirt', 'top'] },
        { term: 'top', matches: ['top', 'tee', 't-shirt', 'shirt', 'blouse', 'camisole', 'tank'] },
        { term: 'camisole', matches: ['camisole', 'top', 'tank'] },
        { term: 'tank', matches: ['tank', 'top'] },
        { term: 'boots', matches: ['boots', 'shoes', 'footwear'] },
        { term: 'loafers', matches: ['loafers', 'shoes', 'footwear', 'flats'] },
        { term: 'sneakers', matches: ['sneakers', 'shoes', 'trainers'] },
        { term: 'shoes', matches: ['shoes', 'footwear', 'sneakers', 'boots', 'loafers', 'flats'] },
        { term: 'jumpsuit', matches: ['jumpsuit', 'romper', 'overall'] },
        { term: 'suit', matches: ['suit', 'blazer'] },
        { term: 'tunic', matches: ['tunic', 'top', 'dress'] },
        { term: 'corset', matches: ['corset', 'top', 'bustier'] },
        { term: 'kimono', matches: ['kimono', 'duster', 'robe', 'cardigan'] },
        { term: 'set', matches: ['set', 'suit', 'coord', 'co-ord', 'matching', 'outfit'] },
        { term: 'matching', matches: ['set', 'suit', 'coord', 'co-ord', 'matching', 'outfit'] },
        { term: 'scarf', matches: ['scarf', 'wrap', 'muffler', 'wool'] },
        { term: 'layering', matches: ['layer', 'layered', 'outfit', 'cardigan', 'sweater', 'blazer', 'coat', 'jacket'] },
        { term: 'plaid', matches: ['plaid', 'tartan', 'checked', 'check', 'flannel'] },
        { term: 'maxi', matches: ['maxi', 'dress', 'skirt'] },
        { term: 'chinos', matches: ['chinos', 'pants', 'trousers'] },
        { term: 'riding', matches: ['riding', 'coat', 'blazer', 'jacket', 'boots'] },
        { term: 'corduroys', matches: ['corduroys', 'corduroy', 'pants', 'trousers'] },
        { term: 'mesh', matches: ['mesh', 'sheer', 'top', 'shirt'] },
        { term: 'fringe', matches: ['fringe', 'jacket', 'vest', 'suede'] },
        { term: 'shoulder', matches: ['shoulder', 'vest', 'top', 'outfit'] },
        { term: 'duster', matches: ['duster', 'coat', 'cardigan', 'kimono'] },
        { term: 'distressed', matches: ['distressed', 'shredded', 'ripped', 'grunge', 'distressed knit'] },
        { term: 'harness', matches: ['harness', 'tactical', 'straps', 'chest harness'] },
        { term: 'vinyl', matches: ['vinyl', 'shiny', 'coated', 'utility'] },
        { term: 'tailoring', matches: ['tailored', 'blazer', 'trousers', 'suit'] },
        { term: 'cashmere', matches: ['cashmere', 'knit', 'sweater', 'wool'] },
        { term: 'double-breasted', matches: ['double-breasted', 'blazer', 'coat', 'suit'] },
        { term: 'power', matches: ['power', 'suit', 'blazer', 'trousers'] },
        { term: 'satin', matches: ['satin', 'silk', 'shiny', 'dress', 'shirt', 'top'] },
        { term: 'monochrome', matches: ['monochrome', 'matching', 'set', 'tonal', 'suit'] },
        { term: 'draped', matches: ['draped', 'asymmetric', 'wrap', 'coat', 'dress'] },
        { term: 'silhouette', matches: ['silhouette', 'coat', 'dress', 'outfit'] },
        { term: 'lounge', matches: ['lounge', 'knitwear', 'pants', 'comfortable', 'set'] },
        { term: 'tweed', matches: ['tweed', 'wool', 'blazer', 'dress', 'jacket'] },
        { term: 'sweatshirt', matches: ['sweatshirt', 'hoodie', 'pullover', 'sweater'] },
        { term: 'co-ord', matches: ['set', 'coord', 'co-ord', 'matching', 'outfit'] },
        { term: 'resort', matches: ['resort', 'vacation', 'linen', 'summer', 'set', 'outfit'] }
    ];

    for (const map of mappings) {
        if (titleLower.includes(map.term)) {
            keywords.push(...map.matches);
        }
    }
    
    // Add title words itself as fallback
    const titleWords = titleLower.replace(/[&,]/g, '').split(/\s+/).filter(w => w.length > 3);
    keywords.push(...titleWords);

    return [...new Set(keywords)];
}

/**
 * Extracts occasion keywords for soft scoring.
 */
function extractOccasionKeywords(occasion) {
    if (!occasion) return [];
    const norm = occasion.toLowerCase();
    if (norm.includes('birthday')) {
        return ['party dress', 'birthday outfit', 'celebration look', 'cocktail outfit', 'event fashion'];
    }
    if (norm.includes('date')) {
        return ['dinner outfit', 'evening dress', 'romantic date outfit', 'luxury restaurant look'];
    }
    if (norm.includes('college') || norm.includes('campus')) {
        return ['campus outfit', 'casual student outfit', 'hoodie and jeans', 'everyday college fashion'];
    }
    if (norm.includes('europe') || norm.includes('trip') || norm.includes('capsule') || norm.includes('vacation')) {
        return ['travel outfit', 'airport outfit', 'capsule wardrobe', 'vacation outfit', 'city walking outfit'];
    }
    return [];
}

/**
 * Scores a Pexels photo based on card details and runs hard rejections.
 * Returns score (integer) if valid, or null if rejected.
 */
function scoreAndValidatePhoto(photo, garmentKeywords, card) {
    if (!photo) return null;

    const photoText = [
        photo.alt || '',
        photo.url ? path.basename(photo.url).replace(/-\d+$/, '').replace(/-/g, ' ') : ''
    ].join(' ').toLowerCase();

    // 1. Hard Rejections
    if (HARD_REJECTIONS.some(w => photoText.includes(w))) {
        return null;
    }

    // Must have basic fashion keywords to avoid random stock photos
    const isFashionRelated = [
        'outfit', 'fashion', 'wearing', 'style', 'model', 'look', 'wear', 
        'woman', 'man', 'girl', 'person', 'clothing', 'clothes', 'posing'
    ].some(w => photoText.includes(w));
    
    if (!isFashionRelated) {
        return null;
    }

    let score = 0;
    let garmentMatched = false;

    // 2. Soft Scoring

    // Title / garment keywords match (+5 points for exact garment match)
    const matchedGarment = garmentKeywords.some(keyword => {
        const regex = new RegExp(`\\b${keyword}\\w*\\b`, 'i');
        return regex.test(photoText);
    });
    if (matchedGarment) {
        score += 5;
        garmentMatched = true;
    }

    // Color match / Combination match
    const colorKeywordsMap = {
        'black': ['black', 'darkwear', 'noir'],
        'white': ['white', 'ivory', 'cream', 'resort'],
        'cream / ivory': ['cream', 'ivory', 'off-white', 'eggshell'],
        'beige / tan': ['beige', 'tan', 'camel', 'khaki', 'sand'],
        'brown': ['brown', 'chocolate', 'espresso', 'mocha', 'coffee', 'tan'],
        'gray': ['gray', 'grey', 'charcoal', 'slate', 'heather'],
        'navy': ['navy', 'blue', 'marine'],
        'olive / sage': ['olive', 'sage', 'green', 'khaki'],
        'burgundy': ['burgundy', 'maroon', 'wine', 'bordeaux'],
        'light blue': ['light blue', 'sky blue', 'blue', 'pastel blue'],
        'red': ['red', 'scarlet', 'crimson', 'cherry'],
        'pink': ['pink', 'blush', 'rose', 'fuchsia'],
        'yellow': ['yellow', 'mustard', 'butter yellow', 'gold'],
        'royal blue': ['royal blue', 'blue', 'electric blue', 'sapphire'],
        'purple': ['purple', 'lavender', 'plum', 'lilac', 'violet']
    };

    const colorComboKeywordsMap = {
        'black': ['black', 'darkwear', 'noir'],
        'white': ['white', 'ivory', 'cream', 'resort'],
        'cream': ['cream', 'ivory', 'off-white', 'eggshell'],
        'ivory': ['cream', 'ivory', 'off-white', 'eggshell'],
        'beige': ['beige', 'tan', 'camel', 'khaki', 'sand'],
        'tan': ['beige', 'tan', 'camel', 'khaki', 'sand'],
        'camel': ['beige', 'tan', 'camel', 'khaki', 'sand'],
        'brown': ['brown', 'chocolate', 'espresso', 'mocha', 'coffee', 'tan'],
        'chocolate': ['brown', 'chocolate', 'espresso', 'mocha', 'coffee', 'tan'],
        'gray': ['gray', 'grey', 'charcoal', 'slate', 'heather'],
        'grey': ['gray', 'grey', 'charcoal', 'slate', 'heather'],
        'navy': ['navy', 'blue', 'marine'],
        'olive': ['olive', 'sage', 'green', 'khaki'],
        'sage': ['olive', 'sage', 'green', 'khaki'],
        'sage green': ['olive', 'sage', 'green', 'khaki'],
        'burgundy': ['burgundy', 'maroon', 'wine', 'bordeaux'],
        'light blue': ['light blue', 'sky blue', 'blue', 'pastel blue'],
        'sky blue': ['light blue', 'sky blue', 'blue', 'pastel blue'],
        'red': ['red', 'scarlet', 'crimson', 'cherry'],
        'pink': ['pink', 'blush', 'rose', 'fuchsia'],
        'yellow': ['yellow', 'mustard', 'butter yellow', 'gold'],
        'royal blue': ['royal blue', 'blue', 'electric blue', 'sapphire'],
        'purple': ['purple', 'lavender', 'plum', 'lilac', 'violet'],
        'plum': ['purple', 'lavender', 'plum', 'lilac', 'violet'],
        'silver': ['silver', 'metallic', 'chrome']
    };

    const boardType = card.boardType;
    const boardName = card.boardName || '';

    if (boardType === 'colorCombination') {
        // Color Combination Match = +5 (requires BOTH colors to match)
        const parts = boardName.split('+').map(p => p.trim().toLowerCase());
        if (parts.length === 2) {
            const kw1 = colorComboKeywordsMap[parts[0]] || [parts[0]];
            const kw2 = colorComboKeywordsMap[parts[1]] || [parts[1]];
            const match1 = kw1.some(kw => photoText.includes(kw));
            const match2 = kw2.some(kw => photoText.includes(kw));
            if (match1 && match2) {
                score += 5;
            }
        }

        // Board Match = +4
        let boardMatched = false;
        if (boardName) {
            const normBoard = boardName.toLowerCase().replace(/[^a-z0-9]/g, ' ');
            const boardWords = normBoard.split(/\s+/).filter(w => w.length > 3 && w !== 'girl');
            boardMatched = boardWords.some(w => photoText.includes(w));
        }
        if (boardMatched) {
            score += 4;
        }

        // Aesthetic Match = +2
        const AESTHETIC_KEYWORDS = [
            'minimalist', 'minimalism', 'quiet luxury', 'y2k', 'dark academia', 'academia', 
            'cottagecore', 'cottage', 'streetwear', 'street style', 'gorpcore', 'outdoor', 
            'grunge', 'coquette', 'balletcore', 'old money', 'preppy', 'grandpa', 
            'cyberpunk', 'techwear', 'boho', 'bohemian', 'whimsigoth', 'indie sleaze', 'clean girl'
        ];
        const hasAestheticMatch = AESTHETIC_KEYWORDS.some(ak => photoText.includes(ak));
        if (hasAestheticMatch) {
            score += 2;
        }
    } else {
        // Default scoring (for aesthetics, movements, occasions, colorStories)
        // Color match (+4 points for colorStory)
        let colorMatched = false;
        if (boardType === 'colorStory') {
            const colorName = boardName.toLowerCase();
            const keywords = colorKeywordsMap[colorName] || [colorName];
            colorMatched = keywords.some(kw => photoText.includes(kw));
        }
        if (colorMatched) {
            score += 4;
        }

        // Board Match = +3
        let boardMatched = false;
        if (boardName) {
            const normBoard = boardName.toLowerCase().replace(/[^a-z0-9]/g, ' ');
            const boardWords = normBoard.split(/\s+/).filter(w => w.length > 3 && w !== 'girl');
            boardMatched = boardWords.some(w => photoText.includes(w));
        }
        if (boardMatched) {
            score += 3;
        }
    }

    return { score, garmentMatched };
}

/**
 * Loads cache from disk
 */
function loadCache() {
    try {
        if (fs.existsSync(CACHE_FILE)) {
            return JSON.parse(fs.readFileSync(CACHE_FILE, 'utf8'));
        }
    } catch (e) {
        console.error('[Pexels Cache] Error loading cache:', e.message);
    }
    return {};
}

/**
 * Saves cache to disk
 */
function saveCache(cache) {
    try {
        fs.writeFileSync(CACHE_FILE, JSON.stringify(cache, null, 2));
    } catch (e) {
        console.error('[Pexels Cache] Error writing cache:', e.message);
    }
}

/**
 * Fetches search results from Pexels API
 */
function fetchFromPexels(query) {
    return new Promise(resolve => {
        const apiKey = process.env.PEXELS_API_KEY;
        if (!apiKey) {
            console.error('[Pexels API] Error: PEXELS_API_KEY is not defined in environment.');
            resolve([]);
            return;
        }

        const url = `https://api.pexels.com/v1/search?query=${encodeURIComponent(query)}&per_page=15&orientation=portrait`;
        
        const req = https.get(url, {
            headers: {
                'Authorization': apiKey,
                'Accept': 'application/json',
                'User-Agent': 'ThreadTheoryCuratedLookbook/1.0'
            }
        }, res => {
            if (res.statusCode !== 200) {
                console.error(`[Pexels API] Error: API returned status ${res.statusCode}`);
                resolve([]);
                return;
            }

            let body = '';
            res.on('data', chunk => body += chunk);
            res.on('end', () => {
                try {
                    const json = JSON.parse(body);
                    resolve(json.photos || []);
                } catch (e) {
                    console.error('[Pexels API] Error parsing response:', e.message);
                    resolve([]);
                }
            });
        });

        req.on('error', err => {
            console.error('[Pexels API] Request error:', err.message);
            resolve([]);
        });
        req.setTimeout(5000, () => {
            req.destroy();
            resolve([]);
        });
    });
}

/**
 * Resolves a Pexels photo for a curated card.
 * Uses cached image if exists, else queries Pexels once and caches the result.
 */
async function resolveCardImage(card) {
    const cache = loadCache();
    
    // 1. Return cached image if exists
    if (cache[card.id]) {
        return cache[card.id];
    }

    console.log(`[Pexels Resolver] Resolving image for card "${card.title}" (ID: ${card.id})`);
    
    // 2. Fetch candidates from Pexels (include occasion/colorStory/colorCombination name in query if applicable)
    let query = `${card.title} outfit fashion`;
    if (card.boardType === 'occasion') {
        query = `${card.title} ${card.occasion || card.boardName} fashion outfit`;
    } else if (card.boardType === 'colorStory') {
        query = `${card.title} ${card.boardName} fashion outfit`;
    } else if (card.boardType === 'colorCombination') {
        query = `${card.title} ${card.boardName} fashion outfit`;
    }
    const rawPhotos = await fetchFromPexels(query);
    
    // 3. Extract keywords and score candidates
    const garmentKeywords = extractGarmentKeywords(card.title);
    const candidates = [];

    rawPhotos.forEach(photo => {
        const res = scoreAndValidatePhoto(photo, garmentKeywords, card);
        if (res !== null) {
            candidates.push({ 
                photo, 
                score: res.score, 
                garmentMatched: res.garmentMatched 
            });
        }
    });

    // 4. Select the best match
    let resolvedUrl = null;
    if (candidates.length > 0) {
        // Sort by garmentMatched (descending), then by score (descending)
        candidates.sort((a, b) => {
            if (a.garmentMatched !== b.garmentMatched) {
                return a.garmentMatched ? -1 : 1;
            }
            return b.score - a.score;
        });
        resolvedUrl = candidates[0].photo.src.large || candidates[0].photo.src.original;
        console.log(`[Pexels Resolver] Match found: ${resolvedUrl} (Garment Matched: ${candidates[0].garmentMatched}, Score: ${candidates[0].score})`);
    } else {
        // Fallback to next best fashion search if strict query yields nothing
        console.log(`[Pexels Resolver] No candidates matched strict query. Retrying with general aesthetic outfit...`);
        const fallbackQuery = `${card.boardName || 'fashion'} outfit women`;
        const fallbackPhotos = await fetchFromPexels(fallbackQuery);
        
        const fallbackCandidates = [];
        fallbackPhotos.forEach(photo => {
            const res = scoreAndValidatePhoto(
                photo, 
                ['outfit', 'fashion', 'style'], 
                card
            );
            if (res !== null) {
                fallbackCandidates.push({ 
                    photo, 
                    score: res.score, 
                    garmentMatched: res.garmentMatched 
                });
            }
        });

        if (fallbackCandidates.length > 0) {
            fallbackCandidates.sort((a, b) => {
                if (a.garmentMatched !== b.garmentMatched) {
                    return a.garmentMatched ? -1 : 1;
                }
                return b.score - a.score;
            });
            resolvedUrl = fallbackCandidates[0].photo.src.large || fallbackCandidates[0].photo.src.original;
            console.log(`[Pexels Resolver] Fallback match found: ${resolvedUrl}`);
        } else {
            // Hard fallback to local placeholder
            resolvedUrl = card.image || card.img;
            console.warn(`[Pexels Resolver] Complete fallback to local asset: ${resolvedUrl}`);
        }
    }

    // 5. Update Cache
    cache[card.id] = resolvedUrl;
    saveCache(cache);

    return resolvedUrl;
}

module.exports = { resolveCardImage };
