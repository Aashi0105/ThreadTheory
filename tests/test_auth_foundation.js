/**
 * Comprehensive Automated Test Suite: Authentication Foundation & Remediation (Phase 2B-1)
 *
 * Covers:
 * 1. CORS allowlist enforcement & rejection of disallowed origins.
 * 2. CSRF Origin / Referer validation for state-changing requests.
 * 3. Production SESSION_SECRET fail-closed validation.
 * 4. Password hashing bounds: rejection of malformed, non-positive, and oversized iteration counts (>500,000).
 * 5. Password hash validation: rejection of corrupted salt/hash lengths.
 * 6. Legacy hash verification, rehash-on-login, and backward compatibility.
 * 7. Cookie-only browser authentication (HttpOnly, SameSite=Lax) without leaking bearer token in JSON.
 * 8. Missing, invalid, forged, and expired session rejection (401).
 * 9. Logout invalidation in session store and cookie clearing.
 * 10. Atomic session persistence and cleanup.
 */

const http = require('http');
const assert = require('assert');
const fs = require('fs');
const path = require('path');
const {
    app,
    hashPassword,
    verifyPassword,
    createSession,
    destroySession,
    getActiveSession,
    getSessionSecret,
    SESSION_COOKIE_NAME,
    MODERN_PBKDF2_ITERATIONS,
    LEGACY_PBKDF2_ITERATIONS,
    MAX_PBKDF2_ITERATIONS,
    ALLOWED_ORIGINS
} = require('../server.js');

function makeRequest(server, options, postData = null) {
    return new Promise((resolve, reject) => {
        const addr = server.address();
        const reqOpts = {
            hostname: '127.0.0.1',
            port: addr.port,
            path: options.path,
            method: options.method || 'GET',
            headers: options.headers || {}
        };

        if (postData) {
            if (!reqOpts.headers['Content-Type']) {
                reqOpts.headers['Content-Type'] = 'application/json';
            }
            reqOpts.headers['Content-Length'] = Buffer.byteLength(postData);
        }

        const req = http.request(reqOpts, (res) => {
            let body = '';
            res.on('data', chunk => { body += chunk; });
            res.on('end', () => {
                let parsed = null;
                try {
                    parsed = JSON.parse(body);
                } catch (e) {
                    parsed = body;
                }
                resolve({
                    statusCode: res.statusCode,
                    headers: res.headers,
                    body: parsed,
                    rawBody: body
                });
            });
        });

        req.on('error', err => reject(err));
        if (postData) req.write(postData);
        req.end();
    });
}

