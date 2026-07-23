#!/usr/bin/env node

/**
 * Baker Street — Sherlock Holmes Analytical Framework installer.
 * Copies the sherlock skill into the platform-specific skills directory.
 *
 * Usage:
 *   npx github:tywinlu1988/Baker-Street                        # Claude Code (default)
 *   npx github:tywinlu1988/Baker-Street --platform codex       # Codex CLI
 *   npx github:tywinlu1988/Baker-Street --platform antigravity # Antigravity
 *   npx github:tywinlu1988/Baker-Street --platform cursor      # Cursor
 *   node install.js --force   # overwrite existing installation
 */

import { copyFileSync, existsSync, mkdirSync, readdirSync, statSync, readFileSync } from 'node:fs';
import { join, dirname } from 'node:path';
import { homedir } from 'node:os';
import { fileURLToPath } from 'node:url';

const __dirname = dirname(fileURLToPath(import.meta.url));
const args = process.argv.slice(2);
const force = args.includes('--force') || args.includes('-f');

// Parse --platform flag
const platformIdx = args.indexOf('--platform');
const platform = platformIdx !== -1 ? args[platformIdx + 1] : 'claude';

// Platform → skill directory mapping
const PLATFORM_DIRS = {
  claude:      join(homedir(), '.claude', 'skills', 'sherlock'),
  codex:       join(homedir(), '.codex', 'skills', 'sherlock'),
  antigravity: join(homedir(), '.antigravity', 'skills', 'sherlock'),
  cursor:      join(homedir(), '.cursor', 'skills', 'sherlock'),
};

// Platform → display names
const PLATFORM_NAMES = {
  claude: 'Claude Code',
  codex: 'Codex CLI',
  antigravity: 'Antigravity',
  cursor: 'Cursor',
};

// Platform → invocation examples
const PLATFORM_USAGE = {
  claude: '  /sherlock "Your question here"',
  codex: '  @sherlock analyze "Your question here"',
  antigravity: '  /analyze --skill sherlock "Your question here"',
  cursor: '  @sherlock "Your question here"',
};

if (!PLATFORM_DIRS[platform]) {
  console.error(`❌ Unknown platform: ${platform}`);
  console.error(`   Supported: ${Object.keys(PLATFORM_DIRS).join(', ')}`);
  process.exit(1);
}

const dest = PLATFORM_DIRS[platform];
const platformName = PLATFORM_NAMES[platform];

// Resolve tool names for this platform
let toolMap = null;
try {
  const toolMapPath = join(__dirname, '.claude', 'skills', 'sherlock', 'tool-map.json');
  if (existsSync(toolMapPath)) {
    toolMap = JSON.parse(readFileSync(toolMapPath, 'utf-8'));
  }
} catch (e) {
  // Tool map not available — use generic names
}

// Look for source skill directory
const src = join(__dirname, '.claude', 'skills', 'sherlock');
if (!existsSync(src)) {
  console.error('❌ Source skill directory not found. Are you running from the Baker-Street package?');
  process.exit(1);
}

if (existsSync(dest) && !force) {
  console.log(`⚠️  sherlock skill already installed at ${dest}`);
  console.log('   Use --force to overwrite: npx github:tywinlu1988/Baker-Street --force');
  process.exit(0);
}

// Recursively copy a directory
function copyDir(srcDir, destDir) {
  if (!existsSync(destDir)) {
    mkdirSync(destDir, { recursive: true });
  }
  for (const entry of readdirSync(srcDir)) {
    const srcPath = join(srcDir, entry);
    const destPath = join(destDir, entry);
    if (statSync(srcPath).isDirectory()) {
      copyDir(srcPath, destPath);
    } else {
      copyFileSync(srcPath, destPath);
    }
  }
}

copyDir(src, dest);

console.log('');
console.log(`🔍 Baker Street v0.5.0 — Sherlock Holmes Analytical Framework`);
console.log('');
console.log(`✅ Installed to ${dest}`);
console.log(`   Platform: ${platformName}`);
if (toolMap && toolMap.platforms[platform]) {
  const mapping = toolMap.platforms[platform];
  console.log(`   Tool mapping: web_search→${mapping.web_search}, run_command→${mapping.run_command}`);
}
console.log('');
console.log('Usage:');
console.log(PLATFORM_USAGE[platform] || '  Consult your platform documentation for skill invocation.');
console.log('');
console.log('The 7 personas are waiting. The game is afoot.');
