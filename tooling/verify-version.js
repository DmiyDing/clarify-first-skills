const fs = require('fs');
const path = require('path');

const packageJsonPath = path.join(__dirname, '../package.json');
const skillMdPath = path.join(__dirname, '../clarify-first/SKILL.md');
const changelogPath = path.join(__dirname, '../CHANGELOG.md');
const referencesDir = path.join(__dirname, '../clarify-first/references');

// 1. Get version from package.json
const packageJson = JSON.parse(fs.readFileSync(packageJsonPath, 'utf8'));
const pkgVersion = packageJson.version;
console.log(`package.json version: ${pkgVersion}`);

// 2. Get version from skill.md (frontmatter)
const skillMdContent = fs.readFileSync(skillMdPath, 'utf8');
const skillVersionMatch = skillMdContent.match(/version:\s*([0-9.]+)/);
if (!skillVersionMatch) {
  console.error('Error: Could not find version in clarify-first/SKILL.md frontmatter');
  process.exit(1);
}
const skillVersion = skillVersionMatch[1];
console.log(`skill.md version:     ${skillVersion}`);

// 3. Get version from CHANGELOG.md (first H2)
const changelogContent = fs.readFileSync(changelogPath, 'utf8');
const changelogMatch = changelogContent.match(/## \[([0-9.]+)\]/);
if (!changelogMatch) {
  console.error('Error: Could not find latest version in CHANGELOG.md');
  process.exit(1);
}
const changelogVersion = changelogMatch[1];
console.log(`CHANGELOG.md version: ${changelogVersion}`);

// 4. Check references/ directory for version declarations
console.log('\n📚 Checking references/ directory...');
const referenceFiles = fs.readdirSync(referencesDir)
  .filter(file => file.endsWith('.md'))
  .map(file => path.join(referencesDir, file));

const versionPatterns = [
  /v([0-9]+\.[0-9]+\.[0-9]+)/i,           // v1.2.0
  /version:\s*([0-9]+\.[0-9]+\.[0-9]+)/i, // version: 1.2.0
  /\[([0-9]+\.[0-9]+\.[0-9]+)\]/i,         // [1.2.0]
];

let referenceMismatches = [];

referenceFiles.forEach(filePath => {
  const fileName = path.basename(filePath);
  const content = fs.readFileSync(filePath, 'utf8');
  
  // Check if file contains any version declaration
  let foundVersion = null;
  for (const pattern of versionPatterns) {
    const match = content.match(pattern);
    if (match) {
      foundVersion = match[1];
      break;
    }
  }
  
  if (foundVersion) {
    console.log(`  ${fileName}: Found version ${foundVersion}`);
    if (foundVersion !== pkgVersion) {
      referenceMismatches.push({ file: fileName, version: foundVersion, expected: pkgVersion });
    }
  } else {
    // MANDATORY: All reference files must have version declaration
    console.error(`  ${fileName}: ❌ No version declaration found (MANDATORY)`);
    referenceMismatches.push({ file: fileName, version: null, expected: pkgVersion, error: 'Missing version declaration' });
  }
});

// Compare core versions
if (pkgVersion !== skillVersion || pkgVersion !== changelogVersion) {
  console.error('\n❌ Core version mismatch detected!');
  process.exit(1);
}

// Check reference mismatches
if (referenceMismatches.length > 0) {
  console.error('\n❌ Reference file version issues (MANDATORY):');
  referenceMismatches.forEach(({ file, version, expected, error }) => {
    if (error === 'Missing version declaration') {
      console.error(`  ${file}: ❌ Missing version declaration (expected ${expected})`);
    } else {
      console.error(`  ${file}: Found ${version}, expected ${expected}`);
    }
  });
  console.error('\n💡 Tip: All reference files MUST have version declaration matching the main version.');
  console.error('   Format: "Version: 1.2.0" or "v1.2.0" or "[1.2.0]"');
  process.exit(1); // Exit with error - version declarations are now MANDATORY
}

console.log('\n✅ All core versions match.');
if (referenceMismatches.length === 0) {
  console.log('✅ All reference file versions match (where declared).');
}
process.exit(0);