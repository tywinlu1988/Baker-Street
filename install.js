#!/usr/bin/env node

/**
 * Baker Street — Sherlock Holmes Analytical Framework installer.
 * Copies the sherlock skill into ~/.claude/skills/ so Claude Code can use it.
 *
 * Usage:
 *   npx github:tywinlu1988/Baker-Street       # install to ~/.claude/skills/sherlock
 *   node install.js           # same as above
 *   node install.js --force   # overwrite existing installation
 */

import { copyFileSync, existsSync, mkdirSync, readdirSync, statSync } from 'node:fs';
import { join, dirname } from 'node:path';
import { homedir } from 'node:os';
import { fileURLToPath } from 'node:url';

const __dirname = dirname(fileURLToPath(import.meta.url));
const force = process.argv.includes('--force') || process.argv.includes('-f');

const src = join(__dirname, '.claude', 'skills', 'sherlock');
const dest = join(homedir(), '.claude', 'skills', 'sherlock');

if (!existsSync(src)) {
  console.error('❌ Source skill directory not found. Are you running from the Baker-Street package?');
  process.exit(1);
}

if (existsSync(dest) && !force) {
  console.log('⚠️  sherlock skill already installed at ~/.claude/skills/sherlock');
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
console.log('🔍 Baker Street v0.3.2 — Sherlock Holmes Analytical Framework');
console.log('');
console.log('✅ Installed to ~/.claude/skills/sherlock');
console.log('');
console.log('Usage:');
console.log('  /sherlock "Your question here"');
console.log('  /sherlock --depth deep "Complex analysis"');
console.log('  /sherlock --tldr "Quick answer"');
console.log('');
console.log('The 7 personas are waiting. The game is afoot.');
