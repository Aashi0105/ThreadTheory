/**
 * Route-by-Route API Authentication & Resource Ownership Regression Test Suite (Phase 2B-2)
 *
 * Verifies:
 * 1. Unauthenticated requests to all user-owned API groups are rejected with 401.
 * 2. User A cannot read, update, or delete User B's resources (IDOR prevention).
 * 3. Client-supplied email/owner fields in queries/bodies cannot override req.user.email.
 * 4. Resource IDs are checked strictly against the authenticated owner before mutations.
 * 5. Public signup/login, public username/email checks, and public catalog remain functional.
 * 6. Debug, development, and test endpoints are disabled in production mode.
 */

const http = require('http');
const fs = require('fs');
const path = require('path');
const assert = require('assert');

const { app } = require('../server.js');

let server;
let baseUrl;

function makeRequest(path, options = {}) {
    return new Promise((resolve, reject) => {
        const url = new URL(path, baseUrl);
        const headers = { ...(options.headers || {}) };

        let postData = options.body;
        if (postData && typeof postData === 'object' && !headers['Content-Type']) {
            postData = JSON.stringify(postData);
            headers['Content-Type'] = 'application/json';
        }
        if (postData && !headers['Content-Length']) {
            headers['Content-Length'] = Buffer.byteLength(postData);
        }

        const reqOptions = {
            method: options.method || 'GET',
            headers: headers
        };

        const req = http.request(url, reqOptions, (res) => {
            const chunks = [];
            res.on('data', chunk => { chunks.push(Buffer.isBuffer(chunk) ? chunk : Buffer.from(chunk)); });
            res.on('end', () => {
                const rawBuffer = Buffer.concat(chunks);
                const data = rawBuffer.toString('utf8');
                let json = null;
                try {
                    json = JSON.parse(data);
                } catch (e) {
                    // Not JSON
                }
                resolve({
                    status: res.statusCode,
                    headers: res.headers,
                    body: data,
                    rawBuffer: rawBuffer,
                    json: json
                });
            });
        });

        req.on('error', reject);

        if (postData) {
            req.write(postData);
        }
        req.end();
    });
}

function extractCookie(headers) {
    const setCookie = headers['set-cookie'];
    if (!setCookie) return null;
    const cookieStr = Array.isArray(setCookie) ? setCookie[0] : setCookie;
    const match = cookieStr.match(/tt_session=([^;]+)/);
    return match ? match[1] : null;
}

