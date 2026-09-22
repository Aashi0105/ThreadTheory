const path = require('path');
const fs = require('fs');

let GoogleGenAI;

// Helper to dynamically import the ESM @google/genai module in a CommonJS environment
async function getGenAI() {
    if (!GoogleGenAI) {
        try {
            const genaiModule = await import('@google/genai');
            GoogleGenAI = genaiModule.GoogleGenAI;
        } catch (err) {
            console.error("Failed to import @google/genai in gemini_stylist:", err);
            throw err;
        }
    }
    return GoogleGenAI;
}

/**
 * AI Stylist service using Gemini to curate outfits from the user's wardrobe.
 * 
 * @param {string} prompt - The user prompt/aesthetic request
 * @param {Array} wardrobeItems - User's wardrobe items
 * @param {string} [weather] - Optional weather condition
 * @param {string} [season] - Optional season
 * @returns {Promise<Object>} The curated outfit result
 */
async function curateOutfit(prompt, wardrobeItems, weather = "", season = "") {
    // Read API key from environment
    const apiKey = process.env.GEMINI_API_KEY;
    if (!apiKey) {
        throw new Error("GEMINI_API_KEY is not defined in the environment.");
    }

    const GenAIClass = await getGenAI();
    const ai = new GenAIClass({ apiKey });

    // Format wardrobe inventory for Gemini
    const wardrobeList = wardrobeItems.map(item => ({
        id: item.id,
        name: item.name,
        category: item.category,
        subcategory: item.subcategory || "",
        season: item.season || "",
        dominantColor: item.dominantColor || item.color || ""
    }));

    // Prepare system instructions and query
    const systemPrompt = `You are a professional fashion stylist.

The user owns ONLY the wardrobe items listed below.
You are NOT allowed to invent clothing.
You are NOT allowed to suggest items that do not exist in the wardrobe.
Choose the best outfit from the provided wardrobe only.
Return valid JSON only.

Wardrobe Inventory:
${JSON.stringify(wardrobeList, null, 2)}`;

    const userPrompt = `User Request: "${prompt}"
Optional context: Season is ${season || 'any'}, Weather is ${weather || 'any'}.

Please curate the best matching outfit coordinates using only the available wardrobe items from the inventory. Returns an array of selected item IDs in 'selectedItems'.`;

    try {
        const modelName = 'gemini-2.5-flash';
        console.log("Using Gemini model:", modelName);
        console.log(`Sending curate request to Gemini for prompt: "${prompt}"...`);

        const requestPayload = {
            model: modelName,
            contents: [
                { role: 'user', parts: [{ text: `${systemPrompt}\n\n${userPrompt}` }] }
            ],
            config: {
                responseMimeType: 'application/json',
                responseSchema: {
                    type: 'OBJECT',
                    properties: {
                        selectedItems: {
                            type: 'ARRAY',
                            items: { type: 'STRING' },
                            description: 'List of exact item IDs selected from the wardrobe inventory'
                        },
                        aesthetic: { type: 'STRING', description: 'The overall aesthetic style of the outfit (e.g. Old Money, Streetwear)' },
                        occasion: { type: 'STRING', description: 'The occasion this outfit is suited for' },
                        confidence: { type: 'INTEGER', description: 'A style confidence match percentage from 50 to 99' },
                        reason: { type: 'STRING', description: 'Detailed explanation of why these pieces work together for the request' },
                        tips: {
                            type: 'ARRAY',
                            items: { type: 'STRING' },
                            description: 'A list of 2-3 specific styling/accessorizing tips'
                        }
                    },
                    required: ['selectedItems', 'aesthetic', 'occasion', 'confidence', 'reason', 'tips']
                }
            }
        };

        console.log("Gemini Request Payload:", JSON.stringify(requestPayload, null, 2));

        const response = await ai.models.generateContent(requestPayload);

        const responseText = response.text;
        if (!responseText) {
            throw new Error("Received empty response from Gemini.");
        }

        const result = JSON.parse(responseText);
        console.log("=== GEMINI STYLIST VALIDATION AUDIT ===");
        console.log("Parsed response object before validation:", JSON.stringify(result, null, 2));

        // Validation Layer
        const validItems = [];
        const selectedItems = result.selectedItems || [];

        for (const selected of selectedItems) {
            if (!selected) continue;

            const queryStr = selected.toString().toLowerCase().trim();
            console.log(`Auditing selection item: "${selected}" (queryStr: "${queryStr}")`);

            // Match by id or case-insensitive name
            const matchedItem = wardrobeItems.find(item => {
                const itemId = item.id ? item.id.toString().toLowerCase().trim() : '';
                const itemName = item.name ? item.name.toString().toLowerCase().trim() : '';
                return itemId === queryStr || itemName === queryStr;
            });

            if (matchedItem) {
                console.log(`Matched selection "${selected}" to wardrobe item ID: "${matchedItem.id}" (name: "${matchedItem.name}", category: "${matchedItem.category}")`);
                // Ensure no duplicate items are added
                if (!validItems.some(item => item.id === matchedItem.id)) {
                    validItems.push(matchedItem);
                } else {
                    console.log(`Skipped selection "${selected}" - already in validItems.`);
                }
            } else {
                console.warn(`VALIDATION FAILURE: Selection "${selected}" does not exist in wardrobeItems list. Discarding.`);
            }
        }

        // Categorize the validated items
        let top = null;
        let bottom = null;
        let shoes = null;
        let outerwear = null;

        for (const item of validItems) {
            const category = (item.category || "").toLowerCase().trim();
            if (['tops & blouses', 'knitwear', 'dresses', 'tops'].includes(category)) {
                if (!top) {
                    top = item;
                    console.log(`Assigned Top slot to item ID: "${item.id}" (category: "${item.category}")`);
                } else {
                    console.log(`Top slot already occupied by "${top.id}". Skipping item: "${item.id}"`);
                }
            } else if (['bottoms', 'pants'].includes(category)) {
                if (!bottom) {
                    bottom = item;
                    console.log(`Assigned Bottom slot to item ID: "${item.id}" (category: "${item.category}")`);
                } else {
                    console.log(`Bottom slot already occupied by "${bottom.id}". Skipping item: "${item.id}"`);
                }
            } else if (['footwear', 'shoes'].includes(category)) {
                if (!shoes) {
                    shoes = item;
                    console.log(`Assigned Shoes slot to item ID: "${item.id}" (category: "${item.category}")`);
                } else {
                    console.log(`Shoes slot already occupied by "${shoes.id}". Skipping item: "${item.id}"`);
                }
            } else if (['outerwear'].includes(category)) {
                if (!outerwear) {
                    outerwear = item;
                    console.log(`Assigned Outerwear slot to item ID: "${item.id}" (category: "${item.category}")`);
                } else {
                    console.log(`Outerwear slot already occupied by "${outerwear.id}". Skipping item: "${item.id}"`);
                }
            } else {
                console.log(`Item ID: "${item.id}" category "${item.category}" did not match any of the slot validation categories.`);
            }
        }

        // If a dress is selected as the top, we must not have a bottom
        if (top && (top.category || "").toLowerCase() === 'dresses') {
            bottom = null;
            console.log("Dress detected in Top slot - clearing Bottom slot per dress rule.");
        }

        const finalOutfitItems = [top, bottom, shoes, outerwear].filter(Boolean);
        const success = finalOutfitItems.length >= 1;

        // Logging outfit item count
        console.log("Outfit item count:", finalOutfitItems.length);

        let finalReason = result.reason || '';
        let errorMsg = undefined;

        if (finalOutfitItems.length < 2) {
            const warningMsg = "Validation Warning: Selected outfit has only " + finalOutfitItems.length + " item. Recommendation generated from available pieces.";
            console.warn(warningMsg);
            
            if (finalOutfitItems.length === 1) {
                finalReason = "Limited wardrobe inventory. Recommendation generated from available pieces.\n\n" + finalReason;
            }
        } else {
            console.log("VALIDATION SUCCESS: Curated outfit passes 2+ items validation rules.");
        }

        if (!success) {
            errorMsg = `Validation failed: Selected outfit has 0 valid wardrobe items matching Gemini suggestions. ` +
                       `Selected by Gemini: [${selectedItems.join(', ')}].`;
            console.warn(`VALIDATION FAILURE: ${errorMsg}`);
        }

        const finalResponse = {
            success,
            error: errorMsg,
            top,
            bottom,
            shoes,
            outerwear,
            aesthetic: result.aesthetic,
            occasion: result.occasion,
            confidence: Math.min(99, Math.max(50, result.confidence || 75)),
            reason: finalReason,
            tips: result.tips || []
        };

        // Logging final response
        console.log("Final response:", JSON.stringify(finalResponse, null, 2));

        return finalResponse;

    } catch (error) {
        console.error("Error in gemini_stylist:", error);
        return { success: false, error: error.message };
    }
}

module.exports = {
    curateOutfit
};
