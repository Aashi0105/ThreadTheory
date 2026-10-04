const fs = require('fs');
const path = require('path');

const BASE_URL = 'http://127.0.0.1:3000';

async function runTests() {
    console.log("==================================================");
    console.log("THREADTHEORY PHASE 2.7 - LIVE BACKEND VERIFICATION");
    console.log("==================================================\n");

    const results = [];

    // Test 1: Recommendation request with NO email
    try {
        const res = await fetch(`${BASE_URL}/api/recommendations`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ prompt: 'casual outfit' })
        });
        const data = await res.json();
        const pass = res.status === 400 && data.success === false && !data.recommended_outfit;
        results.push({
            name: "1. Recommendation request with NO email",
            pass,
            evidence: `Status ${res.status}, response: ${JSON.stringify(data)}`
        });
    } catch (e) {
        results.push({ name: "1. Recommendation request with NO email", pass: false, evidence: e.message });
    }

    // Test 2: Recommendation request with blank/whitespace email
    try {
        const res = await fetch(`${BASE_URL}/api/recommendations`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ prompt: 'casual outfit', email: '   ' })
        });
        const data = await res.json();
        const pass = res.status === 400 && data.success === false && !data.recommended_outfit;
        results.push({
            name: "2. Recommendation request with blank email",
            pass,
            evidence: `Status ${res.status}, response: ${JSON.stringify(data)}`
        });
    } catch (e) {
        results.push({ name: "2. Recommendation request with blank email", pass: false, evidence: e.message });
    }

    // Test 3: Recommendation score - check no fabricated 88 or 82
    try {
        const res = await fetch(`${BASE_URL}/api/recommendations`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ prompt: 'casual weekend outfit', email: 'demo@threadtheory.io' })
        });
        const data = await res.json();
        const hasNo88 = data && data.synergyScore !== 88 && data.score !== 88 && data.synergyScore !== 82 && data.score !== 82;
        const pass = res.status === 200 && data.success === true && (data.synergyScore === null || data.synergyScore === 0) && hasNo88;
        results.push({
            name: "3. Recommendation score (No fake 88 / 82)",
            pass,
            evidence: `Status ${res.status}, synergyScore: ${data?.synergyScore}, score: ${data?.score}, isGemini: ${data?.isGemini}`
        });
    } catch (e) {
        results.push({ name: "3. Recommendation score", pass: false, evidence: e.message });
    }

    // Test 4: User A isolation
    try {
        const resA = await fetch(`${BASE_URL}/api/recommendations`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ prompt: 'casual outfit', email: 'aashi@example.com' })
        });
        const dataA = await resA.json();
        let allUserA = true;
        let itemNames = [];
        ['top', 'bottom', 'outerwear', 'shoes'].forEach(slot => {
            const item = dataA && dataA[slot];
            if (item) {
                itemNames.push(`${slot}:${item.name}(${item.id})`);
                if (item.owner && item.owner.toLowerCase() !== 'aashi@example.com') {
                    allUserA = false;
                }
            }
        });
        const pass = resA.status === 200 && allUserA;
        results.push({
            name: "4. User A recommendation isolation",
            pass,
            evidence: `Status ${resA.status}, user items: ${itemNames.join(', ')}`
        });
    } catch (e) {
        results.push({ name: "4. User A recommendation isolation", pass: false, evidence: e.message });
    }

    // Test 5: Non-image upload rejected at upload boundary
    try {
        const formData = new FormData();
        formData.append('name', 'Malicious Script');
        formData.append('category', 'Tops');
        formData.append('subcategory', 'T-Shirts');
        formData.append('season', 'Summer');
        formData.append('occasion', 'Party');
        formData.append('owner', 'demo@threadtheory.io');
        const fakeBlob = new Blob(['echo "hello world"'], { type: 'application/x-sh' });
        formData.append('image', fakeBlob, 'script.sh');

        const res = await fetch(`${BASE_URL}/api/wardrobe/add`, {
            method: 'POST',
            body: formData
        });
        const data = await res.json();
        const pass = res.status === 400 && data.success === false;
        results.push({
            name: "5. Non-image upload rejection (.sh file)",
            pass,
            evidence: `Status ${res.status}, response: ${JSON.stringify(data)}`
        });
    } catch (e) {
        results.push({ name: "5. Non-image upload rejection", pass: false, evidence: e.message });
    }

    // Test 6: Valid image upload accepted
    let uploadedItemId = null;
    try {
        const pngBytes = Buffer.from('iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mNk+M9QDwADhgGAWjR9awAAAABJRU5ErkJggg==', 'base64');
        const formData = new FormData();
        formData.append('name', 'Phase 2.7 Verified Linen Shirt');
        formData.append('category', 'Tops');
        formData.append('subcategory', 'Linen Shirts');
        formData.append('season', 'Summer');
        formData.append('occasion', 'Casual');
        formData.append('formality', 'smart casual');
        formData.append('owner', 'demo@threadtheory.io');
        const imgBlob = new Blob([pngBytes], { type: 'image/png' });
        formData.append('image', imgBlob, 'sample_shirt.png');

        const res = await fetch(`${BASE_URL}/api/wardrobe/add`, {
            method: 'POST',
            body: formData
        });
        const data = await res.json();
        const pass = res.status === 200 && data.success === true && data.item;
        if (pass) {
            uploadedItemId = data.item.id;
        }
        results.push({
            name: "6. Valid image upload acceptance (PNG)",
            pass,
            evidence: `Status ${res.status}, item created id: ${data?.item?.id}`
        });
    } catch (e) {
        results.push({ name: "6. Valid image upload acceptance", pass: false, evidence: e.message });
    }

    // Test 7: Formality vs Occasion SQLite synchronization check
    try {
        const { execFileSync } = require('child_process');
        const pyExe = path.join(__dirname, '..', 'venv', 'Scripts', 'python.exe');
        const dbPath = path.join(__dirname, '..', 'wardrobe.db');
        
        let pass = { ok: false, row: null };
        if (uploadedItemId) {
            const pyCode = "import sqlite3, json; conn = sqlite3.connect(r'" + dbPath + "'); cursor = conn.cursor(); cursor.execute('SELECT formality, occasion FROM wardrobe WHERE id = ?', ('" + uploadedItemId + "',)); row = cursor.fetchone(); conn.close(); print(json.dumps({'formality': row[0], 'occasion': row[1]} if row else None))";
            const out = execFileSync(pyExe, ['-c', pyCode], { encoding: 'utf8' }).trim();
            const rowData = JSON.parse(out);
            if (rowData && rowData.formality === 'smart casual' && rowData.occasion === 'Casual') {
                pass = { ok: true, row: rowData };
            } else {
                pass = { ok: false, row: rowData };
            }
        }

        results.push({
            name: "7. Formality mapping integrity in SQLite",
            pass: pass.ok === true,
            evidence: `Stored row: formality='${pass.row?.formality}', occasion='${pass.row?.occasion}'`
        });
    } catch (e) {
        results.push({ name: "7. Formality mapping integrity", pass: false, evidence: e.message });
    }

    // Test 8: Delete wardrobe item and check JSON + SQLite sync
    try {
        if (uploadedItemId) {
            const delRes = await fetch(`${BASE_URL}/api/wardrobe/${uploadedItemId}?email=demo@threadtheory.io`, {
                method: 'DELETE'
            });
            const delData = await delRes.json();
            
            // Check SQLite via Python
            const { execFileSync } = require('child_process');
            const pyExe = path.join(__dirname, '..', 'venv', 'Scripts', 'python.exe');
            const dbPath = path.join(__dirname, '..', 'wardrobe.db');
            const pyDelCode = "import sqlite3, json; conn = sqlite3.connect(r'" + dbPath + "'); cursor = conn.cursor(); cursor.execute('SELECT id FROM wardrobe WHERE id = ?', ('" + uploadedItemId + "',)); row = cursor.fetchone(); conn.close(); print(json.dumps(row is None))";
            const sqliteDeleted = JSON.parse(execFileSync(pyExe, ['-c', pyDelCode], { encoding: 'utf8' }).trim());

            // Check JSON
            const wardrobeJson = JSON.parse(fs.readFileSync(path.join(__dirname, '..', 'data', 'wardrobe.json'), 'utf8'));
            const jsonDeleted = !wardrobeJson.some(i => String(i.id) === String(uploadedItemId));

            const pass = delRes.status === 200 && delData.success && sqliteDeleted && jsonDeleted;
            results.push({
                name: "8. Delete wardrobe item (JSON + SQLite sync)",
                pass,
                evidence: `Delete status: ${delRes.status}, sqliteDeleted: ${sqliteDeleted}, jsonDeleted: ${jsonDeleted}`
            });
        } else {
            results.push({ name: "8. Delete wardrobe item", pass: false, evidence: "Skipped because item creation failed" });
        }
    } catch (e) {
        results.push({ name: "8. Delete wardrobe item", pass: false, evidence: e.message });
    }

    // Test 9: Portable INSP_BRAIN_DIR path behavior
    try {
        const res = await fetch(`${BASE_URL}/assets/inspiration/nonexistent_test.png`);
        const text = await res.text();
        const pass = res.status === 404 && text === 'Inspiration image not found';
        results.push({
            name: "9. Portable INSP_BRAIN_DIR handling",
            pass,
            evidence: `Status ${res.status}, response: ${text}`
        });
    } catch (e) {
        results.push({ name: "9. Portable INSP_BRAIN_DIR handling", pass: false, evidence: e.message });
    }

    // Print summary table
    console.log("\n==================== VERIFICATION SUMMARY ====================");
    results.forEach(r => {
        console.log(`[${r.pass ? 'PASS' : 'FAIL'}] ${r.name}`);
        console.log(`       Evidence: ${r.evidence}`);
    });

    const allPassed = results.every(r => r.pass);
    console.log(`\nOVERALL: ${allPassed ? 'ALL TESTS PASSED' : 'SOME TESTS FAILED'}`);
    process.exit(allPassed ? 0 : 1);
}

runTests();