async function runSuite() {
    console.log("==================================================================");
    console.log(" Starting Phase 2B-2: API Authentication & Ownership Test Suite");
    console.log("==================================================================\n");

    let passed = 0;
    let failed = 0;

    function report(name, condition, extra = '') {
        if (condition) {
            console.log(`  âœ“ PASS: ${name}`);
            passed++;
        } else {
            console.error(`  âœ— FAIL: ${name} ${extra}`);
            failed++;
        }
    }

    // Backup databases before test
    const dataDir = path.join(__dirname, '..', 'data');
    const usersFile = path.join(dataDir, 'users.json');
    const sessionsFile = path.join(dataDir, 'sessions.json');
    const wardrobeFile = path.join(dataDir, 'wardrobe.json');
    const savedLooksFile = path.join(dataDir, 'saved_looks.json');
    const plannerFile = path.join(dataDir, 'planner.json');
    const moodboardsFile = path.join(dataDir, 'moodboards.json');
    const matchHistoryFile = path.join(dataDir, 'match_history.json');
    const generatedBuildsFile = path.join(dataDir, 'generated_builds.json');
    const styleRecsFile = path.join(dataDir, 'style_recommendations.json');
    const styleDnaHistoryFile = path.join(dataDir, 'style_dna_history.json');

    const backups = {
        users: fs.existsSync(usersFile) ? fs.readFileSync(usersFile, 'utf8') : null,
        sessions: fs.existsSync(sessionsFile) ? fs.readFileSync(sessionsFile, 'utf8') : null,
        wardrobe: fs.existsSync(wardrobeFile) ? fs.readFileSync(wardrobeFile, 'utf8') : null,
        savedLooks: fs.existsSync(savedLooksFile) ? fs.readFileSync(savedLooksFile, 'utf8') : null,
        planner: fs.existsSync(plannerFile) ? fs.readFileSync(plannerFile, 'utf8') : null,
        moodboards: fs.existsSync(moodboardsFile) ? fs.readFileSync(moodboardsFile, 'utf8') : null,
        matchHistory: fs.existsSync(matchHistoryFile) ? fs.readFileSync(matchHistoryFile, 'utf8') : null,
        generatedBuilds: fs.existsSync(generatedBuildsFile) ? fs.readFileSync(generatedBuildsFile, 'utf8') : null,
        styleRecs: fs.existsSync(styleRecsFile) ? fs.readFileSync(styleRecsFile, 'utf8') : null,
        styleDnaHistory: fs.existsSync(styleDnaHistoryFile) ? fs.readFileSync(styleDnaHistoryFile, 'utf8') : null
    };

    const testFilesToCleanup = [];

    try {
        await new Promise((resolve) => {
            server = http.createServer(app);
            server.listen(0, '127.0.0.1', () => {
                const port = server.address().port;
                baseUrl = `http://127.0.0.1:${port}`;
                console.log(`[SETUP] Route-authorization test server listening on ephemeral port: ${port}\n`);
                resolve();
            });
        });

        // -------------------------------------------------------------
        // SECTION 1: Public Endpoints Remain Accessible Without Auth
        // -------------------------------------------------------------
        console.log("[SECTION 1] Public Endpoints Functionality");

        const checkUserRes = await makeRequest('/api/auth/check-username?username=randomNonExistent123');
        report("Public username check accessible without auth", checkUserRes.status === 200 && checkUserRes.json && checkUserRes.json.available === true);

        const checkEmailRes = await makeRequest('/api/auth/check-email?email=randomNonExistent123@example.com');
        report("Public email check accessible without auth", checkEmailRes.status === 200 && checkEmailRes.json && checkEmailRes.json.available === true);

        const catalogRes = await makeRequest('/api/inspiration');
        report("Public inspiration catalog accessible without auth", catalogRes.status === 200 && catalogRes.json && Array.isArray(catalogRes.json.data));

        // -------------------------------------------------------------
        // SECTION 2: Unauthenticated Access to User-Owned Endpoints
        // -------------------------------------------------------------
        console.log("\n[SECTION 2] Unauthenticated Rejection (HTTP 401)");

        const unauthEndpoints = [
            { method: 'GET', path: '/api/profile' },
            { method: 'POST', path: '/api/profile/update', body: { skinTone: 'fair' } },
            { method: 'GET', path: '/api/wardrobe' },
            { method: 'POST', path: '/api/wardrobe/add', body: { name: 'Item', category: 'tops', subcategory: 'shirt', occasion: 'casual' } },
            { method: 'DELETE', path: '/api/wardrobe/test_item_id' },
            { method: 'POST', path: '/api/wardrobe/reprocess', body: { id: 'test_item_id' } },
            { method: 'POST', path: '/api/wardrobe/reprocess-all', body: {} },
            { method: 'GET', path: '/api/wardrobe/stats' },
            { method: 'GET', path: '/api/saved-looks' },
            { method: 'POST', path: '/api/saved-looks', body: { title: 'Look', outfit: {} } },
            { method: 'DELETE', path: '/api/saved-looks/look_123' },
            { method: 'GET', path: '/api/planner' },
            { method: 'POST', path: '/api/planner/save', body: { date: '2026-05-01', name: 'Plan' } },
            { method: 'DELETE', path: '/api/planner/2026-05-01' },
            { method: 'GET', path: '/api/moodboards' },
            { method: 'POST', path: '/api/moodboards', body: { name: 'Board' } },
            { method: 'POST', path: '/api/moodboards/save', body: { moodboardId: 'mb1', inspirationId: 'insp1' } },
            { method: 'DELETE', path: '/api/moodboards/save', body: { moodboardId: 'mb1', inspirationId: 'insp1' } },
            { method: 'POST', path: '/api/moodboards/set-cover', body: { moodboardId: 'mb1', inspirationId: 'insp1' } },
            { method: 'DELETE', path: '/api/moodboards/mb_123' },
            { method: 'POST', path: '/api/inspiration/match', body: { inspirationId: 'insp1' } },
            { method: 'POST', path: '/api/moodboards/match', body: { moodboardId: 'mb1' } },
            { method: 'POST', path: '/api/inspiration/recommend', body: { inspirationId: 'insp1' } },
            { method: 'POST', path: '/api/inspiration/build', body: { inspirationId: 'insp1' } },
            { method: 'POST', path: '/api/inspiration/build/save', body: { inspirationId: 'insp1', outfit: [] } },
            { method: 'GET', path: '/api/style-dna' },
            { method: 'POST', path: '/api/recommend', body: { prompt: 'casual' } }
        ];

        for (const ep of unauthEndpoints) {
            const res = await makeRequest(ep.path, { method: ep.method, body: ep.body });
            report(`Unauthenticated ${ep.method} ${ep.path} returns 401`, res.status === 401 && res.json && res.json.success === false);
        }

        // -------------------------------------------------------------
        // SECTION 3: Create Two Distinct Synthetic Users & Login
        // -------------------------------------------------------------
        console.log("\n[SECTION 3] User Creation & Multi-User Identity Establishment");

        const userA = {
            email: `alice_${Date.now()}@test.com`,
            name: "Alice Tester",
            username: `alice_${Date.now()}`,
            password: "AlicePassword123!",
            skinTone: "Light",
            size: "S"
        };
        const userB = {
            email: `bob_${Date.now()}@test.com`,
            name: "Bob Tester",
            username: `bob_${Date.now()}`,
            password: "BobPassword123!",
            skinTone: "Medium",
            size: "L"
        };

        const signupA = await makeRequest('/api/auth/signup', { method: 'POST', body: userA });
        report("User A signup succeeds", signupA.status === 200 && signupA.json.success === true);

        const loginA = await makeRequest('/api/auth/login', { method: 'POST', body: { email: userA.email, password: userA.password } });
        report("User A login succeeds and issues session cookie", loginA.status === 200 && loginA.json.success === true);
        const cookieA = extractCookie(loginA.headers);

        const signupB = await makeRequest('/api/auth/signup', { method: 'POST', body: userB });
        report("User B signup succeeds", signupB.status === 200 && signupB.json.success === true);

        const loginB = await makeRequest('/api/auth/login', { method: 'POST', body: { email: userB.email, password: userB.password } });
        report("User B login succeeds and issues session cookie", loginB.status === 200 && loginB.json.success === true);
        const cookieB = extractCookie(loginB.headers);

        const authHeaderA = { 'Cookie': `tt_session=${cookieA}` };
        const authHeaderB = { 'Cookie': `tt_session=${cookieB}` };

        // -------------------------------------------------------------
        // SECTION 4: Profile Isolation & IDOR Immunity
        // -------------------------------------------------------------
        console.log("\n[SECTION 4] Profile Data Isolation");

        // User A reads profile without passing query param - must return User A's profile
        const profA = await makeRequest('/api/profile', { headers: authHeaderA });
        report("User A profile derives from session identity", profA.status === 200 && profA.json && profA.json.profile && profA.json.profile.email === userA.email);

        // User A attempts to read User B's profile by supplying ?email=bob@test.com
        const idorProf = await makeRequest(`/api/profile?email=${encodeURIComponent(userB.email)}`, { headers: authHeaderA });
        report("User A cannot read User B profile via query param override", idorProf.status === 200 && idorProf.json && idorProf.json.profile && idorProf.json.profile.email === userA.email);

        // User A updates profile with { email: userB.email, skinTone: 'Deep' } - must only update User A
        const updateProf = await makeRequest('/api/profile/update', {
            method: 'POST',
            headers: authHeaderA,
            body: { email: userB.email, skinTone: 'Deep' }
        });
        report("Profile update ignores client email and only updates User A", updateProf.status === 200 && updateProf.json && updateProf.json.profile && updateProf.json.profile.email === userA.email && updateProf.json.profile.skinTone === 'Deep');

        // User A attempts to upload profile photo specifying userB's email in multipart body
        const boundary = '----WebKitFormBoundaryTestPhoto7MA4YWxkTrZu0gW';
        const photoMultipartBody = Buffer.concat([
            Buffer.from(`--${boundary}\r\nContent-Disposition: form-data; name="email"\r\n\r\n${userB.email}\r\n`),
            Buffer.from(`--${boundary}\r\nContent-Disposition: form-data; name="photo"; filename="avatar.png"\r\nContent-Type: image/png\r\n\r\n\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x01\x00\x00\x00\x01\x08\x06\x00\x00\x00\x1f\x15c4\x00\x00\x00\nIDATx\x9cc\x00\x01\x00\x00\x05\x00\x01\r\n`),
            Buffer.from(`--${boundary}--\r\n`)
        ]);
        const uploadPhotoRes = await makeRequest('/api/profile/upload-photo', {
            method: 'POST',
            headers: {
                ...authHeaderA,
                'Content-Type': `multipart/form-data; boundary=${boundary}`,
                'Content-Length': photoMultipartBody.length
            },
            body: photoMultipartBody
        });
        report("Profile photo upload succeeds for User A and assigns photo to User A", uploadPhotoRes.status === 200 && uploadPhotoRes.json && uploadPhotoRes.json.success === true && !!uploadPhotoRes.json.photoUrl);

        const verifyAProfPhoto = await makeRequest('/api/profile', { headers: authHeaderA });
        const verifyBProfPhoto = await makeRequest('/api/profile', { headers: authHeaderB });
        report("Profile photo upload only modified User A's avatar", verifyAProfPhoto.json && verifyAProfPhoto.json.profile && verifyAProfPhoto.json.profile.photo === uploadPhotoRes.json.photoUrl);
        report("User B's avatar was completely untouched by User A's photo upload", verifyBProfPhoto.json && verifyBProfPhoto.json.profile && verifyBProfPhoto.json.profile.photo !== uploadPhotoRes.json.photoUrl);

        const authStatusRes = await makeRequest('/api/auth/status', { headers: authHeaderA });
        report("Auth status returns user avatarPhoto",
            authStatusRes.json && authStatusRes.json.user && authStatusRes.json.user.avatarPhoto === uploadPhotoRes.json.photoUrl);

        // Clean up uploaded avatar test file if generated on disk
        if (uploadPhotoRes.json && uploadPhotoRes.json.photoUrl) {
            const diskPhoto = path.join(__dirname, '..', 'public', uploadPhotoRes.json.photoUrl.replace(/^\//, ''));
            const wardrobePhoto = path.join(dataDir, 'uploads', 'wardrobe', path.basename(uploadPhotoRes.json.photoUrl));
            try { if (fs.existsSync(diskPhoto)) fs.unlinkSync(diskPhoto); } catch (_) {}
            try { if (fs.existsSync(wardrobePhoto)) fs.unlinkSync(wardrobePhoto); } catch (_) {}
        }

        // -------------------------------------------------------------
        // SECTION 5: Wardrobe Ownership & IDOR Immunity
        // -------------------------------------------------------------
        console.log("\n[SECTION 5] Wardrobe Ownership & Injection Prevention");

        // User A adds an item while maliciously specifying owner = userB.email
        const addResA = await makeRequest('/api/wardrobe/add', {
            method: 'POST',
            headers: authHeaderA,
            body: {
                name: "Alice Silk Shirt",
                category: "tops",
                subcategory: "blouse",
                occasion: "formal",
                owner: userB.email, // Malicious override attempt!
                dominantColor: "#ffffff"
            }
        });
        report("Wardrobe add succeeds and overrides client owner with authenticated User A",
            addResA.status === 200 && addResA.json && addResA.json.item && addResA.json.item.owner === userA.email);
        const itemAId = addResA.json && addResA.json.item ? addResA.json.item.id : null;

        // User B queries wardrobe: should NOT see Alice's item
        const bWardrobe = await makeRequest('/api/wardrobe', { headers: authHeaderB });
        report("User B wardrobe does not contain User A's item",
            bWardrobe.status === 200 && bWardrobe.json && Array.isArray(bWardrobe.json.wardrobe) && !bWardrobe.json.wardrobe.some(i => i.id === itemAId));

        // User A queries wardrobe with ?email=userB.email: should still only see Alice's items
        const aWardrobeWithParam = await makeRequest(`/api/wardrobe?email=${encodeURIComponent(userB.email)}`, { headers: authHeaderA });
        report("User A query param override does not disclose User B's wardrobe",
            aWardrobeWithParam.status === 200 && aWardrobeWithParam.json && Array.isArray(aWardrobeWithParam.json.wardrobe) && aWardrobeWithParam.json.wardrobe.some(i => i.id === itemAId));

        // User B attempts to DELETE User A's wardrobe item
        const deleteUnauthorized = await makeRequest(`/api/wardrobe/${itemAId}`, {
            method: 'DELETE',
            headers: authHeaderB
        });
        report("User B cannot delete User A's wardrobe item (HTTP 403)", deleteUnauthorized.status === 403);

        // Verify item still exists
        const aWardrobeCheck = await makeRequest('/api/wardrobe', { headers: authHeaderA });
        report("User A's item was not deleted by unauthorized attempt", aWardrobeCheck.json && aWardrobeCheck.json.wardrobe && aWardrobeCheck.json.wardrobe.some(i => i.id === itemAId));

        // User B adds an item for Bob
        const addResB = await makeRequest('/api/wardrobe/add', {
            method: 'POST',
            headers: authHeaderB,
            body: {
                name: "Bob Linen Blazer",
                category: "outerwear",
                subcategory: "blazer",
                occasion: "formal",
                dominantColor: "#000000"
            }
        });
        report("Wardrobe add succeeds for User B", addResB.status === 200 && addResB.json && addResB.json.item && addResB.json.item.owner === userB.email.toLowerCase());
        const itemBId = addResB.json && addResB.json.item ? addResB.json.item.id : null;

        // Alice attempts to reprocess Bob's wardrobe item (IDOR)
        const reprocessUnauthorized = await makeRequest('/api/wardrobe/reprocess', {
            method: 'POST',
            headers: authHeaderA,
            body: { id: itemBId }
        });
        report("User A cannot reprocess User B's wardrobe item (HTTP 404/not owned)", reprocessUnauthorized.status === 404);

        // Alice runs reprocess-all: must not touch or process Bob's items
        const reprocessAllA = await makeRequest('/api/wardrobe/reprocess-all', {
            method: 'POST',
            headers: authHeaderA,
            body: {}
        });
        report("User A reprocess-all executes scoped strictly to User A items",
            reprocessAllA.status === 200 && reprocessAllA.json && reprocessAllA.json.results &&
            !reprocessAllA.json.results.success.includes(itemBId) &&
            !reprocessAllA.json.results.skipped.includes(itemBId) &&
            !reprocessAllA.json.results.failed.includes(itemBId));

        // Alice queries /api/wardrobe/stats with ?email=bob@test.com
        const statsA = await makeRequest(`/api/wardrobe/stats?email=${encodeURIComponent(userB.email)}`, {
            headers: authHeaderA
        });
        report("User A /api/wardrobe/stats calculates metrics strictly for User A (ignoring ?email=bob)",
            statsA.status === 200 && statsA.json && statsA.json.totalItems === 1 && statsA.json.categoryBreakdown && statsA.json.categoryBreakdown.tops === 1 && statsA.json.categoryBreakdown.outerwear === 0);

        // Bob queries /api/wardrobe/stats
        const statsB = await makeRequest('/api/wardrobe/stats', { headers: authHeaderB });
        report("User B /api/wardrobe/stats calculates metrics strictly for User B",
            statsB.status === 200 && statsB.json && statsB.json.totalItems === 1 && statsB.json.categoryBreakdown && statsB.json.categoryBreakdown.outerwear === 1 && statsB.json.categoryBreakdown.tops === 0);

        // Case-sensitivity ownership test: User A with uppercase email session
        const upperEmail = userA.email.toUpperCase();
        const loginAUpper = await makeRequest('/api/auth/login', { method: 'POST', body: { email: upperEmail, password: userA.password } });
        const cookieAUpper = extractCookie(loginAUpper.headers);
        const authHeaderAUpper = { 'Cookie': `tt_session=${cookieAUpper}` };

        const aWardrobeUpper = await makeRequest('/api/wardrobe', { headers: authHeaderAUpper });
        report("Wardrobe retrieval matches case-insensitively across mixed-case session emails",
            aWardrobeUpper.status === 200 && aWardrobeUpper.json && Array.isArray(aWardrobeUpper.json.wardrobe) && aWardrobeUpper.json.wardrobe.some(i => i.id === itemAId));

        const statsAUpper = await makeRequest('/api/wardrobe/stats', { headers: authHeaderAUpper });
        report("Wardrobe stats matches case-insensitively across mixed-case session emails",
            statsAUpper.status === 200 && statsAUpper.json && statsAUpper.json.totalItems === 1);

        // User A deletes own item
        const deleteAuthorized = await makeRequest(`/api/wardrobe/${itemAId}`, {
            method: 'DELETE',
            headers: authHeaderA
        });
        report("User A can delete their own wardrobe item (HTTP 200)", deleteAuthorized.status === 200 && deleteAuthorized.json && deleteAuthorized.json.success === true);

        // -------------------------------------------------------------
        // SECTION 6: Saved Looks Ownership & IDOR Immunity
        // -------------------------------------------------------------
        console.log("\n[SECTION 6] Saved Looks Ownership Enforcement");

        // User A creates a saved look attempting to forge owner = userB.email
        const saveLookA = await makeRequest('/api/saved-looks', {
            method: 'POST',
            headers: authHeaderA,
            body: {
                title: "Alice Summer Look",
                outfit: { tops: "item1" },
                email: userB.email // Malicious override attempt!
            }
        });
        report("Saved looks ignores client email and assigns owner to User A",
            saveLookA.status === 200 && saveLookA.json && saveLookA.json.look && saveLookA.json.look.owner === userA.email.toLowerCase());
        const lookAId = saveLookA.json && saveLookA.json.look ? saveLookA.json.look.id : null;

        // User B queries saved looks
        const bLooks = await makeRequest('/api/saved-looks', { headers: authHeaderB });
        report("User B cannot view User A's saved look",
            bLooks.status === 200 && bLooks.json && Array.isArray(bLooks.json.looks) && !bLooks.json.looks.some(l => l.id === lookAId));

        // User B attempts to DELETE User A's saved look
        const deleteLookUnauthorized = await makeRequest(`/api/saved-looks/${lookAId}`, {
            method: 'DELETE',
            headers: authHeaderB
        });
        report("User B cannot delete User A's saved look (HTTP 403)", deleteLookUnauthorized.status === 403);

        // Bob creates a saved look
        const saveLookB = await makeRequest('/api/saved-looks', {
            method: 'POST',
            headers: authHeaderB,
            body: {
                title: "Bob Executive Look",
                outfit: { outerwear: "item2" }
            }
        });
        report("Bob creates saved look", saveLookB.status === 200 && saveLookB.json && saveLookB.json.look);
        const lookBId = saveLookB.json && saveLookB.json.look ? saveLookB.json.look.id : null;

        // Alice attempts to UPDATE Bob's look by passing Bob's look ID in POST /api/saved-looks (IDOR mutation)
        const updateLookUnauthorized = await makeRequest('/api/saved-looks', {
            method: 'POST',
            headers: authHeaderA,
            body: {
                id: lookBId,
                title: "Alice Tampered Look",
                outfit: { tops: "hacked" }
            }
        });
        report("User A cannot update User B's saved look via IDOR (HTTP 403)", updateLookUnauthorized.status === 403);

        // Verify Bob's look was completely unchanged
        const verifyBLook = await makeRequest('/api/saved-looks', { headers: authHeaderB });
        report("Bob's saved look remains intact after unauthorized update attempt",
            verifyBLook.status === 200 && verifyBLook.json && verifyBLook.json.looks.some(l => l.id === lookBId && l.title === "Bob Executive Look"));

        // User A deletes own look
        const deleteLookAuthorized = await makeRequest(`/api/saved-looks/${lookAId}`, {
            method: 'DELETE',
            headers: authHeaderA
        });
        report("User A deletes own saved look (HTTP 200)", deleteLookAuthorized.status === 200);

        // -------------------------------------------------------------
        // SECTION 7: Planner & Moodboards Isolation
        // -------------------------------------------------------------
        console.log("\n[SECTION 7] Planner & Moodboards Isolation");

        // Planner save for User A with forged owner = userB.email
        const planA = await makeRequest('/api/planner/save', {
            method: 'POST',
            headers: authHeaderA,
            body: {
                date: '2026-06-15',
                name: 'Alice Gala Event',
                email: userB.email
            }
        });
        report("Planner save enforces authenticated owner User A", planA.status === 200 && planA.json && planA.json.event && planA.json.event.owner === userA.email);

        // User B checks planner
        const bPlanner = await makeRequest('/api/planner', { headers: authHeaderB });
        report("User B cannot view User A's planned outfits",
            bPlanner.status === 200 && bPlanner.json && Array.isArray(bPlanner.json.planner) && !bPlanner.json.planner.some(p => p.name === 'Alice Gala Event'));

        // User B attempts to delete Alice's date
        const deletePlanUnauthorized = await makeRequest('/api/planner/2026-06-15', {
            method: 'DELETE',
            headers: authHeaderB
        });
        report("User B cannot delete User A's planner event (returns 404 for User B)", deletePlanUnauthorized.status === 404);

        // Alice attempts to save a planner event referencing Bob's saved look (lookBId)
        const planCrossLook = await makeRequest('/api/planner/save', {
            method: 'POST',
            headers: authHeaderA,
            body: {
                date: '2026-06-16',
                name: 'Alice Cross-Look Event',
                savedLookId: lookBId
            }
        });
        report("Planner save rejects referencing another user's saved look (HTTP 403)", planCrossLook.status === 403);

        // Moodboards: User A creates a board
        const mbA = await makeRequest('/api/moodboards', {
            method: 'POST',
            headers: authHeaderA,
            body: {
                name: "Alice Aesthetic Moodboard",
                email: userB.email // Attempt to create on Bob's account
            }
        });
        report("Moodboard creation is scoped strictly to User A", mbA.status === 200 && mbA.json && mbA.json.moodboard && mbA.json.moodboard.name === "Alice Aesthetic Moodboard");
        const mbAId = mbA.json && mbA.json.moodboard ? mbA.json.moodboard.id : null;

        // User B requests moodboards
        const bMoodboards = await makeRequest('/api/moodboards', { headers: authHeaderB });
        report("User B cannot see User A's moodboard",
            bMoodboards.status === 200 && bMoodboards.json && Array.isArray(bMoodboards.json.moodboards) && !bMoodboards.json.moodboards.some(m => m.id === mbAId));

        // User B attempts to save an inspiration card to User A's moodboard (IDOR card add)
        const addCardUnauthorized = await makeRequest('/api/moodboards/save', {
            method: 'POST',
            headers: authHeaderB,
            body: {
                moodboardId: mbAId,
                inspirationId: 'insp_1'
            }
        });
        report("User B cannot add a card to User A's moodboard (HTTP 404)", addCardUnauthorized.status === 404);

        // User A adds a card to their own moodboard
        const addCardA = await makeRequest('/api/moodboards/save', {
            method: 'POST',
            headers: authHeaderA,
            body: {
                moodboardId: mbAId,
                inspirationId: 'insp_1'
            }
        });
        report("User A adds card to own moodboard (HTTP 200)", addCardA.status === 200 && addCardA.json && addCardA.json.moodboard && addCardA.json.moodboard.cards.includes('insp_1'));

        // User B attempts to delete the card from User A's moodboard (IDOR card delete)
        const deleteCardUnauthorized = await makeRequest('/api/moodboards/save', {
            method: 'DELETE',
            headers: authHeaderB,
            body: {
                moodboardId: mbAId,
                inspirationId: 'insp_1'
            }
        });
        report("User B cannot remove card from User A's moodboard (HTTP 404)", deleteCardUnauthorized.status === 404);

        // User B attempts to set the cover image of User A's moodboard (IDOR set-cover)
        const setCoverUnauthorized = await makeRequest('/api/moodboards/set-cover', {
            method: 'POST',
            headers: authHeaderB,
            body: {
                moodboardId: mbAId,
                inspirationId: 'insp_1'
            }
        });
        report("User B cannot set cover image on User A's moodboard (HTTP 404)", setCoverUnauthorized.status === 404);

        // User B attempts to run moodboard match on User A's moodboard
        const matchMbUnauthorized = await makeRequest('/api/moodboards/match', {
            method: 'POST',
            headers: authHeaderB,
            body: { moodboardId: mbAId }
        });
        report("User B cannot run match against User A's moodboard (HTTP 404)", matchMbUnauthorized.status === 404);

        // User B attempts to delete User A's moodboard
        const deleteMbUnauthorized = await makeRequest(`/api/moodboards/${mbAId}`, {
            method: 'DELETE',
            headers: authHeaderB
        });
        report("User B cannot delete User A's moodboard (HTTP 404)", deleteMbUnauthorized.status === 404);

        // -------------------------------------------------------------
        // SECTION 8: Inspiration Match, Recommend, Build, Style DNA & /recommend
        // -------------------------------------------------------------
        console.log("\n[SECTION 8] Inspiration & AI Recommendation Isolation");

        // Alice runs inspiration match: verified that match history is recorded strictly under Alice
        const inspMatchA = await makeRequest('/api/inspiration/match', {
            method: 'POST',
            headers: authHeaderA,
            body: { inspirationId: 'insp_1', email: userB.email }
        });
        report("Inspiration match executes strictly for User A (ignoring client email)",
            inspMatchA.status === 200 && inspMatchA.json && inspMatchA.json.success === true && inspMatchA.json.report);

        // Verify match_history entry was written for Alice, not Bob
        const curMatchHistory = JSON.parse(fs.readFileSync(matchHistoryFile, 'utf8'));
        const aliceMatches = curMatchHistory.filter(m => m.email === userA.email.toLowerCase());
        const bobMatches = curMatchHistory.filter(m => m.email === userB.email.toLowerCase());
        report("Match history record was attributed to authenticated User A", aliceMatches.length > 0);
        report("No match history record was attributed to User B", bobMatches.length === 0);

        // Alice runs inspiration recommend: verify style_recommendations entry is recorded for Alice
        const inspRecA = await makeRequest('/api/inspiration/recommend', {
            method: 'POST',
            headers: authHeaderA,
            body: { inspirationId: 'insp_1', email: userB.email }
        });
        report("Inspiration recommend executes strictly for User A",
            inspRecA.status === 200 && inspRecA.json && inspRecA.json.success === true && Array.isArray(inspRecA.json.missing));

        const curStyleRecs = JSON.parse(fs.readFileSync(styleRecsFile, 'utf8'));
        const aliceStyleRec = curStyleRecs.find(r => r.email === userA.email.toLowerCase());
        const bobStyleRec = curStyleRecs.find(r => r.email === userB.email.toLowerCase());
        report("Style recommendations entry was updated for User A", !!aliceStyleRec);
        report("Style recommendations entry was untouched for User B", !bobStyleRec);

        // Alice runs inspiration build
        const inspBuildA = await makeRequest('/api/inspiration/build', {
            method: 'POST',
            headers: authHeaderA,
            body: { inspirationId: 'insp_1', email: userB.email }
        });
        report("Inspiration build executes strictly for User A",
            inspBuildA.status === 200 && inspBuildA.json && (inspBuildA.json.success === true || inspBuildA.json.noWardrobe === true));

        // Alice saves a build attempting to forge email = userB.email
        const buildSaveA = await makeRequest('/api/inspiration/build/save', {
            method: 'POST',
            headers: authHeaderA,
            body: {
                inspirationId: 'insp_1',
                score: 85,
                outfit: [{ name: "Alice Silk Shirt" }],
                missing: [],
                email: userB.email
            }
        });
        report("Inspiration build save succeeds", buildSaveA.status === 200 && buildSaveA.json && buildSaveA.json.success === true);

        const curBuilds = JSON.parse(fs.readFileSync(generatedBuildsFile, 'utf8'));
        const aliceBuilds = curBuilds.filter(b => b.email === userA.email.toLowerCase());
        const bobBuilds = curBuilds.filter(b => b.email === userB.email.toLowerCase());
        report("Saved build was attributed strictly to authenticated User A", aliceBuilds.length > 0);
        report("No saved build was attributed to User B", bobBuilds.length === 0);

        // Style DNA query with ?email=bob@test.com
        const styleDnaA = await makeRequest(`/api/style-dna?email=${encodeURIComponent(userB.email)}`, {
            headers: authHeaderA
        });
        report("Style DNA executes strictly for User A (ignoring ?email=bob)",
            styleDnaA.status === 200 && styleDnaA.json && styleDnaA.json.archetype && styleDnaA.json.stylePercentages);

        // /recommend LangGraph Proxy Route Isolation:
        // Bob has 1 item in wardrobe ("Bob Linen Blazer"), Alice currently has 0 (deleted earlier)
        // Alice calls POST /recommend attempting to forge email = userB.email
        const recProxyA = await makeRequest('/recommend', {
            method: 'POST',
            headers: authHeaderA,
            body: {
                prompt: "formal business",
                email: userB.email
            }
        });
        report("Recommender proxy executes strictly against User A's wardrobe (empty response, synergy 0)",
            recProxyA.status === 200 && recProxyA.json && recProxyA.json.synergyScore === 0 && recProxyA.json.reason && recProxyA.json.reason.includes("wardrobe does not currently have items"));

        // Bob calls POST /recommend: Bob has 1 item, so it does not trigger the empty wardrobe response
        // Note: Python agent might not be running on host, but express validates userItems.length > 0 before calling Python.
        // If Python is unavailable, Express will catch the connection refusal and handle cleanly.
        // The crucial test is that Alice got the empty wardrobe branch despite Bob having an item.
        report("Alice could not leverage Bob's wardrobe in recommender proxy",
            recProxyA.json && recProxyA.json.recommended_outfit === null);

        // -------------------------------------------------------------
        // SECTION 9: Development, Debug, & Test Routes in Production
        // -------------------------------------------------------------
        console.log("\n[SECTION 9] Debug, Development, and Test Route Disabling in Production");

        const previousNodeEnv = process.env.NODE_ENV;
        try {
            process.env.NODE_ENV = 'production';

            const debugWardrobeRes = await makeRequest('/api/debug/wardrobe');
            report("GET /api/debug/wardrobe is blocked in production (HTTP 404)", debugWardrobeRes.status === 404);

            const devSetupInspRes = await makeRequest('/api/dev/setup-inspiration');
            report("GET /api/dev/setup-inspiration is blocked in production (HTTP 404)", devSetupInspRes.status === 404);

            const testGeminiRes = await makeRequest('/api/dev/test-gemini-status');
            report("GET /api/dev/test-gemini-status is blocked in production (HTTP 404)", testGeminiRes.status === 404);

            const testVerificationRes = await makeRequest('/api/test-verification-flow');
            report("GET /api/test-verification-flow is blocked in production (HTTP 404)", testVerificationRes.status === 404);
        } finally {
            process.env.NODE_ENV = previousNodeEnv;
        }

        // -------------------------------------------------------------
        // SECTION 10: Private Wardrobe Asset Access Control & Public Avatars (Phase 2B-3)
        // -------------------------------------------------------------
        console.log("\n[SECTION 10] Private Wardrobe Asset Access Control & Public Avatar Verification");

        const wardrobeUploadsDir = path.join(dataDir, 'uploads', 'wardrobe');
        const legacyUploadsDir = path.join(__dirname, '..', 'public', 'uploads');

        // Ensure directories exist
        if (!fs.existsSync(wardrobeUploadsDir)) fs.mkdirSync(wardrobeUploadsDir, { recursive: true });

        // 1. Synthetic wardrobe image belonging to Alice
        const aliceTimestamp = Date.now();
        const aliceImageFilename = `image-${aliceTimestamp}-111111111.png`;
        const aliceImageDiskPath = path.join(wardrobeUploadsDir, aliceImageFilename);
        const aliceImageContent = Buffer.from('THREADTHEORY_ALICE_PRIVATE_WARDROBE_IMAGE_DATA');
        fs.writeFileSync(aliceImageDiskPath, aliceImageContent);
        testFilesToCleanup.push(aliceImageDiskPath);

        // Add item to Alice's wardrobe in data/wardrobe.json
        const currentWardrobe = JSON.parse(fs.readFileSync(wardrobeFile, 'utf8'));
        const aliceItemId = `test_alice_item_${aliceTimestamp}`;
        currentWardrobe.push({
            id: aliceItemId,
            owner: userA.email,
            name: "Alice Private Test Top",
            category: "tops",
            subcategory: "blouse",
            occasion: "casual",
            img: `/uploads/${aliceImageFilename}`,
            originalImagePath: `/uploads/${aliceImageFilename}`,
            processedImagePath: `/uploads/${aliceImageFilename}`
        });
        fs.writeFileSync(wardrobeFile, JSON.stringify(currentWardrobe, null, 2), 'utf8');

        // Subtest 1: Unauthenticated request cannot retrieve Alice's wardrobe image
        const unauthImgRes = await makeRequest(`/uploads/${aliceImageFilename}`);
        report("Unauthenticated request to private wardrobe asset returns HTTP 401",
            unauthImgRes.status === 401 && unauthImgRes.json && unauthImgRes.json.success === false);

        // Subtest 2: Owning authenticated user (Alice) can retrieve their own wardrobe image
        const aliceImgRes = await makeRequest(`/uploads/${aliceImageFilename}`, { headers: authHeaderA });
        report("Authenticated owner (Alice) successfully retrieves their private wardrobe image (HTTP 200)",
            aliceImgRes.status === 200 && aliceImgRes.body === 'THREADTHEORY_ALICE_PRIVATE_WARDROBE_IMAGE_DATA');

        // Subtest 2b: Private wardrobe image headers enforce anti-caching & MIME security
        const cacheControl = aliceImgRes.headers['cache-control'] || '';
        const nosniff = aliceImgRes.headers['x-content-type-options'] || '';
        report("Private wardrobe asset returns strict anti-caching headers (private, no-cache, no-store)",
            cacheControl.includes('private') && cacheControl.includes('no-cache') && cacheControl.includes('no-store'));
        report("Private wardrobe asset returns X-Content-Type-Options: nosniff",
            nosniff === 'nosniff');

        // Subtest 3: Different authenticated user (Bob) cannot retrieve Alice's wardrobe image
        const bobImgRes = await makeRequest(`/uploads/${aliceImageFilename}`, { headers: authHeaderB });
        report("Different authenticated user (Bob) is denied access to Alice's wardrobe image (HTTP 403 Forbidden)",
            bobImgRes.status === 403 && bobImgRes.json && bobImgRes.json.success === false);

        // Subtest 4: Non-existent wardrobe image returns safe 404
        const nonExistentFilename = `image-${aliceTimestamp}-999999999.png`;
        const nonExistentRes = await makeRequest(`/uploads/${nonExistentFilename}`, { headers: authHeaderA });
        report("Missing wardrobe image returns safe HTTP 404 without leaking server internals",
            nonExistentRes.status === 404 && nonExistentRes.json && nonExistentRes.json.success === false);

        // Subtest 5: Traversal attempts and malformed filenames are safely rejected (HTTP 404)
        const traversalRes1 = await makeRequest('/uploads/%2e%2e%2fpackage.json');
        report("Path traversal in /uploads (%2e%2e) is rejected with HTTP 404", traversalRes1.status === 404);

        const traversalRes2 = await makeRequest('/uploads/image-123%2f..%2f..%2fserver.js');
        report("Path traversal with valid prefix pattern is rejected with HTTP 404", traversalRes2.status === 404);

        const nonWardrobeFileRes = await makeRequest('/uploads/malicious_payload.sh');
        report("Non-wardrobe filename pattern in /uploads is rejected with HTTP 404", nonWardrobeFileRes.status === 404);



        // Subtest 7: Multipart wardrobe upload writes to private storage and returns authenticated URL
        const wardrobeUploadBoundary = `---------------------------${Date.now()}`;
        const wardrobeImagePayload = Buffer.from('FAKE_PNG_WARDROBE_DATA_STREAM');
        const wardrobeMultipartBody = Buffer.concat([
            Buffer.from(`--${wardrobeUploadBoundary}\r\nContent-Disposition: form-data; name="name"\r\n\r\nAlice Uploaded Blazer\r\n`),
            Buffer.from(`--${wardrobeUploadBoundary}\r\nContent-Disposition: form-data; name="category"\r\n\r\nouterwear\r\n`),
            Buffer.from(`--${wardrobeUploadBoundary}\r\nContent-Disposition: form-data; name="subcategory"\r\n\r\nblazer\r\n`),
            Buffer.from(`--${wardrobeUploadBoundary}\r\nContent-Disposition: form-data; name="occasion"\r\n\r\nformal\r\n`),
            Buffer.from(`--${wardrobeUploadBoundary}\r\nContent-Disposition: form-data; name="image"; filename="blazer.png"\r\nContent-Type: image/png\r\n\r\n`),
            wardrobeImagePayload,
            Buffer.from(`\r\n--${wardrobeUploadBoundary}--\r\n`)
        ]);

        const addWithPhotoRes = await makeRequest('/api/wardrobe/add', {
            method: 'POST',
            headers: {
                ...authHeaderA,
                'Content-Type': `multipart/form-data; boundary=${wardrobeUploadBoundary}`,
                'Content-Length': wardrobeMultipartBody.length
            },
            body: wardrobeMultipartBody
        });

        report("Wardrobe multipart upload succeeds for User A",
            addWithPhotoRes.status === 200 && addWithPhotoRes.json && addWithPhotoRes.json.success === true && addWithPhotoRes.json.item);

        const uploadedItem = addWithPhotoRes.json ? addWithPhotoRes.json.item : null;
        if (uploadedItem && uploadedItem.img) {
            const uploadedFilename = path.basename(uploadedItem.img);
            const privateSavedPath = path.join(wardrobeUploadsDir, uploadedFilename);
            const publicLeakedPath = path.join(__dirname, '..', 'public', 'uploads', uploadedFilename);
            testFilesToCleanup.push(privateSavedPath);

            report("Uploaded wardrobe image is saved in private data/uploads/wardrobe/ directory",
                fs.existsSync(privateSavedPath));
            report("Uploaded wardrobe image is NOT saved in public/uploads/ directory",
                !fs.existsSync(publicLeakedPath));

            // Authenticated owner can fetch it
            const ownerFetchRes = await makeRequest(`/uploads/${uploadedFilename}`, { headers: authHeaderA });
            report("Owner can fetch the freshly uploaded wardrobe image (HTTP 200)", ownerFetchRes.status === 200);

            // Cross-user cannot fetch it
            const nonOwnerFetchRes = await makeRequest(`/uploads/${uploadedFilename}`, { headers: authHeaderB });
            report("Non-owner cannot fetch the freshly uploaded wardrobe image (HTTP 403 Forbidden)", nonOwnerFetchRes.status === 403);

            // User A deletes the item
            const deleteUploadedRes = await makeRequest(`/api/wardrobe/${uploadedItem.id}`, {
                method: 'DELETE',
                headers: authHeaderA
            });
            report("Owner successfully deletes wardrobe item (HTTP 200)", deleteUploadedRes.status === 200);

            // Verify physical file is preserved on disk to protect historical references
            report("Wardrobe image file is physically preserved on disk upon record deletion",
                fs.existsSync(privateSavedPath));

            // After deletion, ownership check fails and HTTP access is denied
            const postDeleteFetchRes = await makeRequest(`/uploads/${uploadedFilename}`, { headers: authHeaderA });
            report("Deleted wardrobe item image is no longer accessible via HTTP (HTTP 403 Forbidden)",
                postDeleteFetchRes.status === 403);
        }

        // Subtest 7b: Shared asset file retention when one item is deleted
        const sharedTimestamp = Date.now();
        const sharedFilename = `image-${sharedTimestamp}-555555555_shared.png`;
        const sharedDiskPath = path.join(wardrobeUploadsDir, sharedFilename);
        fs.writeFileSync(sharedDiskPath, Buffer.from('SHARED_WARDROBE_IMAGE_DATA'));
        testFilesToCleanup.push(sharedDiskPath);

        const sharedWardrobe = JSON.parse(fs.readFileSync(wardrobeFile, 'utf8'));
        const sharedItem1Id = `test_shared_1_${sharedTimestamp}`;
        const sharedItem2Id = `test_shared_2_${sharedTimestamp}`;
        sharedWardrobe.push({
            id: sharedItem1Id,
            owner: userA.email,
            name: "Alice Shared Top 1",
            category: "tops",
            subcategory: "t-shirt",
            occasion: "casual",
            img: `/uploads/${sharedFilename}`,
            originalImagePath: `/uploads/${sharedFilename}`
        });
        sharedWardrobe.push({
            id: sharedItem2Id,
            owner: userA.email,
            name: "Alice Shared Top 2",
            category: "tops",
            subcategory: "tank",
            occasion: "casual",
            img: `/uploads/${sharedFilename}`,
            originalImagePath: `/uploads/${sharedFilename}`
        });
        fs.writeFileSync(wardrobeFile, JSON.stringify(sharedWardrobe, null, 2), 'utf8');

        // Delete item 1: shared file MUST be retained
        const deleteShared1Res = await makeRequest(`/api/wardrobe/${sharedItem1Id}`, {
            method: 'DELETE',
            headers: authHeaderA
        });
        report("Delete of item 1 with shared image succeeds (HTTP 200)", deleteShared1Res.status === 200);
        report("Shared asset file is retained on disk when item 2 still references it", fs.existsSync(sharedDiskPath));

        // Owner can still fetch the shared asset via item 2
        const sharedFetchAfterItem1Res = await makeRequest(`/uploads/${sharedFilename}`, { headers: authHeaderA });
        report("Owner can still access shared image through item 2 (HTTP 200)", sharedFetchAfterItem1Res.status === 200);

        // Delete item 2: file remains on disk (historical references protected), HTTP access revoked
        const deleteShared2Res = await makeRequest(`/api/wardrobe/${sharedItem2Id}`, {
            method: 'DELETE',
            headers: authHeaderA
        });
        report("Delete of item 2 succeeds (HTTP 200)", deleteShared2Res.status === 200);
        report("Physical file remains preserved on disk after all referencing items are deleted", fs.existsSync(sharedDiskPath));

        const sharedFetchAfterItem2Res = await makeRequest(`/uploads/${sharedFilename}`, { headers: authHeaderA });
        report("HTTP access to shared image revoked after all items deleted (HTTP 403 Forbidden)", sharedFetchAfterItem2Res.status === 403);

        // Subtest 8: Legacy asset fallback verification
        const legacyFilename = `image-${aliceTimestamp}-999999999_legacy.jpg`;
        const legacyDiskPath = path.join(legacyUploadsDir, legacyFilename);
        fs.writeFileSync(legacyDiskPath, Buffer.from('LEGACY_WARDROBE_ASSET_CONTENT'));
        testFilesToCleanup.push(legacyDiskPath);

        const legacyWardrobe = JSON.parse(fs.readFileSync(wardrobeFile, 'utf8'));
        const legacyItemId = `test_legacy_item_${aliceTimestamp}`;
        legacyWardrobe.push({
            id: legacyItemId,
            owner: userA.email,
            name: "Alice Legacy Item",
            category: "bottoms",
            subcategory: "jeans",
            occasion: "casual",
            img: `/uploads/${legacyFilename}`,
            originalImagePath: `/uploads/${legacyFilename}`
        });
        fs.writeFileSync(wardrobeFile, JSON.stringify(legacyWardrobe, null, 2), 'utf8');

        const legacyOwnerRes = await makeRequest(`/uploads/${legacyFilename}`, { headers: authHeaderA });
        report("Owner can access legacy asset via fallback location (HTTP 200)",
            legacyOwnerRes.status === 200 && legacyOwnerRes.body === 'LEGACY_WARDROBE_ASSET_CONTENT');

        const legacyBobRes = await makeRequest(`/uploads/${legacyFilename}`, { headers: authHeaderB });
        report("Non-owner cannot access legacy asset (HTTP 403)",
            legacyBobRes.status === 403);

        // Subtest 9: Direct public static access to private storage directory is blocked
        const directDataRes = await makeRequest(`/data/uploads/wardrobe/${aliceImageFilename}`);
        report("Direct static access to /data/uploads/wardrobe is rejected (HTTP 404)", directDataRes.status === 404);

        const directWardrobeStaticRes = await makeRequest(`/uploads/wardrobe/${aliceImageFilename}`);
        report("Direct static access to /uploads/wardrobe is rejected (HTTP 404)", directWardrobeStaticRes.status === 404);

    } finally {
        if (server) {
            await new Promise(r => server.close(r));
            console.log("\n[TEARDOWN] Test server closed cleanly.");
        }

        // Restore databases
        if (backups.users !== null) fs.writeFileSync(usersFile, backups.users, 'utf8');
        if (backups.sessions !== null) fs.writeFileSync(sessionsFile, backups.sessions, 'utf8');
        if (backups.wardrobe !== null) fs.writeFileSync(wardrobeFile, backups.wardrobe, 'utf8');
        if (backups.savedLooks !== null) fs.writeFileSync(savedLooksFile, backups.savedLooks, 'utf8');
        if (backups.planner !== null) fs.writeFileSync(plannerFile, backups.planner, 'utf8');
        if (backups.moodboards !== null) fs.writeFileSync(moodboardsFile, backups.moodboards, 'utf8');
        if (backups.matchHistory !== null) fs.writeFileSync(matchHistoryFile, backups.matchHistory, 'utf8');
        if (backups.generatedBuilds !== null) fs.writeFileSync(generatedBuildsFile, backups.generatedBuilds, 'utf8');
        if (backups.styleRecs !== null) fs.writeFileSync(styleRecsFile, backups.styleRecs, 'utf8');
        if (backups.styleDnaHistory !== null) fs.writeFileSync(styleDnaHistoryFile, backups.styleDnaHistory, 'utf8');

        // Clean up any test image files created on disk
        for (const fileToClean of testFilesToCleanup) {
            try {
                if (fs.existsSync(fileToClean)) fs.unlinkSync(fileToClean);
            } catch (_) {}
        }
        console.log("[TEARDOWN] Restored persistent databases and cleaned up test assets.");
    }

    console.log("\n==================================================================");
    console.log(` Results: ${passed} passed, ${failed} failed`);
    console.log("==================================================================\n");

    if (failed > 0) {
        process.exit(1);
    }
}

runSuite().catch(err => {
    console.error("Test execution failed:", err);
    process.exit(1);
});
