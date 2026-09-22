/**
 * resolve_images.js
 * Pre-resolves all 75 curated aesthetics cards in ThreadTheory lookbook using Pexels API
 * and caches them locally in pexels_search_cache.json.
 */

const fs = require('fs');
const path = require('path');

// Load environment variables from .env file
const envPath = path.join(__dirname, '.env');
if (fs.existsSync(envPath)) {
    try {
        const envContent = fs.readFileSync(envPath, 'utf8');
        envContent.split(/\r?\n/).forEach(line => {
            const trimmedLine = line.trim();
            if (trimmedLine && !trimmedLine.startsWith('#')) {
                const eqIdx = trimmedLine.indexOf('=');
                if (eqIdx > 0) {
                    const key = trimmedLine.substring(0, eqIdx).trim();
                    const value = trimmedLine.substring(eqIdx + 1).trim().replace(/(^["']|["']$)/g, '');
                    process.env[key] = value;
                }
            }
        });
        console.log("Successfully loaded environment variables from .env file.");
    } catch (e) {
        console.error("Failed to parse .env file:", e);
    }
}

const curatedInspiration = require('./inspiration_dataset.js');
const { resolveCardImage } = require('./pexels_helper.js');

async function resolveAllAesthetics() {
    console.log("======================================================================");
    console.log("ThreadTheory: Running Pre-Resolution script for all 150 lookbook cards...");
    console.log("======================================================================");
    
    // Filter to all cards in the dataset
    const cards = curatedInspiration.filter(c => c.boardType === 'aesthetic' || c.boardType === 'movement' || c.boardType === 'occasion' || c.boardType === 'colorStory' || c.boardType === 'colorCombination');
    console.log(`Found ${cards.length} cards to resolve.`);

    let completed = 0;
    for (let i = 0; i < cards.length; i++) {
        const card = cards[i];
        const boardLabel = card.boardType.toUpperCase();
        console.log(`[${i + 1}/${cards.length}] Resolving: "${card.title}" (${boardLabel}: "${card.boardName}")`);
        try {
            const url = await resolveCardImage(card);
            console.log(`  -> Resolved: ${url}`);
            completed++;
        } catch (err) {
            console.error(`  -> Failed to resolve "${card.title}":`, err.message);
        }
        // Small delay to prevent Pexels rate limits (100ms)
        await new Promise(r => setTimeout(r, 100));
    }

    console.log("======================================================================");
    console.log(`Finished pre-resolution. Successfully resolved ${completed}/${cards.length} images.`);
    console.log("Cache written to pexels_search_cache.json.");
    console.log("======================================================================");
}

resolveAllAesthetics().catch(err => {
    console.error("Fatal error during resolution:", err);
    process.exit(1);
});