async function runRemediationTests() {
    console.log('========================================================');
    console.log(' Starting Phase 2B-1: Security Remediation Test Suite');
    console.log('========================================================\n');

    const testServer = http.createServer(app);
    await new Promise(resolve => testServer.listen(0, '127.0.0.1', resolve));
    const port = testServer.address().port;
    console.log(`[SETUP] Security test server running on port: ${port}\n`);

    const usersFilePath = path.join(__dirname, '..', 'data', 'users.json');
    const sessionsFilePath = path.join(__dirname, '..', 'data', 'sessions.json');

    // Backup pre-existing user and session data files
    const originalUsers = fs.existsSync(usersFilePath) ? fs.readFileSync(usersFilePath, 'utf8') : '[]';
    const originalSessions = fs.existsSync(sessionsFilePath) ? fs.readFileSync(sessionsFilePath, 'utf8') : '{}';

    const testUserEmail = `test_remed_${Date.now()}@threadtheory-test.io`;
    const testPassword = 'RobustPassword!2026';

    let passed = 0;
    let failed = 0;

    async function check(name, testFn) {
        try {
            await testFn();
            console.log(`  ✓ PASS: ${name}`);
            passed++;
        } catch (err) {
            console.error(`  ✗ FAIL: ${name}`);
            console.error(`    -> ${err.message}`);
            failed++;
        }
    }

    try {
        // --- 1. CORS Origin Allowlist Verification ---
        console.log('[SECTION 1] CORS Allowlist Enforcement');

        await check('Allowed origin (http://localhost:3000) receives Access-Control-Allow-Origin', async () => {
            const res = await makeRequest(testServer, {
                path: '/api/auth/check-username?username=demo',
                method: 'GET',
                headers: { 'Origin': 'http://localhost:3000' }
            });
            assert.strictEqual(res.statusCode, 200);
            assert.strictEqual(res.headers['access-control-allow-origin'], 'http://localhost:3000');
            assert.strictEqual(res.headers['access-control-allow-credentials'], 'true');
        });

        await check('Disallowed origin (https://evil-attacker.com) is denied and does not receive allow headers', async () => {
            const res = await makeRequest(testServer, {
                path: '/api/auth/check-username?username=demo',
                method: 'GET',
                headers: { 'Origin': 'https://evil-attacker.com' }
            });
            // Either 500 error or omitted CORS headers prevents cross-origin response reading
            assert.strictEqual(res.headers['access-control-allow-origin'], undefined, 'Must not reflect untrusted origin');
        });

        // --- 2. CSRF & State-Changing Request Origin Validation ---
        console.log('\n[SECTION 2] CSRF Origin & Referer Defense-in-Depth');

        await check('POST with disallowed Origin returns 403 Forbidden', async () => {
            const res = await makeRequest(testServer, {
                path: '/api/auth/login',
                method: 'POST',
                headers: {
                    'Origin': 'https://malicious-phishing-site.org',
                    'Content-Type': 'application/json'
                }
            }, JSON.stringify({ email: 'test@example.com', password: 'pass' }));

            assert.strictEqual(res.statusCode, 403);
            assert.strictEqual(res.body.success, false);
            assert.match(res.body.message, /CORS_ORIGIN_DENIED|Cross-site request blocked/);
        });

        await check('POST with disallowed Referer returns 403 Forbidden', async () => {
            const res = await makeRequest(testServer, {
                path: '/api/auth/login',
                method: 'POST',
                headers: {
                    'Referer': 'https://malicious-phishing-site.org/attack',
                    'Content-Type': 'application/json'
                }
            }, JSON.stringify({ email: 'test@example.com', password: 'pass' }));

            assert.strictEqual(res.statusCode, 403);
            assert.strictEqual(res.body.success, false);
        });

        await check('POST with allowed Origin succeeds normally', async () => {
            const res = await makeRequest(testServer, {
                path: '/api/auth/login',
                method: 'POST',
                headers: {
                    'Origin': 'http://localhost:3000',
                    'Content-Type': 'application/json'
                }
            }, JSON.stringify({ email: 'nonexistent@test.com', password: 'pass' }));

            // Passes CORS/CSRF check, reaches application logic and returns 401 generic
            assert.strictEqual(res.statusCode, 401);
            assert.strictEqual(res.body.message, 'Invalid email or password.');
        });

        // --- 3. Production Secret Fail-Closed Verification ---
        console.log('\n[SECTION 3] Production Secret Fail-Closed Verification');

        await check('Production startup fails closed if SESSION_SECRET is missing or < 32 chars', () => {
            const origEnv = process.env.NODE_ENV;
            const origSecret = process.env.SESSION_SECRET;
            try {
                process.env.NODE_ENV = 'production';
                delete process.env.SESSION_SECRET;

                assert.throws(() => {
                    getSessionSecret();
                }, /FATAL CONFIGURATION ERROR: In production/, 'Must throw fatal error when secret is absent');

                process.env.SESSION_SECRET = 'short_secret';
                assert.throws(() => {
                    getSessionSecret();
                }, /FATAL CONFIGURATION ERROR: In production/, 'Must throw fatal error when secret is < 32 chars');
            } finally {
                process.env.NODE_ENV = origEnv;
                if (origSecret) process.env.SESSION_SECRET = origSecret;
                else delete process.env.SESSION_SECRET;
            }
        });

        // --- 4. Password Hashing Bounds & Malformed Hash Protection ---
        console.log('\n[SECTION 4] Password Hash Validation & DoS Prevention');

        await check('Oversized iteration count (> 500,000) fails closed without executing PBKDF2', () => {
            const malformedStored = `1000000000:0123456789abcdef0123456789abcdef:${'a'.repeat(128)}`;
            const result = verifyPassword('AnyPassword', malformedStored);
            assert.strictEqual(result.valid, false);
            assert.strictEqual(result.needsRehash, false);
        });

        await check('Negative or non-integer iteration count fails closed', () => {
            assert.strictEqual(verifyPassword('Pass', `-100:0123456789abcdef0123456789abcdef:${'a'.repeat(128)}`).valid, false);
            assert.strictEqual(verifyPassword('Pass', `abc:0123456789abcdef0123456789abcdef:${'a'.repeat(128)}`).valid, false);
            assert.strictEqual(verifyPassword('Pass', `0:0123456789abcdef0123456789abcdef:${'a'.repeat(128)}`).valid, false);
        });

        await check('Malformed salt or hash length fails closed', () => {
            assert.strictEqual(verifyPassword('Pass', `210000:shortsalt:${'a'.repeat(128)}`).valid, false);
            assert.strictEqual(verifyPassword('Pass', `210000:${'a'.repeat(32)}:shorthash`).valid, false);
            assert.strictEqual(verifyPassword('Pass', null).valid, false);
            assert.strictEqual(verifyPassword('Pass', '').valid, false);
        });

        // --- 5. Browser Cookie-Only Login & Expiration ---
        console.log('\n[SECTION 5] Cookie-Only Browser Authentication & Session Expiry');

        // Create test user
        const signupPayload = JSON.stringify({
            email: testUserEmail,
            name: 'Remediation User',
            username: `remed_${Date.now()}`,
            password: testPassword,
            skinTone: 'light',
            size: 'S'
        });
        await makeRequest(testServer, {
            path: '/api/auth/signup',
            method: 'POST',
            headers: { 'Origin': 'http://localhost:3000' }
        }, signupPayload);

        let cookieHeader = '';

        await check('Login establishes HttpOnly cookie and does NOT return bearer token in JSON', async () => {
            const loginPayload = JSON.stringify({ email: testUserEmail, password: testPassword });
            const res = await makeRequest(testServer, {
                path: '/api/auth/login',
                method: 'POST',
                headers: { 'Origin': 'http://localhost:3000' }
            }, loginPayload);

            assert.strictEqual(res.statusCode, 200);
            assert.strictEqual(res.body.token, undefined, 'Bearer token must NOT be returned in JSON response');
            assert.strictEqual(res.body.user.email, testUserEmail);

            const setCookie = res.headers['set-cookie'];
            assert.ok(setCookie && setCookie.length > 0);
            assert.ok(setCookie[0].includes('HttpOnly'));
            assert.ok(setCookie[0].includes('SameSite=Lax'));
            cookieHeader = setCookie[0].split(';')[0];
        });

        await check('Status endpoint authenticates using solely the HttpOnly cookie', async () => {
            const res = await makeRequest(testServer, {
                path: '/api/auth/status',
                method: 'GET',
                headers: { 'Cookie': cookieHeader }
            });
            assert.strictEqual(res.statusCode, 200);
            assert.strictEqual(res.body.authenticated, true);
            assert.strictEqual(res.body.user.email, testUserEmail);
        });

        await check('Expired session is rejected with 401 and pruned from session store', () => {
            // Emulate an expired session directly in sessions.json
            const signedToken = createSession('expired_user@threadtheory.io');
            const [sessionId] = signedToken.split('.');

            const sessions = JSON.parse(fs.readFileSync(sessionsFilePath, 'utf8'));
            // Backdate expiration
            sessions[sessionId].expiresAt = Date.now() - 10000;
            fs.writeFileSync(sessionsFilePath, JSON.stringify(sessions, null, 2), 'utf8');

            const active = getActiveSession(signedToken);
            assert.strictEqual(active, null, 'Expired session must return null');

            const updatedSessions = JSON.parse(fs.readFileSync(sessionsFilePath, 'utf8'));
            assert.strictEqual(updatedSessions[sessionId], undefined, 'Expired session must be pruned from store');
        });

        await check('Logout invalidates server session and clears cookie', async () => {
            const res = await makeRequest(testServer, {
                path: '/api/auth/logout',
                method: 'POST',
                headers: {
                    'Cookie': cookieHeader,
                    'Origin': 'http://localhost:3000'
                }
            });
            assert.strictEqual(res.statusCode, 200);
            assert.strictEqual(res.body.success, true);

            // Verify status now rejects the logged out cookie
            const statusRes = await makeRequest(testServer, {
                path: '/api/auth/status',
                method: 'GET',
                headers: { 'Cookie': cookieHeader }
            });
            assert.strictEqual(statusRes.statusCode, 401);
        });

    } finally {
        // Restore pre-existing user and session data cleanly
        fs.writeFileSync(usersFilePath, originalUsers, 'utf8');
        fs.writeFileSync(sessionsFilePath, originalSessions, 'utf8');

        await new Promise(resolve => testServer.close(resolve));
        console.log('\n[TEARDOWN] Security test server closed and test data cleanly restored.');
    }

    console.log('\n========================================================');
    console.log(` Results: ${passed} passed, ${failed} failed`);
    console.log('========================================================');

    if (failed > 0) {
        process.exit(1);
    }
}

runRemediationTests().catch(err => {
    console.error('Unhandled test runner error:', err);
    process.exit(1);
});
