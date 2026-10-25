/**
 * Regression Test Suite: Static File Exposure & Public Assets Verification
 *
 * Verifies that:
 * 1. Required frontend entry points and public assets remain accessible (HTTP 200).
 * 2. Sensitive files (/server.js, /data/users.json, /data/wardrobe.json, /wardrobe.db, /package.json, /requirements.txt) return HTTP 404.
 * 3. URL-encoded traversal and directory traversal attempts return HTTP 404 / Cannot GET.
 * 4. Existing explicit API routes continue to reach their intended handlers.
 */

const http = require('http');
const assert = require('assert');
const { app } = require('../server.js');

function makeRequest(server, path, method = 'GET') {
    return new Promise((resolve, reject) => {
        const addr = server.address();
        const options = {
            hostname: '127.0.0.1',
            port: addr.port,
            path: path,
            method: method
        };

        const req = http.request(options, (res) => {
            let body = '';
            res.on('data', chunk => { body += chunk; });
            res.on('end', () => {
                resolve({
                    statusCode: res.statusCode,
                    headers: res.headers,
                    body: body
                });
            });
        });

        req.on('error', err => reject(err));
        req.end();
    });
}

async function runTests() {
    console.log('====================================================');
    console.log(' Starting Static File Exposure & Security Regression');
    console.log('====================================================\n');

    // Bind server to an ephemeral test port
    const testServer = http.createServer(app);
    await new Promise((resolve) => {
        testServer.listen(0, '127.0.0.1', resolve);
    });

    const port = testServer.address().port;
    console.log(`[SETUP] Test server listening on ephemeral port: ${port}\n`);

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
        // Group 1: Public Frontend Entry Points Must Be Accessible (HTTP 200)
        console.log('[GROUP 1] Public Frontend Pages Accessibility');
        const allowedPages = [
            '/',
            '/index.html',
            '/studio.html',
            '/closet.html',
            '/calendar.html',
            '/my-looks.html',
            '/inspiration.html',
            '/login.html',
            '/signup.html',
            '/style-dna.html'
        ];

        for (const page of allowedPages) {
            await check(`Route '${page}' returns HTTP 200 with HTML`, async () => {
                const res = await makeRequest(testServer, page);
                assert.strictEqual(res.statusCode, 200, `Expected 200, got ${res.statusCode}`);
                assert.match(res.body, /<!DOCTYPE html>|<html/i, 'Response body should contain HTML markup');
            });
        }

        // Group 2: Public Assets Directory Accessibility
        console.log('\n[GROUP 2] Public Assets Accessibility');
        await check("Static asset '/assets/fashion_moodboard.jpg' returns HTTP 200", async () => {
            const res = await makeRequest(testServer, '/assets/fashion_moodboard.jpg');
            assert.strictEqual(res.statusCode, 200, `Expected 200, got ${res.statusCode}`);
            assert.strictEqual(res.headers['content-type'], 'image/jpeg');
        });

        await check("Static asset '/assets/mannequin_base.png' returns HTTP 200", async () => {
            const res = await makeRequest(testServer, '/assets/mannequin_base.png');
            assert.strictEqual(res.statusCode, 200, `Expected 200, got ${res.statusCode}`);
            assert.strictEqual(res.headers['content-type'], 'image/png');
        });

        // Group 3: Sensitive File Exposure Blocked (HTTP 404)
        console.log('\n[GROUP 3] Sensitive File Access Blocked (HTTP 404)');
        const sensitiveFiles = [
            '/server.js',
            '/package.json',
            '/package-lock.json',
            '/requirements.txt',
            '/vite.config.js',
            '/wardrobe.db',
            '/data/users.json',
            '/data/wardrobe.json',
            '/data/saved_looks.json',
            '/data/planner.json',
            '/data/moodboards.json',
            '/task.md',
            '/validation_batch.md',
            '/api.py',
            '/app.py',
            '/graph.py',
            '/.env',
            '/.env.example'
        ];

        for (const file of sensitiveFiles) {
            await check(`Sensitive path '${file}' returns HTTP 404`, async () => {
                const res = await makeRequest(testServer, file);
                assert.strictEqual(res.statusCode, 404, `Expected 404 for ${file}, but got ${res.statusCode}`);
                assert.doesNotMatch(res.body, /"password"/, `Body must never leak password data`);
                assert.doesNotMatch(res.body, /express\(\)/, `Body must never leak server code`);
            });
        }

        // Group 4: Traversal Attempts Blocked (HTTP 404)
        console.log('\n[GROUP 4] Directory Traversal Variations Blocked (HTTP 404)');
        const traversalAttempts = [
            '/assets/../server.js',
            '/assets/%2e%2e/server.js',
            '/assets/%2e%2e%2fserver.js',
            '/assets/..%2fpackage.json',
            '/assets/%2e%2e%2fdata/users.json',
            '/uploads/../server.js',
            '/uploads/%2e%2e%2f.env',
            '/assets/inspiration/../../server.js',
            '/assets/inspiration/%2e%2e/%2e%2e/server.js'
        ];

        for (const pathAttempt of traversalAttempts) {
            await check(`Traversal attempt '${pathAttempt}' returns HTTP 404`, async () => {
                const res = await makeRequest(testServer, pathAttempt);
                assert.strictEqual(res.statusCode, 404, `Expected 404 for ${pathAttempt}, got ${res.statusCode}`);
                assert.doesNotMatch(res.body, /express\(\)/, `Body must not contain server source`);
            });
        }

        // Group 5: Explicit API Routes Remain Functional
        console.log('\n[GROUP 5] API Route Functionality Preserved');
        await check("API route '/api/auth/check-username' returns 400 when missing query parameter", async () => {
            const res = await makeRequest(testServer, '/api/auth/check-username');
            assert.strictEqual(res.statusCode, 400, `Expected 400, got ${res.statusCode}`);
            const data = JSON.parse(res.body);
            assert.strictEqual(data.success, false);
        });

        await check("API route '/api/inspiration' returns curated dataset", async () => {
            const res = await makeRequest(testServer, '/api/inspiration');
            assert.strictEqual(res.statusCode, 200, `Expected 200, got ${res.statusCode}`);
            const data = JSON.parse(res.body);
            assert.ok(data.success === true, 'Expected success: true');
            assert.ok(Array.isArray(data.data), 'Expected array of cards in data.data');
        });

    } finally {
        await new Promise((resolve) => testServer.close(resolve));
        console.log('\n[TEARDOWN] Test server closed cleanly.');
    }

    console.log('\n====================================================');
    console.log(` Results: ${passed} passed, ${failed} failed`);
    console.log('====================================================');

    if (failed > 0) {
        process.exit(1);
    }
}

runTests().catch(err => {
    console.error('Test run failed with unhandled error:', err);
    process.exit(1);
});
