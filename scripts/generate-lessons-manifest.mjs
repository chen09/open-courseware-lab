#!/usr/bin/env node

import { readdir, readFile, writeFile } from "node:fs/promises";
import path from "node:path";
import { fileURLToPath } from "node:url";

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);
const repoRoot = path.resolve(__dirname, "..");
const lessonsRoot = path.join(repoRoot, "lessons");
const manifestPath = path.join(lessonsRoot, "manifest.json");

async function walk(dir) {
  const entries = await readdir(dir, { withFileTypes: true });
  const files = [];
  for (const entry of entries) {
    const fullPath = path.join(dir, entry.name);
    if (entry.isDirectory()) {
      files.push(...(await walk(fullPath)));
    } else {
      files.push(fullPath);
    }
  }
  return files;
}

function toWebPath(filePath) {
  return `./${path.relative(repoRoot, filePath).split(path.sep).join("/")}`;
}

async function main() {
  const allFiles = await walk(lessonsRoot);
  const metaFiles = allFiles.filter((f) => path.basename(f) === "meta.json");

  const lessons = [];
  for (const metaFile of metaFiles) {
    const raw = await readFile(metaFile, "utf8");
    const meta = JSON.parse(raw);
    const lessonDir = path.dirname(metaFile);

    lessons.push({
      id: meta.id || "",
      title: meta.title || {},
      subject: meta.subject || "",
      gradeBand: meta.gradeBand || "",
      topic: meta.topic || "",
      slug: meta.slug || path.basename(lessonDir),
      features: Array.isArray(meta.features) ? meta.features : [],
      path: `${toWebPath(lessonDir)}/`,
      entry: meta.entry || "index.html",
      assets: Array.isArray(meta.assets) ? meta.assets : []
    });
  }

  lessons.sort((a, b) => {
    const ka = `${a.subject}/${a.gradeBand}/${a.topic}/${a.slug}`;
    const kb = `${b.subject}/${b.gradeBand}/${b.topic}/${b.slug}`;
    return ka.localeCompare(kb);
  });

  const manifest = {
    generatedAt: new Date().toISOString(),
    count: lessons.length,
    lessons
  };

  await writeFile(manifestPath, `${JSON.stringify(manifest, null, 2)}\n`, "utf8");
  process.stdout.write(`Wrote ${manifestPath} with ${lessons.length} lessons.\n`);
}

main().catch((err) => {
  process.stderr.write(`Failed to generate lessons manifest: ${err.message}\n`);
  process.exit(1);
});
